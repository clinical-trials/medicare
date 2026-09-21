# Medicare prescription affordability: targeted retrieval, September 21, 2026

This is one AI agent's preliminary retrieval and extraction, not independent human screening or a completed systematic review. `REVIEW_SCOPE.md` was read first. The two requested PMID records and two additional original Medicare studies were examined. All are historical evidence; none establishes current nationwide reimbursement bias.

The structured record is [drug_access_candidates.json](drug_access_candidates.json); query strings, source URLs, access failures, metadata checksums and retrieval date are in [retrieval_audit.json](retrieval_audit.json). The two `*_metadata_europepmc.json` files preserve the source MED metadata responses. These are targeted **other-method** retrievals; the root agent's formal database search has a separate audit. DA identifiers are local retrieval IDs. The parent assigned **L-R01** to PMID33298705 and **L-R02** to PMID33656528; this folder does not modify the canonical registers.

## Decisions

| Candidate | Citation / PMID | Preliminary disposition |
|---|---|---|
| DA-20260921-01 | Correa-de-Araujo et al., 2005; [15692281](https://pubmed.ncbi.nlm.nih.gov/15692281/) | Unresolved; full text and Medicare payer composition required. |
| DA-20260921-02 | Dusetzina et al., 2022; [36255428](https://pubmed.ncbi.nlm.nih.gov/36255428/) | Spending context only; no patient-sex effect estimate in accessed main report. |
| DA-20260921-03 | Nekui et al., 2021; [33298705](https://pubmed.ncbi.nlm.nih.gov/33298705/) | Direct patient-sex affordability candidate; identity unresolved. |
| DA-20260921-04 | De Avila et al., 2021; [33656528](https://pubmed.ncbi.nlm.nih.gov/33656528/) | Direct patient-sex affordability candidate; identity unresolved; adjusted null uncertainty retained. |

Neither direct candidate verifies cisgender identity. Keep these outside an explicitly confirmed-cisgender primary synthesis until eligibility is resolved. Both assess shared functions and heterogeneous medication needs; neither supports a sex-exclusive anatomy classification. Sex comparisons, drug coverage, utilization and clinical need remain distinct.

## National Medicare survey: Nekui et al.

The 2016 MCBS sample comprised 12,625 community-dwelling beneficiaries: 2,155 under 65 and 10,470 aged 65 or older. It includes traditional Medicare and Medicare Advantage. The outcome asks about cost-related nonadherence (CRN) over the previous 12 months. Enrollment data supplied sex; gender identity was not reported. [Methods and Tables 1–3](https://pmc.ncbi.nlm.nih.gov/articles/PMC7735208/)

| Outcome / age | Male prevalence, % (95% CI) | Female prevalence, % (95% CI) | Adjusted female:male OR (95% CI) |
|---|---:|---:|---:|
| Any CRN, <65 | 28.5 (25.2–31.9) | 40.5 (36.7–44.3) | 1.66 (1.31–2.10) |
| Any CRN, ≥65 | 12.8 (11.4–14.1) | 15.7 (14.6–16.8) | 1.21 (1.04–1.41) |
| Reduced spending on basic needs, <65 | 15.3 (12.2–18.4) | 23.4 (19.6–27.2) | 1.56 (1.10–2.23) |
| Reduced spending on basic needs, ≥65 | 3.5 (2.8–4.1) | 5.6 (4.9–6.4) | 1.30 (1.02–1.64) |
| Any cost-reduction strategy, <65 | 43.0 (39.2–46.9) | 52.3 (47.4–57.1) | 1.42 (1.12–1.79) |
| Any cost-reduction strategy, ≥65 | 43.7 (41.5–45.8) | 44.3 (42.2–46.3) | **1.04 (0.94–1.14)** |

Prevalences are survey-weighted; Table 2 contains the sex rows and Table 3 the adjusted estimates. CRN outcome-response Ns were 2,150 and 10,457 respectively. Sex-specific event counts and exact model Ns were not established; multiplying weighted percentages by unweighted sample counts would fabricate numerators.

Adjustment includes demographic, income, health, functioning and drug-coverage variables. Self-report, residual confounding and selection remain limitations. Cost-reduction strategies such as requesting a generic are not necessarily harmful nonadherence. The older group's final estimate includes the null. Supplements were identified but not extracted. [Main report](https://pmc.ncbi.nlm.nih.gov/articles/PMC7735208/)

## Selected longitudinal cohort: De Avila et al.

The Chicago cohort included 1,655 Medicare beneficiaries at elevated hospitalization risk, recruited during 2012–2018. Five surveys covered a baseline three-month recall and twelve months of follow-up. Persistent CRN meant reporting CRN at least three times. The authors use “gender” but state the survey asked sex; this does not verify cisgender status. [Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC7930921/)

| Outcome | Women | Men | Adjusted woman:man OR (95% CI), P |
|---|---:|---:|---:|
| Persistent CRN | 162/1,036 (15.6%) | 68/619 (11.0%) | **1.36 (0.95–1.95), .10** |
| Transient CRN | 227/1,036 (21.9%) | 160/619 (25.9%) | **0.81 (0.62–1.07), .15** |

Unadjusted persistent-CRN P=.008, while the adjusted interval includes 1. This is uncertainty, not proof of equivalence or removal of a causal mechanism. Model reference-outcome coding and analysis N need verification before pooling. Table 1's P values compare age-group demographic distributions, not within-age sex effects. [Results, Figure 2 and Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC7930921/)

The sample was 87.7% Black and excluded 223 participants who died, plus other incomplete records. Some unanswered CRN items were treated as no reported CRN. Generalization, survivor selection and self-report require appraisal. This observational sex comparison is not randomized merely because the source cohort came from a care-model trial. Its persistent outcome should not be pooled directly with annual any-CRN prevalence.

## Requested leads needing restraint

**Correa-de-Araujo et al.** The abstract reports average drug expenditures of $1,178 for women and $1,009 for men, approximately 17% higher for women. It does not establish that these are out-of-pocket costs. The title emphasizes private insurance, whereas the abstract refers to Medicare and private insurance. Full text is needed to establish the population, years, expenditure denominator and payer-specific findings. Do not reject solely on the title or call higher spending reimbursement discrimination. No accessible full text was found in this targeted run. [Verified abstract](https://pubmed.ncbi.nlm.nih.gov/15692281/)

**Dusetzina et al.** The study follows 2008–2019 spending in a 20% FFS Medicare sample continuously enrolled in A/B/D, allowing eligible entrants and deaths. It reports sex composition, not a sex effect. Spending combines allowed Medicare amounts, other-payer payments and patient liabilities, adjusted to 2019 dollars and estimated rebates; it is not patient OOP alone. [Methods and Results](https://pmc.ncbi.nlm.nih.gov/articles/PMC9579917/)

A source discrepancy requires reconciliation before quoting totals: the abstract reports per-capita totals of $16,345/$20,117 for 2008/2019, while the body reports $16,062/$18,940. The 2019 component arithmetic also does not reproduce the reported 27.2% drug share exactly. These are flags for source verification, not proposed corrections. The metadata's linked PMID 36255438 is a **commentary**, not an erratum. Supplements were not inspected. [Abstract and main Results](https://pmc.ncbi.nlm.nih.gov/articles/PMC9579917/)

## Bibliography for these candidates

1. Correa-de-Araujo R, Miller GE, Banthin JS, Trinh Y. Gender differences in drug use and expenditures in a privately insured population of older adults. *J Womens Health (Larchmt).* 2005;14(1):73–81. [DOI:10.1089/jwh.2005.14.73](https://doi.org/10.1089/jwh.2005.14.73). PMID **15692281**.
2. Dusetzina SB, Huskamp HA, Qin X, Keating NL. Prescription Drug Spending in Fee-for-Service Medicare, 2008-2019. *JAMA.* 2022;328(15):1515–1522. [DOI:10.1001/jama.2022.17825](https://doi.org/10.1001/jama.2022.17825). PMID **36255428**; PMCID **PMC9579917**.
3. Nekui F, Galbraith AA, Briesacher BA, Zhang F, Soumerai SB, Ross-Degnan D, Gurwitz JH, Madden JM. Cost-related Medication Nonadherence and Its Risk Factors Among Medicare Beneficiaries. *Med Care.* 2021;59(1):13–21. [DOI:10.1097/MLR.0000000000001458](https://doi.org/10.1097/MLR.0000000000001458). PMID **33298705**; PMCID **PMC7735208**.
4. De Avila JL, Meltzer DO, Zhang JX. Prevalence and Persistence of Cost-Related Medication Nonadherence Among Medicare Beneficiaries at High Risk of Hospitalization. *JAMA Netw Open.* 2021;4(3):e210498. [DOI:10.1001/jamanetworkopen.2021.0498](https://doi.org/10.1001/jamanetworkopen.2021.0498). PMID **33656528**; PMCID **PMC7930921**.

Titles, authors, journal metadata, DOI and PMID were matched to Europe PMC CORE/source MED on September 21, 2026. No linked correction or retraction was returned for these four records; this limited check does not prove none exists. No canonical register, bibliography or exclusion log was changed.
