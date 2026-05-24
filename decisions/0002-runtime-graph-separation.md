# ADR-0002: Runtime state lives in a separate named graph

- **Status:** Accepted
- **Date:** 2026-05-23

## Context

Through 0.2.0, design-time `core:Resource` instances carried `core:hasState
runtime:Available` directly, and `shape:ResourceShape` enforced
`sh:minCount 1` on `core:hasState`. This violated the project's own
"do not mix runtime and design-time" rule: any consumer loading the
design-time graph in isolation failed validation, and any consumer loading
two snapshots simultaneously triggered the "multiple states" warning.

## Decision

Split each example into:

- `plant.ttl` — design-time structure (Plant, Resources, ControlComponents,
  provided Skills, payload/reach, OPC UA interfaces). No `core:hasState`.
- `runtime.ttl` — runtime snapshot. Declares the ontology as
  `runtime:Snapshot`, carries a `runtime:snapshotTaken xsd:dateTime`, and
  asserts `core:hasState` for the live resources.

SHACL shapes split correspondingly:

- `shapes-resource.ttl` — design-time constraints (identifier, payload,
  provided skills, "Plant must not use canPerform").
- `shapes-runtime.ttl` — `sh:targetSubjectsOf core:hasState` so the
  "exactly one current state" warning only fires inside a runtime snapshot.

`runtime:Snapshot` is a new class in `runtime.ttl` (0.3.0) that marks the
graph itself as runtime-bearing. Graph-database operators are expected to
load runtime snapshots into a separate named graph
(`graph/runtime/<plant-id>`) so the design-time graph stays clean.

## Consequences

- Consumers that need both views must load both files (validate_repo.py
  does this by overlaying runtime.ttl onto the design graph).
- The example walk-through documents that the inference rules and the
  cq04 ("resources with state X") competency question run on the runtime
  graph, not the design-time graph.
- A future ADR can extend this pattern to a `Snapshot` taxonomy
  (e.g. `MaintenanceSnapshot`, `EnergySnapshot`) without affecting the
  spine.
