"""Integrate verified candidate records without overwriting broad-search source records."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def read(path):
    return json.loads(path.read_text())

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def upsert(rows, additions):
    index = {r["id"]: r for r in rows}
    index.update({r["id"]: r for r in additions})
    return list(index.values())

drug = read(HERE / "drug_access/integration_proposal.json")
bone = read(HERE / "bone/extraction.json")["records"]
metadata = read(ROOT / "research/bibliography_metadata.json")
new_meta = drug["metadata_records"]
new_studies = drug["studies"]
new_subjects = drug["evidence_subjects"]
for r in bone:
    m = r["metadata"]
    sid = r["proposed_root_study_id"]
    new_meta.append({**m, "id": sid, "record_type": "journal-article", "original_citation": m["title"],
        "verification_source": f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID%3A{m["pmid"]}+AND+SRC%3AMED&format=json&resultType=core',
        "notes": [r["correction_check"]["result"], "Population identity unresolved; AI candidate extraction, not human eligibility adjudication."]})
    first = sid == "L-R03"
    coding = {"id": sid, "subject_id": "patient_care", "unit_of_analysis": r["study"]["unit_of_analysis"],
        "patient_sex_gender_role": r["sex_gender"]["measurement"] + "; gender identity not reported",
        "physician_sex_gender_role": "No physician-sex comparison", "comparison_axis": r["sex_gender"]["comparison"],
        "inference_boundary": "Shared bone system. Utilization does not identify denied claims or reimbursement causation; identity remains unresolved."}
    new_subjects.append(coding)
    new_studies.append({**coding, "citation": m["title"], "year": m["year"], "design": r["study"]["design"],
        "population": "80,439 eligible Asian American beneficiaries; women >=65, men >=70" if first else "588,737 Medicare Advantage women aged >=50 within 1,638,454 MA/commercial women",
        "payer": r["study"]["payer"], "data_period": r["study"]["study_years"] or "Not established from abstract",
        "finding": "Asian American subgroup DXA receipt: women 19.8% versus men 5.0% (P<.001). Overall 12,102/80,439 (15.1%). Sex-specific denominators and adjusted sex effects unavailable." if first else "MA women: two-year bone measurement 22.9% (95% CI 22.8–23.0); age 65–79: 26.8% (26.6–26.9), n=394,791; age >=80: 12.9% (12.7–13.1), n=135,661. Women-only, not a sex-effect estimate.",
        "limitation": "Abstract-only; differing age thresholds; unknown observation years and clinical-need adjustment. The adjusted reported contrast concerns race, not sex. Identity unresolved." if first else "Selected continuously enrolled MA/commercial women; MA descriptive results separable, adjusted models mix payers. Bone measurement broader than DXA; nonreceipt does not prove unmet need. Identity unresolved; no male comparator.",
        "relevance": "Shared-system bone screening and clinical eligibility; candidate awaiting human full-text/identity adjudication",
        "url": m["url"], "doi_or_pmid": f'{m["doi"]}; PMID {m["pmid"]}',
        "extraction_level": r["access"]["level"], "extraction_source": "research/review_2026-09-21/bone/extraction.json",
        "primary_synthesis_eligible": False})
for s in new_studies:
    s["population_screening_status"] = "Candidate: identity eligibility unresolved; human screening pending"
    s["identity_reporting"] = s["patient_sex_gender_role"]
    s["screening_notes"] = "Provisional AI extraction on 2026-09-21. Not included in a confirmed-cisgender primary synthesis; no formal risk-of-bias or certainty assessment."
    s["review_status"] = "AI preliminary candidate extraction"
    s["clinical_basis_id"] = "shared"
metadata["records"] = upsert(metadata["records"], new_meta)
metadata["generated_on"] = "2026-09-21"
save(ROOT / "research/bibliography_metadata.json", metadata)
followup = read(ROOT / "research/literature_followup.json")
followup["studies"] = upsert(followup["studies"], new_studies)
for s in new_studies:
    if not any(p["id"] == s["id"] for p in followup["provenance"]):
        followup["provenance"].append({"id": s["id"], "checked": "2026-09-21", "extraction": s["extraction_source"],
            "method": "Targeted other-method retrieval and provisional AI extraction; reconciled by PMID against database results", "source_access": s["extraction_level"]})
save(ROOT / "research/literature_followup.json", followup)
subjects = read(ROOT / "research/evidence_subjects.json")
subjects["studies"] = upsert(subjects["studies"], new_subjects)
subjects["updated_on"] = "2026-09-21"
save(ROOT / "research/evidence_subjects.json", subjects)
save(ROOT / "research/retrieval_evidence.json", {"updated_on": "2026-09-21", "status": "Reviewed retrieval leads/context outside the active register; no final full-text exclusion counts", "records": drug["outside_active_register"]})

valuation = read(HERE / "valuation/extraction.json")["studies"]
updates = {r["id"]: {"extraction_level": r["access_level"], "last_reviewed_on": "2026-09-21",
    "extraction_source": "research/review_2026-09-21/valuation/extraction.json", "screening_notes": r["proposed_status"]} for r in valuation}
updates["L-P02"]["limitation"] = "Small selected set; null does not establish equivalence. Journal abstract reports 10 pairs (7 female higher), AUA companion 9 (6 female higher). Full text, valuation year and numerical CIs pending."
updates["L-P03"]["limitation"] = "Specialty compensation multipliers are not Medicare conversion factors; global/perioperative work omitted. Published arithmetic discrepancies flagged in extraction notes. NSQIP is not a Medicare-only cohort."
save(ROOT / "research/study_review_updates.json", {"updated_on": "2026-09-21", "updates": updates})
scope = read(ROOT / "research/review_scope.json")
for care_id in ["G04", "G05"]:
    override = scope["overrides"].setdefault(care_id, {})
    override["study_ids"] = list(dict.fromkeys(["L-G04", "L-G05", "L-R03", *(["L-R04"] if care_id == "G04" else [])]))
save(ROOT / "research/review_scope.json", scope)

spec = read(ROOT / "research/preliminary_synthesis.json")
spec["version"] = "1.1"
spec["updated_on"] = "2026-09-21"
patterns = {p["id"]: p for p in spec["patterns"]}
patterns["PAT-02"]["boundary"] = "Selected pairs cannot establish a universal effect. Nonsignificance does not establish equivalence. Full texts of Penn/Hathaway remain pending; Hathaway journal/companion pair counts disagree (10/9). Polan dollar rates model specialty compensation; some printed arithmetic needs verification."
patterns["PAT-04"]["observation"] = "Historical Medicare bone-testing use was lower in men. A men's fragility-fracture outreach program increased testing from 4.9% to 10.7%. A newly checked, identity-unresolved Asian American Medicare study reports DXA receipt of 19.8% in women and 5.0% in men, with different age thresholds. A separate women-only MA study reports lower two-year bone measurement at age >=80 than 65–79."
patterns["PAT-04"]["study_ids"] = list(dict.fromkeys(patterns["PAT-04"]["study_ids"] + ["L-R03", "L-R04"]))
patterns["PAT-04"]["boundary"] = "New patient records have unresolved identity eligibility. The Asian American result is crude and abstract-only, with women >=65 versus men >=70; it is not a national adjusted sex effect. MA women-only results do not estimate a male/female gap. Need, preferences, intervals and delivery barriers remain distinct from coverage."
patterns["PAT-06"]["observation"] = "The Lancet review connects biology and social pathways to clinical need; kidney-care interviews identify perceived practical barriers. Newly extracted, identity-unresolved Medicare studies report female-higher cost-related nonadherence in a 2016 national survey but an imprecise adjusted persistent-nonadherence contrast in a selected Chicago cohort."
patterns["PAT-06"]["study_ids"] = list(dict.fromkeys(patterns["PAT-06"]["study_ids"] + ["L-R01", "L-R02"]))
patterns["PAT-06"]["boundary"] = "Patient identity eligibility and human verification remain pending. Annual any-nonadherence and persistent nonadherence are different outcomes; do not pool them. These historical observational results do not establish current coverage discrimination."
patterns["PAT-06"]["dashboard"] = "Medication affordability is a measurable access pathway. National and selected-cohort results differ in precision and outcome; identity eligibility remains unresolved."
hypothesis = {"id": "HYP-09", "title": "Medication affordability and sex differences in nonadherence", "stream": "Patient care/access",
    "statement": "Among beneficiaries with comparable medication needs, financial burden contributes to sex differences in cost-related nonadherence, with potentially different effects for younger and older beneficiaries.",
    "population": "Medicare beneficiaries using indicated medicines; retain <65 and >=65 strata and resolve the project identity criterion before primary inclusion.",
    "exposure": "Actual patient cost sharing and changes in financial protection; keep coverage, income and disease burden distinct.",
    "comparator": "Comparable medication needs across sex and policy periods; benefit-change studies need defensible controls.",
    "outcome": "Annual any cost-related nonadherence and longitudinal persistence analyzed separately; retain reduced spending on necessities as a separate outcome.",
    "test": "Extract complete age-specific estimates, assess overlap and outcome compatibility, then examine policy-change designs with pretrends, clinical need and potential mediators specified.",
    "alternatives": "Different illness and medicine burdens, income, recall, patient preferences, plan selection and survivor selection; adjustment may also remove pathways of disparity.",
    "weakens": "Precise null contrasts in clinically comparable groups and no differential response to financial protection would weaken the proposed mechanism; imprecise null results do not establish equality.",
    "readiness": "Two provisional full-text candidates; identity eligibility, human verification and appraisal pending", "priority": "Further evidence extraction",
    "evidence_ids": ["L-R01"], "counter_ids": ["L-R02"], "policy_ids": [],
    "next_step": "Verify complete tables and model denominators, retrieve supplements, complete independent human review and search for compatible policy-change studies.",
    "evidence_summary": "MCBS 2016 female:male adjusted OR 1.66 (1.31–2.10) under65 and 1.21 (1.04–1.41) at65+. Chicago persistent-nonadherence OR 1.36 (0.95–1.95). Different endpoints and samples prevent direct pooling; neither establishes current causal bias."}
spec["hypotheses"] = upsert(spec["hypotheses"], [hypothesis])
save(ROOT / "research/preliminary_synthesis.json", spec)
print("Integrated four candidate records, two separately logged retrieval references, three extraction updates, and one exploratory hypothesis.")
