---
type: Task
title: Close SF-424C release gates
priority: P1
description: >-
  Prove the banked SF-424C through calculation parity, consumer lifecycle,
  accessibility, and release gates.
superbee_progress_status: in_progress
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T20:34:41.049Z'
assignee: codex_root_sf424c
---
# Goal

Close the remaining calculation, lifecycle, differential-parity, and release gates for the already-banked SF-424C portable form.

# Delivered baseline

- The producer declaration, 18 semantic questions, 24 source-backed calculations, XML mapping, and exact XSD conformance are complete.
- Representative populated and sparse producer calculations match the legacy oracle, with one documented empty-draft difference.
- SF-424C is included in the current 38-form consumer bank and remains unregistered.

# Acceptance criteria

- Run portable and legacy implementations against shared populated, sparse, invalid-total, federal-share, program-income, save/reload, locked/print, submission, and XML fixtures.
- Prove calculations and validation through actual consumer lifecycle and browser surfaces, including the intentional empty-draft behavior.
- Complete semantic review of the proposed mappings plus instruction and accessibility review.
- Govern every accepted parity delta with exact evidence, review state, and regression coverage.
- Record catalog browser and differential-parity receipts before any production registration decision.
- Add no SF-424C-specific compiler, rule-engine, loader, renderer, or adapter branch.

# Boundary

This task validates and releases the existing portable design; it does not reopen the construction-budget architecture without a demonstrated generic defect.

[depends on](migrate-sf424c-parity-oracle.md)

[depends on](add-portable-form-preview-registration.md)

[depends on](run-portable-catalog-browser-matrix.md)

[depends on](build-uniform-legacy-differential-parity.md)

[depends on](enforce-evidence-backed-parity-deltas.md)
