# Local raw artifacts (not committed)

Put generated logs, browser traces, screenshots, recordings, benchmark outputs, JSON/CSV dumps and temporary AI-agent output beneath this directory only when appropriately safe to store locally. `.gitignore` excludes **everything here except this README**.

Durable, sanitized, reviewable summaries belong in [`docs/evidence/`](../docs/evidence/README.md), [`docs/research/`](../docs/research/README.md), or [`docs/experiments/`](../docs/experiments/README.md). Never use an ignored artifact path as the sole long-term proof of an important decision or result. Handle sensitive or large data in approved access-controlled storage; ignoring Git does not encrypt the file.

Evidence to preserve across machines requires a sanitized [artifact manifest](../docs/evidence/ARTIFACTS.md) and approved storage; a Git-ignored file is local-only and may be lost.
