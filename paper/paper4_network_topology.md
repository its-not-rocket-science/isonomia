# Paper 4 Pre-Development: Network Topology Characterisation and ABM Design

**Status:** Research notes — pre-ABM development
**Purpose:** Document the empirical network constraints the ABM must reproduce,
the structural findings that refine the theoretical model, and the design
decisions that follow from them.

---

## 1. What the empirical network looks like

### Basic structure
- 350 nodes, 756 edges (447 comparator, 199 parallel, 110 contrast)
- Mean degree 3.99; power-law degree distribution (γ ≈ 1.92, r² = 0.877);
  not exponential (KS p < 0.0001)
- Scale-free-like topology: heterogeneous hubs (max degree = 39),
  most nodes low-degree
- Largest connected component: 348 nodes (99%)

### Community structure
Louvain community detection finds **13 communities** on the full graph
(modularity = 0.556 — strong), 30 on the hand-coded subgraph (modularity = 0.590).

**Critical finding:** Communities are NOT geographically defined
(region assortativity r = −0.006) but ARE EDR-defined
(EDR assortativity r = 0.673, L assortativity r = 0.595). Geographic proximity
is irrelevant to who cites whom; governance philosophy is what organises
the network. This directly confirms the geographic null result from Paper 1
and constrains the ABM: agents don't need spatial coordinates, they need
EDR values.

Community EDR profiles (hand-coded subgraph, 7 multi-member communities):

| Community | n | EDR mean | EDR range | Character |
|---|---|---|---|---|
| 7 | 12 | 0.797 | 0.70–0.93 | High-freedom: San, Inuit, Swiss |
| 2 | 10 | 0.562 | 0.43–0.80 | Mixed-high: Hanseatic, Cucuteni-Trypillia |
| 9 | 13 | 0.417 | 0.10–0.70 | Mixed-low: Greek Democracy, Kurultai |
| 17 | 10 | 0.398 | 0.10–0.75 | Mixed-low: Viking, Andean Ayllu, Celtic |
| 0 | 15 | 0.334 | 0.02–0.83 | Heterogeneous hub: Paris Commune, British Parliament |
| 3 | 6 | 0.244 | 0.13–0.52 | Low-freedom: Holy Roman, Byzantine |
| 18 | 8 | 0.200 | 0.03–0.53 | Low-freedom: Magna Carta, Golden Horde |

The bipolarity is real but is not a clean two-cluster split. There are
two large high-EDR communities (7, 2) and three low-EDR communities (0, 3, 18),
with two mixed communities (9, 17) spanning the threshold. The degree-4 sign
reversal emerges from navigating between these poles through the mixed
communities in the middle.

### Contrast edge structure
- 39% of contrast edges cross the θ = 0.45 boundary (high↔low EDR)
- 40% are within high-EDR (fine-grained differentiation within the
  freedom regime — e.g. Norwegian vs Swiss vs Athenian governance forms)
- 21% are within low-EDR

Cross-theta contrast edges have ΔEDR = 0.378; same-regime contrast edges
have ΔEDR = 0.147 (Mann-Whitney p < 0.0001). **Contrast edges
preferentially link across the EDR threshold, but the majority (60%)
represent within-regime fine-grained differentiation.** This is an important
finding for the ABM: the schismogenesis mechanism operates at two scales —
cross-regime (high-EDR vs low-EDR, the primary polarisation) and
within-regime (differentiation among systems that share a broad governance
philosophy but differ in specific freedoms).

### Temporal structure
Contrast edges have a higher mean temporal gap than comparators
(4,947y vs 1,445y mean), but this is not significant (p = 0.256) due
to high variance. The large mean gap for contrast edges reflects cases
like Natufian Communities (−10,000) cited against Norwegian Democracy (+2020)
— civilisational-scale contrast that was explicitly the point. Schismogenesis
is not time-local any more than it is spatially local.

### The degree-4 sign reversal — precise characterisation
r = 0.721 (degree-1) → 0.617 (degree-2) → 0.315 (degree-3) → −0.341 (degree-4)

This decay pattern is consistent with a network that has **two large
internally cohesive clusters separated by a bridge region of mixed-EDR
nodes**. At degree-1 and degree-2, you are within your own cluster
(positive correlation). At degree-3, you're in the bridge region
(attenuating). At degree-4, you've entered the other cluster
(sign reversal). The modularity structure (community 9 and 17 as bridges)
supports this interpretation.

---

## 2. ABM Target Constraints

The ABM must reproduce the following empirical properties. Listed in
order of theoretical importance:

### Hard constraints (ABM fails if it doesn't reproduce these)
1. **Degree-4 sign reversal**: r decay from ~0.72 to −0.34 across four
   network hops. This is the primary structural claim of Paper 1.
2. **Strong modularity** (M ≈ 0.55–0.60): the network is not random;
   it has genuine community structure.
3. **EDR-assortative communities** (r ≈ 0.67): communities are organised
   by EDR, not geography.
4. **Schismogenesis signal**: contrast edges have larger ΔEDR than
   comparator edges (the original p = 0.0004 result).

### Soft constraints (ABM should get approximately right)
5. **Scale-free degree distribution** (γ ≈ 1.92): some systems become
   widely cited hubs; most are low-degree.
6. **Geographic null**: network structure should not require spatial
   proximity to reproduce — agents interact based on EDR distance, not
   physical distance.
7. **60% within-regime contrast edges**: the mechanism produces
   fine-grained differentiation within regimes, not only cross-regime
   polarisation.

### Properties the ABM does NOT need to reproduce
- Exact community membership (which historical systems end up in which
  community)
- Exact degree of specific nodes
- Temporal ordering of edge formation

---

## 3. ABM Design

### What the ABM is modelling
The Bateson schismogenesis process: societies in contact develop increasingly
differentiated identities precisely because of that contact. In governance
terms: a society that becomes aware of a neighbouring governance model
responds by either adopting similar features (contagion) or deliberately
distinguishing itself (schismogenesis). The citation network in Paper 1
captures the outcome of this process across historical time; the ABM asks
whether a simple local update rule can generate the observed network
topology.

### Agent design
Each agent represents a governance system with:
- `edr`: current EDR composite (0–1)
- `edges`: dictionary of {neighbour: edge_type} where
  edge_type ∈ {comparator, contrast}
- `l`: surplus legibility (0–1), treated as a time-varying external
  parameter in the coupled model

Agents do not have spatial coordinates. They have an `awareness_set`:
the set of other governance systems they know about (directly or through
their network neighbours). In the historical record, awareness is
primarily driven by trade routes, conquest, and scholarship — not
pure geographic proximity. The awareness_set initialises randomly and
grows as the network develops.

### Update rule (Option B: edge-formation model)
At each time step, each agent:

1. **Assesses** a random potential contact from its awareness_set.
2. **Computes** ΔEDR = |own_edr − contact_edr|.
3. **Classifies** the relationship:
   - If ΔEDR < α (similarity threshold): form/maintain a *comparator* edge
     (structural similarity — positive influence possible)
   - If ΔEDR ≥ α: form/maintain a *contrast* edge (deliberate
     differentiation — push toward greater divergence)
4. **Updates** own EDR based on neighbours:
   - Comparator edges: pull toward neighbour EDR (contagion):
     `edr += β * (neighbour_edr − edr)` for each comparator neighbour
   - Contrast edges: push away from neighbour EDR (schismogenesis):
     `edr -= γ * (neighbour_edr − edr)` for each contrast neighbour
   - EDR is clipped to [0, 1]
5. **Lock-in pressure**: if `l > l_threshold`, apply a drift toward
   appointment/hereditary succession basins by reducing edr at rate δ.
   This couples the schismogenesis model to the lock-in sequence.

### Parameters
| Parameter | Description | Initial range to sweep |
|---|---|---|
| α | ΔEDR threshold for contrast vs comparator | 0.15 – 0.45 |
| β | Contagion strength (comparator pull) | 0.01 – 0.10 |
| γ | Schismogenesis strength (contrast push) | 0.01 – 0.10 |
| δ | Lock-in pressure (EDR drift at high L) | 0.001 – 0.02 |
| N | Number of agents | 50 – 350 |
| k | Initial mean degree | 2 – 8 |
| l_threshold | L level triggering lock-in drift | 0.45 – 0.70 |

**Key theoretical prediction about parameters:** The degree-4 sign reversal
requires γ > β (schismogenesis stronger than contagion), otherwise the
network converges to a single cluster rather than bipolar structure. The
ratio γ/β is the primary parameter of interest.

### Evaluation metrics (matching ABM output to empirical targets)
For each parameter set, run 50 replicates and compute:
1. Mean EDR correlation at degrees 1–4 (target: 0.72, 0.62, 0.32, −0.34)
2. Louvain modularity (target: 0.55–0.60)
3. EDR assortativity (target: 0.67)
4. Fraction of contrast edges crossing theta boundary (target: 0.39)
5. Mean ΔEDR for contrast vs comparator edges (target: 0.24 vs 0.19)

Loss function: sum of squared deviations from targets, weighted by
empirical confidence in each target.

---

## 4. The Three G-W Case Studies

### Celtic non-urbanisation
- **In dataset**: Celtic Tribal Assemblies (EDR = 0.70, L = 0.30, degree = 3,
  0 contrast edges in current network)
- **The historical claim**: The Celts in contact with Mediterranean
  urbanism *chose* non-urbanisation as a deliberate contrast. Oppida
  existed but were not cities in the Mediterranean sense; hill forts
  organised around assembly rather than administrative centres.
  Graeber-Wengrow cite this as a schismogenesis case — Celtic governance
  was partly constituted by its refusal of what they saw as the
  Mediterranean governance model.
- **ABM prediction**: Celtic Tribal Assemblies should end up in the
  high-EDR cluster (EDR = 0.70, confirmed) and should form contrast
  edges with Mediterranean systems (Rome, Athens, Carthage). Currently
  has 0 contrast edges — this is a network coding gap, not an absence
  of the relationship.
- **Data work needed**: Add contrast edges from Celtic Tribal Assemblies
  to Roman Republic, Greek Democracy, Phoenician Merchant Oligarchies
  in network_edges.csv. Justification: direct textual evidence (Posidonius,
  Julius Caesar's Gallic Wars, Greek accounts of Hyperboreans).

### Zomia state-avoidance
- **In dataset**: Zomia Highland Communities (EDR = 0.92, L = 0.05,
  degree = 0 — isolated node, not in graph)
- **The historical claim**: Scott (2009) documents that Zomia highland
  communities in Southeast Asia organised their entire subsistence
  strategy around maintaining illegible surplus precisely to resist
  incorporation into lowland states. This is the purest example of
  deliberate EDR maintenance — the low-L, high-EDR counter-strategy
  predicted by Paper 2's counter-case analysis.
- **ABM prediction**: Zomia should be in the high-EDR cluster with
  strong contrast edges to lowland state systems. Currently isolated
  because it has no edges in the network — another coding gap.
- **Data work needed**: Add Zomia to the network with contrast edges
  to Confucian Bureaucracy, Ming Dynasty administration, Khmer Devaraja,
  and Thai and Burmese lowland states. Add parallel edges to other
  state-avoidance communities (Maroon Communities, Aboriginal Elders
  Councils, San Xaro Networks).

### Haudenosaunee constitutional development
- **In dataset**: Iroquois Confederacy / Haudenosaunee
  (EDR = 0.77, L = 0.35, degree = 27, 0 contrast edges)
- **The historical claim**: Graeber-Wengrow argue that Haudenosaunee
  political philosophy — particularly as expressed through Deganawida's
  Great Law of Peace — was partly constituted by contact with and
  explicit rejection of both the European colonial models arriving from
  the east and the more hierarchical Mississippian and Moundbuilder
  traditions to the south and west. The Haudenosaunee understood their
  governance as a specific alternative.
- **ABM prediction**: Haudenosaunee should have contrast edges to
  British Parliamentary System and French governance models (European
  contact), and to Mississippian Chiefdoms (internal North American
  contrast). Currently has 27 comparator/parallel edges but 0 contrast —
  coding gap.
- **Data work needed**: Add contrast edges to British Parliamentary
  System, French Absolutism (if in dataset), and Mississippian Chiefdoms.
  Historical justification: direct accounts of Haudenosaunee leaders
  criticising European governance (the Adario dialogues, recorded by
  Lahontan 1703, influenced Enlightenment political thought).

---

## 5. Immediate Next Steps

### Step 1: Network coding additions (1–2 hours)
Add the missing edges identified above to `network_edges.csv`:
- Celtic → Roman Republic (contrast), Greek Democracy (contrast),
  Phoenician (contrast)
- Zomia → Confucian Bureaucracy (contrast), Ming (contrast),
  Khmer (contrast); → Maroon Communities (parallel), San (parallel)
- Haudenosaunee → British Parliamentary (contrast),
  Mississippian Chiefdoms (contrast)

Also check: does Zomia Highland Communities have L coded? Currently
L = 0.05 — correct for a deliberately low-legibility system.

### Step 2: Build the base ABM (1 week)
Write `src/schismogenesis_abm.py` implementing:
- Agent class with edr, edges, awareness_set
- Edge-formation rule (Option B)
- EDR update rule
- Parameter sweep infrastructure
- Output: degree-shell correlation, modularity, assortativity, contrast
  edge fraction, ΔEDR by edge type
- Evaluation against the 5 empirical targets above

No figure generation by default. `--figure` flag for visualisations.

### Step 3: Parameter sweep and calibration (2–3 days)
Grid search over α, β, γ with N=200 agents, 50 replicates each.
Target: reproduce degree-4 sign reversal within ±0.10 at each hop.
Expected finding: γ/β > 1 is necessary condition; α ≈ 0.25–0.35
likely optimal.

### Step 4: Couple to lock-in sequence (1–2 days)
Add δ parameter (EDR drift at high L). Test whether coupling reproduces
the historical observation that high-L civilisations converge on
appointment/hereditary succession while simultaneously losing the
contrast-citation diversity of lower-L periods. Expected: high L
compresses the EDR distribution toward the low-EDR cluster, reducing
modularity and making the network more monopular.

### Step 5: Case study trajectories (2–3 days)
For each G-W case study: initialise the ABM with the historical
starting conditions (EDR, L, awareness set) and run forward in time.
Check whether the ABM trajectory matches the historical outcome
(Celtic maintained high-EDR through contrast to Mediterranean;
Zomia maintained high-EDR through withdrawal; Haudenosaunee maintained
high-EDR through constitutional development in contrast to colonial models
until colonial incorporation forced EDR collapse).

---

## 6. Key Uncertainties

**Network coding quality**: The citation network is built from secondary
sources and reflects what scholars have documented, not the full range
of historical governance relationships. Zomia's isolation (degree=0) is
a documentation gap, not evidence of genuine isolation. The ABM
calibration should use the hand-coded subgraph (n=97) rather than the
full graph to avoid noise from auto-coded systems.

**Scale**: The empirical network has 350 nodes built up over 12,000 years.
An ABM with N=200 agents and T=500 time steps is not a simulation of
that process — it is a test of whether the local update rules are
sufficient to generate the observed topology. The ABM is a plausibility
model, not a historical simulation.

**EDR dynamics**: The update rule assumes EDR changes in response to
network influence. In reality, EDR changes are driven primarily by the
L→A→EDR suppression sequence (Paper 2) and the succession mechanism
dynamics (Paper 3). The schismogenesis ABM isolates the network dynamic
for theoretical analysis; the full coupled model is a longer-term project.

---

## References for Case Studies

Graeber, D. and Wengrow, D. (2021). *The Dawn of Everything*. Chapters
on Celtic non-urbanisation (pp. 225–270), Zomia (pp. 73–74, 150–151),
and Haudenosaunee (pp. 27–33, 68–72).

Lahontan, Baron de (1703). *Nouveaux Voyages de M. le Baron de Lahontan
dans l'Amérique Septentrionale*. The Hague.

Scott, J. C. (2009). *The Art of Not Being Governed*. Yale University Press.

Caesar, Julius. *De Bello Gallico*, Books VI–VII (Celtic governance).

Posidonius of Apamea (fragments, via Athenaeus and Strabo): observations
on Celtic assembly governance and contrast with Hellenistic models.

---

## 7. ABM Development Log — Parameter Search

### Findings from initial parameter search (Phase 1 of ABM development)

**The sign reversal is reproducible.** The homophily-based edge formation
rule (v3/v4) consistently produces the correct sign pattern:
r_d1 ≈ +0.60–0.80, r_d2 ≈ +0.55–0.80, r_d3 ≈ −0.40–0.70, r_d4 ≈ −0.60–0.85.
The empirical targets (0.72, 0.62, 0.32, −0.34) are in the achievable range.

**The modularity gap is the primary remaining challenge.** The model
produces modularity M ≈ 0.34–0.40, against the empirical target of 0.55–0.60.
The sign reversal is strong but the community structure is weaker than
observed. This is a meaningful finding: it suggests the empirical network
has additional structure beyond what the schismogenesis rule alone produces —
likely the historically structured awareness set (trade routes, conquest
patterns, scholarly transmission) creates tighter clusters than a random
awareness set does.

**The cross-theta contrast fraction is the hardest constraint.** In all
configurations tested, cross-theta contrast edges dominate (cr_θ ≈ 0.70–0.98
vs target 0.39). The empirical 39% cross-theta rate means most contrast
edges are within-regime — systems that share a broad governance philosophy
but differentiate on specifics. This within-regime contrast is not produced
by a simple two-cluster bimodal initialisation. It requires either:
(a) more than two EDR clusters (empirically, the hand-coded subgraph has
    7 multi-member communities across the EDR spectrum), or
(b) the awareness set to be biased toward same-regime contacts for contrast
    edge formation.

**Key parameter finding:** the γ/β ratio (schismogenesis/contagion) must
be > 1.5 but < 3.0 to get the sign reversal without over-polarisation.
Anchor force ≈ 0.005–0.008 is needed to prevent full polarisation to {0,1}.
α (contrast threshold) ≈ 0.25 produces better results than α = 0.30.

### Revised ABM design for Phase 2

The v4 model architecture is correct. Two changes needed before the sweep:

1. **Multi-modal initialisation**: Replace the two-cluster bimodal with
   the empirical EDR distribution from the hand-coded dataset (7 modes
   corresponding to the Louvain communities). This will produce within-cluster
   contrast edges naturally.

2. **Awareness set structure**: Instead of a uniform random awareness set,
   bias toward same-epoch and same-region contacts, with a smaller fraction
   of cross-epoch/cross-region awareness. This makes the network structure
   more historically realistic and should increase modularity.

These changes are implemented in `schismogenesis_abm.py` v2 (to be written
after the initial sweep establishes baseline parameters).
