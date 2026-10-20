---
name: docs-steward
description: Maintain canonical documentation ownership, stable links and safe archiving without duplicating rules or promoting unapproved research.
---

# Docs Steward

1. Locate the one existing canonical owner in docs/INDEX.md, then make the smallest appropriate edit. Read docs/agents/documentation.md.
2. If the content is research or observed test output, leave it in the proper non-canonical directory. Approval is required to change intended behavior or accepted decisions.
3. Update links, affected ownership maps, area guides, and context routes only when their routes changed. Preserve stable IDs, revision history and substantive status qualifiers.
4. Do not overwrite an accepted decision with newer unapproved prose or silently discard displaced information; archive or supersede with source and date.
5. Run `python tools/repo.py docs check`; report what it validates and what it does not. If Python is unavailable, inspect changed links manually and report the limitation.
