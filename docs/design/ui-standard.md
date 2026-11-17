# UI design standard

**Owner:** visual design, accessible components, responsive layout and optional shared theme for user-facing interfaces.

This is a recommended default for UI projects created from the framework-neutral template, not an authorization to replace a project's existing stack. Follow [UX behavior](ux-standard.md) and the [UI workflow](ux-sop.md). Existing architecture and accepted product decisions win over these preferences.

## Design principles

Prefer consistency, accessibility, mobile usability and low complexity. Reuse established components rather than making custom controls. Apply WCAG 2.2 AA requirements where relevant; measure actual results instead of assuming a component library guarantees accessibility.

Use a small, coherent set of color, type, spacing, radius and motion tokens. Provide light and dark schemes when appropriate. Avoid conveying status through color alone. Keep visible focus indicators, semantic controls and labels; design keyboard and touch access together.

For projects adopting Silver's default visual identity, [ui-theme](../../packages/ui-theme/README.md) supplies optional CSS tokens, minimal standalone HTML styles and a Mantine theme. The CSS and Mantine theme are currently manually coordinated; treat them as related sources requiring review, not automatically synchronized generated code.

## Choosing the stack

| Surface | First choice | Avoid |
| --- | --- | --- |
| Existing application | Its current accessible component system | Framework migration for appearance |
| New React dashboard | Mantine plus the optional ui-theme package | Building a component library |
| Single-file HTML / Apps Script | Semantic HTML with optional tokens/base CSS | A new build toolchain |
| Public site | Existing project stack, with tokens when useful | Prescribing Astro or Tailwind without a need |

Tabler icons, Roboto Flex, JetBrains Mono, TanStack Table and Mantine Charts are optional established choices, not mandatory dependencies. Import fonts legally and locally when feasible. Add a tool only for a demonstrated capability.

## Layout and typography

Design for realistic small, medium and wide viewports; the bundle's reference widths are 390, 1024 and 1920 CSS pixels. Prefer responsive content, wrapping toolbars, readable tables with horizontal overflow or equivalent mobile presentation, and an explicit overflow strategy. Avoid forcing every page into a full-height app shell or requiring cards where a table is more accessible.

The optional token profile uses a compact six-step type scale and 4px-based spacing. Tabular numerals help align metrics and currency. Component inventories are a starting set, not a cap: use an established accessible component when the task actually needs it.

## Interaction and visual states

Design and inspect loading, empty, error, loaded, unusually long, permission-limited and stale states as applicable. Use content-shaped skeletons where useful, meaningful error recovery, and reduced-motion preferences. Loading indicators and transitions should express real progress, not decoration.

Check contrast on the smallest and least prominent text, keyboard focus, icon-only labels, and touch targets. In the reference profile, text aims for at least 4.5:1 and non-text controls at least 3:1, with applicable WCAG exceptions. Record genuine project-specific deviations in its brief, rather than silently overriding established patterns.

**Source:** Adapted from the user-supplied UI/UX standards bundle; verify implementation claims against the actual application.