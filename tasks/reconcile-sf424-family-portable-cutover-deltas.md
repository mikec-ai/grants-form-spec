---
type: Task
title: Reconcile SF-424 family portable cutover deltas
priority: P0
description: >-
  Resolve the producer, declaration, and reviewed compatibility differences
  exposed by PR63 while production remains fail-closed on legacy definitions.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T05:04:56.884Z'
---
# Goal

Resolve the portable-versus-legacy schema and validation deltas exposed when consumer PR #63 temporarily made SF-424, SF-424 Short, and SF-424A production-active. Keep the three portable candidates banked and previewable while production stays on the legacy definitions until each delta is mechanically fixed or explicitly reviewed as intentional.

# Incident evidence

- Consumer PR #63 head `44a217345868ed15192431ee755c9f41febcc8b7` consumed producer revision `14b08b8cbd6016778a8f0688ed924a7ede4c8d2d` and produced 12 relevant API test failures across the three forms. The failures collapse to three root causes; repeated fixtures amplify the same field-level differences.
- Consumer PR #65 began by restoring the three legacy definitions for production while preserving the portable bank, adapter, and preview seam. Its current head `1f2f47f164674e91904d7392978ae58c63c5936d` also closes a CI-classifier gap: the lightweight additive lane had allowed modifications to existing portable artifacts and XSDs, while those 
