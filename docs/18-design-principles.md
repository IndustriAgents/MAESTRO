# 18 — Design Principles

> *See [README §24](../README.md#24-final-design-principles).*

The seven rules below are the ones that decide whether MAESTRO survives
contact with a real plant.

## DO

1. **Keep ontology modular.** One concern, one `.ttl`. Cross-module
   coupling only through `owl:imports` and `rdfs:subPropertyOf core:*`.
2. **Separate logical and physical layers.** A `core:Resource` is
   physical; a `core:Skill` is logical. Never put behaviour into a
   resource class.
3. **Separate capability and execution.** A `cap:Capability` is what; a
   `ros:ROSNode` (or `plc:FunctionBlock`, or `iec61499:CompositeFB`) is
   how.
4. **Align with standards.** Use SSN/SOSA, QUDT, DIN 8580, VDI 2860/3682,
   PackML, ISA-95. Re-inventing vocabulary kills interoperability.
5. **Use semantic reasoning.** OWL2-RL for inheritance, SHACL for
   validation, SPARQL CONSTRUCT for inference, SPARQL SELECT for queries.
6. **Use named graphs.** Design-time, run-time, inference results all
   live in their own graphs (§15).
7. **Use skills as abstraction.** Skills are the keystone; everything
   else clips onto them.

## DO NOT

1. **Tightly couple technologies.** A `skill:Transfer` must never
   `rdfs:subClassOf` something in `ros:` or `iec61499:`.
2. **Encode process logic inside machines.** Process orchestration
   belongs in `process.ttl`, not in a robot's class definition.
3. **Make machine-specific capabilities.** `cap:CobotIRB1200Pick` is a
   smell — `cap:PickPlaceCapability` realised by a skill that the Cobot
   `core:provides` is correct.
4. **Use LLMs as knowledge storage.** Facts live in the graph; the LLM
   only translates between natural language and SPARQL.
5. **Mix runtime and design-time semantics.** A `core:Resource` in
   `graph/resource` is design-time; its `core:hasState` in
   `graph/runtime` is run-time. Do not collapse them.
6. **Mix execution and capability.** Even if a single team owns both,
   keep them in separate modules so future teams can replace one without
   touching the other.

## Stability contract — frozen core vs. extension

MAESTRO is layered so that exactly one tier is invariant and everything that
*does* change is isolated from it. Three tiers, from most to least stable:

1. **Frozen core — `core:` (`ontologies/core/manufacturing-core.ttl`).**
   The `core:Entity` taxonomy (`PhysicalEntity`/`LogicalEntity` →
   `Resource`, `Plant`, `Skill`, `Capability`, `Process`, `Product`, `State`,
   `Event`, `Constraint`, `ControlComponent`) and the universal spine
   properties (`hasPart`/`partOf`, `provides`, `implements`, `controls`,
   `realizedBySkill`, `requiresCapability`, `composedOfSkill`, `hasState`,
   `constrains`, `canPerform`, `canManufacture`, …). The core **imports
   nothing** and is the one thing every other file depends on, so it is treated
   as **frozen**: it changes only at a major version, never within a release
   line. Downstream data, rules and queries can rely on it permanently.

2. **MAESTRO modules — `prod:` `res:` `skill:` `cap:` `proc:` `recipe:`
   `policy:` `com:` `runtime:` `safety:` `motion:` `sensor:` …** Each is a
   *stable but versioned extension* that couples to the core **only** through
   `owl:imports` + `rdfs:subClassOf` / `rdfs:subPropertyOf core:*`
   (DO-rule 1). New classes, properties and whole modules are added here as the
   domain grows; one concern can be revised or replaced without touching the
   core or the other modules. These **will keep extending** — that is their job.

3. **External standards — the `«EXT»` extension points.** OPC UA, AAS, DTDL,
   ECLASS/DPP, ISA-88/95, CAEX/AutomationML, QUDT, SOSA/SSN, PROV-O,
   SAREF4INMA, ODRL, … are **always an extension**: they are bridged from an
   *adapter* module via `rdfs:subClassOf` / `skos:exactMatch` and are **never
   absorbed** into the core or a module's own TBox (DO-NOT-rule 1 — a skill must
   never `rdfs:subClassOf` something in `ros:`/`iec61499:`). A new protocol or
   passport scheme is added by writing a new adapter, leaving everything above
   it untouched.

**The contract in one line:** the `core:` spine is permanent; modules extend it;
external standards clip on at the edge. Change always flows *outward* — never
into the core.

The schema figures make this visible: in
[`figures/png/14-maestro-core-schema.png`](../figures/png/14-maestro-core-schema.png)
the frozen `core:` classes are drawn with a **gold double border**, MAESTRO
module classes use the normal cluster fill, and the `«EXT»` note shapes are the
external extension points — with a matching "Stability contract" legend. The
distribution-station example
([`figures/png/15-distribution-newsystem4-schema.png`](../figures/png/15-distribution-newsystem4-schema.png))
uses the same encoding at the instance level (individuals typed by a frozen
`core:` class carry the gold border).
