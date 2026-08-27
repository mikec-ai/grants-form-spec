---
type: Task
title: Implement repeatable attachment interaction generically
priority: P0
assignee: Codex-attachment-array
description: >-
  Completed in grants-form-workbench PR #6 (merge
  f6dde5ba24f47c29fa274cff62111850dab15838). Generic AttachmentArray applies
  only to explicit widget plus array-of-UUID schema, including resolved question
  references; serializes ordered UUIDs only; handles atomic staging/rollback,
  max interaction, min schema validation, removal/rejection/stale/session
  disposal, and both presets. No form IDs/backend/file policy/content
  extraction. Full isolated run 228 tests + 2 approved skips; exact producer
  reimport 38/38; independent review approved. Hosted CI allocated no runner and
  executed zero steps.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T06:28:05.988Z'
---
[depends on](advance-workbench-producer-baseline.md)
