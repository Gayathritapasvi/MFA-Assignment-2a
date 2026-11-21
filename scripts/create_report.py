#!/usr/bin/env python3
"""Regenerate the sample alignment plot and report PDF from current TextGrid outputs."""
from pathlib import Path
import re, subprocess, sys
import numpy as np
import soundfile as sf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
name='ISLE_SESS0131_BLOCKD02_01_sprt1'
wav=ROOT/'data/corpus/ISLE_SESS0131'/f'{name}.wav'
grid=ROOT/'outputs/textgrids/ISLE_SESS0131'/f'{name}.TextGrid'
if not wav.exists() or not grid.exists():
    raise SystemExit('Generate the prepared WAV and TextGrid before building the report.')
text=grid.read_text(encoding='utf-8')
sections=re.split(r'\n\s*item \[\d+\]:',text)[1:]
def intervals(section):
    return [(float(a),float(b),label) for a,b,label in re.findall(r'xmin\s*=\s*([\d.]+)\s+xmax\s*=\s*([\d.]+)\s+text\s*=\s*"([^"]*)"',section)]
if len(sections)<2:
    raise SystemExit(f'Expected word and phone tiers in {grid}')
words,phones=map(intervals,sections[:2])
audio,rate=sf.read(wav); ts=np.arange(len(audio))/rate
fig,ax=plt.subplots(3,1,figsize=(10,4.8),sharex=True,gridspec_kw={'height_ratios':[2,1,1]})
ax[0].plot(ts,audio,linewidth=.5,color='#286196'); ax[0].set_ylabel('Amplitude'); ax[0].set_title('Waveform with MFA TextGrid intervals (programmatic visualization)')
for axis,items,title in [(ax[1],words,'Words'),(ax[2],phones,'Phones')]:
    for start,end,label in items:
        axis.axvspan(start,end,alpha=.15,color='#4887b3'); axis.axvline(start,color='#59809e',lw=.6)
        if end-start>.035: axis.text((start+end)/2,.5,label,ha='center',va='center',fontsize=7,rotation=0 if title=='Words' else 90)
    axis.set_yticks([]); axis.set_ylabel(title)
ax[2].set_xlabel('Time (seconds)'); ax[2].set_xlim(0,len(audio)/rate); fig.tight_layout()
figpath=ROOT/'outputs'/'sample_alignment.png'; fig.savefig(figpath,dpi=170); plt.close(fig)
subprocess.run([sys.executable,str(ROOT/'scripts'/'build_assignment_report.py')],check=True)
print(f'Created {figpath} and outputs/Assignment_2a_Alignment_Report.pdf')
