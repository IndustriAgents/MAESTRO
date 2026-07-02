# Relating the Festo Distributing Station (newsystem4) to the MAESTRO Core

**Purpose.** This document demonstrates, in detail, how the distribution-station
example relates to the *universal* MAESTRO core ontology. It is written for
inclusion in the project technical documentation and for the Spindox
"MAESTRO-on-our-testbed" demonstration. Every statement below is taken from the
actual files
(`examples/distribution-station-newsystem4/{plant,product,runtime}.ttl`) and the
loaded MAESTRO ontology (`ontologies/**/*.ttl`), and is reproducible with the
scripts in the last section.

---

## 1. The principle: one frozen core, everything else extends it

MAESTRO is a **modular, universal manufacturing ontology**. It is layered so that
exactly one tier is invariant and everything domain-specific is an extension of
it:

| Tier | What it is | Stability |
|---|---|---|
| **Frozen core** — `core:` (`ontologies/core/manufacturing-core.ttl`) | The universal abstractions (`core:Entity` taxonomy) and the spine relations (`hasPart`, `provides`, `implements`, `controls`, `realizedBySkill`, `requiresCapability`, `composedOfSkill`, `hasState`, `canPerform`, `canManufacture`, …). Imports nothing. | **Invariant** — changes only at a major version. |
| **MAESTRO modules** — `res:`, `skill:`, `cap:`, `proc:`, `prod:`, `iec61499:`, `opcua:`, `motion:`, `sensor:`, `runtime:`, … | Domain/adapter vocabularies that couple to core **only** via `owl:imports` + `rdfs:subClassOf` / `rdfs:subPropertyOf core:*`. | Stable, versioned **extensions**. |
| **Example / testbed** — `ex:` (this station) | The Festo-specific classes (`ex:FeederUnit`, `ex:IOSignal`, …) and all the A-Box individuals (`FeederUnit1`, `IO_push`, …). | A concrete **instantiation** of the above. |

**The distribution-station example is therefore not a separate model — it is the
universal core, specialised down to the Festo testbed.** No element of the
example introduces a new top-level concept; each one *specialises* a core class
or *sub-properties* a core relation.

---

## 2. Class alignment — every example class is a kind of a core class

Running the `rdfs:subClassOf` closure over the example + ontology shows that
**every domain class used in the example resolves to a frozen `core:` class**
(0 classes without a core ancestor). Grouped by the core class they specialise:

### `core:Resource` (physical manufacturing assets)
```
core:Resource
 ├── res:Machine            ← ex:FeederUnit (FeederUnit1), ex:TransferUnit (TransferUnit1),
 │                            ex:Magazine (Magazine1), ex:ControlConsole (ControlConsole1)
 │     └── res:Robot ← res:TransferArm (TransferArm1)
 ├── res:Actuator           ← ex:PneumaticCylinder (FeederCylinder1 · DSNU-8-80),
 │                            ex:RotaryDrive (TransferMotor1 · DSR-16-180),
 │                            ex:VacuumValve (VacuumValve1), ex:VacuumGenerator (VacuumGenerator1)
 ├── res:Tool               ← ex:Pusher (FeederPusher1), ex:VacuumFilter (VacuumFilter1 · VAF-8),
 │                            ex:SuctionCup (SuctionCup1 · VAS-8), res:VacuumUnit (VacuumUnit1)
 ├── sensor:Sensor          ← ex:MagneticProximitySensor (SME-8 ×2),
 │   (⊑ core:Resource +      ex:ThroughBeamSensor (SOEG-L), ex:LimitSwitch (S-3-E ×2),
 │    sosa:Sensor)           ex:VacuumSwitch (VPEV)
 └── res:ControllerDevice ← res:PLC (Device_EcoRT_0 · Soft_dPAC)
```

### `core:Plant`
```
core:Plant ← DistributingStation1   (the whole station)
```

### `core:Skill` (logical, executable behaviour)
```
core:Skill
 ├── skill:AtomicSkill
 │     ├── skill:HandlingSkill     ← Type_skMagazineEject
 │     ├── skill:MotionSkill       ← Type_skMoveToMagazine, Type_skMoveToDownstream
 │     └── skill:ManipulationSkill ← Type_skGripWorkpiece, Type_skReleaseWorkpiece
 ├── skill:CompositeSkill
 │     └── skill:TransferSkill     ← Type_skSwivelArmTransfer
 └── (direct)                      ← the registered runtime skills Reg_Magazine,
                                     Reg_SwivelArm (+ its 4 sub-skills), Reg_ButtonsLights
```

### `core:Capability`
```
core:Capability ← cap:HandlingCapability, cap:PickPlaceCapability, cap:TransportCapability
                  (reusable capability individuals from capability.ttl)
```

### `core:Process`
```
core:Process ← proc:ManufacturingProcess
                 ├── proc:HandlingProcess  ← PushProcess, GripProcess, ReleaseProcess
                 └── proc:TransportProcess ← DistributeWorkpieceProcess,
                       (⊑ HandlingProcess)   MoveToMagazineProcess, MoveToDownstreamProcess
```

### `core:Product`
```
core:Product ← prod:Part ← WorkpieceWP
```

### `core:ControlComponent` (the IEC 61499 / Schneider Electric control layer)
```
core:ControlComponent
 └── iec61499:FunctionBlock
       ├── iec61499:CompositeFB ← FBT_skMagazine_mo, FBT_skSwivelArm_mo_cmp1,
       │                           the 4 elementary-operation FBTs, FBT_skButtonsLights,
       │                           the FB instances (Inst_Magazine, Inst_SwivelArm_Cmp1, …)
       ├── iec61499:BasicFB     ← FBT_SkillMagazineController_b_a, FBT_…Orchestrator, B_MERGE4
       ├── ex:ProtocolAdapterFB ← FBT_Magazine2Magasine, FBT_SwivelArm2Transfer (+ instances)
       └── ex:PermitAdapterFB   ← FBT_True_Adp, FBT_True_Adp_rev (+ instances)
```

### `core:State`
```
core:State ← ex:IOSignal ← the 11 datapoints
             (IO_pos_e, IO_pos_r, IO_empty, IO_at_mgz, IO_at_next, IO_vmon,
              IO_push, IO_to_mgz, IO_to_next, IO_vcm_on, IO_vcm_off)
```

### `core:LogicalEntity` (other logical artefacts)
```
core:LogicalEntity ← motion:LinearMotion (CylinderLinearMotion),
                     motion:RotationalMotion (ArmRotationalMotion),
                     iec61499:Application (App_APP1),
                     iec61499:RuntimeResource (Runtime_RES0),
                     opcua:OpcUaSkillInterface (OpcUaDistributionInterface),
                     sensor:ObservableProperty (the 4 observed properties)
```

> **Result.** The example exercises **8 of the ~12 core classes** —
> `Plant`, `Resource`, `Skill`, `Capability`, `Process`, `Product`, `State`,
> `ControlComponent` (plus `LogicalEntity`). A class-token audit of all **71
> individuals** in the example returns **0 terms** that are not an instance of a
> MAESTRO core/module class.

---

## 3. Property alignment — every relation is (or specialises) a core spine relation

The edges in the example are either core spine properties used directly, or
`rdfs:subPropertyOf` a core spine property, or module/local object properties
that range over core classes.

### 3a. Core spine properties used directly
`core:hasPart` / `core:partOf`, `core:provides`, `core:hasState`,
`core:identifier`, `core:description`.

### 3b. Module / example properties that `rdfs:subPropertyOf` a core property
| Property (example/module) | `rdfs:subPropertyOf` |
|---|---|
| `cap:realizedBySkill` | `core:realizedBySkill` |
| `proc:requiresCapability` | `core:requiresCapability` |
| `skill:composedOfSkill` | `core:composedOfSkill` |
| `skill:requiresMotion` | `core:requiresMotion` |
| `iec61499:implementsSkill` | `core:implements` |
| `iec61499:controlsResource` | `core:controls` |
| `iec61499:hostsRuntimeResource` | `core:hosts` |
| `ex:feeds` | `core:connectedTo` |
| `ex:permits` | `core:connectedTo` |
| `ex:bridges` | `core:connectedTo` |
| `ex:drivenBy` | `core:dependsOn` |
| `ex:hostedOn` | `core:dependsOn` |
| `ex:hasSubProcess` | `core:hasPart` |
| `ex:hasSubSkill` | `core:composedOfSkill` (→ already a core spine property) |

### 3c. Example properties that specialise a *skill-module* relation (over core classes)
| Property | `rdfs:subPropertyOf` | Operates over |
|---|---|---|
| `ex:controlsIO` | `skill:hasPostcondition` | `core:Skill` → `core:State` (`ex:IOSignal`) |
| `ex:receivesIO` | `skill:hasPrecondition` | `core:Skill` → `core:State` (`ex:IOSignal`) |

### 3d. Local object properties whose domain/range are core/module classes
`ex:createsSignal` (`core:Resource` → `ex:IOSignal ⊑ core:State`),
`ex:commandsActuator` (`ex:IOSignal` → `res:Actuator ⊑ core:Resource`),
`ex:instanceOfFBT` (FB → FB), `ex:ofType` (registered `core:Skill` → skill TYPE),
`opcua:exposes` (interface → `core:Skill`), `proc:precedes`,
`prod:requiresProcess` (`core:Product` → `core:Process`).

### 3e. Inferred core relations (materialised by the universal rules)
`core:canPerform` (`core:Resource` → `core:Capability`) and
`core:canManufacture` (`core:Plant` → `core:Product`).

---

## 4. The demonstration: universal core reasoning runs on the testbed

The decisive point for "how MAESTRO can be used with our testbed" is that
MAESTRO's **domain-agnostic** inference rules (`rules/capability-inference.rq`,
`rules/manufacturing-ability.rq` — written for *no specific plant*) operate
purely on the core spine, and therefore fire unchanged on the Festo data.

**Reasoning chain (all core-level):**
```
iec61499:implementsSkill ⊑ core:implements      FBT_skSwivelArm_mo_cmp1 implements Type_skSwivelArmTransfer
iec61499:controlsResource ⊑ core:controls       FBT_skSwivelArm_mo_cmp1 controls   TransferUnit1
cap:realizedBySkill ⊑ core:realizedBySkill       cap:PickPlaceCapability realizedBySkill Type_skSwivelArmTransfer
                                          ⇒ (rule)  TransferUnit1  core:canPerform  cap:PickPlaceCapability

core:hasPart  +  prod:requiresProcess  +  proc:requiresCapability
                                          ⇒ (rule)  DistributingStation1  core:canManufacture  WorkpieceWP
```

**Materialised conclusions** (verified by running the two rules over the example):
- `FeederUnit1    core:canPerform cap:HandlingCapability`
- `TransferUnit1  core:canPerform cap:PickPlaceCapability`
- `TransferMotor1 core:canPerform cap:TransportCapability`
- **`DistributingStation1 core:canManufacture WorkpieceWP`**

In other words: we described the testbed in MAESTRO's universal vocabulary, and
the **core's own reasoning** told us what the station can do — without any
plant-specific logic.

---

## 5. Figures

| Figure | Shows |
|---|---|
| `figures/png/16-core-to-festo-bridge.png` | The core ↔ testbed alignment: each Festo individual specialises a frozen `core:` class via `rdf:type` / `rdfs:subClassOf`. |
| `figures/png/15-distribution-newsystem4-schema.png` | The full example instance graph, clustered by layer; individuals typed by a frozen `core:` class carry a gold double border. |
| `figures/png/14-maestro-core-schema.png` | The universal MAESTRO/HHM-Core schema the example instantiates (frozen core marked, extension modules and `«EXT»` external bridges distinguished). |

See also [`../../docs/18-design-principles.md`](../../docs/18-design-principles.md#stability-contract--frozen-core-vs-extension)
for the frozen-core-vs-extension stability contract, and
[`../../docs/05-core-ontology.md`](../../docs/05-core-ontology.md) for the core
class taxonomy and relationship spine.

---

## 6. Reproducibility

**Prove every example class rolls up to a core class:**
```python
from pathlib import Path
import rdflib
from rdflib.namespace import RDF, RDFS, OWL

g = rdflib.Graph()
for p in Path("ontologies").glob("**/*.ttl"):
    g.parse(p, format="turtle")
for f in ["plant.ttl", "product.ttl", "runtime.ttl"]:
    g.parse(f"examples/distribution-station-newsystem4/{f}", format="turtle")

CORE = "https://w3id.org/maestro/core#"

def core_ancestor(cls):
    seen, stack = set(), [cls]
    while stack:
        c = stack.pop()
        if str(c).startswith(CORE):
            return c
        for sup in g.objects(c, RDFS.subClassOf):
            if sup not in seen:
                seen.add(sup); stack.append(sup)
    return None

EX = "https://w3id.org/maestro/examples/distribution-station-newsystem4#"
for cls in {t for s, p, t in g.triples((None, RDF.type, None))
            if str(s).startswith(EX) and t not in (OWL.Class, OWL.NamedIndividual)}:
    print(cls, "->", core_ancestor(cls))   # every line ends in a core: class
```

**Run the universal rules and see the testbed conclusions:**
```python
for rule in ["rules/capability-inference.rq", "rules/manufacturing-ability.rq"]:
    for triple in g.query(Path(rule).read_text(encoding="utf-8")):
        g.add(triple)

CORE_NS = rdflib.Namespace(CORE)
EX_NS   = rdflib.Namespace(EX)
print(list(g.triples((None, CORE_NS.canPerform, None))))
print(list(g.triples((EX_NS.DistributingStation1, CORE_NS.canManufacture, None))))
```

**Repository validation** (`python tests/validate_repo.py`) parses the example,
enforces the SHACL shapes and re-derives these inferences as part of the regular
test suite — so the alignment described here is continuously checked, not a
one-off claim.
