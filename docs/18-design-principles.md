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
