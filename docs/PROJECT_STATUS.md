# Isonomia project status

Status: active research repository.

This repository should be read as paper-support code and data, not as a finished social-science dataset or a production package.

## What is strong

- The repository contains data, code, papers, and visualisations in one place.
- The coding scheme distinguishes direct evidence, inference, and auto-coding.
- The strongest quantitative claims are tied to the hand-coded subset.
- Cross-validation scripts are separated from the repository data because the external datasets are not redistributed.
- The project has a clear theoretical spine: linking emergence and collapse models through EDR resilience.

## What remains provisional

- Many cases remain auto-coded and need review.
- Historical operationalisation always involves judgement calls.
- Cross-validation depends on external datasets with their own concepts and limitations.
- Correlation results should not be read as causal proof.
- The succession and CTMC work is still being developed.

## How visitors should use this repository

Use it to inspect the argument, reproduce the supplied figures, review the coding scheme, and test whether the framework is useful.

Do not treat the dataset as a finished authority on all governance systems. It is an evolving research instrument.

## Next presentation improvements

- Add a visual gallery to the README.
- Add a single `make figures` or `python -m isonomia.figures` entry point.
- Add a data dictionary generated from the CSV columns.
- Add a short note explaining how to cite the repository and papers.
