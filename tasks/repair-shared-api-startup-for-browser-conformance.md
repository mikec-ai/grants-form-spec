---
type: Task
title: Repair shared API startup for hosted browser conformance
priority: P0
assignee: codex-ci-startup
description: >-
  Diagnose and repair the branch-independent hosted API readiness failure that
  prevents Pa11y and all E2E shards from starting Playwright. Preserve ordinary
  production behavior; add actionable startup diagnostics and tests. Acceptance:
  a hosted lower-environment run reaches the browser matrix and publishes
  summary/receipt/trace artifacts, or the task records a precisely evidenced
  external blocker without claiming conformance.
superbee_progress_status: in_progress
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T09:34:43.127Z'
---
[depends on](../run-portable-catalog-browser-matrix.md)
