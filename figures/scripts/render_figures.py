"""
MAESTRO — Publication-quality figure renderer.

Generates all 7 architecture figures used in the README and docs.
Inspired by the PaperBanana / academic-paper aesthetic: muted palette,
clean sans-serif typography, generous whitespace, rounded boxes with
hairline borders, and a reserved title band above the diagram.

Outputs land in ``figures/png/`` at 300 DPI.

Usage:
    python figures/scripts/render_figures.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle


# ---------------------------------------------------------------------------
#  GLOBAL STYLE
# ---------------------------------------------------------------------------

PALETTE = {
    "ink":        "#1F2A36",
    "muted":      "#5C6B7A",
    "rule":       "#CFD8DC",
    "bg":         "#FFFFFF",
    "panel":      "#F7F9FB",

    "product":    "#D6E4F0",
    "process":    "#C5DDEE",
    "capability": "#FCE7A2",
    "skill":      "#F4B860",
    "orchestr":   "#E0DAF0",
    "execution":  "#F5C8C5",
    "resource":   "#C7E2B4",
    "motion":     "#B8DCEB",
    "factory":    "#D0D5DA",

    "cat_core":   "#D6E4F0",
    "cat_phys":   "#FDE2C7",
    "cat_logic":  "#F4C2C2",
    "cat_exec":   "#E0DAF0",
    "cat_rt":     "#C7E8D1",
    "cat_cross":  "#E5EFC8",
    "cat_reas":   "#FFF1B8",
    "cat_umbr":   "#F4B860",
}

plt.rcParams.update({
    "font.family":        "DejaVu Sans",
    "font.size":          10,
    "axes.edgecolor":     PALETTE["ink"],
    "axes.linewidth":     0.6,
    "savefig.dpi":        300,
    "savefig.facecolor":  PALETTE["bg"],
    "savefig.bbox":       "tight",
    "savefig.pad_inches": 0.25,
    "figure.facecolor":   PALETTE["bg"],
    "figure.dpi":         150,
})


# ---------------------------------------------------------------------------
#  DRAWING HELPERS
# ---------------------------------------------------------------------------

# Reserved space at top of each figure for the title and subtitle.
TITLE_BAND = 1.5


@dataclass
class BoxStyle:
    fill: str = PALETTE["panel"]
    edge: str = PALETTE["ink"]
    lw:   float = 0.9
    pad:  float = 0.02
    rounding: float = 0.04


def draw_box(ax, x, y, w, h, *, label, sublabel=None,
             style: BoxStyle | None = None, fontsize=10,
             fontweight="bold", subfontsize=8.5,
             text_color=None):
    """Rounded rectangle with bold title + optional subtitle, centred."""
    style = style or BoxStyle()
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={style.pad},rounding_size={style.rounding}",
        linewidth=style.lw,
        edgecolor=style.edge,
        facecolor=style.fill,
    )
    ax.add_patch(box)
    cx, cy = x + w / 2, y + h / 2
    text_color = text_color or PALETTE["ink"]
    if sublabel:
        ax.text(cx, cy + 0.13 * h, label,
                ha="center", va="center",
                fontsize=fontsize, fontweight=fontweight,
                color=text_color)
        ax.text(cx, cy - 0.20 * h, sublabel,
                ha="center", va="center",
                fontsize=subfontsize, color=PALETTE["muted"],
                style="italic")
    else:
        ax.text(cx, cy, label,
                ha="center", va="center",
                fontsize=fontsize, fontweight=fontweight,
                color=text_color)


def draw_arrow(ax, x1, y1, x2, y2, *, label=None, color=None,
               lw=1.0, style="-|>", curve=0.0, fontsize=8.5,
               label_offset=(0, 0)):
    """Clean directional arrow with optional centred label."""
    color = color or PALETTE["ink"]
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style,
        mutation_scale=12,
        linewidth=lw,
        color=color,
        connectionstyle=f"arc3,rad={curve}",
        zorder=2,
    )
    ax.add_patch(arrow)
    if label:
        mx = (x1 + x2) / 2 + label_offset[0]
        my = (y1 + y2) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center",
                fontsize=fontsize, color=PALETTE["muted"],
                bbox=dict(facecolor=PALETTE["bg"], edgecolor="none",
                          pad=1.5))


def setup_axes(ax, xlim, ylim, title=None, subtitle=None,
               title_band=TITLE_BAND):
    """Reserve ``title_band`` units at the top of ``ylim`` for title text.

    Diagrams must keep their content below ``ylim[1] - title_band``.
    """
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    cx = (xlim[0] + xlim[1]) / 2
    if title:
        ax.text(cx, ylim[1] - title_band * 0.35, title,
                ha="center", va="center",
                fontsize=15, fontweight="bold",
                color=PALETTE["ink"])
    if subtitle:
        ax.text(cx, ylim[1] - title_band * 0.72, subtitle,
                ha="center", va="center",
                fontsize=10, color=PALETTE["muted"],
                style="italic")


def save(fig, name, out_dir):
    out_path = Path(out_dir) / f"{name}.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    return out_path


# ---------------------------------------------------------------------------
#  FIGURE 1 — Semantic Stack
# ---------------------------------------------------------------------------

def fig_01_semantic_stack(out_dir):
    fig, ax = plt.subplots(figsize=(7.5, 11))

    layers = [
        ("Product Layer",        "prod:Product · prod:Part · prod:Assembly",   PALETTE["product"]),
        ("Process Layer",        "proc:ManufacturingProcess  (DIN 8580)",      PALETTE["process"]),
        ("Capability Layer",     "cap:Capability — what a plant CAN do",       PALETTE["capability"]),
        ("Skill Layer",          "skill:AtomicSkill · skill:CompositeSkill",   PALETTE["skill"]),
        ("Orchestration Layer",  "SPARQL · SHACL · SWRL · LLM",                PALETTE["orchestr"]),
        ("Execution Layer",      "ROS · IEC 61131 · IEC 61499 · OPC UA · AAS", PALETTE["execution"]),
        ("Resource Layer",       "res:Machine · res:Robot · res:Sensor",       PALETTE["resource"]),
        ("Motion Layer",         "motion:LinearMotion · JointMotion · …",      PALETTE["motion"]),
        ("Physical Factory",     "Real-world plant",                           PALETTE["factory"]),
    ]

    xlim = (0, 7.5)
    ylim = (0, 12.0)
    setup_axes(ax, xlim, ylim,
               title="MAESTRO — Semantic Stack",
               subtitle="Nine layers, each independent and replaceable")

    box_x, box_w = 1.0, 5.5
    box_h = 0.92
    gap = 0.11
    y_top_first = ylim[1] - TITLE_BAND - 0.20
    y0 = y_top_first - box_h     # bottom-y of first box

    # subtle panel band behind the stack
    band_top = y_top_first + 0.15
    band_h = (box_h + gap) * len(layers) + 0.15
    ax.add_patch(Rectangle((0.6, band_top - band_h), 6.3, band_h,
                           facecolor=PALETTE["panel"], edgecolor="none",
                           zorder=0))

    for i, (lab, sub, color) in enumerate(layers):
        y = y0 - i * (box_h + gap)
        style = BoxStyle(fill=color, edge=PALETTE["ink"],
                         lw=1.4 if lab == "Skill Layer" else 0.8)
        draw_box(ax, box_x, y, box_w, box_h,
                 label=lab, sublabel=sub, style=style,
                 fontsize=11, subfontsize=8.5)
        if i < len(layers) - 1:
            cx = box_x + box_w / 2
            draw_arrow(ax, cx, y, cx, y - gap, lw=1.0)

    # keystone callout (anchored to Skill Layer = index 3)
    skill_y = y0 - 3 * (box_h + gap)
    ax.annotate(
        "keystone\nabstraction",
        xy=(box_x + box_w, skill_y + box_h / 2),
        xytext=(box_x + box_w + 0.35, skill_y + box_h / 2),
        ha="left", va="center",
        fontsize=9, color=PALETTE["muted"], style="italic",
        arrowprops=dict(arrowstyle="-", color=PALETTE["muted"], lw=0.7),
    )

    return save(fig, "01-semantic-stack", out_dir)


# ---------------------------------------------------------------------------
#  FIGURE 2 — Modular Ontology Stack
# ---------------------------------------------------------------------------

def fig_02_modular_stack(out_dir):
    fig, ax = plt.subplots(figsize=(14, 10))
    xlim = (0, 14)
    ylim = (0, 11)
    setup_axes(ax, xlim, ylim,
               title="MAESTRO — Modular Ontology Stack",
               subtitle="24 .ttl modules, organised by concern, unified through maestro.ttl")

    # Umbrella node at top (below title band)
    umbrella_x, umbrella_y, umbrella_w, umbrella_h = 4.6, 8.0, 4.8, 0.90
    draw_box(ax, umbrella_x, umbrella_y, umbrella_w, umbrella_h,
             label="maestro.ttl",
             sublabel="top-level umbrella  ·  owl:imports every module",
             style=BoxStyle(fill=PALETTE["cat_umbr"], edge=PALETTE["ink"], lw=1.3),
             fontsize=12, subfontsize=8.8)
    ux, uy = umbrella_x + umbrella_w / 2, umbrella_y

    # Helper to draw category card with a list of modules stacked vertically.
    def draw_category(x, y, w, h, header, color, modules,
                      pill_cols=1, pill_h=0.36, pill_gap=0.08,
                      header_fs=11):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor=color, edgecolor=PALETTE["ink"], linewidth=0.9))
        ax.text(x + w / 2, y + h - 0.30, header,
                ha="center", va="top", fontsize=header_fs,
                fontweight="bold", color=PALETTE["ink"])
        # pills stacked vertically (single column by default)
        inner_pad = 0.18
        col_w = (w - inner_pad * (pill_cols + 1)) / pill_cols
        n = len(modules)
        rows_needed = (n + pill_cols - 1) // pill_cols
        first_y = y + h - 0.75
        for i, m in enumerate(modules):
            r, c = divmod(i, pill_cols)
            px = x + inner_pad + c * (col_w + inner_pad)
            py = first_y - r * (pill_h + pill_gap) - pill_h
            ax.add_patch(FancyBboxPatch(
                (px, py), col_w, pill_h,
                boxstyle="round,pad=0.01,rounding_size=0.05",
                facecolor="white", edgecolor=PALETTE["rule"], linewidth=0.55))
            ax.text(px + col_w / 2, py + pill_h / 2, m,
                    ha="center", va="center", fontsize=8.7,
                    color=PALETTE["ink"])
        return (x + w / 2, y + h)

    # Top row of categories (5 columns)
    row_y, row_h = 4.7, 2.85
    pad = 0.25
    n = 5
    total_w = 13.5
    col_w = (total_w - pad * (n - 1)) / n

    cat_row1 = [
        ("core",      PALETTE["cat_core"],
         ["manufacturing-core"]),
        ("physical",  PALETTE["cat_phys"],
         ["resource", "motion"]),
        ("logical",   PALETTE["cat_logic"],
         ["skill", "capability", "process", "product"]),
        ("execution", PALETTE["cat_exec"],
         ["iec61131", "iec61499", "ros", "opcua", "aas"]),
        ("runtime",   PALETTE["cat_rt"],
         ["runtime", "state"]),
    ]
    arrow_targets = []
    for i, (hdr, color, mods) in enumerate(cat_row1):
        x = 0.25 + i * (col_w + pad)
        tgt = draw_category(x, row_y, col_w, row_h, hdr, color, mods,
                            pill_cols=1)
        arrow_targets.append(tgt)

    # Bottom row: cross-cutting (wide, 2 columns) + reasoning (narrow, 1 column)
    row2_y, row2_h = 1.5, 2.85
    cross_w = 9.0
    reas_w = total_w - cross_w - pad
    tgt_cross = draw_category(0.25, row2_y, cross_w, row2_h,
                              "cross-cutting", PALETTE["cat_cross"],
                              ["sensor", "unit", "communication", "safety",
                               "quality", "maintenance", "energy"],
                              pill_cols=2)
    tgt_reas = draw_category(0.25 + cross_w + pad, row2_y, reas_w, row2_h,
                             "reasoning", PALETTE["cat_reas"],
                             ["reasoning", "planning"],
                             pill_cols=1)
    arrow_targets.extend([tgt_cross, tgt_reas])

    # Arrows from umbrella to each category
    for cx, cy in arrow_targets:
        offset_x = cx - ux
        curve = 0.0
        if abs(offset_x) > 0.5:
            curve = 0.06 if offset_x > 0 else -0.06
        draw_arrow(ax, ux, uy, cx, cy, lw=0.7,
                   color=PALETTE["muted"], style="-|>",
                   curve=curve)

    # Footnote
    ax.text(7.0, 0.55,
            "Importing  maestro.ttl  pulls in every module.   "
            "Each module declares its own owl:imports explicitly — the dependency graph is acyclic.",
            ha="center", va="center",
            fontsize=9.5, color=PALETTE["muted"], style="italic",
            bbox=dict(facecolor=PALETTE["panel"], edgecolor=PALETTE["rule"],
                      boxstyle="round,pad=0.45", lw=0.6))

    return save(fig, "02-modular-stack", out_dir)


# ---------------------------------------------------------------------------
#  FIGURE 3 — Skill Hierarchy
# ---------------------------------------------------------------------------

def fig_03_skill_hierarchy(out_dir):
    fig, ax = plt.subplots(figsize=(12, 8))
    xlim = (0, 12)
    ylim = (0, 9.0)
    setup_axes(ax, xlim, ylim,
               title="MAESTRO — Skill Class Hierarchy",
               subtitle="Skills are LOGICAL — execution technologies implement them")

    # Root box
    root_x, root_y, root_w, root_h = 5.2, 6.5, 1.6, 0.7
    draw_box(ax, root_x, root_y, root_w, root_h, label="core:Skill",
             style=BoxStyle(fill=PALETTE["skill"], edge=PALETTE["ink"], lw=1.3),
             fontsize=11)

    # Two children (further apart for clean trunk routing)
    child_w, child_h = 1.95, 0.65
    atomic_cx, compos_cx = 2.5, 9.5     # centre x
    children_y = 5.0                    # bottom y of children
    atomic_x = atomic_cx - child_w / 2
    compos_x = compos_cx - child_w / 2

    draw_box(ax, atomic_x, children_y, child_w, child_h,
             label="skill:AtomicSkill",
             style=BoxStyle(fill="#FCD9A8", edge=PALETTE["ink"], lw=1.0),
             fontsize=10)
    draw_box(ax, compos_x, children_y, child_w, child_h,
             label="skill:CompositeSkill",
             style=BoxStyle(fill="#FCD9A8", edge=PALETTE["ink"], lw=1.0),
             fontsize=10)

    rx, ry = root_x + root_w / 2, root_y
    # Root → children: straight lines (no overlap risk)
    draw_arrow(ax, rx, ry, atomic_cx, children_y + child_h,
               lw=0.9, style="-", color=PALETTE["ink"])
    draw_arrow(ax, rx, ry, compos_cx, children_y + child_h,
               lw=0.9, style="-", color=PALETTE["ink"])

    atomic_leaves = [
        "skill:MotionSkill",
        "skill:ManipulationSkill",
        "skill:HandlingSkill",
        "skill:InspectionSkill",
    ]
    composite_leaves = [
        "skill:AssemblySkill",
        "skill:WeldingSkill",
        "skill:CoordinationSkill",
        "skill:ProcessSkill",
        "skill:TransferSkill",
    ]

    leaf_w, leaf_h = 2.10, 0.46
    leaf_gap = 0.20

    # Trunk-and-branch routing for both columns.
    # Trunk drops from each child to a shared horizontal level, then branches
    # right (atomic) or left (composite) to each leaf's vertical centre.
    def draw_tree_column(parent_cx, parent_bottom, leaves,
                         leaf_x, leaf_align_right,
                         highlight_label=None):
        # Compute leaf positions
        leaves_top = 3.7
        ys = [leaves_top - i * (leaf_h + leaf_gap) for i in range(len(leaves))]
        # Trunk drop point: a little below parent_bottom
        trunk_y_top = parent_bottom - 0.15
        trunk_y_bottom = ys[-1] + leaf_h / 2
        # Vertical trunk
        ax.plot([parent_cx, parent_cx],
                [trunk_y_top, trunk_y_bottom],
                color=PALETTE["muted"], lw=0.7, zorder=1)
        # Short stub from parent bottom to trunk start
        ax.plot([parent_cx, parent_cx],
                [parent_bottom, trunk_y_top],
                color=PALETTE["muted"], lw=0.7, zorder=1)
        # Branches
        for y, lab in zip(ys, leaves):
            cy = y + leaf_h / 2
            edge_x = (leaf_x + leaf_w) if leaf_align_right else leaf_x
            # horizontal branch
            ax.plot([parent_cx, edge_x],
                    [cy, cy],
                    color=PALETTE["muted"], lw=0.7, zorder=1)
            is_highlight = lab == highlight_label
            style = BoxStyle(
                fill="#F4D3C3" if is_highlight else "#FFEDD5",
                edge=PALETTE["ink"],
                lw=1.2 if is_highlight else 0.7)
            draw_box(ax, leaf_x, y, leaf_w, leaf_h, label=lab,
                     style=style, fontsize=9,
                     fontweight="bold" if is_highlight else "normal")

    # Atomic column: trunk on right of atomic-child, leaves on the right
    draw_tree_column(atomic_cx, children_y,
                     atomic_leaves,
                     leaf_x=atomic_cx + 0.55,
                     leaf_align_right=False)
    # Composite column: trunk on left of composite-child, leaves on the left
    draw_tree_column(compos_cx, children_y,
                     composite_leaves,
                     leaf_x=compos_cx - 0.55 - leaf_w,
                     leaf_align_right=True,
                     highlight_label="skill:TransferSkill")

    # Composition annotation (centre, below)
    ax.text(6.0, 0.65,
            "Composite skills declare their structure via  core:requires\n"
            "e.g.   skill:TransferSkill   →   MoveLinear  +  VacuumPick  +  Release",
            ha="center", va="center", fontsize=9.7,
            color=PALETTE["muted"], style="italic",
            bbox=dict(facecolor=PALETTE["panel"], edgecolor=PALETTE["rule"],
                      boxstyle="round,pad=0.45", lw=0.6))

    return save(fig, "03-skill-hierarchy", out_dir)


# ---------------------------------------------------------------------------
#  FIGURE 4 — Reasoning Chain
# ---------------------------------------------------------------------------

def fig_04_reasoning_chain(out_dir):
    fig, ax = plt.subplots(figsize=(10, 12))
    xlim = (0, 10)
    ylim = (0, 13.5)
    setup_axes(ax, xlim, ylim,
               title="MAESTRO — Core Reasoning Chain",
               subtitle="From product intent to physical motion — the canonical inference path")

    nodes = [
        ("Product",          "prod:Product",                          PALETTE["product"]),
        ("Process",          "proc:ManufacturingProcess",             PALETTE["process"]),
        ("Capability",       "cap:Capability",                        PALETTE["capability"]),
        ("Skill",            "skill:AtomicSkill / CompositeSkill",    PALETTE["skill"]),
        ("ControlComponent", "implemented by execution adapter",      PALETTE["execution"]),
        ("Resource",         "res:Machine · res:Robot · res:Sensor",  PALETTE["resource"]),
        ("Motion",           "motion:LinearMotion · JointMotion · …", PALETTE["motion"]),
    ]
    relations = ["requires", "requires", "realizedBy", "implementedBy",
                 "controls", "performs"]

    box_x, box_w = 2.3, 5.2
    box_h = 0.92
    gap = 0.62
    y_top_first = ylim[1] - TITLE_BAND - 0.20
    y0 = y_top_first - box_h
    centres = []
    for i, (lab, sub, color) in enumerate(nodes):
        y = y0 - i * (box_h + gap)
        is_keystone = lab == "Skill"
        draw_box(ax, box_x, y, box_w, box_h,
                 label=lab, sublabel=sub,
                 style=BoxStyle(fill=color, edge=PALETTE["ink"],
                                lw=1.4 if is_keystone else 0.9),
                 fontsize=12, subfontsize=9)
        centres.append((box_x + box_w / 2, y, y + box_h))

    for i in range(len(nodes) - 1):
        cx, y_bot, _ = centres[i]
        _, _, y_top_next = centres[i + 1]
        draw_arrow(ax, cx, y_bot, cx, y_top_next, lw=1.1)
        my = (y_bot + y_top_next) / 2
        ax.text(cx + 0.30, my, relations[i],
                ha="left", va="center",
                fontsize=10, color=PALETTE["muted"], style="italic")

    # ControlComponent side-fan
    adapters = ["ROS node", "PLC FB", "IEC 61499 FB", "OPC UA method", "AAS operation"]
    ad_y = centres[4][1] + box_h / 2
    ad_x = box_x + box_w + 0.35
    pill_w, pill_h = 1.65, 0.40
    pill_gap = 0.06
    n = len(adapters)
    total_h = n * pill_h + (n - 1) * pill_gap
    start_y = ad_y - total_h / 2
    for i, name in enumerate(adapters):
        py = start_y + i * (pill_h + pill_gap)
        ax.add_patch(FancyBboxPatch(
            (ad_x, py), pill_w, pill_h,
            boxstyle="round,pad=0.02,rounding_size=0.05",
            facecolor="#F2DDDB", edgecolor=PALETTE["ink"], linewidth=0.65))
        ax.text(ad_x + pill_w / 2, py + pill_h / 2, name,
                ha="center", va="center",
                fontsize=8.8, color=PALETTE["ink"])
    # bracket spine
    ax.add_patch(Rectangle((ad_x - 0.20, start_y), 0.05, total_h,
                           facecolor=PALETTE["muted"], edgecolor="none"))
    # short bracket arrow tying ControlComponent → fan
    draw_arrow(ax, box_x + box_w, ad_y, ad_x - 0.20, ad_y,
               lw=0.8, color=PALETTE["muted"], style="-")

    return save(fig, "04-reasoning-chain", out_dir)


# ---------------------------------------------------------------------------
#  FIGURE 5 — LLM + GraphDB Pipeline
# ---------------------------------------------------------------------------

def fig_05_llm_pipeline(out_dir):
    fig, ax = plt.subplots(figsize=(15, 7.0))
    xlim = (0, 15)
    ylim = (0, 7.5)
    setup_axes(ax, xlim, ylim,
               title="MAESTRO — LLM + GraphDB Pipeline",
               subtitle="LLM owns intent and explanation; deterministic reasoning owns the decision")

    # Caption sub-text kept short so it fits within each box.
    stages = [
        ("User\nCommand",          "NL input",          "#E9EEF4"),
        ("LLM Intent\nExtraction", "entities",          "#E0DAF0"),
        ("SPARQL\nGeneration",     "fill template",     "#D0C7E8"),
        ("GraphDB\nReasoning",     "OWL · SHACL",       "#BDB1DD"),
        ("Capability\nInference",  "canPerform",        "#A99CD2"),
        ("LLM\nExplanation",       "NL answer",         "#C7DDF0"),
        ("Execution\nLayer",       "OPC UA / ROS",      "#C7E2B4"),
    ]

    n = len(stages)
    gap = 0.25
    margin = 0.40
    avail_w = xlim[1] - 2 * margin - gap * (n - 1)
    box_w = avail_w / n
    box_h = 2.05
    y_box = 2.8

    centres = []
    for i, (lab, sub, color) in enumerate(stages):
        x = margin + i * (box_w + gap)
        text_color = "#FFFFFF" if i in (3, 4) else PALETTE["ink"]
        sub_color = "#ECE7F4" if i in (3, 4) else PALETTE["muted"]
        ax.add_patch(FancyBboxPatch(
            (x, y_box), box_w, box_h,
            boxstyle="round,pad=0.02,rounding_size=0.09",
            facecolor=color, edgecolor=PALETTE["ink"], linewidth=0.9))
        ax.text(x + box_w / 2, y_box + box_h * 0.66, lab,
                ha="center", va="center", fontsize=10.5,
                fontweight="bold", color=text_color)
        ax.text(x + box_w / 2, y_box + box_h * 0.22, sub,
                ha="center", va="center", fontsize=8.6,
                color=sub_color, style="italic")
        centres.append((x, x + box_w))

    for i in range(n - 1):
        x_right = centres[i][1]
        x_left_next = centres[i + 1][0]
        my = y_box + box_h / 2
        draw_arrow(ax, x_right, my, x_left_next, my, lw=1.1)

    # caption block below
    ax.text(xlim[1] / 2, 1.05,
            "The LLM does two narrow text tasks — parse intent, render explanation.\n"
            "The decision (which resource, which skill, in which state) is taken by deterministic graph reasoning.",
            ha="center", va="center", fontsize=10,
            color=PALETTE["muted"], style="italic",
            bbox=dict(facecolor=PALETTE["panel"], edgecolor=PALETTE["rule"],
                      boxstyle="round,pad=0.55", lw=0.6))

    return save(fig, "05-llm-graphdb-pipeline", out_dir)


# ---------------------------------------------------------------------------
#  FIGURE 6 — Final Future-Proof Architecture
# ---------------------------------------------------------------------------

def fig_06_final_architecture(out_dir):
    fig, ax = plt.subplots(figsize=(10, 13))
    xlim = (0, 10)
    ylim = (0, 14.5)
    setup_axes(ax, xlim, ylim,
               title="MAESTRO — Final Future-Proof Architecture",
               subtitle="Industry 4.0 / 5.0 layered manufacturing semantics")

    spine_top = [
        ("Product Layer",     PALETTE["product"]),
        ("Process Layer",     PALETTE["process"]),
        ("Capability Layer",  PALETTE["capability"]),
        ("Skill Layer",       PALETTE["skill"]),
    ]
    box_w, box_h = 4.6, 0.9
    box_x = 2.7
    gap = 0.50
    y_top_first = ylim[1] - TITLE_BAND - 0.20
    y0 = y_top_first - box_h

    for i, (lab, color) in enumerate(spine_top):
        y = y0 - i * (box_h + gap)
        is_keystone = lab == "Skill Layer"
        draw_box(ax, box_x, y, box_w, box_h, label=lab,
                 style=BoxStyle(fill=color, edge=PALETTE["ink"],
                                lw=1.4 if is_keystone else 0.9),
                 fontsize=12)
        if i > 0:
            cx = box_x + box_w / 2
            draw_arrow(ax, cx, y + box_h + gap, cx, y + box_h, lw=1.0)

    skill_bottom_y = y0 - 3 * (box_h + gap)
    adapter_y = skill_bottom_y - 1.4
    adapter_h = 0.85
    adapter_w = 1.95
    adapter_specs = [
        ("ROS",        1.30, "#F5C8C5"),
        ("IEC 61131",  4.02, "#F5C8C5"),
        ("IEC 61499",  6.75, "#F5C8C5"),
    ]
    for name, ax_x, color in adapter_specs:
        draw_box(ax, ax_x, adapter_y, adapter_w, adapter_h, label=name,
                 style=BoxStyle(fill=color, edge=PALETTE["ink"], lw=0.9),
                 fontsize=11)
        draw_arrow(ax, box_x + box_w / 2, skill_bottom_y,
                   ax_x + adapter_w / 2, adapter_y + adapter_h, lw=0.9)

    opcua_y = adapter_y - 1.3
    draw_box(ax, box_x, opcua_y, box_w, box_h,
             label="OPC UA Layer",
             style=BoxStyle(fill="#D1C4E9", edge=PALETTE["ink"], lw=1.0),
             fontsize=12)
    for name, ax_x, _ in adapter_specs:
        draw_arrow(ax, ax_x + adapter_w / 2, adapter_y,
                   box_x + box_w / 2, opcua_y + box_h, lw=0.9)

    bottom_stack = [
        ("Resource Layer",   PALETTE["resource"]),
        ("Motion Layer",     PALETTE["motion"]),
        ("Physical Factory", PALETTE["factory"]),
    ]
    cur_y = opcua_y
    for lab, color in bottom_stack:
        cur_y -= (box_h + gap)
        draw_box(ax, box_x, cur_y, box_w, box_h, label=lab,
                 style=BoxStyle(fill=color, edge=PALETTE["ink"], lw=0.9),
                 fontsize=12)
        draw_arrow(ax, box_x + box_w / 2, cur_y + box_h + gap,
                   box_x + box_w / 2, cur_y + box_h, lw=1.0)

    return save(fig, "06-final-architecture", out_dir)


# ---------------------------------------------------------------------------
#  FIGURE 7 — GraphDB Named Graphs
# ---------------------------------------------------------------------------

def fig_07_named_graphs(out_dir):
    fig, ax = plt.subplots(figsize=(14, 8.5))
    xlim = (0, 14)
    ylim = (0, 9.5)
    setup_axes(ax, xlim, ylim,
               title="MAESTRO — GraphDB Named Graphs",
               subtitle="One module per named graph: separates design-time, run-time, and inferred data")

    rows = [
        (6.6,  "design-time · core",        PALETTE["cat_core"],
         ["graph/core", "graph/resource", "graph/motion"]),
        (5.2,  "design-time · logical",     PALETTE["cat_logic"],
         ["graph/skill", "graph/capability", "graph/process", "graph/product"]),
        (3.8,  "execution adapters",        PALETTE["cat_exec"],
         ["graph/ros", "graph/iec61131", "graph/iec61499", "graph/opcua", "graph/aas"]),
        (2.4,  "run-time",                  PALETTE["cat_rt"],
         ["graph/runtime", "graph/state"]),
        (1.0,  "reasoning",                 PALETTE["cat_reas"],
         ["graph/reasoning", "graph/planning"]),
    ]

    node_w, node_h = 1.80, 0.72
    label_x = 0.25
    label_w = 3.10              # reserve space for row labels
    start_x = label_x + label_w
    arrow_x = xlim[1] - 0.55
    gap_x = 0.20

    # Make sure 5 nodes fit
    max_nodes = max(len(items) for _, _, _, items in rows)
    avail = arrow_x - start_x - 0.35
    if max_nodes * node_w + (max_nodes - 1) * gap_x > avail:
        node_w = (avail - (max_nodes - 1) * gap_x) / max_nodes

    for y, header, color, items in rows:
        ax.text(label_x + 0.05, y + node_h / 2, header,
                ha="left", va="center", fontsize=10.5,
                fontweight="bold", color=PALETTE["muted"])
        # Separator line spans from start_x to arrow_x (does NOT cover label)
        ax.add_patch(Rectangle((start_x - 0.10, y - 0.20),
                               arrow_x - (start_x - 0.10), 0.015,
                               facecolor=PALETTE["rule"], edgecolor="none"))
        for i, name in enumerate(items):
            x = start_x + i * (node_w + gap_x)
            draw_box(ax, x, y, node_w, node_h, label=name,
                     style=BoxStyle(fill=color, edge=PALETTE["ink"], lw=0.7),
                     fontsize=9.4, fontweight="normal")

    # flow arrows between rows (right margin)
    for y_from, y_to in [(6.6, 5.2), (5.2, 3.8), (3.8, 2.4), (2.4, 1.0)]:
        draw_arrow(ax,
                   arrow_x, y_from - 0.05,
                   arrow_x, y_to + node_h + 0.05,
                   lw=0.9, color=PALETTE["muted"])

    return save(fig, "07-graphdb-named-graphs", out_dir)


# ---------------------------------------------------------------------------
#  ENTRY POINT
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
#  FIGURE 8 — UML Package Architecture (CaSkMan-paper style)
# ---------------------------------------------------------------------------

# Distinct palette for the CaSkMan-style figures.
CASK_PEACH = "#FCE3C0"      # ontology package fill (tan / peach)
CASK_BLUE  = "#3F89B0"      # structural class fill
CASK_BLUE_LIGHT = "#B9D6E3"
CASK_ORANGE = "#F7B26B"     # extension class fill
CASK_ORANGE_LIGHT = "#FCE3C0"
HEX_BLUE   = "#3FA9D0"      # abstract capabilities
HEX_RED    = "#C0185D"      # machine structure
HEX_YELLOW = "#D9B448"      # executable skills
HEX_GREY   = "#FAFAFA"      # cross-cutting / neutral


def draw_package(ax, x, y, w, h, *, label, fill=CASK_PEACH,
                 edge=PALETTE["ink"], lw=0.9, fontsize=10):
    """UML 'package' box: a small tab on the top-left, a body below.

    Two stacked rectangles produce the classic UML package silhouette.
    """
    tab_h = 0.22
    tab_w = max(0.8, min(w * 0.50, len(label) * 0.13 + 0.20))
    # Tab
    ax.add_patch(Rectangle((x, y + h), tab_w, tab_h,
                           facecolor=fill, edgecolor=edge, lw=lw))
    # Body
    ax.add_patch(Rectangle((x, y), w, h,
                           facecolor=fill, edgecolor=edge, lw=lw))
    # Label centred inside the body
    ax.text(x + w / 2, y + h / 2, label,
            ha="center", va="center",
            fontsize=fontsize, fontweight="bold",
            color=PALETTE["ink"])


def draw_dashed_import(ax, x1, y1, x2, y2, label="«import»",
                       color=PALETTE["ink"], lw=0.8, fontsize=8.5,
                       label_at=0.55):
    """Dashed UML-import arrow (open triangle) with «import» label."""
    line = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>",
        mutation_scale=11,
        linestyle=(0, (4, 3)),
        linewidth=lw,
        color=color,
        zorder=2,
    )
    ax.add_patch(line)
    if label:
        lx = x1 + (x2 - x1) * label_at
        ly = y1 + (y2 - y1) * label_at
        ax.text(lx, ly, label,
                ha="center", va="center",
                fontsize=fontsize, color=PALETTE["muted"], style="italic",
                bbox=dict(facecolor=PALETTE["bg"], edgecolor="none", pad=1.0))


def fig_08_package_architecture(out_dir):
    fig, ax = plt.subplots(figsize=(16, 10.5))
    xlim = (0, 16)
    ylim = (0, 11)
    setup_axes(ax, xlim, ylim,
               title="MAESTRO — Ontology Package Architecture",
               subtitle="UML package view: MAESTRO modules and the external standards they integrate")

    # Centre: maestro.ttl umbrella (slightly larger to be visually dominant)
    UC_W, UC_H = 2.6, 1.05
    UC_X = 8.0 - UC_W / 2
    UC_Y = 5.4
    draw_package(ax, UC_X, UC_Y, UC_W, UC_H, label="maestro.ttl",
                 fill=PALETTE["cat_umbr"], lw=1.4, fontsize=13)
    umb_cx, umb_cy = UC_X + UC_W / 2, UC_Y + UC_H / 2

    # Inner ring: the seven MAESTRO category modules (well-spread).
    inner_modules = [
        # (cx, cy, label)
        (4.4,  8.4, "core"),
        (6.6,  9.1, "physical"),
        (9.4,  9.1, "logical"),
        (11.6, 8.4, "execution"),
        (12.4, 4.5, "runtime"),
        (10.0, 2.0, "cross-cutting"),
        (4.0,  2.0, "reasoning"),
    ]
    inner_w, inner_h = 1.80, 0.85
    inner_cxcy = {}
    for cx, cy, lab in inner_modules:
        bx, by = cx - inner_w / 2, cy - inner_h / 2
        draw_package(ax, bx, by, inner_w, inner_h, label=lab,
                     fill=CASK_PEACH, lw=1.0, fontsize=10.5)
        inner_cxcy[lab] = (cx, cy)
        # Inner module → umbrella: short clean arrow, NO label (label clutters centre)
        # connect from edge of inner to edge of umbrella
        dx = umb_cx - cx
        dy = umb_cy - cy
        # Use a slight curve so multiple incoming arrows don't overlap visually
        draw_dashed_import(ax, cx, cy, umb_cx, umb_cy,
                           label=None, lw=0.7,
                           color=PALETTE["muted"])

    # Outer ring: external standards (kept FAR from centre so labels don't pile up)
    outer_modules = [
        # left column
        (1.5, 9.6, "DIN 8580",      "logical"),
        (1.5, 8.1, "VDI 3682",      "logical"),
        (1.5, 6.6, "VDI 2860",      "logical"),
        (1.5, 5.1, "ISA-95",        "reasoning"),
        (1.5, 3.6, "PackML",        "runtime"),

        # right column
        (14.6, 9.6, "OPC UA",       "execution"),
        (14.6, 8.1, "IEC 61131",    "execution"),
        (14.6, 6.6, "IEC 61499",    "execution"),
        (14.6, 5.1, "ROS 2",        "execution"),
        (14.6, 3.6, "AAS",          "execution"),

        # bottom row
        (5.8, 0.9, "SSN / SOSA",    "cross-cutting"),
        (8.0, 0.7, "QUDT",          "cross-cutting"),
        (10.2, 0.9, "IEC 61508",    "cross-cutting"),
    ]
    outer_w, outer_h = 1.55, 0.72
    # Show «import» label on FIRST arrow per target only (avoid pileup)
    label_used = set()
    for cx, cy, lab, target in outer_modules:
        bx, by = cx - outer_w / 2, cy - outer_h / 2
        draw_package(ax, bx, by, outer_w, outer_h, label=lab,
                     fill="#FBEFD8", lw=0.8, fontsize=9.5)
        tx, ty = inner_cxcy[target]
        show_label = target not in label_used
        label_used.add(target)
        draw_dashed_import(ax, cx, cy, tx, ty,
                           label="«import»" if show_label else None,
                           lw=0.65, color=PALETTE["muted"], fontsize=8,
                           label_at=0.45)

    # Legend — placed in the bottom-left whitespace
    LX, LY = 0.4, 0.30
    ax.add_patch(FancyBboxPatch(
        (LX, LY), 4.0, 0.45,
        boxstyle="round,pad=0.05,rounding_size=0.05",
        facecolor=PALETTE["panel"], edgecolor=PALETTE["rule"], lw=0.6))
    ax.text(LX + 2.0, LY + 0.22,
            "Solid borders · MAESTRO   ·   Light fill · External   ·   ⇢ «import»",
            ha="center", va="center",
            fontsize=8.8, color=PALETTE["muted"], style="italic")

    return save(fig, "08-package-architecture", out_dir)


# ---------------------------------------------------------------------------
#  FIGURE 9 — Standards Alignment Honeycomb
# ---------------------------------------------------------------------------

def draw_hex(ax, cx, cy, radius, *, label, fill, edge=PALETTE["ink"],
             lw=0.9, fontsize=12, text_color="white", flat_top=False):
    """Hexagon (pointy-top by default) with a centred label."""
    orientation = 0.0 if flat_top else (3.141592653589793 / 6)
    from matplotlib.patches import RegularPolygon
    hexpatch = RegularPolygon(
        (cx, cy), numVertices=6, radius=radius,
        orientation=orientation,
        facecolor=fill, edgecolor=edge, linewidth=lw, zorder=1,
    )
    ax.add_patch(hexpatch)
    # Multi-line labels: split on \n
    ax.text(cx, cy, label,
            ha="center", va="center",
            fontsize=fontsize, fontweight="bold",
            color=text_color)


def fig_09_standards_honeycomb(out_dir):
    fig, ax = plt.subplots(figsize=(13, 9))
    xlim = (0, 13)
    ylim = (0, 9.5)
    setup_axes(ax, xlim, ylim,
               title="MAESTRO — Standards Alignment",
               subtitle="Each MAESTRO module aligns with an established standard, grouped by purpose")

    # Pointy-top hex spacing:
    #   dx = sqrt(3) * R between columns
    #   dy = 1.5 * R between rows
    R = 0.95
    import math
    DX = math.sqrt(3) * R
    DY = 1.5 * R

    # Layout grid (col, row) → centre; col offset on odd rows for honeycomb.
    def cell(col, row, origin_x, origin_y):
        x = origin_x + col * DX + (DY * 0 if row % 2 == 0 else 0)
        # offset every other row horizontally by half a column
        if row % 2 == 1:
            x += DX / 2
        y = origin_y - row * DY
        return x, y

    ORIGIN_X, ORIGIN_Y = 2.8, 7.4

    # Cells defined as (col, row, label, group)
    cells = [
        # GROUP: Abstract Capabilities — top left cluster (blue)
        (0, 0, "DIN\n8580",    "abstract"),
        (1, 0, "VDI\n3682",    "abstract"),
        (0, 1, "VDI\n2860",    "abstract"),

        # GROUP: Machine Structure — top right (red/magenta)
        (2, 0, "VDI\n2206",    "structure"),

        # GROUP: Executable Skills (yellow)
        (2, 1, "ISA 88\n/ PackML", "skills"),
        (1, 1, "DIN EN\n61360",    "neutral"),
        (1, 2, "OPC UA",            "skills"),
        (2, 2, "IEC\n61131",        "skills"),
        (3, 1, "IEC\n61499",        "skills"),
        (3, 2, "ROS 2",             "skills"),

        # GROUP: Cross-cutting (sage/green-grey)
        (0, 2, "SSN /\nSOSA",       "cross"),
        (4, 0, "AAS",               "skills"),
        (4, 1, "QUDT",              "cross"),
        (4, 2, "IEC\n61508",        "cross"),
    ]

    group_style = {
        "abstract":  dict(fill=HEX_BLUE,   text_color="white"),
        "structure": dict(fill=HEX_RED,    text_color="white"),
        "skills":    dict(fill=HEX_YELLOW, text_color="#3D2F00"),
        "cross":     dict(fill="#8FBF7A",  text_color="white"),
        "neutral":   dict(fill="white",    text_color=PALETTE["ink"]),
    }

    centres = {}
    for col, row, label, group in cells:
        x, y = cell(col, row, ORIGIN_X, ORIGIN_Y)
        s = group_style[group]
        draw_hex(ax, x, y, R, label=label,
                 fill=s["fill"], text_color=s["text_color"],
                 fontsize=11,
                 lw=0.6 if group == "neutral" else 1.0,
                 edge="#888888" if group == "neutral" else PALETTE["ink"])
        centres[label] = (x, y, group)

    # Group annotations (off to the side, leader lines)
    annotations = [
        ("Abstract\nCapabilities", (1.05, 6.4), HEX_BLUE,   ["DIN\n8580", "VDI\n3682", "VDI\n2860"]),
        ("Machine\nStructure",     (11.7, 7.5), HEX_RED,    ["VDI\n2206"]),
        ("Executable\nSkills",     (11.9, 3.3), HEX_YELLOW, ["IEC\n61499", "ROS 2", "AAS"]),
        ("Cross-cutting",          (1.10, 2.9), "#5A8049",  ["SSN /\nSOSA"]),
    ]
    for text, (tx, ty), color, anchors in annotations:
        ax.text(tx, ty, text, ha="center", va="center",
                fontsize=12, fontweight="bold", color=color)
        # leader line to first anchor
        if anchors and anchors[0] in centres:
            ax_x, ax_y, _ = centres[anchors[0]]
            ax.plot([tx, ax_x], [ty, ax_y],
                    color=color, lw=0.6, alpha=0.45, zorder=0)

    # footer
    ax.text(xlim[1] / 2, 0.5,
            "Hexagon groups mirror the standards layering used in CaSkMan; MAESTRO extends them with cross-cutting concerns (sensors, units, safety).",
            ha="center", va="center", fontsize=9.5,
            color=PALETTE["muted"], style="italic")

    return save(fig, "09-standards-honeycomb", out_dir)


# ---------------------------------------------------------------------------
#  FIGURE 10 — Class Alignment Diagram
# ---------------------------------------------------------------------------

def fig_10_class_alignment(out_dir):
    fig, ax = plt.subplots(figsize=(15, 10.5))
    xlim = (0, 15)
    ylim = (-0.6, 10.5)
    setup_axes(ax, xlim, ylim,
               title="MAESTRO — Class Alignment Across Modules",
               subtitle="Two-colour view: structural core: classes and domain extension classes, with labelled OWL relations")

    # Helper: pill-style class box
    def class_box(x, y, w, h, label, *, kind="core"):
        if kind == "core":
            fill, edge = CASK_BLUE, PALETTE["ink"]
            text_color = "white"
        else:
            fill, edge = CASK_ORANGE_LIGHT, "#A06820"
            text_color = PALETTE["ink"]
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            facecolor=fill, edgecolor=edge, linewidth=0.9))
        ax.text(x + w / 2, y + h / 2, label,
                ha="center", va="center",
                fontsize=9.5, fontweight="bold",
                color=text_color)

    def edge(x1, y1, x2, y2, label=None, dashed=False,
             label_at=0.55, label_off=(0, 0.08)):
        line = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>",
            mutation_scale=11,
            linestyle=(0, (4, 3)) if dashed else "-",
            linewidth=0.8,
            color=PALETTE["ink"],
            zorder=2,
        )
        ax.add_patch(line)
        if label:
            lx = x1 + (x2 - x1) * label_at + label_off[0]
            ly = y1 + (y2 - y1) * label_at + label_off[1]
            ax.text(lx, ly, label,
                    ha="center", va="center",
                    fontsize=8.2, color=PALETTE["muted"],
                    style="italic",
                    bbox=dict(facecolor="#FFFAE6", edgecolor="#E0CFA0",
                              boxstyle="round,pad=0.18", lw=0.4))

    # Box geometry constants
    bw, bh = 2.45, 0.58

    # Row Y coordinates (top to bottom)
    Y_PROD  = 8.3
    Y_PROC  = 7.0
    Y_CAP   = 5.8
    Y_SKILL = 4.5
    Y_CTRL  = 3.0
    Y_RES   = 1.6
    Y_MOT   = 0.45

    # COLUMN x-anchors
    X_LEFT, X_CENTER, X_RIGHT = 1.0, 6.3, 11.6

    # ----- LEFT COLUMN (Domain classes - orange) -----
    class_box(X_LEFT, Y_PROD,  bw, bh, "prod:Product",      kind="domain")
    class_box(X_LEFT, Y_PROC,  bw, bh, "proc:ManufacturingProcess", kind="domain")
    class_box(X_LEFT, Y_CAP,   bw, bh, "cap:Capability",    kind="domain")
    class_box(X_LEFT, Y_SKILL, bw, bh, "skill:CompositeSkill", kind="domain")
    class_box(X_LEFT, Y_CTRL,  bw, bh, "plc:FunctionBlock", kind="domain")
    class_box(X_LEFT, Y_RES,   bw, bh, "res:Robot",         kind="domain")
    class_box(X_LEFT, Y_MOT,   bw, bh, "motion:LinearMotion", kind="domain")

    # ----- CENTER COLUMN (Core classes - blue) -----
    class_box(X_CENTER, Y_PROD,  bw, bh, "core:Product",     kind="core")
    class_box(X_CENTER, Y_PROC,  bw, bh, "core:Process",     kind="core")
    class_box(X_CENTER, Y_CAP,   bw, bh, "core:Capability",  kind="core")
    class_box(X_CENTER, Y_SKILL, bw, bh, "core:Skill",       kind="core")
    class_box(X_CENTER, Y_CTRL,  bw, bh, "core:ControlComponent", kind="core")
    class_box(X_CENTER, Y_RES,   bw, bh, "core:Resource",    kind="core")
    class_box(X_CENTER, Y_MOT,   bw, bh, "core:LogicalEntity", kind="core")

    # ----- RIGHT COLUMN (Adapter classes - orange) -----
    class_box(X_RIGHT, Y_SKILL, bw, bh, "skill:MotionSkill",     kind="domain")
    class_box(X_RIGHT, Y_CTRL,  bw, bh, "ros:ROSNode",            kind="domain")
    class_box(X_RIGHT, Y_RES,   bw, bh, "res:Cobot",              kind="domain")
    class_box(X_RIGHT, Y_PROD,  bw, bh, "prod:Part",              kind="domain")
    class_box(X_RIGHT, Y_PROC,  bw, bh, "proc:AssemblyProcess",   kind="domain")
    class_box(X_RIGHT, Y_CAP,   bw, bh, "cap:PickPlaceCapability", kind="domain")
    class_box(X_RIGHT, Y_MOT,   bw, bh, "motion:Motion",           kind="domain")

    # ----- SUBCLASS relationships (left/right → centre via rdfs:subClassOf) -----
    # Pattern: small triangular arrows with "rdfs:subClassOf" label
    def subclass(src_x, src_y, dst_x, dst_y, label_at=0.6):
        edge(src_x, src_y, dst_x, dst_y,
             label="rdfs:subClassOf", dashed=False,
             label_at=label_at, label_off=(0, 0.10))

    # Domain (left) → Core (centre)
    for ya in [Y_PROD, Y_PROC, Y_CAP, Y_SKILL, Y_CTRL, Y_RES, Y_MOT]:
        subclass(X_LEFT + bw, ya + bh / 2,
                 X_CENTER, ya + bh / 2,
                 label_at=0.50)

    # Adapter (right) → Core (centre)
    for ya in [Y_PROD, Y_PROC, Y_CAP, Y_SKILL, Y_CTRL, Y_RES, Y_MOT]:
        subclass(X_RIGHT, ya + bh / 2,
                 X_CENTER + bw, ya + bh / 2,
                 label_at=0.50)

    # ----- KEY OWL RELATIONS (vertical, between centre nodes) -----
    def vrel(y_from, y_to, label):
        cx = X_CENTER + bw / 2
        edge(cx, y_from, cx, y_to + bh,
             label=label, label_at=0.5, label_off=(0.10, 0))

    vrel(Y_PROD,  Y_PROC, "core:requires")
    vrel(Y_PROC,  Y_CAP,  "core:requires")
    vrel(Y_CAP,   Y_SKILL,"core:realizes")
    vrel(Y_SKILL, Y_CTRL, "core:implements")
    vrel(Y_CTRL,  Y_RES,  "core:controls")
    vrel(Y_RES,   Y_MOT,  "performs (via Motion)")

    # ----- LEGEND (bottom-centre, below the diagram) -----
    LY = -0.30
    ax.add_patch(FancyBboxPatch(
        (1.0, LY - 0.05), 13.0, 0.55,
        boxstyle="round,pad=0.05,rounding_size=0.05",
        facecolor=PALETTE["panel"], edgecolor=PALETTE["rule"], lw=0.6))
    # core swatch
    ax.add_patch(Rectangle((1.6, LY + 0.13), 0.35, 0.22,
                           facecolor=CASK_BLUE, edgecolor=PALETTE["ink"], lw=0.6))
    ax.text(2.05, LY + 0.24, "core:  (structural)",
            ha="left", va="center",
            fontsize=10, color=PALETTE["ink"], fontweight="bold")
    # domain swatch
    ax.add_patch(Rectangle((5.2, LY + 0.13), 0.35, 0.22,
                           facecolor=CASK_ORANGE_LIGHT, edgecolor="#A06820", lw=0.6))
    ax.text(5.65, LY + 0.24, "module:  (domain / adapter)",
            ha="left", va="center",
            fontsize=10, color=PALETTE["ink"], fontweight="bold")
    # edge legend
    ax.text(10.0, LY + 0.24,
            "—▸ rdfs:subClassOf       ⇢ core:requires / realizes / implements / controls",
            ha="left", va="center",
            fontsize=9, color=PALETTE["muted"], style="italic")

    return save(fig, "10-class-alignment", out_dir)


def main():
    here = Path(__file__).resolve().parent
    out_dir = here.parent / "png"
    out_dir.mkdir(parents=True, exist_ok=True)

    renderers = [
        fig_01_semantic_stack,
        fig_02_modular_stack,
        fig_03_skill_hierarchy,
        fig_04_reasoning_chain,
        fig_05_llm_pipeline,
        fig_06_final_architecture,
        fig_07_named_graphs,
        fig_08_package_architecture,
        fig_09_standards_honeycomb,
        fig_10_class_alignment,
    ]
    for fn in renderers:
        out = fn(out_dir)
        print(f"OK  {out}")


if __name__ == "__main__":
    main()
