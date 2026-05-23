# MAESTRO Examples

Worked plant instances that exercise the MAESTRO stack:
resource -> skill -> capability -> process -> product.

| Example | Description |
|---|---|
| [`transfer-arm/`](transfer-arm/) | Single TransferArm + VacuumUnit. Demonstrates `core:canPerform cap:PickPlaceCapability` inference. |
| [`multi-robot-assembly/`](multi-robot-assembly/) | Two cobots + conveyor + assembly station using the same capability vocabulary. |

## Running An Example

```python
from pathlib import Path
import rdflib

g = rdflib.Graph()
for path in Path("ontologies").glob("**/*.ttl"):
    g.parse(path, format="turtle")
g.parse("examples/transfer-arm/plant.ttl", format="turtle")
g.parse("examples/transfer-arm/product.ttl", format="turtle")

print(f"Triples: {len(g)}")
```

For the full parse/query/materialization check, run:

```bash
python tests/validate_repo.py
```
