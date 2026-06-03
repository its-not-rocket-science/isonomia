"""
succession_attraction_basins.py
================================
Static attraction basin analysis for the isonomia succession model.

Phase 1 of the succession/Markov model programme. Establishes the
cross-sectional result: succession mechanism clusters into attraction
basins defined primarily by D₀ (pre-existing disobedience freedom),
with L (surplus legibility) shaping the basin landscape and D₀
determining which basin a high-L system occupies.

Usage
-----
    python src/succession_attraction_basins.py

Outputs (to visuals/)
---------------------
    attraction_basins.png   — six-panel figure (see paper caption)

Requirements
------------
    pandas, numpy, scipy, scikit-learn, matplotlib
    governance_extended.csv in data/

Theoretical context
-------------------
The lock-in sequence (Paper 2) predicts that rising L should shift the
stationary distribution of succession mechanisms toward hereditary and
appointment forms as E and D are suppressed.  The counter-case
hypothesis (central to the D₀ interruption argument) predicts that
systems entering high-L conditions with pre-existing high D₀ should
resist this shift — retaining elective or rotation succession even at
high L.

This script tests the static (cross-sectional) version of that
prediction on the hand-coded dataset.  The dynamic Markov chain model
(Phase 3) requires time-ordered within-system succession changes, which
is a separate data-collection task.

Statistical approach
--------------------
1. Multinomial logistic regression: P(succession type | L, D₀, L×D₀)
   — provides predicted probability curves and interaction assessment.
2. Chi-square test on succession type × L regime cross-tab
   — establishes that L predicts succession type distribution.
3. Mann-Whitney U on D₀ for elective vs hereditary in high-L set
   — tests the D₀ moderator hypothesis directly.
4. Binary logistic for elective vs hereditary in high-L: odds ratio.

Data notes
----------
- Working set: hand-coded systems (confidence 2–3) with both
  Succession Method and surplus_legibility coded: n = 64.
- Succession vocabulary is normalised to five canonical types:
  hereditary, elective, appointment, consensus, rotation.
  (charismatic excluded: n = 1, insufficient for modelling.)
- 'Lottery' is mapped to 'elective' (sortition is a sub-type of
  elective succession); 'Testing' to 'charismatic' (merit-by-ordeal).
"""

import os
import sys
import argparse
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.gridspec import GridSpec
from scipy import stats
from scipy.stats import chi2_contingency
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report

# numpy divide-by-zero in np.where expressions is expected (masked by the
# condition) — suppress to keep output clean
warnings.filterwarnings('ignore', category=RuntimeWarning,
                        message='invalid value encountered in')

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT        = os.path.join(SCRIPT_DIR, '..')
DATA_PATH   = os.path.join(ROOT, 'data', 'governance_extended.csv')
OUTPUT_DIR  = os.path.join(ROOT, 'visuals')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Succession vocabulary normalisation ───────────────────────────────────────
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

# Visual identity — consistent across all panels
COLOURS = {
    'hereditary':  '#c0392b',
    'appointment': '#e67e22',
    'elective':    '#2980b9',
    'consensus':   '#27ae60',
    'rotation':    '#8e44ad',
}
MARKERS = {
    'hereditary': 'o', 'appointment': 's', 'elective': '^',
    'consensus':  'D', 'rotation':    'P',
}
TYPE_ORDER = ['consensus', 'rotation', 'elective', 'appointment', 'hereditary']


def sig(p):
    return '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'


# ── Load and prepare ──────────────────────────────────────────────────────────

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    for col in ['exit_freedom', 'disobedience_freedom', 'arrangement_freedom',
                'surplus_legibility', 'info_infrastructure',
                'sovereignty_index', 'admin_index', 'competitive_politics_index']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['succ_canon'] = df['Succession Method'].map(CANON)
    df['L']   = df['surplus_legibility']
    df['D0']  = df['disobedience_freedom']
    df['EDR'] = (df['exit_freedom'] + df['disobedience_freedom'] +
                 df['arrangement_freedom']) / 3
    df['SAP'] = (df['sovereignty_index'] + df['admin_index'] +
                 df['competitive_politics_index']) / 3

    # Working set: hand-coded, both L and D0 present, no charismatic
    ws = df[
        df['coding_confidence'].isin([2, 3]) &
        df['succ_canon'].notna() &
        df['L'].notna() &
        df['D0'].notna() &
        (df['succ_canon'] != 'charismatic')
    ].copy()
    ws['L_D0'] = ws['L'] * ws['D0']
    return ws


# ── Statistical model ─────────────────────────────────────────────────────────

def fit_model(ws):
    """Fit multinomial logistic regression and return (model, scaler, classes)."""
    X = ws[['L', 'D0', 'L_D0']].values
    y = ws['succ_canon'].values
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    lr = LogisticRegression(solver='lbfgs', max_iter=2000, C=1.0, random_state=42)
    lr.fit(Xs, y)
    return lr, scaler, lr.classes_


def sweep_probabilities(lr, scaler, d_val, L_range=None):
    """Predicted probabilities across L at a fixed D₀."""
    if L_range is None:
        L_range = np.linspace(0.05, 0.92, 200)
    X = np.column_stack([L_range, np.full(len(L_range), d_val), L_range * d_val])
    return lr.predict_proba(scaler.transform(X))


def run_statistics(ws, lr, scaler):
    """Run all statistical tests and return a results dict."""
    res = {}

    # Chi-square: succession type × L regime
    tab = pd.crosstab(ws['succ_canon'],
                      (ws['L'] >= 0.60).map({True: 'H', False: 'L'}))
    chi2, p_chi, dof, _ = chi2_contingency(tab)
    res['chi2'] = chi2
    res['p_chi2'] = p_chi
    res['dof'] = dof
    res['n_total'] = len(ws)

    # Mann-Whitney: D₀ for elective vs hereditary in high-L systems
    hi_l = ws[ws['L'] >= 0.60]
    eh   = hi_l[hi_l['succ_canon'].isin(['elective', 'hereditary'])]
    e_d  = eh[eh['succ_canon'] == 'elective']['D0']
    h_d  = eh[eh['succ_canon'] == 'hereditary']['D0']
    u, p_mw = stats.mannwhitneyu(e_d, h_d, alternative='greater')
    rb = 1 - 2 * u / (len(e_d) * len(h_d))
    res['mw_U']     = u
    res['p_mw']     = p_mw
    res['rb']       = rb
    res['n_hil']    = len(eh)
    res['e_median'] = e_d.median()
    res['h_median'] = h_d.median()

    # Binary logistic: odds ratio for D₀ in high-L elective vs hereditary
    eh2 = eh.copy()
    eh2['y'] = (eh2['succ_canon'] == 'elective').astype(int)
    lr2 = LogisticRegression(solver='lbfgs', max_iter=1000)
    lr2.fit(eh2[['D0']].values, eh2['y'].values)
    res['OR_D0'] = float(np.exp(lr2.coef_[0][0]))

    # Multinomial accuracy
    X = ws[['L', 'D0', 'L_D0']].values
    Xs = scaler.transform(X)
    res['accuracy'] = lr.score(Xs, ws['succ_canon'].values)

    # Print summary
    print()
    print('=== ATTRACTION BASIN STATISTICS ===')
    print()
    print(f"Working set: n = {res['n_total']} hand-coded systems")
    print()
    print(f"Chi² (succession type × L regime):")
    print(f"  χ² = {chi2:.2f}  df = {dof}  p = {p_chi:.4f} {sig(p_chi)}")
    print()
    print(f"Mann-Whitney D₀ (elective vs hereditary, high-L ≥ 0.60):")
    print(f"  elective   n = {len(e_d)}  median D₀ = {e_d.median():.2f}")
    print(f"  hereditary n = {len(h_d)}  median D₀ = {h_d.median():.2f}")
    print(f"  U = {u:.0f}  p = {p_mw:.4f} {sig(p_mw)}  rank-biserial r = {rb:.3f}")
    print()
    print(f"Binary logistic odds ratio for D₀ (high-L, elective vs hereditary):")
    print(f"  OR = {res['OR_D0']:.2f}  (1 unit increase in D₀ → {res['OR_D0']:.1f}× odds of elective)")
    print()
    print(f"Multinomial logistic accuracy (L + D₀ + L×D₀): {res['accuracy']:.3f}")
    print()

    return res


# ── Figure ────────────────────────────────────────────────────────────────────

def make_figure(ws, lr, scaler, classes, res):
    plt.rcParams.update({
        'font.family': 'serif', 'font.size': 9,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.grid': True, 'grid.alpha': 0.22, 'grid.linewidth': 0.5,
    })

    L_sw = np.linspace(0.05, 0.92, 200)
    p_lo = sweep_probabilities(lr, scaler, 0.10, L_sw)
    p_hi = sweep_probabilities(lr, scaler, 0.85, L_sw)

    type_handles = [
        mlines.Line2D([], [], color=COLOURS[t], marker=MARKERS[t],
                      markerfacecolor=COLOURS[t], markeredgecolor='white',
                      markeredgewidth=0.5, markersize=8,
                      linestyle='none', label=t)
        for t in ['hereditary', 'appointment', 'elective', 'consensus', 'rotation']
    ]

    # 3-row GridSpec: rows 0-1 are the 2×3 plot grid, row 2 is a thin
    # shared-legend strip. height_ratios keeps the legend strip compact.
    fig = plt.figure(figsize=(15, 10))
    gs  = GridSpec(3, 3, figure=fig,
                   height_ratios=[1, 1, 0.08],
                   hspace=0.44, wspace=0.38)

    # ── A: L × D₀ scatter ────────────────────────────────────────────────────
    ax_a = fig.add_subplot(gs[0, 0])
    for t in TYPE_ORDER:
        sub = ws[ws['succ_canon'] == t]
        ax_a.scatter(sub['L'], sub['D0'], c=COLOURS[t], marker=MARKERS[t],
                     s=50, alpha=0.85, edgecolors='white', lw=0.5, zorder=4)

    anno = {
        'Norwegian Sovereign Wealth Democracy': ('Norway',     (0.72, 0.94)),
        'Gadaa System':                          ('Gadaa',      (0.30, 0.92)),
        'Roman Republic':                        ('Rome Rep.',  (0.50, 0.58)),
        'Confucian Bureaucracy':                 ('Confucian',  (0.80, 0.08)),
    }
    for _, row in ws.iterrows():
        if row['System'] in anno:
            lbl, txt_xy = anno[row['System']]
            ax_a.annotate(lbl, xy=(row['L'], row['D0']), xytext=txt_xy,
                          fontsize=6.5, color='#333333',
                          arrowprops=dict(arrowstyle='->', color='#aaaaaa', lw=0.7))

    ax_a.axvline(0.60, color='#aaaaaa', lw=0.8, ls=':', zorder=1)
    ax_a.axhline(0.50, color='#aaaaaa', lw=0.8, ls=':', zorder=1)
    ax_a.text(0.613, 0.03, 'L = 0.60', fontsize=6, color='#999999')
    ax_a.text(0.07,  0.515, 'D₀ = 0.50', fontsize=6, color='#999999')
    ax_a.set_xlabel('L — surplus legibility', fontsize=9)
    ax_a.set_ylabel('D₀ — disobedience freedom', fontsize=9)
    ax_a.set_title(f'A.  Succession types in L × D₀ space  (n = {res["n_total"]})',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    # No legend here — see shared legend strip below

    # ── B: Predicted probability curves ──────────────────────────────────────
    ax_b = fig.add_subplot(gs[0, 1])
    for probs, ls, al, lw in [(p_lo, '--', 0.70, 1.2), (p_hi, '-', 0.95, 2.0)]:
        for i, cls in enumerate(classes):
            if cls not in COLOURS:
                continue
            ax_b.plot(L_sw, probs[:, i], color=COLOURS[cls], ls=ls, lw=lw, alpha=al)

    ax_b.annotate('↑ D₀ suppresses\nhereditary',
                  xy=(0.75, 0.07), xytext=(0.53, 0.17),
                  fontsize=6.5, color=COLOURS['hereditary'],
                  arrowprops=dict(arrowstyle='->', color=COLOURS['hereditary'], lw=0.8))
    ax_b.annotate('↑ D₀ boosts\nelective',
                  xy=(0.75, 0.66), xytext=(0.51, 0.56),
                  fontsize=6.5, color=COLOURS['elective'],
                  arrowprops=dict(arrowstyle='->', color=COLOURS['elective'], lw=0.8))

    ax_b.axvline(0.60, color='#cccccc', lw=0.8, ls=':', zorder=1)
    ax_b.set_xlabel('L — surplus legibility', fontsize=9)
    ax_b.set_ylabel('Predicted probability', fontsize=9)
    ax_b.set_ylim(-0.02, 1.02)
    ax_b.set_title('B.  P(type | L, D₀) — multinomial logistic\n'
                   '(solid = D₀ 0.85  —  dashed = D₀ 0.10)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    # No per-panel type legend

    # ── C: Moderator shading ──────────────────────────────────────────────────
    ax_c = fig.add_subplot(gs[0, 2])
    for i, cls in enumerate(classes):
        if cls not in COLOURS:
            continue
        ax_c.fill_between(L_sw, p_lo[:, i], p_hi[:, i],
                          alpha=0.13, color=COLOURS[cls])
        ax_c.plot(L_sw, p_hi[:, i], color=COLOURS[cls], lw=2.0, ls='-')
        ax_c.plot(L_sw, p_lo[:, i], color=COLOURS[cls], lw=1.0, ls='--')
    ax_c.axvline(0.60, color='#cccccc', lw=0.8, ls=':', zorder=1)
    ax_c.set_xlabel('L — surplus legibility', fontsize=9)
    ax_c.set_ylabel('Predicted probability', fontsize=9)
    ax_c.set_ylim(-0.02, 1.02)
    ax_c.set_title('C.  D₀ moderator effect  (shading = gap)\n'
                   '(solid = D₀ 0.85  —  dashed = D₀ 0.10)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    # No per-panel type legend

    # ── D: Boxplot D₀ by type × L regime ─────────────────────────────────────
    ax_d = fig.add_subplot(gs[1, 0])
    lo_l = ws[ws['L'] < 0.60]
    hi_l = ws[ws['L'] >= 0.60]
    x_pos = np.arange(len(TYPE_ORDER))
    for regime, fc, offset in [
        (lo_l, '#5dade2', -0.18),
        (hi_l, '#e74c3c', +0.18),
    ]:
        vals = [regime[regime['succ_canon'] == t]['D0'].values for t in TYPE_ORDER]
        ax_d.boxplot(vals, positions=x_pos + offset, widths=0.30,
                     patch_artist=True, notch=False,
                     boxprops=dict(facecolor=fc, alpha=0.65),
                     medianprops=dict(color='#111111', lw=1.8),
                     whiskerprops=dict(lw=0.8), capprops=dict(lw=0.8),
                     flierprops=dict(marker='.', ms=4, alpha=0.5, color=fc))
    ax_d.set_xticks(x_pos)
    ax_d.set_xticklabels(TYPE_ORDER, fontsize=8, rotation=18, ha='right')
    ax_d.set_ylabel('D₀ — disobedience freedom', fontsize=9)
    ax_d.set_ylim(-0.05, 1.05)
    ax_d.set_title('D.  D₀ by type × L regime\n'
                   '(blue = L < 0.60  —  red = L ≥ 0.60)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    # Panel D has its own L-regime legend (not succession types)
    lo_p = mpatches.Patch(facecolor='#5dade2', alpha=0.65, label='L < 0.60')
    hi_p = mpatches.Patch(facecolor='#e74c3c', alpha=0.65, label='L ≥ 0.60')
    ax_d.legend(handles=[lo_p, hi_p], fontsize=7.5, loc='upper right',
                frameon=True, framealpha=0.92)

    # ── E: Attraction basin scatter (high-L only) ─────────────────────────────
    ax_e = fig.add_subplot(gs[1, 1])
    hi_l_all = ws[ws['L'] >= 0.60].copy()
    for t in TYPE_ORDER:
        sub = hi_l_all[hi_l_all['succ_canon'] == t]
        if len(sub) == 0:
            continue
        ax_e.scatter(sub['D0'], sub['L'], c=COLOURS[t], marker=MARKERS[t],
                     s=58, alpha=0.88, edgecolors='white', lw=0.5, zorder=4)

    key_labels = {
        'Norwegian Sovereign Wealth Democracy': 'Norway',
        'Confucian Bureaucracy': 'Confucian Bur.',
        'Tang Dynasty': 'Tang',
        'Ottoman Empire': 'Ottoman',
        'Roman Republic': 'Rome Rep.',
        'Swiss Consensus Democracy': 'Switzerland',
    }
    for _, row in hi_l_all.iterrows():
        if row['System'] in key_labels:
            ax_e.annotate(key_labels[row['System']], (row['D0'], row['L']),
                          xytext=(5, 3), textcoords='offset points',
                          fontsize=6, color='#333333')

    ax_e.axvline(0.50, color='#aaaaaa', lw=0.8, ls=':', zorder=1)
    ax_e.set_xlabel('D₀ — disobedience freedom', fontsize=9)
    ax_e.set_ylabel('L — surplus legibility', fontsize=9)
    ax_e.set_title('E.  Attraction basins (L ≥ 0.60)\n'
                   'D₀ discriminates elective from hereditary',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    ax_e.text(0.97, 0.97,
              f'Elective vs hereditary (D₀)\n'
              f'Mann-Whitney p = {res["p_mw"]:.4f} {sig(res["p_mw"])}\n'
              f'rank-biserial r = {res["rb"]:.3f}',
              transform=ax_e.transAxes, fontsize=7.5, va='top', ha='right',
              bbox=dict(boxstyle='round,pad=0.4', fc='white',
                        ec='#cccccc', alpha=0.92))
    # No per-panel type legend

    # ── F: Statistics table ───────────────────────────────────────────────────
    ax_f = fig.add_subplot(gs[1, 2])
    ax_f.axis('off')
    col_labels = ['Test', 'Result', 'p', 'n']
    rows = [
        ['χ²: succession × L',
         f'{res["chi2"]:.2f} (df={res["dof"]})',
         f'{res["p_chi2"]:.4f} {sig(res["p_chi2"])}',
         str(res['n_total'])],
        ['MW: D₀ elective vs\nhereditary (L ≥ 0.60)',
         f'U = {res["mw_U"]:.0f}  r = {res["rb"]:.3f}',
         f'{res["p_mw"]:.4f} {sig(res["p_mw"])}',
         str(res['n_hil'])],
        ['Binary logit OR(D₀)\nelective vs hereditary',
         f'OR = {res["OR_D0"]:.2f}',
         '—',
         str(res['n_hil'])],
        ['Multinomial accuracy\n(L + D₀ + L×D₀)',
         f'{res["accuracy"]:.3f}',
         '—',
         str(res['n_total'])],
    ]
    tbl = ax_f.table(cellText=rows, colLabels=col_labels,
                     loc='center', cellLoc='left')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(7.5)
    tbl.scale(1, 1.9)
    col_w = [0.38, 0.30, 0.20, 0.09]
    for (r, c), cell in tbl.get_celld().items():
        cell.set_width(col_w[c] if c < len(col_w) else 0.12)
        if r == 0:
            cell.set_facecolor('#2c3e50')
            cell.set_text_props(color='white', fontweight='bold')
            cell._loc = 'center'
        elif r % 2 == 0:
            cell.set_facecolor('#f5f6fa')
    ax_f.set_title('F.  Key statistics',
                   fontsize=9, fontweight='bold', loc='left', pad=6)

    # ── Shared succession-type legend strip (row 2, spanning all 3 columns) ──
    # A single invisible axis spanning the full bottom strip hosts one horizontal
    # legend centred below all six panels.
    ax_leg = fig.add_subplot(gs[2, :])
    ax_leg.axis('off')
    ax_leg.legend(
        handles=type_handles,
        loc='center',
        ncol=len(type_handles),
        fontsize=8.5,
        frameon=True,
        framealpha=0.95,
        edgecolor='#cccccc',
        title='Succession type  (colour + marker consistent across all panels)',
        title_fontsize=8,
        handlelength=1.2,
        handletextpad=0.5,
        columnspacing=1.5,
    )

    fig.suptitle(
        'Succession mechanism attraction basins: '
        'surplus legibility and disobedience freedom as predictors\n'
        'Static model — hand-coded isonomia systems (confidence 2–3), '
        f'n = {res["n_total"]}',
        fontsize=11, fontweight='bold', y=0.995
    )

    out_path = os.path.join(OUTPUT_DIR, 'attraction_basins.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


# ── Print confusion matrix and classification report ─────────────────────────

def print_model_diagnostics(ws, lr, scaler):
    X = ws[['L', 'D0', 'L_D0']].values
    y = ws['succ_canon'].values
    Xs = scaler.transform(X)
    y_pred = lr.predict(Xs)

    print('=== MULTINOMIAL MODEL DIAGNOSTICS ===')
    print()
    print('Confusion matrix (rows = actual, columns = predicted):')
    cm = pd.DataFrame(
        confusion_matrix(y, y_pred, labels=lr.classes_),
        index=lr.classes_, columns=lr.classes_
    )
    print(cm)
    print()
    print('Classification report:')
    print(classification_report(y, y_pred, labels=lr.classes_, zero_division=0))

    print()
    print('Predicted probabilities at key L × D₀ grid points:')
    print(f'{"D₀":>6}  {"L":>5}  ' +
          '  '.join(f'{c:>12}' for c in lr.classes_))
    for d_val in [0.10, 0.50, 0.85]:
        for l_val in [0.30, 0.60, 0.80]:
            X_pt = np.array([[l_val, d_val, l_val * d_val]])
            probs = lr.predict_proba(scaler.transform(X_pt))[0]
            row = f'{d_val:>6.2f}  {l_val:>5.2f}  '
            row += '  '.join(f'{p:>12.3f}' for p in probs)
            print(row)
        print()


# ── Succession type descriptive table ─────────────────────────────────────────

def print_descriptive_table(ws):
    print('=== SUCCESSION TYPE DESCRIPTIVE STATISTICS ===')
    print()
    desc = ws.groupby('succ_canon').agg(
        n=('L', 'count'),
        L_mean=('L', 'mean'),
        L_std=('L', 'std'),
        D0_mean=('D0', 'mean'),
        D0_std=('D0', 'std'),
        EDR_mean=('EDR', 'mean'),
    ).round(3)
    print(desc.to_string())
    print()
    print('Cross-tab: succession type × L regime (low < 0.60 / high ≥ 0.60):')
    print(pd.crosstab(ws['succ_canon'],
                      (ws['L'] >= 0.60).map({True: 'L ≥ 0.60', False: 'L < 0.60'})))
    print()
    print('Cross-tab: succession type × D₀ regime (low < 0.50 / high ≥ 0.50):')
    print(pd.crosstab(ws['succ_canon'],
                      (ws['D0'] >= 0.50).map({True: 'D₀ ≥ 0.50', False: 'D₀ < 0.50'})))
    print()


# ── Phase 2: Transition parsing and analysis ──────────────────────────────────
#
# The succession_changes field in governance_extended.csv records documented
# within-system succession mechanism transitions in the format:
#
#   '[from_type]->[to_type] (YEAR): trigger_note'
#
# Multiple transitions per system are separated by ' | '.
# Trigger types: P_to_S, external_shock, elite_reform, collapse,
#                reconsolidation, internal, other
#
# 'changed' flag: 1 if from_succ != to_succ, 0 if same type (L/D shift).
# Same-type transitions are retained because they provide L-conditional
# stability evidence for the Markov model (Phase 3).
#
# Data coverage (Phase 2 complete):
#   37 transition events across 24 systems
#   26 type-changing, 11 same-type (L/D shift)
#   Trigger breakdown: elite_reform=11, external_shock=10, collapse=6,
#                      internal=5, reconsolidation=4, other=1


TRIG_COLOURS = {
    'collapse':       '#c0392b',
    'elite_reform':   '#27ae60',
    'external_shock': '#e67e22',
    'internal':       '#8e44ad',
    'reconsolidation':'#2980b9',
    'other':          '#aaaaaa',
}

TRIG_ORDER = ['elite_reform', 'external_shock', 'collapse',
              'reconsolidation', 'internal']


def parse_succession_changes(df):
    """Parse the succession_changes field into a flat transition DataFrame.

    Each row in the output is one transition event.  L_from and D0_from
    are the values for the *from* system at the time of the transition
    (taken from the system's coded values — a limitation for systems whose
    L or D0 changed over time, noted in coding_scheme.md).

    Returns a pandas DataFrame with columns:
        system, year, from_succ, to_succ, L_from, D0_from,
        trigger, region, changed
    """
    rows = []
    trig_keywords = {
        'P_to_S':          'P_to_S',
        'external_shock':  'external_shock',
        'elite_reform':    'elite_reform',
        'collapse':        'collapse',
        'reconsolidation': 'reconsolidation',
        'internal':        'internal',
    }
    for _, sys_row in df[df['succession_changes'].fillna('') != ''].iterrows():
        for entry in sys_row['succession_changes'].split(' | '):
            entry = entry.strip()
            if not entry:
                continue
            try:
                arrow_part, rest = entry.split(' (', 1)
                from_succ, to_succ = arrow_part.split('->')
                year_str, note = rest.split('): ', 1)
                year = int(year_str.strip())
                trig = next(
                    (v for k, v in trig_keywords.items() if k in note.lower()),
                    'other'
                )
                rows.append({
                    'system':    sys_row['System'],
                    'year':      year,
                    'from_succ': from_succ.strip(),
                    'to_succ':   to_succ.strip(),
                    'L_from':    sys_row.get('surplus_legibility', float('nan')),
                    'D0_from':   sys_row.get('disobedience_freedom', float('nan')),
                    'trigger':   trig,
                    'region':    sys_row.get('Region', ''),
                    'changed':   int(from_succ.strip() != to_succ.strip()),
                })
            except Exception as exc:
                print(f"  Parse warning: {entry[:60]} — {exc}")

    tdf = pd.DataFrame(rows)
    print(f"  Parsed {len(tdf)} transition events across "
          f"{tdf['system'].nunique()} systems "
          f"({tdf['changed'].sum()} type-changing, "
          f"{(tdf['changed']==0).sum()} same-type L/D shifts)")
    return tdf


def save_transition_csv(tdf):
    """Write parsed transitions to data/transition_data.csv."""
    out = os.path.join(ROOT, 'data', 'transition_data.csv')
    tdf.to_csv(out, index=False)
    print(f"  Transition data saved to {out}")


def run_transition_statistics(tdf):
    """Print transition matrix and key statistics."""
    changed = tdf[tdf['changed'] == 1]
    print()
    print('=== PHASE 2 TRANSITION STATISTICS ===')
    print()
    print(f'Total events: {len(tdf)}  '
          f'(type-changing: {len(changed)}, '
          f'same-type: {len(tdf)-len(changed)})')
    print()
    print('Transition matrix (row = from, col = to; type-changing only):')
    print(pd.crosstab(changed['from_succ'], changed['to_succ']))
    print()
    print('Row-normalised transition probabilities:')
    print(pd.crosstab(changed['from_succ'], changed['to_succ'],
                      normalize='index').round(2))
    print()
    print('Trigger → destination:')
    print(pd.crosstab(changed['trigger'], changed['to_succ']))
    print()

    # L-conditional: high-L vs low-L transition probabilities
    hi_ch = changed[changed['L_from'] >= 0.60]
    lo_ch = changed[changed['L_from'] < 0.60]
    print(f'High-L transitions (L≥0.60, n={len(hi_ch)}):')
    if len(hi_ch) >= 3:
        print(pd.crosstab(hi_ch['from_succ'], hi_ch['to_succ'],
                          normalize='index').round(2))
    print()
    print(f'Low-L transitions (L<0.60, n={len(lo_ch)}):')
    if len(lo_ch) >= 3:
        print(pd.crosstab(lo_ch['from_succ'], lo_ch['to_succ'],
                          normalize='index').round(2))
    print()

    # Key theoretical tests
    print('Key tests:')
    elite = changed[changed['trigger'] == 'elite_reform']
    print(f'  Elite reform → hereditary: '
          f'{(elite["to_succ"]=="hereditary").sum()}/{len(elite)} '
          f'= {(elite["to_succ"]=="hereditary").mean():.2f}')
    internal = changed[changed['trigger'] == 'internal']
    print(f'  Internal → hereditary: '
          f'{(internal["to_succ"]=="hereditary").sum()}/{len(internal)} '
          f'= {(internal["to_succ"]=="hereditary").mean():.2f}')
    print()

    # Markov cell coverage
    types = ['hereditary', 'appointment', 'elective', 'consensus', 'rotation']
    n_cells = len(types) * (len(types) - 1)
    n_filled = sum(1 for f in types for t in types
                   if f != t and len(changed[
                       (changed['from_succ'] == f) &
                       (changed['to_succ'] == t)]) > 0)
    print(f'Markov matrix coverage: {n_filled}/{n_cells} cells filled '
          f'({100*n_filled/n_cells:.0f}%)')
    print('Empty cells (most critical for Phase 3):')
    for f in types:
        for t in types:
            if f != t:
                n = len(changed[(changed['from_succ']==f) & (changed['to_succ']==t)])
                if n == 0:
                    print(f'  {f}→{t}')


def make_transition_figure(tdf):
    """Build the six-panel Phase 2 transition analysis figure."""
    import matplotlib.pyplot as _plt
    import matplotlib.lines as _ml
    import matplotlib.patches as _mp
    from matplotlib.gridspec import GridSpec as _GS
    import numpy as _np

    _plt.rcParams.update({
        'font.family': 'serif', 'font.size': 9,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.grid': True, 'grid.alpha': 0.22, 'grid.linewidth': 0.5,
    })

    changed = tdf[tdf['changed'] == 1].copy()
    types_m = ['hereditary', 'appointment', 'elective', 'consensus', 'rotation']
    n_t = len(types_m)

    # Raw count matrix
    matrix = _np.zeros((n_t, n_t))
    for _, row in changed.iterrows():
        f, t = row['from_succ'], row['to_succ']
        if f in types_m and t in types_m:
            matrix[types_m.index(f), types_m.index(t)] += 1
    rs = matrix.sum(1, keepdims=True)
    matrix_norm = _np.where(rs > 0, matrix / rs, 0)

    # High-L vs low-L matrices
    hi_ch = changed[changed['L_from'] >= 0.60]
    lo_ch = changed[changed['L_from'] < 0.60]
    m_hi = _np.zeros((n_t, n_t))
    m_lo = _np.zeros((n_t, n_t))
    for _, row in hi_ch.iterrows():
        f, t = row['from_succ'], row['to_succ']
        if f in types_m and t in types_m:
            m_hi[types_m.index(f), types_m.index(t)] += 1
    for _, row in lo_ch.iterrows():
        f, t = row['from_succ'], row['to_succ']
        if f in types_m and t in types_m:
            m_lo[types_m.index(f), types_m.index(t)] += 1
    rs_hi = m_hi.sum(1, keepdims=True)
    rs_lo = m_lo.sum(1, keepdims=True)
    m_hi_n = _np.where(rs_hi > 0, m_hi / rs_hi, _np.nan)
    m_lo_n = _np.where(rs_lo > 0, m_lo / rs_lo, _np.nan)
    diff = _np.where(_np.isnan(m_hi_n) | _np.isnan(m_lo_n), _np.nan,
                     m_hi_n - m_lo_n)

    # Trigger matrix
    trig_order = ['elite_reform', 'external_shock', 'collapse',
                  'reconsolidation', 'internal']
    dest_order = ['elective', 'appointment', 'hereditary', 'rotation']
    trig_matrix = _np.zeros((len(trig_order), len(dest_order)))
    for _, row in changed.iterrows():
        t_k, d = row['trigger'], row['to_succ']
        if t_k in trig_order and d in dest_order:
            trig_matrix[trig_order.index(t_k), dest_order.index(d)] += 1
    rs_t = trig_matrix.sum(1, keepdims=True)
    trig_norm = _np.where(rs_t > 0, trig_matrix / rs_t, 0)

    type_handles = [
        _ml.Line2D([], [], color=COLOURS[t], marker=MARKERS[t],
                   markerfacecolor=COLOURS[t], markeredgecolor='white',
                   markeredgewidth=0.5, markersize=7,
                   linestyle='none', label=t)
        for t in ['hereditary', 'appointment', 'elective', 'consensus']
    ]

    fig = _plt.figure(figsize=(16, 9))
    gs  = _GS(2, 3, figure=fig, hspace=0.46, wspace=0.40)

    # ── A: Empirical transition matrix heatmap ────────────────────────────────
    ax_a = fig.add_subplot(gs[0, 0])
    im = ax_a.imshow(matrix_norm, cmap='Blues', vmin=0, vmax=1, aspect='auto')
    for i in range(n_t):
        for j in range(n_t):
            if i != j:
                n_val = int(matrix[i, j])
                txt = f'{matrix_norm[i,j]:.2f}\n(n={n_val})'
                c = 'white' if matrix_norm[i, j] > 0.55 else '#333333'
                ax_a.text(j, i, txt, ha='center', va='center',
                          fontsize=7, color=c)
    ax_a.set_xticks(range(n_t))
    ax_a.set_yticks(range(n_t))
    ax_a.set_xticklabels(types_m, fontsize=8, rotation=20, ha='right')
    ax_a.set_yticklabels(types_m, fontsize=8)
    ax_a.set_xlabel('To', fontsize=9)
    ax_a.set_ylabel('From', fontsize=9)
    ax_a.set_title('A.  Empirical transition matrix\n'
                   '(row-normalised; diagonal = no-change)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    _plt.colorbar(im, ax=ax_a, shrink=0.85, label='Transition probability')

    # ── B: L-conditional difference ──────────────────────────────────────────
    ax_b = fig.add_subplot(gs[0, 1])
    im2 = ax_b.imshow(diff, cmap='RdBu_r', vmin=-0.6, vmax=0.6, aspect='auto')
    for i in range(n_t):
        for j in range(n_t):
            if i != j and not _np.isnan(diff[i, j]):
                ax_b.text(j, i, f'{diff[i,j]:+.2f}',
                          ha='center', va='center', fontsize=7.5)
    ax_b.set_xticks(range(n_t))
    ax_b.set_yticks(range(n_t))
    ax_b.set_xticklabels(types_m, fontsize=8, rotation=20, ha='right')
    ax_b.set_yticklabels(types_m, fontsize=8)
    ax_b.set_xlabel('To', fontsize=9)
    ax_b.set_ylabel('From', fontsize=9)
    ax_b.set_title('B.  L-conditional shift: high-L minus low-L\n'
                   '(blue=more likely at high L, red=less likely)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    _plt.colorbar(im2, ax=ax_b, shrink=0.85,
                  label='Δ probability (high-L − low-L)')

    # ── C: Trigger → destination heatmap ─────────────────────────────────────
    ax_c = fig.add_subplot(gs[0, 2])
    im3 = ax_c.imshow(trig_norm, cmap='Greens', vmin=0, vmax=1, aspect='auto')
    for i in range(len(trig_order)):
        for j in range(len(dest_order)):
            n_val = int(trig_matrix[i, j])
            if n_val > 0:
                c = 'white' if trig_norm[i, j] > 0.6 else '#333333'
                ax_c.text(j, i, f'{trig_norm[i,j]:.2f}\n(n={n_val})',
                          ha='center', va='center', fontsize=7, color=c)
    ax_c.set_xticks(range(len(dest_order)))
    ax_c.set_yticks(range(len(trig_order)))
    ax_c.set_xticklabels(dest_order, fontsize=8, rotation=15, ha='right')
    ax_c.set_yticklabels(trig_order, fontsize=8)
    ax_c.set_xlabel('Destination type', fontsize=9)
    ax_c.set_title('C.  Trigger → destination type\n'
                   '(row-normalised probabilities)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    _plt.colorbar(im3, ax=ax_c, shrink=0.85,
                  label='P(destination | trigger)')

    # ── D: D₀ at transition by destination type ───────────────────────────────
    ax_d = fig.add_subplot(gs[1, 0])
    dest_types = ['hereditary', 'appointment', 'elective', 'rotation']
    for i, dest in enumerate(dest_types):
        d0v = changed[changed['to_succ'] == dest]['D0_from'].values
        jitter = _np.random.default_rng(42).normal(0, 0.06, len(d0v))
        ax_d.scatter(d0v, _np.full(len(d0v), i) + jitter,
                     c=COLOURS.get(dest, '#888888'),
                     marker=MARKERS.get(dest, 'o'),
                     s=55, alpha=0.80, edgecolors='white', lw=0.5, zorder=4)
        if len(d0v):
            ax_d.plot([_np.median(d0v)] * 2, [i - 0.28, i + 0.28],
                      color='#333333', lw=2.5, zorder=5)
    # Annotate the Rome P→S exception
    rome_hered = changed[(changed['system'] == 'Roman Republic') &
                         (changed['to_succ'] == 'hereditary')]
    for _, rr in rome_hered.iterrows():
        ax_d.annotate('Rome\n(P→S)',
                      xy=(rr['D0_from'], dest_types.index('hereditary')),
                      xytext=(rr['D0_from'] + 0.06,
                              dest_types.index('hereditary') + 0.35),
                      fontsize=6.5, color='#c0392b',
                      arrowprops=dict(arrowstyle='->', color='#c0392b', lw=0.8))
    ax_d.set_yticks(range(len(dest_types)))
    ax_d.set_yticklabels(dest_types, fontsize=8)
    ax_d.set_xlabel('D₀ at time of transition', fontsize=9)
    ax_d.set_title('D.  D₀ at transition by destination type\n(bar = median)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    ax_d.axvline(0.50, color='#aaaaaa', lw=0.8, ls=':')

    # ── E: L at transition by trigger type ────────────────────────────────────
    ax_e = fig.add_subplot(gs[1, 1])
    for i, trig in enumerate(trig_order):
        sub = changed[changed['trigger'] == trig]
        if len(sub) == 0:
            continue
        jitter = _np.random.default_rng(42 + i).normal(0, 0.07, len(sub))
        ax_e.scatter(sub['L_from'].values,
                     _np.full(len(sub), i) + jitter,
                     c=[COLOURS.get(t, '#888888') for t in sub['to_succ']],
                     s=55, alpha=0.80, edgecolors='white', lw=0.5, zorder=4)
        ax_e.plot([sub['L_from'].median()] * 2, [i - 0.28, i + 0.28],
                  color='#333333', lw=2.5, zorder=5)
    ax_e.axvline(0.60, color='#aaaaaa', lw=0.8, ls=':')
    ax_e.set_yticks(range(len(trig_order)))
    ax_e.set_yticklabels(trig_order, fontsize=8)
    ax_e.set_xlabel('L at time of transition', fontsize=9)
    ax_e.set_title('E.  L at transition by trigger type\n'
                   '(dot colour = destination; bar = median)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    ax_e.legend(handles=type_handles, fontsize=7, title='Dest.',
                title_fontsize=7, loc='lower right',
                frameon=True, framealpha=0.92, ncol=2)

    # ── F: Summary table ──────────────────────────────────────────────────────
    ax_f = fig.add_subplot(gs[1, 2])
    ax_f.axis('off')
    cells_filled = sum(1 for i in range(n_t) for j in range(n_t)
                       if i != j and matrix[i, j] > 0)
    cells_total = n_t * (n_t - 1)
    elite = changed[changed['trigger'] == 'elite_reform']
    internal = changed[changed['trigger'] == 'internal']
    rows_f = [
        ['Total transition events', '37', 'n_systems=24'],
        ['Type-changing', '26', '—'],
        ['Same-type (L/D shift)', '11', '—'],
        ['Markov cells filled',
         f'{cells_filled}/{cells_total}',
         f'{100*cells_filled/cells_total:.0f}%'],
        ['Elite reform → hereditary',
         f'{(elite["to_succ"]=="hereditary").sum()}/{len(elite)}',
         '0%'],
        ['Internal → hereditary',
         f'{(internal["to_succ"]=="hereditary").sum()}/{len(internal)}',
         '100%'],
        ['P→S exception (Rome)', '1 case', 'D₀=0.50'],
    ]
    tbl = ax_f.table(cellText=rows_f,
                     colLabels=['Metric', 'Value', 'Note'],
                     loc='center', cellLoc='left')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(7.5)
    tbl.scale(1, 1.65)
    col_w = [0.45, 0.22, 0.28]
    for (r, c), cell in tbl.get_celld().items():
        cell.set_width(col_w[c] if c < 3 else 0.20)
        if r == 0:
            cell.set_facecolor('#2c3e50')
            cell.set_text_props(color='white', fontweight='bold')
            cell._loc = 'center'
        elif r % 2 == 0:
            cell.set_facecolor('#f5f6fa')
    ax_f.set_title('F.  Phase 2 transition summary',
                   fontsize=9, fontweight='bold', loc='left', pad=6)

    fig.suptitle(
        'Succession model Phase 2: empirical transition matrix and trigger analysis\n'
        f'{len(tdf)} transition events across {tdf["system"].nunique()} systems  '
        f'({tdf["changed"].sum()} type-changing, {(tdf["changed"]==0).sum()} same-type)',
        fontsize=11, fontweight='bold', y=0.998
    )
    out = os.path.join(OUTPUT_DIR, 'transition_matrix.png')
    _plt.savefig(out, dpi=150, bbox_inches='tight')
    _plt.close()
    print(f"Saved: {out}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Succession attraction basin analysis — Phase 1 (static) '
                    'and Phase 2 (transition matrix)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Phases:
  Phase 1 (default): static attraction basin analysis
    Multinomial logistic P(type | L, D0, L*D0); chi-square; Mann-Whitney;
    binary logistic OR.  Outputs: visuals/attraction_basins.png,
    data/succession_working_set.csv.

  Phase 2 (--phase2): transition matrix and trigger analysis
    Parses succession_changes field from governance_extended.csv;
    builds empirical transition matrix conditioned on L; trigger → destination
    probabilities; D0 at transition by destination.
    Outputs: visuals/transition_matrix.png, data/transition_data.csv.

  Both phases run together with --phase2 flag.
"""
    )
    parser.add_argument('--data', default=DATA_PATH,
                        help='Path to governance_extended.csv')
    parser.add_argument('--phase2', action='store_true',
                        help='Also run Phase 2 transition analysis')
    parser.add_argument('--no-figure', action='store_true',
                        help='Skip figure generation')
    args = parser.parse_args()

    # ── Phase 1 ───────────────────────────────────────────────────────────────
    ws = load_data(args.data)
    print(f"Loaded working set: {len(ws)} hand-coded systems with "
          f"succession type, L, and D₀")
    print(f"Succession type counts:")
    print(ws['succ_canon'].value_counts().to_string())

    print_descriptive_table(ws)

    lr, scaler, classes = fit_model(ws)
    res = run_statistics(ws, lr, scaler)
    print_model_diagnostics(ws, lr, scaler)

    if not args.no_figure:
        make_figure(ws, lr, scaler, classes, res)

    out_csv = os.path.join(ROOT, 'data', 'succession_working_set.csv')
    ws.to_csv(out_csv, index=False)
    print(f"Working dataset saved to {out_csv}")

    # ── Phase 2 ───────────────────────────────────────────────────────────────
    if args.phase2:
        print()
        print("=== PHASE 2: TRANSITION ANALYSIS ===")
        df_full = pd.read_csv(args.data)
        df_full.columns = df_full.columns.str.strip()
        for col in ['surplus_legibility', 'disobedience_freedom']:
            df_full[col] = pd.to_numeric(df_full[col], errors='coerce')

        tdf = parse_succession_changes(df_full)
        save_transition_csv(tdf)
        run_transition_statistics(tdf)

        if not args.no_figure:
            make_transition_figure(tdf)
    else:
        print()
        print("Run with --phase2 to generate transition matrix analysis.")
        print("Requires succession_changes field in governance_extended.csv.")


if __name__ == '__main__':
    main()

