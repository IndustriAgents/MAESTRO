# 20. Digital Twin (Asset Administration Shell) + Twinning Layer

`ontologies/execution/aas.ttl` carries the **digital-twin envelope** of an
asset, **inspired by** the AAS 3.0 metamodel (Plattform Industrie 4.0 /
IDTA). It is a lightweight semantic bridge, **not** a strict AAS 3.0
implementation (see `docs/04-standard-alignment.md`).

## What 0.4.0 adds

**AAS-3.0-inspired structure**

- `aas:SubmodelElementCollection` — nested element groups.
- `aas:OperationVariable` + `aas:hasInputVariable` /
  `hasOutputVariable` / `hasInoutputVariable` — operation signatures.
- `aas:referencesElement` — what an operation variable carries. Its
  range is left **open** (`core:LogicalEntity`) so a variable can point
  at an IEC 61499 `ex:IOSignal` (a `core:State`), which is **not** an
  AAS submodel element.
- `aas:value` / `aas:valueType` on `aas:Property`.
- `aas:ModelingKind` (`aas:Template` / `aas:Instance`) + `aas:hasKind`.

**Twinning / synchronisation layer**

| Property | Meaning |
|---|---|
| `aas:mirrorsEntity` | The physical entity the twin mirrors — range `core:PhysicalEntity`, so it covers both a `core:Resource` **and** a whole `core:Plant` |
| `aas:reflectsState` | A State submodel tracks this `core:State` |
| `aas:synchronizedVia` | The channel (→ `com:Channel`) keeping the twin in sync |
| `aas:lastSynced` | Timestamp of the last sync |

> **Design choice.** `mirrorsEntity` targets `core:PhysicalEntity` (not
> `core:Resource`) precisely so a shell can mirror a `core:Plant`, which
> is a `PhysicalEntity` but not a `Resource`.

## Live-state separation

The State submodel only **declares** which runtime states the twin
tracks (`aas:reflectsState runtime:Available, …`). The **live**
`core:hasState` assertions stay in the runtime snapshot graph
(`runtime.ttl`), per `decisions/0002-runtime-graph-separation.md`. The
twin describes the structure; the runtime graph holds the value.

## Worked examples

Both stations now carry a twin:

- `examples/distribution-station/digital-twin.ttl` — `ex:DS_AAS`
  `mirrorsEntity ex:DistributingStation1` (a Plant), `synchronizedVia`
  the OPC UA channel, with Identification / TechnicalData / Operation /
  State submodels. Operation variables `referencesElement` the DS I/O
  signals, tying AAS operations to the IEC 61499 skill methods.
- `examples/drilling-station/digital-twin.ttl` — `ex:DrillingStation_AAS`
  with the same four-submodel shape.

`CQ09` answers "which AAS submodels reflect which runtime states?".

See also `docs/13-aas-runtime.md`.
