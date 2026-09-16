# medicare

Research on sex-based differences in Medicare coverage, reimbursement, patient costs and access to clinically indicated care. Medicare is the national policy benchmark for care in later life and substantial health needs.

This is an ongoing evidence register and analysis framework for a future systematic review and white paper. It is not a completed systematic review or a national estimate of reimbursement bias.

## Current deliverables

Updated September 16, 2026.

- [Evidence register and analysis dashboard](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_evidence_register_2026-09-16.xlsx): 40 care-item/indication rows and 34 active literature records, with coverage findings, clinical classifications, sources and limitations.
- [Living bibliography](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_bibliography.md) and [RIS reference export](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_references.ris).
- [White-paper analysis framework](outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_anatomy_physiology_analysis_framework.md): Medicare benchmark rationale, anatomy/physiology distinctions, patient versus physician sex/gender, and planned comparison methods.
- [Current review scope](REVIEW_SCOPE.md): population eligibility, analytic rules and dated amendments.

The current population scope concerns cisgender women and men. Transgender-focused evidence is retained in the exclusion log. Reporting male/female sex alone does not establish gender identity; unresolved eligibility remains marked for review. Younger Medicare beneficiaries remain in scope and will be analyzed separately where the evidence permits.

The dashboard distinguishes shared body systems, female and male reproductive anatomy, female and male reproductive physiology, and mixed or site-dependent services. Clinical need, policy eligibility, spending and realized access are separate analytical concepts. Study classifications also distinguish patient care/access (18), service/anatomy valuation or coverage (10), physician sex/gender (3), and general patient background (3). These are evidence roles, not counts of proven disparities.

## Research records

- [Active evidence data](research/scoped_evidence.json)
- [Verified citation metadata](research/bibliography_metadata.json) and [reference registry](research/reference_registry.json)
- [Clinical classification rules](research/clinical_basis.json) and [study subject classifications](research/evidence_subjects.json)
- [Medicare benchmark rationale and sources](research/medicare_benchmark.json)
- [Research scripts and source data](research/)

[The initial research memo](Medicare_gender_bias_review_2026-09-16.md) is preserved as a historical first-pass analysis. The current scope and register incorporate later amendments; the initial memo is not the final white paper.

## Reproduction and source notices

The Python analysis scripts and downloaded public source files are retained for traceability. Workbook generation uses the Codex artifact runtime. Some workbook scripts contain local workspace/runtime/template paths and need configuration in another environment; a standalone installation is not packaged here. Local dependencies and rendering diagnostics are excluded from Git.

Third-party data and code sets retain their source terms and copyright notices, including the AMA/ADA notices in the CMS relative-value archive. Source inclusion or formulary listing is not itself proof of Medicare coverage for every indication.
