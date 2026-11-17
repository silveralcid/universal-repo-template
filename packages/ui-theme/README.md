# Optional ui-theme package

An **opt-in** CSS token set and Mantine v7 theme adapted from the uploaded UI/UX standards bundle. No UI stack is installed at the repository root and no application is automatically migrated to this theme.

## Use from the repository

For a standalone HTML artifact, copy or link `tokens.css`, then `base.css`. The latter intentionally styles basic HTML elements and should **not** be imported into a Mantine app.

For an existing Mantine v7 React project, install the package locally or from its eventual published registry version, then import `theme` with `MantineProvider`, and load `@mantine/core/styles.css` plus the `tokens.css` stylesheet. A local install can point at this package directory. The provided theme does not bundle Mantine, React or font binaries.

This package is **not published by this repository**. Do not instruct a new project to install `@silveralcid/ui-theme` from GitHub Packages until an actual release is verified.

## Maintenance

- CSS tokens are the visible source of the sample palette. `src/theme.ts` mirrors selected colors for Mantine. They do not auto-generate one another; inspect both when changing colors.
- The seed `#1F6E6A` is descriptive. No deterministic Material color-generation pipeline is configured.
- Theme CSS supports browser color preference and explicit `data-theme` or Mantine `data-mantine-color-scheme` for dark mode. Avoid contradictory attributes.
- Light/dark contrast should be rechecked after palette edits; the token sample alone does not guarantee accessibility of a complete application.
- Only add a publish workflow after a maintainer deliberately chooses a release process. Publishing or tag pushes are not configured here.
- The project must install dependencies locally or through a deliberate CI job; there is no root-level build/dependency requirement.

See the [UI standard](../../docs/design/ui-standard.md). Avoid wholesale restyling of existing projects.