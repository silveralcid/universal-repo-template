# Engineering code-quality standards

**Owner:** provider-neutral implementation and review standards. Apply to the
changed scope. [AGENTS.md](../../AGENTS.md) owns the core build philosophies;
[testing](TESTING.md) owns test design; [security](SECURITY.md) owns general
security and data-handling policy. Existing stack conventions remain authoritative.

## Before implementation

State the user-visible behavior, important failures and acceptance before coding.
Inspect existing architecture, callers, contracts and tooling. Reuse the nearest
appropriate capability. For a substantial new component, follow the proportional
[adopt, adapt, then build check](../agents/startup.md#research-and-reuse-gate).
Record only meaningful tradeoffs in the existing owner or ADR.

## Keep the change understandable

- Give each behavior and fact one clear owner. Prefer straightforward functions,
  modules and data flow over extra layers. Extract shared code for demonstrated
  repeated behavior, not superficial similarity or hypothetical future consumers.
- Use names that express domain intent and small cohesive boundaries. Follow the
  project's formatter, type system and lint rules. Explain non-obvious intent or
  constraints in comments; avoid narration of self-evident code.
- Make inputs, outputs and failure behavior explicit at public boundaries.
  Validate untrusted input and preserve compatibility unless a contract change
  is part of the task. Keep domain rules separate from unnecessary transport or
  provider coupling without building a speculative adapter framework.
- Use existing dependencies and platform capabilities first. Add a framework,
  service, agent or dependency only for a concrete need with acceptable licensing,
  maintenance, security and integration cost. Avoid unrelated cleanup.

## Preserve correctness through failure

Handle errors at the layer that can act on them. Preserve useful cause/context;
do not swallow exceptions or return a success-shaped default after failure.
Release files, connections and background work on success, error and cancellation.
Use bounded retries only for appropriate transient failures.

For durable writes, money or external effects, consider validation, atomicity,
duplicate requests, partial completion and recovery proportional to the risk.
Enforce permissions at a trusted boundary. Keep secrets and sensitive inputs out
of source and diagnostic output. Use measured bottlenecks or actual scale needs
to justify performance and concurrency complexity.

## Finish an integrated slice

Connect the changed behavior to its actual entrypoint and callers. Remove replaced
dead paths only within scope; do not leave a placeholder that resembles working
functionality. Keep contracts, setup commands and owning docs synchronized.

Review the diff for correctness, maintainability, data integrity and accidental
scope. Follow [TESTING.md](TESTING.md) for proportionate evidence and
[definition of done](../agents/definition-of-done.md) for completion. Explain
remaining tradeoffs and stop when the agreed acceptance conditions are met.
