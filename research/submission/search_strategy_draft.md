# Draft search strategy and audit specification

September 16, 2026. **Not executed, not librarian-validated, and not a complete systematic search.** This is a concrete starting strategy for testing and translation, not evidence that the review has searched these databases.

## Planned sources

MEDLINE via PubMed; Embase; CINAHL; EconLit; Scopus or Web of Science; relevant government research and policy repositories; backward/forward citation searches. Confirm licenses and record platforms before execution. The medical, nursing/allied-health, economic and multidisciplinary sources cover distinct parts of the question. An inaccessible source cannot be silently counted as searched.

## PubMed core search

Run from inception through the documented execution date, without language, age, sex/gender, human-study, design or full-text-availability filters. Confirm current controlled-vocabulary mappings and the Search Details translation before running the final version. The core intentionally omits a mandatory sex/gender block: some eligible sex-specific care and policy studies do not identify themselves as gender research.

```text
(
  "Medicare"[Mesh]
  OR medicare[tiab]
  OR "Medicare Advantage"[tiab]
  OR "Medicare Part D"[tiab]
  OR "Medicare Part B"[tiab]
  OR "Medicare Part A"[tiab]
)
AND
(
  "Reimbursement Mechanisms"[Mesh]
  OR "Insurance Coverage"[Mesh]
  OR "Health Services Accessibility"[Mesh]
  OR "Health Expenditures"[Mesh]
  OR "Fees and Charges"[Mesh]
  OR "Drug Formularies"[Mesh]
  OR reimburs*[tiab]
  OR coverag*[tiab]
  OR payment*[tiab]
  OR "relative value"[tiab]
  OR RVU[tiab] OR RVUs[tiab]
  OR formular*[tiab]
  OR "prior authorization"[tiab]
  OR "step therapy"[tiab]
  OR "cost sharing"[tiab]
  OR "out of pocket"[tiab]
  OR copay*[tiab] OR coinsurance[tiab] OR deductible*[tiab]
  OR affordab*[tiab]
  OR access*[tiab]
  OR utilization[tiab] OR utilisation[tiab]
  OR denial*[tiab] OR denied[tiab]
  OR delay*[tiab]
  OR "unmet need"[tiab]
)
```

Do not narrow the core automatically if it retrieves a large number of records. Pilot relevance and missing sentinel studies, document tradeoffs, and have the final search peer-reviewed using PRESS [M-005]. The broad yield is a feasibility consideration to quantify, not a reason to pick only familiar care areas.

## Supplementary sex/gender and valuation search

Studies may use Medicare fee schedules without mentioning Medicare in the abstract. Test a complementary search:

```text
(
  "Sex Factors"[Mesh]
  OR sex[tiab] OR gender[tiab]
  OR women[tiab] OR men[tiab]
  OR female*[tiab] OR male*[tiab]
)
AND
(
  reimburs*[tiab] OR payment*[tiab]
  OR "relative value"[tiab] OR RVU[tiab] OR RVUs[tiab]
  OR "physician fee schedule"[tiab]
  OR "resource based relative value"[tiab]
  OR "insurance coverage"[tiab]
  OR "out of pocket"[tiab]
)
```

This may retrieve non-Medicare studies; determine payer applicability at screening rather than imposing a fragile US filter. Classify physician-gender records as their own context stream. No NOT transgender/cisgender filter is used: search-stage exclusion could remove mixed studies with extractable eligible findings.

## Clinical modules and citation following

Pilot modules for menopausal/vaginal care, sexual health, hypogonadism, bone/fracture care, breast/lymphatic care, pelvic/reproductive services, and shared cardiovascular/cancer/pain/mental-health conditions. Combine validated indication synonyms with Medicare/coverage concepts; preserve all exact module strings and counts before execution. These modules supplement rather than replace the broad search. Do not claim their vocabulary is complete until a librarian and clinical experts review it.

Use a diverse, independently chosen sentinel set from the current register to test retrieval: patient costs/access; historical bone care; a coverage-policy change; service RVUs; and physician payments. Record which query retrieved each and investigate misses. Retrieving the seed papers alone does not validate comprehensiveness.

For citation searching, log the seed report, cited/citing direction, index, date, number exported and identifier list. Include the organizing Lancet review and relevant earlier systematic reviews as seeds. Re-screen all resulting studies independently; a citation in a review does not establish eligibility.

## Policy-source search

Search official CMS national/local coverage databases, benefit and claims manuals, Medicare.gov, Federal Register/eCFR and SSA statutory text using recorded indication, code, benefit and exclusion terms. For each query retain the exact search, date, source interface and inspected results. Archive relevant versions and stable links when permitted. Search plan documents only for specified implementation questions; label them plan examples unless a defined sampling frame supports a national estimate.

Retain separate policy and scientific-study logs. Policy documents and raw CMS analysis rows do not become human study participants or database-search hits.

## Required search-log fields

| Field | Meaning |
|---|---|
| search_id / protocol_version | Stable query ID and governing draft/final protocol |
| database / platform / coverage | Name, vendor/interface, temporal/index coverage |
| query / limits / translation | Complete executed text, filters, automatic mapping and adaptations |
| run_timestamp / time_zone | Actual date and time, never the document's preparation date |
| retrieved_count / exported_count | Both counts with explanation for discrepancies |
| raw_export / checksum | Immutable RIS/XML/CSV file path, format and SHA-256 |
| deduplication_run | Rules, version, input/output counts and duplicate mapping |
| searcher / peer_reviewer | Actual responsible people and PRESS record |
| update_or_original | Relationship to prior runs and new-record count |

Maintain separate decision tables for records, reports, studies, full-text retrieval, exclusion reasons and linked reports. Reconcile unique records identified by databases and by other methods without counting the same report twice. Produce the final flow only from these reconciled logs. Use PRISMA-S [M-004] for reporting, and preserve failed/inaccessible searches as limitations rather than inventing result counts.

M-004 and M-005 are in the [living bibliography](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_bibliography.md).
