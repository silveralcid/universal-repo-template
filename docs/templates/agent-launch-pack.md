# Agent launch-pack prompt template

> Use when an agent's **full executable prompt** will be committed to GitHub and selected through a small chat launcher. Follow the [presentation and handoff standard](../prompts/repository-attached-agent-launch-packs.md) and the project's existing `AGENTS.md` and delivery rules. Replace or remove placeholders; a file with TBD fields is not launch-ready.

## [PROJECT / FEATURE] — [AGENT ROLE / LANE]

**Mission:** [Specific outcome and acceptance, not merely "research" or "write code"]
**Assigned executor/model:** [The explicit requested model and standing agent, when required by the project; the user selects the model in their client]
**Repository:** `[OWNER/REPOSITORY]`
**Agent branch and isolated worktree:** `[TASK_BRANCH]`
**Starting point:** `[EXACT_VERIFIED_SHA_OR_APPROVED_PARENT]`
**PR base/integration authority:** `[PARENT_BRANCH]` — [INTEGRATOR]
**Coordinator and dependencies:** [EXACT ISSUE/PR URLs, dependency checkpoint names]
**Canonical owner documents:** [Minimum task-specific links]

### Exclusive write scope

Owned: [EXACT PATHS/GLOBS AND TESTS]

Not owned: [SHARED HOT FILES, CONTRACTS, OTHER LANES' PATHS, PROTECTED TRUNKS, RIGHTS-GATED ASSETS]

If a change needs another lane's file, publish a contract/request through the coordinator; do not race edits.

### Start immediately

1. Inspect current repository/PR branch heads, existing code and the relevant owner docs. State any contradictions rather than fabricating missing APIs.
2. Do independent useful work without waiting for other lanes. [REAL TASK PHASES AND TECHNICAL REQUIREMENTS].
3. Publish the smallest tested public interface early as [CHECKPOINT NAME] with exact commit SHA, signatures and consumer notes. Consume other lane checkpoints only when actually published.
4. Implement and test [EXPLICIT PASS/FAIL ACCEPTANCE, NEGATIVE CASES, BUDGETS]. Preserve rights, security, game/runtime and other protected boundaries.
5. Commit and push scoped files, open/update [DRAFT OR ALLOWED PR] against [APPROVED BASE], and post [STATUS NAME, SOURCE SHA, EXACT TEST COMMANDS/RESULTS, UNRUN/BLOCKED CHECKS] to [COORDINATOR].
6. If blocked, finish independent work; leave a durable continuation and an explicit dependency request. Do not claim nonexistent asynchronous capabilities.

### Completion and handoff

[REAL USER-VISIBLE / CODE ACCEPTANCE]
[REQUIRED TESTS AND EVIDENCE]
[INTEGRATOR WIRING RESPONSIBILITIES]
[EXPLICIT MERGE/DEPLOY PERMISSION STATUS — DEFAULT NO]

A complete committed prompt file is **not** proof this session has executed. The accompanying chat launcher is a short pointer to this file, not a replacement for it.
