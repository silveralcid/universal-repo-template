# Verification workflow

**Owner:** executing the appropriate checks and locating their evidence.
[TESTING.md](TESTING.md) owns risk selection and test design;
[command registration](../agents/commands.md) owns configuration, selection,
exit codes and receipt semantics; [definition of done](../agents/definition-of-done.md)
owns completion and status meanings.

## Keep the claims separate

| Check | Establishes | Does not establish |
|---|---|---|
| `python tools/repo.py check --tests` | Template documentation, agent configuration and helper regression checks | Application behavior or real connectivity |
| Registered project checks | The selected native commands' observed results | Adequate assertions or unselected behavior |
| Actual integration/acceptance procedure | The exercised boundaries and outcomes in that environment | Untested providers, production state or human acceptance |

For documentation changes run `python tools/repo.py docs check`; keep compact
instructions within `python tools/repo.py docs budget --strict`. The existing
repository-health CI runs infrastructure checks. It does not discover a new
application's framework or configure that application's CI automatically.

## Register a project's real checks

After selecting the stack, edit `.repo/project.json` to invoke existing native
scripts and tests. Set applicable command slots to reviewed `argv` objects;
keep a required but unavailable check `null` and explain the gap. Omit genuinely
inapplicable slots and record why in project notes. No stack is preselected in
the template. Do not substitute `tools/tests` for application tests or add a
command that only prints success.

Example `commands.test` value for an existing Node project's `test:ci` script:

```json
{
  "argv": ["npm", "run", "test:ci"],
  "cwd": ".",
  "timeout_seconds": 120,
  "mutates_external": false
}
```

Use the actual project command. Examples for already existing suites include
`["{python}", "-m", "unittest", "discover", "-s", "app_tests", "-v"]`
or `["cargo", "test", "--locked"]`. These examples do not install a framework
or ensure tests were discovered. Register separate integration/smoke commands
when the project's acceptance needs them; use its real working directory and
reasonable timeout. Keep credentials out of the registry.

```bash
python tools/repo.py verify plan --name test
python tools/repo.py verify run --name test --execute
```

Inspect the plan and underlying scripts first. Select all checks required by
the changed behavior, including shared contracts and callers beyond an area
mapping. Native commands may also be run directly with equivalent evidence.
Configure the application's existing CI to install its reviewed stack and run
the same applicable commands; template health remains a separate result.

## Inspect and report results

Inspect native output for actual discovered/executed tests, unexpected skips,
suppressed errors and meaningful assertions. A receipt's process PASS is not an
assessment of test quality. Report exact source, environment, commands, result
and limits under the [testing evidence contract](TESTING.md#evidence-sufficient-for-handoff).
Check hosted workflow results for the actual PR head before claiming CI success.
Release/deploy verification additionally follows [delivery](../agents/delivery.md).

Receipts and raw logs belong in ignored `.repo-local/` or
[`artifacts/`](../../artifacts/README.md). Preserve a concise sanitized record in
[`docs/evidence/`](../evidence/README.md) only when future reuse warrants it.
[Research and evidence](../agents/research-and-evidence.md) owns storage and
authority distinctions; planned experiments are not executed test evidence.
