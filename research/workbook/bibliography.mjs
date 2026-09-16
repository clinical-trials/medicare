import fs from 'node:fs/promises';
import assert from 'node:assert/strict';

const root='/Users/lgm/Documents/ChatGPT/Medicare';
const out=`${root}/outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8`;
const date='2026-09-16';
const clean=x=>String(x??'').replace(/[\r\n]+/g,' ').trim();
const link=u=>clean(u).replace(/\(/g,'%28').replace(/\)/g,'%29');
const period=s=>{const t=clean(s);return !t?'':/[.!?]$/.test(t)?t:t+'.';};
const author=a=>a.literal||`${a.family||''} ${a.initials||a.given||''}`.trim();

export function formatCitation(m,short=false){
  if(!m?.title)return m?.original_citation||'';
  const names=(m.authors||[]).map(author);
  const limit=short?1:6;
  const authors=names.length>limit?`${names.slice(0,limit).join(', ')}, et al`:names.join(', ');
  const details=`${m.year||''}${m.volume?`;${m.volume}`:''}${m.issue?`(${m.issue})`:''}${m.pages?`:${m.pages}`:''}`;
  return [period(authors),period(m.title),period(m.journal_abbreviation||m.journal),period(details)].filter(Boolean).join(' ');
}

export async function loadMetadata(){
  const data=JSON.parse(await fs.readFile(`${root}/research/bibliography_metadata.json`,'utf8').catch(e=>{if(e.code==='ENOENT')return '{"records":[]}';throw e;}));
  return new Map(data.records.map(x=>[x.id,x]));
}

export function synchronizeCitation(study,metadata){
  const m=metadata.get(study.id);
  if(!m?.metadata_status?.startsWith('Verified'))return study;
  return {...study,original_citation:study.original_citation||study.citation,citation:formatCitation(m,true),year:m.year||study.year,
    doi_or_pmid:[m.doi,m.pmid?`PMID ${m.pmid}`:'',!m.doi&&m.pmcid?m.pmcid:''].filter(Boolean).join('; '),
    citation_metadata_status:m.metadata_status};
}

export async function buildBibliography(data,drugSources){
  const metadata=await loadMetadata();
  const activeIds=new Set(data.studies.map(x=>x.id));
  const excludedIds=new Set(data.excludedStudies.map(x=>x.id));
  const sourceStudies=[...data.studies,...data.excludedStudies];
  const contextStatuses=new Set(['Clinical background','Clinician context','Qualitative access context']);
  const scientific=sourceStudies.map(s=>{
    const m=metadata.get(s.id)||{id:s.id,original_citation:s.citation,metadata_status:'Unverified legacy citation',authors:[]};
    return {...m,source_type:'scientific',citation:formatCitation(m),source_url:s.url,
      status:excludedIds.has(s.id)?'Excluded by current population scope':s.synthesis_role==='context_only'?(s.context_type==='qualitative_access'?'Qualitative access context':s.context_type==='clinical_background'?'Clinical background':'Clinician context'):s.synthesis_role==='historical_patient_candidate'?'Historical patient evidence; eligibility pending':'Candidate evidence / retained code-policy component',
      access_level:s.extraction_level||'Citation/abstract extraction recorded; full-text review pending',
      eligibility:s.population_screening_status||'See workbook population-screening status',
      analytic_subject:s.analytic_subject,unit_of_analysis:s.unit_of_analysis,
      patient_sex_gender_role:s.patient_sex_gender_role,physician_sex_gender_role:s.physician_sex_gender_role,
      comparison_axis:s.comparison_axis,inference_boundary:s.inference_boundary,
      linked_care_ids:data.items.filter(i=>i.study_ids.includes(s.id)).map(i=>i.id),
      related_reference_ids:s.related_reference_ids||[]};
  });
  const corrections=[...metadata.values()].filter(m=>m.record_type==='correction'&&activeIds.has(m.related_record_id)).map(m=>({...m,source_type:'scientific',citation:formatCitation(m),source_url:m.url,status:'Linked correction; not an independent study',access_level:'Correction metadata verified',linked_care_ids:[]}));
  const previous=JSON.parse(await fs.readFile(`${root}/research/reference_registry.json`,'utf8').catch(e=>{if(e.code==='ENOENT')return '{"policy_sources":[]}';throw e;}));
  const policyMap=new Map((previous.policy_sources||[]).map(x=>[x.url,{...x,linked_record_ids:[],descriptions:[],current_use:false}]));
  let nextId=Math.max(0,...[...policyMap.values()].map(x=>Number(x.id.replace('P-',''))||0))+1;
  function add(url,description,recordId,extra={}){
    if(!url?.startsWith('http'))return;
    let s=policyMap.get(url);
    if(!s){s={id:`P-${String(nextId++).padStart(3,'0')}`,url,descriptions:[],linked_record_ids:[],source_type:'policy_or_data',recorded_on:date,verification_status:'Carried from research sources; not reverified during bibliography backfill'};policyMap.set(url,s);}
    if(description&&!s.descriptions.includes(description))s.descriptions.push(description);
    if(recordId&&!s.linked_record_ids.includes(recordId))s.linked_record_ids.push(recordId);
    s.current_use=true;Object.assign(s,extra);
  }
  for(const i of [...data.items,...data.excludedItems]){
    for(const u of [i.policy_url,i.policy_url2])add(u,i.item,i.id);
  }
  for(const s of drugSources.supplemental_policy_sources||[])add(s.url,s.topic,'Supplemental source');
  const fm=JSON.parse(await fs.readFile(`${root}/research/formulary_results.json`,'utf8')).metadata;
  add(fm.archive_url,'CMS monthly Part D formulary archive','Drug formularies',{source_version:fm.formulary_release,source_access_date:fm.retrieved});
  add(fm.reference_url,'CMS formulary reference file','Drug formularies',{source_version:fm.reference_date,source_access_date:fm.retrieved});
  const pairs=JSON.parse(await fs.readFile(`${root}/research/procedure_pairs_2026.json`,'utf8'));
  add(pairs.cms_landing_url,'CMS RVU26C physician relative value files','Procedure values',{source_version:pairs.csv_released,source_access_date:pairs.review_date});
  add(pairs.pair_selection_source.author_table_url,'Author-published procedure comparison table','Procedure values');
  const cms=JSON.parse(await fs.readFile(`${root}/research/sources/CMS_source_metadata.json`,'utf8'));
  for(const s of cms){
    add(s.landingPage,s.title,'CMS data sources',{official_title:s.title,source_version:s.modified});
    if(s.describedBy)add(s.describedBy,`Data dictionary: ${s.title}`,'CMS data sources');
  }
  for(const s of data.benchmark?.sources||[]){
    add(s.url,s.title,'Medicare benchmark rationale',{official_title:s.title,organization:s.organization,authors:s.authors,report:s.report,source_version:s.data_period,source_access_date:s.accessed_on,verification_status:'Verified against official source for benchmark framing on 2026-09-16',notes:s.note});
  }
  const policies=[...policyMap.values()].sort((a,b)=>a.id.localeCompare(b.id));
  const clinicalGuidance=data.clinicalBasis?.sources||[];
  const records=[...scientific,...corrections];
  assert.equal(new Set(records.map(x=>x.id)).size,records.length,'Duplicate reference ID');
  const counts={active_studies:data.studies.length,excluded_studies:data.excludedStudies.length,linked_corrections:corrections.length,verified_scientific_metadata:records.filter(x=>x.metadata_status?.startsWith('Verified')).length,policy_and_data_sources:policies.filter(x=>x.current_use).length};
  counts.clinical_guidance_sources=clinicalGuidance.length;
  const lines=['# Medicare sex-based coverage and reimbursement: working bibliography','',`Updated ${date}. Stable IDs match the evidence register. ${counts.active_studies} active literature records; ${counts.excluded_studies} scope-excluded records retained for audit; ${counts.linked_corrections} linked correction.`,
    '', 'This is a living reference list for an ongoing review, not a completed systematic-review bibliography. Publication metadata have been checked separately from full-text extraction, eligibility and risk-of-bias assessment. References cited within reviews are not automatically included as screened studies.',
    '', 'Use `[L-ID]` in working drafts. The bibliography gives up to six authors followed by et al.; the RIS export preserves all available authors. Article titles and publication details follow MEDLINE metadata. Policy descriptions below are source labels, not verified publication titles unless identified as such. The record date is not a new policy verification date.',''];
  function emit(section,rows){
    lines.push(`## ${section}`,'');
    for(const r of rows){
      lines.push(`### ${r.id}`,'',r.citation||r.original_citation,'');
      const urls=[r.doi?`[DOI](https://doi.org/${link(r.doi)})`:'',r.pmid?`[PMID ${r.pmid}](https://pubmed.ncbi.nlm.nih.gov/${r.pmid}/)`:'',r.source_url?`[Reviewed source](${link(r.source_url)})`:''].filter(Boolean);
      lines.push(urls.join(' · '),'',`**Role:** ${r.status}. **Access:** ${r.access_level}.`,'',`**Citation metadata:** ${r.metadata_status}${r.verified_on?`; checked ${r.verified_on}`:''}.`,'');
      if(r.linked_care_ids?.length)lines.push(`Care-item links: ${r.linked_care_ids.join(', ')}.`,'');
      if(r.analytic_subject)lines.push(`**Analytic subject:** ${r.analytic_subject}. **Unit:** ${r.unit_of_analysis}.`,'',`Patient sex/gender: ${r.patient_sex_gender_role}. Physician sex/gender: ${r.physician_sex_gender_role}.`,'',`Comparison: ${period(r.comparison_axis)} Inference boundary: ${period(r.inference_boundary)}`,'');
      if(r.related_record_id)lines.push(`Linked reference: [${r.related_record_id}](#${r.related_record_id.toLowerCase()}) (${r.relationship}).`,'');
      for(const note of r.notes||[])lines.push(`Metadata note: ${note}`,'');
    }
  }
  emit('Candidate evidence and retained code/policy studies',scientific.filter(x=>activeIds.has(x.id)&&!contextStatuses.has(x.status)));
  emit('Contextual literature',scientific.filter(x=>contextStatuses.has(x.status)));
  emit('Linked corrections',corrections);
  emit('Excluded records retained for audit',scientific.filter(x=>excludedIds.has(x.id)));
  lines.push('## Clinical guidance for anatomy and physiology classification','', 'These sources support clinical classification, not Medicare coverage decisions. C-IDs are guidance records and are not counted as scientific studies.','');
  for(const s of clinicalGuidance){
    const ids=data.items.filter(i=>i.classification_source_ids?.includes(s.id)).map(i=>i.id);
    lines.push(`### ${s.id}`,'',`${s.organization}. ${s.title}. [Source](${link(s.url)}).`,'',`Accessed ${s.accessed_on}. ${s.role} Linked care items: ${ids.join(', ')}.`,'');
  }
  lines.push('## Policy, formulary and data sources','');
  for(const s of policies){
    lines.push(`### ${s.id}`,'',`${s.official_title||s.descriptions[0]||s.url}. [Source](${link(s.url)}).`,'',`Linked records: ${s.linked_record_ids.join(', ')||'Archived source'}. ${s.source_version?`Version/date: ${s.source_version}. `:''}${s.source_access_date?`Recorded source access: ${s.source_access_date}. `:''}${s.verification_status}.`,'');
    if(s.notes)lines.push(`Context and measurement: ${s.notes}`,'');
    if(s.authors||s.report)lines.push(`${[s.authors,s.report].filter(Boolean).join('. ')}.`,'');
  }
  const ris=[];
  const field=(tag,value)=>{if(value!==undefined&&value!==null&&value!=='')ris.push(`${tag}  - ${clean(value)}`);};
  for(const r of records){
    field('TY','JOUR');field('ID',r.id);
    for(const a of r.authors||[])field('AU',a.literal||`${a.family}, ${a.given||a.initials||''}`);
    field('TI',r.title||r.original_citation);field('JO',r.journal);field('JA',r.journal_abbreviation);field('PY',r.year);field('VL',r.volume);field('IS',r.issue);
    const pages=(r.pages||'').split(/[-–]/);field('SP',pages[0]);if(pages.length===2)field('EP',pages[1]);
    field('DO',r.doi);field('AN',r.pmid);field('UR',r.source_url||r.url);field('KW',r.status);field('Y2',r.verified_on);
    field('N1',`Stable ID ${r.id}. ${r.status}. ${r.access_level}. ${r.metadata_status}. ${(r.notes||[]).join(' ')}`);
    if(r.analytic_subject)field('N1',`Analytic subject: ${r.analytic_subject}. Patient sex/gender: ${r.patient_sex_gender_role}. Physician sex/gender: ${r.physician_sex_gender_role}. Comparison: ${r.comparison_axis}. Inference boundary: ${r.inference_boundary}.`);
    if(r.related_record_id)field('N1',`${r.relationship}: ${r.related_record_id}`);
    field('ER',' ');ris.push('');
  }
  for(const s of policies){
    field('TY','ELEC');field('ID',s.id);field('TI',s.official_title||s.descriptions[0]||s.url);field('UR',s.url);field('KW','Policy/data source');field('N1',`Source description from register; not necessarily formal title. Linked records: ${s.linked_record_ids.join(', ')}. ${s.verification_status}. ${s.source_version?`Version: ${s.source_version}.`:''}${s.notes?` ${s.notes}`:''}${s.authors?` Authors: ${s.authors}.`:''}${s.report?` ${s.report}.`:''}`);field('ER',' ');ris.push('');
  }
  for(const s of clinicalGuidance){
    field('TY','ELEC');field('ID',s.id);field('AU',`${s.organization},`);field('TI',s.title);field('UR',s.url);field('KW','Clinical classification guidance');field('Y2',s.accessed_on);field('N1',s.role);field('ER',' ');ris.push('');
  }
  await fs.mkdir(out,{recursive:true});
  await fs.writeFile(`${out}/Medicare_gender_care_bibliography.md`,lines.join('\n'));
  await fs.writeFile(`${out}/Medicare_gender_care_references.ris`,ris.join('\n'));
  await fs.writeFile(`${root}/research/reference_registry.json`,JSON.stringify({updated_on:date,counts,scientific_references:records,policy_sources:policies,clinical_guidance_sources:clinicalGuidance},null,2));
  console.log('Bibliography '+JSON.stringify(counts));
  return counts;
}
