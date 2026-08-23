---
type: Task
title: Distinguish XML array wrapper cardinality
priority: P0
assignee: key_person_xml_agent
description: >-
  Make collection-wrapper and per-item-wrapper XML arrays explicit so budgets
  and Key Person compile identically across producer and SGG.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T16:44:53.395Z'
---
# Goal

Remove the ambiguity where the same portable array mapping can mean one collection wrapper or one wrapper per item.

# Acceptance criteria

- Add one narrow declarative array mode, with current collection behavior as the compatibility default.
- Key Person explicitly selects per-item wrapper behavior.
- Existing subaward budget arrays retain one collection wrapper and byte/behavior parity.
- Producer reference renderer and SGG transformer implement the same semantics.
- Conformance tests cover both shapes and exact XSD validation.
- No namespace heuristic or form-specific branch.

# Boundary

Do not redesign the XML mapping vocabulary beyond this demonstrated cardinality distinction.
