---
type: Task
title: Close lobbying and certification cohort technical gates
priority: P1
assignee: codex_lobbying_certification_closure
description: >-
  Gather bounded adapter, runtime, browser-plan, lifecycle, attestation, and
  exact-XML evidence for SF-LLL, CD-511, and Grants.gov Lobbying without
  accepting policy text, semantics, or production registration.
superbee_progress_status: in_progress
superbee_updated_by: codex_lobbying_certification_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T17:55:00Z'
---
# Goal

Close the smallest shared technical handoff for three already-banked lobbying and certification profiles through existing generic Simpler mechanisms while preserving their distinct meanings and release gates.

# Fixed scope

- SF-LLL: prove projected identity/contact/disclosure conditions, constants and value maps, service-individual repetition, submitter population, static policy presentation, generic XML, and exact XSD.
- CD-511: prove projected identity/attestation paths, `atLeastOneOf` award-number-or-project-name validation, submitter population, static policy presentation, generic XML, and exact XSD.
- Grants.gov Lobbying: prove projected identity/attestation paths, submitter population, static policy presentation, generic XML, and exact XSD.
- Add dedicated form-local adapter/runtime/browser closure evidence and CI-map routing only.
- Add no form-specific or shared compiler, adapter, renderer, rule, population, browser-harness, or XML branch.

# Safety boundaries

- Preserve exact source/version/hash provenance and proposed-vs-reviewed semantic status.
- Policy/certification text acceptance, constants and value-map policy acceptance, and attestation interpretation remain human gates.
- CD-511 `atLeastOneOf` is verified as emitted generic JSON Schema; do not reinterpret it.
- Submitter population is technical lifecycle evidence, not authorization or policy approval.
- All three forms remain unregistered unless an existing legacy runtime identity is explicitly being used only as an oracle; no registration change is authorized.
- Human semantic, legal/policy, accessibility/assistive-technology, content/instruction, privacy/security, operational, UAT, cutover, and production-release gates remain open.
- Do not touch PR #122, PR #123, the PHS 398 Cover Page Supplement lane, or externally owned R&R Subaward Budget work.

# Acceptance criteria

- Each form has exact provenance, projected consumer schema/UI/rule evidence, generic lifecycle/attestation evidence, generic XML, and exact-XSD validation.
- Static policy content and policy bindings remain immutable source artifacts; tests do not declare the text accepted.
- Dedicated browser plans expose only source-backed generic capabilities and produce bounded receipts before closure.
- Runtime identities and registrations remain unchanged.
- All attributable checks pass; unrelated failures are classified with exact receipts.

# Implementation checkpoint — 2026-08-25

- Private consumer branch: `codex/lobbying-certification-technical-closure`
- Consumer head: `c22ec7ad508692cafb4c4975b723e1af3f898f2a`
- Private consumer PR: https://github.com/mikec-ai/simpler-grants-gov/pull/125
- Scope is test/evidence-only in the three existing form-local suites; no shared runtime, adapter, compiler, browser harness, artifact, registration, or producer change.
- Exact available source URI/hash sets remain pinned. Semantic review remains `proposed`; CD-511 and Grants.gov Lobbying policy bindings remain `draft`; all three forms remain absent from portable registrations.
- Local attributable receipt: Ruff green and 32/32 focused API tests green across SF-LLL, CD-511, Grants.gov Lobbying, and registration boundaries.
- Review follow-up pins SF-LLL's exact three calculated response paths/rules, the exact Prime→`Y: Yes` / SubAwardee→`N: No` projection, and representative exact-XSD-valid XML for both values. CD-511 and Grants.gov Lobbying now assert exact extraction receipts; Grants.gov Lobbying asserts the complete ordered `(type, uri, sha256)` source set.
- Exactly one bounded browser cohort run was dispatched for `sflll,cd511,gg-lobbying`: https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32880367987 (pending).
- Stale broad runs for superseded head `4c103920a` were cancelled: API `32879944180`; E2E `32879944838`.
- The automatically launched broad E2E run for pre-hardening head `f830a630e` (`32880351049`) was cancelled to avoid duplicating its exact bounded browser cohort run. Its broad API run was `32880350142`.
- After CI hardening PR #126 merged at `bb8b7d5c6`, this branch was rebased and local Ruff + 32/32 focused tests remained green. Superseded-head runs `32880367987` and `32880350142` were cancelled.
- First hosted test-only focused-path proof on rebased head: API `32880826731` classified `portable_focused` with exact selected IDs `cd511`, `gg-lobbying`, `sflll`, their exact three mapped test files, and zero changed artifacts; Focused Portable Form Checks passed (job `97910331871`, 7m03s) while full API/bank jobs stayed skipped. E2E/browser `32880827041` also passed classification and its single bounded `(1,1)` cohort shard passed (job `97911386532`, 12m45s). Only the merged browser-report job remains pending.
- Hosted checks are pending. Technical closure remains `in_progress` until the exact bounded browser and attributable hosted receipts are reviewed.

[depends on](migrate-sflll-parity-oracle.md)

[depends on](migrate-cd511-parity-oracle.md)

[depends on](migrate-gg-lobbying-parity-oracle.md)
