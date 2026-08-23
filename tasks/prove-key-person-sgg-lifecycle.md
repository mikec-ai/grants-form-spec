---
type: Task
title: Prove Key Person through the SGG lifecycle
priority: P0
assignee: key_person_lifecycle_agent
description: >-
  Exercise R&R Key Person Expanded through generic SGG registration-ready
  projection, validation, persistence, print, submission, and XML without
  production opt-in.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:41:45.759Z'
---
# Goal

Prove the existing portable Key Person form through the complete technical SGG lifecycle.

# Acceptance criteria

- Add only registration-ready identity/type plumbing; do not activate production registration.
- Cover repeated-person add/edit/delete/max, validation, nested attachments, save/reload, locked/print, submit, and assembled XML.
- Consume the portable artifacts and generic adapter paths with no form-specific branch.
- Record human semantic, accessibility, instruction, identifier, and release gates explicitly.

# Boundary

Technical completion is not production approval or semantic acceptance.

[depends on](project-key-person-xml-in-sgg.md)

[depends on](integrate-key-person-overflow-gating.md)

# Result

Technical lifecycle proof is complete in the mikec-ai/simpler-grants-gov fork.

- PR #35 merged as 36e87ab0b933c9c98575db7dc929f63a054bd043: registration-ready identity and FormType plumbing, repeated-row interactions/max, nested validation, real database save/reload, all seven attachment ownership/audit paths, locked/print response rendering, and submit service/status transition.
- PR #36 merged as 5b16ea30628936fbe4bf0637838e07ccb30505d2: generic portable XML projection and exact XSD validation.
- PR #37 merged as 26fb5f686b0d0555028eb50b0115e485ad699c1a: actual overflow condition artifacts and frontend behavior.
- Runtime construction, persistence, validation, attachment audit, print, and submission use generic paths with zero form-specific adapter branches.

Production registration remains absent. Semantic mappings remain proposed, and accessibility, instructions, identifiers, one-row deletion behavior, State/Province stale-value handling, policy, and release acceptance remain explicit human/operational gates.
