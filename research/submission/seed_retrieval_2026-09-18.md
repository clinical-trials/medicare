# Seed retrieval log: Medicare sex-equity review

Date: September 18, 2026. This is an **orientation retrieval**, not the formal systematic search and not a PRISMA study-selection count. It was used to test whether the existing question retrieves distinct evidence streams. The exact formal search remains the draft in `search_strategy_draft.md` and must be executed in the named databases, peer-reviewed with PRESS, exported, deduplicated, screened by two human reviewers, and updated before submission.

## Searches run

Web-assisted searches were run against indexed literature and official sources using these concepts:

1. `Medicare gender sex differences coverage access out-of-pocket women men systematic review`
2. `Medicare reimbursement gender differences physician payment women men study`
3. `Medicare sex differences utilization osteoporosis screening men women access`
4. `Medicare out-of-pocket costs women men sex differences prescription drugs`

These searches are exploratory and are not substitutes for direct database exports. Search-engine ranking and snippets can omit records, duplicate versions, or favor highly cited items. No record below is automatically included in the review.

## Candidate leads for independent screening

Correction recorded September 21, 2026: the original orientation table below attributed PMID 15692281 to Wilson et al. Verified MEDLINE authors are **Correa-de-Araujo R, Miller GE, Banthin JS, Trinh Y**. The original table is retained as an audit trail; the corrected record is L-X01 in the living bibliography. This corrects our seed log, not the published article.

| Lead | PMID | Preliminary role | Why it matters | Primary eligibility status |
|---|---:|---|---|---|
| Corrieri et al., *Income-, education- and gender-related inequalities in out-of-pocket health-care payments for 65+ patients: a systematic review* (2010) | [20701794](https://pubmed.ncbi.nlm.nih.gov/20701794/) | Prior systematic review / novelty lead | Reviews gender and out-of-pocket-payment inequalities in older adults; must be compared with our Medicare-specific question and updated evidence. | Unscreened lead; not an included study |
| Wilson et al., *Gender differences in drug use and expenditures in a privately insured population of older adults* (2005) | [15692281](https://pubmed.ncbi.nlm.nih.gov/15692281/) | Patient prescription-cost context | Includes older adults and Medicare-related insurance context; payer and data source require full-text verification before Medicare inclusion. | Unscreened lead; likely context or mixed-payer evidence |
| *Bone Density Screening Rates Among Medicare Beneficiaries: An Analysis with a focus on Asian Americans* (2024) | [38459983](https://pubmed.ncbi.nlm.nih.gov/38459983/) | Patient access/utilization | Uses Medicare 5% Research Identifiable Files and reports sex-stratified DXA screening; requires identity-measurement, age, clinical-eligibility and full-text review. | Unscreened candidate |
| *Gender Differences in Medicare Payments Among Cardiologists* (2021) | [34495296](https://pubmed.ncbi.nlm.nih.gov/34495296/) | Physician-gender context | Medicare payment data; patient sex is not the exposure and the result must remain outside the primary patient-equity synthesis. | Existing contextual record; re-screen under formal protocol |
| *Gender based disparities in Medicare physician reimbursement persist across years and specialty* (2024) | [38883793](https://pubmed.ncbi.nlm.nih.gov/38883793/) | Physician-gender context | Multi-year CMS payment analysis; total physician reimbursement and service volume are distinct from patient coverage or payment. | Unscreened contextual lead |
| *Gender Differences in Medicare Practice and Payments to Neurosurgeons* (2023) | [37819669](https://pubmed.ncbi.nlm.nih.gov/37819669/) | Physician-gender context | Medicare fee-for-service physician payment and practice metrics; not a patient-sex outcome. | Unscreened contextual lead |
| *Gender composition in the work environment and physicians' income from Medicare Part B fee-for-service payments* (2024) | [39617910](https://pubmed.ncbi.nlm.nih.gov/39617910/) | Physician-gender context | Longitudinal Medicare Part B physician-payment analysis; mechanisms and physician unit require separate appraisal. | Unscreened contextual lead |
| *Prescription Drug Spending in Fee-for-Service Medicare, 2008-2019* (2022) | [36255428](https://pubmed.ncbi.nlm.nih.gov/36255428/) | Medicare drug-policy background | Establishes Part B/Part D spending context; sex is descriptive, not necessarily a comparative equity analysis. | Unscreened background lead |

## What this seed retrieval suggests

The indexed literature separates into at least three streams: patient access/utilization and spending; service or policy valuation; and physician-gender payments. Physician-payment studies are numerous and directly Medicare-linked, but they do not answer whether women or men patients receive equitable coverage. Patient-level Medicare sex comparisons appear more condition-specific and need-focused, such as bone-density screening and drug spending, so the formal search cannot depend only on the terms “gender bias” or “reimbursement.”

The orientation retrieval does not establish direction, prevalence, or causality. It also does not establish that any study population is exclusively cisgender. Male/female administrative coding remains an identity-eligibility issue under `REVIEW_SCOPE.md`.

## Next required steps

1. Verify each candidate's title, authors, DOI, PMID and correction status against PubMed/MEDLINE metadata.
2. Retrieve full texts and independently apply the protocol's Medicare, outcome, sex/gender, identity, design and clinical-need criteria.
3. Add only eligible studies to `research/scoped_evidence.json` after stable IDs, subject classification, source-access level and limitations are recorded. Keep all unresolved and excluded leads in the audit trail.
4. Do not use this seed table as a PRISMA flow diagram or as evidence that the formal search is complete.
