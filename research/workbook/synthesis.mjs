import fs from 'node:fs/promises';
import assert from 'node:assert/strict';

const root='/Users/lgm/Documents/ChatGPT/Medicare';
const out=`${root}/outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8`;
const support=`${root}/research/workbook`;

export async function addSynthesis(wb,{studies,items}){
  const spec=JSON.parse(await fs.readFile(`${root}/research/preliminary_synthesis.json`,'utf8'));
  const meta=JSON.parse(await fs.readFile(`${root}/research/bibliography_metadata.json`,'utf8'));
  const registry=JSON.parse(await fs.readFile(`${root}/research/reference_registry.json`,'utf8'));
  const fm=JSON.parse(await fs.readFile(`${root}/research/formulary_results.json`,'utf8'));
  const pairs=JSON.parse(await fs.readFile(`${root}/research/procedure_pairs_2026.json`,'utf8'));
  const byId=new Map(meta.records.map(x=>[x.id,x]));
  const policies=new Map(registry.policy_sources.map(x=>[x.id,x]));
  const active=new Set(studies.map(x=>x.id));active.add('L-B01-E1');
  const allReferences=new Set();
  for(const p of spec.patterns)for(const id of [...p.study_ids,...p.policy_ids])allReferences.add(id);
  for(const h of spec.hypotheses)for(const id of [...h.evidence_ids,...h.counter_ids,...h.policy_ids])allReferences.add(id);
  for(const id of allReferences){
    assert(byId.has(id)||policies.has(id),`Unknown synthesis citation ${id}`);
    if(byId.has(id)){assert(active.has(id),`Out-of-scope synthesis article ${id}`);assert(/^\d+$/.test(byId.get(id).pmid),`Missing PMID ${id}`);}
  }
  assert.equal(new Set(spec.hypotheses.map(x=>x.id)).size,spec.hypotheses.length);
  const cite=id=>byId.has(id)?`[${id}; PMID ${byId.get(id).pmid}](https://pubmed.ncbi.nlm.nih.gov/${byId.get(id).pmid}/)`:`[${id}](${policies.get(id).url})`;
  const citeMany=ids=>ids.map(cite).join('; ');
  const pmids=ids=>[...new Set(ids)].map(id=>`${id}: ${byId.get(id).pmid}`).join('; ');
  const navy='#102332',panel='#19354D',ink='#243B50',pale='#EDF4F8';
  const box=(s,r,value,fill=navy,color='#FFFFFF',size=11)=>{s.getRange(r).unmerge();s.getRange(r).merge();s.getRange(r).values=[[value]];s.getRange(r).format={fill,font:{name:'Aptos',size,color,bold:true},wrapText:true,verticalAlignment:'center'};};
  const put=(s,r,value)=>s.getRange(r).values=[[value]];
  const form=(s,r,value)=>s.getRange(r).formulas=[[value]];

  // This is a separate hypothesis unit, not an addition to the study inventory.
  let sheet;try{sheet=wb.worksheets.getItem('Hypotheses');}catch{sheet=wb.worksheets.add('Hypotheses');}sheet.showGridLines=false;sheet.tabColor=panel;
  const oldNotes=new Map(sheet.getRange('A9:R50').values.filter(r=>r[0]).map(r=>[r[0],r[17]||'']));
  const headers=['Hypothesis ID','Evidence stream','Proposed hypothesis','Observed pattern / limits','Proposed test','What would weaken it','Analysis readiness','Research priority','Population and need','Exposure','Comparator','Primary / secondary outcomes','Alternative explanations','Next step','Supporting / motivating studies','Counterevidence / qualification','PMIDs (study ID: PMID)','Research notes','Policy source IDs'];
  const rows=spec.hypotheses.map(h=>[h.id,h.stream,h.statement,h.evidence_summary,h.test,h.weakens,h.readiness,h.priority,h.population,h.exposure,h.comparator,h.outcome,h.alternatives,h.next_step,h.evidence_ids.join(', '),h.counter_ids.join(', ')||'No direct counter-study extracted; see alternative explanations',pmids([...h.evidence_ids,...h.counter_ids]),oldNotes.get(h.id)||'',h.policy_ids.join(', ')||'No direct policy estimate attached']);
  const end=8+rows.length;
  const oldTable=sheet.tables.items.find(x=>x.name==='ResearchHypotheses');if(oldTable)oldTable.delete();
  sheet.getRange('A8:S50').clear({applyTo:'contents'});
  sheet.getRange(`A8:S${end}`).values=[headers,...rows];
  const table=sheet.tables.add(`A8:S${end}`,true,'ResearchHypotheses');table.style='TableStyleMedium2';table.showFilterButton=true;
  sheet.getRange(`A8:S${end}`).format={font:{name:'Aptos',size:11,color:ink},wrapText:true,verticalAlignment:'top'};
  const widths=[100,165,390,610,460,420,310,180,370,340,390,420,410,430,190,250,360,330,190];
  widths.forEach((w,i)=>sheet.getRange(`${String.fromCharCode(65+i)}:${String.fromCharCode(65+i)}`).format.columnWidthPx=w);
  sheet.getRange('A8:S8').format={fill:panel,font:{name:'Aptos',size:11,bold:true,color:'#FFFFFF'},rowHeightPx:55,wrapText:true,verticalAlignment:'center'};
  for(let r=9;r<=end;r++){sheet.getRange(`A${r}:S${r}`).format.fill=r%2?'#FFFFFF':'#F2F6F9';sheet.getRange(`A${r}:S${r}`).format.rowHeightPx=170;}
  sheet.getRange(`R9:R${end}`).format.fill='#FFF4D6';
  box(sheet,'A1:F2','Preliminary synthesis and testable hypotheses',navy,'#FFFFFF',22);
  box(sheet,'A3:F4',`${spec.created_on}. Hypotheses generated from the selected register; causal tests have not been completed. Patient, physician and service comparisons remain separate.`,pale,ink);
  box(sheet,'A5:F6','Define clinical need independently of coverage. Retain null and reversed findings. Use the linked study IDs and PMIDs to inspect evidence; notes in column R are editable.',pale,ink);
  sheet.freezePanes.freezeRows(8);sheet.freezePanes.freezeColumns(2);

  // Derived three-state composition retains the original plan-segment denominator.
  const drug=wb.worksheets.getItem('Drug formularies');
  const sourceRows=drug.getRange('A9:K21').values;
  const index=new Map(sourceRows.map((r,i)=>[r[0],i+9]));
  drug.getRange('M8:T21').values=[['Formulation (same row as A)','No matched listing (n)','No listing share','Listed; all options PA/ST (n)','All options PA/ST share','At least one option without PA/ST (n)','Option without PA/ST share','Interpretation'],...Array.from({length:13},()=>Array(8).fill(null))];
  drug.getRange('M8:T21').format={font:{name:'Aptos',size:11,color:ink},wrapText:true,verticalAlignment:'top'};
  [['M',300],['N',150],['O',150],['P',185],['Q',175],['R',205],['S',175],['T',440]].forEach(([c,w])=>drug.getRange(`${c}:${c}`).format.columnWidthPx=w);
  drug.getRange('M8:T8').format={fill:panel,font:{name:'Aptos',size:11,color:'#FFFFFF',bold:true},wrapText:true,verticalAlignment:'center'};
  box(drug,'M3:T4','Three mutually exclusive states per formulation: no matched listing; listed but every option requires PA and/or ST; or at least one listed option without either flag. Shares use all analyzed plan segments.',pale,ink);
  box(drug,'M5:T6','These are administrative flags, not clinical suitability, paid claims or beneficiary exposure. An option without PA/ST may have quantity limits and costs. Formularies recur across segments; do not sum rows across drugs.',pale,ink);
  const distributions=[];
  for(const r of fm.results){
    const rr=index.get(r.group);assert(rr,`Missing formulary row ${r.group}`);
    const n=r.plan_segments_total,l=r.plan_segments_listed,u=r.plan_segments_with_at_least_one_option_with_neither_PA_nor_ST;
    assert(n>=l&&l>=u&&u>=0);
    const d={group:r.group,total:n,no_matched_listing:n-l,listed_all_options_PA_or_ST:l-u,at_least_one_option_without_PA_ST:u};
    distributions.push(d);
    form(drug,`M${rr}`,`=A${rr}`);form(drug,`N${rr}`,`=B${rr}-C${rr}`);form(drug,`O${rr}`,`=N${rr}/B${rr}`);
    form(drug,`P${rr}`,`=C${rr}-H${rr}`);form(drug,`Q${rr}`,`=P${rr}/B${rr}`);form(drug,`R${rr}`,`=H${rr}`);form(drug,`S${rr}`,`=R${rr}/B${rr}`);
    put(drug,`T${rr}`,'Same CMS source as column J. No matched listing does not rule out an exception. PA/ST requirements need clinical and policy review.');
    for(const [c,expected] of [['N',d.no_matched_listing],['P',d.listed_all_options_PA_or_ST],['R',d.at_least_one_option_without_PA_ST]])assert.equal(drug.getRange(`${c}${rr}`).values[0][0],expected);
    assert.equal(d.no_matched_listing+d.listed_all_options_PA_or_ST+d.at_least_one_option_without_PA_ST,n);
  }
  // Do not turn missing PA/ST data in the supplementary paroxetine row into zero.
  form(drug,'M21','=A21');form(drug,'N21','=B21-C21');form(drug,'O21','=N21/B21');
  for(const c of ['P','Q','R','S'])put(drug,`${c}21`,'Not extracted');
  put(drug,'T21','Supplementary paroxetine row: listing is known; PA/ST states remain unavailable.');
  for(const c of ['N','P','R'])drug.getRange(`${c}9:${c}21`).setNumberFormat('#,##0');
  for(const c of ['O','Q','S'])drug.getRange(`${c}9:${c}21`).setNumberFormat('0.0%');
  for(let r=9;r<=21;r++)drug.getRange(`M${r}:T${r}`).format.fill=r%2?'#FFFFFF':'#F2F6F9';
  const changed=index.get('Fezolinetant / Veozah'),base=drug.getRange(`H${changed}`).values[0][0];
  put(drug,`H${changed}`,base+1);assert.equal(drug.getRange(`P${changed}`).values[0][0],2380-base-1);assert.equal(drug.getRange(`R${changed}`).values[0][0],base+1);put(drug,`H${changed}`,base);

  const dash=wb.worksheets.getItem('Dashboard');
  dash.getRange('B97:Q124').unmerge();dash.getRange('B97:Q124').clear({applyTo:'contents'});
  dash.getRange('B97:Q124').format={fill:navy,font:{name:'Aptos',size:12,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center',rowHeightPx:25};
  box(dash,'B97:Q97','PRELIMINARY PATTERNS AND HYPOTHESES',panel,'#FFFFFF',14);dash.getRange('B97:Q97').format.rowHeightPx=36;
  box(dash,'B98:Q100',spec.central_hypothesis,navy,'#C1D1DD',12);
  for(let i=0;i<spec.patterns.length;i++){
    const p=spec.patterns[i],r=101+i*3,fill=i%2?panel:'#152D42';
    box(dash,`B${r}:F${r+2}`,p.title,fill,'#FFFFFF',11);box(dash,`G${r}:Q${r+2}`,p.dashboard,fill,'#C1D1DD',12);
  }
  box(dash,'B120:I123','Next: audit clinically suitable formulations within plans and expand the full procedure-pair comparison. These are descriptive steps before patient-level causal tests.',panel,'#C1D1DD',12);
  box(dash,'J120:Q123',`${spec.hypotheses.length} hypotheses are detailed on the Hypotheses tab, with PMIDs, alternative explanations and findings that would weaken each claim. None is a confirmed causal result.`,panel,'#C1D1DD',12);

  const selected=distributions.filter(x=>!x.group.includes('any single-ingredient'));
  const pct=(v,n)=>(100*v/n).toFixed(1)+'%';
  const nformat=n=>n.toLocaleString('en-US');
  const report=['# Medicare sex/gender equity: preliminary synthesis and hypotheses','',`Version ${spec.version} | ${spec.updated_on||spec.created_on} | ${spec.status}.`,'',
    `**Working thesis:** ${spec.central_hypothesis}`,'',
    `${spec.method} The source set contains ${items.length} care-item rows and ${studies.length} active literature records. The hypothesis numbers below are research propositions, not additional studies.`,'',
    `The organizing clinical review is ${cite(spec.anchor_study_id)}; retain its correction ${cite(spec.anchor_correction_id)}. It supports a framework for clinical need and sex/gender mechanisms, rather than a direct Medicare payment conclusion.`,'',
    '## Patterns in the current evidence',''];
  for(const p of spec.patterns)report.push(`### ${p.id}. ${p.title}`,'',`**Observed:** ${p.observation}`,'',`**Interpretation to investigate:** ${p.interpretation}`,'',`**Limit:** ${p.boundary}`,'',`Sources: ${citeMany([...p.study_ids,...p.policy_ids])}.`,'');
  report.push('## A descriptive result from the existing formulary data','',
    'The table below re-expresses the existing CMS snapshot using one denominator for each formulation. It does not test clinical suitability or a sex effect. Counts are not enrollment weighted, and the same formulary may appear in several plan segments. Percentages are rounded independently; do not sum across drug rows. PA means prior authorization; ST means step therapy.','',
    '| Formulation | No matched listing, n (%) | Listed, every option has PA/ST, n (%) | At least one listed option without PA/ST, n (%) | Denominator |',
    '|---|---:|---:|---:|---:|',
    ...selected.map(d=>`| ${d.group} | ${nformat(d.no_matched_listing)} (${pct(d.no_matched_listing,d.total)}) | ${nformat(d.listed_all_options_PA_or_ST)} (${pct(d.listed_all_options_PA_or_ST,d.total)}) | ${nformat(d.at_least_one_option_without_PA_ST)} (${pct(d.at_least_one_option_without_PA_ST,d.total)}) | ${nformat(d.total)} |`),'',
    `Calculations: no listing = total minus listed; every option has PA/ST = listed minus segments with an option free of both flags. The source contains ${fm.metadata.formularies_used} formularies across ${nformat(fm.metadata.unsuppressed_unique_plan_segments)} segments; ${fm.metadata.suppressed_plan_segments_excluded} suppressed segments were excluded. Source release ${fm.metadata.formulary_release}, retrieved ${fm.metadata.retrieved}. ${citeMany(['P-002','P-034','P-037','P-038'])}.`,'',
    'An option without PA/ST can still have quantity limits, high cost or an unsuitable dose. Nonlisting is not proof that an exception was denied. The supplementary paroxetine row is excluded from this three-state table because PA/ST were not extracted. Testosterone is a counterexample to a simple female-only restriction story, not a clinical substitute for menopausal therapy. Fezolinetant safety monitoring must be considered when evaluating restrictions.','',
    `The local 2026 procedure check includes ${pairs.pairs.length} selected pairs: ${pairs.pairs.filter(p=>p.higher_work_rvu==='male').length} have higher male-procedure work RVUs and ${pairs.pairs.filter(p=>p.higher_work_rvu==='female').length} have higher female-procedure work RVUs. This small purposive subset is a matching illustration, not an estimated national sex effect. ${citeMany(['P-035','P-036'])}.`,'',
    '## Testable hypotheses','',
    'All hypotheses were developed after viewing this evidence. Priorities describe the proposed research sequence, not certainty or importance scores. The outcome definitions, effect sizes of interest, windows and adjustment sets must be finalized before confirmatory testing.');
  for(const h of spec.hypotheses){
    report.push('',`### ${h.id}. ${h.title}`,'',`**${h.stream}. Hypothesis:** ${h.statement}`,'',
      `**Population:** ${h.population}`,'',`**Exposure and comparison:** ${h.exposure} ${h.comparator}`,'',`**Outcome:** ${h.outcome}`,'',
      `**Proposed test:** ${h.test}`,'',`**Alternative explanations:** ${h.alternatives}`,'',`**What would weaken it:** ${h.weakens}`,'',
      `**Readiness:** ${h.readiness}. **Priority:** ${h.priority}. **Next step:** ${h.next_step}`,'',
      `Motivating evidence: ${citeMany(h.evidence_ids)}. ${h.counter_ids.length?`Counterevidence or qualification: ${citeMany(h.counter_ids)}. `:''}${h.policy_ids.length?`Policy/data: ${citeMany(h.policy_ids)}.`:''}`);
  }
  report.push('','## Interpretation and design limits','',...spec.guardrails.map(x=>`- ${x}`),'','## Next analyses','');
  for(const a of spec.next_analyses)report.push(`${a.order}. **${a.action}** (${a.hypothesis_ids.join(', ')}). ${a.why}`,'');
  report.push('## Broader literature search','',spec.search_expansion,'','## Citation and audit trail','',
    `Study IDs and numeric PMIDs above resolve to the active register and its [living bibliography](./Medicare_gender_care_bibliography.md). No cited primary references from background reviews were automatically added. The current verified scientific metadata contain ${meta.records.length} records, including ${studies.length} active candidates/context records, eight scope-excluded papers, one correction and two separately logged retrieval references. Excluded studies and outside-register references do not supply the substantive synthesis.`,'',
    'The workbook retains the underlying records, a new Hypotheses tab, the dashboard pattern summary, and derived formulation states beside the existing Drug formularies inputs. The active population scope, patient/physician distinction and clinical anatomy/physiology classifications remain in force.','');
  await fs.writeFile(`${out}/Medicare_preliminary_synthesis_and_hypotheses_2026-09-16.md`,report.map(line=>line.trimEnd()).join('\n'));
  const analysis={updated_on:spec.updated_on||spec.created_on,stage:spec.status,active_studies:studies.length,care_items:items.length,hypotheses:spec.hypotheses.length,pattern_count:spec.patterns.length,formulary_source:fm.metadata,formulary_distributions:distributions,procedure_pair_count:pairs.pairs.length,reference_ids:[...allReferences].sort()};
  await fs.writeFile(`${root}/research/synthesis_analysis.json`,JSON.stringify(analysis,null,2)+'\n');
  for(const [sheetName,range,name] of [['Dashboard','B97:Q123','synthesis-dashboard'],['Hypotheses','A8:C11','hypotheses-opening'],['Hypotheses','E8:H10','hypotheses-tests'],['Drug formularies','M8:S14','formulary-states']]){
    const blob=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(`${support}/${name}.png`,new Uint8Array(await blob.arrayBuffer()));
  }
  return analysis;
}
