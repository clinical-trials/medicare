"""Build the preliminary Medicare white paper and four reproducible figures.

Requires Python 3, reportlab, matplotlib and pypdf. Run from any directory.
Inputs are the existing curated JSON register; no new evidence is inferred.
"""
from pathlib import Path
import json
import re
import os
import tempfile
from html import escape, unescape

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'medicare-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.font_manager import findfont, FontProperties
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Image, Table, TableStyle, KeepTogether)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8'
FIG = OUT / 'white_paper_figures'
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
PDF = OUT / 'Medicare_sex_gender_equity_white_paper_2026-09-16.pdf'
MD = PDF.with_suffix('.md')
def read(name): return json.loads((ROOT / 'research' / (name + '.json')).read_text())
analysis, pairs, synth, registry = (read(x) for x in
    ['synthesis_analysis', 'procedure_pairs_2026', 'preliminary_synthesis', 'reference_registry'])
records = {x['id']: x for key in ['scientific_references', 'methodology_references',
            'policy_sources', 'clinical_guidance_sources'] for x in registry[key]}

NAVY, TEAL, GOLD, GREY = '#15384A', '#157F82', '#D1A34B', '#C4CCD1'
INK, MUTED, PALE = '#243B49', '#526674', '#EEF4F5'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10, 'axes.labelcolor':INK,
    'text.color':INK, 'xtick.color':MUTED, 'ytick.color':INK, 'svg.fonttype':'none',
    'axes.spines.top':False, 'axes.spines.right':False, 'axes.spines.left':False,
    'axes.unicode_minus':False})

def savefig(fig, name):
    fig.savefig(FIG / (name + '.png'), dpi=260, facecolor='white')
    fig.savefig(FIG / (name + '.svg'), facecolor='white')
    plt.close(fig)

# Figure 1: conceptual classification, not an empirical or causal diagram.
fig, ax = plt.subplots(figsize=(8.0, 3.5))
fig.subplots_adjust(left=.01, right=.99, bottom=.01, top=.99)
ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis('off')
columns = [(.015, 'PATIENT CARE', 'Clinical need and access',
    'Unit: patient / care episode\n\nCoverage and restrictions\nPatient costs and delays\nAppropriate completed care',
    'Compare eligible women and men,\nor evaluate need within one group.'),
    (.35, 'SERVICE VALUATION', 'Anatomy and clinical work',
    'Unit: service / procedure code\n\nWork relative value units\nFull-episode resources\nPayment rules and amounts',
    'Match purpose and resources;\nretain differences in both directions.'),
    (.685, 'PHYSICIAN PAYMENTS', 'Clinician sex / gender',
    'Unit: physician / claim\n\nAnnual Medicare receipts\nClinical time and service mix\nComparable-service payments',
    'Analyze physician differences\nseparately from patient differences.')]
for x, label, title, body, note in columns:
    ax.add_patch(FancyBboxPatch((x,.13),.30,.81,boxstyle='round,pad=.008',
                              facecolor=PALE,edgecolor='#D7E2E5'))
    ax.text(x+.017,.87,label,fontsize=9,color=TEAL,weight='bold')
    ax.text(x+.017,.77,title,fontsize=10.2,weight='bold')
    ax.text(x+.017,.67,body,fontsize=9.1,linespacing=1.65,va='top')
    ax.text(x+.017,.23,note,fontsize=8.2,linespacing=1.4,va='top')
ax.text(.5,.025,'Anatomy, patient sex/gender and physician sex/gender are separate variables.',
        ha='center',fontsize=10,weight='bold',color=NAVY)
savefig(fig,'figure_1_analytical_streams')

# Figure 2: 10 specific formulations, not overlapping aggregate hormone groups.
dist = [r for r in analysis['formulary_distributions'] if 'any single-ingredient' not in r['group']]
assert len(dist)==10
for r in dist:
    assert r['total']==5499
    assert sum(r[k] for k in ['at_least_one_option_without_PA_ST',
        'listed_all_options_PA_or_ST','no_matched_listing'])==5499
names = ['Estradiol oral tablet (generic)','Estradiol vaginal cream (generic)',
         'Estradiol vaginal insert (generic)','Estradiol patch (generic)',
         'Estradiol topical gel (generic)','Estring (brand)',
         'Testosterone topical gel (generic)','Fezolinetant / Veozah',
         'Ospemifene / Osphena','Prasterone / Intrarosa']
fig, ax = plt.subplots(figsize=(8,5.1))
fig.subplots_adjust(left=.38,right=.98,top=.83,bottom=.13)
series = [('at_least_one_option_without_PA_ST',TEAL),('listed_all_options_PA_or_ST',GOLD),
          ('no_matched_listing',GREY)]
left=[0.0]*10
for key,col in series:
    vals=[r[key]/5499*100 for r in dist]
    ax.barh(range(10),vals,left=left,color=col,height=.64,edgecolor='white',linewidth=.35)
    for i,(v,l) in enumerate(zip(vals,left)):
        if v>=9: ax.text(l+v/2,i,f'{v:.1f}%',ha='center',va='center',fontsize=8.3,
                        color='white' if col==TEAL else INK)
    left=[a+b for a,b in zip(left,vals)]
ax.set_yticks(range(10),names,fontsize=9.3); ax.invert_yaxis()
ax.set_xlim(0,100); ax.set_xticks([0,25,50,75,100],['0%','25%','50%','75%','100%'])
ax.set_xlabel('Share of 5,499 analyzed plan segments',labelpad=10)
ax.tick_params(axis='y',length=0,pad=9); ax.spines['bottom'].set_color(GREY)
fig.legend(handles=[Patch(color=TEAL,label='At least one listed option without PA/ST'),
    Patch(color=GOLD,label='Listed, but every matched option has PA and/or ST'),
    Patch(color=GREY,label='No matched listing')],loc='upper left',bbox_to_anchor=(.035,.995),
    frameon=False,ncol=1,fontsize=9)
savefig(fig,'figure_2_formulary_states')

# Figure 3: signed differences in units, not percent, payment or a pooled effect.
fig,ax=plt.subplots(figsize=(8,4.0))
fig.subplots_adjust(left=.39,right=.95,top=.82,bottom=.20)
labels=['Sling placement\n53440 / 57288','Sling revision or removal\n53442 / 57287',
        'Simple genital lesion treatment\n54050 / 56501','Complete external genital excision\n55150 / 56625',
        'Pelvic exenteration\n51597 / 58240']
deltas=[p['male_minus_female_work_rvu'] for p in pairs['pairs']]
for p,d in zip(pairs['pairs'],deltas):
    assert abs(p['male']['work_rvu']-p['female']['work_rvu']-d)<1e-8
ax.barh(range(5),deltas,color=[GOLD if d>0 else TEAL for d in deltas],height=.52)
ax.axvline(0,color=NAVY,lw=1)
for i,d in enumerate(deltas):
    ax.text(d+(.14 if d>0 else -.14),i,f'{d:+.2f}',va='center',
            ha='left' if d>0 else 'right',fontsize=10,weight='bold')
ax.set_yticks(range(5),labels,fontsize=9.4); ax.invert_yaxis(); ax.tick_params(axis='y',length=0,pad=10)
ax.set_xlim(-7.8,3.6); ax.set_xticks([-6,-4,-2,0,2]); ax.spines['bottom'].set_color(GREY)
ax.set_xlabel('Work RVUs: first listed code minus second listed code',fontsize=9.2,labelpad=11)
ax.text(.02,1.12,'Second listed code higher',transform=ax.transAxes,color=TEAL,fontsize=9)
ax.text(.99,1.12,'First listed code higher',transform=ax.transAxes,ha='right',color='#976E22',fontsize=9)
savefig(fig,'figure_3_selected_work_rvu_differences')

# Figure 4: a proposed measurement pathway. Arrows do not assert causal estimates.
fig,ax=plt.subplots(figsize=(8,2.65))
fig.subplots_adjust(left=.01,right=.99,top=.98,bottom=.02)
ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
stages=[('CLINICAL NEED','Symptoms, risk,\nbenefit, preference'),('RECOGNITION','Diagnosis,\nreferral, offer'),
        ('BENEFIT RULES','Eligibility, listing,\nprior authorization'),('PRACTICAL ACCESS','Cost, transport,\ntime, caregiving'),
        ('COMPLETED CARE','Suitable treatment,\npatient outcomes')]
for i,(title,body) in enumerate(stages):
    x=.008+i*.2
    ax.add_patch(FancyBboxPatch((x,.30),.178,.48,boxstyle='round,pad=.006',
        facecolor=PALE if i<4 else '#DFEEEE',edgecolor='#B8CDCF'))
    ax.text(x+.089,.67,title,ha='center',fontsize=8,weight='bold',color=TEAL)
    ax.text(x+.089,.52,body,ha='center',va='top',fontsize=9,linespacing=1.55)
    if i<4: ax.annotate('',xy=(x+.198,.54),xytext=(x+.181,.54),
        arrowprops={'arrowstyle':'->','color':MUTED,'lw':1.2})
ax.text(.5,.11,'Include people with unmet need and those who never generate a paid claim.',
        ha='center',fontsize=10,weight='bold',color=NAVY)
savefig(fig,'figure_4_care_pathway')

# Typography and document components.
for name,family,style,weight in [('Body','DejaVu Sans','normal','normal'),
    ('BodyBold','DejaVu Sans','normal','bold'),('BodyItalic','DejaVu Sans','italic','normal'),
    ('Display','DejaVu Serif','normal','normal')]:
    pdfmetrics.registerFont(TTFont(name,findfont(FontProperties(family=family,style=style,weight=weight))))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=10,leading=14.6,textColor=colors.HexColor(INK),spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8.5,leading=12.2,textColor=colors.HexColor(MUTED),spaceAfter=7),
 'h1':ParagraphStyle('h1',fontName='Display',fontSize=23,leading=28,textColor=colors.HexColor(NAVY),spaceAfter=15),
 'h2':ParagraphStyle('h2',fontName='BodyBold',fontSize=11.7,leading=16,textColor=colors.HexColor(TEAL),spaceBefore=9,spaceAfter=5),
 'eyebrow':ParagraphStyle('eyebrow',fontName='BodyBold',fontSize=8.5,leading=12,textColor=colors.HexColor(TEAL),spaceAfter=7),
 'caption':ParagraphStyle('caption',fontName='Body',fontSize=8.6,leading=12.3,textColor=colors.HexColor(MUTED),spaceBefore=5,spaceAfter=10),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=8.5,leading=11.7,textColor=colors.HexColor(INK)),
 'ref':ParagraphStyle('ref',fontName='Body',fontSize=8.3,leading=11.4,textColor=colors.HexColor(INK),spaceAfter=10),
}
story=[]; manuscript=[]; cited=set(); sections=[]
IDPAT=r'\b(?:L-[A-Z]\d{2}(?:-E\d+)?|P-\d{3}|M-\d{3}|C-\d{3})\b'
def markdown_text(text):
    text=re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>',
                lambda m:f'[{m.group(2)}]({unescape(m.group(1))})',text)
    text=text.replace('<br/>','\n')
    return unescape(re.sub('<[^>]+>','',text))
def mark(text):
    for rid in re.findall(IDPAT,text):
        if rid not in records: raise ValueError('Unknown reference '+rid)
        cited.add(rid)
    return re.sub(IDPAT,lambda m:f'<a href="#ref-{m.group()}" color="{TEAL}">{m.group()}</a>',text)
def p(text,style='body'):
    manuscript.append(markdown_text(text))
    story.append(Paragraph(mark(text),styles[style]))
def heading(title): p(title,'h2')
def page(num,title):
    if story: story.append(PageBreak())
    sections.append((num,title))
    manuscript.append('\n## '+title+'\n')
    story.append(Paragraph(f'<a name="section-{num}"/>WHITE PAPER / {num:02}',styles['eyebrow']))
    story.append(Paragraph(title,styles['h1']))
def table(rows,widths,header=True):
    items=[[Paragraph(mark(str(c)),styles['cell']) for c in row] for row in rows]
    t=Table(items,colWidths=widths,hAlign='LEFT',repeatRows=1 if header else 0)
    rules=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#C9D7DB'))]
    if header:
        rules.extend([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DFECEE')),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F8F9')])])
    t.setStyle(TableStyle(rules));story.extend([t,Spacer(1,9)])
    manuscript.append('\n'+'\n'.join(' | '.join(re.sub('<[^>]+>','',str(c)) for c in row) for row in rows)+'\n')
def figure(name,height,caption):
    story.append(Image(str(FIG/(name+'.png')),width=516,height=height))
    p(caption,'caption');manuscript.append(f'![{name}](white_paper_figures/{name}.png)')
def callout(title,text):
    a=Paragraph(title,styles['h2']); b=Paragraph(mark(text),styles['body'])
    box=Table([[a],[b]],colWidths=[516]);box.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor(PALE)),('BOX',(0,0),(-1,-1),.4,colors.HexColor('#CADCDF')),
        ('LEFTPADDING',(0,0),(-1,-1),13),('RIGHTPADDING',(0,0),(-1,-1),13),
        ('TOPPADDING',(0,0),(-1,0),5),('BOTTOMPADDING',(0,-1),(-1,-1),10)]))
    story.extend([box,Spacer(1,10)]);manuscript.extend([title,markdown_text(text)])

# Page 1: cover with substantive abstract and honest review stage.
story.append(Spacer(1,34))
p('MEDICARE RESEARCH / WHITE PAPER / VERSION 1.0','eyebrow')
story.append(Paragraph('Sex, gender and equity<br/>in Medicare reimbursement',
    ParagraphStyle('cover',parent=styles['h1'],fontSize=32,leading=39,spaceAfter=20)))
manuscript.append('# Sex, gender and equity in Medicare reimbursement')
p('Preliminary evidence synthesis and research agenda','h2')
p('Coverage, service valuation and access to care for women and men', 'body')
p('September 16, 2026', 'small')
story.append(Spacer(1,20))
callout('The central question',
 'Do Medicare benefit rules, payment values and practical barriers align with the clinical needs of women and men? This paper identifies signals worth testing, including possible disadvantages affecting either sex, while distinguishing patient access from physician payments.')
heading('Abstract')
p('The selected evidence suggests that reimbursement inequity is a question about clinical indication, benefit design, service valuation and completed care. It does not establish a uniform disadvantage to one sex. The formulary snapshot and basic Part D exclusion rules contradict the broad premise that Medicare excludes estradiol while routinely covering Viagra for erectile dysfunction. Procedure studies report differing results, and shared conditions such as osteoporosis reveal possible gaps affecting men. Physician payment studies address a separate question.')
p('This paper brings together 34 retained literature records and 40 selected care-item/indication rows, describes two reproducible CMS data summaries, and proposes eight exploratory hypotheses. The Lancet review by Mauvais-Jarvis and colleagues provides the organizing clinical framework. [L-B01; L-B01-E1]')
p('<b>Review status:</b> Preliminary narrative synthesis. Comprehensive searching, final eligibility adjudication, full-text extraction, formal risk-of-bias appraisal and outcome-specific certainty assessment remain unfinished. No meta-analysis or causal effect estimate is presented.','small')
p('Prepared from the Medicare research repository: <a href="https://github.com/clinical-trials/medicare" color="#157F82">github.com/clinical-trials/medicare</a>. No institutional affiliation or external endorsement is asserted.','small')

page(1,'What the evidence currently supports')
p('The working thesis is that inequity can arise when policy and practical access fail to meet clinical need. A difference in spending or use is a signal for investigation; its cause and clinical significance require separate evidence.')
for title,text in [
 ('1. Formulation and indication matter','Generic oral estradiol and vaginal cream had a listed option without prior authorization or step therapy in all 5,499 analyzed plan segments. Other formulations varied. Basic Part D excludes drugs when used for sexual or erectile dysfunction; other eligible indications and supplemental benefits must be assessed separately. [P-002; P-003; P-026]'),
 ('2. Procedure comparisons are sensitive to the match','One study reports lower female-anatomy work RVUs in 41 of 55 pairs, while a smaller, closely matched study finds no statistically significant overall difference. Our five-pair 2026 illustration contains differences in both directions. [L-P01; L-P02; P-035; P-036]'),
 ('3. Sex-specific care can be assessed on its own merits','A benefit change can be evaluated against desired, clinically indicated care within one population. An opposite-sex counterpart is not required. Observational contraceptive coverage evidence provides one starting point. [L-G09]'),
 ('4. Shared-condition gaps may disadvantage men','Historical bone-density testing was much lower in men. A selected male fracture cohort benefited from outreach, although the trial did not compare men with women. Current eligibility includes several qualifying routes. [L-G04; L-G05; P-012]'),
 ('5. Physician payments are a distinct evidence stream','Selected studies report lower annual Medicare payments to women physicians. Service volume, referrals, clinical time, specialty and billing circumstances require investigation; some per-service comparisons are null. [L-C01; L-C02; L-C03]'),
 ('6. Coverage alone is an incomplete access measure','Financial, transport and caregiving barriers may affect treatment completion. Interviews and clinical frameworks suggest mechanisms, but do not quantify Medicare-specific causal effects. [L-Q01; L-B01]')]:
    heading(title);p(text)

page(2,'Scope, sources and methods')
heading('Medicare as a national policy benchmark')
p('Medicare is a useful benchmark for care in later life, when per-person use and spending are substantial. In 2020, adults aged 65 and older were 17% of the population and accounted for 37% of all-payer personal health care spending. This does not mean that Medicare finances most US care or that most lifetime care occurs after age 65. Younger beneficiaries remain in scope. [P-041; P-043]')
heading('Population and dated scope amendment')
p('At the investigator\'s direction, the scope was amended on September 16, 2026 to focus on cisgender women and men and exclude transgender-focused patient studies and gender-affirming-care indications. The amendment followed initial searching. Male/female reporting does not establish gender identity: such cohorts remain candidates pending eligibility adjudication. Mixed-population results are eligible only when the in-scope results can be separated. Policy and code data contain no patient identity.')
heading('Current synthesis')
p('We organized the selected register by clinical indication, anatomy/physiology, analytic subject, payer and policy period. We retained conflicting and null findings and separated official rules from empirical evidence about their effects. This is a structured narrative synthesis of an assembled evidence set, not an exhaustive review of all Medicare procedures or prescriptions.')
table([['Register component','Current extent and interpretation'],
 ['Care inventory','40 selected care-item/indication rows; neither a census nor a representative sample.'],
 ['Active literature','34 records: 27 primary candidates or retained code-policy components and 7 contextual records.'],
 ['Analytic subjects','18 patient care/access; 10 service/anatomy valuation; 3 physician sex/gender; 3 general clinical background.'],
 ['Audit trail','8 excluded studies and 1 linked correction retained separately. Two methodology references are separate from the 34 literature records.']], [125,391])
p('PMIDs, DOIs, source links, access levels and stable reference IDs are preserved. Verified metadata does not imply full-text review or final inclusion. Some findings are available only through abstracts or accessible excerpts. No formal GRADE ratings have been assigned. [M-001; M-002]','small')

page(3,'Separate the clinical and payment questions')
figure('figure_1_analytical_streams',226,
 '<b>Figure 1. Three analytical streams.</b> Proposed classification framework, not a measured causal model. The patient, service and physician units must remain separate. Clinical framing draws on the Lancet review and its correction. [L-B01; L-B01-E1]')
p('Anatomy and physiology describe the care being delivered. They do not establish a person\'s gender identity or the gender of the clinician. Record the original study\'s sex/gender terminology and measurement method.')
table([['Clinical basis','Examples and comparison approach'],
 ['Shared body systems/functions','Bone, breast, lymphatic, cardiovascular and pelvic-floor care. Compare need within the same indication; sex-defined eligibility or unequal disease burden does not make the anatomy exclusive.'],
 ['Female reproductive anatomy','Local vaginal or cervical care. Assess clinical need, benefits, alternatives and the policy rationale.'],
 ['Male reproductive anatomy','Prostate or penile care. Use the same need-based assessment; do not assume an interchangeable female counterpart.'],
 ['Reproductive physiology','Menopause and male hypogonadism are distinct indications. Hormone names alone do not define clinical equivalence.'],
 ['Mixed/site-dependent services','Split bundled procedures or services by site, indication and code before comparison.']], [140,376])
p('Clinical need must be defined independently of coverage eligibility. Otherwise people excluded by a rule disappear from the denominator, concealing possible unmet need.','small')

page(4,'Drug coverage varies within clinical care')
figure('figure_2_formulary_states',329,
 '<b>Figure 2. Formulary states for ten selected formulations, August 2026.</b> Each bar contains 5,499 unsuppressed plan segments, equally weighted, using 328 formularies. PA = prior authorization; ST = step therapy. States are mutually exclusive within each row. Small segments are unlabeled; exact counts appear in the appendix. Sources: CMS monthly file and reference file. [P-002; P-034; P-037; P-038]')
p('The national snapshot does not support a blanket estradiol exclusion. Oral, vaginal and transdermal products still differ in indication, dose, suitability and restrictions. Testosterone gel is shown as another clinical context, not an equivalent treatment comparator.')
p('Basic Part D excludes a drug when used for sexual or erectile dysfunction. A product used for another eligible indication, such as sildenafil for pulmonary arterial hypertension, requires a separate coverage assessment. Brand-versus-generic naming does not establish inequity. [P-003; P-026]')
p('Clinical evidence is mixed: one vaginal estradiol trial found no primary symptom advantage over dual placebo; a broader review found possible benefits for selected symptoms, generally with low certainty. These findings do not settle every formulation or indication. [L-D03; L-D04]')
p('<b>Inference limit:</b> Listed means at least one matched product/strength. These data contain no beneficiary enrollment weights, clinical need, actual costs, denials or treatment outcomes. PA/ST flags do not disclose the criteria. Nonlisting does not rule out a successful exception. [P-033]','small')

page(5,'Procedure valuation: signals in both directions')
figure('figure_3_selected_work_rvu_differences',258,
 '<b>Figure 3. Five selected procedure pairs, July 2026.</b> Bars show national, unadjusted work relative value units (RVUs): first listed code minus second. Published anatomical/indication comparisons are illustrative, not random or a pooled sex effect. The urologic exenteration code 51597 is not exclusive to male patients. [P-035; P-036; P-045]')
table([['Study','Observed result','What it can establish'],
 ['Penn, 2025 [L-P01]','41/55 female-anatomy codes had lower work RVUs; male codes averaged 30% higher.','A selected-pair valuation signal; incomplete full-text extraction.'],
 ['Hathaway, 2024 [L-P02]','7/10 female procedures had higher work RVUs; no significant overall difference.','Sensitivity to clinical matching; a small null result is not equivalence.'],
 ['Polan, 2021 [L-P03]','Female procedures: 10.6 vs 9.7 RVUs/hour, but $555 vs $599 modeled compensation/hour.','Different measures can give different directions; dollars use specialty compensation assumptions.']], [102,208,206])
p('Work RVUs are not dollars paid. Complete comparisons need independently measured preoperative, intraoperative and postoperative work, intensity and risk. Matching global periods alone is insufficient. For the genital-lesion pair, compare like treatment methods; the male code specifies chemical treatment. [P-035; P-036]','small')
p('Breast reconstruction adds a within-condition question: flap procedures may have lower work RVUs per operative hour than implant procedures. This is a complexity/valuation question, not a patient-sex or physician-gender estimate. [L-P07]','small')

page(6,'From benefit rules to completed care')
figure('figure_4_care_pathway',171,
 '<b>Figure 4. Proposed care-pathway measurement framework.</b> Arrows organize measurements; they do not represent estimated causal effects. Clinical need is assessed independently of reimbursement eligibility. Practical barriers are hypotheses to test. [L-B01; L-Q01]')
heading('Shared-condition care can reveal gaps affecting men')
p('In historical Medicare data from 1999-2005, 30.0% of women and 4.4% of men in the analyzed white/Black populations received central dual-energy X-ray absorptiometry (DXA) at least once. These are utilization findings, not need-adjusted estimates of discrimination. In a later trial of selected men after fragility fracture, outreach increased testing from 4.9% to 10.7% and treatment initiation from 2.5% to 4.0%. That trial had no female comparison. [L-G04; L-G05]')
heading('A policy change can be studied within one population')
p('Among younger women with disabilities, gaining dual Medicare-Medicaid coverage was associated with a 3.9-percentage-point increase in contraceptive use (95% CI, 3.5-4.3). This observational result motivates study of desired, appropriate contraception; more utilization is not automatically better care. [L-G09]')
heading('Historical burden must be interpreted against current policy')
p('A breast-cancer study reported greater monthly out-of-pocket spending with lymphedema. Insurer-policy research also describes coverage gaps. Both predate Medicare\'s compression-treatment benefit, which began in 2024. A current evaluation should test unmet need and costs after the change; compression items, pumps and surgery are distinct benefits. [L-A01; L-A02; P-021; P-022]')
p('Kidney-care interviews with 51 nephrologists in 22 countries suggest financial, transport and caregiving barriers. Only seven respondents were in the United States. Their accounts are perceptions, not measured Medicare denial rates or causal estimates. [L-Q01]','small')

page(7,'Physician sex/gender: a separate question')
p('The user-supplied ophthalmology, cardiology and surgery papers compare physicians. They cannot establish that women patients receive lower coverage or payments. Annual Medicare receipts also differ from physician salary, per-service payment and patient out-of-pocket cost. [L-C01; L-C02; L-C03]')
table([['Evidence','Outcome and finding','Interpretation boundary'],
 ['Ophthalmology\nAhmad, 2020 [L-C01]','Women ophthalmologists had lower adjusted annual Medicare collections.','Abstract-level extraction; collections do not measure salary or a patient-sex contrast.'],
 ['Cardiology\nRaber, 2021 [L-C02]','Women cardiologists had lower annual payments; common-code comparisons included null results.','Service volume and mix matter. Annual differences do not establish different rates for identical claims.'],
 ['Surgery\nMunir, 2024 [L-C03]','Adjusted annual payments were lower for women in general, oncologic and colorectal surgery.','CPT matching cannot recover all modifiers, settings or clinical circumstances.']], [119,196,201])
heading('A concrete illustration from surgery')
p('For general surgeons, the adjusted annual female-minus-male payment difference was -$14,963 (95% CI, -$18,822 to -$11,105). In colorectal surgery, the unadjusted payment-per-service comparison was not statistically significant (P = .52). These are different outcomes and analyses; they should not be pooled into a single claim about reimbursement rates. [L-C03]')
heading('A testable physician pathway')
p('Referral opportunities, procedure opportunities and clinical time may contribute to annual receipts. Measure the total annual difference first, then examine these pathways. Automatically adjusting for every pathway may remove part of the difference under investigation. Comparable-rate testing requires claim-level information on service, modifier, place of service, geography and billing circumstances.')
callout('Keep the question attached to its unit',
 'Patient access: did an eligible person receive appropriate care?<br/>Service valuation: how is comparable clinical work valued?<br/>Physician payments: how do receipts differ across clinicians and why?')
p('The physician stream is contextual to the primary patient-access inquiry. It remains separate in figures, evidence extraction and future certainty assessments.','small')

def hypothesis_card(rid, title, claim, test, challenge, refs):
    heading(rid+' / '+title)
    p('<b>Hypothesis:</b> '+claim)
    p('<b>Test:</b> '+test+' <b>What would weaken it:</b> '+challenge+' '+refs,'small')

page(8,'Exploratory hypotheses: patient access')
p('These hypotheses were developed after inspecting the selected evidence. They are research propositions, not preregistered analyses or confirmed findings. Clinical need and patient preferences must be established independently of coverage rules.','small')
hypothesis_card('HYP-01','Formulation restrictions',
 'For beneficiaries who need a particular formulation for menopause symptoms or genitourinary syndrome of menopause (GSM), greater cost or authorization burden reduces timely use of suitable treatment.',
 'Link within-indication plan changes to orders, denials, initiation, persistence and symptoms; assess clinical suitability and enrollment weighting.',
 'Precise evidence of no meaningful access difference after accounting for safety, alternatives and preferences.',
 '[L-D01; L-D03; L-D04; P-002; P-029; P-033]')
hypothesis_card('HYP-03','Contraceptive benefit design',
 'More comprehensive benefits improve receipt of desired, appropriate contraception among younger beneficiaries with disabilities.',
 'Study verified coverage transitions with comparison groups, clinical need and stated preferences; distinguish drug and procedure benefits.',
 'A precise lack of meaningful improvement despite a verified reduction in financial or administrative barriers.',
 '[L-G09; L-G10; P-015; P-018; P-019]')
hypothesis_card('HYP-04','Bone care after fracture',
 'Men receive less appropriate osteoporosis care after fracture than women with comparable need, and targeted outreach reduces this gap.',
 'Use a contemporary eligible cohort, including nonrecipients; measure referrals, testing, treatment, follow-up and competing mortality.',
 'Precise need-adjusted parity, or precise failure of an effective outreach intervention to reduce the proposed gap.',
 '[L-G04; L-G05; P-012]')
hypothesis_card('HYP-05','Practical barriers in kidney care',
 'Financial, transport and caregiving burdens contribute to a sex difference in completing indicated kidney care.',
 'Measure burdens and completion directly, then evaluate support that actually reduces the between-sex burden difference.',
 'Such support precisely fails to reduce the completion gap. Absence of a sex-by-intervention interaction alone is not a refutation.',
 '[L-Q01]')

page(9,'Exploratory hypotheses: valuation and policy')
hypothesis_card('HYP-02','Comparable clinical work',
 'Across a prespecified matched set, female-anatomy procedures have lower average work RVUs after accounting for independently measured complete clinical work.',
 'Fix the clinical matches before viewing values; measure the full episode. Estimate mean paired differences and matching sensitivity.',
 'Precise average parity would weaken the average-penalty hypothesis, without proving every individual pair fair.',
 '[L-P01; L-P02; L-P03; P-035; P-036]')
hypothesis_card('HYP-06','Physician opportunity and receipts',
 'Referral and procedure opportunities and clinical time contribute to annual Medicare receipt differences by physician sex/gender.',
 'Estimate the total annual difference first; examine time-standardized and pathway-specific estimates second, with complete claim circumstances.',
 'Precisely estimated minimal contribution from the proposed pathways, or disappearance of the annual difference under comparable observation.',
 '[L-C01; L-C02; L-C03]')
hypothesis_card('HYP-07','The 2024 compression benefit',
 'The Medicare compression-treatment benefit reduces cost-related unmet need among beneficiaries with lymphedema.',
 'Use post-policy patient data, a defensible comparator and pretrend checks; measure costs and receipt of needed compression items.',
 'An estimate precise enough to exclude a meaningful reduction in unmet need; an imprecise null is inconclusive.',
 '[L-A01; L-A02; P-021; P-022]')
hypothesis_card('HYP-08','Complex reconstruction',
 'Complex flap reconstruction has lower valuation relative to complete clinical work than implant reconstruction, beyond similar patterns in other reconstructive services.',
 'Measure complete episodes and outside comparators first. Study patient access separately when recipient and nonrecipient data are available.',
 'A sufficiently precise estimate excluding a prespecified meaningful relative disadvantage. Broad real-payment declines alone are insufficient.',
 '[L-P07; L-P08; L-P09; P-035]')
p('Priority sequence: complete the formulation audit; extend the analogous-procedure set; design a contemporary shared-condition patient-access study. All eight hypotheses remain untested in this project.','small')

page(10,'Completing the systematic review')
heading('Search and screen transparently')
p('The next phase should specify dated searches across bibliographic databases and Medicare policy sources, publish complete search strings, deduplicate records, and use independent screening with documented resolution of disagreements. Expand beyond reproductive care to cardiovascular, kidney, lung, cancer, metabolic, musculoskeletal, pain, mental-health and preventive care. Use the Lancet review for citation following, then screen underlying papers independently. [L-B01]')
heading('Appraise evidence at the appropriate level')
p('Assess risk of bias with tools matched to study design. Extract policy authority, effective date, population, indication, payer, comparator, effect estimate, uncertainty and source access. Separate national rules from contractor and plan implementation; separate Original Medicare, Medicare Advantage and Part D. Prespecify causal questions and avoid automatically adjusting away possible mechanisms of inequity.')
table([['Method','Plain-language purpose','Current status'],
 ['PRISMA [M-001]','Show how a review identified, selected, assessed and synthesized evidence. It is reporting guidance, not a quality score.','A complete reproducible search and screening flow are not yet available.'],
 ['GRADE [M-002]','Assess confidence in the body of evidence for a specific outcome, considering bias, inconsistency, indirectness, imprecision and publication bias.','No formal outcome-specific certainty ratings have been completed.']], [96,260,160])
heading('Limits of this white paper')
p('The evidence set is selected and concentrated in reproductive care. Eligibility and extraction remain incomplete for some studies; several reports have only abstract or excerpt access. Historical findings span different policy eras. Formulary data are not enrollment weighted, and reused formularies make plan segments dependent. Procedure pairs are purposive and do not measure all clinical work. Claims alone miss untreated need, cash purchases and some denials. These constraints prevent a national estimate of the prevalence or causal magnitude of reimbursement bias.')
callout('Plain-language concept for public communication',
 'We are asking whether Medicare rules help women and men obtain the care they actually need. We will track how evidence is found and selected using PRISMA, then assess how much confidence each important conclusion deserves using GRADE. The goal is to identify where policies appear fair, where care may be harder to obtain, and what evidence is still missing. This paper is the starting synthesis, not the completed review.')

page(11,'Data appendix: figures 2 and 3')
p('<b>Table A1.</b> Exact plan-segment counts underlying Figure 2. Every row totals 5,499. U = at least one listed option without PA/ST; R = listed, but every matched option has PA and/or ST; NL = no matched listing. These states are not rates of claim approval. [P-002; P-034; P-037; P-038]','small')
table([['Formulation','U','R','NL']]+[[name,str(r['at_least_one_option_without_PA_ST']),
    str(r['listed_all_options_PA_or_ST']),str(r['no_matched_listing'])] for name,r in zip(names,dist)],
    [312,68,68,68])
p('<b>Data handling.</b> County repetitions were removed from 112,294 plan-county rows. Nineteen suppressed segments were excluded. The resulting 5,499 segments comprise 5,055 contract-plan pairs and reuse 328 formularies. CMS public-file exclusions include employer, PACE, most demonstration and non-Part-D plans. Formulation groups were matched through the August reference file; 23 basic-file RxCUIs were unmatched and unclassified. PA/ST criteria, quantity limits, dose suitability, patient costs and enrollment weights are not evaluated here.','small')
p('<b>Table A2.</b> Work RVUs underlying Figure 3. National unadjusted values, July 2026 nonQPP file; no geographic or claim-specific adjustments. Columns follow the published comparator order, without inferring patient sex. [P-035; P-036; P-045]','small')
table([['Code pair (first / second)','First code','Second code','Difference']]+[[p['male']['cpt']+' / '+p['female']['cpt'],
    f"{p['male']['work_rvu']:.2f}",f"{p['female']['work_rvu']:.2f}",f"{p['male_minus_female_work_rvu']:+.2f}"] for p in pairs['pairs']],
    [210,102,102,102])
p('Reproducibility: figures derive from research/synthesis_analysis.json and research/procedure_pairs_2026.json. The repository preserves source dates, URLs, data extraction scripts and source notices. A static release is dated September 16, 2026; later policy or formulary changes require a new analysis.','small')

# References include every citation actually used, with numeric PMIDs and access status.
page(12,'References and source notes')
p('Stable IDs connect this paper to the evidence workbook and living bibliography. Every cited scientific article has a verified PMID below. Access notes describe the extraction available to this project, not the quality of the publication. Policy labels are descriptive source labels. No excluded study supplies this synthesis.','small')
policy_labels={
 'P-002':'CMS. Monthly Part D formulary archive, August 2026 (release August 26, 2026).',
 'P-003':'Social Security Act, section 1860D-2(e)(2)(A). Covered Part D drug exclusions.',
 'P-012':'Medicare.gov. Bone mass measurements: benefit eligibility.',
 'P-015':'CMS Medicare Coverage Database. WPS billing and coding article A55951: local IUD policy.',
 'P-018':'CMS. National Coverage Determination 230.3: Sterilization.',
 'P-019':'Medicare.gov. Prescription drugs (outpatient): Part D benefit framework.',
 'P-021':'Medicare.gov. Lymphedema compression treatment items.',
 'P-022':'CMS. Transmittal R12532BP, 2024: Lymphedema compression treatment items.',
 'P-026':'CMS. Part D questions and answers on drugs for sexual or erectile dysfunction (2006).',
 'P-029':'FDA. Veozah (fezolinetant): warning about rare serious liver injury.',
 'P-033':'CMS. Part D exceptions.',
 'P-034':'CMS. CY 2026 August formulary reference file (reference date August 25, 2026).',
 'P-035':'CMS. RVU26C physician fee schedule relative value files, July 2026. NonQPP file released June 30, 2026.',
 'P-036':'Hathaway and colleagues. Author-published comparison table: analogous urological and gynecological procedures. AUA News, July 2024.',
 'P-037':'CMS. Monthly Prescription Drug Plan Formulary and Pharmacy Network Information: dataset description.',
 'P-038':'CMS. 2026 public-use file record layout: monthly formulary and pharmacy network information.',
 'P-041':'CMS. U.S. Personal Health Care Spending by Age and Sex: 2020 Highlights.',
 'P-043':'Medicare.gov. Get started with Medicare: age and other eligibility routes.',
 'P-045':'National Library of Medicine, VSAC. CPT 51597 descriptor, code system version 2021. Used to check anatomy classification, not 2026 RVU values.',
}
ref_ids=sorted(cited,key=lambda x: (0 if x.startswith('L-') else 1 if x.startswith('M-') else 2,x))
manuscript.append('\n## References\n')
for rid in ref_ids:
    r=records[rid]
    if rid.startswith(('L-','M-')):
        text=f'<a name="ref-{rid}"/><b>[{rid}]</b> '+escape(r['citation'])
        pmid=str(r['pmid']); assert pmid.isdigit()
        text+=f' <a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" color="{TEAL}">PMID: {pmid}</a>.'
        if r.get('doi'): text+=f' DOI: <a href="https://doi.org/{r["doi"]}" color="{TEAL}">{escape(r["doi"])}</a>.'
        access=r.get('access_level','');
        if access: text+='<br/><font color="#526674">Project access: '+escape(access)+'.</font>'
    else:
        text=f'<a name="ref-{rid}"/><b>[{rid}]</b> '+escape(policy_labels[rid])
        text+=f' <a href="{escape(r["url"],quote=True)}" color="{TEAL}">Official/source document</a>. Recorded September 16, 2026.'
    story.append(Paragraph(text,styles['ref']))
    manuscript.append(markdown_text(text)+'\n')

def decorate(canvas,doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#D3DFE3'));canvas.setLineWidth(.55)
    canvas.line(48,44,564,44)
    canvas.setFillColor(colors.HexColor(MUTED));canvas.setFont('Body',7.2)
    canvas.drawString(48,29,'MEDICARE / PRELIMINARY EVIDENCE SYNTHESIS / SEPTEMBER 2026')
    canvas.drawRightString(564,29,str(doc.page))
    if doc.page>1:
        canvas.setFont('Body',7.5);canvas.setFillColor(colors.HexColor(TEAL))
        canvas.drawString(48,764,'SEX, GENDER AND EQUITY IN MEDICARE REIMBURSEMENT')
    canvas.restoreState()

doc=SimpleDocTemplate(str(PDF),pagesize=(612,792),rightMargin=48,leftMargin=48,
    topMargin=49,bottomMargin=58,title='Sex, gender and equity in Medicare reimbursement',
    author='Medicare research project',subject='Preliminary evidence synthesis and research agenda',
    pageCompression=1)
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
MD.write_text('\n\n'.join(manuscript)+'\n')
reader=PdfReader(str(PDF))
alltext='\n'.join(p.extract_text() or '' for p in reader.pages)
assert all(f'Figure {n}.' in alltext for n in range(1,5))
assert len(re.findall(r'PMID:',alltext))==sum(r.startswith(('L-','M-')) for r in ref_ids)
for rid in ref_ids:
    assert f'[{rid}]' in alltext
assert '32828189' in alltext and '32891210' in alltext
assert '33782057' in alltext and '21195583' in alltext
manifest={'title':'Sex, gender and equity in Medicare reimbursement','date':'2026-09-16',
    'stage':analysis['stage'],'pdf':PDF.name,'pages':len(reader.pages),'figures':4,
    'cited_references':ref_ids,'scientific_and_methodology_pmids':{
        rid:records[rid]['pmid'] for rid in ref_ids if rid.startswith(('L-','M-'))},
    'input_files':['research/synthesis_analysis.json','research/procedure_pairs_2026.json',
        'research/preliminary_synthesis.json','research/reference_registry.json'],
    'checks':['All formulation states sum to 5,499','All five RVU differences recomputed',
        'Every in-text reference resolves','All scientific and methodology citations retain PMIDs',
        'Four figure captions present'], 'visual_review':'Required after generation'}
(OUT/'Medicare_white_paper_manifest_2026-09-16.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'pdf':str(PDF),'pages':len(reader.pages),'references':len(ref_ids),'figures':4},indent=2))
for i,pg in enumerate(reader.pages,1):
    t=pg.extract_text() or ''
    print(i,len(t),t[:90].replace('\n',' | '))
