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
├── res:ControllerDevice          (res:PLC, res:IndustrialPC)
└── res:Module                    (0.4.0 — reconfigurable plug-and-produce module)
```

> **Sensors moved (0.3.0).** `res:Sensor` and `res:Camera` were removed to drop
> duplicate definitions — use `sensor:Sensor` / `sensor:VisionSensor` (SOSA-aligned,
> and also subclasses of `core:Resource`). See
> [`decisions/0004-collision-rename.md`](../decisions/0004-collision-rename.md).

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
res:payload       → unit:Quantity   # unit-bearing; replaces deprecated res:payloadKg
res:reach         → unit:Quantity   # unit-bearing; replaces deprecated res:reachMm
```

> `res:payloadKg` / `res:reachMm` (bare `xsd:float`) are **deprecated** — use the
> unit-bearing `res:payload` / `res:reach` (`unit:Quantity`).

Datasheet-style properties stay here; runtime state lives in
[`runtime.ttl`](../ontologies/runtime/runtime.ttl).

## Reconfigurable modules & topology (new in 0.4.0 — HHM-Core P6)

`res:Module` is a reconfigurable, plug-and-produce production module (MTP-style).
It is a subclass of both `core:Resource` and `aml:InternalElement`, so it doubles
as the anchor for imported **AutomationML / CAEX** (IEC 62714) plant topology:

```turtle
ex:Station1 a res:Module ;
    core:provides   skill-lib:Transfer ;
    aml:hasInterface ex:Port1 .        # ex:Port1 a aml:ExternalInterface
```

The topology mirror — `aml:InternalElement`, `aml:ExternalInterface`,
`aml:InternalLink` with `aml:hasInterface` / `aml:linksInterface` — lives in
[`physical/automationml.ttl`](../ontologies/physical/automationml.ttl). CAEX is an
XML schema, not OWL, so these are MAESTRO-local mirrors.
