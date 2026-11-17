# UX workflow and acceptance

**Owner:** the smallest repeatable procedure for UI-facing changes.

This adapts the uploaded bundle's five-step workflow and remains subordinate to [delivery](../agents/delivery.md) and [definition of done](../agents/definition-of-done.md). Do not create ceremonies or artifacts without a concrete benefit.

## Five steps

1. **Problem:** State who uses the feature, the pain or failure, frequency when known and one observable outcome worth shipping. Stop if there is no real problem.
2. **Flow:** Sketch the normal path and key alternatives using whichever notation is fastest. Identify unnecessary detours.
3. **States:** Before polishing layout, consider loading, empty/no records, empty/no matches, error/unreachable backend, typical loaded, unusually large/long content, read-only/permission denial, stale data and agent-run partial/failure states where applicable.
4. **Build:** Use existing architecture and components, then the applicable [UI](ui-standard.md), [UX](ux-standard.md), [data](data-display.md), and [agent surface](agent-surfaces.md) guidance. Deliver a working path before speculative polish.
5. **Verify:** Check representative phone/tablet/desktop widths (390, 1024 and 1920 CSS pixels are useful samples), light/dark if supported, keyboard and screen-reader semantics, contrast, long/empty states, and an actual failure mode. Validate permission/undo/URL/export behavior only when the feature requires it.

## Practical completion check

- The normal workflow works from its real entrypoint and makes meaningful progress.
- Important loading, error, empty, large-content and permission states have been observed or are honestly marked untested.
- At least one relevant failure/recovery case is verified, rather than inferred from code.
- Layout is usable at representative sizes without clipping, inaccessible controls or unrelated blank-space hacks.
- Focus order, labels, meaningful status, text contrast and reduced-motion behavior are considered proportionally.
- Data freshness, missing values, timezones and background-run status are truthful where relevant.
- Documentation reflects actual changes; meaningful deviations are recorded in the project's existing brief/decision owner.

For known users, observe one real workflow when uncertainty warrants it. Do not require user interviews for straightforward internal fixes. Adopt new standards incrementally in existing applications rather than undertaking an unrelated redesign.