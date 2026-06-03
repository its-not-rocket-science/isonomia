"""
succession_attraction_basins.py
================================
Static attraction basin analysis for the isonomia succession model.

Phase 1: cross-sectional result — succession mechanism clusters into
attraction basins defined by D0 (pre-existing disobedience freedom),
with L (surplus legibility) shaping the basin landscape.

Phase 2: empirical transition matrix from the succession_changes field.

Usage
-----
    python src/succession_attraction_basins.py
    python src/succession_attraction_basins.py --phase2
    python src/succession_attraction_basins.py --phase2 --figure

Outputs (always written)
------------------------
    data/succession_working_set.csv   — Phase 1 working set
    data/transition_data.csv          — Phase 2 (requires --phase2)

Outputs (only with --figure)
-----------------------------
    visuals/attraction_basins.png     — Phase 1 six-panel figure
    visuals/transition_matrix.png     — Phase 2 six-panel figure

Statistical approach
--------------------
1. Multinomial logistic regression: P(succession type | L, D0, L*D0)
2. Chi-square test on succession type x L regime cross-tab
3. Mann-Whitney U on D0 for elective vs hereditary in high-L set
4. Binary logistic for elective vs hereditary in high-L: odds ratio

Phase 3 (CTMC model) is in succession_markov_ctmc.py.
"""

import os
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

warnings.filterwarnings('ignore', category=RuntimeWarning,
                        message='invalid value encountered in')

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.join(SCRIPT_DIR, '..')
DATA_PATH  = os.path.join(ROOT, 'data', 'governance_extended.csv')
OUTPUT_DIR = os.path.join(ROOT, 'visuals')

# ── Vocabulary ─────────────────────────────────────────────────────────────────
CANON = {
    'Hereditary': 'hereditary', 'Dynastic': 'hereditary',
    'Inheritance': 'hereditary', 'Matrilineal': 'hereditary',
    'Patriarchal': 'hereditary',
    'Election': 'elective', 'Elections': 'elective', 'Elective': 'elective',
    'Sortition': 'elective', 'Referendum': 'elective', 'Lottery': 'elective',
    'Consensus': 'consensus', 'Elder consensus': 'consensus',
    'Acclamation': 'consensus',
    'Rotation': 'rotation', 'Age grades': 'rotation',
    'Appointment': 'appointment', 'Merit-based': 'appointment',
    'Exams': 'appointment', 'Co-optation': 'appointment',
    'Promotion': 'appointment',
    'Charismatic': 'charismatic', 'Charismatic selection': 'charismatic',
    'Oratory skill': 'charismatic', 'Competition': 'charismatic',
    'Competitive': 'charismatic', 'Testing': 'charismatic',
}

COLOURS = {
    'hereditary': '#c0392b', 'appointment': '#e67e22',
    'elective': '#2980b9', 'consensus': '#27ae60', 'rotation': '#8e44ad',
}
MARKERS = {
    'hereditary': 'o', 'appointment': 's', 'elective': '^',
    'consensus': 'D', 'rotation': 'P',
}
TYPE_ORDER = ['consensus', 'rotation', 'elective', 'appointment', 'hereditary']

TRIG_COLOURS = {
    'collapse': '#c0392b', 'elite_reform': '#27ae60',
    'external_shock': '#e67e22', 'internal': '#8e44ad',
    'reconsolidation': '#2980b9', 'other': '#aaaaaa',
}
TRIG_ORDER = ['elite_reform', 'external_shock', 'collapse',
              'reconsolidation', 'internal']


def sig(p):
    return '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'


# ── Data loading ───────────────────────────────────────────────────────────────

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    for col in ['exit_freedom', 'disobedience_freedom', 'arrangement_freedom',
                'surplus_legibility', 'info_infrastructure',
                'sovereignty_index', 'admin_index',
                'competitive_politics_index']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['succ_canon'] = df['Succession Method'].map(CANON)
    df['L']   = df['surplus_legibility']
    df['D0']  = df['disobedience_freedom']
    df['EDR'] = (df['exit_freedom'] + df['disobedience_freedom'] +
                 df['arrangement_freedom']) / 3
    df['SAP'] = (df['sovereignty_index'] + df['admin_index'] +
                 df['competitive_politics_index']) / 3
    ws = df[
        df['coding_confidence'].isin([2, 3]) &
        df['succ_canon'].notna() &
        df['L'].notna() &
        df['D0'].notna() &
        (df['succ_canon'] != 'charismatic')
    ].copy()
    ws['L_D0'] = ws['L'] * ws['D0']
    return ws


# ── Phase 1: static model ──────────────────────────────────────────────────────

def fit_model(ws):
    X = ws[['L', 'D0', 'L_D0']].values
    y = ws['succ_canon'].values
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    lr = LogisticRegression(solver='lbfgs', max_iter=2000, C=1.0,
                            random_state=42)
    lr.fit(Xs, y)
    return lr, scaler, lr.classes_


def sweep_probabilities(lr, scaler, d_val, L_range=None):
    if L_range is None:
        L_range = np.linspace(0.05, 0.92, 200)
    X = np.column_stack([L_range, np.full(len(L_range), d_val),
                         L_range * d_val])
    return lr.predict_proba(scaler.transform(X))


def run_statistics(ws, lr, scaler):
    res = {}
    tab = pd.crosstab(ws['succ_canon'],
                      (ws['L'] >= 0.60).map({True: 'H', False: 'L'}))
    chi2, p_chi, dof, _ = chi2_contingency(tab)
    res.update(chi2=chi2, p_chi2=p_chi, dof=dof, n_total=len(ws))

    hi_l = ws[ws['L'] >= 0.60]
    eh   = hi_l[hi_l['succ_canon'].isin(['elective', 'hereditary'])]
    e_d  = eh[eh['succ_canon'] == 'elective']['D0']
    h_d  = eh[eh['succ_canon'] == 'hereditary']['D0']
    u, p_mw = stats.mannwhitneyu(e_d, h_d, alternative='greater')
    rb = 1 - 2 * u / (len(e_d) * len(h_d))
    res.update(mw_U=u, p_mw=p_mw, rb=rb, n_hil=len(eh),
               e_median=e_d.median(), h_median=h_d.median())

    eh2 = eh.copy()
    eh2['y'] = (eh2['succ_canon'] == 'elective').astype(int)
    lr2 = LogisticRegression(solver='lbfgs', max_iter=1000)
    lr2.fit(eh2[['D0']].values, eh2['y'].values)
    res['OR_D0'] = float(np.exp(lr2.coef_[0][0]))

    Xs = scaler.transform(ws[['L', 'D0', 'L_D0']].values)
    res['accuracy'] = lr.score(Xs, ws['succ_canon'].values)

    print()
    print('=== ATTRACTION BASIN STATISTICS ===')
    print()
    print(f"Working set: n = {res['n_total']} hand-coded systems")
    print()
    print(f"Chi\u00b2 (succession type \u00d7 L regime):")
    print(f"  \u03c7\u00b2 = {chi2:.2f}  df = {dof}  p = {p_chi:.4f} {sig(p_chi)}")
    print()
    print(f"Mann-Whitney D\u2080 (elective vs hereditary, high-L \u2265 0.60):")
    print(f"  elective   n = {len(e_d)}  median D\u2080 = {e_d.median():.2f}")
    print(f"  hereditary n = {len(h_d)}  median D\u2080 = {h_d.median():.2f}")
    print(f"  U = {u:.0f}  p = {p_mw:.4f} {sig(p_mw)}"
          f"  rank-biserial r = {rb:.3f}")
    print()
    print(f"Binary logistic OR for D\u2080 (high-L, elective vs hereditary):")
    print(f"  OR = {res['OR_D0']:.2f}")
    print()
    print(f"Multinomial accuracy (L + D\u2080 + L\u00d7D\u2080): {res['accuracy']:.3f}")
    print()
    return res


def print_model_diagnostics(ws, lr, scaler):
    y      = ws['succ_canon'].values
    Xs     = scaler.transform(ws[['L', 'D0', 'L_D0']].values)
    y_pred = lr.predict(Xs)
    print('=== MULTINOMIAL MODEL DIAGNOSTICS ===')
    print()
    print('Confusion matrix (rows = actual, columns = predicted):')
    print(pd.DataFrame(
        confusion_matrix(y, y_pred, labels=lr.classes_),
        index=lr.classes_, columns=lr.classes_
    ))
    print()
    print('Classification report:')
    print(classification_report(y, y_pred, labels=lr.classes_,
                                 zero_division=0))
    print()
    print('Predicted probabilities at key L \u00d7 D\u2080 grid points:')
    print(f'{"D\u2080":>6}  {"L":>5}  ' +
          '  '.join(f'{c:>12}' for c in lr.classes_))
    for d_val in [0.10, 0.50, 0.85]:
        for l_val in [0.30, 0.60, 0.80]:
            X_pt = np.array([[l_val, d_val, l_val * d_val]])
            probs = lr.predict_proba(scaler.transform(X_pt))[0]
            print(f'{d_val:>6.2f}  {l_val:>5.2f}  ' +
                  '  '.join(f'{p:>12.3f}' for p in probs))
        print()


def print_descriptive_table(ws):
    print('=== SUCCESSION TYPE DESCRIPTIVE STATISTICS ===')
    print()
    desc = ws.groupby('succ_canon').agg(
        n=('L', 'count'),
        L_mean=('L', 'mean'), L_std=('L', 'std'),
        D0_mean=('D0', 'mean'), D0_std=('D0', 'std'),
        EDR_mean=('EDR', 'mean'),
    ).round(3)
    print(desc.to_string())
    print()
    print('Cross-tab: succession type \u00d7 L regime (low < 0.60 / high \u2265 0.60):')
    print(pd.crosstab(ws['succ_canon'],
                      (ws['L'] >= 0.60).map(
                          {True: 'L \u2265 0.60', False: 'L < 0.60'})))
    print()
    print('Cross-tab: succession type \u00d7 D\u2080 regime (low < 0.50 / high \u2265 0.50):')
    print(pd.crosstab(ws['succ_canon'],
                      (ws['D0'] >= 0.50).map(
                          {True: 'D\u2080 \u2265 0.50', False: 'D\u2080 < 0.50'})))
    print()


# ── Phase 1 figure ─────────────────────────────────────────────────────────────

def make_figure(ws, lr, scaler, classes, res, visuals_dir=OUTPUT_DIR):
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
        for t in ['hereditary', 'appointment', 'elective',
                  'consensus', 'rotation']
    ]

    fig = plt.figure(figsize=(15, 10))
    gs  = GridSpec(3, 3, figure=fig, height_ratios=[1, 1, 0.08],
                   hspace=0.44, wspace=0.38)

    # A: L x D0 scatter
    ax_a = fig.add_subplot(gs[0, 0])
    for t in TYPE_ORDER:
        sub = ws[ws['succ_canon'] == t]
        ax_a.scatter(sub['L'], sub['D0'], c=COLOURS[t], marker=MARKERS[t],
                     s=50, alpha=0.85, edgecolors='white', lw=0.5, zorder=4)
    anno = {
        'Norwegian Sovereign Wealth Democracy': ('Norway',    (0.72, 0.94)),
        'Gadaa System':                          ('Gadaa',     (0.30, 0.92)),
        'Roman Republic':                        ('Rome Rep.', (0.50, 0.58)),
        'Confucian Bureaucracy':                 ('Confucian', (0.80, 0.08)),
    }
    for _, row in ws.iterrows():
        if row['System'] in anno:
            lbl, txt_xy = anno[row['System']]
            ax_a.annotate(lbl, xy=(row['L'], row['D0']), xytext=txt_xy,
                          fontsize=6.5, color='#333333',
                          arrowprops=dict(arrowstyle='->',
                                          color='#aaaaaa', lw=0.7))
    ax_a.axvline(0.60, color='#aaaaaa', lw=0.8, ls=':', zorder=1)
    ax_a.axhline(0.50, color='#aaaaaa', lw=0.8, ls=':', zorder=1)
    ax_a.text(0.613, 0.03, 'L = 0.60', fontsize=6, color='#999999')
    ax_a.text(0.07, 0.515, 'D\u2080 = 0.50', fontsize=6, color='#999999')
    ax_a.set_xlabel('L \u2014 surplus legibility', fontsize=9)
    ax_a.set_ylabel('D\u2080 \u2014 disobedience freedom', fontsize=9)
    ax_a.set_title(f'A.  Succession types in L \u00d7 D\u2080 space'
                   f'  (n = {res["n_total"]})',
                   fontsize=9, fontweight='bold', loc='left', pad=6)

    # B: predicted probability curves
    ax_b = fig.add_subplot(gs[0, 1])
    for probs, ls, al, lw in [(p_lo, '--', 0.70, 1.2),
                               (p_hi, '-',  0.95, 2.0)]:
        for i, cls in enumerate(classes):
            if cls not in COLOURS:
                continue
            ax_b.plot(L_sw, probs[:, i], color=COLOURS[cls],
                      ls=ls, lw=lw, alpha=al)
    ax_b.annotate('\u2191 D\u2080 suppresses\nhereditary',
                  xy=(0.75, 0.07), xytext=(0.53, 0.17), fontsize=6.5,
                  color=COLOURS['hereditary'],
                  arrowprops=dict(arrowstyle='->',
                                  color=COLOURS['hereditary'], lw=0.8))
    ax_b.annotate('\u2191 D\u2080 boosts\nelective',
                  xy=(0.75, 0.66), xytext=(0.51, 0.56), fontsize=6.5,
                  color=COLOURS['elective'],
                  arrowprops=dict(arrowstyle='->',
                                  color=COLOURS['elective'], lw=0.8))
    ax_b.axvline(0.60, color='#cccccc', lw=0.8, ls=':', zorder=1)
    ax_b.set_xlabel('L \u2014 surplus legibility', fontsize=9)
    ax_b.set_ylabel('Predicted probability', fontsize=9)
    ax_b.set_ylim(-0.02, 1.02)
    ax_b.set_title('B.  P(type | L, D\u2080) \u2014 multinomial logistic\n'
                   '(solid = D\u2080 0.85  \u2014  dashed = D\u2080 0.10)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)

    # C: moderator shading
    ax_c = fig.add_subplot(gs[0, 2])
    for i, cls in enumerate(classes):
        if cls not in COLOURS:
            continue
        ax_c.fill_between(L_sw, p_lo[:, i], p_hi[:, i],
                          alpha=0.13, color=COLOURS[cls])
        ax_c.plot(L_sw, p_hi[:, i], color=COLOURS[cls], lw=2.0, ls='-')
        ax_c.plot(L_sw, p_lo[:, i], color=COLOURS[cls], lw=1.0, ls='--')
    ax_c.axvline(0.60, color='#cccccc', lw=0.8, ls=':', zorder=1)
    ax_c.set_xlabel('L \u2014 surplus legibility', fontsize=9)
    ax_c.set_ylabel('Predicted probability', fontsize=9)
    ax_c.set_ylim(-0.02, 1.02)
    ax_c.set_title('C.  D\u2080 moderator effect  (shading = gap)\n'
                   '(solid = D\u2080 0.85  \u2014  dashed = D\u2080 0.10)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)

    # D: boxplot D0 by type x L regime
    ax_d = fig.add_subplot(gs[1, 0])
    lo_l = ws[ws['L'] < 0.60]
    hi_l = ws[ws['L'] >= 0.60]
    x_pos = np.arange(len(TYPE_ORDER))
    for regime, fc, offset in [(lo_l, '#5dade2', -0.18),
                                (hi_l, '#e74c3c', +0.18)]:
        vals = [regime[regime['succ_canon'] == t]['D0'].values
                for t in TYPE_ORDER]
        ax_d.boxplot(vals, positions=x_pos + offset, widths=0.30,
                     patch_artist=True,
                     boxprops=dict(facecolor=fc, alpha=0.65),
                     medianprops=dict(color='#111111', lw=1.8),
                     whiskerprops=dict(lw=0.8), capprops=dict(lw=0.8),
                     flierprops=dict(marker='.', ms=4, alpha=0.5, color=fc))
    ax_d.set_xticks(x_pos)
    ax_d.set_xticklabels(TYPE_ORDER, fontsize=8, rotation=18, ha='right')
    ax_d.set_ylabel('D\u2080 \u2014 disobedience freedom', fontsize=9)
    ax_d.set_ylim(-0.05, 1.05)
    ax_d.set_title('D.  D\u2080 by type \u00d7 L regime\n'
                   '(blue = L < 0.60  \u2014  red = L \u2265 0.60)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    ax_d.legend(
        handles=[mpatches.Patch(facecolor='#5dade2', alpha=0.65,
                                 label='L < 0.60'),
                 mpatches.Patch(facecolor='#e74c3c', alpha=0.65,
                                 label='L \u2265 0.60')],
        fontsize=7.5, loc='upper right', frameon=True, framealpha=0.92)

    # E: attraction basin scatter (high-L only)
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
            ax_e.annotate(key_labels[row['System']],
                          (row['D0'], row['L']),
                          xytext=(5, 3), textcoords='offset points',
                          fontsize=6, color='#333333')
    ax_e.axvline(0.50, color='#aaaaaa', lw=0.8, ls=':', zorder=1)
    ax_e.set_xlabel('D\u2080 \u2014 disobedience freedom', fontsize=9)
    ax_e.set_ylabel('L \u2014 surplus legibility', fontsize=9)
    ax_e.set_title('E.  Attraction basins (L \u2265 0.60)\n'
                   'D\u2080 discriminates elective from hereditary',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    ax_e.text(0.97, 0.97,
              f'Elective vs hereditary (D\u2080)\n'
              f'Mann-Whitney p = {res["p_mw"]:.4f} {sig(res["p_mw"])}\n'
              f'rank-biserial r = {res["rb"]:.3f}',
              transform=ax_e.transAxes, fontsize=7.5, va='top', ha='right',
              bbox=dict(boxstyle='round,pad=0.4', fc='white',
                        ec='#cccccc', alpha=0.92))

    # F: statistics table
    ax_f = fig.add_subplot(gs[1, 2])
    ax_f.axis('off')
    rows = [
        ['\u03c7\u00b2: succession \u00d7 L',
         f'{res["chi2"]:.2f} (df={res["dof"]})',
         f'{res["p_chi2"]:.4f} {sig(res["p_chi2"])}',
         str(res['n_total'])],
        ['MW: D\u2080 elective vs\nhereditary (L \u2265 0.60)',
         f'U = {res["mw_U"]:.0f}  r = {res["rb"]:.3f}',
         f'{res["p_mw"]:.4f} {sig(res["p_mw"])}',
         str(res['n_hil'])],
        ['Binary logit OR(D\u2080)\nelective vs hereditary',
         f'OR = {res["OR_D0"]:.2f}', '\u2014', str(res['n_hil'])],
        ['Multinomial accuracy\n(L + D\u2080 + L\u00d7D\u2080)',
         f'{res["accuracy"]:.3f}', '\u2014', str(res['n_total'])],
    ]
    tbl = ax_f.table(cellText=rows,
                     colLabels=['Test', 'Result', 'p', 'n'],
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

    # Shared legend strip
    ax_leg = fig.add_subplot(gs[2, :])
    ax_leg.axis('off')
    ax_leg.legend(handles=type_handles, loc='center', ncol=5,
                  fontsize=8.5, frameon=True, framealpha=0.95,
                  edgecolor='#cccccc',
                  title='Succession type  '
                        '(colour + marker consistent across all panels)',
                  title_fontsize=8, handlelength=1.2,
                  handletextpad=0.5, columnspacing=1.5)

    fig.suptitle(
        'Succession mechanism attraction basins: '
        'surplus legibility and disobedience freedom as predictors\n'
        'Static model \u2014 hand-coded isonomia systems '
        f'(confidence 2\u20133), n = {res["n_total"]}',
        fontsize=11, fontweight='bold', y=0.995)

    os.makedirs(visuals_dir, exist_ok=True)
    out_path = os.path.join(visuals_dir, 'attraction_basins.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


# ── Phase 2: transition parsing ────────────────────────────────────────────────

def parse_succession_changes(df):
    """Parse succession_changes field into flat transition DataFrame.

    Returns DataFrame with columns:
        system, year, from_succ, to_succ, L_from, D0_from,
        trigger, region, changed
    """
    trig_kw = {
        'P_to_S': 'P_to_S', 'external_shock': 'external_shock',
        'elite_reform': 'elite_reform', 'collapse': 'collapse',
        'reconsolidation': 'reconsolidation', 'internal': 'internal',
    }
    rows = []
    for _, sys_row in df[df['succession_changes'].fillna('') != ''].iterrows():
        for entry in sys_row['succession_changes'].split(' | '):
            entry = entry.strip()
            if not entry:
                continue
            try:
                arrow_part, rest = entry.split(' (', 1)
                from_succ, to_succ = arrow_part.split('->')
                year_str, note    = rest.split('): ', 1)
                trig = next(
                    (v for k, v in trig_kw.items() if k in note.lower()),
                    'other')
                rows.append({
                    'system':    sys_row['System'],
                    'year':      int(year_str.strip()),
                    'from_succ': from_succ.strip(),
                    'to_succ':   to_succ.strip(),
                    'L':         sys_row.get('surplus_legibility',
                                              float('nan')),
                    'D0':        sys_row.get('disobedience_freedom',
                                              float('nan')),
                    'trigger':   trig,
                    'region':    sys_row.get('Region', ''),
                    'changed':   int(from_succ.strip() != to_succ.strip()),
                })
            except Exception as exc:
                print(f"  Parse warning: {entry[:60]} \u2014 {exc}")
    tdf = pd.DataFrame(rows)
    print(f"  Parsed {len(tdf)} transition events across "
          f"{tdf['system'].nunique()} systems "
          f"({tdf['changed'].sum()} type-changing, "
          f"{(tdf['changed'] == 0).sum()} same-type L/D shifts)")
    return tdf


def save_transition_csv(tdf, data_dir):
    out = os.path.join(data_dir, 'transition_data.csv')
    tdf.to_csv(out, index=False)
    print(f"  Transition data saved to {out}")


def run_transition_statistics(tdf):
    changed = tdf[tdf['changed'] == 1]
    print()
    print('=== PHASE 2 TRANSITION STATISTICS ===')
    print()
    print(f'Total events: {len(tdf)}  '
          f'(type-changing: {len(changed)}, '
          f'same-type: {len(tdf) - len(changed)})')
    print()
    print('Transition matrix (row = from, col = to; type-changing only):')
    print(pd.crosstab(changed['from_succ'], changed['to_succ']))
    print()
    print('Row-normalised transition probabilities:')
    print(pd.crosstab(changed['from_succ'], changed['to_succ'],
                      normalize='index').round(2))
    print()
    print('Trigger \u2192 destination:')
    print(pd.crosstab(changed['trigger'], changed['to_succ']))
    print()

    hi_ch = changed[changed['L'] >= 0.60]
    lo_ch = changed[changed['L'] < 0.60]
    print(f'High-L transitions (L\u226510.60, n={len(hi_ch)}):')
    if len(hi_ch) >= 3:
        print(pd.crosstab(hi_ch['from_succ'], hi_ch['to_succ'],
                          normalize='index').round(2))
    print()
    print(f'Low-L transitions (L<0.60, n={len(lo_ch)}):')
    if len(lo_ch) >= 3:
        print(pd.crosstab(lo_ch['from_succ'], lo_ch['to_succ'],
                          normalize='index').round(2))
    print()

    types = ['hereditary', 'appointment', 'elective', 'consensus', 'rotation']
    n_cells  = len(types) * (len(types) - 1)
    n_filled = sum(1 for f in types for t in types
                   if f != t and len(changed[(changed['from_succ'] == f) &
                                              (changed['to_succ']   == t)]) > 0)
    print(f'Markov matrix coverage: {n_filled}/{n_cells} cells '
          f'({100 * n_filled / n_cells:.0f}%)')

    elite    = changed[changed['trigger'] == 'elite_reform']
    internal = changed[changed['trigger'] == 'internal']
    print(f'Elite reform \u2192 hereditary: '
          f'{(elite["to_succ"] == "hereditary").sum()}/{len(elite)}')
    print(f'Internal \u2192 hereditary: '
          f'{(internal["to_succ"] == "hereditary").sum()}/{len(internal)}')


# ── Phase 2 figure ─────────────────────────────────────────────────────────────

def make_transition_figure(tdf, visuals_dir=OUTPUT_DIR):
    """Six-panel Phase 2 transition analysis figure."""
    plt.rcParams.update({
        'font.family': 'serif', 'font.size': 9,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.grid': True, 'grid.alpha': 0.22, 'grid.linewidth': 0.5,
    })

    changed  = tdf[tdf['changed'] == 1].copy()
    types_m  = ['hereditary', 'appointment', 'elective', 'consensus', 'rotation']
    n_t      = len(types_m)
    d_order  = ['elective', 'appointment', 'hereditary', 'rotation']

    def count_matrix(df_sub, types):
        m = np.zeros((len(types), len(types)))
        for _, row in df_sub.iterrows():
            f, t = row['from_succ'], row['to_succ']
            if f in types and t in types:
                m[types.index(f), types.index(t)] += 1
        return m

    matrix   = count_matrix(changed, types_m)
    rs       = matrix.sum(1, keepdims=True)
    m_norm   = np.where(rs > 0, matrix / rs, 0)

    hi_ch = changed[changed['L'] >= 0.60]
    lo_ch = changed[changed['L'] < 0.60]
    m_hi  = count_matrix(hi_ch, types_m)
    m_lo  = count_matrix(lo_ch, types_m)
    rs_hi = m_hi.sum(1, keepdims=True)
    rs_lo = m_lo.sum(1, keepdims=True)
    m_hi_n = np.where(rs_hi > 0, m_hi / rs_hi, np.nan)
    m_lo_n = np.where(rs_lo > 0, m_lo / rs_lo, np.nan)
    diff   = np.where(np.isnan(m_hi_n) | np.isnan(m_lo_n), np.nan,
                      m_hi_n - m_lo_n)

    trig_matrix = np.zeros((len(TRIG_ORDER), len(d_order)))
    for _, row in changed.iterrows():
        tk, d = row['trigger'], row['to_succ']
        if tk in TRIG_ORDER and d in d_order:
            trig_matrix[TRIG_ORDER.index(tk), d_order.index(d)] += 1
    rs_t      = trig_matrix.sum(1, keepdims=True)
    trig_norm = np.where(rs_t > 0, trig_matrix / rs_t, 0)

    type_handles = [
        mlines.Line2D([], [], color=COLOURS[t], marker=MARKERS[t],
                      markerfacecolor=COLOURS[t], markeredgecolor='white',
                      markeredgewidth=0.5, markersize=7,
                      linestyle='none', label=t)
        for t in ['hereditary', 'appointment', 'elective', 'consensus']
    ]

    fig = plt.figure(figsize=(16, 9))
    gs  = GridSpec(2, 3, figure=fig, hspace=0.46, wspace=0.40)

    def heatmap(ax, data, cmap, vmin, vmax, xticks, yticks,
                xlabel, ylabel, title, cbar_label, annotate_fn=None):
        im = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto')
        ax.set_xticks(range(len(xticks)))
        ax.set_yticks(range(len(yticks)))
        ax.set_xticklabels(xticks, fontsize=8, rotation=20, ha='right')
        ax.set_yticklabels(yticks, fontsize=8)
        ax.set_xlabel(xlabel, fontsize=9)
        ax.set_ylabel(ylabel, fontsize=9)
        ax.set_title(title, fontsize=9, fontweight='bold', loc='left', pad=6)
        plt.colorbar(im, ax=ax, shrink=0.85, label=cbar_label)
        if annotate_fn:
            annotate_fn(ax, data)

    def ann_matrix(ax, data):
        nr, nc = data.shape
        for i in range(nr):
            for j in range(nc):
                if i != j and not np.isnan(data[i, j]):
                    n_val = int(matrix[i, j]) if data is m_norm else ''
                    txt   = (f'{data[i,j]:.2f}\n(n={n_val})'
                             if data is m_norm
                             else f'{data[i,j]:+.2f}')
                    c = 'white' if abs(data[i, j]) > 0.55 else '#333333'
                    ax.text(j, i, txt, ha='center', va='center',
                            fontsize=7, color=c)

    heatmap(fig.add_subplot(gs[0, 0]), m_norm, 'Blues', 0, 1,
            types_m, types_m, 'To', 'From',
            'A.  Empirical transition matrix\n'
            '(row-normalised; diagonal = no-change)',
            'Transition probability', ann_matrix)

    ax_b = fig.add_subplot(gs[0, 1])
    heatmap(ax_b, diff, 'RdBu_r', -0.6, 0.6,
            types_m, types_m, 'To', 'From',
            'B.  L-conditional shift: high-L minus low-L\n'
            '(blue=more likely at high L, red=less likely)',
            '\u0394 probability (high-L \u2212 low-L)',
            lambda ax, d: [
                ax.text(j, i, f'{d[i,j]:+.2f}', ha='center', va='center',
                        fontsize=7.5)
                for i in range(n_t) for j in range(n_t)
                if i != j and not np.isnan(d[i, j])
            ])

    def ann_trig(ax, data):
        for i in range(len(TRIG_ORDER)):
            for j in range(len(d_order)):
                nv = int(trig_matrix[i, j])
                if nv > 0:
                    c = 'white' if data[i, j] > 0.6 else '#333333'
                    ax.text(j, i, f'{data[i,j]:.2f}\n(n={nv})',
                            ha='center', va='center', fontsize=7, color=c)

    heatmap(fig.add_subplot(gs[0, 2]), trig_norm, 'Greens', 0, 1,
            d_order, TRIG_ORDER, 'Destination type', '',
            'C.  Trigger \u2192 destination type\n(row-normalised)',
            'P(destination | trigger)', ann_trig)

    # D: D0 at transition by destination
    ax_d = fig.add_subplot(gs[1, 0])
    for i, dest in enumerate(d_order):
        d0v = changed[changed['to_succ'] == dest]['D0'].values
        jit = np.random.default_rng(42).normal(0, 0.06, len(d0v))
        ax_d.scatter(d0v, np.full(len(d0v), i) + jit,
                     c=COLOURS.get(dest, '#888'), marker=MARKERS.get(dest, 'o'),
                     s=55, alpha=0.80, edgecolors='white', lw=0.5, zorder=4)
        if len(d0v):
            ax_d.plot([np.median(d0v)] * 2, [i - 0.28, i + 0.28],
                      color='#333333', lw=2.5, zorder=5)
    rome = changed[(changed['system'] == 'Roman Republic') &
                   (changed['to_succ'] == 'hereditary')]
    for _, rr in rome.iterrows():
        ax_d.annotate('Rome\n(P\u2192S)',
                      xy=(rr['D0'], d_order.index('hereditary')),
                      xytext=(rr['D0'] + 0.06,
                               d_order.index('hereditary') + 0.35),
                      fontsize=6.5, color='#c0392b',
                      arrowprops=dict(arrowstyle='->',
                                      color='#c0392b', lw=0.8))
    ax_d.set_yticks(range(len(d_order)))
    ax_d.set_yticklabels(d_order, fontsize=8)
    ax_d.set_xlabel('D\u2080 at time of transition', fontsize=9)
    ax_d.set_title('D.  D\u2080 at transition by destination\n(bar = median)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    ax_d.axvline(0.50, color='#aaaaaa', lw=0.8, ls=':')

    # E: L at transition by trigger
    ax_e = fig.add_subplot(gs[1, 1])
    for i, trig in enumerate(TRIG_ORDER):
        sub = changed[changed['trigger'] == trig]
        if len(sub) == 0:
            continue
        jit = np.random.default_rng(42 + i).normal(0, 0.07, len(sub))
        ax_e.scatter(sub['L'].values, np.full(len(sub), i) + jit,
                     c=[COLOURS.get(t, '#888') for t in sub['to_succ']],
                     s=55, alpha=0.80, edgecolors='white', lw=0.5, zorder=4)
        ax_e.plot([sub['L'].median()] * 2, [i - 0.28, i + 0.28],
                  color='#333333', lw=2.5, zorder=5)
    ax_e.axvline(0.60, color='#aaaaaa', lw=0.8, ls=':')
    ax_e.set_yticks(range(len(TRIG_ORDER)))
    ax_e.set_yticklabels(TRIG_ORDER, fontsize=8)
    ax_e.set_xlabel('L at time of transition', fontsize=9)
    ax_e.set_title('E.  L at transition by trigger type\n'
                   '(dot colour = destination; bar = median)',
                   fontsize=9, fontweight='bold', loc='left', pad=6)
    ax_e.legend(handles=type_handles, fontsize=7, title='Dest.',
                title_fontsize=7, loc='lower right',
                frameon=True, framealpha=0.92, ncol=2)

    # F: summary table
    ax_f = fig.add_subplot(gs[1, 2])
    ax_f.axis('off')
    n_cells  = n_t * (n_t - 1)
    n_filled = sum(1 for i in range(n_t) for j in range(n_t)
                   if i != j and matrix[i, j] > 0)
    elite    = changed[changed['trigger'] == 'elite_reform']
    internal = changed[changed['trigger'] == 'internal']
    rows_f = [
        ['Total transition events', str(len(tdf)),
         f'n_systems={tdf["system"].nunique()}'],
        ['Type-changing', str(len(changed)), '\u2014'],
        ['Same-type (L/D shift)', str(len(tdf) - len(changed)), '\u2014'],
        ['Markov cells filled',
         f'{n_filled}/{n_cells}',
         f'{100 * n_filled / n_cells:.0f}%'],
        ['Elite reform \u2192 hereditary',
         f'{(elite["to_succ"] == "hereditary").sum()}/{len(elite)}', '0%'],
        ['Internal \u2192 hereditary',
         f'{(internal["to_succ"] == "hereditary").sum()}/{len(internal)}',
         '100%'],
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
        'Succession model Phase 2: empirical transition matrix '
        'and trigger analysis\n'
        f'{len(tdf)} transition events across '
        f'{tdf["system"].nunique()} systems  '
        f'({tdf["changed"].sum()} type-changing, '
        f'{(tdf["changed"] == 0).sum()} same-type)',
        fontsize=11, fontweight='bold', y=0.998)

    os.makedirs(visuals_dir, exist_ok=True)
    out = os.path.join(visuals_dir, 'transition_matrix.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Succession attraction basin analysis — Phase 1 + Phase 2',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Phase 1 (default): static cross-sectional model.
  Writes: data/succession_working_set.csv

Phase 2 (--phase2): empirical transition matrix.
  Writes: data/transition_data.csv

Figures: only generated with --figure.
  Writes: visuals/attraction_basins.png  (Phase 1)
          visuals/transition_matrix.png  (Phase 2, requires --phase2)

All paths resolved relative to the governance_extended.csv location.
""")
    parser.add_argument('--data', default=DATA_PATH,
                        help='Path to governance_extended.csv')
    parser.add_argument('--phase2', action='store_true',
                        help='Run Phase 2 transition analysis')
    parser.add_argument('--figure', action='store_true',
                        help='Generate figures')
    args = parser.parse_args()

    data_dir    = os.path.dirname(os.path.abspath(args.data))
    visuals_dir = os.path.join(os.path.dirname(data_dir), 'visuals')
    os.makedirs(data_dir,    exist_ok=True)
    os.makedirs(visuals_dir, exist_ok=True)

    ws = load_data(args.data)
    print(f"Loaded working set: {len(ws)} hand-coded systems")
    print(ws['succ_canon'].value_counts().to_string())
    print()

    print_descriptive_table(ws)
    lr, scaler, classes = fit_model(ws)
    res = run_statistics(ws, lr, scaler)
    print_model_diagnostics(ws, lr, scaler)

    if args.figure:
        make_figure(ws, lr, scaler, classes, res, visuals_dir)

    ws.to_csv(os.path.join(data_dir, 'succession_working_set.csv'), index=False)
    print(f"Working dataset saved to {data_dir}/succession_working_set.csv")

    if args.phase2:
        print()
        print("=== PHASE 2: TRANSITION ANALYSIS ===")
        df_full = pd.read_csv(args.data)
        df_full.columns = df_full.columns.str.strip()
        for col in ['surplus_legibility', 'disobedience_freedom']:
            df_full[col] = pd.to_numeric(df_full[col], errors='coerce')
        tdf = parse_succession_changes(df_full)
        save_transition_csv(tdf, data_dir)
        run_transition_statistics(tdf)
        if args.figure:
            make_transition_figure(tdf, visuals_dir)
    else:
        print()
        print("Run with --phase2 for transition matrix analysis.")


if __name__ == '__main__':
    main()
