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
  at: '2026-08-23T20:54:07.907Z'
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
- The final D diff was three commits directly atop merged producer `main`; PR `#52` merged at immutable producer revision `e0b0fb24c421a7c70e395afedf5be3f37f366606`. GitHub CI run `32665096478` passed from the reviewed head (including independent TypeSpec compilation and portable-artifact publication).
- A bounded comparison against the merged SF-424B contract found no competing policy/projector abstraction or form-specific adapter branch. The D policy, response ownership, and namespace/version deltas use the shared contracts as intended.
- Forms remain `draft`, absent from production registration, and no HHS upstream worktree was mutated.

## Generic SGG consumer canaries (2026-08-23)

- Consumer PR `mikec-ai/simpler-grants-gov#47` merged at immutable revision `0738a54e4b372a25738fc5b79df251955815bbef`.
- The complete 28-form consumer selection is pinned exactly to producer merge `e0b0fb24c421a7c70e395afedf5be3f37f366606`; 290 transitive runtime artifacts were selected by the atomic updater.
- Base SF-424D preserves legacy SGG runtime UUID `fecdf956-0b63-480b-9b44-66541e059646`. Individual and Mandatory have distinct declarative SGG-owned runtime identities. All three use existing `FormType.SF424D` and remain absent from `registrations.json`.
- One thin base projection maps canonical `signedDate` to legacy `date_signed` and the canonical acceptance section identifier to `signature`; the variants declaratively extend that projection. No SF-424D loader, policy, post-population, or XML code branch was added.
- Exact official XSD SHA-256 checks pass for base (`22026ea7...`), Individual (`52187d42...`), and Mandatory (`6685f2c1...`). Generic XML generation validates all three wire profiles against those pinned bytes.
- Focused artifact/provenance/registration/policy/post-population/locked-editability/XML canaries pass: 26/26. A broader portable-form and XML tranche passed 221 tests; its sole setup error was an existing SF-424A DB test attempting to resolve unavailable local host `grants-db`.
- Six D-family DB save/reload/submission lifecycle cases are committed. They reached the same missing-local-DB fixture boundary and therefore still need execution in a provisioned DB test environment before the consumer lifecycle review gate is marked passed.

# Remaining gates

- Complete policy-owner/semantic and accessibility review. Source provenance and deterministic cross-profile policy equivalence are already passed; these reviews remain human gates.
- Execute the six committed DB lifecycle canaries in a provisioned SGG test environment and record the result. The non-DB locked/print, post-population, policy, and exact-XSD consumer gates already pass.
- Perform explicit production-registration and instruction-asset review only after the human and DB lifecycle gates pass; do not register implicitly.
