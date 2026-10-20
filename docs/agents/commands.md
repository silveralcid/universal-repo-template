# Command registration and execution

**Owner:** `.repo/project.json` commands, `.repo/areas.json` scoped selection and verification runner behavior.

## Register actual commands, not aspirational aliases

Project schema 2 uses an object keyed by command name. Each value is `null` or this shape:

```json
{
  "argv": ["{python}", "-m", "unittest", "discover", "-s", "app_tests"],
  "cwd": ".",
  "timeout_seconds": 120,
  "mutates_external": false
}
```

This is an example, not an installed test framework. `{python}` resolves to the Python running the helper. Every other argument is literal. Set Node, Rust, engine, Java or other executables as appropriate. Do not put credentials in argv or configuration. No command interpolation, environment expansion, pipe, automatic shell wrapper or dependency installation is provided. A script executable can still do anything its account permits: **this is not a sandbox**.

Inspect package hooks and scripts before execution. On Windows, a `.cmd` executable can have OS-specific shell behavior; prefer an explicit reviewed executable invocation. Pipelines belong in a reviewed project script, not a string passed to the helper. Configure `cwd` using repository-relative forward-slash paths. Symlink and parent traversal paths are rejected. The caller's environment is inherited; use a restricted environment/account for untrusted work.

`setup` documents install/bootstrap and is excluded from verification execution. Run it separately after inspection and authorization. No deployment, CRM write, email send, production migration or other external mutation belongs in the verification registry.

## Plan before execution

```bash
python tools/repo.py verify plan
python tools/repo.py verify plan --name test
python tools/repo.py verify run --name test --execute
```

Without `--execute`, `run` prints the plan, runs nothing and exits 2. Unset commands stay NOT_CONFIGURED. A failing/blocked check returns 1; incomplete coverage with no failed check returns 2; only all selected configured checks passing returns 0. A successful selective run makes no claim about unselected checks.

Receipts and raw logs go to ignored `.repo-local/runs/<UTC-run-id>/`. The console prints only statuses and the receipt path, not raw output. Receipts record source before/after, exact argv, durations and log SHA-256. A dirty checkout is explicitly marked; the working-tree status hash identifies the status listing, **not all uncommitted contents**. For reproducible high-stakes evidence, commit or capture the actual changed files/patch checksum separately.

Commands are timeout-bounded. On POSIX the runner terminates the process group at timeout; on Windows it can guarantee termination only of the direct child. Inspect descendants and use a disposable workspace for potentially spawning tools. The runner does not cap log size or network traffic; choose bounded tests, storage limits and a real sandbox when needed.

## Area selection

`.repo/areas.json` starts empty. Register real areas like:

```json
{
  "schema_version": 1,
  "areas": [{
    "id": "workflow-core",
    "guide": "docs/agents/areas/workflow-core.md",
    "paths": ["packages/workflow-core/*"],
    "checks": ["test", "typecheck"]
  }]
}
```

Create the guide and actual commands before registering. Patterns use Python `fnmatchcase`: case-sensitive and `*` can cross `/`; they are not Gitignore semantics. `verify plan --path packages/workflow-core/src/jobs.ts` selects mapped checks. Unknown paths or no applicable selection fall back to all non-setup slots, not to zero tests. Mappings cannot prove dependency coverage; expand manually for shared contracts, root config, schemas and integration.

The helper is optional. Running a native project command directly is legitimate; record the evidence accurately.

## Automatic area registration

When a new real subsystem emerges, create the guide and canonical spec together, before touching unrelated global instructions:

```bash
python tools/repo.py area new --id workflow-core --title 'Workflow Core' --path 'packages/workflow-core/**' --check test
python tools/repo.py area list
python tools/repo.py context --topic area:workflow-core
python tools/repo.py docs budget --strict
```

This creates draft documents and adds mappings to `.repo/areas.json`, `docs/context/routes.json`, `docs/INDEX.md` and `docs/agents/README.md`. Existing documents are never silently replaced; a duplicate ID or unsafe path aborts. The new guide points to one area specification, not a second copy. You must still configure `test` in `.repo/project.json` before that slot can actually execute. `verify plan --path <file>` uses the registered paths as **hints**; path globs cannot prove transitive contract coverage.
