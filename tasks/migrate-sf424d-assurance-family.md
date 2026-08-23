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
  at: '2026-08-23T20:41:57.610Z'
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

## Producer implementation and exact-source gates (2026-08-23)

- Producer branch: `codex/sf424d-family-20260823`
- Producer PR: `mikec-ai/grants-form-spec#52` against `main`. It supersedes `#51`, which GitHub automatically closed when its temporary stacked base branch was deleted after `#50` merged.
- Merged SF-424B policy-contract foundation: `bc1d60325e52fbffd782756ec40c9dba232fd978` (`#50`; producer tip `f2125e2c6c5be9363f6dfbda36999dd89ad85e57`)
- Final main-based audit commits: `aa3a077` (source audit) and `a7f83a2` (wire/XSD canaries)
- Final declarative producer commit: `7b23153b0decf2c0d744f70083942cbccbb88c76` (`Bank declarative SF-424D assurance profiles`)
- All three official FID records were independently checked and are currently Active at v1.1: base FID 238, Individual FID 522, Mandatory FID 329.
- Exact XSD, DAT, instructions, sample-PDF, and read-only-PDF URLs and SHA-256 digests are pinned under `research/sf424d-family/official-source-audit.json` and the three emitted evidence sidecars.
- The twenty policy items are identical across all three profiles and are authored once as `grants-gov/construction-assurances@1.1`; they are not question-bank questions. Canonical source text-array SHA-256: `89c82c4e717dab69a9a751259e9148b97d6b092e88d1a57e8537953c5ee1c4be`.
- The producer uses the same canonical acceptance shell as SF-424B: `signature`, `title`, `applicantOrganization`, and `signedDate`. The analysis reports 8/8 inherited question identities and 2/2 platform behaviors reused for each of the three D profiles, with zero new question/capture/behavior capabilities.
- Individual and Mandatory XSD shapes differ only by namespace/prefix. Base additionally carries `glob:FormVersionIdentifier` plus `glob:coreSchemaVersion`; the variants use local fixed `FormVersion`.
- Base and Mandatory title/organization are locked system values; Individual title/organization are applicant input. Signature/date remain locked platform values for all three. Those deltas live in policy bindings and TypeSpec composition rather than an adapter branch.
- One factored XML acceptance mapping is composed by three declarative profiles. Fully populated samples for all profiles validate against the exact official XSD bytes, including the profile-qualified root attributes and the base-only global version child.
- The base SGG implementation oracle is pinned at `mikec-ai/simpler-grants-gov@30dd50cf0493146c32f89f78398979523e040080`, file SHA-256 `8236db821592dc3b36e3e95971b514af4657b3b41e781259f0797e46d091fb2a`.
- Full producer preflight passes on the final restack: 99 TypeScript tests, 120 Python tests with 8 existing skips, artifact validation (145 blocks/859 artifacts), promotion validation, 589-artifact packaging, 20 XML profiles, and the unclassified-field ratchet (49 remaining, unchanged by this family).
- The final D diff is three commits directly atop merged producer `main`; PR `#52` is mergeable. GitHub CI run `32665096478` passed from final producer commit `7b23153` (including independent TypeSpec compilation and portable-artifact publication).
- Forms remain `draft`, absent from production registration, and no HHS upstream worktree was mutated.

# Remaining gates

- Merge SF-424D producer PR `#52` after CI and review; `#50` is already merged and superseded stacked PR `#51` is closed.
- Complete policy-owner/semantic and accessibility review. Source provenance and deterministic cross-profile policy equivalence are already passed; these reviews remain human gates.
- Add generic SGG consumer canaries for lifecycle, locked/print, post-population, policy-section projection, and XML consumption without adding an SF-424D code branch.
- Perform explicit production-registration and instruction-asset review only after the consumer gates pass; do not register implicitly.
