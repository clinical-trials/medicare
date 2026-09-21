# Exercises only the real parser loop in memory; does not run main or write exports.
# Regression target: restoring journal-only title/date/identifier paths must fail.
import ast,gzip,json,re,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
HERE=ROOT/'research/review_2026-09-21'
source=(HERE/'prepare_search.py').read_text()
tree=ast.parse(source)
main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
loop=next(n for n in main.body if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='path')
namespace={'gzip':gzip,'json':json,'re':re,'ET':ET,'Path':Path,'ROOT':ROOT,'records':[],'paths':sorted((HERE/'pubmed/raw').glob('priority_metadata_*.xml')),'old':{},'core':set(),'supp':set()}
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name not in ['main','write_csv']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),str(HERE/'prepare_search.py'),'exec'),namespace)
exec(compile(ast.Module(body=[loop],type_ignores=[]),str(HERE/'prepare_search.py'),'exec'),namespace)
rows={r['pmid']:r for r in namespace['records']}
book=rows['22379646']
assert book['title'].startswith("Saving Women's Lives:"), f"Book title lost: {book['title']!r}"
assert book['year']==2005,book
assert book['doi']=='10.17226/11156',book
assert book['document_type']=='book',book
assert 'Institute of Medicine' in book['authors'],book
assert book['publisher']=='National Academies Press (US)',book
chapter=rows['21249787']
assert 'Financial and Demographic Influences' in chapter['title'],chapter
assert chapter['document_type']=='book_chapter',chapter
assert chapter['book_title'].startswith('Advances in Patient Safety:'),chapter
assert chapter['year']==2005,chapter
assert chapter['authors']=='Bernard D; Encinosa WE',chapter
assert chapter['publisher']=='Agency for Healthcare Research and Quality (US)',chapter
books=[]
for f in namespace['paths']:
 for record in ET.fromstring(f.read_bytes()):
  if record.tag=='PubmedBookArticle':
   pmid=record.findtext('BookDocument/PMID'); b=rows[pmid]
   assert b['title'] and b['book_title'] and b['year'],(pmid,b)
   assert b['publication_types'],(pmid,'publication type missing')
   books.append(pmid)
assert len(books)==24,len(books)
old=json.loads((HERE/'pubmed/priority_records.json').read_text())
ignore={'existing_study_id','in_core','in_supplement'}
for row in old:
 if row['pmid'] in books: continue
 for key,value in row.items():
  if key not in ignore: assert rows[row['pmid']][key]==value,(row['pmid'],key,value,rows[row['pmid']][key])
print('PASS: 24 book records retain titles, dates and types; known chapter/book author/DOI cases pass; 6745 journal records unchanged in existing metadata fields.')
