---
type: Task
title: Make attachment auditing array-aware
priority: P0
assignee: attachment_audit_agent
description: >-
  Teach Simpler attachment auditing to traverse repeated form rows generically
  so nested attachments participate in save/update reconciliation.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T15:50:19.017Z'
---
# Goal

Make attachment discovery and audit traverse runtime arrays without form-specific paths.

# Acceptance criteria

- Schema/UI pointers containing items are translated into generic instance traversal rather than treated as literal payload keys.
- Root attachments, nested object attachments, repeated-row attachments, and attachment arrays are covered by regression tests.
- Save and update auditing finds additions and removals within repeated rows.
- Existing attachment behavior is unchanged.
- No branch is keyed to R&R Key Person Expanded or another individual form.

# Scope boundary

Do not redesign attachment storage, validation rules, or form registration.
