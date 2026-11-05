from tex_common import *
p=D['p2']; b=p['base']; plan=p['plan']; pj=plan['proj']
acts=p['acts']
def rng(x,key):
    v=x.get(key); 
    return '--' if not v else f'{v[0]*100:+.0f} to {v[1]*100:+.0f}'
tab='\n'.join(f'{ACT_EN[a["id"]]} & {rng(a["eff"],"c")} & {rng(a["eff"],"v")} & {rng(a["eff"],"e")} & {rng(a["eff"],"s")} & {a["effort"]} & {n0(a["imp"]["lo"])} / {n0(a["imp"]["mid"])} / {n0(a["imp"]["hi"])}\\\\' for a in sorted(acts,key=lambda a:-a['imp']['mid']))
six=[sum(pj[k][:6])-sum(pj['base'][:6]) for k in ('lo','mid','hi')]
cap=p['cap']
capt='\n'.join(f'{x} & {n0(c["clicks"])} & {n0(c["extra"])} & {c["cpcUp"]*100:.0f}\\%\\\\' for x,c in cap)
tor=dict(p['tor'])
cnt={}
for br in BRANDS:
    for k,v in br['comps'].items(): cnt[k]=cnt.get(k,0)+v
topc=sorted(cnt.items(),key=lambda x:-x[1])[:3]
abstract=r'''Performance marketing for consumer-finance lead generation is usually discussed as a collection of tactics. We argue that most of it can be organised around one accounting identity, $\mathrm{ROAS}=\mathrm{CVR}\times \mathrm{EPL}/\mathrm{CPC}$, and a small set of levers that move its terms. We describe a media-buying advisor that (i) diagnoses an account from spend, ROAS, CPC, conversion and impression share, (ii) places the account against a reference portfolio of nine anonymised accounts and the competitors that appear in their auctions, (iii) compares ad copy against competitor copy, and (iv) ranks a catalogue of 15 actions by estimated profit uplift, with low, mid and high scenarios. In a worked example (monthly spend of 20{,}000 euros, ROAS 90\%) a five-action plan lifts ROAS to between @@RLO@@ and @@RHI@@. The uplift ranges are hypotheses derived from practitioner principles, not measured results, and we describe how to test them.'''
body=r'''
\section{Introduction}
Lead generators buy traffic on search and social platforms, sell the resulting leads to lenders, and are judged on return on ad spend (ROAS). Advice in this area is often a list of tactics without a way to compare them. This paper describes a decision-support tool, the \emph{Media Buying Advisor}, built around the unit economics of a lead and the practitioner knowledge of an operator who manages accounts in several markets.

\section{Unit economics}
Let $S$ be monthly spend, $c$ the average cost per click (CPC), $v$ the click-to-lead conversion rate, and $e$ the earnings per lead (EPL, the revenue obtained by selling a lead on average). Then
\begin{align}
 \text{clicks}=S/c,\qquad \text{leads}=Sv/c,\qquad \text{CPL}=c/v,\qquad \text{revenue}=\text{leads}\times e,
\end{align}
\begin{equation}
 \mathrm{ROAS}=\frac{\text{revenue}}{S}=\frac{v\,e}{c},\qquad c^{*}=v\,e,
\end{equation}
where $c^{*}$ is the break-even CPC. Profit from media is $S(\mathrm{ROAS}-1)$, before staff and tooling. A lever is a multiplicative change in one of $c$, $v$, $e$ or $S$. If an action changes them by relative amounts $\delta_c,\delta_v,\delta_e,\delta_s$ then the new ROAS is $\mathrm{ROAS}\,(1+\delta_v)(1+\delta_e)/(1+\delta_c)$ and the new profit is $S(1+\delta_s)\,[\mathrm{ROAS}'-1]$. This is the engine behind every number in the tool.

\subsection{Combining actions}
Actions overlap: two improvements to landing pages do not add. We combine a plan by multiplying lever factors after damping each effect by $0.7$, that is $\prod_k(1+0.7\,\delta^{(k)})$ per lever. The factor is a judgement, not an estimate, and it is exposed so users can change it.

\section{Operating principles}
The action catalogue encodes principles taken from a practitioner question-and-answer document. We summarise those that drive the model:
\begin{itemize}\setlength{\itemsep}{1pt}
\item Start campaigns with target CPA bidding; move to target ROAS only when a campaign runs stably on its own, because changing the global EPL disturbs ROAS targets.
\item Feed the bidding algorithm many predictable conversion signals, for example a first-call acceptance signal valued close to EPL, rather than only the scarce final sales.
\item Exclude users already in the database through an API and buy only new users; reactivate old users with email and SMS rather than platform remarketing.
\item Do not add negative keywords by default from day one; remove keywords using conversion value per partner, and treat low-quality demand (for example, borrowers with payment-default records) as separate campaigns with their own landing pages.
\item Budgets for branded and competitor campaigns exceed demand and spend only what demand allows; generic campaigns are tested at roughly 500 euros a day and not cut because of poor early performance.
\item Review daily, optimise weekly, and log every change with the effect observed a week later.
\end{itemize}

\section{Reference portfolio}
The tool is calibrated against nine anonymised accounts across five markets (December 2023 to April 2026, the last month incomplete). Figure~\ref{fig:roas} shows monthly ROAS for the nine accounts: the middle 80\% of account-months lie between 23\% and 106\%, individual months range from near zero to above 200\%, and the same account can swing by tens of points from one month to the next. Competition is also visible. The weekly auction reports name rivals; the most frequently cited are Competitor1, Competitor2 and Competitor3 in our anonymised labelling (Figure~\ref{fig:comp}). Reported impression share is typically between 11\% and 16\% (median about 14\%; Figure~\ref{fig:is}), which means substantial volume is available if returns allow.
@@F1@@
@@F2@@
@@F3@@

\section{Diagnosis}
The worked example uses spend of @@S@@ per month, ROAS 90\%, CPC 0.95\,\texteuro{}, conversion 9\% and impression share 15\%. These imply an EPL of @@EPL@@, a CPL of @@CPL@@ and a break-even CPC of @@BE@@. The account loses @@LOSS@@ a month in media. Figure~\ref{fig:heat} maps ROAS for combinations of CPC and conversion around this point: the account becomes profitable if either CPC falls by about 10\% or conversion rises by about 10\%.
\begin{figure}[H]\centering\includegraphics[width=0.62\linewidth]{fig/p2_heat.pdf}\caption{ROAS as a function of CPC and click-to-lead conversion for the worked example.}\label{fig:heat}\end{figure}
Figure~\ref{fig:tor} shows sensitivity to $\pm20\%$ changes. Conversion and EPL move profit by about @@T1@@ per 20\%, CPC by about @@T2@@, and a 20\% rise in volume changes profit by @@T3@@, because an account below break-even loses more as it scales.
@@F4@@
\subsection{Problem triage}
The tool accepts a stated problem and reorders actions. \emph{No traffic}: check impression share, bid and budget limits, and widen match types and signals. \emph{Traffic too expensive}: rewrite ads against competitors to lift quality, remove expensive keywords with low value, adjust schedules. \emph{Low conversion}: shorten the form, align landing pages with queries, and audit server-side tracking. \emph{Low quality}: separate low-quality demand, send values only for the partners that matter, and exclude existing users. \emph{ROAS falling}: audit tracking first, then review per-partner approval by campaign.

\subsection{Capacity}
If clicks scale with impression share, raising it from 15\% to a target $s$ gives $\text{clicks}\times s/15$. We assume CPC rises by $0.3\%$ for every 1\% of extra clicks. Table~\ref{tab:cap} gives the result for the example.
\begin{table}[H]\centering\small\caption{Click capacity in the worked example (baseline impression share 15\%).}\label{tab:cap}
\begin{tabular}{rrrr}\toprule Target share (\%) & Clicks & Extra clicks & CPC increase\\\midrule
@@CAP@@
\bottomrule\end{tabular}\end{table}

\section{Action catalogue and uplift}
Table~\ref{tab:acts} lists 15 actions with the relative change they induce in CPC, conversion, EPL and volume, as low-to-high ranges in percent, an effort score (1 easy, 3 hard), and the resulting monthly profit change in euros for the worked example (low / mid / high). The ranges are our hypotheses informed by the principles above.
\begin{table}[H]\centering\scriptsize\caption{Action catalogue (changes in percent; profit impact in euros per month).}\label{tab:acts}
\begin{tabular}{p{5.6cm}rrrrrr}\toprule Action & CPC & Conv. & EPL & Vol. & Effort & Impact (lo/mid/hi)\\\midrule
@@TAB@@
\bottomrule\end{tabular}\end{table}
@@F5@@
A plan of five actions (@@PLANIDS@@) lifts ROAS to @@RLO@@, @@RMID@@ and @@RHI@@ in the low, mid and high scenarios, and monthly profit from @@BASEP@@ to a steady state between @@PLO@@ and @@PHI@@. With a three-month linear ramp, extra profit over six months is @@S6LO@@, @@S6MID@@ and @@S6HI@@ (Figure~\ref{fig:proj}).
@@F6@@

\section{Ad-copy comparison}
Search ads are compared by message coverage. Each line of ad copy is tagged for nine claims: speed, amount, no fees, fully online, trust, flexibility, rate disclosure, call to action and urgency. The tool reports the share of lines that contain each claim for the advertiser and for pasted competitor copy, and lists claims that rivals use and the advertiser does not. It does not retrieve ads; the user pastes text from public ad libraries. Advertisers must still follow platform rules for financial services and local rate-disclosure requirements.

\section{Limitations}
(i) Uplift ranges are assumptions; they should be replaced by test results as soon as they exist. (ii) The tool analyses one account at a time and does not model cross-campaign cannibalisation. (iii) Reference-portfolio data are partial and anonymised, and conversion and CPC in the tool default to market-level guesses. (iv) Profit excludes staff, tooling and partner costs. (v) Impression share is a platform-reported number whose definition changes by campaign type.

\section{Conclusion}
Expressing an account as $\mathrm{ROAS}=ve/c$ makes diagnosis and prioritisation concrete: every action is a change in one of four numbers with a testable range. The next step is to run the highest-ranked actions as controlled tests and replace the hypothesised ranges with measured ones.
'''
refs=r'''\bibitem{varian} H.~R. Varian. Position auctions. \emph{International Journal of Industrial Organization}, 25(6):1163--1178, 2007.
\bibitem{eos} B.~Edelman, M.~Ostrovsky, M.~Schwarz. Internet advertising and the generalized second-price auction. \emph{American Economic Review}, 97(1):242--259, 2007.'''
epl=.9*.95/.09; cpl=.95/.09
def rep(t):
    d={'RLO':pc(plan['roas'][0],0),'RMID':pc(plan['roas'][1],0),'RHI':pc(plan['roas'][2],0),'S':E(20000),'EPL':f'{epl:.2f}\\,\\texteuro{{}}','CPL':f'{cpl:.2f}\\,\\texteuro{{}}','BE':f'{p["be"]:.2f}\\,\\texteuro{{}}','LOSS':E(-b['profit']),
       'T1':E(tor['EPL +20%']),'T2':E(tor['CPC -20%']),'T3':E(tor['Volume +20%']),'CAP':capt,'TAB':tab,'PLANIDS':'first-call CPL signal, excluding existing users, separate low-quality campaigns, value-based negative keywords and per-campaign landing pages','BASEP':E(b['profit']),'PLO':E(pj['lo'][-1]),'PHI':E(pj['hi'][-1]),
       'S6LO':E(six[0]),'S6MID':E(six[1]),'S6HI':E(six[2]),
       'F1':fig('p2_roas','Monthly ROAS of the nine anonymised accounts since 2024; the dashed line is break-even.').replace('\\caption','\\label{fig:roas}\\caption'),
       'F2':fig('p2_comp','Competitors most often cited in weekly auction reports (anonymised labels).',"0.8").replace('\\caption','\\label{fig:comp}\\caption'),
       'F3':fig('p2_is','Average impression share and position across accounts.',"0.8").replace('\\caption','\\label{fig:is}\\caption'),
       'F4':fig('p2_tor','Change in monthly profit for $\\pm20\\%$ changes in each lever (worked example).',"0.8").replace('\\caption','\\label{fig:tor}\\caption'),
       'F5':fig('p2_actions','Estimated monthly profit impact of each action in the worked example.',"0.95").replace('\\caption','\\label{fig:act}\\caption'),
       'F6':fig('p2_proj','Monthly profit with no change and with the five-action plan.',"0.8").replace('\\caption','\\label{fig:proj}\\caption')}
    for k,v in d.items(): t=t.replace('@@'+k+'@@',v)
    return t
open(ROOT/'paper'/'paper.tex','w').write(make('Media Buying Advisor: Unit Economics and Action Ranking for Financial Lead Generation','Diagnosing accounts, reading the auction and estimating uplift',rep(abstract),rep(body),refs))
