"""Extract public CMS source tables from downloaded archives, preserving originals."""
from pathlib import Path
import csv, io, json, shutil, struct, zipfile, zlib

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'sources'
RAW.mkdir(parents=True, exist_ok=True)
tail = Path('/private/tmp/medicare-formulary-zip-tail.bin').read_bytes()
directory = zipfile.ZipFile(io.BytesIO(tail))
for archive in directory.infolist():
    if not archive.filename.startswith(('basic drugs', 'excluded drugs', 'plan information')):
        continue
    offset = archive.header_offset + 2294378643
    origin = 2294039815 if archive.filename.startswith('plan information') else 0
    part = 'plan' if origin else 'first'
    block = Path(f'/private/tmp/medicare-formulary-{part}.bin').read_bytes()
    pos = offset - origin
    header = struct.unpack_from('<4s5H3I2H', block, pos)
    assert header[0] == b'PK\x03\x04'
    start = pos + 30 + header[-2] + header[-1]
    payload = block[start:start + archive.compress_size]
    data = zlib.decompress(payload, -15) if archive.compress_type == 8 else payload
    assert len(data) == archive.file_size
    assert zlib.crc32(data) == archive.CRC
    inner = zipfile.ZipFile(io.BytesIO(data))
    for member in inner.infolist():
        if member.is_dir():
            continue
        target = RAW / Path(member.filename).name
        target.write_bytes(inner.read(member))
        print(target.name, target.stat().st_size, target.read_text(errors='replace')[:650])
frf = zipfile.ZipFile('/private/tmp/medicare-frf2026.zip')
print('FRF members', frf.namelist())
for member in frf.infolist():
    if not member.is_dir():
        target = RAW / Path(member.filename).name
        target.write_bytes(frf.read(member))
        print(target.name, target.stat().st_size)
shutil.copyfile('/private/tmp/medicare-partd-2024.csv', RAW / 'CMS_PartD_Spending_2024.csv')
shutil.copyfile('/private/tmp/medicare-rvu26c.zip', RAW / 'CMS_RVU26C_2026.zip')
catalog = json.loads(Path('/private/tmp/medicare-cms-data.json').read_text())
selected = [x for x in catalog['dataset'] if x['title'] in (
    'Medicare Part D Spending by Drug',
    'Monthly Prescription Drug Plan Formulary and Pharmacy Network Information')]
for x in selected:
    x['distribution'] = x['distribution'][:3]
(RAW / 'CMS_source_metadata.json').write_text(json.dumps(selected, indent=2))
