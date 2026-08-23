---
type: Task
title: Project Key Person XML through SGG
priority: P0
assignee: key_person_xml_agent
description: >-
  Consume the merged portable Key Person XML profile through a generic
  leaf-container projection and validate assembled submission XML against the
  pinned official XSD.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T16:34:48.938Z'
---
# Goal

Complete the consumer half of the merged portable Key Person XML target without form-specific mapping code.

# Acceptance criteria

- Vendor artifacts from merged producer commit 46e71d58516f3c5250702b1de30d8fc27e9ed95a or a later merged ancestor.
- Generic SGG XML projection wraps value/attachment leaves when the portable mapping declares a container element and namespace.
- Objects, groups, and arrays remain unsupported as portable container targets.
- Assemble PI, multiple people, nested attachments, and overflow attachments and validate exact output against the pinned official XSD.
- Submission assembler includes the form generically without production registration.
- No form-specific branch or copied mapping.

# Boundary

Mappings remain proposed/source-bound-unreviewed; technical conformance is not human semantic acceptance.
