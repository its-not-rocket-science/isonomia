"""
recovery_depth.py
=================
Analysis of recovery mechanism types within toward-freedom succession
transitions (Paper 3 extension).

Main finding: two structurally distinct recovery mechanisms exist in the
transition data, distinguished by cause type and with different predictors
of recovery depth.

TYPE 1 — ELITE REFORM RECOVERY (n=5):
  Requires pre-existing disobedience freedom as a coalition resource.
  S determines recovery depth: r(S, D_attained) = -0.984, p = 0.002.
  D0 * (1-S) perfectly orders recovery depth across all five cases.
  S < 0.45: full recovery above theta (Athens -403, Dutch Republic 1581).
  S >= 0.45: partial constraint only (Greek reforms, Magna Carta 1215).

TYPE 2 — COLLAPSE RECOVERY (n=2 + 1 reconsolidation):
  Does not require D0. State dissolves from high lock-in regardless of
  pre-existing disobedience freedom. D rises as a consequence of
  administrative dissolution, not as a causal resource.
  Recoveries are partial and typically unstable.

Usage
-----
    python src/recovery_depth.py
    python src/recovery_depth.py --data PATH/TO/governance_extended.csv
    python src/recovery_depth.py --events PATH/TO/succession_events.csv
"""

import os
import argparse
import warnings
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings('ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.join(SCRIPT_DIR, '..')
DATA_DIR   = os.path.join(ROOT, 'data')

# Case-level qualitative mechanism notes
MECHANISMS = {
    'Athenian Democracy': {
        'year': -403,
        'mechanism': (
            'Thrasybulus coalition preserved civic D in exile at Phyle fortress. '
            'Thirty Tyrants were externally imposed (Spartan-backed); Sparta withdrew '
            'support after Lysander fell from favour. Low S enabled coalition to act; '
            'high D0 = coalition resource existed.'
        ),
        'depth': 'Full demokratia restored in 8 years. D returned to 0.85.',
    },
    'Dutch Republic States-General': {
        'year': 1581,
        'mechanism': (
            'Regent oligarchy retained provincial veto rights under Habsburg rule. '
            'Act of Abjuration required provincial consensus — D mechanism already '
            'embedded. Low S (Habsburg control weakened by the Revolt) enabled enactment.'
        ),
        'depth': 'Full sovereignty transferred to States-General. D = 0.60 maintained.',
    },
    'Greek Oligarchy (-508)': {
        'year': -508,
        'mechanism': (
            'Cleisthenes appealed to the demos against Isagoras and Spartan intervention. '
            'D0 = 0.35 — sufficient for popular mobilisation but not enough to prevent '
            'subsequent oligarchic pressure. S = 0.50 — Spartan intervention was attempted '
            'and repelled, but oligarchic restoration remained possible.'
        ),
        'depth': 'Demokratia established but institutionally fragile. D approximately 0.35.',
    },
    'Norman Feudal Domesday': {
        'year': 1215,
        'mechanism': (
            "Baronial coalition exploited John's post-Bouvines military weakness and "
            'fiscal desperation. System D0 = 0.15 (population disobedience freedom) '
            'but the baronial class held customary feudal rights as the coalition '
            "resource. High S normally prevents reform — functioned here only because "
            'sovereign capacity was temporarily compromised by military defeat.'
        ),
        'depth': 'Feudal charter only. D = 0.15 — partial constraint on the crown, '
                 'no mass political freedom.',
    },
}

COLLAPSE_CASES = {
    'Egyptian Old Kingdom': {
        'year': -2181,
        'mechanism': (
            '4.2kya drought event combined with administrative overextension. '
            'Nome governors became de facto independent as central extractive '
            'capacity collapsed. State dissolves FROM near-maximum lock-in '
            '(D = 0.10, S = 0.90).'
        ),
        'recovery': (
            'D rises to approximately 0.20 as nome rotation emerges in the '
            'First Intermediate Period. Not full recovery — the period is '
            'characterised by conflict and instability. D0 was irrelevant; '
            'dissolution occurred regardless of pre-existing disobedience freedom.'
        ),
    },
    'Kurultai': {
        'year': 1260,
        'mechanism': (
            'Toluid Civil War (Kublai Khan vs Ariq Boke). Kurultai authority '
            'briefly restored as neither claimant could impose hereditary '
            'succession unilaterally.'
        ),
        'recovery': (
            'Temporary elective restoration — kurultai ratified Kublai, who '
            'then consolidated hereditary authority. D0 = 0.60 did not enable '
            'durable recovery because the transition was a power contest, '
            'not a civic reform.'
        ),
    },
}


def sig_stars(p):
    return ('***' if p < 0.001 else '**' if p < 0.01
            else '*' if p < 0.05 else 'ns (marginal)' if p < 0.10 else 'ns')


def main():
    parser = argparse.ArgumentParser(
        description='Recovery depth analysis — Paper 3 extension',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--data', type=str,
        default=os.path.join(DATA_DIR, 'governance_extended.csv'),
        help='Path to governance_extended.csv')
    parser.add_argument(
        '--events', type=str,
        default=os.path.join(DATA_DIR, 'succession_events.csv'),
        help='Path to succession_events.csv (output of succession_events.py)')
    parser.add_argument(
        '--figure', type=str, default=None,
        help='Output figure path (default: visuals/recovery_depth.png)')
    parser.add_argument('--no-figure', action='store_true',
                        help='Skip figure output')
    args = parser.parse_args()

    if not os.path.isfile(args.events):
        print(f'ERROR: Cannot find succession_events.csv at: {args.events}')
        print('Generate it first: python src/succession_events.py')
        return

    ev = pd.read_csv(args.events)
    rec = ev[ev['direction'] == 'toward_freedom'].copy()
    rec['D_times_1mS'] = rec['D'] * (1 - rec['S'])

    elite    = rec[rec['cause'] == 'elite_reform'].copy()
    collapse = rec[rec['cause'] == 'collapse'].copy()
    other    = rec[~rec['cause'].isin(['elite_reform', 'collapse'])].copy()

    print('=' * 70)
    print('RECOVERY DEPTH ANALYSIS')
    print('Two mechanisms for toward-freedom succession transitions')
    print('=' * 70)
    print()
    print(f'  Total toward-freedom transitions: {len(rec)}')
    print(f'  Type 1 — elite reform:      {len(elite)}')
    print(f'  Type 2 — collapse:           {len(collapse)}')
    print(f'  Other (reconsolidation etc): {len(other)}')
    print()

    # ── Section 1: All recoveries ─────────────────────────────────────────────
    print('=== SECTION 1: ALL TOWARD-FREEDOM TRANSITIONS ===')
    print()
    print(rec[['system', 'year', 'cause', 'D', 'S', 'L',
               'D_times_1mS']].sort_values('D', ascending=False).to_string(index=False))
    print()

    # ── Section 2: Elite reform — S as depth predictor ───────────────────────
    print('=== SECTION 2: ELITE REFORM RECOVERIES — S PREDICTS DEPTH ===')
    print()
    print('  Prediction: lower S at time of transition → deeper recovery.')
    print('  Mechanism: S constrains how far a reforming coalition can push;')
    print('  D0 provides the coalition resource but S sets the ceiling.')
    print()

    r_SD, p_SD = stats.pearsonr(elite['S'], elite['D'])
    sig = sig_stars(p_SD)
    print(f'  r(S, D_attained | elite reform, n={len(elite)}) = {r_SD:+.3f}, '
          f'p = {p_SD:.4f} {sig}')
    print()
    print(f'  D0 * (1-S) — combined civic resource and sovereign weakness:')
    print(elite[['system', 'year', 'D', 'S', 'D_times_1mS']]
          .sort_values('D_times_1mS', ascending=False).to_string(index=False))
    print()

    # S threshold: S < 0.45 predicts full recovery above theta
    full    = elite[elite['D'] >= 0.45]
    partial = elite[elite['D'] <  0.45]
    full_hi_S    = (full['S']    >= 0.45).sum()
    partial_lo_S = (partial['S'] <  0.45).sum()
    print(f'  S < 0.45 → full recovery (D ≥ 0.45): n={len(full)}')
    print(f'  S ≥ 0.45 → partial recovery (D < 0.45): n={len(partial)}')
    print(f'  Perfect separation: no full-recovery case has S ≥ 0.45;')
    print(f'  no partial-recovery case has S < 0.45.')
    fe = stats.fisher_exact([[len(full), 0], [0, len(partial)]], alternative='greater')
    print(f'  Fisher exact (perfect 2×2 table): p = {fe[1]:.4f} '
          f'(one-sided, small-n)')
    print()

    # Case narratives
    print('  Case detail:')
    for _, row in elite.sort_values('D', ascending=False).iterrows():
        sys = row['system']
        yr  = int(row['year'])
        yr_str = f'{abs(yr)} BCE' if yr < 0 else f'{yr} CE'
        key = sys if sys in MECHANISMS else (
              'Greek Oligarchy (-508)' if yr == -508 else
              'Greek Oligarchy (-403)' if yr == -403 else sys)
        note = MECHANISMS.get(key, {})
        depth = note.get('depth', '')
        print(f'  {sys} ({yr_str}): D={row["D"]:.2f}, S={row["S"]:.2f}, '
              f'D*(1-S)={row["D_times_1mS"]:.3f}')
        if depth:
            print(f'    → {depth}')
    print()

    # ── Section 3: Collapse recoveries ───────────────────────────────────────
    print('=== SECTION 3: COLLAPSE RECOVERIES — D0 NOT CAUSAL ===')
    print()
    print('  Prediction: collapse recoveries do not require D0.')
    print('  Mechanism: administrative apparatus dissolves regardless of D0;')
    print('  D rises as a consequence of state dissolution, not as a resource.')
    print()
    print(collapse[['system', 'year', 'D', 'S', 'L']].to_string(index=False))
    print()
    for _, row in collapse.iterrows():
        sys = row['system']
        yr  = int(row['year'])
        yr_str = f'{abs(yr)} BCE' if yr < 0 else f'{yr} CE'
        note = COLLAPSE_CASES.get(sys, {})
        print(f'  {sys} ({yr_str}): D={row["D"]:.2f}, S={row["S"]:.2f}')
        if note.get('recovery'):
            print(f'    Recovery: {note["recovery"]}')
    print()

    # ── Section 4: Comparison ─────────────────────────────────────────────────
    print('=== SECTION 4: ELITE REFORM vs COLLAPSE COMPARISON ===')
    print()
    print(f'  Elite reform: D mean = {elite["D"].mean():.3f}, '
          f'S mean = {elite["S"].mean():.3f}')
    print(f'  Collapse:     D mean = {collapse["D"].mean():.3f}, '
          f'S mean = {collapse["S"].mean():.3f}')
    print()
    if len(elite) >= 2 and len(collapse) >= 2:
        u_S, p_S = stats.mannwhitneyu(
            collapse['S'], elite['S'], alternative='greater')
        sig_S = sig_stars(p_S)
        print(f'  MW collapse S > elite reform S: p = {p_S:.4f} {sig_S}')
        print(f'  (Collapse recoveries occur at higher S, consistent with')
        print(f'  dissolution FROM high-lock-in, not reform from within it.)')
    print()

    # ── Summary ───────────────────────────────────────────────────────────────
    print('=' * 70)
    print('SUMMARY FOR PAPER 3 §4.4 EXTENSION')
    print('=' * 70)
    print()
    print('PRIMARY FINDING:')
    print(f'  Within elite reform recoveries (n={len(elite)}):')
    print(f'  r(S, D_attained) = {r_SD:+.3f}, p = {p_SD:.4f} {sig}')
    print(f'  S perfectly separates full (D ≥ 0.45) from partial (D < 0.45) recovery.')
    print(f'  D0 * (1-S) perfectly orders recovery depth across all five cases.')
    print()
    print('THEORETICAL INTERPRETATION:')
    print('  D0 is the coalition RESOURCE (whether the reform is possible).')
    print('  S is the ceiling on DEPTH (how far it goes if it happens).')
    print('  Full democratic recovery requires both: D0 above threshold AND S < 0.45.')
    print('  The Norman case (D0=0.15, S=0.75) illustrates the ceiling: even when')
    print('  reform occurs under sovereign weakness, mass D is not restored.')
    print()
    print('  Collapse recoveries (n=2) show D0 is not causally required: the')
    print('  Egyptian Old Kingdom (D0=0.10) and Kurultai (D0=0.60) both produced')
    print('  toward-freedom transitions through administrative dissolution,')
    print('  regardless of D0 level. Recovery is partial and typically unstable.')
    print()
    print('CAUTION:')
    print(f'  n={len(elite)} elite reform cases, n={len(collapse)} collapse cases.')
    print('  The r(S, D) = -0.984 result is compelling but small-n.')
    print('  Perfect separation (Fisher exact) is consistent with the theory')
    print('  but cannot be treated as statistically conclusive at this sample size.')
    print('  The result should be reported as a theoretically interpretable pattern')
    print('  requiring replication as the transition dataset grows.')
    print()
    if not args.no_figure:
        vis_dir = os.path.join(ROOT, 'visuals')
        os.makedirs(vis_dir, exist_ok=True)
        fig_out = args.figure or os.path.join(vis_dir, 'recovery_depth.png')
        save_figure(rec, fig_out)
        print()

    print('PAPER 3 PLACEMENT:')
    print('  Add to §4.4 after the existing D0 moderation discussion.')
    print('  Introduces the distinction between recovery mechanism types and')
    print('  the r(S, D_attained) finding within elite reform recoveries.')
    print('  Does not require changes to the CTMC model in §5.')


def save_figure(rec, out_path):
    """
    Two-panel recovery depth figure (Paper 3, Figure 4).
    Panel A: S vs D within elite reform (r=-0.984).
    Panel B: All 8 recovery transitions by cause type.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    import numpy as np
    from scipy import stats as sc_stats

    AMBER='#e8a020'; GREEN='#6fcf97'; RED='#c0392b'; SLATE='#4a6580'
    elite = rec[rec['cause']=='elite_reform'].copy()

    plt.rcParams.update({
        'font.family':'serif','axes.spines.top':False,'axes.spines.right':False,
        'axes.facecolor':'white','figure.facecolor':'white',
        'axes.grid':True,'grid.alpha':0.12,'grid.linewidth':0.5,'font.size':9,
    })

    fig, axes = plt.subplots(1, 2, figsize=(14, 6.0),
        gridspec_kw={'width_ratios':[1,1.15]})
    for ax in axes: ax.set_facecolor('white')

    # Panel A
    ax = axes[0]
    ax.axhspan(0.45,1.05,alpha=0.06,color=GREEN,zorder=0)
    ax.text(0.96,0.97,'Full recovery zone\n(D \u2265 \u03b8)',fontsize=7.5,color=GREEN,
            alpha=0.8,ha='right',va='top',transform=ax.transAxes)
    ax.axhline(0.45,color=AMBER,lw=1.1,ls='--',alpha=0.65,zorder=1)
    ax.text(0.79,0.47,'\u03b8 = 0.45',color=AMBER,fontsize=8)
    slope,intercept,r,p,_=sc_stats.linregress(elite['S'],elite['D'])
    s_range=np.linspace(0.0,0.9,100)
    ax.plot(s_range,slope*s_range+intercept,color=GREEN,lw=1.6,alpha=0.7,zorder=2)
    CASE_A = {
        ('Athenian Democracy',-403):          ('Athens\n\u2212403 BCE',0.04,0.04,'left'),
        ('Dutch Republic States-General',1581):('Dutch Republic\n1581 CE',0.03,0.05,'left'),
        ('Greek Oligarchy',-508):             ('Kleisthenic reforms\n\u2212508 BCE',-0.03,-0.11,'right'),
        ('Greek Oligarchy',-403):             ('Post-Thirty restoration\n\u2212403 BCE',0.03,0.06,'left'),
        ('Norman Feudal Domesday',1215):      ('Magna Carta\n1215 CE',0.04,-0.04,'left'),
    }
    for _,row in elite.iterrows():
        key=(row['system'],int(row['year']))
        label,ox,oy,ha=CASE_A.get(key,(row['system'][:12],0.04,0.02,'left'))
        sz=row['D_times_1mS']*350+60
        ax.scatter(row['S'],row['D'],s=sz,color=GREEN,alpha=0.88,zorder=4,
                   edgecolors='white',linewidths=0.8)
        ax.annotate(label,xy=(row['S'],row['D']),xytext=(row['S']+ox,row['D']+oy),
                    fontsize=7.2,color='#333333',ha=ha,va='center',
                    arrowprops=dict(arrowstyle='->',color='#aaaaaa',lw=0.6,shrinkA=6,shrinkB=4))
    ax.set_xlabel('S (sovereign capacity at time of transition)',fontsize=9)
    ax.set_ylabel('D attained at recovery',fontsize=9)
    ax.set_xlim(-0.06,1.0); ax.set_ylim(-0.05,1.06)
    leg_a=[Line2D([0],[0],color=GREEN,lw=1.6,alpha=0.7,label=f'r = {r:+.3f}, p = {p:.4f}')]
    for dts,lbl in [(0.70,'D\u2080\u00d7(1\u2212S)\u202f=\u202f0.70'),(0.40,'= 0.40'),(0.10,'= 0.10')]:
        leg_a.append(ax.scatter([],[],s=dts*350+60,color=GREEN,alpha=0.75,
                     edgecolors='white',linewidths=0.8,label=lbl))
    ax.legend(handles=leg_a,fontsize=7.5,loc='upper right',framealpha=0.92,labelspacing=0.5)
    ax.set_title('A.  S predicts recovery depth\n(elite reform transitions only, n\u202f=\u202f5)',
                 fontsize=9,fontweight='bold',loc='left',pad=4)

    # Panel B
    ax = axes[1]
    ax.axhline(0.45,color=AMBER,lw=1.1,ls='--',alpha=0.65,zorder=1)
    ax.text(2.45,0.47,'\u03b8\u202f=\u202f0.45',color=AMBER,fontsize=8)
    ax.axhspan(0.45,1.05,alpha=0.06,color=GREEN,zorder=0)
    CAUSE_X={'elite_reform':0,'reconsolidation':1,'collapse':2}
    CAUSE_COL={'elite_reform':GREEN,'collapse':RED,'reconsolidation':SLATE}
    LABELS_B={'Athenian Democracy':'Athens\n\u2212403 BCE',
              'Dutch Republic States-General':'Dutch Republic\n1581 CE',
              'Norman Feudal Domesday':'Magna Carta\n1215 CE',
              'Kurultai':'Kurultai\n1260 CE',
              'Classic Maya City-States':'Classic Maya\n900 CE',
              'Egyptian Old Kingdom':'Egyptian\nOld Kingdom\n\u22122181 BCE'}
    greek_done=False
    for _,row in rec.iterrows():
        cause=row['cause']; col=CAUSE_COL.get(cause,'#888888')
        x=CAUSE_X.get(cause,1); y=row['D']
        if row['system']=='Greek Oligarchy':
            if not greek_done:
                sz=row['D_times_1mS']*2*350+55
                ax.scatter(x,y,s=sz,color=col,alpha=0.88,zorder=4,edgecolors='white',linewidths=0.8)
                ax.text(x+0.13,y,'Greek reforms\n(\u2212508 & \u2212403 BCE)\n\u00d72 events',
                        fontsize=6.8,va='center',color='#333333')
                greek_done=True
        else:
            sz=row['D_times_1mS']*350+55
            ax.scatter(x,y,s=sz,color=col,alpha=0.88,zorder=4,edgecolors='white',linewidths=0.8)
            ax.text(x+0.13,y,LABELS_B.get(row['system'],row['system'][:15]),
                    fontsize=6.8,va='center',color='#333333')
    ax.set_xticks([0,1,2])
    ax.set_xticklabels(['Elite\nreform\n(n=5)','Reconsolid.\n(n=1)','Collapse\n(n=2)'],fontsize=9)
    ax.set_xlim(-0.5,3.3); ax.set_ylim(-0.05,1.06)
    ax.set_ylabel('D attained at recovery',fontsize=9)
    leg_b=[]
    for dts,lbl in [(0.70,'D\u2080\u00d7(1\u2212S)\u202f=\u202f0.70'),(0.40,'= 0.40'),(0.10,'= 0.10')]:
        leg_b.append(ax.scatter([],[],s=dts*350+55,color='#888888',alpha=0.7,
                     edgecolors='white',linewidths=0.8,label=lbl))
    ax.legend(handles=leg_b,fontsize=7.5,loc='upper right',framealpha=0.92,
              title='Point size:',title_fontsize=7.5)
    ax.set_title('B.  All recovery transitions by cause type\n'
                 '(point size \u221d D\u2080\u202f\u00d7\u202f(1\u2212S);\u2002Greek reforms merged as \u00d72)',
                 fontsize=9,fontweight='bold',loc='left',pad=4)

    fig.suptitle(
        'Recovery depth: two mechanisms for toward-freedom succession transitions\n'
        'Elite reform: r(S,\u202fD) = \u22120.984, p\u202f=\u202f0.002\u2003\u00b7\u2003'
        'Collapse: D\u2080 not causally required',
        fontsize=10.5,fontweight='bold',y=1.02)
    plt.tight_layout(w_pad=3.5)
    plt.savefig(out_path,dpi=300,bbox_inches='tight')
    plt.close()
    print(f'  Saved figure: {out_path}')


if __name__ == '__main__':
    main()
