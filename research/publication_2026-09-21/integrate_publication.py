from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def read(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
metadata=read(ROOT/'research/bibliography_metadata.json');existing={m['id']:m for m in metadata['records']}
newmeta=read(HERE/'intervention_sources/verified_metadata.json')['records']
for m in newmeta:
 if m['id']=='L-G05':continue
 m={**m,'record_type':'journal-article','reviewed_fulltext_url':m.get('fulltext_url','')}
 if m['id']=='L-T03-P1':m.update(related_record_id='L-T03',relationship='Earlier report of the same trial; not an independent study')
 existing[m['id']]=m
metadata['records']=list(existing.values());metadata['updated_on']='2026-09-21';save(ROOT/'research/bibliography_metadata.json',metadata)
ev=read(HERE/'intervention_evidence.json');translation=[]
for r in ev['records']:
 if r['id']=='L-G05':continue
 translation.append({'id':r['id'],'pmid':r['pmid'],'status':'Translational intervention context; outside primary patient-sex synthesis','active_register':False,'primary_synthesis_eligible':False,'analytic_subject':'Intervention effectiveness and implementation context','unit_of_analysis':r['analysis'] if isinstance(r['analysis'],str) else 'See extraction for participant/order/practice unit and estimand','patient_sex_gender_role':r.get('sex_analysis','Not an intervention-by-sex comparison'),'physician_sex_gender_role':'No physician-gender effect tested','comparison_axis':'Intervention/implementation versus comparator; not female-versus-male treatment effect','inference_boundary':r['sex_equity_conclusion'],'access_level':r['access_limitations'],'source_url':r['source_url'],'source_file':'research/publication_2026-09-21/intervention_evidence.json','related_reference_ids':['L-T03-P1'] if r['id']=='L-T03' else []})
p=ev['linked_parent_reports'][0];translation.append({'id':'L-T03-P1','pmid':p['pmid'],'status':'Linked parent report of L-T03; not an independent trial','active_register':False,'primary_synthesis_eligible':False,'access_level':p['access'],'source_url':p['source'],'related_record_id':'L-T03','relationship':'Earlier report of the same trial','inference_boundary':p['inference_limit']})
save(ROOT/'research/translational_evidence.json',{'updated_on':'2026-09-21','status':'Separate contextual stream for proposed interventions; no primary-sex study added','detailed_new_reports':3,'linked_parent_reports':1,'independent_new_study_families':3,'records':translation})
op=read(HERE/'opportunities.json');save(ROOT/'research/opportunity_assessment.json',op)
cb=read(ROOT/'research/clinical_basis.json');cb['translational_indications']=[
 {'id':'TI-01','opportunity_id':'O-01','indication':'COPD maintenance medication affordability','group_id':'shared','anatomy_or_function':'Respiratory system','eligibility_or_burden':'Documented COPD and clinically indicated maintenance therapy; not sex-exclusive','source_ids':['L-T01']},
 {'id':'TI-02','opportunity_id':'O-01','indication':'Local vaginal treatment for genitourinary symptoms of menopause','group_id':'female_anatomy','anatomy_or_function':'Vaginal reproductive tissue; menopausal physiological context','eligibility_or_burden':'Clinical indication and treatment choice are separate from plan formulary status','source_ids':['L-D01','L-D03','L-D04']},
 {'id':'TI-03','opportunity_id':'O-01','indication':'Systemic menopausal symptom treatment navigation','group_id':'female_physiology','anatomy_or_function':'Reproductive physiological context with systemic drug effects','eligibility_or_burden':'Formulation and individual benefit-risk assessment required; not interchangeable with COPD or local vaginal therapy','source_ids':['L-B01']},
 {'id':'TI-04','opportunity_id':'O-02','indication':'Post-fracture bone-care follow-up','group_id':'shared','anatomy_or_function':'Skeletal system','eligibility_or_burden':'Qualifying fracture and clinical assessment; screening eligibility is not the same as secondary prevention','source_ids':['L-G05','P-012','P-053']},
 {'id':'TI-05','opportunity_id':'O-03','indication':'Non-drug prior-authorization workflow','group_id':'mixed','anatomy_or_function':'Varies by the underlying clinically indicated service','eligibility_or_burden':'Split service and indication before comparing patient groups; payer eligibility is separate','source_ids':['P-046','P-047']},
 {'id':'TI-06','opportunity_id':'O-04','indication':'Procedure-valuation measurement','group_id':'mixed','anatomy_or_function':'Varies by code, organ, episode and service','eligibility_or_burden':'Clinical comparability and work/resource requirements need independent adjudication','source_ids':['L-P01','L-P02','L-P03']},
 {'id':'TI-07','opportunity_id':'O-05','indication':'Lymphedema compression-item fulfillment','group_id':'shared','anatomy_or_function':'Lymphatic system; affected site varies','eligibility_or_burden':'Need is not restricted to breast-cancer survivors or one sex','source_ids':['P-021','P-054','L-A01']},
 {'id':'TI-08','opportunity_id':'O-06','indication':'Kidney education and care coordination','group_id':'shared','anatomy_or_function':'Renal function','eligibility_or_burden':'Stage and clinical need are separate from six-session Medicare education eligibility','source_ids':['P-055','L-Q01']}
];cb['translational_classification_note']='Separate opportunity indications; not additional rows in the 40-item coverage inventory. Classification does not establish patient identity or coverage.';save(ROOT/'research/clinical_basis.json',cb)
up=read(ROOT/'research/study_review_updates.json');up['updates']['L-G05']={'extraction_level':'Full main-text XML and tables reviewed on 2026-09-21; figure images and supplementary appendix not independently inspected','last_reviewed_on':'2026-09-21','extraction_source':'research/publication_2026-09-21/intervention_evidence.json','population':'10,934 men randomized; 7,842 analyzed (3,977 intervention; 3,865 control) after 3,092 post-assignment exclusions','limitation':'Single MA insurer; 28.3% excluded after assignment, including deaths/disenrollment. Selected untreated fracture patients; bundled communication intervention, no software-only effect or direct sex comparison. Process outcomes do not prove fracture reduction. Identity not established.','screening_notes':'Provisional AI full-text update. Randomized N differs from analyzed N; no independent human appraisal or final identity eligibility decision.'};save(ROOT/'research/study_review_updates.json',up)
# Update current scientific-metadata count references without altering historical files.
synth=read(ROOT/'research/preliminary_synthesis.json');synth['publication_update']='Separate translational intervention context and opportunity assessment added 2026-09-21; original nine hypotheses remain exploratory.';save(ROOT/'research/preliminary_synthesis.json',synth)
print('Integrated4 new reference reports in3 independent interventionfamilies; active38unchanged;8 opportunityindications classified.')
methods=read(ROOT/'research/methodology_references.json')
by_id={m['id']:m for m in methods['records']}
for m in read(HERE/'method_metadata_proposals.json')['records']:
 m={**m,'publication_status':'Imported for planned appraisal; instrument not yet applied'}
 by_id[m['id']]=m
methods['records']=list(by_id.values());methods['updated_on']='2026-09-21'
save(ROOT/'research/methodology_references.json',methods)
