---
type: Task
title: Make attachment auditing array-aware
priority: P0
assignee: attachment_audit_agent
description: >-
  Teach Simpler attachment auditing to traverse repeated form rows generically
  so nested attachments participate in save/update reconciliation.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T16:01:04.880Z'
---
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

# Result

Delivered and merged in mikec-ai/simpler-grants-gov PR #33, merge commit 676f889620cb6d6ad74c270a94fb873fc37b7555.

- Generic traversal maps schema items segments to runtime array wildcards and also supports concrete indices.
- Root, nested object, repeated-row, Attachment, and AttachmentArray behavior is covered.
- Old/new attachment identifiers are set-differenced, so row moves and duplicate references do not create false audit events.
- No form-specific branch was introduced.
- Seventeen focused tests passed in implementation; independent review found no actionable issues. Ruff and mypy passed.
