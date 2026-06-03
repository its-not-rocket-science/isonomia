"""
succession_markov_ctmc.py
=========================
Phase 3 of the isonomia succession model: continuous-time Markov chain (CTMC).

Motivation
----------
Phase 1 (static model) established that L and D₀ predict which succession
type a system occupies at any cross-section (χ² p < 0.0001, OR = 6.46).
Phase 2 (transition matrix) documented 31 type-changing transitions across
29 systems.  A discrete-time Markov chain on those transitions produced
L-conditional stationary distributions that contradicted the lock-in
sequence prediction, because the discrete chain treats all transitions as
equally weighted regardless of how long a system spent in each state.

The CTMC corrects this by weighting transitions by dwell time.  A system
that spent 300 years as hereditary before one documented transition
contributes 300 system-years of hereditary exposure and 1 event — giving
a low exit rate — whereas a system with the same succession type for 50
years and one transition contributes a much higher rate.  This is the
correct formulation for the question: given that a system is currently of
type X at legibility level L, at what rate per unit time does it exit to
each other type?

The D₀ moderator prediction (Paper 3 central hypothesis):
  The exit rate from elective succession is lower for systems with high
  pre-existing D₀ than for systems with low D₀, holding L constant.
  Equivalently: high D₀ increases the dwell time in elective succession
  at high L, making it more stable against the hereditary attractor.

Method
------
Each governance system contributes one or more "spells" to the survival
dataset.  A spell is a contiguous period in a single succession type with
a known start date.  Spells end either in an observed type-change (event=1)
or in censoring (event=0, meaning the system ended without a documented
succession type change, or is ongoing).

Transition rates λ_{ij} are estimated as:
    λ_{ij} = (number of i→j transitions) / (total time spent in state i)

with Laplace smoothing (adding a small constant rate) to regularise zero
cells.  The Q matrix has off-diagonal entries λ_{ij} and diagonal entries
-Σ_{j≠i} λ_{ij}.

The stationary distribution π satisfies π Q = 0 and Σ π_i = 1.
It is found by solving the linear system derived from the null space
of Q^T.

Usage
-----
    python src/succession_markov_ctmc.py
    python src/succession_markov_ctmc.py --no-figure

Outputs (to visuals/)
---------------------
    ctmc_model.png              — six-panel figure (see below)

Outputs (to data/)
------------------
    survival_spells.csv         — spell-level survival dataset
    transition_data.csv         — re-parsed (updated from Phase 2)

Figure panels
-------------
A. CTMC stationary distribution as a function of L (sliding window ±0.22)
B. Full Q rate matrix heatmap (off-diagonal rates per 1000 years)
C. Stationary distribution at three L levels (low/mid/high)
D. D₀ moderator: exit rate from elective and hereditary as function of D₀
   threshold (solid = high-D₀ group, dashed = low-D₀ group)
E. Kaplan-Meier survival curves by type; elective stratified by D₀
F. Key results table

Key results (Phase 3)
---------------------
Stationary distributions at L < 0.60 vs L ≥ 0.60:
  appointment:  0.136 → 0.368  (+0.232)   [lock-in prediction: appointment rises]
  elective:     0.399 → 0.225  (−0.174)   [lock-in prediction: elective falls]
  hereditary:   0.419 → 0.339  (−0.080)   [hereditary also falls — but see note]

The appointment rise at high L is the strongest result: as L increases,
bureaucratic appointment replaces both hereditary and elective succession
in the stationary distribution.  This refines the lock-in sequence
prediction: the attractor at high L is not purely hereditary but
hereditary-or-appointment — consistent with the theoretical mechanism
(A rises with L; A enables appointment-based office-holding even as it
suppresses exit freedom).

D₀ moderator confirmed: elective exit rate at high D₀ (D₀ ≥ 0.45) =
0.452 per 1000 years vs low D₀ = 1.235 per 1000 years.  Ratio: 2.73×.
High D₀ roughly triples the stability of elective succession.

Data notes
----------
Survival dataset: 145 spells from 119 systems; 31 events; 102,214
system-years.  Consensus and rotation spells contribute large amounts of
system-time from pre-state and small-scale societies with few documented
transitions — this is correct (those systems genuinely did not transition
much), not a measurement gap.

Five targeted transition additions in Phase 3 data preparation:
  Teotihuacan:           consensus→hereditary (450 CE)
  Tiv Segmentary System: consensus→hereditary (1900)
  Igbo Assemblies:       consensus→appointment (1900)
  Andean Tinku:          rotation→hereditary (1440)
  Mossi Naam Militias:   rotation→hereditary (1896)

These raised the working type-changing transition count from 26 to 31
and filled the consensus→hereditary, consensus→appointment, and
rotation→hereditary cells in the transition matrix.

Limitations
-----------
1.  L and D₀ are coded as single values for each system, not time-varying.
    Systems with long histories (Tang Dynasty, Ottoman Empire) will have
    the same L/D₀ value assigned to spells spanning different eras.

2.  Laplace smoothing is applied at rate 0.002–0.004 per 1000 years for
    zero-count cells.  This makes the stationary distribution estimable
    but regularises rather than removes sparse-data uncertainty.

3.  The consensus and rotation rate estimates are dominated by a small
    number of events relative to large total time.  A CTMC with a single
    consensus→hereditary transition from 4,000 system-years of observation
    will systematically underestimate the consensus exit rate relative to
    what would be found with richer data.

4.  Censoring is assumed to be independent of the transition process
    (non-informative censoring).  Systems that were absorbed by conquest
    may be systematically associated with particular transition types
    (especially →hereditary), which would introduce informative censoring
    bias.  The trigger-type analysis in Phase 2 allows partial assessment
    of this: external_shock transitions cluster at particular D₀ levels.
"""

import os
import sys
import argparse
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', category=np.RankWarning
                        if hasattr(np, 'RankWarning') else UserWarning)

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT        = os.path.join(SCRIPT_DIR, '..')
DATA_PATH   = os.path.join(ROOT, 'data', 'governance_extended.csv')
OUTPUT_DIR  = os.path.join(ROOT, 'visuals')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Constants ─────────────────────────────────────────────────────────────────
TYPES = ['hereditary', 'appointment', 'elective', 'consensus', 'rotation']

COLOURS = {
    'hereditary':  '#c0392b',
    'appointment': '#e67e22',
    'elective':    '#2980b9',
    'consensus':   '#27ae60',
    'rotation':    '#8e44ad',
}

CANON = {
    'Hereditary':   'hereditary', 'Dynastic':       'hereditary',
    'Inheritance':  'hereditary', 'Matrilineal':     'hereditary',
    'Patriarchal':  'hereditary',
    'Election':     'elective',   'Elections':       'elective',
    'Elective':     'elective',   'Sortition':       'elective',
    'Referendum':   'elective',   'Lottery':         'elective',
    'Consensus':    'consensus',  'Elder consensus': 'consensus',
    'Acclamation':  'consensus',
    'Rotation':     'rotation',   'Age grades':      'rotation',
    'Appointment':  'appointment','Merit-based':     'appointment',
    'Exams':        'appointment','Co-optation':     'appointment',
    'Promotion':    'appointment',
    'Charismatic':  'charismatic','Charismatic selection': 'charismatic',
    'Oratory skill':'charismatic','Competition':     'charismatic',
    'Competitive':  'charismatic','Testing':         'charismatic',
}

# Trigger keyword mapping (must match succession_changes field format)
TRIG_MAP = {
    'P_to_S':          'P_to_S',
    'external_shock':  'external_shock',
    'elite_reform':    'elite_reform',
    'collapse':        'collapse',
    'reconsolidation': 'reconsolidation',
    'internal':        'internal',
}

# Laplace smoothing rate (events per 1000 system-years added to empty cells)
LAPLACE_SMOOTH = 0.003


# ── Data loading ──────────────────────────────────────────────────────────────

def load_governance(path=DATA_PATH):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    numeric_cols = ['Start', 'End', 'surplus_legibility', 'disobedience_freedom',
                    'exit_freedom', 'arrangement_freedom', 'sovereignty_index',
                    'admin_index', 'competitive_politics_index', 'coding_confidence']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df['succ_canon'] = df['Succession Method'].map(CANON)
    df['L']  = df['surplus_legibility']
    df['D0'] = df['disobedience_freedom']
    return df


def parse_transitions(df):
    """Parse succession_changes field into a flat transition DataFrame."""
    rows = []
    for _, sys_row in df[df['succession_changes'].fillna('') != ''].iterrows():
        for entry in sys_row['succession_changes'].split(' | '):
            entry = entry.strip()
            if not entry:
                continue
            try:
                arrow_part, rest = entry.split(' (', 1)
                from_s, to_s = arrow_part.split('->')
                year_str, note = rest.split('): ', 1)
                trig = next(
                    (v for k, v in TRIG_MAP.items() if k in note.lower()),
                    'other'
                )
                rows.append({
                    'system':    sys_row['System'],
                    'year':      int(year_str.strip()),
                    'from_succ': from_s.strip(),
                    'to_succ':   to_s.strip(),
                    'L':         sys_row['L'],
                    'D0':        sys_row['D0'],
                    'trigger':   trig,
                    'changed':   int(from_s.strip() != to_s.strip()),
                })
            except Exception as exc:
                print(f"  Parse warning: {entry[:60]} — {exc}")
    tdf = pd.DataFrame(rows)
    print(f"  Parsed {len(tdf)} transition events "
          f"({tdf['changed'].sum()} type-changing)")
    return tdf


def build_survival_spells(df, tdf, current_year=2026):
    """Construct the survival spell dataset.

    Each row is a contiguous spell in one succession type.  Systems with
    documented transitions contribute multiple spells; systems without
    transitions contribute one (right-)censored spell.

    Parameters
    ----------
    df          governance_extended DataFrame
    tdf         parsed transition events DataFrame
    current_year used as censoring time for ongoing systems (no End date)

    Returns
    -------
    DataFrame with columns:
        system, succ_type, duration, event, L, D0, to_succ, trigger
    """
    spells = []
    sys_with_transitions = set(tdf['system'].unique())

    # Systems WITH transitions: partition history into dated spells
    for sys_name, grp in tdf.groupby('system'):
        sys_row = df[df['System'] == sys_name].iloc[0]
        sys_start = sys_row['Start']
        sys_end   = sys_row['End']
        events    = grp.sort_values('year')

        prev_year  = sys_start
        prev_type  = events.iloc[0]['from_succ']

        for _, ev in events.iterrows():
            if pd.isna(prev_year):
                break
            dur = ev['year'] - prev_year
            if dur > 0:
                spells.append({
                    'system':    sys_name,
                    'succ_type': prev_type,
                    'duration':  dur,
                    'event':     ev['changed'],
                    'L':         ev['L'],
                    'D0':        ev['D0'],
                    'to_succ':   ev['to_succ'] if ev['changed'] else None,
                    'trigger':   ev['trigger'],
                })
            prev_year = ev['year']
            prev_type = ev['to_succ']

        # Final censored spell from last transition to system end
        if prev_year is not None and not pd.isna(prev_year):
            end = sys_end if pd.notna(sys_end) else None
            if end and end > prev_year:
                spells.append({
                    'system':    sys_name,
                    'succ_type': prev_type,
                    'duration':  end - prev_year,
                    'event':     0,
                    'L':         sys_row['L'],
                    'D0':        sys_row['D0'],
                    'to_succ':   None,
                    'trigger':   None,
                })

    # Systems WITHOUT transitions: single censored spell
    hc = df[
        df['coding_confidence'].isin([2, 3]) &
        df['succ_canon'].notna() &
        df['L'].notna() &
        df['D0'].notna() &
        (df['succ_canon'] != 'charismatic')
    ]
    for _, row in hc.iterrows():
        if row['System'] in sys_with_transitions:
            continue
        if pd.isna(row['Start']):
            continue
        if pd.notna(row['End']) and row['End'] > row['Start']:
            dur = row['End'] - row['Start']
        else:
            dur = current_year - row['Start']
        if dur > 0:
            spells.append({
                'system':    row['System'],
                'succ_type': row['succ_canon'],
                'duration':  dur,
                'event':     0,
                'L':         row['L'],
                'D0':        row['D0'],
                'to_succ':   None,
                'trigger':   None,
            })

    sdf = pd.DataFrame(spells)
    sdf = sdf[sdf['duration'] > 0].copy()   # remove zero-duration spells

    print(f"\n  Survival dataset: {len(sdf)} spells, "
          f"{int(sdf['event'].sum())} events, "
          f"{sdf['duration'].sum():,.0f} total system-years")
    print()
    print("  Spells by succession type:")
    summary = sdf.groupby('succ_type').agg(
        n=('duration', 'count'),
        events=('event', 'sum'),
        total_yrs=('duration', 'sum'),
        median_dur=('duration', 'median'),
    ).astype({'n': int, 'events': int, 'total_yrs': int})
    print(summary.to_string())
    return sdf


# ── CTMC estimation ───────────────────────────────────────────────────────────

def compute_Q(sdf, smooth=LAPLACE_SMOOTH):
    """Estimate Q matrix from spell data with Laplace smoothing.

    Returns a DataFrame Q where Q.loc[f, t] is the transition rate from
    type f to type t per 1000 years.  Off-diagonal entries ≥ 0; diagonal
    entries = -(sum of row off-diagonals).
    """
    Q = pd.DataFrame(0.0, index=TYPES, columns=TYPES)
    for f in TYPES:
        sub = sdf[sdf['succ_type'] == f]
        total_time = sub['duration'].sum()
        if total_time == 0:
            continue
        for t in TYPES:
            if f == t:
                continue
            n_events = len(sub[(sub['event'] == 1) & (sub['to_succ'] == t)])
            # Laplace: add smooth * (total_time/1000) imaginary events
            Q.loc[f, t] = (n_events + smooth * total_time / 1000) / total_time * 1000
    for t in TYPES:
        Q.loc[t, t] = -Q.loc[t].sum()
    return Q


def stationary(Q_df):
    """Stationary distribution π such that π @ Q = 0 and sum(π) = 1.

    Solves by replacing the last equation with the normalisation constraint.
    Returns a numpy array aligned with TYPES.
    """
    Q = Q_df.values.copy()
    n = Q.shape[0]
    A = Q.T.copy()
    A[-1] = 1
    b = np.zeros(n)
    b[-1] = 1
    try:
        pi = np.linalg.solve(A, b)
        pi = np.clip(pi, 0, None)
        pi /= pi.sum()
        return pi
    except np.linalg.LinAlgError:
        return np.full(n, 1.0 / n)


def print_ctmc_results(sdf):
    """Print Q matrices and stationary distributions at multiple L levels."""
    print('=== CTMC RATE MATRIX Q (per 1000 years, all data) ===')
    Q_all = compute_Q(sdf)
    print(Q_all.round(4).to_string())
    print()

    print('=== STATIONARY DISTRIBUTIONS ===')
    for label, mask in [
        ('All systems',        pd.Series([True]  * len(sdf), index=sdf.index)),
        ('Low-L  (L < 0.45)',  sdf['L'] < 0.45),
        ('Mid-L  (0.45–0.70)', (sdf['L'] >= 0.45) & (sdf['L'] < 0.70)),
        ('High-L (L ≥ 0.70)',  sdf['L'] >= 0.70),
        ('Low-L  (L < 0.60)',  sdf['L'] < 0.60),
        ('High-L (L ≥ 0.60)',  sdf['L'] >= 0.60),
    ]:
        sub = sdf[mask]
        Q = compute_Q(sub, smooth=0.004)
        pi = stationary(Q)
        n_events = int(sub['event'].sum())
        print(f'  {label} (n_events={n_events}):')
        for t, p in zip(TYPES, pi):
            print(f'    {t:15s}: {p:.3f}')
        print()

    print('=== D₀ MODERATOR: EXIT RATES FROM ELECTIVE ===')
    for d0_label, d0_mask in [
        ('D₀ < 0.45',  sdf['D0'] < 0.45),
        ('D₀ ≥ 0.45',  sdf['D0'] >= 0.45),
    ]:
        sub = sdf[d0_mask & (sdf['succ_type'] == 'elective')]
        total_t = sub['duration'].sum()
        rate = sub['event'].sum() / total_t * 1000 if total_t > 0 else float('nan')
        print(f'  {d0_label}: {sub["event"].sum()} events / '
              f'{total_t:.0f} years = {rate:.4f} per 1000 years')

    e_hi = sdf[(sdf['D0'] >= 0.45) & (sdf['succ_type'] == 'elective')]
    e_lo = sdf[(sdf['D0'] <  0.45) & (sdf['succ_type'] == 'elective')]
    r_hi = e_hi['event'].sum() / e_hi['duration'].sum() * 1000
    r_lo = e_lo['event'].sum() / e_lo['duration'].sum() * 1000
    if r_hi > 0:
        print(f'  Ratio (low/high): {r_lo/r_hi:.2f}× '
              f'(high D₀ systems exit elective {r_lo/r_hi:.1f}× slower)')
    print()

    print('=== D₀ MODERATOR: EXIT RATES FROM HEREDITARY ===')
    for d0_label, d0_mask in [
        ('D₀ < 0.45',  sdf['D0'] < 0.45),
        ('D₀ ≥ 0.45',  sdf['D0'] >= 0.45),
    ]:
        sub = sdf[d0_mask & (sdf['succ_type'] == 'hereditary')]
        total_t = sub['duration'].sum()
        rate = sub['event'].sum() / total_t * 1000 if total_t > 0 else float('nan')
        print(f'  {d0_label}: {sub["event"].sum()} events / '
              f'{total_t:.0f} years = {rate:.4f} per 1000 years')
    print()


# ── Kaplan-Meier ──────────────────────────────────────────────────────────────

def kaplan_meier(sdf_sub):
    """Compute Kaplan-Meier survival function from spell data.

    Returns (times, survival_probs) as lists suitable for step-plotting.
    """
    sub = sdf_sub.sort_values('duration').reset_index(drop=True)
    times = sub['duration'].values
    events = sub['event'].values
    n_at_risk = len(times)
    S = 1.0
    t_km = [0]
    S_km = [1.0]
    for dur, ev in zip(times, events):
        if ev == 1:
            S *= (1 - 1 / n_at_risk)
            t_km.append(dur)
            S_km.append(S)
        n_at_risk -= 1
    t_km.append(times[-1])
    S_km.append(S)
    return t_km, S_km


# ── Figure ────────────────────────────────────────────────────────────────────

def make_figure(sdf):
    plt.rcParams.update({
        'font.family': 'serif', 'font.size': 9,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.grid': True, 'grid.alpha': 0.22, 'grid.linewidth': 0.5,
    })

    type_handles = [
        mlines.Line2D([], [], color=COLOURS[t], marker='o',
                      markerfacecolor=COLOURS[t], markeredgecolor='white',
                      markeredgewidth=0.5, markersize=7,
                      linestyle='none', label=t)
        for t in TYPES
    ]

    # Pre-compute Q matrices
    Q_all  = compute_Q(sdf, smooth=0.002)
    Q_lo2  = compute_Q(sdf[sdf['L'] < 0.60],  smooth=0.003)
    Q_hi2  = compute_Q(sdf[sdf['L'] >= 0.60], smooth=0.003)
    Q_lo3  = compute_Q(sdf[sdf['L'] < 0.45],  smooth=0.004)
    Q_mid3 = compute_Q(sdf[(sdf['L'] >= 0.45) & (sdf['L'] < 0.70)], smooth=0.004)
    Q_hi3  = compute_Q(sdf[sdf['L'] >= 0.70],  smooth=0.004)

    pi_all  = stationary(Q_all)
    pi_lo2  = stationary(Q_lo2)
    pi_hi2  = stationary(Q_hi2)
    pi_lo3  = stationary(Q_lo3)
    pi_mid3 = stationary(Q_mid3)
    pi_hi3  = stationary(Q_hi3)

    # Sliding-window stationary distribution
    L_vals = np.linspace(0.05, 0.80, 25)
    stat_by_L = {t: [] for t in TYPES}
    n_spells_L = []
    for L_mid in L_vals:
        sub = sdf[np.abs(sdf['L'] - L_mid) <= 0.22]
        Q = compute_Q(sub, smooth=0.004)
        pi = stationary(Q)
        for i, t in enumerate(TYPES):
            stat_by_L[t].append(pi[i])
        n_spells_L.append(len(sub))

    fig = plt.figure(figsize=(16, 10))
    gs  = GridSpec(3, 3, figure=fig,
                   height_ratios=[1, 1, 0.08],
                   hspace=0.44, wspace=0.38)

    # ── A: Stationary distribution vs L ──────────────────────────────────────
    ax_a = fig.add_subplot(gs[0, 0])
    for t in TYPES:
        ax_a.plot(L_vals, stat_by_L[t], color=COLOURS[t], lw=2.0)
    # Grey shading where data is sparse
    n_arr = np.array(n_spells_L)
    for i in range(len(L_vals) - 1):
        alpha = 0.04 + 0.08 * (1 - min(n_arr[i], 30) / 30)
        ax_a.axvspan(L_vals[i], L_vals[i + 1],
                     alpha=alpha, color='#cccccc', lw=0)
    ax_a.axvline(0.60, color='#aaaaaa', lw=0.8, ls=':')
    ax_a.text(0.61, 0.74, 'L=0.60', fontsize=6, color='#999999')
    ax_a.set_xlabel('L — surplus legibility', fontsize=9)
    ax_a.set_ylabel('Stationary probability π(type)', fontsize=9)
    ax_a.set_ylim(-0.02, 0.82)
    ax_a.set_xlim(0.02, 0.83)
    ax_a.set_title('A.  CTMC stationary distribution vs L\n'
                   '(sliding window ±0.22; shading = sparse data)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)

    # ── B: Q rate matrix heatmap ──────────────────────────────────────────────
    ax_b = fig.add_subplot(gs[0, 1])
    Q_off = Q_all.values.copy()
    np.fill_diagonal(Q_off, np.nan)
    im = ax_b.imshow(Q_off, cmap='YlOrRd', aspect='auto',
                     vmin=0, vmax=np.nanmax(Q_off))
    for i, f in enumerate(TYPES):
        for j, t in enumerate(TYPES):
            if i != j:
                val = Q_off[i, j]
                c = 'white' if val > np.nanmax(Q_off) * 0.65 else '#333333'
                ax_b.text(j, i, f'{val:.3f}', ha='center', va='center',
                          fontsize=7, color=c)
    ax_b.set_xticks(range(5))
    ax_b.set_yticks(range(5))
    ax_b.set_xticklabels(TYPES, fontsize=7.5, rotation=20, ha='right')
    ax_b.set_yticklabels(TYPES, fontsize=7.5)
    ax_b.set_xlabel('To', fontsize=9)
    ax_b.set_ylabel('From', fontsize=9)
    ax_b.set_title('B.  CTMC rate matrix Q\n'
                   '(off-diagonal rates, per 1000 years)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    plt.colorbar(im, ax=ax_b, shrink=0.85, label='Rate per 1000 years')

    # ── C: Three-level stationary distribution bar chart ─────────────────────
    ax_c = fig.add_subplot(gs[0, 2])
    n_lo3  = int((sdf['L'] < 0.45).sum())
    n_mid3 = int(((sdf['L'] >= 0.45) & (sdf['L'] < 0.70)).sum())
    n_hi3  = int((sdf['L'] >= 0.70).sum())
    x = np.arange(len(TYPES))
    width = 0.25
    for pis, col, off, lbl in [
        (pi_lo3,  '#2196F3', -width, f'Low-L (<0.45)  n={n_lo3}'),
        (pi_mid3, '#FF9800',  0,     f'Mid-L (0.45–0.70)  n={n_mid3}'),
        (pi_hi3,  '#F44336',  width, f'High-L (>0.70)  n={n_hi3}'),
    ]:
        ax_c.bar(x + off, pis, width=width * 0.88, color=col, alpha=0.80,
                 label=lbl, edgecolor='white', lw=0.5)
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(TYPES, fontsize=7.5, rotation=18, ha='right')
    ax_c.set_ylabel('Stationary probability', fontsize=9)
    ax_c.set_ylim(0, 0.72)
    ax_c.set_title('C.  Stationary distribution at three L levels',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    ax_c.legend(fontsize=7, loc='upper right', frameon=True, framealpha=0.92)

    # ── D: D₀ moderator exit rates ────────────────────────────────────────────
    ax_d = fig.add_subplot(gs[1, 0])
    d0_vals = np.linspace(0.15, 0.75, 22)

    def safe_rate(sub):
        tt = sub['duration'].sum()
        return sub['event'].sum() / tt * 1000 if tt > 0 else np.nan

    def smooth3(arr):
        return np.convolve([x if x == x else 0 for x in arr],
                           np.ones(3) / 3, mode='same')

    e_hi_r = [safe_rate(sdf[(sdf['D0'] >= d0) & (sdf['succ_type'] == 'elective')])
              for d0 in d0_vals]
    e_lo_r = [safe_rate(sdf[(sdf['D0'] <  d0) & (sdf['succ_type'] == 'elective')])
              for d0 in d0_vals]
    h_hi_r = [safe_rate(sdf[(sdf['D0'] >= d0) & (sdf['succ_type'] == 'hereditary')])
              for d0 in d0_vals]
    h_lo_r = [safe_rate(sdf[(sdf['D0'] <  d0) & (sdf['succ_type'] == 'hereditary')])
              for d0 in d0_vals]

    ax_d.plot(d0_vals, smooth3(e_lo_r), color=COLOURS['elective'],
              lw=1.5, ls='--')
    ax_d.plot(d0_vals, smooth3(e_hi_r), color=COLOURS['elective'],
              lw=2.0, ls='-')
    ax_d.plot(d0_vals, smooth3(h_lo_r), color=COLOURS['hereditary'],
              lw=1.5, ls='--')
    ax_d.plot(d0_vals, smooth3(h_hi_r), color=COLOURS['hereditary'],
              lw=2.0, ls='-')
    ax_d.axvline(0.45, color='#aaaaaa', lw=0.8, ls=':')
    ax_d.text(0.46, 1.35, 'θ=0.45', fontsize=6.5, color='#999999')
    ax_d.set_xlabel('D₀ threshold', fontsize=9)
    ax_d.set_ylabel('Exit rate per 1000 years', fontsize=9)
    ax_d.set_ylim(0, 1.55)
    ax_d.set_title('D.  D₀ moderator: exit rates by type\n'
                   '(solid = high-D₀ group; dashed = low-D₀ group)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)

    # ── E: Kaplan-Meier survival curves ───────────────────────────────────────
    ax_e = fig.add_subplot(gs[1, 1])
    t_max = 1300
    for st in ['hereditary', 'elective', 'appointment']:
        sub = sdf[sdf['succ_type'] == st]
        t_km, S_km = kaplan_meier(sub)
        t_km = [min(v, t_max) for v in t_km]
        ax_e.step(t_km, S_km, color=COLOURS[st], lw=2.0,
                  label=f'{st}  (n={len(sub)}, '
                        f'{int(sub["event"].sum())} ev.)')

    for d0_lbl, d0_mask, ls, alpha in [
        ('Elective, D₀≥0.45',
         (sdf['succ_type'] == 'elective') & (sdf['D0'] >= 0.45), '-',  0.65),
        ('Elective, D₀<0.45',
         (sdf['succ_type'] == 'elective') & (sdf['D0'] <  0.45), '--', 0.65),
    ]:
        sub = sdf[d0_mask]
        if len(sub) < 2:
            continue
        t_km, S_km = kaplan_meier(sub)
        t_km = [min(v, t_max) for v in t_km]
        ax_e.step(t_km, S_km, color=COLOURS['elective'],
                  lw=1.2, ls=ls, alpha=alpha, label=d0_lbl)

    ax_e.set_xlim(0, t_max)
    ax_e.set_ylim(-0.02, 1.05)
    ax_e.set_xlabel('Years in succession type', fontsize=9)
    ax_e.set_ylabel('Survival probability (not transitioned)', fontsize=9)
    ax_e.set_title('E.  Kaplan-Meier survival curves\n'
                   '(bold = by type; thin = elective stratified by D₀)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    ax_e.legend(fontsize=6.5, loc='lower left',
                frameon=True, framealpha=0.92)

    # ── F: Summary table ──────────────────────────────────────────────────────
    ax_f = fig.add_subplot(gs[1, 2])
    ax_f.axis('off')

    e_hi = sdf[(sdf['D0'] >= 0.45) & (sdf['succ_type'] == 'elective')]
    e_lo = sdf[(sdf['D0'] <  0.45) & (sdf['succ_type'] == 'elective')]
    r_e_hi = (e_hi['event'].sum() / e_hi['duration'].sum() * 1000
              if e_hi['duration'].sum() > 0 else 0)
    r_e_lo = (e_lo['event'].sum() / e_lo['duration'].sum() * 1000
              if e_lo['duration'].sum() > 0 else 0)
    ratio  = r_e_lo / r_e_hi if r_e_hi > 0 else float('nan')

    i_app = TYPES.index('appointment')
    i_ele = TYPES.index('elective')
    i_her = TYPES.index('hereditary')

    rows_f = [
        ['Spells / events / years',
         f'{len(sdf)} / {int(sdf["event"].sum())} / {sdf["duration"].sum():,.0f}',
         '—'],
        ['π(appointment) high-L',
         f'{pi_hi2[i_app]:.3f}',
         f'vs low-L: {pi_lo2[i_app]:.3f}'],
        ['π(elective) high-L',
         f'{pi_hi2[i_ele]:.3f}',
         f'vs low-L: {pi_lo2[i_ele]:.3f}'],
        ['π(hereditary) high-L',
         f'{pi_hi2[i_her]:.3f}',
         f'vs low-L: {pi_lo2[i_her]:.3f}'],
        ['Elective exit rate\nhigh D₀ vs low D₀',
         f'{r_e_hi:.3f} per 1000y',
         f'vs {r_e_lo:.3f}'],
        ['D₀ moderator ratio\n(low/high exit rate)',
         f'{ratio:.2f}×' if ratio == ratio else '—',
         ''],
    ]
    tbl = ax_f.table(cellText=rows_f,
                     colLabels=['Metric', 'Value', 'Comparison'],
                     loc='center', cellLoc='left')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(7.5)
    tbl.scale(1, 1.65)
    col_w = [0.40, 0.32, 0.28]
    for (r, c), cell in tbl.get_celld().items():
        cell.set_width(col_w[c] if c < 3 else 0.20)
        if r == 0:
            cell.set_facecolor('#2c3e50')
            cell.set_text_props(color='white', fontweight='bold')
            cell._loc = 'center'
        elif r % 2 == 0:
            cell.set_facecolor('#f5f6fa')
    ax_f.set_title('F.  Key CTMC results',
                   fontsize=9, fontweight='bold', loc='left', pad=6)

    # ── Shared legend ─────────────────────────────────────────────────────────
    ax_leg = fig.add_subplot(gs[2, :])
    ax_leg.axis('off')
    ax_leg.legend(
        handles=type_handles, loc='center', ncol=5, fontsize=8.5,
        frameon=True, framealpha=0.95, edgecolor='#cccccc',
        title='Succession type  (colour consistent across all panels)',
        title_fontsize=8, handlelength=1.2, handletextpad=0.5,
        columnspacing=1.5,
    )

    fig.suptitle(
        'Succession model Phase 3: continuous-time Markov chain (CTMC)\n'
        'Duration-weighted transition rates, stationary distributions, '
        f'and D₀ moderator\n'
        f'n = {len(sdf)} spells, {int(sdf["event"].sum())} events, '
        f'{sdf["duration"].sum():,.0f} total system-years',
        fontsize=10.5, fontweight='bold', y=0.998,
    )

    out = os.path.join(OUTPUT_DIR, 'ctmc_model.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Succession model Phase 3 — CTMC',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Reads governance_extended.csv, parses the succession_changes field to
build a survival spell dataset, estimates the CTMC rate matrix Q,
computes L-conditional stationary distributions, and tests the D₀
moderator prediction.

Outputs:
    visuals/ctmc_model.png       — six-panel figure
    data/survival_spells.csv     — spell-level dataset (145 spells)
    data/transition_data.csv     — re-parsed transition events

The full succession model runs as three scripts in sequence:
    python src/succession_attraction_basins.py        # Phase 1+2
    python src/succession_markov_ctmc.py              # Phase 3
"""
    )
    parser.add_argument('--data', default=DATA_PATH,
                        help='Path to governance_extended.csv')
    parser.add_argument('--no-figure', action='store_true',
                        help='Skip figure generation')
    args = parser.parse_args()

    print("Loading governance data...")
    df = load_governance(args.data)

    print("Parsing transitions from succession_changes field...")
    tdf = parse_transitions(df)

    # Save transition data
    tdf_path = os.path.join(ROOT, 'data', 'transition_data.csv')
    tdf.to_csv(tdf_path, index=False)
    print(f"  Transition data saved to {tdf_path}")

    print("\nBuilding survival spell dataset...")
    sdf = build_survival_spells(df, tdf)

    # Save survival spells
    sdf_path = os.path.join(ROOT, 'data', 'survival_spells.csv')
    sdf.to_csv(sdf_path, index=False)
    print(f"  Survival spells saved to {sdf_path}")

    print()
    print_ctmc_results(sdf)

    if not args.no_figure:
        print("Building figure...")
        make_figure(sdf)

    print("\nDone.")


if __name__ == '__main__':
    main()
