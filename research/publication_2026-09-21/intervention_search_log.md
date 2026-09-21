# Targeted supplemental intervention search and extraction

Date: September 21, 2026. Extractor: one AI agent. Independent human screening, eligibility adjudication and formal risk-of-bias/GRADE assessments have **not** been completed. This is a bounded purposive search for translational interventions, not an exhaustive intervention review or a new PRISMA flow.

## Search route and scope

`REVIEW_SCOPE.md` was read before extraction. The purpose was to test whether practical medication-affordability or fracture-outreach approaches have intervention evidence, including negative results. New reports without a patient-sex comparison are proposed as **translational context**, outside the 38-study active register and primary patient-sex synthesis. Existing L-G05 receives a detailed supplemental extraction. No care items, canonical literature records, hypothesis counts or bibliography files were changed by this task.

No participant was inferred to be cisgender from recorded sex, anatomy, age, disease or medication. Identity remains unresolved under the current scope. No selected report demonstrates closure of a patient-sex/gender disparity. Prescriber involvement is not a physician-gender exposure.

### Existing PubMed archive triage

Input: `research/review_2026-09-21/pubmed/all_records.jsonl.gz`, 58,686 records. The following case-insensitive regular expressions were applied to titles:

```text
real.time.*(benefit|prescrip|price|cost)
(medication|drug).*(cost|afford).*(trial|intervention)
(trial|intervention).*(medication|drug).*(cost|afford)
osteopor.*(random|trial|intervention|outreach)
```

This produced 18 title hits, saved with titles, PMIDs and matching patterns in `intervention_sources/archive_title_triage.json`. It is targeted prioritization, **not** formal screening of all non-hits and not an exclusion decision. The broad search counts remain unchanged.

Archive membership was checked directly: PMIDs **33273290, 39073823 and 40608336 are present**; **42599729 and its parent 36094537 are absent**. The latter two were retrieved through the explicit supplemental route below; their absence was not treated as an exclusion. This task did not diagnose or amend the original queries.

### Web discovery queries

The following queries were executed with web search on September 21, 2026:

1. `Medicare real time prescription benefit tool randomized trial cost adherence`
2. `Medicare medication affordability intervention randomized trial cost related nonadherence`
3. `site.pubmed.ncbi.nlm.nih.gov "Real-Time Prescription Benefit Tool Availability and Prescription Medication Fill Rates"`
4. `site.pmc.ncbi.nlm.nih.gov "Reduced Cost Sharing and Medication Management Services for COPD"`

Selection prioritized original US Medicare intervention evidence, an existing fracture-outreach RCT, and a recent RTPB trial analysis with a separately reported Medicare stratum. Search-engine results and citation following are supplemental discovery routes; there is no claim of reproducible exhaustive ranking or complete screening. Citations within reviews or papers were not automatically imported.

Observed but not extracted/adjudicated leads included CLEAN Meds (Canadian setting), the MedAAAction protocol (PMID 42009102; protocol rather than outcomes), diabetes RTPB observational research (PMID 40884225), and a later COPD telephone teaching report. These are leads, not included evidence or finalized exclusions.

## Verification and access

All five records, including the linked parent, were matched by exact PMID to Europe PMC's MEDLINE records using:

```text
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID%3A{PMID}+AND+SRC%3AMED&format=json&resultType=core
```

Raw JSON, author lists, titles, DOI, PMID, journal details and retrieved correction/comment fields are preserved in `intervention_sources/`. Clean metadata for proposed integration is in `intervention_sources/verified_metadata.json`. Bibliographic verification does not establish eligibility or full-text review. The 2022 parent has metadata/abstract review only.

Full main-text XML was downloaded for PMIDs 33273290, 40608336 and 42599729 from Europe PMC. PMID 39073823 XML returned HTTP 500 twice; its full publisher main text, Tables 1–3, limitations and disclosures were read at the [JAMA article](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2821705). Its supplements/protocol were not reviewed. Some PMC browser views returned a recaptcha; public Europe PMC XML was available without bypassing access controls.

For PMID 42599729, the public [Europe PMC supplementary-files endpoint](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13476843/supplementaryFiles) returned a ZIP. Supplement 2 was extracted. eTable 6 (PDF page 7) was rendered and visually checked for the Medicare estimates. Other supplementary tables were selectively inspected; this is not a claim that every supplement or the original protocol was fully appraised. The ZIP, PDF and extracted text are preserved. `retrieval_manifest.json` records requests, saved files and failures.

No correction/retraction link was returned in the retrieved MEDLINE notice lists for the four detailed reports. The parent 2022 article has two **Comment in** links, PMIDs 36094566 and 37115192; these are not errata or independent trials. A bounded MEDLINE check does not establish that no correction exists elsewhere.

## Extracted reports and counterevidence

| ID / PMID | Design and population | Findings and boundary |
|---|---|---|
| L-G05 / [33273290](https://pubmed.ncbi.nlm.nih.gov/33273290/) | Randomized claims-triggered letters/calls to men aged 50–85 with fragility fractures and their physicians; Humana MA with drug coverage | 10,934 randomized, 7,842 analyzed; BMD testing 10.7% vs 4.9%, adjusted OR 2.13 (95% CI 1.74–2.62). Medication initiation 4.0% vs 2.5%, adjusted OR 1.59 (1.19–2.12). Substantial post-randomization exclusions; no demonstrated fracture reduction or sex-gap effect. |
| Proposed L-T01 / [39073823](https://pubmed.ncbi.nlm.nih.gov/39073823/) | Randomized invitation to lower inhaler cost sharing plus pharmacist management; 19,113 Humana MA beneficiaries with COPD | ITT PDC +3.8 percentage points (3.1–4.5); estimated program LATE +15.5 (12.8–18.1). OOP spending ITT −$49.5 (−68.9 to −30.0), exploratory. Exacerbations +2.0 per 1,000 (−23.4 to 27.4) and total spending −$125.8 (−953.1 to 701.4), both null. Bundled intervention; excludes low-income subsidy recipients. |
| Proposed L-T02 / [40608336](https://pubmed.ncbi.nlm.nih.gov/40608336/) | Difference-in-differences study of click-activated RTPB availability; 2,805,060 MA beneficiaries, 78,119 practices | OOP +1.2% (−0.7 to 3.0), total prescription spending +0.5% (−0.2 to 1.2), monthly fills +0.01 (−0.01 to 0.02): overall null. Actual tool use unobserved; availability imputed; no clinical outcomes. |
| Proposed L-T03 / [42599729](https://pubmed.ncbi.nlm.nih.gov/42599729/) | Post hoc cluster-RCT analysis; 38,289 orders in 198 practices, 57.2% Medicare orders | All-payer fills +1.2 points (−1.3 to 3.7), null; highest-cost class +14.5 (8.4–20.6), exploratory. **Medicare-specific:** all orders +0.5 (−2.4 to 3.4), null; highest-cost classes +10.5 (1.9–19.2), exploratory. Only 2.8% of all orders analyzed; high-cost Medicare N not given. |

Proposed linked parent **L-T03-P1 / [PMID 36094537](https://pubmed.ncbi.nlm.nih.gov/36094537/)** is the 2022 primary cost report of the **same trial, NCT04940988**. It is not an additional independent trial. Its abstract reports estimated prescription-order OOP reductions; estimated order prices are not actual patient spending. Its full text was not extracted here.

The machine-readable extraction stores exact outcome units, denominators, confidence intervals, subgroup restrictions, measurement sources, funding/sponsor roles and provisional appraisal domains. Do not combine odds ratios, PDC differences, prescription-order fills, log-model percentage effects and dollar spending into one effect measure.

## Source inconsistencies to resolve before publication

- COPD Table 1 prints control age 75–84 as 4,212/9,477 (36.0%), which does not agree arithmetically. No corrected count was invented; the main-text median age and verified sex denominators are retained.
- Ying 2026: Europe PMC's first-publication field says August 7; article XML says August 14. The conflict is explicit in metadata. Year, DOI, title, volume and issue agree.
- Ying Supplement 2 eTable 1 ends follow-up December 14 versus December 31 in the main article; age-bin labels 41–65/66+ differ from main 41–64/≥65 despite identical counts. Main-text labels are retained with this caveat.
- Ying eTable 2 reports 21,205 excluded orders, whereas main eligible minus analytic counts equal 21,752. Reconciliation is pending.
- Ying eTable 6 prints the intermediate-cost Medicare CI as `1.7 (-27, 6.2)`; visual inspection confirms the printed value. It was not silently changed to −2.7 and is not used as an inferential result. The overall and highest-cost Medicare estimates were clearly legible and separately extracted.

These are reported discrepancies, not diagnosed author errors or evidence of misconduct. They warrant clarification before final publication reliance.

## Testable implications, not efficacy claims

1. A claims/EHR outreach workflow could target beneficiaries with a clinically indicated but uncompleted bone-health assessment. Test completed assessment and appropriate treatment first; also measure incident fractures, reach failures, mortality and disenrollment. Include comparable women and men and a prespecified sex interaction to test gap closure. L-G05 supports a care-process signal but does not prove a software-only effect or fracture prevention.
2. A medication-affordability workflow could focus on high-cost prescriptions with clinically acceptable alternatives and include pharmacist follow-up. A prospective trial should compare the bundle with information alone and usual care, verify actual fills/OOP, and prespecify sex, income, subsidy and Medicare-plan strata. L-T01 supports bundled adherence improvement; L-T02 supplies a large null availability result; L-T03's high-cost signal remains exploratory. No selected report supports a claim of proven sex-equity improvement or guaranteed cost savings.

No registrations, author contacts, journal submissions or external messages were made.
