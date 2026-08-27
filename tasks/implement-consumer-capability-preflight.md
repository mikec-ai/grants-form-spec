---
type: Task
title: Implement consumer capability preflight for agent-authored forms
priority: P1
assignee: Codex
description: >-
  Create a form-neutral, machine-readable preflight that evaluates portable form
  packages against explicitly registered consumer capabilities. It must report
  exact affected paths, supported and unsupported declarations, stable reason
  codes, package provenance, and an overall ready/partial/blocked outcome
  without changing semantic review status. Expose it through the agent-tools CLI
  with structured TOON stdout, stderr-only diagnostics, exit 2 for unknown
  flags, and behavior tests. Audit the pinned cohort and prove findings against
  real packages.
superbee_progress_status: in_progress
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T12:33:52.562Z'
---

