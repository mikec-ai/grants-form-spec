---
type: Task
title: Distinguish XML array wrapper cardinality
priority: P0
assignee: key_person_xml_agent
description: >-
  Make collection-wrapper and per-item-wrapper XML arrays explicit so budgets
  and Key Person compile identically across producer and SGG.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:20:26.155Z'
---
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

# Result

Delivered in ordered producer and consumer changes.

- grants-form-spec PR #39 merged as 3ba1c1c25a111c91085bec9ca89ab1fc2be645ef.
- simpler-grants-gov PR #36 merged as 5b16ea30628936fbe4bf0637838e07ccb30505d2.
- Optional repeatElementPerItem defaults to the existing single collection-wrapper behavior.
- Key Person alone opts into one KeyPerson wrapper per repeated Profile.
- Two-budget regression proves one BudgetAttachments wrapper with two inner budget items.
- Producer and consumer exact-XSD tests pass with no namespace heuristic or form branch.
