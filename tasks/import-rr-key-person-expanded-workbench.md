---
type: Task
title: Import R&R Key Person Expanded into the workbench
priority: P0
assignee: Codex
description: >-
  Use R&R Senior/Key Person Profile (Expanded) as form 25 and the first
  empirical customer of single-package agent preflight. Import the exact
  producer package at pinned revision 77fcbe1d, prove both presentation profiles
  and the expanded catalog conformance matrix without form-ID runtime branches,
  preserve all proposed/unreviewed mappings and unresolved behavior gates, and
  record whether the marginal form requires runtime code or configuration only.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T14:19:35.067Z'
---
## Delivered

Merged [grants-form-workbench PR #20](https://github.com/mikec-ai/grants-form-workbench/pull/20) at merge commit `f51a6689b29d6ac6c818858e7a36056f3af23d38`.

R&R Senior/Key Person Profile (Expanded) 4.0 is the twenty-fifth exact producer form in the independent workbench. It was the first new form evaluated through the single-package agent loop. Result: configuration-only consumer adoption—no renderer, capability, or form-ID-specific production code changed. Existing compound person/address, repeatable collection, attachment, and declarative ENABLE-rule capabilities covered it in both profiles.

## Exact receipts

- producer revision: `77fcbe1d63fdb5d5e247f0a9e3bb3b7a1939b46d`
- package SHA-256: `d4d2b64a06bf083f828baf63fa3cce24d4f08def99b7461bc9ca95a1464eec23`
- source path: `specs/forms/rr-key-person-expanded.tsp`
- source SHA-256: `f553a2197f563febb76d7caf05563861629c788605681e4e3e0f3215a37d8b5a`
- deterministic import: 25 forms and 374 captured files
- single-package preflight: 18/18 findings supported across `generic/v1` and `simpler-compatible/v1`
- expanded conformance: 75/75 cases passed
- full workbench: 23 test files and 325 tests passed
- agent-tools: 14/14 tests passed
- build and browser-catalog freshness check: passed
- implementation commit: `5fa112d`

GitHub Actions run `33081513161` failed before execution with zero job steps and no log. No repository check ran; the complete local gate above is the merge evidence.

## Review boundary

All three portable occurrences remain unreviewed. Nine producer behavior-evidence records remain captured as unresolved; no portable behavior artifact was invented or promoted. Accessibility, XML parity, policy approval, and human acceptance remain separate gates.
