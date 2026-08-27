---
type: Task
title: Implement deterministic source-evidence authoring scaffolder
priority: P0
assignee: Codex
description: >-
  Add a design-time agent CLI that converts pinned deterministic form extraction
  into a strict portable-form authoring draft, without adding runtime or
  renderer dependencies. Prove the boundary on a second genuinely new form.
superbee_progress_status: in_progress
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T15:55:33.495Z'
---
# Scope

Build the scaffolding step between deterministic extraction evidence and the existing portable-form authoring compiler. The output is a reviewable draft, never semantic authority.

# Acceptance evidence

- Design-time package only; no consumer/runtime import.
- Exact input provenance survives into the draft and source-evidence receipt.
- Similar wording never auto-promotes semantic equivalence.
- Every generated source question remains unreviewed.
- Unknown input and unsupported structures fail closed with structured TOON and exit code 2 or 1 as appropriate.
- A second form absent from the portable baseline compiles and renders from the scaffolded draft.
- Tests cover determinism, provenance, review-state boundaries, and unknown flags.
