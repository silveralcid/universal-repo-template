# Reusable Codex and Claude Code task prompts

These are **templates**, not another instruction hierarchy. Every prompt says to use `AGENTS.md` and current repository state; the [skills](../../.agents/skills/README.md), [canonical owners](../INDEX.md) and [delivery policy](../agents/delivery.md) always control what may be changed.

Use `python tools/repo.py prompt list` or `python tools/repo.py prompt show <name>` to select and copy a prompt. Replace `[GOAL]`, `[CONSTRAINTS]`, `[AREA]` and other bracketed fields with concrete information; remove placeholders not relevant to your task. **Never paste secrets or customer data into prompts.** Do not send every prompt, whole document corpus, or all tasks to a new agent.

| Prompt | Best use |
|---|---|
| [Investigate](investigate.md) | A bounded evidence-gathering pass before choosing an implementation |
| [Implement](implement.md) | One settled vertical feature or fix |
| [Autonomous sequential build](sequential-build.md) | A long but scoped build with reversible decisions and recoverable blockers |
| [Bug fix](bugfix.md) | Reproduce, isolate the root cause, fix and defend with regression tests |
| [QA and independent review](qa-review.md) | Review objective correctness, not alternative personal style |
| [Integration](integration.md) | Coordinate branches, ownership and dependency-aware merge preparation |
| [Repository-attached agent launch packs](repository-attached-agent-launch-packs.md) | Store each full lane/integrator prompt in GitHub and return one dropdown + short copyable launch script; [full prompt skeleton](../templates/agent-launch-pack.md) |
| [Research](research.md) | Research of possibly unrelated or tangential value |
| [Continuation](continuation.md) | Resume from prior branch, plan and evidence without restarting everything |

Prompts can be used in either provider. Do not set a model tier or permission in the prompt and assume the host enforces it: native models, client permissions and pricing live outside this repository. The [operating-cost policy](../agents/operating-cost.md) is guidance, not a billing or safety guarantee.
