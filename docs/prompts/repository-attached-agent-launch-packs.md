# Repository-attached agent launch packs

Keep complete task instructions in reviewed repository files. Use a short chat launcher to direct each agent to its assigned file. This is a handoff convention, not permission to start sessions, modify protected branches, or deploy.

Follow the current [coordination rules](../agents/coordination.md), [delivery policy](../agents/delivery.md), and [prompt library](README.md). Project-specific instructions take precedence.

## Prepare the work

Inspect the repository, relevant branches, current work, and document ownership before assigning tasks. Use parallel agents only when the work can be divided without conflicting ownership. Give shared entrypoints, interfaces, and dependency files one integrator.

Write one complete prompt per lane using the [prompt skeleton](../templates/agent-launch-pack.md). Each prompt must identify the mission, verified starting ref, branch and worktree, exclusive files, dependencies, acceptance checks, handoff, and approval boundaries. Remove unresolved placeholders before calling a prompt ready.

Commit the prompt files to the appropriate branch and read them back from the remote. Confirm that each advertised path exists at the stated ref. Publishing instructions does not mean an agent has executed them.

## Present the launch choices

Provide links to the full instructions and a compact launcher. Where the interface supports it, use one labeled selector, one selection-dependent script preview, and a working copy action. Selecting another lane must change the actual file and branch references in the copied text, not merely the visible label.

Use accessible controls with keyboard support and clear labels. Do not display inert controls that imply functionality. A copied prompt is user-initiated dispatch, not a background execution service. If interactive controls are unavailable, use a small table of links and separately copyable launch instructions.

A generic example follows. Replace each placeholder with verified project values before delivery:

```text
In <owner>/<repository>, read the complete prompt at <path> on <verified-ref>. Use its assigned branch and separate worktree. Read the current repository rules and coordination record, implement the assigned work, run the required checks, and publish the requested handoff. Coordinate through the repository rather than asking the user to relay other agents' output. Do not merge or deploy without authorization.
```

## Coordinate execution

Once sessions are actually started, publish checkpoints, interface contracts, dependencies, and blockers through the repository's established collaboration channel. Do not claim background monitoring or continuous execution unless the runtime actually provides it. Keep independent work moving while documenting dependencies that cannot be resolved.

Distinguish instructions prepared, branches available, sessions started, changes published, tests run, and integration approved. Report the exact checks performed and any checks not run. The chat launcher is a pointer to complete instructions, never a substitute for them.

## Acceptance

Every launch option must have a readable remote prompt, matching branch and role, non-conflicting file ownership, explicit dependencies, and testable completion criteria. The copy action must reproduce the selected script exactly. Links must resolve at the advertised ref. Preparation must never be presented as completed engineering work or an approved deployment.

Use generic examples in reusable material. Keep private project names, account identifiers, historical coordination links, and personal preferences out of the shared template. Review exports using the [sharing guide](../engineering/SHARING.md).
