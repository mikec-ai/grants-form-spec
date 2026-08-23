---
type: Task
title: Bank the SF-424D assurance profile family
priority: P1
assignee: sf424d_family_agent
description: >-
  Publish the active construction-assurance profiles over the shared portable
  policy and attestation contract.
superbee_progress_status: in_progress
superbee_updated_by: sf424d_family_agent
generated:
  by: 'process:superbee'
  at: '2026-08-23T20:04:23.629Z'
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

# Progress receipts

## Official-source audit staged (2026-08-23)

- Producer branch: `codex/sf424d-family-20260823`
- Staging commit: `ca0ba79b346d4b7ae05108ee628145342e7d51ba`
- Fresh worktree baseline: `origin/main` at `7db589062431f3db063e847ddf6bfc2046b38c7b`
- All three official FID records were independently checked and are currently Active at v1.1: base FID 238, Individual FID 522, Mandatory FID 329.
- Exact XSD, DAT, instructions, sample-PDF, and read-only-PDF URLs and SHA-256 digests are staged under `research/sf424d-family/official-source-audit.json`.
- The twenty policy items are identical across all three profiles and staged as one source-bound, unreviewed construction bundle. Canonical policy-text-array SHA-256: `89c82c4e717dab69a9a751259e9148b97d6b092e88d1a57e8537953c5ee1c4be`.
- Individual and Mandatory XSD shapes differ only by namespace/prefix. Base additionally carries `glob:FormVersionIdentifier` plus `glob:coreSchemaVersion`; the variants use local fixed `FormVersion`.
- Base and Mandatory title/organization are prefilled; Individual title/organization are applicant input. Signature/date remain platform values for all three.
- Exact official XSD fixtures and six focused audit tests are staged. Full producer preflight passed: 93 TypeScript tests, 96 Python tests with 8 pre-existing skips, artifact validation, packaging, and unclassified ratchet.

# Remaining gates

- Rebase onto the stable shared policy/assurance/attestation foundation from the SF-424B work.
- Convert the staged construction policy and profile matrix into production declarative artifacts without introducing a competing generic contract.
- Emit and validate all three XML profiles against the pinned official XSDs.
- Add consumer lifecycle, locked/print, accessibility, policy, and release gates; do not register forms without explicit approval.
