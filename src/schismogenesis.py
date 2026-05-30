"""
schismogenesis.py — Network analysis of governance system relationships.

Builds a graph from the Comparators and Comparative Insights columns,
where nodes are governance systems and edges encode:
  - comparator: cited as structurally similar
  - parallel:   explicitly noted as parallel in Comparative Insights
  - contrast:   explicitly noted as contrast (schismogenesis candidate)

Key outputs:
  1. Network statistics — degree, centrality, clustering
  2. Schismogenesis detection — contrast-edge pairs where the two nodes
     differ significantly in EDR composite (deliberate differentiation)
  3. EDR neighbourhood analysis — does a system's neighbours' EDR predict
     its own EDR? (tests the contagion vs schismogenesis hypothesis)
  4. Four visualisations saved to visuals/

Usage:
    python src/schismogenesis.py

Requires:
    pip install networkx matplotlib numpy scipy
"""

import csv, os, math, warnings
warnings.filterwarnings('ignore')

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import numpy as np

DATA_PATH  = os.path.join(os.path.dirname(__file__), '..', 'data', 'governance_extended.csv')
EDGES_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'network_edges.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'visuals')

THRESHOLD = 0.45

# ── Load data ─────────────────────────────────────────────────────────────────

def load_nodes(path=DATA_PATH):
    nodes = {}
    with open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try:
                E = float(r['exit_freedom'])
                D = float(r['disobedience_freedom'])
                R = float(r['arrangement_freedom'])
                S = float(r['sovereignty_index'])
                A = float(r['admin_index'])
                P = float(r['competitive_politics_index'])
                nodes[r['System']] = {
                    'EDR':    (E + D + R) / 3,
                    'SAP':    (S + A + P) / 3,
                    'S': S, 'A': A, 'P': P,
                    'E': E, 'D': D, 'R': R,
                    'conf':   int(r.get('coding_confidence', 1) or 1),
                    'region': r.get('Region', ''),
                    'epoch':  r.get('Historical Epoch', ''),
                    'start':  r.get('Start', ''),
                    'collapse': r.get('collapse_mode', ''),
                    'gw':     str(r.get('gw_discussed','')).upper() == 'TRUE',
                }
            except (ValueError, TypeError):
                continue
    return nodes

def load_edges(path=EDGES_PATH):
    edges = []
    with open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            edges.append((r['source'], r['target'], r['edge_type']))
    return edges

def build_graph(nodes, edges):
    G = nx.Graph()
    for name, attrs in nodes.items():
        G.add_node(name, **attrs)
    for src, tgt, etype in edges:
        if src in nodes and tgt in nodes:
            if G.has_edge(src, tgt):
                # Upgrade edge type priority: contrast > parallel > comparator
                current = G[src][tgt].get('edge_type','comparator')
                priority = {'contrast':2, 'parallel':1, 'comparator':0}
                if priority.get(etype,0) > priority.get(current,0):
                    G[src][tgt]['edge_type'] = etype
            else:
                G.add_edge(src, tgt, edge_type=etype)
    return G

# ── Analysis ──────────────────────────────────────────────────────────────────

def network_stats(G, nodes):
    hc = [n for n in G.nodes if nodes[n]['conf'] >= 2]
    subG = G.subgraph(hc)

    print("=== Network Statistics ===")
    print(f"Total nodes: {G.number_of_nodes()}  |  Edges: {G.number_of_edges()}")
    print(f"Hand-coded subgraph: {subG.number_of_nodes()} nodes, {subG.number_of_edges()} edges")

    by_type = {}
    for _,_,d in G.edges(data=True):
        t = d.get('edge_type','comparator')
        by_type[t] = by_type.get(t,0) + 1
    print(f"Edge types: {by_type}")

    components = list(nx.connected_components(G))
    print(f"Connected components: {len(components)}")
    largest = max(components, key=len)
    print(f"Largest component: {len(largest)} nodes ({100*len(largest)//G.number_of_nodes()}%)")

    # Degree distribution
    degrees = [d for _,d in G.degree()]
    print(f"Degree — mean: {np.mean(degrees):.1f}, max: {max(degrees)}, "
          f"median: {np.median(degrees):.0f}")

    # Top 10 by degree centrality
    dc = nx.degree_centrality(G)
    top = sorted(dc.items(), key=lambda x:-x[1])[:10]
    print(f"\nTop 10 by degree centrality:")
    for name, score in top:
        edr = nodes[name]['EDR']
        print(f"  {name[:42]:42s}  centrality={score:.3f}  EDR={edr:.2f}")

    return subG

def schismogenesis_analysis(G, nodes):
    """
    Contrast edges where |EDR_A - EDR_B| > 0.3 are strong schismogenesis candidates:
    two systems that cite each other as contrasts AND differ substantially in freedoms.
    """
    print("\n=== Schismogenesis Analysis ===")
    contrast_edges = [(u,v,d) for u,v,d in G.edges(data=True)
                      if d.get('edge_type') == 'contrast'
                      and u in nodes and v in nodes]
    print(f"Total contrast edges: {len(contrast_edges)}")

    strong = []
    for u, v, d in contrast_edges:
        delta_edr = abs(nodes[u]['EDR'] - nodes[v]['EDR'])
        delta_sap = abs(nodes[u]['SAP'] - nodes[v]['SAP'])
        if delta_edr > 0.25 or delta_sap > 0.25:
            strong.append((u, v, delta_edr, delta_sap,
                          nodes[u]['EDR'], nodes[v]['EDR']))

    strong.sort(key=lambda x: -(x[2]+x[3]))
    print(f"Strong schismogenesis pairs (ΔEDR>0.25 or ΔSAP>0.25): {len(strong)}")
    print(f"\n{'Source':42s}  {'Target':42s}  ΔEDR  ΔSAP")
    print("-" * 100)
    for u, v, de, ds, eu, ev in strong[:20]:
        print(f"  {u[:40]:40s}  {v[:40]:40s}  {de:.2f}  {ds:.2f}")
        print(f"    EDR: {eu:.2f} vs {ev:.2f}")

    return strong

def neighbourhood_edr_analysis(G, nodes):
    """
    For each hand-coded node, compute mean EDR of its neighbours.
    Test whether own EDR correlates with neighbour EDR (contagion)
    vs anti-correlates (schismogenesis / deliberate differentiation).
    """
    print("\n=== Neighbourhood EDR Analysis ===")
    hc = [n for n in G.nodes if nodes[n]['conf'] >= 2 and G.degree(n) > 0]

    own_edr, nbr_edr = [], []
    for n in hc:
        nbrs = [nodes[nb]['EDR'] for nb in G.neighbors(n) if nb in nodes]
        if not nbrs: continue
        own_edr.append(nodes[n]['EDR'])
        nbr_edr.append(np.mean(nbrs))

    if len(own_edr) < 3:
        print("  Insufficient data for correlation")
        return own_edr, nbr_edr

    # Pearson correlation
    oe, ne = np.array(own_edr), np.array(nbr_edr)
    r = np.corrcoef(oe, ne)[0,1]
    print(f"Own EDR vs mean neighbour EDR correlation: r = {r:.3f} (n={len(own_edr)})")
    if r > 0.3:
        print("  → Positive: contagion dominant (similar systems cite each other)")
    elif r < -0.2:
        print("  → Negative: schismogenesis dominant (dissimilar systems cite each other)")
    else:
        print("  → Near-zero: mixed signal — both dynamics present")

    # Contrast-only neighbourhood
    own_c, nbr_c = [], []
    for n in hc:
        nbrs_c = [nodes[nb]['EDR'] for nb in G.neighbors(n)
                  if nb in nodes and G[n][nb].get('edge_type') == 'contrast']
        if not nbrs_c: continue
        own_c.append(nodes[n]['EDR'])
        nbr_c.append(np.mean(nbrs_c))

    if len(own_c) >= 3:
        rc = np.corrcoef(np.array(own_c), np.array(nbr_c))[0,1]
        print(f"Own EDR vs contrast-neighbour EDR only: r = {rc:.3f} (n={len(own_c)})")

    return own_edr, nbr_edr

# ── Visualisations ────────────────────────────────────────────────────────────

REGION_COLOURS = {
    'Mesopotamia':  '#e41a1c', 'Egypt':      '#ff7f00', 'Greece':     '#ffdd44',
    'Rome':         '#f4c430', 'China':      '#984ea3', 'India':      '#4daf4a',
    'Europe':       '#377eb8', 'Africa':     '#a65628', 'Americas':   '#f781bf',
    'Middle East':  '#e78ac3', 'Southeast Asia': '#8da0cb', 'Oceania': '#66c2a5',
}

def region_colour(region):
    r = (region or '').lower()
    for k, c in REGION_COLOURS.items():
        if k.lower() in r:
            return c
    return '#cccccc'

def plot_network(G, nodes):
    """Full network — nodes coloured by EDR, sized by degree."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    hc_nodes = [n for n in G.nodes if nodes[n]['conf'] >= 2]
    subG = G.subgraph(hc_nodes).copy()
    if subG.number_of_nodes() == 0:
        print("No hand-coded nodes in graph — skipping network plot")
        return

    fig, ax = plt.subplots(figsize=(16, 12))

    # Layout: spring with EDR-weighted repulsion so high-EDR nodes spread outward
    pos = nx.spring_layout(subG, k=3.5, seed=42, iterations=120)

    cmap = cm.RdYlGn
    edr_vals = [nodes[n]['EDR'] for n in subG.nodes]
    degrees  = dict(subG.degree())

    # Edge colours by type
    edge_colours = {
        'contrast':   '#d62728',
        'parallel':   '#1f77b4',
        'comparator': '#aaaaaa',
    }
    for etype, colour in edge_colours.items():
        elist = [(u,v) for u,v,d in subG.edges(data=True)
                 if d.get('edge_type') == etype]
        width = 2.0 if etype == 'contrast' else (1.2 if etype == 'parallel' else 0.6)
        alpha = 0.8 if etype == 'contrast' else (0.5 if etype == 'parallel' else 0.25)
        nx.draw_networkx_edges(subG, pos, edgelist=elist,
                               edge_color=colour, width=width, alpha=alpha, ax=ax)

    # Nodes
    node_colours = [cmap(nodes[n]['EDR']) for n in subG.nodes]
    node_sizes   = [100 + 40 * degrees.get(n,0) for n in subG.nodes]
    nx.draw_networkx_nodes(subG, pos, node_color=node_colours,
                           node_size=node_sizes, alpha=0.9, ax=ax)

    # Labels for high-degree or GW-discussed nodes
    label_nodes = {n for n in subG.nodes
                   if degrees.get(n,0) >= 5 or nodes[n]['gw']}
    labels = {n: n for n in label_nodes}
    nx.draw_networkx_labels(subG, pos, labels=labels,
                            font_size=6.5, font_weight='bold', ax=ax)

    # Legend — edge types
    handles = [
        mpatches.Patch(color='#d62728', label='Contrast (schismogenesis candidate)'),
        mpatches.Patch(color='#1f77b4', label='Parallel (structural similarity)'),
        mpatches.Patch(color='#aaaaaa', label='Comparator (general citation)'),
    ]
    ax.legend(handles=handles, fontsize=9, loc='lower left', framealpha=0.85)

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0,1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.5, pad=0.01)
    cbar.set_label('EDR Composite', fontsize=9)
    cbar.ax.axhline(THRESHOLD, color='black', lw=1.5, linestyle='--')

    ax.set_title('Governance System Network — hand-coded systems\n'
                 'Node colour = EDR composite; size = degree; '
                 'red edges = contrast (schismogenesis)', fontsize=12)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'network_full.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: network_full.png")

def plot_schismogenesis_pairs(strong_pairs, nodes):
    """Bar chart of top schismogenesis pairs by ΔEDR."""
    if not strong_pairs:
        print("No strong schismogenesis pairs to plot")
        return

    top = strong_pairs[:15]
    labels = [f"{u[:20]}…\nvs {v[:20]}…" if len(u)>20 or len(v)>20
              else f"{u}\nvs {v}" for u,v,*_ in top]
    delta_edr = [x[2] for x in top]
    delta_sap = [x[3] for x in top]

    x = np.arange(len(top))
    w = 0.4
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(x - w/2, delta_edr, w, label='ΔEDR', color='#e41a1c', alpha=0.8)
    ax.bar(x + w/2, delta_sap, w, label='ΔSAP', color='#377eb8', alpha=0.8)
    ax.axhline(0.25, color='grey', lw=1, linestyle='--', alpha=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=6.5, rotation=30, ha='right')
    ax.set_ylabel('Absolute difference')
    ax.set_title('Top schismogenesis candidates — contrast-cited pairs with largest EDR/SAP divergence\n'
                 '(Systems that explicitly contrast each other but differ substantially in governance structure)',
                 fontsize=11)
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'schismogenesis_pairs.png'), dpi=150)
    plt.close()
    print("Saved: schismogenesis_pairs.png")

def plot_neighbourhood_edr(own_edr, nbr_edr, G, nodes):
    """Scatter of own EDR vs mean neighbour EDR with trend line."""
    if len(own_edr) < 3:
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: all edges
    ax = axes[0]
    oe, ne = np.array(own_edr), np.array(nbr_edr)
    r = np.corrcoef(oe, ne)[0,1]
    ax.scatter(ne, oe, c=[cm.RdYlGn(e) for e in oe], s=45, alpha=0.8,
               edgecolors='white', linewidths=0.4)
    m, b = np.polyfit(ne, oe, 1)
    xr = np.linspace(ne.min(), ne.max(), 100)
    ax.plot(xr, m*xr+b, 'k--', lw=1.5, alpha=0.6)
    ax.axhline(THRESHOLD, color='crimson', lw=1, linestyle=':', alpha=0.6)
    ax.axvline(THRESHOLD, color='crimson', lw=1, linestyle=':', alpha=0.6)
    ax.set_xlabel('Mean neighbour EDR', fontsize=10)
    ax.set_ylabel('Own EDR', fontsize=10)
    ax.set_title(f'All edges\nr = {r:.3f} (n={len(oe)})', fontsize=11)
    ax.set_xlim(0,1); ax.set_ylim(0,1)

    # Right: contrast edges only
    ax = axes[1]
    hc = [n for n in G.nodes if nodes[n]['conf'] >= 2 and G.degree(n) > 0]
    own_c, nbr_c = [], []
    for n in hc:
        nbrs_c = [nodes[nb]['EDR'] for nb in G.neighbors(n)
                  if nb in nodes and G[n][nb].get('edge_type') == 'contrast']
        if not nbrs_c: continue
        own_c.append(nodes[n]['EDR'])
        nbr_c.append(np.mean(nbrs_c))

    if len(own_c) >= 3:
        oc, nc = np.array(own_c), np.array(nbr_c)
        rc = np.corrcoef(oc, nc)[0,1]
        ax.scatter(nc, oc, c=[cm.RdYlGn(e) for e in oc], s=55, alpha=0.85,
                   edgecolors='#d62728', linewidths=0.8)
        m2, b2 = np.polyfit(nc, oc, 1)
        xr2 = np.linspace(nc.min(), nc.max(), 100)
        ax.plot(xr2, m2*xr2+b2, 'k--', lw=1.5, alpha=0.6)
        ax.axhline(THRESHOLD, color='crimson', lw=1, linestyle=':', alpha=0.6)
        ax.axvline(THRESHOLD, color='crimson', lw=1, linestyle=':', alpha=0.6)
        ax.set_xlabel('Mean contrast-neighbour EDR', fontsize=10)
        ax.set_ylabel('Own EDR', fontsize=10)
        ax.set_title(f'Contrast edges only\nr = {rc:.3f} (n={len(oc)})', fontsize=11)
        ax.set_xlim(0,1); ax.set_ylim(0,1)
    else:
        ax.text(0.5, 0.5, 'Insufficient contrast-edge\ndata for hand-coded subset',
                ha='center', va='center', transform=ax.transAxes, fontsize=10)

    fig.suptitle('Neighbourhood EDR Analysis\n'
                 'Does a system\'s EDR correlate with its cited neighbours?\n'
                 'Positive r = contagion; Negative r = schismogenesis',
                 fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'neighbourhood_edr.png'), dpi=150)
    plt.close()
    print("Saved: neighbourhood_edr.png")

def plot_edr_delta_distribution(G, nodes):
    """
    Distribution of |ΔEDR| across all edge types.
    Tests whether contrast edges have larger EDR differences than comparator edges.
    """
    type_deltas = {'contrast':[], 'parallel':[], 'comparator':[]}
    for u, v, d in G.edges(data=True):
        if u not in nodes or v not in nodes: continue
        # Use all nodes; hand-coded flagged separately
        both_hc = nodes[u]['conf'] >= 2 and nodes[v]['conf'] >= 2
        delta = abs(nodes[u]['EDR'] - nodes[v]['EDR'])
        etype = d.get('edge_type','comparator')
        type_deltas[etype].append(delta)
        if both_hc:
            type_deltas.setdefault(etype+'_hc', []).append(delta)

    fig, ax = plt.subplots(figsize=(10, 5))
    colours = {'contrast':'#d62728','parallel':'#1f77b4','comparator':'#aaaaaa'}
    for etype in ['contrast','parallel','comparator']:
        deltas = type_deltas.get(etype,[])
        if not deltas: continue
        hc_deltas = type_deltas.get(etype+'_hc', [])
        hc_note = f', hc n={len(hc_deltas)} mean={np.mean(hc_deltas):.2f}' if hc_deltas else ''
        ax.hist(deltas, bins=15, alpha=0.6, color=colours[etype],
                label=f'{etype} (all n={len(deltas)}, mean={np.mean(deltas):.2f}{hc_note})')

    ax.set_xlabel('|ΔEDR| between cited pair', fontsize=11)
    ax.set_ylabel('Count', fontsize=11)
    ax.set_title(f'EDR divergence by edge type (all {len(nodes)} systems; hand-coded subset noted in legend)\n'
                 'If contrast edges have larger ΔEDR, schismogenesis is the dominant dynamic',
                 fontsize=11)
    ax.legend(fontsize=9)

    # Means as vertical lines
    for etype in ['contrast','parallel','comparator']:
        deltas = type_deltas.get(etype,[])
        if deltas:
            ax.axvline(np.mean(deltas), color=colours[etype], lw=2,
                       linestyle='--', alpha=0.8)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'edr_delta_by_edgetype.png'), dpi=150)
    plt.close()
    print("Saved: edr_delta_by_edgetype.png")

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("Loading data...")
    nodes = load_nodes()
    edges = load_edges()

    print(f"Nodes loaded: {len(nodes)}")
    print(f"Raw edges loaded: {len(edges)}")

    G = build_graph(nodes, edges)
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges\n")

    subG = network_stats(G, nodes)
    strong_pairs = schismogenesis_analysis(G, nodes)
    own_edr, nbr_edr = neighbourhood_edr_analysis(G, nodes)

    print("\nGenerating visualisations...")
    plot_network(G, nodes)
    plot_schismogenesis_pairs(strong_pairs, nodes)
    plot_neighbourhood_edr(own_edr, nbr_edr, G, nodes)
    plot_edr_delta_distribution(G, nodes)

    print(f"\nDone — outputs in visuals/")
    print("Files: network_full.png, schismogenesis_pairs.png, "
          "neighbourhood_edr.png, edr_delta_by_edgetype.png")
