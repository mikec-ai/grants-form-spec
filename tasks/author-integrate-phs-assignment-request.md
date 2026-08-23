---
type: Task
title: Author and integrate PHS Assignment Request
priority: P1
description: >-
  Deliver the small high-volume assignment-preference profile without
  introducing a PHS-specific workflow engine.
superbee_progress_status: in_progress
superbee_updated_by: promote_new_forms
generated:
  by: 'process:superbee'
  at: '2026-08-23T23:45:20.307Z'
assignee: assignment_request_agent
---
# Goal

Author PHS Assignment Request as a small, high-volume, bounded review-routing profile.

# Evidence starting point

- The research factory records fourteen source question/structure records, thirteen applicant-entered behavior records, and eleven presentation records with a complete behavior partition.
- Two-year usage evidence records 237,461 form instances.

# Acceptance criteria

- Pin and promote exact official XSD, DAT, PDF/XFA, instruction, version, and hash evidence.
- Model awarding-component preferences, study-section preferences, rationales, reviewer expertise, and excluded-reviewer requests declaratively.
- Keep the bounded assignment-preference profile separate from the common application core and from SGG-specific workflow orchestration.
- Reuse canonical identity or organization concepts only where role-qualified semantic evidence supports them.
- Validate optional and repeated preferences, limits, save/reload, locked/print, XML/XSD, submission, and accessibility.
- Add no PHS-specific workflow engine and no form-specific compiler or adapter branch.
- Register only after applicable semantic, privacy, policy, instruction, accessibility, and operational gates pass.

# Producer delivery receipt

Draft producer PR: https://github.com/mikec-ai/grants-form-spec/pull/58

Current head: `8d76d5d704e3a436f27f61ccdf00d9123379be1a`

The PR authors FID 833, version 4.0 as thirteen optional fixed source occurrences composed from five source-local declarative question blocks. It adds no runtime, compiler, adapter, renderer, workflow, lookup, or form-specific conformance branch.

Independent review fixes on current head:

- All five question blocks declare `applicantInput`, inherited by all thirteen emitted and analyzed occurrences.
- All thirteen exact occurrence-to-XSD paths are recorded as proposed mappings. Accepted and publishable semantic coverage remains zero.
- The dynamic NIH G.600 page is represented by a checked-in normalized capture with original retrieval hash, retrieval date, Forms I edition/revision, transformation method, whitespace and no-OCR boundary, and the unresolved `B10`/`BP10` conflict.

Pinned evidence:

- XSD SHA-256 `7e697ee33ea6f72271c0d74fc48c61f4f81faa242a712a4c73e7898f6c4ab976`.
- DAT SHA-256 `e08625bf4ebaee23a66e1ef85346c83e86726a58e36a6c5705f66fffaf867255`.
- Grants.gov readonly XFA PDF SHA-256 `0fdcbdd7bc136ae2872b76fc61a6cb719d8d02d9a1967257a7c9c2e957e4680a`, retrieved 2026-08-23.
- Normalized NIH Forms I section G.600 capture SHA-256 `6aef68689060890e9c3cc650a040ea8b36f893527049e582b9474032368b1120`; original live HTML SHA-256 `e12101cdc12d38cfc9942744e25aec93e28d0a0bee1465cbf615e7187cb64c54`, retrieved 2026-08-23.
- Crosswalk revision `4312f6504b060e2b9ffdbd2307fc41130c3123a0`; extracted source-set SHA-256 `63ef51469ecffd0b7a39bd58f827ebe88bc60e8d368ed0789e4608a862660b4b`.

Verification receipt:

- `npm run preflight` passed.
- Updated-head GitHub CI passed in 1m27s: https://github.com/mikec-ai/grants-form-spec/actions/runs/32670351671/job/97270159780
- 102 TypeScript/TypeSpec tests and 171 Python tests passed locally; one existing environment-dependent test skipped.
- Artifact, promotion, package, exact XML/XSD, evidence coverage, and independent TypeSpec compilation checks passed.
- Classified field gate passed with zero unclassified fields and zero exceptions.

# Explicitly unresolved

- Crosswalk concepts remain agent-proposed and excluded from reviewed coverage.
- Awarding-component and study-section values remain bounded free strings; no enum or lookup was inferred.
- The readonly PDF uses illustrative study-section code `B10`, while the DAT uses `BP10`. The authored help omits the disputed example and exact visual/instruction parity is not claimed.
- Reviewer exclusion remains one source-defined free-text response. No person or organization equivalence was inferred; privacy and access-control review remains open.
- Save/reload, locked/print, submission, accessibility, consumer integration, registration, and production approval remain downstream gates.
- PR #58 remains open for independent review and is intentionally unmerged.

# Exit evidence

The producer form landed in a focused PR without a runtime extension. Its source-specific implementation consists of one declarative form, five source-local question blocks, one evidence sidecar, one XML target profile, one exact official XSD fixture, and focused tests/documentation.

[depends on](release-rr-key-person-expanded-canary.md)

[depends on](build-generic-xml-xsd-conformance-harness.md)

[depends on](enforce-rule-evidence-target-coverage.md)

[consumer delivery follows](automate-cross-repo-form-promotion.md)

# Consumer banking receipt

Consumer PR [#51](https://github.com/mikec-ai/simpler-grants-gov/pull/51) banks PHS Assignment Request from immutable producer revision `2fde5118f440f31c7527fde784d573bb3ab3d912` without inventing workflow behavior, a runtime identity, compatibility projection, or registration. The 31-form selection contains 342 digest-verified artifacts and pins producer bundle SHA-256 `72aee82f3d5d04ff7862a978a5953e876489622c219d9482f2b712347e5a622e`. The exact official XSD is vendored at SHA-256 `7e697ee33ea6f72271c0d74fc48c61f4f81faa242a712a4c73e7898f6c4ab976`.

Generic artifact/XSD integrity, 25 focused tests, 225 non-DB form-spec and legacy Attachment XML tests, Ruff, and changed-loader mypy pass. `registrations.json` is unchanged. The form remains banked-only, unavailable to runtime projection or preview, and unregistered pending explicit consumer identity/projection plus semantic, privacy, policy, instruction, accessibility, operational, and release review.

## Formatting baseline and rebased review head

Public-fork formatting baseline [#52](https://github.com/mikec-ai/simpler-grants-gov/pull/52) isolated the pre-existing repository format debt from the promotion: formatting head `746b3350461b43211f5975943a8c7e12415fcca0`, merged to public-fork main as `caa617c1d1ee4aaebb016ed76c048f02cb5515ca`. Promotion PR [#51](https://github.com/mikec-ai/simpler-grants-gov/pull/51) then rebased cleanly at review head `b2c647a395dc8b133fec92941e9b3a60eec84ef2`. Repository-wide isort, Black, and Ruff checks pass locally; 32 focused promotion/provenance/runtime tests pass. Hosted API and E2E comparisons are recorded below.

### Hosted CI classification

At PR #51 head `b2c647a395dc8b133fec92941e9b3a60eec84ef2`, all hosted formatting, lint, migration, and security stages pass. The full API suite records 4,502 passed, 1 skipped, and 23 failures. Public-fork main at formatting baseline #52 records 4,499 passed, 1 skipped, and the exact same 23 failures; the three additional passing tests are the promotion’s banked-only fail-closed coverage. Both heads also fail before Playwright because the detached API server does not become ready within the workflow’s 800-second wait. No E2E assertion executes. These hosted failures are therefore classified as existing main-branch debt, not a promotion regression. After independent review and the baseline comparison, PR #51 was merged by the repository owner at 2026-08-23T23:44:10Z as public-fork main commit d08e0c64f50a374e515a1f5184ae68f4600653ad. The promotion agent did not issue the merge.
