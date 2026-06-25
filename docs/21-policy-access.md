# 21 — Policy / Access Control / Modes (new in 0.4.0 — HHM-Core P3)

> *See [`policy.ttl`](../ontologies/cross-cutting/policy.ttl) and the priority map in
> [19-hhm-core-bridge.md](19-hhm-core-bridge.md).*

The policy module adds the governance cluster MAESTRO previously lacked entirely:
**who** may run **what**, in **which operating mode**, backed by **what evidence**.
`Policy` / `Permission` / `Prohibition` are bridged to **ODRL 2.2**; `Role`, `Mode`
and `Evidence` are MAESTRO-local but referenced by the policy. Full ODRL is bundled
for reference only in [`references/odrl22.ttl`](../references/odrl22.ttl) (not imported).

SHACL remains the enforcement mechanism — a policy *describes* governance; the
shapes in [`constraints/shapes-policy.ttl`](../constraints/shapes-policy.ttl) *enforce* it.

## Classes

| Class | `rdfs:subClassOf` | Purpose |
|---|---|---|
| `policy:Policy` | `odrl:Policy` | A group of permissions/prohibitions governing skills, steps, modules or endpoints |
| `policy:Permission` | `odrl:Permission` | Ability to perform an action over a target |
| `policy:Prohibition` | `odrl:Prohibition` | Inability to perform an action over a target |
| `policy:Role` | `core:LogicalEntity` | An actor role to which permissions are granted (RBAC) |
| `policy:Mode` | `core:LogicalEntity` | An operating mode — individuals `AutoMode` · `ManualMode` · `MaintenanceMode` |
| `policy:Evidence` | `core:LogicalEntity` | An audit/observation reference backing a decision |

## Properties

`policy:contains` (→ `core:Constraint`), `policy:hasPermission`,
`policy:hasProhibition`, `policy:grantedTo` (Permission → Role),
`policy:requiresPermission`, `policy:requiresMode` (→ `Mode`),
`policy:hasEvidence`.

## Example

```turtle
ex:OpPolicy a policy:Policy ;
    policy:contains       ex:Constraint1 ;     # core:Constraint core:constrains skill-lib:Transfer
    policy:hasPermission  ex:Perm1 ;
    policy:requiresMode   policy:AutoMode ;
    policy:hasEvidence    ex:Ev1 .

ex:Perm1 a policy:Permission ;
    policy:grantedTo ex:OperatorRole .         # ex:OperatorRole a policy:Role
```

## Relationship to safety

The same release reified safety mitigation: `safety:Mitigation` with
`safety:increases` / `safety:reduces`, plus the additive `core:constrains`
property a `core:Constraint` uses to point at its target. A policy's
`policy:contains` edge reuses `core:Constraint`, so access rules and safety
constraints share one constraint vocabulary. See the hazard/risk/mitigation
block in [`examples/hhm-bridge/plant.ttl`](../examples/hhm-bridge/plant.ttl).
