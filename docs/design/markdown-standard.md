# Markdown presentation guidelines

**Owner:** optional readability conventions for new design-facing Markdown. Repository-wide documentation authority remains [documentation policy](../agents/documentation.md), [docs index](../INDEX.md), and existing source owners.

Prefer one meaningful H1, descriptive headings, concise paragraphs, fenced code with language tags, and relative links to in-repository sources. Avoid decorative formatting and duplicate normative content. A single source of truth beats repeating a standard in every prompt or module.

Short, reviewable sentences and modest heading depth can improve diffs, but **do not require** front matter, a fixed sentence-per-line style, filename renames, maximum H3 depth, or wholesale reformatting of existing docs. Use only metadata a project actually maintains. Do not create a new docs linter that competes with the template's established validation without a reviewed adoption plan.

The template's \`python tools/repo.py docs check\` and \`docs budget --strict\` remain the canonical documentation checks. Any optional markdownlint or Prettier setup must be scoped and measured against existing files before it becomes blocking.

Project proposals, observations, tests and approved decisions still belong in their established owners, not in a visual-style document. Keep credentials, user data and raw logs out of shared Markdown.