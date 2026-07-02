# 11 — Product Ontology

> *See [README §11](../README.md#11-product-ontology) · file [`product.ttl`](../ontologies/logical/product.ttl).*

A Product is the **demand side** of the manufacturing knowledge graph.
It states what processes it requires; capability/skill/control-component
inference does the rest.

## Class hierarchy

```
core:Product
├── prod:Part
├── prod:Assembly
├── prod:ProductType          (0.4.0 — the design/catalogue item)
│   └── prod:Variant          (0.4.0 — a configuration of a type)
└── prod:ProductInstance      (0.4.0 — a physically produced unit)
prod:Feature
prod:Tolerance
prod:Material
prod:Requirement              (0.4.0)
prod:Identifier               (0.4.0 — GTIN · UUID · IRDI · IRI)
prod:BOMNode                  (0.4.0)
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
prod:mass             → unit:Quantity   # unit-bearing; replaces the deprecated prod:massKg
```

Features carry tolerances; tolerances will eventually drive process
selection (e.g. a `prod:Tolerance` of ±0.01 mm forces a precision
`proc:MachiningProcess`).

> `prod:massKg` (a bare `xsd:float`) is **deprecated** — use `prod:mass`
> with a `unit:Quantity` so mass carries an explicit unit.

## Identity, variants & BOM (new in 0.4.0 — HHM-Core P4)

0.4.0 adds an explicit **type / instance** split, configuration variants,
requirements, multi-scheme identifiers and a structured bill of materials.

| Construct | Class / property | Purpose |
|---|---|---|
| Type vs instance | `prod:ProductType`, `prod:ProductInstance` (`prod:instanceOfType`) | The catalogue item vs a physically built unit |
| Variant | `prod:Variant` (`prod:variantOf`) | A configuration of a base `ProductType` |
| Requirement | `prod:Requirement` (`prod:appliesTo` → `prod:Feature`) | A functional/dimensional/regulatory requirement on a feature |
| Identifier | `prod:Identifier` → `GTIN` · `UUID` · `IRDI` · `IRI` (`prod:hasIdentifier`, `prod:scheme`, `prod:value`) | Scheme-qualified identity; `core:identifier` stays the simple string id |
| BOM | `prod:BOMNode` (`prod:hasBOMNode`, `prod:nodeFor`, `prod:quantity`, `prod:position`, `prod:refDesignator`) | Structured bill-of-materials node beyond `core:hasPart` |

```turtle
ex:WidgetType a prod:ProductType , prod:Assembly ;
    prod:hasIdentifier ex:WidgetGTIN ;     # ex:WidgetGTIN a prod:GTIN
    prod:hasBOMNode    ex:Bom1 ;
    prod:hasFeature    ex:Hole1 .

ex:Widget1 a prod:ProductInstance ;
    prod:instanceOfType ex:WidgetType .
```

The **Digital Product Passport** view (`dpp:ProductPassport`, `dpp:describes`,
`dpp:hasIdentifier`) and ECLASS dictionary alignment live in
[`cross-cutting/dpp.ttl`](../ontologies/cross-cutting/dpp.ttl). See
[19-hhm-core-bridge.md](19-hhm-core-bridge.md) and the worked
[`examples/hhm-bridge/plant.ttl`](../examples/hhm-bridge/plant.ttl).
