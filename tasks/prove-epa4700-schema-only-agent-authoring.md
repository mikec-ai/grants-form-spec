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
- Authored definition SHA-256: `95db2d3b9445f88fa4aee6066c3f2ced5fb7de68b1103ced8c6bfd80cf95f7fb`.
- Independent evidence receipt SHA-256: `63ae5b66469cb25600c514a638d702f0c9e2e7956affddae0c8bf34723ae0171`.
- Compiled portable package SHA-256: `c57c28bf7382bccee602679b33a48b00ab0b3d3f7815191b275bce6765ca090a`.
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
