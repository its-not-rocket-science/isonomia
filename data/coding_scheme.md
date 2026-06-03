# Coding Scheme
## SAP/EDR Variables — Operationalisation Guidelines

This document defines the coding criteria for all quantitative variables in `governance_extended.csv`. The goal is sufficient precision that two independent coders would agree within ±0.15 on any given score.

---

## General Principles

1. **Code the system at its modal period**, not its peak or nadir. If a system lasted 500 years and was hierarchical for 400, code the hierarchical configuration. Note exceptions in the `notes` field.

2. **Code structural capacity, not formal ideology.** A system may claim to be democratic while structurally eliminating D. Code what the structure permits, not what it claims.

3. **Use the anchor values below** as calibration points. When uncertain, ask: which anchor case most resembles this system on this dimension?

4. **Coding confidence** reflects evidence quality:
   - `3` = Direct archaeological/textual evidence for the specific variables
   - `2` = Reasonable inference from known structural features
   - `1` = Speculative; sparse evidence; high uncertainty

5. **The `gw_discussed` flag** marks cases Graeber & Wengrow explicitly engage with in *The Dawn of Everything* (2021). These are the cases where the framework must be most precise.

---

## Sovereignty Index (S) — 0.0 to 1.0

*Measures the concentration and durability of coercive power in identifiable authority.*

| Value | Description | Anchor Cases |
|---|---|---|
| 0.0–0.1 | No identifiable coercive authority; violence is distributed and situational | San Xaro Networks, Zomia Highland Communities |
| 0.15–0.25 | Situational authority exists but is ad hoc, personal, and easily ignored | Natufian Communities, Highland New Guinea Big Man |
| 0.3–0.45 | Established authority that can be and regularly is refused; no monopoly on violence | Gadaa System, Iroquois Confederacy, Celtic Tribal Assemblies |
| 0.5–0.65 | Recognised sovereignty with meaningful institutional constraints | Roman Republic, Akan Chieftaincy, Tlaxcala Republic |
| 0.7–0.8 | Strong sovereignty with limited formal constraints; resistance is costly | Khmer Devaraja, Tang Dynasty, Mauryan Empire |
| 0.85–1.0 | Near-absolute sovereign power; resistance is fatal; monopoly on legitimate violence | Egyptian Old Kingdom, Zulu Monarchy, Aztec Triple Alliance |

**Key question:** Can the sovereign's authority be refused without fatal consequences to the refuser?

---

## Administration Index (A) — 0.0 to 1.0

*Measures the extent and sophistication of record-keeping, surveillance, and bureaucratic apparatus.*

| Value | Description | Anchor Cases |
|---|---|---|
| 0.0–0.1 | Oral tradition only; no records; no systematic tracking of persons or resources | San Xaro Networks, Highland New Guinea Big Man, Zomia |
| 0.15–0.25 | Mnemonic devices, tallies, or tokens; partial tracking of specific transactions | Inca (pre-quipu period), Göbekli Tepe |
| 0.3–0.45 | Quipu-style systems, proto-writing, or partial script used for specific purposes | Inca Empire, Early Uruk, Hittite Panku Council |
| 0.5–0.65 | Partial literacy; records for trade and religion but not full census or legal code | Minoan Crete, Classic Maya City-States |
| 0.7–0.8 | Full administrative literacy; census, taxation records, legal codes, correspondence | Satrapy System, Late Uruk, Mauryan Empire |
| 0.85–1.0 | Complete bureaucratic apparatus; examination systems, legal plurality, population registers | Confucian Bureaucracy, Tang Dynasty, Ottoman Empire |

**Key question:** Can the state track, record, and enforce obligations on individual persons?

**Institutional complexity vs administrative apparatus:** A measures specifically the *administrative deployment of information systems* — census, taxation records, legal codes, correspondence, population registers. High institutional complexity (elaborate assemblies, age-set rotations, ceremonial procedures) does not imply high A unless that complexity is used to track and manage populations. The Gadaa System has high institutional complexity but very low A (oral tradition, no population records, no taxation apparatus). The Inca Empire has high A despite no writing (quipu knotted-cord system tracks every household's labour obligations). Score A on administrative capacity, not organisational sophistication.

**Partial writing systems:** When a society has a writing system used for religion or trade but not yet for census, taxation, or legal enforcement, score A at 0.4–0.5 rather than 0.7+. The administrative deployment of literacy is what matters, not literacy itself.

---

## Competitive Politics Index (P) — 0.0 to 1.0

*Measures the degree to which politics operates through prestige competition, performance, and heroic display.*

| Value | Description | Anchor Cases |
|---|---|---|
| 0.0–0.1 | No political competition; authority is ascribed or entirely suppressed | Extreme theocracies where politics = religious observance |
| 0.15–0.3 | Personal prestige exists but is non-transferable and non-political | Natufian Communities, Göbekli Tepe |
| 0.35–0.5 | Competitive selection for positions; prestige influences governance | Gadaa System, Iroquois Confederacy, Kurultai |
| 0.55–0.7 | Institutionalised competition; elections, contests, or tournaments determine authority | Roman Republic, Greek Democracy, Confucian examinations |
| 0.75–0.85 | Politics as performance; ritual display and competitive feasting as primary governance mode | Pacific Potlatch, Classic Maya City-States, Theatrocracy |
| 0.9–1.0 | Governance IS performance; spectacle is the mechanism of authority | Balinese Negara, Theatrocracy at peak |

**Key question:** Is authority achieved through competitive display rather than ascription or administrative position?

**Critical distinction — competitive display vs performance of held power:** P measures competition *for* positions or authority, not the theatrical exercise of authority already held. Military campaigns, public executions, elaborate court ceremonies, and ideological spectacle in absolute monarchies are expressions of S, not P. High P requires that the political order creates genuine competition — where multiple actors vie for influence, position, or legitimacy through display. An absolute ruler who holds pageants is low-P; a system where daimyo compete for rank through attendance, gifts, and conspicuous display is moderate-P even within a hierarchical order; a system where political authority is literally constituted by ritual performance (Balinese Negara) is high-P.

**Common miscoding:** Totalitarian states (Qin, Soviet) are often overcoded on P because their propaganda and ideological apparatus looks like competitive display. These are S mechanisms deployed administratively, not P. The test is: does the display *determine* who holds authority, or does it *confirm* authority already held by other means?

---

## Exit Freedom (E) — 0.0 to 1.0

*Measures how easily members can leave the governance system without catastrophic cost.*

| Value | Description | Anchor Cases |
|---|---|---|
| 0.0–0.1 | Exit is physically prevented or legally capital; debt bondage, serfdom, hostage systems | Tokugawa Shogunate, Mauryan Empire at peak |
| 0.15–0.25 | Exit possible but socially catastrophic; total loss of kin, status, and resources | Aztec Triple Alliance, Egyptian Old Kingdom |
| 0.3–0.45 | Exit possible with significant friction; requires abandoning land or patronage | Khmer Devaraja, Feudal Europe |
| 0.5–0.65 | Exit feasible; migration or joining another community is a known option | Çatalhöyük, Iroquois Confederacy, Tlaxcala Republic |
| 0.7–0.8 | Exit is relatively easy; mobility is expected and culturally normal | Celtic Tribal Assemblies, Norse Thing System, Kurultai |
| 0.85–1.0 | Exit is structurally built in; seasonal dispersal, nomadism, or community fission is the norm | San Xaro Networks, Zomia, Scythian Confederacy, Inuit Qaggiq |

**Key question:** Could an ordinary member leave this system within a year without losing their life or everything they have?

---

## Disobedience Freedom (D) — 0.0 to 1.0

*Measures whether authority can be refused through legitimate or customary channels.*

| Value | Description | Anchor Cases |
|---|---|---|
| 0.0–0.1 | Refusal of authority = death or severe punishment; no sanctioned channel for dissent | Tokugawa Shogunate, Zulu Monarchy at peak |
| 0.15–0.25 | Refusal possible only through underground/illegal means; no legitimate channel | Egyptian Old Kingdom, Aztec Triple Alliance |
| 0.3–0.45 | Ritual or customary refusal channels exist but are narrow and risky | Roman Republic (client obligations), Akan Chieftaincy |
| 0.5–0.6 | Meaningful right to refuse within defined domains; some institutional protection | Greek Democracy, Iroquois Confederacy |
| 0.65–0.75 | Strong customary right to refuse; levelling mechanisms, ridicule, or council override | Igbo Assemblies, San Xaro Networks, Gadaa System |
| 0.8–1.0 | Disobedience is structurally encoded; authority literally requires consent to function | Gadaa (age-set rotation means authority cannot be held indefinitely) |

**Key question:** Can an ordinary member refuse a direct instruction from authority without punishment?

**Special cases:** The Gadaa System's age-set rotation means the *system itself* enforces D — no leader can exceed their term. Code as 0.85. The Iroquois clan mothers' veto encodes D institutionally — code D higher than general council refusal would suggest.

---

## Arrangement Freedom (R) — 0.0 to 1.0

*Measures whether members can create new social institutions or reorganise existing ones.*

| Value | Description | Anchor Cases |
|---|---|---|
| 0.0–0.1 | Social structure entirely fixed by sacred law; innovation = heresy | Theocracies at peak; some late Imperial China |
| 0.15–0.25 | Minor variation within rigid categories; no structural innovation | Tokugawa (strict class system); Egyptian Old Kingdom |
| 0.3–0.45 | Institutional innovation possible if it doesn't threaten existing hierarchy | Roman Republic; most stable monarchies |
| 0.5–0.6 | New institutions regularly created; governance forms are understood as human choices | Swiss Cantonal Democracy; Iroquois Confederacy |
| 0.65–0.8 | Seasonal or periodic institutional reinvention; governance forms deliberately varied | Gadaa System; many seasonal forager communities |
| 0.85–1.0 | Social arrangements are explicitly understood as contingent human creations; high recombination | Maroon Communities; Zomia; Natufian seasonal oscillation |

**Key question:** Does the society understand its governance arrangements as chosen and changeable, or as sacred/natural and fixed?

**Note on G&W:** Their argument is partly that awareness of *R* — the knowledge that social arrangements are inventions — was widespread in early human history and has been systematically suppressed by ideologies of inevitability. High *R* is not naivety; it is sophisticated political self-consciousness.

---

## Surplus Legibility (L) — 0.0 to 1.0

*Following James Scott: how measurable, countable, and extractable is the primary surplus of this society?*

| Value | Description | Anchor Cases |
|---|---|---|
| 0.0–0.1 | Surplus is dispersed, mobile, or hidden; roots, forest products, game — unquantifiable | San Xaro Networks, Zomia, Inuit |
| 0.2–0.35 | Some legibility; herds can be counted, plots estimated, but extraction is difficult | Nomadic pastoralists, swidden agriculturalists |
| 0.4–0.55 | Moderate legibility; fixed agriculture with some surplus tracking | PPNA, early Çatalhöyük |
| 0.6–0.75 | High legibility; grain stores, standardised units, taxable outputs | Early Uruk, Zapotec, Mississippian |
| 0.8–0.9 | Maximum legibility; census-linked grain taxation; complete extraction apparatus | Inca, Mauryan, Aztec |
| 0.95–1.0 | Near-total legibility; industrial-scale surplus tracking (rare before modern period) | — |

---

## Information Infrastructure (I) — 0.0 to 1.0

*The existence and deployment of systems for recording obligations, debts, ownership, and persons.*

| Value | Description | Anchor Cases |
|---|---|---|
| 0.0–0.1 | Oral tradition only; memory is the only record | San Xaro, Highland New Guinea |
| 0.15–0.25 | Mnemonic devices; tally sticks; ritual memory systems | Aboriginal Elders Councils, early Natufian |
| 0.3–0.4 | Tokens, tallies, or proto-writing for specific transactions | Ubaid tokens, early quipu |
| 0.45–0.6 | Partial writing system; records for trade, religion, or royal propaganda but not full admin | Minoan Linear A, Shang oracle bones, early Uruk |
| 0.65–0.8 | Full writing system deployed for administrative purposes; legal codes, census, correspondence | Late Uruk, Satrapy, Hittite |
| 0.85–1.0 | Complete literate bureaucracy; debt systems, property records, population registers, legal plurality | Confucian Bureaucracy, Ottoman, Tang |

**Note:** The Inca case demonstrates that high L can exist without high I (the quipu system achieves ~0.6 I without writing). Score I based on the *administrative deployment* of information systems, not literacy alone.

---

## Seasonality (categorical)

*Whether the governance mode deliberately oscillates between different configurations.*

| Value | Meaning |
|---|---|
| `high` | Deliberate, institutionalised oscillation; winter/summer or ceremonial/everyday modes |
| `medium` | Some seasonal variation in governance intensity; ceremonial periods that shift authority |
| `low` | Minimal seasonal variation; governance operates in roughly continuous mode |
| `none` | No seasonal governance oscillation |
| `unknown` | Insufficient evidence |

---

## Binding Mechanism (categorical)

*The primary mechanism that reduces exit freedom — what makes it hard to leave.*

| Value | Meaning |
|---|---|
| `none` | No binding mechanism; exit is free |
| `land` | Agricultural land tenure; leaving means losing your productive base |
| `debt` | Financial obligation that follows you |
| `clan` | Kinship obligations that require presence |
| `military` | Service obligation; desertion is punishable |
| `ritual` | Sacred obligations; leaving means spiritual severance |
| `tribute` | Tributary relationship; non-participation is punished |
| `labour` | Corvée or service obligation |
| `status` | Social position is location-specific; leaving = losing all rank |
| `hostage` | Family members held as guarantors (Tokugawa sankin-kōtai) |
| `community` | Strong communal obligations without formal coercion |
| `honour` | Social shame for departure; non-coercive but powerful |
| `coercion` | Direct physical enforcement; slavery, serfdom |

Multiple values may apply; separate with `/`.

---

## Collapse Mode (categorical)

*How the system ended, if it did.*

| Value | Meaning |
|---|---|
| `ongoing` | System continues to present |
| `transition` | Transformed into a successor form (not abrupt) |
| `fragmentation` | Split into smaller successor polities |
| `conquest` | Absorbed by external military force |
| `abandonment` | Population dispersed without clear cause |
| `colonial disruption` | Disrupted or destroyed by European colonial expansion |
| `colonial imposition` | Replaced by externally imposed governance |
| `colonial absorption` | Gradually absorbed into colonial administrative systems |
| `regicide` | Killed through internal assassination/coup |
| `revolution` | Replaced by internal political transformation |
| `dissolution` | Formally dissolved without conquest |
| `climate` | Linked to climatic/environmental stress |
| `forced opening` | Opened by external pressure (Perry's Japan) |
| `annexation` | Formally annexed by larger power |
| `FIP` | First Intermediate Period (Egypt-specific) |
| `unknown` | Insufficient evidence |

Multiple values may apply.

---

## Scale Variables

### scale_population (ordinal 1–5)
| Value | Approximate population |
|---|---|
| 1 | < 1,000 |
| 2 | 1,000 – 50,000 |
| 3 | 50,000 – 500,000 |
| 4 | 500,000 – 5,000,000 |
| 5 | > 5,000,000 |

### scale_territory (ordinal 1–5)
| Value | Approximate territory |
|---|---|
| 1 | < 100 km² (village, city) |
| 2 | 100 – 10,000 km² (city-state, small region) |
| 3 | 10,000 – 500,000 km² (small nation, large region) |
| 4 | 500,000 – 5,000,000 km² (large nation, small empire) |
| 5 | > 5,000,000 km² (large empire, continental scale) |

---

## External Construct Validity

The EDR composite and SAP variables have been cross-validated against five independent external datasets. Matched rows and all correlation results are stored in `data/crossval_matched.csv` (source column identifies dataset; mismatch_flag column identifies temporal proxies excluded from primary correlations). Run `src/crossvalidate_edr.py --vdem ... --polity ... --seshat ... --wjp ... --fiw ... --ccp ...` to reproduce all figures and tables.

---

### V-Dem v16 (https://www.v-dem.net)

16 matched systems, 1789–2015. Two systems removed after structural mismatch review: Roman Republic (ITA 1870 is post-Risorgimento Italy, not a valid proxy) and Qin Legalism (CHN 1949 is PRC, not a valid proxy). Dutch Republic re-matched from NLD 1800 to NLD 1789 (within Republic lifespan; 1800 was Batavian/Kingdom of Holland).

| Isonomia variable | V-Dem variable | r | p | n |
|---|---|---|---|---|
| EDR composite | Liberal democracy index (v2x_libdem) | 0.868 | <0.001 | 16 |
| EDR composite | Egalitarian democracy (v2x_egaldem) | 0.899 | <0.001 | 12 |
| EDR composite | Deliberative democracy (v2x_delibdem) | 0.912 | <0.001 | 12 |
| E (exit freedom) | Freedom of movement (v2clfmove) | 0.893 | <0.001 | 16 |
| R (arrangement) | Civil society organisations (v2cseeorgs) | 0.776 | <0.001 | 16 |
| D (disobedience) | Judicial compliance (v2jucomp) | 0.650 | 0.006 | 16 |

---

### Polity5 (https://www.systemicpeace.org/inscrdata.html)

11 matched systems.

| Isonomia variable | Polity5 variable | r | p | n |
|---|---|---|---|---|
| EDR composite | DEMOC (0–10) | 0.847 | 0.001 | 11 |
| SAP composite | AUTOC (0–10) | 0.895 | <0.001 | 11 |
| S (sovereignty) | AUTOC | 0.870 | 0.001 | 11 |
| D (disobedience) | XCONST (executive constraints) | 0.747 | 0.008 | 11 |
| P (competitive politics) | PARCOMP | 0.491 | ns | 11 |

Note on P: lower correlation expected. iso_P captures prestige competition and non-electoral competitive politics that Polity's electoral-focused PARCOMP does not measure. Range restriction (iso_P 0.30–0.75 in modern matched set) additionally suppresses the correlation. See FIW-B result below.

---

### WJP Rule of Law Index 2025 (https://worldjusticeproject.org/rule-of-law-index/)

7 direct matches (target year ≥ 1980; modern political entity matched to WJP data). 7 proxy matches (target year < 1980; WJP measures successor state — excluded from primary correlations, shown in figure as grey points).

Sub-factor mapping: D → Factor 1 (government constraints), 1.2 (judiciary limits government), 1.5 (non-governmental checks), 4.3 (due process). E → 4.4 (expression), 4.6 (privacy). R → 4.7 (assembly), 3.3 (civic participation).

| Isonomia variable | WJP sub-factor composite | r | p | n |
|---|---|---|---|---|
| E (exit freedom) | Expression + privacy (4.4, 4.6) | 0.904 | 0.005 | 7 |
| R (arrangement) | Assembly + civic participation (4.7, 3.3) | 0.861 | 0.013 | 7 |
| D (disobedience) | Constraints + due process (F1, 1.2, 1.5, 4.3) | 0.640 | ns | 7 |
| EDR composite | Overall rule of law | 0.633 | ns | 7 |

Note: D and EDR ns at n = 7; proxy points (shown in figure) suggest positive pattern across the full range. n = 7 limits statistical power. WJP does not cover Switzerland (CHE) or Iceland (ISL).

---

### Freedom House Freedom in the World 2013–2021 (https://freedomhouse.org/report/freedom-world)

9 direct matches (target year ≥ 1980). 7 proxy matches (target year < 1980 — excluded from correlations).

Sub-score mapping: B (Political Pluralism and Participation) → iso_P; D (Freedom of Expression and Belief) → iso_E; E (Associational and Organisational Rights) → iso_R; F (Rule of Law) → iso_D. All sub-scores normalised to 0–1 from raw maximums (B: 16, D: 16, E: 12, F: 16).

| Isonomia variable | FIW sub-score | r | p | n |
|---|---|---|---|---|
| E (exit freedom) | FIW-D Expression and Belief | 0.895 | 0.001 | 9 |
| R (arrangement) | FIW-E Associational Rights | 0.943 | <0.001 | 9 |
| D (disobedience) | FIW-F Rule of Law | 0.866 | 0.003 | 9 |
| EDR composite | Civil Liberties aggregate | 0.923 | <0.001 | 9 |
| EDR composite | Total score | 0.923 | <0.001 | 9 |
| P (competitive politics) | FIW-B Political Pluralism | 0.357 | ns | 9 |

Note on P: iso_P range 0.30–0.75 in direct matched set causes range restriction. Grey proxy points in `crossval_fiw.png` show positive pattern across full range. FIW-B is the best available external P proxy; the ns result reflects the composition of the modern matched set rather than construct invalidity.

---

### CCP Comparative Constitutions Project v5 (https://comparativeconstitutionsproject.org/download-data/)

14 matched systems (Habsburg at AUT 1900 and Joseon at KOR 1895 excluded: year gaps of 18y and 53y respectively exceed threshold). CCP codes de jure constitutional text only.

Variable recoding: binary provisions (1 = right enshrined, 2 = right absent, 96/98 = n/a → NaN) recoded to 1.0/0.0/NaN. intexec (executive independence from legislature, ordinal 1–4) recoded as (4 − intexec) / 3, where high = constrained executive.

Composite mapping: ccp_D = mean(judind, dueproc, habcorp, fairtri, intexec_recoded); ccp_E = mean(freemove, express, privacy, press); ccp_R = mean(assem, assoc, petition).

| Isonomia variable | CCP composite | r | p | n |
|---|---|---|---|---|
| D (disobedience) | judind + dueproc + intexec (recoded) + habcorp + fairtri | 0.681 | 0.021 | 11 |
| E (exit freedom) | freemove + express + privacy + press | 0.230 | ns | 11 |
| R (arrangement) | assem + assoc + petition | 0.084 | ns | 11 |

**Important note — binary ceiling effect:** ccp_E and ccp_R use binary provisions that show near-zero variance in the matched set (most constitutions enshrine these rights in text). This suppresses r for E and R and does not indicate measurement failure. ccp_D retains variance because intexec is ordinal (1–4) and constitutional constraint provisions vary meaningfully across the matched systems.

**De jure / de facto gaps** — systems where |iso − ccp| > 0.4 on any dimension (ccp_dejure_gap = 1 in crossval_matched.csv):

| System | iso_E | ccp_E | iso_D | ccp_D | iso_R | ccp_R | Interpretation |
|---|---|---|---|---|---|---|---|
| Soviet Republics System | 0.05 | 0.75 | 0.05 | 0.40 | 0.08 | 1.00 | 1977 constitution enshrined rights denied in practice — passive revolution |
| Meiji Oligarchy | 0.20 | 0.75 | 0.15 | 0.00 | 0.20 | 1.00 | 1889 constitution; rights overridden by lèse-majesté and public peace laws |
| Singaporean Technocracy | 0.65 | 0.50 | 0.20 | 0.00 | 0.20 | 0.67 | Constitution silent on executive constraint (intexec = unconstrained) |
| European Union Governance | 0.70 | 1.00 | 0.55 | 0.75 | 0.55 | 1.00 | German Basic Law over-scores for EU governance; mismatch of unit |
| British Parliamentary System | 0.80 | 0.25 | 0.85 | 0.40 | 0.70 | 0.33 | No written constitution; common-law freedoms absent from CCP text coding |
| Althingi Carbon-Neutral Parliament | 0.80 | 0.75 | 0.85 | 0.40 | 0.75 | 0.67 | Iceland's constitution under-specifies rights relative to practice |
| Cossack Hetmanate | 0.65 | 0.75 | 0.65 | 0.80 | 0.55 | 1.00 | Ukrainian constitution generous on paper; gap narrows with gap ≤ 0.4 except R |

The Soviet, Meiji cases are the strongest instances of the passive-revolution mechanism described in Paper 2 Section 8.3. The British case illustrates CCP's limitation for unwritten constitutional systems, not a coding error.

---

### Seshat: Global History Databank — Equinox-2020 (https://seshat-db.com/downloads_page/)

14 pre-modern systems, 3000 BCE–1600 CE.

| Isonomia variable | Seshat variable | r | p | n |
|---|---|---|---|---|
| A (admin index) | Admin composite (admin levels, bureaucrats, merit promotion) | 0.604 | 0.022 | 14 |
| I (info infrastructure) | Writing composite (written records, script) | 0.672 | 0.008 | 14 |
| S (sovereignty) | Military composite (professional soldiers, military levels) | 0.774 | 0.003 | 12 |
| SAP composite | Admin composite | 0.710 | 0.004 | 14 |
| D (disobedience) | Legal composite (formal legal code, executive constraints) | 0.066 | ns | 11 |

Note: D non-result is expected — Seshat measures social complexity, not freedom. No Seshat variable captures exit, disobedience, or arrangement freedom directly.

Note on Inca and iso_I: iso_I = 0.70 (quipu-based information infrastructure) vs Seshat writing composite = 0.00 (no script). This is not a coding error. iso_I measures state capacity to track resources and populations; Seshat's writing composite measures script presence. The Inca administered the largest pre-Columbian empire without writing, using khipu knotted-cord records. The divergence is annotated in `crossval_seshat.png` and illustrates the distinction between information infrastructure (iso_I) and script-based literacy (Seshat writing composite). Mongol Empire and Achaemenid Empire are absent from the current matched set (both are in Seshat as mn_mongol_emp and ir_achaemenid_emp); planned addition for Paper 4.

## Reliability Exercise Results

A blind re-coding of 25 systems spanning the full EDR and SAP range was conducted by the primary coder. Results after P and A clarifications:

| Dimension | MAD | Target | Status |
|---|---|---|---|
| S | 0.078 | < 0.15 | ✓ |
| A | 0.096 | < 0.15 | ✓ |
| P | 0.086 | < 0.15 | ✓ |
| E | 0.086 | < 0.15 | ✓ |
| D | 0.120 | < 0.15 | ✓ |
| R | 0.132 | < 0.15 | ✓ |
| L | 0.088 | < 0.15 | ✓ |
| I | 0.129 | < 0.15 | ✓ |
| **SAP composite** | **0.072** | < 0.15 | **✓** |
| **EDR composite** | **0.089** | < 0.15 | **✓** |

Categorical agreement: collapse mode 84% ✓, binding mechanism 36% (multi-value matching), seasonality 8% (vocabulary inconsistency). Categorical variables do not contribute to the paper's main quantitative findings.

Remaining substantive disagreements (dEDR ≥ 0.15): Napoleon R (original conservative reading retained), Cucuteni D (original retained), Gadaa D (original retained). Gupta EDR, Ottoman R, and Soviet R revised based on exercise findings.

## Inter-rater Reliability Targets

For a paper with quantitative analysis, we aim for Cohen's κ > 0.6 on the categorical variables and mean absolute deviation < 0.15 on the continuous 0–1 indices. The anchor cases above are designed to provide calibration points that make this achievable.

The most contested codings are likely to be:
- **D for systems with formal refusal mechanisms that rarely function** (e.g. Mandate of Heaven)
- **A for systems with sophisticated non-literate administration** (e.g. Inca quipu)
- **R for systems where governance reinvention is implicit rather than explicit**

In all contested cases, err toward the lower value and note the uncertainty.
