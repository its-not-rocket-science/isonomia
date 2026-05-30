"""
edr_resilience.py — EDR resilience threshold analysis.

Identifies systems near or below the resilience threshold and analyses
whether collapse mode correlates with EDR composite as the model predicts.

Usage:
    python src/edr_resilience.py
"""
import csv, os, statistics

DATA_PATH = os.path.join(os.path.dirname(__file__),'..','data','governance_extended.csv')
THRESHOLD = 0.45

def load():
    rows = []
    with open(DATA_PATH) as f:
        for r in csv.DictReader(f):
            try:
                r['_E'] = float(r['exit_freedom'])
                r['_D'] = float(r['disobedience_freedom'])
                r['_R'] = float(r['arrangement_freedom'])
                r['_S'] = float(r['sovereignty_index'])
                r['_A'] = float(r['admin_index'])
                r['_P'] = float(r['competitive_politics_index'])
                r['_EDR'] = (r['_E']+r['_D']+r['_R'])/3
                r['_SAP'] = (r['_S']+r['_A']+r['_P'])/3
                r['_conf'] = int(r.get('coding_confidence',1) or 1)
                rows.append(r)
            except (ValueError, TypeError):
                continue
    return rows

def analyse(rows):
    hc = [r for r in rows if r['_conf'] >= 2]
    all_edr = [r['_EDR'] for r in rows]
    hc_edr  = [r['_EDR'] for r in hc]

    print(f"=== EDR Resilience Analysis ===")
    print(f"Total systems: {len(rows)}  |  Hand-coded: {len(hc)}")
    print(f"EDR mean (all): {statistics.mean(all_edr):.3f}  stdev: {statistics.stdev(all_edr):.3f}")
    print(f"EDR mean (hand-coded): {statistics.mean(hc_edr):.3f}  stdev: {statistics.stdev(hc_edr):.3f}")
    print(f"Resilience threshold θ = {THRESHOLD}")
    fragile_all = [r for r in rows if r['_EDR'] < THRESHOLD]
    fragile_hc  = [r for r in hc   if r['_EDR'] < THRESHOLD]
    print(f"Below θ (all): {len(fragile_all)} ({100*len(fragile_all)/len(rows):.0f}%)")
    print(f"Below θ (hand-coded): {len(fragile_hc)} ({100*len(fragile_hc)/len(hc):.0f}%)")

    # EDR-SAP correlation
    n = len(hc)
    em = statistics.mean(hc_edr)
    sm = statistics.mean([r['_SAP'] for r in hc])
    cov = sum((hc[i]['_EDR']-em)*(hc[i]['_SAP']-sm) for i in range(n))/n
    r_corr = cov/(statistics.stdev(hc_edr)*statistics.stdev([r['_SAP'] for r in hc]))
    print(f"\nEDR-SAP correlation (hand-coded, n={n}): r = {r_corr:.3f}")

    # Collapse mode analysis: do fragile systems collapse differently?
    from collections import Counter
    fragile_modes  = Counter(r.get('collapse_mode','unknown') for r in fragile_hc)
    resilient_modes = Counter(r.get('collapse_mode','unknown') for r in hc if r['_EDR'] >= THRESHOLD)
    print(f"\n=== Collapse modes — fragile (EDR < θ) ===")
    for k,v in fragile_modes.most_common(): print(f"  {v:3d}  {k}")
    print(f"\n=== Collapse modes — resilient (EDR >= θ) ===")
    for k,v in resilient_modes.most_common(): print(f"  {v:3d}  {k}")

    # Lock-in sequence: systems where L is high but EDR still above threshold (pre-lock-in)
    print(f"\n=== High L, EDR still above θ (pre-lock-in candidates) ===")
    candidates = [r for r in hc if float(r.get('surplus_legibility',0) or 0) >= 0.6
                  and r['_EDR'] >= THRESHOLD]
    for r in sorted(candidates, key=lambda x: x['_EDR']):
        print(f"  {r['System'][:40]:40s}  L={r['surplus_legibility']}  EDR={r['_EDR']:.2f}")

if __name__ == '__main__':
    rows = load()
    analyse(rows)
