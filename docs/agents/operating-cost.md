# Model-agnostic context, delegation and cost policy

**Canonical owner:** task effort, model routing and context use. This optimizes **total effort to a correct, verifiable result**, not the smallest initial model call. The repository does not control Codex/Claude pricing, model entitlement, host approval policy or actual token billing. No model or provider is required.

## Work classification before choosing an agent/model

| Work | Default approach | Escalate when |
|---|---|---|
| Grep/search, read a few files, isolated rename, small format fix | Do directly in the current session. No subagent or detailed plan. | Symbols or requirements remain ambiguous, or blast radius broadens. |
| Scoped implementation with settled acceptance and tests | One implementing agent/session with the task-relevant area guide. Use the normal capable implementation tier available. | Several interacting systems, nondeterministic bug, or repeated incorrect attempts. |
| Broad design, semantic conflict, architecture, security-critical integration | Stronger reasoning/review and a compact explicit plan; isolate interfaces before spawning workers. | A human must decide intended behavior, or an irreversible external mutation is proposed. |
| Mechanical inventory, bounded evidence extraction and deterministic checks | Lightweight direct execution or a less expensive capable agent, if genuinely supported by the client. | Evidence is contradictory or needs cross-domain judgment. |
| Independent review | Separate focused review context of diff, acceptance and targeted evidence, not the whole project corpus. | Cross-domain or high-risk changes need deeper integration tests. |

Never choose a model just because a previous project used it. Prefer the available capability that consistently meets acceptance with the lowest **expected** combined discovery, implementation, testing and rework cost. Escalate after *specific evidence* of persistent uncertainty, not arbitrary attempts or blanket model upgrades. No cost figures are claimed without measured usage.

## The cheap, correct task loop

1. **Inspect live state:** Git branch/head, scope and actual existing work. A Ready packet narrows discovery; verify drift, don't start the investigation over.
2. **Route selectively:** `AGENTS.md` → one area guide → exact canonical section(s) and relevant source/tests. Use `python tools/repo.py context --topic area:<id>` when registered. `context` lists paths; it never concatenates entire document bodies.
3. **Choose effort:** tiny direct task, scoped feature, or long-risky effort. Use [reusable prompts](../prompts/README.md) only where structure removes ambiguity.
4. **Implement the smallest runnable slice** and run **narrow checks** during the loop. Run broader integration once near handoff, at release/merge boundaries or after meaningful changed interfaces.
5. **Report true evidence**, unrun checks, the source ref and next action; create a plan/handoff only if a new session benefits. Don't generate long transcripts or duplicate every test output in the repository.

## Subagent break-even rule

Delegate **only** if the task has independent scope, a concrete output contract, low file overlap, an integration owner and a benefit greater than the extra setup/review/merge context. One grep, reading several files, ordinary code trace, a single-file edit or Git bookkeeping does not justify a second agent. Parallel agents on the same state/authority usually create more work than they save; sequence dependent slices.

If a tool can't constrain a specialist to read-only, do not interpret the words "read-only" as a sandbox; use host permissions and review capabilities separately. Commit, PR, merge and external write permissions remain controlled by [delivery](delivery.md).

## Context budget and large files

- Short entrypoints and indexes are pointers, not manuals. The comprehensive human README is intentionally exempt from the per-file warning.
- Search `rg`/symbols/section IDs before opening long code or docs; read contiguous relevant ranges, not the whole file. Don't reload unchanged unrelated sections on continuation. `python tools/repo.py context diff --snapshot <file>` detects byte-level drift, not semantic drift.
- Run `python tools/repo.py docs budget` for estimated character÷4 sizes and `--strict` as a local/CI guard. Thresholds are in [context-budgets.json](../../.repo/context-budgets.json); missing/invalid config fails `docs check`.
- A large file warning asks whether a **real area boundary** exists. If so, split into one canonical owner per concern and retain stable links/section IDs. Never delete approved decisions or historical evidence to satisfy a budget. Exclude archives, raw logs and exploratory research from default agent packs.
- Do not require all prompt templates, all skill bodies, all prior research or all QA logs on every session. Agent imports, user messages, cached system context and subagent summaries may still have costs not represented here.

## Measuring whether routing saves money

Use comparable task families and record only **available measured** usage (calls, provider-reported tokens/price, retries, duration), plus correctness, regressions and useful accepted output. When those metrics aren't accessible, write "not measured". Do not report hypothetical savings as observed. Inspect [agent evaluation](agent-evaluation.md) for an evidence template and sampling risks.
