@AGENTS.md

# Claude Code adapter

Use the shared rules above. Claude-specific settings are in `.claude/settings.json`, area pointers in `.claude/rules/`, and optional specialists in `.claude/agents/`.

Canonical skills live under `.agents/skills/`. Their thin Claude loaders explicitly open that source; resolve its links from the canonical directory. Do not maintain a second workflow here.

Inspect instruction/skill discovery in the installed client using [native smoke validation](docs/agents/agent-setup-validation.md). No startup hook or automatic installation is enabled. The comprehensive README is reference; use START-HERE and task routes instead of preloading it.
