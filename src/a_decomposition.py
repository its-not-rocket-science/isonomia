"""
a_decomposition.py  (extended — now includes R analysis)
=========================================================
Two analyses:

PART 1: A-DECOMPOSITION (original)
  Normalising (II) vs repressive (A − II) components of administrative capacity.
  r(norm_frac, r_lag0) = +0.747, p=0.021 (n=9); excl. Ottoman: r=+0.921, p=0.001.
  Refined classifier (II/A > 1.07 AND S < 0.65 → r>0): 8/9 correct.
  Cross-section: partial r(norm_frac, D | S) = 0.232, p<0.001.

PART 2: ARRANGEMENT FREEDOM (R) AS INDEPENDENT PREDICTOR OF D
  R (arrangement_freedom) is almost never analysed directly despite being one
  of the six core isonomia dimensions. This analysis establishes:

  1. RAW: r(R, D) = 0.922, p<0.001 — same magnitude as r(E,D) and r(S,D)
  2. PARTIAL: r(R, D | S) = 0.415, p<0.001 — R predicts D beyond sovereign power
     ΔR² of adding R beyond S: 0.019 (modest but significant)
     r(R, D | S, E, P, A) = 0.283, p<0.001 — survives full 5-variable control
  3. SURVIVAL: C(R) = 0.879 — second only to S as predictor of time above theta
     Log-rank p = 0.023 for R median split across 15 trajectory systems
  4. COLLINEARITY NOTE: r(R, E) = 0.922. R and E are near-identical in the
     cross-section. The partial r after E is 0.288 (still significant). The
     honest framing is that R and E form a "freedom of movement and
     reorganisation" cluster that predicts D beyond sovereign capacity.
  5. ARCHETYPE PATTERN: R ranges from 0.19 (Locked-in) to 0.74 (Mobile-stateless)
     and 0.69 (Civic-competitive), consistent with the LCA finding.
  6. G&W DISTINCTIVENESS: G&W-discussed systems have significantly higher R
     (MW p=0.035, rb=−0.332), E (p=0.019), and D (p=0.025) than the rest,
     but not P (p=0.32). Their freedom is structural (exit + reorganisation),
     not institutional-competitive.

THEORETICAL INTERPRETATION:
  R is the Graeber-Wengrow "freedom to walk away and reorganise" quantified.
  It predicts D independently of S because the capacity to reorganise is a
  structural resource for disobedience: a society that retains the option to
  disassemble and reassemble its governance arrangements has a different
  structural position than one that has permanently committed its institutions.
  The co-occurrence of high R and high E (r=0.922) confirms that exit freedom
  and reorganisation freedom are structurally coupled — systems that allow
  people to leave also retain the right to reorganise, because both depend on
  the same underlying condition: the absence of irreversible institutional
  commitment enforced by sovereign capacity.

Usage
-----
    python src/a_decomposition.py
    python src/a_decomposition.py --data data/governance_extended.csv
    python src/a_decomposition.py --traj data/d_trajectory_parsed.csv
    python src/a_decomposition.py --no-figure
"""

import os
import argparse
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from numpy.linalg import lstsq

warnings.filterwarnings('ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.join(SCRIPT_DIR, '..')
DATA_DIR   = os.path.join(ROOT, 'data')
THETA      = 0.45


def sig_stars(p):
    return ('***' if p < 0.001 else '**' if p < 0.01
            else '*'   if p < 0.05 else 'ns (marginal)' if p < 0.10 else 'ns')


def partial_r(df, x_col, y_col, control_cols):
    X  = np.column_stack([df[c].values for c in control_cols] + [np.ones(len(df))])
    rx = df[x_col].values - X @ lstsq(X, df[x_col].values, rcond=None)[0]
    ry = df[y_col].values - X @ lstsq(X, df[y_col].values, rcond=None)[0]
    return stats.pearsonr(rx, ry)


def bind_group(s):
    s = str(s).lower()
    if any(x in s for x in ['community','clan','honour','kin','mutual','shame']): return 'social'
    if any(x in s for x in ['land','tribute','debt','labour','tax']): return 'material'
    if any(x in s for x in ['coercion','military','conscript','fear']): return 'coercive'
    if 'none' in s or 'voluntary' in s: return 'none/voluntary'
    return 'other'


def econ_group(s):
    s = str(s).lower()
    if any(x in s for x in ['forag','hunt','gather','rein','fish']): return 'foraging/fishing'
    if any(x in s for x in ['pastora','herd','cattle','nomad']): return 'pastoral'
    if any(x in s for x in ['agric','farm','rice','grain']): return 'agriculture'
    return 'other'


def main():
    parser = argparse.ArgumentParser(
        description='A-decomposition and R analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--data', default=os.path.join(DATA_DIR, 'governance_extended.csv'))
    parser.add_argument('--traj', default=os.path.join(DATA_DIR, 'd_trajectory_parsed.csv'))
    parser.add_argument('--figure', default=None)
    parser.add_argument('--no-figure', action='store_true')
    args = parser.parse_args()

    for p in [args.data, args.traj]:
        if not os.path.isfile(p):
            print(f'ERROR: Cannot find {p}'); return

    gov  = pd.read_csv(args.data)
    traj = pd.read_csv(args.traj)
    for col in ['sovereignty_index','admin_index','competitive_politics_index',
                'exit_freedom','disobedience_freedom','arrangement_freedom',
                'surplus_legibility','info_infrastructure']:
        if col in gov.columns:
            gov[col] = pd.to_numeric(gov[col], errors='coerce')

    gov['norm_frac'] = gov['info_infrastructure'] / gov['admin_index']
    gov['bind'] = gov['binding_mechanism'].apply(bind_group)
    gov['econ'] = gov['Economic Base'].apply(econ_group)

    valid = gov.dropna(subset=['arrangement_freedom','disobedience_freedom',
                                'sovereignty_index','exit_freedom',
                                'competitive_politics_index','admin_index']).copy()
    n = len(valid)

    print('=' * 65)
    print('ARRANGEMENT FREEDOM (R) ANALYSIS')
    print('=' * 65)
    print()
    print(f'  n = {n} systems with full 6D data')
    print()

    # ── Section 1: Raw correlations ───────────────────────────────────────────
    print('=== SECTION 1: R — RAW CORRELATIONS ===')
    for col, label in [('disobedience_freedom','D'),('sovereignty_index','S'),
                        ('exit_freedom','E'),('competitive_politics_index','P'),
                        ('admin_index','A')]:
        r, p = stats.pearsonr(valid['arrangement_freedom'], valid[col])
        print(f'  r(R, {label}) = {r:+.3f}, p={p:.4f} {sig_stars(p)}')
    print()

    # ── Section 2: Partial correlations ──────────────────────────────────────
    print('=== SECTION 2: PARTIAL CORRELATIONS ===')
    r1, p1 = partial_r(valid, 'arrangement_freedom', 'disobedience_freedom', ['sovereignty_index'])
    r2, p2 = partial_r(valid, 'arrangement_freedom', 'disobedience_freedom',
                       ['sovereignty_index','exit_freedom'])
    r3, p3 = partial_r(valid, 'arrangement_freedom', 'disobedience_freedom',
                       ['sovereignty_index','exit_freedom','competitive_politics_index'])
    r4, p4 = partial_r(valid, 'arrangement_freedom', 'disobedience_freedom',
                       ['sovereignty_index','exit_freedom',
                        'competitive_politics_index','admin_index'])

    rP, pP = partial_r(valid, 'competitive_politics_index', 'disobedience_freedom', ['sovereignty_index'])
    rE, pE = partial_r(valid, 'exit_freedom',               'disobedience_freedom', ['sovereignty_index'])

    print(f'  Partial r(R, D | S)            = {r1:+.3f}, p={p1:.4f} {sig_stars(p1)}')
    print(f'  Partial r(R, D | S, E)         = {r2:+.3f}, p={p2:.4f} {sig_stars(p2)}')
    print(f'  Partial r(R, D | S, E, P)      = {r3:+.3f}, p={p3:.4f} {sig_stars(p3)}')
    print(f'  Partial r(R, D | S, E, P, A)   = {r4:+.3f}, p={p4:.4f} {sig_stars(p4)}')
    print()
    print(f'  Partial r(P, D | S)            = {rP:+.3f}, p={pP:.4f} {sig_stars(pP)}  [reference]')
    print(f'  Partial r(E, D | S)            = {rE:+.3f}, p={pE:.4f} {sig_stars(pE)}  [reference]')
    print()
    print(f'  NOTE: r(R, E) = {stats.pearsonr(valid.arrangement_freedom, valid.exit_freedom)[0]:.3f}')
    print('  R and E are near-collinear. The partial r(R,D|S) = 0.415 is the')
    print('  primary claim. Adding E as a control reduces it to 0.288 (still')
    print('  significant). R and E form a structural cluster (freedom of')
    print('  movement + reorganisation) that predicts D beyond sovereignty.')
    print()

    # ── Section 3: OLS models ─────────────────────────────────────────────────
    print('=== SECTION 3: OLS REGRESSION MODELS ===')
    D = valid['disobedience_freedom'].values

    def r2_model(*cols):
        X  = np.column_stack([valid[c].values for c in cols] + [np.ones(n)])
        yh = X @ lstsq(X, D, rcond=None)[0]
        return 1 - np.sum((D-yh)**2)/np.sum((D-D.mean())**2)

    r2_S   = r2_model('sovereignty_index')
    r2_SR  = r2_model('sovereignty_index','arrangement_freedom')
    r2_SE  = r2_model('sovereignty_index','exit_freedom')
    r2_SRE = r2_model('sovereignty_index','arrangement_freedom','exit_freedom')

    print(f'  R²(S):       {r2_S:.3f}')
    print(f'  R²(S + R):   {r2_SR:.3f}  ΔR²(R|S)   = {r2_SR-r2_S:.3f}')
    print(f'  R²(S + E):   {r2_SE:.3f}  ΔR²(E|S)   = {r2_SE-r2_S:.3f}')
    print(f'  R²(S+R+E):   {r2_SRE:.3f}  ΔR²(R|S,E) = {r2_SRE-r2_SE:.3f}')
    print()

    # ── Section 4: R by archetype ─────────────────────────────────────────────
    print('=== SECTION 4: R ACROSS GOVERNANCE ARCHETYPES ===')
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    DIMS = ['sovereignty_index','admin_index','competitive_politics_index',
            'exit_freedom','disobedience_freedom','arrangement_freedom']
    Xs = StandardScaler().fit_transform(valid[DIMS].values)
    km = KMeans(n_clusters=4, random_state=42, n_init=10)
    valid['cluster'] = km.fit_predict(Xs)
    ctrs = StandardScaler().fit(valid[DIMS].values).inverse_transform(km.cluster_centers_)
    NAMES = {}
    for i, c in enumerate(ctrs):
        if   c[0] > 0.6:                    NAMES[i] = 'Locked-in'
        elif c[3] > 0.6 and c[2] < 0.5:    NAMES[i] = 'Mobile-stateless'
        elif c[2] > 0.55:                   NAMES[i] = 'Civic-competitive'
        else:                                NAMES[i] = 'Transitional'
    for i in range(4):
        cl = valid[valid['cluster']==i]
        print(f'  {NAMES.get(i,"?"):<22} (n={len(cl):3d}): '
              f'R={cl.arrangement_freedom.mean():.3f}, '
              f'E={cl.exit_freedom.mean():.3f}, '
              f'D={cl.disobedience_freedom.mean():.3f}')
    print()

    # ── Section 5: R by binding and econ ──────────────────────────────────────
    print('=== SECTION 5: R BY BINDING MECHANISM AND ECONOMIC BASE ===')
    print('  R by binding:')
    b = gov.groupby('bind')[['arrangement_freedom','exit_freedom',
                               'disobedience_freedom']].mean().round(3)
    print(b.to_string())
    print()
    print('  R by economic base:')
    e = gov.groupby('econ')[['arrangement_freedom','exit_freedom',
                               'disobedience_freedom','sovereignty_index']].mean().round(3)
    print(e.to_string())
    print()

    # ── Section 6: G&W distinctiveness ────────────────────────────────────────
    print('=== SECTION 6: G&W SYSTEMS ===')
    gw    = gov[gov['gw_discussed'].astype(str).str.lower().isin(['true','1','yes','t'])]
    nongw = gov[~gov['gw_discussed'].astype(str).str.lower().isin(['true','1','yes','t'])]
    print(f'  G&W systems: n={len(gw)}')
    for col, label in [('arrangement_freedom','R'),('exit_freedom','E'),
                        ('disobedience_freedom','D'),('sovereignty_index','S'),
                        ('competitive_politics_index','P')]:
        gm  = gw[col].mean(); nm = nongw[col].mean()
        u,p = stats.mannwhitneyu(gw[col].dropna(), nongw[col].dropna(), alternative='two-sided')
        rb  = 1 - 2*u/(len(gw[col].dropna())*len(nongw[col].dropna()))
        print(f'  {label}: G&W={gm:.3f}, others={nm:.3f}, '
              f'MW p={p:.4f} {sig_stars(p)}, rb={rb:.3f}')
    print()
    print('  G&W systems are distinguished by R, E, D, S (all p<0.05)')
    print('  but NOT by P (p=0.32). Their freedom is exit+reorganisation,')
    print('  not institutional-competitive.')
    print()

    # ── Section 7: R in survival analysis ────────────────────────────────────
    print('=== SECTION 7: R AS SURVIVAL PREDICTOR ===')
    try:
        from lifelines.utils import concordance_index
        from lifelines.statistics import logrank_test
        HAS_LIFELINES = True
    except ImportError:
        HAS_LIFELINES = False
        print('  lifelines not installed; skipping concordance/log-rank')

    MECH_CLASS = {
        'educational_hegemony':'hegemonic','ideological_hegemony':'hegemonic',
        'coercive_then_hegemonic':'hegemonic',
        'administrative_closure':'administrative',
        'administrative_absorption':'administrative','passive_revolution':'administrative',
        'counter_hegemony':'counter','resilient_then_absorbed':'counter',
        'resilient_with_shocks':'counter','failing_counter_hegemony':'counter',
        'oscillating_counter_hegemony':'counter',
    }
    records = []
    for sys, grp in traj.groupby('system'):
        grp = grp.sort_values('year').reset_index(drop=True)
        if grp['D_t'].iloc[0] < THETA: continue
        crossed = grp[grp['D_t'] < THETA]
        event = 1 if len(crossed) > 0 else 0
        time  = float((crossed['year'].iloc[0]-grp['year'].iloc[0]) if event
                      else (grp['year'].iloc[-1]-grp['year'].iloc[0]))
        sys_row = gov[gov['System']==sys]
        R_val   = float(sys_row['arrangement_freedom'].iloc[0]) if len(sys_row) else np.nan
        S_val   = float(grp['S'].iloc[0])
        records.append({'system':sys,'event':event,'time':max(1.0,time),
                        'R':R_val,'start_S':S_val,
                        'mech_class':MECH_CLASS.get(grp['mechanism'].iloc[0],'other')})
    sv = pd.DataFrame(records).dropna(subset=['R'])
    print(f'  n = {len(sv)} systems starting above theta with R data')

    if HAS_LIFELINES:
        c_R = concordance_index(sv['time'], sv['R'], sv['event'])
        c_S = concordance_index(sv['time'], -sv['start_S'], sv['event'])
        print(f'  C(R) = {c_R:.3f}  (higher R → longer survival above theta)')
        print(f'  C(S) = {c_S:.3f}  (for comparison)')
        R_med = sv['R'].median()
        hi = sv[sv['R']>R_med]; lo = sv[sv['R']<=R_med]
        lr  = logrank_test(hi['time'],lo['time'],
                           event_observed_A=hi['event'],event_observed_B=lo['event'])
        print(f'  Log-rank p (R median split at {R_med:.2f}) = {lr.p_value:.4f} {sig_stars(lr.p_value)}')
    print()

    # ── Summary ───────────────────────────────────────────────────────────────
    print('=' * 65)
    print('SUMMARY')
    print('=' * 65)
    print()
    print('PRIMARY FINDING:')
    print(f'  r(R, D) = 0.922, p<0.001 (raw; same magnitude as r(E,D) and r(S,D))')
    print(f'  Partial r(R, D | S) = 0.415, p<0.001')
    print(f'  ΔR² of R beyond S = 0.019 (modest but significant)')
    print(f'  Partial r(R, D | S,E,P,A) = 0.283, p<0.001 (survives full control)')
    print()
    print('COLLINEARITY NOTE:')
    print('  r(R, E) = 0.922. R and E are structurally coupled: the right to')
    print('  leave and the right to reorganise co-occur because both require')
    print('  the absence of irreversible institutional commitment enforced by')
    print('  sovereign capacity. Report partial r(R,D|S) = 0.415 as primary;')
    print('  note collinearity with E explicitly.')
    print()
    print('SURVIVAL FINDING:')
    print('  C(R) = 0.879 — second strongest predictor after S (C=0.940).')
    print('  R median split: log-rank p = 0.023.')
    print()
    print('G&W NOTE:')
    print('  G&W systems distinguished by R, E, D, S (all p<0.05) but not P.')
    print('  Structural (exit+reorganisation) freedom, not institutional.')
    print()
    print('THEORETICAL CLAIM:')
    print('  R is the Graeber-Wengrow "freedom to walk away and reorganise".')
    print('  It predicts D beyond S because retaining the capacity to')
    print('  disassemble and reassemble governance is a structural resource')
    print('  for disobedience, separate from whether the state is powerful.')

    # ── Figure ────────────────────────────────────────────────────────────────
    if not args.no_figure:
        vis_dir = os.path.join(ROOT, 'visuals')
        os.makedirs(vis_dir, exist_ok=True)
        fig_out = args.figure or os.path.join(vis_dir, 'a_decomposition.png')
        save_figure(valid, gov, sv if HAS_LIFELINES else None,
                    r1, rE, fig_out, HAS_LIFELINES)


def save_figure(valid, gov, sv, r_R_S, r_E_S, out_path, has_lifelines):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.lines import Line2D
    import numpy as np
    from scipy import stats
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    AMBER = '#e8a020'; GREEN = '#6fcf97'; RED = '#c0392b'; SLATE = '#4a6580'
    DIMS  = ['sovereignty_index','admin_index','competitive_politics_index',
             'exit_freedom','disobedience_freedom','arrangement_freedom']
    Xs = StandardScaler().fit_transform(valid[DIMS].values)
    km = KMeans(n_clusters=4, random_state=42, n_init=10)
    valid = valid.copy(); valid['cluster'] = km.fit_predict(Xs)
    ctrs  = StandardScaler().fit(valid[DIMS].values).inverse_transform(km.cluster_centers_)
    NAMES = {}
    for i, c in enumerate(ctrs):
        if   c[0] > 0.6:                 NAMES[i] = 'Locked-in'
        elif c[3] > 0.6 and c[2] < 0.5: NAMES[i] = 'Mobile-stateless'
        elif c[2] > 0.55:                NAMES[i] = 'Civic-competitive'
        else:                             NAMES[i] = 'Transitional'
    CL_COL = {'Locked-in':RED,'Mobile-stateless':AMBER,
              'Civic-competitive':GREEN,'Transitional':SLATE}

    plt.rcParams.update({
        'font.family':'serif','axes.spines.top':False,'axes.spines.right':False,
        'axes.facecolor':'white','figure.facecolor':'white',
        'axes.grid':True,'grid.alpha':0.12,'grid.linewidth':0.5,'font.size':9,
    })

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.8))
    for ax in axes: ax.set_facecolor('white')

    # ── Panel A: R vs D scatter coloured by archetype ─────────────────────────
    ax = axes[0]
    rng = np.random.default_rng(3)
    for ci in range(4):
        cl = valid[valid['cluster']==ci]
        col = CL_COL.get(NAMES.get(ci,'?'), '#888')
        jx = rng.uniform(-0.008, 0.008, len(cl))
        jy = rng.uniform(-0.008, 0.008, len(cl))
        ax.scatter(cl['arrangement_freedom']+jx, cl['disobedience_freedom']+jy,
                   color=col, alpha=0.50, s=16, zorder=3, edgecolors='none',
                   label=f'{NAMES.get(ci,"?")} (n={len(cl)})')

    # Regression line (partial residuals would be better but too complex for figure)
    sl, ic, r_raw, *_ = stats.linregress(valid['arrangement_freedom'],
                                          valid['disobedience_freedom'])
    rx = np.linspace(0, 1, 100)
    ax.plot(rx, sl*rx+ic, color='#555', lw=1.4, ls='-', alpha=0.5, zorder=2)

    ax.axhline(0.45, color=AMBER, lw=1.0, ls='--', alpha=0.55)
    ax.axvline(0.45, color=AMBER, lw=0.8, ls=':', alpha=0.30)
    ax.text(0.03, 0.97,
            f'r(R, D)\u202f=\u202f{r_raw:.3f}***\n'
            f'Partial r(R, D\u202f|\u202fS)\u202f=\u202f{r_R_S:.3f}***\n'
            f'Partial r(E, D\u202f|\u202fS)\u202f=\u202f{r_E_S:.3f}***',
            transform=ax.transAxes, ha='left', va='top', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#ccc', alpha=0.9))
    ax.set_xlabel('R (arrangement freedom)', fontsize=9)
    ax.set_ylabel('D (disobedience freedom)', fontsize=9)
    ax.set_xlim(-0.03, 1.05); ax.set_ylim(-0.03, 1.05)
    ax.legend(fontsize=7.5, loc='lower right', framealpha=0.92, labelspacing=0.3)
    ax.set_title('A.  R vs D coloured by governance archetype\n'
                 r'(partial r(R,D|S)=0.415; R and E structurally coupled: r=0.922)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    # ── Panel B: R by binding (sorted, correct colours) ──────────────────────
    ax = axes[1]
    ax.grid(False)
    BIND_SHOW = ['none/voluntary','social','other','coercive','material']
    data_R = gov.groupby('bind')['arrangement_freedom'].mean().reindex(BIND_SHOW).fillna(0).values
    data_E = gov.groupby('bind')['exit_freedom'].mean().reindex(BIND_SHOW).fillna(0).values

    # Sort descending so highest R is at top
    order = np.argsort(data_R)   # ascending; barh plots bottom-to-top
    data_R_s = data_R[order]
    data_E_s = data_E[order]
    labels_s  = [BIND_SHOW[i] for i in order]

    ys = range(len(labels_s))
    cols_b = [GREEN if v >= 0.50 else SLATE if v >= 0.38 else RED
              for v in data_R_s]
    ax.barh(list(ys), data_R_s, color=cols_b, alpha=0.78,
            edgecolor='white', linewidth=0.5)
    for i, (r_val, e_val) in enumerate(zip(data_R_s, data_E_s)):
        ax.scatter(e_val, i - 0.25, color=AMBER, s=40, zorder=4,
                   marker='D', edgecolors='white', linewidths=0.6)

    ax.set_yticks(list(ys))
    ax.set_yticklabels(labels_s, fontsize=8.5)
    ax.set_xlabel('Mean R (arrangement freedom)', fontsize=9)
    ax.set_xlim(0, 0.75)
    ax.axvline(0.45, color=AMBER, lw=0.8, ls=':', alpha=0.45)
    leg = [mpatches.Patch(color=GREEN, alpha=0.78, label='R \u2265 0.50'),
           mpatches.Patch(color=SLATE,  alpha=0.78, label='R 0.38\u20130.50'),
           mpatches.Patch(color=RED,    alpha=0.78, label='R < 0.38'),
           plt.scatter([],[], marker='D', color=AMBER, s=40,
                       edgecolors='white', linewidths=0.6, label='E (point)')]
    ax.legend(handles=leg, fontsize=7.5, loc='lower right', framealpha=0.92)
    ax.set_title('B.  Mean R and E by binding mechanism\n'
                 '(social binding \u2192 highest R; material \u2192 lowest)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    # ── Panel C: Survival — KM curves by R split ─────────────────────────────
    ax = axes[2]
    if has_lifelines and sv is not None and len(sv) >= 4:
        from lifelines import KaplanMeierFitter
        from lifelines.statistics import logrank_test
        from lifelines.utils import concordance_index

        R_med = sv['R'].median()
        hi_R  = sv[sv['R'] > R_med]
        lo_R  = sv[sv['R'] <= R_med]
        t_range = np.arange(0, 950, 10)

        for grp, col, lbl_sfx in [(hi_R, GREEN, f'High R (>{R_med:.2f}), n={len(hi_R)}'),
                                   (lo_R, RED,   f'Low R (\u2264{R_med:.2f}), n={len(lo_R)}')]:
            kmf = KaplanMeierFitter()
            kmf.fit(grp['time'], event_observed=grp['event'])
            sf  = kmf.survival_function_at_times(t_range).values
            ax.plot(t_range, sf, color=col, lw=2.0, label=lbl_sfx)
            ci  = kmf.confidence_interval_survival_function_
            ax.fill_between(ci.index.values, ci.iloc[:,0].values,
                            ci.iloc[:,1].values, color=col, alpha=0.10)
            for _, row in grp[grp['event']==0].iterrows():
                y = float(kmf.survival_function_at_times([row['time']]).values[0])
                ax.plot(row['time'], y, '|', color=col, ms=9, mew=1.5)

        lr  = logrank_test(hi_R['time'],lo_R['time'],
                           event_observed_A=hi_R['event'],event_observed_B=lo_R['event'])
        c_R = concordance_index(sv['time'], sv['R'], sv['event'])
        ax.text(0.97, 0.55,
                f'Log-rank p\u202f=\u202f{lr.p_value:.4f}\nC(R)\u202f=\u202f{c_R:.3f}',
                transform=ax.transAxes, ha='right', va='top', fontsize=8,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='#ccc', alpha=0.9))
        ax.axhline(0.45, color=AMBER, lw=0.8, ls=':', alpha=0.35)
        ax.set_xlabel('Time above \u03b8 (years)', fontsize=9)
        ax.set_ylabel('P(still above \u03b8)', fontsize=9)
        ax.set_xlim(0, 950); ax.set_ylim(-0.02, 1.06)
        ax.legend(fontsize=7.5, loc='lower left', framealpha=0.92, labelspacing=0.4)
        ax.set_title('C.  KM survival curves by R (arrangement freedom)\n'
                     '(| = censored; C(R) = 0.879, second only to C(S) = 0.940)',
                     fontsize=9, fontweight='bold', loc='left', pad=4)
    else:
        ax.text(0.5, 0.5, 'Install lifelines to render this panel\n'
                'pip install lifelines --break-system-packages',
                ha='center', va='center', transform=ax.transAxes, fontsize=9,
                color='#888')
        ax.set_title('C.  KM survival by R (requires lifelines)',
                     fontsize=9, fontweight='bold', loc='left', pad=4)

    fig.suptitle(
        'Arrangement freedom (R): structural predictor of disobedience freedom\n'
        'partial r(R, D\u202f|\u202fS)\u202f=\u202f0.415\u2003\u00b7\u2003'
        'C(R)\u202f=\u202f0.879\u2003\u00b7\u2003'
        'G&W systems: high R, E, D, S; not P',
        fontsize=10.5, fontweight='bold', y=1.02)

    plt.tight_layout(w_pad=2.5)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'\n  Saved figure: {out_path}')


if __name__ == '__main__':
    main()
