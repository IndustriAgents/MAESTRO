# Explanation of Figures 14 and 15

This document explains two Graphviz figures:

- **Figure 14 — `14-maestro-core-schema.png`** — the **MAESTRO HHM-Core schema**
  (the universal ontology, at the class level).
- **Figure 15 — `15-distribution-newsystem4-schema.png`** — the **Festo
  Distributing Station (newsystem4) knowledge graph** (one concrete instance of
  that ontology, at the individual level).

Figure 15 is Figure 14 *instantiated*: every box in Figure 15 is an instance of a
class shown (or specialised) in Figure 14.

---

## How to read both figures (shared conventions)

- **Box** = a class (Fig 14) or an individual (Fig 15). The small italic text in a
  Fig 15 box is the individual's type, e.g. `FeederUnit1 (ex:FeederUnit)`.
- **Arrow** = a relationship (an ontology property). The label on the arrow is the
  property name, e.g. `hasPart`, `implementsSkill`, `realizedBySkill`.
- **Coloured rounded outline** = a *cluster*, grouping one concern/layer (Product,
  Skills, Resources, IEC 61499 control, …).
- **Gold box with a double border** = a **frozen `core:` class** (Fig 14) or an
  individual **typed by a frozen `core:` class** (Fig 15). This is the invariant
  spine of MAESTRO.
- **Orange "note" shapes (`«EXT»`)** = **external standards / artefacts** that
  MAESTRO bridges to but never absorbs — always an extension.
- **Solid arrow** = an asserted triple (a fact stated in the files).
- **Dashed / dotted arrow** = a secondary or attribute relation; **red dashed**
  (Fig 15) = an **inferred** triple produced by the reasoning rules.

Each figure also carries a **"Stability contract" legend** (top-left) that
restates the three tiers: frozen core → MAESTRO modules → external extension
points.

---

## Figure 14 — MAESTRO HHM-Core Schema

**What it is.** A class-level map of the whole MAESTRO ontology, organised into
the seven manufacturing concerns that the 0.4.0 "HHM-Core" release covers. It
answers: *what concepts does MAESTRO define, and how do they relate?*

**The seven clusters (concerns):**

| Cluster (colour) | Module(s) | What it models |
|---|---|---|
| **Product** (purple) | `product.ttl`, `dpp.ttl` | `prod:ProductType` / `ProductInstance` / `Variant` / `Feature` / `Requirement` / `Identifier` / `BOMNode` / `Material` — what is to be produced, its identity and bill of materials. |
| **Resources / Mechanical** (teal) | `resource.ttl`, `capability.ttl` | `res:AssemblyStation` / `Module` / `Machine` and `core:Capability` — the physical assets and what they *can do*. |
| **Skills** (red) | `core:Skill` + `skill.ttl` | `skill:AtomicSkill` / `CompositeSkill`, the reified orchestration (`SubSkillLink`, `ControlFlow`, `DataBinding`), typed parameters, pre/post-conditions and the neutral `SkillInterface` / `SkillService`. The keystone layer. |
| **Recipe / Planning** (blue) | `recipe.ttl` | `recipe:Recipe` / `PlanStep` — a neutral process plan whose steps are realised by skills. |
| **Safety / Security / Policy** (black) | `policy.ttl`, `safety.ttl`, `core:Constraint` | `policy:Policy` / `Permission` / `Role` / `Mode` / `Evidence`, `safety:Hazard` / `Risk` / `Mitigation`, and the `core:Constraint` that limits skills, steps, modules and endpoints. |
| **Invocation Hooks** (orange) | `communication.ttl` | `com:Endpoint` / `Protocol` / `Binding` / `OperationSignature` / `EventStream` — the protocol-neutral way a skill is actually called. |
| **Execution / Provenance** (violet) | `runtime.ttl` (+ `prov.ttl`, `trace.ttl`) | `runtime:SkillExecution` / `TimeInterval` / `Fault` and `core:State` — the record of a skill actually running. |

**The frozen core inside the clusters.** Four classes carry the **gold double
border** because they belong to the frozen `core:` spine: `core:Skill`,
`core:Capability`, `core:Constraint`, `core:State`. Everything else in the boxes
(`prod:…`, `skill:…`, `recipe:…`, `com:…`, …) is a **module that extends** that
core via `rdfs:subClassOf` / `rdfs:subPropertyOf`.

**The `«EXT»` extension points.** The orange notes name the external standards
each cluster bridges, e.g. ECLASS/DPP, CAEX (AutomationML), ISA-88, ISA-95,
OPC UA, REST, DTDL, AAS, QUDT, SOSA/SSN, PROV-O, SAREF4INMA, ODRL, CaSkMan.
These are **always extensions** — bridged via `rdfs:subClassOf` / `skos:exactMatch`
in adapter modules, never copied into the core.

**Key relationships to point out** (the manufacturing "spine"):
`Product → requiresProcess → Process → requiresCapability → Capability →
realizedBySkill → Skill`, and on the execution side `Skill ← implements ←
ControlComponent → controls → Resource`. The Skills cluster shows how a
`CompositeSkill` is decomposed (`hasSubSkillLink → linksTo / hasControlFlow /
hasDataBinding`), and the Invocation cluster shows how a skill is exposed
(`SkillService → exposesInterface → SkillInterface → exposedVia → Endpoint →
hasBinding → Binding → specializesAs → Protocol`).

---

## Figure 15 — Festo Distributing Station (newsystem4) knowledge graph

**What it is.** The actual knowledge graph of our testbed: every box is a real
individual from `examples/distribution-station-newsystem4/{plant,product,runtime}.ttl`,
and every arrow is a real triple. It answers: *what does our station consist of,
and what can MAESTRO infer about it?* It is grouped into six layers.

**The six clusters:**

| Cluster (colour) | Contents |
|---|---|
| **Plant & Resources** (teal) | `DistributingStation1` and its parts: `FeederUnit1` (Magazine, FeederPusher, FeederCylinder · DSNU-8-80), `TransferUnit1` (TransferMotor · DSR-16-180, TransferArm, VacuumUnit → valve / generator / filter · VAF-8 / suction cup · VAS-8), `ControlConsole1`. Edges: `hasPart`, `feeds`, `drivenBy`. |
| **Sensors & I/O Datapoints** (amber) | The 6 sensors (SME-8 ×2, SOEG-L, S-3-E ×2, VPEV) and the 11 datapoints (ovals): inputs `pos_e/pos_r/empty/at_mgz/at_next/vmon`, outputs `push/to_mgz/to_next/vcm_on/vcm_off`. Edges: `createsSignal` (sensor→input), `commandsActuator` (output→actuator). |
| **Skill TYPES** (red) | The 7 skills: `Type_skMagazineEject`, the 4 elementary swivel-arm ops, the composite `Type_skSwivelArmTransfer`, the HMI `Type_skButtonsLights`, plus the two motion specs. Edges: `hasSubSkill`, `requiresMotion`, and `provides` from the resources. |
| **Capability / Process / Product** (purple) | `cap:HandlingCapability` / `PickPlaceCapability` / `TransportCapability`, the 5-step `DistributeWorkpieceProcess` (Push→…→Release) and `WorkpieceWP`. Edges: `realizedBySkill`, `hasSubProcess`, `precedes`, `requiresCapability`, `requiresProcess`. |
| **IEC 61499 Control** (lavender) | The function-block types (`FBT_*`) with `implementsSkill` + `controlsResource`, the `Soft_dPAC` device / `Runtime_RES0` / `App_APP1`, and the FB instances wired by `permits` / `bridges` / `instanceOfFBT`. |
| **OPC UA Skill Interface** (blue) | `OpcUaDistributionInterface` that `exposes` the registered skills `Reg_Magazine` / `Reg_SwivelArm` / `Reg_ButtonsLights` (each `ofType` a skill TYPE, `partOf` the application). |

**Gold double-bordered boxes** = individuals typed by a **frozen `core:` class**:
`DistributingStation1` (`core:Plant`), the three `Reg_*` registered skills
(`core:Skill`), and the three `cap:*` capabilities (`core:Capability`). They show
the universal core showing through the Festo-specific names.

**Red dashed arrows = inferred facts.** These are *not* asserted in the files —
they are produced by MAESTRO's universal reasoning rules:
`FeederUnit1 canPerform HandlingCapability`,
`TransferUnit1 canPerform PickPlaceCapability`,
`TransferMotor1 canPerform TransportCapability`, and the headline
**`DistributingStation1 canManufacture WorkpieceWP`**.

**The `«EXT»` notes** here name the real external artefacts the example bridges:
IEC 61499 / Schneider Electric (the control project, `Soft_dPAC`), the OPC UA
server, the Festo MPS hardware datasheets, SOSA (`sosa:observes`) and QUDT
(`unit:Quantity`).

---

## How the two figures relate (the one-sentence takeaway)

**Figure 14 is the universal vocabulary; Figure 15 is that vocabulary filled in
with our testbed.** Every box in Figure 15 is an instance of a class in Figure 14
(directly or via one or two `rdfs:subClassOf` steps), and the same core
relationships drive the reasoning in both. That is the demonstration that MAESTRO
— a universal ontology — applies to the Festo distribution station:

```
Figure 14 (classes)            Figure 15 (our station)
  core:Resource         ⟵type⟵  FeederUnit1, TransferMotor1, sensors, …
  core:Plant            ⟵type⟵  DistributingStation1
  core:Skill            ⟵type⟵  Type_skSwivelArmTransfer, Reg_Magazine, …
  core:Capability       ⟵type⟵  cap:PickPlaceCapability, …
  core:Process          ⟵type⟵  DistributeWorkpieceProcess, …
  core:Product          ⟵type⟵  WorkpieceWP
  core:ControlComponent ⟵type⟵  FBT_skMagazine_mo (Schneider Electric), …
  core:State            ⟵type⟵  IO_push, IO_vmon, … (the 11 datapoints)
```

A dedicated alignment diagram (`16-core-to-festo-bridge.png`) and a full
write-up (`examples/distribution-station-newsystem4/CORE-ALIGNMENT.md`) make this
core↔testbed mapping explicit.
