---
type: Task
title: Migrate Grants.gov Lobbying Form through the portable parity oracle
priority: P1
description: >-
  The portable, unregistered Grants.gov Lobbying Form implementation and
  public-fork consumer canary are merged; remaining release gates are tracked
  separately.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:44:22.426Z'
assignee: gg_lobbying_agent
---
# Goal

Replace SGG's legacy Grants.gov Lobbying Form with portable artifacts as a sibling certification profile that reuses shared identity and attestation foundations without importing SF-LLL disclosure semantics.

# Evidence starting point

- The research factory records eleven source question/structure records, twenty behavior records, four static-policy items, and four proposed components.
- SGG already provides schema, UI, rules, XML mappings, the official XSD, fixtures, and lifecycle behavior.
- Two-year usage evidence records 39,941 form instances.

# Acceptance criteria

- Pin exact official source versions/hashes and the legacy SGG oracle revision.
- Reuse reviewed identity, representative, signature, date, and attestation primitives without importing SF-LLL-specific disclosure semantics.
- Preserve the Grants.gov Lobbying Form as its own versioned certification profile.
- Run complete, missing-attestation, signature/date, application-context, XML, save/reload, locked/print, and submission fixtures through legacy and portable implementations.
- Validate XML against the exact official XSD and classify every parity difference.
- Add no form-specific compiler or adapter branch.
- Register only after applicable semantic, policy, accessibility, instruction, and release gates pass.

# Delivery receipt — 2026-08-23

## Producer — merged

- PR 49: https://github.com/mikec-ai/grants-form-spec/pull/49
- Immutable merge commit: `7ebb2033de2cd7c31a6039fd3b7f492adb70aeed`.
- Grants.gov Lobbying remains form id `gg-lobbying`, FID 255, version 1.1, distinct from `sflll`.
- The form composes `primary-org/legal-name`, `aor/name`, `aor/title`, `aor/signature`, and `aor/date-signed`; all ten measured question occurrences have existing bank lineage and the form adds no unclassified field debt.
- Immutable certification text is `policy-content/v1` (`grants-gov/lobbying-certification@1.1`); submission attestation and response pointers are `form-policy-binding/v1`.
- The shared policy projector from PR 48 emits the static SGG presentation. The temporary documented-empty-section behavior and its commit are absent from merged history.
- The form owns a portable Grants.gov XML target and exact official-XSD fixture. No form-specific compiler behavior was added.
- Emitted policy artifact digests: `policy-content.json` = `21f0e972f0a7b7929bfa3644d4efeebdfddd344994772c3ad1725d3f4e8ef403`; `policy-binding.json` = `59f49779ba7e942353ab118c54313e94e3f2ee1db11b3ff55f638ba985a7ab7a`.

## Exact provenance

- Official XSD: `a41d88b19e240dbb5f9b13815c0426d2396414fc1af8d6ab6a96f35855a0a5f7`
- Official readonly PDF: `9c8194fd874951382f448a047c81fe1a901f5f70cb9bfeb7e31a7478748b6439`
- Official instructions PDF: `72062133a94e4757b90a8694c900d5303daa62d2093f3d4444f1aae0bb5ba0e8`
- Official DAT worksheet: `4489cf1e023991a36a49d4015b323fb87ad152dfa915ef750f0f19c5d5138ba2`
- Crosswalk revision: `4312f6504b060e2b9ffdbd2307fc41130c3123a0`
- Extracted source-set digest: `b545bd44a103bba32721c07e7e1dd0d708e5435b416a2ccf1005cc4de9325895`
- Legacy SGG oracle revision: `30dd50cf0493146c32f89f78398979523e040080`
- Legacy `form_json.py` digest: `bdf73a05a75b5020218f06864118f4c1e9ccc396934feaccc49e9acbbe406ad8`

## Consumer — merged

- PR 42: https://github.com/mikec-ai/simpler-grants-gov/pull/42
- Immutable merge commit: `9a912428ba6cf5c33f417f95d0a4207fe68e3d7a`.
- The adapter pins immutable merged producer revision `7ebb2033de2cd7c31a6039fd3b7f492adb70aeed` in the 22-form, 242-artifact selection at merge.
- The already-shared artifact selector retains declared `policy-content.json` and `policy-binding.json`; GG Lobbying adds only declarative legacy UI identifier projection and the existing SGG runtime identity.
- Required-field, nested representative, signature/date, submitter application-context, JSON save/reload, browser/print UI-input, XML, exact-XSD, policy, evidence, and legacy-oracle parity canaries pass.
- Portable XML is canonically equal to legacy output and validates against the exact official XSD.
- `gg-lobbying` remains absent from `registrations.json`; no production cutover or HHS upstream change was made.

## Validation

- Producer preflight at the immutable merged revision passed: 99 TypeScript tests and 98 Python tests, with 8 environment/source-checkout skips.
- Producer artifact validation passed for 138 blocks and 774 artifacts; package verification covered 519 artifacts; the unclassified-field ratchet was 49 at that merge.
- Consumer focused GG Lobbying/CD-511/selector/provenance/integrity/registration/XML tranche: 48 passed.
- Consumer portable-form tranche excluding the database-backed SF-424A lifecycle module: 187 passed.
- Ruff passed for the changed consumer test surface.
- Independent post-merge validation on `9a912428ba6cf5c33f417f95d0a4207fe68e3d7a` passed 39 focused canary, artifact integrity/provenance, registration-boundary, sync-selection, XML, and exact-XSD tests. The merged tree exactly matched an independent regeneration from producer `7ebb2033de2cd7c31a6039fd3b7f492adb70aeed`.
- Fork-only PR 45 removed the single extra blank line in `test_gg_lobbying_portable.py` and merged as `ef863fe137b8afa5e5ac0d7fd2f2d3d5405ea56d`. Black and Ruff pass, and the focused GG Lobbying module remains green at 7 tests; no behavior, registration, or HHS/upstream change was included.
- Both repository PRs are merged; no configured consumer CI checks were reported.

# Remaining release gates

- Obtain semantic and policy-owner approval for the exact certification text and proposed question reuse.
- Complete accessibility and instruction review.
- Explicitly approve production registration/cutover.
- With an available DB/browser environment, run the registered browser, locked-state, print, persistence, and full submission route before production registration.

# Exit evidence

The portable, unregistered bank implementation is landed end to end. Actual reuse is ten question occurrences with existing canonical lineage, five direct shared question compositions, one generic versioned policy binding, one portable XML profile, and one declarative consumer identifier projection. The remaining differences are the versioned lobbying certification content and official wire/root identity; SF-LLL disclosure questions and filing behavior are not imported.

[depends on](migrate-sflll-parity-oracle.md)
