# Research library — including ideas of uncertain relevance

This is **not** the implementation specification. Research can be tangential, future-looking, external, contradictory, or eventually discarded. Preserve why it was collected without forcing it onto the current roadmap. The owner of research status/handling is [research and evidence policy](../agents/research-and-evidence.md).

| Bucket | Use |
|---|---|
| [`inbox/`](inbox/) | Unprocessed links, notes and unanswered questions |
| [`exploratory/`](exploratory/) | Investigation with unknown or ambiguous project relevance |
| [`candidates/`](candidates/) | Potential future fit; merits further testing |
| [`validated/`](validated/) | Findings with credible direct evidence; still not approved scope |
| [`archive/`](archive/) | Superseded, rejected or deliberately parked research |

Every substantive study should include sources, source dates, retrieval method, alternatives, confidence, applicability, copyright/data restrictions and the next decision (or "none"). For a blank record run `python tools/repo.py new research --slug <topic> --bucket exploratory`.

For high-value studies spanning projects, use the [optional navigation index](INDEX.md) and mark revalidation triggers. Unrelated but useful ideas may stay exploratory indefinitely.
