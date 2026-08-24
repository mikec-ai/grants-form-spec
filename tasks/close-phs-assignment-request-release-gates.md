---
type: Task
title: Close PHS Assignment Request release gates
priority: P1
description: >-
  Prove the banked PHS Assignment Request through consumer lifecycle, privacy,
  accessibility, and release gates.
superbee_progress_status: in_progress
superbee_updated_by: phs_assignment_release
generated:
  by: 'process:superbee'
  at: '2026-08-24T20:43:57.308Z'
assignee: phs_assignment_release
---
# Goal

Close the remaining product and release gates for the already-banked PHS Assignment Request without reopening its portable authoring architecture.

# Delivered baseline

- The declarative producer form and exact source evidence are complete.
- Producer preflight and hosted CI passed.
- The generic consumer bank contains the form and its exact official XSD.
- The form remains unregistered and unavailable to production routing.

# Acceptance criteria

- Exercise representative optional and repeated preferences through save/reload, validation, locked/print, and submission lifecycle surfaces.
- Verify reviewer-exclusion data receives appropriate privacy, authorization, logging, export, and retention treatment.
- Complete instruction, semantic, policy, accessibility, and operational review, preserving unresolved source conflicts explicitly.
- Record a real-browser conformance receipt through the shared preview and catalog harness.
- Register or release only through a separate approved decision; banking alone is not release evidence.
- Add no PHS Assignment Request-specific compiler, loader, renderer, adapter, or conformance branch.

# Boundary

This task consumes the banked artifact. It does not redefine its semantic questions or treat an existing runtime as source authority.

# Automated handoff progress

Consumer PR [#86](https://github.com/mikec-ai/simpler-grants-gov/pull/86) at initial head `8842f494c987f1e41d6d34d6b2cb633777dcdc43` adds focused form-level evidence without a runtime identity, registration, or product-code branch.

- All 13 source-defined optional slots are exercised, including all three awarding-component suggestions, three study-section suggestions, five expertise slots, rationale, and reviewer exclusion.
- Empty and representative full responses pass Simpler validation. The representative response survives JSON persistence and submit-time validation with complete status.
- The source-declared 7-, 20-, 40-, and 1,000-character limits execute at the Simpler validation boundary.
- Representative XML preserves all values and validates locally against the exact official XSD SHA-256 `7e697ee33ea6f72271c0d74fc48c61f4f81faa242a712a4c73e7898f6c4ab976` and its pinned local import closure.
- Source provenance and all 13 proposed semantic mappings remain explicit; published semantic acceptance is not claimed.
- The form remains absent from `registrations.json`.
- Focused local verification: 33 tests passed across the new handoff, preview, and browser-plan suites; Ruff and Black passed.

The bounded generated browser plan mechanically records 13 editable controls and no required-field, `fieldList`, attachment, conditional, calculation, or read-only capability. The source version expresses repeated preferences as fixed numbered slots, not as a dynamic repeater; no array behavior was invented.

A manually dispatched real-browser run is in progress at [workflow run 32775257287](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32775257287). The generic planner already supports a bounded `PORTABLE_BROWSER_FORM_IDS=phs-assignment-request` selection, but the hosted workflow does not expose or propagate that input and therefore expands the run to the full catalog. This CI parallelization defect was reported centrally rather than fixed in this form-specific slice.

# Open human and operational gates

- Authorized privacy/security reviewers must decide and evidence access, edit, authorization, audit logging, exports, printable/submission/retrieval artifacts, backups, retention, deletion, incident response, redaction, and sensitivity treatment for `notReview`, which can contain names, affiliations, relationships, and exclusion reasons.
- Human semantic/instruction review must confirm all labels, optionality, limits, and paths and resolve the source conflict between illustrative PDF code `B10` and DAT code `BP10`.
- Human policy review must decide whether bounded free strings remain correct for awarding components and study sections; no enum or lookup was inferred.
- Human accessibility review must cover reading order, labels, errors, keyboard operation, assistive technology, zoom/reflow, and print. Automated Axe evidence is not approval.
- NIH operational, records, support, and release review remains open.
- Production identity, registration, routing, and release require a separate approved decision and change.

[depends on](author-integrate-phs-assignment-request.md)

[depends on](add-portable-form-preview-registration.md)

[depends on](run-portable-catalog-browser-matrix.md)
