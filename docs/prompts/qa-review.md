# Prompt — independent QA and change review

Follow `AGENTS.md`, `docs/agents/definition-of-done.md` and the task's accepted specification.

**Target branch/PR/ref:** [TARGET]
**Acceptance:** [ACCEPTANCE]
**Review focus:** [CONSTRAINTS]

Inspect the actual diff and base, owning area and affected tests. Determine whether the desired behavior is connected and verifiable. Check correctness, security, scope, behavior regressions, contract drift, stubs disguised as integrations, missing test coverage and misleading completion claims. Review only what materially affects the requirements or risk; don't demand a subjective rewrite of otherwise correct code.

Return actionable findings prioritized by severity with exact paths, evidence and the smallest corrective action. Separate VERIFIED, UNVERIFIED and NOT RUN. Distinguish your own observations from CI reports. Review mode is read-only unless I explicitly authorize fixes; do not merge or deploy.
