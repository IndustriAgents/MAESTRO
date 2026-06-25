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
| CQ06 | Which sub-skills, in what control-flow order, compose a composite skill? | [`cq06-subskill-control-flow.rq`](../queries/cq/cq06-subskill-control-flow.rq) |
| CQ07 | Which plan steps realise a recipe, and which skill realises each step? | [`cq07-recipe-steps-skills.rq`](../queries/cq/cq07-recipe-steps-skills.rq) |
| CQ08 | Which policy governs which skill/target, for which role and operating mode? | [`cq08-policy-grants.rq`](../queries/cq/cq08-policy-grants.rq) |
| CQ09 | Which SkillExecution produced a traced item, over what time interval? | [`cq09-execution-trace.rq`](../queries/cq/cq09-execution-trace.rq) |
| CQ10 | Which Digital Product Passport and identifiers belong to a product instance? | [`cq10-product-passport-identifiers.rq`](../queries/cq/cq10-product-passport-identifiers.rq) |

CQ06–CQ10 (new in 0.4.0) are exercised by the
[`examples/hhm-bridge/`](../examples/hhm-bridge/) plant and runtime snapshot.
