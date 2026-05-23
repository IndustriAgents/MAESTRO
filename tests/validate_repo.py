from pathlib import Path

import rdflib
from rdflib.namespace import RDF, RDFS


ROOT = Path(__file__).resolve().parents[1]
CORE = rdflib.Namespace("http://example.org/maestro/core#")
CAP = rdflib.Namespace("http://example.org/maestro/capability#")
EX_TRANSFER = rdflib.Namespace("http://example.org/maestro/examples/transfer-arm#")
EX_ASSEMBLY = rdflib.Namespace("http://example.org/maestro/examples/multi-robot-assembly#")


def parse_all_turtle() -> None:
    for path in sorted(
        list(ROOT.glob("ontologies/**/*.ttl"))
        + list(ROOT.glob("constraints/**/*.ttl"))
        + list(ROOT.glob("examples/**/*.ttl"))
    ):
        graph = rdflib.Graph()
        graph.parse(path, format="turtle")


def load_data_graph() -> rdflib.Graph:
    graph = rdflib.Graph()
    for path in sorted(list(ROOT.glob("ontologies/**/*.ttl")) + list(ROOT.glob("examples/**/*.ttl"))):
        graph.parse(path, format="turtle")
    return graph


def subclass_closure(graph: rdflib.Graph) -> dict[rdflib.term.Node, set[rdflib.term.Node]]:
    parents: dict[rdflib.term.Node, set[rdflib.term.Node]] = {}
    for child, parent in graph.subject_objects(RDFS.subClassOf):
        if isinstance(parent, rdflib.URIRef):
            parents.setdefault(child, set()).add(parent)

    changed = True
    while changed:
        changed = False
        for child, direct in list(parents.items()):
            inherited = set()
            for parent in direct:
                inherited.update(parents.get(parent, set()))
            if not inherited.issubset(direct):
                direct.update(inherited)
                changed = True
    return parents


def instances_of(graph: rdflib.Graph, klass: rdflib.URIRef) -> set[rdflib.term.Node]:
    parents = subclass_closure(graph)
    instances = set()
    for subject, typ in graph.subject_objects(RDF.type):
        if typ == klass or klass in parents.get(typ, set()):
            instances.add(subject)
    return instances


def apply_construct_rules(graph: rdflib.Graph) -> None:
    for path in [ROOT / "rules/capability-inference.rq", ROOT / "rules/manufacturing-ability.rq"]:
        inferred = graph.query(path.read_text(encoding="utf-8"))
        for triple in inferred:
            graph.add(triple)


def assert_query_counts(graph: rdflib.Graph) -> None:
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
        assert len(rows) >= minimum, f"{query_name} returned {len(rows)} rows, expected at least {minimum}"


def assert_competency_questions(graph: rdflib.Graph) -> None:
    pre_materialization_counts = {
        "cq01-available-pick-place.rq": 2,
        "cq02-skill-implementations.rq": 5,
        "cq03-product-capabilities.rq": 1,
        "cq04-resources-without-provided-skills.rq": 2,
    }
    for query_name, minimum in pre_materialization_counts.items():
        query = (ROOT / "queries" / "cq" / query_name).read_text(encoding="utf-8")
        rows = list(graph.query(query))
        assert len(rows) >= minimum, f"{query_name} returned {len(rows)} rows, expected at least {minimum}"


def assert_post_materialization_competency_questions(graph: rdflib.Graph) -> None:
    query = (ROOT / "queries" / "cq" / "cq05-plant-manufacturing-ability.rq").read_text(encoding="utf-8")
    rows = list(graph.query(query))
    assert len(rows) >= 1, "cq05-plant-manufacturing-ability.rq returned no materialized results"


def assert_semantic_spine(graph: rdflib.Graph) -> None:
    direct_requires = list(graph.triples((None, CORE.requires, None)))
    assert not direct_requires, f"core:requires has direct assertions: {direct_requires[:5]}"

    for plant in instances_of(graph, CORE.Plant):
        assert (plant, CORE.identifier, None) in graph, f"Plant lacks core:identifier: {plant}"
        assert (plant, CORE.canPerform, None) not in graph, f"Plant incorrectly uses core:canPerform: {plant}"

    for resource in instances_of(graph, CORE.Resource):
        assert (resource, CORE.identifier, None) in graph, f"Resource lacks core:identifier: {resource}"

    assert (CAP.PickPlaceCapability, RDF.type, CORE.Capability) in graph
    assert (CAP.PickPlaceCapability, CORE.realizedBySkill, None) in graph or any(
        pred for pred in graph.predicates(CAP.PickPlaceCapability, None)
        if (pred, RDFS.subPropertyOf, CORE.realizedBySkill) in graph
    )


def assert_materialized_inference(graph: rdflib.Graph) -> None:
    apply_construct_rules(graph)
    expected_can_perform = {
        (EX_TRANSFER.TransferArm1, CAP.PickPlaceCapability),
        (EX_ASSEMBLY.CobotA, CAP.PickPlaceCapability),
    }
    for triple in expected_can_perform:
        assert (triple[0], CORE.canPerform, triple[1]) in graph, f"Missing inferred canPerform: {triple}"

    assert (EX_TRANSFER.Plant1, CORE.canManufacture, EX_TRANSFER.ProductA) in graph
    assert_post_materialization_competency_questions(graph)


def main() -> None:
    parse_all_turtle()
    graph = load_data_graph()
    assert_query_counts(graph)
    assert_competency_questions(graph)
    assert_semantic_spine(graph)
    assert_materialized_inference(graph)
    print("MAESTRO validation passed")


if __name__ == "__main__":
    main()
