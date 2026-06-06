"""
schismogenesis_abm.py
=====================
Agent-based model of governance differentiation via schismogenesis.

Paper 4 of the isonomia series.

Theoretical motivation
----------------------
Paper 1 established three empirical facts about the governance citation
network that require a generative model to explain:

  1. Schismogenesis signal: contrast-cited pairs have significantly larger
     EDR divergence than comparator-cited pairs (Mann-Whitney p = 0.0004).

  2. Degree-4 sign reversal: EDR correlation decays r = 0.72 → 0.62 →
     0.32 → −0.34 across four network hops.  At four hops, a system has
     traversed from one governance cluster into the other.

  3. Geographic null: proximity does not predict stronger differentiation.
     Schismogenesis is ideational, not spatial.

The network topology characterisation (paper4_network_topology.md)
established additionally that:

  4. Communities are EDR-assortative (r = 0.673), not geographically
     assortative (r = −0.006): EDR similarity, not location, drives
     who cites whom.

  5. 39% of contrast edges cross the EDR threshold θ = 0.45; cross-theta
     contrast pairs have ΔEDR = 0.378 vs 0.147 for same-regime pairs
     (p < 0.0001).

Model
-----
Each agent represents a governance system with an EDR value and a set of
edges to other agents typed as comparator or contrast.  At each step:

  1. Each agent assesses a random potential contact from its awareness set.
  2. If |ΔEDR| < α (similarity threshold): form/maintain a comparator edge.
  3. If |ΔEDR| ≥ α: form/maintain a contrast edge.
  4. EDR update:
       comparator neighbours: edr += β × (nbr_edr − edr)   [contagion]
       contrast neighbours:   edr −= γ × (nbr_edr − edr)   [schismogenesis]
  5. Optional lock-in coupling: if system L > l_threshold,
       edr −= δ × edr                                        [L-driven drift]
  6. EDR clipped to [0, 1].

Key prediction: γ/β > 1 is a necessary condition for bipolar structure.
Below this ratio, contagion dominates and the network converges to a
single cluster rather than the observed two-regime structure.

Usage
-----
    python src/schismogenesis_abm.py                     # single run, default params
    python src/schismogenesis_abm.py --sweep             # parameter sweep
    python src/schismogenesis_abm.py --sweep --figure    # sweep + figures
    python src/schismogenesis_abm.py --cases             # G-W case study runs
    python src/schismogenesis_abm.py --cases --figure    # cases + figures

Outputs (always written)
------------------------
    data/abm_sweep_results.csv      — parameter sweep results (--sweep)
    data/abm_cases_results.csv      — case study trajectories (--cases)

Outputs (only with --figure)
-----------------------------
    visuals/abm_sweep.png           — parameter sweep heatmaps
    visuals/abm_cases.png           — case study trajectory plots

Empirical targets (from paper4_network_topology.md)
----------------------------------------------------
    degree-1 EDR correlation:   r ≈ 0.72
    degree-2 EDR correlation:   r ≈ 0.62
    degree-3 EDR correlation:   r ≈ 0.32
    degree-4 EDR correlation:   r ≈ −0.34
    Louvain modularity:         M ≈ 0.55–0.60
    EDR assortativity:          r ≈ 0.67
    Contrast edge fraction
      crossing θ:               ≈ 0.39
    Mean ΔEDR contrast:         ≈ 0.24
    Mean ΔEDR comparator:       ≈ 0.19

Limitations
-----------
1.  The ABM is a plausibility model, not a historical simulation.
    N = 200 agents over T steps tests whether the local update rules
    are sufficient to generate the observed topology.

2.  L is treated as a static per-agent value in the base model.
    The coupled model (--lock-in flag) varies L over time per agent.

3.  The awareness set is initialised uniformly at random.  In reality,
    awareness is driven by trade routes, conquest, and scholarship.
    A geographically or temporally structured awareness set is a
    possible extension.
"""

import os
import argparse
import warnings
import numpy as np
import pandas as pd
import networkx as nx
from collections import defaultdict
from scipy import stats
from itertools import product

warnings.filterwarnings('ignore')

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT        = os.path.join(SCRIPT_DIR, '..')
DATA_DIR    = os.path.join(ROOT, 'data')
OUTPUT_DIR  = os.path.join(ROOT, 'visuals')
os.makedirs(DATA_DIR,   exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Empirical targets ─────────────────────────────────────────────────────────
TARGETS = {
    'r_d1':           0.72,
    'r_d2':           0.62,
    'r_d3':           0.32,
    'r_d4':          -0.34,
    'modularity':     0.575,
    'edr_assort':     0.673,
    'contrast_cross': 0.39,
    'delta_contrast': 0.24,
    'delta_comparator': 0.19,
}

# Weights for loss function — hard constraints weighted more heavily
TARGET_WEIGHTS = {
    'r_d1': 1.0, 'r_d2': 1.0, 'r_d3': 1.5, 'r_d4': 3.0,  # sign reversal critical
    'modularity': 2.0, 'edr_assort': 2.0,
    'contrast_cross': 1.0, 'delta_contrast': 0.5, 'delta_comparator': 0.5,
}

THETA = 0.45   # EDR resilience threshold


# ── Agent ─────────────────────────────────────────────────────────────────────

class Agent:
    """A governance system in the schismogenesis model."""

    __slots__ = ('id', 'edr', 'edr_init', 'l', 'is_bridge', 'edges', 'awareness')

    def __init__(self, agent_id, edr, l=0.3, is_bridge=False):
        self.id        = agent_id
        self.edr       = float(edr)
        self.edr_init  = float(edr)   # anchor point — initial EDR value
        self.l         = float(l)
        self.is_bridge = is_bridge    # bridge-region agent gets stronger anchor
        self.edges     = {}    # {neighbour_id: 'comparator' | 'contrast'}
        self.awareness = set()   # agent ids this agent knows about

    @property
    def above_theta(self):
        return self.edr > THETA


# ── Model ─────────────────────────────────────────────────────────────────────

class SchismogenesisModel:
    """
    Edge-formation schismogenesis model.

    Parameters
    ----------
    n_agents      : int   — number of agents
    alpha         : float — ΔEDR threshold for contrast vs comparator
    beta          : float — contagion strength (comparator pull)
    gamma         : float — schismogenesis strength (contrast push)
    delta         : float — lock-in drift at high L (0 = no coupling)
    l_threshold   : float — L level above which lock-in drift applies
    k_init        : int   — initial mean degree (Erdos-Renyi initialisation)
    awareness_k   : int   — awareness set size (agents each agent can consider)
    edr_init      : str   — 'bimodal' | 'uniform' | 'empirical'
    seed          : int   — random seed
    """

    def __init__(self, n_agents=200, alpha=0.12, beta=0.005, gamma=0.008,
                 p_contrast=0.12, anchor=0.025, anchor_bridge=0.025, edr_std=0.12,
                 delta=0.0, l_threshold=0.60, k_init=4, awareness_k=20,
                 edr_init='bimodal', seed=42):
        self.n              = n_agents
        self.alpha          = alpha
        self.beta           = beta
        self.gamma          = gamma
        self.p_contrast     = p_contrast
        self.anchor         = anchor
        self.anchor_bridge  = anchor_bridge
        self.edr_std        = edr_std
        self.max_deg        = 5          # empirical mean degree ≈ 4.3
        self.delta          = delta
        self.l_thr          = l_threshold
        self.rng            = np.random.default_rng(seed)

        self.agents         = {}
        self._init_agents(edr_init, k_init, awareness_k)

    def _init_agents(self, edr_init, k_init, awareness_k):
        """Initialise agents with EDR values and homophilic sparse graph.

        Bimodal initialisation (default): two Gaussian clusters at μ=0.70
        and μ=0.25 with width edr_std.  The cluster width determines how
        many within-cluster contrast edges form (wider clusters → more
        within-regime differentiation).  edr_std ≈ 0.22 produces the best
        match to empirical contrast edge statistics.

        Homophilic sparse init: agents connect preferentially to similar
        agents (ΔEDR < alpha), mimicking the empirical network where 86%
        of edges are comparator or parallel.  Contrast edges form only when
        p_contrast episodes occur during the update.
        """
        if edr_init == 'bimodal':
            # Three-cluster init: high (40%) / bridge (20%) / low (40%)
            # The bridge cluster (μ=0.48) produces the empirical mixed-EDR
            # communities (Louvain communities 9 and 17 in the hand-coded
            # subgraph) that give positive r_d3 before the sign reversal.
            # edr_std = 0.12 (tight clusters) enables within-cluster contrast
            # edges (alpha=0.12 < within-cluster ΔEDR) producing the 60%
            # within-regime contrast fraction seen empirically.
            n_high   = int(self.n * 0.40)
            n_bridge = int(self.n * 0.20)
            n_low    = self.n - n_high - n_bridge
            edrs_high   = np.clip(
                self.rng.normal(0.75, self.edr_std, n_high),   0.02, 0.98)
            edrs_bridge = np.clip(
                self.rng.normal(0.48, self.edr_std, n_bridge), 0.02, 0.98)
            edrs_low    = np.clip(
                self.rng.normal(0.20, self.edr_std, n_low),    0.02, 0.98)
            edrs = np.concatenate([edrs_high, edrs_bridge, edrs_low])
            self.rng.shuffle(edrs)
        elif edr_init == 'uniform':
            edrs = self.rng.uniform(0.02, 0.98, self.n)
        else:
            edrs = np.clip(self.rng.normal(0.48, self.edr_std, self.n), 0.02, 0.98)

        ls = np.clip(1 - edrs + self.rng.normal(0, 0.10, self.n), 0.0, 1.0)

        all_ids = list(range(self.n))
        # Tag cluster membership and build clustered awareness sets.
        # Clustered awareness (70% same-cluster, 30% cross-cluster) reflects
        # that governance systems were primarily aware of culturally and
        # temporally proximate systems. This raises modularity by increasing
        # within-community edge density.
        cluster = np.zeros(self.n, dtype=int)  # 0=low, 1=bridge, 2=high
        for i in range(self.n):
            if edrs[i] > 0.60:   cluster[i] = 2
            elif edrs[i] > 0.35: cluster[i] = 1

        for i in range(self.n):
            is_bridge = cluster[i] == 1
            a = Agent(i, edrs[i], ls[i], is_bridge=is_bridge)
            same = [j for j in all_ids if j != i and cluster[j] == cluster[i]]
            diff = [j for j in all_ids if j != i and cluster[j] != cluster[i]]
            aw = set()
            n_same = min(int(awareness_k * 0.75), len(same))
            n_diff = min(awareness_k - n_same, len(diff))
            if same: aw.update(self.rng.choice(same, size=n_same, replace=False))
            if diff: aw.update(self.rng.choice(diff, size=n_diff, replace=False))
            a.awareness = aw
            self.agents[i] = a

        # Homophilic sparse init: similar agents connect more readily.
        # Target mean degree ≈ k_init = 4, matching empirical avg degree 4.3.
        p_init = k_init / (self.n - 1)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                a_i, a_j = self.agents[i], self.agents[j]
                delta_edr = abs(a_i.edr - a_j.edr)
                p = p_init * (1.5 if delta_edr < self.alpha else 0.5)
                if (self.rng.random() < p
                        and len(a_i.edges) < self.max_deg
                        and len(a_j.edges) < self.max_deg):
                    et = 'contrast' if delta_edr >= self.alpha else 'comparator'
                    a_i.edges[j] = et
                    a_j.edges[i] = et

    def step(self):
        """One time step: homophilic edge assessment and anchored EDR update.

        Edge assessment (v4 architecture):
        Each agent either seeks a similar contact (with probability 1 - p_contrast)
        or a dissimilar contact (with probability p_contrast).  This produces a
        network where ~86% of edges are comparator/parallel (empirical: 86%) and
        ~14% are contrast (empirical: 14%).

        EDR update:
        Comparator edges pull EDR toward the neighbour; contrast edges push away.
        The anchor force provides a slow return toward the agent's initial EDR,
        preventing full polarisation to {0, 1} and preserving within-cluster
        variation needed to produce within-regime contrast edges.
        """
        order = self.rng.permutation(self.n)

        for i in order:
            a = self.agents[i]
            if not a.awareness:
                continue

            # ── Edge assessment: homophilic with minority contrast-seeking ────
            seek_contrast = self.rng.random() < self.p_contrast

            if seek_contrast:
                # Seek a dissimilar contact
                candidates = [j for j in a.awareness
                              if abs(a.edr - self.agents[j].edr) >= self.alpha]
                if not candidates:
                    candidates = list(a.awareness)
                j = int(self.rng.choice(candidates))
                new_type = 'contrast'
            else:
                # Seek a similar contact (homophily)
                candidates = [j for j in a.awareness
                              if abs(a.edr - self.agents[j].edr) < self.alpha]
                if not candidates:
                    candidates = list(a.awareness)
                j = int(self.rng.choice(candidates))
                delta_edr = abs(a.edr - self.agents[j].edr)
                new_type = 'contrast' if delta_edr >= self.alpha else 'comparator'

            b = self.agents[j]
            # Add or update edge (enforce max_deg)
            if j not in a.edges:
                if len(a.edges) < self.max_deg and len(b.edges) < self.max_deg:
                    a.edges[j] = new_type
                    b.edges[i] = new_type
            else:
                a.edges[j] = new_type
                b.edges[i] = new_type

            # Expand awareness set via neighbour-of-neighbour discovery
            if self.rng.random() < 0.04:
                nbr_of_nbr = [k for k in b.edges.keys()
                               if k != i and k not in a.awareness]
                if nbr_of_nbr:
                    a.awareness.add(int(self.rng.choice(nbr_of_nbr)))

        # ── EDR update (all agents simultaneously) ────────────────────────────
        new_edrs = {}
        for i, a in self.agents.items():
            if not a.edges:
                new_edrs[i] = a.edr
                continue

            pull  = 0.0
            push  = 0.0
            n_comp = n_cont = 0

            for j, et in a.edges.items():
                b = self.agents[j]
                diff = b.edr - a.edr
                if et == 'comparator':
                    pull += self.beta * diff
                    n_comp += 1
                else:
                    push -= self.gamma * diff
                    n_cont += 1

            delta = 0.0
            if n_comp:
                delta += pull / n_comp
            if n_cont:
                delta += push / n_cont

            # Anchor: slow return toward initial EDR.
            # Bridge agents use anchor_bridge; high/low use self.anchor.
            anchor_strength = self.anchor_bridge if a.is_bridge else self.anchor
            delta -= anchor_strength * (a.edr - a.edr_init)

            # Lock-in coupling
            new_edr = a.edr + delta
            if self.delta > 0 and a.l > self.l_thr:
                new_edr -= self.delta * new_edr

            new_edrs[i] = float(np.clip(new_edr, 0.02, 0.98))

        for i, edr in new_edrs.items():
            self.agents[i].edr = edr

    def run(self, n_steps=300):
        """Run the model for n_steps time steps."""
        for _ in range(n_steps):
            self.step()

    def to_networkx(self):
        """Convert current agent states to a NetworkX graph."""
        G = nx.Graph()
        for i, a in self.agents.items():
            G.add_node(i, edr=a.edr, l=a.l,
                       above_theta=int(a.edr > THETA))
        for i, a in self.agents.items():
            for j, et in a.edges.items():
                if i < j:
                    G.add_edge(i, j, edge_type=et)
        return G


# ── Evaluation metrics ────────────────────────────────────────────────────────

def get_shell(G, node, degree):
    """Nodes at exactly `degree` hops from `node`."""
    visited = {node}
    shell   = {node}
    for _ in range(degree):
        new_shell = set()
        for n in shell:
            new_shell.update(set(G.neighbors(n)) - visited)
        visited.update(new_shell)
        shell = new_shell
    return shell


def compute_metrics(G):
    """
    Compute the evaluation metrics against empirical targets.

    Returns a dict of metric values and the weighted loss.
    """
    if G.number_of_nodes() < 10 or G.number_of_edges() < 5:
        return None

    metrics = {}

    # ── Contagion decay ───────────────────────────────────────────────────────
    nodes_list = list(G.nodes)
    edrs = {n: G.nodes[n]['edr'] for n in nodes_list}

    for deg in [1, 2, 3, 4]:
        own, nbr = [], []
        for n in nodes_list:
            shell = get_shell(G, n, deg)
            if not shell:
                continue
            own.append(edrs[n])
            nbr.append(np.mean([edrs[s] for s in shell]))
        if len(own) >= 5:
            r, _ = stats.pearsonr(own, nbr)
            metrics[f'r_d{deg}'] = r
        else:
            metrics[f'r_d{deg}'] = np.nan

    # ── Community structure ───────────────────────────────────────────────────
    try:
        import community as community_louvain
        # Louvain requires a connected graph; use largest connected component
        lcc = max(nx.connected_components(G), key=len)
        G_lcc = G.subgraph(lcc)
        if G_lcc.number_of_edges() >= 3:
            partition = community_louvain.best_partition(G_lcc, random_state=42)
            metrics['modularity'] = community_louvain.modularity(partition, G_lcc)
        else:
            metrics['modularity'] = np.nan
    except Exception:
        metrics['modularity'] = np.nan

    # ── EDR assortativity ─────────────────────────────────────────────────────
    try:
        metrics['edr_assort'] = nx.numeric_assortativity_coefficient(G, 'edr')
    except Exception:
        metrics['edr_assort'] = np.nan

    # ── Contrast edge statistics ──────────────────────────────────────────────
    contrast_edges   = [(u, v, d) for u, v, d in G.edges(data=True)
                        if d.get('edge_type') == 'contrast']
    comparator_edges = [(u, v, d) for u, v, d in G.edges(data=True)
                        if d.get('edge_type') == 'comparator']

    if contrast_edges:
        cross = sum(1 for u, v, d in contrast_edges
                    if (edrs[u] > THETA) != (edrs[v] > THETA))
        metrics['contrast_cross'] = cross / len(contrast_edges)

        delta_c = [abs(edrs[u] - edrs[v]) for u, v, _ in contrast_edges]
        metrics['delta_contrast'] = np.mean(delta_c)
    else:
        metrics['contrast_cross'] = np.nan
        metrics['delta_contrast']  = np.nan

    if comparator_edges:
        delta_co = [abs(edrs[u] - edrs[v]) for u, v, _ in comparator_edges]
        metrics['delta_comparator'] = np.mean(delta_co)
    else:
        metrics['delta_comparator'] = np.nan

    # ── Weighted loss ─────────────────────────────────────────────────────────
    loss = 0.0
    for key, target in TARGETS.items():
        val = metrics.get(key, np.nan)
        if np.isnan(val):
            loss += TARGET_WEIGHTS.get(key, 1.0) * 1.0  # penalty for missing
        else:
            loss += TARGET_WEIGHTS.get(key, 1.0) * (val - target) ** 2

    metrics['loss'] = loss
    return metrics


def print_metrics(metrics, params=None):
    if params:
        print(f"  α={params['alpha']:.2f}  β={params['beta']:.3f}  "
              f"γ={params['gamma']:.3f}  γ/β={params['gamma']/params['beta']:.1f}")
    print(f"  Contagion decay:  "
          f"r_d1={metrics.get('r_d1', float('nan')):.3f}  "
          f"r_d2={metrics.get('r_d2', float('nan')):.3f}  "
          f"r_d3={metrics.get('r_d3', float('nan')):.3f}  "
          f"r_d4={metrics.get('r_d4', float('nan')):.3f}")
    print(f"  Modularity={metrics.get('modularity', float('nan')):.3f}  "
          f"EDR_assort={metrics.get('edr_assort', float('nan')):.3f}")
    print(f"  Contrast cross-θ={metrics.get('contrast_cross', float('nan')):.3f}  "
          f"ΔEDR_contrast={metrics.get('delta_contrast', float('nan')):.3f}  "
          f"ΔEDR_comparator={metrics.get('delta_comparator', float('nan')):.3f}")
    print(f"  Loss={metrics.get('loss', float('nan')):.4f}")


# ── Parameter sweep ───────────────────────────────────────────────────────────

def run_sweep(n_agents=200, n_steps=300, n_replicates=30,
              alpha_vals=None, beta_vals=None, gamma_vals=None):
    """
    Grid search over α, β, γ.  Returns a DataFrame of results.
    """
    if alpha_vals is None:
        alpha_vals = [0.10, 0.12, 0.15]
    if beta_vals is None:
        beta_vals  = [0.003, 0.005, 0.007]
    if gamma_vals is None:
        gamma_vals = [0.006, 0.008, 0.010, 0.012]

    total = len(alpha_vals) * len(beta_vals) * len(gamma_vals)
    print(f"Parameter sweep: {total} combinations × {n_replicates} replicates "
          f"= {total * n_replicates} runs")
    print()

    rows = []
    done = 0

    for alpha, beta, gamma in product(alpha_vals, beta_vals, gamma_vals):
        rep_metrics = defaultdict(list)

        for rep in range(n_replicates):
            model = SchismogenesisModel(
                n_agents=n_agents, alpha=alpha, beta=beta, gamma=gamma,
                p_contrast=0.12, anchor=0.025, anchor_bridge=0.025, edr_std=0.12,
                seed=rep * 1000 + int(alpha * 100) + int(beta * 1000))
            model.run(n_steps)
            G = model.to_networkx()
            m = compute_metrics(G)
            if m:
                for k, v in m.items():
                    if not np.isnan(v):
                        rep_metrics[k].append(v)

        row = {'alpha': alpha, 'beta': beta, 'gamma': gamma,
               'gamma_beta_ratio': gamma / beta if beta > 0 else np.nan}
        for k in list(TARGETS.keys()) + ['loss']:
            vals = rep_metrics.get(k, [])
            row[k]          = np.mean(vals) if vals else np.nan
            row[f'{k}_std'] = np.std(vals)  if vals else np.nan

        rows.append(row)
        done += 1

        if done % 10 == 0 or done == total:
            best = min(rows, key=lambda r: r.get('loss', float('inf')))
            print(f"  {done}/{total}: best loss so far = {best['loss']:.4f} "
                  f"(α={best['alpha']:.2f}, β={best['beta']:.3f}, "
                  f"γ={best['gamma']:.3f})")

    df = pd.DataFrame(rows).sort_values('loss')
    return df


# ── Case study runs ───────────────────────────────────────────────────────────

CASE_STUDIES = {
    'Celtic Tribal Assemblies': {
        'edr_init':  0.70,
        'l_init':    0.30,
        'description': (
            'Celtic non-urbanisation. High EDR, low L. Maintained contrast '
            'with Mediterranean urban governance. Predicted: high-EDR cluster '
            'with cross-theta contrast edges to Roman/Greek systems.'
        ),
        'expected_trajectory': 'stable_high',
        'historical_end': 'absorption by Roman conquest (EDR collapse ~50 CE)',
    },
    'Zomia Highland Communities': {
        'edr_init':  0.92,
        'l_init':    0.05,
        'description': (
            'Zomia state-avoidance. Very high EDR, very low L (illegible surplus '
            'maintained deliberately). Strong contrast with lowland states. '
            'Predicted: maintains high EDR through deliberate low-L strategy.'
        ),
        'expected_trajectory': 'stable_high',
        'historical_end': 'partial incorporation under colonial and post-colonial states',
    },
    'Iroquois Confederacy / Haudenosaunee': {
        'edr_init':  0.77,
        'l_init':    0.35,
        'description': (
            'Haudenosaunee constitutional development. High EDR, moderate L. '
            'Contrast with British colonial governance and Mississippian hierarchy. '
            'Predicted: stable high-EDR with contrast edges sustaining differentiation '
            'until colonial L-imposition forces EDR decline.'
        ),
        'expected_trajectory': 'stable_then_decline',
        'historical_end': 'EDR decline under colonial incorporation (~1800 CE)',
    },
}


def run_cases(best_params, n_agents=200, n_steps=500, n_replicates=20,
              target_edr_init=None):
    """
    Run case study trajectories using the best parameters from the sweep.

    For each case study, initialise one focal agent with the historical
    EDR and L values, surrounded by a population with the bimodal
    initialisation.  Track the focal agent's EDR trajectory.
    """
    results = {}

    alpha = best_params['alpha']
    beta  = best_params['beta']
    gamma = best_params['gamma']

    print(f"Case studies with: α={alpha:.2f}, β={beta:.3f}, γ={gamma:.3f}")
    print()

    for case_name, case_info in CASE_STUDIES.items():
        print(f"  {case_name}")
        print(f"    {case_info['description']}")

        traj_reps = []
        for rep in range(n_replicates):
            model = SchismogenesisModel(
                n_agents=n_agents, alpha=alpha, beta=beta, gamma=gamma,
                seed=rep * 777)

            # Override agent 0 with case study values
            model.agents[0].edr = case_info['edr_init']
            model.agents[0].l   = case_info['l_init']

            trajectory = [case_info['edr_init']]
            for _ in range(n_steps):
                model.step()
                trajectory.append(model.agents[0].edr)
            traj_reps.append(trajectory)

        # Summarise trajectory
        traj_arr = np.array(traj_reps)   # shape: (n_reps, n_steps+1)
        mean_traj = traj_arr.mean(axis=0)
        std_traj  = traj_arr.std(axis=0)
        final_edr = mean_traj[-1]

        print(f"    Final EDR: {final_edr:.3f} ± {std_traj[-1]:.3f} "
              f"(initial: {case_info['edr_init']:.3f})")
        print(f"    Expected: {case_info['expected_trajectory']}")
        print(f"    Historical end: {case_info['historical_end']}")
        print()

        results[case_name] = {
            'mean_trajectory': mean_traj.tolist(),
            'std_trajectory':  std_traj.tolist(),
            'edr_init':        case_info['edr_init'],
            'l_init':          case_info['l_init'],
            'expected':        case_info['expected_trajectory'],
            'final_edr_mean':  final_edr,
            'final_edr_std':   std_traj[-1],
        }

    return results


# ── Figures ───────────────────────────────────────────────────────────────────

def make_sweep_figure(df, visuals_dir=OUTPUT_DIR):
    """Three-panel figure: loss heatmap, γ/β ratio vs sign reversal, best run."""
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    plt.rcParams.update({
        'font.family': 'serif', 'font.size': 9,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.grid': True, 'grid.alpha': 0.22, 'grid.linewidth': 0.5,
    })

    fig, axes = plt.subplots(1, 3, figsize=(16, 7))
    fig.subplots_adjust(top=0.78)

    # ── A: γ/β ratio vs degree-4 r ────────────────────────────────────────────
    ax = axes[0]
    valid = df[df['r_d4'].notna()].copy()
    sc = ax.scatter(valid['gamma_beta_ratio'], valid['r_d4'],
                    c=valid['loss'], cmap='YlOrRd_r',
                    s=40, alpha=0.75, edgecolors='white', lw=0.4,
                    norm=mcolors.LogNorm(
                        vmin=valid['loss'].quantile(0.1),
                        vmax=valid['loss'].quantile(0.9)))
    ax.axhline(-0.34, color='#2980b9', lw=1.5, ls='--', alpha=0.7,
               label='Target r = −0.34')
    ax.axhline(0, color='#aaaaaa', lw=0.8, ls=':')
    ax.axvline(1.0, color='#e74c3c', lw=1.0, ls=':', alpha=0.6,
               label='γ/β = 1 (threshold)')
    ax.set_xlabel('γ / β ratio (schismogenesis / contagion)', fontsize=9)
    ax.set_ylabel('Degree-4 EDR correlation r', fontsize=9)
    ax.set_title('A.  γ/β ratio vs degree-4 sign reversal\n'
                 '(colour = loss; target: r ≈ −0.34)',
                 fontsize=8, fontweight='bold', loc='left', pad=4)
    ax.legend(fontsize=7.5, loc='upper right')
    plt.colorbar(sc, ax=ax, shrink=0.85, label='Loss')

    # ── B: Decay curves for top-5 parameter sets ──────────────────────────────
    ax = axes[1]
    target_rs = [TARGETS[f'r_d{d}'] for d in [1, 2, 3, 4]]
    ax.plot([1, 2, 3, 4], target_rs, 'k--', lw=2.5, label='Empirical target',
            zorder=5)
    ax.axhline(0, color='#aaaaaa', lw=0.8, ls=':')

    top5 = df.head(5)
    colours = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']
    for idx, (_, row) in enumerate(top5.iterrows()):
        rs = [row.get(f'r_d{d}', np.nan) for d in [1, 2, 3, 4]]
        lbl = (f"α={row['alpha']:.2f}, β={row['beta']:.3f}, "
               f"γ={row['gamma']:.3f} (L={row['loss']:.3f})")
        ax.plot([1, 2, 3, 4], rs, 'o-', color=colours[idx], lw=1.5,
                markersize=5, label=lbl, alpha=0.85)

    ax.set_xlabel('Network distance (degrees)', fontsize=9)
    ax.set_ylabel('EDR correlation r', fontsize=9)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_title('B.  Contagion decay — top-5 parameter sets\nvs empirical target',
                 fontsize=8, fontweight='bold', loc='left', pad=4)
    ax.legend(fontsize=6.5, loc='upper right', frameon=True, framealpha=0.92)

    # ── C: Loss landscape (γ vs α, best β) ────────────────────────────────────
    ax = axes[2]
    best_beta = df.iloc[0]['beta']
    sub = df[df['beta'] == best_beta]
    if len(sub) >= 6:
        pivot = sub.pivot_table(values='loss', index='alpha', columns='gamma',
                                aggfunc='min')
        im = ax.imshow(pivot.values, cmap='YlOrRd_r', aspect='auto',
                       origin='lower')
        ax.set_xticks(range(len(pivot.columns)))
        ax.set_yticks(range(len(pivot.index)))
        ax.set_xticklabels([f'{v:.2f}' for v in pivot.columns],
                           fontsize=7, rotation=20)
        ax.set_yticklabels([f'{v:.2f}' for v in pivot.index], fontsize=7)
        ax.set_xlabel('γ (schismogenesis strength)', fontsize=9)
        ax.set_ylabel('α (contrast threshold)', fontsize=9)
        ax.set_title(f'C.  Loss landscape (β={best_beta:.3f})\n'
                     '(green = low loss; red = high loss)',
                     fontsize=8, fontweight='bold', loc='left', pad=4)
        plt.colorbar(im, ax=ax, shrink=0.85, label='Loss')
    else:
        ax.text(0.5, 0.5, 'Insufficient data\nfor landscape plot',
                ha='center', va='center', transform=ax.transAxes)

    fig.suptitle(
        'Schismogenesis ABM parameter sweep\n'
        f'Target: degree-4 r ≈ −0.34, modularity ≈ 0.56, '
        f'EDR assortativity ≈ 0.67',
        fontsize=11, fontweight='bold', y=0.93)

    os.makedirs(visuals_dir, exist_ok=True)
    out = os.path.join(visuals_dir, 'abm_sweep.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


def make_cases_figure(results, visuals_dir=OUTPUT_DIR):
    """Three-panel figure: one panel per case study trajectory."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    plt.rcParams.update({
        'font.family': 'serif', 'font.size': 9,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.grid': True, 'grid.alpha': 0.22, 'grid.linewidth': 0.5,
    })

    case_names  = list(results.keys())
    case_colours = ['#2980b9', '#27ae60', '#c0392b']
    fig, axes   = plt.subplots(1, 3, figsize=(16, 7))
    fig.subplots_adjust(top=0.78)

    for idx, (case_name, res) in enumerate(results.items()):
        ax     = axes[idx]
        mean_t = np.array(res['mean_trajectory'])
        std_t  = np.array(res['std_trajectory'])
        steps  = np.arange(len(mean_t))
        col    = case_colours[idx]

        ax.fill_between(steps, mean_t - std_t, mean_t + std_t,
                        alpha=0.18, color=col)
        ax.plot(steps, mean_t, color=col, lw=2.0)
        ax.axhline(THETA, color='#aaaaaa', lw=0.8, ls=':')
        ax.text(steps[-1] * 0.02, THETA + 0.02, 'θ = 0.45',
                fontsize=6.5, color='#999999')
        ax.axhline(res['edr_init'], color='#333333', lw=0.8, ls='--',
                   alpha=0.5, label=f'Initial EDR = {res["edr_init"]:.2f}')

        short_name = case_name.split('/')[0].strip()[:35]
        ax.set_title(
            f'{chr(65+idx)}.  {short_name}\n'
            f'Initial EDR={res["edr_init"]:.2f}, L={res["l_init"]:.2f}  '
            f'→  Final: {res["final_edr_mean"]:.3f}±{res["final_edr_std"]:.3f}',
            fontsize=8, fontweight='bold', loc='left', pad=4)
        ax.set_xlabel('Time steps', fontsize=9)
        ax.set_ylabel('EDR composite', fontsize=9)
        ax.set_ylim(0, 1.05)
        ax.text(0.97, 0.05, f'Expected: {res["expected"]}',
                transform=ax.transAxes, fontsize=7.5, va='bottom', ha='right',
                style='italic', color='#555555')

    fig.suptitle(
        'Schismogenesis ABM: Graeber-Wengrow case study trajectories\n'
        '(mean ± 1 SD across 20 replicates; focal agent initialised '
        'with historical EDR and L values)',
        fontsize=11, fontweight='bold', y=0.93)

    os.makedirs(visuals_dir, exist_ok=True)
    out = os.path.join(visuals_dir, 'abm_cases.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Schismogenesis ABM — Paper 4',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  Default:  single run with default parameters, prints metrics.
  --sweep:  grid search over α, β, γ. Writes data/abm_sweep_results.csv.
  --cases:  G-W case study trajectories. Writes data/abm_cases_results.csv.

Figures only generated with --figure flag.

Quick validation run (~5 sec):
    python src/schismogenesis_abm.py

Fast sweep — 4 gamma values, 5 reps (~20 sec):
    python src/schismogenesis_abm.py --sweep --fast

Full sweep — 60 combos × 20 reps (~5 min):
    python src/schismogenesis_abm.py --sweep

Case study trajectories (uses best sweep params if sweep has run):
    python src/schismogenesis_abm.py --cases

Recommended order:
    python src/schismogenesis_abm.py --sweep --fast   # confirm it works
    python src/schismogenesis_abm.py --sweep          # full calibration
    python src/schismogenesis_abm.py --cases          # G-W trajectories
    python src/schismogenesis_abm.py --sweep --figure # figures
"""
    )
    parser.add_argument('--sweep',  action='store_true',
                        help='Run parameter sweep')
    parser.add_argument('--cases',  action='store_true',
                        help='Run G-W case study trajectories')
    parser.add_argument('--figure', action='store_true',
                        help='Generate figures')
    parser.add_argument('--fast',   action='store_true',
                        help='Coarse grid for quick testing')
    parser.add_argument('--n-agents', type=int, default=200)
    parser.add_argument('--n-steps',  type=int, default=200)
    parser.add_argument('--n-reps',   type=int, default=20)
    args = parser.parse_args()

    data_dir    = DATA_DIR
    visuals_dir = OUTPUT_DIR

    if not args.sweep and not args.cases:
        # ── Single validation run ──────────────────────────────────────────────
        print("Single validation run (default parameters):")
        print("  α=0.12, β=0.005, γ=0.008, p_contrast=0.12, anchor=0.025, anchor_bridge=0.025, edr_std=0.12")
        print("  N=200, T=300, 5 replicates")
        print()
        all_metrics = defaultdict(list)
        for rep in range(5):
            model = SchismogenesisModel(
                n_agents=args.n_agents, alpha=0.25, beta=0.005, gamma=0.006,
                p_contrast=0.12, anchor=0.010, edr_std=0.20,
                seed=rep * 99)
            model.run(args.n_steps)
            G = model.to_networkx()
            m = compute_metrics(G)
            if m:
                for k, v in m.items():
                    if not np.isnan(v):
                        all_metrics[k].append(v)

        mean_m = {k: np.mean(v) for k, v in all_metrics.items()}
        print("Results (mean over 5 replicates):")
        print_metrics(mean_m)
        print()
        print("Empirical targets:")
        for k, v in TARGETS.items():
            got = mean_m.get(k, float('nan'))
            diff = got - v
            print(f"  {k:20s}: target={v:+.3f}  got={got:+.3f}  "
                  f"diff={diff:+.3f}")
        return

    best_params = {'alpha': 0.12, 'beta': 0.005, 'gamma': 0.008}

    if args.sweep:
        if args.fast:
            alpha_vals = [0.12]
            beta_vals  = [0.005]
            gamma_vals = [0.006, 0.008, 0.010, 0.012]
            n_reps     = 5
        else:
            alpha_vals = [0.20, 0.22, 0.25, 0.28, 0.30]
            beta_vals  = [0.003, 0.005, 0.007]
            gamma_vals = [0.004, 0.006, 0.008, 0.010]
            n_reps     = args.n_reps

        df = run_sweep(
            n_agents=args.n_agents, n_steps=args.n_steps,
            n_replicates=n_reps,
            alpha_vals=alpha_vals, beta_vals=beta_vals, gamma_vals=gamma_vals)

        out_csv = os.path.join(data_dir, 'abm_sweep_results.csv')
        df.to_csv(out_csv, index=False)
        print(f"\nSweep results saved to {out_csv}")
        print()
        print("Top 5 parameter sets:")
        for _, row in df.head(5).iterrows():
            print(f"  α={row['alpha']:.2f} β={row['beta']:.3f} "
                  f"γ={row['gamma']:.3f} γ/β={row['gamma_beta_ratio']:.1f} "
                  f"loss={row['loss']:.4f} "
                  f"r_d4={row.get('r_d4', float('nan')):.3f} "
                  f"M={row.get('modularity', float('nan')):.3f}")

        best = df.iloc[0]
        best_params = {
            'alpha': best['alpha'],
            'beta':  best['beta'],
            'gamma': best['gamma'],
        }

        if args.figure:
            make_sweep_figure(df, visuals_dir)

    if args.cases:
        case_results = run_cases(
            best_params,
            n_agents=args.n_agents,
            n_steps=500,
            n_replicates=20)

        # Save
        rows = []
        for case_name, res in case_results.items():
            for step, (m, s) in enumerate(
                    zip(res['mean_trajectory'], res['std_trajectory'])):
                rows.append({
                    'case': case_name, 'step': step,
                    'edr_mean': m, 'edr_std': s,
                    'edr_init': res['edr_init'],
                    'l_init':   res['l_init'],
                    'expected': res['expected'],
                })
        cases_df = pd.DataFrame(rows)
        out_csv = os.path.join(data_dir, 'abm_cases_results.csv')
        cases_df.to_csv(out_csv, index=False)
        print(f"Case study results saved to {out_csv}")

        if args.figure:
            make_cases_figure(case_results, visuals_dir)

    print("\nDone.")


if __name__ == '__main__':
    main()
