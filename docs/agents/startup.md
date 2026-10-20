# Startup and first implementation

**Owner:** first-session orientation, project bootstrap and the transition to useful code. [Delivery](delivery.md) owns permissions; [definition of done](definition-of-done.md) owns completion.

## Detect the actual situation

Inspect the working directory, instructions, Git status, package/engine/workspace manifests, entrypoints, current tests and the user's requested outcome. `doctor` is an optional local report, not a remote freshness check. A repository containing only this template has no application yet. Existing code is never a blank-slate invitation.

In an established project, preserve its framework, source layout, dependency manager, test locations and instruction hierarchy unless migration was requested. If a supplied task packet already identifies valid scope/evidence, verify drift instead of restarting research. An unmerged spec ref can be read without merging its branch.

## Turn the request into a buildable slice

Fill the smallest relevant portion of [the project brief](../project/BRIEF.md): user, problem, initial outcome, constraints, acceptance, non-goals. Extract what is already in the prompt; don't ask for it again. Low-risk reversible choices can be assumptions with reasons. Paid integrations, data retention, access rights, public distribution and destructive behavior require appropriate owner decisions.

A blank project with a clear outcome authorizes a reasonable stack choice under the requested implementation. Explain that choice briefly and proceed. Choose local/mock boundaries for missing optional external systems only when they still satisfy the first-slice acceptance; label them and never pretend they are connected.

## Start building, not just planning

Use an isolated task branch when available. Without Git, report the missing version control and produce usable local files; bootstrap may initialize Git when authorized. No remote account is needed for local progress. New project dependencies may be installed locally after checking their purpose and install scripts; no global installs or new cloud resources by default.

Create a plan only for meaningful dependencies, long-running tasks or parallel work. Register actual setup/check commands in [project metadata](../../.repo/project.json) after the stack exists. Start with one end-to-end user action, not a large collection of unconnected back-end modules. Add an area guide only when a real subsystem warrants one.

## Stop conditions and recovery

Don't pursue repeated unchanged failing attempts. After a few attempts with no new evidence, isolate the hypothesis, gather a narrower observation or ask for the exact missing decision. Never use broader permissions to hide a missing dependency. Keep independent safe work moving.

Use [START-HERE](../../START-HERE.md)'s first-handoff requirements. Template checks can pass before application commands exist; report both states separately. Full [README](../../README.md) instructions are for humans and deeper lookup, not mandatory session context.
