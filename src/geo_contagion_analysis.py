"""
geo_contagion_analysis.py
Dedicated analysis and visualisation for:
  1. Geographic schismogenesis — does proximity predict stronger differentiation?
  2. Contagion decay — how far does EDR similarity propagate through the network?

Run after schismogenesis.py (requires network_edges.csv and governance_extended.csv).

Usage:
    python src/geo_contagion_analysis.py

Outputs (visuals/):
    geo_schismogenesis.png   — distance vs ΔEDR scatter + quartile breakdown
    contagion_decay.png      — EDR correlation by network degree (full + contrast-only)
"""
import csv, math, os, warnings
warnings.filterwarnings('ignore')

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from scipy import stats
from collections import defaultdict
import statistics as stat

DATA_PATH  = os.path.join(os.path.dirname(__file__), '..', 'data', 'governance_extended.csv')
EDGES_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'network_edges.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'visuals')

# ── Load ──────────────────────────────────────────────────────────────────────

def load():
    nodes = {}
    with open(DATA_PATH, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try:
                nodes[r['System']] = {
                    'lat':    float(r['Latitude'])  if r.get('Latitude','').strip()  else None,
                    'lon':    float(r['Longitude']) if r.get('Longitude','').strip() else None,
                    'EDR':    (float(r['exit_freedom'])+float(r['disobedience_freedom'])+float(r['arrangement_freedom']))/3,
                    'SAP':    (float(r['sovereignty_index'])+float(r['admin_index'])+float(r['competitive_politics_index']))/3,
                    'conf':   int(r.get('coding_confidence',1) or 1),
                    'start':  r.get('Start',''),
                    'region': r.get('Region',''),
                }
            except: continue

    edges = []
    with open(EDGES_PATH, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            edges.append(r)

    return nodes, edges


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2-lat1); dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def build_geo_edges(nodes, edges):
    geo = []
    for r in edges:
        s, t, et = r['source'], r['target'], r['edge_type']
        if s not in nodes or t not in nodes: continue
        ns, nt = nodes[s], nodes[t]
        if ns['lat'] is None or nt['lat'] is None: continue
        try: ts = int(ns['start']); tt = int(nt['start']); tgap = abs(ts-tt)
        except: tgap = None
        geo.append({
            'src': s, 'tgt': t, 'type': et,
            'dist':      haversine(ns['lat'], ns['lon'], nt['lat'], nt['lon']),
            'delta_edr': abs(ns['EDR'] - nt['EDR']),
            'delta_sap': abs(ns['SAP'] - nt['SAP']),
            'edr_s':     ns['EDR'], 'edr_t': nt['EDR'],
            'tgap':      tgap,
            'conf':      min(ns['conf'], nt['conf']),
        })
    return geo


def build_graph(nodes, edges):
    G = nx.Graph()
    for r in edges:
        s, t = r['source'], r['target']
        if s in nodes and t in nodes:
            G.add_edge(s, t, edge_type=r['edge_type'])
    return G


# ── Geographic schismogenesis ─────────────────────────────────────────────────

def plot_geo_schismogenesis(geo):
    contrast   = [e for e in geo if e['type'] == 'contrast']
    parallel   = [e for e in geo if e['type'] == 'parallel']
    comparator = [e for e in geo if e['type'] == 'comparator']

    fig, axes = plt.subplots(1, 3, figsize=(17, 6))

    EDGE_COLOURS = {'contrast':'#d62728','parallel':'#1f77b4','comparator':'#aaaaaa'}
    KM_MAX = 20000

    # Panel 1: Distance vs ΔEDR scatter for all edge types
    ax = axes[0]
    for et, elist in [('comparator', comparator), ('parallel', parallel), ('contrast', contrast)]:
        xs = [e['dist'] for e in elist]
        ys = [e['delta_edr'] for e in elist]
        alpha = 0.5 if et == 'comparator' else 0.7
        size  = 18  if et == 'comparator' else 30
        ax.scatter(xs, ys, c=EDGE_COLOURS[et], s=size, alpha=alpha,
                   label=f'{et} (n={len(elist)})', edgecolors='none', zorder=3)
        # Trend line
        if len(xs) > 5:
            m, b = np.polyfit(xs, ys, 1)
            xr = np.linspace(0, KM_MAX, 100)
            ax.plot(xr, m*xr+b, color=EDGE_COLOURS[et], lw=1.5, alpha=0.7, linestyle='--')
        r, p = stats.spearmanr(xs, ys)
        sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'ns'
        ax.text(0.97, {'contrast':0.95,'parallel':0.88,'comparator':0.81}[et],
                f'{et}: ρ={r:.2f} {sig}',
                transform=ax.transAxes, ha='right', fontsize=8.5,
                color=EDGE_COLOURS[et])

    ax.set_xlabel('Distance between cited pair (km)', fontsize=10)
    ax.set_ylabel('|ΔEDR|', fontsize=10)
    ax.set_title('Distance vs EDR divergence by edge type\nNo significant geographic pattern (schismogenesis at civilisational scale)', fontsize=9)
    ax.legend(fontsize=8, loc='upper left')
    ax.set_xlim(0, KM_MAX); ax.set_ylim(0, 0.85)

    # Panel 2: ΔEDR by distance quartile (contrast vs comparator)
    ax = axes[1]
    c_sorted = sorted(contrast, key=lambda x: x['dist'])
    co_sorted = sorted(comparator, key=lambda x: x['dist'])
    n_q = 4

    def quartile_means(elist, n_q):
        n = len(elist)
        qs = [elist[i*n//n_q:(i+1)*n//n_q] for i in range(n_q)]
        return [(stat.mean(q['dist'] for q in qi),
                 stat.mean(q['delta_edr'] for q in qi),
                 len(qi)) for qi in qs if qi]

    c_q  = quartile_means(c_sorted,  n_q)
    co_q = quartile_means(co_sorted, n_q)
    
    # guard before indexing into c_q and co_q
    if not c_q or not co_q:
        print("  No geographic contrast data — skipping plot")
        return

    x_c  = [q[0] for q in c_q];  y_c  = [q[1] for q in c_q]
    x_co = [q[0] for q in co_q]; y_co = [q[1] for q in co_q]

    ax.plot(x_c,  y_c,  'o-', color='#d62728', lw=2, markersize=8,
            label='Contrast (by distance quartile)')
    ax.plot(x_co, y_co, 's--', color='#aaaaaa', lw=1.5, markersize=7,
            label='Comparator (by distance quartile)')

    # Annotate contrast quartile n's
    for q in c_q:
        ax.annotate(f'n={q[2]}', (q[0], q[1]),
                    xytext=(0, 8), textcoords='offset points',
                    ha='center', fontsize=7.5, color='#d62728')

    # Key finding annotation: Q1 vs Q4
    q1_mean = c_q[0][1]; q4_mean = c_q[-1][1]
    ax.annotate(f'Q1 (nearest): μ={q1_mean:.2f}\nQ4 (most distant): μ={q4_mean:.2f}\nDecline: {q1_mean-q4_mean:+.3f}',
                xy=(0.05, 0.92), xycoords='axes fraction', fontsize=8,
                color='#d62728', va='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

    ax.set_xlabel('Mean distance within quartile (km)', fontsize=10)
    ax.set_ylabel('Mean |ΔEDR|', fontsize=10)
    ax.set_title('ΔEDR by distance quartile\nNearest contrast pairs show marginally larger divergence',
                 fontsize=9)
    ax.legend(fontsize=8)
    ax.set_ylim(0.1, 0.35)

    # Panel 3: Contemporary vs anachronistic contrast pairs
    ax = axes[2]
    with_time = [e for e in contrast if e['tgap'] is not None]
    bins = [0, 100, 300, 500, 1000, 2000, 5000, 50000]
    bin_labels = ['<100', '100–300', '300–500', '500–1k', '1k–2k', '2k–5k', '>5k']
    bin_means, bin_ns = [], []
    for lo, hi in zip(bins[:-1], bins[1:]):
        subset = [e['delta_edr'] for e in with_time if lo <= e['tgap'] < hi]
        if subset:
            bin_means.append(stat.mean(subset))
            bin_ns.append(len(subset))
        else:
            bin_means.append(None)
            bin_ns.append(0)

    x_pos = range(len(bin_labels))
    bars = ax.bar(x_pos, [m if m else 0 for m in bin_means],
                  color=['#d62728' if m and m > 0.23 else '#ffaaaa' for m in bin_means],
                  alpha=0.8, edgecolor='white')
    for i, (m, n) in enumerate(zip(bin_means, bin_ns)):
        if m: ax.text(i, m + 0.005, f'n={n}', ha='center', fontsize=7.5)

    ax.axhline(stat.mean(e['delta_edr'] for e in contrast), color='grey',
               lw=1.5, linestyle='--', alpha=0.7, label='Overall mean')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'{l}yr' for l in bin_labels], fontsize=8, rotation=25, ha='right')
    ax.set_xlabel('Temporal gap between contrast pair (years)', fontsize=10)
    ax.set_ylabel('Mean |ΔEDR|', fontsize=10)
    ax.set_title('ΔEDR by temporal gap (contrast edges)\nContemporary pairs show similar divergence to anachronistic',
                 fontsize=9)
    ax.legend(fontsize=8)
    ax.set_ylim(0, 0.4)

    fig.suptitle('Geographic Schismogenesis Analysis\n'
                 'Schismogenesis operates at civilisational scale — not constrained by geography or contemporaneity',
                 fontsize=12, fontweight='bold')
    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(os.path.join(OUTPUT_DIR, 'geo_schismogenesis.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: geo_schismogenesis.png")


# ── Contagion decay ───────────────────────────────────────────────────────────

def get_degree_shell(G, n, degree):
    """Return nodes at exactly `degree` hops from n."""
    if degree == 1:
        return [nb for nb in G.neighbors(n) if nb != n]
    shell, closer = set(), {n}
    current = {n}
    for d in range(1, degree):
        new_shell = set()
        for node in current:
            new_shell.update(G.neighbors(node))
        new_shell -= closer
        closer.update(new_shell)
        current = new_shell
    at_d = set()
    for node in current:
        at_d.update(G.neighbors(node))
    return list(at_d - closer)


def compute_decay(G, nodes, hc, max_degree=4):
    results = {}
    for degree in range(1, max_degree+1):
        own, nbr = [], []
        for n in hc:
            nbrs_d = [nb for nb in get_degree_shell(G, n, degree) if nb in nodes]
            if not nbrs_d: continue
            own.append(nodes[n]['EDR'])
            nbr.append(np.mean([nodes[nb]['EDR'] for nb in nbrs_d]))
        if len(own) >= 5:
            r_val, p_val = stats.pearsonr(own, nbr)
            boots = []
            for _ in range(2000):
                idx = np.random.choice(len(own), len(own), replace=True)
                try:
                    br, _ = stats.pearsonr([own[i] for i in idx], [nbr[i] for i in idx])
                    boots.append(br)
                except ValueError:
                    pass
            ci = np.percentile(boots, [2.5, 97.5])
            results[degree] = {'r': r_val, 'p': p_val, 'n': len(own),
                                'ci_lo': ci[0], 'ci_hi': ci[1]}
    return results


def plot_contagion_decay(G, nodes, edges_raw):
    if G.number_of_edges() == 0:
        print("  No graph edges — skipping contagion decay plot")
        return
    
    hc = [n for n in G.nodes if n in nodes and nodes[n]['conf'] >= 2]

    # Full graph decay
    decay_full = compute_decay(G, nodes, hc, max_degree=4)

    # Contrast-only graph
    G_c = nx.Graph()
    for r in edges_raw:
        if r['edge_type'] == 'contrast' and r['source'] in nodes and r['target'] in nodes:
            G_c.add_edge(r['source'], r['target'])
    hc_c = [n for n in hc if n in G_c]
    decay_contrast = compute_decay(G_c, nodes, hc_c, max_degree=3)

    # Parallel-only graph
    G_p = nx.Graph()
    for r in edges_raw:
        if r['edge_type'] == 'parallel' and r['source'] in nodes and r['target'] in nodes:
            G_p.add_edge(r['source'], r['target'])
    hc_p = [n for n in hc if n in G_p]
    decay_parallel = compute_decay(G_p, nodes, hc_p, max_degree=3)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    def sig(p): return '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'ns'

    # Panel 1: Full graph decay with CI ribbon
    ax = axes[0]
    degs = sorted(decay_full.keys())
    rs   = [decay_full[d]['r']     for d in degs]
    ci_lo = [decay_full[d]['ci_lo'] for d in degs]
    ci_hi = [decay_full[d]['ci_hi'] for d in degs]
    ns_d  = [decay_full[d]['n']     for d in degs]

    # Degree-0 anchor: r=1.0 by definition (self-correlation)
    plot_degs  = [0] + degs
    plot_rs    = [1.0] + rs
    plot_ci_lo = [1.0] + ci_lo
    plot_ci_hi = [1.0] + ci_hi

    ax.fill_between(plot_degs, plot_ci_lo, plot_ci_hi,
                    alpha=0.2, color='#1f77b4', label='95% CI (bootstrap)')
    ax.plot(plot_degs, plot_rs, 'o-', color='#1f77b4', lw=2.5, markersize=10,
            label='Full network')
    ax.scatter([0], [1.0], color='#1f77b4', s=80, zorder=5, marker='s')
    ax.annotate('r=1.0\n(self, degree-0)', (0, 1.0),
                xytext=(8, -18), textcoords='offset points', fontsize=8,
                color='#1f77b4', alpha=0.75)
    ax.axhline(0, color='grey', lw=0.8, linestyle='--', alpha=0.5)

    for d, r_v, p_v, n in zip(degs, rs, [decay_full[d]['p'] for d in degs], ns_d):
        ax.annotate(f'r={r_v:.2f} {sig(p_v)}\n(n={n})',
                    (d, r_v), xytext=(10, 5 if r_v >= 0 else -20),
                    textcoords='offset points', fontsize=8.5)

    # Highlight the degree-4 sign reversal
    if 4 in decay_full and decay_full[4]['r'] < 0:
        ax.axvspan(3.5, 4.5, alpha=0.08, color='crimson')
        ax.text(4, decay_full[4]['r'] - 0.08,
                'Sign reversal\nat degree-4',
                ha='center', fontsize=8, color='crimson',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

    ax.set_xlabel('Network distance (degrees)', fontsize=11)
    ax.set_ylabel('EDR correlation r', fontsize=11)
    ax.set_title('Contagion decay — full citation network\n'
                 'EDR similarity propagates to degree-3, reverses at degree-4',
                 fontsize=10)
    ax.set_xticks([0] + degs)
    ax.set_xlim(-0.3, max(degs)+0.5)
    ax.set_ylim(-0.6, 1.0)
    ax.legend(fontsize=9)

    # Panel 2: Decay by edge type
    ax = axes[1]
    colours = {'full': '#1f77b4', 'contrast': '#d62728', 'parallel': '#2ca02c'}
    for label, decay, colour in [
        ('Full network', decay_full, '#1f77b4'),
        ('Contrast edges only', decay_contrast, '#d62728'),
        ('Parallel edges only', decay_parallel, '#2ca02c'),
    ]:
        if not decay: continue
        degs_l = sorted(decay.keys())
        rs_l   = [decay[d]['r'] for d in degs_l]
        ps_l   = [decay[d]['p'] for d in degs_l]
        ns_l   = [decay[d]['n'] for d in degs_l]
        plot_degs_l = [0] + degs_l
        plot_rs_l   = [1.0] + rs_l
        ax.plot(plot_degs_l, plot_rs_l, 'o-', color=colour, lw=2, markersize=8,
                label=f'{label}', alpha=0.85)
        ax.scatter([0], [1.0], color=colour, s=60, zorder=5, marker='s', alpha=0.85)
        for d, r_v, p_v, n in zip(degs_l, rs_l, ps_l, ns_l):
            ax.annotate(f'{sig(p_v)} n={n}', (d, r_v),
                        xytext=(5, 3), textcoords='offset points', fontsize=7.5,
                        color=colour, alpha=0.85)

    ax.axhline(0, color='grey', lw=0.8, linestyle='--', alpha=0.5)
    ax.set_xlabel('Network distance (degrees)', fontsize=11)
    ax.set_ylabel('EDR correlation r', fontsize=11)
    ax.set_title('Contagion decay by edge type\n'
                 'Contrast edges: positive at degree-1, drops to ns at degree-2',
                 fontsize=10)
    ax.set_xticks([0,1,2,3,4])
    ax.set_xlim(-0.3, 4.5)
    ax.set_ylim(-0.6, 1.0)
    ax.legend(fontsize=9)

    fig.suptitle('Contagion Decay Analysis\n'
                 'EDR similarity propagates through 3 network hops; contrast-edge diffusion is local',
                 fontsize=12, fontweight='bold')
    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(os.path.join(OUTPUT_DIR, 'contagion_decay.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: contagion_decay.png")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("Loading data...")
    nodes, edges = load()
    geo = build_geo_edges(nodes, edges)
    G   = build_graph(nodes, edges)
    print(f"Nodes: {len(nodes)}, Geo edges: {len(geo)}, Graph edges: {G.number_of_edges()}")

    print("Geographic schismogenesis analysis...")
    plot_geo_schismogenesis(geo)

    print("Contagion decay analysis...")
    plot_contagion_decay(G, nodes, edges)

    print("\nDone — outputs in visuals/")
