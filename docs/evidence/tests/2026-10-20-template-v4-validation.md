# Template v4 validation

**Date:** 2026-10-20 (UTC)
**Status:** PASS for the local checks below; native agent execution and application correctness are not claimed.
**Scope:** template documentation, configuration structure, local helper behavior and distribution integrity.
**Source identity:** the exact distributed files are recorded in [the template SHA-256 manifest](../../../.repo/template-manifest.json). No Git commit or remote repository exists for this build.

## Environment

Linux; Python 3.13.5; Git 2.47.3. Helpers target Python 3.11+, but this run used 3.13.5. Dependencies: Python standard library and local Git only. Tests use disposable synthetic fixtures; no user project, customer data, credentials, dependency installation, paid API, model session or external service was used.

## Commands and observed results

| Check actually performed | Result | What it establishes |
|---|---|---|
| `python tools/repo.py check --tests` | PASS — 59 tests, zero failures/errors/skips | Mechanical infrastructure regressions, not application tests |
| The same command from a fresh ZIP extraction | PASS — 59 tests | Packaged files, not just a working directory, are usable |
| The same command after initializing an adopted fixture, adding app files and registering a synthetic command | PASS — 59 tests | Infrastructure checks continue to work after project development starts; the registered command was not executed |
| `python tools/repo.py agents check --cli` | Static PASS; both native clients NOT ON PATH | Native files parsed/checked; not native discovery or permission enforcement |
| `python tools/repo.py doctor` | No template configuration errors; application UNCONFIGURED | Blank project is reported honestly, not as runtime-ready |
| `python tools/repo.py context --topic bootstrap` | PASS; approximately 2,807 estimated tokens | Selective paths/reasons, no document-body concatenation; character/4 estimate |
| `python tools/repo.py verify plan --path unknown/first-file.ts` | Conservative all-check fallback; NOT CONFIGURED | Unknown areas cannot silently select no checks |
| `python tools/repo.py verify run --name test` without `--execute` | Exit 2; NOT EXECUTED; no local receipt or command side effect | Execution opt-in is required |
| Pristine adoption dry-run, apply and repeated apply | PASS | Dry-run writes nothing; clean add-only adoption is repeatable |
| `init` in an adopted temporary copy | PASS | Changes metadata, not application dependencies or source layout |
| ZIP CRC, entry paths and every distribution manifest hash | PASS | Archive consistency and content identity, not publisher authentication |

## Regression coverage

Tests include valid and broken file/fragment links; scoped and duplicate routes; missing skills; invalid TOML; command configuration; no implicit shell or execution; safe paths and symlink rejection; source-content snapshots including removed files and changed routes; knowledge discovery and cache drift; blank record creation and overwrite refusal; real subprocess success, failure, missing executables and timeout; unconfigured checks remaining incomplete; cached Git refs, detached/missing-base preflight and filename hygiene; non-overwriting adoption; and the CI entrypoint.

The fixture builder copies only helper Python files and constructs synthetic documents/configuration. It never clones the adopting project's app tree, dependencies, secrets, raw evidence or private research. A runnable-project compatibility check adds synthetic app files and a registered command, then confirms the full infrastructure suite still passes without executing that command.

## Explicitly NOT RUN / not proven

Codex and Claude Code were not installed on PATH, so no live skill discovery, custom-agent dispatch, model response or permission smoke session ran. Windows and macOS execution, Python 3.11/3.12, hosted GitHub Actions, external-storage retention, real application behavior, secret-content scanning and cloud deployment were not tested. Native setup must still be checked in the actual installed client using [the smoke guide](../../agents/agent-setup-validation.md).

Template checks do not prove semantic alignment, complete application test selection, read-only enforcement, licensing, security isolation or network safety. Hashes prove byte identity only. The execution runner requires trusted commands and is not a sandbox. No green template check should be reported as a passing application, native agent session or hosted CI run.
