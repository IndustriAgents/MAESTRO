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
| `aas.ttl` | AAS | Lightweight, AAS-3.0-*inspired* bridge (submodels, operation variables, modelling kind, twinning); full AAS 3.0 Reference/Key model still needed |
| `opcua.ttl` | OPC UA | SkillInterface pattern; companion-spec mappings still needed |
| `safety.ttl` | IEC 61508 / ISO 13849 | Local SIL/PL/hazard vocabulary; label-level alignment |
| `security.ttl` | IEC 62443 | Local zone/conduit/threat/SL vocabulary; safety/security convergence via `security:triggersHazard`; formal mappings still needed |
| `operation.ttl` | ISO 14649 / STEP-NC | *Inspired-by* operation + cutting-technology model (not the full workingstep/feature/toolpath model); formal mappings still needed |

## Import Policy

MAESTRO does not import full upstream standard ontologies by default. The
upstream graphs can be large, versioned independently, and sometimes carry
separate licensing or operational assumptions. Instead, MAESTRO declares
small bridge axioms and leaves full imports to deployment profiles that
need them.
