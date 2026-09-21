# medicare

Research on sex-based differences in Medicare coverage, reimbursement, patient costs and access to clinically indicated care. Medicare is the national policy benchmark for care in later life and substantial health needs.

This is an ongoing evidence register, analysis framework and preliminary white paper for a future systematic review. It is not a completed systematic review or a national estimate of reimbursement bias.

## Current deliverables

Updated September 21, 2026.

- [Inclusion and exclusion criteria figure](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/eligibility_figure/): standalone vector PDF, editable SVG, 300-dpi PNG and caption for future publication. Shows adopted scope, proposed empirical criteria, exclusions, unresolved eligibility and separate contextual streams; no completed selection counts are implied.
- [Current manuscript with figures and supplements (PDF)](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_equity_research_and_health_IT_manuscript_2026-09-21.pdf) and [editable Word manuscript](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_equity_research_and_health_IT_manuscript_2026-09-21.docx): a journal-style preliminary synthesis with a 199-word abstract, approximately 3,400 words of main text, two figures, two tables, detailed methods, six health IT opportunity assessments and 59 cited sources. Independent human screening, final eligibility, formal appraisal and the remaining source searches are unfinished. This is not yet a submission-ready completed systematic review.
- [Health IT opportunity assessment workbook](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_health_IT_opportunity_assessment_2026-09-21.xlsx): six unranked domains with patient-benefit questions, intervention evidence including null findings, current policy, data/workflow needs, prospective users/buyers and validation studies. Payment for software, purchasing demand and profitability are unverified.
- [Publication research package and reproducibility guide](research/publication_2026-09-21/README.md): two targeted search extensions add 461 unique PMIDs to the baseline, for **59,147** with complete metadata (47,152 abstracts; 11,995 without abstracts). All remain in the human review queue; query-ordering flags do not exclude records. Three new intervention study families and a linked parent report are retained as separate context, with verified PMIDs.
- [Executed literature search and audit](research/review_2026-09-21/README.md): 58,686 unique PubMed records with complete bibliographic exports; 46,735 include abstracts. The development search preceded PRESS review. Exact queries, corrections, hashes, duplicate mappings and diagnostic retrieval checks are preserved. No completed human screening is claimed.
- [Review working tables](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_review_working_tables_2026-09-21.xlsx): six sheets with search progress, nine targeted source updates/leads, outcome estimates, a 50-record calibration set with blank fields for two human reviewers, full abstracts and the executed search log.
- [Health Affairs Scholar submission preparation](research/submission/README.md): verified journal requirements and fees, an unsent inquiry draft, a detailed proposed systematic-review protocol, draft searches, the PRISMA 2020 readiness crosswalk and attached-checklist appraisal, proposed manuscript Methods, and an appraisal of the attached methodological guide. The formal review remains unfinished; proposed remaining procedures are separated from executed exploratory searches and extraction. Seven additional methodology references (M-003–M-009) and verified PMIDs are retained in the living bibliography/RIS; the evidence workbook has been updated; the September 16 preliminary PDF remains a historical version.
- [White paper with figures (PDF)](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_sex_gender_equity_white_paper_2026-09-16.pdf): September 16 version 1.1 (predates the latest search/extraction update), 17 pages, four figures, eight exploratory hypotheses and 42 cited sources, with numeric PMIDs for scientific and methodology articles. The expanded Methods section on pages 3-5 covers eligibility, source identification, extraction, synthesis and CMS analysis. Clearly labeled as a preliminary synthesis. [Markdown manuscript](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_sex_gender_equity_white_paper_2026-09-16.md) and [figure files](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/white_paper_figures/).
- [Evidence register and analysis dashboard](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_evidence_register_2026-09-16.xlsx): 40 care-item/indication rows and 38 active literature records (31 broadly labeled candidates and seven contextual records; updated September 21), with coverage findings, clinical classifications, sources and limitations. The [publication-role audit](research/publication_2026-09-21/evidence_roles.json) separates direct Medicare candidates from clinical efficacy and other-payer background; these counts are not final included studies.
- [Living bibliography](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_bibliography.md) and [RIS reference export](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_references.ris).
- [White-paper analysis framework](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_anatomy_physiology_analysis_framework.md): Medicare benchmark rationale, anatomy/physiology distinctions, patient versus physician sex/gender, and planned comparison methods.
- [Preliminary synthesis and testable hypotheses](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_preliminary_synthesis_and_hypotheses_2026-09-16.md): six provisional patterns and nine hypotheses, with counterevidence, tests and PMIDs. The workbook includes a Hypotheses tab and a dashboard summary.
- [Plain-language press concept](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_press_concept_PRISMA_GRADE_2026-09-16.md): explains the research question, PRISMA reporting and GRADE certainty assessment, with the current review stage stated explicitly.
- [Current review scope](REVIEW_SCOPE.md): population eligibility, analytic rules and dated amendments.

The current population scope concerns cisgender women and men. Transgender-focused evidence is retained in the exclusion log. Reporting male/female sex alone does not establish gender identity; unresolved eligibility remains marked for review. Younger Medicare beneficiaries remain in scope and will be analyzed separately where the evidence permits.

The dashboard distinguishes shared body systems, female and male reproductive anatomy, female and male reproductive physiology, and mixed or site-dependent services. Clinical need, policy eligibility, spending and realized access are separate analytical concepts. Study classifications also distinguish patient care/access (22), service/anatomy valuation or coverage (10), physician sex/gender (3), and general patient background (3). These are evidence roles, not counts of proven disparities.

## Research records

- [Active evidence data](research/scoped_evidence.json)
- [Verified citation metadata](research/bibliography_metadata.json) and [reference registry](research/reference_registry.json)
- [Clinical classification rules](research/clinical_basis.json) and [study subject classifications](research/evidence_subjects.json)
- [Medicare benchmark rationale and sources](research/medicare_benchmark.json)
- [Research scripts and source data](research/)

[The initial research memo](Medicare_gender_bias_review_2026-09-16.md) is preserved as a historical first-pass analysis. The current scope and register incorporate later amendments; the initial memo is not the final white paper.

## Reproduction and source notices

The Python analysis scripts and downloaded public source files are retained for traceability. Workbook generation uses the Codex artifact runtime. Some workbook scripts contain local workspace/runtime/template paths and need configuration in another environment; a standalone installation is not packaged here. Local dependencies and rendering diagnostics are excluded from Git.

The current manuscript and figures can be regenerated with the [publication builder](research/publication_2026-09-21/README.md). The historical September 16 PDF has its own [white-paper builder](research/whitepaper/README.md). Its Figure 3 uses first-code/second-code comparisons because the urologic exenteration code is not exclusive to male patients; the classification check is documented as P-045. Legacy extraction keys remain preserved in the source JSON.

Third-party data and code sets retain their source terms and copyright notices, including the AMA/ADA notices in the CMS relative-value archive. Source inclusion or formulary listing is not itself proof of Medicare coverage for every indication.
