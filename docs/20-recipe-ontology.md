# 20 — Recipe / Plan Ontology (new in 0.4.0 — HHM-Core P2)

> *See [`recipe.ttl`](../ontologies/logical/recipe.ttl) and the priority map in
> [19-hhm-core-bridge.md](19-hhm-core-bridge.md).*

The recipe module adds a neutral, technology-independent **procedural plan** that
sits between the process taxonomy ([`process.ttl`](../ontologies/logical/process.ttl))
and the ISA-95 work orders ([`planning.ttl`](../ontologies/reasoning/planning.ttl)):
an ordered container of `PlanStep`s, each *realised by* a MAESTRO skill.

It is bridged to **ISA-88 (IEC 61512)**. ISA-88 has no single free upstream OWL,
so the `isa88:` namespace is an **illustrative placeholder** — repoint it at a
chosen S88 vocabulary in a deployment profile.

## Class hierarchy

```
core:Process
├── recipe:Recipe              (= isa88:Procedure)
│   └── recipe:ProcessPlan
├── recipe:UnitProcedure       (= isa88:UnitProcedure)
└── recipe:Operation           (= isa88:Operation)
recipe:PlanStep                (= isa88:Phase; subclass of core:LogicalEntity)
```

## Properties

| Property | Domain → Range | Purpose |
|---|---|---|
| `recipe:hasStep` | `Recipe` → `PlanStep` | A recipe contains a plan step |
| `recipe:realizedBy` | `PlanStep` → `core:Skill` | Step-level realization (finer than capability-level `core:realizedBySkill`) |
| `recipe:hasControlFlow` | `PlanStep` → `skill:ControlFlow` | Sequence / parallel / alt / loop / optional (sub-property of `skill:hasControlFlow`) |
| `recipe:hasDataBinding` | `PlanStep` → `skill:DataBinding` | Feeds one step's output into this step's input |
| `recipe:nextStep` | `PlanStep` → `PlanStep` | Sequential successor |
| `recipe:forFeature` | `PlanStep` → `prod:Feature` | The product feature the step produces |
| `recipe:requiresOperation` | `prod:Feature` → `PlanStep` | Inverse of `forFeature` (Feature requires operation) |
| `recipe:hasContext` | `Recipe` → `plan:OperationsDefinition` | Anchors the recipe in its ISA-95 / IEC 62264 MOM context |

## Example

```turtle
ex:WidgetRecipe a recipe:Recipe ;
    core:identifier "recipe-widget-001" ;
    recipe:hasStep ex:Step1 , ex:Step2 .

ex:Step1 a recipe:PlanStep ;
    recipe:realizedBy     skill-lib:MoveLinear ;
    recipe:hasControlFlow ex:Seq1 ;       # ex:Seq1 a skill:Sequence
    recipe:forFeature     ex:Hole1 ;
    recipe:nextStep       ex:Step2 .

ex:Step2 a recipe:PlanStep ;
    recipe:realizedBy     skill-lib:Transfer ;
    recipe:hasDataBinding ex:DB1 .
```

Validated by [`constraints/shapes-recipe.ttl`](../constraints/shapes-recipe.ttl).
A complete instance is in
[`examples/hhm-bridge/plant.ttl`](../examples/hhm-bridge/plant.ttl).
