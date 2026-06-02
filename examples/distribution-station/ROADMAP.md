# MAESTRO — Validation Roadmap

**Author:** Melwin Xavier
**Date:** 2026-05-28
**Status:** Draft for review (Spindox handover)

This roadmap tracks the **validation milestones** of the MAESTRO ontology
framework against Festo MPS reference stations. Milestone numbers
(M1 / M2 / M3) are independent of the code release version
(`vX.Y.Z` in `CHANGELOG.md`).

| Milestone | Station | Example files | New ontology modules exercised | Query class enabled |
|---|---|---|---|---|
| **M1 (v.0.1)** | Distributing Station | 3 (`plant.ttl`, `product.ttl`, `runtime.ttl`) | core, resource, motion, skill, capability, process, product, skill-lib, motion-lib, iec61499, opcua, sensor, unit, runtime, state, reasoning (16 base modules imported via `maestro.ttl`) | **Basic feasibility** — `core:canManufacture`, `core:canPerform` |
| **M2 (v.0.2)** | Distributing Station | 3 + `motion-process.ttl` + `security.ttl` | + extended `motion.ttl` (constant-speed sub-classes), `safety.ttl` instances | **Queries with time** — cycle-time estimation, scheduling, SIL-aware filtering |
| **M3 (v.0.3)** | **Drilling Station** | 5 (`plant`, `product`, `runtime`, `digital-twin`, `machine-operations`) | + `aas.ttl` instances, extended motion-operations vocabulary | **Gap identification** — find missing capabilities for a requested process |

---

## M1 — Distributing Station, basic feasibility *(largely complete)*

### Deliverables already in the repository

- `examples/distribution-station/plant.ttl` — 523 triples, mechatronic
  topology, skill TYPES, IEC 61499 FBTs, OPC UA interface.
- `examples/distribution-station/product.ttl` — `WorkpieceWP3` + 5-step
  `DistributeWorkpieceProcess`.
- `examples/distribution-station/runtime.ttl` — PackML-aligned snapshot.
- `rules/capability-inference-ds.rq` — DS-specific bridge rule (joins
  resource-side skill TYPES with library-side skills through their shared
  semantic class).
- `examples/distribution-station/distribution-station-explainer.md` —
  end-to-end walk-through of the live GraphDB session (5 568 triples,
  OWL2-RL + 2 SPARQL CONSTRUCT rules).

### Headline reasoning chain (verified live)

```
ex:DistributingStation1 core:canManufacture ex:WorkpieceWP3 .
```

### To close M1

- [ ] Git tag `v0.1-roadmap-m1` on the current `usecase_festo` branch.
- [ ] One-page README in `examples/distribution-station/` listing which
      modules are loaded and how to reproduce the GraphDB session.
- [ ] Share the explainer + 3 TTL files + bridge rule with Spindox.

---

## M2 — Distributing Station + Motion-with-time + Security

### Goals

Extend the M1 model so that the orchestrator can answer **time-aware**
questions: *"how long does it take to manufacture WP3 right now?"*,
*"which capabilities are SIL-rated for use with workpiece WP3?"*.

### Ontology additions

1. **Motion process with timing** — extend `motion.ttl` with
   constant-speed sub-classes (per professor's example):

   ```turtle
   motion:RotationalConstantSpeedMotion rdfs:subClassOf motion:RotationalMotion .
   motion:LinearConstantSpeedMotion     rdfs:subClassOf motion:LinearMotion .
   ```

   The DS arm rotation (90° in 1 s) and the pusher stroke (50 mm in 1.2 s)
   are already modelled with `motion:hasVelocity`; reclassify them under
   the constant-speed sub-classes so a planner can rely on the type.

2. **Security / functional safety** — instantiate `safety.ttl` for the DS:

   ```turtle
   ex:DS_EStop            a safety:EmergencyStop ;
                          safety:hasSIL safety:SIL2 ;
                          safety:mitigates ex:PinchHazardAtMagazine .
   ex:PinchHazardAtMagazine a safety:Hazard .
   ```

   Wire the E-stop to the IEC 61499 application (`ex:App_Comp_Skill_Adp`)
   via `core:dependsOn`.

### New example files

- `examples/distribution-station/motion-process.ttl` — per-skill expected
  durations consolidated, plus the constant-speed reclassification.
- `examples/distribution-station/security.ttl` — DS hazards, E-stop, SILs.

### New queries

- `queries/ds-02-cycle-time.rq` — sum `skill:expectedDurationSeconds`
  along the 5-step transport chain to compute total cycle time.
- `queries/ds-03-safety-coverage.rq` — list hazards that have no
  mitigating safety function in the DS plant.

### To close M2

- [ ] Land the two new example files and two new queries.
- [ ] Extend the explainer with a section on time-aware reasoning.
- [ ] Git tag `v0.2-roadmap-m2`.

---

## M3 — Drilling Station, 5 example files, gap identification

### Goals

Demonstrate **portability** of the framework: a second MPS station
(Drilling) modelled with the same ontology stack, plus three modelling
concerns the DS example does not exercise — **Digital Twin (AAS)**,
**extended machine operations**, and **gap-identification queries**.

### New example folder

```
examples/drilling-station/
├── plant.ttl                # plant topology, drill spindle, clamping fixture
├── product.ttl              # drilled workpiece + drilling process
├── runtime.ttl              # PackML snapshot
├── digital-twin.ttl         # AAS submodels + properties + operations
└── machine-operations.ttl   # spindle motion (rotational constant speed),
                             #   feed motion (linear constant speed), drilling cycle
```

### Ontology additions

1. **Digital Twin** — populate `aas.ttl` instances:
   - `ex:DrillingStation_AAS a aas:AssetAdministrationShell` linked to
     `ex:DrillingStation1`.
   - Submodels for *Identification*, *TechnicalData*, *Operation*,
     *State*.
   - `aas:operation` entries that reference the IEC 61499 skill methods.

2. **Machine operations** — extend the motion vocabulary so that a drill
   cycle can be expressed as a sequence of typed motions:

   ```
   DrillCycle = RotationalConstantSpeedMotion (spindle)
              ∧ LinearConstantSpeedMotion (feed)
   ```

### New queries

- `queries/drill-01-can-manufacture.rq` — reuse the manufacturing-ability
  rule on the new plant.
- `queries/drill-02-gap-identification.rq` — for a requested process,
  return the **missing** capabilities:

  ```sparql
  SELECT ?process ?missingCap WHERE {
    ?product prod:requiresProcess ?process .
    ?process proc:requiresCapability ?missingCap .
    FILTER NOT EXISTS {
      ?plant core:hasPart+ ?r .
      ?r core:canPerform ?missingCap .
    }
  }
  ```

### To close M3

- [ ] Stand up the Drilling Station example end-to-end.
- [ ] Validate the AAS submodels parse against the AAS metamodel.
- [ ] Run gap-identification against a deliberately incomplete plant to
      prove it returns the right missing capability.
- [ ] Git tag `v0.3-roadmap-m3`.

---

## Open questions for the professor

1. Should *Security* sit in M2 (currently here, paired with Motion) or
   move to M3 per the recent note? Current draft keeps it in M2 because
   the DS already has the actuators/hazards to instantiate; M3 then
   focuses purely on the second station + AAS + machine operations.
2. For the Drilling Station, is the target a physical MPS station we
   already have, or a model-only validation?
3. Naming: are we comfortable using **M1/M2/M3** (validation milestones)
   in parallel with `vX.Y.Z` (code releases)?
