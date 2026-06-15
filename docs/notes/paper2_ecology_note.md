# Robustness and extension notes for Paper 2 ecology analysis
# For inclusion in `docs/notes/` alongside `paper2_ecology_note.md`

---

## Note A: Ecological setting of D₀ (original note — see docs/notes/paper2_ecology_note.md)

## Note B: Seasonality as a mechanism for ecological S-constraints

The ecology analysis (`src/ecology_of_freedom.py`) finds r(|latitude|, D) = +0.316
mediated 84.7% through S. A further question is: what is the structural mechanism
through which ecological conditions constrain S?

Seasonality of resource availability provides a partial answer. Across 388 systems
with coded seasonality, the correlation with D is r = +0.348, KW H = 45.84 (p < 0.001).
However, 95.9% of this relationship is mediated through S, and the partial
r(seasonality, D | S) = 0.043 (p = 0.44) is non-significant. Seasonality does not
independently predict D beyond what S already explains; it is an ecological predictor
of S.

The mechanism operates through binding type. High-seasonality societies show 75.0%
none/voluntary binding, 16.7% social binding, and only 4.2% material binding.
No-seasonality societies show 50.9% material binding (land, tribute, debt) and
only 7.3% none/voluntary. This crosstab (chi-squared p < 0.001) identifies the
mechanism: episodic, mobile resources cannot be monopolised year-round, preventing
the construction of material-binding surplus extraction structures (land tenure,
tributary systems, debt peonage) that are the mechanism through which S rises.

The Graeber-Wengrow argument about seasonal variation in social structure
(Mauss and Beuchat 1904-05; discussed in The Dawn of Everything, chapter 3)
is therefore supported in a specific, mechanistic sense: seasonal episodicity
does not directly produce egalitarianism, but it prevents the construction
of the sovereign capacity that suppresses it.

**Statistical note:** r(seasonality, S) = -0.355, p < 0.001 (n = 388).
Partial r(seasonality, D | lat + S) = 0.038, p = 0.50. The seasonal effect
on D operates entirely through S, not independently.

---

## Note C: Gender structure as an independent predictor of D

Gender structure (coded in the `Gender Roles` field) shows a strong raw correlation
with D (r ≈ 0.35 before controlling for era). After controlling for historical era,
the within-era correlations remain substantial: r(gender, D | classical) = +0.716,
r(gender, D | medieval) = +0.586 (both p < 0.001).

Critically, the gender-D relationship survives controlling for binding mechanism:
partial r(gender, D | binding) = +0.403, p < 0.001. Gender structure is not
simply a proxy for social versus material binding — it carries independent
information about D after binding type is accounted for.

Two mechanisms are plausible but cannot be distinguished cross-sectionally:

(a) Latent variable: gender egalitarianism and political disobedience freedom both
    reflect a common underlying disposition toward horizontal rather than vertical
    social organisation. They are correlated because they measure aspects of the
    same structural property, not because one causes the other.

(b) Constituency expansion: societies with broader gender participation in governance
    have more people with a stake in maintaining D, producing higher effective D
    through a larger resistance-capable population.

**Coding note:** The `Gender Roles` field contains ~140 unique values and required
broad categorisation (egalitarian-ish = gender-neutral, gender-balanced, gender-mixed,
gender-equal; male-dominated = all others). This coding is rough; finer distinctions
would strengthen or attenuate the result.

---

## Note D: Collapse cause as evidence for lock-in brittleness

(This note was incorporated directly into Paper 2 §8.2 as a robustness result.)
See `paper_02_lock_in.md` §8.2 for the full analysis and statistics.

Summary: internal collapses (revolt, civil war, administrative dissolution; n=16)
occur at the highest S (mean=0.675) and lowest D (mean=0.200) of any collapse type.
Environmental collapses occur at significantly higher D (mean=0.492) and lower S
(mean=0.444). MW D: p=0.003; MW S: p=0.002. Lock-in produces brittleness, not
stability.
