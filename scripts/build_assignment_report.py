#!/usr/bin/env python3
"""Render REPORT.md into a short PDF and include the generated alignment figure."""
from pathlib import Path
import re, html
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'REPORT.md'; target=ROOT/'outputs'/'Assignment_2a_Alignment_Report.pdf'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportTitle',parent=styles['Title'],fontSize=19,leading=23,alignment=TA_CENTER,textColor=colors.HexColor('#143d59'),spaceAfter=8))
styles.add(ParagraphStyle(name='H2x',parent=styles['Heading2'],fontSize=13,leading=16,textColor=colors.HexColor('#1f5a7a'),spaceBefore=10,spaceAfter=5))
styles.add(ParagraphStyle(name='Bodyx',parent=styles['BodyText'],fontSize=9.3,leading=13,spaceAfter=6))

def inline(s):
    s=html.escape(s,quote=False)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`(.+?)`',r'<font name="Courier">\1</font>',s)
    return s

def page_num(canvas,doc):
    canvas.saveState(); canvas.setFont('Helvetica',8); canvas.setFillColor(colors.grey)
    canvas.drawString(0.65*inch,0.38*inch,'Assignment 2a · Forced alignment · Praat-checked sample')
    canvas.drawRightString(7.85*inch,0.38*inch,str(doc.page)); canvas.restoreState()

lines=source.read_text(encoding='utf-8').splitlines(); story=[]; i=0
while i<len(lines):
    raw=lines[i].strip()
    if not raw: i+=1; continue
    if raw.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-{3,}:?',c or '-') for c in cells): rows.append(cells)
            i+=1
        if rows:
            data=[[Paragraph(inline(c),styles['Bodyx']) for c in row] for row in rows]
            widths=[1.65*inch]+[(6.95*inch-1.65*inch)/(len(data[0])-1)]*(len(data[0])-1) if len(data[0])>1 else [6.95*inch]
            tab=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
            tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dceaf2')),('TEXTCOLOR',(0,0),(-1,0),colors.HexColor('#143d59')),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#9aabb5')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
            story.extend([tab,Spacer(1,7)])
        continue
    if raw.startswith('# '): story.append(Paragraph(inline(raw[2:]),styles['ReportTitle'])); i+=1; continue
    if raw.startswith('## '): story.append(Paragraph(inline(raw[3:]),styles['H2x'])); i+=1; continue
    if raw.startswith('### '): story.append(Paragraph(inline(raw[4:]),styles['Heading3'])); i+=1; continue
    if raw.startswith('- '): story.append(Paragraph('• '+inline(raw[2:]),styles['Bodyx'])); i+=1; continue
    if re.match(r'^\d+\.\s',raw):
        content=re.sub(r'^\d+\.\s*','',raw)
        story.append(Paragraph('• '+inline(content),styles['Bodyx'])); i+=1; continue
    if raw.startswith('---'): i+=1; continue
    story.append(Paragraph(inline(raw),styles['Bodyx']))
    if 'outputs/sample_alignment.png' in raw:
        fig=ROOT/'outputs'/'sample_alignment.png'
        if fig.exists(): story.extend([Spacer(1,4),Image(str(fig),width=7.0*inch,height=3.2*inch),Spacer(1,8)])
    if 'outputs/praat_manual_inspection_sample.png' in raw:
        fig=ROOT/'outputs'/'praat_manual_inspection_sample.png'
        if fig.exists():
            story.append(Paragraph('<b>Praat Editor screenshot supplied by the student:</b>',styles['Bodyx']))
            story.extend([Spacer(1,3),Image(str(fig),width=7.0*inch,height=3.94*inch),Spacer(1,8)])
    i+=1

target.parent.mkdir(parents=True,exist_ok=True)
doc=SimpleDocTemplate(str(target),pagesize=letter,rightMargin=.65*inch,leftMargin=.65*inch,topMargin=.58*inch,bottomMargin=.65*inch,title='Assignment 2a Forced Alignment Report')
doc.build(story,onFirstPage=page_num,onLaterPages=page_num)
print(f'Created {target}')
