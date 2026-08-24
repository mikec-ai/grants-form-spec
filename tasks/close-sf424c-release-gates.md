---
type: Task
title: Close SF-424C release gates
priority: P1
description: >-
  Prove the banked SF-424C through calculation parity, consumer lifecycle,
  accessibility, and release gates.
superbee_progress_status: in_progress
generated:
  by: 'process:superbee'
  at: '2026-08-24T23:56:13.462Z'
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

# Automated handoff progress — 2026-08-24

- Consumer PR [mikec-ai/simpler-grants-gov#85](https://github.com/mikec-ai/simpler-grants-gov/pull/85) separates representative applicant input from calculated output and exercises the ordinary application services.
- Save/reload materializes and persists all 24 source-backed calculations from applicant-entered values.
- The calculated response passes the real submission service and records the submitted application state.
- Seven targeted portable, lifecycle, XML, and exact-XSD tests pass locally; Ruff format and lint pass.
- No SF-424C-specific runtime, compiler, loader, renderer, or adapter branch was added, and production registration remains unchanged.
- Catalog browser/print evidence is being produced by the shared catalog-matrix task. Human semantic, instruction, accessibility, policy, and release approval remain open and must not be inferred from these automated receipts.

[depends on](migrate-sf424c-parity-oracle.md)

[depends on](add-portable-form-preview-registration.md)

[depends on](run-portable-catalog-browser-matrix.md)

[depends on](build-uniform-legacy-differential-parity.md)

[depends on](enforce-evidence-backed-parity-deltas.md)

## Declarative Table closure — 2026-08-24

- Producer PR [mikec-ai/grants-form-spec#95](https://github.com/mikec-ai/grants-form-spec/pull/95) merged as `d75d511d19f5c790442049d7ed6b1aa47949982f` at `2026-08-24T23:53:38Z`.
- The generic SGG Table projector now derives columns, rows, cell paths, monetary display, and input/read-only state from a regular object-of-objects model. SF-424C supplies only its form-local table heading; no form-id branch or copied 16-row generator was added.
- The producer's complete preflight passed: 124 TypeSpec tests, 346 Python tests with 10 skips, 30 exact-XSD fixtures, 1,536 validated artifacts, and zero unclassified field occurrences or exceptions.
- Consumer PR [mikec-ai/simpler-grants-gov#97](https://github.com/mikec-ai/simpler-grants-gov/pull/97) pins the merged producer revision and recursively projects nested Table cell definitions through the existing canonical-to-Simpler rename map. The generated 16-row, four-column SF-424C UI artifact passes Simpler's frontend AJV contract and focused Table/FormFields tests.
- Local consumer receipts: 35 focused projection, SF-424C, integrity, and provenance tests passed; 48 frontend Table, UI-schema, and FormFields tests passed. Five additional legacy calculation tests require the local `grants-db` service and were unable to initialize outside the composed environment.
- Bounded four-browser run [32791482621](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32791482621) is executing at consumer head `c954ec151dd0838917d8d8457305cffa0281e4ee`. Do not claim browser closure until its receipts are read.
- Production registration remains unchanged. Human semantic, instruction, accessibility, policy, and release approvals remain open.
