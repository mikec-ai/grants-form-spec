---
type: Task
title: Project Key Person XML through SGG
priority: P0
assignee: key_person_xml_agent
description: >-
  Consume the merged portable Key Person XML profile through a generic
  leaf-container projection and validate assembled submission XML against the
  pinned official XSD.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:41:44.622Z'
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

# Result

Delivered and merged in mikec-ai/simpler-grants-gov PR #36, merge commit 5b16ea30628936fbe4bf0637838e07ccb30505d2.

- Artifacts pin stable merged producer commit 3ba1c1c25a111c91085bec9ca89ab1fc2be645ef.
- Generic leaf container and explicit repeated-array wrapper modes project without a form branch.
- Technical submission XML contains PI, two repeated people, ordinary person values, eight nested/overflow attachments, exact QNames/order/data, and passes the official XSD.
- The complete five-file imported XSD closure is byte-pinned and hash-verified; all 33 vendored XSDs compile.
- Existing subaward budget wrapper behavior remains locked by exact-XSD regression.
- Independent review closed provenance and value-assertion gaps before merge.

Production registration remains disabled. Mappings remain proposed/source-bound-unreviewed, and exact XSD validation plus semantic, accessibility, instruction, identifier, and release acceptance remain explicit gates.

[depends on](distinguish-xml-array-wrapper-cardinality.md)
