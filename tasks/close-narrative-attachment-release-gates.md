---
type: Task
title: Close narrative attachment release gates
priority: P1
assignee: codex_narrative_attachment_closure
description: >-
  Prove Project Narrative Attachment, Budget Narrative Attachment, and Other
  Narrative Attachments end to end as three distinct semantic roles reusing one
  generic attachment-capture mechanism.
superbee_progress_status: in_progress
superbee_updated_by: codex_narrative_attachment_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T02:38:15.696Z'
---
# Scope

Close bounded release-evidence gates for Project Narrative Attachment, Budget Narrative Attachment, and Other Narrative Attachments in the current portable architecture.

These are three distinct semantic narrative roles that reuse one generic attachment-capture mechanism. Do not collapse them into one semantic question, and do not add form-id branches.

# Acceptance criteria

- Verify exact producer/consumer pins, official XSD version/hash, extraction provenance, and runtime identities for all three forms.
- Exercise the generic API and browser plan across attachment selection/upload, validation, save/reload, print, and bounded accessibility checks where the environment supports them.
- Record exact commits, hosted run/artifact IDs and hashes, pass/fail/inconclusive counts, and unavailable or human-only gates.
- Keep all work in mikec-ai forks and avoid active R&R Subaward Budget 10YR/30, PHS Inclusion, and PHS Additional Indirect Costs files.
