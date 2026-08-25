---
type: Task
title: Close PHS 398 Cover Page Supplement technical gates
priority: P1
assignee: codex_phs398_cover_closure
description: >-
  Gather dedicated adapter/runtime, exact XML/XSD, compiled-condition, and
  bounded browser evidence for the unregistered PHS 398 Cover Page Supplement.
superbee_progress_status: in_progress
superbee_updated_by: codex_phs398_cover_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T17:51:51.518Z'
---
# Goal

Close the smallest automated technical handoff for the already-banked, unregistered PHS 398 Cover Page Supplement through the generic portable adapter and Simpler runtime.

# Fixed scope

- Rebase from current private-fork main after NIFA PR #121.
- Add dedicated producer/consumer contract and bounded browser evidence using only generic compiler, adapter, renderer, XML, and harness paths.
- Prove exact source/XSD provenance and representative XML against the pinned official PHS 398 Cover Page Supplement 5.0 XSD.
- Prove only the condition transitions actually compiled in the artifact; preserve source-bound-uncompiled behaviors as explicit open gates.
- Avoid all files owned by active private-fork PRs #122 and #123 and the externally owned R&R Subaward Budget 10YR/30 lane.

# Required open gates

- Human embryonic stem-cell line clearing and mutual exclusion remain open unless explicitly compiled and proven from source.
- Inactive-value clearing/retention semantics remain open wherever the artifact does not encode them.
- Cross-form/application-type predicates for inventions and patents remain open.
- Attachment filename/content policy and attachment upload stabilization remain open.
- Semantic mappings remain proposed and contribute nothing to reviewed coverage.
- Human semantic, visual/content, assistive-technology accessibility, agency-profile, instruction, privacy/security, policy, operational, UAT, registration, and production-release gates remain open.

# Acceptance criteria

- No form-specific compiler, loader, adapter, renderer, XML transformer, or browser-harness branch.
- Exact producer/consumer revisions, artifact digests, source hashes, XSD hash, and bounded receipt URLs are recorded.
- Dedicated adapter/runtime tests cover preview build, artifact integrity, representative XML/XSD, and all currently compiled condition effects.
- Four-browser bounded receipts cover preview registration, adapter preflight, Apply render, deterministic save/reload, automated axe scan, and print; attachment results remain separately attributable.
- Any newly discovered generic defect is recorded separately and fixed centrally only after evidence.

# Implementation receipt in progress

Private-fork PR #124 head `3324478dbd0535f1541b77e430aa0b88944082f6` pins the exact projected snake_case UI fixture; exercises all 13 compiled effects against it; executes both HFT attachment IDs and missing-ID failures through the projected rule schema and shared processor before exact XML/XSD; and asserts the complete 17-record source-bound-uncompiled set. Local receipts are 4 API tests and 27 frontend condition tests, with focused Python/TypeScript/lint/format checks green.

Fresh exact-head bounded run `32880329902` is pending. The redundant automatic broad E2E was intentionally canceled under attributable-CI policy; API, frontend, Pa11y, and the bounded browser gate remain enabled.

[depends on](author-integrate-phs398-cover-page-supplement.md)

[depends on](bank-phs398-cover-page-supplement-in-sgg.md)

[depends on](add-portable-form-preview-registration.md)
