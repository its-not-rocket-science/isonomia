# Isonomia

> A research repository for modelling the emergence, resilience, and dissolution of governance systems.  
> Status: active paper-support and data-analysis repository.

Isonomia is named for the pre-Athenian idea of equal political arrangement: a form of equality under law and collective ordering that is older and broader than modern electoral democracy.

This repository contains data, code, visualisations, and paper drafts for a theoretical framework connecting two bodies of work that are usually discussed separately:

- emergence models: how governance forms arise;
- collapse models: why complex hierarchical societies become fragile or fail.

The central argument is that three freedoms associated with Graeber and Wengrow — exit, disobedience, and arrangement — can be treated as a composite resilience indicator and tested against historical governance data.

## What is in this repository

```text
isonomia/
├── data/
│   ├── governance_extended.csv
│   ├── network_edges.csv
│   ├── crossval_matched.csv
│   ├── succession_working_set.csv
│   ├── survival_spells.csv
│   ├── transition_data.csv
│   └── coding_scheme.md
├── docs/
│   ├── data_gap_analysis.md
│   ├── theoretical_framework.md
│   └── PROJECT_STATUS.md
├── paper/
│   ├── paper_01_framework_v3.md
│   └── paper_02_lock_in.md
├── src/
│   ├── phase_space.py
│   ├── edr_resilience.py
│   ├── schismogenesis.py
│   ├── geo_contagion_analysis.py
│   ├── lock_in_figures.py
│   ├── crossvalidate_edr.py
│   ├── succession_attraction_basins.py
│   └── succession_markov_ctmc.py
├── visuals/
└── requirements.txt
```

## Quick start

```bash
git clone https://github.com/its-not-rocket-science/isonomia
cd isonomia
pip install -r requirements.txt

python src/edr_resilience.py
python src/phase_space.py
python src/schismogenesis.py
python src/geo_contagion_analysis.py
python src/succession_attraction_basins.py
python src/succession_attraction_basins.py --phase2
python src/succession_markov_ctmc.py
```

## Model summary

### SAP phase space

The model uses three elementary forms of domination:

- **S — Sovereignty:** concentration of coercive power.
- **A — Administration:** bureaucratic or record-keeping apparatus.
- **P — Competitive politics:** prestige, heroic competition, or performative politics.

### EDR resilience composite

The model uses three freedoms:

- **E — Exit:** can members leave the system?
- **D — Disobedience:** can authority be refused?
- **R — Arrangement:** can new social forms be created?

The working hypothesis is that systems with high EDR retain more self-correcting capacity, while low-EDR systems are more exposed to Turchin/Tainter-style fragility and collapse dynamics.

## Preliminary findings

The current repository reports:

- an EDR–SAP correlation of `r = -0.844` in the hand-coded subset (`n = 125`);
- an EDR–SAP correlation of `r = -0.775` in the full dataset (`n = 389`);
- a resilience threshold around `θ = 0.45`;
- a bimodal EDR distribution, suggesting clustering above and below the threshold;
- no simple secular decline in EDR over time.

These are research findings, not settled claims. Coding confidence and validation notes are documented in `data/coding_scheme.md`.

## Dataset

`data/governance_extended.csv` contains 389 governance systems spanning approximately 12,000 BCE to the present.

Coding confidence is marked as:

- `3` — direct archaeological or textual evidence for the relevant variables;
- `2` — reasonable inference from known structural features;
- `1` — auto-coded from governance type or characteristics and requiring human review.

The hand-coded subset is the basis for the strongest quantitative claims.

## Cross-validation

External validation scripts support comparisons against V-Dem, Polity5, World Justice Project, Freedom House, Comparative Constitutions Project, and Seshat datasets.

Those datasets are not redistributed here. Place downloaded files in `downloads/` and run:

```bash
python src/crossvalidate_edr.py   --vdem downloads/V-Dem-CY-Core-v16.csv   --polity downloads/p5v2018d.xls   --seshat downloads/Equinox2020.05.2023.csv   --wjp downloads/2025_wjp_rule_of_law_index_HISTORICAL_DATA_FILE.xlsx   --fiw downloads/All_data_FIW_2013-2021.xlsx   --ccp downloads/ccpcnc_v5.zip
```

Matched results are written to:

```text
data/crossval_matched.csv
```

## Status

See [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) for a plain-English status note.

Current broad status:

- Paper 1: submitted.
- Paper 2: draft complete.
- Paper 3: succession model in progress.
- Paper 4: schismogenesis agent-based model planned.
- Paper 5: deeper V-Dem and Seshat validation planned.

## Licence

MIT — see `LICENSE`.
