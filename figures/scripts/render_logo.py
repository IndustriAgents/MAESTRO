"""
MAESTRO — Logo renderer.

Generates the MAESTRO project logo: an industrial-AI dot composition
("Orchestrated Core") composed entirely of dots in deep-navy ink on white.

The mark layers a central orchestrator node, a hexagonal inner ring of
agent / capability nodes, a knowledge-graph mid ring, sixteen graduated
gear-tooth radial arms, and an outer dispersion field — reading as both
industrial (gear silhouette) and AI (propagating-decision motif).

Outputs land in ``figures/png/`` at 300 DPI plus an SVG vector master in
``figures/src/``.

Usage:
    python figures/scripts/render_logo.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle


# Matches PALETTE["ink"] in render_figures.py — kept as a literal so this
# script has no cross-file dependency.
INK = "#1F2A36"

CANVAS_HALF = 500.0  # Data-space half-extent for the full-bleed renders.
SQUARE_HALF = 380.0  # Tighter crop for the square favicon variant.

OUT_PNG_DIR = Path(__file__).resolve().parents[1] / "png"
OUT_SRC_DIR = Path(__file__).resolve().parents[1] / "src"


def _ring_positions(n: int, radius: float, phase: float = 0.0):
    angles = np.linspace(0.0, 2 * np.pi, n, endpoint=False) + phase
    return [(radius * np.cos(a), radius * np.sin(a)) for a in angles]


def _add_dot(ax, x: float, y: float, r: float) -> None:
    ax.add_patch(Circle((x, y), radius=r, facecolor=INK,
                        edgecolor="none", linewidth=0))


def _draw_logo(ax) -> None:
    # 1) Core orchestrator node.
    _add_dot(ax, 0.0, 0.0, 18.0)

    # 2) Inner hex ring — 6 agent / capability nodes (flat-top hexagon).
    for (x, y) in _ring_positions(6, radius=90.0, phase=np.pi / 6):
        _add_dot(ax, x, y, 10.0)

    # 3) Mid ring — 12 knowledge-graph nodes.
    for (x, y) in _ring_positions(12, radius=180.0):
        _add_dot(ax, x, y, 6.0)

    # 4) Gear-tooth radial arms — 16 arms × 3 graduated dots.
    arm_steps = [(240.0, 7.0), (300.0, 4.0), (360.0, 2.0)]
    for (ux, uy) in _ring_positions(16, radius=1.0):
        for (r_pos, dot_r) in arm_steps:
            _add_dot(ax, ux * r_pos, uy * r_pos, dot_r)

    # 5) Dispersion field — seeded random halo for depth / motion.
    rng = np.random.default_rng(42)
    n = 80
    r = rng.uniform(360.0, 460.0, size=n)
    theta = rng.uniform(0.0, 2 * np.pi, size=n)
    for ri, ti in zip(r, theta):
        _add_dot(ax, ri * np.cos(ti), ri * np.sin(ti), 1.5)


def _make_figure(*, square: bool):
    px = 512 if square else 1024
    inches = px / 300.0
    fig, ax = plt.subplots(figsize=(inches, inches), dpi=300)
    half = SQUARE_HALF if square else CANVAS_HALF
    ax.set_xlim(-half, half)
    ax.set_ylim(-half, half)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    _draw_logo(ax)
    return fig


def main() -> None:
    OUT_PNG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_SRC_DIR.mkdir(parents=True, exist_ok=True)

    # 1) 1024×1024 on white + SVG vector master from the same figure.
    fig = _make_figure(square=False)
    fig.patch.set_facecolor("white")
    fig.savefig(OUT_PNG_DIR / "maestro-logo.png", dpi=300, facecolor="white")
    fig.savefig(OUT_SRC_DIR / "maestro-logo.svg", facecolor="white")
    plt.close(fig)

    # 2) 1024×1024 transparent.
    fig = _make_figure(square=False)
    fig.savefig(OUT_PNG_DIR / "maestro-logo-transparent.png",
                dpi=300, transparent=True)
    plt.close(fig)

    # 3) 512×512 tight-crop square (white).
    fig = _make_figure(square=True)
    fig.patch.set_facecolor("white")
    fig.savefig(OUT_PNG_DIR / "maestro-logo-square.png",
                dpi=300, facecolor="white")
    plt.close(fig)

    print("Logo outputs written:")
    for p in [
        OUT_PNG_DIR / "maestro-logo.png",
        OUT_PNG_DIR / "maestro-logo-transparent.png",
        OUT_PNG_DIR / "maestro-logo-square.png",
        OUT_SRC_DIR / "maestro-logo.svg",
    ]:
        print(f"  {p}")


if __name__ == "__main__":
    main()
