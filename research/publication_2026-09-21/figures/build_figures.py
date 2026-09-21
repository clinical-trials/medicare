#!/usr/bin/env python3
"""Build publication diagrams from archived counts; requires Matplotlib.

Run with a Python environment containing matplotlib:
    python build_figures.py

SVG text remains editable. PNGs are exactly 7 inches wide at 300 dpi.
The diagrams describe review status and a proposed validation framework,
not completed PRISMA selection, intervention efficacy or formal certainty.
"""
from pathlib import Path
import json
import os

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/medicare-matplotlib-config")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent
PROJECT = OUT.parents[2]
PUB = OUT.parent
BLUE = "#315E86"
PALE = "#F0F5F9"
BLACK = "#151515"
LINE = "#8B98A4"
matplotlib.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "text.color": BLACK,
    "svg.fonttype": "none",
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

def canvas(height):
    fig = plt.figure(figsize=(7, height))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 7)
    ax.set_ylim(0, height)
    ax.axis("off")
    return fig, ax

def box(ax, x, y, w, h, fill="white", dashed=False):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.035",
                      linewidth=1.0, edgecolor=BLUE if fill == PALE else LINE,
                      facecolor=fill, linestyle=(0, (4, 3)) if dashed else "solid")
    ax.add_patch(p)
    return p

def txt(ax, x, y, s, size=10, weight="normal", ha="left", va="center"):
    return ax.text(x, y, s, fontsize=size, fontweight=weight, ha=ha, va=va,
                   color=BLACK, linespacing=1.30)

def arrow(ax, start, end, color=BLUE):
    p = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10,
                        linewidth=1.1, color=color, shrinkA=0, shrinkB=0)
    ax.add_patch(p)

def line(ax, points):
    ax.plot([p[0] for p in points], [p[1] for p in points], color=BLUE, lw=1.1,
            solid_capstyle="round", zorder=0)

def save(fig, name, description):
    for suffix in ("svg", "png"):
        fig.savefig(OUT / f"{name}.{suffix}", dpi=300,
                    metadata={"Description": description} if suffix == "svg" else
                             {"Description": description, "Software": "Matplotlib"})
    plt.close(fig)

extension = json.loads((PUB / "search_extensions/manifest.json").read_text())
queue = json.loads((PUB / "queue_summary.json").read_text())
baseline = json.loads((PROJECT / "research/review_2026-09-21/search_summary.json").read_text())
counts = {
    "baseline_core_hits": baseline["corrected_core"],
    "baseline_supplemental_hits": baseline["supplement"],
    "baseline_raw_hits": baseline["corrected_core"] + baseline["supplement"],
    "baseline_exact_PMID_duplicates": baseline["duplicate_hits_removed_by_pmid"],
    "baseline_unique": extension["baseline_unique_records"],
    "extension_hits": extension["extension_raw_hits"],
    "extension_baseline_overlap": extension["extension_overlap_with_baseline"],
    "extension_new": extension["new_unique_records"],
    "combined_unique": extension["combined_unique_records"],
    "abstract_available": queue["abstracts"],
    "abstract_unavailable": queue["no_abstracts"],
    "separately_selected_register": 38,
}
assert counts["baseline_core_hits"] + counts["baseline_supplemental_hits"] == counts["baseline_raw_hits"]
assert counts["baseline_raw_hits"] - counts["baseline_exact_PMID_duplicates"] == counts["baseline_unique"] == 58686
assert counts["extension_hits"] - counts["extension_baseline_overlap"] == counts["extension_new"] == 461
assert counts["baseline_unique"] + counts["extension_new"] == counts["combined_unique"] == queue["records"] == 59147
assert counts["abstract_available"] + counts["abstract_unavailable"] == counts["combined_unique"]
assert queue["human_screened"] == 0 and queue["records_excluded"] == 0

# Figure 1: separate two retrieval routes and prevent the selected register
# from looking like an included-study count from the unreviewed corpus.
fig, ax = canvas(7.6)
txt(ax, .35, 7.23, "Figure 1. Retrieval and review status", 14, "bold")
txt(ax, .35, 6.92, "21 September 2026 | Development searches; selection review incomplete", 9.5)

for x, title, number, detail in [
    (.35, "Baseline PubMed queries", "60,770 records", "43,904 core + 16,866 supplemental"),
    (3.70, "Targeted PubMed extensions", "756 records", "494 bone care + 262 prescription IT"),
]:
    box(ax, x, 5.70, 2.95, 1.00)
    txt(ax, x+1.475, 6.47, title, 10.6, "bold", ha="center")
    txt(ax, x+1.475, 6.14, number, 15, "bold", ha="center")
    txt(ax, x+1.475, 5.87, detail, 8.9, ha="center")

arrow(ax, (1.825, 5.68), (1.825, 5.30))
arrow(ax, (5.175, 5.68), (5.175, 5.30))
for x, title, detail in [
    (.35, "58,686 unique PMIDs", "2,084 exact-PMID duplicates removed"),
    (3.70, "461 additional PMIDs", "295 baseline-overlapping hits removed"),
]:
    box(ax, x, 4.43, 2.95, .85)
    txt(ax, x+1.475, 4.97, title, 12.2, "bold", ha="center")
    txt(ax, x+1.475, 4.64, detail, 8.9, ha="center")

line(ax, [(1.825,4.42),(1.825,4.23),(5.175,4.23),(5.175,4.42)])
arrow(ax, (3.5,4.23), (3.5,4.02))
box(ax, 1.23, 3.31, 4.54, .69, fill=PALE)
txt(ax, 3.5, 3.75, "59,147 unique records combined", 13, "bold", ha="center")
txt(ax, 3.5, 3.49, "Bibliographic metadata retrieved for every record", 9.6, ha="center")

line(ax, [(3.5,3.30),(3.5,3.10),(1.825,3.10),(1.825,2.97)])
line(ax, [(3.5,3.10),(5.175,3.10),(5.175,2.97)])
arrow(ax, (1.825,2.97), (1.825,2.83))
arrow(ax, (5.175,2.97), (5.175,2.83))
for x, title, detail in [
    (.35, "47,152 with abstracts", "Available for title/abstract review"),
    (3.70, "11,995 without abstracts", "Retained; retrieval judgment required"),
]:
    box(ax, x, 2.17, 2.95, .64)
    txt(ax, x+1.475, 2.58, title, 11.8, "bold", ha="center")
    txt(ax, x+1.475, 2.33, detail, 9.0, ha="center")

line(ax, [(1.825,2.16),(1.825,2.01),(5.175,2.01),(5.175,2.16)])
arrow(ax, (3.5,2.01), (3.5,1.79))
box(ax, .35, 1.08, 6.30, .69, fill=PALE)
txt(ax, 3.5, 1.54, "Human screening and appraisal pending", 12.5, "bold", ha="center")
txt(ax, 3.5, 1.28, "Eligibility, related reports, extraction verification and outcome certainty", 9.8, ha="center")

box(ax, .35, .21, 6.30, .58, dashed=True)
txt(ax, 3.5, .59, "Separate selected register: 38 candidate or contextual records", 10.8, "bold", ha="center")
txt(ax, 3.5, .36, "Earlier selected retrieval; not the screening output of this corpus", 9.6, ha="center")
save(fig, "figure1_retrieval_status",
     "Actual development-search retrieval status, September21,2026. Not a completed PRISMA selection flow. The separately selected register is not an included-study count from the corpus.")

# Figure 2: five validation stages; prospective, not a claim that products
# or the selected evidence have already passed any stage.
fig, ax = canvas(7.6)
txt(ax, .35, 7.23, "Figure 2. A health IT validation pathway", 14, "bold")
txt(ax, .35, 6.91, "Proposed research framework | Evidence is required at each stage", 9.8)
stages = [
    ("1  NEED", "Define clinically indicated care and unmet need.",
     "Use an eligible denominator; include patients who receive no care."),
    ("2  MECHANISM", "Identify where financing or delivery impedes care.",
     "Distinguish coverage, cost, authorization, referral and follow-through."),
    ("3  INTERVENTION", "Specify the workflow, comparator and causal hypothesis.",
     "Separate software effects from staffing, subsidies and other support."),
    ("4  BENEFIT AND EQUITY", "Test patient benefit, harms and equitable reach.",
     "Prespecify sex comparisons; assess health outcomes beyond process."),
    ("5  IMPLEMENTATION", "Verify feasibility, sustained outcomes and a credible buyer.",
     "Measure workload, data access, cost and adoption; payment is distinct."),
]
for i, (label, main, detail) in enumerate(stages):
    y = 5.53 - i*1.14
    box(ax, .35, y, 6.30, .97, fill=PALE if i == 3 else "white")
    ax.plot([.35,.35],[y+.07,y+.90],color=BLUE,lw=3)
    txt(ax, .58, y+.75, label, 11.2, "bold")
    txt(ax, .58, y+.46, main, 10.8)
    txt(ax, .58, y+.19, detail, 9.5)
    if i < 4:
        arrow(ax, (3.5,y-.02), (3.5,y-.15))
txt(ax, .35, .57, "Advance, revise or stop according to the evidence.", 11.1, "bold")
txt(ax, .35, .29, "Average benefit does not establish equity; a coverage code does not establish a market.", 9.2)
save(fig, "figure2_validation_pathway",
     "Conceptual five-stage health IT validation pathway: need, mechanism, intervention, benefit and equity, implementation. Proposed research framework, not validated product efficacy or commercial viability.")

manifest = {
    "generated_on": "2026-09-21",
    "generator": "Matplotlib " + matplotlib.__version__,
    "dimensions_inches": [7,7.6], "png_dpi": 300,
    "counts": counts,
    "source_files": ["research/review_2026-09-21/search_summary.json", "research/publication_2026-09-21/search_extensions/manifest.json", "research/publication_2026-09-21/queue_summary.json", "research/publication_2026-09-21/manuscript.md"],
    "outputs": ["figure1_retrieval_status.svg","figure1_retrieval_status.png","figure2_validation_pathway.svg","figure2_validation_pathway.png"],
    "interpretation": ["Figure1 is actual retrieval status, not a completed PRISMA selection flow.", "38 selected records are a separate route, not screening output.", "Figure2 is a proposed five-stage validation framework, not a claim of validated products."],
}
(OUT / "figure_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print("Built four figure files; count reconciliation passed.")
