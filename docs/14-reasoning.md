# 14 - Reasoning Architecture

> See README [section 18](../README.md#18-reasoning-architecture), [section 19](../README.md#19-core-reasoning-model), and [section 20](../README.md#20-example-swrl-rules).

MAESTRO uses a layered reasoning model:

| Layer | Technology | What it does |
|---|---|---|
| Semantic inheritance | OWL2-RL/RDFS | Subclass, subproperty, inverse-property propagation |
| Validation | SHACL | Rejects malformed graphs before inference |
| Capability inference | SPARQL CONSTRUCT | Materializes `core:canPerform` |
| Manufacturing inference | SPARQL CONSTRUCT | Materializes `core:canManufacture` |
| Orchestration | SPARQL SELECT | Application and LLM query layer |

The SWRL files remain readable sketches, but the executable rule artifacts
are:

- [`rules/capability-inference.rq`](../rules/capability-inference.rq)
- [`rules/manufacturing-ability.rq`](../rules/manufacturing-ability.rq)

## Canonical Reasoning Chain

```text
Product
  prod:requiresProcess
Process
  proc:requiresCapability
Capability
  cap:realizedBySkill
Skill
  implemented by ControlComponent
ControlComponent
  controls Resource
Resource
  core:canPerform Capability
Plant
  core:canManufacture Product
```

## Capability Inference

```sparql
CONSTRUCT {
    ?resource core:canPerform ?capability .
}
WHERE {
    ?capability ?realizedBy ?skill .
    ?realizedBy rdfs:subPropertyOf* core:realizedBySkill .
    ?component ?implements ?skill ;
               ?controls ?resource .
    ?implements rdfs:subPropertyOf* core:implements .
    ?controls rdfs:subPropertyOf* core:controls .
}
```

## Manufacturing Ability

```sparql
CONSTRUCT {
    ?plant core:canManufacture ?product .
}
WHERE {
    ?plant core:hasPart ?resource .
    ?resource core:canPerform ?capability .
    ?product prod:requiresProcess ?process .
    ?process proc:requiresCapability ?capability .
}
```

Run `python tests/validate_repo.py` to parse the ontology, execute the
queries, materialize these rules, and check the core expected inferences.
