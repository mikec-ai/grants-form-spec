---
type: Task
title: Import a pinned producer-backed form cohort into the workbench
priority: P0
assignee: Codex-producer-cohort-agent
description: >-
  Implement a generic repeatable import from exact grants-form-spec revisions
  for SF-424, SF-424 Short, Attachment Form, and PHS Assignment Request. Initial
  commit 1033f0d captured 99 artifacts and preserved conservative review status,
  but independent review withheld approval on three P1 boundaries: packaged
  question compilation mishandles nested $id and $anchor references; ignored
  dist output can be stale unless the importer itself executes or verifies the
  pinned generator; and the agent-facing CLI lacks complete AXI
  version/help/error behavior. Remediation must preserve raw
  bytes/digests/revisions/review states, use resource-aware cycle-safe reference
  handling, generate or cryptographically verify artifacts inside the import,
  provide structured TOON stdout and actionable exit codes without raw
  dependency leakage, and retain zero form-ID branches or semantic upgrades.
superbee_progress_status: in_progress
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T00:56:58.692Z'
---
[depends on](implement-portable-form-catalog.md)
