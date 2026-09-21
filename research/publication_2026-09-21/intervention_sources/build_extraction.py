"""Serialize a bounded, manually checked AI extraction; not automated screening."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
DATE = "2026-09-21"
IDS = {"33273290": "L-G05", "39073823": "L-T01", "40608336": "L-T02", "42599729": "L-T03", "36094537": "L-T03-P1"}
records = []
for pmid, sid in IDS.items():
    m = json.loads((HERE / f"{pmid}_europepmc.json").read_text())["resultList"]["result"][0]
    j = m["journalInfo"]
    correction = (m.get("commentCorrectionList") or {}).get("commentCorrection", [])
    record = {
        "id": sid, "id_status": "Existing canonical ID" if sid == "L-G05" else "Proposed context ID; parent report suffix is provisional",
        "original_citation": m["authorString"] + " " + m["title"] + " " + j["journal"]["medlineAbbreviation"] + ". " + str(j["yearOfPublication"]) + ";" + j["volume"] + "(" + j["issue"] + "):" + m["pageInfo"] + ".",
        "authors": [{"family": a.get("lastName", ""), "given": a.get("firstName", ""), "initials": a.get("initials", "")} for a in m["authorList"]["author"]],
        "title": m["title"].rstrip("."), "journal": j["journal"]["title"], "journal_abbreviation": j["journal"]["medlineAbbreviation"],
        "year": j["yearOfPublication"], "volume": j["volume"], "issue": j["issue"], "pages": m["pageInfo"], "doi": m["doi"], "pmid": pmid, "pmcid": m["pmcid"],
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/", "fulltext_url": f"https://pmc.ncbi.nlm.nih.gov/articles/{m['pmcid']}/",
        "verification_source": f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID%3A{pmid}+AND+SRC%3AMED&format=json&resultType=core",
        "verified_on": DATE, "metadata_status": "Verified against Europe PMC MEDLINE record; title/DOI/PMID consistent",
        "indexed_first_publication_date": m.get("firstPublicationDate"), "issue_date": j.get("dateOfPublication"),
        "publication_types_as_indexed": m.get("pubTypeList", {}).get("pubType", []),
        "linked_notices": correction,
        "correction_check": "No correction/retraction link returned in the retrieved MEDLINE commentCorrectionList; this bounded check does not establish that no notice exists. Linked comments, if present, are not corrections.",
        "review_status": "Provisional AI extraction; independent human screening/eligibility/risk-of-bias review pending",
        "role": "Linked parent report of the same trial, not an independent trial" if pmid == "36094537" else "Translational intervention context; does not test a patient-sex disparity",
        "notes": [],
    }
    if pmid == "39073823":
        record.update(online_publication_date="2024-07-29", reviewed_fulltext_url="https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2821705", access_level="Publisher full main text, tables 1-3 and disclosures reviewed; supplements not reviewed")
        record["notes"].append("Europe PMC firstPublicationDate represents the October issue; publisher explicitly dates online publication July 29, 2024. XML retrieval failed twice with HTTP 500; publisher web text was accessible.")
    elif pmid == "40608336":
        record.update(online_publication_date="2025-07-03", access_level="Full main text and tables reviewed in Europe PMC XML; supplements not reviewed")
        record["notes"].append("Europe PMC firstPublicationDate July 1 is the issue date; article XML explicitly dates online publication July 3, 2025.")
    elif pmid == "42599729":
        record.update(article_reported_publication_date="2026-08-14", access_level="Full main text and tables reviewed in Europe PMC XML; Supplement 2 selectively reviewed, eTable 6 visually verified; protocol not reviewed")
        record["notes"].append("Date discrepancy preserved: MEDLINE-derived firstPublicationDate is August 7, 2026; article XML Published field and pub-date say August 14, 2026. Year, volume, issue, DOI, title and PMID agree; no date silently substituted.")
    elif pmid == "36094537":
        record.update(access_level="Verified metadata and abstract only in this supplemental extraction", linked_trial_id="NCT04940988", linked_report_id="L-T03")
        record["notes"].append("MEDLINE publication-type labels include Comment, but the verified title/abstract describe the original cluster randomized trial. Design classification follows the article; linked Comment in records are not separate corrections or trials.")
    else:
        record.update(access_level="Full main text and tables reviewed in Europe PMC XML; figure images and supplement not independently inspected")
    record["date_notes"] = {
        "33273290": "Issue: February 2021. Europe PMC firstPublicationDate 2021-02-01; no separate online date asserted in this extraction.",
        "39073823": "Publisher online publication July 29, 2024; issue October 2024. Europe PMC firstPublicationDate 2024-10-01 is the issue date.",
        "40608336": "Article XML online publication July 3, 2025; issue July 2025. Europe PMC firstPublicationDate 2025-07-01 is the issue date.",
        "42599729": "Unresolved source discrepancy: article XML Published field and pub-date August 14, 2026; Europe PMC MEDLINE firstPublicationDate August 7, 2026. Issue August 2026; no exact publication day silently chosen.",
        "36094537": "Issue November 2022. Europe PMC firstPublicationDate 2022-11-01; separate online date not independently verified in this bounded extraction.",
    }[pmid]
    records.append(record)

def outcome(name, estimate, low, high, unit, source, **extra):
    return {"outcome": name, "estimate": estimate, "ci_level": 0.95, "ci_low": low, "ci_high": high, "unit": unit, "source_locator": source, **extra}

common = {
    "extracted_on": DATE,
    "review_status": "Provisional AI screening and extraction; no independent human review or completed formal risk-of-bias/GRADE assessment",
    "identity_status": "Gender identity not established; never classified as confirmed cisgender",
    "primary_patient_sex_synthesis": False,
    "sex_equity_conclusion": "No reported intervention-by-patient-sex/gender test in the reviewed material; no demonstrated closure of a women/men equity gap.",
    "physician_gender_effect": "Not evaluated; physician/prescriber involvement is not a physician-gender exposure",
    "care_item_addition": False,
}
studies = []

studies.append({**common,
    "id": "L-G05", "pmid": "33273290", "title": records[0]["title"],
    "eligibility_recommendation": "Retain existing candidate record; new detailed extraction supports translational context, not a between-sex effect estimate. Population-identity eligibility remains unresolved.",
    "design": "Randomized patient/physician outreach intervention; post-randomization complete-follow-up analysis",
    "trial_family": "Pasquale osteoporosis outreach, independent of other selected interventions",
    "population": {"payer": "Humana Medicare Advantage with prescription drug coverage", "geography": "United States; one insurer; South approximately 68%", "age": "Men aged 50-85; intervention mean 71.1 (SD8.4), control 71.0 (SD8.4)", "eligibility": "Recent fragility fracture; no BMD testing or osteoporosis pharmacotherapy in prior year/before intervention; exclusions for specified trauma, cancer/Paget disease and repeat same-site fracture", "identity": "Reported men/administrative eligibility; exact sex-field provenance and gender identity not reported", "clinical_basis": "Shared bone system; male-only eligibility is separate from anatomy"},
    "data_period": "Fracture identification May 1, 2016-May 31, 2017; index approximately two months after fracture; 12-month follow-up",
    "denominators": {"initially_randomized": 10934, "analyzed_total": 7842, "analyzed_intervention": 3977, "analyzed_control": 3865, "excluded_after_randomization": 3092, "deaths_excluded": 157, "disenrollment_excluded": 2512, "all_contacts_dead_ends_excluded": 8, "preintervention_BMD_or_treatment_excluded": 415, "initial_arm_counts": None, "note": "Initial arm allocation not independently read from figure; do not infer exact event counts from rounded percentages. 3,092/10,934 (28.3%) excluded after assignment."},
    "intervention": "Claims identify recent fracture; patient letters, physician mail/fax, up to three telephone attempts to each over one month; prompts assessment and appropriate osteoporosis care.",
    "comparator": "No outreach/usual care",
    "software_directness": "Claims-triggered workflow plus human outreach; not a software-only trial or a coverage-rule experiment.",
    "outcomes": [
        outcome("BMD testing by 12 months", 2.13, 1.74, 2.62, "adjusted odds ratio", "Table 2, BMD testing multivariable model", intervention_percent=10.7, control_percent=4.9, denominator_intervention=3977, denominator_control=3865, unadjusted_OR=2.31, unadjusted_CI=[1.94,2.76], endpoint_type="Access/process", definition="BMD includes DXA and other modalities; do not call the endpoint DXA only."),
        outcome("Osteoporosis pharmacotherapy initiation", 1.59, 1.19, 2.12, "adjusted odds ratio", "Table 2, OPT initiation multivariable model", intervention_percent=4.0, control_percent=2.5, denominator_intervention=3977, denominator_control=3865, unadjusted_OR=1.60, unadjusted_CI=[1.24,2.07], endpoint_type="Treatment initiation/process"),
        outcome("BMD or pharmacotherapy initiation", 2.09, 1.77, 2.46, "unadjusted odds ratio", "Results, Impact of the intervention", endpoint_type="Composite process"),
    ],
    "analysis": "Logistic adjustment used age, race, region, fracture site, Deyo-Charlson/selected comorbidities and selected medications with backward stepwise retention P<=0.10.",
    "null_or_negative_evidence": ["Incident fractures, quality of life and cost effectiveness were not measured as outcome improvements.", "Absolute treatment initiation remained low (4.0%); the study does not establish health benefit from this delivery intervention."],
    "implementation": {"reported_approximate_cost_USD_per_patient": 70, "cost_limit": "Approximate program estimate, about half development/evaluation; not a formal cost-effectiveness or ROI result.", "contact_gradient": "BMD 25.0% when patient and physician reached by phone, 13.7% one reached, 6.5% neither; contact intensity was not randomized and is vulnerable to selection."},
    "funding": "Amgen and Humana",
    "conflicts": "Yehoshua, Chines and Caloyeras: Amgen employees/stock; Pasquale, Sheer and McFadden: Humana employees/stock; Pasquale also reported Amgen stock.",
    "appraisal": {"status": "Provisional AI domain notes; no formal overall rating", "randomization": "Called randomized, but sequence/concealment not sufficiently detailed in reviewed main text.", "deviations": "Cannot isolate letter, fax and telephone components; intensity analyses are nonrandom.", "missing_data": "28.3% post-assignment exclusions, including disenrollment and death; no full intention-to-treat effect demonstrated.", "measurement": "Claims-based tests/fills are care processes, not actual use or fracture prevention.", "selective_reporting": "Prospective protocol not verified; stepwise models and reach gradients require caution.", "applicability": "Selected untreated male fracture patients aged50-85 in one MA insurer; mostly White/Southern; no female comparator."},
    "source_locators": ["Full text Methods: study population, outreach program, outcomes, statistical analysis", "Results and Tables1-2", "Funding/author disclosures"],
    "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7899217/",
    "access_limitations": "Full main-text XML and tables reviewed. Figure images and supplementary appendix not independently inspected.",
})

studies.append({**common,
    "id": "L-T01", "pmid": "39073823", "title": records[1]["title"],
    "eligibility_recommendation": "New translational intervention context, outside the active primary patient-sex evidence register; identity unresolved.",
    "design": "Individual randomized encouragement trial; intention-to-treat invitation effect and instrumental-variable local average treatment effect (LATE)",
    "trial_family": "NCT05497999",
    "population": {"payer": "Humana Medicare Advantage with Part D", "age": "Median74, IQR69-80; includes beneficiaries under65", "sex_measurement": "Sex from enrollment files, female/male; 78 have unavailable baseline demographic data", "female": "10,497/19,035 (55.2%)", "identity": "Gender identity not reported", "eligibility": "COPD diagnosis within two years, prior inhaler fill, PDC<80%, at least three months prior Humana enrollment", "exclusions": "PartD Low-Income Subsidy, coverage-gap phase, hospice, end-stage kidney disease, selected insurer-subsidiary primary care sites", "clinical_basis": "Shared respiratory system"},
    "data_period": "Program randomizations first three months2020 and2021; claimsJan2019-Dec2021; follow-up from randomization to calendar-year end (9-12 months)",
    "denominators": {"randomized_and_analyzed": 19113, "invited": 9601, "control": 9512, "female_invited": 5238, "sex_denominator_invited": 9558, "female_control": 5259, "sex_denominator_control": 9477},
    "intervention": "Phone/mail invitation to opt into $0 inhaler cost sharing at preferred retail/mail pharmacies or $10 other in-network pharmacy, plus up to three pharmacist calls for medication management, prescribing coordination and inhaler technique.",
    "comparator": "No invitation; beneficiaries could independently opt in (29.4% enrollment invited vs5.1% control).",
    "software_directness": "Bundled benefit redesign and human pharmacy care; cannot attribute effect to a digital tool or cost sharing alone.",
    "outcomes": [
        outcome("Maintenance inhaler PDC",3.8,3.1,4.5,"percentage-point ITT invitation effect","Table2; Results primary outcome",intervention_percent=32.0,control_percent=28.4,endpoint_type="Refill-based adherence proxy",LATE=15.5,LATE_CI=[12.8,18.1]),
        outcome("PDC>=80%",1.7,1.0,2.5,"percentage-point ITT invitation effect","Table2",intervention_percent=8.1,control_percent=6.3,endpoint_type="Refill-based adherence proxy",LATE=7.1,LATE_CI=[4.2,10.0]),
        outcome("Moderate-to-severe COPD exacerbations",2.0,-23.4,27.4,"events per1000 beneficiaries, ITT difference","Table2; prespecified secondary outcome",intervention_rate=454.2,control_rate=445.6,endpoint_type="Claims-based clinical outcome",LATE=8.2,LATE_CI=[-96.2,112.5],interpretation="Null; no demonstrated reduction"),
        outcome("Total medical and prescription spending",-125.8,-953.1,701.4,"USD ITT difference","Table2; prespecified secondary outcome",intervention_mean_USD=19038.3,control_mean_USD=19156.1,endpoint_type="Total spending",LATE=-516.4,LATE_CI=[-3910.5,2877.7],interpretation="Null; no demonstrated total-cost saving"),
        outcome("Out-of-pocket prescription spending",-49.5,-68.9,-30.0,"USD ITT difference","Table2; exploratory outcome",intervention_mean_USD=619.5,control_mean_USD=675.0,endpoint_type="Patient spending",LATE=-203.0,LATE_CI=[-282.8,-123.2]),
        outcome("Difference in PDC invitation effects: Black minus White",1.8,-0.5,4.1,"percentage-point interaction","Table3; racial difference in invitation effect",p_value=0.13,Black_effect=5.5,Black_CI=[3.3,7.7],White_effect=3.7,White_CI=[2.9,4.4],interpretation="Racial heterogeneity test null; not a patient-sex comparison"),
    ],
    "analysis": "Six simple-randomization instances pooled; adjusted sex, age, region, baseline outcome, randomization month/year; follow-up duration weights. Race analysis includes interactions; overall analysis omits race. LATE applies to invitation-induced enrollees and assumes invitation affects outcomes only through enrollment. Multiplicity addressed for secondary outcomes with Benjamini-Hochberg.",
    "sex_analysis": "Sex covariate only; no sex-stratified intervention effects or sex interaction reported in reviewed main text/tables.",
    "null_or_negative_evidence": ["No statistically significant effect on exacerbations, short-acting inhaler fills or total spending.", "Racial effect-difference confidence interval includes zero; cannot establish reduced racial or sex disparities.", "PDC is not actual/proper inhaler use; more 90-day mail supplies can increase measured PDC."],
    "funding": "Humana research/educational gift to Harvard Medical School and AHRQ F32HS029259.",
    "conflicts": "Humana funding/fees or equity reported by Chernew, Press, Boudreau, Powers and McWilliams; other outside interests reported in article disclosures.",
    "sponsor_role": "Humana involved in program development, study design/conduct, data collection and manuscript review; reported no role in management/analysis/interpretation, preparation/approval or decision to submit.",
    "appraisal": {"status": "Provisional AI domain notes; no formal overall rating", "randomization": "Individual simple randomization described; protocol publicly posted before analysis but after implementation.", "deviations": "Control uptake expected in encouragement design; ITT preserves assignment. LATE adds exclusion-restriction/monotonicity assumptions and is not the average effect for all enrollees.", "missing_data": "19,113 randomized analyzed; varying observed follow-up weighted; demographic denominator19,035. Further attrition auditing requires supplement/protocol.", "measurement": "Claims PDC and exacerbation algorithms; actual inhaler use, FEV1 and quality of life unavailable; education may alter ascertainment of exacerbations.", "selective_reporting": "Plan after intervention; OOP explicitly exploratory. Secondary clinical outcomes less precisely estimated.", "applicability": "Single MA insurer, low-income subsidy beneficiaries excluded, bundled intervention; uptake responders less likely to have dementia."},
    "source_discrepancies": ["Publisher Table1 control age75-84 cell is printed4212/9477(36.0%), arithmetically inconsistent. No corrected count invented; age-bin counts not used."],
    "source_url": "https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2821705",
    "source_locators": ["Methods, eligibility/randomization/variables/statistical analysis", "Tables1-3", "Results and Limitations", "Article Information disclosures and sponsor role"],
    "access_limitations": "Full publisher main text/tables reviewed; XML failed twice; supplements/protocol not independently reviewed. Historical VBID discussion is not a current-policy verification.",
})

studies.append({**common,
    "id": "L-T02", "pmid": "40608336", "title": records[2]["title"],
    "eligibility_recommendation": "New translational intervention context with important null evidence; outside active patient-sex register; identity unresolved.",
    "design": "Difference-in-differences natural experiment of EHR real-time prescription benefit availability",
    "trial_family": "Zink national-insurer RTPB availability study; not randomized",
    "population": {"payer": "One national insurer's Medicare Advantage HMO/PPO enrollees", "age": "Mean70.9, SD9.2", "sex_gender_measurement": "Authors call it gender self-reported at MA enrollment, female/male/unknown; 56.7% female. Exact gender-identity status not established by those categories.", "clinical_basis": "Shared medication-access/affordability system across drug classes"},
    "data_period": "April2018-March2020; vendor introduced tool March2019",
    "denominators": {"unique_beneficiaries": 2805060, "beneficiary_months": 33001795, "practices_total": 78119, "treated_practices": 3863, "untreated_practices": 74256, "treated_beneficiary_months": 2645075, "untreated_beneficiary_months": 30356720, "unique_ever_treated_beneficiaries": 371241, "unique_untreated_beneficiaries": 2694281, "note": "Beneficiary treatment assignment may vary by month; unique treated/untreated populations overlap and must not be added."},
    "intervention": "Click-activated EHR dropdown providing expected patient costs and lower-cost medication/pharmacy alternatives; availability inferred from vendor-linked prescribing data.",
    "comparator": "Practices without inferred vendor-tool availability before/after March2019",
    "software_directness": "Direct software-availability evaluation; actual clicks/use unobserved. Structured prescribing required; free text bypasses tool.",
    "outcomes": [
        outcome("Monthly out-of-pocket prescription spending",1.2,-0.7,3.0,"percent DID effect","Results; primary outcome; Table2 log models",p_value=0.23,endpoint_type="Patient spending",interpretation="Null; body reports percentage change, not dollars"),
        outcome("Monthly total prescription spending",0.5,-0.2,1.2,"percent DID effect","Results; Table2",p_value=0.19,endpoint_type="Total prescription spending",interpretation="Null"),
        outcome("Monthly prescription fills",0.01,-0.01,0.02,"fills per beneficiary-month DID difference","Results; Table2",p_value=0.36,endpoint_type="Utilization/process",interpretation="Null; not direct adherence or clinical outcome"),
        outcome("Lipid-modifying drug spending",0.9,0.2,1.6,"percent DID effect","Results subgroup analyses; Table3",endpoint_type="Drug-class spending",interpretation="Increase; preserve contrary finding"),
    ],
    "analysis": "Practice tax-ID and time fixed effects; HMO-by-HRR-by-year effects plus age, gender, race, low-income subsidy, dual status and HMO; SE clustered by practice. Treated practice definition >=50% clinicians linked to vendor data; alternative10%/90% definitions and event-study checks. Log-spending models summarized as percentage changes in the article body.",
    "sex_analysis": "Enrollment gender is an adjustment covariate; no sex/gender intervention contrast reported in reviewed material.",
    "null_or_negative_evidence": ["No overall improvement in spending, fills, mail-order share or 90-day share.", "High-cost drug-class subgroup also null; lipid-modifying spending increased.", "90% treatment-threshold sensitivity yielded a small positive fill effect; do not say every sensitivity result was null.", "No clinical outcomes measured; no observed clicks, so cannot equate availability null with efficacy of actively used recommendations."],
    "implementation": "Only about7% of prescriptions were suggested alternatives; potential average savings about$4/prescription reported, not a demonstrated realized saving.",
    "funding": "Research/educational gift from Humana to Harvard Medical School.",
    "conflicts": "Sutherland: Humana employee; Boudreau: Humana employee/equity. Zink, McWilliams and Chernew reported other outside fees, roles or support; Bozzi has Humana affiliation. No other disclosures reported.",
    "sponsor_role": "Humana collected/prepared data and participated in design/conduct/interpretation/manuscript meetings; reported no data-management/analysis or submission-decision role.",
    "appraisal": {"status": "Provisional AI nonrandomized-intervention domain notes; no formal ROBINS-I result", "confounding": "Practice selection, imputed treatment and time-varying confounding; parallel trends/no anticipation/no spillover assumptions. Event-study checks support but cannot prove assumptions.", "selection": "Beneficiaries need a calendar year enrollment; practice assignment follows prescribing and may change monthly.", "classification": "Tool availability inferred by >=50% clinicians' link; actual use unavailable.", "deviations": "Clinician engagement, competing cost tools and free-text bypass unmeasured.", "missing_data": "Exposure classification/EHR capture and unenrollment can be informative; complete-enrollment sensitivity reported.", "measurement": "Claims spending/fills objectively measured within plan; not medication consumption or health benefit.", "reporting": "Multiple subgroup/sensitivity findings; no prospective protocol checked.", "applicability": "One insurer and EHR vendor; historical pre-2025 PartD benefit environment."},
    "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12232181/",
    "source_locators": ["Methods, patient population/tool identification/statistical analysis", "Tables1-3; Results", "Limitations; article author-notes/funding"],
    "access_limitations": "Full main text and tables reviewed from XML; supplementary estimates not independently extracted.",
})

studies.append({**common,
    "id": "L-T03", "pmid": "42599729", "title": records[3]["title"],
    "eligibility_recommendation": "New translational intervention context, with separately extractable exploratory Medicare subgroup; outside active patient-sex register; identity unresolved.",
    "design": "Post hoc analysis of specialty-stratified practice-cluster randomized trial; fill outcome and subgroup analyses not prespecified",
    "trial_family": "NCT04940988", "linked_parent_pmid": "36094537", "linked_parent_provisional_id": "L-T03-P1",
    "dependence": "Same trial as Desai2022; do not count as two independent trials or pool correlated estimates as independent studies.",
    "population": {"payer": "Mixed payer;57.2% of analytic medication orders Medicare", "setting": "NYU Langone urban ambulatory network; one EHR/RTPB tool", "age": "59.2% of orders for age>=65 in main Table1; younger adults included", "sex_measurement": "EHR sex, female/male;22,690 female orders(59.3%),15,599 male orders(40.7%); identity not reported", "clinical_basis": "Shared medication access system; drug-class cost strata are not sex-linked anatomy"},
    "data_period": "Main text: January13-December31,2021; previous primary report throughJuly31; analysesOctober18,2022-August9,2024",
    "denominators": {"all_orders": 1386577, "RTPB_eligible_orders": 60041, "analyzed_orders": 38289, "analyzed_percent_all_orders": 2.8, "intervention_orders": 23226, "control_orders": 15063, "analyzed_unique_patients": 22357, "intervention_patients": 13838, "control_patients": 9458, "analyzed_practices": 198, "intervention_practices": 97, "control_practices": 101, "Medicare_orders": 21897, "Medicare_intervention_orders": 13039, "Medicare_control_orders": 8858, "highest_cost_orders_all_payers": 1814, "highest_cost_Medicare_orders": None, "note": "Unit is prescription order. Patients/prescribers can appear in both exposures; do not add arm patient counts. Highest-cost Medicare N not reported in eTable6."},
    "intervention": "Point-of-prescribing EHR alert suggests up to three lower-cost clinically equivalent alternatives (drug, supply or pharmacy); initial order cost>=$5 and savings>=$0.10/day required. Identical engine in controls but alerts suppressed.",
    "comparator": "No displayed RTPB recommendations in randomized control practices",
    "software_directness": "Direct software intervention; only orders with available price/alternative and linked dispense data analyzed. Applicability limited to a small fraction of all prescribing.",
    "outcomes": [
        outcome("All-payer prescription orders filled",1.2,-1.3,3.7,"adjusted percentage-point difference","Main Table2",n=38289,intervention_percent=55,control_percent=54,endpoint_type="Prescription fill/process",interpretation="Overall null"),
        outcome("All-payer highest-cost drug-class orders filled",14.5,8.4,20.6,"adjusted percentage-point difference","Main Table2; drug-class mean cost>$120.83 per30days",n=1814,intervention_percent=49,control_percent=33,endpoint_type="Prescription fill/process",interpretation="Exploratory positive subgroup; quartiles are of drug classes, not equal order counts"),
        outcome("Medicare prescription orders filled",0.5,-2.4,3.4,"adjusted percentage-point difference","Supplement2 eTable6 p7, visually checked",n=21897,intervention_percent=55,control_percent=55,endpoint_type="Prescription fill/process",interpretation="Medicare subgroup overall null"),
        outcome("Medicare highest-cost drug-class orders filled",10.5,1.9,19.2,"adjusted percentage-point difference","Supplement2 eTable6 p7, visually checked; rounded threshold>$120.8",n=None,endpoint_type="Prescription fill/process",interpretation="Exploratory Medicare subgroup; exact high-cost N absent"),
        outcome("Highest-cost drug-class fills in lowest-income ZIP quartile",30.3,19.5,41.1,"adjusted percentage-point difference","Main Results and Figure2 text",intervention_percent=49,control_percent=27,endpoint_type="Prescription fill/process",interpretation="Exploratory ecological income stratum; not a patient-sex effect"),
        outcome("Highest-cost drug-class fills in highest-income ZIP quartile",1.0,-10.2,12.2,"adjusted percentage-point difference","Main Results and Figure2 text",endpoint_type="Prescription fill/process",interpretation="Null in higher-income stratum; not evidence of a statistically tested difference from low-income stratum"),
    ],
    "analysis": "Logistic regression adjusted age, EHR sex, insurance, specialty and drug class; robust SE clustered by practice, sensitivity two-way practice/patient clustering. Dispense matching on patient/medication/prescriber and +/-28-day date window; alternate algorithms and less-restrictive inclusion sensitivity checks.",
    "sex_analysis": "Sex adjustment only; no sex-stratified intervention effect or intervention-by-sex test in main text or reviewed supplement tables.",
    "null_or_negative_evidence": ["Overall and Medicare-wide fill effects null.", "Lower-cost drug classes showed no clear improvement.", "No clinical outcomes, long-term adherence, actual drug ingestion or cost-effectiveness demonstrated.", "High-cost and income findings are post hoc, multiple comparisons, hypothesis generating; ZIP income is not individual income.", "Restricting patients to those with any dispense record conditions on observed filling; only63.8% eligible orders enter analysis, and2.8% of all orders."],
    "funding": "AHRQ K01HS026980 (Desai),3T32HS026120-05S1 (Ying), and NCPDP Foundation.",
    "conflicts": "None reported in article.",
    "sponsor_role": "Reported no funder role in design/conduct, data handling/analysis, manuscript or submission.",
    "appraisal": {"status": "Provisional AI cluster-RCT domain notes; no formal overall RoB2 rating", "randomization": "Specialty-stratified practice profiles randomized1:1; residual specialty imbalance due cluster size. Same trial as2022 parent.", "recruitment_after_randomization": "Eligibility based on prices/alternatives and observation of dispensing after assignment; identical background engines reduce differential eligibility but selection remains a concern.", "deviations": "Some patients/prescribers exposed in both arms; contamination possible; no need to assume exclusive arms.", "missing_data": "Incomplete PBM/pharmacy fill coverage; patients need any dispense record in primary analysis. Sensitivity checks do not establish complete capture.", "measurement": "Record-linkage based fill outcome, not continuous adherence or health. Pharmacy capture need not include every dispensing event.", "selective_reporting": "Fill outcome not prespecified; extended follow-up and multiple stratified analyses. Strong subgroup signals require prospective replication.", "applicability": "One urban system, one tool, narrow recommendation eligibility and much higher Medicare share in analyzed orders than all orders."},
    "source_discrepancies": ["Article XML publication dateAug14 conflicts with MEDLINE-derived first dateAug7; retained in metadata.", "Supplement2 eTable1 footnote ends studyDec14,2021; main methods/Table1 endDec31,2021.", "Supplement age bins41-65/66+ differ from main41-64/>=65 despite identical counts; main bins retained for extraction.", "eTable6 intermediate-cost Medicare CI is printed1.7(-27,6.2); visually confirmed. Do not silently change to-2.7; that estimate not used for inference.", "Supplement eTable2 excluded orders21,205 differs from main eligible60,041 minus analyzed38,289=21,752; denominator reconciliation pending."],
    "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13476843/",
    "source_locators": ["Main methods/results/Table1-2", "Main limitations/disclosures", "Supplement2 eTable6 page7 (visual verification), eTables1-2 for audit discrepancies"],
    "access_limitations": "Full main text and tables reviewed; Supplement2 selectively reviewed. Original protocol and full2022 parent report not reviewed in this bounded task. Do not call full formal risk-of-bias review complete.",
})

payload = {
    "updated_on": DATE,
    "purpose": "Targeted supplemental translational intervention evidence for Medicare research and health IT hypotheses; separate from primary patient-sex disparity synthesis",
    "status": "Provisional AI extraction, not a completed systematic review or independent human adjudication",
    "counts": {"detailed_reports": 4, "existing_canonical_reports": 1, "new_context_reports_proposed": 3, "additional_linked_parent_reports": 1, "independent_study_families_among_detailed_reports": 4, "new_primary_patient_sex_studies": 0},
    "scope": {"identity": "Unresolved under current REVIEW_SCOPE; no confirmed cisgender labels", "clinical_care_items_added": 0, "canonical_register_edited": False, "formal_GRADE_performed": False},
    "records": studies,
    "linked_parent_reports": [{"proposed_id": "L-T03-P1", "pmid": "36094537", "trial_id": "NCT04940988", "linked_report_id": "L-T03", "independent_trial": False, "access": "Verified metadata and abstract only", "summary": "2022 primary trial report assesses estimated out-of-pocket costs of orders. It is the parent trial of the2026 post hoc fill analysis, not a second independent intervention.", "abstract_only_results": {"orders": 867757, "eligible_orders": 36419, "eligible_percent": 4.2, "adjusted_estimated_OOP_percent_change": -11.2, "CI": [-15.7,-6.4]}, "inference_limit": "Order-price estimates are not realized patient spending; do not upgrade abstract-only verification to full-text extraction.", "source": "https://pubmed.ncbi.nlm.nih.gov/36094537/"}],
    "synthesis_boundaries": ["Process/adherence-proxy improvement is not demonstrated health benefit.", "Bundled financial assistance/pharmacist programs cannot isolate a software effect.", "No selected report establishes closure of patient sex/gender gaps; heterogeneity analyses concern race/income/cost/insurance or a male-only cohort.", "Medicare Advantage single-insurer data do not represent all Original Medicare/PartD policies.", "No pooled meta-analysis: different interventions, estimands, periods and outcome units; shared trial reports explicitly linked."],
}
(OUT / "intervention_evidence.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
(HERE / "verified_metadata.json").write_text(json.dumps({"generated_on": DATE, "records": records}, indent=2, ensure_ascii=False) + "\n")
manifest = json.loads((HERE / "retrieval_manifest.json").read_text())
extra_requests = [
    {"pmid": "39073823", "url": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11287444/fullTextXML", "status": "Second attempt HTTP500; publisher fulltext used"},
    {"pmid": "39073823", "url": "https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2821705", "status": "Full main-text web view read; source not downloaded locally; extracted results and locators retained"},
    {"pmid": "42599729", "url": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13476843/supplementaryFiles", "file": "42599729_supplementary_files.zip", "status": "HTTP200; ZIP saved; Supplement2 PDF extracted, eTable6 visually inspected"},
]
for req in extra_requests:
    if req not in manifest["requests"]: manifest["requests"].append(req)
manifest["limitations"] = ["PMC browser/web views returned recaptcha for some articles; EuropePMC public XML used when available.", "No author contact or access-control circumvention; access failures remain documented."]
(HERE / "retrieval_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
assert len(payload["records"]) == 4 and len(records) == 5
assert 9601+9512 == 19113 and 3977+3865 == 7842
assert 2645075+30356720 == 33001795 and 13039+8858 == 21897
print("Wrote four detailed reports, five metadata records including one linked parent, and retrieval manifest.")
