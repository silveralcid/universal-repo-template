# Provider and tooling references

Checked 2026-10-20. These external references inform native adapter syntax, not project requirements. Recheck when clients change; account and managed settings still apply. No vendor content is copied into this template.

| Topic | Official source |
|---|---|
| Codex project configuration | [Configuration reference](https://developers.openai.com/codex/config-reference) |
| Codex instruction discovery | [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) |
| Codex custom specialists and parent permissions | [Subagents](https://developers.openai.com/codex/subagents) |
| Codex canonical skills | [Skills](https://developers.openai.com/codex/skills) |
| Claude instructions and AGENTS import compatibility | [Memory and instructions](https://code.claude.com/docs/en/memory) |
| Claude project and local settings | [Settings](https://code.claude.com/docs/en/settings) |
| Claude tool-restricted specialists | [Subagents](https://code.claude.com/docs/en/sub-agents) |
| Claude skill discovery | [Skills](https://code.claude.com/docs/en/skills) |
| GitHub workflow security | [Security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) |

Native client sessions, authentication, OS permission enforcement and cloud execution are not verified merely by these references or local template tests. Record actual results separately.

## Template CI provenance

The template-only workflow pins [actions/checkout v7.0.1 to commit 3d3c42e5aac5ba805825da76410c181273ba90b1](https://github.com/actions/checkout/commit/3d3c42e5aac5ba805825da76410c181273ba90b1), inspected 2026-10-20. Its permissions and untrusted-code handling follow [GitHub's secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use). A static local review does not claim this workflow has run in GitHub Actions.
