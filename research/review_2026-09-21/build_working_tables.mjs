import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const root=process.cwd(),dir=path.join(root,'research/review_2026-09-21');
const read=async p=>JSON.parse(await fs.readFile(path.join(root,p),'utf8'));
const [summary,calibration,manifest,scoped,metadata,retrieval]=await Promise.all([
 'research/review_2026-09-21/search_summary.json','research/review_2026-09-21/calibration_50.json','research/review_2026-09-21/pubmed/manifest.json','research/scoped_evidence.json','research/bibliography_metadata.json','research/retrieval_evidence.json'].map(read));
assert.equal(summary.metadata_exported,58686,'Complete metadata export must finish before workbook generation');
const mr=Array.isArray(metadata)?metadata:metadata.records;
const meta=new Map(mr.map(x=>[x.id,x]));
const wb=Workbook.create();
const names=['Review progress','Study extraction','Effect estimates','Screening calibration','Abstracts','Search log'];
const [progress,extract,effect,screen,abstracts,search]=names.map(n=>wb.worksheets.add(n));
const navy='#183A4A',teal='#166B70',ink='#243E4C',pale='#EDF4F5',input='#FFF0C6';
function col(n){let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26);}return s;}
function put(s,c,v){s.getRange(c).values=[[v]];}
function formula(s,c,v){s.getRange(c).formulas=[[v]];}
function setup(s,widths,title,note,headers,rows,name){
 const last=col(widths.length),end=7+rows.length;
 s.showGridLines=false;
 s.getRange(`A1:${last}${Math.max(end,10)}`).format={font:{name:'Arial',size:10,color:ink},fill:'#FFFFFF',wrapText:true,verticalAlignment:'top'};
 widths.forEach((w,i)=>s.getRange(`${col(i+1)}:${col(i+1)}`).format.columnWidthPx=w);
 const titleCol=widths[1]>=300?'B':widths[2]>=400?'C':'D';
 put(s,`${titleCol}2`,title);s.getRange(`${titleCol}2`).format={font:{name:'Arial',size:16,bold:true,color:navy},rowHeightPx:46};
 const noteWidth=widths[titleCol.charCodeAt(0)-65];
 put(s,`${titleCol}3`,note);s.getRange(`${titleCol}3`).format={font:{name:'Arial',size:10,color:ink},rowHeightPx:Math.max(50,Math.ceil(note.length/(noteWidth/6))*16+18),wrapText:true};
 s.getRange(`A7:${last}${end}`).values=[headers,...rows];
 const t=s.tables.add(`A7:${last}${end}`,true,name);t.style='TableStyleMedium2';t.showFilterButton=true;
 s.getRange(`A7:${last}7`).format={fill:navy,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeightPx:44,horizontalAlignment:'center',verticalAlignment:'center'};
 rows.forEach((row,i)=>{const lines=Math.max(...row.map((v,j)=>String(v??'').split('\n').reduce((n,t)=>n+Math.max(1,Math.ceil(t.length/Math.max(12,(widths[j]-12)/6.3))),0)));s.getRange(`A${i+8}:${last}${i+8}`).format.rowHeightPx=Math.max(76,Math.min(540,lines*16+16));});
 for(let r=8;r<=end;r++)s.getRange(`A${r}:${last}${r}`).format.fill=r%2?pale:'#FFFFFF';
 s.freezePanes.freezeRows(7);s.freezePanes.freezeColumns(2);s.tabColor=teal;
 return end;
}
const ids=['L-R01','L-R02','L-R03','L-R04','L-P01','L-P02','L-P03','L-X01','L-X02'];
const selected=ids.map(id=>({...scoped.studies.find(s=>s.id===id),...retrieval.records.find(s=>s.id===id),id}));
const erows=selected.map(s=>{const m=meta.get(s.id);assert(m?.pmid,s.id);return[s.id,m.pmid,m.title,s.status||s.population_screening_status||'Provisional source review; human screening pending',s.extraction_level||s.access_level,s.unit_of_analysis||'See retrieval reference notes',s.population||'Outside active register; eligibility unresolved',s.payer||'See retrieval notes',s.data_period||'See source',s.finding,s.limitation||s.reason,s.url||m.url,s.extraction_source||'research/review_2026-09-21/drug_access/drug_access_candidates.json'];});
setup(extract,[90,130,440,320,340,280,360,260,260,630,580,330,360],'Evidence extraction — 21 Sep 2026','Four new candidates, three source rechecks and two separately logged retrieval references. AI extraction requires human verification. No formal risk-of-bias or certainty ratings.',
 ['Study ID','PMID','Verified title','Current status','Access / review level','Unit of analysis','Population','Medicare / payer relation','Data period','Extracted finding','Limitations / next step','Source URL','Detailed extraction file'],erows,'ExtractionUpdates');

extract.getRange('L8:L16').format.font={name:'Arial',size:10,color:'#126D92'};
const outcomes=[
 ['L-R01','33298705','Any cost-related nonadherence','Medicare <65; MCBS 2016','Female versus male','Adjusted odds ratio',1.66,1.31,2.10,'Weighted prevalence: 40.5% versus 28.5%.','Table 3; 95% CI; cross-sectional. Sex from enrollment; identity unresolved.'],
 ['L-R01','33298705','Any cost-related nonadherence','Medicare >=65; MCBS 2016','Female versus male','Adjusted odds ratio',1.21,1.04,1.41,'Weighted prevalence: 15.7% versus 12.8%.','Table 3; 95% CI. Cohort N differs from outcome respondent N.'],
 ['L-R02','33656528','Persistent nonadherence (>=3 surveys)','Selected Chicago Medicare cohort, 2012–2018','Female versus male','Adjusted odds ratio',1.36,.95,1.95,'162/1,036 (15.6%) versus 68/619 (11.0%); adjusted P=.10.','Table 2; 95% CI. Different endpoint from L-R01; imprecise estimate; identity unresolved.'],
 ['L-R02','33656528','Transient nonadherence (1 survey)','Selected Chicago Medicare cohort, 2012–2018','Female versus male','Adjusted odds ratio',.81,.62,1.07,'Adjusted P=.15.','Table 2; 95% CI. Preserve contrary direction and uncertainty; exact model denominator requires verification.'],
 ['L-R03','38459983','DXA receipt','Asian American Medicare subgroup','Women >=65 versus men >=70','Crude percentages',null,null,null,'19.8% versus 5.0%; P<.001.','Abstract only. Different age thresholds; sex denominators and adjusted sex effect unavailable. Not a national adjusted comparison.'],
 ['L-R04','27884649','Bone mass measurement within two years','Medicare Advantage women, 2008–2014','Age >=80 versus 65–79','Crude percentages',null,null,null,'12.9% (95% CI 12.7–13.1) versus 26.8% (26.6–26.9).','Table 2; women only. N=135,661 versus 394,791. Broader than DXA; no male/female effect.'],
 ['L-P01','39978776','Per-procedure work RVU','55 selected procedure pairs; 2023 valuation','Male-associated versus female-associated procedures','Published mean relative difference',null,null,null,'Male-associated procedures averaged 30% higher work RVU; 41/55 female-associated procedures had lower work RVU.','Abstract only. Pair selection and time adjustment require full-text review. Code valuation is distinct from patient or physician sex effects.'],
 ['L-P02','38758183','RVU and RVU per minute','Selected clinically matched procedure pairs','Female-associated versus male-associated procedures','Null reported; CI unavailable',null,null,null,'Journal abstract: 10 pairs, 7 female higher / 3 male higher; no significant aggregate difference reported.','Full text pending. AUA companion reports 9 pairs / 6 female higher; discrepancy unresolved. Null is not equivalence.'],
 ['L-P03','34736273','Work RVU per operative hour','12 pairs / 25 CPT codes; 12,120 NSQIP cases 2015–2018','Female-specific versus male-specific procedure labels','Median and IQR',null,null,null,'10.6 (IQR 7.2–16.2) versus 9.7 (7.4–12.8); P<.001.','Main text / Table 1. NSQIP is not a Medicare-only cohort. IQR is not confidence interval; full perioperative work omitted.'],
 ['L-P03','34736273','Modeled specialty compensation per hour','Same selected procedure set','Female-specific versus male-specific procedure labels','Median USD/hour and IQR',null,null,null,'$555 (IQR 377–843) versus $599 (457–790); P<.001.','Specialty survey compensation multipliers, not Medicare reimbursement rates. Published arithmetic discrepancies require verification.']
].map(r=>[...r,`https://pubmed.ncbi.nlm.nih.gov/${r[1]}/`]);
setup(effect,[90,160,290,330,330,250,110,110,110,520,560,330],'Selected outcome estimates','Keep outcomes, populations and units separate. The odds-ratio columns contain 95% confidence limits only. Empty numeric fields mean the source uses a different measure or lacks the estimate.',
 ['Study ID','PMID','Outcome','Population / period','Comparison','Effect measure','Estimate','95% CI lower','95% CI upper','Other reported result','Source location and interpretation boundary','Source URL'],outcomes,'SelectedEstimates');
effect.getRange('G8:I17').setNumberFormat('0.00');
const srows=calibration.map((r,i)=>[r.pmid,r.title,null,r.reviewer_1,r.reviewer_1_decision,r.reviewer_2,r.reviewer_2_decision,r.adjudication,r.reason,r.decision_date,r.existing_study_id,r.sampling_reason,r.authors,r.year,r.journal,r.doi,r.source_url,`Abstracts row ${8+i}`]);
const send=setup(screen,[110,500,185,165,135,165,135,150,310,125,100,360,360,80,280,290,330,140],'Human screening calibration','50 deliberately selected records for reviewer calibration; not a representative sample or final inclusion set. Enter separate reviewer names and decisions in amber cells. Sex reporting alone does not confirm cisgender eligibility.',
 ['PMID','Title','Review status','Reviewer 1 name','Reviewer 1 decision','Reviewer 2 name','Reviewer 2 decision','Adjudicated decision','Exclusion reason / discussion','Decision date','Existing study ID','Sampling basis','Authors','Year','Journal / book','DOI','PubMed URL','Full abstract location'],srows,'CalibrationRecords');
screen.getRange(`D8:J${send}`).format.fill=input;
for(const c of ['E','G','H'])screen.getRange(`${c}8:${c}${send}`).dataValidation={rule:{type:'list',values:['Retrieve full text','Exclude','Unclear']}};
for(let r=8;r<=send;r++)formula(screen,`C${r}`,`=IF(OR(D${r}="",E${r}="",F${r}="",G${r}=""),"Awaiting two reviews",IF(D${r}=F${r},"Check reviewer names",IF(OR(E${r}<>G${r},E${r}="Unclear"),IF(OR(H${r}="",H${r}="Unclear"),"Resolve disagreement",IF(AND(H${r}="Exclude",I${r}=""),"Add exclusion reason","Adjudicated")),IF(AND(E${r}="Exclude",I${r}=""),"Add exclusion reason","Concordant"))))`);
screen.getRange(`N8:N${send}`).setNumberFormat('0');screen.getRange(`J8:J${send}`).setNumberFormat('yyyy-mm-dd');
const arows=calibration.map(r=>[r.pmid,r.abstract||'No abstract in retrieved PubMed record; retrieve full text where potentially eligible.',r.title,r.source_url,r.raw_xml]);
setup(abstracts,[110,1240,450,330,420],'Full PubMed abstracts','Exact exported abstract text, including section labels. Abstracts are not full-text reviews. No abstract is not itself an exclusion criterion.',
 ['PMID','Abstract','Title','PubMed URL','Archived raw source'],arows,'CalibrationAbstracts');
arows.forEach((r,i)=>{const lines=r[1].split('\n').reduce((n,line)=>n+Math.max(1,Math.ceil(line.length/182)),0);abstracts.getRange(`A${i+8}:E${i+8}`).format.rowHeightPx=Math.max(112,Math.min(540,lines*16+28));});
const currentCore=manifest.query_repairs.find(x=>x.id.includes('CORE'));
const supp=manifest.runs.find(x=>x.id.includes('SUPP'));
const priority=manifest.query_repairs.find(x=>x.id.includes('PRIORITY'));
const logRows=[
 [currentCore.id,currentCore.query.replace(/\s+/g,' ').trim(),currentCore.retrieved_count,'Identification — current core','2026-09-21','pubmed/manifest.json; raw search partitions','Corrected MeSH heading added 60 IDs, removed 0.'],
 [supp.id,supp.query.replace(/\s+/g,' ').trim(),supp.retrieved_count,'Identification — supplementary','2026-09-21','pubmed/manifest.json; raw search partitions','No Medicare restriction; worldwide/other-payer hits still require screening.'],
 [priority.id,priority.query.replace(/\s+/g,' ').trim(),priority.retrieved_count,'Metadata priority subset only','2026-09-21','pubmed/manifest.json','Subset of the union; not a third identification source or an eligibility filter.'],
 ['UNION','Current core OR supplementary; exact PMID duplicate removal',summary.unique_identified,'Unique identified records','2026-09-21','pubmed/current_unique_pmids.txt; deduplication_map.csv','Only exact PMID duplicates resolved; report families and study overlap remain pending.'],
 ['METADATA','NCBI PubMed XML efetch for every unique PMID',summary.metadata_exported,'Complete bibliographic export','2026-09-21','pubmed/all_records.jsonl.gz; all_records.csv.gz; raw/','Abstract absence retained explicitly. Original response and stored-file hashes retained.'],
 ['CALIBRATION','Purposive known sources plus deterministic SHA-256 ordering within topic keywords; see prepare_search.py',calibration.length,'Preparation for two human reviewers','2026-09-21','calibration_50.csv; prepare_search.py','Post-search selection; no independent human decisions entered.']
];
setup(search,[240,1100,110,270,120,480,520],'Executed search log','Development search executed before PRESS review. Search results are not included studies. Whitespace is reflowed here; exact submitted queries, translations, timestamps, warnings and hashes are archived.',
 ['Run / stage','Query (whitespace reflowed) / operation','Record count','Role','Execution date','Archive path (relative to review folder)','Qualification'],logRows,'ExecutedSearches');

search.getRange('C8:C13').setNumberFormat('#,##0');
const progressRows=[
 ['Identification','Corrected core hits',summary.corrected_core,'Exact executed PubMed query','Search log / archived manifest'],
 ['Identification','Supplementary hits',summary.supplement,'May include non-Medicare and non-US records','Search log / archived manifest'],
 ['Deduplication','Duplicate query hits',summary.duplicate_hits_removed_by_pmid,'Exact PMID only; removed once from union','pubmed/deduplication_map.csv'],
 ['Identification','Unique retrieved records',null,'Not included-study count','Core + supplement − duplicate hits'],
 ['Export','Bibliographic records archived',summary.metadata_exported,'All retrieved PMIDs; abstracts when available','pubmed/all_records.jsonl.gz'],
 ['Export','Records with abstracts',summary.with_abstract,'Abstracts are not full texts','search_summary.json'],
 ['Export','Records without abstracts',summary.without_abstract,'No abstract does not justify automatic exclusion','search_summary.json'],
 ['Calibration','Records prepared',calibration.length,'Purposive sample; not representative','Screening calibration'],
 ['Calibration','Two-reviewer agreement / adjudication',null,'Formula counts resolved paired decisions in this workbook only','Screening calibration, status column'],
 ['Calibration','Awaiting two reviews',null,'Names and both decisions required','Screening calibration, status column'],
 ['Calibration','Other unresolved records',null,'Disagreements, missing reasons or duplicate reviewer names','Screening calibration, status column'],
 ['Selected evidence','Active working-register records',scoped.studies.length,'Candidates and contextual records; not final inclusions','Updated evidence register'],
 ['Selected evidence','New patient-access candidates',4,'Gender identity unresolved; human verification pending','L-R01–L-R04'],
 ['Selected evidence','Existing source rechecks',3,'Source discrepancies retained; full-text gaps disclosed','L-P01–L-P03'],
 ['Context leads','References outside active register',2,'Not counted as screened full-text exclusions','L-X01–L-X02']
];
setup(progress,[160,430,140,560,460],'Medicare review working tables','Updated 21 September 2026. Preliminary evidence and a reproducible search archive. Human screening, PRESS, additional databases and formal appraisal remain pending.',
 ['Stage','Metric','Count','Interpretation','Source / method'],progressRows,'ReviewProgress');
progress.getRange('A8:E22').format.rowHeightPx=38;progress.getRange('C8:C22').setNumberFormat('#,##0');
formula(progress,'C11','=C8+C9-C10');
formula(progress,'C16',`=COUNTIF('Screening calibration'!C8:C${send},"Concordant")+COUNTIF('Screening calibration'!C8:C${send},"Adjudicated")`);
formula(progress,'C17',`=COUNTIF('Screening calibration'!C8:C${send},"Awaiting two reviews")`);
formula(progress,'C18','=C15-C16-C17');
put(progress,'B24','Read the evidence carefully');progress.getRange('B24').format.font={name:'Arial',size:12,bold:true,color:navy};
put(progress,'B25','Coverage, payment, affordability and utilization answer different questions.');put(progress,'D25','Patient sex/gender, physician sex/gender and service valuation are separate evidence streams. Shared bone/systemic care is distinct from reproductive anatomy.');
put(progress,'B27','Current patient candidates do not establish cisgender identity from sex labels.');put(progress,'D27','PRISMA guides reporting. GRADE concerns certainty for an outcome across a body of evidence. No formal GRADE ratings have been assigned.');
progress.getRange('B25:E28').format.rowHeightPx=55;
// Verify paired human-review logic and reset all demonstration edits before export.
wb.recalculate();assert.equal(progress.getRange('C16').values[0][0],0);assert.equal(progress.getRange('C17').values[0][0],50);
screen.getRange('D8:E8').values=[['Reviewer A','Retrieve full text']];wb.recalculate();assert.equal(progress.getRange('C16').values[0][0],0);
screen.getRange('F8:G8').values=[['Reviewer B','Retrieve full text']];wb.recalculate();assert.equal(progress.getRange('C16').values[0][0],1);
put(screen,'F8','Reviewer A');wb.recalculate();assert.equal(progress.getRange('C16').values[0][0],0);
put(screen,'F8','Reviewer B');put(screen,'G8','Exclude');wb.recalculate();assert.equal(screen.getRange('C8').values[0][0],'Resolve disagreement');
put(screen,'H8','Exclude');wb.recalculate();assert.equal(screen.getRange('C8').values[0][0],'Add exclusion reason');
put(screen,'I8','Calibration test only');wb.recalculate();assert.equal(progress.getRange('C16').values[0][0],1);
screen.getRange('D8:J8').values=[Array(7).fill('')];wb.recalculate();assert.equal(progress.getRange('C16').values[0][0],0);assert.equal(progress.getRange('C17').values[0][0],50);assert.equal(progress.getRange('C11').values[0][0],58686);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:10},maxChars:1200});
console.log('Formula-error inspection',JSON.stringify(errors));
await fs.mkdir(path.join(dir,'previews'),{recursive:true});
for(const [name,range,stem] of [['Review progress','A1:D18','progress'],['Study extraction','A1:D10','citations'],['Study extraction','J7:K10','findings'],['Effect estimates','F7:K11','effects'],['Effect estimates','A1:F8','effect-heading'],['Screening calibration','A7:G10','calibration'],['Abstracts','A7:B8','abstract'],['Search log','A7:C8','search']]){
 const b=await wb.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(path.join(dir,'previews',`${stem}.png`),new Uint8Array(await b.arrayBuffer()));
}
const output=path.join(root,'outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_review_working_tables_2026-09-21.xlsx');
await(await SpreadsheetFile.exportXlsx(wb)).save(output);
await fs.writeFile(path.join(dir,'workbook_verification.json'),JSON.stringify({verified_on:'2026-09-21',worksheets:names,identified:58686,metadata:summary.metadata_exported,new_candidates:4,source_rechecks:3,outside_active_references:2,calibration_records:50,human_decisions_entered:0,paired_reviewer_formula_tests:'passed; one reviewer cannot resolve; duplicate names flagged; conflicting decisions require adjudication; exclusions require reason',formula_error_inspection:errors,output:path.relative(root,output)},null,2)+'\n');
console.log(JSON.stringify({output,rows:calibration.length,worksheets:names.length}));
