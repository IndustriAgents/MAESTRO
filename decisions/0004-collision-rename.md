# ADR-0004: Resolve cross-module class-name collisions

- **Status:** Accepted
- **Date:** 2026-05-23

## Context

Through 0.2.0, the following local-name collisions lived in the codebase:

| Conflicting local names | Modules | Different concept? |
|---|---|---|
| `Resource` | `core:`, `iec61499:` | Yes (physical asset vs IEC 61499 runtime resource) |
| `Event` | `core:`, `iec61499:` | Yes (point-in-time occurrence vs FB execution event) |
| `FunctionBlock` | `plc:`, `iec61499:` | Yes (IEC 61131 FB vs IEC 61499 FB) |
| `Sensor` | `res:`, `sensor:` | No (duplicate of the same concept) |
| `Observation` | `res:` (none) / `sensor:` (SOSA-aligned) | n/a |

Each collision relied on prefix disambiguation, which works in SPARQL but
fails as a documentation and onboarding strategy. Comments warned readers
not to confuse the two, which is exactly the smell that signals an
unresolved design problem.

## Decision

- **Rename** the colliding IEC 61499 classes:
  - `iec61499:Resource` → `iec61499:RuntimeResource`
  - `iec61499:Event`    → `iec61499:ExecutionEvent` (now `rdfs:subClassOf core:Event`)
- **Declare disjointness** between the two FunctionBlock classes:
  `iec61499:FunctionBlock owl:disjointWith plc:FunctionBlock`.
- **Remove** the duplicates from `resource.ttl`:
  - `res:Sensor` → deleted (use `sensor:Sensor`).
  - `res:Camera` → deleted (use `sensor:VisionSensor`).
- **Re-align** `iec61499:Device rdfs:subClassOf core:Resource` so a physical
  61499 device shows up under the same Resource taxonomy as
  `res:ControllerDevice`.
- **Promote** shared semantics to `core:` so adapters do not invent
  parallel names: `core:hosts`, `core:emits`, `core:consumes`. IEC 61499's
  `hostsResource`, `emitsEvent`, `consumesEvent` are now subproperties.

## Consequences

- Breaking change for any consumer that referenced
  `iec61499:Resource`/`iec61499:Event`. The migration script rewrites these.
- SHACL/OWL reasoners will now flag any individual asserted as both
  `plc:FunctionBlock` and `iec61499:FunctionBlock` (which was a latent bug
  before).
- The SOSA-aligned sensor model is the single source of truth for sensor
  classes; downstream consumers federating with SOSA-native graphs no
  longer need bridge rules for the basic types.
