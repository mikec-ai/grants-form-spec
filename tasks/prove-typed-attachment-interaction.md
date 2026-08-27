---
type: Task
title: Prove typed attachment interaction through the portable boundary
priority: P1
description: >-
  Completed in grants-form-workbench PR #3 (merge
  7f69264debfd8c1b0df9f6c0d3e5d11cbe25fc0f). Attachment answers now serialize
  UUID references only while exact File/Blob handles remain in a session-owned
  consumer registry. Tests cover staging, commit, rejection after behavior
  failure, replacement, removal, StrictMode, true unmount, stale callbacks, and
  new-session disposal. Upload transport, file policy, backend persistence, and
  content extraction remain explicit follow-ons.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T04:14:59.620Z'
assignee: Codex-attachment-agent
---
[depends on](close-workbench-multi-form-proof.md)
