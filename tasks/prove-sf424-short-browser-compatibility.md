---
type: Task
title: Prove SF-424 Short browser compatibility
description: >-
  Draft consumer PR 73 is open against PR 71 at commit 6c8b2727a. The generic
  bounded plan selects sf424-short, the preview adapter resolves its reusable
  references without a form-specific branch, 28 focused selection/preview/seed
  tests pass, and the complete declarative parity suite passes. The real-Simpler
  browser receipt remains the only completion gate and will run after the shared
  SF-424 recording environment is released.
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T14:35:12.526Z'
superbee_progress_status: in_progress
priority: P0
assignee: codex-root
---
# Goal

Deliver one independently reviewable SF-424 Short compatibility increment with pinned producer and consumer revisions.

# Acceptance criteria

- The bounded browser plan selects only `sf424-short`.
- Registration, API preflight, Apply render, representative save/reload, accessibility, and print probes run through the generic harness.
- Any failure is classified at its first owning boundary; no form-specific adapter branch is introduced.
- Receipts, screenshots, and traces remain ignored build artifacts.
- Focused tests, TypeScript, lint, and formatting pass before a fork-only push.
