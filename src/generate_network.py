"""
generate_network.py
===================
Generates the governance citation network data for Paper 4.

Produces two files:
  data/network_nodes.csv  — 353 governance systems with EDR, L, region
  data/network_edges.csv  — 773 citation edges (449 comparator, 204 parallel,
                            120 contrast), typed by EDR distance

The network structure matches Paper 4 §2:
  N = 353 nodes (real systems from governance_extended.csv)
  E = 773 edges (comparator: ΔEDR < alpha; contrast: ΔEDR >= alpha)
  Mean |ΔEDR| contrast:   ~0.64 (distance-based; see calibration ceiling §4.2)
  Mean |ΔEDR| comparator: ~0.07

Note: the distance-based edge-formation rule over-predicts cross-theta contrast
edges (contrast_cross ~0.89 vs empirical 0.42). This is the calibration ceiling
documented in Paper 4 §4.2 — historically structured awareness sets would fix it.

Usage
-----
    python src/generate_network.py
    python src/generate_network.py --data PATH/TO/governance_extended.csv
    python src/generate_network.py --seed 42
"""

import os
import argparse
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.join(SCRIPT_DIR, '..')
DATA_DIR   = os.path.join(ROOT, 'data')

N_NODES   = 353
N_COMP    = 449
N_PAR     = 204
N_CONT    = 120
ALPHA     = 0.20   # contrast threshold


def main():
    parser = argparse.ArgumentParser(
        description='Generate governance citation network data for Paper 4',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--data', type=str,
        default=os.path.join(DATA_DIR, 'governance_extended.csv'),
        help='Path to governance_extended.csv')
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    if not os.path.isfile(args.data):
        print(f'ERROR: Cannot find {args.data}')
        print('Run from repo root or pass --data PATH')
        return

    print('Generating governance citation network...')
    print(f'  N_nodes={N_NODES}, N_edges={N_COMP+N_PAR+N_CONT} '
          f'({N_COMP} comparator, {N_PAR} parallel, {N_CONT} contrast)')

    gov = pd.read_csv(args.data)
    gov['EDR'] = pd.to_numeric(gov['disobedience_freedom'], errors='coerce')
    gov['L']   = pd.to_numeric(gov['surplus_legibility'],   errors='coerce')
    gov_valid  = gov.dropna(subset=['EDR', 'L']).reset_index(drop=True)
    n_real     = min(len(gov_valid), N_NODES)

    node_df = pd.DataFrame([{
        'id':     i,
        'system': gov_valid.loc[i, 'System'],
        'edr':    float(gov_valid.loc[i, 'EDR']),
        'L':      float(gov_valid.loc[i, 'L']),
        'region': str(gov_valid.loc[i, 'Region'])
                  if 'Region' in gov_valid.columns else 'Unknown',
    } for i in range(n_real)])

    print(f'  Using {n_real} real systems from governance_extended.csv')
    print(f'  EDR range: {node_df.edr.min():.3f} – {node_df.edr.max():.3f}, '
          f'mean={node_df.edr.mean():.3f}')

    rng   = np.random.default_rng(args.seed)
    edrs  = node_df['edr'].values
    edges = []
    edge_set = set()

    def add_edge(i, j, etype):
        key = (min(i, j), max(i, j))
        if key not in edge_set:
            edge_set.add(key)
            edges.append({
                'source':    i,
                'target':    j,
                'edge_type': etype,
                'delta_edr': round(abs(edrs[i] - edrs[j]), 4),
            })
            return True
        return False

    def candidate_pool(i, etype, n=20):
        pool  = rng.choice(
            [j for j in range(n_real) if j != i],
            size=min(n, n_real - 1),
            replace=False)
        diffs = np.abs(edrs[pool] - edrs[i])
        if etype == 'contrast':
            idx = np.argsort(-diffs)[:5]
        else:
            idx = np.argsort(diffs)[:5]
        return pool[idx]

    for etype, n_target in [('comparator', N_COMP),
                             ('parallel',   N_PAR),
                             ('contrast',   N_CONT)]:
        current = sum(1 for e in edges if e['edge_type'] == etype)
        attempts = 0
        while current < n_target and attempts < 100_000:
            i = rng.integers(n_real)
            pool = candidate_pool(i, etype)
            if len(pool):
                j = int(rng.choice(pool))
                if add_edge(int(i), j, etype):
                    current += 1
            attempts += 1
        print(f'  {etype:<12}: {current}/{n_target} edges generated')

    edge_df = pd.DataFrame(edges)

    os.makedirs(DATA_DIR, exist_ok=True)
    nodes_path = os.path.join(DATA_DIR, 'network_nodes.csv')
    edges_path = os.path.join(DATA_DIR, 'network_edges.csv')
    node_df.to_csv(nodes_path, index=False, float_format='%.4f')
    edge_df.to_csv(edges_path, index=False, float_format='%.4f')

    print()
    print(f'  Saved: {nodes_path}  ({len(node_df)} nodes)')
    print(f'  Saved: {edges_path}  ({len(edge_df)} edges)')
    print()
    print('Edge statistics:')
    print(f'  Mean |ΔEDR| contrast:   '
          f'{edge_df[edge_df.edge_type=="contrast"].delta_edr.mean():.3f}')
    print(f'  Mean |ΔEDR| comparator: '
          f'{edge_df[edge_df.edge_type=="comparator"].delta_edr.mean():.3f}')
    theta = 0.45
    cont  = edge_df[edge_df.edge_type == 'contrast']
    cross = sum(
        1 for _, r in cont.iterrows()
        if (edrs[r['source']] >= theta) != (edrs[r['target']] >= theta))
    print(f'  Contrast cross-theta:   {cross/len(cont):.3f} '
          f'(target 0.420; ceiling due to distance-based rule)')
    print()
    print('Run the ABM:')
    print('  python src/schismogenesis_abm.py --no-sweep   # fast demo')
    print('  python src/schismogenesis_abm.py              # full sweep (~20 min)')


if __name__ == '__main__':
    main()
