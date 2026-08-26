---
type: Task
title: Verify both PHS Inclusion matrix occurrences
priority: P0
description: >-
  Prove standalone and embedded Inclusion Enrollment matrices without inferring
  unpinned rules.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-26T12:42:07.282Z'
assignee: codex
---
# Scope

Apply and verify the generic nested-matrix contract in both occurrences of the shared Inclusion Enrollment Report question: standalone PHS Inclusion Enrollment and embedded within PHS Human Subjects.

# Evidence boundary

Do not compile the 8 conditions or 28 calculation targets until exact operands and blank-value semantics are pinned. Record those as separate open gates.

# Acceptance

- Standalone and embedded matrices render with equivalent dimensional semantics.
- Add/delete, save/reload, validation routing, locked state, print, keyboard, and screen-reader coordinate context are exercised.
- Exact producer, consumer, manifest, and browser receipts are recorded in Superbee.

[depends on](extend-simpler-nested-table-runtime.md)

# Browser receipts — 2026-08-26

- Standalone application: `03a2785d-8f3c-48ac-b624-b97fe55f63cc`; form occurrence `7df125e8-5c86-4589-8e00-81fc7bc27411`.
- Embedded application: `741db86a-4099-4cec-bcaf-f4b17a90c432`; form occurrence `8eeb6cad-3fad-4675-98b2-9ae65e01a47e`.
- Standalone rendered planned and cumulative tables, protected the 28 exact F791 source-backed calculated-output coordinates, added a second report with entry-scoped names, and persisted entered values through save/reload.
- Embedded rendered planned and cumulative tables under one study/report occurrence with full study/report-scoped names and coordinate-qualified accessible labels. Study title, report title, and an entered matrix value persisted through save/reload.
- The embedded totals remain applicant-editable by design pending exact evidence. `evidence/forms/phs-human-subjects/evidence.json` records one unresolved calculation disposition covering the 28 total-like coordinates because the pinned parent XSD and F705 DAT contain zero calculation records.
- Producer PR #120 merged at `c700c8bd1edb4e7537325e26a141776826f643b8`; generic consumer runtime PR #139 merged at `88c7fc6c88058f3a2336218b128352c815e824af`; artifact/validator PR #140 merged at `c886be7101c93a8308182d8491aa0308080708f5`.

# Still open

- Locked-state, print, keyboard-order, and validation-routing browser evidence.
- Browser delete receipt (requires explicit destructive-action authorization at execution time).
- Exact embedded-study calculation/condition evidence review; do not transfer standalone F791 semantics by similarity.
