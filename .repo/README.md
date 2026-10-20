# Repository metadata

`project.json` is the human-edited project configuration (schema 2). It stores project name/kind, explicit or auto integration branch, optional release branch and actual command definitions. `null` means not configured. It never stores credentials or current PR state.

`areas.json` is an optional list of real code areas, guide paths, path patterns and command names. Empty is valid. Use `python tools/repo.py area new` to generate the canonical draft spec, area guide, routing and owner index together. See [command registration](../docs/agents/commands.md).

`template-manifest.json` records the pristine template's file hashes for non-overwriting adoption. It is not a living project's configuration or a mandate to reverse customization. See [adoption](../docs/agents/adoption-and-upgrades.md).

Generated caches, context snapshots, logs and receipts belong in ignored `.repo-local/`, not beside this authored metadata.

`context-budgets.json` configures estimated chars/4 thresholds for compact entrypoints, scoped area guides and routes. `docs budget --strict` uses it as a local quality gate; it is not model-token billing.
