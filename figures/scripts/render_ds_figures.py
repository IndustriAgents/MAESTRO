"""
MAESTRO — Distribution Station explainer: publication-quality figures.

Outputs ds-01..ds-05.png in figures/png/ at 300 DPI.
"""
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

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
    "rtgreen":    "#C7E8D1",
    "inferred":   "#FFF1B8",
    "rule_col":   "#F4B860",
}

plt.rcParams.update({
    "font.family":        "DejaVu Sans",
    "font.size":          10,
    "axes.edgecolor":     PALETTE["ink"],
    "axes.linewidth":     0.6,
    "savefig.dpi":        300,
    "savefig.facecolor":  PALETTE["bg"],
    "savefig.bbox":       "tight",
    "savefig.pad_inches": 0.30,
    "figure.facecolor":   PALETTE["bg"],
    "figure.dpi":         150,
})

TITLE_BAND = 1.5


def box(ax, x, y, w, h, label, sub=None, fill=PALETTE["panel"],
        edge=PALETTE["ink"], lw=0.9, fs=10, sfs=8.5, fw="bold"):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle="round,pad=0.02,rounding_size=0.04",
                       linewidth=lw, edgecolor=edge, facecolor=fill)
    ax.add_patch(p)
    cx, cy = x + w/2, y + h/2
    if sub:
        ax.text(cx, cy + 0.18*h, label, ha="center", va="center",
                fontsize=fs, fontweight=fw, color=PALETTE["ink"])
        ax.text(cx, cy - 0.24*h, sub, ha="center", va="center",
                fontsize=sfs, color=PALETTE["muted"], style="italic")
    else:
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=fs, fontweight=fw, color=PALETTE["ink"])


def panel(ax, x, y, w, h, header, fill=PALETTE["panel"],
          edge=PALETTE["ink"], header_fs=11, sub=None, sub_fs=8.5):
    """Panel where the header sits at the top (not centred)."""
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle="round,pad=0.02,rounding_size=0.04",
                       linewidth=0.9, edgecolor=edge, facecolor=fill)
    ax.add_patch(p)
    cx = x + w/2
    ax.text(cx, y + h - 0.22, header, ha="center", va="top",
            fontsize=header_fs, fontweight="bold", color=PALETTE["ink"])
    if sub:
        ax.text(cx, y + h - 0.55, sub, ha="center", va="top",
                fontsize=sub_fs, color=PALETTE["muted"], style="italic")


def arrow(ax, x1, y1, x2, y2, label=None, color=None, lw=1.0,
          style="-|>", curve=0.0, fs=8.5, dx=0.0, dy=0.0):
    color = color or PALETTE["ink"]
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=12, linewidth=lw, color=color,
                        connectionstyle=f"arc3,rad={curve}", zorder=2)
    ax.add_patch(a)
    if label:
        mx = (x1 + x2) / 2 + dx
        my = (y1 + y2) / 2 + dy
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color=PALETTE["muted"],
                bbox=dict(facecolor=PALETTE["bg"], edgecolor="none", pad=1.5))


def setup(ax, xlim, ylim, title, subtitle=None):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("auto"); ax.axis("off")
    cx = (xlim[0] + xlim[1]) / 2
    top = ylim[1]
    ax.text(cx, top - 0.45, title, ha="center", va="center",
            fontsize=15, fontweight="bold", color=PALETTE["ink"])
    if subtitle:
        ax.text(cx, top - 1.05, subtitle, ha="center", va="center",
                fontsize=10, color=PALETTE["muted"], style="italic")


def save(fig, name, out_dir):
    p = Path(out_dir) / f"{name}.png"
    fig.savefig(p, dpi=300)
    plt.close(fig)
    return p


# =========================================================================
# Figure DS-01 — Plant topology
# =========================================================================
def ds01_plant_topology(out_dir):
    fig, ax = plt.subplots(figsize=(13, 9))
    setup(ax, (0, 14), (0, 10),
          "Festo Distributing Station — Plant Topology",
          "ex:DistributingStation1  core:hasPart  {FeederUnit1, TransferUnit1}")

    # Legend row (below title)
    box(ax, 0.8, 7.95, 2.2, 0.55, "Resources",
        fill=PALETTE["resource"], fs=9)
    box(ax, 3.2, 7.95, 1.7, 0.55, "Plant",
        fill=PALETTE["factory"], fs=9)
    box(ax, 5.1, 7.95, 2.5, 0.55, "Sensors / IOs",
        fill=PALETTE["product"], fs=9)
    box(ax, 7.8, 7.95, 3.7, 0.55, "Material flow (skill colour)",
        fill=PALETTE["skill"], fs=9)

    # Plant
    box(ax, 5.5, 6.4, 3.0, 0.9, "DistributingStation1",
        sub="core:Plant", fill=PALETTE["factory"], fs=12)

    # FeederUnit
    box(ax, 0.8, 4.0, 5.4, 2.0, "FeederUnit1",
        sub="ex:FeederUnit  ⊑  res:Machine",
        fill=PALETTE["resource"], fs=12)
    # TransferUnit
    box(ax, 7.8, 4.0, 5.4, 2.0, "TransferUnit1",
        sub="ex:TransferUnit  ⊑  res:Machine",
        fill=PALETTE["resource"], fs=12)

    # Feeder parts
    box(ax, 1.0, 2.4, 1.5, 0.7, "Magazine1", sub="Magazine",
        fs=9, sfs=7.5, fw="normal")
    box(ax, 2.7, 2.4, 1.5, 0.7, "Pusher1", sub="Tool",
        fs=9, sfs=7.5, fw="normal")
    box(ax, 4.4, 2.4, 1.7, 0.7, "Cylinder1", sub="Pneumatic actuator",
        fs=9, sfs=7.5, fw="normal")
    box(ax, 1.0, 1.0, 5.1, 0.8,
        "EmptySensor1 · PusherRearSensor1 · PusherFrontSensor1",
        sub="sensor:ProximitySensor",
        fs=8.5, sfs=7.5, fw="normal", fill=PALETTE["product"])

    # Transfer parts
    box(ax, 8.0, 2.4, 1.9, 0.7, "TransferArm1", sub="res:TransferArm",
        fs=9, sfs=7.5, fw="normal")
    box(ax, 10.1, 2.4, 1.7, 0.7, "VacuumUnit1", sub="res:VacuumUnit",
        fs=9, sfs=7.5, fw="normal")
    box(ax, 12.0, 2.4, 1.1, 0.7, "Valve1", sub="Actuator",
        fs=8.5, sfs=7, fw="normal")
    box(ax, 8.0, 1.0, 5.1, 0.8,
        "TransferArmLeftSensor1 · TransferArmRightSensor1 · VacuumSense1",
        sub="sensor:ProximitySensor · sensor:PressureSensor",
        fs=8.5, sfs=7.5, fw="normal", fill=PALETTE["product"])

    # Plant -> units
    arrow(ax, 6.5, 6.4, 3.5, 6.05, label="core:hasPart",
          curve=-0.15, dx=-0.4, dy=0.18)
    arrow(ax, 7.5, 6.4, 10.5, 6.05, label="core:hasPart",
          curve=0.15, dx=0.4, dy=0.18)
    # FeederUnit -> TransferUnit (feeds)
    arrow(ax, 6.2, 5.0, 7.8, 5.0,
          label="ex:feeds  ⊑  core:connectedTo",
          color=PALETTE["skill"], lw=1.4, fs=9, dy=0.28)
    # Feeder -> parts
    for x in (1.75, 3.45, 5.25):
        arrow(ax, 3.5, 4.0, x, 3.1, color=PALETTE["muted"], lw=0.7)
    arrow(ax, 3.5, 4.0, 3.55, 1.8, color=PALETTE["muted"], lw=0.7)
    # Transfer -> parts
    for x in (8.95, 10.95, 12.55):
        arrow(ax, 10.5, 4.0, x, 3.1, color=PALETTE["muted"], lw=0.7)
    arrow(ax, 10.5, 4.0, 10.55, 1.8, color=PALETTE["muted"], lw=0.7)

    return save(fig, "ds-01-plant-topology", out_dir)


# =========================================================================
# Figure DS-02 — Skill bridge
# =========================================================================
def ds02_skill_bridge(out_dir):
    fig, ax = plt.subplots(figsize=(13, 8))
    setup(ax, (0, 14), (0, 9),
          "Capability Inference — TYPE skills bridge to library skills via a shared semantic class",
          "Custom rule joins ex:Type_sk*  ↔  skill:*Skill  ↔  skill-lib:*")

    # Column headers
    ax.text(2.4, 7.3, "Resource-side TYPE skills",
            ha="center", fontsize=10, fontweight="bold", color=PALETTE["ink"])
    ax.text(2.4, 6.95, "(declared in plant.ttl, owned by Resources)",
            ha="center", fontsize=8.5, color=PALETTE["muted"], style="italic")

    ax.text(7.0, 7.3, "Shared semantic class",
            ha="center", fontsize=10, fontweight="bold", color=PALETTE["ink"])
    ax.text(7.0, 6.95, "(skill: ontology, TBox)",
            ha="center", fontsize=8.5, color=PALETTE["muted"], style="italic")

    ax.text(11.6, 7.3, "Library skills + capabilities",
            ha="center", fontsize=10, fontweight="bold", color=PALETTE["ink"])
    ax.text(11.6, 6.95, "(skill-lib + capability ontologies)",
            ha="center", fontsize=8.5, color=PALETTE["muted"], style="italic")

    rows = [
        ("ex:Type_skTransfer_adp",       "skill:TransferSkill",
         "skill-lib:Transfer",           "cap:PickPlaceCapability", True),
        ("ex:Type_skGoToLeft / GoToRight","skill:MotionSkill",
         "skill-lib:MoveLinear / MoveJoint", "cap:TransportCapability", True),
        ("ex:Type_skPick / skPlace",     "skill:ManipulationSkill",
         "skill-lib:VacuumPick",          "(no DS capability)", False),
        ("ex:Type_skLoad_adp / skPush_adp","skill:HandlingSkill",
         "(no library)",                  "cap:HandlingCapability", False),
    ]
    ys = [5.5, 4.2, 2.9, 1.6]
    for (left, mid, right, cap, hit), y in zip(rows, ys):
        box(ax, 0.6, y, 3.8, 0.85, left, sub=mid,
            fill=PALETTE["execution"], fs=9.5, sfs=8)
        box(ax, 5.1, y, 3.9, 0.85, mid, fill=PALETTE["capability"], fs=10)
        rc = PALETTE["skill"] if hit else PALETTE["panel"]
        box(ax, 9.6, y, 4.0, 0.85, right, sub=cap, fill=rc, fs=9.5, sfs=8)
        # arrows
        arrow(ax, 4.4, y+0.42, 5.1, y+0.42, color=PALETTE["muted"], lw=0.9,
              label="rdf:type", fs=7.5, dy=0.18)
        if hit:
            arrow(ax, 9.0, y+0.42, 9.6, y+0.42, color=PALETTE["ink"], lw=1.4,
                  label="realizedBySkill", fs=7.5, dy=0.18)
        else:
            arrow(ax, 9.0, y+0.42, 9.6, y+0.42, color=PALETTE["muted"], lw=0.5)

    # Output (inferred) row
    box(ax, 0.6, 0.2, 13.0, 0.9,
        "INFERRED   ex:TransferUnit1 core:canPerform cap:PickPlaceCapability ,  "
        "cap:TransportCapability   ·   "
        "ex:TransferArm1 core:canPerform cap:TransportCapability",
        fill=PALETTE["inferred"], fs=9, fw="bold")

    return save(fig, "ds-02-skill-bridge", out_dir)


# =========================================================================
# Figure DS-03 — Reasoning pipeline
# =========================================================================
def ds03_reasoning_pipeline(out_dir):
    fig, ax = plt.subplots(figsize=(13, 8))
    setup(ax, (0, 14), (0, 9),
          "Distribution Station — End-to-end reasoning pipeline",
          "Three TTL inputs · OWL2-RL materialisation · two SPARQL CONSTRUCT rules · single answer")

    # Stage 1 — TTL inputs
    box(ax, 0.4, 5.0, 2.5, 1.6, "plant.ttl",
        sub="design-time topology\n5 machines · 6 sensors\n10 skill TYPES · 10 FBTs",
        fill=PALETTE["resource"], fs=11, sfs=8)
    box(ax, 0.4, 3.0, 2.5, 1.6, "product.ttl",
        sub="WP3 + 5-step\ntransport process",
        fill=PALETTE["product"], fs=11, sfs=8)
    box(ax, 0.4, 1.0, 2.5, 1.6, "runtime.ttl",
        sub="2026-05-25 snapshot\ncore:hasState",
        fill=PALETTE["rtgreen"], fs=11, sfs=8)

    # Stage 2 — GraphDB store
    panel(ax, 3.7, 1.0, 3.6, 5.6,
          header="GraphDB  maestro-ds",
          header_fs=12,
          sub="OWL2-RL-optimized ruleset",
          fill=PALETTE["panel"])
    ax.text(5.5, 5.0, "5 568 triples · 19 named graphs", ha="center",
            fontsize=9, color=PALETTE["muted"], style="italic")
    ax.text(5.5, 3.4,
            "Materialises:\n"
            "→  rdfs:subClassOf*\n"
            "→  rdfs:subPropertyOf*\n"
            "→  rdf:type lifting\n"
            "→  domain / range",
            ha="center", va="center", fontsize=9.5,
            color=PALETTE["ink"])

    # Stage 3 — Rules
    box(ax, 8.0, 4.6, 3.3, 1.8,
        "capability-inference-ds.rq",
        sub="custom SPARQL CONSTRUCT\nclass-bridge rule",
        fill=PALETTE["rule_col"], fs=10.5, sfs=8.5)
    box(ax, 8.0, 1.7, 3.3, 1.8,
        "manufacturing-ability.rq",
        sub="MAESTRO library rule\nSPARQL CONSTRUCT",
        fill=PALETTE["rule_col"], fs=10.5, sfs=8.5)

    # Stage 4 — Inferred facts
    box(ax, 11.9, 4.6, 1.8, 1.8, "core:\ncanPerform",
        sub="3 triples", fill=PALETTE["inferred"], fs=10, sfs=8.5)
    box(ax, 11.9, 1.7, 1.8, 1.8, "core:\ncanManufacture",
        sub="1 triple", fill=PALETTE["inferred"], fs=10, sfs=8.5)

    # Stage 5 — Orchestrator
    box(ax, 4.5, 0.0, 7.0, 0.75,
        "Orchestrator / LLM:  \"can DistributingStation1 manufacture WP3?\"",
        fill=PALETTE["orchestr"], fs=10, fw="bold")

    # Arrows
    for y in (5.8, 3.8, 1.8):
        arrow(ax, 2.9, y, 3.7, y, color=PALETTE["muted"], lw=1.0)
    # store -> rules
    arrow(ax, 7.3, 5.5, 8.0, 5.5, color=PALETTE["ink"], lw=1.3,
          label="SPARQL", fs=8, dy=0.22)
    arrow(ax, 7.3, 2.6, 8.0, 2.6, color=PALETTE["ink"], lw=1.3,
          label="SPARQL", fs=8, dy=0.22)
    # rules -> inferred
    arrow(ax, 11.3, 5.5, 11.9, 5.5, color=PALETTE["ink"], lw=1.3)
    arrow(ax, 11.3, 2.6, 11.9, 2.6, color=PALETTE["ink"], lw=1.3)
    # inferred -> orchestrator
    arrow(ax, 12.8, 4.6, 10.5, 0.75, color=PALETTE["muted"], lw=0.8, curve=0.2)
    arrow(ax, 12.8, 1.7, 10.5, 0.75, color=PALETTE["muted"], lw=0.8, curve=-0.15)

    return save(fig, "ds-03-reasoning-pipeline", out_dir)


# =========================================================================
# Figure DS-04 — Named graphs (bar chart)
# =========================================================================
def ds04_named_graphs(out_dir):
    data = [
        ("…/examples/distribution-station/plant", 523),
        ("…/core",                                204),
        ("…/resource",                            103),
        ("…/runtime",                              87),
        ("…/unit",                                 76),
        ("…/skill",                                74),
        ("…/process",                              72),
        ("…/capability",                           69),
        ("…/iec61499",                             67),
        ("…/motion",                               62),
        ("…/product",                              55),
        ("…/opcua",                                55),
        ("…/examples/distribution-station/product",44),
        ("…/sensor",                               39),
        ("…/state",                                37),
        ("…/reasoning",                            34),
        ("…/skill-lib",                            27),
        ("…/motion-lib",                           15),
        ("…/examples/distribution-station/runtime",13),
    ]
    labels = [d[0] for d in data][::-1]
    counts = [d[1] for d in data][::-1]
    colors = []
    for lbl in labels:
        if "distribution-station" in lbl:
            colors.append(PALETTE["skill"])
        elif lbl in ("…/runtime", "…/state"):
            colors.append(PALETTE["rtgreen"])
        elif lbl in ("…/reasoning",):
            colors.append(PALETTE["inferred"])
        else:
            colors.append(PALETTE["resource"])

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(labels, counts, color=colors,
                   edgecolor=PALETTE["ink"], linewidth=0.7)
    ax.set_facecolor(PALETTE["bg"])
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(PALETTE["muted"])
    ax.spines["bottom"].set_color(PALETTE["muted"])
    ax.tick_params(colors=PALETTE["ink"], labelsize=9)
    ax.set_xlabel("Triples loaded", fontsize=10, color=PALETTE["ink"])
    ax.set_title(
        "GraphDB  maestro-ds  —  triple count per named graph\n"
        "5 568 explicit triples across 19 named graphs",
        fontsize=13, fontweight="bold", color=PALETTE["ink"],
        loc="left", pad=12)
    for bar, c in zip(bars, counts):
        ax.text(bar.get_width() + 6, bar.get_y() + bar.get_height()/2,
                str(c), va="center", fontsize=8.5, color=PALETTE["ink"])
    ax.set_xlim(0, max(counts) * 1.15)
    fig.tight_layout()
    p = Path(out_dir) / "ds-04-named-graphs.png"
    fig.savefig(p, dpi=300)
    plt.close(fig)
    return p


# =========================================================================
# Figure DS-05 — Three layers in one SPARQL query
# =========================================================================
def ds05_three_layers(out_dir):
    fig, ax = plt.subplots(figsize=(14, 9))
    setup(ax, (0, 14), (0, 10),
          "One SPARQL query joins three layers of triples",
          "explicit  +  OWL/RDFS-inferred  +  custom-rule-derived")

    mono = {"family": "DejaVu Sans Mono"}

    # --- LEFT: three layer panels with top-aligned headers ---
    panel(ax, 0.4, 6.0, 6.2, 1.8,
          header="Explicit triples",
          sub="asserted in plant.ttl, product.ttl, runtime.ttl",
          fill=PALETTE["resource"], header_fs=12)
    ax.text(0.7, 6.5,
            "ex:WP3            prod:requiresProcess   ex:DistributeProcess .\n"
            "ex:TransferUnit1  core:provides          ex:Type_skTransfer_adp .\n"
            "ex:DistStation1   core:hasState          runtime:Available .",
            ha="left", va="top", fontsize=8.5, color=PALETTE["ink"],
            **mono)

    panel(ax, 0.4, 3.9, 6.2, 1.8,
          header="OWL2-RL-inferred triples",
          sub="materialised at load-time by the GraphDB ruleset",
          fill=PALETTE["capability"], header_fs=12)
    ax.text(0.7, 4.4,
            "ex:Type_skTransfer_adp  a  core:Skill .\n"
            "ex:FeederUnit1          core:connectedTo  ex:TransferUnit1 .\n"
            "ex:TransferUnit1        a  res:Machine ,  core:Resource .",
            ha="left", va="top", fontsize=8.5, color=PALETTE["ink"],
            **mono)

    panel(ax, 0.4, 1.8, 6.2, 1.8,
          header="Custom-rule-derived triples",
          sub="materialised by capability + manufacturing CONSTRUCT rules",
          fill=PALETTE["inferred"], header_fs=12)
    ax.text(0.7, 2.3,
            "ex:TransferUnit1  core:canPerform     cap:PickPlaceCapability .\n"
            "ex:TransferArm1   core:canPerform     cap:TransportCapability .\n"
            "ex:DistStation1   core:canManufacture ex:WP3 .",
            ha="left", va="top", fontsize=8.5, color=PALETTE["ink"],
            **mono)

    # --- RIGHT: SPARQL query + result ---
    panel(ax, 7.4, 4.3, 6.2, 3.5,
          header="SPARQL  SELECT  query (against the materialised store)",
          fill=PALETTE["panel"], header_fs=11)
    ax.text(7.6, 6.7,
            "SELECT ?plant ?product ?state WHERE {\n"
            "  ?plant   a core:Plant ;                # explicit\n"
            "           core:canManufacture ?product; # rule-derived\n"
            "           core:hasState ?state .        # explicit (runtime)\n"
            "  ?product prod:requiresProcess ?proc .\n"
            "  ?product a/rdfs:subClassOf*\n"
            "           core:Product .                # OWL-inferred\n"
            "}",
            ha="left", va="top", fontsize=9.0, color=PALETTE["ink"], **mono)

    panel(ax, 7.4, 1.8, 6.2, 2.2,
          header="Single result row",
          fill=PALETTE["rtgreen"], header_fs=12)
    ax.text(10.5, 2.55,
            "?plant    →  ex:DistributingStation1\n"
            "?product  →  ex:WorkpieceWP3\n"
            "?state    →  runtime:Available",
            ha="center", va="center", fontsize=10,
            color=PALETTE["ink"], **mono)

    # Arrows
    arrow(ax, 6.6, 6.9, 7.4, 6.5, color=PALETTE["muted"], lw=0.8, curve=0.1)
    arrow(ax, 6.6, 4.8, 7.4, 5.7, color=PALETTE["muted"], lw=0.8, curve=-0.05)
    arrow(ax, 6.6, 2.7, 7.4, 5.1, color=PALETTE["muted"], lw=0.8, curve=-0.25)
    arrow(ax, 10.5, 4.3, 10.5, 4.0, color=PALETTE["ink"], lw=1.4)

    return save(fig, "ds-05-three-layers", out_dir)


# =========================================================================
def main():
    here = Path(__file__).resolve()
    out = here.parents[1] / "png"
    out.mkdir(parents=True, exist_ok=True)
    print("Rendering Distribution Station figures into", out)
    for fn in (ds01_plant_topology, ds02_skill_bridge,
               ds03_reasoning_pipeline, ds04_named_graphs,
               ds05_three_layers):
        p = fn(out)
        print("  wrote", p.name)


if __name__ == "__main__":
    main()
