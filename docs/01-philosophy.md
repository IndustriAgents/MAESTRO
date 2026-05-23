# 01 — Core Philosophy

> *See [README §1](../README.md#1-core-philosophy).*

Traditional manufacturing systems hard-wire **function into machine**:

```
Machine → Function
```

That model dies as soon as you swap a vendor or reconfigure the cell. MAESTRO
inverts the dependency. A factory describes itself in four cleanly
separated layers:

```
Capability
    realized by Skill
        executed by Control System
            controlling Resource
```

The benefit is concrete:

- **Vendor swap.** Replace a Beckhoff PLC with a Siemens one — the Skills
  it implements stay identical; only the `core:ControlComponent` instance
  changes.
- **Multi-vendor cells.** A ROS robot and an IEC 61499 controller can
  share a `skill:Transfer` definition without either party knowing about
  the other.
- **AI orchestration.** An LLM can reason over Capabilities (high-level
  intent) and let SPARQL find the concrete Skills/ControlComponents that
  realise them.

This is the same separation-of-concerns that lets web browsers run any
JavaScript framework — declare the contract once, plug in any
implementation.

## Reading order

1. [§2 — Master architecture](02-master-architecture.md)
2. [§5 — Core ontology](05-core-ontology.md)
3. [§8 — Skill ontology](08-skill-ontology.md) (the keystone)
