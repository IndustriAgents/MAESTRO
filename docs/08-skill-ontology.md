# 08 - Skill Ontology

> See [README section 8](../README.md#8-skill-ontology) and [`skill.ttl`](../ontologies/logical/skill.ttl).

Skills are reusable logical behavior specifications. They are not ROS
nodes, PLC function blocks, IEC 61499 function blocks, or OPC UA methods.
Execution technologies implement skills.

## Class Hierarchy

```text
core:Skill
|-- skill:AtomicSkill
|   |-- skill:MotionSkill
|   |-- skill:ManipulationSkill
|   |-- skill:HandlingSkill
|   `-- skill:InspectionSkill
`-- skill:CompositeSkill
    |-- skill:AssemblySkill
    |-- skill:WeldingSkill
    |-- skill:CoordinationSkill
    |-- skill:ProcessSkill
    `-- skill:TransferSkill
```

The reusable skill entries, such as `skill:MoveLinear` and
`skill:Transfer`, are individuals of these classes. This keeps them
directly queryable from SPARQL and rule engines.

## Composition

Composite skills declare their structure through `skill:composedOfSkill`:

```turtle
skill:Transfer
    a skill:TransferSkill ;
    skill:composedOfSkill skill:MoveLinear ;
    skill:composedOfSkill skill:VacuumPick ;
    skill:composedOfSkill skill:Release .
```

Motion skills point at motion specification individuals through
`skill:requiresMotion`, for example:

```turtle
skill:MoveLinear
    a skill:MotionSkill ;
    skill:requiresMotion motion:LinearMotionSpec .
```

## Skill Metadata

```turtle
skill:hasPrecondition          # -> core:State
skill:hasPostcondition         # -> core:State
skill:hasParameter             # -> open parameter node
skill:expectedDurationSeconds  # xsd:float, deprecated long term in favor of quantity values
```
