# Example - Transfer Arm Plant

Single-cell example: one `res:TransferArm` carrying a `res:VacuumUnit`,
driven by three logical control components.

| Skill | Control component | Adapter |
|---|---|---|
| `skill:MoveLinear` | `ex:MoveItNode` | ROS / MoveIt |
| `skill:VacuumPick` | `ex:VacuumControlFB` | IEC 61131 PLC FB |
| `skill:Transfer` | `ex:FB_TransferCoordinator` | IEC 61499 CompositeFB |

The composite `skill:Transfer` is also exposed through
`ex:OpcUaTransferInterface`.

## Reasoning Chain

```text
cap:PickPlaceCapability cap:realizedBySkill skill:Transfer
skill:Transfer skill:composedOfSkill skill:MoveLinear
skill:Transfer skill:composedOfSkill skill:VacuumPick

ex:MoveItNode ros:implementsSkill skill:MoveLinear
ex:MoveItNode ros:controlsResource ex:TransferArm1

ex:VacuumControlFB plc:implementsSkill skill:VacuumPick
ex:VacuumControlFB plc:controlsResource ex:VacuumUnit1

ex:FB_TransferCoordinator iec61499:implementsSkill skill:Transfer
ex:FB_TransferCoordinator iec61499:controlsResource ex:TransferArm1

INFERRED: ex:TransferArm1 core:canPerform cap:PickPlaceCapability
INFERRED: ex:Plant1 core:canManufacture ex:ProductA
```

## Running

```python
from pathlib import Path
import rdflib

g = rdflib.Graph()
for path in Path("ontologies").glob("**/*.ttl"):
    g.parse(path, format="turtle")
g.parse("examples/transfer-arm/plant.ttl", format="turtle")
g.parse("examples/transfer-arm/product.ttl", format="turtle")

for triple in g.query(Path("rules/capability-inference.rq").read_text()):
    g.add(triple)

for row in g.query(Path("queries/01-resources-with-capability.rq").read_text()):
    print(row)
```

The repository-level regression check runs the same core path:

```bash
python tests/validate_repo.py
```
