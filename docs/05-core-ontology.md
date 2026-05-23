# 05 - Core Ontology

> See [README section 5](../README.md#5-core-ontology-design) and [`manufacturing-core.ttl`](../ontologies/core/manufacturing-core.ttl).

The core ontology is the root of the import graph. Every other module
imports it; it imports nothing. It contains only universal abstractions
and the load-bearing relations that downstream modules specialize.

## Class Taxonomy

```text
core:Entity
|-- core:PhysicalEntity
|   |-- core:Resource
|   `-- core:Plant
`-- core:LogicalEntity
    |-- core:Skill
    |-- core:Capability
    |-- core:Process
    |-- core:Product
    |-- core:State
    |-- core:Event
    |-- core:Constraint
    `-- core:ControlComponent
```

`core:PhysicalEntity` is disjoint with `core:LogicalEntity`. The core
also declares disjointness between `core:Skill`, `core:Capability`, and
`core:Process` so the ontology catches boundary violations early.

## Relationship Spine

```turtle
prod:requiresProcess       # Product -> ManufacturingProcess
proc:requiresCapability    # ManufacturingProcess -> Capability
cap:realizedBySkill        # Capability -> Skill
skill:composedOfSkill      # Composite Skill -> constituent Skill
skill:requiresMotion       # Skill -> Motion specification
core:implements            # ControlComponent -> Skill
core:controls              # ControlComponent -> Resource
core:deployedOn            # ControlComponent -> physical controller Resource
core:hasPart / core:partOf # mereological containment
core:canPerform            # inferred: Resource -> Capability
core:canManufacture        # inferred: Plant -> Product
core:hasPlantCapability    # Plant-level capability summary
```

`core:requires` remains only as a deprecated parent property for one
minor-version compatibility window. New data should use the precise
module-level predicates above.

## Inferred Relations

`core:canPerform` is resource-scoped. Do not assert it on `core:Plant`.
Use `core:hasPlantCapability` for plant-level summaries and
`core:canManufacture` for product-level conclusions.
