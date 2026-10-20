# Prompt — autonomous sequential build

Follow `AGENTS.md`, `START-HERE.md`, and the `project-bootstrap`/`implement-task` skills as appropriate.

**Product/outcome:** [GOAL]
**Constraints and known decisions:** [CONSTRAINTS]
**Definition of usable first slice:** [ACCEPTANCE]

Make a short execution plan in `docs/plans/active/` **only because this task spans dependent steps or sessions**. Identify the smallest runnable vertical slice, then build sequentially by dependency order. Inspect current repository state and existing work before each consequential slice; load only affected area guides, relevant sections and narrow tests. Reuse current stack or choose the simplest sensible one for an actually empty application; avoid speculative architectures.

Do as much independent, reversible implementation as the repository and authorization allow. If authentication, unavailable credentials, external approval, design ambiguity or infrastructure blocks one step, document the exact blocker and continue other **independent** work. Use mocks/fixtures only when clearly labeled and do not call a mock integration complete. Avoid repetitive research loops, redundant subagents and full-suite runs after tiny edits.

At each useful boundary, update the plan, actual verification evidence and resumable next action. Deliver code, real app integration, relevant tests and a branch/PR handoff. **No unapproved merging, deployment, paid-service enrollment or external mutation.** Stop when acceptance is met or every remaining path has a named external decision/blocker; report each unrun check instead of guessing.
