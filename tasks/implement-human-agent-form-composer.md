---
type: Task
title: Implement shared human-agent form composer foundation
priority: P0
assignee: Codex
description: >-
  Delivered a renderer-independent authoring workspace where agents and humans
  edit the same portable-form-authoring draft. Humans can inspect agent
  rationale, add/remove/reorder exact questions, inspect review state and
  provenance, serialize the draft, and see a live generic preview.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T20:16:45.343Z'
---
# Architectural boundary

The GUI and agent are peer clients of the same neutral `portable-form-authoring/v1` draft. Search, filters, and other transient UI state remain outside it. Agent rationale uses a separate `portable-form-agent-proposal/v1` receipt and applies through the same `selectQuestion` command as a human click.

# Delivery receipts

- [grants-form-workbench PR #37](https://github.com/mikec-ai/grants-form-workbench/pull/37) merged from commit `469bde3179021b61a6de1a3fc0ef80e0cdb6ff23`.
- New framework-neutral package: `@grants-form-workbench/authoring-workspace`.
- The composer assembles 185 exact question records from the currently verified portable packages, failing closed on conflicting schemas.
- Every new occurrence remains `proposed`; the composer cannot promote reviewed coverage.
- Exact question URI, authority, SHA-256, and source receipts survive preview compilation.
- 29 focused authoring, integration, and architecture tests passed; typecheck and production build passed. The full non-agent suite reached 356 passing and 1 skipped with one unrelated attachment timing flake under concurrent load; that same test passed in the focused run.
- GitHub Actions did not start because of the account spending limit, not a code failure.

# Deliberately deferred

Visual rule authoring, section/repeatable-group editing, persistence and approval, and source-evidence-backed publication remain separate follow-up slices.
