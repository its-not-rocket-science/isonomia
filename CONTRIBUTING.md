# Contributing to Isonomia

Thank you for your interest in contributing. Isonomia is an active research
project. The most useful contributions right now are coding reviews, additional
historical cases, and methodological feedback.

---

## What kind of contributions are welcome?

### High priority
- **Inter-rater reliability coding** — independently coding a subset of the 401
  governance systems using the published codebook and reporting agreement
  statistics. Contact the author before starting.
- **Additional historical cases** — well-documented governance systems not
  currently in the dataset, particularly from under-represented regions
  (sub-Saharan Africa, Southeast Asia, Oceania, pre-Columbian Americas).
- **Methodological critique** — issues identifying problems with coding
  decisions, statistical choices, or theoretical framing.

### Medium priority
- **Bug reports** in the analysis scripts (`src/`).
- **Documentation improvements** — clarifications to the codebook, README,
  or inline code comments.
- **Replication attempts** — running the analysis scripts and reporting any
  discrepancies.

### Lower priority (but welcome)
- Performance improvements to the interactive visualisations in `docs/`.
- Accessibility improvements to the GitHub Pages site.

---

## How to contribute

1. **Open an issue first** before submitting a pull request, so we can discuss
   whether the change fits the project's direction.
2. **Fork the repository** and create a branch from `main`.
3. **Follow existing code style** — Python scripts use standard PEP 8 formatting.
4. **Test your changes** — run the relevant analysis scripts and confirm outputs
   are unchanged for existing data.
5. **Submit a pull request** with a clear description of what changed and why.

---

## Reporting issues

Use the issue tracker for:
- Bugs in analysis scripts
- Factual errors in the dataset
- Broken links or paths in the README
- Suggestions for new features or analyses

Please include enough detail to reproduce the problem — Python version, OS,
and the exact command or script that failed.

---

## Data contributions

If you want to propose a new governance system for the dataset:
- Check that it is not already present (see `data/governance_extended.csv`).
- Provide at minimum: system name, approximate date range, region, and
  primary source(s).
- Code against the published codebook (see `data/attributes.md` — if this
  file is missing from your local clone, request it via an issue).

---

## Contact

Paul Schleifer — ORCID [0009-0004-7972-3566](https://orcid.org/0009-0004-7972-3566)

Open an issue rather than emailing directly where possible, so discussions
are visible to other contributors.
