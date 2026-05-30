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

## Inter-rater Reliability Targets

For a paper with quantitative analysis, we aim for Cohen's κ > 0.6 on the categorical variables and mean absolute deviation < 0.15 on the continuous 0–1 indices. The anchor cases above are designed to provide calibration points that make this achievable.

The most contested codings are likely to be:
- **D for systems with formal refusal mechanisms that rarely function** (e.g. Mandate of Heaven)
- **A for systems with sophisticated non-literate administration** (e.g. Inca quipu)
- **R for systems where governance reinvention is implicit rather than explicit**

In all contested cases, err toward the lower value and note the uncertainty.
