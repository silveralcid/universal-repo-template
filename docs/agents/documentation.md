# Documentation authoring policy

**Owner:** documentation authority, maintenance, movement and selective reading, across providers.

Find the existing owner in [docs/INDEX](../INDEX.md), edit its smallest relevant section, and link rather than duplicate normative text. Put new depth beside its subject; keep entrypoints and routing files compact. The human README may be comprehensive but is not an agent's mandatory startup corpus.

## Status and location

CONFIRMED/accepted owner decisions belong in owning specifications, [decisions](../decisions/README.md) or [ADRs](../adr/README.md). PROPOSED, OPEN, DEFERRED, OBSERVED and SUPERSEDED stay distinct. [Research](../research/README.md), experiments, evidence and handoffs are not competing product specifications. Hypotheses and unknown-relevance findings remain valuable without becoming requirements.

## Move, split or retire

Preserve approved meaning, certainty, identifiers, dates, source attribution and unresolved questions. Keep one-hop redirects or explicit compatibility anchors for used historical links; update known backlinks and task routes in the same change. Don't create redirect chains or cycles. Never discard unique information merely to satisfy a context budget. Deduplicated content can be removed once its canonical owner and provenance are retained; material historical evidence can move to the archive.

Before inventing a new document, search the owner map and local records. A single coherent topic is a sensible split boundary; arbitrary line counts are not. Native provider adapters and generated catalogs are not authorities. Keep instructions in each provider loader as pointers only.

## Continuation and changes

Record consumed paths, relevant section IDs and exact source commit when a long/risky task needs them. The optional context snapshot stores SHA-256 of actual file bytes; it is not a Git blob hash or a semantic revision. A changed file needs affected-section inspection; unchanged unrelated docs need no reread. A route-only change updates navigation without automatically changing product intent.

## Validation

`python tools/repo.py docs check` checks configured requirements, routes, provider scaffold structure and common Markdown local links/fragments. It supports ATX headings, explicit HTML IDs, inline links/images and reference definitions; it is not a complete Markdown renderer, semantic conflict detector, network link checker or runtime test. Use explicit simple ASCII anchors for stable cross-document IDs. Complex Markdown constructs and generated site-specific anchors need manual review.

The checker traverses only root instruction files and documentation/provider roots. It skips dependency/build trees and symlinks. Module-local documentation elsewhere is checked only when linked as a target, not recursively linted; register critical area guidance under docs. `docs budget` reports estimated characters/4, not exact token counts.

## New project domains

When a real area earns dedicated documentation, run [the area scaffolder](../areas/README.md) instead of creating an isolated markdown file. It registers the canonical spec, agent pointer, indexed ownership and context route together. Generated content is explicitly DRAFT until an owner confirms its requirements. Update domain sections in the canonical area document; the agent guide stays short and links to its owner.

[Context budget warnings](../context/README.md#area-registration-and-budgets) recommend targeted splitting; they do not allow deletion of decisions, research provenance or historical evidence. Exceeding a threshold isn't itself a reason to create dozens of fragmented documents.
