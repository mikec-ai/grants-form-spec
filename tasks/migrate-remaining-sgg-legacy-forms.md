---
type: Task
title: Migrate the remaining four SGG legacy forms
superbee_progress_status: in_progress
priority: P1
description: >-
  Migrate four legacy-only Simpler forms after uniform parity machinery is
  ready; EPA Key Contacts is not yet portable or banked and is the named
  later-candidate oracle migration.
actor: Codex
timestamp: '2026-08-23T22:26:31.600Z'
superbee_updated_by: codex
assignee: personal_data_closure
---
# Goal

Migrate the four SGG legacy forms that remain outside the portable catalog after the current expansion tranche:

- EPA Form 4700-4;
- EPA Key Contacts;
- Project Abstract, distinct from Project Abstract Summary;
- Supplementary NEH Cover Sheet.

# Delivery approach

Treat each form as a source-evidenced portable definition, use the legacy implementation as a compatibility oracle, and route all differences through the intentional-delta gate. Reuse canonical questions and compositions where semantics genuinely match; preserve form-local concepts where they do not.

# Acceptance criteria

- Each form has authoritative source evidence, generated artifacts, and producer contract gates.
- Each form passes SGG artifact-bank, schema/rules/XML, browser/lifecycle, locked/print, and applicable XSD gates.
- Portable-versus-legacy parity receipts and any intentional deltas are complete.
- No form is production-registered without a separate human release decision.

[depends on](build-uniform-legacy-differential-parity.md)

[depends on](enforce-evidence-backed-parity-deltas.md)

## Active isolated slice — EPA Key Contacts

The `personal_data_closure` lane claimed the smallest non-overlapping slice on 2026-08-25: EPA Key Contacts only. Project Abstract remains independently owned; EPA 4700-4 and the Supplementary NEH Cover Sheet remain outside this slice.

Producer PR [grants-form-spec #110](https://github.com/mikec-ai/grants-form-spec/pull/110) merged on 2026-08-25 at `5e7f6d3fd2aaa8c150477c460d3731055bd72594` (reviewed head `cea50b88e06bace76faf7344e9b82825b0907d30`). The merged isolated source/declarative/XML slice includes:

- exact official v2.0 XSD, DAT, read-only PDF, XFA PDF, GlobalLibrary V2, and UniversalCodes V2 identities and hashes are pinned;
- one role-qualified contact composition serves Authorized Representative, Payee, Administrative Contact, and Project Manager;
- all 36 exact DAT runtime effects remain machine-readable as `source-bound-uncompiled`, including four explicitly unresolved initial-active/post-blur State transitions;
- all semantic mappings remain `proposed`, accepted mappings remain zero, and published coverage is not increased;
- implementation-derived analysis reports five reused question blocks, zero new question blocks, and 24 exploratory associations;
- one source-identical `ContactPersonDataTypeV3` mapping projects all four roles, preserving exact XSD sequence, namespaces, optional-role behavior, and the official `AdminstrativeContact` wire spelling;
- the byte-identical root XSD fixture hashes to `157a9c8a21cdc39b4c6b5df94c3745ecd4f174cb390187441de862fb35b50b01`;
- full producer preflight passed locally: 125 TypeSpec tests, 377 Python tests (10 skipped), exact-XSD fixture, evidence, artifact, classification, package, and analysis gates.

This receipt proves the producer-side source contract, declarative composition, generic XML projection, differential wire compatibility, and exact-XSD conformance only. Consumer registration, save/reload/browser/lifecycle parity, accessibility, privacy/policy, operations, human semantic review, and production release remain separate gates. No consumer branch was created by this lane.

## Behavior closure classification

Producer PR [grants-form-spec #112](https://github.com/mikec-ai/grants-form-spec/pull/112) merged at `59efac07a205b92aee76b6c0f3f12918356c9380` on 2026-08-25. It records the bounded behavior plan and first evidence correction:

- eight U.S.-specific State/ZIP requiredness effects are exact emitted targets of the existing generic `requiredPathWhen` contract and are now marked compiled;
- 24 any-present role-completeness effects already have standard optional-object/required-descendant JSON Schema representation, but remain source-bound-uncompiled until generic evidence recognition and an unregistered consumer validation/initial-render receipt exist;
- four State initial-active/post-Country-exit interaction effects remain unresolved because the current value-only condition contract has no event trigger or distinct initial effect;
- the two honest choices are an event-aware generic interaction extension or a separately reviewed intentional timing delta. No form-specific branch is permitted.

The plan is pinned at `research/epa-key-contacts/behavior-closure-plan.md`. Full local producer preflight passed with 125 TypeSpec tests and 380 Python tests (10 skipped); both hosted checks (`form-spec` and `proof-package`) passed before merge. Semantic mappings remain proposed and accepted mappings remain zero.

## Generic optional-object evidence closure

Producer PR [grants-form-spec #113](https://github.com/mikec-ai/grants-form-spec/pull/113) merged on 2026-08-25 at `7c3be8e32968b49b5ce48f53a832c00220eb5bee` from reviewed head `1523fed603e1e121f4d77aa84b161bfe8b947e16`.

- the evidence projector now generically recognizes exact required descendant leaves beneath optional object occurrences;
- the verifier resolves local and external `$ref` composition, merges unconditional `allOf` constraints, requires an exact emitted occurrence, and only recognizes targets explicitly claimed as compiled;
- positive and fail-closed tests prove a referenced optional object is recognized, an unclaimed rule creates no evidence obligation, a wrong descendant is rejected, and a required root object is not misclassified;
- the change contains no EPA, role, contact, form-ID, compiler, or consumer-adapter special case;
- 24 any-present role-completeness effects are now exact compiled producer targets, bringing EPA Key Contacts to 32 compiled effects total;
- exactly four State initial-active/post-Country-exit timing effects remain `source-bound-uncompiled` and unresolved;
- semantic review remains `proposed`, accepted mappings remain zero, and consumer registration remains absent.

Exact verification receipts: full local producer preflight passed with 125 TypeSpec tests, 387 Python tests (10 skipped), 8 XML projection tests, 321 validated blocks, 1,721 validated artifacts, and 43 projected evidence sidecars. Hosted `proof-package` run `32855602146` passed; hosted `form-spec` run `32855602057` passed in 2m7s. The separate unregistered consumer schema/initial-render receipt remains the next bounded integration gate and must not register the form.

## Merged unregistered consumer receipt

Private-fork consumer PR [simpler-grants-gov #118](https://github.com/mikec-ai/simpler-grants-gov/pull/118) merged on 2026-08-25 at `000eb82a02e751733e9c8375c030f9ba9c3c1e92` from reviewed head `b05ebf58f3c473c97cc95455ebb4419be5f01048`, rebased on attachment-lifecycle baseline `95fcbf5273c9093a494307b5125b87b8284df488`.

- the exact producer merge `7c3be8e32968b49b5ce48f53a832c00220eb5bee` is additively banked as the 43rd form with `registrationChanged: false`;
- `runtime_identity("epa-key-contacts")` and `load_form("epa-key-contacts")` both remain fail-closed, while the private bank projector and preview builder load the package without XML enablement;
- all four optional roles accept absence, reject a partial role containing only an optional field, expose the same six source-required leaf constraints, and accept a complete non-U.S. role;
- all four U.S. roles require State and ZIP through the emitted schema;
- initial preview rule processing leaves `{}` unchanged and does not materialize Authorized Representative, Payee, Administrative Contact, or Project Manager objects;
- evidence remains exactly 32 compiled effects, four unresolved `source-bound-uncompiled` timing effects, semantic review `proposed`, and zero accepted mappings.

The additive promotion exposed an exact-source issue: Simpler's existing `EPA_KeyContacts_2_0-V2.0.xsd` had LF-normalized bytes (`2321d483...`) while the official producer fixture preserves CRLF bytes (`157a9c8...`). The XML content was otherwise identical. The branch replaces the tracked XSD with the producer-pinned official byte-identical fixture; existing integrity and non-database legacy EPA XML checks pass.

This was intentionally a one-time full-CI admission because the exact producer pin also advanced existing R&R Personal Data artifacts and shared personal-data question blocks. The fail-closed classifier remained unchanged and correctly selected `full`. The explicit CI-map entry now means subsequent EPA-local artifact/test changes qualify for `portable_focused`; unrelated producer-pin deltas still fail closed.

Exact consumer receipts:

- local source-promotion, EPA, and classifier suite: 39/39 passed; targeted Ruff lint and format passed;
- hosted API run `32866467828`, job `97862954632`: full format, lint, migrations, and security passed; the 4,805-item suite completed with 4,803 passed and two skipped, and the job passed in 20m44s;
- hosted E2E run `32866468174`: shards 1/4, 2/4, 3/4, and 4/4 passed in 12m23s, 19m6s, 20m32s, and 15m54s respectively; merged-report job `97871059362` passed in 45s;
- exact XSD SHA-256 remains `157a9c8a21cdc39b4c6b5df94c3745ecd4f174cb390187441de862fb35b50b01`;
- registrations, runtime identities, and projections remain unchanged; EPA remains deliberately unregistered;
- evidence remains 32 compiled effects and four unresolved timing effects; semantic review remains proposed with zero accepted mappings.
