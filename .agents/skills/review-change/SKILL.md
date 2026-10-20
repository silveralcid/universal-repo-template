---
name: review-change
description: "Use for independent review of a diff or delivered implementation. Does not authorize edits or automatic reimplementation."
---

# review-change

Read actual changed code, acceptance and relevant owners, then inspect source-matched evidence. Follow docs/agents/definition-of-done.md. Focus on correctness, security, integration, regressions, scope/ownership drift and absent negative tests. Separate implemented versus integrated versus verified. Confirm any claimed failure on the relevant baseline before calling it inherited. Report concrete findings by severity with path, consequence, evidence and minimal remedy; no stylistic rewrite of correct code. State exact checks actually run and those not run. Review is read-only unless fixes are explicitly requested; do not approve or merge on behalf of the owner.
