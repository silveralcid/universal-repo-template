# Research, experiments and evidence — single operating policy

**Owns:** how to store unapproved ideas, dated investigations, exploratory work, experiments, observed results and source provenance. This is a provider-neutral policy linked from `AGENTS.md` and skills.

## Keep epistemic categories separate

| Location | Meaning | Authority |
|---|---|---|
| [`docs/research/`](../research/README.md) | Background studies, loosely related questions, leads, candidate ideas and validated findings | **Non-canonical** regardless of apparent quality |
| [`docs/experiments/`](../experiments/README.md) | Pre-registered hypotheses, methods, trials and learnings | **Non-canonical**; an experiment is not an approved feature |
| [`docs/evidence/`](../evidence/README.md) | Timestamped test runs, benchmarks, manual QA, reproductions and agent evaluations | **Observed** results, not guaranteed continuing truth |
| [`docs/handoffs/`](../handoffs/README.md) | Continuation packets and dependencies for current work | Working state, **not** branch or product canon |
| [`docs/decisions/`](../decisions/README.md), [`docs/adr/`](../adr/README.md), canonical specs | Owner-approved decisions and scoped contracts | **Intended behavior**, according to its owner |
| [`docs/archive/`](../archive/README.md) | Superseded historical records | Historical only |
| [`artifacts/`](../../artifacts/README.md) | Raw untracked command output, logs, captures, traces or bulky evidence | Local transient data; ignored by Git |

## How a research idea advances

1. `inbox`: a lead or source with no verification, possibly unrelated.
2. `exploratory`: bounded investigation, applicability unknown; record hypotheses and disconfirming evidence.
3. `candidates`: plausible project fit and a concrete suggested validation, *not approved*.
4. `validated`: independently substantiated claim (source/date/version pinned), still *not approved*.
5. `archive`: out-of-date, superseded or deliberately not pursued; keep backlink when useful.

Movement between buckets changes research maturity, **never project authority**. To adopt a finding, obtain the owner decision, update the canonical owner, and link back to the source research; do not copy entire studies into project requirements. A rejected or unrelated idea may remain safely in exploratory/archive forever.

## Experiment and test discipline

A trial needs hypothesis, baseline, method, controlled variable, expected observation, actual results, limitations and outcome. A **test result** needs source ref/SHA, environment, exact command or manual procedure, input/fixture, status (`PASS`, `FAIL`, `NOT RUN`, `BLOCKED`, `INCONCLUSIVE`), timestamps, artifacts, and attribution. Include repeatability notes and avoid presenting a quick benchmark as conclusive.

Prefer short, reviewed Markdown summaries in Git. Large screenshots, recordings, browser profiles, CSV dumps and potentially private logs belong under ignored `artifacts/` or approved secure storage; reference sanitized hashes or restricted locations rather than committing PII or credentials. Never claim a missing file, test run, owner decision or dataset exists.

## Practical writing tools

- `python tools/repo.py new research --slug <name> --bucket exploratory`
- `python tools/repo.py new experiment --slug <name> --bucket proposed`
- `python tools/repo.py new evidence --slug <name> --bucket tests`
- `python tools/repo.py new evidence --slug <name> --bucket benchmarks`
- `python tools/repo.py new handoff --slug <name> --bucket active`

These create blank dated records and refuse collisions; they do not execute research or tests. Templates live in [`docs/templates/`](../templates/).

## Source revalidation and traceability

Keep findings discoverable through the optional [research index](../research/INDEX.md), using links rather than copying findings. A current source may become stale: record the date/version, what could invalidate it, and the next revalidation trigger. Evidence that influenced a proposed or adopted decision should link forward from the study and backward from the decision and relevant acceptance tests. This is a **chain of references**, not competing copies of the source.

Raw artifacts and retention are governed by [evidence artifact handling](../evidence/ARTIFACTS.md); security and prompt injection by [trust boundaries](trust-boundaries.md).
