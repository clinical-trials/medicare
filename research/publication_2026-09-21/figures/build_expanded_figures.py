"""Build Figures 1, 2, 3, 5 and 6 from existing conceptual records.

Run with the bundled Python runtime. No evidence is added or reclassified.
SVG text remains editable. PNGs are rendered from vector PDF at 300 dpi.
"""
from pathlib import Path
import hashlib, json, subprocess, re, zipfile
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderPDF, renderSVG
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
TMP=HERE.parent/'rendered/figure_intermediates'
TMP.mkdir(parents=True, exist_ok=True)
POPPLER='/Users/lgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm'
for name,file in [('Arial','Arial.ttf'),('Arial-Bold','Arial Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+file))
W,H=504,547.2
INK='#172C3D';BLUE='#315E86';GRAY='#566573';LINE='#AEBBC5'
PALE='#F0F5F9';RED='#943D32';AMBER='#775717'

class Figure:
    def __init__(self,number,title,subtitle):
        self.d=Drawing(W,H);self.number=number;self.title=title;self.checks=[]
        self.d.add(Rect(0,0,W,H,fillColor=HexColor('#FFFFFF'),strokeColor=None))
        self.text(22,22,f'Figure {number}. {title}',14,True)
        self.text(22,46,subtitle,9.4,color=GRAY)
    def text(self,x,y,s,size=10,bold=False,color=INK,width=None,leading=None):
        font='Arial-Bold' if bold else 'Arial';leading=leading or size*1.32
        lines=[]
        for explicit in s.split('\n'):
            if width:
                current=''
                for word in explicit.split():
                    trial=(current+' '+word).strip()
                    if current and pdfmetrics.stringWidth(trial,font,size)>width:
                        lines.append(current);current=word
                    else:current=trial
                lines.append(current)
            else:lines.append(explicit)
        ascent,descent=pdfmetrics.getAscentDescent(font,size)
        for i,line in enumerate(lines):
            length=pdfmetrics.stringWidth(line,font,size)
            bottom=y+i*leading+ascent-descent
            assert x>=16 and x+length<=W-16,(self.number,line,x+length)
            assert y>=10 and bottom<=H-10,(self.number,line,bottom)
            self.d.add(String(x,H-y-ascent-i*leading,line,fontName=font,fontSize=size,fillColor=HexColor(color)))
        return y+len(lines)*leading
    def box(self,x,y,w,h,title,body,size=10,fill=PALE,color=BLUE):
        self.d.add(Rect(x,H-y-h,w,h,rx=3,ry=3,fillColor=HexColor(fill),strokeColor=HexColor(color),strokeWidth=.8))
        end=self.text(x+12,y+11,title,10.4,True,color,width=w-24)
        end=self.text(x+12,end+7,body,size,width=w-24)
        assert end<=y+h-6,(self.number,title,end,y+h)
    def arrow(self,x1,y1,x2,y2,dashed=False):
        self.d.add(Line(x1,H-y1,x2,H-y2,strokeColor=HexColor(BLUE),strokeWidth=1,strokeDashArray=[3,3] if dashed else None))
        self.d.add(Polygon([x2,H-y2,x2-3,H-y2+6,x2+3,H-y2+6],fillColor=HexColor(BLUE),strokeColor=None))
    def footer(self,s,y=500):
        self.text(22,y,s,9,width=460,color=GRAY)
    def save(self,stem):
        svg=HERE/(stem+'.svg');png=HERE/(stem+'.png');pdf=TMP/(stem+'.pdf')
        renderSVG.drawToFile(self.d,str(svg))
        c=Canvas(str(pdf),pagesize=(W,H),pageCompression=1)
        c.setTitle(f'Figure {self.number}. {self.title}')
        renderPDF.draw(self.d,c,0,0);c.showPage();c.save()
        subprocess.run([POPPLER,'-r','300','-singlefile','-png',str(pdf),str(HERE/stem)],check=True)
        return [svg,png]

def eligibility():
    f=Figure(2,'Inclusion and exclusion criteria','Adopted scope: 16 Sep 2026 | Operational screening proposed: 21 Sep 2026')
    f.box(22,70,460,64,'REVIEW POPULATION AND OUTCOMES',
        'Cisgender women and men; retain eligible Medicare beneficiaries under 65. Coverage, payment, patient costs and clinically indicated care access.',9.8)
    f.box(22,146,224,116,'PATIENT EVIDENCE',
        'Relevant original Medicare research with a sex comparison or a clinical-need/access question within an eligible sex-linked population. Establish patient eligibility.',9.8)
    f.box(258,146,224,116,'SERVICE VALUATION',
        'Original service/code research involving Medicare, with a sex-related valuation question and defensible comparators. Code-only results require no patient-identity assessment.',9.8)
    f.box(22,274,224,121,'EXCLUDE FROM PRIMARY',
        'Transgender-focused patient studies; gender-affirming-care indications. Combined mixed-population estimates without separable eligible cisgender results. Retain citation and reason.',9.6,fill='#FBF4F2',color=RED)
    f.box(258,274,224,121,'AWAITING INFORMATION',
        'Recorded male/female sex with identity unreported: clarify; never infer cisgender identity. Unclear eligibility remains pending. Log unretrieved reports separately.',9.6,fill='#FCF8EB',color=AMBER)
    f.box(22,407,460,77,'RETAIN SEPARATELY AS CONTEXT',
        'Policy/formulary sources, clinical reviews, physician-gender research, other-payer evidence and general intervention studies. Policy sources have no patient-identity test; eligible empirical findings use the routes above.',9.5,fill='#F5F7F8',color=GRAY)
    f.footer('No opposite-sex counterpart is required. Retain null/opposing findings. No automatic exclusion by language or access. Final eligibility and selection counts remain pending.')
    return f.save('figure2_eligibility_criteria')

def streams(spec):
    f=Figure(1,'Separate the subjects of comparison','Analytical framework | Preserve units, measured variables and inference limits')
    for i,p in enumerate(spec['panels']):
        body='\n\n'.join(p['lines'])+'\n\n'+p['boundary']
        f.box(22+i*158,77,144,315,p['title'],body,9.6,fill=PALE if i<2 else '#F5F7F8',color=BLUE if i<2 else GRAY)
    b=spec['supporting_band']
    f.box(22,411,460,73,b['title'],b['text'],10,fill='#F5F7F8',color=GRAY)
    f.footer(spec['footer'])
    return f.save('figure1_evidence_streams')

def clinical(spec):
    f=Figure(3,'Clinical anatomy and physiology','Classify each care indication | Categories describe services, not patient identity')
    for i,p in enumerate(spec['panels']):
        x=22+(i%2)*236;y=77+(i//2)*121
        f.box(x,y,224,109,p['title'],'\n'.join(p['lines']),9.8)
    f.text(22,449,'Record separate descriptors',10.4,True,color=BLUE)
    f.text(22,469,'Policy eligibility: sex-defined rules.   Disease burden: need and distribution.',9.5,width=460)
    f.footer(spec['footer'])
    return f.save('figure3_clinical_basis')

def pathway(spec):
    f=Figure(5,'Financing and care outcomes','Measurement framework | Dashed links show relationships to evaluate')
    b=spec['context_band'];f.box(22,74,460,67,b['title'],b['text'],10)
    for i,p in enumerate(spec['panels'][:3]):
        f.box(22+i*158,161,144,139,p['title'],'\n'.join(p['lines'])+'\n\n'+p['measurement_question'],9.5)
        f.arrow(94+i*158,300,252,333,dashed=True)
    p=spec['panels'][3]
    f.box(87,335,330,67,p['title'],'; '.join(p['lines']),9.8)
    f.arrow(252,402,252,426,dashed=True)
    p=spec['panels'][4]
    f.box(87,428,330,62,p['title'],'; '.join(p['lines']),9.8)
    f.footer('Links are hypotheses, with unestablished effects. Retain payer, policy year, age and entitlement. Assess equitable reach separately from average benefit.')
    return f.save('figure5_financing_care')

def opportunities(spec):
    f=Figure(6,'Health IT research opportunities','Six unranked domains | Workflows and evaluation targets are proposals')
    for i,p in enumerate(spec['panels']):
        f.box(22+(i%2)*236,79+(i//2)*137,224,124,p['label']+'  '+p['title'],'\n\n'.join(p['lines']),9.6)
    f.footer(spec['footer'])
    return f.save('figure6_opportunity_domains')

def build_manifest(content):
    base=json.loads((HERE/'figure_manifest.json').read_text())
    records=[]
    mapping=[(1,'figure1_evidence_streams',content[0]),(3,'figure3_clinical_basis',content[1]),
             (5,'figure5_financing_care',content[2]),(6,'figure6_opportunity_domains',content[3])]
    for number,stem,spec in mapping:
        records.append({'number':number,'title':spec['title'],'png':stem+'.png','svg':stem+'.svg',
            'caption':spec['caption'],'alt_text':spec['figure_type']+'. '+spec['footer'],
            'source_paths':spec['local_source_paths'],'source_ids':spec['source_ids']})
    records.append({'number':2,'title':'Inclusion and exclusion criteria','png':'figure2_eligibility_criteria.png',
        'svg':'figure2_eligibility_criteria.svg','alt_text':'Adopted population scope, proposed screening routes, exclusions, unresolved eligibility and context are distinguished. No selection counts.',
        'caption':'The adopted September 16 scope is distinguished from operational screening proposed September 21. Original Medicare, Medicare Advantage and Part D results are extracted separately. Mixed populations contribute only separable eligible results; unreported gender identity remains unresolved rather than inferred. Code-only research has no individual patient-identity assessment, whereas any patient component requires one. Clinical need is assessed independently of coverage. Contextual records and exclusion reasons remain in the audit trail. The compact framework summarizes REVIEW_SCOPE.md and draft protocol sections 2, 3 and 6; it is not a completed PRISMA selection flow. [M-001]',
        'source_paths':['REVIEW_SCOPE.md','research/submission/Medicare_systematic_review_protocol.md'],'source_ids':['M-001']})
    records.append({'number':4,'title':'Retrieval and review status','png':'figure4_retrieval_status.png',
        'svg':'figure4_retrieval_status.svg','alt_text':'59,147 unique report records identified; human screening and appraisal pending. The selected 38-record register is separate.',
        'caption':'Counts describe executed PubMed development searches as of September 21, 2026. Each unique PMID is a report record, not necessarily an independent study. Search extensions were developed after the initial search. No counts of full-text exclusions or final included studies are inferred. The selected 38-record register and targeted intervention retrieval are separate routes requiring later reconciliation. This is an audit diagram, not a completed PRISMA selection flow.',
        'source_paths':base['source_files'],'source_ids':[]})
    records.append({'number':7,'title':'A health IT validation pathway','png':'figure7_validation_pathway.png',
        'svg':'figure7_validation_pathway.svg','alt_text':'Need, mechanism, intervention, benefit and equity, and implementation require distinct evidence.',
        'caption':'Conceptual framework developed for this project after exploratory evidence review. Each stage requires a specified patient population, clinical indication and appropriate comparator. Progress may reveal that clinical support, policy change or an existing service is more useful than new software. Average benefit, equitable reach and commercial feasibility require separate evidence; no composite score or profitability ranking is implied.',
        'source_paths':['research/publication_2026-09-21/manuscript.md','research/publication_2026-09-21/opportunities.json'],'source_ids':[]})
    records.sort(key=lambda r:r['number'])
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    for r in records:
        r['source_sha256']={s:sha(ROOT/s) for s in r['source_paths']}
        r['output_sha256']={e:sha(HERE/r[e]) for e in ['png','svg']}
    manifest={'prepared_on':'2026-09-21','edition':'Seven-figure expanded research and white-paper edition',
        'figure_count':7,'dimensions_inches':[7,7.6],'png_dpi':300,'editable_svg_text':True,
        'new_evidence_added':False,'population_scope_changed':False,'figures':records}
    (HERE/'expanded_figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    caption='# Seven figure publication captions\n\nExpanded research edition, September 21, 2026. Figure numbering follows first citation. Final journal allocation between main text and supplement remains to be determined.\n\n'
    for r in records:caption+=f"## Figure {r['number']} {r['title']}\n\n{r['caption']}\n\n"
    caption+='Scientific source metadata and numeric PMIDs are in the accompanying reference provenance JSON and the living bibliography.\n'
    (HERE/'expanded_figure_captions.md').write_text(caption)
    out=ROOT/'outputs/01a0ab2c-c289-74e3-8442-d7966be4cbe8/Medicare_seven_publication_figures_2026-09-21.zip'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for r in records:
            for ext in ['png','svg']:z.write(HERE/r[ext],r[ext])
        for name in ['expanded_figure_captions.md','expanded_figure_manifest.json','expanded_figure_content.json']:
            z.write(HERE/name,name)
    print(json.dumps({'figures':7,'svg_and_png_exports':14,'source_hashes_recorded':True,'zip':str(out)},indent=2))

if __name__=='__main__':
    content=json.loads((HERE/'expanded_figure_content.json').read_text())['figures']
    streams(content[0]);eligibility();clinical(content[1]);pathway(content[2]);opportunities(content[3])
    build_manifest(content)
