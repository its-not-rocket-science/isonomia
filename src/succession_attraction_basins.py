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

    type_handles = [mpatches.Patch(color=COLOURS[t], label=t)
                    for t in ['hereditary', 'appointment', 'elective',
                               'consensus', 'rotation']]

    fig = plt.figure(figsize=(15, 9))
    gs  = GridSpec(2, 3, figure=fig, hspace=0.44, wspace=0.38)

    # ── A: L × D₀ scatter ────────────────────────────────────────────────────
    ax_a = fig.add_subplot(gs[0, 0])
    for t in TYPE_ORDER:
        sub = ws[ws['succ_canon'] == t]
        ax_a.scatter(sub['L'], sub['D0'], c=COLOURS[t], marker=MARKERS[t],
                     s=50, alpha=0.85, edgecolors='white', lw=0.5, zorder=4)

    # Four anchor-case annotations, placed to avoid cluster overlap
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
    ax_a.legend(handles=type_handles, fontsize=7, loc='upper left',
                frameon=True, framealpha=0.92, edgecolor='#dddddd',
                title='Succession type', title_fontsize=7)

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
    ax_b.legend(handles=type_handles, fontsize=7, loc='center right',
                frameon=True, framealpha=0.92, edgecolor='#dddddd')

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
    ax_c.legend(handles=type_handles, fontsize=7, loc='upper right',
                frameon=True, framealpha=0.92, edgecolor='#dddddd')

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
    ax_e.legend(handles=type_handles, fontsize=7, loc='lower right',
                frameon=True, framealpha=0.92, edgecolor='#dddddd')

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
    print(classification_report(y, y_pred, labels=lr.classes_))

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


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Succession attraction basin analysis — isonomia static model'
    )
    parser.add_argument('--data', default=DATA_PATH,
                        help='Path to governance_extended.csv')
    parser.add_argument('--no-figure', action='store_true',
                        help='Skip figure generation')
    args = parser.parse_args()

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

    # Save the working dataset for Phase 2 (transition coding) and Phase 3
    out_csv = os.path.join(os.path.dirname(OUTPUT_DIR), 'data',
                           'succession_working_set.csv')
    ws.to_csv(out_csv, index=False)
    print(f"Working dataset saved to {out_csv}")
    print()
    print("=== PHASE 2 PREPARATION ===")
    print()
    print("The Markov transition model requires time-ordered within-system")
    print("succession changes.  The following hand-coded systems have notes")
    print("suggesting documented transitions:")
    trans_candidates = ws[ws['notes'].str.contains(
        'succession|transition|changed|reform|replaced|republic|empire',
        case=False, na=False
    )][['System', 'succ_canon', 'L', 'D0', 'notes']]
    if len(trans_candidates):
        for _, row in trans_candidates.iterrows():
            print(f"  {row['System']} ({row['succ_canon']}, "
                  f"L={row['L']:.2f}, D₀={row['D0']:.2f})")
            print(f"    Note: {str(row['notes'])[:120]}...")
    print()
    print("Recommended additions to governance_extended.csv:")
    print("  - succession_changes: structured field recording documented")
    print("    within-system succession mechanism changes")
    print("  - Format: '[from_type]->[to_type] (YEAR): cause_note'")
    print("  - Priority systems: Rome Republic→Empire, Athens oscillation,")
    print("    England Elective→Hereditary→Constitutional, Egypt Old→Middle")
    print("    Kingdom resets, Qin Legalism→Han consolidation")


if __name__ == '__main__':
    main()
