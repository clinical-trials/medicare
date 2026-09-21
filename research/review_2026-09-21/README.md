# September 21, 2026 Medicare review development run

A PubMed search and complete metadata export were executed before PRESS peer review. This is a reproducible **development run**, not a completed systematic review or a final set of included studies. The [population scope](../../REVIEW_SCOPE.md) still applies, including unresolved gender identity in sex-coded cohorts. The [protocol snapshot](protocol_before_search.md) preserves the draft used for this run; it was written after earlier exploratory evidence work and is not a prospective registration.

The [review working tables](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_review_working_tables_2026-09-21.xlsx) contain search progress, source extractions, selected effect estimates, editable paired-reviewer calibration fields, full abstracts and the search log. The [main evidence dashboard](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_evidence_register_2026-09-16.xlsx) was updated on September 21; its original filename is retained. The September 16 white-paper PDF has not yet incorporated this search or the new extraction.

## What ran

The Codex AI assistant executed PubMed through NCBI E-utilities on September 21, 2026. The first archived request began at 17:13:15 UTC and the last archived response completed at 17:31:04 UTC. Full submitted queries, PubMed translations, warnings, timestamps and parameters are retained in [queries.json](pubmed/queries.json), [manifest.json](pubmed/manifest.json) and the [raw response directory](pubmed/raw/). MEDLINE/PubMed is one source here, not two databases.

| Query / reconciliation step | Records |
|---|---:|
| Original draft core, retained for audit | 43,844 |
| Corrected core, current set | 43,904 |
| Supplementary sex/gender valuation/cost query | 16,866 |
| Current core + supplement hits before PMID deduplication | 60,770 |
| Duplicate hits across the two queries | 2,084 |
| **Unique current PMIDs** | **58,686** |
| Metadata records exported | **58,686** |
| Records containing an abstract | 46,735 |
| Records without an abstract | 11,951 |
| Identifier-only records remaining | 0 |

The initial core used an unrecognized MeSH phrase, `"Drug Formularies"[Mesh]`. Replacing it with `"Formularies as Topic"[Mesh]` added 60 records and removed none. The original query and IDs remain archived; `PM-CORE-20260921-R1` is the corrected current query. The supplementary query was unchanged. Do not add original and corrected query counts together.

The core imposed no eligibility filters for sex/gender, age, language, study design or full-text availability, and no substantive publication-date limit. Recursive publication-date partitions were a technical means to retrieve results beyond ESearch's 9,999-ID output limit; their union was reconciled against the unrestricted query count. The supplementary query intentionally retrieves some non-Medicare and physician-gender literature that requires later classification.

A **6,769-record priority subset** was exported first to support inspection and calibration. It is an ordering aid, not an eligibility filter or a third identification source. The heading correction did not change this subset. The remaining 51,917 metadata records were subsequently exported, so all 58,686 current PMIDs now have XML metadata. An absent abstract is retained as missing information, not a screening exclusion.

## Archive verification and transport recovery

Re-running [prepare_search.py](prepare_search.py) with the bundled Python runtime completed successfully against the full export. Independent local checks reconciled all five original/corrected query-ID files with their manifest counts and SHA-256 values; all 164 XML batch response PMID sets with requested IDs; and all 58,686 normalized JSONL and CSV records with the current PMID union. No duplicate or missing metadata PMID remained.

All **223 successful raw response bodies** matched their recorded SHA-256 and byte counts. Stored-file hashes were also checked wherever supplied; lossless gzip bodies were decompressed for response-hash verification. The request-sidecar parameters and endpoint URLs retain the actual request specifications. There are 117 sidecars explicitly marked POST; 106 earlier sidecars do not have an explicit method field, so that logging difference is preserved rather than silently backfilled.

During the export, long EFetch requests were switched to POST and the run resumed using previously cached response files. Successful responses were validated before storage and retained; the archive is not a complete log of every failed request or retry. The [export script](run_pubmed.py) records the transport and cache behavior. The historical `metadata_export` field in the manifest describes the earlier priority-only stage; `complete_metadata_export` and [search_summary.json](search_summary.json) give the current complete state.

## Selection work still pending

The [deduplication map](pubmed/deduplication_map.csv) is reversible and uses **exact PMID only** across the corrected core and supplementary query. Different PMIDs can describe the same study, related reports or overlapping cohorts; DOI/title/report-family review remains pending. These are bibliographic record counts, not counts of unique studies or participants, and not final PRISMA inclusion counts.

A post-execution diagnostic check retrieved **9 of 10** selected known records. [sentinel_retrieval.csv](pubmed/sentinel_retrieval.csv) identifies **L-G04 / PMID 18302495** as missing from both queries. These sources were chosen from the existing pilot register after execution; 9/10 is not a validated recall estimate or independent search-sensitivity assessment. The missing paper remains a relevant lead and must inform search revision or separately logged retrieval.

The [50-record calibration set](calibration_50.csv) combines known diagnostic sources with title-term domain samples in deterministic SHA-256 order. It is purposive, not representative. **All reviewer, decision and adjudication fields remain blank.** Preparing the sample is not completing calibration or human screening. All full-search records remain awaiting independent human title/abstract screening.

## Evidence work alongside the search

Targeted retrieval notes are retained separately for [medication affordability](drug_access/README.md), [bone care](bone/) and [service valuation](valuation/notes.md). Their source routes must be reconciled against database records by PMID/report before any formal flow is produced. Targeted AI extraction does not mean the full retrieved corpus was screened.

At this update, the working register has 38 active literature records and 40 care items. Four new patient-care candidates, L-R01–L-R04, retain unresolved identity eligibility. Eight earlier scope-excluded studies, one linked correction and two outside-register leads/context records remain separately identifiable in the 49-record scientific metadata set. The nine hypotheses are exploratory, including the newly added medication-affordability hypothesis; none becomes prospective because a database search has now run.

## Required next steps and limits

- Obtain independent information-specialist PRESS review, investigate the missed diagnostic source, revise and rerun as justified, and retain amendments and earlier exports.
- Execute and document the other planned databases and citation searches; Embase, CINAHL, EconLit and a multidisciplinary citation index have not been searched in this run. Access and source selection need confirmation.
- Complete report-family deduplication, independent human calibration/screening/extraction, eligibility adjudication and full-text exclusion accounting. Preserve unresolved identity; do not infer cisgender status from recorded sex.
- Appraise risk of bias with design-appropriate tools, assess certainty only for suitable bodies of evidence, and finalize synthesis after compatible outcomes and denominators are established.

No completed systematic review, independent human screening, formal risk-of-bias/GRADE assessment, registration, journal submission or editor contact is claimed. The current local search is developmental and predates PRESS review; broad retrieval volume does not demonstrate completeness.
