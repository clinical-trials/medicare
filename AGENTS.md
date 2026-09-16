# Medicare research workspace

Read `REVIEW_SCOPE.md` before further evidence screening, synthesis, or white-paper drafting. It records the user's current population criterion and how to handle unreported gender identity and mixed-population studies.

Preserve original broad-search source records as an audit trail. Use `research/scoped_evidence.json` and the current workbook for the active register. Excluded records belong in the exclusion log, not the primary synthesis.

Classify every added care-item/indication in `research/clinical_basis.json`. Keep shared anatomy/functions, sex-linked reproductive anatomy, reproductive physiology and mixed/site-dependent services distinct. Sex-defined policy eligibility and disease burden are separate from anatomy. Preserve this distinction in the dashboard and white paper; do not force mixed rows into one sex.

Use `research/medicare_benchmark.json` for the later-life Medicare benchmark rationale. Keep utilization, spending and unmet need distinct; preserve age and entitlement strata, including younger Medicare beneficiaries. Do not describe Medicare as financing most US care or age-specific cross-sectional spending as a lifetime share of care.

`research/workbook/build_evidence.mjs` builds the original broad register. If rebuilding from it, run `research/workbook/apply_scope.mjs` afterwards to apply the current scope. Do not describe the working register as a completed systematic review.

Maintain citations and the living bibliography on every evidence update. Preserve stable study IDs, original citations, DOI/PMID, source URLs, review status, access level and correction links. Verify new scientific metadata in `research/bibliography_metadata.json`; bibliographic verification is separate from full-text review and study eligibility. Do not automatically import references cited by a review as screened evidence.

The investigator identified the Lancet review by Mauvais-Jarvis et al., "Sex and gender: modifiers of health, disease, and medicine" (L-B01; PMID 32828189), as a key organizing review for the broad inquiry. Prioritize its clinical framework and reference list when expanding the search, while screening underlying articles independently. Retain its linked correction (L-B01-E1; PMID 32891210).

Keep a verified PMID for every scientific article whenever available, including excluded articles and corrections. Match PMID to title, authors and DOI; never substitute a PMCID or DOI for a PMID. Preserve PMIDs in metadata, the register, the bibliography and RIS export. If a PMID is missing, record whether lookup is pending or no matching PubMed record was found, with the lookup date and source; do not silently leave the reason unknown or invent an identifier. Show the numeric PMID explicitly in the bibliography.

`apply_scope.mjs` synchronizes verified citations into the register and regenerates the human-readable bibliography, RIS export and `research/reference_registry.json` through `research/workbook/bibliography.mjs`. Preserve excluded records as an audit trail and distinguish corrections from independent studies. Use `[L-ID]` in working white-paper drafts until final journal numbering is assigned. Policy sources use stable `P-###` IDs; descriptive labels are not asserted publication titles.

Classify every active study in `research/evidence_subjects.json`. Distinguish patient sex/gender, physician sex/gender, service/anatomy valuation and general background, retaining each variable’s role, unit and comparison axis. Physician-gender evidence is a separate contextual stream; clinician respondents or prescriber datasets do not alone imply a physician-gender comparison. Do not infer patient disparities from clinician payment totals or code valuations.

Maintain `research/preliminary_synthesis.json` as the exploratory pattern and hypothesis register. `research/workbook/synthesis.mjs`, called by `apply_scope.mjs`, generates the synthesis report, Hypotheses sheet, dashboard pattern summary and derived formulary states. Separate observations from hypotheses, retain opposing evidence and falsification criteria, and preserve PMIDs. Hypotheses were developed after inspecting the selected evidence; do not call them prospectively registered or confirmed causal results.

Public explanations must distinguish PRISMA reporting guidance from GRADE assessment of certainty for a body of evidence about an outcome. Do not describe PRISMA as a quality score, grade each paper as if that were full GRADE, or claim completed formal ratings before assessment. Keep methodology references and PMIDs in `research/methodology_references.json` and the bibliography under M-IDs, separate from the clinical evidence counts. The press concept is a draft, not an announcement of completed review findings.
