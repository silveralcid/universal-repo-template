# Prompt — apply UI/UX standards

For a task that changes a user-facing interface, first follow `AGENTS.md`, the existing project stack, and the relevant owning docs. Use the focused [UX workflow](../design/ux-sop.md) and only the relevant [appearance](../design/ui-standard.md), [behavior](../design/ux-standard.md), [data](../design/data-display.md), or [agent surface](../design/agent-surfaces.md) guidance.

**Outcome:** [GOAL]
**Existing stack, constraints, and deviations:** [CONSTRAINTS]
**Acceptance:** [ACCEPTANCE]

Identify the normal user path and relevant states before polishing. Reuse the existing component library or proven alternatives; the optional ui-theme package is not a new-stack mandate. Keep URL state safe, distinguish missing values, show real failure/recovery, and respect keyboard/touch/contrast needs. For background or agent actions, make provenance, approvals, partial outcomes, and retries intelligible.

Implement the smallest runnable slice and verify relevant screen sizes, states, keyboard/focus, light/dark where supported, and a real failure mode where feasible. Report exactly what was tested, what remains unverified, source ref, and next action. Do not redesign adjacent features, introduce dependencies just for visual consistency, or claim CI/UI validation when only documentation checks ran.