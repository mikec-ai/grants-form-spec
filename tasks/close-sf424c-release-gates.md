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
  at: '2026-08-25T00:31:46.020Z'
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
- Consumer PR [mikec-ai/simpler-grants-gov#97](https://github.com/mikec-ai/simpler-grants-gov/pull/97) merged as `82912c5de7315bc6bb0e13ed589c8264c919c0cc` at `2026-08-25T00:11:33Z`. It pins the merged producer revision and recursively projects nested Table cell definitions through the existing canonical-to-Simpler rename map. The generated 16-row, four-column SF-424C UI artifact passes Simpler's frontend AJV contract and focused Table/FormFields tests.
- Local consumer receipts: 35 focused projection, SF-424C, integrity, and provenance tests passed; 48 frontend Table, UI-schema, and FormFields tests passed. Five additional legacy calculation tests require the local `grants-db` service and were unable to initialize outside the composed environment.
- Bounded browser run [32791681432](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32791681432) passed at the exact rebased consumer head `bc3da014971c2ffec80f55b5498434210e6ddd22`: four `@portable-catalog` probes passed against only `sf424c` in 1.4 minutes after the hosted application environment started. The run created the SF-424C preview opportunity/application, rendered the generated Table through the real frontend, and completed without an SF-424C-specific runtime branch.
- Broad API run [32791671803](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32791671803) completed after the merge with 4,714 passing tests, one skip, and six failures. None involved SF-424C, Table projection, or the generic adapter: one R&R Budget source-promotion assertion retained the earlier producer revision `fbb2554f...` instead of the correctly pinned `d75d511d...`, and five failures were fully-populated lifecycle validations across the R&R Budget family. These are concurrent R&R Budget follow-up defects, not evidence against the SF-424C table closure; no SF-424C production code was changed in response.
- Production registration remains unchanged. Human semantic, instruction, accessibility, policy, and release approvals remain open.
