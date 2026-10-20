# Adopt or upgrade without destroying an existing repository

**Owner:** bringing this infrastructure into new or established projects. Repository writes still follow [delivery](delivery.md).

## New project

Extract the inner `universal-repo-template/` contents into your intended root, including hidden folders. Review configuration, set the brief, and follow [START-HERE](../../START-HERE.md). No source layout, framework or database is created until the requested project needs it.

## Established project

Work on a dedicated branch. Run the helper from a **pristine extracted template**, not a modified project:

```bash
python /path/to/template/tools/repo.py adopt --into /path/to/existing-project
```

This dry-run classifies bundled files ADD, SAME or CONFLICT using the bundled manifest. It makes no writes, deletes or installs. Source/destination must not overlap; symlink paths are rejected. If every target is compatible, `--apply` copies only missing files using exclusive creation and rechecks the plan immediately first. Any pre-existing conflicting file blocks all planned copying. A race or I/O failure during copying may leave already-added files; inspect the diff, never assume all-or-nothing transactionality.

Most real repositories have conflicts in README, AGENTS, gitignore or config. That's expected: compare and merge those changes manually by their owning sections. Do not replace the established instruction hierarchy, package manifest, test commands, model choice, MCP setup or permission rules wholesale. The helper deliberately does not attempt semantic policy merges or force overwrites. It never edits your global/home configuration or existing remotes.

## v3 to v4

Python helpers now require 3.11+ for real TOML parsing; no silent parser skip. Application commands move to schema 2 objects (`argv`, `cwd`, `timeout_seconds`) instead of shell strings; null stays unconfigured. Infrastructure tests move from root `tests/` to `tools/tests/`; update workflows and remove only the old template test, not your app tests. Preserve any current project metadata, command values and local settings. Add START-HERE and the new skill pointers. Review your changed canonical policies rather than generating duplicate versions.

## Ongoing upgrades

`.repo/template-manifest.json` fingerprints the pristine distribution, excluding itself. It is provenance for safe adoption, not a requirement that a living project remain identical to the template. Compare old template -> your customized project -> new template; keep local decisions and merge upstream fixes explicitly. No update service, automatic overwrite or mandatory upgrade check runs. Use a pristine ZIP for future adoption; a source mismatch is intentional refusal, not a reason to bypass it.
