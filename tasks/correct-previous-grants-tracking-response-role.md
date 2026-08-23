---
type: Task
title: Correct lifecycle response ownership
priority: P0
assignee: correct_tracking_role
description: >-
  Audit PR43 lifecycle occurrences against pinned population instructions;
  classify R&R applicant-entered values separately from classic SF-424
  system-populated values while preserving external authority and proposal-only
  semantic mappings.
superbee_progress_status: done
superbee_updated_by: correct_tracking_role
generated:
  by: 'process:superbee'
  at: '2026-08-23T19:17:41.121Z'
---
# Scope

Audit the standalone R&R SF-424, Multi-Project Cover, and classic SF-424 lifecycle fields against pinned sources. `ResponseRole` identifies the actor populating the response; the organization that originally assigned a value remains in descriptions and provenance.

# Evidence-backed disposition

- R&R State-received date, State application identifier, agency routing identifier, and prior Grants.gov tracking number: `applicantInput` in both covers (8 occurrences).
- Classic SF-424 State-received date and State application identifier: read-only `systemValue` (2 occurrences).
- Multi-Project submitted date: `applicantInput` (unchanged).
- Attestations and technical controls: unchanged.
- SF-424 Federal Award Identifier: distinct and still unresolved, not equated to the tracking number.

# Delivery

Merged producer PR: [mikec-ai/grants-form-spec#46](https://github.com/mikec-ai/grants-form-spec/pull/46), main commit `c4a7fa5e722bca4dd92eb66a887bc2f7f6e0a865`.

Pinned standalone instructions SHA `666647f...` and Multi-Project DAT SHA `361e00d...` independently direct applicant entry. All semantic mappings remain proposed and unpublished. Local preflight and GitHub CI passed: 91 TypeSpec tests, 87 Python tests, 131 blocks / 712 artifacts, and ratchet 76 initial / 27 resolved / 49 remaining. No HHS/upstream repository or issue was modified.
