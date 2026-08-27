---
type: Task
title: Execute portable behaviors through the workbench state pipeline
priority: P0
assignee: Codex-behavior-integration-agent
description: >-
  Delivered and independently approved in grants-form-workbench integration
  commits 53e3b1a and f140c14. Portable conditions and calculations now execute
  through the generic renderer without producer, form-ID, standards, or
  presentation coupling. Optional exact non-repeated condition bindings remain
  explicit consumer configuration; portable outcomes and consumer effects have
  separate receipts. Calculated outputs are read-only rendered state and are
  removed from applicant-authored data; behavior failures suppress persistence
  callbacks; post-transition data is revalidated against the post-behavior
  schema before callbacks. Static requiredness is never weakened. Full
  verification passed with 130 tests, one intentional skip, typecheck, all
  builds, and a clean dependency tree. Independent review found and then
  verified the same-edit requiredness validation fix. Row-specific
  repeated-field effects remain deliberately deferred pending a row-aware
  contract.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T00:54:59.317Z'
---
[depends on](implement-portable-declarative-behaviors.md)
