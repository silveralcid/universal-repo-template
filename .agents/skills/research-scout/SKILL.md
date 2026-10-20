---
name: research-scout
description: Investigate speculative, cross-domain, external, loosely relevant, or unresolved questions and produce sourced non-canonical research records.
---

# Research Scout

1. Identify the question, current repository owners, and why the topic might matter (or why relevance is unknown). Avoid searching all docs by default.
2. Collect traceable primary sources when possible. Record source URL/ref, retrieval or observation date, applicable version, and limits. Check whether the source is licensed for reuse; do not copy third-party code or copyrighted text wholesale.
3. Separate OBSERVED evidence, INFERENCE, HYPOTHESIS, PROPOSED action, and UNKNOWN. Include counter-evidence or a falsification test.
4. Choose `docs/research/inbox/` for raw leads, `exploratory/` for uncertain applicability, `candidates/` for plausible relevance, or `validated/` for substantiated findings. Even validated research stays non-canonical until explicitly adopted by the owner.
5. For a requested saved record, use `python tools/repo.py new research --slug <slug> --bucket exploratory` or the research template. Otherwise return a concise research note without mutating the repo.
6. Link an explicitly approved project decision into its one owning ADR/decision/spec, rather than copying the study into `AGENTS.md` or design canon. Observe docs/agents/research-and-evidence.md.
