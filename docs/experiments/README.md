# Experiments — hypotheses and trials, not decisions

Store **proposed** experiment designs under [`proposed/`](proposed/), **active** scoped experiments under [`active/`](active/), and conclusive or inconclusive summaries under [`completed/`](completed/). Detailed actual run evidence belongs under [`docs/evidence/`](../evidence/README.md); raw datasets and logs belong under ignored [`artifacts/`](../../artifacts/README.md).

Required fields: question, falsifiable hypothesis, owner/approval for side effects, variables, baseline/control, procedure, expected outcomes, stopping rule, source ref, measurements, uncertainty and conclusion. Never treat a favorable result as authorization to modify canonical behavior.

New blank plan: `python tools/repo.py new experiment --slug <slug> --bucket proposed`. See [policy](../agents/research-and-evidence.md).
