# Reproducible continuation / handoff

Use a concise handoff for **multi-session, multi-agent, high-risk, or dependency-heavy** work. Do not produce detailed SHA inventories for trivial single-file edits.

A useful handoff names:

- Objective, explicit acceptance criteria, confirmed/non-goal scope, decision status and blockers.
- Git repository, integration base, working branch, PR, source commit, unmerged dependencies and owned paths.
- Canonical documents / **specific sections actually consumed**, with source ref and relevant file blob SHA for work sensitive to evolving design.
- Verified state: commands, environment, exact results, what was not run and why. Label CI vs local vs manual clearly.
- What remains: next smallest compatible slice, sequencing, deferred decisions and review needed.

Compare affected section content rather than reloading an entire documentation tree whenever a broad index changes. Never claim your session inherited fresh instructions automatically: check them explicitly. Use [the handoff template](../templates/handoff.md) as needed.

For active multi-phase work, link its **single active execution plan** from `docs/plans/active/` rather than copying the planned milestones into each handoff.
