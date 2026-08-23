---
type: Task
title: Integrate Key Person overflow gating
priority: P0
assignee: key_person_xml_agent
description: >-
  Apply the merged count-or-presence condition to all three Key Person overflow
  uploads and carry the emitted artifacts through SGG.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:41:44.862Z'
---
# Goal

Use the merged bounded condition capability in the actual R&R Key Person declaration and consumer artifacts.

# Acceptance criteria

- All three overflow attachments enable at 99 structured people or remain enabled while their own saved value is present.
- Canonical and SGG emitted conditions bind the exact list and target attachment paths.
- Existing six Key Person conditions remain unchanged and three reviewed overflow gates are added.
- Simpler repins stable merged producer artifacts and artifact-backed frontend tests exercise both branches for each upload.
- No form-specific runtime branch or production registration.

# Boundary

Do not broaden the condition language or claim policy/release acceptance.

# Result

Delivered in ordered producer and consumer changes.

- grants-form-spec PR #40 merged as 3c6fd775476aa45e6e10d4972e5d581131b19a28.
- simpler-grants-gov PR #37 merged as 26fb5f686b0d0555028eb50b0115e485ad699c1a.
- The original six Key Person conditions remain byte-locked and exactly three compound rules were added.
- Every overflow upload enables at 99 senior/key people or while its own saved attachment exists; sibling uploads do not cross-enable one another.
- Canonical and SGG artifacts use exact root/list/own-target pointers, including snake_case consumer projection.
- Artifact-backed frontend tests cover capacity, own saved value, disabled state, and sibling isolation for all three controls.
- No runtime branch, registration, evidence-status change, or production opt-in was introduced.
