---
type: Task
title: Close SBIR/STTR Information technical gates
priority: P1
assignee: codex_sbir_sttr_closure
description: >-
  Gather bounded generic lifecycle, compiled-condition, attachment, and
  exact-XSD evidence for the already-banked unregistered SBIR/STTR Information
  form while preserving proposed semantics and unresolved policy rules.
superbee_progress_status: in_progress
superbee_updated_by: codex_sbir_sttr_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T17:10:00Z'
---
# Goal

Close the smallest automated technical handoff for the already-banked SBIR/STTR Information package through generic Simpler runtime paths.

# Fixed scope

- Prove the 11 compiled conditional-required transitions and 10 consumer enablement effects without compiling the five explicitly unresolved clear/remove or policy-conflict rules.
- Prove the three semantically distinct attachments through the shared attachment capture and XML mechanisms.
- Prove representative XML against the exact pinned `SBIR_STTR_Information_3_0-V3.0.xsd` source.
- Run bounded lifecycle/browser evidence through ordinary Apply and print routes.
- Add no SBIR/STTR-specific compiler, adapter, loader, renderer, harness, eligibility engine, policy DSL, or registration branch.

# Safety boundaries

- SBIR/STTR Information remains unregistered and lower-environment preview-only.
- Semantic mappings remain `proposed` and contribute nothing to reviewed coverage.
- The four clear/remove effects and disputed compound Commercialization Plan condition remain source-bound uncompiled.
- Human semantic, visual/content, accessibility/assistive-technology, agency-profile, instruction, privacy/security, policy, operational, UAT, registration, and production-release gates remain open.
- Do not touch the externally owned R&R Subaward Budget 10YR/30 lane.

# Acceptance criteria

- Exact producer/consumer revisions, source digests, and XSD digest are recorded.
- Focused tests cover exact compiled conditions, attachment XML, representative XML/XSD validation, and the proposed/unregistered boundary.
- Four-browser bounded receipts cover render, save/reload, automated accessibility scan, and print.
- Runtime identities and registrations remain unchanged.
- All attributable checks pass; unrelated failures are classified with exact evidence.

[depends on](author-integrate-sbir-sttr-information.md)

[depends on](bank-sbir-sttr-information-in-sgg.md)

[depends on](add-portable-form-preview-registration.md)

# Implementation receipt — 2026-08-25

- Private consumer PR: `mikec-ai/simpler-grants-gov#122`
- Branch/head: `codex/sbir-sttr-technical-closure` at `03562edbe`
- Base at implementation start: private fork main `d613c0aea5fca8a5dc6c05c34a320ef60918ee4b`
- Collision check: zero changed-file overlap with NIFA PR #121 head `41192ca6`; no R&R Subaward Budget 10YR/30 files touched.
- Focused API verifier: 12/12 passed, including representative generic XML emission and exact pinned v3.0 XSD validation.
- API verifier plus registration boundary: 18/18 passed.
- Frontend generic condition evaluator: 10/10 passed.
- Ruff, ESLint, Prettier, and TypeScript checks passed.
- Evidence explicitly preserves 27 `proposed` mappings, 11 compiled behavior records, and five source-bound-uncompiled records. Runtime registration remains absent.
- Hosted CI classification: `full`, expected for this first tests/CI-map technical admission without a producer artifact delta. Merge is held pending attributable hosted results.
