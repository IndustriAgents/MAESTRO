# Glossary — IRIs, Prefixes, Abbreviations

## Namespace prefixes

| Prefix | IRI | Module |
|---|---|---|
| `core:` | `https://w3id.org/maestro/core#` | [`manufacturing-core.ttl`](../ontologies/core/manufacturing-core.ttl) |
| `res:` | `https://w3id.org/maestro/resource#` | [`resource.ttl`](../ontologies/physical/resource.ttl) |
| `motion:` | `https://w3id.org/maestro/motion#` | [`motion.ttl`](../ontologies/physical/motion.ttl) |
| `skill:` | `https://w3id.org/maestro/skill#` | [`skill.ttl`](../ontologies/logical/skill.ttl) |
| `cap:` | `https://w3id.org/maestro/capability#` | [`capability.ttl`](../ontologies/logical/capability.ttl) |
| `proc:` | `https://w3id.org/maestro/process#` | [`process.ttl`](../ontologies/logical/process.ttl) |
| `prod:` | `https://w3id.org/maestro/product#` | [`product.ttl`](../ontologies/logical/product.ttl) |
| `plc:` | `https://w3id.org/maestro/iec61131#` | [`iec61131.ttl`](../ontologies/execution/iec61131.ttl) |
| `iec61499:` | `https://w3id.org/maestro/iec61499#` | [`iec61499.ttl`](../ontologies/execution/iec61499.ttl) |
| `ros:` | `https://w3id.org/maestro/ros#` | [`ros.ttl`](../ontologies/execution/ros.ttl) |
| `opcua:` | `https://w3id.org/maestro/opcua#` | [`opcua.ttl`](../ontologies/execution/opcua.ttl) |
| `aas:` | `https://w3id.org/maestro/aas#` | [`aas.ttl`](../ontologies/execution/aas.ttl) |
| `runtime:` | `https://w3id.org/maestro/runtime#` | [`runtime.ttl`](../ontologies/runtime/runtime.ttl) |
| `state:` | `https://w3id.org/maestro/state#` | [`state.ttl`](../ontologies/runtime/state.ttl) |
| `sensor:` | `https://w3id.org/maestro/sensor#` | [`sensor.ttl`](../ontologies/cross-cutting/sensor.ttl) |
| `unit:` | `https://w3id.org/maestro/unit#` | [`unit.ttl`](../ontologies/cross-cutting/unit.ttl) |
| `com:` | `https://w3id.org/maestro/communication#` | [`communication.ttl`](../ontologies/cross-cutting/communication.ttl) |
| `safety:` | `https://w3id.org/maestro/safety#` | [`safety.ttl`](../ontologies/cross-cutting/safety.ttl) |
| `qa:` | `https://w3id.org/maestro/quality#` | [`quality.ttl`](../ontologies/cross-cutting/quality.ttl) |
| `maint:` | `https://w3id.org/maestro/maintenance#` | [`maintenance.ttl`](../ontologies/cross-cutting/maintenance.ttl) |
| `energy:` | `https://w3id.org/maestro/energy#` | [`energy.ttl`](../ontologies/cross-cutting/energy.ttl) |
| `reas:` | `https://w3id.org/maestro/reasoning#` | [`reasoning.ttl`](../ontologies/reasoning/reasoning.ttl) |
| `plan:` | `https://w3id.org/maestro/planning#` | [`planning.ttl`](../ontologies/reasoning/planning.ttl) |
| `recipe:` | `https://w3id.org/maestro/recipe#` | [`recipe.ttl`](../ontologies/logical/recipe.ttl) |
| `policy:` | `https://w3id.org/maestro/policy#` | [`policy.ttl`](../ontologies/cross-cutting/policy.ttl) |
| `dpp:` | `https://w3id.org/maestro/dpp#` | [`dpp.ttl`](../ontologies/cross-cutting/dpp.ttl) |
| `aml:` | `https://w3id.org/maestro/automationml#` | [`automationml.ttl`](../ontologies/physical/automationml.ttl) |
| `dtdl:` | `https://w3id.org/maestro/dtdl#` | [`dtdl.ttl`](../ontologies/execution/dtdl.ttl) |
| `trace:` | `https://w3id.org/maestro/trace#` | [`trace.ttl`](../ontologies/execution/trace.ttl) |
| `mprov:` | `https://w3id.org/maestro/prov#` | [`prov.ttl`](../ontologies/execution/prov.ttl) (datatype timestamp aliases) |
| `shape:` | `https://w3id.org/maestro/shapes#` | [`constraints/`](../constraints/) |

## External prefixes referenced

| Prefix | IRI | Source |
|---|---|---|
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | W3C RDF |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | W3C RDFS |
| `owl:` | `http://www.w3.org/2002/07/owl#` | W3C OWL 2 |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | XML Schema |
| `sh:` | `http://www.w3.org/ns/shacl#` | W3C SHACL |
| `sosa:` | `http://www.w3.org/ns/sosa/` | W3C SOSA |
| `ssn:` | `http://www.w3.org/ns/ssn/` | W3C SSN |
| `qudt:` | `http://qudt.org/schema/qudt/` | QUDT |
| `dct:` | `http://purl.org/dc/terms/` | Dublin Core Terms |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | W3C SKOS |
| `odrl:` | `http://www.w3.org/ns/odrl/2/` | ODRL 2.2 (policy bridge) |
| `prov:` | `http://www.w3.org/ns/prov#` | W3C PROV-O (provenance bridge) |
| `s4inma:` | `https://saref.etsi.org/saref4inma/` | ETSI SAREF4INMA (traceability bridge) |
| `isa88:` | `http://www.example.org/ISA-88#` | ISA-88 / IEC 61512 — **illustrative placeholder**, no single free OWL; repoint in a deployment profile |
| `eclass:` | `https://www.w3id.org/eclass#` | ECLASS dictionary — **illustrative placeholder**; repoint at eClassOWL / IEC CDD |

> `odrl:`, `prov:`, and `s4inma:` are the real upstream IRIs the bridge axioms
> point at; reference copies live under [`references/`](../references/) but are
> **not** imported into the validated stack (see [04-standard-alignment.md](04-standard-alignment.md)).
> `isa88:` and `eclass:` are illustrative placeholders, not loaded ontologies.

## Abbreviations

| Abbr. | Stands for |
|---|---|
| AAS | Asset Administration Shell |
| AGV | Automated Guided Vehicle |
| BOM | Bill of Materials |
| CAEX | Computer Aided Engineering Exchange (IEC 62714 / AutomationML) |
| CNC | Computer Numerical Control |
| DDS | Data Distribution Service |
| DPP | Digital Product Passport (ESPR) |
| DTDL | Digital Twins Definition Language (Azure) |
| ECC | Execution Control Chart (IEC 61499) |
| ECLASS | Cross-industry product/service classification dictionary |
| ESPR | Ecodesign for Sustainable Products Regulation (EU) |
| FB | Function Block |
| FBD | Function Block Diagram (IEC 61131-3) |
| GTIN | Global Trade Item Number |
| IEC | International Electrotechnical Commission |
| IRDI | International Registration Data Identifier |
| ISA-88 | Batch control / procedural model standard (IEC 61512) |
| ISA-95 | Enterprise-Control System Integration standard |
| KPI | Key Performance Indicator |
| MoveIt | ROS motion planning framework |
| MTBF | Mean Time Between Failures |
| ODRL | Open Digital Rights Language (W3C) |
| OEE | Overall Equipment Effectiveness |
| OPC UA | OPC Unified Architecture |
| OWL | Web Ontology Language |
| PackML | Packaging Machine Language |
| PL | Performance Level (ISO 13849) |
| PLC | Programmable Logic Controller |
| PROV-O | Provenance Ontology (W3C) |
| RDF | Resource Description Framework |
| ROS | Robot Operating System |
| SAREF4INMA | SAREF extension for Industry & Manufacturing (ETSI) |
| SFC | Sequential Function Chart |
| SHACL | Shapes Constraint Language |
| SIL | Safety Integrity Level (IEC 61508) |
| SOSA | Sensor, Observation, Sample, and Actuator (W3C) |
| SPARQL | SPARQL Protocol and RDF Query Language |
| SSN | Semantic Sensor Network (W3C) |
| ST | Structured Text (IEC 61131-3) |
| SWRL | Semantic Web Rule Language |
| TF | Transform tree (ROS) |
| VDI | Verein Deutscher Ingenieure |
