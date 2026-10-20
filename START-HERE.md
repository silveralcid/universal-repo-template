# Start here

**Goal:** give an agent a product/task description and start a verified first slice, not spend the session configuring a template.

## Human: one useful input

Open this folder in Codex or Claude Code after installing and signing in to your chosen client. Review the repository before granting it trust. Give the agent this prompt, replacing the bracketed goal:

```text
Read START-HERE.md and AGENTS.md. Use project-bootstrap, then implement-task.
Build: [the product or feature, intended user, and first useful outcome].
Use the existing stack when one exists. In a blank project, choose the smallest
sensible stack consistent with my constraints and record why. Do not add a
framework, database, service, or abstraction merely because the template has room.
This authorizes scoped local project scaffolding, implementation, tests, and
necessary project-local dependency setup after inspecting its scripts.
Use an isolated branch when Git is available. Preserve unrelated work.
Do not merge, deploy, spend money, contact users, or mutate external data.
Do not stop after planning: deliver one runnable, tested vertical slice unless
a material blocker prevents it. Record the blocker and keep independent work moving.
Report startup commands, what was built and connected, actual test results,
limitations, and the next useful slice. No invented results or unearned DONE status.
```

A sentence describing the outcome is enough to start discovery. A chosen stack and detailed spec are welcome but not required. Missing credentials are not permission to invent or commit them. Account authentication and OS/client permission prompts remain yours.

## Agent: startup sequence

Read [startup](docs/agents/startup.md), then only the relevant owners. The project brief is [BRIEF.md](docs/project/BRIEF.md); the owner map is [docs/INDEX.md](docs/INDEX.md). The comprehensive [README](README.md) is reference, not mandatory full-context loading.

1. Inspect the actual checkout, task, current instructions, stack manifests and working tree. Recognize a blank project versus an existing one.
2. Turn the user's task into a concise brief and the smallest testable outcome. Resolve low-risk implementation details yourself; escalate only material, irreversible ambiguity.
3. Inspect tool availability. Optional: `python tools/repo.py doctor`, then `python tools/repo.py context --topic bootstrap`.
4. In an existing project, reuse its architecture and commands. In an empty one, add only the stack needed for the requested outcome. Do not rewrite existing agent configuration wholesale.
5. Record actual setup/check commands in `.repo/project.json`. When a *real, separately owned module* appears, use `python tools/repo.py area new --id <slug> --path <glob> [--check test]` rather than inventing areas beforehand. See [area scaffolding](docs/areas/README.md).
6. Build the slice, connect its real entrypoint, run targeted checks, and explain how the human can reproduce it. Follow [definition of done](docs/agents/definition-of-done.md).

## Optional manual preparation

Python 3.11+ powers the helpers; it is not a requirement for the application. On Windows replace `python` with `py -3` when needed. On macOS/Linux, `python3` is commonly the command.

```bash
python tools/repo.py init --name "My Project" --branch main
python tools/repo.py check --tests
python tools/repo.py agents check --cli
```

Use the actual integration branch, not automatically `main`. `init` changes metadata only; it does not initialize Git or install anything. For an empty directory, `git init -b main` is an optional separate operation. An unknown remote must not block a useful local implementation.

## The first handoff must contain

A runnable first outcome or a precise blocker; entrypoint/startup commands; configured checks and their real results; outstanding product decisions; source/working-tree identity; and the next useful task. A docs-only green check is not proof that the new application works.

For repeat tasks, use exactly **one** appropriate template from [agent prompts](docs/prompts/README.md) (`python tools/repo.py prompt show implement`), not the entire prompt library. The [cost policy](docs/agents/operating-cost.md) discourages duplicate discovery, needless subagents and whole-corpus reads. Run `python tools/repo.py docs budget --strict` to spot oversized instructions; it does not measure actual billing.
