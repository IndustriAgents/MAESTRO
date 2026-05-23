# 09 - Capability Ontology

> See [README section 9](../README.md#9-capability-ontology) and [`capability.ttl`](../ontologies/logical/capability.ttl).

A capability is what the plant or a resource can do, expressed at the
level a production manager, MES, planner, or LLM would care about.

MAESTRO now models reusable capabilities as individuals of
`core:Capability`, organized with SKOS. This avoids the previous
class-as-value pattern and makes capability reasoning straightforward in
SPARQL and rule engines.

## Capability Scheme

```turtle
cap:PickPlaceCapability
    a core:Capability, skos:Concept ;
    skos:broader cap:HandlingCapability ;
    cap:realizedBySkill skill:Transfer .

cap:TransportCapability
    a core:Capability, skos:Concept ;
    cap:realizedBySkill skill:MoveLinear, skill:MoveJoint .
```

## Granularity Rule

Capabilities must remain high level.

| Good | Bad |
|---|---|
| `cap:TransportCapability` | `cap:MoveCylinderLeftCapability` |
| `cap:WeldingCapability` | `cap:RobotABBIRB1200WeldsAlClass5` |

If the name encodes a machine, vendor, axis, or implementation detail, it
belongs in a skill, resource, or adapter module, not in the capability
scheme.

## Capability To Skill Binding

Use `cap:realizedBySkill`, a subproperty of `core:realizedBySkill`.
Do not encode the binding as an anonymous OWL restriction unless the
project deliberately switches back to class-expression reasoning.
