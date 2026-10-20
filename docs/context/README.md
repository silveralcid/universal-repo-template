# Lightweight, provider-neutral context routing

`routes.json` names **required and optional paths** for each task type and a rough token budget. It does not duplicate document bodies and is not itself a specification authority. `python tools/repo.py context --topic <topic>` prints just a routing report. Add a route only when a real recurring task needs it.

Example topics: `research`, `experiment`, `evidence`, `review`, `handoff`, `documentation`, `implementation`. Archives, raw artifacts, previous unrelated experiments and unvetted research are **never implicitly loaded**. Context estimates are approximate characters ÷ 4, not exact model tokens. [Canonical owner map](../INDEX.md) determines authority.
