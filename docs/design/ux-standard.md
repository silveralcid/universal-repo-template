# UX behavior standard

**Owner:** navigation, forms, feedback, permissions and practical user-interface behavior. [UI appearance](ui-standard.md), [data formatting](data-display.md), and [agent surfaces](agent-surfaces.md) have their own owners.

## Navigation and lists

Give the common user task the shortest clear path. Keep navigation shallow where it improves comprehension, but do not split a coherent workflow merely to meet a fixed depth. Make important records directly reachable.

Preserve filters, sort, pagination, selected tabs and scroll position across navigation or reload where the framework supports it. Prefer shareable URLs for non-sensitive view state; never put secrets, private content or authorization tokens into query parameters.

Use pagination for work queues and auditable records, virtualization for genuinely large lists, and infinite scrolling mainly for feeds. Show result counts when known. Make active filters visible and easy to clear. Use sensible default sorting and keyboard-accessible bulk actions.

## Forms and irreversible actions

Use real labels and semantic controls. Show validation at a useful moment (often blur or submit), preserve values after errors, and explain how to correct them. Avoid disabling a submit control without a discoverable reason; do not prohibit disabled states when waiting, permission-limited, or otherwise necessary.

Separate destructive from primary actions. Prefer undo for truly reversible changes, and confirmation with scope and consequences for irreversible operations. Never imply an undo exists when recovery is not possible. Autosave drafts only when appropriate for the data and user's expectations.

## Feedback, latency and failure

Provide prompt feedback proportional to latency. Show real progress steps when possible; do not invent percentages. Keep unaffected controls usable. For slow tasks, allow background execution only if the application supports it. Optimistic updates are appropriate only where failure can be reconciled.

Async errors explain what failed and what can be done next. Preserve useful stale data with a timestamp when connection or refresh fails, clearly labeled stale. Distinguish empty because no data exists from empty because filters matched nothing.

Sentence case, verb-first action labels and useful recovery language are preferred. Avoid vague messages and decorative alerts.

## Permission, access and performance

Expose unauthorized or read-only state honestly without leaking data. Keyboard access must not depend on hover; Escape should dismiss the topmost applicable overlay. Respect browser back behavior and reduced motion.

Export filtered data where users need it and are authorized; ensure exported dates, numbers and labels are machine-readable. Do not make export or telemetry a universal requirement for every UI. If collecting analytics, log the minimum decision-useful information and exclude sensitive content. Performance budgets are project-specific acceptance targets, not universal hard limits.

Internationalization, offline operation and browser support are project decisions, never globally forbidden by this template.