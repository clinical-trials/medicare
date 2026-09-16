"""Add native URL relationships for the unsupported artifact-tool hyperlink feature.

All workbook cells, formulas, tables, charts and styling are authored by artifact-tool.
This bounded compatibility pass changes only source-cell hyperlink relationships.
"""
import sys
import zipfile
from pathlib import Path
from lxml import etree as ET

path = Path(sys.argv[1])
MAIN = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
DOCREL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ns = {'m': MAIN}
with zipfile.ZipFile(path) as z:
    files = {n: z.read(n) for n in z.namelist()}
strings = []
if 'xl/sharedStrings.xml' in files:
    strings = [''.join(si.itertext()) for si in ET.fromstring(files['xl/sharedStrings.xml']).findall(f'{{{MAIN}}}si')]
total = 0
following = {'printOptions','pageMargins','pageSetup','headerFooter','rowBreaks','colBreaks','customProperties','cellWatches','ignoredErrors','smartTags','drawing','legacyDrawing','legacyDrawingHF','picture','oleObjects','controls','webPublishItems','tableParts','extLst'}
for name in list(files):
    if not name.startswith('xl/worksheets/sheet') or not name.endswith('.xml'):
        continue
    tree = ET.fromstring(files[name])
    matches = []
    for cell in tree.findall('.//m:sheetData/m:row/m:c', ns):
        v = cell.find('m:v', ns)
        text = None
        if cell.get('t') == 's' and v is not None:
            text = strings[int(v.text)]
        elif cell.get('t') == 'inlineStr':
            text = ''.join(cell.find('m:is', ns).itertext())
        elif cell.get('t') == 'str' and v is not None:
            text = v.text
        if text and text.startswith(('https://', 'http://')) and '\n' not in text:
            matches.append((cell.get('r'), text))
    if not matches:
        continue
    relname = name.rsplit('/',1)[0] + '/_rels/' + name.rsplit('/',1)[1] + '.rels'
    relations = ET.fromstring(files[relname]) if relname in files else ET.Element(f'{{{REL}}}Relationships', nsmap={None:REL})
    used = {r.get('Id') for r in relations}
    links = tree.find(f'{{{MAIN}}}hyperlinks')
    if links is None:
        links = ET.Element(f'{{{MAIN}}}hyperlinks')
        pos = next((i for i,c in enumerate(tree) if ET.QName(c).localname in following),len(tree))
        tree.insert(pos,links)
    url_by_ref = dict(matches)
    rel_by_id = {r.get('Id'): r for r in relations}
    for existing_link in list(links):
        ref = existing_link.get('ref')
        rid = existing_link.get(f'{{{DOCREL}}}id')
        relation = rel_by_id.get(rid)
        if relation is not None and relation.get('Type') == DOCREL+'/hyperlink':
            if ref in url_by_ref:
                relation.set('Target',url_by_ref[ref])
            elif relation.get('Target','').startswith(('https://','http://')):
                links.remove(existing_link)
                relations.remove(relation)
    existing = {l.get('ref') for l in links}
    counter=1
    for ref,url in matches:
        if ref in existing:
            continue
        while f'rIdSource{counter}' in used:
            counter+=1
        rid=f'rIdSource{counter}';used.add(rid)
        ET.SubElement(relations,f'{{{REL}}}Relationship',Id=rid,Type=DOCREL+'/hyperlink',Target=url,TargetMode='External')
        ET.SubElement(links,f'{{{MAIN}}}hyperlink',ref=ref,attrib={f'{{{DOCREL}}}id':rid})
        total+=1
    files[name]=ET.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
    files[relname]=ET.tostring(relations,xml_declaration=True,encoding='UTF-8',standalone=True)
tmp=path.with_suffix('.tmp')
with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
    for name,data in files.items():
        z.writestr(name,data)
tmp.replace(path)
print(f'Added {total} native source hyperlinks.')
