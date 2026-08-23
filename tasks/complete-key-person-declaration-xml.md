---
type: Task
title: Complete Key Person declaration and XML target
priority: P0
assignee: key_person_xml_agent
description: >-
  Correct pinned DAT behaviors and author the reviewed Grants.gov XML/XSD target
  for R&R Key Person Expanded.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T16:06:46.448Z'
---
# Goal

Close source-bound declaration gaps and produce representative official XML for R&R Key Person Expanded.

# Acceptance criteria

- Add DAT-backed US ZIP minimum and PD/PI project-role default with exact evidence references.
- Resolve state/province XML safety without inventing semantics.
- Compose reusable reviewed name, address, attachment, and research-person XML fragments.
- Generate PI, multiple-person, and attachment XML and validate it against pinned RR_KeyPersonExpanded_4_0-V4.0.xsd.
- Add tests and preserve semantic review gates.

# Boundary

Do not implement overflow attachment boolean gating here and do not enable production registration.
