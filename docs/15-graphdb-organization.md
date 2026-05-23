# 15 — GraphDB Organization

> *See [README §21](../README.md#21-graphdb-organization).*

![Named Graphs](../figures/png/07-graphdb-named-graphs.png)

Store every module in a **dedicated named graph**. This pays off in
three concrete ways:

1. **Lifecycle separation.** Design-time graphs (`graph/skill`,
   `graph/capability`, …) rarely change. Runtime graphs
   (`graph/runtime`) change every few seconds. Keeping them apart lets
   the triple store cache aggressively.
2. **Reasoning scope.** OWL2-RL inference over `graph/runtime` alone is
   cheap; over the whole stack it is expensive. Named graphs let you
   point the reasoner at just the subset that changed.
3. **Access control.** A read-only consumer can be granted access to
   `graph/capability` (high-level intent) without exposing
   `graph/iec61499` (vendor-specific FB layouts).

## Recommended graph layout

```
graph/core           graph/resource       graph/motion
graph/skill          graph/capability     graph/process
graph/product        graph/ros            graph/iec61131
graph/iec61499       graph/opcua          graph/runtime
graph/reasoning      graph/planning       graph/aas
```

## Loading the stack into GraphDB

```bash
# 1. create a fresh repository
curl -X PUT 'http://localhost:7200/rest/repositories/maestro' \
     -H 'Content-Type: application/json' \
     -d @maestro-repo-config.json

# 2. load each module into its named graph
for f in ontologies/**/*.ttl; do
  graph=$(basename "$f" .ttl)
  curl -X POST "http://localhost:7200/repositories/maestro/statements?context=<http://example.org/maestro/$graph>" \
       -H 'Content-Type: text/turtle' \
       --data-binary @"$f"
done
```

## Reasoning rule sets

Inside GraphDB, run the SPARQL CONSTRUCT rules in [`rules/`](../rules/)
and attach SHACL shapes to `graph/reasoning/shapes`. Materialised inferences land in
`graph/reasoning/inferred` — keep them isolated so you can drop and
re-derive on demand.
