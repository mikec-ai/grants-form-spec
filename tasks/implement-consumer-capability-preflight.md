---
type: Task
title: Implement consumer capability preflight for agent-authored forms
priority: P1
assignee: Codex
description: >-
  Implemented and merged a form-neutral consumer capability preflight in
  grants-form-workbench PR #16 (merge d77f543497e90239a1e977a87fefa317fe4d9b96).
  The agent-facing CLI verifies canonical package digests, preserves exact UI
  and behavior source receipts, reports stable supported/unsupported reasons
  with exact UI/data/behavior paths, and leaves semantic review states
  untouched. Audit receipt: all 23 pinned forms are ready for declared
  capabilities in both generic/v1 and simpler-compatible/v1; zero accepted
  semantic mappings are claimed. Verification: 9/9 new CLI/preflight tests, 7/7
  boundary tests, typecheck, build, and 23-form asset check pass. Broad UI runs
  retain a pre-existing timing flake in the attachment-array test that passes in
  isolation. PHS Fellowship cannot be preflighted honestly until it is emitted
  as a portable package.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T12:51:37.693Z'
---

