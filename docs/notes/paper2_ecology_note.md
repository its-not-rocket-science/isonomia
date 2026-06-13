# Ecological setting of D₀: robustness note for Paper 2

## Where to insert this

The note belongs in the **limitations section** of Paper 2, after the acknowledgement 
of the D₀ circularity concern (that D₀ and D share the same measurement framework), 
and before the conclusion. It can also be referenced in a footnote from the first 
paragraph introducing D₀ as a moderator.

Suggested in-text footnote at first mention of D₀ (Section 3 or wherever the OR=6.46 
is introduced):

> ³ The distribution of D₀ across systems is itself non-random: ecological conditions
> partially set the structural floor on D₀ via their effect on sovereign capacity S.
> See the robustness note in Section [X] and the companion analysis
> `src/ecology_of_freedom.py`.

---

## The note itself

**Subsection heading (add to limitations or a new robustness subsection):**

### The Ecological Setting of D₀

The D₀ moderator finding — that systems starting above θ=0.45 have a 6.46× higher 
odds of avoiding lock-in — treats initial disobedience freedom as an exogenous 
starting condition. A natural question is whether that starting condition is itself 
systematically structured by factors outside the governance framework. If D₀ is 
ecologically determined, the OR=6.46 finding partly reflects geographic fortune 
rather than institutional path dependence.

An exploratory cross-sectional analysis across the 327 geocoded systems in the 
dataset finds a significant positive correlation between absolute latitude and D 
(r=+0.316, p<0.001, n=327). High-latitude societies have substantially higher D 
than tropical ones, with 73.7% of high-latitude systems (|lat|≥40°) above the 
θ=0.45 threshold compared with 36.7% of low-latitude systems (|lat|<25°; 
Mann-Whitney p<0.001). Mediation analysis shows that 84.7% of this relationship 
runs through S: high-latitude ecological conditions constrain state-building 
capacity, which in turn sets a higher structural floor on D. This is the 
cross-sectional analogue of the lock-in sequence itself — the same S→D pathway 
that operates dynamically within the sequence also structures the cross-sectional 
distribution of starting points.

Importantly, the latitude-D relationship is not driven by agricultural surplus 
accumulation in the way that standard political economy models predict. 
Stratifying by economic base, r(|lat|, D) is non-significant for agricultural 
systems (r=+0.102, p=0.45, n=58) but significant for foraging/fishing 
(r=+0.386, p=0.005, n=52) and extraction economies (r=+0.447, p=0.003, n=41). 
This pattern contradicts a simple Boserup interpretation: the ecological roots of 
high D₀ run through ecological constraints on S in non-agricultural societies, 
not through the channelling of agricultural surplus through state apparatus. 
Once a society is agricultural, latitude ceases to predict D, because surplus 
accumulation becomes the dominant variable regardless of geographic location.

The result survives the two most obvious confounds. Excluding all European and 
North American systems, the correlation remains: r=+0.264, p<0.001, n=285. 
Restricting to systems with higher coding confidence (coding_confidence>1), 
the correlation strengthens: r=+0.477, p=0.0001, n=65. The relationship is 
therefore not an artefact of high-D Scandinavian and North American liberal 
democracies inflating the high-latitude cluster, nor of speculative low-confidence 
prehistoric codings.

The implication for the D₀ moderator finding is that the odds advantage of 
starting above θ is partly structurally set by ecological conditions. Systems 
in ecological settings that constrain state capacity — non-agricultural, 
high-latitude, resource-dispersed — begin with higher D₀ floors and therefore 
enter the lock-in sequence with more structural room for resistance. This does 
not invalidate the D₀ finding: the OR=6.46 is a conditional probability given 
the lock-in process begins, and the process begins across ecological settings. 
But it does suggest that the most ecologically constrained states face a double 
structural advantage: lower S makes lock-in harder to initiate, and the 
resulting higher D₀ makes it harder to complete if initiated.

*Note: This is an exploratory cross-sectional result. It is not causal: single-coder 
codings, the acknowledged circularity between S and D in the framework, and the 
absence of an instrumental variable for ecological conditions mean that the 
latitude-D result should be treated as suggestive rather than confirmatory. 
Full analysis is available in `src/ecology_of_freedom.py`.*
