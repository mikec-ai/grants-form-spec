---
type: Task
title: Correct prior Grants.gov tracking response role
priority: P0
assignee: correct_tracking_role
description: >-
  Correct the R&R tracking-number occurrences using pinned source instructions
  and the portable ResponseRole contract; preserve proposal-only semantic
  mapping and unchanged XML/runtime behavior.
superbee_progress_status: in_progress
superbee_updated_by: correct_tracking_role
generated:
  by: 'process:superbee'
  at: '2026-08-23T19:03:30.822Z'
---
# Scope

Verify the standalone R&R SF-424 and Multi-Project Cover tracking fields against pinned sources. Model the response occurrence according to who supplies it into the application while keeping its source authority and canonical semantic identity explicit.

# Acceptance

- Both affected R&R occurrences have the evidence-backed response role.
- Standalone and Multi-Project share the canonical prior-tracking identity only as an unpublished proposal.
- SF-424 federal award identity remains separate.
- Ratchet, analysis, XML, UI, and validation tests remain honest.
