# Prompt — bounded investigation

In this repository, follow `AGENTS.md` and the relevant area guide. **Read-only investigation** unless I explicitly ask you to save a report.

**Question:** [GOAL]
**Known symptoms / evidence:** [EVIDENCE]
**Constraints:** [CONSTRAINTS]

Inspect current code, relevant existing research, docs, issues and tests. Use the context route for the affected area, then grep symbols/headings before opening large files. Do not repeat settled research, invent a root cause or expand into unrelated subsystems. Distinguish observed facts, plausible explanations and unresolved questions. Prefer the smallest reproduction or verification needed to separate hypotheses. Use external sources only where necessary and retain links and retrieval dates.

Deliver: current state; competing hypotheses and evidence; narrowest recommended fix or next experiment; actual owner/files/acceptance/verification; blockers that truly require a human decision. Do **not** implement, deploy, merge or touch production data. Stop when there is enough evidence to produce a Ready implementation packet, or clearly explain why one cannot responsibly be produced.
