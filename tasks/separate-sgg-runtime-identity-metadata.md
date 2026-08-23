---
type: Task
title: Separate SGG runtime identity from portable FormMeta
priority: P0
assignee: identity_agent
description: >-
  Move only demonstrated SGG runtime identity fields into a versioned SGG-owned
  registration/target record, preserving compatibility and avoiding wholesale
  target-vocabulary relocation.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T16:05:59.673Z'
---
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

# Result

Delivered through ordered producer and adapter changes.

- mikec-ai/grants-form-spec PR #35 merged as fb85da8b7fc58f9000be7da491f317502da3b269.
- mikec-ai/simpler-grants-gov PR #32 merged as 0c14d8bfea32b182c51803e5f2e31f1c426518ec.
- Portable FormMeta no longer owns the SGG-generated UUID, FormType, or SGG schema version. The legacy Grants.gov FID remains portable source identity.
- A versioned SGG record preserves the exact UUID, FormType, and version triples for all 19 forms; only the prior five registrations remain active and no instruction UUID was invented.
- The adapter consumes identity through one generic path with no per-form branch.
- Producer preflight passed with 659 artifacts; 119 adapter lifecycle/parity tests and all static checks passed.
- Independent review required and verified an exact all-19 compatibility lock plus repinning to the merged producer commit before adapter merge.
