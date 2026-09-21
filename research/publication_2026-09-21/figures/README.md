# Seven figure expanded publication edition

The investigator requested more than five figures on September 21, 2026. The manuscript now includes seven numbered figures in order of first citation:

1. Separate the subjects of comparison
2. Inclusion and exclusion criteria
3. Clinical anatomy and physiology
4. Retrieval and review status
5. Financing and care outcomes
6. Health IT research opportunities
7. A health IT validation pathway

All have editable SVG and 300-dpi PNG exports at 7 by 7.6 inches. [Download the complete set with captions and provenance](../../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_seven_publication_figures_2026-09-21.zip). The manuscript's bibliography includes all caption citations and numeric PMIDs where applicable. Figure 4 alone reports search counts; the other figures are conceptual frameworks, not new empirical findings.

`expanded_figure_manifest.json` records the seven final assets, captions, source hashes and export hashes. `expanded_figure_content.json` preserves panel content and reference provenance. Rebuild Figures 4 and 7 with `build_figures.py` using Matplotlib; rebuild Figures 1, 2, 3, 5 and 6 and the ZIP with `build_expanded_figures.py` using ReportLab and Poppler. Then run `build_publication.py`, render the DOCX and inspect all pages. The original two diagram exports and their earlier audit below remain as history; current numbering is given above.

The expanded edition supersedes the earlier four-display planning budget for the working white paper. Final journal selection of main and supplementary displays remains pending. The separate, detailed eligibility figure remains unchanged; Figure 2 is a compact manuscript adaptation. No population-scope change, evidence addition, final eligibility decision or formal appraisal is implied.

---

# Publication figures and intervention-section audit

Generated September 21, 2026. This is an AI consistency audit, not independent human evidence screening or appraisal.

## Files

- `figure1_retrieval_status.svg` and `.png`: actual development-search retrieval and review status. The 38-record selected register is a separate, unconnected panel, not an included-study count from the search corpus.
- `figure2_validation_pathway.svg` and `.png`: proposed five-stage health IT research framework: need, mechanism, intervention, benefit and equity, implementation.
- `build_figures.py`: reusable Matplotlib generator with checks against the archived search/queue summaries.
- `figure_manifest.json`: dimensions, counts, provenance and inference limits.

Each figure is 7 by 7.6 inches. PNGs are 2,100 by 2,280 pixels at 300 dpi. SVGs retain editable text. Both rendered PNGs were visually inspected for legibility, clipping, arrows and label placement. All text is black on white or pale blue, with restrained blue connectors and accents.

The script requires Matplotlib. In this environment it was installed in a temporary dependency directory and run as:

```sh
PYTHONPATH=/private/tmp/medicare-figure-deps /Users/lgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/publication_2026-09-21/figures/build_figures.py
```

In another environment, use any compatible Python installation with Matplotlib. The diagrams are dated snapshots; count assertions intentionally fail if the archived counts change without updating figure labels.

## Figure 1 reconciliation

60,770 baseline query hits minus 2,084 exact-PMID duplicates = 58,686 unique baseline records. The two extensions contain 756 records, including 295 already present in the baseline, leaving 461 additional records. Combined unique records = 59,147 = 47,152 with abstracts + 11,995 without abstracts. These abstract counts indicate available metadata, not screening decisions. Human screening, eligibility adjudication, related-report linkage and formal appraisal remain pending.

The source is one database's development searches, not a complete multi-database search or completed PRISMA selection flow. The selected 38 candidate/context records were assembled through earlier retrieval and are not the result of corpus screening.

## Intervention manuscript audit

Checked `manuscript.md` against `intervention_evidence.json`, including L-G05 and L-T01–03, the linked parent L-T03-P1 and relevant discussion boundaries.

The reported denominators, effect estimates, confidence intervals, exploratory Medicare subgroup status, lack of sex-gap evidence and shared-trial dependence match the extraction. L-G05 correctly distinguishes 10,934 randomized from 7,842 analyzed and notes 28.3% post-assignment exclusions.

Three clarity recommendations were sent to the manuscript author and confirmed in the revised text:

1. L-T02 total spending is **total prescription spending**, not all health spending.
2. The Figure 2 description now includes all five conceptual elements, with benefit/equity distinct.
3. L-T01's exclusion of low-income subsidy beneficiaries is stated.

No remaining material discrepancy was identified in this bounded intervention-section check. This audit did not reappraise all other manuscript evidence or resolve the published-source inconsistencies already recorded in `intervention_search_log.md`. No manuscript or canonical JSON was edited by this task.
# Standalone eligibility figure

The [inclusion and exclusion figure](../../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/eligibility_figure/) adds PDF, editable SVG, 300-dpi PNG and a publication caption for future use. It distinguishes adopted scope from proposed operational screening, unresolved eligibility from exclusions, and patient evidence from service valuation and context. It introduces no study counts or scope amendment. Regenerate with `build_eligibility_figure.py` using the bundled Python runtime; this builder uses ReportLab and Poppler. Source/output hashes are in `eligibility_figure_manifest.json`.
