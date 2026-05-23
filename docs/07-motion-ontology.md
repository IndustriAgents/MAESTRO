# 07 — Motion Ontology

> *See [README §7](../README.md#7-motion-ontology) · file [`motion.ttl`](../ontologies/physical/motion.ttl).*

Motion semantics are **machine-independent**. The same `motion:LinearMotion`
applies whether the actuator is a robot end-effector, a CNC tool head, or
an AGV.

## Class hierarchy

```
motion:Motion
├── motion:LinearMotion
├── motion:RotationalMotion
├── motion:JointMotion
├── motion:CartesianMotion
├── motion:SynchronizedMotion
├── motion:TrajectoryMotion
└── motion:ForceControlledMotion
```

## Why this module must stay independent

> Motion MUST remain independent from ROS, PLCs, and IEC 61499.

If `motion:LinearMotion` referenced a ROS `moveit_msgs/PoseStamped`, the
whole stack would inherit a ROS dependency. Instead, the motion module
declares **abstract geometric kinematics** (velocity, acceleration,
precision, frames, axes). It is each *execution adapter's* job to map
those concepts into the runtime types of its protocol.

## Common properties

```turtle
motion:hasVelocity      xsd:float    # m/s or rad/s
motion:hasAcceleration  xsd:float
motion:hasPrecision     xsd:float    # mm
motion:hasCoordinateFrame motion:CoordinateFrame
motion:requiresAxis     motion:Axis
motion:numberOfAxes     xsd:integer
```
