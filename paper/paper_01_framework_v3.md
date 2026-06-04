# Isonomia I: A Phase-Space Framework for Governance Emergence, Resilience, and Dissolution

**Working paper — isonomia series, Paper 1**

*Corresponding author: [Author]*
*Independent researcher*
*Repository: https://github.com/its-not-rocket-science/isonomia*
*Dataset: https://github.com/its-not-rocket-science/global-governance-models*

**Data availability:** The full dataset (`governance_extended.csv`, n = 389), coding scheme, analysis scripts, and all figures are publicly available at https://github.com/its-not-rocket-science/isonomia under MIT licence. Data will additionally be deposited in the JWSR Dataverse upon acceptance.

---

> **Abstract**
>
> The study of governance in deep history is divided between two literatures that address opposite ends of the same causal loop: emergence models ask why hierarchy arises from egalitarian baselines, while collapse models ask why it fails. We propose a unified phase-space framework bridging governance emergence and collapse. Drawing on Graeber and Wengrow's (2021) three elementary forms of domination — sovereignty (S), administration (A), and competitive politics (P) — we construct a continuous SAP phase space in which each governance system occupies a position rather than a categorical type. Against this we operationalise the three freedoms Graeber and Wengrow identify as historically fundamental — exit (E), disobedience (D), and arrangement (R) — as a composite resilience indicator (EDR). We propose that societies above a threshold θ in the EDR composite retain self-correcting capacity, while those below θ enter a fragile regime in which Turchin and Tainter collapse dynamics operate. Analysis of 389 governance systems spanning 12,000 years finds: EDR-SAP correlation r = −0.844 (hand-coded n = 125); a bimodal EDR distribution with trough at θ ≈ 0.45; no secular decline in high-EDR societies across the full timeline; and a citation network of 760 edges showing contrast-cited systems have significantly larger EDR divergence than general comparators (Mann-Whitney U, p = 0.0004), with EDR similarity propagating three network hops before reversing sign. These findings are consistent with governance forms being contingent configurations subject to internal lock-in dynamics and inter-civilisational schismogenesis rather than stadial inevitabilities. Cross-validation of the EDR composite against five independent external datasets confirms external construct validity. Against V-Dem v16 (Coppedge et al. 2026, n = 16 matched systems), EDR correlates with the liberal democracy index at r = 0.868, the egalitarian democracy index at r = 0.899, and the deliberative democracy index at r = 0.912 (all p < 0.001); individual components validate against purpose-matched V-Dem sub-indices (E vs movement r = 0.893, R vs civil society r = 0.776, D vs judicial compliance r = 0.650). Against Polity5 (Marshall and Gurr 2020, n = 11), EDR correlates with DEMOC at r = 0.847 and SAP with AUTOC at r = 0.895 (both p < 0.001). Against the WJP Rule of Law Index 2025 (World Justice Project 2025, n = 7 direct matches), E correlates with the expression and privacy sub-factor at r = 0.904 and R with assembly and civic participation at r = 0.861. Against Freedom House Freedom in the World 2013–2021 (Freedom House 2021, n = 9 direct matches), EDR correlates with the Civil Liberties aggregate at r = 0.923 (E vs expression r = 0.895, R vs associational rights r = 0.943, D vs rule of law r = 0.866). Against the CCP Comparative Constitutions Project v5 (Elkins et al. 2025, n = 11 with constitutional data), D correlates with constitutional constraint provisions at r = 0.681; the non-results for E and R reflect the de jure/de facto gap in constitutional text coding rather than measurement failure. Pre-modern validation against Seshat Equinox-2020 (Turchin et al. 2015, n = 14 systems, 3000 BCE–1600 CE) yields r = 0.604–0.774 for SAP-side variables. This is Paper 1 of a series; Papers 2–4 address the lock-in sequence, schismogenesis dynamics, and extended cross-validation.

---

## 1. Introduction

The scholarly study of how societies govern themselves across deep history has generated two rich but largely disconnected literatures. The first, which we term the *collapse tradition*, takes complex hierarchical societies as its starting point and asks under what conditions they fail. Tainter's (1988) account of declining marginal returns on administrative complexity, Turchin's (2003, 2016) secular cycle model of elite overproduction and popular immiseration, and the HANDY computational framework (Motesharrei et al. 2014) all share this orientation: hierarchy is the baseline, and collapse is the anomaly requiring explanation.

The second, which we term the *emergence tradition*, takes the long sweep of human prehistory as its starting point and asks a prior question: given that human beings spent most of their evolutionary and cultural history in relatively flexible, non-hierarchical arrangements, how and why do rigid, permanently hierarchical societies arise at all? Mann's (1986) account of the sources of social power, Fukuyama's (2011) political order theory, and most recently Graeber and Wengrow's (2021) systematic anthropological challenge to stadial models all work within this orientation.

These two traditions are not in conflict. They address opposite ends of the same causal loop. A complete account of governance in human history requires both: a model of how hierarchy emerges, a model of how it sustains itself, and a model of how it dissolves. What is missing is the unified framework that connects them.

This paper proposes such a framework. We draw primarily on Graeber and Wengrow's *The Dawn of Everything* (2021), which provides the most systematic recent challenge to the evolutionary staging models implicit in most comparative work, and which identifies both the mechanisms by which hierarchy arises and the freedoms whose suppression is its precondition. We construct a continuous phase space from their three elementary forms of domination, operationalise their three freedoms as a composite resilience indicator, and show that this indicator bridges the emergence and collapse literatures through a single threshold mechanism.

The framework has a second theoretical motivation beyond disciplinary integration. Both the collapse and emergence traditions tend to treat governance forms as products of structural conditions — ecological, demographic, economic. Graeber and Wengrow's contribution is to insist that human beings have historically understood their governance arrangements as choices, and have made those choices in explicit dialogue with the arrangements of their neighbours and predecessors. Schismogenesis — the dynamic by which societies define themselves in deliberate contrast to adjacent models — is not a peripheral ethnographic observation but a structural feature of how governance diversity is produced and maintained. A model that ignores this network dimension cannot explain why neighbouring societies with similar ecological and demographic conditions so frequently develop radically different governance forms, or why the most influential governance systems in the historical record are often not the largest or most powerful but the most explicitly counter-modelled.

The paper is structured as follows. Section 2 reviews the Graeber-Wengrow argument and its implications for model construction. Section 3 presents the SAP phase space. Section 4 introduces the EDR resilience composite and the central threshold hypothesis. Section 5 develops the lock-in sequence connecting surplus legibility to freedom suppression. Section 6 presents the schismogenesis network component. Section 7 integrates the framework with Turchin and Tainter collapse models. Section 8 describes the dataset and empirical analysis. Section 9 presents results. Section 10 discusses implications and limitations. Section 11 concludes and maps the subsequent paper series.

---

## 2. The Graeber-Wengrow Challenge

Graeber and Wengrow's *The Dawn of Everything* is, among other things, an extended argument against what they call the "myth of the primitive" — the assumption, shared across the political spectrum from Hobbes to Rousseau, that pre-state human societies were either brutish and violent or innocent and simple. The archaeological and ethnographic record, they argue, shows something far more interesting: that human beings have, throughout their history, been sophisticated political actors who understood the contingency of their governance arrangements and frequently changed them.

Four claims from this work are directly relevant to framework construction.

**Seasonality and deliberate oscillation.** Many documented societies alternated between radically different governance modes depending on season, ceremony, or circumstance — hierarchical and authoritarian during winter aggregation and ritual periods, egalitarian and dispersed during summer foraging. Graeber and Wengrow argue this is not instability or incipient state formation: it is deliberate institutional design. The implication for modelling is significant. Governance systems cannot be treated as fixed points on a typological scale; they must be understood as trajectories in a continuous space.

**Three elementary forms of domination.** Drawing on their comparative ethnographic and archaeological analysis, Graeber and Wengrow identify three independent sources from which hierarchical arrangements are constructed: sovereignty (the capacity for charismatic violence, the right to kill), administration (bureaucratic record-keeping, surveillance, and the management of populations), and what they call heroic or competitive politics (the pursuit of prestige, honour, and personal charisma through performance and display). Most existing comparative frameworks conflate these, treating them as aspects of a single "complexity" dimension. Graeber and Wengrow show that they are genuinely separable: the Inca Empire maintained extraordinary administrative sophistication (quipu accounting, road networks, census-based redistribution) with relatively constrained sovereignty and minimal competitive politics; the Balinese Negara described by Geertz (1980) was organised almost entirely around competitive political performance with minimal administrative apparatus; the Egyptian Old Kingdom concentrated sovereignty to near-absolute levels without the administrative bureaucracy that later characterised Chinese imperial governance.

**Three freedoms as political self-consciousness.** Against the three forms of domination, Graeber and Wengrow identify three freedoms that pre-state societies recognised, defended, and sometimes lost: the freedom to move away (exit the community), the freedom to disobey (refuse authority without fatal consequence), and the freedom to create new social arrangements (reorganise institutions). These are not romanticised primitives. They are documented political values. The Wendat confederacy criticised French absolutism with philosophical precision. The Crow people maintained explicit structural mechanisms to prevent any individual accumulating lasting authority. Zomia highland communities in Southeast Asia, as Scott (2009) documents in detail, organised their entire subsistence strategy around maintaining illegible surplus precisely to preserve their freedom from incorporation into lowland states.

**Getting stuck.** Graeber and Wengrow's most politically provocative claim is that the permanent, self-reproducing hierarchy characteristic of states was not an evolutionary inevitability but a historical accident — the convergence of specific technologies of control. Cereal agriculture bound populations to fixed plots. Grain-based surplus was uniquely legible — measurable, storable, and transportable — enabling systematic taxation. Literate administration enabled the recording of obligations across time, turning debt and tribute into persistent structural features rather than situational arrangements. Societies that acquired all three simultaneously tended, for the first time, to lose the ability to self-correct.

---

## 3. The SAP Phase Space

We operationalise Graeber and Wengrow's three elementary forms of domination as continuous indices scored 0–1, producing a three-dimensional phase space in which each governance system occupies a position rather than a categorical type.

**S — Sovereignty index**: The concentration and durability of coercive power in identifiable authority. At S ≈ 0, violence is distributed and situational, with no individual or institution holding a monopoly. At S ≈ 1, sovereign authority is near-absolute and refusal is fatal. Anchor cases: San Xaro Networks (S = 0.05), Egyptian Old Kingdom (S = 0.90).

**A — Administration index**: The extent and sophistication of record-keeping, surveillance, and bureaucratic apparatus deployed for the management of populations. At A ≈ 0, governance operates through oral tradition and memory alone. At A ≈ 1, a complete literate bureaucracy manages census, taxation, legal codes, and correspondence across the polity. Anchor cases: Highland New Guinea Big Man System (A = 0.05), Confucian Bureaucracy (A = 0.95).

**P — Competitive politics index**: The degree to which political authority is achieved and maintained through prestige competition, performance, and heroic display rather than ascription or administrative position. At P ≈ 0, authority is fixed by birth or sacred order with no competitive dimension. At P ≈ 1, governance is constituted by ritual performance and competitive display. Anchor cases: Egyptian Old Kingdom (P = 0.20), Balinese Negara (P = 0.95).

The SAP ternary is a phase space rather than a typology. The same numerical value can be produced by different combinations: high-SAP states differ in whether they achieve this through sovereignty-dominant, administration-dominant, or competitive-politics-dominant configurations. The framework captures this variability in a way that categorical types cannot.

Several structural observations follow from the phase space. High-A systems tend to channel P into institutionalised administrative competition (the Chinese examination system, the Roman cursus honorum), suppressing unmediated charismatic S. High-S systems tend to eliminate P as a threat to sovereign authority — competitors for charismatic power are executed, exiled, or absorbed. The most historically durable large states — Tang Dynasty China, Ottoman Empire, Roman Empire — occupy a band where all three are simultaneously elevated, forming what we term the full lock-in zone. Crucially, as Graeber and Wengrow demonstrate, this combination is historically contingent: many large-scale, complex societies maintained low S+A while sustaining high P (Northwest Coast Potlatch cultures) or low S+P while sustaining high A (Inca Empire) for extended periods.

The SAP ternary is illustrated in Figure 1. Nodes represent governance systems, coloured by EDR composite (Section 4). The gradient from green (high EDR) at the apex and centre to red (low EDR) at the S-A base confirms that high-EDR systems cluster toward competitive-politics-dominant configurations, while low-EDR systems cluster toward sovereignty-administration combinations.

---

## 4. The EDR Resilience Composite

### 4.1 The three freedoms as variables

We operationalise Graeber and Wengrow's three freedoms as continuous indices scored 0–1.

**E — Exit freedom**: Can members leave the governance system without catastrophic cost? At E ≈ 0, exit is physically prevented or legally capital — through debt bondage, serfdom, or the Tokugawa sankin-kōtai hostage system, in which daimyo were required to alternate residences and leave family members as guarantors of loyalty, making defection physiologically impossible for those with families. At E ≈ 1, exit is structurally built into the governance form — nomadic peoples, seasonal foragers, and deliberately mobile communities like Zomia's highland swidden farmers. Anchor cases: Tokugawa Shogunate (E = 0.05), Zomia Highland Communities (E = 0.95).

**D — Disobedience freedom**: Can authority be refused through legitimate or customary channels? At D ≈ 0, refusal is fatal — the Qin Legalist state deployed collective punishment at the household level, making individual disobedience structurally impossible. At D ≈ 1, disobedience is institutionally encoded — the Gadaa System of the Oromo people rotates authority through age-sets on a fixed eight-year cycle, making it structurally impossible for any individual to retain authority beyond their term regardless of personal preference. Anchor cases: Qin Legalism (D ≈ 0.0), Gadaa System (D = 0.85).

**R — Arrangement freedom**: Can members create new social institutions or reorganise existing ones? At R ≈ 0, social structure is fixed by sacred law or natural order — innovation is heresy. At R ≈ 1, governance arrangements are explicitly understood as contingent human choices, routinely revised and experimented with. The Maroon communities of Jamaica and Suriname, composed of escaped enslaved people who had experienced near-zero values of all three freedoms, exhibit maximum R by definition: they built their governance from scratch. Anchor cases: Late-period Tokugawa Shogunate (R = 0.05), Maroon Communities (R = 0.85).

### 4.2 The EDR composite and central hypothesis

The EDR composite is defined as the unweighted mean of the three freedom indices:

**EDR = (E + D + R) / 3**

We propose the following central hypothesis:

*H1: Societies where EDR exceeds a threshold θ retain self-correcting capacity through the three-freedom mechanism. Societies where EDR falls below θ enter a fragile regime in which Turchin and Tainter collapse dynamics become operative.*

The mechanism connecting EDR to resilience is as follows. High EDR provides distributed error-correction: bad leadership is abandoned through exit (E), bad decisions are refused through disobedience (D), and failing institutions are replaced through reorganisation (R). This is not merely a normative claim about freedom — it is a functional claim about information processing and feedback. A governance system with high EDR receives accurate signals about its own failures and has the structural capacity to respond. A system with low EDR has severed the feedback loops: members cannot leave, cannot refuse, and cannot reorganise. The system is blind to its own dysfunction until external perturbation forces a reset.

When EDR drops below θ, the system enters the fragile regime described by Turchin and Tainter. Elite extraction can overshoot the level that would previously have triggered resistance, because the resistance mechanism is broken. Elite overproduction compounds as the administrative apparatus grows to manage increasing extraction. Marginal returns on complexity decline as coerced inputs replace voluntary ones. The system becomes increasingly brittle until a sufficiently large perturbation — invasion, climate shock, epidemic, or elite civil war — triggers disintegration.

### 4.3 Empirical findings

Analysis of the full 389-system dataset (hand-coded n = 125, auto-coded n = 264) finds an EDR-SAP correlation of r = −0.775 (hand-coded subset: r = −0.844, p < 0.001). This is consistent with H1: high-domination configurations systematically suppress the three freedoms. The relationship holds across all major historical periods and geographic regions.

The EDR distribution is bimodal (Figure 3). Systems cluster in two distinct regimes — a high-EDR cluster (EDR > 0.55) and a low-EDR cluster (EDR < 0.35) — with a trough at θ ≈ 0.45. Forty-two percent of all systems in the dataset fall below this threshold. The bimodality is consistent with a genuine phase boundary rather than a smooth gradient: governance systems do not populate the threshold zone but are pushed above or below it by the dynamics described in Section 5.

The timeline analysis (Figure 4) reveals that the weighted trend in EDR across hand-coded systems declines from approximately 0.90 at 12,000 BCE to approximately 0.42 at 4,000 BCE — crossing the estimated threshold θ at the point of early state emergence in Mesopotamia. After this crossing, the trend stabilises near θ through the classical period, before bifurcating in the modern era as high-EDR democratic and federal systems emerge alongside persisting low-EDR autocratic ones. Crucially, high-EDR societies appear at every point in the timeline, including the medieval and modern periods. There is no secular decline in freedom: the stadial inevitability of hierarchy is not supported by the data.

Collapse mode analysis provides further support for H1. Among hand-coded systems, fragile systems (EDR < θ) collapse predominantly via conquest (n = 15), internal fragmentation (n = 5), and revolution (n = 5) — consistent with the prediction that low-EDR systems lack internal corrective capacity and must be reset by external force. Resilient systems (EDR ≥ θ) that ended did so predominantly via colonial disruption (n = 5) — external destruction rather than internal failure — or graceful transition (n = 6). The asymmetry is theoretically significant: resilient societies, when they ended, were destroyed from outside. Fragile societies collapsed from within.

---

## 5. The Lock-In Sequence: Surplus Legibility and Information Infrastructure

The mechanism by which EDR is suppressed operates through two intermediate variables that drive the SAP phase space toward the full lock-in zone.

**L — Surplus legibility**: Following Scott's (2017) analysis, we define surplus legibility as the degree to which a society's primary productive output is measurable, countable, and extractable by external agents. Foraging, swidden, and pastoral economies are inherently illegible (L ≈ 0.1–0.2): forest products, root crops, and mobile herds cannot be counted from a distance. Cereal grain agriculture is uniquely legible (L ≈ 0.6–0.8): grain is storable, measurable, and transportable in ways that make it straightforwardly taxable. The Inca case (L ≈ 0.90) demonstrates that legibility is not the same as literacy: the quipu knotted-cord accounting system achieved near-maximum surplus legibility without writing, through a sophisticated administrative apparatus that tracked every household's labour obligations across the entire empire.

**I — Information infrastructure**: The existence and administrative deployment of systems for recording obligations, debts, ownership, and persons across time. Oral tradition alone (I ≈ 0.1–0.2), token and tally systems (I ≈ 0.3–0.4), partial writing for trade and religion (I ≈ 0.5–0.6), full literate bureaucracy with census and legal codes (I ≈ 0.7–0.85), and digital administrative systems (I ≈ 0.90–0.95). I is distinct from cultural literacy: it measures the administrative deployment of information systems for population management.

The lock-in sequence proceeds as follows:

1. Rising L (through agricultural intensification and territorial fixation) enables surplus extraction.
2. Rising L drives rising A: the administrative apparatus required to manage extraction creates demand for information infrastructure.
3. Rising A suppresses E: administrative systems require stable, trackable populations; exit is increasingly legally prevented or economically catastrophic as land tenure, debt, and conscription obligations bind people to place.
4. With E suppressed, D weakens: the threat of exit was the primary structural leverage through which communities refused authority. Once exit is closed off, disobedience becomes individually costly without collective enforcement.
5. With E and D suppressed, R is eliminated: social arrangements previously understood as human choices are redefined as natural or sacred necessities, foreclosing institutional experimentation.
6. EDR drops below θ: the system enters the fragile regime.

The Early Uruk / Late Uruk transition (c. 4000–2700 BCE) is the best-documented instance of this sequence. Early Uruk (EDR ≈ 0.48, L = 0.70, I = 0.55) shows the first large city (~40,000 inhabitants), temple-based redistribution, and proto-cuneiform accounting — high L and rising I — but no evidence of palace, hereditary kingship, or royal burials. Late Uruk and Early Dynastic (EDR ≈ 0.28, L = 0.85, I = 0.75) shows the palace emerging as distinct from the temple, hereditary royal burials at Ur, and military expansion. EDR drops 0.20 points across this transition, crossing the estimated θ threshold. The lock-in sequence is visible in the archaeological record.

Seventeen pre-lock-in candidates — systems with L ≥ 0.6 but EDR still above θ — are identified in the dataset. These include Early Uruk, Teotihuacan, Mohenjo-daro, the Venetian Republic, the Hanseatic League, and the Norwegian Sovereign Wealth Democracy. The theoretical interest of these cases is precisely that they possess high surplus legibility without having completed the lock-in sequence. The counter-cases — Norway (L = 0.75, EDR = 0.87), Swiss Consensus Democracy (L = 0.65, EDR = 0.85), British Parliamentary System (L = 0.75, EDR = 0.78) — all share a common feature: strong pre-existing institutional D (constitutional protections, federalism, merchant veto rights) established before L rose to its current level. This suggests that the lock-in sequence can be interrupted if D is institutionally robust before legibility increases — a finding with implications beyond the historical analysis that we leave for Paper 4 of this series.

---

## 6. Schismogenesis and the Network Structure of Governance

### 6.1 Schismogenesis as a governance dynamic

One of Graeber and Wengrow's most theoretically original contributions, and the one most absent from existing computational models, is their application of Bateson's (1935) concept of schismogenesis to governance formation. Bateson coined the term to describe the process by which two groups in contact develop increasingly differentiated identities precisely because of that contact — each group defining itself against the other's model. Graeber and Wengrow argue that this dynamic explains governance diversity in a way that ecological or demographic accounts cannot.

The Northwest Coast Potlatch societies did not accidentally develop their prestige-redistribution economics: they developed them in conscious opposition to hierarchical chiefdom models visible among neighbouring groups. Zomia highland communities maintained illegible surplus and high mobility not as a default pre-modern condition but as a deliberate strategy of state-avoidance — actively choosing governance forms that resisted incorporation into the lowland states they could observe. The Celtic tribal assemblies maintained non-urbanisation in the presence of Mediterranean urban models they knew directly.

This has a structural implication: governance forms are not only responses to internal conditions (ecology, surplus, population density) but also to the governance landscape in which societies are embedded.

### 6.2 Network construction

We construct a governance citation network from the Comparators and Comparative Insights columns of the source dataset, in which nodes are governance systems and edges encode the relationship between citing and cited system. Three edge types are distinguished: *comparator* (general citation of structural similarity), *parallel* (explicit identification of parallel governance forms in Comparative Insights), and *contrast* (explicit identification of contrasting forms). The resulting network contains 389 nodes and 760 edges (200 parallel, 111 contrast, 449 comparator), with a largest connected component of 348 nodes (89%).

### 6.3 Empirical findings

**Degree centrality.** The ten most-cited systems by degree centrality are the Iroquois Confederacy / Haudenosaunee (centrality = 0.103, EDR = 0.77), Phoenician Merchant Oligarchies (0.067, EDR = 0.57), Swiss Cantonal Democracy (0.067, EDR = 0.78), Holy Roman Empire (0.067, EDR = 0.47), and Venetian Republic (0.054, EDR = 0.55). The pattern is theoretically significant: the most-cited governance forms are predominantly mid-to-high EDR systems that served as explicit reference points — both models to emulate and counter-models to differentiate against — across multiple historical periods and geographies.

**Schismogenesis signal.** Contrast-cited pairs show significantly larger EDR divergence than general comparators (Mann-Whitney U, p = 0.0004, rank-biserial r = −0.204). Of 111 contrast edges, 48 (43%) involve pairs with ΔEDR > 0.25 or ΔSAP > 0.25, constituting strong schismogenesis candidates. The consistent pattern across these pairs is that ΔEDR exceeds ΔSAP: schismogenesis operates preferentially on the freedom dimensions rather than the domination dimensions. Societies that contrast themselves against each other differ primarily in how much freedom they provide their members, not in the structural form of their domination apparatus.

**Geographic null result.** Geographic proximity does not predict stronger schismogenesis: nearby contrast pairs (≤ 3,000 km, n = 57, mean ΔEDR = 0.247) do not show significantly larger EDR divergence than distant contrast pairs (> 3,000 km, n = 35, mean ΔEDR = 0.226; Mann-Whitney p = 0.25). This null result is itself theoretically informative. It implies that schismogenesis in the historical record operates at civilisational scale — societies differentiate against distant models they know about, not only immediate neighbours. The Celts maintained non-urbanisation in contrast to Mediterranean models they observed directly; contemporary blockchain governance advocates explicitly contrast their systems against both ancient despotisms and modern administrative states. Civilisational awareness, not physical proximity, is the relevant distance.

**Contagion decay.** EDR similarity between governance systems propagates through the citation network with a characteristic decay: Pearson r = 0.72 at degree-1 (95% CI: 0.60–0.81), r = 0.61 at degree-2 (0.45–0.76), r = 0.32 at degree-3 (0.11–0.54), and r = −0.34 at degree-4 (−0.51, −0.14; p = 0.0008). The sign reversal at degree-4 is statistically significant and theoretically interpretable: the citation network has a bipolar structure, with high-EDR and low-EDR clusters that are internally cohesive but externally contrasted. At four network hops, a system has crossed from one cluster into the other. This structural bipolarity is consistent with the bimodal EDR distribution observed in Section 4.3.

The contrast-edge subgraph shows a more compressed decay: r = 0.65 at degree-1 (p < 0.001, n = 41), dropping to r = −0.45 at degree-2 (ns, n = 19). Contrast-edge similarity is purely local: one hop away from a contrast relationship, the positive correlation inverts. This is consistent with the schismogenesis interpretation — societies differentiate against their immediate contrast partners, but the differentiation does not propagate further.

---

## 7. Integration with Collapse Models

### 7.1 The secular cycle reframed

Turchin's (2003, 2016) secular cycle model identifies roughly 200–300 year oscillations between integrative and disintegrative phases in complex societies, driven by elite overproduction and popular immiseration. The isonomia framework reframes these dynamics as follows.

The integrative phase corresponds to a SAP configuration in which EDR remains above θ. The self-correcting mechanism is operational: popular pressure constrains elite extraction, leadership failures can be resisted or abandoned, and institutional experimentation is possible. Elite competition is channelled through legitimate competitive-politics structures (P) rather than extraction.

The disintegrative phase begins when A has grown to the point where D is structurally suppressed. Once the disobedience mechanism is broken, elites can extract beyond the level that would previously have triggered popular resistance. Elite overproduction compounds as the administrative apparatus offers expanding opportunities for extraction without accountability. The system overshoots the sustainable extraction level, not because elites are uniquely greedy but because the feedback mechanism that previously regulated extraction has been disabled.

The isonomia framework predicts that societies entering the disintegrative phase will exhibit specific characteristics: high A, suppressed D, declining E (mobility increasingly restricted as administrative capture intensifies), and SAP composite above the full lock-in threshold. These are testable predictions against Turchin's own cliodynamics database — a cross-validation exercise planned for Paper 4 of this series.

### 7.2 Marginal returns on complexity reframed

Tainter's (1988) *declining marginal returns on complexity* is one of the most cited explanations for civilisational collapse. The isonomia framework offers a more precise specification: the complexity that yields diminishing returns is specifically administrative apparatus (A) once it has eliminated meaningful E and D. Forced inputs are always less efficient than voluntary ones — the information content of compelled behaviour is lower, the transaction costs of enforcement are higher, and the creative problem-solving capacity of participants is degraded. When the only available inputs to the governance system are coerced, the overhead of maintaining coercion consumes increasing shares of surplus until the system cannot sustain itself.

This reframing makes a prediction that Tainter's original formulation does not: systems that maintain E and D while building high A should not exhibit declining marginal returns, or should exhibit them much later and less severely. The counter-cases identified in Section 5 — Norway, Switzerland, the Hanseatic League — are consistent with this prediction: all three maintain high A alongside preserved E and D, and none has exhibited the collapse dynamics that the raw A level might predict.

### 7.3 Collapse as freedom restoration

The most significant implication of the isonomia framework concerns how collapse itself should be understood. Tainter and Turchin both treat collapse primarily as a failure — of complexity, of social coherence, of population. The framework presented here predicts something different: that collapse of a low-EDR system should *restore* the three freedoms.

When a high-SAP, low-EDR system disintegrates — through conquest, fragmentation, or internal revolution — the specific mechanisms of freedom suppression are disrupted. Land becomes available (restoring E). Surveillance apparatus breaks down (restoring D). New institutional arrangements become possible (restoring R). The EDR composite rises above θ, and the self-correcting mechanism is re-engaged.

This prediction is consistent with the archaeological record. The First Intermediate Period following the Egyptian Old Kingdom's collapse shows evidence of increased regional autonomy and nome governors' independence — a partial restoration of E and D. The period following Rome's fragmentation shows improved average nutrition and reduced working hours for ordinary populations in many regions. The "Dark Ages" following Bronze Age collapse in the eastern Mediterranean show, in multiple sites, evidence of local experimentation and reduced social stratification. These are not simply poverty: they are the predicted signature of an EDR reset.

---

## 8. Dataset and Methods

### 8.1 Dataset construction

The primary dataset (`governance_extended.csv`) was constructed by merging and extending the `global-governance-models` repository (Schleiferdyne Systems, 2026) with 67 theory-driven additions targeting cases critical to the framework's empirical grounding. The final dataset contains 389 governance systems spanning approximately 12,000 BCE to the present, drawing on archaeological, ethnographic, and historical sources across all inhabited regions.

Each system is scored on ten continuous variables (S, A, P, E, D, R, L, I, scale_population, scale_territory) and five categorical variables (seasonality, binding_mechanism, collapse_mode, Historical Epoch, Region). Scoring follows the explicit criteria documented in `data/coding_scheme.md`, which specifies anchor cases and inter-rater reliability targets for each variable.

### 8.2 Coding confidence

Three confidence levels are assigned:

- **Confidence 3**: Direct archaeological or textual evidence for the specific variables coded. Examples: Egyptian Old Kingdom (royal annals, pyramid records, archaeological survey), Tokugawa Shogunate (Bakufu administrative records, sankin-kōtai documentation), Confucian Bureaucracy (examination records, census registers).
- **Confidence 2**: Reasonable inference from known structural features of the system. Examples: Gadaa System (ethnographic documentation of age-set rotation), Iroquois Confederacy (recorded Great Law of Peace, clan mothers' documented veto authority).
- **Confidence 1**: Auto-coded from governance type and characteristics using a heuristic model; requires human review.

Of 389 systems, 125 are hand-coded at confidence 2 or 3. All quantitative findings reported in this paper use the hand-coded subset unless otherwise noted. Auto-coded systems are included in visualisations where noted.

### 8.3 Network construction

The governance citation network was constructed from the Comparators and Comparative Insights columns of the source dataset, using a canonical name resolution algorithm to consolidate name variants and deduplicate entries (see `src/schismogenesis.py` for full implementation). The resulting network contains 389 nodes and 760 edges. Edge types (comparator, parallel, contrast) were derived from the syntactic structure of Comparative Insights entries (keywords "Parallels:" and "Contrasts:") supplemented by the Comparators column.

### 8.4 Statistical methods

EDR-SAP correlation: Pearson r on hand-coded subset. Network neighbourhood correlations: Pearson r with bootstrap confidence intervals (2,000 resamples). Schismogenesis significance: Mann-Whitney U (non-parametric, appropriate for these distributions), one-tailed. Geographic analysis: Spearman rank correlation of distance vs. ΔEDR; Mann-Whitney U for near/distant comparison. Contagion decay confidence intervals: bootstrap (2,000 resamples). All analyses conducted in Python using NumPy, SciPy, and NetworkX.

### 8.5 Reproducibility

All data, code, and figures are publicly available at https://github.com/its-not-rocket-science/isonomia under MIT licence. The repository contains five analysis scripts: `phase_space.py` (SAP ternary and EDR visualisations), `edr_resilience.py` (resilience threshold analysis and collapse mode breakdown), `schismogenesis.py` (network construction, schismogenesis analysis, and statistical tests), `geo_contagion_analysis.py` (geographic schismogenesis and contagion decay), and `crossvalidate_edr.py` (cross-validation against V-Dem v16, Polity5, WJP, Freedom House FIW, CCP, and Seshat). The validation script accepts five optional external datasets via command-line flags: `--vdem` (V-Dem v16, available at https://www.v-dem.net), `--polity` (Polity5, available at https://www.systemicpeace.org/inscrdata.html), `--seshat` (Seshat Equinox-2020, available at https://seshat-db.com/downloads_page/), `--wjp` (WJP Historical Data, available at https://worldjusticeproject.org/rule-of-law-index/), `--fiw` (Freedom in the World, available at https://freedomhouse.org/report/freedom-world), and `--ccp` (CCP v5, available at https://comparativeconstitutionsproject.org/download-data/). None of these external datasets is redistributed in the repository. All figures in this paper can be regenerated from the dataset by running these scripts in order. The coding scheme (`data/coding_scheme.md`) documents the operationalisation criteria for all variables, including the inter-rater reliability exercise results, the clarifications to the P and A variable definitions, and the complete external validity tables for all five cross-validation datasets.

---

## 9. Results

### 9.1 SAP phase space

The SAP ternary (Figure 1) shows that 389 governance systems, when positioned in the phase space defined by their sovereignty, administration, and competitive politics indices, exhibit a clear colour gradient from green (high EDR) at the P apex and centre to red (low EDR) at the S-A base. This gradient would not be expected if SAP and EDR were independent: it reflects the systematic suppression of freedoms by domination configurations, consistent with H1.

The distribution of systems within the ternary is non-uniform. The S-A base (low competitive politics) is densely populated with low-EDR systems. The P apex region is sparsely populated but predominantly high-EDR. The centre of the ternary — balanced S+A+P — contains the widest range of EDR values, reflecting the theoretical prediction that the full lock-in zone requires high values across all three domination dimensions simultaneously.

### 9.2 EDR distribution

The EDR distribution across 389 systems (Figure 3) is bimodal, with a trough at approximately 0.45. The hand-coded subset (n = 125) shows the same structure. The trough aligns precisely with the proposed threshold θ = 0.45, consistent with the interpretation that θ marks a genuine phase boundary: systems are pushed to one side or the other by the lock-in dynamics described in Section 5, and do not populate the threshold region in equilibrium.

Forty-two percent of all systems (165 of 389) fall below θ. Among hand-coded systems, 43% (54 of 125) fall below θ.

### 9.3 Timeline

The weighted trend analysis (Figure 4) shows EDR declining from approximately 0.90 at 12,000 BCE to approximately 0.42 at 4,000 BCE — a crossing of θ that coincides with the emergence of the first states in Mesopotamia. After this crossing, the weighted trend stabilises near θ through the classical and medieval periods, reflecting the simultaneous existence of high-EDR and low-EDR systems in the same periods. In the modern era (post-1500 CE), the right side of the timeline shows a bifurcation: a cluster of very high-EDR systems (Zomia, Swiss Consensus Democracy, Norwegian Sovereign Wealth Democracy, Iroquois Confederacy) alongside a dense cluster of very low-EDR systems (Tang Dynasty, Tokugawa Shogunate, Soviet Republics, Singaporean Technocracy). This bifurcation contradicts any monotonic narrative of either progress or decline.

### 9.4 Collapse mode asymmetry

Among hand-coded systems, the 54 systems below θ (fragile regime) show a collapse mode distribution dominated by conquest (n = 15, 28%), internal fragmentation (n = 5), and revolution (n = 5). The 71 systems above θ (resilient regime) that ended did so predominantly via colonial disruption (n = 5), graceful transition (n = 6), or fragmentation (n = 6). The asymmetry is consistent with H1: fragile systems collapse internally; resilient systems are destroyed externally.

### 9.5 Schismogenesis

Contrast edges show significantly larger EDR divergence than comparator edges (Mann-Whitney U, p = 0.0004; contrast mean ΔEDR = 0.239, comparator mean ΔEDR = 0.194). The effect size (rank-biserial r = −0.204) is small-medium, appropriate for a complex historical dataset with heterogeneous sources. The geographic analysis finds no significant relationship between distance and ΔEDR for any edge type (all Spearman ρ < 0.08, all p > 0.18), consistent with the interpretation that schismogenesis operates at civilisational scale.

### 9.6 Contagion decay

EDR similarity propagates through the citation network with significant decay across three hops: r = 0.72 (degree-1, 95% CI: 0.60–0.81), r = 0.61 (degree-2, 95% CI: 0.45–0.76), r = 0.32 (degree-3, 95% CI: 0.11–0.54). All three are statistically significant (all p < 0.01). At degree-4, the correlation reverses sign (r = −0.34, 95% CI: −0.51 to −0.14, p = 0.0008), indicating a bipolar network structure consistent with the bimodal EDR distribution: at four network hops, a system has traversed from one cluster to the other. The sign reversal is the strongest single piece of evidence for the framework's claim that the citation network has a genuine two-regime structure rather than a smooth gradient.

The contrast-only subgraph shows a more compressed decay, with positive correlation at degree-1 (r = 0.65, p < 0.001, n = 41) dropping to non-significant negative correlation at degree-2 (r = −0.45, ns, n = 19), confirming that schismogenesis-based differentiation is structurally local: one hop away from a contrast relationship, the positive EDR correlation inverts. This is consistent with the geographic null result in Section 9.5 — schismogenesis operates at civilisational scale but is network-local, not spatially diffuse.

### 9.7 Inter-rater reliability

A blind re-coding of 25 systems by the primary coder produced MAD = 0.072 on SAP composites and MAD = 0.089 on EDR composites, both meeting the pre-specified targets. All eight continuous dimensions individually met MAD < 0.15. Categorical agreement on collapse mode was 84%; binding mechanism and seasonality showed lower agreement due to multi-value structure and vocabulary inconsistency. Three dataset revisions followed the exercise (see Section 10.2).

---

## 10. Discussion

### 10.1 The stadial model and its failure

The most fundamental implication of these findings concerns the stadial evolutionary model of governance — the assumption, present across the spectrum from Hobbes to Fukuyama, that human societies develop from simple to complex, from egalitarian to hierarchical, in a sequence that is either inevitable or at least robustly predicted by ecological and demographic conditions.

The timeline result (Section 9.3) is inconsistent with this model. High-EDR societies appear at every point in the 12,000-year span of the dataset. The Natufian communities of the Levant at 12,500 BCE show high EDR; so do the Iroquois Confederacy of 1450 CE, the Swiss Cantonal Democracy of 1291, the Norse Thing system of 800–1300 CE, and the Norwegian Sovereign Wealth Democracy of the present. Hierarchy is not the terminus of a developmental sequence: it is one configuration among many that human societies have adopted, sustained, and abandoned throughout their history.

The SAP phase space result reinforces this. If stadial evolution were correct, the ternary should show systems clustered at the high-SAP, low-EDR corner as the evolutionary endpoint. Instead it shows systems distributed across the full space, with the high-EDR region populated by systems from every historical period and geographic location.

### 10.2 Measurement limitations

**Inter-rater reliability.** A blind re-coding of 25 systems spanning the full EDR and SAP range was conducted by the primary coder after completion of the initial dataset. All eight continuous dimensions met the pre-specified target of MAD < 0.15: SAP composite MAD = 0.072, EDR composite MAD = 0.089. Per-dimension results: S = 0.078, A = 0.096, P = 0.086, E = 0.086, D = 0.120, R = 0.132, L = 0.088, I = 0.129. Categorical agreement on collapse mode was 84%; binding mechanism and seasonality showed lower agreement due to multi-value structure and vocabulary inconsistency respectively, not conceptual disagreement. These variables do not contribute to the paper's main quantitative findings.

The exercise identified two systematic sources of interpretive ambiguity subsequently clarified in the coding scheme. First, P (competitive politics) was initially overcoded in absolute states (Qin Legalism, Assyrian Military Autocracy) by conflating the *performance of held power* with genuine *competition for authority*. The coding scheme now distinguishes these explicitly. Second, A (administration) was initially undercoded in systems with high institutional complexity but low record-keeping capacity (Gadaa System, Vedic assemblies), and undercoded in systems with sophisticated non-literate administration (Minoan Linear A, Egyptian nome system). The scheme now specifies that A measures the administrative deployment of information systems, not organisational sophistication per se.

Three substantive disagreements (dEDR ≥ 0.15) were resolved by revising the dataset: Gupta Golden Age EDR downward (caste system constraints on E and D underweighted in original), Ottoman Empire R upward (millet system constitutes genuine arrangement freedom), and Soviet Republics R marginally upward (samizdat culture acknowledged). Three further disagreements (Napoleon R, Cucuteni-Trypillia D, Gadaa D) were reviewed and the original conservative readings retained, with the disagreements documented as expected uncertainty at confidence level 2.

**Auto-coded systems.** The auto-coded systems (n = 264) are included in network analysis and full-dataset statistics, but their EDR values are heuristic approximations derived from governance type and characteristics. The auto-coding systematically regresses toward the mean, which partially explains the lower correlation in the full dataset (r = −0.779) versus the hand-coded subset (r = −0.844). All substantive claims in this paper are based on the hand-coded subset.

**Network coverage.** The citation network captures explicit comparisons made in secondary sources and does not capture the full range of historically significant governance relationships. Systems without rich secondary literature are underrepresented in the network analysis but not in the phase-space or resilience analyses.

**Threshold identification.** The threshold θ = 0.45 is identified empirically from the bimodal EDR distribution trough and has not been cross-validated against independent collapse event data. This cross-validation is a primary goal of Paper 4 in this series.

**External construct validity.** Cross-validation against five independent external datasets confirms that the EDR and SAP composites measure the constructs they claim to measure. All external datasets are distinct from each other in methodology, temporal scope, and measurement philosophy, and the convergent results across them substantially reduce the risk that the correlations reflect shared measurement artefact.

*V-Dem v16* (Coppedge et al. 2026): 16 isonomia systems with modern-state equivalents, matched by country and target year. EDR correlates with the liberal democracy index at r = 0.868 (p < 0.001), the egalitarian democracy index at r = 0.899 (p < 0.001), and the deliberative democracy index at r = 0.912 (p < 0.001). Individual component validation: E against V-Dem freedom of movement r = 0.893 (p < 0.001), R against civil society participation r = 0.776 (p < 0.001), D against judicial compliance r = 0.650 (p = 0.006). Two systems previously matched to temporally mismatched proxies — Roman Republic (matched to Italy 1870) and Qin Legalism (matched to China 1949) — were removed from the V-Dem set after identifying structural incompatibility; Dutch Republic was re-matched from Netherlands 1800 to Netherlands 1789, which falls within the Republic's lifespan. These corrections reduced n from 18 to 16 and marginally improved correlation strength by removing noise from the structural mismatches.

*Polity5* (Marshall and Gurr 2020): 11 matched systems. EDR vs DEMOC r = 0.847 (p = 0.001), SAP vs AUTOC r = 0.895 (p < 0.001), S vs AUTOC r = 0.870 (p = 0.001), D vs XCONST r = 0.747 (p = 0.008). P vs PARCOMP r = 0.491 (ns), consistent with the expectation that P captures prestige competition and non-electoral competitive politics more broadly than Polity's electoral-focused PARCOMP.

*WJP Rule of Law Index 2025* (World Justice Project 2025): 7 direct matches to modern systems, plus 7 pre-1980 proxy matches (flagged separately and excluded from correlations). The WJP's sub-factor structure allows more granular validation than composite indices: E against the expression and privacy composite (sub-factors 4.4 and 4.6) r = 0.904 (p = 0.005), R against assembly and civic participation (sub-factors 4.7 and 3.3) r = 0.861 (p = 0.013), D against the government constraints and due process composite (Factor 1, sub-factors 1.2, 1.5, and 4.3) r = 0.640 (ns at n = 7 — the reduced n limits power). The strong E and R results against WJP sub-factors, independent of V-Dem, substantially strengthen the convergent validity of those two dimensions.

*Freedom House Freedom in the World 2013–2021* (Freedom House 2021): 9 direct matches (systems with target year ≥ 1980), plus 7 proxy matches. FIW's sub-score structure provides validation across all three EDR components and, crucially, a first independent reading on P. E vs FIW-D Expression and Belief r = 0.895 (p = 0.001), R vs FIW-E Associational and Organisational Rights r = 0.943 (p < 0.001), D vs FIW-F Rule of Law r = 0.866 (p = 0.003), EDR vs FIW Civil Liberties aggregate r = 0.923 (p < 0.001). The P dimension against FIW-B Political Pluralism yields r = 0.357 (ns), consistent with Polity PARCOMP; both datasets have limited variation on P in the modern state set (iso_P ranges from 0.30 to 0.75 across direct matches), which suppresses the correlation through range restriction. The grey proxy points in the FIW figure, spanning the pre-1980 systems, show a visually consistent positive pattern across the full P range, suggesting the range restriction rather than the measurement is the binding constraint.

*CCP Comparative Constitutions Project v5* (Elkins et al. 2025): 14 matched systems with constitutional coverage (two further systems — Habsburg at 1900 and Joseon at 1895 — had year gaps exceeding ten years and were excluded). CCP codes de jure constitutional text rather than de facto implementation, creating a specific and theoretically anticipated divergence from isonomia's de facto coding. D against the constitutional constraint composite (judicial independence, due process, habeas corpus, fair trial, and executive constraint ordinality) r = 0.681 (p = 0.021, n = 11). E and R both return non-significant correlations (r = 0.230 and r = 0.084), which reflects the binary ceiling in constitutional provisions: almost every constitution in the matched set enshrines freedom of movement and assembly in its text, producing near-zero variance that suppresses correlation regardless of actual freedom. Seven of fourteen systems show de jure/de facto gaps exceeding 0.4 on at least one EDR dimension. The most theoretically significant cases: Soviet Republics System (ccp_E = 0.75, iso_E = 0.05; ccp_R = 1.00, iso_R = 0.08 — the 1977 Soviet constitution enshrined rights it systematically denied), Meiji Oligarchy (ccp_E = 0.75, iso_E = 0.20; ccp_R = 1.00, iso_R = 0.20 — the 1889 Meiji constitution included rights provisions operating under sweeping lèse-majesté and public peace laws), and British Parliamentary System (ccp_E = 0.25, iso_E = 0.80 — the UK has no written constitution and common-law freedoms do not appear in CCP's text coding). These divergence cases directly illustrate the passive-revolution mechanism described in Paper 2: constitutional rights provisions that preserve the form of freedom while suppressing its substance. The CCP non-results for E and R are therefore not failures of validation but confirmations of the distinction between de jure and de facto freedom that the isonomia framework requires.

*Seshat Equinox-2020* (Turchin et al. 2015): 14 pre-modern systems, 3000 BCE–1600 CE. A vs Seshat admin composite r = 0.604 (p = 0.022), I vs writing composite r = 0.672 (p = 0.008), S vs military composite r = 0.774 (p = 0.003), SAP composite vs admin composite r = 0.710 (p = 0.004). D vs Seshat legal composite r = 0.066 (ns), consistent with the observation that Seshat was built to measure social complexity rather than the Graeber-Wengrow freedoms: no Seshat variable captures exit, disobedience, or arrangement freedom directly. The Inca Empire represents a notable case in the I validation: iso_I = 0.70 (quipu-based information infrastructure) against Seshat writing composite = 0.00, because Seshat's writing composite scores the absence of script. This divergence is not a measurement error; it illustrates that the isonomia I variable measures state administrative capacity to track resources and populations, while Seshat's writing composite measures script presence. The Inca figure is annotated in the crossval_seshat figure accordingly.

### 10.3 Theoretical extensions

Several theoretical questions raised by this framework require dedicated treatment in subsequent papers.

The lock-in sequence (Section 5) is the most empirically tractable component and the most directly relevant to contemporary governance. The counter-cases — systems with high L that have not suppressed EDR — require close analysis to identify the conditions under which the sequence is interrupted. This is the subject of Paper 2.

The schismogenesis network model (Section 6) is the most theoretically novel component. The current analysis establishes the signal (contrast edges show larger ΔEDR, p = 0.0004) and the geographic null, but does not model the dynamics by which schismogenesis propagates through the network or how the degree-4 sign reversal is maintained. A dedicated agent-based model of schismogenesis dynamics is the subject of Paper 4.

The irreversibility question — under what conditions can a society below θ return above it through endogenous reform — is addressed empirically only in passing in the current paper. It is theoretically significant because it distinguishes between collapse-and-reset (the Turchin and Tainter prediction) and reform-in-place (the democratic transition literature). Paper 4 addresses this through cross-validation with the Polity IV and V-Dem datasets.

---

## 11. Conclusion

We have proposed a unified phase-space framework for the emergence, resilience, and dissolution of governance systems, grounded in Graeber and Wengrow's (2021) anthropological revision of civilisational history. The framework positions each governance system in a continuous SAP (sovereignty-administration-competitive politics) space, defines a composite EDR (exit-disobedience-arrangement) resilience indicator, and proposes that the threshold between resilient and fragile regimes is marked by θ ≈ 0.45 in the EDR composite.

Empirical analysis of 389 governance systems spanning 12,000 years finds results consistent with the framework's central predictions: a strong negative EDR-SAP correlation (r = −0.844, hand-coded subset), a bimodal EDR distribution with a trough at θ, no secular decline in high-EDR societies across the full timeline, asymmetric collapse modes by EDR regime, and a statistically significant schismogenesis signal in the citation network (contrast ΔEDR > comparator ΔEDR, p = 0.0004). Cross-validation across five independent external datasets — V-Dem v16, Polity5, WJP Rule of Law Index, Freedom House FIW, and CCP Comparative Constitutions Project — yields consistent convergent validity for the EDR and SAP composites and their components, with EDR correlations ranging from r = 0.847 to r = 0.923 against three composite democracy indices. Pre-modern validation against Seshat Equinox-2020 confirms the SAP dimensions against independent social complexity measures.

The framework's primary contribution is not the identification of specific empirical regularities but the integration of two previously disconnected literatures through a single mechanism: the three-freedom error-correction system that high-EDR societies maintain and low-EDR societies progressively dismantle. This integration generates predictions that neither the emergence tradition nor the collapse tradition produces independently — in particular, the prediction that collapse restores freedom, that schismogenesis is civilisational in scale rather than geographic, and that the L→I→A→EDR suppression sequence can be interrupted by pre-existing institutional D.

The framework also has implications for how we read the present. Several of the high-L, high-EDR counter-cases identified in Section 5 — Norway, the Swiss Consensus Democracy, the Hanseatic League — suggest that the lock-in sequence is not mechanically inevitable. They share a common feature: strong pre-existing institutional D established before legibility increased to its current level. If that pattern holds under further analysis (the subject of Paper 2), it implies that the sequence can be interrupted — that societies can accumulate administrative capacity and surplus legibility without sacrificing the three freedoms, if those freedoms are institutionally robust beforehand. That finding, if confirmed, has direct relevance to contemporary debates about digital surveillance, platform-mediated economic legibility, and the governance of AI systems as novel administrative infrastructures.

These predictions are falsifiable, and the dataset and code to test them are publicly available.

---

## References

Bateson, Gregory. 1935. "Culture Contact and Schismogenesis." *Man* 35:178–183.

Coppedge, Michael, John Gerring, Carl Henrik Knutsen, et al. 2026. *V-Dem Codebook v16*. Varieties of Democracy Project. https://www.v-dem.net/data/the-v-dem-dataset/

Elkins, Zachary, Tom Ginsburg, and James Melton. 2025. *Comparative Constitutions Project: Constitute*, v5. https://comparativeconstitutionsproject.org/download-data/

Freedom House. 2021. *Freedom in the World 2013–2021*. Washington, DC: Freedom House. https://freedomhouse.org/report/freedom-world

Fukuyama, Francis. 2011. *The Origins of Political Order*. New York: Farrar, Straus and Giroux.

Geertz, Clifford. 1980. *Negara: The Theatre State in Nineteenth-Century Bali*. Princeton, NJ: Princeton University Press.

Graeber, David and David Wengrow. 2021. *The Dawn of Everything: A New History of Humanity*. London: Allen Lane.

Mann, Michael. 1986. *The Sources of Social Power, Vol. 1: A History of Power from the Beginning to AD 1760*. Cambridge: Cambridge University Press.

Motesharrei, Safa, Jorge Rivas, and Eugenia Kalnay. 2014. "Human and Nature Dynamics (HANDY): Modeling Inequality and Use of Resources in the Collapse or Sustainability of Societies." *Ecological Economics* 101:90–102.

Scott, James C. 2009. *The Art of Not Being Governed: An Anarchist History of Upland Southeast Asia*. New Haven, CT: Yale University Press.

Scott, James C. 2017. *Against the Grain: A Deep History of the Earliest States*. New Haven, CT: Yale University Press.

Tainter, Joseph. 1988. *The Collapse of Complex Societies*. Cambridge: Cambridge University Press.

Turchin, Peter. 2003. *Historical Dynamics: Why States Rise and Fall*. Princeton, NJ: Princeton University Press.

Turchin, Peter. 2016. *Ages of Discord: A Structural-Demographic Analysis of American History*. Chaplin, CT: Beresta Books.

Coppedge, Michael, John Gerring, Carl Henrik Knutsen, et al. 2026. *V-Dem Codebook v16*. Varieties of Democracy Project. https://www.v-dem.net/data/the-v-dem-dataset/

Marshall, Monty G. and Ted Robert Gurr. 2020. *Polity5: Political Regime Characteristics and Transitions, 1800–2018*. Center for Systemic Peace. https://www.systemicpeace.org/inscrdata.html

Turchin, Peter, Rob Brennan, Thomas E. Currie, Kevin Feeney, et al. 2015. "Seshat: The Global History Databank." *Cliodynamics* 6(1): 77–107. https://seshat-db.com/downloads_page/

World Justice Project. 2025. *WJP Rule of Law Index: Historical Data 2012–2025*. Washington, DC: World Justice Project. https://worldjusticeproject.org/rule-of-law-index/

---

## Figure Captions

**Figure 1. SAP Phase Space.** Each of 389 governance systems positioned in the continuous three-dimensional space defined by sovereignty (S), administration (A), and competitive politics (P) indices, visualised as a ternary plot. Node colour encodes EDR composite (red = low, green = high). Large nodes are hand-coded (confidence ≥ 2); small nodes are auto-coded (confidence 1). The dashed line on the colourbar marks θ = 0.45.

**Figure 2. EDR vs. SAP Scatter.** EDR composite (y-axis) plotted against SAP composite (x-axis) for 389 systems, coloured by collapse mode. Dashed line: linear trend for hand-coded subset (r = −0.844). Shaded region: fragile regime (EDR < θ = 0.45). Large dots: hand-coded; small dots: auto-coded.

**Figure 3. EDR Distribution.** Histogram of EDR composite values across all 389 systems (light blue) and hand-coded subset (dark blue). Dashed red line: resilience threshold θ = 0.45. Dotted blue line: overall mean (0.47). Shaded region: fragile regime.

**Figure 4. EDR Timeline.** EDR composite plotted against start date for hand-coded systems, with Gaussian-weighted trend line. Shaded region: fragile regime. Epoch shading (grey italic): Pre-state, Early states, Medieval, Early modern–present.

**Figure 5. Governance Citation Network.** Spring-layout network of 125 hand-coded systems. Node colour: EDR composite (red–green). Node size: degree. Red edges: contrast (schismogenesis candidates). Blue edges: parallel (structural similarity). Grey edges: comparator (general citation).

**Figure 6. Contagion Decay.** Left panel: EDR correlation by network distance (full citation network), with 95% bootstrap CI ribbon. Degree-0 anchor: r = 1.0 (self-correlation). Sign reversal at degree-4 highlighted. Right panel: Decay by edge type (full network, contrast-only, parallel-only).

---

## Acknowledgements

The global-governance-models dataset that forms the upstream source for this analysis is maintained at https://github.com/its-not-rocket-science/global-governance-models. The author thanks the anonymous reviewers and the editorial board for their engagement with the framework and its methods. All errors remain the author's own.

## Appendix A: The isonomia Paper Series

This paper is the first in a planned series. The series architecture is as follows:

**Paper 1 (this paper): The Framework.** SAP phase space, EDR resilience composite, empirical validation across 389 systems. Establishes the theoretical scaffolding and primary empirical findings.

**Paper 2: The Lock-In Sequence.** Detailed analysis of the L→I→A→EDR suppression mechanism. Case studies: Early Uruk transition, Qin Legalist state, Inca Empire. Counter-case analysis: conditions under which high-L societies preserve EDR. Relevance to contemporary governance (digital surveillance, platform capitalism as L+I drivers).

**Paper 3: Succession Mechanism Attraction Basins and the Markov Transition Model.** Analysis of how succession mechanism type (hereditary, elective, appointment, consensus, rotation) varies as a function of surplus legibility (L) and pre-existing disobedience freedom (D₀). Phase 1 (static model, n = 117) finds that L and D₀ together predict succession type with chi-square p < 0.0001 and an odds ratio of 6.46 for D₀ in elective versus hereditary succession at high L (rank-biserial r = −0.782, p = 0.0001). Phase 2 (transition matrix, 43 type-changing events across 44 systems) documents conditional transition probabilities: elite reform events produce 0% hereditary outcomes (11 cases); L predicts appointment as a transition destination (OR = 2.24, permutation p = 0.005). Phase 3 (continuous-time Markov chain, 149 spells, 39 events, 110,589 system-years) estimates duration-weighted transition rates and L-conditional stationary distributions. π(appointment) rises from 0.135 at low L to 0.595 at high L (+0.460); π(elective) falls from 0.394 to 0.115 (−0.279). The primary attractor at high L is appointment, not hereditary, refining the lock-in sequence prediction: rising A enables bureaucratic appointment as the dominant governance form. The D₀ moderator is confirmed dynamically: high-D₀ elective systems exit elective succession at 0.55 per 1000 years versus 2.74 for low-D₀ systems (5.03×; Cox PH joint test p = 0.026). A secondary finding identifies consensus as a founding state rather than an equilibrium state — no documented transition from appointment or hereditary back to consensus exists in the dataset — directly supporting the Graeber-Wengrow claim about the asymmetric and largely irreversible nature of freedom loss.

**Paper 4: Schismogenesis Dynamics.** Agent-based model of governance differentiation in networked societies. Tests whether the observed network bipolarity (degree-4 sign reversal) can be reproduced by a simple schismogenesis rule. Historical case studies: Celtic non-urbanisation, Zomia state-avoidance, Haudenosaunee constitutional development in relation to European contact.

**Paper 5: Cross-Validation and Predictive Testing.** Cross-validation of EDR and SAP against five independent external datasets is reported in Paper 1 (Section 10.2): V-Dem v16 (r = 0.868–0.912, n = 16), Polity5 (r = 0.847–0.895, n = 11), WJP Rule of Law Index (E r = 0.904, R r = 0.861, n = 7 direct), Freedom House FIW (EDR r = 0.923, n = 9 direct), and CCP Comparative Constitutions Project (D r = 0.681, n = 11). Paper 5 extends this to the full V-Dem country-year dataset (n ≈ 180 countries, 1789–present), deepens the Seshat pre-modern validation (preliminary results in Paper 1 Section 10.2), adds the Mongol Empire and Achaemenid Empire to the Seshat matched set, tests the threshold hypothesis against documented collapse events in the cliodynamics database, and addresses the irreversibility question: conditions under which societies cross θ in the upward direction without external disruption.

**Paper 6 (provisional): Contemporary Implications.** Application of the framework to contemporary governance challenges — the digital surveillance state as A-maximisation, platform economies as novel L mechanisms, climate emergency as an external perturbation on low-EDR systems. Policy implications of the lock-in sequence interruption finding.
