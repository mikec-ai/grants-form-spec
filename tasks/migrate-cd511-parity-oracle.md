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
  at: '2026-08-23T20:19:12.975Z'
---
# Goal

Migrate CD-511 v1.1 (FID 276) through the portable parity oracle as a small Commerce lobbying-certification profile.

# Acceptance criteria

- Pin exact official XSD, DAT, instructions availability, form identity/version, policy text, and legacy SGG oracle revision.
- Reuse reviewed organization, person-name, title, signature, submitted-date, and policy/attestation primitives without conflating CD-511 with SF-LLL or the Grants.gov Lobbying Form.
- Declare the award-number-or-project-name requirement portably and test both valid alternatives plus the missing-both failure.
- Preserve XML sequence, namespace, lifecycle population, save/reload, locked/print, accessibility, and official-XSD validity.
- Add no CD-511-specific compiler or adapter branch.
- Keep semantic, legal-policy, human, and operational approvals explicit before registration.

# Progress receipt — 2026-08-23

- Producer PR: https://github.com/mikec-ai/grants-form-spec/pull/48 at `13f01d9561280f60e3dcebecefc60e65b8bdf82f`.
- Consumer PR: https://github.com/mikec-ai/simpler-grants-gov/pull/43 at `0e555d7eda4335213420049e403484727835e9ee`.
- Added generic `@Validation.atLeastOneOf`; emitted output is ordinary JSON Schema `anyOf`/`required` with no CD-511 compiler or adapter branch.
- Reused all seven semantic question occurrences: organization name, federal action number, project title, AOR name/title/signature/date.
- Added the generic versioned `policy-content/v1` and `form-policy-binding/v1` path, including explicit validated presentation order and generic retention in the SGG artifact selection.
- Pinned official XSD `f13c05b8e62fe1e7cf0198053f79fdd34efe4b7d10b56974d27a7dd45d013fde`, official PDF `9c77e249ecb0755f6e000eaa0becd9f6a459fe91adf766f2c64e898d6253d92e`, DAT `0910535d9bf55262ae383482e8e18753b142b828fb580b68cf452a5fc6e2ed8e`, and legacy SGG oracle revision `30dd50cf0493146c32f89f78398979523e040080`.
- Producer preflight passed: 96 TypeScript tests, 92 Python tests with 8 existing skips, artifact/package/promotion validation, exact-XSD XML canary, and unclassified-field ratchet.
- Consumer focused suite passed 15/15; broader non-DB form-spec plus portable XML suite passed 159/159. A broader selection reached 164 passing; three DB-backed tests could not run because the local `grants-db` hostname was unavailable.
- CD-511 remains intentionally absent from `registrations.json`.

# Remaining gates

- Review the exact policy transcription and the proposed AOR interpretation of the source-labeled Contact Person.
- Complete save/reload, locked/print, browser accessibility, and instruction-asset review in the provisioned application environment.
- Merge producer before consumer, refresh the consumer pin if the producer merge commit changes artifacts, then decide registration separately.
