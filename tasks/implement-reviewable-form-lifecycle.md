---
type: Task
title: Implement reviewable standalone form lifecycle
priority: P0
assignee: Codex
description: >-
  Add individual recommendation decisions, restorable draft revisions, and
  readiness/export gating to the standalone form workbench.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-28T01:57:49.264Z'
---
# Outcome

Turn the standalone workbench's agent-authored happy path into a controlled, resumable review workflow without coupling authoring to the renderer or SGG.

# Acceptance criteria

- A reviewer can accept, reject, or defer individual agent recommendations instead of accepting the entire package at once.
- Review decisions preserve the recommendation evidence and decision attribution without converting proposed semantic mappings into reviewed mappings.
- Drafts and their review history can be serialized, restored, and verified through a versioned consumer-neutral contract.
- The UI shows a readiness gate that distinguishes working draft, ready for human review, and target-export eligibility.
- Export operates on the compiled portable package through an edge adapter; the authoring workspace does not import SGG code.
- Tests cover every new behavior and enforce the existing package boundaries.

# Delivery boundary

Implement the lifecycle and UI orchestration in the standalone workbench. Do not change `grants-form-spec`, CommonGrants, the Grants Standard, or Simpler runtime behavior in this slice.

# Result

Merged [grants-form-workbench PR #47](https://github.com/mikec-ai/grants-form-workbench/pull/47) at `3aa3cb580777f93ae3433d70e12848ce0841b08d`.

- Added versioned `portable-form-authoring-review-session/v1` lifecycle records with exact recommendation packages, current decisions, and immutable attributed revision history.
- Added individual accept, reject-with-correction, and defer controls. Implementation acceptance preserves proposed semantic-review state and does not change coverage.
- Added injected persistence plus automatic local save and resume in the standalone composer.
- Added working-draft, ready-for-human-review, and export-eligible gates.
- Added neutral portable-package and decision-record downloads. SGG projection remains at the separate adapter/CLI edge rather than being imported by the browser application.
- Added architecture policy for the new inward-only package and an explicit composition-root allowance for the existing design-time SGG export command.

# Verification

- Root TypeScript build passed.
- 34 focused lifecycle, architecture, and portal tests passed.
- Production build passed.
- PHS Assignment Request source review was saved, the composer was unmounted, and the exact review resumed with oracle parity.
- GitHub Actions failed before executing any steps because of the repository/account runner condition already seen on the prior workbench PR; no code failure or log was produced.

[depends on](prove-workbench-authored-package-in-sgg.md)
