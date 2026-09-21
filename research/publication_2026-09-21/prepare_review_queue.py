"""Create an auditable computational queue. No record is excluded or human-screened."""
import csv,gzip,hashlib,json,re,xml.etree.ElementTree as ET
from collections import defaultdict,Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def tx(el):return ''.join(el.itertext()).strip() if el is not None else ''
with gzip.open(ROOT/'research/review_2026-09-21/pubmed/all_records.jsonl.gz','rt') as f: records=[json.loads(l) for l in f]
for p in sorted((HERE/'search_extensions/raw').glob('additional_metadata_*.xml.gz')):
 for el in ET.fromstring(gzip.decompress(p.read_bytes())):
  a=el.find('MedlineCitation/Article');book=a is None
  if book:a=el.find('BookDocument')
  pmid=el.findtext('BookDocument/PMID' if book else 'MedlineCitation/PMID');assert a is not None and pmid
  ids={e.get('IdType'):tx(e) for e in el.findall('BookDocument/ArticleIdList/ArticleId' if book else 'PubmedData/ArticleIdList/ArticleId')}
  authors=[tx(e.find('CollectiveName')) or (tx(e.find('LastName'))+' '+tx(e.find('Initials'))).strip() for e in a.findall('AuthorList/Author')]
  date_path='Book/PubDate' if book else 'Journal/JournalIssue/PubDate'
  year=tx(a.find(date_path+'/Year')) or tx(a.find(date_path+'/MedlineDate'))[:4]
  records.append({'record_id':'R-'+pmid,'pmid':pmid,'title':tx(a.find('ArticleTitle')) or tx(a.find('Book/BookTitle')),'authors':'; '.join(authors),'year':year,'journal':tx(a.find('Journal/Title')),'doi':ids.get('doi',''),'pmcid':ids.get('pmc',''),'abstract':'\n'.join((e.get('Label','')+': ' if e.get('Label') else '')+tx(e) for e in a.findall('Abstract/AbstractText')),'publication_types':'; '.join(tx(e) for e in a.findall('PublicationTypeList/PublicationType')),'source_url':f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/','raw_xml':str(p.relative_to(ROOT)),'in_core':False,'in_supplement':False,'document_type':('book_chapter' if tx(a.find('ArticleTitle')) else 'book') if book else 'journal_article','book_title':tx(a.find('Book/BookTitle')) if book else '', 'publisher':tx(a.find('Book/Publisher/PublisherName')) if book else '','status':'Awaiting independent human title/abstract screening'})
assert len(records)==len({r['pmid'] for r in records})==59147
base=set((ROOT/'research/review_2026-09-21/pubmed/current_unique_pmids.txt').read_text().splitlines())
bone=set((HERE/'search_extensions/PM-BONE-20260921-E1.pmids.txt').read_text().splitlines())
rx=set((HERE/'search_extensions/PM-RXIT-20260921-E1.pmids.txt').read_text().splitlines())
rules={
 'medicare':r'\bmedicare\b',
 'sex_or_gender':r'\b(sex|gender|female\w*|male\w*|women|woman|men|man)\b',
 'patient_costs':r'out.of.pocket|cost.related|cost.sharing|affordab|copay|co.pay|coinsurance|nonadher',
 'service_valuation':r'relative value|\brvus?\b|fee schedule|reimburse|\bpayment',
 'bone_care':r'osteopor|fragility fracture|bone mass|bone mineral|\bdxa\b|\bdexa\b',
 'health_it':r'decision support|electronic prescrib|e.prescrib|real.time benefit|price transparency|cost transparency|portal|interoperab|prior authoriz',
 'transgender_focus_signal':r'transgender|gender.affirm|gender.diverse|gender dysphor'}
compiled={k:re.compile(v,re.I) for k,v in rules.items()}
bydoi=defaultdict(list);bytitle=defaultdict(list)
for r in records:
 if r.get('doi'):bydoi[r['doi'].lower().strip()].append(r['pmid'])
 title=re.sub(r'\W+','',r['title'].lower())
 if title:bytitle[title].append(r['pmid'])
rows=[]
for r in records:
 text=r['title']+'\n'+r['abstract'];flags={k:bool(v.search(text)) for k,v in compiled.items()}
 if flags['medicare'] and flags['sex_or_gender'] and (flags['patient_costs'] or flags['service_valuation']):queue='A Medicare sex and cost or valuation signals'
 elif flags['medicare'] and (flags['bone_care'] or flags['health_it']):queue='B Medicare bone or health IT signals'
 elif flags['sex_or_gender'] and flags['service_valuation']:queue='C Sex and valuation signals without Medicare text'
 elif not r['abstract']:queue='D No abstract requires retrieval judgment'
 else:queue='E All other retrieved records retained'
 d=r.get('doi','').lower().strip();t=re.sub(r'\W+','',r['title'].lower())
 rows.append({'record_id':r['record_id'],'pmid':r['pmid'],'title':r['title'],'year':r['year'],'journal':r.get('journal',''),'doi':r.get('doi',''),'pmcid':r.get('pmcid',''),'queue':queue,**flags,'in_baseline':r['pmid'] in base,'in_bone_extension':r['pmid'] in bone,'in_rxit_extension':r['pmid'] in rx,'has_abstract':bool(r['abstract']),'same_doi_pmids':';'.join(p for p in bydoi.get(d,[]) if p!=r['pmid']),'same_normalized_title_pmids':';'.join(p for p in bytitle.get(t,[]) if p!=r['pmid']),'human_review_status':'Awaiting independent human screening','source_url':r['source_url'],'raw_xml':r['raw_xml']})
rows.sort(key=lambda r:(r['queue'],hashlib.sha256(('queue-20260921:'+r['pmid']).encode()).hexdigest()))
with gzip.open(HERE/'review_queue.csv.gz','wt',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
with gzip.open(HERE/'extension_records.jsonl.gz','wt',encoding='utf-8') as f:
 for r in records:
  if r['pmid'] not in base:f.write(json.dumps(r,ensure_ascii=False)+'\n')
duplicates=[{'type':'same DOI','key':k,'pmids':v,'status':'Candidate report relationship; not automatically merged'} for k,v in bydoi.items() if len(v)>1]+[{'type':'same normalized title','key':k,'pmids':v,'status':'Candidate report relationship; not automatically merged'} for k,v in bytitle.items() if len(v)>1]
(HERE/'report_relationship_candidates.json').write_text(json.dumps(duplicates,ensure_ascii=False,indent=2)+'\n')
summary={'date':'2026-09-21','records':len(rows),'rules':rules,'queue_counts':dict(Counter(r['queue'] for r in rows)),'abstracts':sum(r['has_abstract'] for r in rows),'no_abstracts':sum(not r['has_abstract'] for r in rows),'same_doi_groups':sum(len(v)>1 for v in bydoi.values()),'same_title_groups':sum(len(v)>1 for v in bytitle.values()),'human_screened':0,'records_excluded':0,'auto_merged':0,'scope_decisions':0,'limitations':'Keyword ordering has not been validated for sensitivity or fairness; demographic mentions can be incidental. No queue tier is an exclusion. Transgender keyword flags do not themselves establish focus or participant identity. Same DOI/title may be distinct reports or notices; human adjudication is required.'}
(HERE/'queue_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='rules'},indent=2))
