---
type: Task
title: Produce evidence-backed PHS response-role review packet
priority: P0
assignee: Codex
description: >-
  Merged grants-form-workbench PR #29 (merge commit 203abc3): added a generic
  standalone review packet that presents exact pinned evidence beside each
  proposed field response role and behavior disposition. Reviewers can accept,
  reject, or leave decisions proposed and download a revised overlay; accepted
  decisions require reviewer, authority, and evidence URI, and the overlay must
  still pass grants-form-review. The packet cannot compile forms, publish
  coverage, or activate runtime behavior. PHS proof contains 12 field decisions,
  30 behavior decisions, and the two exact calculation rules from the pinned
  DAT-derived evidence. Verification: 58 agent-tool tests, 44 targeted
  contract/architecture tests, typecheck, catalog checks, question-catalog
  check, production build, and browser QA passed. GitHub CI again failed before
  executing any steps; merge used the complete local evidence. Generated packet
  SHA-256: 4703b63cb063d0fb4f5d6742b7e5922b4f767ff32ff0e1a5e767e2be97c02475.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T16:44:02.001Z'
---
[depends on](implement-review-gated-portable-response-roles.md)
