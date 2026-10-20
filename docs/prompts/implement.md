# Prompt — scoped implementation

Follow `AGENTS.md`, the live source and the relevant `docs/agents/areas/` guide; use the `implement-task` skill.

**Outcome:** [GOAL]
**Scope and exclusions:** [CONSTRAINTS]
**Acceptance:** [ACCEPTANCE]

Check current branch/dependencies and the actual project implementation. Read only the task's owner and directly affected contracts. Treat any supplied packet as a starting hypothesis, not a replacement for live code. Reuse existing implementations and choose the smallest coherent vertical slice, including the real callsite/UI/consumer. Make reversible implementation choices without new rounds of permission requests; escalate only irreversible, costly, sensitive or unresolved owner decisions. Do not expand to nearby features.

Run the narrowest useful checks during development; then run applicable integration/acceptance checks. Record PASS/FAIL/NOT RUN/NOT CONFIGURED honestly. Update the canonical documentation in the same change when behavior or contract changes. Commit to an isolated branch and create a draft PR if authorized/tooling permits; **do not merge or deploy** without explicit approval.

Report what is implemented, actually connected and tested; links/commit; scope left undone; blockers; next smallest slice. No speculative claims of completion.
