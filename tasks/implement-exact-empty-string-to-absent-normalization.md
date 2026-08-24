---
type: Task
title: Implement exact empty-string-to-absent input normalization
priority: P0
description: >-
  Producer step is implemented in draft grants-form-spec PR #74 at head
  6589465b08f72fe07e26f7e77ba6be621dc44552. Full local preflight and hosted CI
  are green. The versioned exact-path policy, reviewed SF-424A evidence, generic
  fail-closed projector, manifest hash, and test matrix are complete. Consumer
  execution before canonical validation and XML remains pending, so the
  cross-repository task stays in progress.
superbee_progress_status: in_progress
superbee_updated_by: codex-operational-evidence
generated:
  by: 'process:superbee'
  at: '2026-08-24T05:35:50.538Z'
assignee: codex-operational-evidence
---
# Goal

Introduce one narrowly scoped compatibility capability for source-optional string fields whose legacy capture representation is the exact empty string. The portable form package declares the affected occurrence paths. Generic consumers convert exact empty strings to absent properties before canonical validation and XML projection. The SF-424A Other Information fields are the first source-audited canary.

# Contract

Add a versioned portable sibling artifact named response-normalization.json and include its content hash in the package manifest. Initial contract identifier: grants-form-response-normalization/v1.

The artifact contains an operations array. Each operation has:

- path: an RFC 6901 exact JSON Pointer into the resolved canonical response schema. No globs, form identifiers, name matching, or inference.
- operation: the closed enum value empty-string-to-absent.
- evidenceRef: a stable reference to reviewed source evidence in the package evidence artifact.

The first declaration contains exactly these paths: /directChargesExplanation, /indirectChargesExplanation, and /remarks.

The canonical question and form schemas remain authoritative. These fields stay optional and retain minLength 1. The normalization artifact describes a compatibility transformation at the input boundary; it does not redefine semantic validity.

# Producer/compiler rules

The generic compiler validates every declaration against the fully resolved canonical schema and fails closed when:

- the JSON Pointer is malformed, stale, duplicated, or does not resolve to a property;
- the target is required, is not a scalar string, permits null, or permits the empty string;
- the path traverses an array or requires wildcard semantics in v1;
- the operation is unknown;
- evidenceRef is missing, unresolved, or not reviewed;
- the emitted artifact is absent from or mismatched with the manifest hash.

The compiler contains no form IDs or SF-424A path lists. The form declaration owns the three paths. Shared question-bank entries are not weakened.

# Consumer pipeline

The SGG adapter loads and validates the versioned artifact generically with the rest of the immutable package. After any transport-to-canonical key projection, but before canonical JSON Schema validation, rules evaluation, or XML mapping, it applies operations to a copied response object.

For empty-string-to-absent, delete the exact declared property only when its value is exactly the zero-length string. Do not trim. Preserve strings containing spaces, tabs, or line breaks. Do not convert null, false, zero, arrays, or objects. Do not mutate the stored/raw payload. Reapplying the operation is idempotent.

Canonical validation still rejects a direct present empty string. The compatibility entry point accepts the legacy payload by first producing the omission-only canonical representation. XML projection receives only the normalized, canonically validated object. Existing generic XML omission logic must emit no empty child and must omit the OtherInformation wrapper when all three children are absent.

# Tests

Producer contract and compiler:

- accept the three reviewed SF-424A exact paths and emit a deterministic, manifest-hashed artifact;
- reject unknown operations, malformed or duplicate pointers, missing paths, required properties, non-string targets, nullable targets, schemas that already allow empty strings, array traversal, missing evidence, and unreviewed evidence;
- prove generic behavior with an arbitrary synthetic form identity so no form branch can be hidden in the compiler.

Canonical boundary:

- omission passes;
- direct empty string fails minLength 1;
- non-empty and exact whitespace strings retain existing schema behavior;
- null and over-limit values fail normally.

Adapter:

- each declared empty string is independently removed;
- all three empty strings become three omissions;
- mixed empty and non-empty values preserve non-empty values;
- whitespace is byte-preserved;
- null is not normalized and fails canonical validation;
- execution is idempotent and does not mutate its input;
- an undeclared empty-string path remains present and fails canonical validation;
- stale, malformed, unsupported, or unhashed artifacts fail package loading rather than being ignored;
- a synthetic package proves the adapter has no SF-424A or form-ID branch.

XML and differential proof:

- all three absent produces no OtherInformation wrapper;
- one non-empty value produces only its exact source child;
- no case emits an empty XML element;
- generated XML validates against the pinned SF-424A XSD;
- the legacy fixture containing three blank strings is accepted only through the compatibility entry point and its canonical result contains omissions;
- the conformance receipt pins producer and consumer revisions plus the reviewed policy disposition.

# Cross-repository sequence

1. Producer PR in mikec-ai/grants-form-spec: add the versioned artifact contract, generic compiler validation, SF-424A declarative canary, deterministic package emission, and focused tests. Keep generated conformance outputs as CI artifacts, not runtime source.
2. Consumer PR in mikec-ai/simpler-grants-gov: consume an exact producer revision, add the generic loader/executor at the pre-validation boundary, preserve raw payloads, and add adapter/XML/differential tests. Do not add production registrations and do not open against HHS upstream.
3. Cutover PR in the consumer fork only after this task and the remaining SF-424 family cardinality and read-only deltas are resolved: update the pinned package, publish the conformance receipt as a build artifact, then explicitly promote SF-424A.

# Acceptance criteria

- The portable declaration is the sole source of path-specific policy.
- Neither producer compiler nor SGG adapter contains a form ID or form-specific path branch.
- Exact empty strings normalize to omission only at declared reviewed paths and only before canonical validation and XML projection.
- Whitespace is preserved and canonical schemas still reject present empty strings.
- All negative contract checks fail closed.
- Producer and consumer focused suites and repository preflight pass.
- The SF-424A source audit remains linked to this delivery through the reconciliation task.
