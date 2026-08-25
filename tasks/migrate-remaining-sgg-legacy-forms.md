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
