import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {loadMetadata,synchronizeCitation} from './bibliography.mjs';

export async function applyReviewScope(rawItems,rawStudies){
  const scope=JSON.parse(await fs.readFile('/Users/lgm/Documents/ChatGPT/Medicare/research/review_scope.json','utf8'));
  const clinicalBasis=JSON.parse(await fs.readFile('/Users/lgm/Documents/ChatGPT/Medicare/research/clinical_basis.json','utf8'));
  const evidenceSubjects=JSON.parse(await fs.readFile('/Users/lgm/Documents/ChatGPT/Medicare/research/evidence_subjects.json','utf8'));
  const subjectStudies=new Map(evidenceSubjects.studies.map(x=>[x.id,x]));
  const subjectGroups=new Map(evidenceSubjects.groups.map(x=>[x.id,x]));
  assert.equal(subjectStudies.size,evidenceSubjects.studies.length,'Duplicate study subject ID');
  const basisItems=new Map(clinicalBasis.items.map(x=>[x.id,x]));
  const basisGroups=new Map(clinicalBasis.groups.map(x=>[x.id,x]));
  const excludedItems=rawItems.filter(x=>scope.excluded_item_ids.includes(x.id));
  const metadata=await loadMetadata();
  const excludedStudies=rawStudies.filter(x=>scope.excluded_study_ids.includes(x.id)).map(s=>synchronizeCitation(s,metadata));
  const items=rawItems.filter(x=>!scope.excluded_item_ids.includes(x.id)).map(x=>{
    const item={...x,...scope.overrides[x.id]};
    item.study_ids=item.study_ids.filter(id=>!scope.excluded_study_ids.includes(id));
    const b=basisItems.get(item.id),g=b&&basisGroups.get(b.group);
    if(!g)throw new Error(`Clinical basis classification required for ${item.id}`);
    Object.assign(item,{clinical_basis:g.label,clinical_basis_id:g.id,sex_specific_feature:b.sex_feature,analysis_approach:b.approach||g.approach,classification_notes:b.notes,classification_source_ids:b.source_ids||[]});
    return item;
  });
  const context=JSON.parse(await fs.readFile('/Users/lgm/Documents/ChatGPT/Medicare/research/literature_context.json','utf8').catch(e=>{if(e.code==='ENOENT')return '{"studies":[]}';throw e;}));
  const followup=JSON.parse(await fs.readFile('/Users/lgm/Documents/ChatGPT/Medicare/research/literature_followup.json','utf8').catch(e=>{if(e.code==='ENOENT')return '{"studies":[]}';throw e;}));
  const studies=[...rawStudies.filter(x=>!scope.excluded_study_ids.includes(x.id)),...[...context.studies,...followup.studies].filter(x=>!rawStudies.some(s=>s.id===x.id)&&!scope.excluded_study_ids.includes(x.id))].map(s=>synchronizeCitation(s,metadata));
  for(const study of studies){
    const coding=subjectStudies.get(study.id),group=coding&&subjectGroups.get(coding.subject_id);
    assert(group,`Missing analytic subject for ${study.id}`);
    Object.assign(study,coding,{analytic_subject:group.label});
  }
  assert.equal(studies.length,subjectStudies.size,'Subject classifications must match active studies');
  return {scope,clinicalBasis,evidenceSubjects,items,studies,excludedItems,excludedStudies};
}
