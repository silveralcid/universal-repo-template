---
name: work-handoff
description: Create concise, verifiable cross-session handoffs for ongoing implementation, investigation or integration, including branch, tested SHA, blockers and next steps.
---

# Work Handoff

1. Verify real git state, requested base, PR/dependencies and task-local files; never assume a carried-forward handoff is current.
2. Record objective, scope, acceptance, decisions still open, owned paths, upstream dependency order, immutable source revision and relevant consumed document sections/hashes when needed.
3. Separate confirmed implementation, observed checks, intended work, unresolved risk and blocked human decisions. State exactly which commands were run and their results, and which weren't run.
4. Choose one smallest actionable next slice and an explicit review/merge authorization boundary. Do not create a duplicate branch ledger; live GitHub state remains authoritative.
5. If explicitly asked to save, use `python tools/repo.py new handoff --slug <slug> --bucket active` and adapt the generated template. For completed work, move the note to `docs/handoffs/completed/` or archive when no longer useful.
6. Do not use a handoff to sidestep current repository instructions or invent approvals. See docs/agents/handoff.md and docs/agents/delivery.md.
