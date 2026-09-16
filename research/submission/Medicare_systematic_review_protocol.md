# Medicare coverage, payment, and access by sex: draft systematic review protocol

Version 0.1 — September 16, 2026. **Proposed procedures, not completed methods.** Prepared after exploratory searching, selected extraction, hypothesis development, and descriptive CMS analyses. This document does not supersede `REVIEW_SCOPE.md` or retroactively make the earlier work prospective. Changes to eligibility require a dated scope amendment.

## 1. Objective and contribution

Evaluate what empirical evidence shows about differences in Medicare coverage, service valuation, patient costs, and access to clinically indicated care for the project's eligible women and men. Assess whether observed differences plausibly reflect clinical need, benefit design, implementation, or inequitable treatment, while distinguishing association from causal evidence.

The primary publication will be a systematic review of empirical evidence with a separately documented Medicare policy context. The existing original CMS formulary and five-pair RVU analyses will remain exploratory companion analyses unless their inclusion is agreed with the journal and each analysis receives a full independent methods and limitations account. A review's PRISMA flow will not imply that these original analyses were identified as included studies.

The primary systematic searches and eligibility decisions address streams A and B. Physician-gender evidence in stream C remains targeted context in this manuscript; a claim of comprehensive physician-gender synthesis would require its own explicitly defined search, eligibility and appraisal procedures. Clinical background in stream D is also identified as context.

Prior related reviews will be retrieved to establish the incremental contribution: Medicare-specific benefit and policy periods; clinical-need denominators; shared-body versus reproductive-anatomy/physiology distinctions; and separation of patient, service, and physician units. The project will not claim to be the first review without a documented novelty search.

## 2. Questions, units, and outcomes

| Stream | Question and unit | Prespecified outcomes and interpretation |
|---|---|---|
| A: patient care, primary | Among beneficiaries with comparable clinical need, or within a clinically eligible sex-specific population, how do coverage/payment policies relate to access? Unit: beneficiary, episode, or defined eligible population. | Benefit eligibility/restrictions; coverage decisions and denials; appeal outcomes; patient out-of-pocket costs; treatment delays, completion, and unmet need. Receipt of care is not automatically beneficial or appropriate. |
| B: service valuation, separate synthesis | How are clinically and resource-comparable services valued under Medicare? Unit: service/code/indication/year, not patient or clinician gender. | Work RVUs, total RVUs, allowed amounts and actual payments reported separately; measured clinical work and resource use; policy consistency when no valid cross-anatomy comparator exists. |
| C: physician sex/gender, contextual | What does physician-level evidence say about receipts, opportunities, service mix, or rates? Unit: physician or claim. | Annual Medicare receipts, per-service allowed/payment amounts, and salary remain separate. This stream will not be pooled with patient-sex or service-anatomy results. |
| D: policy and clinical context | What are the benefit rules and independent clinical indications? Unit: policy version, clinical recommendation, or evidence source. | Policy eligibility, effective date, jurisdiction, exclusions, and administrative requirements; clinical need and evidence gaps. These are not measured causal effects. |

The primary outcome families are access/coverage and patient financial burden. Service valuation is a separate, prespecified secondary family. Utilization, morbidity, quality of life, and other health outcomes will be reported when linked to these questions; spending alone is not a measure of need or equity. No composite 'gender bias score' or count of statistically significant findings will be used.

For each comparison, define the population, exposure/policy, comparator, outcome, time horizon, and intended estimand before extracting the direction of the result. A women-minus-men contrast applies only where both groups have comparable clinical eligibility. A within-population policy change or need-based assessment does not require an artificial opposite-sex counterpart.

## 3. Eligibility

**Population and setting.** Follow the September 16, 2026 investigator scope: cisgender women and men; exclude transgender-focused patient studies and gender-affirming-care indications. Retain younger Medicare beneficiaries, including disability, ESRD and ALS entitlement. Mixed-payer or mixed-population studies require separately extractable eligible results for primary synthesis. Non-Medicare US and international studies may inform context, but cannot establish Medicare-specific effects.

**Identity reporting.** Record study terminology and how sex and gender were measured. Male/female administrative coding does not verify cisgender identity. Unknown-identity records remain candidates during full-text assessment; reviewers document whether identity was measured, seek author clarification where feasible, and record the response or lack of response. If eligibility cannot be established under the existing scope, do not include the estimate in an explicitly cisgender primary synthesis. Preserve it in an unresolved-eligibility/context table with a reason. Expanding eligibility to sex-coded populations would require a transparent investigator amendment before final selection, not a silent relabeling. Report the number and consequences of these exclusions as an applicability limitation.

**Policy/code sources.** These sources contain no individual gender-identity observations. Assess them by included clinical indication and service, and avoid patient-identity conclusions.

**Designs.** Include original randomized, quasi-experimental, cohort, case-control, cross-sectional, and qualitative studies that directly address a review question. Empirical code-valuation studies are eligible for stream B when their Medicare basis and comparison are identifiable. Clinical efficacy or safety studies with no coverage/payment/cost/access question are background only. Reviews are sources for context and citation searching, not independent primary effect estimates. Commentary and unverified assertions are not empirical outcome evidence.

**Equity relevance.** For stream A, require either a relevant patient sex/gender comparison, an assessment of coverage/access relative to clinical need within a prespecified sex-linked indication or population, or evidence evaluating differential sex-related need/access under a common policy. An unstratified Medicare spending or access study with none of these features is background, not primary evidence. For stream B, require a prespecified service/anatomy valuation question; a general fee-schedule description alone is policy context. These rules preserve within-population studies, including men's fracture-care interventions, without making every Medicare access paper eligible.

Incomplete adjustment for clinical need is an appraisal and interpretation issue, not an automatic exclusion of an otherwise relevant sex comparison.

**Publication and date limits.** Search database inception through each documented execution date. No sex, gender-identity, age, language, full-text-availability, or study-design search filter will be applied to the core search. Seek translation for potentially eligible non-English reports; document any reports that cannot be assessed. Relevant preprints and government research reports will be retained with publication status flagged and assessed separately; identify later peer-reviewed versions and avoid double counting. Conference abstracts are leads; insufficient reports remain 'awaiting sufficient information' unless an explicit final exclusion decision is made. No record will be excluded because of the direction or statistical significance of its results.

## 4. Clinical classification and equity variables

Use the existing `clinical_basis.json` categories: shared systems/functions; female reproductive anatomy; male reproductive anatomy; female reproductive physiology; male reproductive physiology; mixed/site-dependent. Assign by indication and site, splitting bundled services where necessary. Record sex-defined policy eligibility and disease burden independently. Bone, breast, lymphatic and pelvic-floor care are not automatically sex-exclusive anatomy.

Extract patient sex/gender, physician sex/gender, and service/anatomy variables separately using `evidence_subjects.json`. Preserve original definitions, missingness, measurement source and unit. For studies measuring both patient and physician variables, retain main effects, concordance and interaction terms separately.

Record age, disability/entitlement, race/ethnicity, income/dual eligibility, geography, insurance type and other available social factors as potential effect modifiers or sources of unequal need/access. Prespecify subgroup questions using the equity framework [M-006]. The study population restriction is a project boundary, not a claim that excluded populations lack inequity or relevance.

## 5. Information sources and search

A health-sciences librarian or information specialist should develop the strategy; another information specialist should independently peer-review it using PRESS [M-005]. Search MEDLINE/PubMed, Embase, CINAHL, EconLit, and Scopus or Web of Science. These are planned sources: subscription access has not been confirmed and no search is claimed to have run. Record each platform/version, full translated strategy, coverage dates, execution timestamp, limits, results and export file. Report unavailable databases and any replacement with its rationale and limitations.

Combine a sensitive Medicare/financing search without a mandatory sex/gender term with sex/gender and indication-specific supplementary searches. Do not require the word 'bias', a cisgender label, an opposite-sex comparator, or a named drug. This avoids excluding sex-specific care and studies with unanticipated results. The working search is in `search_strategy_draft.md`; it requires pilot testing and specialist review before formal execution.

Search CMS coverage databases, Medicare manuals, Medicare.gov, federal statutes/regulations and relevant government reports separately. Keep national rules, local coverage determinations and plan examples distinct. Conduct backward and forward citation searches for all included studies and key reviews, including the Lancet organizing review [L-B01] and its correction [L-B01-E1]. Record the citation index, date, seed and retrieved records. Investigator-supplied records enter the 'other methods' identification route and are re-screened under the same rules.

Archive each raw export without modification; retain a checksum and source-specific accession ID. Report searches using PRISMA-S [M-004]. Update the searches within 90 days before planned submission as a project operating target, not an asserted journal rule, and again if major new evidence or an extended review interval warrants it.

## 6. Record management and study selection

Deduplicate by normalized DOI and PMID, followed by title/author/year comparisons with human review of uncertain matches. Retain raw records and a reversible duplicate-to-retained-record mapping. Link multiple reports of the same study or overlapping claims cohorts; bibliographic duplicates, secondary reports and independent studies are different entities.

Two human reviewers will independently screen titles/abstracts and full texts. Before formal screening, pilot approximately 50 diverse records and 10 full texts, discuss disagreements and clarify rules; log all amendments. Resolve disagreements by discussion and, when unresolved, a third reviewer. Reviewers will not treat the existing seed register as automatically included.

Use one primary full-text exclusion reason per report in a prespecified hierarchy: wrong payer/setting for the empirical stream; ineligible indication/population; identity eligibility not established; no relevant outcome; ineligible design/non-original report; or insufficient extractable eligible results. Reports not retrieved are counted separately from assessed reports excluded. Keep contextual sources separately rather than labeling them primary Medicare evidence. Maintain reasons at record/report/study levels so PRISMA totals reconcile.

Automation may help deduplication or prioritize screening. Any model, version, date, prompt/procedure and validation must be logged. No generative model acts as either independent human reviewer, makes unverified final exclusions, or substitutes for full-text appraisal. Disclose actual use in the manuscript and cover letter.

## 7. Data extraction and verification

Pilot a structured form on at least five methodologically diverse studies. Two reviewers will independently extract eligibility, principal outcomes, denominators, effect estimates and risk-of-bias judgments; reconcile discrepancies against the full text. One reviewer may extract descriptive bibliographic fields with verification by a second. Preserve page/table/figure locators and verbatim source snippets needed for verification, within copyright limits.

Required fields: stable study/report IDs; full citation, DOI and verified PMID or dated missing-PMID explanation; correction/retraction status; design; data source and cohort overlap; payer and entitlement; recruitment/claims years; geography; clinical indication and need definition; policy exposure and effective dates; anatomy/physiology category; patient and physician measurement; comparison; outcomes/time horizon; numerator/denominator; missing data; effect measure, standard error/confidence interval; unadjusted and adjusted estimates; adjustment variables; funding/conflicts; limitations; source access; and extraction/adjudication audit trail.

Extract absolute differences and relative effects when reported or validly calculable. Preserve the original result; label derived calculations, formulas and assumptions. Record dollars, price year, geographic adjustments, work versus total RVUs, and payment versus charge. Do not mix nominal amounts across years without an explicit conversion method. Choose estimates by a prespecified causal rationale, not significance or maximum adjustment. Contact authors for essential missing information through authorized human correspondence; none has occurred at this stage.

## 8. Policy abstraction and CMS companion analyses

For every policy capture authority, title, URL, effective/revision/retrieval dates, benefit part, national/local/plan scope, eligible indication/population, frequency limits, exclusions, cost sharing, authorization criteria, exceptions/appeals and superseded versions. Distinguish absence of a national policy, explicit noncoverage, no formulary match, clinical ineligibility and a denied claim. Record 'not established' when the source does not resolve coverage. USPSTF grades are clinical recommendation categories, not automatic Medicare coverage states or GRADE certainty ratings.

Historical empirical findings must be aligned with contemporaneous policy. Current rules are presented separately and are not used to reinterpret historical exposures. Examples needing explicit policy-period handling include the 2024 lymphedema compression benefit and changing drug formularies.

If CMS analyses accompany the review, use separate reproducibility appendices. Formulary analysis must preserve release files, RxCUI concept lists, ingredient/form/strength/brand/indication rules, join keys, unmatched concepts, suppression/missingness, and denominators at formulary, contract-plan and segment levels. Report segment-weighted and enrollment-weighted estimands separately if enrollment data are available. Account for shared formularies before any inferential analysis; listing does not establish suitability, affordability, paid claims or unmet need.

For service valuation define the code universe and matching criteria before selecting pairs. Record complete descriptors, modifiers, global periods, setting, status, policy year and independently justified work/resource comparisons. Have clinical experts assess comparability. Keep work RVUs, total RVUs and actual payments separate. A five-pair purposive illustration is not a national sample. CPT 51597 is not male-exclusive. Validate calculations independently without presenting a second AI implementation as a second human reviewer.

## 9. Risk of bias and source appraisal

Two trained reviewers will use design-appropriate tools and record item/domain judgments with supporting text. Use RoB 2 for randomized intervention estimates; JBI tools for observational cohort, analytical cross-sectional, case-control and qualitative designs as applicable; and ROBINS-I only for studies estimating nonrandomized intervention effects for which a target comparison can be specified. Do not apply ROBINS-I mechanically to sex-as-exposure descriptions or all reimbursement studies. Record the tool version at protocol finalization; JBI tools have been revised, including the analytical cross-sectional tool in 2026.

For quasi-experiments assess assignment/exposure timing, pretrends where relevant, concurrent policy changes, outcome measurement, missingness, selection, and appropriate standard errors in addition to the chosen tool. For claims analyses consider access-dependent selection, coding misclassification, suppressed data, confounding, provider/plan clustering and overlap. Do not assume a large sample removes systematic bias.

For code comparisons and policy documents use a separate transparent appraisal of source authority, completeness, currency, comparator validity and reproducibility; identify this as a project-specific framework, not a validated risk-of-bias score. A statute is an authority for a rule, not proof of equitable clinical impact. Do not convert checklist totals into an unsupported numeric quality ranking or use quality scores as meta-analysis weights.

Official tools: [JBI critical appraisal](https://jbi.global/critical-appraisal-tools); [Cochrane risk-of-bias tools](https://www.riskofbias.info/). Version-specific manuals must be read before use.

## 10. Synthesis and conditional meta-analysis

Produce separate evidence tables by analytical stream, clinical category, outcome, Medicare component and policy period. Explain each study's directness to Medicare and to the target population. Group shared-condition comparisons by comparable clinical need; examine sex-specific services against need, alternatives and consistent policy reasoning. Describe contradictory and null findings with the same prominence as other results.

Structured narrative synthesis is the default because questions and units differ. Report effect sizes, uncertainty and risk of bias rather than vote counting significant studies. Use SWiM where its intervention-effect scope fits [M-007], and explain adaptations for descriptive reimbursement evidence rather than claiming universal SWiM applicability. Do not combine original studies with reviews that contain them.

Meta-analysis will be considered only for independent studies with sufficiently compatible populations, indications, exposures/comparators, outcome definitions and time horizons. Two studies are not by themselves a reason to pool. Retain design and estimand separation. For a compatible group, the proposed model is random effects with REML between-study variance and an appropriate small-sample inference method; finalize and justify the method with a statistician before pooling. Report study weights, heterogeneity, confidence intervals, and prediction intervals when estimable and meaningful. Do not pool work RVUs with dollars, annual physician receipts with per-service payments, or odds ratios with risk ratios without valid transformation.

Prespecify sensitivity analyses for risk of bias, overlapping cohorts, adjusted versus unadjusted estimands, historical versus current policy, Medicare-only versus mixed-payer extractable results, and peer-reviewed versus preprint reports. Age/entitlement and socioeconomic subgroups will be examined only with adequate data; label unplanned subgroup analyses exploratory. Evaluate selective reporting against protocols/registrations where available. Funnel-plot/asymmetry analyses require an adequately sized, compatible synthesis and have limited interpretation in heterogeneous observational evidence; absence of a test is not proof that reporting bias is absent.

## 11. Causal interpretation and certainty

Report the total disparity separately from analyses of potential mechanisms. Prespecify causal diagrams for questions about coverage/payment effects: clinical need and case mix may confound an association, while referrals, specialty opportunities, service mix and authorization may be mechanisms. Do not automatically adjust away mechanisms or classify every utilization difference as discrimination.

An inequity interpretation requires evidence about clinical need, benefit/harm, alternatives, patient preferences, preventable barriers and a defensible policy comparison. Observed imbalance, evidence of an access mechanism and a causal policy estimate will remain distinguishable. Population burden and clinically appropriate differences do not imply that identical treatment is always equitable.

Apply GRADE to outcome-specific bodies of evidence for suitable effect questions [M-002], using the framework appropriate to the design and question with a trained methodologist. Do not produce a GRADE label for every paper, statute, code or formulary row. If qualitative findings are formally synthesized, assess confidence with GRADE-CERQual [M-008]. For descriptive policy maps and non-effect valuation summaries, report directness, measurement limitations, consistency and source confidence explicitly without mislabeling these as formal GRADE ratings. PRISMA is reporting guidance [M-001], not a risk-of-bias tool or certification of validity.

## 12. Protocol status, registration, and amendments

Date and archive this draft and all later versions. Record the actual dates of pilot work, formal search, screening, extraction and analysis; preserve the existing exploratory record. Current [PROSPERO eligibility guidance](https://www.crd.york.ac.uk/PROSPERO/help/eligibility), checked September 16, 2026, requires registration before data extraction starts. The present project already has exploratory extraction and synthesis, so eligibility must not be assumed. Seek clarification using truthful stage information if proposing a distinct subsequent review; never backdate, relabel completed work, or claim a registration number before one exists. A public [OSF registration](https://help.osf.io/article/330-welcome-to-registrations) or versioned protocol can document methods for remaining work but does not remove prior evidence exposure or make earlier decisions prospective.

Each amendment must state date, rationale, stage, affected records/outcomes and whether findings were known. Re-screen affected records after eligibility changes. The eight current hypotheses are exploratory; only genuinely new, prospectively fixed analyses can be described as prespecified for the subsequent phase.

## 13. Team, reproducibility, and ethics

Assign two independent human reviewers, an adjudicator, a librarian/information specialist, a systematic-review methodologist, clinical expertise spanning relevant care, and a statistician for any quantitative pooling. Roles may overlap with transparent disclosure; independence of the two screening/appraisal decisions must be preserved. No such team appointments are asserted here.

Use public aggregate data and published evidence. Obtain the institution's research-ethics determination when required and report the actual determination; do not invent an exemption or approval. Restricted claims would require a separate data-governance plan. Record funding, conflicts, author contributions and any patient/public involvement or its absence.

Release allowable search strategies, decision logs, extraction definitions, appraisal judgments, derived data, code, versioned environment details and checksums in a stable repository with a data-availability statement. Do not redistribute copyrighted full texts or restricted source data. Seek an archival version/DOI for the submission snapshot where feasible; a mutable GitHub link alone does not identify an immutable analysis release.

## 14. Reporting and completion criteria

Prepare PRISMA 2020, PRISMA for Abstracts and PRISMA-S materials, plus applicable equity items [M-001, M-004, M-006]. This draft protocol draws on PRISMA-P [M-003]. Complete checklists with manuscript/supplement locations only after procedures and reporting are complete. Reconcile records, reports and studies in the flow diagram, separating database and other-method identification routes. Never substitute the current 34-record inventory for those counts.

Before submission: resolve eligibility; complete independent selection, extraction and appraisal; update searches; reconcile all counts; verify every numerical claim and cited source; freeze the data/code snapshot; complete certainty assessments only where applicable; obtain all author approvals; disclose the public exploratory white paper and actual AI use; and fit the journal's article limits. The existing PDF's Methods accurately describe the pilot and must not be rewritten in past tense to claim these planned steps already occurred.

Method references M-001–M-008 appear in the [living bibliography](../../outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_bibliography.md). The [readiness crosswalk](PRISMA_readiness_crosswalk.md) links the principal reporting requirements to current gaps and required artifacts.
