# Prompt — root-cause bug fix

Follow `AGENTS.md` and the appropriate area route.

**Bug:** [GOAL]
**Reproduction / expected vs actual:** [EVIDENCE]
**Constraints:** [CONSTRAINTS]

Check whether the issue is already fixed, duplicated or being worked on. Reproduce at the narrowest viable level and record the exact observed symptom; if reproduction is unavailable, label the limits. Trace to one authoritative owner and find the root cause rather than stacking defensive workarounds. Write the smallest regression test that fails for the problem when feasible, implement a scoped fix, and check the affected adjacent contract. Don't opportunistically rewrite nearby components.

Run targeted tests and a relevant integration check; inspect any user-visible result when possible. Report the cause and evidence, code paths changed, exact tests and outcomes, residual risks, PR or commit, and any blocker that cannot be safely guessed. Never claim unreproduced or unrun tests passed.
