import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {SpreadsheetFile, FileBlob} from '@oai/artifact-tool';
import {applyReviewScope} from './scoped_data.mjs';
import {buildBibliography} from './bibliography.mjs';
import {writeAnalysisFramework} from './analysis_framework.mjs';
process.on('uncaughtException',e=>{console.error(e.message);process.exit(1);});
const root='/Users/lgm/Documents/ChatGPT/Medicare';
const support=`${root}/research/workbook`;
const path=`${root}/outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_gender_care_evidence_register_2026-09-16.xlsx`;
const datasets=await Promise.all(['drugs','procedures','gender_screening','additional'].map(async n=>JSON.parse(await fs.readFile(`${root}/research/literature_${n}.json`,'utf8'))));
const [drugs,procedures,gender,additional]=datasets;
const benchmark=JSON.parse(await fs.readFile(`${root}/research/medicare_benchmark.json`,'utf8'));
const {scope,clinicalBasis,evidenceSubjects,items,studies,excludedItems,excludedStudies}=await applyReviewScope(datasets.flatMap(x=>x.items),[...procedures.studies,...drugs.studies,...gender.studies,...additional.studies]);
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const care=wb.worksheets.getItem('Data & Targets'),lit=wb.worksheets.getItem('Literature'),dash=wb.worksheets.getItem('Dashboard'),helper=wb.worksheets.getItem('_Chart Helpers');
const navy='#102332',panel='#19354D',ink='#243B50',pale='#EDF4F8';
const reviewed=new Date('2026-09-16T12:00:00Z');
const put=(s,c,v)=>s.getRange(c).values=[[v]];
const form=(s,c,v)=>s.getRange(c).formulas=[[v]];
const box=(s,r,text,fill=navy,color='#FFFFFF',size=11)=>{s.getRange(r).unmerge();s.getRange(r).merge();s.getRange(r).values=[[text]];s.getRange(r).format={fill,font:{name:'Aptos',size,color,bold:true},wrapText:true,verticalAlignment:'center'};};
function replaceTable(s,name,range,headers,rows,clearRange){
  const t=s.tables.items.find(x=>x.name===name);if(t)t.delete();
  s.getRange(clearRange).clear({applyTo:'contents'});
  s.getRange(range).values=[headers,...rows];
  const nt=s.tables.add(range,true,name);nt.style='TableStyleMedium2';nt.showFilterButton=true;
  return nt;
}
const statusColors={'Covered with conditions':'#DFF0E9','Plan dependent':'#E4EFFB','Excluded for this use':'#F9E1DB','Local decision':'#FFF0D0','Not established':'#E9E9EF'};
const statuses=Object.keys(statusColors);
const policyExtras={D05:drugs.supplemental_policy_sources[3].url,D09:drugs.supplemental_policy_sources[0].url,D10:drugs.supplemental_policy_sources[1].url,D11:drugs.supplemental_policy_sources[2].url,D12:drugs.supplemental_policy_sources[5].url};
// Preserve notes by stable item ID when rows move.
const oldCareRows=care.getRange('A9:T70').values;
const notes=new Map(oldCareRows.filter(r=>r[0]).map(r=>[r[0],r[19]||'']));
const careHeaders=[...care.getRange('A8:T8').values[0],'Clinical basis','Sex / eligibility distinction','Analysis approach','Classification rationale'];
const careRows=items.map(x=>[x.id,x.item,x.status,x.medicare_part,x.indication,x.population,x.domain,x.policy_scope,x.policy_summary,x.comparison,x.disparity_evidence,x.evidence_type,x.limitations,x.next_question,x.study_ids.join(', '),reviewed,'',x.policy_url,x.policy_url2||policyExtras[x.id]||'',notes.get(x.id)||'',x.clinical_basis,x.sex_specific_feature,x.analysis_approach,[x.classification_notes,x.classification_source_ids.length?`Clinical guidance: ${x.classification_source_ids.join(', ')} (bibliography).`:''].filter(Boolean).join(' ')]);
const careEnd=8+items.length;
replaceTable(care,'CareInventory',`A8:X${careEnd}`,careHeaders,careRows,'A8:X70');
care.getRange(`U8:X${careEnd}`).format={font:{name:'Aptos',size:11,color:ink,bold:false},wrapText:true,verticalAlignment:'top'};
[['U',235],['V',320],['W',360],['X',400]].forEach(([c,w])=>care.getRange(`${c}:${c}`).format.columnWidthPx=w);
care.getRange('U8:X8').format={fill:panel,font:{name:'Aptos',size:11,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center'};
care.getRange(`P9:P${careEnd}`).setNumberFormat('mm/dd/yy');
for(let r=9;r<=careEnd;r++){
  care.getRange(`A${r}:X${r}`).format.fill=r%2===0?'#F2F6F9':'#FFFFFF';
  care.getRange(`C${r}`).format.fill=statusColors[careRows[r-9][2]];
}
care.getRange(`T9:T${careEnd}`).format.fill='#FFF4D6';care.getRange(`Q8:Q${careEnd}`).format.fill='#FFFFFF';care.getRange(`Q8:Q${careEnd}`).setNumberFormat(';;;');
box(care,'A3:F4','Current scope: care for cisgender men and women. Transgender-focused evidence and gender-affirming care are excluded from synthesis. See Exclusions and Literature for the population-screening rules.',pale,ink);
box(care,'U3:X4','Classify the item and indication: shared systems, reproductive anatomy, reproductive physiology, or mixed/site-dependent care. Sex-defined eligibility is recorded separately.',pale,ink);
box(care,'U5:X6','Filter Clinical basis to review each group. Counts describe selected inventory rows. Clinical guidance IDs resolve in the bibliography; classifications do not change coverage findings.',pale,ink);

const codeStudies=new Set(['L-P01','L-P02','L-P05','L-P06','L-P08','L-A02']);
const litHeaders=[...lit.getRange('A8:O8').values[0],'Population-screening status','Sex / gender reporting','Screening notes','Analytic subject','Unit of analysis','Patient sex/gender role','Physician sex/gender role','Comparison axis','Inference boundary'];
const previousStudyNotes=new Map(lit.getRange('A9:R70').values.filter(r=>r[0]).map(r=>[r[0],r[17]||'']));
const litRows=studies.map(x=>[x.id,x.citation,x.year,x.design,x.population,x.payer,x.data_period,x.finding,x.limitation,x.relevance,items.filter(a=>a.study_ids.includes(x.id)).map(a=>a.id).join(', '),x.extraction_level||'Citation and abstract; full-text extraction not completed','',x.url,x.doi_or_pmid,x.population_screening_status||(codeStudies.has(x.id)?'Policy/code-level component retained':'Candidate: population verification pending'),x.identity_reporting||(codeStudies.has(x.id)?'Code/insurer evidence does not establish patient gender identity. Assess any patient-level component separately.':'Male/female or men/women reported. Cisgender identity and absence of transgender participants are not established by the current extraction.'),previousStudyNotes.get(x.id)||x.screening_notes||'',x.analytic_subject,x.unit_of_analysis,x.patient_sex_gender_role,x.physician_sex_gender_role,x.comparison_axis,x.inference_boundary]);
const litEnd=8+studies.length;
lit.getRange('A35:X110').unmerge();
replaceTable(lit,'ScientificLiterature',`A8:X${litEnd}`,litHeaders,litRows,'A8:X110');
// Remove old section fills when the methods block moves down with new records.
lit.getRange(`A${litEnd+1}:X110`).format.fill='#FFFFFF';
lit.getRange(`A8:X${litEnd}`).format={font:{name:'Aptos',size:11,color:ink,bold:false},wrapText:true,verticalAlignment:'top'};
lit.getRange(`A9:X${litEnd}`).format.rowHeightPx=156;
lit.getRange('A8:X8').format={fill:panel,font:{name:'Aptos',size:11,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center',rowHeightPx:48};
for(let r=9;r<=litEnd;r++)lit.getRange(`A${r}:X${r}`).format.fill=r%2===0?'#F2F6F9':'#FFFFFF';
lit.getRange(`C9:C${litEnd}`).setNumberFormat('0');
lit.getRange(`M8:M${litEnd}`).format.fill='#FFFFFF';lit.getRange(`M8:M${litEnd}`).setNumberFormat(';;;');lit.getRange('M8').format.font={name:'Aptos',size:11,color:'#FFFFFF'};
lit.getRange(`N9:N${litEnd}`).format.font={name:'Aptos',size:10,color:'#176CA4'};
lit.getRange('P:P').format.columnWidthPx=275;lit.getRange('Q:Q').format.columnWidthPx=330;lit.getRange('R:R').format.columnWidthPx=320;
lit.getRange(`P9:P${litEnd}`).format.fill='#EDF2FA';lit.getRange(`R9:R${litEnd}`).format.fill='#FFF4D6';
[['S',245],['T',285],['U',340],['V',340],['W',340],['X',400]].forEach(([c,w])=>lit.getRange(`${c}:${c}`).format.columnWidthPx=w);
box(lit,'S3:X4','Whose sex/gender is analyzed? Patient care, service/anatomy valuation, physician gender and general background are distinct. Filter Analytic subject; read both variable roles and the comparison axis.',pale,ink);
box(lit,'S5:X6','Physician payment evidence is a separate contextual stream. A single-sex clinical population, procedure anatomy, or clinician interview does not establish a between-sex patient or physician effect.',pale,ink);
box(lit,'A3:F4','National review of coverage, payment values, patient costs and access across prescriptions, procedures and shared conditions. Estradiol is one motivating case. Target population: cisgender women and men.',pale,ink);
box(lit,'A5:F6','Population scope amended September 16, 2026. Most summaries remain abstract-based. Excluded records are logged separately. This is not yet a completed systematic review.',pale,ink);
const methodRows=[
 ['National question',scope.national_review_question],
 ['Medicare benchmark',benchmark.rationale],
 ['Age and entitlement',benchmark.age_rule],
 ['Measures and inference',benchmark.measurement_rule],
 ['Age in sex comparisons',benchmark.comparison_rule],
 ['Motivating example',scope.motivating_example_rule],
 ['Structural effects','Examine explicit differences and unequal effects of the same rules. Distinguish coverage, payment valuation, patient spending and realized access. Utilization and service mix may be mechanisms as well as confounders.'],
 ['Population scope','Care for cisgender men and women. Exclude transgender-focused patient evidence and gender-affirming-care indications from the current review and future white paper.'],
 ['Mixed populations','Include only separately extractable eligible cisgender male/female results. Exclude nonseparable mixed results from primary synthesis and record the reason.'],
 ['Identity not reported','Male/female categories do not establish cisgender status. Retain such papers as candidates, record identity as not reported, and resolve eligibility during full-text screening. Do not claim zero transgender participants.'],
 ['Nonpatient evidence','Fee schedules, formularies and benefit policies have no patient cohort. Retain relevant included indications, without implying a cisgender-only patient-level estimate.'],
 ['Analytic subject',scope.analysis_subject_rule],
 ['Clinician context',scope.physician_evidence_rule],
 ['Joint sex/gender analysis',scope.interaction_evidence_rule],
 ['Contextual evidence','General reviews support the clinical framework and citation following. Qualitative clinician interviews can identify perceived patient-access barriers, without estimating Medicare disparities. Label these roles separately; cited studies require independent screening.'],
 ['Scope amendment','Adopted September 16, 2026 after the initial broad search. This is a documented amendment, not a prospectively registered criterion. Research-scope exclusion is distinct from Medicare noncoverage.'],
 ['Search status','Initial targeted searches and citation following completed September 16, 2026. Subsequent searches should apply the amended population criterion. This register is not a complete screened-record inventory.'],
 ['Eligible topic searches',scope.topic_scope],
 ['Policy levels',scope.policy_level_rule],
 ['Source hierarchy','Coverage uses federal benefit rules, CMS/Medicare guidance, named contractor policy and identified formularies. Scientific studies inform effects and disparity hypotheses, not automatic coverage decisions.'],
 ['Study extraction','Record citation, design, population, payer, period, finding and limitations. Source-access details distinguish abstracts from targeted full-text review. Formal risk-of-bias assessment and comprehensive screening remain outstanding.'],
 ['Coverage status','Covered with conditions indicates verified benefit or broad listing. Plan dependent and Local decision require further review. Excluded for this use is indication-specific. Not established means unresolved, not denied.'],
 ['Comparison strategy',scope.comparison_rule],
 ['Clinical basis',scope.clinical_basis_rule],
 ['Anatomy comparisons',scope.anatomy_analysis_rule],
 ['Bias assessment','Assess clinical need, benefit, time, complexity, setting and alternatives. Distinguish observed disparities, unmet need and evidence of structural inequity. Prespecify adjustment choices; retain null and contradictory results.'],
 ['White paper','State the amended population scope and actual measurement of sex/gender. Do not relabel sex-coded cohorts as confirmed cisgender. Findings do not address the excluded population.'],
 ['Bibliography','Use stable [L-ID] citations in drafts. The companion bibliography and RIS export refresh with this register. Metadata verification, full-text extraction, eligibility and risk-of-bias review are separate. Linked corrections are not independent studies.'],
 ['Expansion','Use stable item and study IDs. Record population eligibility and exclusions. Add new source URLs and policy-check dates. Current counts describe selected working records, not a systematic-search flow diagram.'],
 ['Abbreviations','CMS: Centers for Medicare & Medicaid Services. MAC: Medicare Administrative Contractor. MA: Medicare Advantage. NCD: national coverage determination. RVU: relative value unit. PA: prior authorization. ST: step therapy.']
];
let mr=litEnd+3;
box(lit,`A${mr}:F${mr}`,'Review method and population eligibility',panel);lit.getRange(`A${mr}:F${mr}`).format.rowHeightPx=30;
for(const [label,txt] of methodRows){mr++;box(lit,`A${mr}:B${mr}`,label,pale,ink);box(lit,`D${mr}:J${mr}`,txt,'#FFFFFF',ink);lit.getRange(`A${mr}:J${mr}`).format.rowHeightPx=68;}
mr+=3;box(lit,`A${mr}:F${mr}`,'Additional primary policy and label sources',panel);lit.getRange(`A${mr}:F${mr}`).format.rowHeightPx=30;
for(const s of [...drugs.supplemental_policy_sources,...benchmark.sources.map(s=>({topic:`Benchmark context: ${s.title} (${s.data_period})`,url:s.url}))]){mr++;box(lit,`A${mr}:F${mr}`,s.topic,pale,ink);box(lit,`H${mr}:J${mr}`,s.url,'#FFFFFF','#176CA4',10);lit.getRange(`A${mr}:J${mr}`).format.rowHeightPx=55;}

const exclusion=wb.worksheets.add('Exclusions');exclusion.showGridLines=false;exclusion.tabColor='#8B728F';
exclusion.getRange('A1:H30').format={font:{name:'Aptos',size:11,color:ink},wrapText:true,verticalAlignment:'top',fill:'#FFFFFF'};
[95,115,350,260,370,310,110,350].forEach((width,i)=>exclusion.getRange(`${String.fromCharCode(65+i)}:${String.fromCharCode(65+i)}`).format.columnWidthPx=width);
box(exclusion,'A1:F2','Population-scope exclusions',navy,'#FFFFFF',22);
box(exclusion,'A3:F4','These records are outside the current population scope. Their removal is not a finding about study quality, treatment value or Medicare coverage. Original extractions are retained in the research archive.',pale,ink);
box(exclusion,'A5:F6','For mixed cohorts, retain only separately extractable eligible results. Studies reporting sex but not gender identity require full-text screening. Counts below describe this scope amendment only.',pale,ink);
const excludedRows=[...excludedItems.map(x=>[x.id,'Care item',x.item,'Outside active care inventory',x.id==='G03'?'Current sex-marker comparison is linked to transgender-focused evidence; no separate eligible comparison extracted.':'Gender-affirming-care indication or transgender-focused population.',x.id==='G03'?'Combined transgender/intersex row removed in its present form. Intersex status alone is not a population exclusion.':'Keep source record for audit; exclude from current synthesis.',reviewed,x.policy_url]),...excludedStudies.map(x=>[x.id,'Study',x.citation,'Outside current synthesis','Extracted population, comparison or care indication focuses on transgender or gender-diverse patients.','No eligible standalone cisgender subgroup result has been extracted for this review. Preserve citation and scope reason.',reviewed,x.url])];
replaceTable(exclusion,'ScopeExclusions',`A8:H${8+excludedRows.length}`,['Record ID','Record type','Item / citation','Decision','Exclusion reason','Interpretation / subgroup note','Decision date','Source URL'],excludedRows,'A8:H30');
exclusion.getRange('A8:H8').format={fill:panel,font:{name:'Aptos',size:11,bold:true,color:'#FFFFFF'},rowHeightPx:48,verticalAlignment:'center'};
exclusion.getRange(`A9:H${8+excludedRows.length}`).format.rowHeightPx=145;
exclusion.getRange(`G9:G${8+excludedRows.length}`).setNumberFormat('mm/dd/yy');exclusion.getRange(`H9:H${8+excludedRows.length}`).format.font={name:'Aptos',size:10,color:'#176CA4'};
for(let r=9;r<=8+excludedRows.length;r++)exclusion.getRange(`A${r}:H${r}`).format.fill=r%2===0?'#F2F6F9':'#FFFFFF';
exclusion.freezePanes.freezeRows(8);exclusion.freezePanes.freezeColumns(2);

put(dash,'B2','Medicare care for men and women');put(dash,'B3','Medicare as a benchmark for equitable care in later life');put(dash,'B4','Cisgender women and men. Anatomy, physiology and eligibility are distinguished below.');
put(dash,'F5','SCIENTIFIC RECORDS');
const contextCount=studies.filter(x=>x.synthesis_role==='context_only').length;
put(dash,'F8',`${studies.length-contextCount} primary candidates + ${contextCount} context record${contextCount===1?'':'s'}`);
// Clear obsolete formulas beneath the imported merged explanatory cells.
dash.getRange('B44:I52').unmerge();
dash.getRange('B44:I52').values=Array.from({length:9},()=>Array(8).fill(''));
const explanations=[['Coverage','An eligible benefit may still require medical necessity or authorization.'],['Payment','RVU or fee differences require clinically comparable procedures.'],['Access','Low use or high cost does not independently prove denial or bias.'],['Uncertainty','Unresolved coverage is recorded explicitly for further review.']];
for(let i=0;i<explanations.length;i++){const row=45+i*2;box(dash,`B${row}:C${row+1}`,explanations[i][0],'#152D42','#FFFFFF');box(dash,`D${row}:I${row+1}`,explanations[i][1],'#152D42','#C1D1DD');}
box(dash,'J45:Q49','Medicare benchmark: assess sex-based equity in later-life care, when chronic illness and per-person healthcare use are substantial. Keep spending, utilization and unmet need distinct. Retain younger beneficiaries separately by age and entitlement. See Literature for the rationale and sources.','#152D42','#C1D1DD',12);
box(dash,'J51:Q52',`${excludedStudies.length} studies and ${excludedItems.length} care items moved to Exclusions. See Literature for amended methods.`,panel,'#C1D1DD');
// Rebind the existing named-table summaries after shrinking the tables.
statuses.forEach((s,i)=>form(helper,`B${i+2}`,`=COUNTIF(CareInventory[Coverage status],A${i+2})`));
form(helper,'N2','=COUNTA(CareInventory[Item ID])');form(helper,'N3','=COUNTA(ScientificLiterature[Study ID])');form(helper,'N4','=COUNTA(CareInventory[Item ID])-COUNTBLANK(CareInventory[Study IDs])');form(helper,'N5','=COUNTBLANK(CareInventory[Study IDs])');form(helper,'N6','=B5+B6');
put(helper,'M3','Scientific records');
// Anatomy/physiology counts are computed once here and linked into the dashboard.
const basisGroups=clinicalBasis.groups;
helper.getRange('V1:AB8').values=[['Clinical basis',...statuses,'Total'],...basisGroups.map(g=>[g.label,...Array(6).fill(null)]),['Total',...Array(6).fill(null)]];
helper.getRange('V:V').format.columnWidthPx=290;
helper.getRange('W:AB').format.columnWidthPx=165;
helper.getRange('V1:AB8').format={font:{name:'Aptos',size:11,color:ink},wrapText:true,verticalAlignment:'center',rowHeightPx:50};
helper.getRange('V1:AB1').format={fill:panel,font:{name:'Aptos',size:11,color:'#FFFFFF',bold:true},rowHeightPx:65};
const basisCols=['W','X','Y','Z','AA'];
for(let i=0;i<basisGroups.length;i++){
  const r=i+2;
  basisCols.forEach(c=>form(helper,`${c}${r}`,`=COUNTIFS(CareInventory[Clinical basis],$V${r},CareInventory[Coverage status],${c}$1)`));
  form(helper,`AB${r}`,`=SUM(W${r}:AA${r})`);
}
for(const c of [...basisCols,'AB'])form(helper,`${c}8`,`=SUM(${c}2:${c}7)`);
helper.getRange('W2:AB8').setNumberFormat('0');
dash.getRange('B54:Q75').unmerge();dash.getRange('B54:Q75').clear({applyTo:'contents'});
dash.getRange('B54:Q75').format={fill:navy,font:{name:'Aptos',size:12,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center'};
box(dash,'B54:Q54','COVERAGE BY ANATOMY AND REPRODUCTIVE PHYSIOLOGY',panel,'#FFFFFF',14);
dash.getRange('B54:Q54').format.rowHeightPx=36;
box(dash,'B55:Q56','Each care-item/indication is counted once. These are selected inventory counts, not national coverage rates or estimates of bias. Sex-specific eligibility and disease burden remain separate.',navy,'#C1D1DD',11);
box(dash,'B57:F57','Clinical basis',panel,'#FFFFFF',12);
const spans=[['G','H','W'],['I','J','X'],['K','L','Y'],['M','N','Z'],['O','P','AA'],['Q','Q','AB']];
spans.forEach(([a,b],j)=>box(dash,`${a}57:${b}57`,j<5?statuses[j]:'Total',panel,'#FFFFFF',11));
dash.getRange('B57:Q57').format.rowHeightPx=62;
for(let i=0;i<7;i++){
  const r=58+i,hr=i+2,fill=i===6?panel:(i%2?'#152D42':navy);
  box(dash,`B${r}:F${r}`,i===6?'Total inventory':basisGroups[i].label,fill,'#FFFFFF',12);
  spans.forEach(([a,b,c])=>{box(dash,`${a}${r}:${b}${r}`,'',fill,'#FFFFFF',15);form(dash,`${a}${r}`,`='_Chart Helpers'!${c}${hr}`);dash.getRange(`${a}${r}:${b}${r}`).format.horizontalAlignment='center';});
  dash.getRange(`B${r}:Q${r}`).format.rowHeightPx=45;
}
box(dash,'B66:I69','Shared systems: compare clinical need and access, including unmet care. Breast, bone and pelvic-floor care remain shared even when eligibility is sex-specific. Clinical need is assessed independently of reimbursement rules.',panel,'#C1D1DD',12);
box(dash,'J66:Q69','Reproductive anatomy and physiology: assess clinical need, benefit and policy consistency. A male/female counterpart is not required; cross-procedure matches must account for purpose and resources.',panel,'#C1D1DD',12);
box(dash,'B71:Q73','Mixed or site-dependent rows require component review. Endometriosis surgery depends on lesion site; the broad prolapse row remains provisional until the anatomy and repair codes are verified. See Data & Targets, columns U–X, for every classification.',panel,'#C1D1DD',12);
// Study subjects are independent of anatomy and synthesis eligibility.
const subjectGroups=evidenceSubjects.groups;
helper.getRange('AD1:AE6').values=[['Analytic subject','Records'],...subjectGroups.map(g=>[g.label,null]),['Total',null]];
subjectGroups.forEach((g,i)=>form(helper,`AE${i+2}`,`=COUNTIF(ScientificLiterature[Analytic subject],AD${i+2})`));
form(helper,'AE6','=SUM(AE2:AE5)');
helper.getRange('AD:AD').format.columnWidthPx=310;helper.getRange('AE:AE').format.columnWidthPx=100;
helper.getRange('AD1:AE6').format={font:{name:'Aptos',size:11,color:ink},wrapText:true,rowHeightPx:50};
helper.getRange('AD1:AE1').format.fill=pale;helper.getRange('AE2:AE6').setNumberFormat('0');
dash.getRange('B77:Q94').unmerge();dash.getRange('B77:Q94').clear({applyTo:'contents'});
dash.getRange('B77:Q94').format={fill:navy,font:{name:'Aptos',size:12,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center',rowHeightPx:25};
box(dash,'B77:Q77','PATIENT SEX/GENDER AND PHYSICIAN SEX/GENDER',panel,'#FFFFFF',14);
dash.getRange('B77:Q77').format.rowHeightPx=36;
box(dash,'B78:Q79','Selected literature records, classified by the question studied. Counts include clinical and contextual evidence; they are not counts of demonstrated disparities.',navy,'#C1D1DD',11);
for(let i=0;i<subjectGroups.length;i++){
  const g=subjectGroups[i],r=80+i*2,fill=i%2?panel:'#152D42';
  box(dash,`B${r}:F${r+1}`,g.label,fill,'#FFFFFF',12);
  box(dash,`G${r}:H${r+1}`,'',fill,'#FFFFFF',20);form(dash,`G${r}`,`='_Chart Helpers'!AE${i+2}`);
  dash.getRange(`G${r}:H${r+1}`).format.horizontalAlignment='center';
  box(dash,`I${r}:Q${r+1}`,g.description,fill,'#C1D1DD',11);
}
box(dash,'B89:I92','Patient effects: distinguish direct sex comparisons from care within one population, clinical background and perceived barriers. Anatomy-based valuations are a separate comparison.',panel,'#C1D1DD',12);
box(dash,'J89:Q92','Physician effects: compare payments by physician sex/gender. Annual receipts, per-service payments and salary are distinct. Patient effects cannot be inferred from physician effects.',panel,'#C1D1DD',12);
box(dash,'B93:Q94','If both variables are analyzed, record each main effect and any interaction separately. Literature columns S–X retain the unit, variable roles, comparison and inference boundary.',navy,'#C1D1DD',11);
// Verify the new subject counts update when an input changes, then restore.
const firstSubject=studies[0].analytic_subject,fromSubject=subjectGroups.findIndex(g=>g.label===firstSubject)+2;
const targetSubject=subjectGroups.findIndex(g=>g.id==='physician_gender')+2;
const fromCount=helper.getRange(`AE${fromSubject}`).values[0][0],targetCount=helper.getRange(`AE${targetSubject}`).values[0][0];
put(lit,'S9',subjectGroups.find(g=>g.id==='physician_gender').label);
assert.equal(helper.getRange(`AE${fromSubject}`).values[0][0],fromCount-1);
assert.equal(helper.getRange(`AE${targetSubject}`).values[0][0],targetCount+1);
assert.equal(dash.getRange(`G${80+(targetSubject-2)*2}`).values[0][0],targetCount+1);
put(lit,'S9',firstSubject);
// Verify that classification edits propagate through both dimensions, then restore.
const firstGroup=items[0].clinical_basis,firstIdx=basisGroups.findIndex(g=>g.label===firstGroup)+2;
const sharedIdx=basisGroups.findIndex(g=>g.id==='shared')+2;
const beforeFrom=helper.getRange(`AB${firstIdx}`).values[0][0],beforeShared=helper.getRange(`AB${sharedIdx}`).values[0][0];
put(care,'U9',basisGroups.find(g=>g.id==='shared').label);
assert.equal(helper.getRange(`AB${firstIdx}`).values[0][0],beforeFrom-1);
assert.equal(helper.getRange(`AB${sharedIdx}`).values[0][0],beforeShared+1);
assert.equal(dash.getRange(`Q${56+sharedIdx}`).values[0][0],beforeShared+1);
put(care,'U9',firstGroup);
wb.recalculate();
const expected={items:items.length,studies:studies.length,contextRecords:contextCount,primaryCandidateRecords:studies.length-contextCount,excludedItems:excludedItems.length,excludedStudies:excludedStudies.length,withStudies:items.filter(x=>x.study_ids.length).length,statuses:Object.fromEntries(statuses.map(s=>[s,items.filter(x=>x.status===s).length]))};
expected.analyticSubjects=Object.fromEntries(subjectGroups.map(g=>[g.label,studies.filter(x=>x.subject_id===g.id).length]));
assert.equal(helper.getRange('AE6').values[0][0],studies.length);
subjectGroups.forEach((g,i)=>assert.equal(helper.getRange(`AE${i+2}`).values[0][0],expected.analyticSubjects[g.label]));
expected.clinicalBasis=Object.fromEntries(basisGroups.map(g=>[g.label,items.filter(x=>x.clinical_basis===g.label).length]));
assert.equal(helper.getRange('AB8').values[0][0],items.length);
basisGroups.forEach((g,i)=>{assert.equal(helper.getRange(`AB${i+2}`).values[0][0],expected.clinicalBasis[g.label]);basisCols.forEach((c,j)=>assert.equal(helper.getRange(`${c}${i+2}`).values[0][0],items.filter(x=>x.clinical_basis===g.label&&x.status===statuses[j]).length));});
assert.equal(helper.getRange('N2').values[0][0],items.length);assert.equal(helper.getRange('N3').values[0][0],studies.length);assert.equal(helper.getRange('N4').values[0][0],expected.withStudies);
const validStudies=new Set(studies.map(s=>s.id));items.forEach(i=>i.study_ids.forEach(s=>assert(validStudies.has(s))));
statuses.forEach((s,i)=>assert.equal(helper.getRange(`B${i+2}`).values[0][0],expected.statuses[s]));
console.log(JSON.stringify(expected));
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},maxChars:2000});
console.log(errors.ndjson);
assert(!errors.ndjson.includes('"kind":"match"'),'Unexpected cell error');
await(await SpreadsheetFile.exportXlsx(wb)).save(path);
console.log(execFileSync('/Users/lgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',[`${support}/add_native_links.py`,path],{encoding:'utf8'}));
await fs.writeFile(`${root}/research/scoped_evidence.json`,JSON.stringify({scope,clinicalBasis,evidenceSubjects,benchmark,items,studies,excludedItems,excludedStudies,expected},null,2));
await fs.writeFile(`${support}/scope_verification.json`,JSON.stringify(expected,null,2));
await buildBibliography({scope,clinicalBasis,evidenceSubjects,benchmark,items,studies,excludedItems,excludedStudies,expected},drugs);
await writeAnalysisFramework({clinicalBasis,evidenceSubjects,benchmark,items,expected});
for(const [sheetName,range,name] of [['Dashboard','A1:Q14','context-dashboard'],['Dashboard','B43:Q52','benchmark-dashboard'],['Dashboard','B77:Q94','subject-dashboard'],['Literature','S8:X10','subject-columns'],['Literature',`S${9+studies.findIndex(s=>s.id==='L-C03')}:X${9+studies.findIndex(s=>s.id==='L-C03')}`,'surgeon-subject'],['Literature',`A${litEnd+4}:J${litEnd+8}`,'benchmark-methods'],['Literature',`A${mr-3}:J${mr}`,'benchmark-sources']]){const b=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(`${support}/${name}.png`,new Uint8Array(await b.arrayBuffer()));}
console.log(`UPDATED ${path}`);
