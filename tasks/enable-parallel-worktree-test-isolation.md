---
type: Task
title: Enable parallel worktree test isolation
priority: P1
assignee: codex_root_parallel_tests
description: >-
  Remove local Compose collisions so multiple form-evidence agents can run
  repository-native tests concurrently.
superbee_progress_status: in_progress
superbee_updated_by: codex-root-fork
generated:
  by: 'process:superbee'
  at: '2026-08-24T22:40:08.750Z'
---
---
type: Task
title: Enable parallel worktree test isolation
priority: P1
assignee: codex_root_parallel_tests
description: >-
  Remove local Compose collisions so multiple form-evidence agents can run
  repository-native tests concurrently.
superbee_progress_status: in_progress
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T20:58:37.202Z'
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

# Progress — 2026-08-24

- Consumer PR [mikec-ai/simpler-grants-gov#87](https://github.com/mikec-ai/simpler-grants-gov/pull/87) exposes the existing fail-closed portable-form selector to manual and reusable hosted E2E dispatches.
- A bounded selection now uses one shard; the default continues to use the live manifest and four shards.
- The selector is propagated through browser-plan generation and preview seeding without form-specific test paths or registrations.
- Fifteen browser-plan/workflow contract tests pass locally; workflow YAML and Ruff checks pass.
- Local Compose container-name isolation remains open and is deliberately separate from this hosted-workflow increment.
- Independent review found and the same PR corrected two cold-path hazards: bounded shard 1 now installs Firefox and WebKit, and a bounded selector now implies `@portable-catalog` rather than accidentally running the entire E2E suite.
- Invalid or whitespace-bearing selectors fail before expensive downstream jobs; the Python selector remains authoritative for membership in the live manifest.
- A second independent review found reusable-workflow event precedence and changed-test overrides could bypass the catalog tag. PR #87 now routes a selector before pull-request/push logic and suppresses all-test and changed-spec paths, structurally guaranteeing that bounded execution runs only `@portable-catalog`.

# Progress — parallel local stacks

- Consumer PR [mikec-ai/simpler-grants-gov#93](https://github.com/mikec-ai/simpler-grants-gov/pull/93) adds an opt-in `bin/run-isolated-api-test` command.
- Ordinary single-worktree Compose project names and host ports remain the defaults when isolation is not requested.
- Isolated runs derive separate API/database project identities, shared network names, volumes, and deterministic host ports from a validated stack ID.
- Global `container_name` declarations were removed from API, database, and frontend Compose definitions; readiness and teardown now address Compose services through explicit project identities.
- Six focused CLI/configuration tests and six readiness-script tests pass. Mypy, Ruff, Black, isort, ShellCheck, Compose configuration rendering, and `git diff --check` pass.
- Real Docker proof ran two PostgreSQL stacks concurrently with distinct containers, networks, volumes, and ports. Tearing down the first stack and its volume/network left the second accepting connections.
- The full runtime proof is complete on consumer commit `1c79aca3e`: `proof-a` and `proof-b` each initialized independent PostgreSQL, OpenSearch, S3Mock, SQS, DynamoDB, OAuth, SOAP, and Mailpit services, and the same repository-native API test passed concurrently in both stacks (`1 passed` in 6.05 seconds and 6.10 seconds).
- Tearing down `proof-a` left all seven long-running `proof-b` API-side services healthy; the same API test passed again in `proof-b` in 4.94 seconds before its scoped teardown.
- The proof surfaced and fixed one shared Docker Desktop defect: S3Mock's mutable host bind mount could not be chowned in a clean worktree. PR #93 now uses a Compose-scoped named volume and tests that contract.
- A simultaneous clean build of two amd64 API images on this arm64 Mac exceeded the host/QEMU envelope and one `uv build` process segfaulted. Staging the same immutable image once, then initializing and testing both isolated runtime stacks, succeeded. This is a local build-capacity constraint rather than a Compose namespace collision.
- Remaining work is PR review and completion of hosted checks; the concurrent runtime-isolation acceptance criterion is satisfied.
