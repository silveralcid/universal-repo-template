# Delivery and approval policy

**Owner:** Git branches, PRs, integration, external writes, handoffs, and reporting. Provider-neutral; no assumption that the default branch is called `main` or `dev`.

## Permission model

- Questions, analyses, recommendations and research: **read-only**, unless the request explicitly authorizes a write.
- Implementation: authorize necessary scoped local edits, tests, project-local dependency setup after inspecting scripts, local commits, and a proposed **draft PR** if repository and GitHub access exist. It does **not** authorize global installation, new paid services, merging, deployment, external/production database writes, mailing customers or other operational side effects. Work within an application's local test database is distinct from mutating an external production system.
- Merge, release, production deploy, destructive changes and external mutations: require explicit approval with named targets. Never force-push or rewrite another lane's history.

## Branching

1. Inspect current `git` and GitHub state. Resolve the integration target from `.repo/project.json` if explicit; otherwise inspect `origin/HEAD`. **Never infer integration from the current feature branch.** If unavailable, surface the decision before targeting a PR.
2. Branch from the authorized, fresh integration ref or an explicitly approved parent/integration branch. Never write to a protected shared branch as a substitute for a PR.
3. For independent work, prefer small changes and nonoverlapping source ownership. For parallel dependent lanes, declare the parent branch, dependency order, and integration owner before opening child PRs.
4. Verify the PR head and base before merging an authorized batch. Re-run needed checks when the tested head changes. Keep incompatible or blocked work visible rather than manufacturing a green merge.

## Quality ladder

- During edits: the *narrowest relevant checks*.
- Before handoff/PR: configured lint/types/tests/docs checks appropriate to the changed surfaces; report checks not run.
- Merge boundary: integration/acceptance/security checks and real runtime checks when applicable, separately from docs-only checks.
- Post-release: production observability/rollback only for projects that configure them.

## Handoff report

State: outcome, scope in/out, files changed, evidence and source ref, narrow tests **actually run**, remaining risks, PR or local diff, dependencies, and next action. Use [the handoff guide](handoff.md) for multi-session changes. Status must be derived from live git/PR state, not a manually maintained branch ledger.

## GitHub metadata caveat

GitHub automatically chooses the PR template from the repository's **default branch**. If the integration branch differs, keep the template installed on the default branch as well; the workflow must not silently assume a PR to `dev` automatically uses a template that exists only on `dev`.

Cross-lane work follows [coordination](coordination.md). All external inputs must respect [trust boundaries](trust-boundaries.md). For a long task, link the single [execution plan](../../PLANS.md).
