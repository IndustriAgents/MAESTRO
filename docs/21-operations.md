# 21. Machine Operation Ontology (ISO 14649 / STEP-NC-inspired)

`ontologies/logical/operation.ttl` fills a real gap in the stack. MAESTRO
had a high-level **process** taxonomy (DIN 8580, `process.ttl`) and a
low-level **motion** vocabulary (`motion.ttl`), but nothing in between to
carry the **technology of a machining cycle** — spindle speed, feed rate,
depth of cut. ISO 14649 (STEP-NC) `machining_operation` is exactly that
concept.

## Where it sits

A `MachineOperation` is a **new sibling under `core:LogicalEntity`** — it
is deliberately **not** a subclass of Process, Skill, or Motion. Instead
it *bridges* all three, so nothing is duplicated:

```
proc:ManufacturingProcess   ← op:realizesProcess ─┐
core:Skill                  ← op:requiresSkill ───┤  op:MachineOperation
motion:Motion               ← op:composedOfMotion ┘
```

| Class | ISO 14649 analogue |
|---|---|
| `op:MachineOperation` | `operation` |
| `op:MachiningOperation` | `machining_operation` |
| `op:DrillingOperation` / `MillingOperation` / `TurningOperation` | `drilling` / `milling` / `turning` |
| `op:CuttingParameters` | `machining_technology` |

## Cutting parameters are unit-bearing

Cutting parameters use **`unit:Quantity`**, not unit-suffixed datatype
properties:

```turtle
ex:DrillParams1 a op:CuttingParameters ;
    op:spindleSpeed [ a unit:Quantity ; unit:numericValue 1200.0 ; unit:hasUnit unit:RevolutionPerMinute ] ;
    op:feedRate     [ a unit:Quantity ; unit:numericValue 80.0   ; unit:hasUnit unit:MillimetrePerMinute ] ;
    op:depthOfCut   [ a unit:Quantity ; unit:numericValue 10.0   ; unit:hasUnit unit:Millimetre ] .
```

A property like `spindleSpeedRPM` would repeat the repo's own
*deprecated* `res:payloadKg` anti-pattern; `unit:Quantity` keeps the
machining layer consistent with `res:payload` and QUDT alignment.
`operation.ttl` `owl:imports` `unit.ttl`. New units added in 0.4.0:
`RevolutionPerMinute`, `MillimetrePerMinute`, `MetrePerMinute`.

## Worked example

`examples/drilling-station/machine-operations.ttl`:

```turtle
ex:DrillCycle1 a op:DrillingOperation ;
    op:realizesProcess  ex:DrillHoleProcess ;
    op:requiresSkill    skill-lib:Drill ;
    op:composedOfMotion ex:DrillSpindleMotion , ex:DrillFeedMotion ;
    op:hasCuttingParameters ex:DrillParams1 ;
    op:onTool           ex:DrillBit1 .
```

The spindle and feed motions are typed as the new
`motion:RotationalConstantSpeedMotion` / `LinearConstantSpeedMotion`, so
a planner can rely on the constant-speed assumption.

## Validation & queries

- `constraints/shapes-operation.ttl`: a machining operation must declare
  cutting parameters; the spindle speed must be a positive, unit-bearing
  `unit:Quantity`; (warning) a drill operation should compose ≥2 motions.
- `CQ08` answers "which cutting parameters are defined for each machining
  operation?".

> **Scope.** ISO-14649-*inspired* — it models the operation + cutting
> technology, not the full STEP-NC workingstep/feature/toolpath model.
