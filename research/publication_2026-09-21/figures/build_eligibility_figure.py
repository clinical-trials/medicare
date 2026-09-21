"""Generate a standalone publication eligibility figure from the current scope.

Scientific diagram: editable SVG, vector PDF and 300-dpi PNG, not selection counts.
The adopted scope and proposed operational criteria are deliberately distinguished.
"""
from pathlib import Path
import hashlib,json,subprocess
from reportlab.graphics.shapes import Drawing,Rect,String
from reportlab.graphics import renderPDF,renderSVG
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
OUT=ROOT/'outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/eligibility_figure'
OUT.mkdir(parents=True,exist_ok=True)
STEM='Medicare_inclusion_exclusion_criteria_2026-09-21'
W,H=7.2,10.3
INK='#172C3D';BLUE='#315E86';BORDER='#AEBBC5'
RED='#943D32';AMBER='#775717';GRAY='#566573'
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
drawing=Drawing(W*72,H*72)
drawing.add(Rect(0,0,W*72,H*72,fillColor=HexColor('#FFFFFF'),strokeColor=None))
checks=[]
def txt(x,y,s,size=9.25,bold=False,color=INK,ha='left',va='center',region=None):
    font='Arial-Bold' if bold else 'Arial';lines=s.split('\n');leading=size*1.32
    ascent,descent=pdfmetrics.getAscentDescent(font,size)
    baseline=y*72-ascent if va=='top' else y*72-(ascent+descent)/2+(len(lines)-1)*leading/2
    bounds=[]
    for i,line in enumerate(lines):
        width=pdfmetrics.stringWidth(line,font,size)
        xpt=x*72-(width/2 if ha=='center' else width if ha=='right' else 0)
        by=baseline-i*leading
        drawing.add(String(xpt,by,line,fontName=font,fontSize=size,fillColor=HexColor(color)))
        bounds.append((xpt/72,(by+descent)/72,(xpt+width)/72,(by+ascent)/72))
    bb=(min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds))
    checks.append((s,bb,region))
def panel(x,y,w,h,fill='white',edge=BORDER):
    drawing.add(Rect(x*72,y*72,w*72,h*72,rx=3,ry=3,
                     fillColor=HexColor('#FFFFFF' if fill=='white' else fill),strokeColor=HexColor(edge),strokeWidth=.9))
    return (x,y,x+w,y+h)

txt(.28,9.96,'Inclusion and exclusion criteria',16,True,color='#101820')
txt(.28,9.62,'Eligibility framework for the Medicare review in progress',10.3)
txt(.28,9.34,'Adopted scope: 16 Sep 2026   |   Proposed operational screening: 21 Sep 2026',8.5,color=GRAY)

r=panel(.28,8.07,6.64,1.01,fill='#F0F5F9',edge=BLUE)
txt(.46,8.87,'ADOPTED SCOPE',10.2,True,color=BLUE,region=r)
txt(.46,8.62,'Cisgender women and men; retain eligible Medicare beneficiaries younger than 65.',9.2,region=r)
txt(.46,8.43,'Original Medicare, Medicare Advantage and Part D; extract eligible findings separately.',9.2,region=r)
txt(.46,8.24,'Coverage, payment values, patient costs and access to clinically indicated care.',9.2,region=r)

txt(.28,7.91,'INCLUDE IF ELIGIBLE',10.6,True,color=BLUE)
txt(2.40,7.91,'Proposed empirical screening criteria',9.25,color=GRAY)
for x,label,body in [
 (.28,'A  Patient evidence',
  'Original research with a relevant sex comparison\n'
  'or a clinical-need/access question within an\n'
  'eligible sex-linked indication or population.\n'
  'Population eligibility and Medicare results\n'
  'must be established.'),
 (3.70,'B  Service valuation evidence',
  'Original research on Medicare services/codes\n'
  'with a defined sex-related valuation question.\n'
  'Assess clinical and resource comparability.\n'
  'Code-only results require no individual\n'
  'patient-identity assessment.')]:
    r=panel(x,6.21,3.22,1.45,edge=BLUE)
    txt(x+.16,7.42,label,10,True,color=BLUE,region=r)
    txt(x+.16,7.14,body,9.05,va='top',region=r)
txt(.28,5.98,'An opposite-sex comparator is not required; assess clinical need independently of coverage.',8.7)

r=panel(.28,3.78,3.22,1.94,fill='#FBF4F2',edge=RED)
txt(.44,5.48,'EXCLUDE FROM PRIMARY',10.05,True,color=RED,region=r)
txt(.44,5.23,'Adopted population / indication exclusions',8.7,color=GRAY,region=r)
txt(.44,5.04,
    'Transgender-focused patient studies or\n'
    'gender-affirming-care indications.\n\n'
    'Combined mixed-population estimates with\n'
    'no separable eligible cisgender results.',9.15,va='top',region=r)
txt(.44,4.02,'Retain the citation and exclusion reason.\nAssess separable results independently.',8.65,color=RED,region=r)

r=panel(3.70,3.78,3.22,1.94,fill='#FCF8EB',edge=AMBER)
txt(3.86,5.48,'AWAITING INFORMATION',10.05,True,color=AMBER,region=r)
txt(3.86,5.23,'Retain as unresolved; no automatic exclusion',8.7,color=GRAY,region=r)
txt(3.86,5.04,
    'Male/female sex recorded, identity unreported:\n'
    'assess full text and clarify where feasible.\n'
    'Do not infer cisgender identity.\n\n'
    'Unclear eligibility or insufficient reporting:\n'
    'retain pending further information.',9.15,va='top',region=r)
txt(3.86,3.94,'Unretrieved reports are logged separately.',8.65,color=AMBER,region=r)

r=panel(.28,2.05,6.64,1.47,fill='#F5F7F8')
txt(.46,3.27,'RETAIN SEPARATELY AS CONTEXT',10.2,True,color=GRAY,region=r)
txt(.46,3.10,
    'Policy, formulary and descriptive code sources: assess indication, authority and dates;\n'
    'no patient-identity test. Empirical code studies use the service-valuation route above.\n\n'
    'Clinical reviews/efficacy, physician-gender research and other-payer evidence.\n'
    'General intervention/health IT studies without the required equity or need question.',9.15,va='top',region=r)
txt(.46,2.19,'No relevant Medicare empirical finding or review outcome: outside primary eligibility.',8.65,color=GRAY,region=r)

r=panel(.28,.98,6.64,.80)
txt(.46,1.55,'CLASSIFY CARE AND THE SUBJECT OF EACH COMPARISON',9.5,True,region=r)
txt(.46,1.29,'Shared systems | reproductive anatomy | reproductive physiology | mixed/site-dependent',8.85,region=r)
txt(.46,1.10,'Patient sex, physician gender and service anatomy remain distinct analytical variables.',8.85,region=r)

txt(.28,.67,'Retain null and opposing findings. Language or full-text access alone is not an exclusion.',8.8)
txt(.28,.43,'No selection counts or completed decisions are shown. Final eligibility assessment is pending.',8.8)
txt(.28,.19,'Sources: REVIEW_SCOPE.md and draft protocol sections 2, 3 and 6. Figure prepared 21 Sep 2026.',8.1,color=GRAY)

# Geometric checks at final physical size supplement, but do not replace, visual QA.
for text,bb,region in checks:
    if region:
        x0,y0,x1,y1=region
        assert bb[0]>=x0-.01 and bb[2]<=x1+.01 and bb[1]>=y0-.01 and bb[3]<=y1+.01,(text,bb,region)
    assert bb[0]>=.15 and bb[2]<=W-.15 and bb[1]>=.08 and bb[3]<=H-.08,(text,bb)

description='Eligibility criteria for an ongoing Medicare equity review. Adopted scope is distinguished from proposed operational screening; unresolved identity is not an automatic exclusion. No completed selection or counts are implied.'
paths=[OUT/f'{STEM}.{ext}' for ext in ['svg','pdf','png']]
renderSVG.drawToFile(drawing,str(paths[0]))
c=Canvas(str(paths[1]),pagesize=(W*72,H*72),pageCompression=1)
c.setTitle('Inclusion and exclusion criteria');c.setSubject(description)
renderPDF.draw(drawing,c,0,0);c.showPage();c.save()
subprocess.run(['/Users/lgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm',
                '-r','300','-singlefile','-png',str(paths[1]),str(OUT/STEM)],check=True)
sources=[ROOT/'REVIEW_SCOPE.md',ROOT/'research/submission/Medicare_systematic_review_protocol.md']
manifest={'prepared_on':'2026-09-21','status':'Publication figure draft; not a final eligibility decision or completed PRISMA flow',
 'dimensions_inches':[W,H],'png_dpi':300,'svg_text_editable':True,'pdf_vector_with_embedded_fonts':True,
 'scope_amendment_made':False,'new_evidence_added':False,'selection_counts_displayed':False,
 'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
 'outputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
 'verification':'All text lies within the page and associated panels; visual PDF/PNG inspection also required.'}
(HERE/'eligibility_figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
