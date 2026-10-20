# Prompt — resume unfinished agent work

Follow `AGENTS.md` and the `work-handoff` skill.

**Lane/PR/plan:** [TARGET]
**Desired next outcome:** [GOAL]

Read live branch/PR, its real dependencies, the latest small handoff and affected source/section hashes. Do **not** assume a prior transcript, handoff or stale commit is authoritative. Re-open changed relevant sections and newly affected contracts only; preserve completed work, prior test evidence and active lane boundaries. Classify prior work as aligned, adaptable, conflicting or blocked.

Choose the highest-value compatible unfinished slice and continue. Don't restart broad investigation without contradictory live evidence. If a dependency is still blocked, do independent reversible work and document the blocker. Run actual targeted checks on the new slice, update the plan/handoff with what changed, and commit/push to the authorized branch/PR. Do not merge or deploy without explicit approval.
