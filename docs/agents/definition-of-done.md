# Definition of done

**Owner:** when an implementation may be described as complete. Apply proportionally to its scope.

## Implementation acceptance

The requested behavior exists; it is wired to the real application/workflow entrypoint; success and important failure paths are handled; relevant tests or manual observations support the claim; changed contracts and owning docs match; no unapproved external side effects occurred. A useful vertical slice must be runnable by the human from documented commands.

Distinguish **implemented**, **integrated**, **locally verified**, **human accepted**, **CI verified**, **released** and **deployed**. These are separate claims. A callable module without UI/job/entrypoint integration is not a delivered user feature. A placeholder, stub, mocked integration or skipped branch is not real connectivity.

## Required handoff

Give outcome, changed surfaces, startup/reproduction steps, exact checks and outcomes, remaining risks/limitations, source identity and next task. A small change can use the PR or final summary. Use a dated evidence record or handoff only when future reuse warrants it. Never leave critical state only in private model memory.

## Verification truth

- PASS: a named check actually succeeded on the identified source/environment.
- FAIL: the named check executed and failed.
- NOT RUN: no execution occurred; explain why.
- NOT CONFIGURED: the project has no registered check; this is not a pass.
- BLOCKED: an attempted or required check cannot proceed because a dependency, permission or timeout prevents it.
- INCONCLUSIVE: execution did not establish the claim.

Existing-red tests must be established from relevant baseline evidence, not guessed. Known-red status is not automatic permission to merge. Verification can be incomplete while a local implementation is delivered honestly; don't call it fully verified.

## Proportional quality

For changed code consider boundary/error tests, lifecycle cleanup, idempotency when applicable, types/schema validation, data migration and rollback, performance at representative scale, accessibility/input paths for user-facing work, and privacy/rights. These are applicability checks, not a mandate to implement every architecture pattern in a new project.
