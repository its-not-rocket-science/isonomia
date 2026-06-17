# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2026-06-17

First stable release. Tags the dataset, analysis scripts, and GitHub Pages
site as submitted for or under review at the target journals.

### Dataset
- 401 governance systems, six dimensions (S, A, P, E, D, R)
- Systems span deep prehistory to the present
- Core statistical analyses focus on the past 2,600 years
- v7 of `data/governance_extended.csv`
- Supplementary files: `data/d_trajectory_parsed.csv` (30 trajectory systems),
  `data/succession_events.csv` (57 events), `data/network_edges.csv` and
  `data/network_nodes.csv` (353-node citation network, 773 edges)

### Analysis scripts (`src/`)
- `ecology_of_freedom.py` — latitude, economic base, binding mechanism
- `supplementary_analysis.py` — brittleness, seasonality, gender
- `survival_analysis.py` — Kaplan-Meier and Cox PH, time to D-threshold crossing
- `trajectory_cluster_lca.py` — DTW clustering, quadrant transitions, GMM LCA
- `recovery_depth.py` — recovery mechanisms and D₀ × (1−S) ordering
- `a_decomposition.py` — normalising fraction II/A and arrangement freedom R
- `succession_events.py` — succession event parsing and CTMC calibration
- `schismogenesis_abm.py` — Paper 4 agent-based model, parameter sweep,
  G–W case studies
- `generate_network.py` — generates network_edges.csv and network_nodes.csv

### Papers (status at release)
| # | Title | Status |
|---|-------|--------|
| 1 | The Isonomia Index | Under review — JWSR |
| 2 | The Lock-in Sequence | Ready to submit — JWSR / CPS |
| 3 | Succession and the CTMC | Ready to submit — JMS / Social Networks |
| 4 | Schismogenesis ABM | Draft complete — JASSS |
| 5 | Hegemonic Drift | Under review — Social Evolution & History |
| Cliodynamics | Synthesis | Under review — Cliodynamics |

### Site
- Interactive GitHub Pages site at `docs/index.html`
- Sections: Phase Space, Trajectories, Hegemony, Ecology, Succession,
  Recovery, Survival, Archetypes, A-decomp, ABM, Reliability
- All data embedded inline; no external API calls

### Validation
- V-Dem r = 0.91, Polity5 r = 0.87, WJP r = 0.83
  (rounded; full table in Paper 1 and `docs/index.html` Reliability section)

---

## Unreleased

Changes since v1.0.0 will be tracked here.
