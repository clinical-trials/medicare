import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

// Run with the bundled Node runtime. All spreadsheet authoring uses artifact-tool.
const root = '/Users/lgm/Documents/ChatGPT/Medicare';
const sourceDir = path.join(root, 'research/publication_2026-09-21');
const outputDir = path.join(root, 'outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8');
const previewDir = path.join(outputDir, 'opportunity_workbook_previews');
const outputPath = path.join(outputDir, 'Medicare_health_IT_opportunity_assessment_2026-09-21.xlsx');
await fs.mkdir(previewDir, { recursive: true });
const sourceFiles = ['opportunities.json', 'opportunity_policy_sources.json', 'intervention_evidence.json', 'evidence_roles.json', 'readiness.json'];
const sourceHashes = {};
async function readJson(file) {
  const bytes = await fs.readFile(file);
  sourceHashes[path.relative(root, file)] = crypto.createHash('sha256').update(bytes).digest('hex');
  return JSON.parse(bytes.toString('utf8'));
}
const [opportunities, policies, intervention, roles, readiness] = await Promise.all(sourceFiles.map(n => readJson(path.join(sourceDir, n))));
const metadata = await readJson(path.join(root, 'research/bibliography_metadata.json'));
const methods = await readJson(path.join(root, 'research/methodology_references.json'));
const metadataById = new Map(metadata.records.map(x => [x.id, x]));
if (opportunities.domains.length !== 6 || policies.sources.length !== 16 || intervention.records.length !== 4 || intervention.linked_parent_reports.length !== 1) throw new Error('Unexpected source counts');
if (metadata.records.length !== 53 || methods.records.length !== 11 || roles.records.length !== 38) throw new Error('Unexpected current bibliography/register counts');

const workbook = Workbook.create();
const navy = '#233C50', blue = '#25658B', gray = '#546471', pale = '#EDF3F7', amber = '#FFF2CF';
const linkCells = [];
const sheetSpecs = [];
const nice = s => String(s).replaceAll('_', ' ').replace(/\bPartD\b/g, 'Part D').replace(/\bper1000\b/g, 'per 1,000');
const valueText = x => x == null ? 'Not reported / not established' : Array.isArray(x) ? x.map(valueText).join('\n') : typeof x === 'object' ? Object.entries(x).map(([k,v]) => `${nice(k)}: ${valueText(v)}`).join('\n') : nice(x);
const columnName = n => { let s=''; for(n++;n;n=Math.floor((n-1)/26)) s=String.fromCharCode(65+(n-1)%26)+s; return s; };
function link(sheet, row, column, url, label) {
  if (!/^https?:\/\//.test(url)) throw new Error(`Unexpected link: ${url}`);
  const range = sheet.getCell(row-1, column);
  // Native links are attached after export because artifact-tool cannot evaluate HYPERLINK.
  // The explicitly authorized compatibility pass changes relationships only, not cell content.
  range.values = [[label]];
  range.format.font = { name: 'Arial', size: 11, color: blue, underline: 'single' };
  linkCells.push({ sheet: sheet.name, cell: `${columnName(column)}${row}`, url, label });
}
function wrappedLines(text, width) {
  const capacity = Math.max(8, Math.floor((width - 14) / 6.3));
  return String(text ?? '').split('\n').reduce((total, line) => {
    let lines=1, used=0;
    for(const word of line.split(/\s+/)) { if(used && used+word.length+1>capacity){lines++;used=0;} lines+=Math.max(0, Math.ceil(word.length/capacity)-1); used=(used ? used+1 : 0)+(word.length%capacity || Math.min(word.length,capacity)); }
    return total+lines;
  }, 0);
}
function buildSheet(name, title, subtitle, headers, rows, widths, groups=[]) {
  const s = workbook.worksheets.add(name), last = columnName(headers.length-1), end = rows.length+6;
  s.showGridLines = false; s.tabColor = navy;
  s.getRange(`A1:${last}${end}`).format.font = { name:'Arial', size:11, color:'#24313A' };
  s.getRange(`A1:${last}${end}`).format.verticalAlignment = 'center';
  widths.forEach((w,i)=>s.getRange(`${columnName(i)}1:${columnName(i)}${end}`).format.columnWidthPx=w);
  s.getRange(`A1:${last}1`).format.rowHeightPx=14;
  s.mergeCells(`A2:${last}2`); s.getRange('A2').values=[[title]];
  s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:navy};
  s.getRange(`A2:${last}2`).format.rowHeightPx=32;
  s.mergeCells(`A3:${last}3`);s.getRange('A3').values=[[subtitle]];
  s.getRange('A3').format.font={name:'Arial',size:11,color:gray};s.getRange('A3').format.wrapText=true;
  s.getRange(`A3:${last}3`).format.rowHeightPx=44;
  s.getRange(`A4:${last}4`).format.rowHeightPx=10;
  s.mergeCells(`A5:${last}5`);s.getRange('A5').values=[['As of 21 September 2026  •  Preliminary synthesis and research agenda  •  Filterable tables; no opportunity ranking']];
  s.getRange('A5').format.font={name:'Arial',size:10,color:gray};s.getRange(`A5:${last}5`).format.rowHeightPx=26;
  s.getRange(`A6:${last}${end}`).values=[headers,...rows];
  const table=s.tables.add(`A6:${last}${end}`,true,`T_${name.replaceAll(' ','_')}`); table.showFilterButton=true;
  s.getRange(`A6:${last}${end}`).format.wrapText=true;
  s.getRange(`A7:${last}${end}`).format.fill='#FFFFFF';
  s.getRange(`A6:${last}6`).format={fill:navy,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,horizontalAlignment:'left',verticalAlignment:'center',rowHeightPx:42};
  rows.forEach((row,i)=>{
    const rr=s.getRange(`A${i+7}:${last}${i+7}`);
    const lineCount=Math.max(...row.map((v,j)=>wrappedLines(v,widths[j])));
    rr.format.rowHeightPx=Math.max(31,Math.min(390,lineCount*18+14));
    if(i%2) rr.format.fill='#FAFBFC';
  });
  for(const index of groups){ const rr=s.getRange(`A${index+7}:${last}${index+7}`);rr.format.fill=pale;rr.format.borders={top:{style:'thin',color:'#A9B9C5'}};s.getRange(`A${index+7}:B${index+7}`).format.font={name:'Arial',size:11,bold:true,color:navy}; }
  s.freezePanes.freezeRows(6);s.freezePanes.freezeColumns(1);
  sheetSpecs.push({name,range:`A1:${last}${Math.min(end,12)}`,rows:rows.length,columns:headers.length});
  return s;
}

const short = {
 'O-01': ['Appropriate medication receipt, less financial strain, and disease-specific control.', 'Historical Part D spending is not current unmet need. Confirm a patient-level affordability barrier.', 'Bundled COPD program improved refill adherence; average RTBT effects were null. High-cost fill signals are exploratory.', 'Trial of staffed navigation added to existing tools, with appropriate access, symptoms, harms and actual OOP costs.'],
 'O-02': ['Appropriate post-fracture evaluation, shared treatment decisions, and ultimately fewer fractures.', 'Historical testing differences and low follow-up are signals; clinical eligibility must be assessed independently.', 'Male MA outreach increased BMD testing (10.7% vs 4.9%); 28.3% excluded after randomization. No fracture benefit shown.', 'Multisite trial including both sexes; preserve randomization and follow fractures, function and unnecessary testing.'],
 'O-03': ['Shorter clinically important delays and less patient/staff burden for indicated non-drug care.', 'Policy heterogeneity and qualitative access barriers; current Medicare delay rates remain unverified.', 'No evaluated proposed authorization product in this selected evidence. Final CMS-0057 requirements are implementation context.', 'Controlled rollout with clinically eligible nonrecipients, abandonment, erroneous decisions and time to appropriate care.'],
 'O-04': ['Reliable full-episode valuation research; patient access benefits require a later evaluation.', 'Selected code studies differ: a broad positive comparison, a smaller null study, and opposite RVU/hour direction.', 'No evidence that an audit tool improves patient outcomes. Valuation differences do not measure patient or physician gender effects.', 'Independent comparator adjudication, full-episode work measurement and external replication; direction-neutral conclusions.'],
 'O-05': ['Timely receipt and use of correctly fitted compression items, better function and lower burden.', 'Cost and policy studies predate the 2024 benefit; current Medicare fulfillment gaps require measurement.', 'No verified fulfillment-product effect in this selected evidence. Item coverage does not establish software payment.', 'Current access audit, then controlled fulfillment intervention; include unfilled orders, function, costs and skin injury.'],
 'O-06': ['Better understanding, preference-concordant kidney care, and less practical burden.', 'International clinician interviews suggest barriers; only seven US respondents and no Medicare patient effect.', 'No evaluated coordination product here. Begin with patients and caregivers to verify the problem and preferred solutions.', 'US Medicare interviews and access audit, then co-design and controlled pilot before a definitive trial.']
};
const overviewRows=opportunities.domains.map(d=>[d.id,d.domain,...short[d.id], 'UNVERIFIED\nBuyer, payment and commercial viability']);
const overview=buildSheet('Opportunities','Medicare health IT opportunity assessment','Six unranked research and product hypotheses. Candidate patient benefit comes first; no market-size, profitability or return-on-investment estimates are established.',['ID','Domain','Candidate patient benefit','Evidence of need','Intervention evidence','Next validation','Commercial status'],overviewRows,[65,205,225,240,275,260,140],[0,1,2,3,4,5]);
overview.getRange('G7:G12').format.fill=amber;

const details=[], detailGroups=[];
for(const d of opportunities.domains){
 detailGroups.push(details.length);
 const ids=d.evidence.map(e=>e.study_id).join(', '), pids=d.policy_source_ids.join(', ');
 const add=(field,value,source=ids)=>details.push([d.id,field,typeof value==='number'?value:valueText(value),source]);
 add('Domain',d.domain);add('Problem to verify',d.problem);add('Patient and indication',d.patient_and_indication);add('Clinical basis',d.clinical_basis,'Clinical classification; REVIEW_SCOPE.md');add('Existing inventory links',d.existing_inventory_ids.length?d.existing_inventory_ids.join(', '):'None added; hypothesis only','No new care-item rows');
 add('Proposed intervention',d.proposed_intervention.type);d.proposed_intervention.workflow.forEach((v,i)=>add(`Workflow ${i+1}`,v));add('Novelty / alternatives',d.proposed_intervention.novelty_claim);
 d.patient_benefit_outcomes.forEach((v,i)=>add(`Patient outcome ${i+1}`,v));add('Intended users',d.users);add('Prospective buyers — UNVERIFIED',d.potential_buyers,'Research hypothesis; no buyer validation');
 d.data_and_workflow_needs.forEach((v,i)=>add(`Data / workflow need ${i+1}`,v));add('Current policy boundary',d.policy_boundary,pids);
 add('Business / payment status',d.reimbursement_and_business_model.status,pids);add('Direct Medicare software payment',d.reimbursement_and_business_model.direct_medicare_software_payment,pids);add('Candidate business model — UNVERIFIED',d.reimbursement_and_business_model.candidate_model,'No procurement/payment validation');add('Commercial questions unresolved',d.reimbursement_and_business_model.unvalidated,'No ROI / revenue / TAM calculation');
 for(const[k,v]of Object.entries(d.validation_study))add(`Validation: ${nice(k)}`,v);
 d.alternatives_and_risks.forEach((v,i)=>add(`Alternative / risk ${i+1}`,v));add('Remaining evidence gap',d.evidence_gap);add('Why this is unranked',d.why_not_rank_or_claim_profitability);
}
const detailSheet=buildSheet('Opportunity details','Opportunity specifications','Read each proposed mechanism with its evidence gap, comparator and patient-important outcomes. Buyer names are possible purchasers, not confirmed customers.',['ID','Assessment field','Specification / evidence boundary','Supporting IDs'],details,[70,215,700,205],detailGroups);
details.forEach((r,i)=>{if(/UNVERIFIED|Business \/ payment status/.test(r[1]))detailSheet.getRange(`B${i+7}:C${i+7}`).format.fill=amber;});

const evidenceRows=[], evidenceLinks=[], evidenceGroups=[];
for(const d of opportunities.domains)for(const e of d.evidence){
 evidenceGroups.push(evidenceRows.length);
 evidenceRows.push([d.id,e.study_id,e.role,`${e.title}\n\n${e.summary}\n\nLimit: ${e.limits}`,e.pmid,e.doi||'No DOI verified']);
 evidenceLinks.push({row:evidenceRows.length+6,pmid:e.pmid,url:e.source_url,doi:e.doi});
}
const evidenceSheet=buildSheet('Evidence links','Evidence behind the six domains','Need signals, clinical background, intervention effects and valuation findings have different roles. Repeated study IDs are links across domains, not independent studies.',['Domain','Study ID','Evidence role','Finding and inference boundary','PubMed PMID','DOI'],evidenceRows,[70,80,200,700,110,285],evidenceGroups);
evidenceLinks.forEach(e=>{link(evidenceSheet,e.row,4,e.url,e.pmid);if(e.doi)link(evidenceSheet,e.row,5,`https://doi.org/${e.doi}`,e.doi);});

const outcomeRows=[], outcomeGroups=[];
for(const r of intervention.records){
 outcomeGroups.push(outcomeRows.length);
 for(const o of r.outcomes)outcomeRows.push([r.id,o.outcome,o.n??null,o.estimate,o.ci_low,o.ci_high,nice(o.unit),`${o.interpretation||o.endpoint_type}\n${o.source_locator}${o.n===null?'\nOutcome subgroup N not reported.':''}`]);
}
const parent=intervention.linked_parent_reports[0], pr=parent.abstract_only_results;
outcomeGroups.push(outcomeRows.length);
outcomeRows.push([parent.proposed_id,'Estimated out-of-pocket cost of eligible orders',pr.eligible_orders,pr.adjusted_estimated_OOP_percent_change,pr.CI[0],pr.CI[1],'Adjusted percent change','Parent report; abstract only. Same NCT04940988 as L-T03. Estimated order prices are not realized patient spending.']);
const outcomes=buildSheet('Intervention outcomes','Intervention effects and uncertainty','All intervals are 95% CIs. Values retain the source units; percentage points and percent change differ. Blank outcome N means unavailable in this extraction; study denominators are in Intervention notes.',['Report ID','Outcome','Outcome N','Estimate','CI lower','CI upper','Unit / estimand','Interpretation and source locator'],outcomeRows,[95,280,95,80,80,80,230,445],outcomeGroups);
outcomes.getRange(`C7:C${outcomeRows.length+6}`).setNumberFormat('#,##0');outcomes.getRange(`D7:F${outcomeRows.length+6}`).setNumberFormat('0.0##;-0.0##;0.0');outcomes.getRange(`C7:F${outcomeRows.length+6}`).format.horizontalAlignment='right';

const notes=[], noteGroups=[], noteLinks=[];
function addNote(id,field,value,url=null,label='Source'){
 notes.push([id,field,typeof value==='number'?value:valueText(value),url?label:'']);if(url)noteLinks.push({row:notes.length+6,url,label});
}
for(const r of intervention.records){
 noteGroups.push(notes.length);const m=metadataById.get(r.id);if(!m||String(m.pmid)!==r.pmid)throw new Error(`Missing matched metadata ${r.id}`);
 addNote(r.id,'Title',m.title,r.source_url,'Full text');addNote(r.id,'Authors / publication',`${m.authors.map(a=>`${a.family} ${a.initials||a.given}`).join('; ')}\n${m.journal} (${m.year})`);
 addNote(r.id,'PMID',r.pmid,`https://pubmed.ncbi.nlm.nih.gov/${r.pmid}/`,r.pmid);addNote(r.id,'DOI',m.doi,`https://doi.org/${m.doi}`,m.doi);
 for(const k of ['design','trial_family','data_period','intervention','comparator','software_directness'])addNote(r.id,nice(k),r[k]);
 for(const[k,v]of Object.entries(r.population))addNote(r.id,`Population: ${nice(k)}`,v);
 for(const[k,v]of Object.entries(r.denominators))addNote(r.id,`Denominator: ${nice(k)}`,v);
 for(const o of r.outcomes){const extra=Object.fromEntries(Object.entries(o).filter(([k])=>!['outcome','estimate','ci_level','ci_low','ci_high','unit','interpretation','source_locator','n'].includes(k)));if(Object.keys(extra).length)addNote(r.id,`Outcome detail: ${o.outcome}`,extra);}
 for(const k of ['analysis','sex_analysis','null_or_negative_evidence','implementation','funding','conflicts','sponsor_role','source_discrepancies','source_locators','access_limitations','dependence','identity_status','sex_equity_conclusion','physician_gender_effect','review_status'])if(r[k]!=null)addNote(r.id,nice(k),r[k]);
 for(const[k,v]of Object.entries(r.appraisal))addNote(r.id,`Appraisal note: ${nice(k)}`,v);
 addNote(r.id,'Source URL',r.source_url,r.source_url,'Open source');
}
noteGroups.push(notes.length);
const pm=metadataById.get(parent.proposed_id);if(!pm||String(pm.pmid)!==parent.pmid)throw new Error('Parent metadata mismatch');
addNote(parent.proposed_id,'Title',pm.title,parent.source,'PubMed');addNote(parent.proposed_id,'PMID',parent.pmid,parent.source,parent.pmid);addNote(parent.proposed_id,'DOI',pm.doi,`https://doi.org/${pm.doi}`,pm.doi);addNote(parent.proposed_id,'Authors / publication',`${pm.authors.map(a=>`${a.family} ${a.initials||a.given}`).join('; ')}\n${pm.journal} (${pm.year})`);
for(const k of ['trial_id','linked_report_id','independent_trial','access','summary','abstract_only_results','inference_limit'])addNote(parent.proposed_id,nice(k),parent[k]);
const noteSheet=buildSheet('Intervention notes','Intervention reports: design and applicability','Four detailed reports plus one linked parent report. Appraisal notes are provisional AI extraction, not final human risk-of-bias judgments or GRADE ratings.',['Report ID','Field','Extracted information / limitation','Source link'],notes,[95,255,760,180],noteGroups);
noteLinks.forEach(x=>link(noteSheet,x.row,3,x.url,x.label));

const policyRows=[], policyGroups=[], policyLinks=[];
for(const p of policies.sources){
 policyGroups.push(policyRows.length);
 const add=(field,value,linked=false)=>{policyRows.push([p.id,field,valueText(value),linked?'Official source':'']);if(linked)policyLinks.push({row:policyRows.length+6,url:p.url});};
 add('Policy / guidance source',p.title,true);add('Status',p.status);add('Issuer and date',`${p.organization}\nDocument date: ${p.document_date||'Not separately dated'}${p.effective_date?`\nEffective: ${p.effective_date}`:''}${p.page_last_modified?`\nPage modified: ${p.page_last_modified}`:''}`);
 p.verified_facts.forEach((v,i)=>add(`Verified provision ${i+1}`,v));add('Boundary / limitation',p.limits);add('Source locator',p.locator);add('Access / currency',`Checked ${p.retrieved_on}. ${p.access_level}`);add('Source URL',p.url,true);
}
const policySheet=buildSheet('Policy sources','Current policy and implementation context','Sixteen official sources. Final rules, proposed rules and clinical guidance retain their status. Coverage of a clinical service or item does not establish payment for a software product.',['Policy ID','Field','Verified content / boundary','Source link'],policyRows,[90,230,810,145],policyGroups);
policyLinks.forEach(x=>link(policySheet,x.row,3,x.url,'Official source'));
policyRows.forEach((r,i)=>{if(r[0]==='P-048'&&r[1]==='Status')policySheet.getRange(`B${i+7}:C${i+7}`).format.fill=amber;});

const readyRows=[], readyGroups=[];
function rr(section,field,value,source){readyRows.push([section,field,typeof value==='number'?value:valueText(value),source]);}
readyGroups.push(readyRows.length);
rr('Status','Current designation','Preliminary synthesis and research agenda; completed systematic review is the target.','readiness.json');
rr('Status','Assessment method','Project-specific structured assessment; no validated opportunity score, economic evaluation or market study.','readiness.json / opportunities.json');
rr('Status','Scope','Current REVIEW_SCOPE remains active. Gender identity is unresolved where unreported; recorded sex is not proof of cisgender identity.','REVIEW_SCOPE.md');
rr('Status','Patient / clinician distinction','Patient sex, physician gender and service/anatomy valuation are separate analytic streams.','evidence_roles.json');
readyGroups.push(readyRows.length);
const counts=[['Unranked opportunity domains',6,'opportunities.json'],['Official policy sources',16,'opportunity_policy_sources.json'],['Detailed intervention reports',4,'intervention_evidence.json'],['Additional linked parent report',1,'intervention_evidence.json; not independent of L-T03'],['Scientific metadata records',metadata.records.length,'bibliography_metadata.json; includes context/corrections, not an included-study count'],['Methodology references',methods.records.length,'methodology_references.json; separate from science count'],['Active register records',roles.records.length,'evidence_roles.json; not final included studies'],['Combined development-search PMIDs',readiness.current_counts.combined_unique_pmids,'readiness.json; screening target, not eligible studies'],['Human-screened records',readiness.current_counts.human_screened_records,'readiness.json'],['Calibration records prepared',readiness.current_counts.prepared_calibration_records,'readiness.json; preparation is not human screening']];
for(const[label,value,source]of counts)rr('Counts',label,value,source);
if(readiness.current_counts.scientific_metadata_records!==metadata.records.length)rr('Counts','Source snapshot reconciliation',`readiness.json retains ${readiness.current_counts.scientific_metadata_records} scientific metadata records at its audit. Current metadata verifies ${metadata.records.length}; the canonical source files were not changed by this builder.`,'Current bibliography count supersedes earlier snapshot for this workbook');
readyGroups.push(readyRows.length);
for(const[key,value]of Object.entries(readiness.completed_review_claims))rr('Review conduct',nice(key),value?'Completed':'Not completed / not performed','readiness.json');
for(const b of readiness.blockers){readyGroups.push(readyRows.length);rr(b.id,b.component,nice(b.status),b.evidence_file);rr(b.id,'Required work',b.required_action,b.evidence_file);rr(b.id,'Human role',b.human_role,'Independent review remains required');rr(b.id,'Evidence of completion',b.completion_evidence,'Acceptance criterion, not current achievement');}
readyGroups.push(readyRows.length);
for(const[key,count]of Object.entries(roles.role_counts))rr('Roles',nice(key),count,roles.role_definitions[key]);
readyGroups.push(readyRows.length);
for(const[g,i]of opportunities.common_validation_gates.map((g,i)=>[g,i]))rr('Validation',`Common gate ${i+1}`,g,'opportunities.json');
for(const s of sourceFiles)rr('Provenance',s,path.join('research/publication_2026-09-21',s),'Source JSON; no canonical edits');
const readySheet=buildSheet('Readiness','Review readiness and provenance','Counts describe different units. The 38 active records and 59,147 search PMIDs are not included-study counts. Scientific metadata and methodological references are tracked separately.',['Group','Metric / requirement','Value / action','Evidence or interpretation'],readyRows,[100,275,680,360],readyGroups);
readyRows.forEach((r,i)=>{if(typeof r[2]==='number'){readySheet.getRange(`C${i+7}`).setNumberFormat('#,##0');readySheet.getRange(`C${i+7}`).format.font={name:'Arial',size:12,bold:true,color:navy};}});

workbook.recalculate();
let inspections='';
for(const spec of sheetSpecs){const result=await workbook.inspect({kind:'table',range:`'${spec.name}'!A6:${columnName(spec.columns-1)}${Math.min(spec.rows+6,9)}`,include:'values,formulas',tableMaxRows:4,tableMaxCols:spec.columns,maxChars:6500});inspections+=result.ndjson+'\n';}
const errors=await workbook.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'Formula errors across opportunity workbook'});inspections+=errors.ndjson+'\n';
await fs.writeFile(path.join(previewDir,'inspection.ndjson'),inspections);
const previews=[];
for(const spec of sheetSpecs){
 const filename=spec.name.toLowerCase().replaceAll(' ','_')+'.png';
 // Preview the whole overview; representative top ranges on the detailed sheets.
 const range=spec.name==='Opportunities'?'A1:G12':spec.name==='Intervention outcomes'?'A1:H13':spec.name==='Readiness'?'A1:D20':spec.range;
 const rendered=await workbook.render({sheetName:spec.name,range,scale:1,format:'png'});
 const previewPath=path.join(previewDir,filename);await fs.writeFile(previewPath,new Uint8Array(await rendered.arrayBuffer()));previews.push(previewPath);
}
const xlsx=await SpreadsheetFile.exportXlsx(workbook);await xlsx.save(outputPath);
const linkManifest=path.join(previewDir,'native_links.json');await fs.writeFile(linkManifest,JSON.stringify(linkCells,null,2)+'\n');
const linkResult=execFileSync('/Users/lgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',[path.join(sourceDir,'add_opportunity_native_links.py'),outputPath,linkManifest],{encoding:'utf8'});console.log(linkResult.trim());
for(const[file,hash]of Object.entries(sourceHashes)){const current=crypto.createHash('sha256').update(await fs.readFile(path.join(root,file))).digest('hex');if(hash!==current)throw new Error(`Source changed during build: ${file}`);}
const verification={built_on:'2026-09-21',output:outputPath,authoring:'@oai/artifact-tool; native OOXML hyperlink relationships added by explicitly authorized compatibility helper',source_sha256:sourceHashes,counts:{domains:6,policies:16,detailed_intervention_reports:4,linked_parent_reports:1,intervention_outcome_rows:outcomeRows.length,scientific_metadata:metadata.records.length,methodology_references:methods.records.length,active_register:roles.records.length,search_pmids:readiness.current_counts.combined_unique_pmids,human_screened:readiness.current_counts.human_screened_records},sheets:sheetSpecs,native_hyperlink_count:linkCells.length,hyperlink_formula_count:0,hyperlinks:linkCells,previews,formula_error_inspection:errors.ndjson};
await fs.writeFile(path.join(previewDir,'verification.json'),JSON.stringify(verification,null,2)+'\n');
console.log(JSON.stringify({output:outputPath,sheets:sheetSpecs,counts:verification.counts,hyperlinks:linkCells.length,previews},null,2));
