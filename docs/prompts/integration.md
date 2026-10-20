# Prompt — dependency-aware integration

Follow `AGENTS.md` and `docs/agents/coordination.md` / `docs/agents/delivery.md`.

**Integration target (explicit):** [TARGET]
**Candidate branches/PRs:** [CANDIDATES]
**Constraints/approval:** [CONSTRAINTS]

Fetch current source/PR state and verify head SHAs; do not rely on old handoffs. Build a dependency order, identify write-owner collisions and competing implementations, and inspect actual changes. For clean candidates, plan isolated staging and the smallest applicable verification per area. For conflicts, distinguish mechanical reconciliation from unresolved semantics; never silently discard an authority or another lane's work. Do not force-push or rewrite a contributor's history.

Give a concise integrated status with READY / HOLD / BLOCKED, real checks, source SHAs and exact next actions. Open or update an integration PR if authorized. **Only merge when owner permission explicitly names the destination and scope**; otherwise hand back the reviewed PRs. Preserve work on blocked lanes and continue independent candidates.
