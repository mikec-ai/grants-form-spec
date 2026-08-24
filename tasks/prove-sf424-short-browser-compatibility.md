---
type: Task
title: Prove SF-424 Short browser compatibility
description: >-
  Completed on consumer PR 73 at commit ed5685f34. The bounded SF-424 Short
  receipt passes registration, adapter API preflight, real Apply render,
  save/reload with 73 persisted controls after editing organization_name,
  accessibility with zero violations, and ordinary print rendering. The slice
  added only generic capability and renderer improvements: mixed/root
  conditional extraction, removal of resolved definitions before rendering,
  exclusion of prepopulated outputs from editable discovery, and plan-driven
  control selection. Focused API, frontend, typing, lint, formatting, and build
  checks pass; generated evidence remains ignored.
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T15:11:25.626Z'
superbee_progress_status: done
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
