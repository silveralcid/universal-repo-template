# Documentation ownership index

One **canonical owner per topic**. This is a pointer table, not a duplicate specification. Research, experiment notes, evidence, archives and generated indexes never become approved requirements by themselves.

| Topic | Canonical owner |
|---|---|
| Project purpose, scope, audience, success criteria | [Project brief](project/BRIEF.md) |
| Architectural boundaries and interface owners | [Architecture overview](architecture/OVERVIEW.md) |
| Shared Codex and Claude operating rules | [AGENTS.md](../AGENTS.md) |
| Codex-specific native configuration | [Codex setup](../.codex/README.md) |
| Claude Code-specific native configuration | [Claude setup](../.claude/README.md) |
| Reusable cross-provider agent workflows | [Skills index](../.agents/README.md) |
| Agent area routing | [Area router](agents/README.md) |
| Documentation creation, change and archival | [Documentation policy](agents/documentation.md) |
| Research maturity, experiment and evidence handling | [Research/evidence policy](agents/research-and-evidence.md) |
| Research topic library and buckets | [Research index](research/README.md) |
| Experiment lifecycle | [Experiments index](experiments/README.md) |
| Dated observations and test result categories | [Evidence index](evidence/README.md) |
| Task continuation record storage | [Handoff index](handoffs/README.md) |
| Branches, PRs, approvals and delivery | [Delivery](agents/delivery.md) |
| Continuing a paused task | [Handoffs](agents/handoff.md) |
| Verification and evidence interpretation | [Verification](engineering/VERIFICATION.md) |
| Security, privacy, secrets and rights | [Security](engineering/SECURITY.md) |
| Technical design decisions | [Architecture decision records](adr/README.md) |
| Business/product design decisions | [Decision log](decisions/README.md) |
| Runbooks for operational procedures | [Runbooks](runbooks/README.md) |
| Archive and supersession policy | [Archive](archive/README.md) |
| Local raw/generated run artifacts (ignored) | [Artifact policy](../artifacts/README.md) |
| Machine context routes | [Context router](context/README.md) |

## Add an owner

Introduce a new row only when new functionality genuinely needs a new canonical home. Add area guides and path-scoped rules when concrete code or content paths exist. Do not create competing authority because an agent wants a shorter explanation.

## Additional workflow owners

| Topic | Canonical owner |
|---|---|
| Long-horizon task plans and milestones | [Execution plans](../PLANS.md) |
| Parallel agents, worktree isolation, conflicts and dependencies | [Coordination](agents/coordination.md) |
| Untrusted inputs, prompt injection, agent tool security | [Trust boundaries](agents/trust-boundaries.md) |
| Codex/Claude setup and live validation | [Agent setup validation](agents/agent-setup-validation.md) |
| Agent harness evaluation rubric | [Agent evaluation](agents/agent-evaluation.md) |
| Codex vs Claude feature parity and loader matrix | [Provider matrix](agents/provider-matrix.md) |
| Optional cross-domain research navigation | [Research index](research/INDEX.md) |
| Raw evidence manifests and retention | [Artifact handling](evidence/ARTIFACTS.md) |
| Consequential failures and postmortems | [Incident records](incidents/README.md) |

## Additional operational owners

| Topic | Owner |
|---|---|

| First-session bootstrap and build transition | [Startup](agents/startup.md) |
| Completion and integration claims | [Definition of done](agents/definition-of-done.md) |
| Registered commands and scoped execution | [Command registration](agents/commands.md) |
| Knowledge search and consumed-context hashes | [Knowledge navigation](agents/knowledge-navigation.md) |
| Safe template adoption and upgrades | [Adoption](agents/adoption-and-upgrades.md) |
| Proportional context and work cost | [Operating cost](agents/operating-cost.md) |
| Optional local task contracts | [Task packets](tasks/README.md) |
| Cross-subsystem and unresolved contracts | [Contracts](contracts/README.md) |
| Native provider source references | [Provider references](reference/PROVIDER-SOURCES.md) |
