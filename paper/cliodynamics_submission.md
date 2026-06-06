# Governance Phase Space, Lock-In, and Schismogenesis: A Computational Framework for Long-Run Freedom Dynamics

**[Author]**
*Independent researcher*

*Corresponding author: [email]*
*Data and code: [repository URL]*

*Submitted to Cliodynamics: The Journal of Quantitative History and Cultural Evolution*

**Acknowledgements:** The author thanks [to be completed].

**Data availability:** The full dataset (389 governance systems, 12,000-year span),
coding scheme, and all analysis scripts are available at [repository URL] under
MIT licence.

---

## Abstract

We present a computational framework for analysing long-run governance dynamics
across 389 systems spanning 12,000 years. The framework integrates three
mechanisms. First, a governance phase space defined by two composite indices:
SAP (sovereignty, administration, competitive politics) and EDR (exit freedom,
disobedience freedom, arrangement freedom). The EDR composite functions as a
resilience indicator with an empirically identified threshold at θ ≈ 0.45; the
SAP-EDR correlation is r = −0.738 across all 389 systems. Second, the lock-in
sequence: surplus legibility (L) drives rising administrative apparatus (A),
which suppresses E, D, and R through a six-stage causal chain. Cross-validation
across six independent external datasets — V-Dem (r = 0.868–0.912, n = 16),
Polity5 (r = 0.847, n = 11), WJP Rule of Law Index (r = 0.904 for E,
n = 7), Freedom House FIW (r = 0.923, n = 9), CCP Comparative Constitutions
Project (r = 0.681 for D, n = 11), and Seshat Global History Databank
(r = 0.604–0.774, n = 14) — confirms construct validity across measurement
traditions. Third, a continuous-time Markov chain (CTMC) succession model (149
spells, 39 events, 110,589 system-years) shows that the stationary probability
of bureaucratic appointment succession rises from π = 0.135 at low L to
π = 0.595 at high L (+0.460, logistic regression OR = 2.24, permutation
p = 0.005). Pre-existing disobedience freedom (D₀) moderates lock-in: high-D₀
elective systems exit elective succession at 0.55 per 1,000 years versus 2.74
for low-D₀ systems (ratio 5.03×; Cox PH joint test p = 0.026). We then
formalise the network mechanism by which governance differentiation propagates
as an agent-based model of schismogenesis — the process by which contact between
governance systems intensifies rather than erases their differences. The
calibrated model reproduces the empirical citation network's degree-4 sign
reversal (r_d4 = −0.561 vs −0.391 empirical) and modular community structure
(M = 0.448 vs 0.557) from three local parameters. Case study validation against
three Graeber-Wengrow examples from *The Dawn of Everything* confirms the model's
qualitative predictions.

**Keywords:** governance dynamics; agent-based modelling; Markov chain; lock-in;
schismogenesis; comparative historical analysis; EDR composite; succession mechanisms

---

## 1. Introduction

How do governance systems sustain or lose the freedoms that make them resilient
to collapse? This question has occupied comparative historians, political
scientists, and cliodynamicists since Turchin's (2003) secular cycles analysis
established that the long-run oscillation of social complexity is not accidental
but structurally driven. What that literature has lacked is a unified measurement
framework that covers the full range of governance forms — from pre-state hunter-
gatherer bands to modern bureaucratic states — in a way that allows systematic
comparison of the mechanisms by which freedom is sustained, suppressed, and
occasionally recovered.

This paper presents such a framework and tests its core predictions against
quantitative data spanning 12,000 years. The framework is built around three
mechanisms operating at different timescales and levels of analysis: the phase-
space positioning of governance systems in a two-dimensional SAP-EDR space; the
lock-in sequence by which rising surplus legibility suppresses the three freedoms
over decades and centuries; and the schismogenesis dynamic by which contact
between governance systems produces bifurcation rather than convergence over
civilisational time.

The framework draws on Graeber and Wengrow's (2021) historical analysis in *The
Dawn of Everything* but operationalises its claims quantitatively. Graeber and
Wengrow argue that governance diversity is not primordial randomness but the
product of deliberate differentiation — societies making choices about what kind
of society to be, often in explicit response to contact with alternatives. The
framework tests this claim through network analysis of a governance citation
database, an agent-based model of the schismogenesis mechanism, and three
detailed case studies of the systems Graeber and Wengrow identify as canonical
examples of deliberate differentiation.

### 1.1 Contribution to cliodynamics

The framework makes four specific contributions to the cliodynamics literature.
First, a measurement instrument (the EDR-SAP phase space) that is calibrated
against six independent external datasets and covers a wider temporal and
governance range than existing cross-national indices. Second, a mechanistic
model of freedom suppression (the lock-in sequence) that links surplus legibility
to succession mechanism dynamics through a testable causal chain. Third, a
continuous-time Markov chain model of succession mechanism transitions that
produces L-conditional stationary distributions directly comparable to the
empirical cross-section. Fourth, an agent-based model of governance network
dynamics that demonstrates the sufficiency of local schismogenesis rules for
generating the empirically observed bipolar network topology.

---

## 2. The Governance Phase Space

### 2.1 Measurement framework

The isonomia governance dataset codes 389 governance systems on six continuous
indices using a standardised scheme derived from primary and secondary historical
sources. All coding decisions are documented in a public coding scheme
(data/coding_scheme.md). Systems span from the Natufian Communities (~10,500
BCE, n = 1 system) to contemporary digital governance forms (n = 5 systems
coded at 2020–2025), with the densest coverage in the ancient Mediterranean,
East Asian imperial sequences, and pre-colonial Americas.

Three indices constitute the SAP composite measuring domination capacity:
**sovereignty** (S, ability to coercively enforce decisions without appeal),
**administration** (A, capacity to track, register, and extract from populations),
and **competitive politics** (P, presence and independence of political
competition mechanisms). Three indices constitute the EDR composite measuring
freedom preservation: **exit freedom** (E, ability to leave governance
relationships without catastrophic loss), **disobedience freedom** (D, ability
to refuse compliance without fatal consequence), and **arrangement freedom**
(R, ability to reorganise social institutions). All six indices are coded 0–1.
The EDR and SAP composites are simple means of their three components.

**Construct validity** is confirmed across six independent external datasets:

| Dataset | Target variable | r | p | n |
|---|---|---|---|---|
| V-Dem v16 | Liberal democracy | 0.868 | *** | 16 |
| V-Dem v16 | Deliberative democracy | 0.912 | *** | 12 |
| Polity5 | DEMOC score | 0.847 | *** | 11 |
| WJP Rule of Law 2025 | Expression & privacy | 0.904 | ** | 7 |
| Freedom House FIW | Aggregate rights | 0.923 | *** | 9 |
| CCP Constitutions v5 | Exec. constraint | 0.681 | * | 11 |
| Seshat Databank | Admin composite | 0.604 | * | 14 |
| Seshat Databank | Military composite | 0.774 | ** | 12 |

These correlations are consistently strong across measurement traditions that
differ in methodology, temporal scope, and conceptual origin. V-Dem and
Freedom House use expert survey aggregation; Polity5 uses expert coding on
categorical scales; WJP uses survey data from legal practitioners; CCP codes
constitutional text; Seshat codes archaeological and historical evidence. The
convergence across these sources establishes that the EDR composite is measuring
a real construct, not an artefact of any single measurement approach.

### 2.2 Phase-space structure

The SAP-EDR correlation across all 389 systems is r = −0.738 (p < 0.0001),
establishing that domination capacity and freedom preservation are negatively
associated at the cross-sectional level. This is the framework's primary
empirical claim: governance systems occupy a continuous phase space, and the
two axes are inversely correlated.

This inverse correlation should not be taken as a deterministic law. Fourteen
systems in the dataset maintain EDR above θ = 0.45 with SAP above 0.70 —
the counter-cases discussed in Section 4. The correlation describes a structural
tendency, not a mechanical necessity: there are governance configurations that
maintain both high domination capacity and high freedom, but they are exceptions
that require specific enabling conditions rather than the default outcome of
high-SAP governance.

The resilience threshold θ = 0.45 is identified empirically as the EDR level
below which Turchin-Tainter collapse dynamics become significantly more probable.
Systems below θ show higher rates of political instability, succession mechanism
changes, and territorial contraction in the longitudinal data.

---

## 3. The Lock-In Sequence

### 3.1 Mechanism

The lock-in sequence describes a specific causal chain by which rising surplus
legibility (L) suppresses the three freedoms. Surplus legibility, following
Scott (2017), measures how countable, measurable, and extractable a society's
primary productive output is to external administrative agents. Cereal grain
agriculture crosses a critical legibility threshold: grain is storable,
transportable, and ripens in a single observable annual event. Swidden
cultivation, forest products, and pastoral economies are comparatively
illegible — they resist external accounting.

The six-stage sequence runs: (1) L rises through agricultural intensification
or territorial fixation; (2) rising L creates demand for information
infrastructure (I): tokens, tallies, records; (3) high I enables rising
administrative apparatus (A): the capacity to track individuals and enforce
obligations across time; (4) A suppresses E through legal and economic
mechanisms binding people to place; (5) without credible exit options, D
weakens — disobedience becomes individually costly without collective support;
(6) institutional experimentation is redefined as disorder and R approaches
zero. The EDR composite falls below θ.

Four case studies trace this sequence across its full range:

**Natufian to Uruk (Levant and Mesopotamia, ~12,500–3,000 BCE):** The
best-documented instance. Natufian Communities (L = 0.10, EDR = 0.93) show
high mobility, seasonal aggregation without permanent hierarchy, and deliberate
oscillation between egalitarian and ceremonial modes. Over three millennia,
agricultural intensification (Ubaid Culture, L = 0.50, EDR = 0.70) and then
early state formation (Early Uruk, L = 0.70, EDR = 0.47) trace the sequence
in the archaeological record.

**Qin Legalism (China, ~350–207 BCE):** The extreme case. The Shang Yang
reforms systematically maximised L through household registration, standardised
weights and measures, and the prohibition of mobility without administrative
permit. Qin (L = 0.90, A = 0.95, EDR = 0.03) represents the lock-in sequence
near its practical limit: a governance system that deliberately optimised for
extractability and paid for it with complete freedom suppression and rapid
dynastic collapse.

**Inca Empire (Tawantinsuyu, ~1438–1533 CE):** Demonstrates that L can approach
its maximum without writing. The quipu knotted-cord system (L = 0.90, I = 0.60)
achieved near-total legibility through a non-literate administrative apparatus
tracking household labour obligations across the entire empire. Legibility is
not literacy — it is the organisational capacity to render surplus countable
regardless of the medium.

**Zomia Highland Communities (Southeast Asia, ongoing):** The counter-strategy
case. Scott's (2009) analysis of Zomia documents deliberate maintenance of low
legibility as state-avoidance: swidden cultivation, oral tradition, dispersed
settlement, and periodic community dispersal all function as structural
resistance to administrative incorporation. Zomia (L = 0.05, EDR = 0.92)
is not underdeveloped — it is strategically illegible.

### 3.2 Counter-cases and the D₀ moderator

Seven governance systems in the dataset maintain high EDR (≥ 0.70) despite high
L (≥ 0.60): Norway, Switzerland, Iceland, Germany, Estonia, the Venetian
Republic, and the Roman Republic (early period). All seven share a common
feature: institutionally robust disobedience freedom (D₀ ≥ 0.55) established
before legibility reached its current level.

The D₀ moderator operates through a specific mechanism: pre-existing
disobedience freedom raises the cost of the lock-in sequence's Stage 4 transition
(E suppression through administrative binding). In systems where disobedience
is structurally encoded as a legitimate political act — through assembly
traditions, common-law rights, trade union protections, or constitutional
guarantees with enforcement mechanisms — the administrative apparatus cannot
easily bind populations without provoking organised resistance. The lock-in
sequence is interrupted not because L stops rising but because A cannot
translate high L into E suppression in the presence of strong D.

This prediction is tested formally in Section 4 through the CTMC succession
model.

---

## 4. Succession Mechanism Dynamics

### 4.1 Static attraction basin model

We test the lock-in sequence's predictions about succession mechanism
distributions through a three-phase empirical analysis of succession mechanism
change across 117 hand-coded governance systems (working set, confidence ≥ 2,
succession type coded, L and D₀ coded; 8 charismatic systems excluded from the
multinomial model).

Phase 1 (static model): the cross-tabulation of succession type against L regime
(low: L < 0.60; high: L ≥ 0.60) yields χ² = 25.08 (df = 4, p < 0.0001).
The lock-in sequence predicts that high L should shift the succession type
distribution toward hereditary and appointment and away from consensus and
rotation — exactly what the cross-section shows. At low L, consensus and
rotation together account for 45% of systems; at high L, they account for 8%.

The D₀ moderator prediction — that among high-L systems, pre-existing
disobedience freedom discriminates elective from hereditary succession — is
confirmed with large effect size. High-L elective systems have median D₀ = 0.55
(n = 12); high-L hereditary systems have median D₀ = 0.17 (n = 26). Mann-
Whitney U = 278, p = 0.0001, rank-biserial r = −0.782. A one-unit increase
in D₀ multiplies the odds of occupying the elective rather than hereditary
basin by OR = 6.46 at high L.

### 4.2 Empirical transition matrix

Phase 2 analyses 43 type-changing succession mechanism transitions across 44
systems. The trigger-type analysis confirms the D₀ moderator at the dynamic
level: elite reform events — transitions forced by internal coalitions without
external collapse — produce zero hereditary outcomes across 11 documented cases.
Internal succession crises produce 56% hereditary outcomes (5 of 9 cases).

The L-conditional shift is confirmed by logistic regression: each standard-
deviation increase in L at the time of a succession mechanism transition
multiplies the odds of the transition landing in appointment succession by
OR = 2.24 (permutation p = 0.005). This is the primary statistically significant
dynamic result: rising legibility does not merely predict which succession type
a system currently occupies (Phase 1) but predicts where transitions land when
they do occur.

### 4.3 Continuous-time Markov chain

Phase 3 estimates a continuous-time Markov chain from 149 spells across 119
systems (39 events, 110,589 total system-years). The CTMC weights transitions
by dwell time, recovering the fraction of time any governance system would spend
in each succession type given the empirical rates of exit and stability.

The L-conditional stationary distributions are the central result. At low L
(L < 0.60): hereditary π = 0.414, appointment π = 0.135, elective π = 0.394,
consensus π = 0.050, rotation π = 0.007. At high L (L ≥ 0.60): appointment
π = 0.595 (+0.460), hereditary π = 0.263 (−0.151), elective π = 0.115 (−0.279).

The primary attractor at high L is appointment, not hereditary succession. This
refines the lock-in sequence prediction: the sequence does not terminate in
simple dynastic hereditary rule but in a bureaucratic appointment structure that
exploits the administrative infrastructure that high L creates. The Tang Dynasty
Keju examination system, the Ming civil service, the Ottoman devshirme system,
and the Habsburg Haugwitz reforms all represent the appointment attractor
operating at high L — each arose from a preceding hereditary system as the
administrative apparatus grew sophisticated enough to manage empire by competence
rather than kinship.

The D₀ moderator operates at the dynamic level: high-D₀ elective systems
(D₀ ≥ 0.45) exit elective succession at 0.55 per 1,000 years versus 2.74 per
1,000 years for low-D₀ elective systems (ratio 5.03×; Cox PH joint test
p = 0.026). Pre-existing disobedience freedom roughly quintuples the stability
of elective succession against the appointment and hereditary attractors.

**The consensus founding-state finding:** The CTMC gives π(consensus) ≈ 0.04
at both low and high L, yet 16% of the cross-section is coded as consensus.
This discrepancy is theoretically important: consensus succession is a founding
state, not an equilibrium state. Pre-state and small-scale societies begin as
consensus forms without transitioning from other types. The pathway from
consensus to other types is empirically open (three documented transitions);
the pathway back from appointment or hereditary to consensus is empirically
closed (zero documented cases). The CTMC correctly identifies that the long-run
dynamics of any system that enters the transition process favour appointment and
hereditary outcomes; the 16% consensus cross-sectional frequency reflects
systems that have never entered that process — a structural distinction that
directly supports the Graeber-Wengrow argument about asymmetric and largely
irreversible freedom loss.

---

## 5. Schismogenesis and the Governance Citation Network

### 5.1 The citation network

The governance systems in the dataset are connected by a citation network of
773 relationships across 353 nodes, typed as comparator (structural similarity,
n = 449), parallel (independent co-development, n = 204), or contrast (explicit
differentiation, n = 120). Mean degree 4.38; power-law degree distribution
(γ ≈ 1.92, r² = 0.877). Fourteen Louvain communities with modularity M = 0.557.

The network has two striking properties. First, EDR assortativity r = 0.405
with near-zero region assortativity r = 0.024: communities are organised by
governance philosophy, not geography. Second, a degree-4 sign reversal: the
Pearson correlation between a system's EDR and the mean EDR of its citation
partners is positive at degrees 1–3 (r = 0.582, 0.560, 0.314) but negative at
degree-4 (r = −0.391, p < 0.0001). At four citation hops, governance systems
reliably resemble their antipode rather than their neighbour.

This sign reversal is the signature of a bipolar network: two governance
regimes (high-EDR and low-EDR), internally coherent, connected by a mixed
bridge region, and systematically opposed across regime boundaries. The contrast
edges are the mechanism: mean |ΔEDR| for contrast pairs is 0.255 versus 0.193
for comparator pairs (Mann-Whitney p = 0.00015).

### 5.2 The schismogenesis ABM

We formalise the schismogenesis mechanism as an agent-based model and test
whether simple local rules are sufficient to generate the observed network
topology. Gregory Bateson (1935) defined schismogenesis as the process by which
differentiated identities develop and intensify through contact. In governance
terms: a system that becomes aware of a contrasting governance model responds by
reinforcing its own distinctiveness rather than adopting the alternative.

The model contains N = 200 agents, each with an EDR value, initialised from a
three-cluster distribution (40% high-EDR at μ = 0.75, 20% bridge at μ = 0.48,
40% low-EDR at μ = 0.20, all σ = 0.12). Three-cluster initialisation is
essential: two-cluster bimodal initialisation produces the sign reversal at
degree 2→3 rather than the empirical 3→4, because without a bridge region
degree-3 paths always reach the far cluster.

At each step, each agent selects a contact (homophilic by default, contrast-
seeking with probability p_contrast = 0.12), forms or updates an edge (comparator
if |ΔEDR| < α, contrast if |ΔEDR| ≥ α), and updates its EDR:

- Comparator edges: edr += β × (nbr_edr − edr) / n_comparator [contagion]
- Contrast edges: edr -= γ × (nbr_edr − edr) / n_contrast [schismogenesis]
- Anchor force: edr -= anchor × (edr − edr_init) [prevents full polarisation]

An optional lock-in coupling (δ > 0) applies per-step EDR drift for agents
with L above a threshold, coupling the schismogenesis model to the lock-in
sequence.

### 5.3 Calibration results

A parameter sweep over 60 combinations × 20 replicates identifies best-fit
parameters α = 0.20, β = 0.003, γ = 0.006 (loss = 0.553). The calibrated model:

- Reproduces the sign reversal at the correct position: r_d1 = 0.651,
  r_d2 = 0.567, r_d3 = 0.414, r_d4 = −0.561 (empirical: 0.582, 0.560, 0.314,
  −0.391)
- Achieves modular community structure: M = 0.448 (empirical 0.557)
- EDR assortativity r = 0.398 (empirical 0.405 at network level)

Three structural gaps remain: r_d4 overshoots (−0.561 vs −0.391); the fraction
of contrast edges crossing the θ boundary is too high (0.710 vs 0.420); and
mean |ΔEDR| for contrast edges is too large (0.569 vs 0.255). All three
reflect the same cause: the distance-based edge-formation rule assigns contrast
edges to the most dissimilar pairs, while the empirical network assigns them to
historically proximate pairs — Celts contrasting with Mediterranean urbanism
because it is the adjacent alternative, not because it is the most dissimilar
governance form available.

This calibration ceiling is the model's most theoretically informative result.
It demonstrates that the schismogenesis mechanism is a *necessary condition* for
bipolarity — the sign reversal does not emerge without γ/β ≥ 1.0 — but that
the full ΔEDR distribution of the citation network requires historically
structured contact patterns beyond what distance-based rules can provide.
The gap between model and data locates exactly the information that historical
contingency adds to the local mechanism.

The γ/β condition has a clear theoretical interpretation: the sign reversal
requires that schismogenesis be at least as strong as contagion. If contagion
dominates (γ < β), the network converges to a single cluster. If schismogenesis
dominates (γ > β), the network bifurcates. The best-fit γ/β = 2.0 suggests the
empirical network is in the schismogenesis-dominant regime, but not so strongly
that contagion is irrelevant — the positive correlations at degrees 1 and 2
depend on within-cluster contagion maintaining cluster cohesion while cross-
cluster schismogenesis maintains the separation.

### 5.4 Case study validation

Three case studies from Graeber and Wengrow (2021) provide qualitative
validation. Each focal agent is initialised with its historically documented
EDR, L, and citation partner values from the network database.

**Celtic Tribal Assemblies:** EDR 0.70 → 0.802 ± 0.090 (predicted: stable_high
confirmed). The Celtic agent has three contrast partners (Roman Republic, Greek
Democracy, Phoenician Merchant Oligarchies) and four comparator partners.
Contact with low-EDR Mediterranean systems activates schismogenesis, driving
the Celtic agent further toward its own governance pole rather than toward the
Mediterranean alternative. This is the Bateson mechanism in direct operation:
contrast contact with administrative urbanism strengthens, rather than erodes,
the governance alternative.

**Zomia Highland Communities:** EDR 0.92 → 0.972 ± 0.037 (predicted: stable_high
confirmed). Zomia has four contrast partners (Confucian Bureaucracy, Ming Yellow
Register Census, Khmer Devaraja, Khmer Water Mandala — all very low-EDR lowland
states) and three parallel partners. The contrast mechanism drives Zomia's EDR
to the ceiling. The near-zero variance (±0.037) reflects the stability of a
system with maximally dissimilar contrast partners. Scott's (2009) thesis that
Zomia maintained high illegibility *because of* lowland state contact is
directly reproduced.

**Iroquois Confederacy / Haudenosaunee:** EDR 0.77 → 0.616 ± 0.080 with
L-coupling onset at t = 200 (predicted: stable_then_decline confirmed). The
trajectory has two phases. Before colonial L-imposition (t < 200), the
Haudenosaunee agent rises toward ~0.88, sustained by contrast with hierarchical
alternatives. At t = 200, colonial administration raises L to 0.65 and activates
δ = 0.008 per-step drift. EDR declines smoothly to 0.616 by t = 500. This
two-phase trajectory couples the schismogenesis mechanism (sustains high EDR
through contrast-based identity) with the lock-in sequence (overwhelms it when
colonial L-imposition activates). Neither mechanism alone predicts the observed
historical arc.

---

## 6. Integrated Findings and Discussion

### 6.1 A unified account of long-run governance dynamics

The three mechanisms — phase space positioning, lock-in sequence, and
schismogenesis — are not independent. The lock-in sequence explains the
L-conditional shift in the CTMC stationary distribution: as L rises, the
appointment attractor strengthens because the administrative infrastructure
that high L creates is precisely what appointment-based governance exploits.
The schismogenesis mechanism explains why this shift is not universal: systems
in the high-EDR cluster are reinforced in their distinctiveness by contrast
with the appointment-converging low-EDR cluster, as long as the schismogenesis
dynamic is stronger than the L-imposition force. When L-imposition overwhelms
it — as in the Haudenosaunee case — the two-phase trajectory results.

The D₀ moderator connects the succession model to the schismogenesis model.
In the succession model, high D₀ quintuples the stability of elective succession
against the appointment attractor (Section 4.3). In the schismogenesis model,
the counter-cases (Section 3.2) all have high D₀ established before legibility
reached its current level. The mechanism is the same in both: pre-existing
disobedience freedom raises the cost of the lock-in transition — whether that
transition is the succession of a ruler (succession model) or the administrative
incorporation of a community (schismogenesis model).

### 6.2 The Graeber-Wengrow argument and the one-way valve

The consensus founding-state finding (Section 4.3) and the calibration ceiling
(Section 5.3) together support the Graeber-Wengrow claim about asymmetric
freedom loss. The consensus finding establishes a one-way valve: governance
systems can transition from consensus to hereditary or appointment, but zero
documented cases show the reverse. The calibration ceiling establishes that
the full ΔEDR distribution of the citation network requires historically specific
contact patterns — the Celts specifically contrasted themselves with Rome, not
with every low-EDR system in the database.

Both findings are consistent with the Graeber-Wengrow thesis that governance
diversity reflects deliberate choices responding to proximate alternatives, not
random variation, and that some of those choices are much harder to reverse than
to make. The framework makes this thesis quantitatively precise: the one-way
valve is visible in the transition matrix, the deliberate differentiation is
visible in the schismogenesis signal (contrast edges have larger ΔEDR than
comparator edges, p = 0.00015), and the irreversibility is visible in the CTMC
stationary distribution (π(consensus) ≈ 0.04 despite 16% observed frequency).

### 6.3 Contemporary implications

The lock-in sequence's contemporary relevance is most acute where the P→S
pathway (competitive politics generating sovereignty) and rising digital
legibility interact. Digital administrative systems raise L and I simultaneously
and at a pace that may outstrip the development of constitutional D mechanisms.
The Norwegian and Swiss counter-cases suggest the protective mechanism: D₀
established before L rises. Systems that are building digital administrative
capacity without simultaneously encoding disobedience freedom in institutions
that predate the administrative apparatus may be retracing the Uruk sequence
at compressed timescales.

The schismogenesis model's contemporary relevance concerns governance
polarisation. The degree-4 sign reversal in the historical citation network
suggests that governance contact between dissimilar systems tends to intensify
rather than reduce differences. Contemporary evidence of democratic backsliding
in systems with high exposure to authoritarian governance models is consistent
with the schismogenesis prediction: the contrast mechanism reinforces each
system's existing trajectory. Whether the γ/β condition (schismogenesis ≥
contagion) holds in contemporary governance contact networks is an empirical
question the framework can in principle address once contemporary network data
is coded.

---

## 7. Limitations

**Single-value L and D₀ coding.** Each governance system is assigned a single
characteristic value for L and D₀, not a time series. Systems with documented
internal variation (Tang Dynasty 618–907 CE, Ottoman Empire 1299–1922 CE) are
coded to their modal or representative period. This attenuates the dynamic
effects in the CTMC and introduces bias toward mean-regression in the transition
analysis.

**Selection bias in the transition dataset.** Documented succession mechanism
transitions are concentrated among historically rich polities — Mesopotamian,
East Asian, and Mediterranean state sequences. Pre-state, oral-tradition, and
non-literate societies are underrepresented, potentially overstating the
frequency of high-L transition patterns in the dynamic model.

**Markov property.** The CTMC assumes transition rates from any state depend
only on the current state. This is likely violated: systems that previously
maintained elective succession and are forced temporarily into appointment by
external shock (Athens under the Thirty Tyrants) may be more likely to return
to elective than systems that have always been appointment-based. The available
n (43 type-changing transitions) is insufficient to estimate history-dependent
models.

**ABM plausibility vs. simulation.** The schismogenesis ABM is a plausibility
model testing whether local schismogenesis rules are sufficient to generate the
observed network topology. It is not a historical simulation of the process
that produced the network. No mapping from model time-steps to historical time
is attempted.

**Three-cluster approximation.** The empirical citation network has 14 Louvain
communities; the ABM uses three initialisation clusters. The approximation
captures the topology needed for the degree-4 sign reversal (bridge region
between high- and low-EDR clusters) but not the internal structure of any
individual community.

---

## 8. Conclusion

We have presented a unified computational framework for long-run governance
dynamics integrating three mechanisms across three analytical levels. The
phase-space framework (SAP-EDR, r = −0.738, validated across six external
datasets) provides the measurement scaffold. The lock-in sequence (six-stage
causal chain, CTMC logistic regression OR = 2.24 permutation p = 0.005,
D₀ moderator ratio 5.03×) provides the mechanistic account of freedom
suppression. The schismogenesis ABM (sign reversal reproduced, modularity
M = 0.448, three G-W case studies confirmed) provides the network-level account
of governance differentiation.

The integrated framework makes a specific claim about governance resilience:
the systems that maintain high EDR under high L are those that established
institutionally robust disobedience freedom before legibility rose. This
prediction is confirmed in the static model (OR = 6.46), the dynamic model
(5.03× exit rate ratio), and the case study trajectories (Zomia, Celtic). The
Haudenosaunee case demonstrates the complementary prediction: when L-imposition
overwhelms pre-existing D, the schismogenesis mechanism that had sustained
high EDR is insufficient to prevent lock-in.

Three research directions follow directly. First, extending the CTMC to
history-dependent transition rates requires more coded transitions, particularly
in the consensus→other and rotation→other cells currently estimated by Laplace
smoothing. Second, replacing the distance-based edge-formation rule in the ABM
with historically structured awareness sets would test whether the calibration
ceiling is closed by known contact patterns. Third, applying the framework to
contemporary digital governance — where L and I are rising rapidly in many
jurisdictions — would test whether the lock-in sequence's predictions hold at
the decadal timescale.

---

## References

Bateson, G. (1935). Culture contact and schismogenesis. *Man*, 35, 178–183.

Bateson, G. (1958). *Naven* (2nd ed.). Stanford University Press.

Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). Fast
unfolding of communities in large networks. *Journal of Statistical Mechanics*,
P10008.

Clauset, A., Shalizi, C. R., & Newman, M. E. J. (2009). Power-law distributions
in empirical data. *SIAM Review*, 51(4), 661–703.

Cox, D. R. (1972). Regression models and life-tables. *Journal of the Royal
Statistical Society B*, 34(2), 187–220.

Coppedge, M., Gerring, J., Knutsen, C. H., Lindberg, S. I., Teorell, J., et al.
(2023). *V-Dem dataset v16*. Varieties of Democracy Project.
https://www.v-dem.net

Elkins, Z., Ginsburg, T., & Melton, J. (2025). *Comparative Constitutions
Project: Constitute*, v5. https://comparativeconstitutionsproject.org

Freedom House. (2021). *Freedom in the World 2013–2021: Aggregate Category and
Subcategory Scores*. Freedom House.

Gavrilets, S. (2010). Rapid transition towards the egalitarian syndrome.
*PLOS Computational Biology*, 8(e1002035).

Graeber, D., & Wengrow, D. (2021). *The Dawn of Everything: A New History of
Humanity*. Allen Lane.

Marshall, M. G., & Gurr, T. R. (2020). *Polity5: Political Regime
Characteristics and Transitions, 1800–2018*. Center for Systemic Peace.

Motesharrei, S., Rivas, J., & Kalnay, E. (2014). Human and nature dynamics
(HANDY). *Ecological Economics*, 101, 90–102.

Newman, M. E. J. (2006). Modularity and community structure in networks.
*PNAS*, 103(23), 8577–8582.

Scott, J. C. (2009). *The Art of Not Being Governed*. Yale University Press.

Scott, J. C. (2017). *Against the Grain: A Deep History of the Earliest States*.
Yale University Press.

Tainter, J. (1988). *The Collapse of Complex Societies*. Cambridge University
Press.

Turchin, P. (2003). *Historical Dynamics*. Princeton University Press.

Turchin, P. (2016). *Ages of Discord*. Beresta Books.

Turchin, P., Currie, T. E., Turner, E. A. L., & Gavrilets, S. (2013). War,
space, and the evolution of Old World complex societies. *PNAS*, 110(41),
16384–16389.

Turchin, P., et al. (2015). Seshat: The Global History Databank.
*Cliodynamics*, 6(1), 77–107.

World Justice Project. (2025). *WJP Rule of Law Index: Historical Data
2012–2025*. https://worldjusticeproject.org
