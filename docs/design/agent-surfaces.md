# Agent and long-running UI surfaces

**Owner:** visibility, provenance, authorization, status and recovery for background jobs, scheduled runs, agents and automated pipelines.

The user should be able to determine what happened, why it happened, and how to review, correct or repeat it without reading private logs.

## Provenance and approval

Distinguish human-created, machine-generated, and human-edited output when it matters. Link generated artifacts to the originating run, preserving meaningful edits and timestamps.

For actions with external effects, display the actual proposed action or artifact and obtain approval unless the owner has explicitly authorized that specific unattended behavior. Approval must reflect permissions and any revocation/expiry rules. Provide edit/reject options where useful. Do not silently turn a reviewable proposal into an executed action.

## Progress and run history

Show the current step, elapsed time, meaningful counts, completed/skipped work, outputs and next required human action. Avoid invented percentage completion. Stream only when partial results are useful and not misleading.

Distinguish queued, running, succeeded, partial, failed, blocked, cancelled and nothing-to-do when those states exist. A run that did not execute is not the same as one that executed and found no work.

## Failures and uncertainty

A failed run identifies the failing step, what was affected, whether any external change was committed, and safe retry/resume choices. Escalate repeated failures rather than hiding them behind success banners.

Expose relevant uncertainty close to probabilistic outputs. Do not invent precise confidence numbers; use calibrated scores only when calibration evidence exists, or qualitative review categories with documented meaning.

## Audit and privacy

Keep sufficient action history for the project's audit and troubleshooting needs, accessible from the UI when authorized. Record actor, time, reference to inputs, action and outcome. Redact secrets, personal data, and sensitive payloads; do not indiscriminately log raw prompts or customer content. Retention must follow actual project policy, not a universal fixed duration.