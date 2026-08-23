---
type: Task
title: Bank the SF-424D assurance profile family
priority: P1
assignee: sf424d_family_agent
description: >-
  Publish the active construction-assurance profiles over the shared portable
  policy and attestation contract.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T19:52:13.781Z'
---
# Goal

Bank the SF-424D construction-assurance family as versioned profiles over the shared portable policy/attestation contract.

# Scope

- SF-424D v1.1 (FID 238)
- Individual SF-424D v1.1 (FID 522), subject to an explicit current-status check
- Mandatory SF-424D v1.1 (FID 329), subject to an explicit current-status check

# Acceptance criteria

- Pin official XSD, DAT, instructions, legal-policy content, form identity, version, and hashes per profile.
- Represent the twenty construction assurances as a versioned policy bundle, not ordinary question-bank questions.
- Reuse organization, representative-title, platform signature/date, acceptance-event, and profile machinery from the assurance foundation.
- Keep namespace, root, prepopulation/editability, labels, and policy differences declarative.
- Emit separate artifacts and official-XSD-valid XML with no SF-424D adapter branch.
- Run lifecycle, locked/print, accessibility, policy, and release gates explicitly.

[depends on](migrate-sf424b-parity-oracle.md)
