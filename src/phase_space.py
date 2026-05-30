"""
phase_space.py — SAP/EDR visualisations for the isonomia dataset.

Usage:
    python src/phase_space.py

Outputs (in visuals/):
    sap_ternary.png        SAP phase space coloured by EDR composite
    edr_distribution.png   EDR histogram with resilience threshold
    edr_sap_scatter.png    EDR vs SAP scatter coloured by collapse mode
    timeline_edr.png       EDR over time (hand-coded subset) with trend
"""
import csv, math, os, warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import matplotlib.patches as mpatches
    import numpy as np
    from scipy.ndimage import uniform_filter1d
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

DATA_PATH  = os.path.join(os.path.dirname(__file__), '..', 'data', 'governance_extended.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'visuals')
THRESHOLD  = 0.45

# ── Collapse mode grouping ────────────────────────────────────────────────────
COLLAPSE_GROUPS = {
    'External force':   (['conquest','invasion','conquest/disaster','conquest/absorption',
                          'conquest/invasion','collapse/conquest','regicide/conquest'], '#e41a1c'),
    'Internal collapse':(['revolution','autocracy','fragmentation','fragmentation/FIP',
                          'fragmentation/displacement','dissolution','defeat',
                          'expulsion/death','decline','decline/transition',
                          'abandonment/collapse','collapse/fire','collapse/invasion',
                          'invasion/transition','abandonment/fragmentation'], '#984ea3'),
    'Colonial':         (['colonial disruption','colonial absorption','colonial imposition',
                          'colonial enclosure','colonial conquest','colonial destruction',
                          'colonial pressure'], '#ff7f00'),
    'Climate/ecology':  (['climate','abandonment/drought','abandonment/climate'], '#4daf4a'),
    'Abandonment':      (['abandonment','dispersal/transition'], '#a65628'),
    'Transition':       (['transition','reform','forced opening/reform',
                          'monarchical centralisation','annexation','absorption'], '#377eb8'),
    'Ongoing':          (['ongoing'], '#1a9641'),
    'Unknown':          (['unknown'], '#cccccc'),
}

def collapse_group(mode):
    m = (mode or 'unknown').strip().lower()
    for group, (modes, color) in COLLAPSE_GROUPS.items():
        if m in modes:
            return group, color
    return 'Unknown', '#cccccc'

# ── Data loading ──────────────────────────────────────────────────────────────
def load_data(path=DATA_PATH):
    rows = []
    with open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try:
                r['_S']    = float(r['sovereignty_index'])
                r['_A']    = float(r['admin_index'])
                r['_P']    = float(r['competitive_politics_index'])
                r['_E']    = float(r['exit_freedom'])
                r['_D']    = float(r['disobedience_freedom'])
                r['_R']    = float(r['arrangement_freedom'])
                r['_EDR']  = (r['_E'] + r['_D'] + r['_R']) / 3
                r['_SAP']  = (r['_S'] + r['_A'] + r['_P']) / 3
                r['_conf'] = int(r.get('coding_confidence', 1) or 1)
                rows.append(r)
            except (ValueError, TypeError):
                continue
    return rows

# ── SAP ternary ───────────────────────────────────────────────────────────────
def ternary_coords(S, A, P):
    total = S + A + P
    if total == 0: return 0.5, 0.33
    s, a, p = S/total, A/total, P/total
    x = 0.5 * (2*a + p)
    y = (math.sqrt(3) / 2) * p
    return x, y

# Label positions: (system_name, x_offset, y_offset)
LABEL_NUDGES = {
    'San Xaro Networks':                        ( 6,  4),
    'Balinese Negara':                          ( 6,  4),
    'Çatalhöyük':                               (-60, 6),
    'Zomia Highland Communities':               ( 6,  4),
    'Gadaa System':                             (-62, 4),
    'Iroquois Confederacy / Haudenosaunee':     ( 6, -8),
    'Confucian Bureaucracy':                    ( 6,  4),
    'Tokugawa Shogunate':                       (-68, 4),
    'Early Uruk':                               ( 6,  4),
    'Late Uruk / Early Dynastic':               ( 6, -8),
    'Tang Dynasty':                             ( 6,  4),
    'Teotihuacan':                              ( 6, -8),
}

def plot_sap_ternary(rows):
    fig, ax = plt.subplots(figsize=(12, 10))
    h = math.sqrt(3) / 2

    # Triangle
    ax.plot([0,1,0.5,0], [0,0,h,0], 'k-', lw=1.8)

    # Grid lines
    for frac in [0.25, 0.5, 0.75]:
        for pts in [
            [ternary_coords(frac,1-frac,0), ternary_coords(frac,0,1-frac)],
            [ternary_coords(0,frac,1-frac), ternary_coords(1-frac,frac,0)],
            [ternary_coords(0,1-frac,frac), ternary_coords(1-frac,0,frac)],
        ]:
            ax.plot([pts[0][0],pts[1][0]], [pts[0][1],pts[1][1]],
                    color='grey', lw=0.4, alpha=0.45, linestyle='--')

    # Axis labels — outside corners
    ax.text(-0.08, -0.04, 'Sovereignty (S)', fontsize=12, ha='left',  fontweight='bold')
    ax.text( 1.04, -0.04, 'Administration (A)', fontsize=12, ha='right', fontweight='bold')
    ax.text( 0.5,  h+0.04, 'Competitive\nPolitics (P)', fontsize=12, ha='center', fontweight='bold')

    # Fraction labels on edges
    for frac in [0.25, 0.5, 0.75]:
        x1,y1 = ternary_coords(0, 1-frac, frac)
        ax.text(x1-0.03, y1, f'{int(frac*100)}', fontsize=7, color='grey', ha='right')
        x2,y2 = ternary_coords(1-frac, frac, 0)
        ax.text(x2+0.02, y2-0.01, f'{int(frac*100)}', fontsize=7, color='grey')

    cmap = cm.RdYlGn

    # Auto-coded (background layer)
    for r in rows:
        if r['_conf'] >= 2: continue
        x, y = ternary_coords(r['_S'], r['_A'], r['_P'])
        ax.scatter(x, y, c=[cmap(r['_EDR'])], s=18, alpha=0.3,
                   edgecolors='none', zorder=2)

    # Hand-coded (foreground)
    for r in rows:
        if r['_conf'] < 2: continue
        x, y = ternary_coords(r['_S'], r['_A'], r['_P'])
        ax.scatter(x, y, c=[cmap(r['_EDR'])], s=70, alpha=0.92,
                   edgecolors='white', linewidths=0.7, zorder=4)

    # Labels with nudges
    for r in rows:
        if r['_conf'] < 2: continue
        sys = r['System']
        if sys not in LABEL_NUDGES: continue
        x, y = ternary_coords(r['_S'], r['_A'], r['_P'])
        dx, dy = LABEL_NUDGES[sys]
        ax.annotate(sys, (x, y), fontsize=7,
                    xytext=(dx, dy), textcoords='offset points',
                    alpha=0.9, zorder=5)

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0,1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.55, pad=0.02, aspect=25)
    cbar.set_label('EDR Composite (resilience →)', fontsize=10)
    cbar.ax.axhline(THRESHOLD, color='black', lw=1.5, linestyle='--')
    cbar.ax.text(2.6, THRESHOLD, f' θ={THRESHOLD}', va='center', fontsize=8)

    # Legend for dot sizes
    ax.scatter([],[], s=70, c='grey', alpha=0.9, label='Hand-coded (confidence ≥2)')
    ax.scatter([],[], s=18, c='grey', alpha=0.35, label='Auto-coded (confidence 1)')
    ax.legend(fontsize=9, loc='lower center', framealpha=0.7)

    ax.set_xlim(-0.12, 1.12); ax.set_ylim(-0.10, 1.02)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('SAP Phase Space — coloured by EDR resilience composite', fontsize=13, pad=16)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'sap_ternary.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: sap_ternary.png")


# ── EDR distribution ──────────────────────────────────────────────────────────
def plot_edr_distribution(rows):
    fig, ax = plt.subplots(figsize=(10, 5))
    all_edr  = [r['_EDR'] for r in rows]
    hand_edr = [r['_EDR'] for r in rows if r['_conf'] >= 2]

    ax.hist(all_edr,  bins=20, alpha=0.45, color='steelblue',
            label=f'All systems (n={len(all_edr)})')
    ax.hist(hand_edr, bins=20, alpha=0.80, color='#1a3a6b',
            label=f'Hand-coded (n={len(hand_edr)})')
    ax.axvline(THRESHOLD, color='crimson', lw=2, linestyle='--',
               label=f'θ = {THRESHOLD} (resilience threshold)')
    ax.axvline(sum(all_edr)/len(all_edr), color='steelblue', lw=1.5, linestyle=':',
               label=f'Mean (all) = {sum(all_edr)/len(all_edr):.2f}')

    fragile = sum(1 for e in all_edr if e < THRESHOLD)
    ymax = ax.get_ylim()[1]
    ax.fill_betweenx([0, ymax], 0, THRESHOLD, alpha=0.04, color='crimson')
    ax.text(THRESHOLD/2, ymax*0.88, f'Fragile regime\n({fragile} systems, {100*fragile//len(all_edr)}%)',
            ha='center', color='crimson', fontsize=9)
    ax.text((THRESHOLD+1)/2, ymax*0.72, f'Resilient regime\n({len(all_edr)-fragile} systems)',
            ha='center', color='#2d7a2d', fontsize=9)

    ax.set_xlabel('EDR Composite', fontsize=11)
    ax.set_ylabel('Count', fontsize=11)
    ax.set_title(f'Distribution of EDR Resilience Composite\nacross {len(all_edr)} governance systems', fontsize=12)
    ax.legend(fontsize=9)
    ax.set_xlim(0, 1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'edr_distribution.png'), dpi=150)
    plt.close()
    print("Saved: edr_distribution.png")


# ── EDR vs SAP scatter ────────────────────────────────────────────────────────
def plot_edr_sap_scatter(rows):
    fig, ax = plt.subplots(figsize=(11, 9))

    # Plot auto-coded first (background)
    for r in rows:
        if r['_conf'] >= 2: continue
        _, color = collapse_group(r.get('collapse_mode',''))
        ax.scatter(r['_SAP'], r['_EDR'], c=color, s=18, alpha=0.25,
                   edgecolors='none', zorder=2)

    # Plot hand-coded on top
    plotted_groups = {}
    for r in rows:
        if r['_conf'] < 2: continue
        group, color = collapse_group(r.get('collapse_mode',''))
        ax.scatter(r['_SAP'], r['_EDR'], c=color, s=65, alpha=0.88,
                   edgecolors='white', linewidths=0.5, zorder=4)
        plotted_groups[group] = color

    # Threshold line
    ax.axhline(THRESHOLD, color='crimson', lw=1.5, linestyle='--', alpha=0.8)
    ax.text(0.01, THRESHOLD + 0.015, f'θ = {THRESHOLD}', color='crimson', fontsize=9)

    # Fragile zone shading
    ax.fill_between([0,1], 0, THRESHOLD, alpha=0.04, color='crimson')

    # Trend line (hand-coded only)
    hc = [(r['_SAP'], r['_EDR']) for r in rows if r['_conf'] >= 2]
    xs, ys = [x for x,_ in hc], [y for _,y in hc]
    m, b = np.polyfit(xs, ys, 1)
    xr = np.linspace(0, 1, 200)
    ax.plot(xr, m*xr+b, 'k--', lw=1.2, alpha=0.45,
            label=f'Trend (hand-coded, r=−0.84)')

    # Legend — grouped collapse modes only
    handles = [mpatches.Patch(color=c, label=g)
               for g, (_, c) in COLLAPSE_GROUPS.items()
               if g in plotted_groups or g == 'Unknown']
    handles.append(plt.Line2D([0],[0], color='k', linestyle='--', lw=1.2,
                               alpha=0.45, label='Trend (hand-coded)'))
    ax.legend(handles=handles, fontsize=9, loc='upper right',
              title='Collapse mode', title_fontsize=9, framealpha=0.85)

    # Size legend
    ax.scatter([],[], s=65, c='grey', alpha=0.88, label='Hand-coded')
    ax.scatter([],[], s=18, c='grey', alpha=0.3,  label='Auto-coded')
    leg2 = ax.legend(loc='lower left', fontsize=9, framealpha=0.7)
    ax.add_artist(handles and plt.legend(handles=handles, fontsize=9, loc='upper right',
                  title='Collapse mode', title_fontsize=9, framealpha=0.85) or leg2)

    ax.set_xlabel('SAP Composite (domination)', fontsize=11)
    ax.set_ylabel('EDR Composite (resilience)', fontsize=11)
    ax.set_title('EDR resilience vs SAP domination\ncoloured by collapse mode (grouped)',
                 fontsize=12)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'edr_sap_scatter.png'), dpi=150)
    plt.close()
    print("Saved: edr_sap_scatter.png")


# ── Timeline ──────────────────────────────────────────────────────────────────
TIMELINE_LABELS = {
    'Çatalhöyük':                           ( 0,  10),
    'Early Uruk':                           ( 0,  10),
    'Late Uruk / Early Dynastic':           ( 0, -14),
    'Roman Republic':                       ( 0,  10),
    'Tang Dynasty':                         ( 0, -14),
    'Iroquois Confederacy / Haudenosaunee': ( 0,  10),
    'Tokugawa Shogunate':                   ( 0, -14),
    'Swiss Cantonal Democracy':             ( 0,  10),
    'Natufian Communities':                 ( 0,  10),
    'Zomia Highland Communities':           ( 0, -14),
}

def plot_timeline_edr(rows):
    hand = [r for r in rows if r['_conf'] >= 2]
    timed = []
    for r in hand:
        s = str(r.get('Start','')).strip()
        try:
            timed.append((int(s), r['_EDR'], r['System']))
        except ValueError:
            continue
    if not timed:
        print("Skipping timeline"); return
    timed.sort()

    xs = np.array([t[0] for t in timed])
    ys = np.array([t[1] for t in timed])

    fig, ax = plt.subplots(figsize=(15, 6))
    cmap = cm.RdYlGn

    # Threshold band
    ax.axhline(THRESHOLD, color='crimson', lw=1.5, linestyle='--', alpha=0.7, zorder=2)
    ax.fill_between([xs.min()-500, xs.max()+500], 0, THRESHOLD,
                    alpha=0.04, color='crimson')
    ax.text(xs.min()-200, THRESHOLD+0.02, f'θ = {THRESHOLD}',
            color='crimson', fontsize=9)

    # Scatter
    ax.scatter(xs, ys, c=[cmap(y) for y in ys], s=55, zorder=4,
               edgecolors='white', linewidths=0.5)

    # Loess-style trend: sort by x, apply rolling mean
    window = max(5, len(xs)//8)
    # bin into regular intervals for smooth line
    x_bins = np.linspace(xs.min(), xs.max(), 40)
    y_bins = []
    for xb in x_bins:
        # weighted average of nearby points
        weights = np.exp(-0.5*((xs - xb)/((xs.max()-xs.min())*0.08))**2)
        if weights.sum() > 0:
            y_bins.append(np.average(ys, weights=weights))
        else:
            y_bins.append(np.nan)
    y_bins = np.array(y_bins)
    valid = ~np.isnan(y_bins)
    ax.plot(x_bins[valid], y_bins[valid], color='#333333', lw=2,
            alpha=0.5, linestyle='-', label='Weighted trend (bandwidth = 8% range)')

    # Labels
    for start, edr, sys in timed:
        if sys not in TIMELINE_LABELS: continue
        dx, dy = TIMELINE_LABELS[sys]
        ax.annotate(sys, (start, edr), fontsize=7.5,
                    xytext=(dx, dy), textcoords='offset points',
                    ha='center', alpha=0.9,
                    arrowprops=dict(arrowstyle='-', color='grey',
                                   lw=0.6, alpha=0.5) if dy != 0 else None)

    # Epoch shading
    epochs = [
        (-13000, -3000, '#e8f4e8', 'Pre-state'),
        (-3000,   500,  '#fff3e0', 'Early states'),
        (500,    1500,  '#e8eaf6', 'Medieval'),
        (1500,   2100,  '#fce4ec', 'Early modern–present'),
    ]
    for x0, x1, color, label in epochs:
        if x0 > xs.max() or x1 < xs.min(): continue
        ax.axvspan(max(x0, xs.min()-200), min(x1, xs.max()+200),
                   alpha=0.12, color=color, zorder=0)
        mid = (max(x0, xs.min()) + min(x1, xs.max())) / 2
        ax.text(mid, 0.97, label, ha='center', va='top',
                fontsize=8, color='grey', style='italic', transform=ax.get_xaxis_transform())

    ax.set_xlabel('Start date (CE/BCE)', fontsize=11)
    ax.set_ylabel('EDR Composite', fontsize=11)
    ax.set_title('EDR resilience over time — hand-coded systems\n'
                 'EDR declines at state emergence (~4000 BCE) but high-EDR societies persist at every period',
                 fontsize=12)
    ax.set_ylim(0, 1.02)
    ax.legend(fontsize=9, loc='lower right')

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0,1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.6, pad=0.01, aspect=25)
    cbar.set_label('EDR Composite', fontsize=9)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'timeline_edr.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: timeline_edr.png")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if not HAS_MPL:
        print("Install: pip install matplotlib numpy scipy")
        raise SystemExit(1)
    rows = load_data()
    print(f"Loaded {len(rows)} rows")
    plot_sap_ternary(rows)
    plot_edr_distribution(rows)
    plot_edr_sap_scatter(rows)
    plot_timeline_edr(rows)
    print("Done — outputs in visuals/")
