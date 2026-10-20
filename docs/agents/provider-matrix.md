# Codex and Claude Code capability matrix

Native details were checked against official documentation on 2026-10-20; installed versions and managed settings can differ. See [sources](../reference/PROVIDER-SOURCES.md) and [smoke checks](agent-setup-validation.md).

| Concern | Codex | Claude Code |
|---|---|---|
| Shared guidance | Root and applicable nested AGENTS.md; overrides can take precedence | CLAUDE.md imports shared AGENTS.md; direct AGENTS support also exists in current clients |
| Scoped rules | Nested AGENTS discovery depends on working directory; inspect edited subtrees explicitly | Path-scoped `.claude/rules/` pointers |
| Project configuration | `.codex/config.toml`; trust and managed configuration affect loading | `.claude/settings.json`; local/global/managed settings can combine |
| Shared skills | `.agents/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` thin loaders opening canonical source |
| Optional specialists | `.codex/agents/*.toml` | `.claude/agents/*.md` |
| Researcher write restriction | Instructions only; parent sandbox/approval governs | Explicit allowlist omits shell, editing and MCP mutation tools |
| Setup proof | Parse + client version is not discovery proof | Parse + client version is not discovery proof |
| Tooling without local execution | Read-only guidance still useful; no invented test claims | Same |

This template configures only these two providers. No global model selection, provider API keys, MCP server, cloud environment, authentication, automatic hook or elevated permission preset is installed. Do not set CODEX_HOME to the repository merely to load project instructions: keep authentication in its normal user-managed location.

Native startup discovery can be version-dependent. Manual reading of START-HERE/AGENTS and the canonical skill is the documented fallback, not permission to invent another implementation. Instructions guide behavior; they are not a general security sandbox.
