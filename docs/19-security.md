# 19. Security Ontology (IEC 62443) + Safety/Security Convergence

`ontologies/cross-cutting/security.ttl` adds **OT cybersecurity** to
MAESTRO, complementing the **functional safety** already in
`safety.ttl`. The two together let the knowledge graph reason about the
**safety/security convergence** that matters on a cyber-physical plant:
a cyber attack that ends in a physical hazard.

## Why a separate module

`safety.ttl` is *functional safety* (IEC 61508 / ISO 13849 — SIL, PL,
hazards, emergency stop). It answers "can the machine hurt someone, and
is that mitigated?". It says nothing about *who can reach the control
network*. Cybersecurity (IEC 62443) is a distinct concern with its own
vocabulary — zones, conduits, threats, vulnerabilities, controls, and
security levels SL1–SL4 — so it lives in its own module.

## Vocabulary

| Class | Meaning (IEC 62443) |
|---|---|
| `security:SecurityZone` | Assets sharing common security requirements |
| `security:Conduit` | Channels connecting two zones |
| `security:Threat` | Potential cause of an unwanted incident |
| `security:Vulnerability` | Exploitable weakness |
| `security:SecurityControl` | Countermeasure |
| `security:SecurityRisk` | A cyber risk — **subclass of `safety:Risk`** |
| `security:SecurityLevel` | `SL1`–`SL4` |

Key relations: `hasSecurityLevel`, `connectsZones`, `locatedInZone`,
`securesChannel` (→ `com:Channel`), `protects`, `mitigatesThreat`,
`exposedTo`, `exploits`, `hasVulnerability`, `posesRisk`.

## The convergence link

```turtle
security:triggersHazard  rdfs:domain security:Threat ;
                         rdfs:range  safety:Hazard .
```

A `Threat` that `triggersHazard` a `safety:Hazard` connects the two
worlds. Because `security:SecurityRisk ⊑ safety:Risk`, cyber and
physical risk also share one root. This makes a single query able to
ask: *which hazards are reachable from a cyber threat, and are they
covered by **both** a `SecurityControl` and a `SafetyFunction`?*

`security.ttl` `owl:imports` `safety.ttl` so `triggersHazard` can carry
a typed range.

## Worked example

`examples/distribution-station/security.ttl` models the Festo DS:

- **Functional safety**: `ex:DS_EStop` (SIL 2, PL d) mitigates
  `ex:PinchHazardAtMagazine`, protects `ex:FeederUnit1`, and reaches
  `ex:SafeTorqueOff`. The IEC 61499 application `core:dependsOn` it.
- **Cybersecurity**: a `ControlZone` (SL2, the PLC + OPC UA server) and a
  `FieldZone` (SL1), joined by `ex:ControlConduit`, which
  `securesChannel ex:DS_OpcUaChannel`. `ex:MitmThreat` exploits an
  unauthenticated-OPC-UA vulnerability and **`triggersHazard`** the
  pinch hazard; `ex:OpcUaAuth` mitigates it.

## Validation & queries

- `constraints/shapes-security.ttl`: a zone has exactly one security
  level; a conduit connects exactly two zones; (warnings) a threat
  should be mitigated, and a cyber-triggerable hazard should also have a
  mitigating safety function.
- `queries/ds-04-security-exposure.rq` lists exposed assets, the hazard
  each threat can trigger, and the mitigating control.
- `CQ07` answers "which assets are exposed to a cyber threat that can
  trigger a physical hazard?".

> **Scope.** This is an IEC-62443-*aligned* vocabulary for reasoning
> over zones/conduits/threats — not a conformance tool. See
> `docs/04-standard-alignment.md` for the bridge-axiom policy.
