# 22 — Provenance & Traceability (new in 0.4.0 — HHM-Core P5)

> *See [`prov.ttl`](../ontologies/execution/prov.ttl),
> [`trace.ttl`](../ontologies/execution/trace.ttl), the runtime additions in
> [`runtime.ttl`](../ontologies/runtime/runtime.ttl), and the priority map in
> [19-hhm-core-bridge.md](19-hhm-core-bridge.md).*

0.4.0 turns the runtime layer into a **lineage record**. The runtime module gained
`runtime:SkillExecution` and `runtime:TimeInterval`; two execution-side bridges then
align those to W3C and ETSI standards so every fired skill carries standard
provenance and item/batch genealogy "for free".

## Runtime record

```turtle
ex:Exec1 a runtime:SkillExecution ;
    runtime:executes    skill-lib:Transfer ;
    runtime:executedOn  ex:Station1 ;
    runtime:invokedVia  ex:Endpoint1 ;
    runtime:hasInput    ex:PV1 ;          # ex:PV1 a skill:ParameterValue
    runtime:hasStatus   runtime:Executing ;
    runtime:hasTime     ex:TI1 .          # ex:TI1 a runtime:TimeInterval (startTime/endTime)
```

Validated by [`constraints/shapes-runtime.ttl`](../constraints/shapes-runtime.ttl).

## PROV-O bridge (`prov.ttl`)

A `runtime:SkillExecution` **is** a `prov:Activity`, and its edges map onto the
standard PROV-O properties:

| MAESTRO | PROV-O |
|---|---|
| `runtime:SkillExecution` | `rdfs:subClassOf prov:Activity` |
| `runtime:executes`, `runtime:hasInput` | `rdfs:subPropertyOf prov:used` |
| `runtime:executedOn` | `rdfs:subPropertyOf prov:wasAssociatedWith` |
| `mprov:startedAtTime` / `mprov:endedAtTime` | `rdfs:subPropertyOf prov:startedAtTime` / `prov:endedAtTime` |

Time is split deliberately: `runtime:hasTime` stays an *object* property to a
`TimeInterval`, while the `mprov:` datatype aliases carry the PROV timestamps
directly on the activity (mixing object/datatype property hierarchies would be
illegal). Full PROV-O is in [`references/prov-o.ttl`](../references/prov-o.ttl)
(not imported).

## SAREF4INMA traceability (`trace.ttl`)

| Class | `rdfs:subClassOf` | Purpose |
|---|---|---|
| `trace:Item` | `s4inma:Item` | A produced item / unit |
| `trace:Batch` | `s4inma:Batch` | A production batch grouping items |
| `trace:TraceEvent` | `core:Event` | A genealogy record emitted during execution |

Edges: `trace:producedItem` (SkillExecution → Item; also a `prov:generated` edge),
`trace:partOfBatch` (Item → Batch), `trace:usedEquipment` (SkillExecution → Resource).

```turtle
ex:Exec1 trace:producedItem  ex:Item1 ;     # ex:Item1 a trace:Item
         trace:usedEquipment ex:Station1 .
ex:Item1 trace:partOfBatch   ex:Batch1 .     # ex:Batch1 a trace:Batch
```

Full SAREF4INMA is in [`references/saref4inma.ttl`](../references/saref4inma.ttl)
(not imported). The complete runtime snapshot is
[`examples/hhm-bridge/runtime.ttl`](../examples/hhm-bridge/runtime.ttl).
