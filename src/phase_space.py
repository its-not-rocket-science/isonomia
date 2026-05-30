"""
phase_space.py — SAP/EDR visualisations for the isonomia dataset.

Usage:
    python src/phase_space.py

Outputs (in visuals/):
    sap_ternary.png        SAP phase space coloured by EDR composite
    edr_distribution.png   EDR histogram with resilience threshold
    edr_sap_scatter.png    EDR vs SAP scatter coloured by collapse mode
    timeline_edr.png       EDR over time (hand-coded subset)
"""
import csv, math, os, warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

DATA_PATH  = os.path.join(os.path.dirname(__file__), '..', 'data', 'governance_extended.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'visuals')
THRESHOLD  = 0.45

def load_data(path=DATA_PATH):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            try:
                r['_S']   = float(r['sovereignty_index'])
                r['_A']   = float(r['admin_index'])
                r['_P']   = float(r['competitive_politics_index'])
                r['_E']   = float(r['exit_freedom'])
                r['_D']   = float(r['disobedience_freedom'])
                r['_R']   = float(r['arrangement_freedom'])
                r['_EDR'] = (r['_E'] + r['_D'] + r['_R']) / 3
                r['_SAP'] = (r['_S'] + r['_A'] + r['_P']) / 3
                r['_conf'] = int(r.get('coding_confidence', 1) or 1)
                rows.append(r)
            except (ValueError, TypeError):
                continue
    return rows

def ternary_coords(S, A, P):
    total = S + A + P
    if total == 0: return 0.5, 0.33
    s, a, p = S/total, A/total, P/total
    x = 0.5 * (2*a + p)
    y = (math.sqrt(3) / 2) * p
    return x, y

def plot_sap_ternary(rows):
    fig, ax = plt.subplots(figsize=(11, 9))
    tri_x = [0, 1, 0.5, 0]
    tri_y = [0, 0, math.sqrt(3)/2, 0]
    ax.plot(tri_x, tri_y, 'k-', lw=1.5)
    ax.text(-0.06, -0.03, 'Sovereignty (S)', fontsize=11, ha='left')
    ax.text(1.02,  -0.03, 'Administration (A)', fontsize=11, ha='right')
    ax.text(0.5, math.sqrt(3)/2+0.03, 'Competitive Politics (P)', fontsize=11, ha='center')
    for frac in [0.25, 0.5, 0.75]:
        for pts in [
            [ternary_coords(frac,1-frac,0), ternary_coords(frac,0,1-frac)],
            [ternary_coords(0,frac,1-frac), ternary_coords(1-frac,frac,0)],
            [ternary_coords(0,1-frac,frac), ternary_coords(1-frac,0,frac)],
        ]:
            ax.plot([pts[0][0],pts[1][0]], [pts[0][1],pts[1][1]], color='grey', lw=0.4, alpha=0.5)
    cmap = cm.RdYlGn
    for r in rows:
        x, y = ternary_coords(r['_S'], r['_A'], r['_P'])
        alpha = 0.9 if r['_conf'] >= 2 else 0.35
        size  = 55  if r['_conf'] >= 2 else 20
        ax.scatter(x, y, c=[cmap(r['_EDR'])], s=size, alpha=alpha,
                   edgecolors='white' if r['_conf'] >= 2 else 'none', linewidths=0.5, zorder=3)
    label_cases = {
        'San Xaro Networks','Çatalhöyük','Early Uruk','Late Uruk / Early Dynastic',
        'Iroquois Confederacy / Haudenosaunee','Confucian Bureaucracy',
        'Balinese Negara','Zomia Highland Communities','Tokugawa Shogunate',
        'Gadaa System','Teotihuacan','Tang Dynasty',
    }
    for r in rows:
        if r['System'] in label_cases and r['_conf'] >= 2:
            x, y = ternary_coords(r['_S'], r['_A'], r['_P'])
            ax.annotate(r['System'], (x, y), fontsize=6.5, xytext=(4,4),
                        textcoords='offset points', alpha=0.85)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0,1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label('EDR Composite', fontsize=10)
    cbar.ax.axhline(THRESHOLD, color='black', lw=1.5, linestyle='--')
    ax.set_xlim(-0.1,1.1); ax.set_ylim(-0.08,1.0)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('SAP Phase Space — coloured by EDR resilience composite\n(large = hand-coded; small = auto-coded)', fontsize=12)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR,'sap_ternary.png'), dpi=150, bbox_inches='tight')
    plt.close(); print("Saved: sap_ternary.png")

def plot_edr_distribution(rows):
    fig, ax = plt.subplots(figsize=(10,5))
    all_edr  = [r['_EDR'] for r in rows]
    hand_edr = [r['_EDR'] for r in rows if r['_conf'] >= 2]
    ax.hist(all_edr,  bins=20, alpha=0.45, color='steelblue', label=f'All (n={len(all_edr)})')
    ax.hist(hand_edr, bins=20, alpha=0.75, color='darkblue',  label=f'Hand-coded (n={len(hand_edr)})')
    ax.axvline(THRESHOLD, color='crimson', lw=2, linestyle='--', label=f'θ = {THRESHOLD}')
    ax.axvline(sum(all_edr)/len(all_edr), color='steelblue', lw=1.5, linestyle=':',
               label=f'Mean = {sum(all_edr)/len(all_edr):.2f}')
    ax.set_xlabel('EDR Composite', fontsize=11)
    ax.set_ylabel('Count', fontsize=11)
    ax.set_title('Distribution of EDR Resilience Composite', fontsize=12)
    ax.legend(fontsize=9)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR,'edr_distribution.png'), dpi=150)
    plt.close(); print("Saved: edr_distribution.png")

COLLAPSE_COLOURS = {
    'conquest':'#e41a1c','colonial disruption':'#ff7f00','colonial absorption':'#fdbf6f',
    'fragmentation':'#984ea3','abandonment':'#a65628','revolution':'#377eb8',
    'climate':'#4daf4a','transition':'#999999','ongoing':'#1a9641','unknown':'#cccccc',
}

def plot_edr_sap_scatter(rows):
    fig, ax = plt.subplots(figsize=(10,8))
    plotted = set()
    for r in rows:
        mode  = r.get('collapse_mode','unknown') or 'unknown'
        color = COLLAPSE_COLOURS.get(mode,'#cccccc')
        alpha = 0.85 if r['_conf'] >= 2 else 0.3
        size  = 55   if r['_conf'] >= 2 else 18
        label = mode if mode not in plotted else None
        ax.scatter(r['_SAP'], r['_EDR'], c=color, s=size, alpha=alpha,
                   label=label, edgecolors='white' if r['_conf'] >= 2 else 'none', linewidths=0.4)
        plotted.add(mode)
    ax.axhline(THRESHOLD, color='crimson', lw=1.5, linestyle='--', alpha=0.7)
    ax.text(0.02, THRESHOLD+0.01, f'θ = {THRESHOLD}', color='crimson', fontsize=9)
    hc = [(r['_SAP'], r['_EDR']) for r in rows if r['_conf'] >= 2]
    if len(hc) > 2:
        xs, ys = [x for x,_ in hc], [y for _,y in hc]
        m, b = np.polyfit(xs, ys, 1)
        xr = np.linspace(0, 1, 100)
        ax.plot(xr, m*xr+b, 'k--', lw=1, alpha=0.5, label='Trend (hand-coded)')
    ax.set_xlabel('SAP Composite', fontsize=11); ax.set_ylabel('EDR Composite', fontsize=11)
    ax.set_title('EDR vs SAP — coloured by collapse mode', fontsize=12)
    ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.legend(fontsize=8, loc='upper right', ncol=2)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR,'edr_sap_scatter.png'), dpi=150)
    plt.close(); print("Saved: edr_sap_scatter.png")

def plot_timeline_edr(rows):
    hand = [r for r in rows if r['_conf'] >= 2]
    timed = []
    for r in hand:
        s = str(r.get('Start','')).strip().lstrip('-')
        if s.isdigit():
            timed.append((int(r['Start']), r['_EDR'], r['System']))
    if not timed: print("Skipping timeline"); return
    timed.sort()
    xs, ys = [t[0] for t in timed], [t[1] for t in timed]
    fig, ax = plt.subplots(figsize=(14,5))
    cmap = cm.RdYlGn
    ax.scatter(xs, ys, c=[cmap(y) for y in ys], s=45, zorder=3, edgecolors='white', lw=0.4)
    ax.axhline(THRESHOLD, color='crimson', lw=1.5, linestyle='--', alpha=0.7)
    highlight = {'Çatalhöyük','Early Uruk','Late Uruk / Early Dynastic','Roman Republic',
                 'Tang Dynasty','Iroquois Confederacy / Haudenosaunee','Tokugawa Shogunate'}
    for start, edr, sys in timed:
        if sys in highlight:
            ax.annotate(sys, (start,edr), fontsize=6.5, xytext=(0,8),
                        textcoords='offset points', ha='center', alpha=0.85)
    ax.set_xlabel('Start date (CE/BCE)', fontsize=11)
    ax.set_ylabel('EDR Composite', fontsize=11)
    ax.set_title('EDR resilience over time — hand-coded systems', fontsize=12)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR,'timeline_edr.png'), dpi=150)
    plt.close(); print("Saved: timeline_edr.png")

if __name__ == '__main__':
    if not HAS_MPL:
        print("Install: pip install matplotlib numpy"); raise SystemExit(1)
    rows = load_data()
    print(f"Loaded {len(rows)} rows")
    plot_sap_ternary(rows)
    plot_edr_distribution(rows)
    plot_edr_sap_scatter(rows)
    plot_timeline_edr(rows)
    print("Done — outputs in visuals/")
