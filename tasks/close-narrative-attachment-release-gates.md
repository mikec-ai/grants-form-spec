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
  at: '2026-08-25T03:12:36.165Z'
---
# Scope

Close bounded release-evidence gates for Project Narrative Attachment, Budget Narrative Attachment, and Other Narrative Attachments in the current portable architecture.

These are three distinct semantic narrative roles that reuse one generic attachment-capture mechanism. Do not collapse them into one semantic question, and do not add form-id branches.

# Acceptance criteria

- Verify exact producer/consumer pins, official XSD version/hash, extraction provenance, and runtime identities for all three forms.
- Exercise the generic API and browser plan across attachment selection/upload, validation, save/reload, print, and bounded accessibility checks where the environment supports them.
- Record exact commits, hosted run/artifact IDs and hashes, pass/fail/inconclusive counts, and unavailable or human-only gates.
- Keep all work in mikec-ai forks and avoid active R&R Subaward Budget 10YR/30, PHS Inclusion, and PHS Additional Indirect Costs files.

# Progress receipts

- Consumer PR: `mikec-ai/simpler-grants-gov#103` on `codex/narrative-attachment-release-evidence`; current head `a5ec8a9c383ea6e64f1ade37022fae8d182c824e`.
- Isolated change: a generic capability-driven attachment upload/save/reload/print receipt plus matrix-contract coverage; no form-ID branches and no producer, runtime, adapter, or registration changes.
- Local checks: browser-plan API `24 passed`; focused attachment parity/provenance/registration/differential/preview `49 passed`; TypeScript matrix contract `10 passed`; focused Prettier and ESLint passed.
- Hosted frontend build, lint/type/format/unit, Storybook, and pa11y checks passed on the first PR revision. The broad Mobile Chrome smoke failure is unrelated: ten existing tests failed across legacy attachment, SF-424, performance-site, and SF-424A flows.
- Exact three-form hosted run `32804261169` is in progress at head `a5ec8a9c383ea6e64f1ade37022fae8d182c824e`. A superseded run `32802547328` was canceled after it exposed redundant CI retries in this receipt suite; the generic retry fix is included in the current head.
