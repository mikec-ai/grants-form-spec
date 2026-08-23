---
type: Task
title: Migrate CD-511 through the portable parity oracle
priority: P2
assignee: codex
description: >-
  Bank the small Commerce lobbying-certification form through shared identity,
  policy, attestation, lifecycle, and XML primitives.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T19:52:14.124Z'
---
# Goal

Migrate CD-511 v1.1 (FID 276) through the portable parity oracle as a small Commerce lobbying-certification profile.

# Acceptance criteria

- Pin exact official XSD, DAT, instructions, form identity/version, policy text, and legacy SGG oracle revision.
- Reuse reviewed organization, person-name, title, signature, submitted-date, and policy/attestation primitives without conflating CD-511 with SF-LLL or the Grants.gov Lobbying Form.
- Declare the award-number-or-project-name requirement portably and test both valid alternatives plus the missing-both failure.
- Preserve XML sequence, namespace, lifecycle population, save/reload, locked/print, accessibility, and official-XSD validity.
- Add no CD-511-specific compiler or adapter branch.
- Keep semantic, legal-policy, human, and operational approvals explicit before registration.
