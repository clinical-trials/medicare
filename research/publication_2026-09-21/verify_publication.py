"""Validate counts, bibliography, literal queries, source hashes and artifact structure.

This is a reproducibility check, not human eligibility review or risk-of-bias appraisal.
"""
from pathlib import Path
import csv,gzip,hashlib,json,re,shutil,zipfile
from collections import Counter
from lxml import etree as E
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OUT=ROOT/'outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
stats=read(HERE/'publication_build.json');stem=Path(stats['docx_path']).stem
pdf=HERE/'rendered'/f'{stem}.pdf';reader=PdfReader(pdf)
assert len(reader.pages)==27
page_text=[p.extract_text() or '' for p in reader.pages]
assert all(len(t)>400 for t in page_text), 'Unexpected nearly empty page'
alltext='\n'.join(page_text)
normalized_text=re.sub(r'\s+',' ',alltext)
assert '\ufffd' not in alltext
assert all(s in page_text[16] for s in ['drug*','medicat*','prescrib*','osteoporos*'])
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(stats['docx_path']) as z:
    doc=E.fromstring(z.read('word/document.xml'))
    paras=[''.join(p.itertext()) for p in doc.findall('.//w:p',ns)]
    for q in read(HERE/'search_extensions/queries.json')['queries']:
        assert q['query'] in paras, 'Search query characters changed in DOCX'
    assert len(doc.findall('.//w:tbl',ns))==3 # Two main tables + source-location supplement.
    assert len(doc.findall('.//w:drawing',ns))==2
    assert not doc.findall('.//w:pBdr',ns)
    assert not doc.findall('.//w:trHeight',ns)
assert stats['abstract_words_whitespace_count']<=200
assert stats['title_characters']<=100
assert stats['main_body_words_including_headings_and_stable_ids']<4000
metadata=read(ROOT/'research/bibliography_metadata.json')['records']
methods=read(ROOT/'research/methodology_references.json')['records']
assert len(metadata)==53 and len(methods)==11
for r in metadata+methods:
    assert r['metadata_status'].startswith('Verified'),r['id']
    assert str(r.get('pmid','')).isdigit(),r['id']
assert len({r['pmid'] for r in metadata+methods})==64
registry=read(ROOT/'research/reference_registry.json')
references={r['id']:r for k in ['scientific_references','methodology_references','retrieval_references','translational_references','policy_sources','clinical_guidance_sources'] for r in registry[k]}
assert len(references)==126
bib=(OUT/'Medicare_gender_care_bibliography.md').read_text()
ris=(OUT/'Medicare_gender_care_references.ris').read_text()
entries={re.search(r'^ID  - (.+)$',s,re.M).group(1):s for s in ris.split('TY  - ')[1:]}
assert len(entries)==126
for r in metadata+methods:
    assert f'AN  - {r["pmid"]}' in entries[r['id']]
    assert f'PMID {r["pmid"]}' in bib
for rid in stats['printed_reference_ids']:
    assert rid in references
    r=references[rid]
    if r.get('pmid'):assert f'PMID {r["pmid"]}' in normalized_text,rid
scoped=read(ROOT/'research/scoped_evidence.json')
assert len(scoped['items'])==40 and len(scoped['studies'])==38
assert len(scoped['excludedStudies'])==8
assert len(read(ROOT/'research/clinical_basis.json')['translational_indications'])==8
assert len(read(HERE/'opportunities.json')['domains'])==6
assert read(ROOT/'research/translational_evidence.json')['independent_new_study_families']==3
with gzip.open(HERE/'review_queue.csv.gz','rt') as f:queue=list(csv.DictReader(f))
assert len(queue)==59147 and len({r['pmid'] for r in queue})==59147
review_states=Counter(r['human_review_status'] for r in queue)
assert set(review_states)=={'Awaiting independent human screening'}
abstracts=sum(r['has_abstract']=='True' for r in queue)
assert abstracts==47152,abstracts
payloads=[]
for sidecar in (HERE/'search_extensions/raw').glob('*.request.json'):
    raw=Path(str(sidecar).removesuffix('.request.json'));info=read(sidecar)
    assert sha(raw)==info['stored_sha256']
    content=gzip.decompress(raw.read_bytes()) if raw.suffix=='.gz' else raw.read_bytes()
    assert hashlib.sha256(content).hexdigest()==info['sha256']
    assert len(content)==info['bytes']
    payloads.append(str(raw.relative_to(ROOT)))
assert len(payloads)==5
workbooks={}
sns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
for name in ['Medicare_health_IT_opportunity_assessment_2026-09-21.xlsx','Medicare_gender_care_evidence_register_2026-09-16.xlsx']:
    path=OUT/name
    with zipfile.ZipFile(path) as z:
        errors=[];links=0;formulas=0
        for f in z.namelist():
            if re.match(r'xl/worksheets/sheet\d+\.xml$',f):
                xml=E.fromstring(z.read(f));errors.extend(xml.findall('.//s:c[@t="e"]',sns));links+=len(xml.findall('.//s:hyperlink',sns));formulas+=len(xml.findall('.//s:f',sns))
        assert not errors,name
        if name.startswith('Medicare_health_IT'):
            assert links==85 and formulas==0
            assert len(E.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',sns))==7
            assert b'HYPERLINK is not implemented' not in b''.join(z.read(f) for f in z.namelist() if f.endswith('.xml'))
    workbooks[name]={'sha256':sha(path),'native_hyperlinks':links,'formulas':formulas,'error_cells':0}
wbcheck=OUT/'opportunity_workbook_previews/verification.json'
shutil.copyfile(wbcheck,HERE/'opportunity_workbook_verification.json')
for name,expected in read(wbcheck)['source_sha256'].items():assert sha(ROOT/name)==expected,name
qa={str(n):sha(HERE/'rendered'/f'page-{n}.png') for n in range(1,28)}
result={'verified_on':'2026-09-21','verification_type':'Artifact and source consistency, not completed scientific review',
 'pdf_pages':27,'main_words':stats['main_body_words_including_headings_and_stable_ids'],'abstract_words':199,
 'main_tables':2,'main_figures':2,'printed_references':59,'canonical_references':126,
 'scientific_metadata':53,'methodology_metadata':11,'numeric_verified_pmids':64,
 'queue_records':59147,'with_abstract':abstracts,'without_abstract':len(queue)-abstracts,
 'human_review_states':dict(review_states),'extension_payloads_hash_verified':payloads,
 'literal_docx_queries_verified':True,'pdf_wildcards_verified':True,
 'docx_sha256':sha(Path(stats['docx_path'])),'rendered_pdf_sha256':sha(pdf),
 'workbooks':workbooks,'page_png_sha256':qa,
 'visual_review_logs':['visual_qa_pages_2_8.json','visual_qa_pages_13_27.json'],
 'root_visual_review_pages':[1,9,10,11,12,26],
 'final_visual_correction':'Root rechecked page 26 after removing empty policy-organization punctuation; all other previously reviewed pages remain unchanged after that correction.',
 'scientific_limitations':'No completed independent human screening, eligibility adjudication, formal appraisal or certainty assessment. Clinical and commercial hypotheses remain unvalidated.'}
(HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['page_png_sha256','extension_payloads_hash_verified','workbooks']},indent=2))
