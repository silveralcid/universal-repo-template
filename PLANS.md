# Execution plans (long-horizon work only)

For multi-session, dependency-heavy, high-risk, or multi-agent tasks, create **one live execution plan** using [the template](docs/templates/execution-plan.md) under [`docs/plans/active/`](docs/plans/README.md). Name an explicit owner and dependency order before dispatching parallel agents.

- A plan is **intended work**, never proof of implementation or test success.
- For small edits, skip this; don't make a multi-page plan for a ten-line change.
- Keep scope, non-goals, acceptance, checkpoints, dependency blockers and rollback in the plan; don't duplicate whole specs or research.
- Agent handoffs refer to the active plan and current PR/commit, not a competing task backlog.
- When done, mark accepted outcomes and move to `docs/plans/completed/` with a PR/test link. The live Git branch/PR remains authoritative for actual execution state.

Read [coordination](docs/agents/coordination.md) for lane ownership and merge gates.
