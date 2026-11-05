"""Regenerate every figure of the paper from results/results.json and data/.

Run:  python -m media_buying_advisor.figures
"""
import json
from pathlib import Path
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from . import data as DATA
from .labels import ACT_EN

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'paper' / 'fig'
D = json.load(open(ROOT / 'results' / 'results.json'))
BRANDS = DATA.load_accounts()
B,G,A,Rd,Gy,Pu='#2f6fe0','#12905a','#c47d0c','#c8372f','#6d7690','#7c5ce0'
plt.rcParams.update({'font.size':8.5,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.25,'grid.linewidth':.5,'figure.dpi':150,'savefig.bbox':'tight','font.family':'DejaVu Sans','legend.frameon':False})
OUT.mkdir(parents=True, exist_ok=True)
def sv(n): plt.savefig(OUT / f'{n}.pdf'); plt.close()
# ================= P2
brs=BRANDS; cols=plt.cm.tab10(np.linspace(0,1,10))
fig,ax=plt.subplots(figsize=(6.4,3.2))
for i,b in enumerate(brs):
    s=[r for r in b['series'] if r[2] is not None and r[1]>0 and r[0]>=202401]
    ax.plot(range(len(s)),[r[2] for r in s],lw=1,color=cols[i],label=b['name']) if False else None
ms=sorted({r[0] for b in brs for r in b['series'] if r[0]>=202401}); mi={m:i for i,m in enumerate(ms)}
for i,b in enumerate(brs):
    pts=[(mi[r[0]],r[2]) for r in b['series'] if r[0] in mi and r[2] is not None and r[1]>0]
    ax.plot([a for a,_ in pts],[c for _,c in pts],lw=1,color=cols[i],label=b['name'].replace('Cuenta','Account'))
ax.axhline(1,color='k',ls='--',lw=.8); ax.set_xticks(range(0,len(ms),3)); ax.set_xticklabels([f'{str(m)[:4]}-{str(m)[4:]}' for m in ms[::3]],rotation=45,ha='right'); ax.set_ylabel('ROAS (1.0 = break-even)'); ax.set_ylim(0,2.6); ax.legend(ncol=3,fontsize=6.5); sv('p2_roas')
cnt={}
for b in brs:
    for kx,v in b['comps'].items(): cnt[kx]=cnt.get(kx,0)+v
top=sorted(cnt.items(),key=lambda x:-x[1])[:12]
fig,ax=plt.subplots(figsize=(6.4,3)); ax.barh([a for a,_ in top][::-1],[b for _,b in top][::-1],color=B); ax.set_xlabel('Citations in weekly auction reports'); sv('p2_comp')
byM={}
for b in brs:
    for r in b['ins']:
        if r[0]>=202401: o=byM.setdefault(r[0],{'is':[],'pl':[]}); 
        if r[0]>=202401:
            if r[2] is not None: o['is'].append(r[2])
            if r[3] is not None: o['pl'].append(r[3])
mm=sorted(byM); fig,ax=plt.subplots(figsize=(6.4,2.8)); ax.plot(range(len(mm)),[np.mean(byM[m]['is']) if byM[m]['is'] else np.nan for m in mm],color=B,marker='o',ms=3,label='Impression share (%)'); ax.set_ylabel('Impression share (%)'); ax2=ax.twinx(); ax2.plot(range(len(mm)),[np.mean(byM[m]['pl']) if byM[m]['pl'] else np.nan for m in mm],color=A,marker='o',ms=3); ax2.invert_yaxis(); ax2.set_ylabel('Average position (lower is better)'); ax2.grid(False); ax2.spines['right'].set_visible(True); ax.set_xticks(range(0,len(mm),3)); ax.set_xticklabels([f'{str(m)[:4]}-{str(m)[4:]}' for m in mm[::3]],rotation=45,ha='right'); sv('p2_is')
ex=D['params']['worked_example']; epl=ex['roas']*ex['cpc']/ex['cvr']; cpcs=np.array([.6,.8,1,1.2,1.5])*ex['cpc']; cvrs=np.array([.6,.8,1,1.25,1.5])*ex['cvr']
Z=np.array([[cv*epl/c for c in cpcs] for cv in cvrs]); fig,ax=plt.subplots(figsize=(4.8,3.2)); im=ax.imshow(Z,cmap='RdYlGn',vmin=.2,vmax=1.8,origin='lower',aspect='auto'); ax.set_xticks(range(5)); ax.set_xticklabels([f'{c:.2f}' for c in cpcs]); ax.set_yticks(range(5)); ax.set_yticklabels([f'{c*100:.1f}%' for c in cvrs]); ax.set_xlabel('CPC (EUR)'); ax.set_ylabel('Click-to-lead conversion'); ax.grid(False)
for i in range(5):
    for j in range(5): ax.text(j,i,f'{Z[i,j]*100:.0f}%',ha='center',va='center',fontsize=7)
sv('p2_heat')
acts=sorted(D['p2']['acts'],key=lambda a:a['imp']['mid']); fig,ax=plt.subplots(figsize=(6.4,4.2)); y=np.arange(len(acts))
ax.barh(y,[a['imp']['hi']-a['imp']['lo'] for a in acts],left=[a['imp']['lo'] for a in acts],color=B,alpha=.5); ax.scatter([a['imp']['mid'] for a in acts],y,color=A,zorder=3,s=14); ax.set_yticks(y); ax.set_yticklabels([ACT_EN[a['id']].replace('\\%','%')[:64]+('...' if len(ACT_EN[a['id']])>64 else '') for a in acts],fontsize=6.5); ax.set_xlabel('Monthly profit impact (EUR); bar = low-high, dot = mid'); sv('p2_actions')
t=D['p2']['tor']; idx=np.argsort([v for _,v in t]); fig,ax=plt.subplots(figsize=(6.4,2.7)); ax.barh([t[i][0] for i in idx],[t[i][1] for i in idx],color=[G if t[i][1]>=0 else Rd for i in idx]); ax.set_xlabel('Change in monthly profit (EUR)'); sv('p2_tor')
pj=D['p2']['plan']['proj']; x=range(0,7); fig,ax=plt.subplots(figsize=(6.4,2.8)); base=D['p2']['base']['profit']
for kx,c,l in [('base',Gy,'No change'),('lo',A,'Plan, low'),('mid',B,'Plan, mid'),('hi',G,'Plan, high')]: ax.plot(x,[base]+pj[kx],color=c,marker='o',ms=3,label=l,ls='--' if kx=='base' else '-')
ax.set_xlabel('Month'); ax.set_ylabel('Monthly profit (EUR)'); ax.legend(ncol=4,fontsize=7); sv('p2_proj')

def main(): print('figures written to', OUT)
if __name__=='__main__': main()
