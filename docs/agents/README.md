# Task-specific area router

Use this when real modules or workflows have distinct owners, invariants, and narrow checks. Do not invent project subsystems in a blank template. For shared policies start at [docs/INDEX.md](../INDEX.md) and route to the canonical policy.

| Task | Guide | Narrow check |
|---|---|---|
| Repository documentation changes | [Documentation policy](documentation.md) | `python tools/repo.py docs check` |
| Research, experiments, tests or recorded observations | [Research/evidence policy](research-and-evidence.md) | Verify record provenance and status; no test is inferred |
| Branching, PRs and authorized integration | [Delivery guide](delivery.md) | Current Git/PR status; configured project checks |
| Resuming a complex lane | [Handoff guide](handoff.md) | Source revision and scoped verification evidence |

As actual modules appear, add one row for their owned code paths, canonical docs and targeted check. If separate domains need repeated specialized behavior, add a skill under [`.agents/skills/`](../../.agents/skills/) and a thin Claude loader.

Cross-cutting operational guides: [long-horizon plans](../../PLANS.md), [parallel-agent coordination](coordination.md), [agent smoke checks](agent-setup-validation.md), [trust boundaries](trust-boundaries.md), and [agent evaluation](agent-evaluation.md). Open these only when the task activates the concern.

Real module mappings can be registered in [areas.json](../../.repo/areas.json); see [commands](commands.md). Startup uses [START-HERE](../../START-HERE.md); routine implementation uses [definition of done](definition-of-done.md).
