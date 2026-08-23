---
type: Task
title: Author and integrate PHS Assignment Request
priority: P1
description: >-
  Deliver the small high-volume assignment-preference profile without
  introducing a PHS-specific workflow engine.
superbee_progress_status: in_progress
superbee_updated_by: assignment_request_agent
generated:
  by: 'process:superbee'
  at: '2026-08-23T22:12:39.385Z'
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

Commit: `80891939ec7e6f0fbbd0a0e4284dedcd8a12035d`

The PR authors FID 833, version 4.0 as thirteen optional fixed source occurrences composed from five source-local declarative question blocks. It adds no runtime, compiler, adapter, renderer, workflow, lookup, or form-specific conformance branch.

Pinned evidence:

- XSD SHA-256 `7e697ee33ea6f72271c0d74fc48c61f4f81faa242a712a4c73e7898f6c4ab976`.
- DAT SHA-256 `e08625bf4ebaee23a66e1ef85346c83e86726a58e36a6c5705f66fffaf867255`.
- Grants.gov readonly XFA PDF SHA-256 `0fdcbdd7bc136ae2872b76fc61a6cb719d8d02d9a1967257a7c9c2e957e4680a`, retrieved 2026-08-23.
- NIH Forms I section G.600 instructions SHA-256 `e12101cdc12d38cfc9942744e25aec93e28d0a0bee1465cbf615e7187cb64c54`, retrieved 2026-08-23.
- Crosswalk revision `4312f6504b060e2b9ffdbd2307fc41130c3123a0`; extracted source-set SHA-256 `63ef51469ecffd0b7a39bd58f827ebe88bc60e8d368ed0789e4608a862660b4b`.

Verification receipt:

- `npm run preflight` passed.
- GitHub CI passed: https://github.com/mikec-ai/grants-form-spec/actions/runs/32669787954/job/97268717511
- 102 TypeScript/TypeSpec tests and 170 Python tests passed; one existing environment-dependent test skipped.
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
