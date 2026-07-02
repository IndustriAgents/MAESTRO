# 04 - Standard Alignment

> See [README section 4](../README.md#4-standard-alignment).

Alignment claims in MAESTRO must be backed by explicit bridge axioms.
Prefer:

- `rdfs:subClassOf` when a MAESTRO class narrows an external class.
- `owl:equivalentClass` only when the semantics genuinely match.
- `skos:exactMatch` or `skos:closeMatch` for concept schemes.

## Current Alignment Status

| Module | Standard | Current alignment |
|---|---|---|
| `sensor.ttl` | W3C SSN/SOSA | `sensor:Sensor rdfs:subClassOf sosa:Sensor`; `sensor:Observation rdfs:subClassOf sosa:Observation` |
| `unit.ttl` | QUDT | `unit:Unit rdfs:subClassOf qudt:Unit`; `unit:Quantity rdfs:subClassOf qudt:Quantity` |
| `process.ttl` | DIN 8580 / VDI 3682 | Local process families; formal mappings still needed |
| `skill.ttl` | VDI 2860 | Local skill taxonomy; formal mappings still needed |
| `runtime.ttl` | PackML | Local SKOS state values aligned by label; formal mappings still needed |
| `planning.ttl` | ISA-95 | Local planning classes; formal mappings still needed |
| `aas.ttl` | AAS | Lightweight AAS bridge; full AAS 3.0 Reference/Key model still needed |
| `opcua.ttl` | OPC UA | SkillInterface pattern; companion-spec mappings still needed |
| `recipe.ttl` | ISA-88 (IEC 61512) | `recipe:Recipe rdfs:subClassOf isa88:Procedure`; `recipe:PlanStep rdfs:subClassOf isa88:Phase`. ISA-88 has no single free OWL — `isa88:` is an illustrative placeholder; point a deployment profile at a chosen S88 vocab. |
| `policy.ttl` | ODRL 2.2 | `policy:Policy/Permission/Prohibition rdfs:subClassOf odrl:Policy/Permission/Prohibition`. Full ODRL bundled in `references/odrl22.ttl` (not imported). Role/Mode/Evidence are MAESTRO-local. |
| `prov.ttl` | W3C PROV-O | `runtime:SkillExecution rdfs:subClassOf prov:Activity`; `runtime:executes/hasInput rdfs:subPropertyOf prov:used`; `executedOn → prov:wasAssociatedWith`; `hasTime → prov:atTime`. Full PROV-O in `references/prov-o.ttl` (not imported). |
| `trace.ttl` | ETSI SAREF4INMA | `trace:Item rdfs:subClassOf s4inma:Item`; `trace:Batch rdfs:subClassOf s4inma:Batch`; `trace:producedItem rdfs:subPropertyOf prov:generated`. Full ontology in `references/saref4inma.ttl` (not imported). |
| `dpp.ttl` | DPP (ESPR) / ECLASS | `prod:Feature skos:exactMatch eclass:<IRDI>` (illustrative); `dpp:ProductPassport` is MAESTRO-local. ECLASS dictionary is registration-gated; point a profile at eClassOWL / IEC CDD. |
| `automationml.ttl` | AutomationML / CAEX (IEC 62714) | CAEX is an XSD, not OWL — `aml:InternalElement/ExternalInterface/InternalLink` are MAESTRO-local mirrors; `res:Module rdfs:subClassOf aml:InternalElement`. |
| `dtdl.ttl` | DTDL (Azure Digital Twins) | DTDL is JSON-LD (`dtmi:`), not OWL — `dtdl:Interface rdfs:subClassOf skill:SkillInterface`; `dtdl:Command rdfs:subClassOf com:OperationSignature`; `dtdl:Telemetry rdfs:subClassOf com:EventStream`. |

> Reference copies of the freely-available upstream ontologies (PROV-O, ODRL 2.2,
> SAREF4INMA) are stored under [`references/`](../references/) and are **not** loaded
> into the validated stack — they document the exact upstream IRIs the bridge axioms
> point at, per the import policy below.

## Import Policy

MAESTRO does not import full upstream standard ontologies by default. The
upstream graphs can be large, versioned independently, and sometimes carry
separate licensing or operational assumptions. Instead, MAESTRO declares
small bridge axioms and leaves full imports to deployment profiles that
need them.
