# Claude Code project setup

[`CLAUDE.md`](../CLAUDE.md) imports the shared [`AGENTS.md`](../AGENTS.md) once. `.claude/settings.json` is strict JSON; it only denies reading a few common credential file paths. **Text instructions and deny rules are not a data-leak proof**, including via alternate paths, shell commands, or external tools; keep secrets out of the repository.

- [`agents/`](agents/) supplies two research/review specialists; their descriptions are task triggers, not a requirement to delegate routine work.
- [`skills/`](skills/) contains slim loaders of the canonical `.agents/skills` workflows. A loader must open its referenced source before proceeding.
- [`rules/`](rules/) contains path-filtered references to documentation policy. Rules without `paths:` would load every session.
- `hooks/` is an unconfigured extension point. No session startup, auto-format, network or merge hook runs from this template.
- Personal choices and local permissions belong in `.claude/settings.local.json`, which the template ignores.

Start Claude Code at the repository root. Use `/status`, `/agents`, and `/doctor prompt-audit` if supported to inspect configuration. Claude's AGENTS.md behavior varies by version and instruction-file settings; the explicit `@AGENTS.md` import is retained for reliable shared guidance.

## How to invoke native helpers

Use `/project-bootstrap`, `/implement-task`, or `/review-change` for first-build, implementation, and review workflows. Use `/agents` to see `research-scout` and `verification-reviewer`, or ask Claude to delegate that specific bounded task. Invoke reusable skills via `/research-scout`, `/evidence-reporter`, `/docs-steward`, or `/work-handoff` when the procedure fits. Project native skills are committed so cloud code sessions cloning this repo can read them; this does not install plugins on your account.

Research and verification roles now use **read-only tool allowlists** without shell or mutation tools; they therefore cannot run tests. For actual settings and skill invocation, perform the [native smoke protocol](../docs/agents/agent-setup-validation.md) in your installed Claude version.
