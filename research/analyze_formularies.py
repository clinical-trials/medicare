"""Reproducible descriptive CMS formulary screen; not a causal bias estimate."""
from collections import Counter, defaultdict
from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'sources'
def read(name, delimiter=','):
    with (RAW / name).open(encoding='cp1252' if name.endswith('.txt') else 'utf-8-sig', newline='') as f:
        yield from csv.DictReader(f, delimiter=delimiter)

reference = {r['RxCUI']: r for r in read('CY26 FRF_20260825.csv')}
def ingredient(r, name):
    return r['Related SCDC'].startswith(name + ' ') and ' / ' not in r['Related SCDC']
def estradiol_form(r, form):
    return ingredient(r, 'ESTRADIOL') and r['TTY'] == 'SCD' and r['Related DF'] == form
groups = {
    'Estradiol: any single-ingredient form, generic or brand': lambda r: ingredient(r, 'ESTRADIOL'),
    'Generic estradiol: oral tablet': lambda r: estradiol_form(r, 'ORAL TABLET'),
    'Generic estradiol: vaginal cream': lambda r: estradiol_form(r, 'VAGINAL CREAM'),
    'Generic estradiol: vaginal insert': lambda r: estradiol_form(r, 'VAGINAL INSERT'),
    'Generic estradiol: transdermal patch': lambda r: estradiol_form(r, 'TRANSDERMAL SYSTEM'),
    'Generic estradiol: topical gel': lambda r: estradiol_form(r, 'TOPICAL GEL'),
    'Estring brand': lambda r: r['Related BN'] == 'ESTRING',
    'Testosterone: any single-ingredient form, generic or brand': lambda r: ingredient(r, 'TESTOSTERONE'),
    'Generic testosterone: topical gel': lambda r: ingredient(r, 'TESTOSTERONE') and r['TTY'] == 'SCD' and r['Related DF'] == 'TOPICAL GEL',
    'Fezolinetant / Veozah': lambda r: ingredient(r, 'FEZOLINETANT'),
    'Ospemifene / Osphena': lambda r: ingredient(r, 'OSPEMIFENE'),
    'Prasterone / Intrarosa': lambda r: ingredient(r, 'PRASTERONE'),
}
membership = {rid: [name for name, predicate in groups.items() if predicate(r)] for rid,r in reference.items()}
plans = {}
raw_plan_rows = 0
suppressed = set()
for r in read('plan information  20260831.txt', '|'):
    raw_plan_rows += 1
    key = (r['CONTRACT_ID'],r['PLAN_ID'],r['SEGMENT_ID'])
    if r['PLAN_SUPPRESSED_YN'] != 'N':
        suppressed.add(key)
        continue
    fid = r['FORMULARY_ID'].strip()
    if key in plans:
        assert plans[key] == fid, (key, plans[key], fid)
    plans[key] = fid
fid_counts = Counter(plans.values())
formulary_present = set()
flags = {name: defaultdict(list) for name in groups}
matched_rows = []
basic_rows = 0
unmapped = Counter()
all_ids = set()
for r in read('basic drugs formulary file  20260831.txt', '|'):
    basic_rows += 1
    fid, rid = r['FORMULARY_ID'],r['RXCUI']
    formulary_present.add(fid)
    all_ids.add(rid)
    if rid not in reference:
        unmapped[rid] += 1
    for group in membership.get(rid, []):
        flags[group][fid].append(r)
    if membership.get(rid):
        matched_rows.append(dict(r, description=reference[rid]['RxNorm Description']))
missing_fids = {f:n for f,n in fid_counts.items() if f not in formulary_present}
assert not missing_fids, missing_fids
denom = len(plans)
out = []
for group in groups:
    by_fid = flags[group]
    covered = sum(fid_counts[f] for f in by_fid)
    no_pa = sum(fid_counts[f] for f,rows in by_fid.items() if any(r['PRIOR_AUTHORIZATION_YN']=='N' for r in rows))
    no_pa_st = sum(fid_counts[f] for f,rows in by_fid.items() if any(r['PRIOR_AUTHORIZATION_YN']=='N' and r['STEP_THERAPY_YN']=='N' for r in rows))
    out.append({'group':group,'reference_rxcuis':sum(group in v for v in membership.values()),
                'plan_segments_total':denom,'plan_segments_listed':covered,'listed_pct':round(100*covered/denom,2),
                'plan_segments_with_at_least_one_listed_option_without_PA':no_pa,
                'listed_plan_segments_all_options_PA':covered-no_pa,
                'all_options_PA_pct_of_listed':round(100*(covered-no_pa)/covered,2) if covered else None,
                'plan_segments_with_at_least_one_option_with_neither_PA_nor_ST':no_pa_st})
metadata = {'retrieved':'2026-09-16','formulary_release':'2026-08-26',
    'archive_url':'https://data.cms.gov/sites/default/files/2026-08/d8c9b393-66f0-4973-a748-f66742fe0fd2/2026_20260819.zip',
    'archive_members_date_label':'20260831','reference_date':'2026-08-25',
    'reference_url':'https://www.cms.gov/files/zip/cy-2026-august-formulary-reference-file.zip',
    'basic_rows':basic_rows,'basic_unique_rxcuis':len(all_ids),'unmatched_basic_rxcuis':len(unmapped),
    'unmatched_basic_rows':sum(unmapped.values()),'reference_rows':len(reference),
    'raw_plan_county_rows':raw_plan_rows,'unsuppressed_unique_plan_segments':denom,
    'unique_contract_plan_pairs':len({k[:2] for k in plans}),
    'suppressed_plan_segments_excluded':len(suppressed),'formularies_used':len(fid_counts),
    'missing_formularies':missing_fids,
    'limitations':['Plan-segment weighted, not enrollment weighted; county repetitions removed.',
        'Employer, PACE, demonstration (except included MMP), and non-Part-D plans excluded from CMS monthly public data.',
        'Listed means at least one reference-matched formulation/strength; not every dose or a guarantee of claim approval.',
        'PA flag does not identify age-specific or diagnosis-specific criteria.',
        'No patient cost, denied-claim, indication, clinical-need or gender-identity data.',
        'Missing formulary entries do not preclude approved exceptions.',
        'Reference IDs absent from August reference are not classified; target concept list retained for review.',
        'Hormone groups have different indications; between-group PA comparisons do not establish unfairness.']}
(ROOT / 'formulary_results.json').write_text(json.dumps({'metadata':metadata,'results':out},indent=2))
(ROOT / 'target_drug_reference.json').write_text(json.dumps([r for rid,r in reference.items() if membership[rid]],indent=2))
(ROOT / 'matched_formulary_rows.json').write_text(json.dumps(matched_rows,indent=2))
spending = list(read('CMS_PartD_Spending_2024.csv'))
selected_names = {'Estradiol*','Viagra','Sildenafil Citrate','Revatio','Testosterone','Veozah','Osphena','Intrarosa'}
cols = ['Brnd_Name','Gnrc_Name','Mftr_Name','Tot_Clms_2024','Tot_Benes_2024','Tot_Spndng_2024']
selected = [{k:r[k] for k in cols} for r in spending if r['Mftr_Name']=='Overall' and r['Brnd_Name'] in selected_names]
(ROOT / 'spending_selected.json').write_text(json.dumps({'year':2024,'all_source_rows':len(spending),
    'overall_product_rows':sum(r['Mftr_Name']=='Overall' for r in spending),'rows':selected,
    'caution':'Gross drug spending includes plan and beneficiary amounts, before rebates; not federal reimbursement alone. Drug names lack indication. Beneficiaries cannot be added across products.'},indent=2))
print(json.dumps({'metadata':metadata,'results':out},indent=2))
