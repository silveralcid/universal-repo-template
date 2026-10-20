---
name: evidence-reporter
description: Document actual automated tests, performance benchmarks, manual acceptance checks, incident reproduction, or coding-agent evaluations with trustworthy provenance.
---

# Evidence Reporter

1. Identify the exact claim under verification, scoped code/docs ownership, acceptance criteria and repository/ref/commit.
2. Capture command or procedure, environment, inputs/fixtures, timestamps, actual output summary, observed failures, and baseline comparison when appropriate. Do not infer missing outcomes.
3. Mark each run PASS, FAIL, NOT RUN, BLOCKED, or INCONCLUSIVE. Separate local checks, hosted CI, manual inspection, and simulated evidence.
4. Save durable sanitized summaries in `docs/evidence/<kind>/` when explicitly requested: e.g. `python tools/repo.py new evidence --slug <slug> --bucket tests`. Keep raw logs, traces, screenshots and large outputs under ignored `artifacts/` or approved private storage.
5. Cite measured data and note limitations. A fast benchmark requires pinned workload, environment and comparable baseline; a single run is not a regression verdict.
6. Never claim the evidence file is a product requirement or that a script run by someone else was executed by this agent. See docs/engineering/VERIFICATION.md and docs/agents/research-and-evidence.md.
