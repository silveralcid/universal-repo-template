# Verification policy

**Owner:** What to check, when, and how to report truthfully. Application commands are unset until a project stack is chosen. A documentation check is not proof that an application works.

| Boundary | Minimum verification |
|---|---|
| During implementation | Targeted unit/fixture/manual check; record any checks unavailable |
| Before PR/handoff | Actual configured lint/types/tests and `python tools/repo.py docs check` for docs changes |
| Integration/merge | Cross-boundary checks and real runtime/browser testing as applicable |
| Performance | Equivalent pinned workload and environment, baseline SHA, repeated runs and confidence limitations |
| Security | Provenance and permissions, negative cases, no secrets/PII in committed logs or artifacts |
| Research and agent experimentation | Hypothesis, methods, alternatives, reproducibility, evidence vs decision separation |
| Release/deploy | Explicit approval and environment-specific validation, monitoring and rollback |

Write a concise factual report in [`docs/evidence/`](../evidence/README.md) only for meaningful durable findings. Keep sensitive, raw or large outputs in ignored [`artifacts/`](../../artifacts/README.md) or access-controlled storage. Report statuses **PASS / FAIL / NOT RUN / BLOCKED / INCONCLUSIVE** per executed procedure; never call a proposed test or simulated result a pass.

[`docs/experiments/`](../experiments/README.md) owns experiment plans. [`docs/agents/research-and-evidence.md`](../agents/research-and-evidence.md) owns location and authority distinctions. `.repo/project.json` lists optional application commands; `null` means **not configured**, not passing.
