# Architecture Figures

Publication-quality architecture diagrams used by the project
[`README.md`](../README.md) and the [`docs/`](../docs/) pages.

The canonical figures are rendered procedurally in Python — same visual
style across all seven, reproducible by anyone with `matplotlib`,
versionable as code. PlantUML sources are also kept as a textual fallback.

## Rendering (recommended — matplotlib)

The matplotlib renderer in [`scripts/render_figures.py`](scripts/render_figures.py)
produces seven 300 DPI PNGs into [`png/`](png/) with a shared style
inspired by academic / "PaperBanana" aesthetics: muted palette, clean
sans-serif typography, generous whitespace, hairline borders.

```bash
# from the repository root
pip install matplotlib
python figures/scripts/render_figures.py
```

Output:

```
figures/png/01-semantic-stack.png
figures/png/02-modular-stack.png
figures/png/03-skill-hierarchy.png
figures/png/04-reasoning-chain.png
figures/png/05-llm-graphdb-pipeline.png
figures/png/06-final-architecture.png
figures/png/07-graphdb-named-graphs.png
```

To tweak the look — palette, fonts, box style — edit the constants at
the top of `scripts/render_figures.py` (`PALETTE`, `plt.rcParams`,
`BoxStyle`) and re-run.

## Rendering (alternative — PlantUML)

The original PlantUML sources are kept in [`src/`](src/) for users who
prefer the PlantUML look. You need either the `plantuml` CLI or
`plantuml.jar` (which needs Java).

```bash
plantuml -tpng figures/src/*.puml -o ../png        # PNG
plantuml -tsvg figures/src/*.puml -o ../svg        # SVG
```

> **Note.** The PlantUML and matplotlib outputs land in the same
> `figures/png/` directory and use the same basenames — running one will
> overwrite the other. The matplotlib renderer is the authoritative source
> for the README's embedded figures.

## Diagram catalogue

| # | PNG output | PlantUML | README section | Description |
|---|---|---|---|---|
| 01 | `png/01-semantic-stack.png` | [`src/01-semantic-stack.puml`](src/01-semantic-stack.puml) | §2 | Nine-layer semantic stack |
| 02 | `png/02-modular-stack.png` | [`src/02-modular-stack.puml`](src/02-modular-stack.puml) | §3 | Modular ontology stack with umbrella |
| 03 | `png/03-skill-hierarchy.png` | [`src/03-skill-hierarchy.puml`](src/03-skill-hierarchy.puml) | §8 | Skill class hierarchy |
| 04 | `png/04-reasoning-chain.png` | [`src/04-reasoning-chain.puml`](src/04-reasoning-chain.puml) | §19 | Core reasoning chain |
| 05 | `png/05-llm-graphdb-pipeline.png` | [`src/05-llm-graphdb-pipeline.puml`](src/05-llm-graphdb-pipeline.puml) | §22 | LLM + GraphDB pipeline |
| 06 | `png/06-final-architecture.png` | [`src/06-final-architecture.puml`](src/06-final-architecture.puml) | §25 | Final future-proof architecture |
| 07 | `png/07-graphdb-named-graphs.png` | [`src/07-graphdb-named-graphs.puml`](src/07-graphdb-named-graphs.puml) | §21 | GraphDB named graphs |
| **08** | `png/08-package-architecture.png` | — *(matplotlib only)* | §3 | UML package diagram with `«import»` edges (CaSkMan style) |
| **09** | `png/09-standards-honeycomb.png` | — *(matplotlib only)* | §4 | Standards alignment honeycomb (CaSkMan style) |
| **10** | `png/10-class-alignment.png` | — *(matplotlib only)* | §5 / §19 | Class alignment diagram, two-colour core/adapter view (CaSkMan style) |

Figures **08–10** are inspired by the three diagrams in the
[CaSkade-Automation/CaSkMan](https://github.com/CaSkade-Automation/CaSkMan)
paper (UML package view, ODP honeycomb, class alignment) and are
rendered exclusively by the matplotlib script — they have no PlantUML
counterpart.

## Visual style notes

The matplotlib renderer aims for an academic-paper aesthetic:

- **Palette.** Cool blues for the demand side (product / process),
  warm amber for the keystone Skill layer, lavender for execution
  adapters, sage for resources, and cool blue again for motion — a
  cool–warm–cool progression that visually reinforces the layering.
- **Typography.** DejaVu Sans (cross-platform default with metrics
  matching Arial / Helvetica). Titles 15 pt bold, layer labels 11–12 pt
  bold, sublabels 8.5–9 pt italic in a muted grey.
- **Boxes.** Rounded `FancyBboxPatch` with `lw=0.9` hairline borders.
  The keystone (Skill) layer gets a thicker `lw=1.4` border to mark it.
- **Arrows.** `FancyArrowPatch` with `style="-|>"`, `lw=1.0–1.1`,
  consistent across all figures.
- **Whitespace.** A reserved `TITLE_BAND` (1.5 units) at the top of
  every figure keeps title text from colliding with diagram content.
- **DPI.** 300 — print-grade.

Inspiration: [PaperBanana](https://github.com/dwzhu-pku/PaperBanana)
academic-illustration aesthetic. PaperBanana itself is a multi-agent
generative pipeline; the figures here are hand-coded to the same
publication-quality bar.
