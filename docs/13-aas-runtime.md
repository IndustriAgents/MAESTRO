# 13 - AAS + Runtime

> See README [section 16](../README.md#16-aas-ontology) and [section 17](../README.md#17-runtime-ontology).

## AAS - Asset Administration Shell

`aas.ttl` currently provides a lightweight AAS bridge:

```text
aas:AssetAdministrationShell -> aas:hasSubmodel -> aas:Submodel
aas:Submodel -> aas:hasSubmodelElement -> aas:SubmodelElement
aas:Property, aas:Operation -> subclasses of aas:SubmodelElement
aas:AssetAdministrationShell -> aas:representsAsset -> aas:Asset
```

This is intentionally not yet a full AAS 3.0 Reference/Key model. That
should be handled as a dedicated adapter-hardening task before claiming
strict AAS conformance.

## Runtime - Live Operational State

`runtime.ttl` aligns its state values with PackML, but models them as
canonical individuals of `core:State`, not as classes:

```turtle
runtime:Available a core:State, skos:Concept .
runtime:Busy      a core:State, skos:Concept .
runtime:Fault     a core:State, skos:Concept .
```

Instance data points directly at these canonical values:

```turtle
ex:TransferArm1 core:hasState runtime:Available .
```

State changes remain first-class events:

```turtle
runtime:StateTransition a owl:Class ;
    rdfs:subClassOf runtime:RuntimeEvent .

runtime:enteredState  # -> core:State
runtime:fromState     # -> core:State
runtime:timestamp     # xsd:dateTime
```

Future production work should introduce state occurrences with intervals
for historical state validity. The current `core:hasState` relation is a
current-state shortcut.
