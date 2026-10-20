# Evidence artifact manifest and retention

`docs/evidence/` holds **short summaries** with source revision, exact environment/test input, observed outcome and links. Raw traces/screenshots/profiles/logs/recordings/benchmark tables belong in ignored `artifacts/` or approved access-controlled storage. `.gitignore` does not back them up or secure them.

When evidence must survive a machine reset or agent handoff, use [artifact-manifest template](../templates/artifact-manifest.md) and record: artifact type/path or restricted locator, producing SHA, run ID, creation time, size, SHA-256 digest when practical, privacy class, retention owner/policy, reproduction command and deletion policy. Never put a sensitive presigned download URL into public Markdown.

Artifacts may be pruned when their evidence is superseded or no longer needed, provided accepted results retain enough provenance to be honestly reproduced or their unavailability is declared. Agent should not assume a local ignored artifact exists on another machine or in a cloud session.
