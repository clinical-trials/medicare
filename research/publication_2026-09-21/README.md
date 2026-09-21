# Medicare equity manuscript and health IT opportunity assessment

Prepared September 21, 2026. This package advances the systematic review and its use by researchers and health IT developers. The manuscript is a journal-style **preliminary evidence synthesis and methods package for a systematic review in progress**. It is not a completed systematic review, a reimbursement census, a registered prospective study or an investment recommendation.

## Deliverables

- [PDF manuscript and supplements](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_equity_research_and_health_IT_manuscript_2026-09-21.pdf)
- [Editable Word manuscript](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_equity_research_and_health_IT_manuscript_2026-09-21.docx)
- [Opportunity assessment workbook](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_health_IT_opportunity_assessment_2026-09-21.xlsx)
- [Seven figures with editable SVGs and captions](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_seven_publication_figures_2026-09-21.zip)
- [Main text](manuscript.md), [supplemental methods](supplemental_methods.md), [main tables](publication_tables.json) and [editable scientific figures](figures/)
- [Current evidence register and dashboard](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_evidence_register_2026-09-16.xlsx)
- [Living bibliography](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_bibliography.md) and [RIS](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_references.ris)

The main draft has a 68-character title, 199-word abstract, three key takeaways, six keywords and approximately 3,500 main-text words. At the investigator's request, the expanded research and white-paper edition includes seven figures and two tables. This supersedes the earlier four-display planning budget for this edition; allocation between main text and supplements will be adapted to the final submission journal. Word-count exclusions, editorial fit and final journal requirements must be confirmed at submission. Supplements preserve the detailed methods and opportunity records. No submission or editor contact has occurred.

## What changed

Two targeted PubMed development extensions addressed a known bone-testing retrieval miss and the new health IT purpose. The bone query returned 494 records; the prescription-information query returned 262. Their 756 unique records overlapped the baseline by 295, adding 461 to 58,686, for **59,147**. All have metadata; 47,152 have abstracts and 11,995 do not. Five of the 461 additions are PubMed BookArticle records; the parser preserves that type. These are report records, not necessarily independent studies.

The complete [compressed review queue](review_queue.csv.gz) retains every record. Keyword tiers prioritize reading without excluding records. Seventeen shared-DOI groups and 303 normalized-title groups await report-family inspection; they are not automatically merged duplicates. The prepared 50-record calibration set still has blank human review fields. Human screening, remaining database searches, independent PRESS review, final eligibility, formal appraisal and certainty assessment remain unfinished.

The [intervention extraction](intervention_evidence.json) includes an expanded review of existing L-G05 and new L-T01, L-T02 and L-T03. L-T03-P1 is the same trial's parent report. Three new independent intervention families supply contextual evidence; no primary patient-sex study was added through this route. Positive process findings, null results, attrition, subgroup limits, funding and conflicts are retained. Source discrepancies are not silently corrected. None of the reviewed interventions demonstrates closure of a patient-sex equity gap.

The canonical scientific metadata contain **53** records: 38 active, eight scope exclusions, one correction, two earlier outside-register references and four new translational reports. Eleven methods references, 58 policy/data sources and four clinical guidance sources are separate. The manuscript prints 63 substantive references; the full bibliography/RIS preserve the wider audit trail. All scientific and methodological PMIDs are retained when available.

## Opportunity domains

The six domains are medication affordability, post-fracture follow-up, non-drug authorization, procedure-valuation research, lymphedema fulfillment and kidney-care coordination. Each distinguishes clinical need, the proposed intervention, measurable patient benefit, equity evaluation, implementation needs and unverified commercial assumptions. Evidence of a problem is not evidence that software fixes it; neither establishes demand or a sustainable business. Domains are unranked.

[Opportunity records](opportunities.json), [current policy sources](opportunity_policy_sources.json), [clinical classification](../clinical_basis.json) and [publication evidence roles](evidence_roles.json) retain the anatomy/physiology, patient/physician and payer distinctions. Shared bone, lymphatic and renal functions are not assigned to one sex solely because of disease burden. Local vaginal treatment and systemic menopausal therapy retain different clinical bases.

## Review readiness and audit

See [readiness.json](readiness.json), [methods audit](methods_audit.md), [manuscript checks](manuscript_review.md), [build counts](publication_build.json) and [verification](verification.json). The present scope leaves identity-unreported cohorts outside confirmed-cisgender primary estimates. A proposed separately labeled recorded-sex analysis is awaiting investigator clarification; it was not silently adopted. Human reviewer appointments also remain unconfirmed.

The original search and source records are preserved. The targeted extensions and opportunity framework were developed after preliminary evidence inspection. Their dates and reasons are recorded; they are not retrospectively described as prospective registration.

## Reproduction

Use the bundled Codex Python/Node runtimes and artifact-tool package. Builders contain the existing project's local paths; configure these when reproducing elsewhere. No portable installation or locked third-party runtime is packaged.

1. Read `REVIEW_SCOPE.md`. The initial search audit is in `research/review_2026-09-21/README.md`.
2. `search_extensions.py` contains the extension retrieval procedure; `search_extensions/queries.json` and `manifest.json` retain the exact executed queries, translations, memberships and hashes. Do not overwrite the archive to refresh a search; use a new dated directory.
3. `prepare_review_queue.py` reconciles saved baseline and extension metadata into the all-record queue without screening or exclusions.
4. `integrate_publication.py` synchronizes the verified translational records, separate clinical-indication classifications, L-G05 overlay, opportunity assessment and primary appraisal references. It does not alter original broad-search sources.
5. `research/workbook/apply_scope.mjs` rebuilds the scoped register, bibliography, RIS, analysis framework and existing synthesis. The opportunity workbook has its own builder in this directory.
6. `figures/build_figures.py` generates the retrieval and validation diagrams, now Figures 4 and 7. `figures/build_expanded_figures.py` generates Figures 1, 2, 3, 5 and 6 with ReportLab and Poppler, then packages all seven SVG/300-dpi PNG pairs, captions and source provenance. `build_publication.py` generates the editable DOCX from the main text, supplemental methods, tables, opportunities and canonical reference registry.
7. Use the packaged `documents/render_docx.py` with `--emit_pdf`. Inspect every page, then copy its PDF to the output path. Page PNGs and temporary workbook previews are local QA artifacts excluded from Git.

The retrieval manifest retains source URLs and reading access. Full-text reading caches for L-G05 and L-T02 carry noncommercial/no-derivatives terms and are excluded from the public repository; metadata, source locations and original extraction notes remain. Local derived full-text text files are also excluded. The CC-BY L-T03 XML and supplementary material retain their original notices. Metadata retrieval and source accessibility do not grant rights over third-party publications or clinical code sets. The manuscript and workbook builders use the extraction records and do not require these local reading caches.
