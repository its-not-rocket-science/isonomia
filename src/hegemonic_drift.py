"""
hegemonic_drift.py
==================
D-trajectory analysis: distinguishing coercive lock-in from hegemonic drift.

Paper 5 of the isonomia series.

Theoretical motivation
----------------------
The lock-in sequence (Paper 2) treats D suppression as a unified process driven
by rising surplus legibility (L). Gramsci's theory of hegemony distinguishes
two mechanisms by which D is suppressed:

  Coercive suppression: D declines because overt force makes disobedience
  fatal. S rises sharply; D tracks S.

  Hegemonic drift: D declines because compliance is normalised through
  education, ideology, media, and administrative apparatus. S does not
  rise dramatically; A rises instead, or L enables soft control.
  The population internalises the worldview of the dominant class.

Bateson's schismogenesis (Paper 4) adds a third: schismogenesis resistance,
where high-D systems maintain D through contrast with low-D neighbours.

This script analyses the d_trajectory field in governance_extended.csv —
time-stamped D values within systems — to:

1. Classify trajectories by type: rising, falling-coercive, falling-hegemonic,
   stable-high (counter-hegemonic resistance), stable-low, U-shaped (collapse
   then recovery).

2. Test the hegemonic drift signature: falling D without rising S (or with
   rising A and stable S).

3. Compute the ΔD/ΔS ratio as a hegemony index: low ratio = hegemonic drift
   (D falls faster than S rises); high ratio = coercive suppression.

4. Identify the Gramsci passive revolution signature: D falls before S rises
   (anticipatory hegemony), versus D falls contemporaneous with S rise
   (coercive suppression).

Usage
-----
    python src/hegemonic_drift.py                  # analysis + print results
    python src/hegemonic_drift.py --figure         # + save visuals
    python src/hegemonic_drift.py --data PATH      # custom CSV

Outputs (always)
----------------
    data/d_trajectory_parsed.csv   — parsed time points
    data/hegemony_index.csv        — per-system hegemony index and classification

Outputs (--figure only)
-----------------------
    visuals/hegemonic_drift.png    — 4-panel figure
"""

import os
import argparse
import warnings
import re
import numpy as np
import pandas as pd
from scipy import stats
from collections import defaultdict

warnings.filterwarnings('ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.join(SCRIPT_DIR, '..')
DATA_DIR   = os.path.join(ROOT, 'data')
VIS_DIR    = os.path.join(ROOT, 'visuals')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VIS_DIR,  exist_ok=True)

THETA = 0.45   # EDR resilience threshold


# ── Data loading ──────────────────────────────────────────────────────────────

def load_data(data_path=None):
    if data_path is None:
        data_path = os.path.join(DATA_DIR, 'governance_extended.csv')
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()
    for col in ['sovereignty_index', 'admin_index', 'competitive_politics_index',
                'exit_freedom', 'disobedience_freedom', 'arrangement_freedom',
                'surplus_legibility', 'info_infrastructure']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def parse_d_trajectories(df):
    """
    Parse the d_trajectory field into a long-format DataFrame of
    (system, year, D_value, D_static, S, A, L, mechanism) rows.

    d_trajectory format: "D=0.65@-400, D=0.55@-200, D=0.50@-100"
    """
    rows = []
    coded = df[df['d_trajectory'].notna() & (df['d_trajectory'] != '')]
    for _, row in coded.iterrows():
        traj_str = str(row['d_trajectory'])
        entries = re.findall(r'D=([\d.]+)@(-?\d+)', traj_str)
        if not entries:
            continue
        for d_str, yr_str in entries:
            rows.append({
                'system':     row['System'],
                'year':       int(yr_str),
                'D_t':        float(d_str),
                'D_static':   row['disobedience_freedom'],
                'S':          row['sovereignty_index'],
                'A':          row['admin_index'],
                'L':          row['surplus_legibility'],
                'mechanism':  row.get('hegemonic_mechanism', ''),
                'start':      row['Start'],
                'end':        row['End'],
            })
    traj_df = pd.DataFrame(rows).sort_values(['system', 'year'])
    return traj_df


# ── Trajectory classification ─────────────────────────────────────────────────

def classify_trajectory(system_df):
    """
    Classify a single system's D trajectory.

    Returns dict with:
      - traj_type: rising | falling_hegemonic | falling_coercive |
                   stable_high | stable_low | u_shaped | oscillating
      - delta_D: total D change (end - start)
      - rate_D: mean annual D change per century
      - hegemony_index: |ΔD| / (|ΔS| + 0.01) — higher = more hegemonic drift
      - coercion_index: ΔS / (century)
      - pre_D_drop: D dropped before S rose (passive revolution signature)
    """
    if len(system_df) < 2:
        return None

    sdf = system_df.sort_values('year')
    years = sdf['year'].values
    D_vals = sdf['D_t'].values
    S_val  = sdf['S'].iloc[0]   # static S (single value per system)
    A_val  = sdf['A'].iloc[0]

    delta_D = D_vals[-1] - D_vals[0]
    span    = max(years[-1] - years[0], 1)
    rate_D  = delta_D / span * 100   # per century

    # Hegemony index: how much D changed relative to S level
    # High S + large |ΔD| = coercive
    # Low/moderate S + large |ΔD| = hegemonic drift
    hegemony_index = abs(delta_D) / (S_val + 0.01)

    # Trajectory type
    if abs(delta_D) < 0.08:
        if D_vals.mean() >= THETA:
            traj_type = 'stable_high'
        else:
            traj_type = 'stable_low'
    elif delta_D > 0.08:
        traj_type = 'rising'
    elif delta_D < -0.08:
        # Distinguish hegemonic vs coercive
        if S_val <= 0.55 and A_val >= 0.55:
            traj_type = 'falling_hegemonic'
        elif S_val > 0.65:
            traj_type = 'falling_coercive'
        else:
            traj_type = 'falling_mixed'

    # Check for U-shape: D falls significantly then recovers
    # This catches systems like Soviet where endpoint > start but trough is deep
    trough_depth = D_vals[0] - np.min(D_vals)
    recovery = D_vals[-1] - np.min(D_vals)
    if trough_depth >= 0.15 and recovery >= 0.10:
        traj_type = 'u_shaped'

    # Check for oscillating (multiple reversals)
    reversals = sum(1 for i in range(1, len(D_vals)-1)
                    if (D_vals[i] - D_vals[i-1]) * (D_vals[i+1] - D_vals[i]) < 0)
    if reversals >= 2:
        traj_type = 'oscillating'

    return {
        'traj_type':       traj_type,
        'delta_D':         delta_D,
        'rate_D':          rate_D,
        'hegemony_index':  hegemony_index,
        'S':               S_val,
        'A':               A_val,
        'D_start':         D_vals[0],
        'D_end':           D_vals[-1],
        'D_min':           np.min(D_vals),
        'span_years':      span,
        'n_points':        len(D_vals),
    }


def build_hegemony_index_table(traj_df):
    """Build a per-system hegemony index table."""
    rows = []
    for system, sdf in traj_df.groupby('system'):
        result = classify_trajectory(sdf)
        if result:
            result['system'] = system
            result['mechanism'] = sdf['mechanism'].iloc[0]
            rows.append(result)
    return pd.DataFrame(rows).sort_values('hegemony_index', ascending=False)


# ── Statistical tests ─────────────────────────────────────────────────────────

def run_analysis(traj_df, hi_df):
    """
    Core statistical analysis:
    1. Do falling-hegemonic trajectories differ from falling-coercive in rate?
    2. Is hegemony_index higher for low-S systems (as predicted)?
    3. Does D decline precede S increase (passive revolution test)?
    """
    print("=== D-TRAJECTORY ANALYSIS ===")
    print(f"Systems with coded trajectories: {traj_df['system'].nunique()}")
    print(f"Total time points: {len(traj_df)}")
    print()

    print("=== TRAJECTORY TYPES ===")
    type_counts = hi_df['traj_type'].value_counts()
    for t, n in type_counts.items():
        print(f"  {t:25s}: n={n}")
    print()

    print("=== HEGEMONY INDEX BY MECHANISM ===")
    print(f"  {'Mechanism':30s} {'HI mean':>8} {'HI std':>7} {'ΔD':>7} {'S':>6}  n")
    for mech, sub in hi_df.groupby('mechanism'):
        print(f"  {mech:30s} {sub['hegemony_index'].mean():8.3f} "
              f"{sub['hegemony_index'].std():7.3f} "
              f"{sub['delta_D'].mean():7.3f} "
              f"{sub['S'].mean():6.3f}  {len(sub)}")
    print()

    # PRIMARY TEST: Hegemonic drift starts from higher D₀ than coercive suppression
    # Hegemonic drift = normalisation FROM a prior high-D state
    # Coercive suppression = maintenance of an already-low-D state by force
    heg = hi_df[hi_df['traj_type']=='falling_hegemonic']
    coe = hi_df[hi_df['traj_type']=='falling_coercive']
    if len(heg) >= 2 and len(coe) >= 2:
        print("=== PRIMARY FINDING: D_start by trajectory type ===")
        print(f"  Hegemonic drift:       D_start mean={heg['D_start'].mean():.3f} "
              f"(SD={heg['D_start'].std():.3f}), n={len(heg)}")
        print(f"  Coercive suppression:  D_start mean={coe['D_start'].mean():.3f} "
              f"(SD={coe['D_start'].std():.3f}), n={len(coe)}")
        u, p = stats.mannwhitneyu(
            heg['D_start'], coe['D_start'], alternative='greater')
        sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'ns'
        print(f"  MW hegemonic D_start > coercive: p={p:.4f} {sig}")
        print()
        print("  Interpretation: hegemonic drift requires a prior high-D state")
        print("  to normalise FROM. Coercive systems begin already suppressed.")
        print()
        # SECONDARY: rate of fall
        heg_r = heg['rate_D']; coe_r = coe['rate_D']
        print("=== SECONDARY: Fall rate (hegemonic slower than coercive?) ===")
        print(f"  Hegemonic: mean={heg_r.mean():.3f}/century, n={len(heg_r)}")
        print(f"  Coercive:  mean={coe_r.mean():.3f}/century, n={len(coe_r)}")
        u2, p2 = stats.mannwhitneyu(abs(heg_r), abs(coe_r), alternative='less')
        sig2 = '***' if p2<0.001 else '**' if p2<0.01 else '*' if p2<0.05 else 'ns'
        print(f"  MW hegemonic SLOWER than coercive: p={p2:.4f} {sig2}")
        print()
        # D_start vs |ΔD| correlation
        all_fall = hi_df[hi_df['traj_type'].isin(
            ['falling_hegemonic','falling_coercive'])]
        r_corr, p_corr = stats.pearsonr(
            all_fall['D_start'], all_fall['delta_D'])
        print(f"=== D_start vs total ΔD (falling systems) ===")
        print(f"  r={r_corr:.3f}, p={p_corr:.4f} — higher D_start → more D lost")
        print()

    # Counter-hegemonic systems
    rising = hi_df[hi_df['traj_type']=='rising']
    print("=== COUNTER-HEGEMONIC SYSTEMS (rising D) ===")
    for _, r in rising.iterrows():
        print(f"  {r['system']:40s}: ΔD={r['delta_D']:+.2f}, "
              f"HI={r['hegemony_index']:.3f}, mechanism={r['mechanism']}")
    print()

    # Passive revolution test: Roman Republic
    roman = traj_df[traj_df['system']=='Roman Republic'].sort_values('year')
    if len(roman):
        print("=== PASSIVE REVOLUTION CASE: Roman Republic ===")
        for _, r in roman.iterrows():
            print(f"  {r['year']:6d}: D={r['D_t']:.2f}")
        print(f"  Static S = {roman['S'].iloc[0]:.2f} (constant throughout)")
        print(f"  Interpretation: D declines 0.65→0.35 over 350 years")
        print(f"  while S only rises modestly at the end (Augustan period).")
        print(f"  This is Gramsci's passive revolution: hegemonic D-suppression")
        print(f"  precedes and enables the formal constitutional change.")
        print()

    # Soviet coercion→hegemony transition
    soviet = traj_df[traj_df['system']=='Soviet Republics System'].sort_values('year')
    if len(soviet):
        print("=== COERCION-TO-CONSENT: Soviet Republics System ===")
        for _, r in soviet.iterrows():
            print(f"  {r['year']:6d}: D={r['D_t']:.2f}")
        print(f"  Stalin terror (1937): D → 0.05 via coercion")
        print(f"  Post-Stalin (1956+): D recovers slightly — hegemonic normalisation")
        print(f"  takes over from direct terror as compliance mechanism.")
        print()


# ── Figures ───────────────────────────────────────────────────────────────────

def make_figure(traj_df, hi_df, vis_dir=VIS_DIR):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import matplotlib.lines as mlines

    plt.rcParams.update({
        'font.family': 'serif', 'font.size': 9,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.grid': True, 'grid.alpha': 0.20, 'grid.linewidth': 0.5,
    })

    MECH_COLOURS = {
        'passive_revolution':       '#e74c3c',
        'educational_hegemony':     '#9b59b6',
        'counter_hegemony':         '#27ae60',
        'administrative_drift':     '#e67e22',
        'coercion_to_consent':      '#c0392b',
        'ideological_hegemony':     '#8e44ad',
        'resilient_with_shocks':    '#2ecc71',
        'administrative_absorption':'#d35400',
        'manufactured_consent':     '#f39c12',
        'coercive_then_hegemonic':  '#7f8c8d',
        'failing_counter_hegemony': '#95a5a6',
        'sakoku_hegemony':          '#16a085',
    }
    DEFAULT_COL = '#aaaaaa'

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.subplots_adjust(top=0.88, hspace=0.35, wspace=0.30)

    # ── A: D trajectories — all systems ──────────────────────────────────────
    ax = axes[0, 0]
    # Jitter year slightly so overlapping labels separate
    import random; random.seed(42)
    labelled = set()
    for system, sdf in traj_df.groupby('system'):
        sdf = sdf.sort_values('year')
        mech = sdf['mechanism'].iloc[0]
        col  = MECH_COLOURS.get(mech, DEFAULT_COL)
        sys_row = hi_df[hi_df['system']==system]
        ttype   = sys_row['traj_type'].values[0] if len(sys_row) else ''
        lw      = 2.0 if ('counter' in mech or ttype == 'rising') else 1.2
        ax.plot(sdf['year'], sdf['D_t'], 'o-', color=col, lw=lw,
                markersize=4, alpha=0.85)
        # Label only first point (less crowded) with short name
        first = sdf.iloc[0]
        short = (system.replace(' Democracy','').replace(' System','')
                       .replace(' Monarchy','').replace(' Parliamentary','')
                       .replace(' Sovereign Wealth','')[:20])
        # Stagger label vertical offset slightly to avoid collision
        y_nudge = 8 if 'Confucian' in system else (-8 if 'Zhou' in system else 0)
        ax.annotate(short, (first['year'], first['D_t']),
                    fontsize=5.5, ha='right', va='center',
                    xytext=(-4, y_nudge), textcoords='offset points',
                    color=col, alpha=0.85)

    ax.axhline(THETA, color='#c0392b', lw=1.2, ls='--', alpha=0.7)
    ax.text(-1200, THETA + 0.025, 'θ = 0.45', fontsize=7, color='#c0392b')
    ax.set_xlabel('Year (BCE/CE)', fontsize=9)
    ax.set_ylabel('D (disobedience freedom)', fontsize=9)
    ax.set_xlim(-1300, 2050)
    ax.set_title('A.  D-trajectories across 15 systems\n'
                 '(colour by hegemonic mechanism; label at first coded year)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    # ── B: Hegemony index by mechanism ───────────────────────────────────────
    ax = axes[0, 1]
    # Order by theoretical category: counter-hegemonic → hegemonic → coercive
    # barh plots bottom-to-top, so REVERSE list to get counter_hegemony at top
    MECH_ORDER = [
        'coercive_then_hegemonic', 'sakoku_hegemony', 'educational_hegemony',
        'coercion_to_consent', 'manufactured_consent',
        'administrative_absorption', 'administrative_drift',
        'ideological_hegemony', 'failing_counter_hegemony',
        'passive_revolution', 'resilient_with_shocks', 'counter_hegemony',
    ]
    present = hi_df['mechanism'].unique()
    mech_order = [m for m in MECH_ORDER if m in present] + \
                 [m for m in present if m not in MECH_ORDER]
    y_pos = range(len(mech_order))
    bars = ax.barh(list(y_pos),
                   [hi_df[hi_df['mechanism']==m]['hegemony_index'].mean()
                    for m in mech_order],
                   color=[MECH_COLOURS.get(m, DEFAULT_COL) for m in mech_order],
                   alpha=0.80, height=0.65)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels([m.replace('_', ' ') for m in mech_order], fontsize=7.5)
    ax.axvline(1.0, color='#aaaaaa', lw=0.8, ls=':', alpha=0.7)
    ax.set_xlabel('Hegemony index (|ΔD| / S)', fontsize=9)
    ax.set_title('B.  Hegemony index by mechanism\n'
                 '(higher = more drift relative to coercion capacity)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    # ── C: ΔD vs S — hegemonic drift vs coercive scatter ─────────────────────
    ax = axes[1, 0]
    for _, r in hi_df.iterrows():
        mech = r['mechanism']
        col  = MECH_COLOURS.get(mech, DEFAULT_COL)
        marker = 'v' if r['delta_D'] < 0 else '^'
        ax.scatter(r['S'], abs(r['delta_D']), color=col, marker=marker,
                   s=80, alpha=0.85, zorder=5)
        short = (r['system'].replace(' Democracy','').replace(' System','')
                            .replace(' Monarchy','').replace(' Republic','')
                            .replace(' Bureaucracy','')[:16])
        ax.annotate(short, (r['S'], abs(r['delta_D'])),
                    fontsize=5.5, xytext=(5, 3), textcoords='offset points',
                    color=col, alpha=0.85)

    ax.set_xlabel('S (sovereignty index, proxy for coercion capacity)', fontsize=9)
    ax.set_ylabel('|ΔD| (absolute D change over trajectory)', fontsize=9)
    ax.set_title('C.  D change vs coercion capacity\n'
                 '(▼ = falling D; ▲ = rising D; hegemonic drift: large |ΔD| at low S)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)

    # Hegemonic drift zone: large |ΔD| with low S
    from matplotlib.patches import FancyArrowPatch
    ax.axvline(0.55, color='#95a5a6', lw=0.8, ls='--', alpha=0.5)
    ax.text(0.10, 0.92, 'Hegemonic\ndrift zone', transform=ax.transAxes,
            fontsize=7.5, color='#7f8c8d', style='italic', va='top')
    ax.text(0.62, 0.92, 'Coercive\nzone', transform=ax.transAxes,
            fontsize=7.5, color='#c0392b', style='italic', va='top')

    # ── D: Soviet and Roman case study detail ─────────────────────────────────
    ax = axes[1, 1]

    cases = {
        'Soviet Republics System':   ('#c0392b', 'coercion_to_consent'),
        'Roman Republic':            ('#e74c3c', 'passive_revolution'),
        'British Parliamentary System': ('#27ae60', 'counter_hegemony'),
        'Athenian Democracy':        ('#2ecc71', 'resilient_with_shocks'),
        'Norwegian Sovereign Wealth Democracy': ('#1abc9c', 'counter_hegemony'),
    }

    for system, (col, mech) in cases.items():
        sdf = traj_df[traj_df['system']==system].sort_values('year')
        if len(sdf) == 0:
            continue
        label = system.replace(' System','').replace(' Democracy','')[:28]
        ax.plot(sdf['year'], sdf['D_t'], 'o-', color=col, lw=2.0,
                markersize=5, label=label, alpha=0.90)

    ax.axhline(THETA, color='#c0392b', lw=1.2, ls='--', alpha=0.6)
    ax.text(1921, THETA + 0.02, 'θ = 0.45', fontsize=7, color='#c0392b')

    # Annotate key events
    ax.annotate('Stalin terror', xy=(1937, 0.05), xytext=(1945, 0.02),
                fontsize=6.5, color='#c0392b',
                arrowprops=dict(arrowstyle='->', color='#c0392b', lw=0.8))
    # Magna Carta annotation — points to British Parliamentary data at 1689
    ax.annotate('1689\nBill of Rights', xy=(1689, 0.55), xytext=(1400, 0.48),
                fontsize=6.5, color='#27ae60',
                arrowprops=dict(arrowstyle='->', color='#27ae60', lw=0.8))

    ax.set_xlabel('Year (CE)', fontsize=9)
    ax.set_ylabel('D (disobedience freedom)', fontsize=9)
    ax.legend(fontsize=7, loc='upper left', frameon=True, framealpha=0.9)
    ax.set_title('D.  Case studies — hegemonic drift and counter-hegemony\n'
                 '(post-1000 CE systems)',
                 fontsize=9, fontweight='bold', loc='left', pad=4)
    ax.set_xlim(-450, 2050)
    # Add Roman Republic to Panel D (pre-1000 but theoretically critical)
    roman = traj_df[traj_df['system']=='Roman Republic'].sort_values('year')
    if len(roman):
        ax.plot(roman['year'], roman['D_t'], 's--', color='#c0392b',
                lw=1.5, markersize=4, alpha=0.70, label='Roman Republic')
    ax.legend(fontsize=7, loc='upper left', frameon=True, framealpha=0.9)

    fig.suptitle(
        'Hegemonic drift analysis: D-trajectory coding across 15 governance systems\n'
        'Distinguishing coercive suppression (high S) from hegemonic normalisation '
        '(high A, moderate S)',
        fontsize=11, fontweight='bold', y=0.94)

    out = os.path.join(vis_dir, 'hegemonic_drift.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Hegemonic drift analysis — Paper 5',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Analyses the d_trajectory field in governance_extended.csv to distinguish
coercive D-suppression from hegemonic drift (normalisation without coercion).

Usage:
    python src/hegemonic_drift.py                   # analysis only
    python src/hegemonic_drift.py --figure          # + save figure
    python src/hegemonic_drift.py --data PATH       # custom CSV path
"""
    )
    parser.add_argument('--figure', action='store_true')
    parser.add_argument('--data',   type=str, default=None)
    args = parser.parse_args()

    data_path = args.data or os.path.join(DATA_DIR, 'governance_extended.csv')
    df = load_data(data_path)

    coded = df[df['d_trajectory'].notna() & (df['d_trajectory'].astype(str) != '')]
    if len(coded) == 0:
        print("No d_trajectory data found. Run the dataset update first.")
        print("Expected column 'd_trajectory' in governance_extended.csv")
        return

    print(f"Loaded {len(df)} systems, {len(coded)} with d_trajectory coded")
    print()

    traj_df = parse_d_trajectories(df)
    hi_df   = build_hegemony_index_table(traj_df)

    # Save parsed data
    traj_out = os.path.join(DATA_DIR, 'd_trajectory_parsed.csv')
    traj_df.to_csv(traj_out, index=False)
    print(f"Saved: {traj_out}")

    hi_out = os.path.join(DATA_DIR, 'hegemony_index.csv')
    hi_df.to_csv(hi_out, index=False)
    print(f"Saved: {hi_out}")
    print()

    run_analysis(traj_df, hi_df)

    if args.figure:
        make_figure(traj_df, hi_df)


if __name__ == '__main__':
    main()
