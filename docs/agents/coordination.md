# Parallel-agent and dependency coordination

**Purpose:** Keep many Codex and Claude Code lanes correct, reviewable and cheap to integrate.

1. **Plan only if needed.** For mutually dependent or long-horizon changes, write a concise [execution plan](../../PLANS.md). One integration coordinator owns dependency order. Avoid subagents for a grep, a few reads, or a single small fix.
2. **Exclusive write ownership.** Each active lane declares owned paths/globs. If two lanes need the same file, sequence them or designate one owner and an interface contract; never ask both to race edits in the same worktree.
3. **Isolation.** Prefer one branch and isolated worktree per independently writing lane. Verify the correct base, branch head, clean worktree, and overlaps before implementation. Do not force-push, rebase another agent's active work, or use an unapproved parent branch.
4. **Dependencies.** A downstream lane may investigate against a pinned unmerged dependency, but may not claim it merged; require a specific ref/SHA and name what it depends on. Independent research can run in parallel; implementation of shared contracts cannot.
5. **Review boundary.** Each PR reports exact checked commands and outcomes; merge based on the tested immutable head. A moving head, conflicting owner, failed test or unclear semantics is a HOLD, not permission to guess. Only merge with the owner's authorization.
6. **Derived status.** Git/PR/CI is authoritative for live branch state. Plans and [handoffs](handoff.md) are snapshots; do not build a second manually maintained PR registry.
7. **Conflicts.** Escalate semantic conflicts and any new cross-domain authority to the owner. Mechanical conflicts can be repaired by an authorized integrator after targeted checks; record the resolution and rationale.

Complex tasks use [execution-plan template](../templates/execution-plan.md); resumptions use [handoff template](../templates/handoff.md). Neither overrides current instructions or verified code.

**Read-only preflight:** `python tools/repo.py branch check` reports local status, configured integration base and cached ahead/behind counts. It never verifies the live remote, PR collisions or mergeability; obtain current remote state with authorized tools before merging.
