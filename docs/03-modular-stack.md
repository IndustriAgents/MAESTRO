# 03 — Modular Ontology Stack

> *See [README §3](../README.md#3-complete-modular-ontology-stack).*

![Modular Stack](../figures/png/02-modular-stack.png)

MAESTRO ships as **24 individual `.ttl` files** plus one umbrella file.
Load the umbrella and you get the entire stack; load only the modules you
care about for a tighter graph.

```
ontologies/
├── core/
│   └── manufacturing-core.ttl
├── physical/
│   ├── resource.ttl
│   └── motion.ttl
├── logical/
│   ├── skill.ttl
│   ├── capability.ttl
│   ├── process.ttl
│   └── product.ttl
├── execution/
│   ├── iec61131.ttl
│   ├── iec61499.ttl
│   ├── ros.ttl
│   ├── opcua.ttl
│   └── aas.ttl
├── runtime/
│   ├── runtime.ttl
│   └── state.ttl
├── cross-cutting/
│   ├── sensor.ttl
│   ├── unit.ttl
│   ├── communication.ttl
│   ├── safety.ttl
│   ├── quality.ttl
│   ├── maintenance.ttl
│   └── energy.ttl
├── reasoning/
│   ├── reasoning.ttl
│   └── planning.ttl
└── maestro.ttl                ← top-level umbrella
```

## Import graph

Every module declares its `owl:imports` explicitly. The dependency rule
is **directed and acyclic**:

- `core` imports nothing.
- Every other module imports `core` (transitively).
- `skill` imports `motion`.
- `capability` imports `skill`.
- `process` imports `capability`.
- `product` imports `process`.
- Execution adapters import `skill` only.

This means you can adopt the stack incrementally — start with `core` +
`resource`, then layer on `skill` + `capability`, etc.
