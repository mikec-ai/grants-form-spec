---
type: Task
title: Prove a genuinely new EPA 4700-4 form through schema-only agent authoring
priority: P0
assignee: Codex
description: >-
  Author EPA Form 4700-4, absent from the current portable baseline, from pinned
  source evidence plus reusable and explicitly unreviewed new question records.
  Compile and render it without a prior portable form package or any
  form-specific renderer/compiler branch.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T15:43:14.981Z'
---
# Scope

Authored EPA Form 4700-4 from exact independent source evidence plus the pinned question catalog. No EPA 4700 portable package was used as an input. Seven cross-form mappings remain proposals; 21 new source-specific questions remain unreviewed.

# Delivered proof

- Merged [grants-form-workbench PR #25](https://github.com/mikec-ai/grants-form-workbench/pull/25) at merge commit `c36a1b8259053cf67754d0004644e7fa287b1596`.
- Official EPA XSD SHA-256: `8fe73ada9eadce2422214b17764a0eaf40d09c8a69dcc4408cbea5b1d0755677`.
- Authored definition SHA-256: `7dfb807e5b522c3508adc8f6d3e66f2069994ddd27724f3cc9480076c14d5329`.
- Independent evidence receipt SHA-256: `63ae5b66469cb25600c514a638d702f0c9e2e7956affddae0c8bf34723ae0171`.
- Compiled portable package SHA-256: `e36d350b00c1cf049ecc08d338da8c94c2e9140a29123fb99b29d6210618fad7`.
- Package contains 28 exact question occurrences: 0 accepted, 7 proposed, 21 unreviewed.
- Mixed question authorities are resolved generically: pinned shared catalog questions retain their exact authority while source-specific questions remain within the authored form authority.
- The Simpler-compatible consumer preset now provides generic accessible navigation for declarative categorization. All three EPA sections rendered and navigated in the local browser with no console warnings or errors.
- No form-ID branch was added to compiler, renderer, adapter, or preset.

# Verification

- 46 agent-tool tests passed.
- 169 focused contract, catalog, preset, browser-transport, and conformance tests passed.
- Question catalog and browser asset checks are current.
- Typecheck and production build passed.
- GitHub CI did not start any step because the account spending limit blocked the job; the annotation was reviewed and is unrelated to code.

# Remaining review gates

This is a source-structure, compilation, and rendering proof—not production or semantic acceptance. Exact static policy language, final labels, behavior interpretation, accessibility review, and agency review still require the relevant DAT/PDF/instruction evidence and humans. These unresolved gates do not contribute to published semantic coverage.

# Provenance refresh and semantic projection — 2026-08-28

[grants-form-workbench PR #55](https://github.com/mikec-ai/grants-form-workbench/pull/55) regenerated the portable package from the current checked-in authoring definition and refreshed the exact definition, package, catalog, and cohort receipts. Source commit `266b3f3cf276df88ac2163533aff0d54150a15ca`; merge commit `d5172e07f5270f9b28e39457784a202673cf8ccd`.

The same PR added a generic portable-package semantic projection. Against the explicitly pinned 152-question baseline, EPA 4700-4 deterministically yields 28 source occurrences, seven exact-schema reuse proposals, and 21 new-question proposals. A fixture-only attributed review produces 28 accepted bindings and adds exactly 21 questions to a candidate bank. This test proves the mechanism only; it does not create a real authority receipt or alter published coverage.

# Consumer review handoff — 2026-08-28

[grants-form-workbench PR #56](https://github.com/mikec-ai/grants-form-workbench/pull/56), merge commit `99af82b43a7fab46ef4b47b9fe5c83e27538a90f`, closed the remaining consumer boundary. EPA 4700-4 now explicitly names the digest-verified 152-question baseline used for its comparison, and the verified-form screen opens the full 28-occurrence semantic queue without inferring history from the runtime catalog.

The local browser separates seven reuse candidates from 21 proposed new questions, supports independent approve/reject/revise/defer decisions, and applies only attributed approvals to a candidate preview. One fixture-only dogfood approval changed the local receipt to `1 accepted / 6 proposed / 21 unreviewed`; it is not a real semantic authority decision and does not affect published coverage.
