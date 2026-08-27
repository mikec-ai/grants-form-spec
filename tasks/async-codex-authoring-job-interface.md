---
type: Task
title: Add asynchronous agent-authoring job interface
priority: P1
assignee: Codex
description: >-
  Introduce submit, status, cancel, and result retrieval around the portable
  authoring exchange so browser requests do not block and the local runner
  remains replaceable by a managed service.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T23:30:26.422Z'
---
# Scope

Replace the blocking local Codex authoring request with a small, provider-neutral job lifecycle while preserving the immutable portable exchange and human-review boundary.

# Acceptance criteria

- Submit returns an opaque job identifier without waiting for model completion.
- Status exposes only normalized queued, running, completed, failed, or canceled state.
- Cancel terminates active execution rather than merely hiding its response.
- Result retrieval returns only a fully validated recommendation package.
- The browser polls and can cancel without importing Codex or process details.
- The local implementation is bounded and replaceable by a managed job service.
- Tests cover transitions, cancellation, errors, and the browser review flow.

# Outcome

Merged `mikec-ai/grants-form-workbench` PR #42. Source commit `e2b982803dd6e2229876a0b7cffec6a112086ebe`; merge commit `a0062d7607590ded6231e71637a1bb028752b527`.

- Added a provider-neutral submit/status/cancel/result service with opaque job identifiers, bounded retention and capacity, isolated result copies, and normalized safe errors.
- Added exact digest-bound request validation before any runner dispatch.
- Propagated cancellation through an `AbortSignal` to the active Codex child process, including forced termination fallback and ephemeral-workspace cleanup.
- Replaced the blocking browser call with asynchronous polling, visible queued/running state, and a human-controlled cancel action that leaves the draft unchanged.
- Kept Codex configuration in the local composition root; browser code depends only on the portable exchange and job HTTP interface.

# Verification receipts

- 45 focused tests passed across exchange validation, process cancellation, job transitions, HTTP translation, recommendation import, and browser cancellation.
- Typecheck, question-catalog verification, and production build passed.
- The broader Vitest run reached 384 passing tests and two expected skips; one pre-existing timing-sensitive form interaction failed under parallel load and passed when `App.test.tsx` was rerun alone (21/21).
- The pinned producer reimport suite passed separately (44/44) against `/private/tmp/grants-form-spec-rr-sf424-conditions` at producer revision `a97da3714733566847349efcc013c6a79045b21b`.
- A live local request returned HTTP 202 in queued state, completed in about 11 seconds, and returned one validated `select-question` recommendation for exact ID `project/title`.
- A live browser run exposed the cancel control, canceled the active review, preserved the draft, and produced no browser warnings or errors.
- GitHub Actions run `33126423537` did not start any workflow step. GitHub annotated it as an account billing/spending-limit failure before runner assignment; it is not a code-test result.

# Authority boundary

Recommendations remain agent proposals. This work neither accepts semantic mappings nor changes published coverage.

[depends on](connect-codex-authoring-runner.md)
