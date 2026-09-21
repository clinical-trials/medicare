"""Archive targeted development-search extensions; no screening or eligibility decisions."""
import importlib.util,json,hashlib,gzip,datetime as dt,xml.etree.ElementTree as ET
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('archive_search',ROOT/'research/review_2026-09-21/run_pubmed.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.ARCHIVE=HERE/'search_extensions'
queries=[
 {'id':'PM-BONE-20260921-E1','purpose':'Targeted bone-testing extension after diagnostic miss PMID18302495; post hoc development amendment','query':'("Medicare"[Mesh] OR medicare[tiab]) AND ("Osteoporosis"[Mesh] OR "Bone Density"[Mesh] OR "Densitometry"[Mesh] OR osteoporos*[tiab] OR "bone mass measurement"[tiab] OR "bone mineral density"[tiab] OR DXA[tiab] OR DEXA[tiab])'},
 {'id':'PM-RXIT-20260921-E1','purpose':'Targeted health-IT translation extension following new entrepreneurship purpose; not a comprehensive technology review','query':'("Medicare"[Mesh] OR medicare[tiab]) AND ("real time benefit"[tiab] OR "real-time benefit"[tiab] OR "prescription benefit"[tiab] OR "electronic prescribing"[tiab] OR "e-prescribing"[tiab] OR ((drug*[tiab] OR medicat*[tiab] OR prescrib*[tiab]) AND ("decision support"[tiab] OR "price transparency"[tiab] OR "cost transparency"[tiab] OR "cost information"[tiab])))'}
]
m.ARCHIVE.mkdir(parents=True,exist_ok=True)
if not (m.ARCHIVE/'queries.json').exists():m.save_json(m.ARCHIVE/'queries.json',{'created_at_utc':m.now(),'searcher':'Codex AI assistant','status':'Pre-PRESS targeted development searches, not a completed formal search','eligibility_filters':'No age,language,sex,study-design or full-text filters','queries':queries})
base=set((ROOT/'research/review_2026-09-21/pubmed/current_unique_pmids.txt').read_text().splitlines())
results=[];all_ids=set()
for q in queries:
 r=m.search(q['query'],q['id']);ids=set(r['idlist']);assert int(r['count'])==len(ids)<9999
 (m.ARCHIVE/(q['id']+'.pmids.txt')).write_text('\n'.join(sorted(ids,key=int))+'\n')
 results.append({**q,'count':len(ids),'translation':r.get('querytranslation'),'warnings':r.get('warninglist',{}),'overlap_with_baseline':len(ids&base),'additional_to_baseline':len(ids-base),'id_sha256':hashlib.sha256((m.ARCHIVE/(q['id']+'.pmids.txt')).read_bytes()).hexdigest()})
 all_ids|=ids
new_ids=sorted(all_ids-base,key=int)
for offset in range(0,len(new_ids),200):
 part=new_ids[offset:offset+200];body=m.request('efetch.fcgi',{'id':','.join(part),'retmode':'xml'},f'additional_metadata_{offset:06d}.xml.gz')
 got={r.findtext('MedlineCitation/PMID') or r.findtext('BookDocument/PMID') for r in ET.fromstring(body)};assert got==set(part)
(m.ARCHIVE/'additional_unique_pmids.txt').write_text('\n'.join(new_ids)+'\n')
combined=base|all_ids;(m.ARCHIVE/'combined_unique_pmids.txt').write_text('\n'.join(sorted(combined,key=int))+'\n')
m.save_json(m.ARCHIVE/'manifest.json',{'completed_at_utc':m.now(),'queries':results,'baseline_unique_records':len(base),'extension_raw_hits':sum(x['count'] for x in results),'extension_unique_records':len(all_ids),'extension_overlap_with_baseline':len(all_ids&base),'new_unique_records':len(new_ids),'combined_unique_records':len(combined),'diagnostic_missed_record_18302495_retrieved': '18302495' in all_ids,'deduplication':'Exact PMID only; related reports and cohort overlap still pending','human_screened':0,'reporting_limit':'Targeted, post hoc development extensions; not PRESS reviewed or comprehensive multi-database search'})
print(json.dumps({'queries':[(x['id'],x['count'],x['additional_to_baseline']) for x in results],'new_unique_records':len(new_ids),'combined_unique_records':len(combined),'missing_bone_record_retrieved':'18302495' in all_ids},indent=2))
