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
  at: '2026-08-25T19:06:31.240Z'
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

## Independent-review remediation — 2026-08-25

- Review found that the first condition tests exercised canonical artifacts rather than the projected consumer path, and that the first attachment test asserted declarations without executing the shared mechanisms.
- Remediation head `b15ce13cb8b7fe5ba4351b26fc2e7619b1fd4d0a` closes both evidence gaps without changing shared runtime, NIFA, registration, or the externally owned subaward lane.
- All 11 conditional-required targets now execute against `_load_banked_form`'s snake_case projected schema.
- The frontend's 10 effect cases use snake_case runtime data and a projected-condition fixture; an API regression proves that fixture exactly equals current adapter output, preventing projection drift from producing a false green.
- All three attachment IDs execute through the projected rule schema and shared attachment validator, are emitted with `AttachmentInfo` through the generic XML service, and validate together against the exact pinned v3.0 XSD.
- Updated local receipts: SBIR/STTR API 14/14; API plus registration boundary 20/20; frontend 10/10; Ruff, ESLint, Prettier, and TypeScript green.
- The earlier hosted API run failed before form tests in the unrelated `test_wait_for_api.sh` late-success stdout assertion. No product change was made for that baseline helper flake; new-head checks remain pending and authoritative.
- Exact bounded four-browser SBIR/STTR run dispatched once for head `b15ce13cb`: GitHub Actions run `32879500738` (`portable_browser_form_ids=sbir-sttr-information`). No duplicate broad/API run was dispatched.

## Generic browser-harness remediation — 2026-08-25

- Exact run `32879500738` was canceled after more than 35 minutes without a receipt. Its partial artifact `9576642702` and a local trace showed the generic deterministic edit waiting on Playwright `check()` for an offscreen USWDS radio across the four browser projects; the portable suite itself had retries disabled.
- The same trace proved two attachment-probe defects: it selected the first declared attachment even when conditionally disabled, and it required the unrelated whole form to report `No errors were detected` before accepting durable attachment persistence.
- Private consumer PR `mikec-ai/simpler-grants-gov#129` fixed only the generic portable browser harness and merged as `fe5e6ab92976d0a3c0b81f91c790333e0bdee309`.
- The harness now activates binary controls through their visible associated labels with bounded timeouts, selects the first declared attachment input that is actually visible and enabled, and proves persistence using the save acknowledgement plus the exact filename, Delete affordance, and non-empty hidden attachment ID after reload.
- Regression receipts at PR #129 head `8e5cf6a90`: matrix contract 17/17, Chrome harness 4/4, ESLint and TypeScript green. Direct browser regressions cover hidden and disabled declaration skips, declared-order selection, exact selected definition/control ID, explicit no-eligible failure, offscreen-radio persistence, and attachment persistence despite unrelated validation errors. Independent review was clean.
- Hosted E2E classifier succeeded; redundant broad E2E was canceled before form execution. The prior-head hosted Frontend Checks run `32887241874` completed successfully. Remaining queued PR runs were canceled after merge.
- PR #122 must now rebase onto the merged generic fix and produce one fresh, exact SBIR/STTR browser receipt. The five source-bound behaviors, semantic review, registration, human review, and release gates remain open and unchanged.
