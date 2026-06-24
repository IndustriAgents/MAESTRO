#!/usr/bin/env python3
"""
build_techdoc.py — Generate the MAESTRO stakeholder technical overview (.docx).

Reads the live TTL modules under ontologies/ with rdflib so the per-module
class/property/individual tables always track the ontology, embeds the existing
publication-grade PNG figures from figures/png/, and writes an editable Word
document to docs/MAESTRO-Technical-Overview.docx.

Usage:  python scripts/build_techdoc.py
Deps:   python-docx, rdflib  (both installed in this environment)
"""

from pathlib import Path

import rdflib
from rdflib import OWL, RDF, RDFS
from rdflib.namespace import SKOS

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parent.parent
ONTO = ROOT / "ontologies"
PNG = ROOT / "figures" / "png"
OUT = ROOT / "docs" / "MAESTRO-Technical-Overview.docx"

VERSION = "0.3.0"
AUTHOR = "Melwin Xavier"
DATE = "2026-06-15"

# Brand colours (matched to the figure palette)
NAVY = RGBColor(0x1F, 0x37, 0x5B)
AMBER = RGBColor(0xC8, 0x7A, 0x1E)
GREY = RGBColor(0x55, 0x55, 0x55)

# --------------------------------------------------------------------------- #
# Prefix map (local name shortening for domains / ranges / types)
# --------------------------------------------------------------------------- #
PREFIXES = {
    "https://w3id.org/maestro/core#": "core",
    "https://w3id.org/maestro/resource#": "res",
    "https://w3id.org/maestro/motion#": "motion",
    "https://w3id.org/maestro/skill#": "skill",
    "https://w3id.org/maestro/capability#": "cap",
    "https://w3id.org/maestro/process#": "proc",
    "https://w3id.org/maestro/product#": "prod",
    "https://w3id.org/maestro/iec61131#": "plc",
    "https://w3id.org/maestro/iec61499#": "iec61499",
    "https://w3id.org/maestro/ros#": "ros",
    "https://w3id.org/maestro/opcua#": "opcua",
    "https://w3id.org/maestro/aas#": "aas",
    "https://w3id.org/maestro/runtime#": "runtime",
    "https://w3id.org/maestro/state#": "state",
    "https://w3id.org/maestro/sensor#": "sensor",
    "https://w3id.org/maestro/unit#": "unit",
    "https://w3id.org/maestro/communication#": "com",
    "https://w3id.org/maestro/safety#": "safety",
    "https://w3id.org/maestro/quality#": "qa",
    "https://w3id.org/maestro/maintenance#": "maint",
    "https://w3id.org/maestro/energy#": "energy",
    "https://w3id.org/maestro/reasoning#": "reas",
    "https://w3id.org/maestro/planning#": "plan",
    "https://w3id.org/maestro/skill-lib#": "skill-lib",
    "https://w3id.org/maestro/motion-lib#": "motion-lib",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
    "http://www.w3.org/2002/07/owl#": "owl",
    "http://www.w3.org/2001/XMLSchema#": "xsd",
    "http://www.w3.org/ns/sosa/": "sosa",
    "http://www.w3.org/ns/ssn/": "ssn",
    "http://qudt.org/schema/qudt/": "qudt",
    "http://qudt.org/vocab/unit/": "qudt-unit",
    "http://purl.org/dc/terms/": "dct",
    "http://www.w3.org/2004/02/skos/core#": "skos",
}


def qname(uri) -> str:
    s = str(uri)
    for ns, pfx in PREFIXES.items():
        if s.startswith(ns):
            return f"{pfx}:{s[len(ns):]}"
    return s


# --------------------------------------------------------------------------- #
# Module catalogue: file, prefix, IRI, friendly name, purpose, optional figure
# --------------------------------------------------------------------------- #
CATEGORIES = [
    ("Core", "The single root every other module builds on.", [
        ("core/manufacturing-core.ttl", "core", "https://w3id.org/maestro/core#",
         "Manufacturing Core",
         "The root abstractions of the whole stack. Everything is an Entity, "
         "split into PhysicalEntity and LogicalEntity. The five manufacturing "
         "pillars — Resource, Skill, Capability, Process, Product — and the "
         "universal relations that bind them (provides, realizes, "
         "requiresCapability, implements, controls) live here.",
         "10-class-alignment.png"),
    ]),
    ("Physical layer", "What physically exists on the shop floor and how it moves.", [
        ("physical/resource.ttl", "res", "https://w3id.org/maestro/resource#",
         "Resource",
         "Physical manufacturing assets: machines, robots and cobots, conveyors, "
         "CNC and laser units, tools and grippers, actuators, and the controller "
         "hardware (PLC, industrial PC) that hosts control components.", None),
        ("physical/motion.ttl", "motion", "https://w3id.org/maestro/motion#",
         "Motion",
         "Technology-neutral geometric and kinematic primitives — linear, "
         "rotational, joint, Cartesian, synchronized, trajectory and "
         "force-controlled motion — kept separate from the resources that "
         "execute them.", None),
    ]),
    ("Logical layer", "The vendor-neutral semantics: what is made, how, and what it takes.", [
        ("logical/skill.ttl", "skill", "https://w3id.org/maestro/skill#",
         "Skill",
         "The keystone of the stack. A Skill is reusable logical behaviour — it "
         "is NOT a ROS node, a PLC function block or an OPC UA method; execution "
         "technologies implement skills. Atomic skills are primitives; composite "
         "skills are built from other skills via composedOfSkill.",
         "03-skill-hierarchy.png"),
        ("logical/capability.ttl", "cap", "https://w3id.org/maestro/capability#",
         "Capability",
         "What a plant can do, expressed vendor-neutrally (TransportCapability, "
         "not MoveLeftCapability). Capabilities are organised as a SKOS concept "
         "scheme and are realised by one or more Skills.", None),
        ("logical/process.ttl", "proc", "https://w3id.org/maestro/process#",
         "Process",
         "The manufacturing process taxonomy aligned to DIN 8580 (primary "
         "shaping, forming, separating, joining, coating, property change) plus "
         "handling/transport/inspection, with sequencing relations "
         "(precedes, follows, parallelWith).", None),
        ("logical/product.ttl", "prod", "https://w3id.org/maestro/product#",
         "Product",
         "Products, parts and assemblies, plus the features, tolerances and "
         "materials that drive which processes a product requires.", None),
    ]),
    ("Execution adapters", "Technology-specific bindings that implement logical skills.", [
        ("execution/ros.ttl", "ros", "https://w3id.org/maestro/ros#",
         "ROS / ROS 2",
         "ROS nodes, topics, services, actions, parameters, TF frames and MoveIt "
         "controllers. ROS nodes implement skills and control resources.", None),
        ("execution/iec61131.ttl", "plc", "https://w3id.org/maestro/iec61131#",
         "IEC 61131-3 (PLC)",
         "Classic PLC world: programs, tasks, function blocks, functions and "
         "variables, with the five IEC 61131-3 languages (LD, ST, FBD, SFC, IL) "
         "as individuals.", None),
        ("execution/iec61499.ttl", "iec61499", "https://w3id.org/maestro/iec61499#",
         "IEC 61499",
         "Event-driven distributed control: basic, composite and "
         "service-interface function blocks, applications, runtime resources and "
         "devices. Kept disjoint from IEC 61131 function blocks.", None),
        ("execution/opcua.ttl", "opcua", "https://w3id.org/maestro/opcua#",
         "OPC UA",
         "OPC UA servers, nodes, objects, variables and methods, plus a "
         "SkillInterface pattern that exposes a MAESTRO Skill over the network.", None),
        ("execution/aas.ttl", "aas", "https://w3id.org/maestro/aas#",
         "Asset Administration Shell",
         "The Industry 4.0 digital-twin envelope: administration shells, assets, "
         "submodels and submodel elements (properties, operations).", None),
    ]),
    ("Runtime layer", "Live operational state, kept apart from design-time models.", [
        ("runtime/runtime.ttl", "runtime", "https://w3id.org/maestro/runtime#",
         "Runtime",
         "Live behaviour: runtime events, state transitions and snapshots, with "
         "PackML-aligned operational states (Available, Busy, Executing, Held, "
         "Fault, …) as individuals.", None),
        ("runtime/state.ttl", "state", "https://w3id.org/maestro/state#",
         "State machine",
         "A generic state-machine vocabulary — state machines, transitions, "
         "guards, initial and final states — reused across resources and "
         "control components.", None),
    ]),
    ("Cross-cutting concerns", "Orthogonal aspects that apply across every layer.", [
        ("cross-cutting/unit.ttl", "unit", "https://w3id.org/maestro/unit#",
         "Units & quantities",
         "QUDT-aligned units and unit-bearing quantities, so physical values "
         "carry explicit units instead of bare floats.", None),
        ("cross-cutting/sensor.ttl", "sensor", "https://w3id.org/maestro/sensor#",
         "Sensors",
         "W3C SOSA/SSN-aligned sensors and observations, with industrial sensor "
         "types (temperature, pressure, vibration, force, torque, proximity, "
         "vision).", None),
        ("cross-cutting/communication.ttl", "com", "https://w3id.org/maestro/communication#",
         "Communication",
         "Protocols, channels and endpoints — OPC UA, DDS, MQTT, PROFINET, "
         "EtherCAT, Modbus, HTTP — that connect control components.", None),
        ("cross-cutting/safety.ttl", "safety", "https://w3id.org/maestro/safety#",
         "Safety",
         "Functional safety: safety functions, hazards and risks, with IEC 61508 "
         "SIL and ISO 13849 Performance Level individuals, and emergency stop.", None),
        ("cross-cutting/quality.ttl", "qa", "https://w3id.org/maestro/quality#",
         "Quality",
         "Quality checks, defects, non-conformances, inspection results "
         "(Pass/Fail/Rework) and KPIs (OEE, FPY, scrap rate).", None),
        ("cross-cutting/maintenance.ttl", "maint", "https://w3id.org/maestro/maintenance#",
         "Maintenance",
         "Preventive, corrective, predictive and inspection maintenance actions, "
         "plus fault diagnosis and reliability metrics (RUL, MTBF).", None),
        ("cross-cutting/energy.ttl", "energy", "https://w3id.org/maestro/energy#",
         "Energy",
         "Energy consumers, measurements and sources, with power, energy and "
         "carbon-intensity fields for energy-aware manufacturing.", None),
    ]),
    ("Reasoning & planning", "How the graph is reasoned over, and where it sits in the enterprise.", [
        ("reasoning/reasoning.ttl", "reas", "https://w3id.org/maestro/reasoning#",
         "Reasoning",
         "Documents the layered reasoning stack (semantic inheritance via "
         "OWL2-RL, validation via SHACL, capability inference and orchestration "
         "via SPARQL, explanation via LLM) and the canonical reasoning chain.", None),
        ("reasoning/planning.ttl", "plan", "https://w3id.org/maestro/planning#",
         "Planning (ISA-95)",
         "ISA-95 enterprise hierarchy (enterprise, site, area, work centre, work "
         "unit) and production planning objects (orders, schedules, work orders).", None),
    ]),
    ("Reusable libraries", "Canonical instance data with stable, citable IRIs.", [
        ("lib/skill-lib.ttl", "skill-lib", "https://w3id.org/maestro/skill-lib#",
         "Skill library",
         "Reusable skill individuals (MoveLinear, MoveJoint, VacuumPick, Release, "
         "Transfer) separated from the skill: vocabulary so application data can "
         "cite stable IRIs.", None),
        ("lib/motion-lib.ttl", "motion-lib", "https://w3id.org/maestro/motion-lib#",
         "Motion library",
         "Canonical reusable motion specifications (linear, joint, Cartesian) "
         "that skills point at via requiresMotion.", None),
    ]),
]

PROPERTY_KINDS = {OWL.ObjectProperty: "Object", OWL.DatatypeProperty: "Data",
                  OWL.AnnotationProperty: "Annotation", RDF.Property: "Property"}
SKIP_TYPES = {OWL.Class, RDFS.Class, OWL.ObjectProperty, OWL.DatatypeProperty,
              OWL.AnnotationProperty, RDF.Property, OWL.Ontology}


def parse_module(rel_path):
    """Return (classes, properties, individuals) extracted from one TTL file."""
    g = rdflib.Graph()
    g.parse(ONTO / rel_path, format="turtle")

    classes, properties, individuals = [], [], []
    subjects = set(g.subjects())
    for s in subjects:
        if not isinstance(s, rdflib.URIRef):
            continue
        types = set(g.objects(s, RDF.type))
        label = next((str(o) for o in g.objects(s, RDFS.label)), qname(s).split(":")[-1])
        comment = next((str(o) for o in g.objects(s, RDFS.comment)), "")
        if not comment:
            comment = next((str(o) for o in g.objects(s, SKOS.definition)), "")

        if OWL.Class in types or RDFS.Class in types:
            parents = [qname(p) for p in g.objects(s, RDFS.subClassOf)
                       if isinstance(p, rdflib.URIRef)]
            classes.append((qname(s), ", ".join(sorted(parents)) or "—", comment))
        elif types & set(PROPERTY_KINDS):
            kind = next(PROPERTY_KINDS[t] for t in types if t in PROPERTY_KINDS)
            domains = [qname(d) for d in g.objects(s, RDFS.domain) if isinstance(d, rdflib.URIRef)]
            ranges = [qname(r) for r in g.objects(s, RDFS.range) if isinstance(r, rdflib.URIRef)]
            dr = f"{', '.join(sorted(domains)) or '—'} → {', '.join(sorted(ranges)) or '—'}"
            properties.append((qname(s), kind, dr, comment))
        elif types and not (types & SKIP_TYPES):
            # An individual: typed by a class, not itself a class/property/ontology.
            inst_types = [qname(t) for t in types
                          if isinstance(t, rdflib.URIRef) and t != OWL.NamedIndividual]
            pref = next((str(o) for o in g.objects(s, SKOS.prefLabel)), "")
            individuals.append((qname(s), ", ".join(sorted(inst_types)) or "—",
                                comment or pref))

    classes.sort(key=lambda r: r[0].lower())
    properties.sort(key=lambda r: r[0].lower())
    individuals.sort(key=lambda r: r[0].lower())
    return classes, properties, individuals


# --------------------------------------------------------------------------- #
# docx helpers
# --------------------------------------------------------------------------- #
def add_figure(doc, filename, caption, width=6.3):
    path = PNG / filename
    if not path.exists():
        print(f"  !! MISSING FIGURE: {filename}")
        doc.add_paragraph(f"[figure missing: {filename}]")
        return
    doc.add_picture(str(path), width=Inches(width))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cap.add_run(caption)
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = GREY
    print(f"  embedded figure: {filename}")


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Light Grid Accent 1"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        r = cell.paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = NAVY
    for row in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run(str(val))
            r.font.size = Pt(8.5)
    if widths:
        for row in table.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
    return table


def add_toc_field(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve")
    instr.text = 'TOC \\o "1-2" \\h \\z \\u'
    fld_sep = OxmlElement("w:fldChar"); fld_sep.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "Right-click and choose “Update Field” to build the table of contents."
    fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
    for el in (fld_begin, instr, fld_sep, placeholder, fld_end):
        run._r.append(el)


# --------------------------------------------------------------------------- #
# Build the document
# --------------------------------------------------------------------------- #
def build():
    doc = Document()

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)

    # ---- Cover -----------------------------------------------------------
    if (PNG / "maestro-logo.png").exists():
        doc.add_picture(str(PNG / "maestro-logo.png"), width=Inches(2.6))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for _ in range(2):
        doc.add_paragraph()
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tr = title.add_run("MAESTRO")
    tr.bold = True; tr.font.size = Pt(40); tr.font.color.rgb = NAVY
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr = sub.add_run("Modular Ontology Stack for Future-Proof Manufacturing")
    sr.font.size = Pt(15); sr.font.color.rgb = AMBER
    sub2 = doc.add_paragraph()
    sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr2 = sub2.add_run("Technical Overview & Module Reference")
    sr2.font.size = Pt(13); sr2.italic = True; sr2.font.color.rgb = GREY

    for _ in range(6):
        doc.add_paragraph()
    for line in (f"Version {VERSION}", f"Author: {AUTHOR}", f"Date: {DATE}",
                 "Audience: stakeholder handover"):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(line); r.font.size = Pt(11)

    doc.add_page_break()

    # ---- Table of contents ----------------------------------------------
    doc.add_heading("Contents", level=1)
    add_toc_field(doc)
    doc.add_page_break()

    # ---- 1. Executive summary -------------------------------------------
    doc.add_heading("1. Executive summary", level=1)
    doc.add_paragraph(
        "MAESTRO is a modular, standards-aligned ontology for Industry 4.0/5.0 "
        "manufacturing. It describes a manufacturing system as a knowledge graph "
        "(RDF/OWL) so that software — including reasoners and AI agents — can "
        "answer questions such as “can this plant make this product?” and “which "
        "resources and skills are needed?” without any vendor-specific glue code.")
    doc.add_paragraph(
        "Its central idea is an inversion of the traditional Machine → "
        "Function model. Instead of hard-coding what a machine does, MAESTRO "
        "separates four concerns: a Capability (what is possible, vendor-neutral), "
        "a Skill (the logical behaviour that realises it), an Execution adapter "
        "(the technology that implements the skill — ROS, PLC, IEC 61499, OPC UA), "
        "and a Resource (the physical asset). Because these are decoupled, you can "
        "swap a robot, change a controller, or expose a skill as a service without "
        "rewriting the model.")
    doc.add_paragraph(
        f"This document describes MAESTRO version {VERSION}: its nine-layer "
        "architecture, each of the 24 ontology modules with its current classes "
        "and fields, the reasoning pipeline, a worked example, and the planned "
        "future work for validation and extension.")

    # ---- 2. Architecture overview ---------------------------------------
    doc.add_heading("2. Architecture overview — the nine-layer stack", level=1)
    doc.add_paragraph(
        "MAESTRO is organised as a nine-layer semantic stack. Each layer talks "
        "only to the layer immediately below it, and each layer is replaceable in "
        "isolation. From top to bottom: Product (what is made), Process (how), "
        "Capability (what the plant can do), Skill (logical behaviour), "
        "Orchestration (the SPARQL/SHACL/LLM reasoning fabric), Execution (ROS, "
        "PLC, IEC 61499, OPC UA, AAS), Resource (physical machines), Motion "
        "(kinematic primitives), and the Physical Factory itself.")
    add_figure(doc, "01-semantic-stack.png", "Figure 1 — The nine-layer semantic stack.")
    doc.add_paragraph(
        "Three boundaries do most of the work and are the reason the stack stays "
        "future-proof:")
    for b in (
        "Capability ↔ Skill — separates what is possible (vendor-neutral "
        "intent) from how it is achieved (logical behaviour).",
        "Skill ↔ Execution — separates technology-neutral behaviour from "
        "technology-specific implementation (ROS / PLC / IEC 61499 / OPC UA).",
        "Resource ↔ Motion — separates the physical asset from the geometric "
        "and kinematic semantics of how it moves."):
        doc.add_paragraph(b, style="List Bullet")

    # ---- 3. Modular stack ------------------------------------------------
    doc.add_heading("3. The modular stack and import graph", level=1)
    doc.add_paragraph(
        "The vocabulary is split into 24 small TTL modules grouped by concern and "
        "tied together by a single umbrella file, maestro.ttl, which imports them "
        "all. Every module imports only what it needs (most depend just on core), "
        "which keeps the stack easy to extend: a new concern is a new file plus "
        "one owl:imports line. All modules share the permanent namespace base "
        "https://w3id.org/maestro/ and carry version " + VERSION + ".")
    add_figure(doc, "02-modular-stack.png", "Figure 2 — The 24 modules and the umbrella import graph.")

    # ---- 4. Module-by-module reference -----------------------------------
    doc.add_heading("4. Module-by-module reference", level=1)
    doc.add_paragraph(
        "Each module below lists its purpose, its namespace prefix and IRI, and "
        "the classes, properties and notable individuals it currently defines. "
        "Tables are generated directly from the TTL source, so they reflect the "
        "live ontology.")

    sec = 1
    for cat_name, cat_blurb, modules in CATEGORIES:
        doc.add_heading(f"4.{sec}  {cat_name}", level=2)
        doc.add_paragraph(cat_blurb)
        for rel_path, prefix, iri, friendly, purpose, figure in modules:
            classes, properties, individuals = parse_module(rel_path)
            print(f"{rel_path}: {len(classes)} classes, "
                  f"{len(properties)} properties, {len(individuals)} individuals")

            doc.add_heading(f"{friendly}  ({prefix}:)", level=3)
            meta = doc.add_paragraph()
            meta.add_run("File: ").bold = True
            meta.add_run(f"ontologies/{rel_path}    ")
            meta.add_run("Namespace: ").bold = True
            meta.add_run(iri)
            doc.add_paragraph(purpose)

            if figure:
                add_figure(doc, figure, f"Figure — {friendly} ({figure}).", width=6.0)

            if classes:
                doc.add_paragraph().add_run("Classes").bold = True
                add_table(doc, ["Class", "Subclass of", "Description"],
                          classes, widths=[1.7, 1.7, 3.0])
            if properties:
                doc.add_paragraph().add_run("Properties").bold = True
                add_table(doc, ["Property", "Kind", "Domain → Range", "Description"],
                          properties, widths=[1.6, 0.7, 2.0, 2.1])
            if individuals:
                doc.add_paragraph().add_run("Individuals").bold = True
                add_table(doc, ["Individual", "Type", "Description"],
                          individuals, widths=[1.7, 1.7, 3.0])
        sec += 1

    # ---- 5. Reasoning ----------------------------------------------------
    doc.add_heading("5. Reasoning and the LLM pipeline", level=1)
    doc.add_paragraph(
        "MAESTRO reasons over the graph in layers: OWL2-RL handles semantic "
        "inheritance, SHACL validates the data, SPARQL CONSTRUCT rules infer "
        "capabilities, and SPARQL queries drive orchestration. The canonical "
        "reasoning chain threads the whole stack together:")
    chain = doc.add_paragraph()
    cr = chain.add_run("Product → Process → Capability → Skill "
                       "→ ControlComponent → Resource → Motion")
    cr.bold = True; cr.font.color.rgb = NAVY
    add_figure(doc, "04-reasoning-chain.png", "Figure 3 — The core reasoning chain.")
    doc.add_paragraph(
        "On top of this, a Large Language Model translates a natural-language "
        "question into SPARQL, runs it against the graph database, and explains "
        "the deterministic result. The LLM never stores facts — it only "
        "translates intent and narrates answers; all knowledge lives in the graph.")
    add_figure(doc, "05-llm-graphdb-pipeline.png",
               "Figure 4 — The LLM + graph-database reasoning pipeline.")

    # ---- 6. Standards alignment -----------------------------------------
    doc.add_heading("6. Standards alignment", level=1)
    doc.add_paragraph(
        "MAESTRO does not reinvent existing standards; it federates with them so "
        "models stay interoperable and vendor-independent.")
    add_figure(doc, "09-standards-honeycomb.png",
               "Figure 5 — External standards MAESTRO aligns with.")
    add_table(doc, ["Standard", "Role in MAESTRO", "Module(s)"], [
        ("DIN 8580", "Manufacturing process taxonomy", "process"),
        ("VDI 2860", "Handling skill categories", "skill"),
        ("VDI 3682", "Process sequencing", "process"),
        ("IEC 61131-3", "Classic PLC programming model", "iec61131"),
        ("IEC 61499", "Event-driven distributed control", "iec61499"),
        ("OPC UA", "Interoperable skill interfaces", "opcua"),
        ("Asset Administration Shell", "Digital-twin envelope", "aas"),
        ("ISA-95", "Enterprise / planning hierarchy", "planning"),
        ("PackML", "Operational state model", "runtime"),
        ("IEC 61508 / ISO 13849", "Functional safety (SIL / PL)", "safety"),
        ("QUDT", "Units and quantities", "unit"),
        ("W3C SOSA / SSN", "Sensors and observations", "sensor"),
        ("W3C SKOS", "Capability & state concept schemes", "capability, runtime"),
    ], widths=[2.2, 3.0, 1.6])

    # ---- 7. Worked example ----------------------------------------------
    doc.add_heading("7. Worked example — the Distribution Station", level=1)
    doc.add_paragraph(
        "The Festo MPS Distributing Station is modelled end-to-end as the "
        "reference example. Its plant topology, skill bridge and reasoning "
        "pipeline are all expressed with the same modules described above.")
    add_figure(doc, "ds-01-plant-topology.png", "Figure 6 — Distribution Station plant topology.")
    add_figure(doc, "ds-02-skill-bridge.png",
               "Figure 7 — Bridging resource-side skill types to library skills.")
    add_figure(doc, "ds-03-reasoning-pipeline.png",
               "Figure 8 — Distribution Station reasoning pipeline.")
    add_figure(doc, "ds-05-three-layers.png",
               "Figure 9 — The three-layer (design / reasoning / runtime) view.")
    res = doc.add_paragraph()
    res.add_run("Verified result: ").bold = True
    rr = res.add_run("ex:DistributingStation1 core:canManufacture ex:WorkpieceWP3")
    rr.font.name = "Consolas"; rr.font.color.rgb = NAVY
    doc.add_paragraph(
        "This conclusion is inferred — not asserted — from a live GraphDB session "
        "of roughly 5,500 triples using OWL2-RL plus two SPARQL CONSTRUCT rules.")

    # ---- 8. Future works -------------------------------------------------
    doc.add_heading("8. Future works", level=1)
    doc.add_heading("8.1  Validation roadmap (Festo MPS stations)", level=2)
    doc.add_paragraph(
        "The framework is being validated against Festo MPS reference stations in "
        "three milestones. Milestone numbers (M1/M2/M3) are independent of the "
        "code release version.")
    add_table(doc, ["Milestone", "Station", "Focus", "Query class enabled"], [
        ("M1 (v0.1)", "Distributing Station",
         "Base stack: 16 modules, plant + product + runtime; largely complete.",
         "Basic feasibility — canManufacture, canPerform"),
        ("M2 (v0.2)", "Distributing Station",
         "Constant-speed motion sub-classes for timing; safety (SIL) instances.",
         "Time-aware — cycle-time, scheduling, SIL filtering"),
        ("M3 (v0.3)", "Drilling Station",
         "Second station for portability; AAS digital twin; machine operations.",
         "Gap identification — find missing capabilities"),
    ], widths=[1.1, 1.6, 2.7, 2.0])
    doc.add_paragraph(
        "Each milestone closes with new example files, new SPARQL queries, and a "
        "git tag (v0.1-roadmap-m1 … v0.3-roadmap-m3). Open questions for review "
        "include whether security belongs in M2 or M3, whether the Drilling "
        "Station is a physical or model-only target, and confirming the M1/M2/M3 "
        "naming alongside semantic version tags.")

    doc.add_heading("8.2  Industry 5.0 extensions", level=2)
    doc.add_paragraph(
        "MAESTRO is designed so the next generation of manufacturing concepts can "
        "be added as new modules rather than patches. The current stack already "
        "accommodates:")
    add_table(doc, ["Extension", "How MAESTRO supports it today"], [
        ("Autonomous factories", "The machine-readable reasoning chain lets a planner traverse it without human guidance."),
        ("AI manufacturing agents", "Agents talk to SPARQL, not directly to PLCs; intent extraction is separated from deterministic reasoning."),
        ("Self-reconfiguration", "Skills are not bound to resources; swapping an end-effector re-fires capability inference."),
        ("Manufacturing-as-a-Service", "OPC UA SkillInterfaces expose skills network-wide for remote invocation."),
        ("Semantic digital twins", "aas + runtime cover the AAS envelope plus live behaviour."),
        ("Predictive maintenance", "maintenance carries RUL, MTBF and a dedicated Predictive action class."),
        ("Energy-aware manufacturing", "energy exposes power, energy and carbon intensity by source."),
        ("Human-robot collaboration", "Cobot + safety (SIL/PL) describe the safety envelope; runtime states make it explicit."),
    ], widths=[2.2, 4.4])

    # ---- 9. Glossary -----------------------------------------------------
    doc.add_heading("9. Glossary — namespace prefixes", level=1)
    add_table(doc, ["Prefix", "Namespace IRI", "Module"], [
        ("core:", "https://w3id.org/maestro/core#", "manufacturing-core.ttl"),
        ("res:", "https://w3id.org/maestro/resource#", "resource.ttl"),
        ("motion:", "https://w3id.org/maestro/motion#", "motion.ttl"),
        ("skill:", "https://w3id.org/maestro/skill#", "skill.ttl"),
        ("cap:", "https://w3id.org/maestro/capability#", "capability.ttl"),
        ("proc:", "https://w3id.org/maestro/process#", "process.ttl"),
        ("prod:", "https://w3id.org/maestro/product#", "product.ttl"),
        ("plc:", "https://w3id.org/maestro/iec61131#", "iec61131.ttl"),
        ("iec61499:", "https://w3id.org/maestro/iec61499#", "iec61499.ttl"),
        ("ros:", "https://w3id.org/maestro/ros#", "ros.ttl"),
        ("opcua:", "https://w3id.org/maestro/opcua#", "opcua.ttl"),
        ("aas:", "https://w3id.org/maestro/aas#", "aas.ttl"),
        ("runtime:", "https://w3id.org/maestro/runtime#", "runtime.ttl"),
        ("state:", "https://w3id.org/maestro/state#", "state.ttl"),
        ("sensor:", "https://w3id.org/maestro/sensor#", "sensor.ttl"),
        ("unit:", "https://w3id.org/maestro/unit#", "unit.ttl"),
        ("com:", "https://w3id.org/maestro/communication#", "communication.ttl"),
        ("safety:", "https://w3id.org/maestro/safety#", "safety.ttl"),
        ("qa:", "https://w3id.org/maestro/quality#", "quality.ttl"),
        ("maint:", "https://w3id.org/maestro/maintenance#", "maintenance.ttl"),
        ("energy:", "https://w3id.org/maestro/energy#", "energy.ttl"),
        ("reas:", "https://w3id.org/maestro/reasoning#", "reasoning.ttl"),
        ("plan:", "https://w3id.org/maestro/planning#", "planning.ttl"),
        ("skill-lib:", "https://w3id.org/maestro/skill-lib#", "skill-lib.ttl"),
        ("motion-lib:", "https://w3id.org/maestro/motion-lib#", "motion-lib.ttl"),
    ], widths=[1.3, 3.5, 1.8])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT))
    print(f"\nSaved: {OUT}")


if __name__ == "__main__":
    build()
