# 06 — Resource Ontology

> *See [README §6](../README.md#6-resource-ontology) · file [`resource.ttl`](../ontologies/physical/resource.ttl).*

`resource.ttl` describes the **physical asset hierarchy** of a plant.

```
core:Resource
├── res:Machine
│   ├── res:Robot
│   │   ├── res:Cobot
│   │   └── res:TransferArm
│   ├── res:AGV
│   ├── res:CNC
│   ├── res:Conveyor
│   ├── res:AssemblyStation
│   └── res:LaserUnit
├── res:Tool
│   ├── res:Gripper
│   ├── res:ToolChanger
│   └── res:VacuumUnit
├── res:Actuator
│   └── res:ServoMotor
└── res:Sensor
    └── res:Camera
```

## The golden rule

> Resources do not contain manufacturing semantics. They only **provide
> skills**, **support motion**, and **expose interfaces**.

This means you will not find `res:WeldRobot` (a function-bearing name)
in MAESTRO. You will find a `res:Robot` that `core:provides skill:Weld`.
The difference matters because:

- A `res:Robot` can re-tool — its skill set changes at runtime.
- `res:WeldRobot` would be wrong the instant the robot picks up a
  different end-effector.

## Common properties

```turtle
res:manufacturer  xsd:string
res:model         xsd:string
res:serialNumber  xsd:string
res:payloadKg     xsd:float
res:reachMm       xsd:float
```

Datasheet-style properties stay here; runtime state lives in
[`runtime.ttl`](../ontologies/runtime/runtime.ttl).
