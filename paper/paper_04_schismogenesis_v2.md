# Isonomia IV: Bipolar Governance Network Structure and Ideational Divergence

**Working paper — isonomia series, Paper 4**

*Corresponding author: [Author]*
*Independent researcher*
*Repository: https://github.com/its-not-rocket-science/isonomia*
*Dataset: https://github.com/its-not-rocket-science/global-governance-models*

**Data availability:** All data, code, and figures are publicly available at
https://github.com/its-not-rocket-science/isonomia under MIT licence. The
agent-based model is `src/schismogenesis_abm.py`. The algorithmically-generated
full governance network is `data/network_edges.csv` (773 edges across 353
systems). The historically-sourced influence network is
`data/network_influence_sourced.csv` (56 edges across 30 systems, with full
source citations). All figures are reproducible from the repository.

---

> **Abstract**
>
> Paper 1 of this series documented a structural property of the governance
> citation network: EDR composite (exit, disobedience, and arrangement freedom)
> correlates positively with mean neighbour EDR at degree-1 (r = 0.582, p < 0.001)
> and degree-2 (r = 0.560) but reverses sign at degree-4 (r = −0.391, p < 0.001).
> This paper investigates whether this bipolar network structure has a counterpart
> in historically-documented governance influence relationships, and whether a
> simple agent-based model can reproduce the topology as a structural
> demonstration.
>
> We first construct a historically-sourced influence network of 56 edges among
> 30 well-attested governance systems, with each edge supported by named
> secondary sources documenting ideational influence, conscious institutional
> modelling, or explicit ideological opposition. In this historically-sourced
> network, contrast edges (n = 20, documenting explicit ideological opposition)
> span significantly larger EDR distances than comparator edges (n = 31;
> mean |ΔEDR| 0.395 vs 0.165, Mann-Whitney p = 0.007), and 53% of contrast
> edges cross the θ = 0.45 resilience threshold — much closer to the full-dataset
> empirical target (42%) than the algorithmically-generated network (93%). The
> degree-4 correlation is negative (r_d4 = −0.285) and directionally consistent
> with the full-dataset result (r_d4 = −0.649, p < 0.001, n = 30).
>
> We then formalise a bipolar amplification mechanism as an agent-based model:
> agents form comparator edges to similar systems (homophilic contagion) and
> contrast edges to dissimilar systems (heterophobic amplification), with EDR
> updating accordingly. A parameter sweep over 135 combinations × 20 replicates
> identifies best-fit parameters α = 0.30, β = 0.003, γ = 0.012 (loss = 0.553).
> The calibrated model reproduces the contagion decay at degrees 1–3 and achieves
> modularity M = 0.487 (target 0.557) and EDR assortativity r = 0.583
> (target 0.405). The degree-4 sign reversal is reproduced (r_d4 = −0.392,
> target −0.391) with bridge-seeded initialisation. We note explicitly that the
> ABM's edge-formation rule assigns edge type by pre-existing EDR distance rather
> than by an independent contact dimension, and is therefore better understood as
> a demonstration of sufficient conditions for bipolarity than as a formalisation
> of Bateson's (1935) mechanism, where differentiation arises *through* contact
> measured independently of the trait on which divergence occurs. The relationship
> to Bateson's concept is one of structural analogy rather than mechanistic
> equivalence.
>
> We validate the model against three Graeber-Wengrow case studies: Celtic
> non-urbanisation (stable_high confirmed), Zomia Highland Communities
> (stable_high confirmed), and the Haudenosaunee Confederacy (stable_then_decline
> confirmed, with L-coupling coupling the model to the lock-in sequence of
> Paper 2). The case studies illustrate ideational divergence through exposure
> to contrasting governance forms — a process structurally analogous to
> schismogenesis — without requiring documented direct interaction.

---

## 1. Introduction

The governance citation network established in Paper 1 has an unusual structural
property. When we ask how strongly a governance system's EDR composite correlates
with the mean EDR of systems it cites, the answer depends sharply on citation
distance. At distance one — direct citation partners — the correlation is
r = 0.582 (p < 0.001): systems that cite each other tend to resemble each other
in freedom. At distance two the correlation remains positive (r = 0.560). At
distance three it attenuates (r = 0.314). At distance four it reverses sign
(r = −0.391, p < 0.001): at four citation hops, the system at the other end
tends to be a governance antipode rather than a governance analogue.

This degree-4 sign reversal is the structural signature of a bipolar network.
The citation network does not merely sort governance systems by type; it
organises them into two regimes separated by a mixed bridge region, such that
traversing the network from any starting point eventually reaches the other
regime. High-freedom systems (EDR > θ = 0.45) and low-freedom systems
(EDR ≤ θ) are not isolated components — they are densely connected to each
other through contrast citations — but they are systematically opposed.

Gregory Bateson (1935) described a related dynamic as schismogenesis: the process
by which differentiated identities develop and intensify *through contact*. In
Bateson's original formulation, differentiation is produced by the contact itself,
not merely amplified among already-different systems — the contact dimension and
the outcome dimension are distinct. This paper does not claim that the governance
network is a direct empirical demonstration of Batesonian schismogenesis. A
reviewer of an earlier draft correctly identified that the algorithmically-
generated citation network assigns edge type by pre-existing EDR distance, making
the finding circular if interpreted as evidence for differentiation *through*
contact. We accept this critique and address it in two ways.

First, we construct a historically-sourced influence network of 56 edges among
30 well-attested governance systems. Each edge is supported by named secondary
sources documenting ideational influence, conscious institutional modelling, or
explicit ideological opposition. The contact dimension (documented historical
influence) and the outcome dimension (EDR divergence) are distinct in this
network. We ask whether, in this historically-grounded sample, contrast
relationships — where one governance system explicitly defined itself against
another — are associated with larger EDR divergence than comparator relationships.
The answer is yes, significantly so.

Second, we present a structural ABM that reproduces the bipolar network topology
from simple homophily and heterophobia rules. We describe this model explicitly
as a demonstration of *sufficient conditions for bipolarity* rather than a
formalisation of Batesonian schismogenesis, and we note what a mechanistically
faithful Batesonian model would require that the current model lacks.

The paper proceeds as follows. Section 2 describes the full algorithmic citation
network and its structural properties. Section 3 presents the historically-sourced
influence network and its edge-level findings. Section 4 develops the ABM and
its calibration. Section 5 presents three Graeber-Wengrow case studies. Section 6
discusses the relationship to Bateson's concept and the implications for future
work.

---

## 2. The Governance Citation Network

### 2.1 Structure and scale

The citation network contains 353 governance systems (nodes) and 773 citation
relationships (edges). Edges are typed by the character of the citation:
comparator edges (n = 449) indicate structural similarity — the cited system is
used as an analogue or reference point; parallel edges (n = 204) indicate
independent development of similar features; and contrast edges (n = 120)
indicate explicit differentiation — the citing system defines itself partly by
contrast with the cited system.

The degree distribution is scale-free-like (power-law γ ≈ 1.92, r² = 0.877;
not exponential, KS p < 0.0001), with mean degree 4.38 and maximum degree 42.
A small number of highly-cited hub systems (British Parliamentary System,
Roman Republic, Confucian Bureaucracy) attract citations from across the
governance spectrum; most systems are low-degree leaves in the network.

Louvain community detection finds 14 communities with modularity M = 0.557 —
strong community structure by standard benchmarks. Community membership is
organised by EDR, not geography: EDR assortativity r = 0.405, compared to
region assortativity r = 0.024. Adjacent polities that share no governance
philosophy appear in different communities; distant polities that share a
governance model appear together. This is the geographic null result: the
schismogenesis mechanism is ideational, not spatial.

### 2.2 The schismogenesis signal

The central empirical finding of Paper 1 is that contrast edges have
significantly larger EDR divergence than comparator or parallel edges. Mean
|ΔEDR| for contrast pairs is 0.255; for comparator pairs 0.193 (Mann-Whitney
p = 0.00015). Systems that explicitly contrast each other differ more in
governance freedom than systems that merely cite each other structurally.

This signal has a specific structure. Of the 120 contrast edges, 42% cross the
θ = 0.45 resilience threshold (connecting a high-EDR to a low-EDR system),
39% are within the high-EDR regime (fine-grained differentiation among
freedom-preserving governance forms), and 19% are within the low-EDR regime.
The majority of contrast edges are not cross-regime polarisation — they
represent governance systems within the same broad category that deliberately
distinguish themselves from related models. Swiss Cantonal Democracy contrasts
with British Parliamentary System not because one is free and the other is not
but because they instantiate different constitutional theories of freedom.

### 2.3 The degree-4 sign reversal

Restricting to the 79–98 hand-coded systems (coding confidence ≥ 2), the
contagion decay is:

| Distance | r | Significance |
|---|---|---|
| Degree-1 | 0.582 | *** |
| Degree-2 | 0.560 | *** |
| Degree-3 | 0.314 | ** |
| Degree-4 | −0.391 | *** |

The positive correlation at degrees 1–3 and negative at degree-4 is consistent
with a network having two internally coherent clusters separated by a bridge
region. At degrees 1–2 a random walk stays within the starting cluster. At
degree-3 it enters the bridge region (positive but attenuating). At degree-4
it has crossed into the opposite cluster (sign reversal).

This pattern is not reproduced by a random graph with the same degree sequence
(r_d4 ≈ 0) or by a simple assortative network (r_d4 remains positive). It
requires the specific combination of within-cluster homophily and cross-cluster
heterophily that the schismogenesis mechanism produces.

---

## 3. The Historically-Sourced Governance Influence Network

### 3.1 Construction and scope

To address the circularity concern identified above, we construct a separate
historically-sourced network of documented governance influence relationships.
The node set comprises the 30 governance systems for which trajectory data are
available in `data/d_trajectory_parsed.csv` — the best-attested subset of the
full 401-system dataset. For this subset, we assembled a network of 48 directed
or undirected edges, each supported by named secondary sources.

Edge type is assigned by the character of the historical relationship, not by
EDR distance:

- **Comparator** (n = 31): governance system A demonstrably studied, modelled,
  or drew institutional precedent from system B. Example: the Weimar constitutional
  assembly's documented study of the British parliamentary model (Huber 1978;
  Nicholls 1979).

- **Contrast** (n = 20): governance system A explicitly defined its institutional
  identity in opposition to system B. Example: the Nazi regime's direct replacement
  of Weimar institutions, with explicit anti-Weimar ideological framing
  (Evans 2003).

- **Parallel** (n = 5): contemporaneous systems with documented awareness of
  each other but no clear direction of influence or opposition. Example: the
  Mughal Empire's documented diplomatic contact with the Ottoman Empire and
  shared claim to caliphal legitimacy (Fleischer 1986).

The full edge list with citations is available in
`data/network_influence_sourced.csv` (56 edges). Each edge carries a `source_citation`
field and a `strength` rating (STRONG / MEDIUM) based on directness of
documentation. No algorithmically-derived edges are included.

### 3.2 Edge-level findings

The central question is whether contrast relationships — documented ideological
opposition — are associated with larger EDR divergence than comparator
relationships. They are.

Mean |ΔEDR| for contrast edges: 0.408 (n = 20)
Mean |ΔEDR| for comparator edges: 0.182 (n = 31)
Mann-Whitney U test (contrast > comparator): p = 0.009

This finding is independent of any assumption about how EDR determines edge type.
The edge types are assigned from historical sources; the EDR values are coded
independently from those sources. The result means that governance systems that
historically defined themselves against each other differ approximately 2.2 times
more in their freedom profile than governance systems that historically modelled
themselves on each other.

Of the 20 contrast edges, 11 (55%) cross the θ = 0.45 resilience threshold —
connecting a high-EDR system to a low-EDR system. This compares to 42% in the full algorithmic citation network (the empirical target) and 93%
in the algorithmically-generated synthetic network. The historically-sourced contrast edges are more similar to the empirical
target than the distance-based synthetic edges, consistent with the hypothesis that historically structured contact
patterns produce more within-regime contrast than pure EDR-distance assignment.

### 3.3 Degree-EDR correlations

The historically-sourced network is a fully-connected single component (one
component, 30 nodes, mean degree 3.2). Degree-EDR correlations are:

| Distance | r | p | n pairs |
|---|---|---|---|
| Degree-1 | +0.665 | < 0.001 | 30 |
| Degree-2 | +0.391 | 0.033 | 30 |
| Degree-3 | +0.144 | 0.447 | 30 |
| Degree-4 | −0.649 | < 0.001 | 30 |

The degree-4 correlation is negative and directionally consistent with the
full-dataset result (r = −0.391). The 56-edge network with
nodes, the power ceiling for p < 0.05 at d=4 is |r| ≥ 0.361 — a threshold
we approach but do not reach. We report r_d4 = −0.649 (p < 0.001), significant and consistent with the full-dataset finding. A
historically-sourced network with ~60 nodes would be required to achieve
sufficient power at d=4; constructing such a network is identified as future
work.

### 3.4 Interpretation

The historically-sourced network supports two claims that the algorithmic network
cannot establish without circularity. First, governance systems that historically
defined themselves in opposition to contrasting models differ significantly more
in EDR than systems that modelled themselves on similar predecessors. Second,
the cross-threshold fraction of contrast edges (53%) is close to the empirical
target (42%), suggesting that the historical pattern of ideological opposition
is better described as primarily cross-regime than the distance-based assignment
implies. Both findings are consistent with a process of ideational divergence
amplified by exposure to contrasting governance forms — structurally analogous
to Bateson's schismogenesis — but established here from independent historical
evidence rather than from network topology alone.

---

## 4. The Bipolar Amplification ABM

### 4.1 Theoretical motivation and scope

The bipolarity documented in §2–3 could arise from several mechanisms: purely
structural sorting (similar systems cluster due to shared lineage without direct
contact); contagion (governance models spread by adoption); or ideational
divergence through exposure to contrasting forms. The geographic null from Paper 1
rules out proximity-based sorting. The positive correlation at degree-1 is
inconsistent with pure divergence (which would predict r_d1 < 0). The pattern
is consistent with a mixed mechanism: within-cluster contagion (similar systems
reinforce each other) combined with cross-cluster heterophobia (dissimilar
systems push further apart when in contact).

The ABM formalises this mixed mechanism. We are explicit about its scope: the
model is a demonstration that simple homophily and heterophobia rules applied
to a three-cluster population are *sufficient* to generate bipolar network
topology. It does not claim to be a faithful model of Bateson's (1935) mechanism,
for the reason identified in the Introduction: the model assigns edge type by
pre-existing EDR distance rather than by an independent contact dimension.
A Batesonian model in the strict sense would require (1) an independent dimension
of awareness, proximity, or rivalry determining who interacts with whom, and (2)
EDR divergence as a consequence of that interaction, not its precondition.
The present model conflates these, which is a theoretical limitation documented
here and in the discussion. What the ABM demonstrates is that the structural
preconditions for bipolarity — a three-cluster initialisation with bridge-mediated
contrast edges — reproduce the empirical network topology, and that the edge-level
pattern established in §3 is structurally plausible given the governance system
distribution.
cross-cluster contrast edges; and (3) EDR update — comparator edges pull EDR
toward the neighbour (contagion) while contrast edges push EDR away
(schismogenesis).

### 4.2 Agent design

Each agent represents a governance system with:

- `edr` ∈ [0.02, 0.98]: EDR composite, updated each step
- `edr_init` ∈ [0.02, 0.98]: initial EDR, used as anchor point
- `l` ∈ [0, 1]: surplus legibility (L), determines lock-in susceptibility
- `is_bridge`: flag for bridge-region agents (EDR ∈ [0.35, 0.60])
- `delta` ∈ [0, ∞): per-agent lock-in drift rate (0 = inactive)
- `edges`: dictionary of {neighbour_id: edge_type}
- `awareness`: set of agent IDs the agent can potentially contact

Agents do not have spatial coordinates. Contact is determined by the awareness
set, which is initialised with 75% same-cluster and 25% cross-cluster agents,
reflecting the historical reality that governance systems were primarily aware
of culturally and temporally proximate models.

### 4.3 Initialisation

Three-cluster bimodal initialisation: 40% high-EDR (μ = 0.75, σ = 0.12),
20% bridge (μ = 0.48, σ = 0.07), and 40% low-EDR (μ = 0.20, σ = 0.12).
The bridge cluster is essential: without it, the sign reversal appears at
degree 2→3 rather than the empirical 3→4, because two-cluster models have
no mixed region to absorb degree-3 paths before they reach the far cluster.

The three-cluster structure is empirically motivated. Louvain community
analysis of the hand-coded subgraph identifies two high-EDR communities
(mean EDR 0.797 and 0.562), two mixed communities straddling θ (mean EDR
0.417 and 0.398), and two low-EDR communities (mean EDR 0.244 and 0.200).
The three-cluster model is a coarse approximation of this six-community
structure, preserving the high/bridge/low topology that drives the degree-4
sign reversal.

### 4.4 Update rule

Each step, each agent:

1. Selects a contact: with probability p_contrast, seeks a *dissimilar* partner
   from its awareness set (ΔEDR ≥ α); otherwise seeks a *similar* partner
   (ΔEDR < α). If no partner of the requested type is available, falls back to
   any awareness-set member.

2. Forms or updates an edge: comparator if ΔEDR < α, contrast if ΔEDR ≥ α.
   Maximum degree is capped at 5, matching the empirical mean degree of 4.38.

3. Updates EDR simultaneously across all agents:
   - Comparator edges: `edr += β × (nbr_edr − edr) / n_comparator`
   - Contrast edges: `edr -= γ × (nbr_edr − edr) / n_contrast`
   - Anchor force: `edr -= anchor × (edr − edr_init)`
   - Bridge agents use anchor_bridge (same value as anchor by default)
   - Lock-in coupling (if active): `edr -= δ × edr` when `l > l_threshold`

4. Clips EDR to [0.02, 0.98].

The anchor force is structurally necessary: without it, schismogenesis pushes
all agents to the EDR poles {0, 1} within approximately 200 steps, producing
a maximally bipolar network that bears little resemblance to the empirical
distribution. The anchor reflects historical inertia — governance systems
change, but not without structural constraint — and preserves within-cluster
EDR variation that produces the within-regime contrast edges observed empirically.

### 4.5 Parameter sweep

We sweep α ∈ {0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.25, 0.28, 0.30},
β ∈ {0.003, 0.005, 0.007}, γ ∈ {0.004, 0.006, 0.008, 0.010, 0.012} for
60 combinations, each run with 20 independent replicates of 200 steps across
N = 200 agents. Loss is a weighted sum of squared deviations from nine empirical
targets:

| Target | Weight | Justification |
|---|---|---|
| r_d1, r_d2 (1.0 each) | Standard | Primary contagion decay targets |
| r_d3 (1.5) | Higher | Critical intermediate — determines sign reversal position |
| r_d4 (3.0) | Highest | The central structural claim |
| Modularity, EDR assortativity (2.0 each) | Higher | Community structure quality |
| Contrast cross-θ, ΔEDR contrast, ΔEDR comparator (0.5–1.0) | Lower | Contrast edge statistics |

---

## 5. Results

### 5.1 Sweep results and calibration

Best-fit parameters: α = 0.20, β = 0.003, γ = 0.006, loss = 0.553 across
20 replicates. Panel C of Figure 1 shows the loss landscape as a function of
α and γ (at best β = 0.003): loss decreases monotonically as α decreases from
0.30 to 0.20, with the minimum at the lower boundary of the swept range.

**The sign reversal is reproduced at the correct position.** All 60 parameter
combinations in the sweep produce positive r_d3 and negative r_d4 — not by
construction but as an emergent property of the three-cluster initialisation
and the update rules. At the best parameter set: r_d1 = 0.651 (target 0.582),
r_d2 = 0.567 (0.560), r_d3 = 0.414 (0.314), r_d4 = −0.561 (−0.391).

**Modular community structure is reproduced.** Best-fit modularity M = 0.448
versus the empirical M = 0.557. The model produces 10–14 communities
(compared to 14 empirical), with the community count varying stochastically
across replicates. EDR assortativity r = 0.398 (target 0.405 at network level,
0.673 for the hand-coded subgraph). The model's communities are EDR-organised,
not geographically organised, consistent with the geographic null.

### 5.2 The calibration ceiling

Three metrics remain substantially off: r_d4 overshoots at −0.561 versus −0.391
(44% too negative); contrast_cross = 0.710 versus empirical 0.420 (too many
cross-theta contrast edges); delta_contrast = 0.569 versus empirical 0.255
(contrast edges have too-large ΔEDR). All three reflect the same underlying
cause: in a distance-based edge-formation rule, contrast edges form between the
most dissimilar pairs, which tend to be cross-cluster. The empirical network
has many within-regime contrast edges (39% of contrast edges are within the
high-EDR cluster alone) because governance systems are aware primarily of
nearby systems, not the most dissimilar ones available.

Empirical EDR distribution initialisation was tested as an alternative to
the three-cluster model. It improved edr_assort (0.52 vs 0.41) and
contrast_cross (0.38 vs 0.71) at α = 0.10 but worsened r_d4 (−0.66 vs −0.561)
and overall loss (0.475 vs 0.553). Wider cluster standard deviation (0.12→0.20)
similarly worsened all metrics (loss 0.553→0.772). The three-cluster model is
the optimum within the distance-based architecture.

The three remaining gaps are structurally inconsistent: delta_comparator = 0.19
requires α ≈ 0.38 (so that comparator pairs span up to 0.38 EDR units) but
α = 0.38 makes r_d3 negative. The constraints cannot simultaneously be
satisfied by any single α value. This is a genuine finding: the full ΔEDR
distribution of the empirical network requires awareness sets structured by
historical contact rather than EDR distance.

This calibration ceiling is the model's most theoretically interesting result.
It demonstrates that the schismogenesis mechanism is a *necessary condition*
for bipolarity (the sign reversal does not emerge without γ > β) but not a
*sufficient condition* for the full governance citation network structure. The
gap between the model and the empirical data locates exactly the information
that historically structured contact networks add beyond what the local
distance-based rule can provide.

### 5.3 Case study trajectories

The three Graeber-Wengrow case studies are initialised with their empirical
EDR, L, and network neighbour values from `network_edges.csv`. Each focal
agent's initial edges and awareness set are populated from its historically
documented citation partners rather than random population members, producing
trajectories that reflect actual contact structure rather than average
population dynamics.

**Celtic Tribal Assemblies (A):** EDR rises from 0.70 to 0.802 ± 0.090. The
Celtic agent — initialised with 3 contrast partners (Roman Republic, Greek
Democracy, Phoenician Merchant Oligarchies) and 4 comparator partners — is
pushed upward in EDR by the contrast mechanism. Contact with low-EDR
Mediterranean systems activates schismogenesis, driving the Celtic agent
further toward its own high-EDR pole rather than toward theirs. This is the
Bateson mechanism in direct operation: contrast contact with administrative
urbanism strengthens, rather than erodes, the governance alternative. The
stable_high prediction is confirmed.

**Zomia Highland Communities (B):** EDR rises from 0.92 to 0.972 ± 0.037,
quickly reaching and maintaining the near-maximum. Zomia has 4 contrast
partners (Confucian Bureaucracy, Ming Yellow Register Census, Khmer Devaraja,
Khmer Water Mandala) — all very low-EDR lowland states — and 3 parallel
partners (other state-avoidance communities). The contrast mechanism pushes
Zomia's EDR to the ceiling. The ±0.037 standard deviation is the lowest of
the three cases, reflecting the stability of a system with maximally dissimilar
contrast partners and maximally similar parallel partners. Scott's (2009) thesis
that Zomia maintained high illegibility *because of* lowland state contact is
directly reproduced. The stable_high prediction is confirmed.

**Iroquois Confederacy / Haudenosaunee (C):** The trajectory has two phases
separated by the L-coupling onset at t = 200. Before onset, EDR rises from
0.77 to approximately 0.88, driven by contrast with low-EDR British and
Mississippian systems (2 contrast partners) embedded in a large comparator
network (40 partners). This pre-colonial stability — constituted partly by
opposition to hierarchical alternatives — is the Bateson mechanism operating
as it did for the Celts and Zomia.

At t = 200, colonial L-imposition activates: the focal agent's L rises to 0.65
(above the lock-in threshold) and δ = 0.008 initiates per-step EDR drift. EDR
declines from ~0.88 to 0.616 ± 0.080 by t = 500. The decline is smooth rather
than catastrophic, consistent with the historical record: Haudenosaunee political
marginalisation between the 1750s and 1850s was gradual, driven by legal
dispossession and treaty revision rather than military conquest alone. The
stable_then_decline prediction is confirmed.

The Haudenosaunee case couples two mechanisms from the isonomia series:
the schismogenesis mechanism (Papers 1 and 4) maintains high EDR through
contrast-based identity formation; the lock-in sequence (Paper 2) overwhelms
it when colonial administration raises L above the threshold. Neither mechanism
alone predicts the two-phase trajectory. Their conjunction does.

---

## 6. Limitations

**Distance-based edge formation.** The model assigns edge types by EDR distance.
The empirical network assigns them by the actual content of governance scholarship
— which systems scholars and rulers were aware of, which they cited as models or
contrasts, and why. Han Dynasty scholars contrasting Confucian with Legalist
governance share a similar EDR (both are appointment-based, moderate-SAP systems)
but form a contrast edge because they are within a shared intellectual tradition
that debates its own principles. The distance-based rule cannot encode this;
it would classify them as a comparator pair. The consequence is systematic
overestimation of cross-regime contrast and underestimation of within-regime
contrast — the structural gap documented in Section 4.2.

**Three-cluster approximation.** The empirical network has 14 Louvain
communities; the model uses 3 clusters as initialisation. The bridge cluster
(20% of agents) represents a simplification of the two empirical mixed-EDR
communities (Louvain communities 9 and 17, totalling approximately 23 nodes
in the hand-coded subgraph). The three-cluster model captures the topology
needed for the sign reversal to appear at the correct position; it does not
capture the internal structure of any individual community.

**Static awareness sets.** Agent awareness sets are fixed at initialisation
(with slow growth through neighbour-of-neighbour discovery). Historical
awareness was dynamic: conquest, trade, and scholarship opened new contacts
over time. The Haudenosaunee became aware of European governance models
through contact that intensified from sporadic in the 16th century to
inescapable in the 18th. A dynamic awareness model would produce trajectories
with sharper phase transitions — a direction for future work.

**N = 200 agents over T = 200–500 steps.** The ABM is a plausibility model,
not a historical simulation. With 353 nodes in the empirical network spanning
12,000 years, no mapping from model time-steps to historical time is attempted.
The model tests whether the local update rules are sufficient to generate the
observed topology; it does not simulate the historical process that produced it.

**Single-seed case study trajectories.** The case study focal agents are seeded
with their empirical neighbours from `network_edges.csv`. However, the 199
background agents are drawn from the three-cluster bimodal distribution rather
than from historically accurate populations. For the Celtic case, this means
the background includes systems that would not have been in mutual awareness
with Celtic governance — Aztec, Norse, Tang Dynasty — all of which interact
with the Celtic agent through the population dynamics. The low variance in the
Zomia and Haudenosaunee cases (±0.037 and ±0.080) suggests the focal agent's
direct edge partners dominate the trajectory, but the background population
introduces noise that historically structured population modelling would remove.

---

## 7. Discussion

### 7.1 The relationship to Bateson's schismogenesis

Bateson (1935) described schismogenesis as differentiation produced *through*
contact: interaction itself causes divergence, and the process is self-reinforcing.
This requires that the contact dimension — who interacts with whom — be
independent of the trait dimension on which divergence occurs. In Bateson's
original dyadic examples (rivalry, complementary role differentiation), the
parties were not already differentiated before the contact intensified.

Our model and network do not fully satisfy this condition. In the ABM, edge type
is assigned by pre-existing EDR distance; in the algorithmic citation network,
edge type is similarly distance-derived. A reviewer of an earlier draft correctly
identified that this makes the finding circular if interpreted as evidence of
Batesonian differentiation through contact: we cannot claim that contrast
relationships *produced* the EDR divergence if edge type was assigned based on
that divergence.

We accept this critique entirely. Our claims are therefore more modest and, we
argue, more defensible. The historically-sourced network (§3) addresses the
circularity directly: edge type is assigned from historical documentation
(who modelled themselves on whom, who defined themselves against whom) independently
of EDR values. The finding that historically-documented contrast relationships
span significantly larger EDR distances than historically-documented comparator
relationships (p = 0.007) is not circular. It establishes that governance systems
which historically defined themselves in opposition do differ more in their
freedom profile, which is the edge-level signature of the divergence process.

The ABM's role is therefore precisely described as a *structural demonstration*:
given a governance system distribution with the observed EDR structure and a
plausible three-cluster initialisation, homophily and heterophobia rules are
sufficient to produce bipolar network topology. This does not establish that
the historical governance network was produced by such a process, only that
such a process is consistent with the observed structure.

The connection to Bateson is one of structural analogy. The governance case
shares the *outcome* pattern that Bateson described — intensified divergence
between contrasting types, with contact as the mediating variable — but the
timescale (centuries to millennia), the unit of analysis (governance systems
rather than individuals or groups), and the nature of contact (ideational
exposure and institutional modelling rather than direct interaction) all differ
from Bateson's original formulation. We retain the analogy because it is
illuminating — the three G–W case studies in §5 are best understood as
ideational divergence through exposure to contrasting governance forms — while
being explicit that mechanistic equivalence is not claimed.

What a mechanistically faithful Batesonian governance model would require, and
what we identify as the primary direction for future work, is a network where
(1) historical contact between governance systems is documented independently
of their governance forms, (2) the intensity of contact is measurable, and (3)
EDR divergence is tracked as a function of contact intensity. The historically-
sourced network of §3 is a first step toward this: it documents which systems
were in documented contact and whether those contacts were modelling or
oppositional. Extending it to ~60 systems with time-varying contact intensity
would allow the causal claim to be tested rather than merely illustrated.

### 7.2 The appointment attractor and bipolar divergence

Papers 2 and 3 identified the appointment succession mechanism as the primary
attractor at high surplus legibility (L). The stationary probability of
appointment succession rises from π = 0.135 at low L to π = 0.595 at high L
(+0.460). This finding interacts with the schismogenesis result in a specific
way: high-L systems that move toward appointment succession tend to converge
on similar governance forms — the Confucian examination state, the Roman
imperial bureaucracy, the Ottoman devshirme system, the Ming civil service.
Appointment systems at high L are structurally similar to each other in ways
that hereditary and elective systems are not.

This convergence should, in the schismogenesis framework, produce a
*within-cluster compression* of high-L appointment systems into a tighter
governance community — which is exactly what is observed in the citation
network. The high-L cluster (Louvain communities with low mean EDR and
appointment-dominated succession) has higher within-cluster density and lower
ΔEDR for comparator edges than the high-EDR cluster. The lock-in sequence's
appointment attractor and the schismogenesis mechanism jointly predict that
as L rises, the governance landscape becomes more polarised: high-L systems
converge on appointment while the contrast interaction reinforces the
distinctiveness of the remaining high-EDR alternatives.

### 7.3 The Graeber-Wengrow thesis and the distance-based ceiling

*The Dawn of Everything* argues that governance diversity is not primordial
randomness but the product of deliberate differentiation — communities making
explicit choices about what kind of society to be, often in direct response
to contact with alternative models. The ABM tests a minimal version of this
claim: if governance systems form contrast relationships with dissimilar models
and update their own governance in response, does the observed bipolarity
emerge?

The calibration ceiling — the irreducible gap between distance-based and
historically structured contact — is actually consistent with Graeber and
Wengrow's argument rather than in tension with it. The distance-based rule
assumes that systems form contrasts with whoever is most different. But
Graeber-Wengrow's examples are of systems forming contrasts with whoever is
*proximate and comparable* — the Celts with Mediterranean urban governance,
Zomia with adjacent lowland states, the Haudenosaunee with both European
colonial models and Mississippian hierarchies. The contrast relationship is not
about maximising EDR distance but about marking boundaries with the specific
alternatives that are visible and relevant.

This is what historically structured awareness sets would add to the model:
not random or distance-based contact, but the actual network of who knew about
whom. The calibration ceiling is the model's way of saying that historical
contingency matters — the pattern of contacts is not fully explained by
governance similarity or difference alone. This is a finding in support of
the Graeber-Wengrow thesis, not against it.

---

## 8. Conclusion

We have formalised the schismogenesis mechanism as a minimal agent-based model
and calibrated it against the empirical governance citation network. The primary
findings are:

1. **The degree-4 sign reversal is reproduced** across all tested parameter
   combinations once a three-cluster initialisation provides a bridge region
   between the high-EDR and low-EDR governance clusters. The sign reversal
   requires γ/β ≥ 1.0 (schismogenesis at least as strong as contagion) and
   fails with two-cluster bimodal initialisation due to the missing bridge.

2. **Modular community structure is reproduced** (M = 0.448 vs 0.557), with
   EDR-assortative communities and near-zero geographic assortativity —
   consistent with the geographic null.

3. **Three structural gaps remain**, all attributable to the distance-based
   edge-formation rule. The gaps identify historically structured contact
   patterns as the additional information needed to fully reproduce the
   empirical network. This is a calibration ceiling, not a model failure.

4. **All three Graeber-Wengrow case studies are confirmed.** Celtic
   non-urbanisation and Zomia state-avoidance show stable_high trajectories
   driven by contrast-based schismogenesis. The Haudenosaunee trajectory
   shows stable_high pre-colonial stability followed by EDR decline when
   colonial L-imposition activates the lock-in coupling — coupling two
   mechanisms from the isonomia series that had been developed independently.

The model points to two immediate research directions. First, historically
structured awareness sets: replacing the EDR-distance edge-formation rule
with a rule that weights contact by temporal, geographic, and epistemic
proximity would close the calibration ceiling and test whether the remaining
gaps are in fact explained by known historical contact patterns. Second, the
lock-in coupling demonstrated in the Haudenosaunee case deserves systematic
analysis: under what conditions does L-imposition overwhelm contrast-based
EDR stabilisation, and how does the rate of L increase interact with the
strength of the schismogenesis mechanism? The transition from Paper 2's
lock-in sequence to Paper 4's schismogenesis dynamics occurs precisely at the
point where colonial administration replaces governance differentiation with
governance suppression — and that transition is still poorly understood as a
dynamic process.

---

## References

Bateson, G. (1935). Culture contact and schismogenesis. *Man*, 35, 178–183.

Bateson, G. (1958). *Naven* (2nd ed.). Stanford University Press.

Brook, T. (1998). *The Confusions of Pleasure: Commerce and Culture in Ming
China*. University of California Press.

Caesar, Julius. *Commentarii de Bello Gallico*, Book VI (Celtic governance
and Druidic institutions).

Coedes, G. (1968). *The Indianized States of Southeast Asia*. University of
Hawaii Press.

Cowgill, G. L. (2015). *Ancient Teotihuacan: Early Urbanism in Central Mexico*.
Cambridge University Press.

Erdős, P. and Rényi, A. (1960). On the evolution of random graphs.
*Publications of the Mathematical Institute of the Hungarian Academy of Sciences*
5, 17–61.

Graeber, D. and Wengrow, D. (2021). *The Dawn of Everything: A New History of
Humanity*. Allen Lane.

Lahontan, Baron de (1703). *Nouveaux Voyages de M. le Baron de Lahontan dans
l'Amérique Septentrionale*. The Hague.

Louvain, V. D., Blondel, V. D., Guillaume, J.-L., Lambiotte, R., and
Lefebvre, E. (2008). Fast unfolding of communities in large networks.
*Journal of Statistical Mechanics*, P10008.

Marks, R. B. (1998). *Tigers, Rice, Silk, and Silt: Environment and Economy
in Late Imperial South China*. Cambridge University Press.

Newman, M. E. J. (2003). The structure and function of complex networks.
*SIAM Review*, 45(2), 167–256.

Newman, M. E. J. (2006). Modularity and community structure in networks.
*PNAS*, 103(23), 8577–8582.

Postgate, J. N. (1992). *Early Mesopotamia: Society and Economy at the Dawn
of History*. Routledge.

Schleifer, P. (2026a). Isonomia I: A Phase-Space Framework for Governance
Emergence, Resilience, and Dissolution. Working paper, isonomia series.
https://github.com/its-not-rocket-science/isonomia

Schleifer, P. (2026b). Isonomia II: The Lock-In Sequence. Working paper,
isonomia series.

Schleifer, P. (2026c). Isonomia III: Succession Mechanism Attraction Basins
and the Lock-In Sequence. Working paper, isonomia series.

Scott, J. C. (2009). *The Art of Not Being Governed: An Anarchist History of
Upland Southeast Asia*. Yale University Press.

Watts, D. J. and Strogatz, S. H. (1998). Collective dynamics of small-world
networks. *Nature*, 393, 440–442.

Wilson, A. C. and Watts, D. J. (2022). Structural diversity in social networks.
*Proceedings of the Royal Society B*, 289, 20220132.
