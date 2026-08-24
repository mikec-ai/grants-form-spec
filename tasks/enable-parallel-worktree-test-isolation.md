---
type: Task
title: Enable parallel worktree test isolation
priority: P1
assignee: unassigned
description: >-
  Remove local Compose collisions so multiple form-evidence agents can run
  repository-native tests concurrently.
superbee_progress_status: todo
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T20:40:18.857Z'
---
# Goal

Make repository-native API and browser test stacks safe to run concurrently from multiple isolated git worktrees, so form-specific evidence lanes do not serialize on one developer environment.

# Evidence

On 2026-08-24 an SF-424C lifecycle lane used a fresh worktree and a unique `COMPOSE_PROJECT_NAME`, but Compose still collided with the active stack because services declare global container names such as `sqsmock`. The same test passed through the host virtual environment with `DB_HOST=localhost`, proving the form code was sound and the blockage was test-environment isolation.

The PHS Assignment Request lane independently found that the generic browser-plan command already honors `PORTABLE_BROWSER_FORM_IDS`, but the manually dispatched hosted E2E workflow does not expose or propagate that selector. A one-form handoff therefore schedules the entire 39-form catalog across four shards.

# Acceptance criteria

- Remove or safely parameterize global Compose container names used by repository-native tests.
- Derive isolated networks, volumes, service discovery, and non-conflicting host ports per worktree or explicit test-run identifier.
- Provide one documented command for a targeted API test run from a fresh worktree.
- Demonstrate two concurrent worktree test runs without shared containers, databases, schemas, reports, or teardown affecting one another.
- Add a fail-closed optional hosted-workflow input that propagates the existing `PORTABLE_BROWSER_FORM_IDS` selector, and prove a one-form dispatch schedules only that form while the default remains the live manifest selection.
- Preserve the ordinary single-worktree developer workflow and hosted CI behavior.
- Keep this strictly in development/test tooling; do not change production form runtime behavior.

# Boundary

This task improves execution isolation. It does not redesign the application runtime, portable form architecture, or deployment topology.
