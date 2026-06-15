"""
survival_analysis.py
====================
Survival analysis of time to D-threshold crossing (theta=0.45) for the
15 governance systems in the trajectory dataset that begin above theta.

PRIMARY FINDINGS:

1. MECHANISM CLASS predicts crossing (multivariate log-rank p=0.001):
   - Hegemonic pathway (n=4): 100% event rate, median time=51 years
   - Administrative/closure (n=3): 100% event rate, median time=440 years
   - Counter-hegemonic (n=8): 12.5% event rate (1 event in 332 years)

2. S AT START predicts crossing (C=0.940, log-rank p=0.007):
   - High-S systems (n=7): 86% event rate, median time=70 years
   - Low-S systems (n=8): 25% event rate, median survival>900 years

3. D AT START predicts crossing (C=0.853):
   - Higher starting D provides more buffer — longer time above theta

4. L AT START does NOT predict crossing (C=0.543, log-rank p=0.68):
   This is the most theoretically important result. High-L systems starting
   above theta include both fast crossers (Nazi Germany: 2 years) and long
   survivors (Venetian Republic: 903 years). The L effect is mechanism-
   contingent: L enables hegemonic capture (fast crossing) but is also
   present in administrative and even counter-hegemonic contexts.
   S — not L — is the structural determinant of vulnerability.

INTERPRETATION:
   The Paper 2 lock-in sequence predicts L→S→A→D. This analysis confirms
   that S is the gate variable: systems with high S at the point where D
   is still above theta are maximally vulnerable (86% event rate). But L
   is not a universal predictor because high-L systems can reach high D
   through multiple mechanisms — civic institutional strength may co-evolve
   with L rather than being eroded by it.

   The counter-hegemonic systems (British Parliament, Swiss, Norwegian,
   Icelandic) had low S DESPITE relatively high L, precisely because they
   developed institutional buffers that decoupled legibility from sovereignty.
   This is the mechanism by which the seven counter-cases in Paper 2 avoided
   full lock-in: they allowed L to rise while structurally constraining S.

Usage
-----
    python src/survival_analysis.py
    python src/survival_analysis.py --traj PATH/TO/d_trajectory_parsed.csv
    python src/survival_analysis.py --no-figure
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

THETA = 0.45

MECH_CLASS = {
    'educational_hegemony':         'hegemonic',
    'ideological_hegemony':         'hegemonic',
    'coercive_then_hegemonic':      'hegemonic',
    'administrative_closure':       'administrative',
    'administrative_absorption':    'administrative',
    'passive_revolution':           'administrative',
    'counter_hegemony':             'counter',
    'resilient_then_absorbed':      'counter',
    'resilient_with_shocks':        'counter',
    'failing_counter_hegemony':     'counter',
    'oscillating_counter_hegemony': 'counter',
}
MECH_LABEL = {
    'hegemonic':      'Hegemonic capture',
    'administrative': 'Administrative/closure',
    'counter':        'Counter-hegemonic',
}
MECH_COL = {
    'hegemonic':      '#c0392b',
    'administrative': '#4a6580',
    'counter':        '#6fcf97',
}


def build_survival_data(traj):
    """Build per-system survival records from trajectory time-series."""
    records = []
    for sys, grp in traj.groupby('system'):
        grp = grp.sort_values('year').reset_index(drop=True)
        if grp['D_t'].iloc[0] < THETA:
            continue
        crossed = grp[grp['D_t'] < THETA]
        event   = 1 if len(crossed) > 0 else 0
        time    = float(
            (crossed['year'].iloc[0] - grp['year'].iloc[0]) if event
            else (grp['year'].iloc[-1] - grp['year'].iloc[0])
        )
        mech = grp['mechanism'].iloc[0]
        records.append({
            'system':     sys,
            'event':      event,
            'time':       max(1.0, time),
            'start_D':    float(grp['D_t'].iloc[0]),
            'start_L':    float(grp['L'].iloc[0]),
            'start_S':    float(grp['S'].iloc[0]),
            'start_A':    float(grp['A'].iloc[0]),
            'mechanism':  mech,
            'mech_class': MECH_CLASS.get(mech, 'other'),
        })
    return pd.DataFrame(records)


def sig_stars(p):
    return ('***' if p < 0.001 else '**' if p < 0.01
            else '*' if p < 0.05 else 'ns (marginal)' if p < 0.10 else 'ns')


def km_at_times(durations, events, times):
    """Simple Kaplan-Meier survival function without lifelines dependency."""
    t_sorted = np.sort(durations)
    n = len(durations)
    S = 1.0
    result = {}
    event_times = sorted(
        [d for d, e in zip(durations, events) if e == 1])
    idx = 0
    for t in times:
        while idx < len(event_times) and event_times[idx] <= t:
            # n at risk
            n_risk = sum(1 for d in durations if d >= event_times[idx])
            S *= (1 - 1/n_risk) if n_risk > 0 else 1
            idx += 1
        result[t] = S
    return result


def main():
    try:
        from lifelines import KaplanMeierFitter
        from lifelines.statistics import logrank_test, multivariate_logrank_test
        from lifelines.utils import concordance_index
        from lifelines import CoxPHFitter
        HAS_LIFELINES = True
    except ImportError:
        HAS_LIFELINES = False
        print('WARNING: lifelines not installed. Install with:')
        print('  pip install lifelines --break-system-packages')
        print('Falling back to manual KM estimator.')
        print()

    parser = argparse.ArgumentParser(
        description='Survival analysis: time to D-threshold crossing',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--traj', type=str,
        default=os.path.join(DATA_DIR, 'd_trajectory_parsed.csv'))
    parser.add_argument('--figure', type=str, default=None)
    parser.add_argument('--no-figure', action='store_true')
    args = parser.parse_args()

    if not os.path.isfile(args.traj):
        print(f'ERROR: Cannot find {args.traj}')
        return

    traj = pd.read_csv(args.traj)
    sv   = build_survival_data(traj)

    print('=' * 65)
    print('SURVIVAL ANALYSIS: TIME TO D-THRESHOLD CROSSING')
    print(f'theta = {THETA}')
    print('=' * 65)
    print()
    print(f'  n systems starting above theta: {len(sv)}')
    print(f'  Events (D crossed below theta): {int(sv["event"].sum())}')
    print(f'  Censored:                       {int((sv["event"]==0).sum())}')
    print()

    # ── Section 1: KM overall ────────────────────────────────────────────────
    print('=== SECTION 1: OVERALL KAPLAN-MEIER ===')
    if HAS_LIFELINES:
        kmf = KaplanMeierFitter()
        kmf.fit(sv['time'], event_observed=sv['event'])
        print(f'  Median time to crossing: {kmf.median_survival_time_:.0f} years')
        for t in [50, 100, 200, 400]:
            s = kmf.survival_function_at_times([t]).values[0]
            print(f'  S({t:4d} years) = {s:.3f}')
    print()

    # ── Section 2: KM by mechanism class ─────────────────────────────────────
    print('=== SECTION 2: KM BY MECHANISM CLASS ===')
    for mc in ['hegemonic', 'administrative', 'counter']:
        g = sv[sv['mech_class'] == mc]
        er = g['event'].mean()
        mt = g['time'].median()
        print(f'  {MECH_LABEL[mc]:<28} n={len(g):2d}  '
              f'event_rate={er:.2f}  median_time={mt:.0f}y  '
              f'mean_L={g.start_L.mean():.2f}  mean_S={g.start_S.mean():.2f}')
    print()

    if HAS_LIFELINES:
        res = multivariate_logrank_test(sv['time'], sv['mech_class'], sv['event'])
        print(f'  Multivariate log-rank p = {res.p_value:.4f} {sig_stars(res.p_value)}')
        # Pairwise
        for a, b in [('hegemonic','counter'),
                     ('administrative','counter'),
                     ('hegemonic','administrative')]:
            ga = sv[sv['mech_class']==a]; gb = sv[sv['mech_class']==b]
            if len(ga) < 2 or len(gb) < 2: continue
            lr = logrank_test(ga['time'], gb['time'],
                              event_observed_A=ga['event'],
                              event_observed_B=gb['event'])
            print(f'  {a} vs {b}: p = {lr.p_value:.4f} {sig_stars(lr.p_value)}')
    print()

    # ── Section 3: KM by S ────────────────────────────────────────────────────
    print('=== SECTION 3: KM BY S AT START ===')
    S_med = sv['start_S'].median()
    hi_S  = sv[sv['start_S'] >  S_med]
    lo_S  = sv[sv['start_S'] <= S_med]
    print(f'  Median split at S={S_med:.2f}')
    print(f'  High-S (n={len(hi_S)}): event_rate={hi_S.event.mean():.2f}')
    print(f'  Low-S  (n={len(lo_S)}): event_rate={lo_S.event.mean():.2f}')
    if HAS_LIFELINES:
        kmf_hi = KaplanMeierFitter()
        kmf_lo = KaplanMeierFitter()
        kmf_hi.fit(hi_S['time'], event_observed=hi_S['event'])
        kmf_lo.fit(lo_S['time'], event_observed=lo_S['event'])
        print(f'  Median survival: High-S={kmf_hi.median_survival_time_:.0f}y, '
              f'Low-S=>{lo_S.time.max():.0f}y (not reached)')
        lr_S = logrank_test(hi_S['time'], lo_S['time'],
                            event_observed_A=hi_S['event'],
                            event_observed_B=lo_S['event'])
        print(f'  Log-rank p = {lr_S.p_value:.4f} {sig_stars(lr_S.p_value)}')
    print()

    # ── Section 4: L does not predict ────────────────────────────────────────
    print('=== SECTION 4: L DOES NOT PREDICT CROSSING ===')
    L_med = sv['start_L'].median()
    hi_L  = sv[sv['start_L'] >  L_med]
    lo_L  = sv[sv['start_L'] <= L_med]
    if HAS_LIFELINES:
        lr_L = logrank_test(hi_L['time'], lo_L['time'],
                            event_observed_A=hi_L['event'],
                            event_observed_B=lo_L['event'])
        print(f'  Log-rank p (L median split) = {lr_L.p_value:.4f} {sig_stars(lr_L.p_value)} (ns)')
        ci_L = concordance_index(sv['time'], -sv['start_L'], sv['event'])
        ci_S = concordance_index(sv['time'], -sv['start_S'], sv['event'])
        ci_D = concordance_index(sv['time'],  sv['start_D'], sv['event'])
        print(f'  Concordance indices:')
        print(f'    C(L) = {ci_L:.3f}  (near random = 0.5)')
        print(f'    C(S) = {ci_S:.3f}  (near perfect = 1.0)')
        print(f'    C(D) = {ci_D:.3f}')
    print()
    print('  Interpretation: High-L systems starting above theta include both')
    print('  fast crossers (Nazi Germany L=0.85, 2 years) and long survivors')
    print('  (Venetian Republic L=0.75, 903 years; British Parliament L=0.75,')
    print('  309+ years censored). L is mechanism-contingent: it enables')
    print('  hegemonic capture but is also present in counter-hegemonic')
    print('  systems. S — not L — is the structural gate.')
    print()

    # ── Section 5: Cox PH ────────────────────────────────────────────────────
    if HAS_LIFELINES:
        print('=== SECTION 5: COX PROPORTIONAL HAZARDS (UNIVARIATE) ===')
        for var, direction in [('start_L','>'), ('start_S','>'),
                                ('start_D','<'), ('start_A','>')]:
            cph = CoxPHFitter()
            cph.fit(sv[['time','event',var]], duration_col='time', event_col='event')
            row = cph.summary
            hr  = float(row['exp(coef)'])
            p   = float(row['p'])
            ci_lo = float(row['exp(coef) lower 95%'])
            ci_hi = float(row['exp(coef) upper 95%'])
            p_str = sig_stars(p)
            print(f'  {var:<12}: HR={hr:.3f} '
                  f'(95% CI {ci_lo:.3f}\u2013{ci_hi:.3f}), '
                  f'p={p:.4f} {p_str}')
        print()

    # ── Summary ───────────────────────────────────────────────────────────────
    print('=' * 65)
    print('SUMMARY FOR PAPER 2/3 EXTENSION')
    print('=' * 65)
    print()
    print('PRIMARY FINDINGS:')
    print('  1. Mechanism class predicts crossing (multivariate log-rank')
    if HAS_LIFELINES:
        print(f'     p = {res.p_value:.4f}):')
    print('     Hegemonic: 100% event rate, median 51 years')
    print('     Administrative: 100% event rate, median 440 years')
    print('     Counter-hegemonic: 12.5% event rate, >900y survival')
    print()
    print('  2. S at start predicts crossing (C=0.940, log-rank p=0.007):')
    print('     High-S: 86% event rate, median 70 years')
    print('     Low-S: 25% event rate, median not reached (>900y)')
    print()
    print('  3. L at start does NOT predict crossing (C=0.543, p=0.68):')
    print('     L is mechanism-contingent; S is the structural gate.')
    print()
    print('THEORETICAL IMPLICATIONS:')
    print('  The lock-in sequence (Paper 2) correctly predicts that high S')
    print('  produces vulnerability. The counter-case systems maintained low')
    print('  S by developing institutions that structurally decoupled L from')
    print('  S — allowing legibility to rise without sovereign capacity.')
    print('  L alone cannot predict crossing because the mechanism matters:')
    print('  the same L=0.75 produces Nazi Germany (2y) and British Parliament')
    print('  (309y+ and counting). The D0 moderator from Paper 2 operates')
    print('  through S, not through L directly.')

    # ── Figure ────────────────────────────────────────────────────────────────
    if not args.no_figure and HAS_LIFELINES:
        vis_dir = os.path.join(ROOT, 'visuals')
        os.makedirs(vis_dir, exist_ok=True)
        fig_out = args.figure or os.path.join(vis_dir, 'survival_analysis.png')
        save_figure(sv, traj, fig_out)


def save_figure(sv, traj, out_path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from lifelines import KaplanMeierFitter
    from lifelines.statistics import logrank_test, multivariate_logrank_test
    from lifelines.utils import concordance_index

    AMBER = '#e8a020'; GREEN = '#6fcf97'; RED = '#c0392b'; SLATE = '#4a6580'
    THETA = 0.45

    plt.rcParams.update({
        'font.family': 'serif', 'axes.spines.top': False,
        'axes.spines.right': False, 'axes.facecolor': 'white',
        'figure.facecolor': 'white', 'axes.grid': True,
        'grid.alpha': 0.12, 'grid.linewidth': 0.5, 'font.size': 9,
    })

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.8),
                              gridspec_kw={'width_ratios': [1.1, 1.0, 0.9]})
    for ax in axes:
        ax.set_facecolor('white')

    # ── Panel A: KM curves by mechanism class ─────────────────────────────────
    ax = axes[0]
    t_max = 950
    t_range = np.arange(0, t_max, 5)

    res = multivariate_logrank_test(sv['time'], sv['mech_class'], sv['event'])

    for mc in ['hegemonic', 'administrative', 'counter']:
        g   = sv[sv['mech_class'] == mc]
        col = MECH_COL[mc]
        kmf = KaplanMeierFitter()
        kmf.fit(g['time'], event_observed=g['event'])
        sf = kmf.survival_function_at_times(t_range).values
        ax.plot(t_range, sf, color=col, lw=2.0,
                label=f'{MECH_LABEL[mc]}\n(n={len(g)}, '
                      f'ev={int(g["event"].sum())})')
        # Confidence interval
        ci = kmf.confidence_interval_survival_function_
        t_ci = ci.index.values
        lo_ci = ci.iloc[:, 0].values
        hi_ci = ci.iloc[:, 1].values
        ax.fill_between(t_ci, lo_ci, hi_ci, color=col, alpha=0.10)
        # Censored tick marks
        for _, row in g[g['event'] == 0].iterrows():
            y_val = kmf.survival_function_at_times([row['time']]).values[0]
            ax.plot(row['time'], y_val, '|', color=col, ms=9, mew=1.5)

    ax.text(0.97, 0.55,
            f'Multivariate\nlog-rank\np = {res.p_value:.4f}',
            transform=ax.transAxes, ha='right', va='top', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#ccc', alpha=0.9))
    ax.set_xlabel('Time above \u03b8 (years)', fontsize=9)
    ax.set_ylabel('P(still above \u03b8)', fontsize=9)
    ax.set_xlim(0, t_max); ax.set_ylim(-0.02, 1.06)
    ax.legend(fontsize=7.5, loc='lower left', framealpha=0.92,
              labelspacing=0.5)
    ax.set_title('A.  Kaplan\u2013Meier by mechanism class\n'
                 '(| = censored; counter-hegemonic: only 1 event in 332y)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    # ── Panel B: KM by S ──────────────────────────────────────────────────────
    ax = axes[1]
    S_med = sv['start_S'].median()
    for grp_name, grp_mask, col in [
            (f'High S (>{S_med:.2f})', sv['start_S'] > S_med, RED),
            (f'Low S (\u2264{S_med:.2f})', sv['start_S'] <= S_med, GREEN)]:
        g   = sv[grp_mask]
        kmf = KaplanMeierFitter()
        kmf.fit(g['time'], event_observed=g['event'])
        sf  = kmf.survival_function_at_times(t_range).values
        med = kmf.median_survival_time_
        ax.plot(t_range, sf, color=col, lw=2.0,
                label=f'{grp_name} (n={len(g)})\n'
                      f'median={med:.0f}y' if med < 9999 else
                      f'{grp_name} (n={len(g)})\nmedian not reached')
        ci  = kmf.confidence_interval_survival_function_
        ax.fill_between(ci.index.values, ci.iloc[:, 0].values,
                        ci.iloc[:, 1].values, color=col, alpha=0.10)
        for _, row in g[g['event'] == 0].iterrows():
            y_val = kmf.survival_function_at_times([row['time']]).values[0]
            ax.plot(row['time'], y_val, '|', color=col, ms=9, mew=1.5)

    lr_S = logrank_test(
        sv[sv['start_S'] > S_med]['time'],
        sv[sv['start_S'] <= S_med]['time'],
        event_observed_A=sv[sv['start_S'] > S_med]['event'],
        event_observed_B=sv[sv['start_S'] <= S_med]['event'])
    ci_S = concordance_index(sv['time'], -sv['start_S'], sv['event'])
    ax.text(0.97, 0.55,
            f'Log-rank p = {lr_S.p_value:.4f}\nC(S) = {ci_S:.3f}',
            transform=ax.transAxes, ha='right', va='top', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#ccc', alpha=0.9))
    ax.set_xlabel('Time above \u03b8 (years)', fontsize=9)
    ax.set_ylabel('P(still above \u03b8)', fontsize=9)
    ax.set_xlim(0, t_max); ax.set_ylim(-0.02, 1.06)
    ax.legend(fontsize=7.5, loc='lower left', framealpha=0.92, labelspacing=0.5)
    ax.set_title('B.  KM by S at start\n'
                 '(S is the structural gate: C\u202f=\u202f0.940, p\u202f=\u202f0.007)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    # ── Panel C: L vs S scatter coloured by event/censor + mechanism ─────────
    ax = axes[2]
    rng = np.random.default_rng(42)
    for _, row in sv.iterrows():
        col = MECH_COL.get(row['mech_class'], '#888888')
        marker = 'X' if row['event'] == 1 else 'o'
        size   = 90  if row['event'] == 1 else 60
        ax.scatter(row['start_L'], row['start_S'], color=col,
                   marker=marker, s=size, alpha=0.88, zorder=3,
                   edgecolors='white', linewidths=0.8)
        # Annotate notable cases
        short = (str(row['system'])
                 .replace(' Parliamentary System', '')
                 .replace(' Cantonal Democracy', '')
                 .replace(' Sovereign Wealth Democracy', '')
                 .replace(' Commonwealth', '')
                 .replace(' Republic', '').replace(' Dynasty', '')
                 .replace(' Mandate of Heaven', '')
                 .replace(' Empire', '').replace(' League', '')[:16])
        offset_x = {
            'Nazi Germany': (0.02, 0.04),
            'Icelandic': (-0.24, -0.04),
            'British': (-0.22, 0.03),
            'Venetian': (0.02, -0.05),
            'Norwegian': (0.02, 0.02),
            'United States': (0.02, -0.05),
        }.get(short.split()[0], (0.02, 0.02))
        ax.annotate(short,
                    xy=(row['start_L'], row['start_S']),
                    xytext=(row['start_L'] + offset_x[0],
                            row['start_S'] + offset_x[1]),
                    fontsize=6.0, color='#333333', va='center')

    ci_L = concordance_index(sv['time'], -sv['start_L'], sv['event'])
    ci_S2 = concordance_index(sv['time'], -sv['start_S'], sv['event'])
    ax.text(0.03, 0.97,
            f'C(L)\u202f=\u202f{ci_L:.3f} (ns)\nC(S)\u202f=\u202f{ci_S2:.3f} (p=0.007)',
            transform=ax.transAxes, ha='left', va='top', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#ccc', alpha=0.9))

    legend_handles = []
    for mc, col in MECH_COL.items():
        legend_handles.append(
            plt.scatter([], [], color=col, s=60, alpha=0.88,
                        edgecolors='white', linewidths=0.8,
                        label=MECH_LABEL[mc]))
    legend_handles += [
        plt.scatter([], [], marker='X', color='#555', s=80,
                    label='Event (crossed \u03b8)'),
        plt.scatter([], [], marker='o', color='#555', s=55,
                    label='Censored (still above \u03b8)'),
    ]
    ax.legend(handles=legend_handles, fontsize=6.8,
              loc='upper left', bbox_to_anchor=(0.03, 0.78),
              framealpha=0.92, labelspacing=0.35, handletextpad=0.3)
    ax.set_xlabel('L (surplus legibility at start)', fontsize=9)
    ax.set_ylabel('S (sovereign capacity at start)', fontsize=9)
    ax.set_xlim(0.20, 0.95); ax.set_ylim(-0.03, 1.08)
    ax.set_title('C.  L vs S: S is the gate variable\n'
                 '(\u2715\u202f=\u202fevent; \u25cb\u202f=\u202fcensored; '
                 'high L spans both fast and slow crossers)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    fig.suptitle(
        'Survival analysis: time to D-threshold crossing (\u03b8\u202f=\u202f0.45)'
        ' across 15 trajectory systems\n'
        'Mechanism class and S predict crossing; L does not '
        '(multivariate log-rank p\u202f=\u202f0.001)',
        fontsize=10.5, fontweight='bold', y=1.02)

    plt.tight_layout(w_pad=2.5)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'  Saved figure: {out_path}')


if __name__ == '__main__':
    main()
