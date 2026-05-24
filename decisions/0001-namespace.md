# ADR-0001: Permanent namespace under w3id.org

- **Status:** Accepted
- **Date:** 2026-05-23
- **Supersedes:** the `http://example.org/maestro/*` IRIs used in 0.1.0 and 0.2.0

## Context

Through 0.2.0, every IRI in MAESTRO was anchored under `http://example.org/maestro/*`.
`example.org` is reserved by RFC 2606 for documentation and examples and must
not be used for any published ontology. Anyone deploying MAESTRO into a real
triplestore or federating its IRIs with other linked data would have to migrate
every identifier before doing so.

## Decision

Adopt the W3ID Permanent Identifier Service (`https://w3id.org`) as the IRI
authority for all MAESTRO ontologies. The base IRI becomes:

```
https://w3id.org/maestro/
```

Per-module ontology IRIs follow the existing pattern, e.g.:

| Module | Ontology IRI | Term IRI form |
|---|---|---|
| core | `https://w3id.org/maestro/core` | `https://w3id.org/maestro/core#Resource` |
| skill | `https://w3id.org/maestro/skill` | `https://w3id.org/maestro/skill#MotionSkill` |
| skill-lib (new) | `https://w3id.org/maestro/skill-lib` | `https://w3id.org/maestro/skill-lib#Transfer` |

Every module additionally carries an `owl:versionIRI` of the form
`https://w3id.org/maestro/<module>/0.3.0` so that downstream consumers can
pin a specific release.

## Consequences

- Every triple under the old IRI scheme must be migrated. `rules/migrate-0.2-to-0.3.rq`
  provides a SPARQL UPDATE that rewrites all `http://example.org/maestro` prefixes.
- A w3id redirect needs to be registered in the
  [perma-id/w3id.org](https://github.com/perma-id/w3id.org) repository so that
  the IRIs resolve to the GitHub Pages site of this repository (or to a
  pyLODE/Widoco-generated documentation site).
- Until the redirect lands, IRIs are still well-formed and unique — they just
  return 404 in a browser.
