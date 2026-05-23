# 11 — Product Ontology

> *See [README §11](../README.md#11-product-ontology) · file [`product.ttl`](../ontologies/logical/product.ttl).*

A Product is the **demand side** of the manufacturing knowledge graph.
It states what processes it requires; capability/skill/control-component
inference does the rest.

## Class hierarchy

```
core:Product
├── prod:Part
└── prod:Assembly
prod:Feature
prod:Tolerance
prod:Material
```

## Linking a product to its required processes

```turtle
prod:GearboxHousing
    prod:requiresProcess ex:MachiningStep ;
    prod:requiresProcess ex:InspectionStep .
```

In the examples directory, [`examples/transfer-arm/product.ttl`](../examples/transfer-arm/product.ttl)
uses the same pattern:

```turtle
ex:ProductA
    a prod:Part ;
    prod:requiresProcess ex:PickAndPlaceProcess .
```

`prod:requiresProcess` is a precise product-to-process relation. It
remains a compatibility subproperty of deprecated `core:requires`, but
new rules and queries should use `prod:requiresProcess` directly.

## Features & tolerances

```turtle
prod:hasFeature       → prod:Feature
prod:hasTolerance     → prod:Tolerance
prod:madeOf           → prod:Material
prod:massKg           xsd:float
```

Features carry tolerances; tolerances will eventually drive process
selection (e.g. a `prod:Tolerance` of ±0.01 mm forces a precision
`proc:MachiningProcess`).
