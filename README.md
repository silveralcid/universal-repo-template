# Project starter

A framework-neutral starting point for AI-assisted development. It provides shared agent instructions, focused documentation, local verification helpers, and reusable task prompts without selecting an application stack or paid service.

## Start here

Extract the contents of `project-starter/`, including hidden folders, into a new project directory. Review the files before granting an agent access. Follow [START-HERE](START-HERE.md), write the project brief, and choose the smallest useful first implementation.

Python 3.11 or later is required for the helper commands. The documentation can be used without Python. The helpers use the Python standard library; Git is needed only for Git-specific checks.

```sh
python tools/repo.py check --tests
python tools/repo.py docs budget --strict
python tools/repo.py doctor
python tools/repo.py context --topic bootstrap
```

`doctor` distinguishes missing project configuration from actual runtime readiness. Template tests are not application tests and do not demonstrate that a native agent client works.

## Configure a project

```sh
python tools/repo.py init --name "Example project" --kind application --branch main
```

Use the project's real integration branch. Fill in [the brief](docs/project/BRIEF.md) and register reviewed application commands in `.repo/project.json`. An unset command is not a passing check. Configured commands run only when execution is explicitly requested:

```sh
python tools/repo.py verify plan
python tools/repo.py verify run --name test --execute
```

Commands use argument arrays rather than an implicit shell. They still execute with the local process's permissions; the helper is not a sandbox. Do not register commands from an untrusted source.

## Working conventions

Keep each decision in one owning document and link to it from relevant guidance. Load only the context needed for the task. Record observed evidence separately from proposals and untested assumptions. Keep credentials, raw logs, customer data, and local machine settings out of shared documentation.

The main navigation points are:

| Purpose | Entry point |
|---|---|
| Shared agent rules | [AGENTS.md](AGENTS.md) |
| Documentation navigation | [Documentation index](docs/INDEX.md) |
| Existing-project adoption | [Adoption guide](docs/agents/adoption-and-upgrades.md) |
| Task prompt library | [Prompts](docs/prompts/README.md) |
| Engineering and test design | [Code quality](docs/engineering/CODE-QUALITY.md) and [testing SOP](docs/engineering/TESTING.md) |
| Verification and delivery | [Verification](docs/engineering/VERIFICATION.md) and [delivery](docs/agents/delivery.md) |
| Agent configuration | [Provider adapters](docs/agents/provider-matrix.md) |
| Security and trust | [Security](docs/engineering/SECURITY.md) and [trust boundaries](docs/agents/trust-boundaries.md) |
| Source distribution | [Sharing guide](docs/engineering/SHARING.md) |

Useful local commands include:

```sh
python tools/repo.py prompt list
python tools/repo.py area list
python tools/repo.py context --topic implementation
python tools/repo.py new research --slug example-question
python tools/repo.py catalog build
python tools/repo.py search "example question"
python tools/repo.py branch check
python tools/repo.py hygiene
```

The documentation describes area registration, context snapshots, handoffs, evidence records, and optional coordination workflows. Research does not authorize implementation. A prepared prompt does not mean an agent was started. A successful documentation check does not mean an application was delivered.

## Existing repositories

Preview adoption before writing any files:

```sh
python tools/repo.py adopt --into ../existing-project
```

Review the plan, then add `--apply` only when appropriate. Adoption is additive and refuses conflicting overwrites. Preserve existing application architecture, instructions, and unrelated work.

## Verification

Run `python tools/repo.py check --tests` for the infrastructure tests in `tools/tests`. Run the project's own configured checks separately. Static adapter checks do not verify client authentication, client discovery, operating-system permissions, cloud execution, or deployment.

The included workflow uses read-only repository permissions. It does not grant permission to run untrusted code with secrets or on a privileged persistent runner. No automatic deployment, paid API call, global installation, or remote Git mutation is configured by this package.

## Sharing

Use the reviewed-file exporter rather than copying a working directory:

```sh
python tools/export_source.py --output ../project-starter.zip
```

The exporter excludes Git history and local extras, verifies the package manifest, and normalizes archive metadata. An optional external denylist can check project-specific identifiers without storing them in the repository. See [the sharing guide](docs/engineering/SHARING.md).

**Removing identifiers and archive metadata does not make source code anonymous.** Matching code, distinctive prose, existing public copies, repository ownership, commit history, and the delivery channel can still identify its origin.

## Reuse

Choose and add an appropriate license before offering a reusable public project. No license grant is implied by this document. Preserve required third-party notices and dependency provenance.
