<img src="isonomia-social-preview-hero.png" alt="Isonomia — Equality under the law" width="100%">

# Isonomia

[![Papers](https://img.shields.io/badge/papers-6-1a3d2b)](https://its-not-rocket-science.github.io/isonomia/)
[![V-Dem validation](https://img.shields.io/badge/V--Dem%20validation-r%20%3D%200.91-c9a227)](https://its-not-rocket-science.github.io/isonomia/)
[![Span](https://img.shields.io/badge/historical%20span-2%2C600%20years-8b1a1a)](https://its-not-rocket-science.github.io/isonomia/)
[![MIT licence](https://img.shields.io/badge/licence-MIT-c9a227)](LICENSE)

*Ἰσονομία — equality under the law.*

A formal model of political freedom, legal equality, and governance resilience across roughly 2,600 years of historical systems. Data, code, and papers.

**[→ Interactive research site](https://its-not-rocket-science.github.io/isonomia/)**

---

## Overview

Isonomia addresses a gap in comparative politics: most quantitative governance datasets cover the modern era, treat freedom as a single variable, and provide no formal model of *why* systems persist or collapse. This project builds a formal model from first principles and tests it against historical data spanning ancient city-states, tribal confederacies, empires, colonial systems, and modern democracies.

The model formalises three properties:

- **Legal equality** — the degree to which law applies uniformly across persons and groups
- **Political freedom** — the degree to which subjects can participate in, contest, and exit governance
- **Resilience** — the structural conditions under which systems persist under internal and external stress

---

## Dataset

| Attribute | Value |
|---|---|
| Governance systems | 401 |
| Historical span | ~3000 BCE — present |
| Variables per system | 24 |
| Validation against V-Dem | r = 0.91 |
| Validation against Polity5 | r = 0.87 |
| Validation against WJP Rule of Law | r = 0.83 |

---

## Papers

Six papers are in preparation or under review. See the [research site](https://its-not-rocket-science.github.io/isonomia/) for current submission status.

| Paper | Journals | Status |
|---|---|---|
| Paper 1 — The Isonomia Index | Cliodynamics | Under review |
| Paper 2 — Resilience and collapse | Social Evolution & History | Under review |
| Papers 3–6 | Various | In preparation |

---

## Research site

The [interactive Pages site](https://its-not-rocket-science.github.io/isonomia/) includes:

- **Phase-space explorer** — visualise governance systems as trajectories through freedom/equality/resilience space
- **Trajectory explorer** — trace individual systems through time
- **Validation tables** — full comparison against V-Dem, Polity5, WJP
- **Methodology** — coding guide, source list, reliability section
- **Data download** — full dataset in CSV and JSON

---

## Repository structure

```
isonomia/
├── data/
│   ├── governance_systems.csv     # Master dataset
│   ├── attributes.md              # Data dictionary
│   └── transitions.csv            # Regime transitions
├── src/
│   ├── model/                     # Formal model implementation
│   ├── analysis/                  # Statistical analysis scripts
│   └── figures/                   # Figure generation
├── docs/                          # GitHub Pages site source
└── papers/                        # Paper drafts (anonymised for review)
```

---

## Reproducing the results

```bash
pip install -r requirements.txt
python src/analysis/generate_all.py     # regenerates all figures and tables
python src/analysis/validate.py         # runs V-Dem / Polity5 / WJP validation
```

---

## Related projects

- [global-governance-models](https://github.com/its-not-rocket-science/global-governance-models) — historical governance dataset
- [eunomia](https://github.com/its-not-rocket-science/eunomia) — computational governance reasoning
- [tensor-based-game-theory…](https://github.com/its-not-rocket-science/tensor-based-game-theory-identifying-critical-coalitions-climate-change-negotiations) — related formal methods work

---

## Data licence

Code: MIT.
Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite the repository and note that historical data is estimated; see `data/attributes.md` for source and confidence information per record.

---

Dr Paul Schleifer · [ORCID 0009-0004-7972-3566](https://orcid.org/0009-0004-7972-3566) · London, UK
