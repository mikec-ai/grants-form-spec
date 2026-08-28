---
type: Task
title: Implement reviewable standalone form lifecycle
priority: P0
assignee: Codex
description: >-
  Add individual recommendation decisions, restorable draft revisions, and
  readiness/export gating to the standalone form workbench.
superbee_progress_status: in_progress
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-28T01:42:38.563Z'
---
# Outcome

Turn the standalone workbench's agent-authored happy path into a controlled, resumable review workflow without coupling authoring to the renderer or SGG.

# Acceptance criteria

- A reviewer can accept, reject, or defer individual agent recommendations instead of accepting the entire package at once.
- Review decisions preserve the recommendation evidence and decision attribution without converting proposed semantic mappings into reviewed mappings.
- Drafts and their review history can be serialized, restored, and verified through a versioned consumer-neutral contract.
- The UI shows a readiness gate that distinguishes working draft, ready for human review, and target-export eligibility.
- Export operates on the compiled portable package through an edge adapter; the authoring workspace does not import SGG code.
- Tests cover every new behavior and enforce the existing package boundaries.

# Delivery boundary

Implement the lifecycle and UI orchestration in the standalone workbench. Do not change `grants-form-spec`, CommonGrants, the Grants Standard, or Simpler runtime behavior in this slice.

[depends on](prove-workbench-authored-package-in-sgg.md)
