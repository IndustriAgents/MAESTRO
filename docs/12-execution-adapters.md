# 12 — Execution Adapters (ROS · IEC 61131 · IEC 61499 · OPC UA)

> *See README [§12](../README.md#12-ros-ontology), [§13](../README.md#13-iec-61131-ontology), [§14](../README.md#14-iec-61499-ontology), [§15](../README.md#15-opc-ua-ontology).*

Five execution adapters live under `ontologies/execution/`. Each one:

1. Declares its native control-component class (`ros:ROSNode`,
   `plc:FunctionBlock`, `iec61499:BasicFB`, `opcua:OpcUaMethod`,
   `aas:Operation`).
2. Provides `*:implementsSkill` (subPropertyOf `core:implements`) and
   `*:controlsResource` (subPropertyOf `core:controls`).
3. Adds protocol-specific metadata (NodeId, ROS distribution, FB
   language, …).

## ROS / ROS 2

| Class | Purpose |
|---|---|
| `ros:ROSNode` | Generic node |
| `ros:ROSTopic` | Pub/sub channel |
| `ros:ROSService` | Request/response |
| `ros:ROSAction` | Long-running goal |
| `ros:TFFrame` | A frame on `/tf` |
| `ros:MoveItController` | MoveIt motion planner node |

Bridging properties: `ros:implementsSkill`, `ros:controlsResource`,
`ros:publishes`, `ros:subscribes`, `ros:advertisesAction`,
`ros:advertisesService`. Distribution captured via `ros:rosVersion`
(`"humble"`, `"iron"`, `"jazzy"`).

## IEC 61131-3 (classical PLCs)

| Class | Purpose |
|---|---|
| `plc:PLCProgram` | Top-level program |
| `plc:FunctionBlock` | FB instance |
| `plc:Function` | Pure function |
| `plc:Task` | Cyclic / event-driven task |
| `plc:Variable` | Tag |

Five language individuals are pre-declared: `plc:LadderLogic`,
`plc:StructuredText`, `plc:FunctionBlockDiagram`,
`plc:SequentialFunctionChart`, `plc:InstructionList`.

## IEC 61499 (event-driven distributed automation)

| Class | Purpose |
|---|---|
| `iec61499:BasicFB` | Basic FB defined by an ECC |
| `iec61499:CompositeFB` | FB network |
| `iec61499:ServiceInterfaceFB` | Wraps a non-IEC interface |
| `iec61499:Application` | Distributed application |
| `iec61499:Device` | Physical compute host |
| `iec61499:Resource` | Runtime within a Device |

Event semantics: `iec61499:emitsEvent`, `iec61499:consumesEvent`.

## OPC UA

The OPC UA adapter is patterned after [CaSkMan](https://github.com/CaSkade-Automation/CaSkMan).
Skills are exposed network-wide through `opcua:OpcUaSkillInterface`:

```turtle
ex:OpcUaTransferInterface a opcua:OpcUaSkillInterface ;
    opcua:nodeId "ns=2;s=Skill.Transfer" ;
    opcua:browseName "TransferSkill" ;
    opcua:exposes skill:Transfer .
```

The inverse `opcua:accessibleThrough` lets clients ask: *"how do I
invoke `skill:Transfer` over the wire?"*

## Why five adapters, not one universal one

Each protocol has runtime semantics that cannot be flattened into a
universal vocabulary without losing fidelity (ROS topics ≠ OPC UA
variables ≠ IEC 61499 events). Sharing `core:implements` and
`core:controls` is enough to unify the *capability* layer; the
*execution* layer keeps each adapter's native concepts intact.
