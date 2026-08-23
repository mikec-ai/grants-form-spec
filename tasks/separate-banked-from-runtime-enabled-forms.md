---
type: Task
title: Separate banked forms from runtime-enabled forms
description: >-
  Allow verified artifact banking without inventing Simpler runtime identities,
  while keeping runtime enablement fail-closed.
superbee_updated_by: promote_new_forms
generated:
  by: 'process:superbee'
  at: '2026-08-23T23:44:14.304Z'
priority: P0
superbee_progress_status: in_progress
assignee: promote_new_forms_agent
---
# Goal

Decouple digest-verified artifact banking from Simpler runtime enablement so genuinely new portable forms can be promoted without inventing UUIDs, FormTypes, or compatibility projections.

# Acceptance criteria

- The selected artifact bank may contain forms with no runtime identity.
- Runtime loading, preview, and registration fail closed unless a selected form is explicitly runtime-enabled and has a complete consumer-owned identity/projection record.
- Existing runtime-enabled and production-registered forms retain exact behavior.
- Manifest, provenance, digest, required-XSD, and atomic-selection verification still cover every banked form.
- Tests prove that missing identity is accepted only for banked-only forms and rejected for any runtime-enabled form.
- Production registrations remain unchanged.
- PHS Assignment Request and Attachment Form prove the banked-only path at producer revision `2fde5118f440f31c7527fde784d573bb3ab3d912`.

# Boundary

Do not invent target identities. Test/dev preview enablement is a later explicit consumer decision tracked separately.

[depends on](automate-cross-repo-form-promotion.md)

# Delivery receipt

Consumer PR [#51](https://github.com/mikec-ai/simpler-grants-gov/pull/51) establishes the generic banked-only boundary and proves it with Attachment Form and PHS Assignment Request at producer revision `2fde5118f440f31c7527fde784d573bb3ab3d912`. All 31 banked forms remain subject to manifest, provenance, artifact-digest, and exact-XSD verification. Only the 29 forms in `runtime-identities.json` can enter Simpler projection or preview; adding a registration for a banked-only form also fails closed. The existing five registrations are unchanged.

Verification: 25 focused tests; 225 non-DB form-spec and legacy Attachment XML tests; Ruff; changed-loader mypy; exact XSD SHA-256 `c6b7f40614a2077818f5f3b5df72959f867611b887c5b888005df8adeaa5e8e9` and `7e697ee33ea6f72271c0d74fc48c61f4f81faa242a712a4c73e7898f6c4ab976`; producer bundle SHA-256 `72aee82f3d5d04ff7862a978a5953e876489622c219d9482f2b712347e5a622e`. PR is intentionally unmerged for independent review.

## Formatting baseline and rebased review head

Public-fork formatting baseline [#52](https://github.com/mikec-ai/simpler-grants-gov/pull/52) isolated the pre-existing repository format debt from the promotion: formatting head `746b3350461b43211f5975943a8c7e12415fcca0`, merged to public-fork main as `caa617c1d1ee4aaebb016ed76c048f02cb5515ca`. Promotion PR [#51](https://github.com/mikec-ai/simpler-grants-gov/pull/51) then rebased cleanly and is open, unmerged, at review head `b2c647a395dc8b133fec92941e9b3a60eec84ef2`. Repository-wide isort, Black, and Ruff checks pass locally; 32 focused promotion/provenance/runtime tests pass. Hosted API and E2E runs are in progress.

### Hosted CI classification

At PR #51 head `b2c647a395dc8b133fec92941e9b3a60eec84ef2`, all hosted formatting, lint, migration, and security stages pass. The full API suite records 4,502 passed, 1 skipped, and 23 failures. Public-fork main at formatting baseline #52 records 4,499 passed, 1 skipped, and the exact same 23 failures; the three additional passing tests are the promotion’s banked-only fail-closed coverage. Both heads also fail before Playwright because the detached API server does not become ready within the workflow’s 800-second wait. No E2E assertion executes. These hosted failures are therefore classified as existing main-branch debt, not a promotion regression. PR #51 remains open and unmerged for independent review.
