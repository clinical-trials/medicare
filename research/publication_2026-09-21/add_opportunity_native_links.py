"""Compatibility pass: attach links without changing artifact-tool-authored cells.

Uses the same native OOXML relationship approach as research/workbook/add_native_links.py.
The parent explicitly authorized this pass for artifact-tool's unsupported hyperlink feature.
"""
import json
import posixpath
import sys
import zipfile
from pathlib import Path
from lxml import etree as ET

file = Path(sys.argv[1])
requested = json.loads(Path(sys.argv[2]).read_text())
MAIN = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
DOCREL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
with zipfile.ZipFile(file) as z:
    files = {n: z.read(n) for n in z.namelist()}
book = ET.fromstring(files['xl/workbook.xml'])
rels = ET.fromstring(files['xl/_rels/workbook.xml.rels'])
targets = {r.get('Id'): r.get('Target') for r in rels}
sheet_paths = {}
for sheet in book.find(f'{{{MAIN}}}sheets'):
    target = targets[sheet.get(f'{{{DOCREL}}}id')]
    sheet_paths[sheet.get('name')] = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join('xl', target))
following = {'printOptions','pageMargins','pageSetup','headerFooter','rowBreaks','colBreaks','customProperties','cellWatches','ignoredErrors','smartTags','drawing','legacyDrawing','legacyDrawingHF','picture','oleObjects','controls','webPublishItems','tableParts','extLst'}
changed = set()
for name, xml_path in sheet_paths.items():
    matches = [r for r in requested if r['sheet'] == name]
    if not matches:
        continue
    tree = ET.fromstring(files[xml_path])
    original_cells = ET.tostring(tree.find(f'{{{MAIN}}}sheetData'))
    rel_path = posixpath.join(posixpath.dirname(xml_path), '_rels', posixpath.basename(xml_path) + '.rels')
    relationships = ET.fromstring(files[rel_path]) if rel_path in files else ET.Element(f'{{{REL}}}Relationships', nsmap={None:REL})
    used = {r.get('Id') for r in relationships}
    links = tree.find(f'{{{MAIN}}}hyperlinks')
    if links is None:
        links = ET.Element(f'{{{MAIN}}}hyperlinks')
        tree.insert(next((i for i,c in enumerate(tree) if ET.QName(c).localname in following), len(tree)), links)
    for index, link in enumerate(matches, 1):
        assert tree.find(f'.//{{{MAIN}}}c[@r="{link["cell"]}"]') is not None
        assert link['url'].startswith(('https://', 'http://'))
        rid = f'rIdOpportunity{index}'
        while rid in used:
            rid += 'x'
        used.add(rid)
        ET.SubElement(relationships, f'{{{REL}}}Relationship', Id=rid, Type=DOCREL+'/hyperlink', Target=link['url'], TargetMode='External')
        ET.SubElement(links, f'{{{MAIN}}}hyperlink', ref=link['cell'], display=str(link['label']), attrib={f'{{{DOCREL}}}id':rid})
    assert ET.tostring(tree.find(f'{{{MAIN}}}sheetData')) == original_cells, 'Cell content changed'
    files[xml_path] = ET.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
    files[rel_path] = ET.tostring(relationships, xml_declaration=True, encoding='UTF-8', standalone=True)
    changed.update([xml_path, rel_path])
tmp = file.with_suffix('.tmp')
with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
    for name, data in files.items():
        z.writestr(name, data)
tmp.replace(file)
print(f'Attached {len(requested)} native hyperlinks; artifact-tool-authored cells unchanged.')
