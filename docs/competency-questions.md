# Competency Questions

These questions define the first conformance target for the MAESTRO
examples. Each question has a SPARQL query under [`queries/cq/`](../queries/cq/).

| ID | Question | Query |
|---|---|---|
| CQ01 | Which currently available resources can perform pick-and-place? | [`cq01-available-pick-place.rq`](../queries/cq/cq01-available-pick-place.rq) |
| CQ02 | Which control components implement each reusable skill? | [`cq02-skill-implementations.rq`](../queries/cq/cq02-skill-implementations.rq) |
| CQ03 | Which capabilities are required by each product's process chain? | [`cq03-product-capabilities.rq`](../queries/cq/cq03-product-capabilities.rq) |
| CQ04 | Which resources are missing directly declared provided skills? | [`cq04-resources-without-provided-skills.rq`](../queries/cq/cq04-resources-without-provided-skills.rq) |
| CQ05 | Which plants can manufacture which products after materialization? | [`cq05-plant-manufacturing-ability.rq`](../queries/cq/cq05-plant-manufacturing-ability.rq) |
| CQ06 | Which safety functions mitigate which hazards, and at what SIL? | [`cq06-safety-mitigations.rq`](../queries/cq/cq06-safety-mitigations.rq) |
| CQ07 | Which assets are exposed to a cyber threat that can trigger a physical hazard? | [`cq07-cyber-physical-exposure.rq`](../queries/cq/cq07-cyber-physical-exposure.rq) |
| CQ08 | Which cutting parameters are defined for each machining operation? | [`cq08-cutting-parameters.rq`](../queries/cq/cq08-cutting-parameters.rq) |
| CQ09 | Which AAS submodels reflect which runtime states? | [`cq09-twin-reflected-states.rq`](../queries/cq/cq09-twin-reflected-states.rq) |

CQ06–CQ09 (new in 0.4.0) exercise the security/safety convergence,
machine-operation, and digital-twin additions. There are also five
standalone analysis queries under [`queries/`](../queries/): `ds-02-cycle-time`,
`ds-03-safety-coverage`, `ds-04-security-exposure`, `drill-01-can-manufacture`,
and `drill-02-gap-identification`.
