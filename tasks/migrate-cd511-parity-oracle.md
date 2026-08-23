---
type: Task
title: Migrate CD-511 through the portable parity oracle
priority: P2
assignee: codex
description: >-
  The portable, unregistered CD-511 implementation and public-fork consumer
  canary are merged; remaining release gates are tracked separately.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:43:37.198Z'
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

# Landed implementation — 2026-08-23

- Producer PR https://github.com/mikec-ai/grants-form-spec/pull/48 merged as `a7f900c636d8eeaad68a4069e745e397593c9459`.
- Consumer PR https://github.com/mikec-ai/simpler-grants-gov/pull/43 merged as `f6affacded160c1585a9e148091b27d45eb7689c`.
- Added generic `@Validation.atLeastOneOf`; emitted output is ordinary JSON Schema `anyOf`/`required` with no CD-511 compiler or adapter branch.
- Reused all seven semantic question occurrences: organization name, federal action number, project title, AOR name/title/signature/date.
- Added the generic versioned `policy-content/v1` and `form-policy-binding/v1` path, including explicit validated presentation order and generic retention in the SGG artifact selection.
- Pinned official XSD `f13c05b8e62fe1e7cf0198053f79fdd34efe4b7d10b56974d27a7dd45d013fde`, official PDF `9c77e249ecb0755f6e000eaa0becd9f6a459fe91adf766f2c64e898d6253d92e`, DAT `0910535d9bf55262ae383482e8e18753b142b828fb580b68cf452a5fc6e2ed8e`, and legacy SGG oracle revision `30dd50cf0493146c32f89f78398979523e040080`.
- Merged-producer preflight passed: 99 TypeScript tests, 94 Python tests with 8 existing skips, artifact/package/promotion validation, exact-XSD XML canary, and unclassified-field ratchet.
- Final consumer selection passed 159 non-DB form-spec and portable CD-511 XML tests; 31 focused CD-511 and R&R budget-family tests passed after the immutable producer repin.
- The consumer pin is the merged producer revision, not a feature-branch-only commit.
- CD-511 remains intentionally absent from `registrations.json`.

# Remaining release gates

- Review the exact policy transcription and the proposed AOR interpretation of the source-labeled Contact Person.
- Complete save/reload, locked/print, browser accessibility, and instruction-asset review in the provisioned application environment.
- Decide registration separately after those reviews; no production registration was included in either merge.
