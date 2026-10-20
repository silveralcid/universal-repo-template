# Knowledge navigation and context continuity

**Owner:** derived catalog/search and context snapshot behavior. [Documentation policy](documentation.md) owns authority.

## Discovery without a database

```bash
python tools/repo.py catalog build --write
python tools/repo.py catalog check
python tools/repo.py search "latency" --kind research
python tools/repo.py search "timeout" --kind evidence --limit 10
```

The generated `.repo-local/catalog.json` is ignored and disposable. It contains path, title, category, optional tags and content SHA-256 for authored records under research, experiments, evidence, decisions, ADRs, tasks, plans, handoffs and incidents. README/index/template files are not treated as findings. Nothing is sent to an API; no embedding/model is needed.

Search uses all query terms, case-insensitively, against bounded local text and returns up to three matching line excerpts. It searches current sanitized source records directly, so a stale cached index cannot hide a new finding. No fuzzy/semantic retrieval, image/PDF extraction, network research, secrets scanning or authority inference is claimed. Raw files in artifacts/scratch are never indexed. Keep sensitive data out of authored docs before using search.

## Context routes and snapshots

```bash
python tools/repo.py context list
python tools/repo.py context --topic implementation
python tools/repo.py context --topic implementation --snapshot .repo-local/context-first.json
python tools/repo.py context diff --snapshot .repo-local/context-first.json
```

Snapshots are exclusive-create to avoid overwriting another lane. Choose a new file for each baseline. They record the selected files' actual SHA-256, source HEAD and dirty/unknown state. The comparison names changed/missing files and newly/no-longer-routed owners. It does not decide whether a semantic requirement changed or whether code aligns. Read affected sections, then continue. For important cross-machine work, publish a sanitized source/section record in a handoff rather than relying on this local cache.

Keep stable topics in `docs/context/routes.json`; choose a single area guide per affected subsystem. Avoid one giant route that sends every agent to every policy and historical note.
