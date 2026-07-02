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

The reusable skill *individuals* — `skill-lib:MoveLinear`, `skill-lib:Transfer`,
`skill-lib:VacuumPick`, … — live in the `skill-lib:` namespace
([`ontologies/lib/skill-lib.ttl`](../ontologies/lib/skill-lib.ttl)) since 0.3.0,
which keeps the `skill:` namespace to vocabulary (classes + properties). See
[`decisions/0003-vocabulary-vs-instances.md`](../decisions/0003-vocabulary-vs-instances.md).

## Composition

Composite skills declare their structure through `skill:composedOfSkill`:

```turtle
skill-lib:Transfer
    a skill:TransferSkill ;
    skill:composedOfSkill skill-lib:MoveLinear ;
    skill:composedOfSkill skill-lib:VacuumPick ;
    skill:composedOfSkill skill-lib:Release .
```

Motion skills point at motion specification individuals through
`skill:requiresMotion`, for example:

```turtle
skill-lib:MoveLinear
    a skill:MotionSkill ;
    skill:requiresMotion motion-lib:LinearMotionSpec .
```

## Skill Metadata

```turtle
skill:hasPrecondition          # -> core:State (shortcut) or reified skill:Precondition
skill:hasPostcondition         # -> core:State (shortcut) or reified skill:Effect / Postcondition
skill:requiresCapability       # -> core:Capability (skill-level, HHM-Core)
skill:expectedDurationSeconds  # xsd:float, deprecated long term in favor of quantity values
```

## Orchestration (new in 0.4.0 — HHM-Core P1)

0.4.0 *reifies* skill composition so that control-flow and data-flow can attach
to each edge, and gives skills typed parameters and a protocol-neutral interface.
`skill:composedOfSkill` stays as the plain shortcut; the reified form is richer.

| Construct | Class / property | Purpose |
|---|---|---|
| Reified link | `skill:SubSkillLink` (`skill:hasSubSkillLink`, `skill:linksTo`) | One composite→constituent edge that can carry control/data flow |
| Control flow | `skill:ControlFlow` → `Sequence` · `Parallel` · `Alternative` · `Loop` · `Optional` (`skill:hasControlFlow`) | Branching/looping/optional operator on a link or `recipe:PlanStep` |
| Data binding | `skill:DataBinding` (`skill:hasDataBinding`, `skill:bindsFrom`, `skill:bindsTo`) | Wires a producing parameter to a consuming parameter |
| Typed parameter | `skill:ParameterDef` (`skill:paramType`, `skill:unitRef`, `skill:minValue`/`maxValue`) + `skill:ParameterValue` (`skill:instanceOf`, `skill:value`) | Typed definition + instance value; typed successor of `skill:hasParameter` |
| Precondition / effect | `skill:Precondition`, `skill:Effect` (≡ `skill:Postcondition`), `skill:refersToState` | Reified conditions over `core:State` |
| Neutral interface | `skill:SkillInterface`, `skill:SkillService` (`skill:hasInterfaceContract`, `skill:exposesInterface`) | Protocol-neutral invocation contract; OPC UA / DTDL / AAS interfaces are subclasses |

```turtle
skill-lib:Transfer
    skill:hasSubSkillLink   ex:Link1 ;
    skill:hasParameterDef   ex:Param1 ;
    skill:hasInterfaceContract ex:TransferIface ;
    skill:requiresCapability cap:TransportCapability .

ex:Link1 a skill:SubSkillLink ;
    skill:linksTo        skill-lib:MoveLinear ;
    skill:hasControlFlow ex:Seq1 .      # ex:Seq1 a skill:Sequence
```

A full worked instance lives in
[`examples/hhm-bridge/plant.ttl`](../examples/hhm-bridge/plant.ttl); see
[19-hhm-core-bridge.md](19-hhm-core-bridge.md) for the priority map.
