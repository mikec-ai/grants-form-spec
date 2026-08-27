---
type: Task
title: Execute portable behaviors through the workbench state pipeline
priority: P0
assignee: Codex-behavior-integration-agent
description: >-
  Connect the merged bounded behavior contract to the generic renderer data flow
  so declared conditions and calculations execute without presentation,
  producer, or form-ID coupling. Commit 330d4c3 completed the first
  implementation with 129 passing tests and one intentional skip, but
  independent review correctly withheld approval: an edit that activated
  additive requiredness forwarded validation errors computed against the
  previous schema. The fix must revalidate rendered data against the
  post-behavior schema before any change/state callback and include a same-edit
  regression test. The portable behavior artifact names outcomes but does not
  assign visual effects; condition-to-field effects remain optional explicit
  consumer configuration with separate receipts. Keep applicant inputs,
  calculated outputs, validation outcomes, provenance, rollback, and fail-closed
  errors distinct; schema-required fields may not be weakened. Row-specific
  repeated-field effects remain deferred pending an explicit row-aware contract.
superbee_progress_status: in_progress
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T00:51:51.762Z'
---
[depends on](implement-portable-declarative-behaviors.md)
