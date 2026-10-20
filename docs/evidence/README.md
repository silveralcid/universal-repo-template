# Evidence — actual observed outcomes only

Keep lightweight, sanitized, dated reports of things people or agents **actually did**. These records do not set requirements or guarantee later behavior. Place artifacts by purpose:

- [`tests/`](tests/): unit, integration, end-to-end, regression, and test-suite runs.
- [`benchmarks/`](benchmarks/): performance measurements with pinned baseline, workload and environment.
- [`manual-qa/`](manual-qa/): human observations, UI/UX checklists and visual inspection.
- [`reproductions/`](reproductions/): bug reproductions, negative cases and diagnostic traces summarized in text.
- [`audits/`](audits/): bounded security, architecture, content or release audits with sources.
- [`agent-evals/`](agent-evals/): Codex/Claude agent workflow or skill evaluations, false positives and token/cost observations.

Required truth contract: actual source ref/commit, timestamp, command/procedure, environment, inputs, results, failures, skipped checks, limitations, and artifacts. Use `PASS`, `FAIL`, `NOT RUN`, `BLOCKED` or `INCONCLUSIVE`; do not turn an expected outcome into a tested fact.

Raw or private files go in ignored [`artifacts/`](../../artifacts/README.md) or restricted storage. Summary template: [`docs/templates/evidence-record.md`](../templates/evidence-record.md), or use `python tools/repo.py new evidence --slug <slug> --bucket tests`. See [policy](../agents/research-and-evidence.md).

Store only concise, reproducible summaries here. For raw output retention, hashes and restricted storage pointers use [artifact handling](ARTIFACTS.md). For recurring or high-impact failures, use an [incident record](../incidents/README.md).
