# Template v4.1 local validation

**Date:** 2026-10-20 (UTC)
**Scope:** Area and route scaffolding, reusable prompts, effort policy, static context budgets, existing helper behavior.
**Evidence status:** Local helper/static tests only; not Codex/Claude native execution or application correctness.

## Observed verification

- `python tools/repo.py check --tests`: PASS, **68 tests**, no failures/errors/skips in the working copy.
- `python tools/repo.py docs budget --strict`: PASS, all configured entrypoint/document/required-route estimates within their limits.
- `python tools/repo.py prompt list`: PASS, eight templates discoverable.
- New synthetic tests cover area registration, docs/route/test mapping, duplicate IDs, unsafe paths, missing owner markers, unknown check slots, budget status/strict exit, malformed budget configuration, and read-only prompt output.

## Not verified by these checks

Not a measured model cost reduction, application test result, live Codex or Claude Code skill discovery, production authorization, hosted GitHub Actions, external deployment, or semantic approval of generated draft area specifications. Budget estimates use characters divided by four, not exact model tokens or bills.

## Package and GitHub status

Package-level validation and remote GitHub state are recorded separately at handoff; this local record does not presume a push or a successful hosted CI job.
