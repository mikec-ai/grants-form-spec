---
type: Task
title: Repair shared API startup for hosted browser conformance
priority: P0
assignee: codex
description: >-
  Consumer PR #69 merged to the public fork as
  b8e286cb64157b86823dc2a72066c204bf10d625. The bounded startup fix reduced
  hosted API readiness from an 800-second timeout to 5 seconds, preserved local
  reload behavior, added fail-fast diagnostics, passed API/infra/Pa11y gates,
  and allowed every E2E shard to reach Playwright. Remaining smoke failures are
  pre-existing downstream debt and are not part of this task. Catalog-wide
  browser conformance remains separately owned by
  tasks/run-portable-catalog-browser-matrix and is intentionally not a
  per-change gate.
superbee_progress_status: done
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T11:39:49.038Z'
---
## Diagnostic evidence, 2026-08-24

- Exact consumer main: `c4709fc2931d4c9129871d058247f88bcfcd0e22`.
- Hosted run `32712258368`, failing job `97386828860`: the generic browser plan compiled 39 manifest-selected forms, database seeding and search indexing completed, and Docker reported `grants-api` started. The health waiter then received no successful response for 800 seconds. The workflow captured no container state or service logs.
- A clean local worktree at the same commit, using the same source and preview flag, reached both `HEAD /health` and `GET /health` with HTTP 200. Registry construction completed in about eight seconds after the interpreter began. Observed memory was about 567 MiB for the API and 1.06 GiB for OpenSearch.
- This makes a deterministic form-registry, import, or HTTP-method defect unlikely. The remaining failure boundary is the hosted detached service process/runtime. Exact cause is not yet observable because the current failure path discards container status and logs.

## Smallest next test and repair

1. Make the health waiter fail immediately if the API container exits.
2. On failure, always print `docker compose ps -a`, the API container state, bounded API logs, and both GET and HEAD health results.
3. Start the API in CI without Flask's development reloader, which otherwise creates a second import/process and is unnecessary for an immutable checkout.
4. Add focused shell tests for success, exited-container fail-fast, timeout diagnostics, and actionable exit behavior.
5. Run the hosted browser workflow and only close this task after the browser matrix begins and publishes its CI-only artifacts, or after the diagnostics identify a precisely evidenced external blocker.

## Implementation in progress, 2026-08-24

- Fresh consumer worktree and branch: `codex/repair-shared-api-startup`, based on exact `mikec-ai/simpler-grants-gov` main `c4709fc2931d4c9129871d058247f88bcfcd0e22`.
- The bounded waiter now uses `GET /health`, keeps curl exit/status/body evidence, stops at the `>=` deadline, and fails immediately when `grants-api` is not running.
- Failure output includes `docker compose ps -a`, container state/exit/OOM/error fields, the bounded health body, and the last 300 API log lines.
- A CI-only compose override removes Flask reload for hosted E2E and Pa11y while preserving ordinary local reload behavior.
- Focused shell cases cover readiness, stopped-container fail-fast, a running HTTP 503 response/body, and the exact deadline boundary. Local compose and workflow validation are underway before a draft PR is opened.

## Draft PR receipt, 2026-08-24

- Draft PR: `mikec-ai/simpler-grants-gov#69`, https://github.com/mikec-ai/simpler-grants-gov/pull/69
- Exact head: `83abd7b7349a22c104cba29e311a67e73a8afc16`; exact base: `c4709fc2931d4c9129871d058247f88bcfcd0e22`.
- Local verification is green: five focused shell cases, ShellCheck, actionlint, merged compose configuration, a live health probe invoked from the frontend working directory, and `git diff --check`.
- The task remains in progress. Hosted API, E2E, and Pa11y results are the next evidence boundary; the draft must not be treated as browser conformance until those jobs reach the matrix and publish their CI-only artifacts.

## Independent-review correction, 2026-08-24

- Review found that a curl started just before the deadline could use its full configured timeout and accept a late HTTP 2xx after the overall readiness budget.
- PR #69 was amended at exact head `75456b985971be885bed6a76e8888ead0e89a232`: each curl attempt now clamps connect/max time to the remaining total budget, and a 2xx is accepted only when it completes strictly before the deadline.
- A sixth shell case simulates a slow HTTP 200 completing at the exact boundary and verifies timeout classification, retained HTTP evidence, clamped curl arguments, and compose diagnostics. Local verification remains green; exact-head rereview and restarted hosted runs are pending.
