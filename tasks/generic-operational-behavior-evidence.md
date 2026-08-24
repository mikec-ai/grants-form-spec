---
type: Task
title: Model generic operational behavior evidence
priority: P1
description: >-
  Represent prefill, protected/read-only, and externally derived behavior
  generically and project it into analysis.
superbee_progress_status: in_progress
superbee_updated_by: implement_operational_evidence
generated:
  by: 'process:superbee'
  at: '2026-08-24T04:30:52.725Z'
assignee: implement_operational_evidence
---
# Goal

Design a generic, portable evidence representation for non-rule operational field behavior such as prefill, read-only/protected presentation, and externally derived values, then project that evidence into portfolio analysis without form-specific compiler or analyzer branches.

# Starting evidence

R&R Personal Data provides a bounded canary: its five PD/PI name fields are identified by the official DAT as `Forward-populated` from R&R SF-424 fields 14-1 through 14-5, and the pinned official XFA initializes each field from an R&R SF-424 value before setting its access to `protected`. These records remain source-bound and uncompiled in the current form audit.

# Acceptance criteria

- Define a generic evidence vocabulary that distinguishes operational behavior from calculations and conditions.
- Represent source and destination paths, operation kind, editability/protection, execution status, and exact source provenance without embedding form-specific logic.
- Project the evidence into analysis so prefill and protected-field dependencies are visible and filterable.
- Preserve the existing behavior-evidence contract until the generic design is reviewed.
- Add contract, projection, and negative tests; do not infer runtime behavior from source wording.

[depends on](correct-rr-personal-data-source-parity.md)

# Bounded design review

## Finding

The current `behaviorEvidence` contract is deliberately rule-specific: every record is a `calculation` or `condition`, and `project_evidence.mjs` reconciles compiled records against the SGG rule and UI projections. Non-rule operational semantics currently fall into three disconnected places:

- source audits, where they are durable but not contract-governed or projected into analysis;
- canonical presentation/response-role declarations such as `@UI.readOnly` and `ResponseRole.systemValue`, which describe shape and interaction but not source-backed population or lifecycle semantics; and
- target declarations such as `@Sgg.prePopulate`, which can emit runtime rules without an exact evidence disposition.

Do not broaden `behaviorEvidence.ruleKind`. That would weaken its exact rule-target closure and conflate source evidence with runtime behavior. Add one sibling array, `operationalBehaviorEvidence`, to `grants-form-evidence/v1`.

## Smallest recommended record

Each record should remain occurrence-qualified and atomic:

```json
{
  "canonicalPath": "/projectDirector/name/firstName",
  "operationKind": "prefill",
  "valueSource": {
    "kind": "canonical",
    "blockId": "rr-sf424",
    "path": "/projectDirector/name/firstName"
  },
  "editability": "protected",
  "authority": "official_source",
  "executionStatus": "source-bound-uncompiled",
  "sourceId": "rr-personal-data-dat-f357",
  "sourcePath": "01-02",
  "sourceRecord": "Forward-populated from the identified R&R SF-424 field."
}
```

Use these initial closed vocabularies:

- `operationKind`: `prefill`, `external-derived`, `discard`, `replace`.
- `valueSource.kind`: `canonical` or `external`. A canonical source requires `blockId` and `path`; an external source requires a stable `namespace` and `path`. `discard` may omit `valueSource`; `replace` requires one.
- `editability`: `editable`, `read-only`, `protected`, `not-applicable`. This is a separately inspectable facet, not a substitute for `operationKind`.
- `executionStatus`: initially preserve only `source-bound-uncompiled` and `adapter-projected`. The latter means an adapter artifact contains the operation; it does not claim the runtime executed it. Add a stronger `runtime-verified` state only when a cross-system conformance test exists.
- `authority`: reuse `official_source`, `implementation_parity`, and `unresolved`, with the same source-type restrictions as rule evidence.

Keep `sourcePath` for the exact evidence location and `valueSource.path` for the value dependency. This avoids the current ambiguity between provenance and data flow. Do not put conditions or free-form executable expressions into this record. Context-dependent discard/replace semantics remain source-bound until the existing condition vocabulary can express their trigger.

## Pipeline change

1. Extend `contract/v1/evidence.schema.json` with the optional sibling array and discriminated `valueSource` shapes. Leave `behaviorEvidence` unchanged.
2. In `project_evidence.mjs`, reuse the existing source-authority checks, require every destination `canonicalPath` to match an exact emitted field occurrence, and fail closed on malformed or dangling canonical value sources. This is generic artifact validation, not runtime compilation.
3. Pass the records through to emitted `evidence.json`; do not generate SGG rules from evidence.
4. In `analyze.py`, emit `operationalBehaviorOccurrences` plus `operational-behavior-occurrences.csv` with form, destination, operation, source coordinate, editability, authority, execution status, and evidence coordinate. Keep these rows out of published semantic-coverage and marginal-reuse metrics until their identity/review policy is explicitly accepted.
5. Do not add form-specific compiler, projector, or analyzer branches.

## Migration surface

Start with source-backed canaries rather than bulk-inference:

1. R&R Personal Data: five PD/PI name destinations. One atomic prefill record per field can carry `editability: protected`; the existing audit already pins the exact DAT and XFA evidence.
2. PHS 398 Cover Page Supplement: the multi-project program-income discard and system-summary replacement statements. Preserve them as source-bound until their application-context predicate and summary source are declarative.
3. SF-424D family: prefilled title and applicant-organization roles after their exact field coordinates and source provenance are reconciled.
4. Audit existing `@Sgg.prePopulate`, `ResponseRole.systemValue`, and `@UI.readOnly` occurrences as candidates only. Do not auto-promote declarations into official-source evidence.

Question-bank operational inheritance is intentionally deferred. The current canaries are form-occurrence semantics, and adding inheritance before a repeated source-backed case would increase the contract surface without evidence.

## Required tests

- Contract positives for canonical prefill, external-derived, protected, discard, and replace records.
- Contract negatives for missing destination, missing provenance, invalid source discriminator, missing canonical `blockId`/`path`, missing external `namespace`/`path`, replace without a source, and any unknown operation/editability/status.
- Projector negatives for destination paths that are not exact emitted occurrences, missing evidence source IDs, authority/source-type mismatch, and dangling canonical source coordinates.
- Projector positive showing unchanged passthrough and no runtime-rule generation.
- Analysis fixture proving stable JSON and CSV rows and proving operational rows do not change question similarity, reviewed coverage, or marginal behavior metrics.
- Canary assertions for all five R&R Personal Data name paths, exact provenance, protected editability, and `source-bound-uncompiled` status.

## Sequencing recommendation

Implement this small contract-and-projection slice before the next form whose parity claim depends on prefill, protected/read-only population, external derivation, discard, or replacement. It need not block forms that add only schema, presentation, mappings, calculations, or conditions. The design is ready for implementation, but the task should remain `todo` until an implementer claims it.
