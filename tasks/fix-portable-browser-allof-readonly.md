---
type: Task
title: Fix portable browser allOf read-only discovery
description: >-
  Make shared browser evidence protect read-only fields declared through JSON
  Schema allOf composition.
superbee_updated_by: codex_phs_human_subjects_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T18:14:04.475Z'
priority: P1
superbee_progress_status: todo
---
# Defect

The generic portable browser plan treats three system-owned PHS Human Subjects determinations as editable because their `readOnly: true` declarations are carried through property-level `allOf` composition rather than as a direct property keyword.

# Exact evidence

- Form: `phs-human-subjects`, banked and unregistered.
- Affected projected properties: `involves_human_subjects`, `exempt_from_federal_regulations`, and `exemptions`.
- Each projected property is `{ "allOf": [{ "readOnly": true }] }`; the shared browser plan reports all three under `editableScalar` and omits them from `readOnly`.
- The browser plan currently reports only three read-only technical IDs (`application_id`, repeated `study_id`, and repeated enrollment `report_id`) even though the producer evidence explicitly classifies the three determinations as visible read-only system references.
- A bounded browser run would therefore attempt to edit pre-populated determinations and produce invalid evidence.

# Required generic resolution

- Resolve read-only ownership through valid `allOf` composition without form-ID logic or source-schema mutation.
- Preserve the merged NIFA read-only ancestry behavior.
- Add a generic regression plus a PHS Human Subjects plan regression proving all six system-owned/read-only paths are protected.
- Re-run the bounded PHS Human Subjects plan before any form closure claim.

# Boundary

This is a shared evidence-harness/projection defect, not permission to compile the eleven unreviewed F705 conditions or infer any of the 28 unresolved enrollment calculations.

[blocks](close-phs-human-subjects-technical-gates.md)
