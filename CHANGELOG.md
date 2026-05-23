# Changelog

All notable changes to MAESTRO will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
