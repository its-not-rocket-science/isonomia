# Isonomia III: Succession Mechanism Attraction Basins and the Lock-In Sequence

**Working paper — isonomia series, Paper 3**

*Corresponding author: [Author]*
*Independent researcher*
*Repository: https://github.com/its-not-rocket-science/isonomia*
*Dataset: https://github.com/its-not-rocket-science/global-governance-models*

**Data availability:** All data, code, and figures are publicly available at https://github.com/its-not-rocket-science/isonomia under MIT licence. The succession model analysis scripts are `src/succession_attraction_basins.py` (Phases 1–2) and `src/succession_markov_ctmc.py` (Phase 3). The survival spell dataset (`data/survival_spells.csv`) and transition event dataset (`data/transition_data.csv`) are generated directly from `data/governance_extended.csv` by running these scripts. Data will additionally be deposited in the JWSR Dataverse upon acceptance.

---

> **Abstract**
>
> The lock-in sequence (Paper 2) predicts that rising surplus legibility (L) shifts succession mechanisms toward bureaucratic appointment and hereditary forms as disobedience freedom (D) is suppressed. We test this through three phases of empirical analysis across 389 governance systems spanning 12,000 years. Phase 1 (static model, n = 117 hand-coded systems): L and pre-existing disobedience freedom (D₀) together predict succession type with χ² = 25.08 (df = 4, p < 0.0001). Among high-L systems, D₀ discriminates elective from hereditary succession with OR = 6.46 (Mann-Whitney p = 0.0001, rank-biserial r = −0.782). Phase 2 (transition matrix, 43 type-changing events): elite reform events produce 0% hereditary outcomes (11 cases); internal crises produce 56% hereditary. The probability of transitioning to appointment is higher at high L (54%) than low L (25%), confirmed by logistic regression (OR = 2.24, permutation p = 0.005). Phase 3 (CTMC, 149 spells, 39 events, 110,589 system-years): appointment succession rises from π = 0.136 at low L to π = 0.595 at high L (+0.460); elective falls from π = 0.394 to π = 0.115 (−0.279). The D₀ moderator operates dynamically: high-D₀ elective systems exit elective succession at 0.55 per 1000 years versus 2.74 for low-D₀ systems (5.03×; Cox PH joint test p = 0.026). The logistic regression on transition outcomes is the primary significant result; the CTMC provides its dynamic formalisation. A secondary finding with direct theoretical import concerns consensus succession: CTMC π(consensus) ≈ 0.04 at all L levels, yet 16% of the cross-section is coded as consensus. This discrepancy identifies consensus as a founding state rather than an equilibrium state — a one-way valve into the transition process that has no documented reverse — directly supporting the Graeber-Wengrow claim that the permanent loss of certain freedoms is qualitatively distinct from their temporary suppression.

---

## 1. Introduction

The lock-in sequence proposed in Paper 2 of this series describes a specific causal pathway through which rising surplus legibility (L) suppresses the three freedoms that constitute governance resilience. As L rises, the capacity for administrative surveillance and extraction increases (A↑). Rising A enables more precise information infrastructure (I↑), which in turn enables S (sovereignty) consolidation. E (exit freedom) is suppressed directly as populations become bound to legible occupations and fixed locations. D (disobedience freedom) weakens as the administrative apparatus capable of tracking and punishing dissent is constructed. R (arrangement freedom) is eliminated as the institutions that permit social reorganisation are dismantled or captured. The EDR composite falls below the resilience threshold θ ≈ 0.45, and the society enters the fragile regime in which Turchin-Tainter collapse dynamics operate.

This sequence makes a specific and testable prediction about succession mechanisms. If it is correct, then as L increases, governance systems should shift away from succession mechanisms that require ongoing consent — elective, rotation, and consensus forms — toward mechanisms that concentrate authority without requiring that consent: hereditary succession and, especially, bureaucratic appointment. The appointment prediction is theoretically specific: it is not that high-L systems collapse to simple dynastic hereditary rule, but that rising A creates a bureaucratic infrastructure that appointment-based office-holding exploits. The meritocratic examination system of the Tang and Song dynasties, the Confucian bureaucracy, the Mauryan administrative reforms, and the Habsburg centralisation all represent the appointment attractor operating at high L — each arose from a preceding hereditary system as the administrative apparatus grew sophisticated enough to manage empire by competence rather than kinship alone.

The D₀ moderator prediction is equally specific. If pre-existing disobedience freedom is what determines which basin a high-L system occupies in the static cross-section (Paper 2's Phase 1 finding), then it should also determine how long a system *stays* in its elective basin once there. High-D₀ elective systems should be more stable against the appointment and hereditary attractors — not because they face different structural pressures, but because the social memory of disobedience as a legitimate political act provides a resource for resisting lock-in that low-D₀ systems lack.

Both predictions are empirically tractable. Succession mechanism is one of the best-documented variables in comparative historical analysis — the rules by which rulers are replaced leave records in chronicles, inscriptions, and institutional texts even when the inner workings of governance are obscure. Time-ordering is possible: we know not just what succession mechanism a polity used, but in many cases when and why it changed. And the changes, when they occur, tend to be legible as events rather than gradual processes.

This paper reports three phases of empirical analysis structured to test these predictions with increasing dynamical sophistication.

---

## 2. The Succession Mechanism Typology

We classify succession mechanisms into five canonical types, derived from the operationalisation of the three elementary forms of domination (sovereignty, administration, competitive politics) and their interaction with the three freedoms (exit, disobedience, arrangement).

**Hereditary succession** is the transmission of highest office through kinship lines, typically patrilateral but including matrilineal and bilateral forms. It requires high S (the office-holder has the coercive authority to enforce succession) and moderate A (records of lineage). It is independent of both D (the successor need not be consented to) and R (institutional reorganisation cannot change the succession mechanism without destroying the lineage system). Examples: Tang Dynasty, Ottoman Empire, Egyptian Old Kingdom, Mauryan Empire before Ashoka's administrative reforms.

**Appointment succession** is the selection of office-holders by an established authority with the power to recruit on criteria other than kinship. It requires high A (records, examinations, administrative apparatus) and typically high S (the appointing authority must be able to enforce its selections). The distinctive feature of appointment is that it decouples A from S: bureaucratic competence becomes a route to authority independent of hereditary claim. Examples: Tang Dynasty Keju examination system, Confucian Bureaucracy, Ming Yellow Register Census administration, Habsburg Composite Monarchy after the Haugwitz reforms, Assyrian military autocracy after Tiglath-Pileser III.

**Elective succession** is the selection of office-holders through a defined voting or acclamation procedure involving more than a single appointing authority. It requires high P (competitive display and prestige performance) and D (the voters must be able to refuse candidates without fatal consequence). It is characterised by the structural requirement for ongoing consent: elective systems cannot reproduce themselves through a single holder's will. Examples: Roman Republic, Venetian Merchant Oligarchy, Holy Roman Empire Electoral College, Norse Thing system, Athenian Democracy.

**Consensus succession** is the emergence of authority through collective agreement without formal voting. It requires high D (the community must be able to refuse without consequence) and high R (the community retains the arrangement freedom to constitute and reconstitute authority). It is the form most clearly associated with pre-state and small-scale societies, and the one that most directly preserves the Graeber-Wengrow freedoms. Examples: Iroquois Confederacy, Gadaa System (Oromo), !Kung San, Aboriginal Elders Councils, many pre-pottery Neolithic communities.

**Rotation succession** is the structured circulation of office-holding through a defined group, often an age-grade or lineage segment, according to a schedule rather than a competitive or hereditary mechanism. It preserves R (the institution rotates rather than concentrating) and requires low S (no individual accumulates the coercive authority needed to capture the rotation schedule). Examples: Gadaa System (eight-year age-grade rotation), Andean Tinku (ritual competition determining rotation), Swiss Cantonal Democracy in its early form.

These five types are canonical simplifications. Real systems combine elements: the Venetian system combined sortition (elective) with appointment (the Broglio process) and hereditary eligibility (the Serrata). The typology is used as a modelling tool, not an empirical claim about categorical discreteness.

---

## 3. Phase 1: Static Attraction Basin Analysis

### 3.1 Data and methods

The working set for Phase 1 is the hand-coded subset of the isonomia governance dataset with succession type, surplus legibility, and disobedience freedom all coded (n = 117, confidence 2–3). Systems coded as charismatic (n = 8) are excluded as a distinct category that does not map cleanly onto the five canonical types — charismatic leadership is an origin state rather than a stable succession mechanism, and charismatic systems in the dataset almost universally transition within their first century of attestation. The working set contains: hereditary (n = 37), elective (n = 35), appointment (n = 20), consensus (n = 19), rotation (n = 6). Succession type, surplus legibility, and disobedience freedom are coded at the level of the system as a whole (single values rather than time series); the implications of this for the dynamic model are addressed in Section 6.

The static analysis uses two approaches: a multinomial logistic regression of succession type on L, D₀, and their interaction (L × D₀), providing predicted probability curves across the full L and D₀ space; and a Mann-Whitney U test on D₀ comparing elective versus hereditary systems in the high-L subsample (L ≥ 0.60), directly testing the attraction basin prediction.

### 3.2 Results

The cross-tabulation of succession type against L regime (low: L < 0.60; high: L ≥ 0.60) yields χ² = 25.08 (df = 4, p < 0.0001). This establishes that surplus legibility predicts the distribution of succession types: at low L, consensus (n = 14 of 19 in low-L) and rotation (n = 4 of 6 in low-L) dominate; at high L, hereditary (n = 26 of 37 in high-L) and appointment (n = 17 of 20 in high-L) dominate; elective systems are distributed across both L regimes but with a median L = 0.57, straddling the threshold.

The attraction basin test focuses on the high-L subsample, where the lock-in sequence prediction is most specific: among systems at high L, D₀ should discriminate which basin they occupy. High-L elective systems have a median D₀ = 0.55 (n = 12); high-L hereditary systems have a median D₀ = 0.17 (n = 26). This difference is large and statistically clear: Mann-Whitney U = 278, p = 0.0001 (two-sided), rank-biserial r = −0.782. A binary logistic regression of elective versus hereditary outcome on D₀ in the high-L subsample yields OR = 6.46: each one-unit increase in D₀ multiplies the odds of occupying the elective rather than hereditary basin by 6.46. The rank-biserial r of −0.782 means that in approximately 89% of elective-hereditary paired comparisons, the elective system has the higher D₀.

The multinomial logistic regression (L + D₀ + L × D₀) achieves an accuracy of 0.598 on five classes. The interaction term produces the theoretically expected moderator pattern: at low D₀ (D₀ = 0.10), P(hereditary | L = 0.80) = 0.65 and P(elective | L = 0.80) = 0.05; at high D₀ (D₀ = 0.85), P(elective | L = 0.80) = 0.75 and P(hereditary | L = 0.80) = 0.00. The shift in the predicted probability curves between high and low D₀ — Figure 2B (multinomial logistic predicted probabilities, solid line D₀ = 0.85 versus dashed D₀ = 0.10) — is the static cross-sectional expression of the lock-in sequence moderator: D₀ determines not just the current basin but, within the high-L zone, which attractor dominates.

These Phase 1 results replicate and extend findings reported in Paper 2 and represent the strongest evidence in this paper. The static finding does not depend on the CTMC machinery and is robust to the data limitations described in Section 6.

---

## 4. Phase 2: Empirical Transition Matrix

### 4.1 Data and methods

Phase 2 moves from the static cross-section to documented within-system succession mechanism changes. These are encoded in the `succession_changes` field of `governance_extended.csv` in structured format: `[from_type]->[to_type] (YEAR): trigger_note`. Each entry records the origin succession type, the destination type, the approximate year, and the triggering mechanism (P_to_S, external_shock, elite_reform, collapse, reconsolidation, or internal).

The Phase 2 dataset contains 57 transition entries across 44 systems, of which 43 are type-changing transitions (from ≠ to) and 14 are same-type transitions that record a documented shift in L or D₀ without a mechanism change. The same-type transitions are retained in the Phase 3 survival dataset as evidence of stability under L change but are excluded from the transition matrix analysis here.

### 4.2 The transition matrix

The raw transition matrix (type-changing events only, n = 43) contains twelve of twenty possible off-diagonal cells. The most populated cells are hereditary → appointment (n = 13, 81% of hereditary exit events), appointment → elective (n = 5, 71% of appointment exit events), and elective → hereditary (n = 6, 60% of elective exit events) with elective → appointment (n = 4, 40%) also notable. The rotation row is entirely dominated by rotation → hereditary (n = 4 of 5 rotation exit events).

Several cells remain empty: appointment → consensus, appointment → rotation, elective → consensus, elective → rotation, consensus → rotation, rotation → appointment, rotation → elective (excluding the Swiss case). These absences are theoretically meaningful rather than accidental. The pattern reflects two basin structures: the high-L basin (appointment ↔ hereditary ↔ elective), which has many documented transitions in both directions; and the low-L basin (consensus, rotation), which can transition to the high-L basin but almost never receives transitions from it. No documented case shows a polity transitioning from hereditary or appointment back to consensus — a finding consistent with the Graeber-Wengrow claim that the loss of specific freedoms is asymmetric and largely irreversible. Figure 3B presents the full transition matrix with cell counts and origin-type colour coding; the empty return path to consensus is annotated.

### 4.3 L-conditional transition probabilities

The lock-in sequence predicts that among type-changing transitions at high L, the probability of landing in appointment should be higher than at low L. In the 24 high-L transitions (L ≥ 0.60), appointment is the destination in 13 cases (54% compared to 25% in the 19 low-L transitions). A logistic regression of the binary outcome appointment versus not-appointment on continuous L, across all 43 type-changing transitions, yields a coefficient of 0.807 (OR = 2.24, permutation p = 0.005). This is the primary statistically significant result of the dynamic analysis: each standard-deviation increase in L at the time of a succession mechanism transition multiplies the odds of the transition landing in appointment succession by 2.24.

The permutation p-value of 0.005 is obtained by randomly shuffling the L values across the 43 transitions 5,000 times and computing the proportion of permuted logistic coefficients that exceed the observed coefficient. It is more appropriate than a parametric p-value here because the transition events are not independent (systems that generate one transition are more likely to generate another, and many of the high-L systems share cultural and epistemic contexts).

A further validation of the equilibrium prediction uses the cross-sectional distribution of succession types across all 401 systems. Among high-L systems (L > 0.70, n = 49), 59.2% are in appointment or hereditary succession; among low-L systems (L ≤ 0.40, n = 248), 35.5% are in appointment or hereditary (Mann-Whitney p = 0.001). This cross-sectional result provides independent confirmation of the CTMC's appointment attractor prediction. The transition data shows the complementary pattern: within high-L systems, 60.9% of documented transitions are appointment-to-appointment (already at the attractor), compared to 20.0% in low-L systems. The apparent paradox — that the point-biserial r(L, →appointment) is negative across all 57 transition events — resolves once this ceiling effect is accounted for. High-L systems generate fewer toward-appointment transitions precisely because they are already in appointment succession; their documented transitions are within-type movements that record L or D₀ changes while the succession mechanism is already at the CTMC's predicted equilibrium. This is consistent with, not contrary to, the model. Full replication code and the parsed transition event dataset (57 events, 44 systems) are in `src/succession_events.py` and `data/succession_events.csv`.

### 4.4 Trigger analysis

The trigger-type analysis provides qualitative grounding for the quantitative results. Among the 11 elite reform transitions, zero resulted in hereditary succession (0/11). Among the 9 internal succession crises, 5 resulted in hereditary succession (5/9 = 56%). Among the 11 external shock transitions, 6 resulted in hereditary succession (6/11 = 55%). Among the 5 collapse transitions, 2 resulted in appointment (40%) and 2 in hereditary (40%), with 1 in rotation.

A quantitative summary of the cause-direction relationship: external shock produced toward-appointment transitions at 60.0% and toward-freedom at 0%; elite reform produced toward-appointment at 6.2% and toward-freedom at 31.2%. Fisher exact test (external shock versus elite reform on toward-appointment rate) gives p = 0.002, confirming that the transition cause is a strong predictor of direction independent of the L level at the time of transition. Collapse produced the lowest toward-appointment rate (11.1%), consistent with the collapse-as-attractor-reset mechanism: when the administrative apparatus collapses, the system returns to lower L and lower A, reducing the forces driving toward the appointment attractor. Figure 3A presents these cause-direction relationships as a heatmap with row-normalised percentages. Figure 3C shows D at the time of transition by direction, illustrating the D₀ moderation pattern for elite reform recoveries and annotating the Athens −403 case. The full transition event dataset and replication code are in `src/succession_events.py` and `data/succession_events.csv`.

The elite reform finding is theoretically important. Elite reform transitions — those in which an internal coalition forces a change in the succession mechanism without collapse or conquest — universally produce appointment or elective destinations. The Norman → Magna Carta transition (appointment → elective) required pre-existing customary D that the Norman system had violated; the restoration of Athenian democracy after the Thirty Tyrants (appointment → elective) depended on civic D memory preserved through exile; the Haugwitz reforms in Habsburg Composite Monarchy and the Tiglath-Pileser reforms in Assyrian Military Autocracy both produced appointment systems from hereditary ones through administrative reorganisation that maintained D while restructuring A. None of these elite reform transitions produced hereditary outcomes. This is consistent with the D₀ moderator: elite reform requires sufficient D₀ to sustain the coalition that enforces the reform, and that pre-existing D₀ is incompatible with a hereditary outcome.

The internal and external shock findings tell the complementary story. When succession mechanism changes are forced on a system by conquest or dynastic crisis rather than chosen through elite coalition, hereditary outcomes are much more common. External military conquest tends to install the conquering dynasty's own hereditary mechanism. Internal succession crises — factional seizures, military coups, dynastic extinctions — tend to be resolved by whoever can assert sovereign force, which typically produces a new hereditary arrangement.

The exception that proves the rule is the P_to_S pathway — the mechanism first identified in the Roman Republican transition. Rome's transition from elective to hereditary occurred at D₀ = 0.50, the highest D₀ of any hereditary transition in the dataset. The mechanism is the competitive politics (P) route to sovereignty (S) bypassing D suppression: Octavian's accumulation of imperium and tribunicia potestas was achieved through the legal forms of the Republic and required no direct suppression of disobedience — the disobedience freedoms of the Senate and popular assemblies remained formally intact while the substance of authority had already transferred. This is the passive revolution mechanism described in Paper 2: constitutional forms preserve the appearance of freedom while the substance is evacuated. It appears once in the transition data; it is theoretically important precisely because of its rarity.

**Recovery depth: two mechanisms.** A further distinction within toward-freedom transitions reveals that the bulk D₀ moderation test (Section 4.3) is non-significant because it conflates two structurally different recovery mechanisms. Table 3 presents all eight toward-freedom transitions ordered by D₀ × (1−S).

| System | Year | Cause | D₀ | S | D₀×(1−S) | Recovery depth |
|---|---|---|---|---|---|---|
| Athenian Democracy | 403 BCE | Elite reform | 0.85 | 0.15 | 0.723 | Full — demokratia restored in 8 years |
| Dutch Republic States-General | 1581 CE | Elite reform | 0.60 | 0.30 | 0.420 | Full — sovereignty to States-General |
| Kurultai | 1260 CE | Collapse | 0.60 | 0.60 | 0.240 | Partial/unstable — Kublai consolidates |
| Classic Maya City-States | 900 CE | Reconsolidation | 0.35 | 0.65 | 0.122 | Partial — elective restoration during fragmentation |
| Greek Oligarchy | 508 BCE | Elite reform | 0.35 | 0.50 | 0.175 | Partial — Kleisthenic reforms, institutionally fragile |
| Greek Oligarchy | 403 BCE | Elite reform | 0.35 | 0.50 | 0.175 | Partial — post-Thirty restoration |
| Norman Feudal Domesday | 1215 CE | Elite reform | 0.15 | 0.75 | 0.037 | Partial — Magna Carta only, no mass freedom |
| Egyptian Old Kingdom | 2181 BCE | Collapse | 0.10 | 0.90 | 0.010 | Partial/unstable — nome rotation, conflict-ridden |

*Table 3. All toward-freedom succession transitions, ordered by D₀ × (1−S). Full recovery = D attained ≥ θ = 0.45.*

*Elite reform recoveries* (n = 5: Athens −403, Dutch Republic 1581, Cleisthenic reforms −508/−403, Magna Carta 1215) require pre-existing disobedience freedom as a coalition resource: the reform must be organised and enforced by an internal coalition, and that coalition's capacity depends on pre-existing civic D. Within these five cases, sovereign capacity S at the time of transition is a near-perfect predictor of recovery depth: r(S, D_attained) = −0.984, p = 0.002. S < 0.45 produces full recovery above the resilience threshold (Athens D = 0.85, Dutch Republic D = 0.60); S ≥ 0.45 produces partial constraint only (Greek oligarchic reforms D = 0.35, Magna Carta D = 0.15). The composite D₀ × (1 − S) — civic coalition resource multiplied by sovereign weakness — perfectly orders the five cases from Athens (0.72) through the Dutch Republic (0.42), Greek reforms (0.18), to Magna Carta (0.04). The Norman case is particularly informative: D₀ = 0.15 at the system level, but the baronial coalition held customary feudal rights as the relevant disobedience resource. Reform was possible because John's sovereign capacity was temporarily compromised by military defeat at Bouvines; the high S ceiling (0.75) prevented any recovery extending to mass political freedom. Figure 4A presents the S versus D scatter for elite reform recoveries with the regression line and θ = 0.45 threshold.

*Collapse recoveries* (n = 2: Egyptian Old Kingdom −2181, Kurultai 1260) show that D₀ is not causally required when the administrative apparatus dissolves from within. The Egyptian Old Kingdom produced a toward-freedom transition from D = 0.10 — the lowest D₀ of any recovery case — when the 4.2 kya drought event and administrative overextension dissolved nome-governor accountability to the centre. D rose as a consequence of state dissolution, not as a causal resource. The Kurultai case confirms the distinction: D₀ = 0.60 was present but did not enable durable recovery, because the transition was a power contest (Toluid Civil War) resolved by whichever claimant could consolidate force — Kublai Khan restored hereditary authority within a decade. Collapse recoveries are partial and structurally unstable; elite reform recoveries, when they occur at low S, can be durable. Figure 4B presents all eight recovery transitions by cause type with D₀ × (1−S) encoded as point size.

The implication is a refinement of the D₀ moderator claim from Paper 2: D₀ is the resource that determines *whether* elite reform recovery is possible; S is the ceiling that determines *how far* it goes. Full democratic restoration — succession type changing from appointment or hereditary to elective with D above the resilience threshold — requires both D₀ above a minimum coalition threshold and S below approximately 0.45. This two-condition prediction is supported by the data with the caveat that n = 5 elite reform recoveries precludes statistical confidence; the result should be treated as a theoretically interpretable pattern requiring replication as the transition dataset grows. Full analysis and replication code are in `src/recovery_depth.py`.

---

## 5. Phase 3: The Continuous-Time Markov Chain

### 5.1 Motivation

The Phase 2 transition matrix describes what happens when succession mechanisms change. But most governance systems most of the time do not change their succession mechanism. The Ming Dynasty maintained hereditary succession for 276 years before the Manchu conquest imposed appointment elements; Athenian Democracy survived intact for approximately 130 years between the reforms of Cleisthenes and the first oligarchic interruption. The discrete-time transition matrix, which treats each transition event as equally weighted regardless of dwell time, cannot recover the stationary distribution of the *system* — the fraction of time any governance system, in the long run, would spend in each succession type given the empirical rates of transition and stability.

The continuous-time Markov chain (CTMC) addresses this by weighting transitions by dwell time. Each spell — a contiguous period in one succession type by one system — contributes both its duration (time at risk) and any event (transition out) to the rate estimates. The transition rate from type *i* to type *j*, λ_{ij}, is estimated as the number of observed *i* → *j* transitions divided by the total time systems spent in state *i*. The Q matrix of off-diagonal rates, with diagonal entries equal to minus the row sum, characterises the instantaneous dynamics; its null space gives the stationary distribution.

### 5.2 Survival dataset

The survival dataset contains 149 spells from 119 systems, with 39 events (type-changing transitions) and 110,589 total system-years. Systems that experienced documented succession mechanism changes contribute multiple spells: for example, the Roman Republic contributes one elective spell from the Republic's founding to the Augustan transition (−509 to −27 BCE, duration 482 years, event = 1). Systems without documented transitions contribute a single censored spell covering their full attested duration: Norway contributes one elective spell from 1814 to the present, censored at 2026 (duration 212 years, event = 0).

Spells by succession type: hereditary (n = 46, 14 events, 25,466 system-years, median duration 307 years), elective (n = 45, 11 events, 17,218 system-years, median 230 years), appointment (n = 29, 5 events, 9,512 system-years, median 220 years), consensus (n = 20, 4 events, 51,230 system-years, median 2,400 years), rotation (n = 8, 4 events, 7,058 system-years, median 548 years).

The consensus system-year figure (51,230 years from 4 events) reflects the genuine empirical situation: pre-state and small-scale societies organised around consensus governance lasted for thousands of years without documented succession mechanism changes. The Natufian Communities operated for approximately 4,000 years; Aboriginal Elders Councils for comparable durations. These are not data deficiencies. They contribute to the CTMC as evidence that consensus is an extremely stable succession mechanism once established, with a very low exit rate.

Censoring is assumed non-informative: the decision to end an observation is assumed to be independent of whether the system would subsequently transition. The trigger-type analysis (Section 4.4) provides partial support for this assumption: external-shock transitions, which would be the most likely source of informative censoring (conquest-absorbed systems systematically ending in hereditary outcomes), constitute only 11 of 43 type-changing transitions.

### 5.3 The Q matrix and stationary distributions

The estimated Q matrix (per 1000 years, Laplace-smoothed at 0.003 per 1000 system-years for zero-count cells) is:

|  | →hereditary | →appointment | →elective | →consensus | →rotation |
|---|---|---|---|---|---|
| hereditary | −0.562 | 0.435 | 0.082 | 0.003 | 0.042 |
| appointment | 0.213 | −0.538 | 0.318 | 0.003 | 0.003 |
| elective | 0.352 | 0.235 | −0.593 | 0.003 | 0.003 |
| consensus | 0.042 | 0.023 | 0.023 | −0.090 | 0.003 |
| rotation | 0.570 | 0.003 | 0.003 | 0.003 | −0.579 |

The rotation → hereditary rate (0.570 per 1000 years) is the highest off-diagonal entry, reflecting that rotation systems, when they do transition, overwhelmingly move to hereditary (4 of 5 rotation exit events). The hereditary → appointment rate (0.435) is the second highest and is the mechanistic core of the lock-in sequence prediction: high-L hereditary systems exit to appointment at the highest rate of any type-changing transition in the matrix.

The stationary distributions, computed from the null space of Q^T, are shown for the full dataset and the L-conditional subsets. All data: hereditary 0.322, appointment 0.367, elective 0.243, consensus 0.041, rotation 0.028. Low-L (L < 0.60): hereditary 0.414, appointment 0.135, elective 0.394, consensus 0.050, rotation 0.007. High-L (L ≥ 0.60): hereditary 0.263, appointment 0.595, elective 0.115, consensus 0.004, rotation 0.023.

The appointment shift at high L — from π = 0.135 to π = 0.595, Δπ = +0.460 — is the central CTMC result and directly confirms the lock-in sequence prediction. It refines the prediction in an important way: the primary attractor at high L is not hereditary but appointment. Hereditary succession also falls from 0.414 to 0.263 at high L. The lock-in sequence does not simply consolidate hereditary authority; it builds the administrative infrastructure that appointment-based governance can exploit. The meritocratic examination state, the appointed prefectural bureaucracy, and the professional military administration are all high-L outcomes that are distinct from simple dynasticism. This distinction has implications for how the relationship between complexity and freedom is theorised: the suppression of E and D through A does not terminate in a hereditary arrangement but in a bureaucratic one, where the absence of freedom is administered rather than simply coerced.

The elective fall from 0.394 to 0.115 is the complementary result: at high L, elective succession becomes dynamically unstable. The 0.115 stationary probability at high L does not mean elective systems are impossible at high L — Norway, Switzerland, and the Venetian Republic all maintain high-L elective systems — but that they require active maintenance against the appointment attractor. The D₀ moderator result (Section 5.4) explains what that maintenance consists of.

### 5.4 The D₀ moderator at the dynamic level

The central prediction of Paper 2's lock-in sequence analysis is that D₀ — pre-existing disobedience freedom — is the variable that determines whether a high-L system resists the lock-in trajectory. Phase 1 confirms this at the static level. Phase 3 tests whether D₀ also affects the *dynamics*: do high-D₀ elective systems exit elective succession more slowly than low-D₀ elective systems?

The CTMC answers this through dwell-time comparison. Elective systems with D₀ ≥ 0.45 exit elective succession at 0.546 per 1000 system-years (9 events, 16,489 system-years). Elective systems with D₀ < 0.45 exit at 2.744 per 1000 system-years (2 events, 729 system-years). The ratio is 5.03×: high-D₀ elective systems exit elective succession approximately five times more slowly than low-D₀ elective systems.

The dynamic D₀ result is best understood as a mechanistic complement to the well-powered Phase 1 finding rather than an independent test. The Phase 1 evidence is strong: OR = 6.46, rank-biserial r = −0.782, n = 38, p = 0.0001. It establishes that high-D₀ systems disproportionately *occupy* the elective basin at any cross-section. Phase 3 asks whether they also *stay* there longer once in it. The answer is yes, with a 5× rate ratio — but the low-D₀ elective denominator contains only 2 events in 729 system-years, so the estimate is imprecise. A logrank test yields p = 0.116. The Cox PH joint test (L and D₀ together) reaches p = 0.026, supporting the joint model even where individual coefficients do not. The appropriate framing is: Phase 1 demonstrates that D₀ determines basin occupancy with high confidence; Phase 3 demonstrates, with appropriate uncertainty, that D₀ also prolongs dwell time in the elective basin. Both findings are consistent with the same underlying mechanism — pre-existing disobedience freedom raises the cost of the transition to appointment or hereditary succession — operating at the static and dynamic levels respectively.

A Cox proportional hazards regression with L and D₀ as covariates across the full survival dataset yields an L hazard ratio of 2.39 (p = 0.258) and a D₀ hazard ratio of 0.42 (p = 0.160). Neither is individually significant, but the log-likelihood ratio test for the joint model is significant (χ² = 7.28 on 2 df, p = 0.026), meaning L and D₀ together predict succession mechanism stability at a level that cannot be attributed to chance.

A complementary survival analysis using the 15 trajectory systems that begin above D = 0.45 (Paper 2, `src/survival_analysis.py`) provides an independent test of what predicts time-to-crossing at the dynamic level. The results are structurally consistent with the CTMC but resolve in a different direction: S at the time of trajectory start, not L, is the structural gate variable (concordance index C(S) = 0.940, log-rank p = 0.007; C(L) = 0.543, log-rank p = 0.68). The mechanism class — hegemonic capture, administrative closure, counter-hegemonic — is the strongest predictor (multivariate log-rank p = 0.001). Counter-hegemonic systems show only 12.5% event rate across the full observation window, with the counter-cases from Paper 2 (British Parliament, Swiss Canton, Norwegian, Icelandic Commonwealth) all remaining censored above θ. This finding does not contradict the CTMC — which is calibrated on the full succession dataset including many low-D₀ systems — but refines the dynamic mechanism: L creates the precondition for lock-in, but whether crossing occurs depends on whether L has been allowed to translate into high S. The counter-case systems maintained low S despite rising L through institutional constraints on sovereign capacity; this is what the survival analysis confirms dynamically.

### 5.5 Consensus as founding state rather than equilibrium state

A notable discrepancy between the CTMC stationary distribution and the observed cross-sectional frequencies concerns consensus succession. The CTMC gives π(consensus) ≈ 0.04 at both low and high L, whereas 16% of the Phase 1 working set is coded as consensus (n = 19). Why does the CTMC so substantially underestimate consensus frequency?

The answer is structural. The CTMC models the long-run dynamics of a system that enters the transition process: it estimates the fraction of time a succession mechanism occupies each state given the empirical rates of entry and exit. But consensus systems, in the historical record, almost never enter the transition process *from* other succession types. There is not a single documented case in the transition dataset of a system transitioning from hereditary or appointment back to consensus. There are three transitions from consensus to other types (consensus → hereditary twice, consensus → appointment once, all under colonial imposition). The pathway from consensus to other types is open; the pathway back is closed.

This means that the 19 consensus systems in the working set are not primarily systems that arrived at consensus from other succession mechanisms — they are systems that *began* as consensus forms, in many cases from the first period of their attestation, and remained in that form without documented change until absorbed by external states. They are founding states, not equilibrium states. The CTMC correctly identifies that the equilibrium dynamics — the long-run fate of any system that enters the transition process — heavily favour appointment, hereditary, and elective. What the CTMC cannot recover is the prior question: why are some societies never drawn into the transition process at all?

This finding is one of the most theoretically important in this paper because it directly supports the Graeber-Wengrow argument about the asymmetric and largely irreversible nature of freedom loss. The historical record shows a one-way valve: systems can move from consensus to hereditary or appointment, but not back. The CTMC's low π(consensus) is not a modelling failure — it is an accurate reflection of the empirical transition dynamics — and the discrepancy with the observed frequency is itself evidence of a qualitative distinction between two governance regimes: those that have entered the lock-in sequence and those that have not.

---

## 6. Data and Methodological Limitations

Several limitations of the current analysis merit explicit discussion.

**Single-value L and D₀ coding.** The most consequential limitation is that each governance system is assigned a single value for L and D₀ representing its characteristic level across its full attested period. Systems with long histories and documented internal changes — the Tang Dynasty operated across three centuries with substantial variation in administrative centralisation; the Ottoman Empire under Suleiman was different in both L and D₀ from the late Ottoman period under Abdulhamid II — are assigned a single value that represents an average or modal state. This means that spell-level L and D₀ values in the survival dataset are approximations. The Phase 1 static model, which uses each system's single coded value for cross-sectional analysis, is unaffected. The Phase 3 CTMC, which constructs time-varying spell data, is affected in proportion to how much L and D₀ varied within systems that contributed multiple spells. The direction of this bias is towards attenuation: if L genuinely rose between a system's first and second spell, coding both spells with the same intermediate L value will underestimate the effect of L-change on transition probability.

**Event count and power.** The D₀ moderator survival comparison is based on 2 events in the low-D₀ elective group. Any result from a 2-event analysis is fragile to additional data. The direction (high-D₀ elective systems exiting five times more slowly) is strongly consistent with the Phase 1 static finding and theoretically predicted, but the magnitude is uncertain. The Phase 1 result (OR = 6.46, p = 0.0001, n = 38) is the load-bearing claim; the Phase 3 result provides mechanistic confirmation at the dynamic level while the event count remains thin.

**Non-informative censoring assumption.** The CTMC assumes that censoring is non-informative — that systems without documented succession transitions did not transition off-screen. For pre-state societies with very long consensus spells (Natufian, PPNB, Aboriginal), this assumption is almost certainly violated: many of these systems will have experienced internal succession changes that are not recoverable from the archaeological record. If these unobserved transitions would have shown consensus → hereditary patterns, the true consensus exit rate is higher than estimated, and π(consensus) in the CTMC is overstated. Given that π(consensus) is already low (0.04), this would not change the substantive results.

**Markov property.** The CTMC assumes that transition rates from any state depend only on the current state, not on the history of prior states. This is likely violated: a system that transitioned from elective to appointment under external shock (e.g., Athenian democracy under Macedonian conquest) may be more likely to return to elective if the external constraint is removed, precisely because of its prior history. The Athenian case (elective → appointment → elective within 20 years) is the canonical example. The available n is not sufficient to estimate history-dependent models, and the Markov assumption is retained as the standard starting point for sparse-data chain estimation.

**Selection into the transition dataset.** The 44 systems with documented succession transitions are not a random sample of all governance systems. They are disproportionately systems with rich documentary records — primarily East Asian imperial polities, European feudal and constitutional states, and ancient Mediterranean city-states. Pre-state, oral-tradition, and non-literate systems are underrepresented in the transition data even when they appear in the static working set. This produces a bias toward finding the high-L transition patterns (hereditary → appointment) that characterise literate, administrative states, and may understate the frequency of low-L transitions (consensus → rotation, rotation → elective) that would appear in better-documented pre-state material.

---

## 7. Discussion

### 7.1 The appointment attractor

The most substantively important finding of this paper is that the primary attractor at high surplus legibility is appointment succession, not hereditary succession. This refines the lock-in sequence prediction in a way that has theoretical implications extending beyond the succession model.

The lock-in sequence (Paper 2) identifies rising administrative capacity (A) as the proximate mechanism through which L suppresses E and D: as the state builds the apparatus of surveillance, taxation, and population management, it simultaneously builds the infrastructure for bureaucratic appointment. What happens to hereditary succession as A rises? The historical record is consistent: hereditary succession tends to survive at high L as a legitimating frame while the substance of governance shifts to appointment. The Tang emperor was formally hereditary, but actual governance was administered by the Keju-selected mandarin class. The Ming Yellow Register Census hereditary system coexisted with an appointment-based civilian bureaucracy. The Ottoman Empire maintained hereditary succession to the sultanate while governing through the devshirme system of appointed slave-officials. The Habsburg Composite Monarchy retained hereditary forms while the Haugwitz reforms built the appointed bureaucracy that was the actual instrument of governance.

This pattern suggests that the lock-in sequence does not terminate in a simple hereditary arrangement but in a *dual structure*: hereditary legitimation combined with appointment governance. The former maintains the appearance of descent-based authority (satisfying the S dimension); the latter builds the administrative apparatus (satisfying the A dimension) while ensuring that those who hold actual power do so at the pleasure of an appointing authority. This dual structure is precisely the arrangement under which D and R are most thoroughly suppressed: the hereditary frame closes off the possibility of elective challenge, while the appointment structure ensures that individual office-holders have no independent claim to their positions.

### 7.2 The D₀ moderator and the counter-case prediction

The D₀ moderator result — that pre-existing disobedience freedom quintuples the stability of elective succession at the dynamic level, consistent with the static OR of 6.46 — provides a specific mechanism for the counter-cases identified in Paper 2: governance systems that maintain high EDR despite high L.

The mechanism is not that D₀ prevents L from rising, nor that it prevents the administrative apparatus from being constructed. Norway has among the highest L in the dataset and a highly developed administrative state; Switzerland's federal tax system, healthcare infrastructure, and digital identity systems are fully legible. What D₀ provides is a cultural and institutional memory of disobedience as a legitimate political act — the right to refuse, to appeal, to strike, to vote out, to constitutionally constrain — that makes the transition from elective to appointment succession costly rather than cheap.

In the transition dataset, all 11 elite reform transitions produce elective or appointment outcomes, never hereditary. The mechanism is exactly this: elite reform requires enough D₀ to sustain the coalition that forces the change, and that D₀ is structurally incompatible with accepting a hereditary outcome. The high-D₀ systems that do transition — the Venetian Serrata, for example, which moved from open-elective to restricted-elective in 1297 — tend to move within the elective basin (sortition among an eligible oligarchy) rather than exiting to appointment or hereditary. Even the compression of elective mechanisms at high L preserves the formal requirement for consent.

The counter-case prediction has a specific implication for contemporary governance: the stability of democratic institutions under conditions of rising administrative legibility depends on the maintenance of D₀ — on practices and institutions that preserve disobedience as legitimate — not just on formal constitutional structures. The CCP de jure/de facto gap analysis in Paper 1 (Section 10.2) illustrates this directly: the Soviet 1977 constitution enshrined the freedoms that were simultaneously denied in practice. Constitutional text codes the formal D₀ = 0.75; the de facto D₀ = 0.05. What protects the elective basin is not the text but the living practice.

### 7.3 Consensus as a separate regime

The consensus founding-state finding (Section 5.5) suggests that the succession model describes two structurally distinct regimes rather than one continuous dynamic. Regime I consists of pre-state and small-scale societies that begin in consensus or rotation forms and remain there without entering the transition process. Their trajectory in the governance phase space is determined primarily by ecological, demographic, and cultural factors, not by the lock-in sequence. Regime II consists of state and proto-state societies that have entered the transition process — through conquest, colonisation, agricultural intensification, or endogenous administrative development — and whose succession dynamics are governed by the CTMC estimated in this paper.

The transition from Regime I to Regime II is, in Graeber-Wengrow terms, *getting stuck*: the loss of arrangement freedom (R) that prevents institutional reorganisation back toward consensus forms. This transition is one-directional in the empirical record. No polity in the transition dataset moved from appointment or hereditary to consensus without dissolution and independent reconstitution — and the reconstituted forms (post-collapse hunter-gatherer bands, Zomia-style highland dispersal communities) are typically not considered the *same* political entity as the one that preceded them.

This has an important implication for policy and theory. Reforming high-L states toward greater EDR is not the same problem as maintaining EDR under rising L. The former requires intervention in Regime II dynamics — electing reform governments, building appointment systems with strong constraint provisions, maintaining the institutional memory of disobedience. The latter requires not entering Regime II in the first place, or finding the conditions under which Regime II systems can maintain proximity to the Regime I boundary. The Swiss and Norse cases suggest those conditions include: early constitutional constraint on sovereign authority (preventing S from rising freely with A), strong civil society and trade union traditions (maintaining D₀), and federalist structures that preserve R at subnational levels. None of these is sufficient alone; their interaction is what the framework suggests matters.

---

## 8. Conclusion

This paper has tested the succession mechanism predictions of the isonomia lock-in sequence through three phases of empirical analysis. The primary findings are:

**Phase 1 (static model, n = 117).** Surplus legibility and pre-existing disobedience freedom together strongly predict succession mechanism type at any cross-section. χ² = 25.08 (p < 0.0001). Among high-L systems, D₀ discriminates elective from hereditary succession with large effect size (OR = 6.46, rank-biserial r = −0.782, p = 0.0001). The multinomial logistic model correctly classifies 60% of systems across five types from L and D₀ alone.

**Phase 2 (transition matrix, n = 43 type-changing transitions).** L predicts appointment as a transition destination (OR = 2.24, permutation p = 0.005). Elite reform events produce 0 hereditary outcomes (11/11 non-hereditary). Internal succession crises produce 56% hereditary outcomes. The transition matrix has no documented cases of movement from appointment or hereditary to consensus — the pathway is empirically closed.

**Phase 3 (CTMC, 149 spells, 39 events, 110,589 system-years).** The L-conditional stationary distribution shifts from appointment-minority (π = 0.135) at low L to appointment-dominant (π = 0.595) at high L. Elective succession falls from π = 0.394 to π = 0.115. The D₀ moderator is confirmed: high-D₀ elective systems exit elective succession at 0.546 per 1000 years versus 2.744 per 1000 years for low-D₀ systems (ratio 5.03×; Cox PH joint test p = 0.026). Consensus is a founding state, not an equilibrium state: the one-way valve from consensus to other types has no historical reverse.

Together these findings support the lock-in sequence's central prediction while refining its character: the primary terminus of the lock-in sequence is bureaucratic appointment, not hereditary succession per se. The state that fully realises the lock-in trajectory is not the hereditary monarchy but the administered bureaucratic state — one in which the absence of freedom is managed rather than simply coerced, where D₀ is maintained at precisely low enough levels that disobedience cannot organise, and where R is formally abolished through administrative completeness. The living examples of governance systems that resist this trajectory — Norway, Switzerland, the Iroquois Confederacy before colonial incorporation — share precisely the D₀ properties that the model predicts as the counter-case: high pre-existing disobedience freedom that makes the transition to administered authority costly.

Paper 4 examines the network dynamics of governance differentiation — the schismogenesis process by which adjacent societies develop radically different succession trajectories through mutual contrast-coding — and tests whether the citation network structure predicts the direction of succession mechanism divergence across paired systems.

---

## Figure Captions

**Figure 3. Succession event validation: 57 transitions across 44 governance systems.** Generated by `src/succession_events.py` from `data/governance_extended.csv`. **Panel A:** Cause of transition × direction, heatmap with row-normalised percentages (n = 57 events). Cell colour intensity reflects the proportion of transitions of each cause type that moved in each direction; bold text indicates ≥30%. External shock → appointment (60%) versus elite reform → appointment (6%, → freedom 31%); Fisher exact p = 0.002. **Panel B:** Succession type transition matrix. Cell counts; cell colour reflects origin type. Diagonal cells (self-transitions, excluded from matrix analysis) shown as dashes. Colour strips on margins identify row/column types. The empty return path from appointment or hereditary to consensus is annotated. The dominated hereditary → appointment cell (n = 13) reflects the appointment attractor. **Panel C:** D (disobedience freedom) at the time of transition, by direction. Dot = mean; bar = ±1 SD; jittered individual points shown. The Athens −403 Thrasybulus restoration (D = 0.85, toward freedom via elite reform) is annotated. Mann-Whitney test of recovery versus non-recovery D is non-significant in the bulk (ns, noted); D₀ moderation holds specifically for elite reform recoveries.

**Figure 4. Recovery depth analysis: two mechanisms for toward-freedom succession transitions.** Generated by `src/recovery_depth.py` from `data/succession_events.csv`. **Panel A:** Sovereign capacity (S) versus D attained at recovery, for elite reform transitions only (n = 5). Regression line: r(S, D) = −0.984, p = 0.002. Green shaded region = full recovery zone (D ≥ θ = 0.45). Point size proportional to D₀ × (1−S). Athens −403 BCE (largest point, D = 0.85, S = 0.15) and Dutch Republic 1581 CE (D = 0.60, S = 0.30) fall in the full recovery zone; Greek oligarchic reforms (D = 0.35, S = 0.50) and Magna Carta 1215 CE (D = 0.15, S = 0.75) fall below theta. **Panel B:** All eight toward-freedom transitions by cause type (elite reform, reconsolidation, collapse), with D₀ × (1−S) as point size. Collapse recoveries (red points) show that D₀ is not causally required: the Egyptian Old Kingdom recovered from D₀ = 0.10 through administrative dissolution; the Kurultai recovered from D₀ = 0.60 through a power contest that was subsequently consolidated. Greek Oligarchy events (−508 and −403 BCE) merged as a single point (×2) as both share identical D = 0.35, S = 0.50 coordinates.

---

## References

Bohannan, P. (1958). *The Tiv of Central Nigeria*. London: International African Institute.

Brook, T. (1998). *The Confusions of Pleasure: Commerce and Culture in Ming China*. University of California Press.

Coedes, G. (1968). *The Indianized States of Southeast Asia*. University of Hawaii Press.

Cowgill, G. L. (2015). Ancient Teotihuacan: Early Urbanism in Central Mexico. Cambridge University Press.

Dollinger, P. (1970). *The German Hansa*. Stanford University Press.

Elkins, Z., Ginsburg, T., and Melton, J. (2025). *Comparative Constitutions Project: Constitute*, v5. https://comparativeconstitutionsproject.org

Freedom House (2021). *Freedom in the World 2013–2021*. Washington, DC: Freedom House.

Fukuyama, F. (2011). *The Origins of Political Order*. New York: Farrar, Straus and Giroux.

Graeber, D. and Wengrow, D. (2021). *The Dawn of Everything: A New History of Humanity*. London: Allen Lane.

Ingrao, C. (1994). *The Habsburg Monarchy 1618–1815*. Cambridge University Press.

Israel, J. (1995). *The Dutch Republic: Its Rise, Greatness, and Fall 1477–1806*. Oxford: Clarendon Press.

Legesse, A. (1973). *Gada: Three Approaches to the Study of African Society*. New York: Free Press.

Lewis, M. E. (2007). *The Early Chinese Empires: Qin and Han*. Cambridge, MA: Harvard University Press.

Mann, M. (1986). *The Sources of Social Power, Volume I*. Cambridge University Press.

Marchal, G. P. (2006). *Schweizer Gebrauchsgeschichte*. Basel: Schwabe.

Markoe, G. E. (2000). *Phoenicians*. London: British Museum Press.

Marshall, M. G. and Gurr, T. R. (2020). *Polity5: Political Regime Characteristics and Transitions, 1800–2018*. Center for Systemic Peace.

Motesharrei, S., Rivas, J., and Kalnay, E. (2014). Human and nature dynamics (HANDY). *Ecological Economics* 101: 90–102.

Postgate, J. N. (1992). *Early Mesopotamia: Society and Economy at the Dawn of History*. London: Routledge.

Rowe, J. H. (1946). Inca culture at the time of the Spanish Conquest. In: *Handbook of South American Indians*, Vol. 2. Washington: Smithsonian Institution.

Schleifer, P. (2026a). Isonomia I: A Phase-Space Framework for Governance Emergence, Resilience, and Dissolution. Working paper, isonomia series. https://github.com/its-not-rocket-science/isonomia

Schleifer, P. (2026b). Isonomia II: The Lock-In Sequence. Working paper, isonomia series. https://github.com/its-not-rocket-science/isonomia

Scott, J. C. (2009). *The Art of Not Being Governed: An Anarchist History of Upland Southeast Asia*. New Haven: Yale University Press.

Tadmor, H. (1994). *The Inscriptions of Tiglath-Pileser III, King of Assyria*. Jerusalem: Israel Academy of Sciences.

Tainter, J. (1988). *The Collapse of Complex Societies*. Cambridge University Press.

Thapar, R. (1997). *Aśoka and the Decline of the Mauryas*. Oxford University Press.

Townsend, R. F. (1992). *The Aztecs*. London: Thames and Hudson.

Turchin, P. (2003). *Historical Dynamics*. Princeton University Press.

Turchin, P. (2016). *Ages of Discord*. Chaplin, CT: Beresta Books.

Turchin, P. et al. (2015). Seshat: The Global History Databank. *Cliodynamics* 6(1): 77–107.

World Justice Project (2025). *WJP Rule of Law Index: Historical Data 2012–2025*. https://worldjusticeproject.org
