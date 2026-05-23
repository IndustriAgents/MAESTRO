# Example - Multi-Robot Assembly Cell

Two cobots, one conveyor, and one assembly station coordinated through
ROS nodes and an IEC 61499 cell-level function block.

| Resource | Role | Provided skills |
|---|---|---|
| `ex:CobotA` | Handler | MoveLinear, VacuumPick, Transfer |
| `ex:CobotB` | Motion resource | MoveLinear |
| `ex:Conveyor1` | Material transport | none |
| `ex:AssemblyStation1` | Fixturing | none |

This example shows that the same skill and capability vocabulary scales
from a single arm to a multi-resource workcell without changing ontology
definitions.

## Running

```python
from pathlib import Path
import rdflib

g = rdflib.Graph()
for path in Path("ontologies").glob("**/*.ttl"):
    g.parse(path, format="turtle")
g.parse("examples/multi-robot-assembly/plant.ttl", format="turtle")

query = Path("queries/05-llm-pipeline-template.rq").read_text()
for row in g.query(query):
    print(row)
```
