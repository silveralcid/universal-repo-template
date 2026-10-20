# Project area specifications

A project area represents one coherent domain with a single authoritative specification, narrow ownership and explicit boundaries. The blank template has no invented areas. Create one only when real work needs it:

```bash
python tools/repo.py area new --id workflow-core --title 'Workflow Core' --path 'packages/workflow-core/**' --check test
```

The command creates a **DRAFT**, not approved requirements. It also creates an agent area guide, registers the path/check map, adds a `area:workflow-core` context route and updates the two human indices. Only actual owner-approved requirements may be treated as canon.

Use cross-area contracts under `docs/contracts/` rather than duplicating standards in each area. For large specifications, split into files by real concerns and retain stable links. Never load all areas by default.
