# Data Gap Analysis
## isonomia — Civilisational Emergence & Resilience Framework
### Based on Graeber-Wengrow theoretical requirements

---

## Status

This document records the gap analysis conducted against the original `global-governance-models` dataset (41 entries) and the additions made to produce `governance_extended.csv` (389 entries). All Tier 1 and Tier 2 gaps listed below have been filled. Tier 3 entries represent further enrichment opportunities.

---

## Original Coverage (global-governance-models, v1)

The source dataset contained 41 entries with the following structural biases:

- **Region**: 12 of 41 entries were Greek political forms (29%); every other region had a single entry
- **Time**: 25 of 41 entries fell in 1000 BCE–500 CE; only 3 predated 1000 BCE; nothing post-1900
- **Type**: Governance types were granular but essentially one-per-type — no comparative variation within categories
- **Framework gaps**: No entries for the key cases Graeber & Wengrow build their argument around

---

## Gap 1 — Early Urbanism ✓ FILLED

**Why critical:** G&W's most provocative claim is that the first cities were not hierarchical. Without these cases, the framework has no empirical anchor for its claim about egalitarian urbanism at scale.

| System | Dates | Status |
|---|---|---|
| Çatalhöyük | –7500 to –5700 | ✓ Added (hand-coded, confidence 3) |
| Early Uruk | –4000 to –3100 | ✓ Added (hand-coded, confidence 3) |
| Late Uruk / Early Dynastic | –3100 to –2700 | ✓ Added (hand-coded, confidence 3) |
| Taosi | –2300 to –1800 | ✓ Added (hand-coded, confidence 2) |
| Teotihuacan | 100 to 550 CE | ✓ Added (hand-coded, confidence 3) |
| Mohenjo-daro / Indus Valley | –2600 to –1900 | ✓ Added (hand-coded, confidence 2) |
| Monte Albán | –500 to 700 | Covered via Zapotec Cocijo Cult (existing) |

---

## Gap 2 — Fertile Crescent Pre-State Forms ✓ FILLED

**Why critical:** The Natufian–PPNA–PPNB–Ubaid–Uruk sequence is the core empirical evidence for the "getting stuck" narrative. The dataset previously had nothing in this region before –1650.

| System | Dates | Status |
|---|---|---|
| Natufian Communities | –12500 to –9500 | ✓ Added (hand-coded, confidence 2) |
| Göbekli Tepe | –9600 to –8000 | ✓ Added (hand-coded, confidence 2) |
| PPNA | –9500 to –8700 | ✓ Added (hand-coded, confidence 2) |
| PPNB | –8700 to –6500 | ✓ Added (hand-coded, confidence 2) |
| Ubaid Culture | –6500 to –3800 | ✓ Added (hand-coded, confidence 2) |

---

## Gap 3 — Sub-Saharan Africa (non-coastal) ✓ PARTIALLY FILLED

**Why critical:** The interior African stateless tradition is the strongest real-world evidence for large-scale acephalous governance.

| System | Dates | Status |
|---|---|---|
| Tiv Segmentary Lineage System | –500 to 1900 | ✓ Added (hand-coded, confidence 3) |
| Great Zimbabwe | 1100 to 1450 | In upstream v2 dataset (auto-coded) |
| Kongo Kingdom | 1390 to 1914 | In upstream v2 dataset (auto-coded) |
| Buganda Kingdom | 1300 to 1900 | In upstream v2 dataset (auto-coded) |
| Lovedu Rain-Queen | 1600 to 1900 | Tier 3 — not yet added |

---

## Gap 4 — South and Southeast Asia ✓ PARTIALLY FILLED

| System | Dates | Status |
|---|---|---|
| Vedic Jana/Gana Sanghas | –1500 to –300 | ✓ Added (hand-coded, confidence 2) |
| Mauryan Empire | –322 to –185 | ✓ Added (hand-coded, confidence 3) |
| Zomia Highland Communities | 500 to 1950 | ✓ Added (hand-coded, confidence 3) |
| Balinese Negara | 900 to 1906 | ✓ Added (hand-coded, confidence 3) |
| Maratha Confederacy | 1674 to 1818 | In upstream v2 dataset (auto-coded) |

---

## Gap 5 — Northern Europe and the Steppe ✓ FILLED

| System | Dates | Status |
|---|---|---|
| Celtic Tribal Assemblies | –800 to 43 CE | ✓ Added (hand-coded, confidence 2) |
| Norse Thing System | 800 to 1300 | ✓ Added (hand-coded, confidence 2) |
| Scythian Nomadic Confederacy | –700 to –200 | ✓ Added (hand-coded, confidence 2) |
| Minoan Crete | –2700 to –1450 | ✓ Added (hand-coded, confidence 2) |
| Germanic Thing Assemblies | –200 to 900 | In upstream v2 dataset (auto-coded) |

---

## Gap 6 — Mesoamerica ✓ FILLED

| System | Dates | Status |
|---|---|---|
| Olmec | –1500 to –400 | ✓ Added (hand-coded, confidence 2) |
| Classic Maya City-States | 250 to 900 | ✓ Added (hand-coded, confidence 3) |
| Aztec Triple Alliance | 1428 to 1521 | ✓ Added (hand-coded, confidence 3) |
| Tlaxcala Republic | 1384 to 1521 | ✓ Added (hand-coded, confidence 2) |

---

## Gap 7 — Post-1500 Non-European Governance ✓ PARTIALLY FILLED

| System | Dates | Status |
|---|---|---|
| Iroquois Confederacy / Haudenosaunee | 1450 to 1900 | ✓ Added (hand-coded, confidence 3) |
| Maroon Communities | 1655 to 1900 | ✓ Added (hand-coded, confidence 2) |
| Cherokee Nation | 1820 to 1838 | In upstream v2 dataset (auto-coded) |
| Sioux Nation governance | 1700 to 1890 | In upstream v2 dataset (auto-coded) |
| Meiji Restoration Japan | 1868 to 1912 | In upstream v2 dataset (auto-coded) |

---

## Gap 8 — SAP Phase-Space Anchor Cases ✓ FILLED

These cases anchor the corners and edges of the SAP ternary and are essential for calibrating the coding scheme.

| System | SAP Role | Status |
|---|---|---|
| Egyptian Old Kingdom | High-S anchor | ✓ Added (hand-coded, confidence 3) |
| Egyptian Middle Kingdom | S→A transition | ✓ Added (hand-coded, confidence 3) |
| Shang Dynasty | High-S / proto-A | ✓ Added (hand-coded, confidence 3) |
| Inca Empire (Tawantinsuyu) | High-A without writing | ✓ Added (hand-coded, confidence 3) |
| Highland New Guinea Big Man System | High-P / low-S / low-A | ✓ Added (hand-coded, confidence 3) |
| Tang Dynasty | Full high-SAP | ✓ Added (hand-coded, confidence 3) |
| Ottoman Empire | High-SAP with partial E | ✓ Added (hand-coded, confidence 3) |

---

## Remaining Tier 3 Opportunities

These entries would enrich geographic and temporal coverage but are not required for the paper's core argument. All are present in the upstream v2 dataset as auto-coded entries (confidence 1) and are candidates for hand-coding in the next review pass.

- Lovedu Rain-Queen (Southern Africa, female ritual sovereignty)
- Maratha Confederacy (India, post-Mughal federated resistance)
- Cherokee Constitutional Republic (colonial-pressure governance adaptation)
- Sioux seasonal council / war-leader duality
- Meiji Restoration Japan (deliberate governance reinvention under external pressure)
- Blackfoot Confederacy (Plains nomadic confederacy)
- Mapuche Parlamento Confederacy (Chilean resistance confederacy)

---

## New Columns Added to governance_extended.csv

Beyond new rows, the following columns were added to support the isonomia framework. See `coding_scheme.md` for full operationalisation.

| Column | Type | Description |
|---|---|---|
| `sovereignty_index` | float 0–1 | Concentration of coercive power |
| `admin_index` | float 0–1 | Bureaucratic/record-keeping apparatus |
| `competitive_politics_index` | float 0–1 | Prestige/heroic/performative politics |
| `exit_freedom` | float 0–1 | Can members leave the system? |
| `disobedience_freedom` | float 0–1 | Can authority be refused? |
| `arrangement_freedom` | float 0–1 | Can new social forms be created? |
| `surplus_legibility` | float 0–1 | How measurable/extractable is surplus? |
| `info_infrastructure` | float 0–1 | Writing, recording, debt systems |
| `seasonality` | categorical | Whether governance mode oscillates deliberately |
| `binding_mechanism` | categorical | Primary mechanism preventing exit |
| `scale_population` | ordinal 1–5 | Approximate population scale |
| `scale_territory` | ordinal 1–5 | Approximate territorial scale |
| `collapse_mode` | categorical | How the system ended |
| `gw_discussed` | boolean | Whether G&W explicitly discuss this case |
| `coding_confidence` | ordinal 1–3 | Evidence quality (1=auto-coded, 2–3=hand-coded) |
| `notes` | text | Coding rationale and caveats |
| `succession_changes` | text | Documented within-system succession mechanism transitions; format `[from]->[to] (YEAR): trigger_note`; 24 systems coded, 37 transition events; see `data/coding_scheme.md` for full format specification |

**Note on derived columns:** `succ_canon` is a derived column computed by `succession_attraction_basins.py` at runtime by mapping `Succession Method` through the `CANON` dictionary. It is not stored in `governance_extended.csv`. Scripts that need it apply the mapping directly from `Succession Method`.
