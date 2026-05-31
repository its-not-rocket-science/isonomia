"""
paper02_figures.py
Generates the three figures for Paper 2 (The Lock-In Sequence).

Figure 1: Lock-in sequence timeline — L, I, A, EDR across the Natufian-to-Uruk
          case studies, showing the sequence of variable changes over 10,000 years.

Figure 2: Counter-case scatter — L vs EDR for all hand-coded systems,
          counter-cases labelled, showing high-L/high-EDR outliers.

Figure 3: D as moderator — L vs EDR coloured by D value, showing that
          high D systems maintain high EDR under high L.

Usage:
    python src/paper02_figures.py

Outputs saved to visuals/lock_in_*.png
"""

import csv, os, warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import numpy as np
from scipy import stats

DATA_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data', 'governance_extended.csv')
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'visuals')
THETA       = 0.45
FONT        = {'family': 'serif'}
plt.rcParams.update({'font.family': 'serif', 'font.size': 10})

# ── Load data ─────────────────────────────────────────────────────────────────

def load():
    rows = []
    with open(DATA_PATH, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try:
                r['_E']   = float(r['exit_freedom'])
                r['_D']   = float(r['disobedience_freedom'])
                r['_R']   = float(r['arrangement_freedom'])
                r['_S']   = float(r['sovereignty_index'])
                r['_A']   = float(r['admin_index'])
                r['_P']   = float(r['competitive_politics_index'])
                r['_L']   = float(r['surplus_legibility'])
                r['_I']   = float(r['info_infrastructure'])
                r['_EDR'] = (r['_E'] + r['_D'] + r['_R']) / 3
                r['_conf']= int(r.get('coding_confidence', 1) or 1)
                r['_start']= int(r['Start']) if r.get('Start','').lstrip('-').isdigit() else None
                rows.append(r)
            except (ValueError, TypeError):
                continue
    return rows


# ── Figure 1: Lock-in sequence timeline ──────────────────────────────────────

# Ordered chronologically through the primary sequence + key cases
SEQUENCE = [
    ('Natufian Communities',            -12500),
    ('Göbekli Tepe (ritual complex)',   -9600),
    ('Pre-Pottery Neolithic A (PPNA)',  -9500),
    ('Pre-Pottery Neolithic B (PPNB)',  -8700),
    ('Çatalhöyük',                      -7500),
    ('Ubaid Culture',                   -6500),
    ('Early Uruk',                      -4000),
    ('Late Uruk / Early Dynastic',      -3100),
    ('Egyptian Old Kingdom',            -2686),
]

SHORT_NAMES = {
    'Natufian Communities':             'Natufian',
    'Göbekli Tepe (ritual complex)':    'Göbekli Tepe',
    'Pre-Pottery Neolithic A (PPNA)':   'PPNA',
    'Pre-Pottery Neolithic B (PPNB)':   'PPNB',
    'Çatalhöyük':                       'Çatalhöyük',
    'Ubaid Culture':                    'Ubaid',
    'Early Uruk':                       'Early Uruk',
    'Late Uruk / Early Dynastic':       'Late Uruk',
    'Egyptian Old Kingdom':             'Old Kingdom',
}


def plot_sequence_timeline(rows):
    lookup = {r['System']: r for r in rows}

    fig, axes = plt.subplots(2, 1, figsize=(13, 9), sharex=True)
    fig.subplots_adjust(hspace=0.08)

    # X positions: use start dates
    x_dates = [date for _, date in SEQUENCE]
    x_pos   = np.arange(len(SEQUENCE))
    labels  = [SHORT_NAMES[name] for name, _ in SEQUENCE]

    # Extract values in sequence order
    vals = {}
    for dim in ['_L', '_I', '_A', '_EDR', '_E', '_D', '_R']:
        vals[dim] = []
        for name, _ in SEQUENCE:
            r = lookup.get(name)
            vals[dim].append(r[dim] if r else None)

    # Top panel: L, I, A (drivers)
    ax1 = axes[0]
    colours = {'_L': '#e6a817', '_I': '#d95f02', '_A': '#7570b3'}
    labels_dim = {'_L': 'L (surplus legibility)', '_I': 'I (information infrastructure)',
                  '_A': 'A (administration)'}

    for dim, col in colours.items():
        y = vals[dim]
        y_clean = [v if v is not None else np.nan for v in y]
        ax1.plot(x_pos, y_clean, 'o-', color=col, lw=2, markersize=7,
                 label=labels_dim[dim])

    ax1.axhline(THETA, color='crimson', lw=1.5, linestyle='--', alpha=0.7)
    ax1.set_ylabel('Variable value (0–1)', fontsize=11)
    ax1.set_title('The lock-in sequence: Natufian to Egyptian Old Kingdom\n'
                  'Rising L and I drive rising A; EDR follows inversely',
                  fontsize=11)
    ax1.legend(fontsize=9, loc='upper left')
    ax1.set_ylim(0, 1.05)
    ax1.set_xlim(-0.4, len(SEQUENCE) - 0.6)

    # Annotate the θ crossing
    # EDR crosses θ between Early Uruk (index 6) and Late Uruk (index 7)
    ax1.annotate('', xy=(6.5, THETA+0.02), xytext=(6.5, THETA+0.12),
                 arrowprops=dict(arrowstyle='->', color='crimson', lw=1.5))
    ax1.text(6.5, THETA+0.14, 'EDR crosses θ', ha='center', fontsize=8,
             color='crimson')

    # Bottom panel: EDR and its components
    ax2 = axes[1]
    edr_colours = {'_E': '#1b9e77', '_D': '#2166ac', '_R': '#4dac26', '_EDR': '#000000'}
    edr_labels  = {'_E': 'E (exit)', '_D': 'D (disobedience)',
                   '_R': 'R (arrangement)', '_EDR': 'EDR composite'}
    edr_styles  = {'_E': '--', '_D': '--', '_R': '--', '_EDR': '-'}
    edr_widths  = {'_E': 1.2, '_D': 1.2, '_R': 1.2, '_EDR': 2.5}

    for dim in ['_E', '_D', '_R', '_EDR']:
        y = [v if v is not None else np.nan for v in vals[dim]]
        ax2.plot(x_pos, y, edr_styles[dim], color=edr_colours[dim],
                 lw=edr_widths[dim], markersize=6 if dim == '_EDR' else 0,
                 marker='o' if dim == '_EDR' else None,
                 label=edr_labels[dim], alpha=0.9)

    ax2.axhline(THETA, color='crimson', lw=1.5, linestyle='--',
                label=f'θ = {THETA}', alpha=0.8)
    ax2.fill_between([-0.4, len(SEQUENCE)-0.6], 0, THETA,
                     alpha=0.05, color='crimson')
    ax2.text(0.1, THETA/2, 'Fragile regime', color='crimson',
             fontsize=8, va='center', alpha=0.8)

    ax2.set_ylabel('Variable value (0–1)', fontsize=11)
    ax2.set_xlabel('')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([f'{l}\n({d:,})' for l, (_, d) in
                          zip(labels, SEQUENCE)],
                         fontsize=8.5, rotation=20, ha='right')
    ax2.legend(fontsize=9, loc='upper right')
    ax2.set_ylim(0, 1.05)
    ax2.set_xlim(-0.4, len(SEQUENCE) - 0.6)

    # Add stage annotations
    stages = [(0.5, 2.5, 'Stage 1\nL rises'), (2.5, 4.5, 'Stage 2\nI rises'),
              (4.5, 6.5, 'Stage 3\nA rises'), (6.5, 8.5, 'Stages 4-6\nEDR collapses')]
    for i, (x0, x1, label) in enumerate(stages):
        col = '#cccccc' if i % 2 == 0 else '#eeeeee'
        for ax in axes:
            ax.axvspan(x0, min(x1, len(SEQUENCE)-0.6), alpha=0.15, color=col, zorder=0)
        axes[1].text((x0+min(x1,len(SEQUENCE)-0.6))/2, 0.02, label,
                     ha='center', fontsize=7, color='#666666', style='italic',
                     transform=axes[1].transData)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'lock_in_sequence.png'), dpi=150,
                bbox_inches='tight')
    plt.close()
    print("Saved: lock_in_sequence.png")


AVOIDANCE_LABELS = {
    'Zomia Highland Communities': 'Zomia',
}

# ── Figure 2: Counter-case scatter ───────────────────────────────────────────

COUNTER_CASES = {
    'Phoenician Merchant Oligarchies',
    'Venetian Republic',
    'Hanseatic League',
    'Dutch Republic States-General',
    'British Parliamentary System',
    'Swiss Consensus Democracy',
    'Norwegian Sovereign Wealth Democracy',
}

COUNTER_LABELS = {
    'Phoenician Merchant Oligarchies': 'Phoenician',
    'Venetian Republic':               'Venice',
    'Hanseatic League':                'Hanseatic',
    'Dutch Republic States-General':   'Dutch Republic',
    'British Parliamentary System':    'Britain',
    'Swiss Consensus Democracy':       'Switzerland',
    'Norwegian Sovereign Wealth Democracy': 'Norway',
}

# Lock-in sequence cases for annotation
LOCKIN_LABELS = {
    'Early Uruk':              'Early Uruk',
    'Late Uruk / Early Dynastic': 'Late Uruk',
    'Qin Legalism':            'Qin',
    'Inca Empire (Tawantinsuyu)': 'Inca',
    'Çatalhöyük':              'Çatalhöyük',
}


def plot_counter_scatter(rows):
    hc = [r for r in rows if r['_conf'] >= 2]

    fig, ax = plt.subplots(figsize=(11, 8))

    # All hand-coded systems as background
    for r in hc:
        if r['System'] not in COUNTER_CASES and r['System'] not in LOCKIN_LABELS:
            ax.scatter(r['_L'], r['_EDR'], c='#cccccc', s=25, alpha=0.5,
                       edgecolors='none', zorder=2)

    # Lock-in sequence cases
    for r in hc:
        if r['System'] in LOCKIN_LABELS:
            ax.scatter(r['_L'], r['_EDR'], c='#d62728', s=60, alpha=0.9,
                       edgecolors='white', linewidths=0.5, zorder=4)
            ax.annotate(LOCKIN_LABELS[r['System']], (r['_L'], r['_EDR']),
                        xytext=(6, 6), textcoords='offset points',
                        fontsize=8, color='#d62728')

    # Deliberate illegibility cases (Zomia)
    for r in hc:
        if r['System'] in AVOIDANCE_LABELS:
            ax.scatter(r['_L'], r['_EDR'], c='#2166ac', s=80, alpha=0.95,
                       edgecolors='white', linewidths=0.7, zorder=5,
                       marker='^')
            ax.annotate(AVOIDANCE_LABELS[r['System']], (r['_L'], r['_EDR']),
                        xytext=(6, 4), textcoords='offset points',
                        fontsize=8.5, color='#2166ac', fontweight='bold')

    # Counter-cases
    for r in hc:
        if r['System'] in COUNTER_CASES:
            ax.scatter(r['_L'], r['_EDR'], c='#1b9e77', s=80, alpha=0.95,
                       edgecolors='white', linewidths=0.7, zorder=5,
                       marker='D')
            ax.annotate(COUNTER_LABELS[r['System']], (r['_L'], r['_EDR']),
                        xytext=(6, 4), textcoords='offset points',
                        fontsize=8.5, color='#1b9e77', fontweight='bold')

    # Regression line for all hand-coded
    xs = np.array([r['_L'] for r in hc])
    ys = np.array([r['_EDR'] for r in hc])
    m, b = np.polyfit(xs, ys, 1)
    xr = np.linspace(0, 1, 100)
    r_val, p_val = stats.pearsonr(xs, ys)
    ax.plot(xr, m*xr+b, 'k--', lw=1.2, alpha=0.4,
            label=f'Regression (all hc, r={r_val:.2f})')

    # Threshold lines
    ax.axhline(THETA, color='crimson', lw=1.5, linestyle='--', alpha=0.7)
    ax.axvline(0.60, color='#888888', lw=1, linestyle=':', alpha=0.5)
    ax.text(0.01, THETA + 0.015, f'θ = {THETA}', color='crimson', fontsize=9)
    ax.text(0.61, 0.02, 'L ≥ 0.60\n(high legibility)', color='#888888',
            fontsize=8, style='italic')

    # Shade counter-case zone
    ax.fill_between([0.60, 1.0], THETA, 1.0, alpha=0.06, color='#1b9e77',
                    label='High L, high EDR zone')
    ax.text(0.78, 0.92, 'Counter-case\nzone', color='#1b9e77',
            fontsize=8.5, ha='center', style='italic', alpha=0.8)

    # Legend
    handles = [
        mpatches.Patch(color='#1b9e77', label='Counter-cases (L ≥ 0.60, EDR ≥ θ)'),
        mpatches.Patch(color='#d62728', label='Lock-in sequence cases'),
        plt.scatter([], [], marker='^', color='#2166ac', s=80,
                    label='Deliberate illegibility'),
        mpatches.Patch(color='#cccccc', label='Other hand-coded systems'),
    ]
    ax.legend(handles=handles, fontsize=9, loc='upper right')

    ax.set_xlabel('Surplus Legibility (L)', fontsize=11)
    ax.set_ylabel('EDR Composite (resilience)', fontsize=11)
    ax.set_title('Counter-cases: high surplus legibility with EDR above threshold\n'
                 'Counter-cases (diamonds) cluster above the regression line',
                 fontsize=11)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'lock_in_counter_cases.png'), dpi=150)
    plt.close()
    print("Saved: lock_in_counter_cases.png")


# ── Figure 3: D as moderator ──────────────────────────────────────────────────

def plot_d_moderator(rows):
    hc = [r for r in rows if r['_conf'] >= 2]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left panel: all hand-coded, coloured by D
    ax = axes[0]
    cmap = cm.RdYlGn
    for r in hc:
        ax.scatter(r['_L'], r['_EDR'], c=[cmap(r['_D'])], s=45, alpha=0.85,
                   edgecolors='white', linewidths=0.4, zorder=3)

    # Annotate counter-cases and lock-in cases
    for r in hc:
        if r['System'] in COUNTER_LABELS:
            ax.annotate(COUNTER_LABELS[r['System']], (r['_L'], r['_EDR']),
                        xytext=(5, 4), textcoords='offset points',
                        fontsize=7.5, color='darkgreen', fontweight='bold')
        if r['System'] in LOCKIN_LABELS:
            ax.annotate(LOCKIN_LABELS[r['System']], (r['_L'], r['_EDR']),
                        xytext=(5, -10), textcoords='offset points',
                        fontsize=7.5, color='darkred')
        if r['System'] in AVOIDANCE_LABELS:
            ax.scatter(r['_L'], r['_EDR'], c='#2166ac', s=55, alpha=0.9,
                       edgecolors='white', linewidths=0.5, zorder=5, marker='^')
            ax.annotate(AVOIDANCE_LABELS[r['System']], (r['_L'], r['_EDR']),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=7.5, color='#2166ac', fontweight='bold')

    ax.axhline(THETA, color='crimson', lw=1.5, linestyle='--', alpha=0.7)
    ax.axvline(0.60, color='#888888', lw=1, linestyle=':', alpha=0.4)
    ax.text(0.01, THETA+0.015, f'θ = {THETA}', color='crimson', fontsize=9)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label('D (disobedience freedom)', fontsize=9)
    cbar.ax.axhline(0.55, color='black', lw=1.5, linestyle='--')
    cbar.ax.text(2.6, 0.55, ' D ≥ 0.55\n (counter-cases)', va='center', fontsize=7.5)

    ax.set_xlabel('Surplus Legibility (L)', fontsize=11)
    ax.set_ylabel('EDR Composite', fontsize=11)
    ax.set_title('D as moderator — high D systems\nmaintain EDR under high L', fontsize=11)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    # Right panel: split high-L (≥0.60) by D quartile
    ax2 = axes[1]
    high_l = [r for r in hc if r['_L'] >= 0.60]

    # D quartile boundaries
    d_vals = sorted(r['_D'] for r in high_l)
    q25 = np.percentile(d_vals, 25)
    q50 = np.percentile(d_vals, 50)
    q75 = np.percentile(d_vals, 75)

    quartile_colours = ['#d73027', '#fc8d59', '#91cf60', '#1a9641']
    quartile_labels  = [f'D ≤ {q25:.2f}\n(Q1, n=%d)',
                        f'{q25:.2f} < D ≤ {q50:.2f}\n(Q2, n=%d)',
                        f'{q50:.2f} < D ≤ {q75:.2f}\n(Q3, n=%d)',
                        f'D > {q75:.2f}\n(Q4, n=%d)']

    def d_quartile(d):
        if d <= q25: return 0
        if d <= q50: return 1
        if d <= q75: return 2
        return 3

    quartile_edr = [[], [], [], []]
    for r in high_l:
        quartile_edr[d_quartile(r['_D'])].append(r['_EDR'])

    positions = [1, 2, 3, 4]
    bp = ax2.boxplot(quartile_edr, positions=positions, patch_artist=True,
                     medianprops={'color':'black', 'lw':2},
                     whiskerprops={'lw':1.2}, capprops={'lw':1.2})

    for patch, col in zip(bp['boxes'], quartile_colours):
        patch.set_facecolor(col); patch.set_alpha(0.7)

    ax2.axhline(THETA, color='crimson', lw=1.5, linestyle='--', alpha=0.7,
                label=f'θ = {THETA}')
    ax2.fill_between([0.5, 4.5], 0, THETA, alpha=0.05, color='crimson')

    xlabels = [l % len(q) for l, q in zip(quartile_labels, quartile_edr)]
    ax2.set_xticks(positions)
    ax2.set_xticklabels(xlabels, fontsize=8.5)
    ax2.set_xlabel('D (disobedience freedom) quartile\namong high-L systems (L ≥ 0.60)',
                   fontsize=10)
    ax2.set_ylabel('EDR Composite', fontsize=11)
    ax2.set_title(f'EDR by D quartile (high-L systems only, n={len(high_l)})\n'
                  'Higher D consistently predicts higher EDR under legibility pressure',
                  fontsize=11)
    ax2.legend(fontsize=9)
    ax2.set_ylim(0, 1)

    # Add mean EDR for each quartile
    for pos, q_edr in zip(positions, quartile_edr):
        if q_edr:
            ax2.text(pos, max(q_edr)+0.03, f'μ={np.mean(q_edr):.2f}',
                     ha='center', fontsize=8.5, fontweight='bold')

    # Significance test between Q1 and Q4
    if quartile_edr[0] and quartile_edr[3]:
        u, p = stats.mannwhitneyu(quartile_edr[3], quartile_edr[0], alternative='greater')
        sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'ns'
        ax2.text(2.5, 0.96, f'Q1 vs Q4: p={p:.3f} {sig}', ha='center',
                 fontsize=9, color='#333333',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

    fig.suptitle('Disobedience freedom (D) as moderator of the lock-in sequence\n'
                 'Node colour = D value; high D protects EDR under high L',
                 fontsize=12, fontweight='bold')
    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(os.path.join(OUTPUT_DIR, 'lock_in_d_moderator.png'), dpi=150,
                bbox_inches='tight')
    plt.close()
    print("Saved: lock_in_d_moderator.png")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    rows = load()
    print(f"Loaded {len(rows)} rows, "
          f"{sum(1 for r in rows if r['_conf']>=2)} hand-coded")
    plot_sequence_timeline(rows)
    plot_counter_scatter(rows)
    plot_d_moderator(rows)
    print("Done. Outputs in visuals/lock_in_*.png")
