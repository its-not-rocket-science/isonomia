"""
generate_network_figure.py
==========================
Generates Figure 2 for Paper 4: the historically-sourced governance influence
network and contagion decay comparison.

Output: visuals/network_influence_sourced.png

Two-panel figure:
  Panel A — Node-link diagram of the 56-edge historically-sourced network.
             Nodes sized by degree, coloured by EDR regime.
             Edges coloured by type (comparator/contrast/parallel).
  Panel B — Contagion decay comparison: sourced network vs full dataset.
             Both reproduce sign reversal at d=4.

Key results (56 edges, 30 nodes):
  r_d1 = +0.665 (p < 0.001)
  r_d2 = +0.391 (p = 0.033)
  r_d3 = +0.144 (p = 0.447, ns)
  r_d4 = -0.649 (p < 0.001)
  Mean |ΔEDR| contrast:   0.408  (n = 20)
  Mean |ΔEDR| comparator: 0.182  (n = 31)
  Mann-Whitney p (contrast > comparator): 0.009

Usage
-----
    python src/generate_network_figure.py
    python src/generate_network_figure.py --figure visuals/my_output.png
    python src/generate_network_figure.py --dpi 300
"""

import os
import argparse
import warnings
import numpy as np
import pandas as pd
from collections import defaultdict
from scipy import stats

warnings.filterwarnings('ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.join(SCRIPT_DIR, '..')
DATA_DIR   = os.path.join(ROOT, 'data')
VIS_DIR    = os.path.join(ROOT, 'visuals')

GOV_FILE    = os.path.join(DATA_DIR, 'governance_extended.csv')
SOURCED_FILE = os.path.join(DATA_DIR, 'network_influence_sourced.csv')

# ── Colour palette ─────────────────────────────────────────────────────────────
AMBER = '#e8a020'
GREEN = '#6fcf97'
RED   = '#c0392b'
SLATE = '#4a6580'
BG    = '#1a1f2e'
MID   = '#9ca8b8'
LABEL = '#d0ccc0'

# Short display names for node labels
SHORT = {
    'Zhou Dynasty Mandate of Heaven':       'Zhou',
    'Achaemenid Persian Empire':            'Achaemenid',
    'Roman Republic':                       'Roman Rep.',
    'Athenian Democracy':                   'Athens',
    'Mauryan Empire':                       'Mauryan',
    'Confucian Bureaucracy':                'Confucian',
    'Tang Dynasty':                         'Tang',
    'Venetian Republic':                    'Venice',
    'Abbasid Caliphate':                    'Abbasid',
    'Carolingian Empire':                   'Carolingian',
    'Icelandic Commonwealth':               'Iceland',
    'Song Dynasty':                         'Song',
    'Swiss Cantonal Democracy':             'Swiss',
    'Ottoman Empire':                       'Ottoman',
    'Hanseatic League':                     'Hanseatic',
    'Ming Dynasty':                         'Ming',
    'Aztec Triple Alliance':                'Aztec',
    'Habsburg Composite Monarchy':          'Habsburg',
    'Mughal Empire Akbar Period':           'Mughal',
    'Tokugawa Shogunate':                   'Tokugawa',
    'British Parliamentary System':         'Britain',
    'United States Federal Republic':       'USA',
    'Meiji Oligarchy':                      'Meiji',
    'French Third Republic':                'France III',
    'Weimar Republic':                      'Weimar',
    'Soviet Republics System':              'Soviet',
    'Nazi Germany':                         'Nazi',
    'Chinese Communist Party Governance':   'CCP',
    'Singapore Technocracy':                'Singapore',
    'Norwegian Sovereign Wealth Democracy': 'Norway',
}


def edr_colour(edr):
    if np.isnan(edr): return '#888'
    if edr >= 0.65:   return GREEN
    if edr <= 0.25:   return RED
    return AMBER


def build_adj(edges_df):
    adj = defaultdict(set)
    for _, row in edges_df.iterrows():
        adj[row['source']].add(row['target'])
        adj[row['target']].add(row['source'])
    return adj


def degree_edr_correlations(adj, edr_map, max_d=4):
    all_sys = list(adj.keys())
    edrs    = {s: float(edr_map.get(s, np.nan)) for s in all_sys}
    results = {}
    current = {s: adj[s].copy() for s in all_sys}
    for d in range(1, max_d + 1):
        pairs = []
        for s, nb in current.items():
            if not nb: continue
            edr_s  = edrs.get(s, np.nan)
            nbr_e  = [edrs.get(n, np.nan) for n in nb]
            nbr_e  = [x for x in nbr_e if not np.isnan(x)]
            if nbr_e and not np.isnan(edr_s):
                pairs.append((edr_s, float(np.mean(nbr_e))))
        if len(pairs) >= 5:
            xs, ys = [p[0] for p in pairs], [p[1] for p in pairs]
            r, p   = stats.pearsonr(xs, ys)
            results[d] = (r, p)
        nxt = {}
        for s, nb in current.items():
            exp = set()
            for n in nb: exp |= adj[n]
            exp.discard(s)
            nxt[s] = exp
        current = nxt
    return results


def spring_layout(nodes, adj, edr_map, seed=42, iterations=150, k=2.8):
    """Spring layout anchored vertically to EDR value."""
    try:
        import networkx as nx
        G = nx.Graph()
        for n in nodes: G.add_node(n)
        for n, neighbours in adj.items():
            for m in neighbours:
                if n < m: G.add_edge(n, m)
        pos = nx.spring_layout(G, k=k, iterations=iterations, seed=seed)
        cx = np.mean([pos[n][0] for n in nodes])
        for n in pos:
            edr = float(edr_map.get(n, 0.5))
            pos[n] = (pos[n][0], pos[n][1] * 0.45 + (edr - 0.5) * 1.9)
        return pos
    except ImportError:
        # Fallback: random x, EDR-driven y
        rng = np.random.default_rng(seed)
        return {n: (rng.uniform(-1, 1),
                    (float(edr_map.get(n, 0.5)) - 0.5) * 1.9)
                for n in nodes}


def generate_figure(out_path, dpi=150):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec

    # ── Load data ──────────────────────────────────────────────────────────────
    for path in [GOV_FILE, SOURCED_FILE]:
        if not os.path.isfile(path):
            print(f'ERROR: {path} not found')
            return

    gov = pd.read_csv(GOV_FILE)
    gov['EDR'] = pd.to_numeric(gov['disobedience_freedom'], errors='coerce')
    edr_map = dict(zip(gov['System'], gov['EDR']))

    edges_df = pd.read_csv(SOURCED_FILE)
    adj = build_adj(edges_df)
    nodes = list(adj.keys())

    # ── Layout ─────────────────────────────────────────────────────────────────
    pos = spring_layout(nodes, adj, edr_map)
    cx = np.mean([pos[n][0] for n in nodes])

    # ── Degree-EDR correlations ────────────────────────────────────────────────
    sourced_r = degree_edr_correlations(adj, edr_map)
    full_r    = {1: 0.582, 2: 0.560, 3: 0.314, 4: -0.391}

    print('Degree-EDR correlations (historically-sourced network):')
    for d, (r, p) in sorted(sourced_r.items()):
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
        print(f'  r_d{d} = {r:+.3f}  p = {p:.4f}  {sig}')

    # ── Edge statistics ────────────────────────────────────────────────────────
    cont = [(row['source'], row['target'])
            for _, row in edges_df.iterrows() if row['edge_type'] == 'contrast']
    comp = [(row['source'], row['target'])
            for _, row in edges_df.iterrows() if row['edge_type'] == 'comparator']
    cont_d = [abs(float(edr_map.get(a, np.nan)) - float(edr_map.get(b, np.nan)))
              for a, b in cont]
    comp_d = [abs(float(edr_map.get(a, np.nan)) - float(edr_map.get(b, np.nan)))
              for a, b in comp]
    from scipy.stats import mannwhitneyu
    _, pmw = mannwhitneyu(cont_d, comp_d, alternative='greater')
    theta  = 0.45
    cross  = sum(1 for a, b in cont
                 if (float(edr_map.get(a, 0)) >= theta) !=
                    (float(edr_map.get(b, 0)) >= theta))
    print(f'\nEdge statistics:')
    print(f'  Mean |ΔEDR| contrast:   {np.mean(cont_d):.3f}  (n={len(cont_d)})')
    print(f'  Mean |ΔEDR| comparator: {np.mean(comp_d):.3f}  (n={len(comp_d)})')
    print(f'  Mann-Whitney p:         {pmw:.4f}')
    print(f'  Contrast cross-theta:   {cross}/{len(cont)} = {cross/len(cont):.3f}')

    # ── Figure ─────────────────────────────────────────────────────────────────
    plt.rcParams.update({
        'font.family': 'serif',
        'axes.spines.top': False,
        'axes.spines.right': False,
    })
    fig = plt.figure(figsize=(18, 11), facecolor=BG)
    gs  = GridSpec(1, 2, figure=fig, width_ratios=[2.2, 1],
                   left=0.02, right=0.97, top=0.92, bottom=0.04, wspace=0.05)
    ax_net = fig.add_subplot(gs[0])
    ax_dec = fig.add_subplot(gs[1])
    for ax in [ax_net, ax_dec]:
        ax.set_facecolor(BG)
        for spine in ax.spines.values():
            spine.set_color('#3a4158')

    # ── Panel A: network ───────────────────────────────────────────────────────
    ax_net.axis('off')

    ecols  = {'comparator': '#4a9eff', 'contrast': RED, 'parallel': MID}
    ealpha = {'comparator': 0.50,      'contrast': 0.80, 'parallel': 0.35}
    elw    = {'comparator': 0.9,       'contrast': 1.7,  'parallel': 0.7}
    els    = {'comparator': '-',       'contrast': '-',  'parallel': '--'}

    for _, row in edges_df.iterrows():
        et = row['edge_type']
        a, b = row['source'], row['target']
        if a not in pos or b not in pos: continue
        ax_net.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]],
                    color=ecols.get(et, '#888'),
                    alpha=ealpha.get(et, 0.5),
                    lw=elw.get(et, 1.0),
                    ls=els.get(et, '-'),
                    zorder=1)

    for n in nodes:
        col = edr_colour(float(edr_map.get(n, 0.5)))
        sz  = 70 + len(adj[n]) * 42
        ax_net.scatter(pos[n][0], pos[n][1], s=sz, color=col,
                       zorder=3, edgecolors='white', linewidths=0.8, alpha=0.9)

    # Node radius in display points for each node (used for label offset)
    # scatter s= is area in points², so radius in points = sqrt(s/pi)
    import math
    for n in nodes:
        label = SHORT.get(n, n[:12])
        s = 70 + len(adj[n]) * 42          # same formula as scatter above
        r_pt = math.sqrt(s / math.pi)      # node radius in display points
        # Place label just outside the node edge: 3pt gap
        offset_pt = r_pt + 3
        # Left/right based on x position in panel
        x_range = max(pos[nn][0] for nn in nodes) - min(pos[nn][0] for nn in nodes)
        x_mid   = min(pos[nn][0] for nn in nodes) + x_range / 2
        ha  = 'left'  if pos[n][0] >= x_mid else 'right'
        xo  = offset_pt if ha == 'left' else -offset_pt
        ax_net.annotate(
            label,
            xy=(pos[n][0], pos[n][1]),
            xytext=(xo, 0),
            textcoords='offset points',
            fontsize=7.2, color=LABEL, ha=ha, va='center',
            zorder=4, fontfamily='serif',
            annotation_clip=False,
        )

    n_comp = sum(1 for _, r in edges_df.iterrows() if r['edge_type'] == 'comparator')
    n_cont = sum(1 for _, r in edges_df.iterrows() if r['edge_type'] == 'contrast')
    n_para = sum(1 for _, r in edges_df.iterrows() if r['edge_type'] == 'parallel')

    handles = [
        mpatches.Patch(color=GREEN,    label='High EDR (\u2265 0.65)'),
        mpatches.Patch(color=AMBER,    label='Bridge EDR (0.25\u20130.65)'),
        mpatches.Patch(color=RED,      label='Low EDR (\u2264 0.25)'),
        plt.Line2D([0],[0], color='#4a9eff', lw=1.8, label=f'Comparator (n={n_comp})'),
        plt.Line2D([0],[0], color=RED,       lw=1.8, label=f'Contrast (n={n_cont})'),
        plt.Line2D([0],[0], color=MID, lw=0.9, ls='--', label=f'Parallel (n={n_para})'),
    ]
    leg = ax_net.legend(handles=handles, loc='upper left', fontsize=8.5,
                        facecolor='#1e2840', edgecolor='#3a4158', framealpha=0.88)
    for t in leg.get_texts():
        t.set_color(LABEL)

    ax_net.set_title(
        f'A.\u2002Historically-sourced governance influence network\u2002'
        f'({len(edges_df)} edges, {len(nodes)} nodes)\n'
        'Each edge sourced from named secondary literature; '
        'edge types assigned from historical documentation',
        color=LABEL, fontsize=9.5, fontweight='bold', loc='left', pad=5)

    # ── Panel B: contagion decay ───────────────────────────────────────────────
    ds      = [1, 2, 3, 4]
    sourced = [sourced_r[d][0] for d in ds]
    full    = [full_r[d]       for d in ds]

    ax_dec.axhline(0, color='#555', lw=0.8, alpha=0.6, zorder=1)
    ax_dec.plot(ds, full, 'o--', color=SLATE, lw=2.0, ms=9, zorder=3,
                label='Full dataset\n(353 nodes, algorithmic)')
    ax_dec.plot(ds, sourced, 's-', color=AMBER, lw=2.2, ms=9, zorder=4,
                label='Historically-sourced\n(30 nodes, 56 edges)')

    for d, (r, p) in sourced_r.items():
        sig  = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
        if sig:
            yoff = 0.07 if r >= 0 else -0.10
            ax_dec.text(d, r + yoff, sig, ha='center',
                        color=AMBER, fontsize=11, fontweight='bold')

    ax_dec.set_xticks(ds)
    ax_dec.set_xticklabels([f'd\u202f=\u202f{d}' for d in ds], fontsize=9.5)
    ax_dec.tick_params(colors=MID, labelsize=9)
    ax_dec.yaxis.set_tick_params(labelcolor=MID)
    ax_dec.xaxis.set_tick_params(labelcolor=MID)
    ax_dec.set_ylabel('r(EDR\u1d62, mean EDR of d-hop neighbours)',
                      color=MID, fontsize=9)
    ax_dec.set_ylim(-0.88, 0.92)
    ax_dec.set_xlim(0.7, 4.5)

    leg2 = ax_dec.legend(fontsize=8.5, loc='upper right',
                         facecolor='#1e2840', edgecolor='#3a4158', framealpha=0.88)
    for t in leg2.get_texts():
        t.set_color(LABEL)

    r4s = sourced_r[4][0]
    r4f = full_r[4]
    ax_dec.annotate(f'r_d4\u202f=\u202f{r4s:.3f}***',
                    xy=(4, r4s), xytext=(3.2, r4s - 0.17),
                    color=AMBER, fontsize=8.5,
                    arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.0))
    ax_dec.annotate(f'r_d4\u202f=\u202f{r4f:.3f}',
                    xy=(4, r4f), xytext=(3.1, r4f - 0.20),
                    color=SLATE, fontsize=8.5,
                    arrowprops=dict(arrowstyle='->', color=SLATE, lw=1.0))

    ax_dec.set_title('B.\u2002Contagion decay: sourced vs full dataset\n'
                     'Both reproduce sign reversal at d\u202f=\u202f4',
                     color=LABEL, fontsize=9.5, fontweight='bold',
                     loc='left', pad=5)

    # ── Suptitle ───────────────────────────────────────────────────────────────
    fig.suptitle(
        f'Figure 2.\u2002Historically-sourced governance influence network '
        f'({len(nodes)} nodes, {len(edges_df)} edges) and contagion decay comparison\n'
        f'Contrast edges span 2.2\u00d7 EDR distance of comparator edges '
        f'(MW p\u202f=\u202f{pmw:.3f})\u2003\u00b7\u2003'
        f'Degree-4 sign reversal: r_d4\u202f=\u202f\u2212{abs(r4s):.3f} '
        f'(p\u202f<\u202f0.001)',
        color=LABEL, fontsize=10.5, fontweight='bold', y=0.995)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=dpi, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f'\nSaved: {out_path}')


def main():
    parser = argparse.ArgumentParser(
        description='Generate Figure 2: historically-sourced governance influence network',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    parser.add_argument('--figure', type=str,
                        default=os.path.join(VIS_DIR, 'network_influence_sourced.png'),
                        help='Output path (default: visuals/network_influence_sourced.png)')
    parser.add_argument('--dpi', type=int, default=150,
                        help='Output DPI (default: 150; use 300 for print)')
    args = parser.parse_args()

    print('=' * 60)
    print('FIGURE 2: HISTORICALLY-SOURCED GOVERNANCE INFLUENCE NETWORK')
    print('=' * 60)
    print(f'  Network file: {SOURCED_FILE}')
    print(f'  Output:       {args.figure}')
    print(f'  DPI:          {args.dpi}')
    print()

    generate_figure(args.figure, dpi=args.dpi)


if __name__ == '__main__':
    main()
