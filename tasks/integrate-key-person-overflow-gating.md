---
type: Task
title: Integrate Key Person overflow gating
priority: P0
assignee: key_person_xml_agent
description: >-
  Apply the merged count-or-presence condition to all three Key Person overflow
  uploads and carry the emitted artifacts through SGG.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:22:11.971Z'
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
