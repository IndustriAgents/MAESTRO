# 02 — Master Architecture

> *See [README §2](../README.md#2-master-architecture) and [§25](../README.md#25-final-future-proof-architecture).*

![Semantic Stack](../figures/png/01-semantic-stack.png)

MAESTRO is a **nine-layer semantic stack**. Each layer talks only to the
layer immediately below it, and each layer is replaceable in isolation.

| Layer | Owns |
|---|---|
| Product | What is being made (`prod:Product`, `prod:Part`, `prod:Assembly`). |
| Process | How it is made (DIN 8580 process taxonomy, VDI 3682 sequencing). |
| Capability | What a plant *can do* (`cap:Capability`). |
| Skill | Logical executable behaviour (`skill:AtomicSkill`, `skill:CompositeSkill`). |
| Orchestration | SPARQL / SHACL / CONSTRUCT rules / LLM - the reasoning fabric. |
| Execution | The actual runtime: ROS, IEC 61131, IEC 61499, OPC UA, AAS. |
| Resource | Physical machines, robots, sensors, tools. |
| Motion | Geometric/kinematic primitives (`motion:LinearMotion`, …). |
| Physical Factory | The real-world plant. |

## Why nine layers (and not fewer)

Three boundaries do most of the work:

1. **Capability ↔ Skill.** Capabilities are *what* (vendor-neutral
   intent); Skills are *how* (logical behaviour). Keeping them separate
   makes capability inference a graph-rule problem rather than a code
   problem.
2. **Skill ↔ Execution.** Skills are technology-neutral; ROS/PLCs/FBs
   are technology-specific. Crossing this boundary is what lets MAESTRO
   describe heterogeneous cells.
3. **Resource ↔ Motion.** A robot *is* a resource; its movement *is not*.
   Splitting them makes the motion vocabulary reusable across robots,
   CNCs, and AGVs.

See the final stacked view:

![Final Architecture](../figures/png/06-final-architecture.png)
