# Lightweight, provider-neutral context routing

`routes.json` names **required and optional paths** for each task type and a rough token budget. It does not duplicate document bodies and is not itself a specification authority. `python tools/repo.py context --topic <topic>` prints just a routing report. Add a route only when a real recurring task needs it.

Example topics: `research`, `experiment`, `evidence`, `review`, `handoff`, `documentation`, `implementation`. Archives, raw artifacts, previous unrelated experiments and unvetted research are **never implicitly loaded**. Context estimates are approximate characters ÷ 4, not exact model tokens. [Canonical owner map](../INDEX.md) determines authority.

## Area registration and budgets

Run `python tools/repo.py area new --id <slug> --path 'path/**' [--check test]` to register one real area atomically across the guide, canonical specification, area map, source indexes, and a new `area:<slug>` required-context route. Read just that area when possible; don't pre-load every area route.

`python tools/repo.py docs budget` reports approximate per-file and per-route costs. `--strict` returns a nonzero exit for configured overruns; limits are in [context-budgets.json](../../.repo/context-budgets.json). It is **not** model billing data or exact tokenization. Split documents at coherent boundaries, preserve a canonical owner and retain source links; a size warning alone is not authorization to delete evidence.
