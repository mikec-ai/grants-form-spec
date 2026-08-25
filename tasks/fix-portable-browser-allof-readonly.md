---
type: Task
title: Fix portable browser allOf read-only discovery
description: >-
  Make shared browser evidence protect read-only fields declared through JSON
  Schema allOf composition.
superbee_updated_by: codex_phs_human_subjects_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T18:31:55.318Z'
priority: P1
superbee_progress_status: in_progress
assignee: codex_phs_human_subjects_closure
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

# Implementation awaiting independent review

Private-fork PR #127, rebased onto private main `17a5f7cf862dd71585eb3afd6fb4cdb58c4d24a4`, is at exact head `e990d7305630c100b3411e4fb4ffc111e5b29818`. It changes only the generic browser-plan read-only predicate and its tests. It recursively inspects `readOnly` across each selected schema candidate's `allOf` branches, preserving the existing ancestor protection. A minimal positive/negative regression proves an `allOf`-protected system field is read-only while an otherwise identical applicant field remains editable. After initial review, the PHS regression was strengthened to assert the exact three-field read-only definition set, the exact three-field top-level applicant-editable set, the exact two-repeater top-level set, and the complete top-level UI partition.

Focused receipt: 51 browser-plan, preview, and PHS flattened-scalar XML tests passed; Ruff and Black passed. No bounded form run or merge will occur before independent review.

# Independent review and hold

Independent re-review is clean. Exact bounded run `32883228437` was intentionally canceled after setup passed because the shared attachment probe waits on whole-form validity and PHS Human Subjects has 15 attachment roles; continuing would yield a predictable non-attributable timeout rather than useful evidence. Hosted API run `32883150872` stopped before tests on the unrelated main-branch mypy regression in `check_form_spec_bank.py:189`; that regression is now fixed on the rebased main. Fresh rebase receipts are 87 combined tests, whole mypy across 753 files, Ruff, and Black green. Hosted API run `32884226167` is pending; the redundant automatic E2E was canceled while the attachment probe remains unresolved.

PR #127 is held for its fresh API signal, then may merge independently of the attachment-probe defect because its production change is limited to read-only browser-plan discovery. The bounded Human Subjects form run remains blocked on the attachment-probe fix.

[blocks](close-phs-human-subjects-technical-gates.md)
