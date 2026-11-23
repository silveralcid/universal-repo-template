# Engineering quality upgrade validation

**Status:** locally verified; hosted results belong to the draft PR's checks
**Date:** 2026-11-23
**Environment:** Linux, Python 3.12.14; local SQLite for boundary fixtures
**Base:** `cdc452f236af8eb498d79f86e3f38d40c6005796`
**Executor:** implementation coordinator, independent reviewer, two fresh-context task agents

## Audit and changes under test

The baseline already had a command registry, explicit execution, status meanings,
logs/receipts, path-based selection, documentation validation, context budgets,
source review and coding-agent evaluation guidance. Those mechanisms were reused.
[TESTING.md](../../engineering/TESTING.md) now owns test design and application
AI evaluation; [CODE-QUALITY.md](../../engineering/CODE-QUALITY.md) owns concise
implementation standards. Command semantics and completion statuses retain their
existing owners. No dependency, service, framework or CI privilege was added.

Two baseline runner defects were reproduced: a setup-only registry executed zero
checks yet returned PASS/0; a mixed selection could hide a changed area with no
checks behind another area's passing check. New regressions failed on the old
runner before the fixes. A receipt test also failed because selection metadata
was absent. The fixes preserve selection scope and make empty execution incomplete.

## Executed infrastructure checks

| Command or procedure | Observed result |
|---|---|
| Baseline `python3 tools/repo.py check --tests` in a detached base worktree | PASS, 87 tests |
| Updated `python3 tools/repo.py check --tests` | PASS, 94 tests; no skips |
| Independent execution of the seven added regression methods | PASS, seven methods |
| `python3 tools/repo.py docs check` | PASS, supported local links/fragments, routes and adapter/config structure |
| `python3 tools/repo.py docs budget --strict` | PASS, no budget increases |
| `git diff --check` | PASS |
| `python3 tools/repo.py verify run --name test --execute` in the blank template | Expected exit 2, INCOMPLETE, test NOT_CONFIGURED |

The seven added methods exercise empty selection, missing area checks (including
overlap), explicit selection and receipt scope, a real SQLite failure/recovery,
printed success with nonzero exit, an unknown command that must execute nothing,
and missing canonical policy files. The actual database case fails for a missing
table despite another successful check, then passes after creating its required
schema and row. Tests check process results and independently observed effects.

Context estimates remain under existing caps: AGENTS 1490/1500, implementation
4349/5000, review 4260/5000 and testing 4500/5000. These are characters/4 estimates,
not token billing. Task routes load procedural references only when applicable.

## Representative task trials

Two agents started with fresh conversation context, the repository's
`implement-task` skill, a bounded task directory, requirements and raw code/tests.
They were not given the intended diagnosis. Fixtures and raw reports remained in
ignored `.repo-local/quality-trials/`; they are synthetic local demonstrations,
not a reusable or human-validated benchmark. These trials used Python only.

| Required case | Independently stated expectation and observed evidence |
|---|---|
| Defect | Standard shipping costs 500 cents below 5000 and zero at/above 5000. The implementation used `>`. New fixed expected values failed at 5000 (`500 != 0`), then passed after changing to `>=`. |
| False-positive test | The original shipping test computed its expected value by calling the same function. It passed on the defect. The agent replaced it with requirement-derived constants and demonstrated the previously missed failure. |
| Integration failure | The inventory CLI must persist once in the selected SQLite file and fail honestly on unusable storage. Its mocked test passed while the CLI wrote to memory and swallowed errors. Three real subprocess/database tests failed on the original and passed after repairing the actual entrypoint. |
| Overengineering opportunity | The inventory proposal added adapters, a factory, async queue, broker and migration framework for possible future providers. The agent rejected those additions with a scope-based rationale and reused the existing local SQLite implementation. This is an observed engineering judgment, not a mechanically scored architectural guarantee. |

Shipping ran `python -B -m unittest discover -s . -p 'test_*.py' -v`: original
suite PASS (one method), replacement suite against original source FAIL (one
boundary failure), fixed suite PASS (three methods, 15 subcases, no skips).
Expedited fees and negative-input rejection were also checked.

Inventory ran `python -m unittest -v`: original mocked test PASS; three replacement
tests against original code FAIL; fixed suite PASS (three methods, no skips).
The final checks launched the real CLI, independently reopened the selected file,
checked an exact persisted value and duplicate handling, and rejected both an
unusable path and a trigger-induced write failure without emitting success.
No mocked boundary was used for those claims. Both agents stopped after scoped
acceptance; neither added dependencies or external services.

## Source identity and limitations

The reviewed and executed implementation files have these SHA-256 values:

| File | SHA-256 |
|---|---|
| `tools/repo_support/workflow.py` | `7017a3ef7090cce2ce51d64272504910d24f99cf52f81729aeb2f7f138f50ebd` |
| `tools/tests/test_repo_tool.py` | `5ee99a079d23c2541d54137d7a1cb710c77066c8b5d1c7c158b04f46ae309f3b` |
| `docs/engineering/TESTING.md` | `65a587763b09b81da79488e6d2af8e56a4a51365710aa0351ea3295a577ee0fd` |
| `docs/engineering/CODE-QUALITY.md` | `27a2418f0297087ef20d3a1cc62cadb13bc87c6c405e3be44317c25b7fa3539c` |

The reviewed-source manifest records the complete packaged file identities.
The draft PR records its exact head and hosted workflow outcomes separately.
An independent diff review found no blocking issue in the changed framework.

Mechanically checked: configuration, selection, exit outcomes, receipt scope,
static links/budgets and the listed regressions. Documented and review-dependent:
test-oracle independence, realistic fixtures, adequate coverage, human validation
of AI evaluation cases, subjective quality and real external connectivity.

No live LLM/provider integration, paid model calls, native Codex/Claude client
sessions, multi-stack application benchmark, production test, deployment or
human acceptance was performed. Node and Rust commands are documented examples.
A zero-exit vacuous test can still pass the runner; the shipping trial demonstrates
why independent review and sensitivity evidence remain necessary. Small successful
task trials do not establish universal agent reliability.
