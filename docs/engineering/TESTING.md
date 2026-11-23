# Risk-based testing SOP

**Owner:** test selection, trustworthy test design and application evaluation.
Use this for implementation and review. [Verification](VERIFICATION.md) owns the
execution workflow; [command registration](../agents/commands.md) owns runner
semantics; [definition of done](../agents/definition-of-done.md) owns completion
and status meanings. Read the AI section only for applications that use models,
agents or external tools.

## The task loop

1. **Define the claim.** Before changing code, state the observable outcome,
   acceptance examples and important failure behavior from the owning requirement
   or contract. Resolve material ambiguity. A short task/PR note is sufficient.
2. **Choose checks by risk.** Inspect existing tests, entrypoints, dependencies
   and affected callers. Reuse the project's tools. Map each material claim to a
   check and its expected result; identify boundaries that remain untested.
3. **Establish sensitivity.** For a defect, reproduce the failure when feasible.
   Add or adapt a regression that fails for that defect and passes for the fix.
   If baseline execution is unavailable, explain the substitute evidence.
4. **Implement and verify.** Run narrow checks while editing, then relevant
   integration and acceptance checks on the delivered source. Inspect results,
   failures, discovery counts and skips, not just the exit code.
5. **Report and stop.** Explain why the evidence supports each claim, disclose
   gaps, update affected owners and stop when acceptance is met. Broaden testing
   only for a concrete unresolved risk or an existing required gate.

| Changed risk | Suitable evidence, adapted to the actual project |
|---|---|
| Documentation or reversible presentation | Links/build/render or direct inspection; no ceremonial unit tests |
| Isolated behavior or defect | Focused behavioral tests for representative success, boundary and failure cases |
| Entry point, contract or dependency boundary | Component checks plus an actual call through the application boundary |
| Authentication, money, durable data or destructive operations | Negative authorization/data-integrity checks, transaction/retry/rollback cases and independent review proportional to consequences |
| Concurrency, performance or nondeterminism | Representative workload, controlled environment, repeated observations and explicit uncertainty |

No universal test-count or coverage quota applies. Coverage can reveal untested
paths; it does not establish useful assertions. A trivial reversible change may
need inspection rather than a new test. A consequential change may need several
layers of evidence.

## What makes a test trustworthy

- **Independent expectations:** derive expected results from a requirement,
  accepted example, protocol or independently checked calculation. Do not call
  the implementation to compute its own expected answer, repeat its algorithm,
  or approve generated snapshots without reviewing their meaning. If the test
  conflicts with intent, reconcile the owner before changing the expectation.
- **Observable behavior:** assert outputs, state transitions, persisted values,
  or externally visible effects. A nonempty response, mocked call count, import
  success or absence of an exception alone rarely proves the claimed behavior.
  Avoid assertions about private method order or incidental formatting.
- **Representative cases:** cover relevant ordinary, empty, malformed, boundary
  and failure inputs. Include denial, timeout, cancellation, partial completion
  and retry/idempotency only where the system supports or depends on them.
- **Realistic fixtures:** preserve contract shape, relationships, constraints
  and relevant scale using synthetic or approved sanitized data. Version fixture
  provenance and assumptions. An oversimplified fake must not silently change
  the real protocol's failure semantics.
- **Regression sensitivity:** show the test catches the original failure or a
  plausible controlled fault. For risky new tests, briefly break the relevant
  behavior in a disposable copy and confirm failure, then restore it. Do not
  install a mutation-testing framework without demonstrated value.
- **Reproducibility:** record source, command, environment and fixture identity.
  Pin relevant dependencies; control seeds, clocks, locale and test isolation
  where applicable. Clean up local state. A seed cannot make an external model
  or service deterministic. Preserve flaky failures and investigate them; retries
  must not erase the first failure or manufacture a pass.

## Integration and honest gaps

Exercise the real route, CLI, job, UI action or other entrypoint and check its
meaningful downstream result. Mocks are useful for isolated behavior and forced
failure paths; they cannot establish credentials, reachability, provider schema,
permissions or actual persistence. Label every substituted boundary.

Use disposable local services or an authorized sandbox for connectivity checks.
Record which real components ran, which were simulated and the observed result.
A local protocol fixture proves that local contract only. Missing access means
the external integration is unverified; it does not justify production writes
or a connectivity claim. Follow [security](SECURITY.md) and
[delivery](../agents/delivery.md) for those boundaries.

Ensure the project's native test command discovers the intended suite and fails
when required tests are absent. Inspect unexpected skips and disabled cases.
Do not suppress errors, weaken assertions, replace integration with mocks or
remove tests merely to obtain green output. A zero-exit command with no relevant
assertions is insufficient evidence, even when the runner reports process PASS.

## Applications using LLMs, agents or tools

Use the same risk-based loop, plus a small versioned evaluation set grounded in
real intended tasks. Have a human validate the cases, expected outcomes and
failure severity before calling it a validated benchmark. Generated candidates
and an agent's own labels are provisional. Separate development cases from
held-out checks when tuning prompts or policies could overfit the examples.

Prefer deterministic assertions on schemas, required facts, tool selection and
arguments, authorization, state changes, allowed destinations, budgets and stop
conditions. Include representative normal requests, ambiguous or invalid input,
untrusted instructions, denied actions and tool failures. Check observable
completion against system state; a model saying "done" is not evidence of an
executed action. For write-capable tools, exercise duplicate/partial failures
and enforce authorization outside the model where consequences warrant it.

Keep fast model/tool stubs for reproducible component tests and clearly separate
authorized live model/connector trials. Record dataset and prompt versions,
model identifier when known, parameters, tool versions, environment, sanitized
traces, actual latency/cost when available and per-case outcomes. Repeat variable
cases enough to assess the specific risk; disclose sample size and instability.
Do not claim reliability across unseen tasks or providers from a small sample.

Use human review for subjective quality. An LLM judge is optional advisory
evidence: calibrate it against human labels and inspect disagreements. It must
not be the sole gate for correctness, safety or permission to take an action.
Evaluation of the *coding agent's workflow* belongs separately in
[agent evaluation](../agents/agent-evaluation.md).

## Evidence sufficient for handoff

For each material claim give the expectation's source, actual command or manual
procedure, source/environment identity, observed result, why it is sensitive to
the failure, and what it does not test. Link logs or receipts after sanitization;
use the [test-report template](../templates/test-report.md) only when a durable
record adds value. Report existing failures from baseline evidence and disclose
unrun, unconfigured, blocked, skipped and inconclusive work explicitly.

The helper can check registration, selection, process outcomes and receipts. It
cannot prove that assertions are meaningful, fixtures are realistic, integrations
are real or an agent obeyed this SOP. Those claims require task-specific evidence
and review.
