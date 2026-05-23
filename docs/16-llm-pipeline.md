# 16 - LLM + GraphDB Pipeline

> See [README section 22](../README.md#22-llm--graphdb-architecture).

The LLM pipeline should treat the graph as the source of truth. The LLM
extracts intent and fills SPARQL templates; deterministic graph queries
and materialization decide which resource can actually execute.

## Stages

1. User command: "Move part X to station 3."
2. Intent extraction: identify the requested capability, target product,
   and any state or resource filters.
3. SPARQL generation: render
   [`queries/05-llm-pipeline-template.rq`](../queries/05-llm-pipeline-template.rq).
4. Graph reasoning: apply OWL/RDFS propagation and the SPARQL CONSTRUCT
   rules in [`rules/`](../rules/).
5. Filtering: require `core:hasState runtime:Available` and any payload,
   reach, safety, or quality constraints.
6. Explanation: the LLM summarizes the returned triples.
7. Execution: dispatch through the relevant adapter or OPC UA
   SkillInterface.

## Safety Boundary

The LLM should not invent graph facts or write directly into the runtime
graph without provenance. It should produce candidate SPARQL and
human-readable explanations around validated graph data.
