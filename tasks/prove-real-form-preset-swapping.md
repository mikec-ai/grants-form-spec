---
type: Task
title: Prove presentation swapping across genuine portable forms
priority: P0
assignee: Codex
description: >-
  Completed and independently approved in workbench commits 5286495, 0ab1ac4,
  and 33fc3b4. The demo loads SF-424, SF-424 Short, Attachment Form, and PHS
  Assignment Request through the generic catalog, displays verified
  form/version/digest/producer receipts, and switches between generic and
  Simpler-compatible renderer registries without changing the package or
  response data. Browser evidence covered all four forms; edits persisted across
  preset changes and console errors were zero. A shared Ajv duplicate-schema
  registration defect and rapid A→B→A delayed-callback race were fixed
  generically with regressions. Final lane verification: 173 tests passed, 1
  skipped; typecheck, all builds, dependency tree, and diff checks green.
  Explicit limits: accepted semantic mappings=0; cohort behavior artifacts=0;
  attachment string is not file-upload UX proof; compound person/contact
  controls need a generic renderer; no accessibility, XML, or human parity
  claim.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T02:15:55.537Z'
---
[depends on](integrate-pinned-producer-cohort-in-workbench.md)

[depends on](execute-portable-behaviors-in-workbench-renderer.md)
