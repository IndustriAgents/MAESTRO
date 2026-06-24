"""MAESTRO repository validator.

Validates:
1. Every .ttl file parses as Turtle.
2. Every .rq file parses as SPARQL.
3. Design-time SHACL shapes hold over (ontologies + library + design-time examples).
4. Runtime SHACL shapes hold over the runtime snapshots.
5. SPARQL CONSTRUCT rules materialise the canonical inferences.
6. Example SPARQL queries return at least their expected row counts.
7. Competency questions return at least their expected row counts.
"""

from __future__ import annotations

import sys
from pathlib import Path

import rdflib
from rdflib import Graph
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.parser import parseUpdate

try:
    import pyshacl
except ImportError:  # pragma: no cover
    print("pyshacl is required. pip install -r requirements.txt", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
CORE = rdflib.Namespace("https://w3id.org/maestro/core#")
CAP = rdflib.Namespace("https://w3id.org/maestro/capability#")
EX_TRANSFER = rdflib.Namespace("https://w3id.org/maestro/examples/transfer-arm#")
EX_ASSEMBLY = rdflib.Namespace("https://w3id.org/maestro/examples/multi-robot-assembly#")


def ontology_turtle_files() -> list[Path]:
    return sorted(ROOT.glob("ontologies/**/*.ttl"))


def constraint_files() -> list[Path]:
    return sorted(ROOT.glob("constraints/**/*.ttl"))


def example_plant_files() -> list[Path]:
    """Design-time example files (excludes runtime snapshots)."""
    return [p for p in sorted(ROOT.glob("examples/**/*.ttl")) if p.name != "runtime.ttl"]


def example_runtime_files() -> list[Path]:
    return list(sorted(ROOT.glob("examples/**/runtime.ttl")))


def parse_all_turtle() -> None:
    paths = ontology_turtle_files() + constraint_files() + example_plant_files() + example_runtime_files()
    for path in paths:
        g = Graph()
        g.parse(path, format="turtle")


def parse_all_sparql() -> None:
    """Confirm every .rq parses as either a SPARQL query or an UPDATE script."""
    for path in sorted(ROOT.glob("**/*.rq")):
        text = path.read_text(encoding="utf-8")
        try:
            prepareQuery(text)
        except Exception as query_exc:  # noqa: BLE001
            try:
                parseUpdate(text)
            except Exception as update_exc:  # noqa: BLE001
                raise AssertionError(
                    f"SPARQL parse failed for {path}: "
                    f"as query → {query_exc}; as update → {update_exc}"
                ) from update_exc


def load_design_graph() -> Graph:
    g = Graph()
    for p in ontology_turtle_files():
        g.parse(p, format="turtle")
    for p in example_plant_files():
        g.parse(p, format="turtle")
    return g


def load_runtime_graph(design: Graph) -> Graph:
    g = Graph()
    for triple in design:
        g.add(triple)
    for p in example_runtime_files():
        g.parse(p, format="turtle")
    return g


def load_shapes(*paths: Path) -> Graph:
    g = Graph()
    for p in paths:
        g.parse(p, format="turtle")
    return g


SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")


def shacl_validate(data: Graph, shapes: Graph, label: str) -> None:
    """Run SHACL. Fail only on sh:Violation; print sh:Warning / sh:Info."""
    _conforms, results_graph, results_text = pyshacl.validate(
        data_graph=data,
        shacl_graph=shapes,
        inference="rdfs",            # materialise subPropertyOf / subClassOf chains
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
        debug=False,
    )
    violations = []
    warnings = []
    for result in results_graph.subjects(RDF.type, SH.ValidationResult):
        sev = next(iter(results_graph.objects(result, SH.resultSeverity)), SH.Violation)
        focus = next(iter(results_graph.objects(result, SH.focusNode)), None)
        msg = next(iter(results_graph.objects(result, SH.resultMessage)), "")
        entry = (focus, str(msg))
        if sev == SH.Violation:
            violations.append(entry)
        else:
            warnings.append((sev, focus, str(msg)))
    if warnings:
        sys.stdout.write(f"\nSHACL warnings ({label}): {len(warnings)}\n")
        for sev, focus, msg in warnings:
            sys.stdout.write(f"  [{str(sev).rsplit('#', 1)[-1]}] {focus} — {msg}\n")
    if violations:
        sys.stderr.write(f"\nSHACL VIOLATIONS ({label}): {len(violations)}\n{results_text}\n")
        raise AssertionError(f"SHACL validation failed for {label}.")


def apply_construct_rules(graph: Graph) -> None:
    for path in [ROOT / "rules/capability-inference.rq", ROOT / "rules/manufacturing-ability.rq"]:
        inferred = graph.query(path.read_text(encoding="utf-8"))
        for triple in inferred:
            graph.add(triple)


def assert_query_counts(graph: Graph) -> None:
    minimum_counts = {
        "01-resources-with-capability.rq": 2,
        "02-skill-implementations.rq": 5,
        "03-product-process-chain.rq": 1,
        "04-available-resources.rq": 6,
        "05-llm-pipeline-template.rq": 2,
    }
    for query_name, minimum in minimum_counts.items():
        query = (ROOT / "queries" / query_name).read_text(encoding="utf-8")
        rows = list(graph.query(query))
        assert len(rows) >= minimum, (
            f"{query_name} returned {len(rows)} rows, expected at least {minimum}"
        )


def assert_competency_questions_pre_materialization(graph: Graph) -> None:
    minimums = {
        "cq01-available-pick-place.rq": 2,
        "cq02-skill-implementations.rq": 5,
        "cq03-product-capabilities.rq": 1,
        "cq04-resources-without-provided-skills.rq": 1,
    }
    for query_name, minimum in minimums.items():
        query = (ROOT / "queries" / "cq" / query_name).read_text(encoding="utf-8")
        rows = list(graph.query(query))
        assert len(rows) >= minimum, (
            f"{query_name} returned {len(rows)} rows, expected at least {minimum}"
        )


def assert_competency_questions_post_materialization(graph: Graph) -> None:
    query = (ROOT / "queries" / "cq" / "cq05-plant-manufacturing-ability.rq").read_text(encoding="utf-8")
    rows = list(graph.query(query))
    assert len(rows) >= 1, "cq05-plant-manufacturing-ability.rq returned no materialized results"


def assert_semantic_spine(graph: Graph) -> None:
    direct_requires = list(graph.triples((None, CORE.requires, None)))
    assert not direct_requires, (
        f"core:requires has direct assertions (removed in 0.3.0): {direct_requires[:5]}"
    )

    for plant in graph.subjects(RDF.type, CORE.Plant):
        assert (plant, CORE.identifier, None) in graph, f"Plant lacks core:identifier: {plant}"
        assert (plant, CORE.canPerform, None) not in graph, (
            f"Plant incorrectly uses core:canPerform: {plant}"
        )

    # Walk transitive subclass closure of core:Resource.
    resource_classes = {CORE.Resource}
    changed = True
    while changed:
        changed = False
        for sub in list(graph.subjects(RDFS.subClassOf, None)):
            for parent in graph.objects(sub, RDFS.subClassOf):
                if parent in resource_classes and sub not in resource_classes:
                    resource_classes.add(sub)
                    changed = True

    for cls in resource_classes:
        for instance in graph.subjects(RDF.type, cls):
            assert (instance, CORE.identifier, None) in graph, (
                f"Resource lacks core:identifier: {instance}"
            )

    assert (CAP.PickPlaceCapability, RDF.type, CORE.Capability) in graph
    realizes_objs = list(graph.objects(CAP.PickPlaceCapability, CORE.realizedBySkill)) + list(
        graph.objects(
            CAP.PickPlaceCapability,
            rdflib.URIRef("https://w3id.org/maestro/capability#realizedBySkill"),
        )
    )
    assert realizes_objs, "cap:PickPlaceCapability does not resolve to any Skill."


def assert_materialized_inference(graph: Graph) -> None:
    apply_construct_rules(graph)
    expected_can_perform = {
        (EX_TRANSFER.TransferArm1, CAP.PickPlaceCapability),
        (EX_ASSEMBLY.CobotA, CAP.PickPlaceCapability),
    }
    for triple in expected_can_perform:
        assert (triple[0], CORE.canPerform, triple[1]) in graph, (
            f"Missing inferred canPerform: {triple}"
        )
    assert (EX_TRANSFER.Plant1, CORE.canManufacture, EX_TRANSFER.ProductA) in graph, (
        "Plant1 canManufacture ProductA was not materialized."
    )
    assert_competency_questions_post_materialization(graph)


def main() -> None:
    parse_all_turtle()
    parse_all_sparql()

    design = load_design_graph()
    design_shapes = load_shapes(
        ROOT / "constraints/shapes-resource.ttl",
        ROOT / "constraints/shapes-process.ttl",
        ROOT / "constraints/shapes-skill.ttl",
        ROOT / "constraints/shapes-recipe.ttl",
        ROOT / "constraints/shapes-policy.ttl",
        ROOT / "constraints/shapes-product.ttl",
    )
    shacl_validate(design, design_shapes, "design-time")

    runtime = load_runtime_graph(design)
    runtime_shapes = load_shapes(ROOT / "constraints/shapes-runtime.ttl")
    shacl_validate(runtime, runtime_shapes, "runtime")

    assert_semantic_spine(runtime)
    assert_query_counts(runtime)
    assert_competency_questions_pre_materialization(runtime)
    assert_materialized_inference(runtime)

    print("MAESTRO validation passed")


if __name__ == "__main__":
    main()
