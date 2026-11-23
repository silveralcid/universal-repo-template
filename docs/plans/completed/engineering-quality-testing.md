# Engineering quality and testing upgrade

**Status:** IMPLEMENTED AND LOCALLY VERIFIED; draft review remains the delivery boundary
**Owner:** integration coordinator
**Base:** fresh `origin/main` at `cdc452f236af8eb498d79f86e3f38d40c6005796`
**Delivery:** isolated feature branch and draft PR; no merge or deployment

## Accepted scope and non-goals

Add canonical risk-based testing and concise code-quality owners, connect the
existing entrypoints, and strengthen the existing command runner only where
concrete false-success or missing-check failures are reproducible. Preserve
stack choice, existing functionality, source review, and context budgets. No new
frameworks, dependencies, services, provider-specific policy, or coverage quotas.

## Lanes and dependency order

| Lane | Exclusive write ownership | Exit evidence |
|---|---|---|
| Runner | `tools/repo.py`, `tools/repo_support/`, `tools/tests/` | Existing suite plus focused failure regressions |
| Standards | `docs/engineering/TESTING.md`, `docs/engineering/CODE-QUALITY.md`, `docs/engineering/VERIFICATION.md`, `docs/agents/agent-evaluation.md`, `docs/templates/test-report.md` | One owner per policy, concise applicable guidance |
| Independent review | Read-only inspection and bounded task trials | Defect, integration failure, false-positive test, overengineering findings |
| Coordinator | Remaining routing/docs, project configuration if needed, this plan, source manifest, Git/PR | Source/link/budget checks, exact draft head and CI results |

Audit existing behavior before changing it. Agree runner semantics before
finalizing command documentation. Review and task trials follow implementation;
source-manifest refresh follows reviewed final files. Integrate with targeted
checks, then run the full existing infrastructure and documentation gates.

## Acceptance and evidence

- New projects register their real stack commands; template health cannot prove
  application behavior, integration, or runtime quality.
- Missing checks, command failures, and blocked execution cannot be reported as
  successful application verification where mechanically observable.
- Test guidance covers independent expectations, representative failures,
  realistic fixtures, regression sensitivity, integration, and reproducibility.
- AI application guidance uses deterministic checks and human-validated cases;
  agent behavior evaluation remains separate from application evaluation.
- Representative task trials record what is executed versus reviewed guidance.
- Infrastructure tests, documentation links, context budgets, source checks and
  applicable GitHub Actions are reported against the actual source.

## Risks and rollback

Exit status alone cannot detect vacuous application tests or prove agent
compliance. No live paid services or production data are needed for this work.
Keep changes reviewable and revertible by commit; preserve the existing draft
launch-pack branch. A required unavailable check remains an explicit limitation.

## Completed position

Existing mechanisms were audited and retained. Canonical standards, scoped
routing and seven focused regressions are implemented. The full suite passes
94 tests; docs and all existing context budgets pass. Independent review found
no blocking issue. Fresh-context task trials exercised the four required cases.
See [executed evidence](../../evidence/tests/2026-11-23-engineering-quality.md)
for commands, observed failures/recovery, source hashes and limitations. Source
packaging and hosted checks are finalized on the draft PR; local results do not
stand in for those outcomes. No merge or deployment is part of this task.
