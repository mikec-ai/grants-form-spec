---
type: Task
title: Separate SGG runtime identity from portable FormMeta
priority: P0
assignee: identity_agent
description: >-
  Move only demonstrated SGG runtime identity fields into a versioned SGG-owned
  registration/target record, preserving compatibility and avoiding wholesale
  target-vocabulary relocation.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T15:36:02.486Z'
---
# Goal

Move SGG runtime identity out of the canonical portable form metadata without disturbing the portable artifact graph or creating a second per-form source of truth.

# Acceptance criteria

- `formType` and `sggVersion` are no longer required canonical `FormMeta` fields.
- A versioned SGG-owned registration or target record carries the runtime identity and is consumed through one generic adapter path.
- Form UUID and instruction UUID ownership are reviewed separately and the chosen boundary is recorded rather than inferred.
- Existing registered portable forms retain equivalent runtime identity and behavior through a bounded compatibility migration.
- Producer contract, bundle, Simpler registration, parity, and lifecycle tests remain green.
- No compiler or adapter branch is keyed to an individual form.

# Scope boundary

Do not move every `@Sgg.*` declaration, introduce a new intermediate representation, redesign artifact distribution, or change applicant-visible behavior. The existing forms-only SGG vocabulary remains quarantined unless a later evidenced task retires a specific construct.

# Completion evidence

Record the fields moved, the compatibility mechanism, affected-form count, and before-and-after SGG-specific surface in the portable contract.
