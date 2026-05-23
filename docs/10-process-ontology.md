# 10 — Process Ontology

> *See [README §10](../README.md#10-process-ontology) · file [`process.ttl`](../ontologies/logical/process.ttl).*

Manufacturing logic. Aligned with **DIN 8580** (the six-family process
taxonomy) and **VDI 3682** (process description).

## DIN 8580 alignment

```
proc:ManufacturingProcess
├── proc:PrimaryShaping            (DIN 8580 Group 1)
├── proc:Forming                   (DIN 8580 Group 2)
├── proc:Separating                (DIN 8580 Group 3)
│   └── proc:MachiningProcess
├── proc:JoiningProcess            (DIN 8580 Group 4)
│   └── proc:AssemblyProcess
├── proc:Coating                   (DIN 8580 Group 5)
└── proc:MaterialPropertyChange    (DIN 8580 Group 6)
```

Plus auxiliary processes:

```
proc:HandlingProcess
├── proc:TransportProcess
proc:InspectionProcess
```

## Process relations

```turtle
proc:precedes          # subPropertyOf nothing (inverse: proc:follows)
proc:follows
proc:parallelWith      # SymmetricProperty
proc:requiresCapability   # subPropertyOf core:requiresCapability; range core:Capability
proc:producesState        # range core:State
```

VDI 3682 sequencing falls out of `proc:precedes` / `proc:follows`. The
binding to capability is what closes the chain:

```
Product  -> requiresProcess -> Process -> requiresCapability -> Capability
```

…and from there capability → skill → control component → resource, per
[§19](14-reasoning.md).
