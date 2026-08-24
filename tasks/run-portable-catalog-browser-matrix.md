---
type: Task
title: Run the banked portable catalog through browser conformance
superbee_progress_status: in_progress
priority: P0
description: >-
  Generate manifest-driven real-frontend browser and lifecycle conformance for
  every currently banked portable form.
actor: Codex
timestamp: '2026-08-23T22:26:31.124Z'
superbee_updated_by: Codex-browser-matrix
---
# Goal

Run every form selected by the consumer's verified portable artifact manifest through Simpler's real application-form and print frontend, without production registration or form-specific runtime code. The suite must always use the manifest's live selection rather than pinning a portfolio count in source or durable planning language.

# Dependency and safety boundary

- Depends on the lower-environment preview registry introduced by draft consumer PR 63. Do not edit or duplicate that PR in this task.
- Enable both `ENABLE_PORTABLE_FORM_PREVIEW` and an allowed `local`, `test`, or `dev` environment. Refuse to seed or run otherwise.
- Use PR 63's deterministic preview UUIDs and ordinary form registry. Do not add runtime identities, `FormType` values, instructions, or production registrations.
- Exercise the existing application-form route, `ApplyForm`, save API, reload route, and print route. Do not build a second renderer or a preview-only frontend component.
- Keep XML conformance outside this renderer/lifecycle matrix; exact-source XSD and XML lifecycle gates remain separate.

# Smallest high-leverage design

## 1. Generate one catalog plan

Generate a temporary `portable-browser-plan.json` at test setup from the verified `artifact-manifest.json` selection. For each form, read its resolved manifest, JSON Schema, SGG UI schema, and SGG rule schema and record:

- portable form id, deterministic preview UUID, form name/version, and artifact digests;
- counts and stable paths for UI nodes and schema fields;
- mechanically detected capabilities: editable scalar, required field, `fieldList` repeater, attachment widget/rule, conditional UI state, `readOnly`, and executable `gg_pre_population` calculation;
- the exact planned probes and explicit not-applicable reasons.

Capability discovery must be generic tree walking over declared artifacts. A new banked form changes the plan without editing a TypeScript form list or adding a form-name branch.

## 2. Seed through the real registry

Add one fail-closed local/test seed seam that creates a deterministic opportunity and competition containing every preview UUID from the generated plan, then creates a normal application through the existing application service. Prefer one application with all preview forms so authentication and application setup are paid once. The seeder must verify that the set of created `ApplicationForm` records exactly equals the manifest selection.

The seed seam is test infrastructure only. It may create competition/application rows, but it must not mutate the production registration manifests or make preview forms discoverable when the two-part preview gate is off.

## 3. Run a staged capability matrix

Stage A is exhaustive for every selected form:

- load the ordinary application-form URL and assert the expected form heading;
- assert every UI definition resolves before navigation, the page has no `Error rendering form` alert, and no uncaught page error or failed form API request occurs;
- save the initial response through the ordinary action, reload, and verify the saved response is stable (validation warnings are recorded, not mistaken for renderer failure);
- load the ordinary print URL and verify the form heading, static/locked rendering, and absence of print diagnostics;
- run browser axe against the rendered form and verify an essential keyboard focus target when the plan contains an editable control.

Stage B runs only when the generated capability fingerprint says it applies:

- repeater: add one item, edit a supported child, save/reload, then remove it;
- attachment: upload the existing small PDF fixture, save/reload, and verify the persisted filename in print;
- conditional: use the declared predicate's trigger path/value and verify target visibility, interaction, or required state in both states;
- calculation: populate declared source operands with schema-valid numbers and verify the declared output after save/reload;
- read-only: verify each declared protected field is non-editable in apply and print.

Start implementation with Stage A plus one generic probe for each Stage B capability. Expand the same generic executors across every applicable form only after those canaries prove the harness. No executor may switch on form id or form name.

## 4. Keep semantic vectors portable

Schema constraints can safely synthesize simple structural probe values. They cannot prove semantically valid minimal or maximal submissions for every form. Do not infer those payloads in SGG fixtures.

Where a minimal-valid, boundary/maximal-valid, conditional, or calculation probe cannot be derived unambiguously from the portable artifacts, add a versioned declarative conformance-vector sidecar to the producer package. It should contain JSON payloads and expected portable outcomes, not SGG locators or Python/TypeScript logic. The consumer matrix mechanically consumes that sidecar. A missing required vector is `inconclusive`, not a passing skip; the receipt identifies the missing declaration.

# Receipts and ownership classification

Emit receipts as CI build artifacts rather than tracked runtime files. Produce one JSON receipt per form plus a catalog summary containing:

- consumer commit, manifest digest, form artifact digests, browser/project, and preview UUID;
- each planned capability with `passed`, `failed`, `not_applicable`, or `inconclusive` status and evidence such as route, schema path, screenshot/trace attachment names, and duration;
- validation-warning counts separately from harness failures;
- the first failed boundary and ownership classification.

Classify by boundary, not by stack-trace guesswork:

1. `producer_content`: artifact integrity, portable contract/self-consistency, or declarative vector failure before SGG projection;
2. `adapter`: portable inputs are valid but loading, projection, preview registration, or API round-trip changes or loses them;
3. `shared_runtime`: the API exposes the expected projected contract but the real apply/save/reload/print frontend fails it;
4. `harness_inconclusive`: authentication, seed, environment, timeout, or missing-vector failure. This never counts as a pass or as product ownership.

Every product failure must resolve to one of the first three. Infrastructure uncertainty remains explicit rather than being falsely assigned.

# Acceptance criteria

- The dependency PR is merged and its exact preview gating remains intact.
- The plan's form set exactly matches the verified manifest selection; changing the selection changes generated Playwright cases without source edits.
- Every selected form has an attributable Stage A receipt from the real apply and print frontend.
- Every mechanically declared capability has either a passing applicable probe, a precise `not_applicable`, or a blocking `inconclusive` that names the missing portable vector.
- At least one repeater, attachment, conditional, calculation, and read-only canary passes through the generic Stage B executors before catalog-wide Stage B expansion.
- There are no form-id/name branches in the plan generator, seeder, or capability executors.
- Production runtime identities and registrations are byte-for-byte unchanged.
- Receipts, screenshots, traces, and summaries are uploaded as build artifacts and are not committed to the runtime repository.
- The catalog release gate fails on `failed` or `inconclusive`; ordinary artifact-only banking remains on the existing lightweight lane and does not run this expensive matrix per form.

# Delivery sequence

1. Merge and pin the preview-registry dependency.
2. Implement plan generation, fail-closed seeding, Stage A, receipts, and ownership phases.
3. Implement one generic canary for each Stage B capability.
4. Add only the portable conformance vectors that generic derivation cannot supply.
5. Expand Stage B across the manifest and publish the first complete catalog summary.

# Current reuse points

Reuse the existing Playwright authentication/application helpers, form navigation, save/status utilities, attachment fixture and upload path, print helpers, `ApplyForm` and `PrintForm` routes, lifecycle utilities, and existing jest-axe conventions. Consolidate receipt/event capture once instead of copying the current form-specific `loadOpportunityConfig` and field-definition registries.

[depends on](add-portable-form-preview-registration.md)

# Implementation progress

The first consumer slice is implemented on a clean branch stacked on the exact preview dependency head. It provides the manifest-driven projected-artifact plan, deterministic lower-environment seed competition, Stage A Apply/save/reload/print/accessibility matrix, boundary-owned receipts, and CI-only receipt/screenshot/trace publication. The live execution receipt currently selects 39 forms; that count remains execution evidence rather than a coded or durable planning assumption.

Stage B generic capability executors and portable conformance vectors remain to be implemented before this task is complete. The branch must be rebased onto consumer main after the preview dependency lands, reviewed, and run through hosted browser CI before a draft PR is opened.
