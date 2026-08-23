---
type: Task
title: Separate banked forms from runtime-enabled forms
description: >-
  Allow verified artifact banking without inventing Simpler runtime identities,
  while keeping runtime enablement fail-closed.
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T22:40:31.558Z'
priority: P0
superbee_progress_status: in_progress
assignee: promote_new_forms_agent
---
# Goal

Decouple digest-verified artifact banking from Simpler runtime enablement so genuinely new portable forms can be promoted without inventing UUIDs, FormTypes, or compatibility projections.

# Acceptance criteria

- The selected artifact bank may contain forms with no runtime identity.
- Runtime loading, preview, and registration fail closed unless a selected form is explicitly runtime-enabled and has a complete consumer-owned identity/projection record.
- Existing runtime-enabled and production-registered forms retain exact behavior.
- Manifest, provenance, digest, required-XSD, and atomic-selection verification still cover every banked form.
- Tests prove that missing identity is accepted only for banked-only forms and rejected for any runtime-enabled form.
- Production registrations remain unchanged.
- PHS Assignment Request and Attachment Form prove the banked-only path at producer revision `2fde5118f440f31c7527fde784d573bb3ab3d912`.

# Boundary

Do not invent target identities. Test/dev preview enablement is a later explicit consumer decision tracked separately.

[depends on](automate-cross-repo-form-promotion.md)
