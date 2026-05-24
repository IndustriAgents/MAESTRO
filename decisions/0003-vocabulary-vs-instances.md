# ADR-0003: Vocabulary lives in `skill:` and `motion:`; instances live in `skill-lib:` and `motion-lib:`

- **Status:** Accepted
- **Date:** 2026-05-23

## Context

Through 0.2.0, the `skill:` namespace contained both classes
(`skill:MotionSkill`, `skill:CompositeSkill`) and individual skill
specifications (`skill:Transfer`, `skill:MoveLinear`). Similarly,
`motion:` contained classes and individual motion specs
(`motion:LinearMotionSpec`). This produced two problems:

1. The same namespace was used for vocabulary (stable, semver-governed)
   and for example data (free to evolve), making it impossible to version
   them separately.
2. Reading `skill:Transfer` was ambiguous to newcomers — class? individual?
   Documentation had to disambiguate every reference.

## Decision

Introduce two library ontologies for reusable individuals:

- `ontologies/lib/skill-lib.ttl` (IRI: `https://w3id.org/maestro/skill-lib`)
  for skill individuals.
- `ontologies/lib/motion-lib.ttl` (IRI: `https://w3id.org/maestro/motion-lib`)
  for motion specification individuals.

`skill:` and `motion:` now contain only classes and properties. The libraries
import the vocabulary and add typed individuals:

```turtle
skill-lib:Transfer a skill:TransferSkill ;
    skill:composedOfSkill skill-lib:MoveLinear ,
                          skill-lib:VacuumPick ,
                          skill-lib:Release .
```

End-user plant data lives in `examples/*/plant.ttl` under the `ex:` namespace
and references library individuals by IRI.

## Consequences

- Capability ontology (`capability.ttl`) imports `skill-lib` and uses
  `skill-lib:Transfer` etc. in `cap:realizedBySkill` assertions.
- The umbrella `maestro.ttl` imports both libraries so a single load still
  yields the full stack.
- Future libraries (`capability-lib`, `process-lib`, …) can follow the same
  pattern without polluting their vocabulary namespaces.
- Migration script `rules/migrate-0.2-to-0.3.rq` rewrites old `skill:*`
  individual references to `skill-lib:*`.
