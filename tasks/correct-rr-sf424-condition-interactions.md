---
type: Task
title: Correct R&R SF-424 disabled-versus-hidden interactions
priority: P0
description: >-
  Corrected the eight R&R SF-424 condition interactions from exact official DAT
  evidence, compiled the supported enablement and requiredness semantics,
  projected them through the generic portable consumer, and verified both
  presentation presets.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T20:01:35.284Z'
assignee: Codex
---
# Delivery receipts

- Producer: [grants-form-spec PR #123](https://github.com/mikec-ai/grants-form-spec/pull/123), source commit `a97da3714733566847349efcc013c6a79045b21b`; merged after both producer checks passed.
- Consumer: [grants-form-workbench PR #36](https://github.com/mikec-ai/grants-form-workbench/pull/36), source commit `8f5dde0ff2f9d2b2c0b41f080813616ee7054cbb`; merged after complete local verification. GitHub Actions did not start because of the account spending limit, not a code failure.
- Exact behavior result: 8 conditions and 8 effects; 7 enable/disable effects, 6 conditional-requiredness effects, and 0 visibility effects. The Previous Grants.gov Tracking ID remains visible and is required only for changed/corrected applications.
- Consumer verification: 354 tests passed and 1 skipped; typecheck, question-catalog check, browser-catalog check, and production build passed.
- Provenance: each projected rule retains the official DAT URI, SHA-256, source path, and source record; conditional requiredness is derived from the pinned compiled JSON Schema.

# Boundary preserved

The importer supports only a bounded, fail-closed JSON Schema `if` plus `then.required` shape and local `#/$defs` references. UI enablement and schema requiredness combine only when their predicates match exactly. No semantic mapping status was promoted.
