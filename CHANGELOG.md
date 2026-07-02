# Changelog

All notable changes to MAESTRO will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-06-24

Closes the gaps identified in the MAESTRO vs. HHM-Core ontology comparison.
Absorbs the missing HHM-Core classes/edges and aligns to the named standards
using MAESTRO's bridge-axiom convention (small `rdfs:subClassOf` / `skos:exactMatch`
to upstream IRIs; no heavy upstream imports in the loaded stack). All additions
are backward-compatible — no terms were removed or renamed.

### Added

- **Skill orchestration (HHM-Core P1)** in `logical/skill.ttl`: reified
  `skill:SubSkillLink`, `skill:ControlFlow` (Sequence/Parallel/Alternative/Loop/Optional),
  `skill:DataBinding`, typed `skill:ParameterDef` + `skill:ParameterValue`,
  `skill:Precondition`/`skill:Effect` classes, and a protocol-neutral
  `skill:SkillInterface` + `skill:SkillService`.
- **Recipe / plan layer (P2)** — new `logical/recipe.ttl` (`recipe:`): `recipe:Recipe`,
  `recipe:ProcessPlan`, `recipe:UnitProcedure`, `recipe:Operation`, `recipe:PlanStep`,
  with `hasStep` / `realizedBy` / `hasControlFlow` / `hasDataBinding` / `nextStep` /
  `forFeature`. Bridged to **ISA-88 (IEC 61512)**.
- **Policy / access control / modes (P3)** — new `cross-cutting/policy.ttl` (`policy:`):
  `Policy`, `Permission`, `Prohibition`, `Role`, `Mode` (auto/manual/maintenance),
  `Evidence`. Bridged to **ODRL 2.2**. Plus `safety:Mitigation` (+ `increases`/`reduces`)
  and the additive `core:constrains` property.
- **Product identity & traceability (P4)** in `logical/product.ttl`:
  `prod:ProductType`/`ProductInstance`, `prod:Variant`, `prod:Requirement`,
  multi-scheme `prod:Identifier` (GTIN/UUID/IRDI/IRI) and structured `prod:BOMNode`.
  New `cross-cutting/dpp.ttl` (`dpp:`) adds a Digital Product Passport view and an
  **ECLASS** dictionary alignment for `aas:semanticId`.
- **Execution provenance (P5)** in `runtime/runtime.ttl`: `runtime:SkillExecution`
  and `runtime:TimeInterval`. New `execution/prov.ttl` aligns SkillExecution to
  **W3C PROV-O** (`prov:Activity`); new `execution/trace.ttl` adds **SAREF4INMA**
  batch/item traceability.
- **Invocation completeness (P6)**: `com:Binding`, `com:OperationSignature`,
  `com:EventStream` in `cross-cutting/communication.ttl`; `res:Module` in
  `physical/resource.ttl`; new `physical/automationml.ttl` (CAEX / IEC 62714) and
  `execution/dtdl.ttl` (Azure Digital Twins DTDL). `opcua:OpcUaSkillInterface` is now
  a subclass of `skill:SkillInterface`.
- New SHACL shapes `constraints/shapes-recipe.ttl`, `shapes-policy.ttl`,
  `shapes-product.ttl`, and extensions to `shapes-skill.ttl` / `shapes-runtime.ttl`,
  all wired into `tests/validate_repo.py`.
- New worked example `examples/hhm-bridge/` (design-time `plant.ttl` + runtime
  `runtime.ttl`) exercising every new module.
- Reference copies of the freely-available upstream ontologies under `references/`:
  `prov-o.ttl`, `odrl22.ttl`, `saref4inma.ttl` (reference only — not imported).
- Full HHM-Core edge coverage: `skill:requiresCapability` (skill-level), the
  `skill:Postcondition` alias of `skill:Effect`, `sensor:hasObservationEvidence`
  (Skill→SOSA Observation), `recipe:requiresOperation` (Feature→PlanStep) and
  `recipe:hasContext` (Recipe→ISA-95), `com:exposedVia` (SkillInterface→Endpoint)
  and `com:DtdlProtocol`, and `aas:publishesInterface` (Submodel→SkillInterface).
  `com:usesProtocol` and `skill:hasPrecondition`/`hasPostcondition` ranges were
  widened so endpoints and reified conditions are valid targets.

### Changed

- Version bumped to `0.4.0` across the umbrella and every edited/new module.
- `examples/distribution-station/plant.ttl`: added `res:payload` to `TransferArm1`
  (fixes a pre-existing SHACL violation so the full suite validates).

## [0.3.0] - 2026-05-23

### BREAKING

- **Namespace migration.** Every IRI moved from `http://example.org/maestro/*`
  (W3C-reserved example domain) to `https://w3id.org/maestro/*`. Run
  `rules/migrate-0.2-to-0.3.rq` plus a textual `example.org → w3id.org`
  rewrite on any existing graph. See `decisions/0001-namespace.md`.
- **Class renames** to remove cross-module local-name collisions
  (`decisions/0004-collision-rename.md`):
  - `iec61499:Resource` → `iec61499:RuntimeResource`
  - `iec61499:Event` → `iec61499:ExecutionEvent` (now `rdfs:subClassOf core:Event`)
  - `iec61499:Device` is now `rdfs:subClassOf core:Resource`
  - `res:Sensor` and `res:Camera` removed; use `sensor:Sensor` / `sensor:VisionSensor`
  - `iec61499:hostsResource` → `iec61499:hostsRuntimeResource`
- **Vocabulary / instance split** (`decisions/0003-vocabulary-vs-instances.md`):
  - `skill:Transfer`, `skill:MoveLinear`, `skill:MoveJoint`, `skill:VacuumPick`,
    `skill:Release` moved to new `skill-lib:` namespace under
    `ontologies/lib/skill-lib.ttl`.
  - `motion:LinearMotionSpec`, `motion:JointMotionSpec`,
    `motion:CartesianMotionSpec` moved to new `motion-lib:` namespace under
    `ontologies/lib/motion-lib.ttl`.
- **Runtime separation** (`decisions/0002-runtime-graph-separation.md`):
  Examples split into `plant.ttl` (design-time) + `runtime.ttl` (snapshot).
  `shape:ResourceShape` no longer requires `core:hasState`; runtime
  constraints moved to `shapes-runtime.ttl` and target `sh:targetSubjectsOf
  core:hasState` instead of every `core:Resource`.
- **Deprecated `core:requires` removed.** Subproperties
  (`core:requiresCapability`, `core:realizedBySkill`, `core:composedOfSkill`,
  `core:requiresMotion`) no longer have a `rdfs:subPropertyOf core:requires`.
  `prod:requiresProcess` also dropped the subProperty assertion.

### Added

- `core:hosts`, `core:emits`, `core:consumes` — promoted from IEC 61499 so
  every adapter can share the same shape.
- `core:providedBy`, `core:implementedBy` — explicit inverses with typed
  domain/range.
- `core:hasPart owl:TransitiveProperty`; `core:partOf owl:TransitiveProperty`.
- `core:connectedTo owl:SymmetricProperty`.
- `core:identifier` is now `owl:FunctionalProperty` and
  `owl:InverseFunctionalProperty`.
- Every universal `core:*` object property carries explicit `rdfs:domain`
  and `rdfs:range`.
- `skill:AtomicSkill owl:disjointWith skill:CompositeSkill`.
- `iec61499:FunctionBlock owl:disjointWith plc:FunctionBlock`.
- `runtime:Snapshot` class and `runtime:snapshotTaken` datatype property.
- `prod:mass` (unit-bearing) replaces the deprecated `prod:massKg`.
- `ontologies/lib/skill-lib.ttl` and `ontologies/lib/motion-lib.ttl`.
- `examples/transfer-arm/runtime.ttl` and
  `examples/multi-robot-assembly/runtime.ttl`.
- `decisions/` ADR folder (0001–0004) documenting breaking decisions.
- `rules/migrate-0.2-to-0.3.rq` — SPARQL UPDATE migration script.
- `unit:*` individuals now carry `owl:sameAs` links to QUDT units
  (`qudt-unit:M`, `qudt-unit:KiloGM`, …).
- `sensor:Observation rdfs:subClassOf core:Event` (was orphaned before).
- Every module declares `owl:versionIRI <…/0.3.0>` so consumers can pin a
  release without losing the base IRI.

### Changed

- `shapes-resource.ttl` rewritten: `sh:maxCount 1` on `core:identifier`,
  `sh:class unit:Quantity` enforced on `res:payload`, `sh:maxCount 0` on
  deprecated `res:payloadKg`. No more `core:hasState` requirement.
- `shapes-runtime.ttl` rewritten with `sh:targetSubjectsOf core:hasState`,
  adds `shape:SnapshotShape`.
- `tests/validate_repo.py` now runs `pyshacl` over both design-time and
  runtime shape sets, validates every `.ttl` parses, every `.rq` parses as
  SPARQL, asserts the spine invariants, runs the SPARQL CONSTRUCT rules
  and verifies the canonical inferences.
- Example plants no longer carry the deprecated `res:payloadKg` /
  `res:reachMm`; only the unit-bearing `res:payload` / `res:reach`.
- `sensor.ttl` removed its shadow SOSA properties
  (`sensor:observes`, `sensor:hasObservation`, `sensor:resultValue`,
  `sensor:resultTime`). Use `sosa:observes`, `sosa:madeObservation`,
  `sosa:hasSimpleResult`, `sosa:resultTime` directly.

### Removed

- `core:requires` (deprecated in 0.2.0).
- `res:Sensor`, `res:Camera`.
- `sensor:observes`, `sensor:hasObservation`, `sensor:resultValue`,
  `sensor:resultTime` (use SOSA).

## [0.2.0] - 2026-05-23

### Changed
- Replaced direct `core:requires` modeling with precise spine relations:
  `proc:requiresCapability`, `cap:realizedBySkill`,
  `skill:composedOfSkill`, and `skill:requiresMotion`.
- Refactored capabilities into queryable `core:Capability` individuals
  organized with SKOS instead of OWL class restrictions.
- Refactored runtime states into canonical `core:State` individuals.
- Split physical controller hardware from logical `core:ControlComponent`
  modeling.
- Replaced illustrative capability/manufacturing inference with executable
  SPARQL CONSTRUCT rules.

### Added
- Core disjointness axioms and `core:partOf`, `core:deployedOn`, and
  `core:hasPlantCapability`.
- Repository validation script and GitHub Actions workflow.
- Competency question documentation and SPARQL query pack.
- Explicit quantity-value hooks for robot payload and reach.

### Deprecated
- Direct use of `core:requires`.
- Unit-suffixed robot properties `res:payloadKg` and `res:reachMm`.

## [0.1.0] - 2026-05-23

### Added
- Initial public release of the MAESTRO ontology stack.
- Core abstractions: `core:Entity`, `core:PhysicalEntity`, `core:LogicalEntity`,
  `core:Resource`, `core:Skill`, `core:Capability`, `core:Process`,
  `core:Product`, `core:ControlComponent`, `core:Plant`.
- Physical ontologies: `resource.ttl`, `motion.ttl`.
- Logical ontologies: `skill.ttl`, `capability.ttl`, `process.ttl`,
  `product.ttl`.
- Execution adapters: `iec61131.ttl`, `iec61499.ttl`, `ros.ttl`,
  `opcua.ttl`, `aas.ttl`.
- Runtime + state vocabularies aligned with PackML.
- Cross-cutting modules: `sensor.ttl` (SSN/SOSA), `unit.ttl` (QUDT),
  `communication.ttl`, `safety.ttl` (IEC 61508), `quality.ttl` (ISO 9001),
  `maintenance.ttl`, `energy.ttl`.
- Reasoning + planning ontologies (ISA-95 aligned).
- Top-level umbrella ontology `maestro.ttl` importing all modules.
- SHACL constraint shapes under `constraints/`.
- SWRL inference rules under `rules/`.
- Example SPARQL queries under `queries/`.
- Two example plants under `examples/` (TransferArm, Multi-Robot-Assembly).
- Seven PlantUML architecture diagrams under `figures/src/`.
- Ten matplotlib-rendered architecture figures under `figures/png/`
  (publication-quality; figures 08-10 styled after the CaSkMan paper).
- `figures/scripts/render_figures.py` — single-file matplotlib renderer.
- Eighteen documentation pages under `docs/` mapping to the 25 README
  sections, plus glossary.
- CaSkMan reference ontology preserved under `references/caskman.ttl`.
