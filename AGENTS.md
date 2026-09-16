# Medicare research workspace

Read `REVIEW_SCOPE.md` before further evidence screening, synthesis, or white-paper drafting. It records the user's current population criterion and how to handle unreported gender identity and mixed-population studies.

Preserve original broad-search source records as an audit trail. Use `research/scoped_evidence.json` and the current workbook for the active register. Excluded records belong in the exclusion log, not the primary synthesis.

Classify every added care-item/indication in `research/clinical_basis.json`. Keep shared anatomy/functions, sex-linked reproductive anatomy, reproductive physiology and mixed/site-dependent services distinct. Sex-defined policy eligibility and disease burden are separate from anatomy. Preserve this distinction in the dashboard and white paper; do not force mixed rows into one sex.

Use `research/medicare_benchmark.json` for the later-life Medicare benchmark rationale. Keep utilization, spending and unmet need distinct; preserve age and entitlement strata, including younger Medicare beneficiaries. Do not describe Medicare as financing most US care or age-specific cross-sectional spending as a lifetime share of care.

`research/workbook/build_evidence.mjs` builds the original broad register. If rebuilding from it, run `research/workbook/apply_scope.mjs` afterwards to apply the current scope. Do not describe the working register as a completed systematic review.

Maintain citations and the living bibliography on every evidence update. Preserve stable study IDs, original citations, DOI/PMID, source URLs, review status, access level and correction links. Verify new scientific metadata in `research/bibliography_metadata.json`; bibliographic verification is separate from full-text review and study eligibility. Do not automatically import references cited by a review as screened evidence.

`apply_scope.mjs` synchronizes verified citations into the register and regenerates the human-readable bibliography, RIS export and `research/reference_registry.json` through `research/workbook/bibliography.mjs`. Preserve excluded records as an audit trail and distinguish corrections from independent studies. Use `[L-ID]` in working white-paper drafts until final journal numbering is assigned. Policy sources use stable `P-###` IDs; descriptive labels are not asserted publication titles.
