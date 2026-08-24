---
type: Task
title: Reconcile SF-424 family portable cutover deltas
priority: P0
description: >-
  Resolve the producer, declaration, and reviewed compatibility differences
  exposed by PR63 while production remains fail-closed on legacy definitions.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T05:10:56.424Z'
assignee: codex-cardinality-emitter
---
# Goal

Resolve the portable-versus-legacy schema and validation deltas exposed when consumer PR #63 temporarily made SF-424, SF-424 Short, and SF-424A production-active. Keep the three portable candidates banked and previewable while production stays on the legacy definitions until each delta is mechanically fixed or explicitly reviewed as intentional.

# Incident evidence

- Consumer PR #63 head `44a217345868ed15192431ee755c9f41febcc8b7` consumed producer revision `14b08b8cbd6016778a8f0688ed924a7ede4c8d2d` and produced 12 relevant API test failures across the three forms. The failures collapse to three root causes; repeated fixtures amplify the same field-level differences.
- Consumer PR #65 began by restoring the three legacy definitions for production while preserving the portable bank, adapter, and preview seam. Its current head `1f2f47f164674e91904d7392978ae58c63c5936d` also closes a CI-classifier gap: the lightweight additive lane had allowed modifications to existing portable artifacts and XSDs, while those changes can alter already-banked behavior. Existing artifact or XSD modifications now require full CI; only strictly additive files qualify for the lightweight lane. Both changes are the correct fail-closed disposition.
- The legacy implementation is a compatibility oracle, not semantic authority. The SF-424A evidence records cited below are still `proposed`, so they cannot yet authorize an intentional production delta.

# Root-cause classification

## A. Duplicate applicant-address validation: producer generic emitter defect

SF-424 and SF-424 Short each compose `primary-org/address`. The published question block already owns three unconditional required paths and two USA-conditional required paths. `cardinalityAnnotations()` in `typespec-form-spec/src/emitters/overlay.ts` recursively copies those same model-level decorators beside the form occurrence `$ref`, so SGG receives two identical validators and reports each missing address field twice.

Correct this in the producer's generic emitter. A reference to a separately published question must retain the question's intrinsic cardinality only in the referenced block. The form occurrence may add only decorators declared on that occurrence. Do not deduplicate validation errors in SGG and do not add form-id branches.

## B. SF-424 Short pre-population versus JSON Schema `readOnly`: producer declarative decision

The producer declaration applies both `@Sgg.prePopulate` and `@UI.readOnly` to six fields: agency name, Assistance Listing number/title, opportunity number/title, and SAM UEI. The legacy SGG oracle hides all six through pre-population UI rules but reserves JSON Schema `readOnly` for the three submission-populated outputs.

This is not an adapter transformation defect. Review the intended portable meaning of `readOnly` separately from the SGG capture mechanism. If legacy behavior is intended, remove the six `@UI.readOnly` declarations in `specs/forms/sf424-short.tsp` while preserving `@Sgg.prePopulate`. If the portable distinction is intentional, record it as a narrow reviewed delta with evidence before cutover. Do not teach the adapter that pre-population implies or removes `readOnly`.

## C. SF-424A optional blank narratives: unresolved semantic delta, then a generic adapter choice only if required

The portable bank defines direct-charge explanation, indirect-charge explanation, and remarks as optional properties whose present values have minimum length 1. The legacy SGG payload convention persists absent values as empty strings and its schemas allow minimum length 0. The producer evidence sidecar ties the 1-character minima to the pinned XSD, but all three mappings remain `proposed` rather than reviewed.

Do not weaken the shared bank questions solely to satisfy legacy fixtures. First review the exact XSD mappings and choose between: (1) retain canonical `minLength: 1`, normalize absent SGG optional text to omission through one generic, declaratively governed adapter policy, and record an accepted legacy delta; or (2) preserve empty-string compatibility through a narrow declarative projection override implemented by a generic adapter capability. Adding `minLength: 0` beside a `$ref` cannot weaken the referenced constraint and is not a valid fix. Any override must target exact paths, carry a reason and review reference, fail on stale paths, and contain no SF-424A branch in Python.

# Minimal correction sequence

1. Land PR #65 independently after its full CI is green. Production remains legacy; portable candidates remain banked and previewable; modifications to existing artifact or XSD files continue through full CI.
2. Fix producer cardinality emission generically, rebuild artifacts, promote the immutable producer revision, and prove one validation issue per missing address path in both forms.
3. Resolve and encode the SF-424 Short read-only decision in producer declarations or the governed intentional-delta ledger; keep pre-population behavior unchanged.
4. Complete semantic review of the three SF-424A XSD mappings. Only then implement the selected generic SGG compatibility behavior or accept the canonical delta.
5. Rerun the same legacy differential suite plus preview/browser receipts. Production cutover is a separate reviewed change after all applicable deltas are resolved or accepted.

# Acceptance criteria

- Producer tests prove that a published question retains intrinsic required/conditional rules while a composing form does not duplicate them, and that explicit occurrence-level narrowing still emits beside the reference.
- SF-424 and SF-424 Short validation receipts contain one error per missing applicant address path, not duplicates.
- SF-424 Short tests independently assert the six pre-population bindings, null UI fields, and the reviewed JSON Schema `readOnly` set.
- SF-424A tests exercise omitted, empty, and nonempty values for all three narrative fields at the canonical producer boundary and the SGG boundary; the chosen difference is represented as reviewed data, not form-specific adapter control flow.
- Differential receipts identify producer revision, consumer revision, form, path, expected/actual behavior, disposition, evidence status, and review state.
- CI classifier tests prove that new additive artifacts may use the lightweight bank lane, while any modification or deletion of an existing artifact or XSD selects full CI. This classification is an architectural parity gate, not merely an optimization.
- No production registration changes accompany the producer or adapter corrections; a later cutover remains fail-closed and separately approved.

# Boundary

No HHS upstream writes. Do not edit or merge PR #63 or PR #65 from this task. Similar behavior is not semantic equivalence, and proposed evidence does not count as reviewed acceptance.

# Producer correction receipt

- Draft producer PR [mikec-ai/grants-form-spec#72](https://github.com/mikec-ai/grants-form-spec/pull/72), exact head `06a7f875b1f32702591531109ec4fd4a5b9e8761`, implements root cause A only.
- The generic emitter now stops recursive cardinality projection at published question boundaries while preserving decorators declared directly on a form occurrence. No form-id or consumer branches were added.
- A generic TypeSpec regression proves intrinsic question cardinality stays in the question and explicit occurrence narrowing remains beside the form reference. Emitted-artifact tests prove SF-424 and SF-424 Short reference `primary-org/address` without copying its `required` or conditional `allOf` branches.
- Full producer preflight passed on base `ec2c34f0a8d5dceeb0043dff13378457b0b5242f`: 116 TypeScript tests, 290 Python tests with 2 skipped, artifact validation, promotion validation, exact-XSD fixture checks, package creation/verification, analysis, independent TypeSpec compilation, and the classified-field gate.
- The task remains in progress because the SF-424 Short `readOnly` decision and SF-424A optional-blank semantic review are intentionally unresolved.
