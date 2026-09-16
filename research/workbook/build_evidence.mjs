import fs from 'node:fs/promises';
// Initial broad-scope build. Apply apply_scope.mjs afterwards for the current user-approved population scope.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { SpreadsheetFile, FileBlob } from '@oai/artifact-tool';
process.on('uncaughtException',err=>{console.error(err.message);console.error(String(err.stack).split('\n').filter(x=>x.includes('build_evidence')).join('\n'));process.exit(1);});

const root='/Users/lgm/Documents/ChatGPT/Medicare';
const out=`${root}/outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8`;
const support=`${root}/research/workbook`;
const read=async n=>JSON.parse(await fs.readFile(`${root}/research/${n}.json`,'utf8'));
const [drugs,procedures,gender,additional,formulary,pairs]=await Promise.all(['literature_drugs','literature_procedures','literature_gender_screening','literature_additional','formulary_results','procedure_pairs_2026'].map(read));
const items=[...drugs.items,...procedures.items,...gender.items,...additional.items];
const studies=[...procedures.studies,...drugs.studies,...gender.studies,...additional.studies];
assert.equal(new Set(items.map(x=>x.id)).size,items.length);
assert.equal(new Set(studies.map(x=>x.id)).size,studies.length);
assert.equal(new Set(studies.map(x=>x.doi_or_pmid.match(/PMID\s*(\d+)/)?.[1]||x.url)).size,studies.length);
const studyIDs=new Set(studies.map(x=>x.id));
items.forEach(x=>x.study_ids.forEach(id=>assert(studyIDs.has(id),`${x.id}: ${id}`)));
const reviewed=new Date('2026-09-16T12:00:00Z');
const statuses=['Covered with conditions','Plan dependent','Excluded for this use','Local decision','Not established'];
items.forEach(x=>assert(statuses.includes(x.status)));

const template='/Users/lgm/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-analytics-dashboard/assets/reference.xlsx';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(template));
const dash=wb.worksheets.getItem('Dashboard');
const care=wb.worksheets.getItem('Data & Targets');
const helper=wb.worksheets.getItem('_Chart Helpers');
const lit=wb.worksheets.add('Literature');
const drug=wb.worksheets.add('Drug formularies');
const rvu=wb.worksheets.add('Procedure values');
const navy='#102332',panel='#19354D',teal='#00A3B5',cyan='#3FC5EC',amber='#EAAF45',ink='#243B50',muted='#596D7E',pale='#EDF4F8';
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const value=(s,c,v)=>s.getRange(c).values=[[v]];
const formula=(s,c,f)=>s.getRange(c).formulas=[[f]];
// This runtime cannot evaluate HYPERLINK. Keep source text native, then add link relationships after export.
const link=(s,c,url)=>{if(url)value(s,c,url);};
const box=(s,r,text,fill=navy,color='#FFFFFF',size=12)=>{s.getRange(r).merge();s.getRange(r).values=[[text]];s.getRange(r).format={fill,font:{name:'Aptos',size,color,bold:true},wrapText:true,verticalAlignment:'center'};};
function base(s,end,widths){
  s.getRange(`A1:${end}220`).format={font:{name:'Aptos',size:11,color:ink},fill:'#FFFFFF',verticalAlignment:'top',wrapText:true};
  s.showGridLines=false;s.tabColor=teal;
  widths.forEach((w,i)=>s.getRange(`${col(i)}:${col(i)}`).format.columnWidthPx=w);
}
function table(s,headers,rows,start,name,widths){
  const end=start+rows.length,last=col(headers.length-1);
  s.getRange(`A${start}:${last}${end}`).values=[headers,...rows];
  const t=s.tables.add(`A${start}:${last}${end}`,true,name);t.style='TableStyleMedium2';t.showFilterButton=true;
  s.getRange(`A${start}:${last}${start}`).format={fill:panel,font:{name:'Aptos',size:11,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center',rowHeightPx:48};
  s.getRange(`A${start+1}:${last}${end}`).format={rowHeightPx:156,verticalAlignment:'top',wrapText:true};
  for(let r=start+1;r<=end;r++)s.getRange(`A${r}:${last}${r}`).format.fill=(r%2===0)?'#F2F6F9':'#FFFFFF';
  widths?.forEach((w,i)=>s.getRange(`${col(i)}:${col(i)}`).format.columnWidthPx=w);
  s.freezePanes.freezeRows(start);s.freezePanes.freezeColumns(2);
  return end;
}

// Preserve the imported dashboard's visual layout. Replace demonstration content with research.
dash.getRange('A1:Q53').clear({applyTo:'contents'});
dash.charts.deleteAll();
dash.getRange('B2:Q52').format.fill=navy;
dash.getRange('B2:Q52').format.font={name:'Aptos',size:11,color:'#FFFFFF'};
dash.getRange('B2:I2').unmerge();box(dash,'B2:I2','Medicare gender-related care',navy,'#FFFFFF',20);
value(dash,'B3','Coverage and reimbursement evidence register');
value(dash,'B4','Preliminary scoping review. Counts describe this selected inventory.');
dash.getRange('B4:I4').format.font={name:'Aptos',size:10,color:'#AFBFCD',italic:true};
value(dash,'J2','POLICIES REVIEWED');value(dash,'N2','PUBLIC FORMULARY SNAPSHOT');
value(dash,'J3',reviewed);dash.getRange('J3').setNumberFormat('mmm d, yyyy');
value(dash,'N3','August 2026');

care.getRange('A1:T100').unmerge();care.getRange('A1:T100').clear({applyTo:'all'});
base(care,'T',[72,270,190,130,255,245,190,340,380,325,395,300,380,350,165,110,24,320,320,330]);
box(care,'A1:F2','Care inventory',navy,'#FFFFFF',22);
box(care,'A3:F4','One row describes a care item and indication. Filter coverage status, Medicare part, scope, or domain. Scroll right for evidence, caveats, sources and review notes.',pale,ink,11);
box(care,'A5:F6','“Not established” means this review did not resolve item-specific coverage. It does not mean excluded. Local rules and selected-plan examples are labeled in the scope column.',pale,ink,11);
value(care,'H2','Review date');value(care,'I2',reviewed);care.getRange('I2').setNumberFormat('mm/dd/yy');
const careHeaders=['Item ID','Care item','Coverage status','Medicare part','Indication','Population','Domain','Policy scope / date','Coverage rule','Comparison','Evidence on disparity or access','Evidence type','Limits / counterevidence','Next research question','Study IDs','Reviewed',' ','Primary policy / formulary source','Additional policy / label source','Reviewer notes'];
const supplementFor={D05:drugs.supplemental_policy_sources[3].url,D09:drugs.supplemental_policy_sources[0].url,D10:drugs.supplemental_policy_sources[1].url,D11:drugs.supplemental_policy_sources[2].url,D12:drugs.supplemental_policy_sources[5].url};
const careRows=items.map(x=>[x.id,x.item,x.status,x.medicare_part,x.indication,x.population,x.domain,x.policy_scope,x.policy_summary,x.comparison,x.disparity_evidence,x.evidence_type,x.limitations,x.next_question,x.study_ids.join(', '),reviewed,'',x.policy_url,x.policy_url2||supplementFor[x.id]||'','']);
const careEnd=table(care,careHeaders,careRows,8,'CareInventory');
care.freezePanes.freezeColumns(3);
care.getRange(`Q8:Q${careEnd}`).setNumberFormat(';;;');
care.getRange(`Q8:Q${careEnd}`).format.fill='#FFFFFF';
care.getRange('Q8').format.font={name:'Aptos',color:'#FFFFFF',size:11};
care.getRange(`P9:P${careEnd}`).setNumberFormat('mm/dd/yy');
care.getRange(`R9:S${careEnd}`).format.font={name:'Aptos',size:10,color:'#176CA4'};
careRows.forEach((row,i)=>{link(care,`R${i+9}`,row[17]);link(care,`S${i+9}`,row[18]);});
care.getRange(`T9:T${careEnd}`).format.fill='#FFF4D6';
care.getRange(`C9:C${careEnd}`).dataValidation={rule:{type:'list',values:statuses}};
const statusColors={'Covered with conditions':'#DFF0E9','Plan dependent':'#E4EFFB','Excluded for this use':'#F9E1DB','Local decision':'#FFF0D0','Not established':'#E9E9EF'};
for(const status of statuses)care.getRange(`C9:C${careEnd}`).conditionalFormats.add('containsText',{text:status,format:{fill:statusColors[status],font:{color:ink,bold:true}}});

base(lit,'O',[95,350,75,260,280,275,190,430,425,335,170,240,24,340,245]);
box(lit,'A1:F2','Scientific literature',navy,'#FFFFFF',22);
box(lit,'A3:F4','Targeted PubMed/PMC and primary-source searches cover payment, coverage, utilization, patient costs and clinical benefit. Both supportive and conflicting studies are retained.',pale,ink,11);
box(lit,'A5:F6','This is an initial scoping register, not an exhaustive systematic review. Most studies were summarized from abstracts. See source-access details, payer, limitations and methods below.',pale,ink,11);
const litHeaders=['Study ID','Citation','Year','Design','Population / sample','Payer / applicability','Data period','Main finding','Limitations','Relevance to this review','Linked item IDs','Source access',' ','Study URL','DOI / PMID'];
const litRows=studies.map(x=>[x.id,x.citation,x.year,x.design,x.population,x.payer,x.data_period,x.finding,x.limitation,x.relevance,items.filter(a=>a.study_ids.includes(x.id)).map(a=>a.id).join(', '),x.extraction_level||'Citation and abstract; full-text extraction not completed','',x.url,x.doi_or_pmid]);
const litEnd=table(lit,litHeaders,litRows,8,'ScientificLiterature');
lit.getRange(`M8:M${litEnd}`).setNumberFormat(';;;');
lit.getRange(`M8:M${litEnd}`).format.fill='#FFFFFF';
lit.getRange('M8').format.font={name:'Aptos',color:'#FFFFFF',size:11};
lit.getRange(`C9:C${litEnd}`).setNumberFormat('0');
lit.getRange(`N9:N${litEnd}`).format.font={name:'Aptos',size:10,color:'#176CA4'};
litRows.forEach((row,i)=>link(lit,`N${i+9}`,row[13]));
let mr=litEnd+3;
box(lit,`A${mr}:F${mr}`,'Review method and interpretation',panel);lit.getRange(`A${mr}:F${mr}`).format.rowHeightPx=30;
const methodRows=[
 ['Scope','US Medicare is the coverage focus. Broader clinical and other-payer studies are included only with explicit applicability limits. Patient sex, anatomy and gender identity are distinct variables.'],
 ['Search completed','September 16, 2026. Targeted topic searches and citation following, with no prespecified publication-year cutoff. This register contains selected records, not every screened result.'],
 ['Search themes','Medicare gender reimbursement; male/female surgical RVUs; vaginal estrogen costs; menopause formularies; contraception and disability; transgender insurance denials; screening; breast reconstruction; lymphedema.'],
 ['Source hierarchy','Coverage classifications use federal benefit rules, CMS/Medicare pages, named contractor guidance and identified plan formularies. Scientific studies inform outcomes and disparity hypotheses, not automatic coverage decisions.'],
 ['Study extraction','Record citation, study design, population, payer, time period, finding and limits. Source-access column distinguishes abstract summaries from targeted full-text review. No formal risk-of-bias tool or meta-analysis was performed.'],
 ['Meaning of status','Covered with conditions means an applicable benefit or broad listing was verified. Plan dependent and Local decision require additional review. Excluded for this use is indication-specific. Not established is an unresolved research finding.'],
 ['Bias assessment','Payment differences, access gaps and clinical effectiveness are different findings. A causal sex/gender bias claim requires credible comparators and adjustment for clinical need, time, complexity, setting, indication and alternatives.'],
 ['Known limitations','No comprehensive code inventory, nationwide denied-claims dataset, enrollment-weighted formulary analysis, or matched patient-level disparity estimate. Some items have policy evidence without an attached scientific study.'],
 ['Expansion','Add items to CareInventory and papers to ScientificLiterature. Keep stable IDs, date the policy check, and record new source URLs. Existing table formulas summarize the populated tables; chart selections remain illustrative.'],
 ['Abbreviations','CMS: Centers for Medicare & Medicaid Services. MAC: Medicare Administrative Contractor. MA: Medicare Advantage. NCD: national coverage determination. RVU: relative value unit. PA: prior authorization. ST: step therapy.']
];
for(const [label,txt] of methodRows){mr++;box(lit,`A${mr}:B${mr}`,label,pale,ink,11);box(lit,`D${mr}:J${mr}`,txt,'#FFFFFF',ink,11);lit.getRange(`A${mr}:J${mr}`).format.rowHeightPx=60;}
mr+=3;box(lit,`A${mr}:F${mr}`,'Additional primary policy and label sources',panel);lit.getRange(`A${mr}:F${mr}`).format.rowHeightPx=30;
for(const source of drugs.supplemental_policy_sources){mr++;box(lit,`A${mr}:F${mr}`,source.topic,pale,ink,11);box(lit,`H${mr}:J${mr}`,source.url,'#FFFFFF','#176CA4',10);link(lit,`H${mr}`,source.url);lit.getRange(`A${mr}:J${mr}`).format.rowHeightPx=55;}

base(drug,'K',[300,120,120,115,155,145,160,170,130,350,380]);
box(drug,'A1:F2','Drug formulary listing',navy,'#FFFFFF',22);
box(drug,'A3:F4','August 2026 CMS public files. Denominator: 5,499 unsuppressed contract-plan-segment combinations after removing county repetitions. Each segment counts equally; results are not enrollment weighted.',pale,ink,11);
box(drug,'A5:F6','Listing means at least one matched option. It does not guarantee a paid claim, every dose, affordability or clinical suitability. PA percentages use listing segments as the denominator. Formulations and indications differ.',pale,ink,11);
const drugHeaders=['Drug / formulation','Plan segments','Segments listing ≥1 option','Listed share','Listing segments: all options PA','All-options PA share','Segments with ≥1 no-PA option','Segments with ≥1 no-PA/no-ST option','Reference drug concepts','CMS public file','Scope / source detail'];
const drugRows=formulary.results.map(x=>[x.group,x.plan_segments_total,x.plan_segments_listed,null,x.listed_plan_segments_all_options_PA,null,x.plan_segments_with_at_least_one_listed_option_without_PA,x.plan_segments_with_at_least_one_option_with_neither_PA_nor_ST,x.reference_rxcuis,formulary.metadata.archive_url,'CMS basic formulary joined by RxCUI to August 25 reference. 328 formularies. Excludes 19 suppressed segments and employer, PACE, non-Part-D and most demonstration plans.']);
const par=drugs.formulary_evidence.supplementary_paroxetine_screen;
drugRows.push([par.description,par.plan_segments_total,par.listed_plan_segments,null,null,null,null,null,1,par.source_url,'Separate exact-RxCUI screen (1430122), same denominator. PA/ST measures not extracted for this supplementary row.']);
const drugEnd=table(drug,drugHeaders,drugRows,8,'DrugFormularies');
drug.getRange(`A9:K${drugEnd}`).format.rowHeightPx=90;
drugRows.forEach((row,i)=>link(drug,`J${i+9}`,row[9]));
for(let r=9;r<=drugEnd;r++){formula(drug,`D${r}`,`=C${r}/B${r}`);if(r<drugEnd)formula(drug,`F${r}`,`=E${r}/C${r}`);}
drug.getRange(`B9:C${drugEnd}`).setNumberFormat('#,##0');drug.getRange(`E9:E${drugEnd}`).setNumberFormat('#,##0');drug.getRange(`G9:I${drugEnd}`).setNumberFormat('#,##0');
drug.getRange(`D9:D${drugEnd}`).setNumberFormat('0.00%');drug.getRange(`F9:F${drugEnd}`).setNumberFormat('0.00%');
drug.getRange(`D9:D${drugEnd}`).conditionalFormats.add('dataBar',{color:teal});
box(drug,`A${drugEnd+3}:F${drugEnd+4}`,'Coverage differs by indication. Basic Part D excludes drugs used for sexual or erectile dysfunction; supplemental benefits may differ. Vaginal-atrophy treatments are not automatically in that excluded category.',pale,ink,11);
box(drug,`A${drugEnd+6}:F${drugEnd+7}`,'23 unmatched RxCUIs were checked independently and did not belong to target groups. No patient gender, diagnosis, denied-claim, cost-sharing or enrollment data were analyzed. Nonlisting does not rule out a formulary exception.',pale,ink,11);
value(drug,`A${drugEnd+9}`,'CMS reference file');value(drug,`B${drugEnd+9}`,formulary.metadata.reference_url);drug.getRange(`B${drugEnd+9}:F${drugEnd+10}`).merge();drug.getRange(`A${drugEnd+9}:F${drugEnd+10}`).format.rowHeightPx=30;

base(rvu,'P',[245,105,240,115,135,245,125,125,145,155,160,155,110,410,350,330]);
box(rvu,'A1:F2','Illustrative procedure values',navy,'#FFFFFF',22);
box(rvu,'A3:F4','Five published analogous pairs checked against the July 2026 CMS physician fee schedule. RVUs are national values before geographic adjustment. They are not patient costs or proof of coverage.',pale,ink,11);
box(rvu,'A5:F6','Positive differences favor the urologic/other comparator. Negative differences favor the gynecologic comparator. The urinary malignancy code is not restricted to men. This selected subset is not a nationwide bias estimate.',pale,ink,11);
const rvuHeaders=['Procedure pair','Other CPT','Urologic / other procedure','Other work RVU','Gynecologic CPT','Gynecologic procedure','Gynecologic work RVU','Work RVU difference','Relative work RVU difference','Other physician facility RVU','Gynecologic physician facility RVU','Relative facility RVU difference','Global days (both)','Comparison limits','CMS source','Pair-selection source'];
const rvuRows=pairs.pairs.map((p,i)=>[p.comparison,p.male.cpt,p.male.label,p.male.work_rvu,p.female.cpt,p.female.label,p.female.work_rvu,null,null,p.male.physician_facility_total_rvu,p.female.physician_facility_total_rvu,null,p.male.global_days,i===2?'Penile code specifies chemical treatment. Vulvar code allows broader methods. Compare only equivalent treatment methods.':i===4?'Urinary-organ malignancy code 51597 is not universally male-only. Procedures may differ in work and extent.':'Same global period does not establish equal time, intensity, risk or total perioperative work.',pairs.cms_landing_url,pairs.pair_selection_source.pubmed_url]);
const rvuEnd=table(rvu,rvuHeaders,rvuRows,8,'ProcedureValues');
rvuRows.forEach((row,i)=>{link(rvu,`O${i+9}`,row[14]);link(rvu,`P${i+9}`,row[15]);});
rvu.getRange('B9:B13').format.horizontalAlignment='center';rvu.getRange('E9:E13').format.horizontalAlignment='center';
rvu.getRange('A8:P8').format.rowHeightPx=78;
for(let r=9;r<=rvuEnd;r++){formula(rvu,`H${r}`,`=D${r}-G${r}`);formula(rvu,`I${r}`,`=H${r}/G${r}`);formula(rvu,`L${r}`,`=(J${r}-K${r})/K${r}`);}
for(const c of ['D','G','H','J','K'])rvu.getRange(`${c}9:${c}${rvuEnd}`).setNumberFormat('0.00');
for(const c of ['I','L'])rvu.getRange(`${c}9:${c}${rvuEnd}`).setNumberFormat('0.0%;(0.0%);0.0%');
box(rvu,`A${rvuEnd+3}:F${rvuEnd+4}`,'Physician facility RVUs describe the physician service when delivered in a facility. They are not hospital facility payments. Relative difference = (other − gynecologic) ÷ gynecologic value.',pale,ink,11);
box(rvu,`A${rvuEnd+6}:F${rvuEnd+7}`,'Pair selection follows Hathaway et al. (2024). Its 10-pair analysis found no statistically significant overall work-RVU difference. Penn et al. (2025), using 55 pairs, found higher average valuation for male-anatomy procedures. See Literature for limitations.',pale,ink,11);

// Reuse the template helper sheet for transparent, cell-linked chart inputs.
helper.getRange('A1:T80').unmerge();helper.getRange('A1:T80').clear({applyTo:'all'});
base(helper,'T',Array(20).fill(135));
helper.getRange('A1:B6').values=[['Coverage classification','Selected items'],...statuses.map(x=>[x,null])];
statuses.forEach((s,i)=>formula(helper,`B${i+2}`,`=COUNTIF(CareInventory[Coverage status],A${i+2})`));
helper.getRange('D1:E7').values=[['Formulation','Listed share'],['Vaginal cream',null],['Estradiol patch',null],['Estradiol gel',null],['Veozah',null],['Osphena',null],['Intrarosa',null]];
[11,13,14,18,19,20].forEach((r,i)=>formula(helper,`E${i+2}`,`='Drug formularies'!D${r}`));
helper.getRange('G1:H6').values=[['Formulation','All-options PA share'],['Estradiol patch',null],['Testosterone gel',null],['Veozah',null],['Osphena',null],['Intrarosa',null]];
[13,17,18,19,20].forEach((r,i)=>formula(helper,`H${i+2}`,`='Drug formularies'!F${r}`));
helper.getRange('J1:K6').values=[['Published pair','Relative work RVU difference'],['Sling placement',null],['Sling revision',null],['Genital lesion',null],['Genital excision',null],['Exenteration',null]];
for(let i=0;i<5;i++)formula(helper,`K${i+2}`,`='Procedure values'!I${i+9}`);
helper.getRange('M1:N6').values=[['Inventory measure','Count'],['Care items',null],['Scientific studies',null],['Items with linked studies',null],['Policy-only items',null],['Local or unresolved',null]];
formula(helper,'N2','=COUNTA(CareInventory[Item ID])');formula(helper,'N3','=COUNTA(ScientificLiterature[Study ID])');
formula(helper,'N4','=COUNTA(CareInventory[Item ID])-COUNTBLANK(CareInventory[Study IDs])');formula(helper,'N5','=COUNTBLANK(CareInventory[Study IDs])');formula(helper,'N6','=B5+B6');
helper.getRange('E2:E7').setNumberFormat('0.0%');helper.getRange('H2:H6').setNumberFormat('0.0%');helper.getRange('K2:K6').setNumberFormat('0.0%');
helper.getRange('A1:T1').format={fill:panel,font:{name:'Aptos',color:'#FFFFFF',bold:true},rowHeightPx:48};helper.getRange('A2:T7').format.rowHeightPx=45;
box(helper,'A10:N12','Chart inputs link to research tables. Classification counts describe selected care items, not the frequency or prevalence of gender bias. Drug shares count plan segments equally; PA shares condition on listing. Procedure differences are illustrative and unadjusted.',pale,ink,11);

const cards=[['B',5,6,8,'CARE ITEMS','N2','Selected item–indication rows'],['F',5,6,8,'SCIENTIFIC STUDIES','N3','Including conflicting findings'],['J',5,6,8,'ITEMS WITH STUDIES','N4','Linked by stable study IDs'],['N',5,6,8,'POLICY-ONLY ITEMS','N5','Literature gaps remain'],['B',10,11,13,'COVERED WITH CONDITIONS','B2','Eligibility rules still apply'],['F',10,11,13,'PLAN DEPENDENT','B3','Product or plan review needed'],['J',10,11,13,'EXCLUDED FOR THIS USE','B4','See indication and policy scope'],['N',10,11,13,'LOCAL OR UNRESOLVED','N6','No blanket coverage inference']];
for(const [c,lr,vr,nr,label,ref,note] of cards){
  const c0=c.charCodeAt(0)-65,last=col(c0+3);dash.getRange(`${c}${lr}:${last}${nr}`).format.fill='#152D42';
  value(dash,`${c}${lr}`,label);dash.getRange(`${c}${lr}`).format.font={name:'Aptos',size:10,bold:true,color:'#B6C7D6'};
  formula(dash,`${c}${vr}`,`='_Chart Helpers'!${ref}`);dash.getRange(`${c}${vr}`).setNumberFormat('#,##0');dash.getRange(`${c}${vr}`).format.font={name:'Aptos',size:28,bold:true,color:'#FFFFFF'};
  dash.getRange(`${c}${nr}:${last}${nr}`).unmerge();box(dash,`${c}${nr}:${last}${nr}`,note,'#152D42','#ABC0D1',10);
  dash.getRange(`${c}${nr}:${last}${nr}`).format.horizontalAlignment='left';
}
value(dash,'B15','COVERAGE CLASSIFICATIONS IN THIS INVENTORY');value(dash,'J15','SELECTED FORMULARY LISTING SHARES');
value(dash,'B29','PRIOR AUTHORIZATION AMONG LISTING SEGMENTS');value(dash,'J29','ILLUSTRATIVE WORK-RVU DIFFERENCES');
for(const r of [15,29,43])dash.getRange(`B${r}:Q${r}`).format={fill:panel,font:{name:'Aptos',size:11,color:'#FFFFFF',bold:true}};
function chart(range,title,from,to,percent,color){
  const ch=dash.charts.add('bar',{title,barOptions:{direction:'bar',grouping:'clustered',gapWidth:70},hasLegend:false});ch.setData(helper.getRange(range));ch.setPosition(from,to);ch.title=title;
  ch.titleTextStyle.fontSize=14;ch.titleTextStyle.typeface='Aptos';ch.hasLegend=false;
  ch.xAxis={axisType:'textAxis',tickLabelPosition:'low',textStyle:{typeface:'Aptos',fontSize:12}};
  ch.yAxis={numberFormatCode:percent?'0%':'0',numberFormatSourceLinked:false,textStyle:{typeface:'Aptos',fontSize:12}};
  ch.series.items[0].fill=color;
  return ch;
}
chart('A1:B6','Selected care items (count)','B16','I28',false,teal);
chart('D1:E7','At least one option listed','J16','Q28',true,teal);
chart('G1:H6','Every listed option requires PA','B30','I42',true,amber);
chart('J1:K6','Other versus gynecologic work RVU','J30','Q42',true,cyan);
value(dash,'B43','HOW TO READ THE EVIDENCE');
dash.getRange('B44:I52').unmerge();dash.getRange('B44:I52').clear({applyTo:'contents'});
const insights=[['Coverage','An eligible benefit may still require medical necessity or authorization.'],['Payment','RVU or fee differences require clinically comparable procedures.'],['Access','Low use or high cost does not independently prove denial or bias.'],['Uncertainty','Unresolved coverage is recorded explicitly for further review.']];
for(let i=0;i<4;i++){const rr=45+i*2;box(dash,`B${rr}:C${rr+1}`,insights[i][0],'#152D42','#FFFFFF',11);box(dash,`D${rr}:I${rr+1}`,insights[i][1],'#152D42','#C1D1DD',11);}
dash.getRange('J45:Q49').unmerge();box(dash,'J45:Q49','This is a starting evidence register. It does not enumerate every Medicare service or establish a nationwide causal estimate of gender bias. National rules, local rules, plan examples and clinical studies are kept distinct.','#152D42','#C1D1DD',12);
dash.getRange('J51:Q52').unmerge();box(dash,'J51:Q52','Care inventory: Data & Targets tab. Sources, study limitations and review methods: Literature tab.',panel,'#C1D1DD',11);
dash.getRange('B44:I44').format.borders={preset:'none'};
dash.getRange('B45:Q52').format.horizontalAlignment='left';

// Check that a real classification edit updates summaries, then restore it.
const coveredOriginal=helper.getRange('B2').values[0][0];
value(care,'C9','Plan dependent');
assert.equal(helper.getRange('B2').values[0][0],coveredOriginal-1);
value(care,'C9',items[0].status);

wb.recalculate();
const expected={items:items.length,studies:studies.length,statuses:Object.fromEntries(statuses.map(s=>[s,items.filter(x=>x.status===s).length])),withStudies:items.filter(x=>x.study_ids.length).length};
assert.equal(helper.getRange('N2').values[0][0],expected.items);
assert.equal(helper.getRange('N3').values[0][0],expected.studies);
assert.equal(helper.getRange('N4').values[0][0],expected.withStudies);
statuses.forEach((s,i)=>assert.equal(helper.getRange(`B${i+2}`).values[0][0],expected.statuses[s]));
assert(Math.abs(drug.getRange('D20').values[0][0]-39/5499)<1e-10);
assert(Math.abs(rvu.getRange('I9').values[0][0]-(13.03-11.83)/11.83)<1e-10);
console.log(JSON.stringify(expected));
console.log((await wb.inspect({kind:'table',range:"'_Chart Helpers'!M1:N6",include:'values,formulas',tableMaxRows:6,tableMaxCols:2,maxChars:3000})).ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:60},summary:'Final formula error scan',maxChars:5000});
console.log(errors.ndjson);
await fs.mkdir(out,{recursive:true});
const output=`${out}/Medicare_gender_care_evidence_register_2026-09-16.xlsx`;
await(await SpreadsheetFile.exportXlsx(wb)).save(output);
console.log(execFileSync('/Users/lgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',[`${support}/add_native_links.py`,output],{encoding:'utf8'}));
console.log(`EXPORTED ${output}`);
const renders=[['Literature','L8:O11','literature-sources']];
for(const [sheetName,range,file]of renders){const b=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(`${support}/${file}.png`,new Uint8Array(await b.arrayBuffer()));console.log(`RENDERED ${file}`);}
await fs.writeFile(`${support}/verification.json`,JSON.stringify({expected,output,errors:errors.ndjson,careEnd,litEnd,drugEnd,rvuEnd},null,2));
