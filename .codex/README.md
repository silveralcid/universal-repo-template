# Codex project setup

Project entrypoint: [`AGENTS.md`](../AGENTS.md). Codex loads repository instructions from `AGENTS.md` (including narrower files added to actual modules later).

- [`config.toml`](config.toml) is a **trusted-project-only** Codex configuration layer. It configures a modest subagent cap but chooses no model, provider, permissions, MCP servers or profiles. Your user-level settings remain yours.
- [`agents/`](agents/) contains usable narrow research and verification custom subagents. Ask Codex to spawn them when tasks are independently useful; they do **not** have their own sandbox/approval policy and inherit the parent session's permissions.
- `rules/` is reserved for project-specific **execution-policy** `.rules` files. It is not a duplicate of Claude's Markdown rules and is intentionally empty until a concrete need arises.
- The canonical skills are in [`.agents/skills/`](../.agents/skills/). Add a focused skill when a repeated workflow justifies it, not one per speculative feature.

The template does not log in, install Codex, grant API access, enable MCP servers, or run hooks. Start Codex at the repository root, then confirm `/status` and project trust in your installed client.

## How to invoke native helpers

Ask Codex to use `research_scout` to explore an uncertain topic, or `verification_reviewer` to inspect an implementation/test claim. Only delegate when isolated exploration or review is worth the extra context; neither role pins a specific model. For an explicit reusable procedure, reference the canonical skill by name (for example, `research-scout` or `evidence-reporter`).

A configuration file that parses successfully is **not** proof Codex loaded it. Run [`agents check`](../docs/agents/agent-setup-validation.md) then verify in an actual trusted Codex session. Custom agents cannot override the parent's approval/sandbox policy; set parent permissions before delegation.
