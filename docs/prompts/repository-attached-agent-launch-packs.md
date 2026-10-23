# Repository-attached agent launch packs — preferred delivery pattern

> **Status: CONFIRMED presentation preference (2026-10-23).** This is a reusable authoring and handoff convention, not a new execution authorization or a claim that a session was launched. It complements [parallel coordination](../agents/coordination.md), [delivery/merge approval](../agents/delivery.md), and the [reusable prompt library](README.md). Project-specific rules always win.

## Core rule: full prompts in GitHub, tiny launch scripts in chat

When the owner asks for multiple Claude, Codex or ChatGPT engineering sessions (especially 2+ concurrent agents and an integrator), **default to the same presentation pattern used for Harem King Forge Module 2 on 2026-10-23**:

1. **Inspect before assigning.** Verify live repository, correct integration parent/branch, existing agent rules, owner paths, in-flight PRs and exact source refs. Decide which lanes actually merit parallelism; do not manufacture N agents just to fill an arbitrary quota.
2. **Write the complete, execution-ready prompt for EACH lane as a tracked Markdown file on an appropriate GitHub feature/coordination branch.** Prefer `docs/<domain>/<feature>/prompts/<LANE>.md` or the repo's established prompt directory. Use a concise launch-pack index/charter for branch topology, file ownership, dependency signals and coordinator URL. Full prompt files, not the chat message, carry all the complex specifications.
3. **Commit/push and read back every actual remote file** before presenting it as ready. Record the branch/ref, exact SHA and relevant status. Open the appropriately scoped PR as required by this repository; publishing prompts **does not** launch agents or approve a merge.
4. **Return direct GitHub links + ONE compact interactive chat launcher**: dropdown of agent/model/role labels; a short selection-dependent script preview; and a working **Copy launch prompt** action. The script tells the selected session to read and **execute the COMPLETE prompt from the checked-in file**. The user copies one mini-script per session.
5. Make the first dropdown option the natural starting lane. If the chat interface cannot support a real dropdown or working copy action, use a compact table with links and short separately copyable scripts. Never display an inert mock dropdown/button or claim that clicking Copy runs an agent. A copied script is user-initiated dispatch, not execution.
6. After the user actually launches sessions, agents coordinate through GitHub issue/PR comments, checkpoints and published interfaces rather than asking the user to relay outputs. An agent runner without durable polling/notifications must not promise background monitoring or uninterrupted autonomous execution.

**Do NOT paste six 2,000-word prompts into chat when they can live in the repository.** Do not replace complete prompts with only miniature scripts or uncommitted local files either. This is a two-layer handoff: **GitHub = durable full instructions; chat = minimal ergonomic dispatcher**.

## Visual and interaction contract

The requested chat UI has this exact information order (the single-select control is real where supported):

> **For each session, the launch instruction is simple:**
>
> **Select the agent you're launching**
>
> `[ Sonnet R1 — Tracing                               ▾ ]`
>
> In `silveralcid/haremking`, read and execute the COMPLETE instructions in `docs/engineering/forge/prompts/M2-R1-TRACE.md`. Use the branch assigned in that file in a separate worktree. Read `REVERSE-STUDIO-EXECUTION.md` and the latest GitHub coordinator #668. Perform the actual engineering work autonomously, commit and push, coordinate via GitHub PRs/comments, and complete all feasible integration or handoff checks. Do not ask me to relay other agents' outputs. Begin immediately.
>
> **[Copy launch prompt]**

Rendering requirements:
- **One selector, not a stacked form.** Options are clearly distinguishable, e.g. `Sonnet R1 — Tracing`, `Sonnet R2 — Native Document`, `Opus — Integrator`; use the model the owner actually chose, but a label does not programmatically select the model.
- **One live script preview.** Changing the dropdown option changes the referenced repository prompt **path** (and relevant branch/role), not merely the label.
- **One working copy action.** It copies the exact visible mini-script of the selected option—never an unrelated prompt, raw JSON, a truncated snippet or an empty value.
- **Full prompts stay one click away** through nearby Markdown GitHub links; include the coordinator/charter once, not repeated paragraphs.
- **Compact by default.** One initial paragraph or table summarizing branch status, then the small selector; no redundant verbose launch scripts alongside it.
- **Exact status language.** `PROMPTS_COMMITTED`, `BRANCHES_READY`, `AGENTS_NOT_YET_STARTED`, `PR_OPEN`, `VERIFIED` mean different things. Do not present launch preparation as deployed/merged/running.
- **Responsive and accessible.** Meaningful selector label, readable text, keyboard-operable select and copy, selected value reflected in preview. Avoid purely decorative controls.

This describes the user-facing **presentation**; it does not prescribe any specific chat UI library or require the agent to develop an application or site for launch.

## Minimum durable launch-pack shape

Recommended feature footprint (adapt to the actual repository's canonical owner and conventions):

```text
docs/<domain>/<feature>/
  EXECUTION.md              # optional: actual agents, dependencies, parent/ref, statuses
  prompts/
    R1-<ROLE>.md             # full executable lane prompt
    R2-<ROLE>.md
    INTEGRATOR.md            # full integration/acceptance prompt
```

For each full prompt, use the [agent prompt skeleton](../templates/agent-launch-pack.md): a real mission; repository and pinned verified base; assigned role/model; exclusive branch/worktree/files; dependencies and where to discover current peer PRs; immediately useful independent work; explicit acceptance/tests/security/rights; exactly what to commit/push and where the PR goes; blocker/continuation rules; merge/deploy authority. Use one owner for shared files and public interfaces. Have the integrator own shared entrypoints, dependency/lockfile changes and cross-lane QA.

A mini-script should normally be 60–130 words and contain no unresolved template placeholders when delivered to the user:

```text
In <owner>/<repo>, read and execute the COMPLETE instructions in <path-to-full-prompt> at <verified-branch-or-ref>. Use the branch assigned there in its own worktree, read <shared-coordinator> and current repository instructions, and implement immediately. Commit/push, open or update the proper PR and post exact SHAs/tests/blockers through GitHub. Coordinate with the other lanes without requiring me to relay messages. Do not merge/deploy unless explicitly authorized.
```

## Example and provenance

The accepted six-agent reference is [Harem King Forge Module 2's committed prompts](https://github.com/silveralcid/haremking/tree/forge/reverse-studio-integration-20261023/docs/engineering/forge/prompts), its [execution charter](https://github.com/silveralcid/haremking/blob/forge/reverse-studio-integration-20261023/docs/engineering/forge/REVERSE-STUDIO-EXECUTION.md) and [coordinator handoff #668](https://github.com/silveralcid/haremking/issues/668#issuecomment-6371590846). These links document a **historical example**; inspect the live repository rather than assuming these branches/PRs remain current.

## Acceptance checklist

- [ ] Every visible dropdown option has a real remote Markdown file containing the **complete** corresponding prompt.
- [ ] Every option's label, prompt path and assigned branch match; integrator is its own option.
- [ ] Branch/owner/dependency collisions and current repository instructions are honored.
- [ ] An agent selection changes the short copied script; Copy copies exactly the current script.
- [ ] Full prompt files and coordinator are linked and can be fetched from the advertised ref.
- [ ] The status accurately distinguishes prepared prompts from started sessions, code changes, tested integration and approved merges.
- [ ] No user-relay dependency, invented tool ability, unauthorized merges or duplicate authority is introduced.
