---
type: Task
title: Migrate Attachment Form through the portable parity oracle
priority: P1
description: >-
  Replace the legacy SGG Attachment Form with portable ordered-attachment
  composition and differential XML/lifecycle parity.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:42:52.833Z'
---
# Goal

Replace SGG's legacy Attachment Form with a portable composition and use the legacy implementation as the ordered-attachment parity oracle.

# Evidence starting point

- The research factory records 91 source question/structure records, 18 behavior records, four proposed components, and fifteen working attachment slots.
- SGG already provides schema, UI, XML mappings, the official XSD, fixtures, and extensive attachment/lifecycle tests.

# Acceptance criteria

- Pin exact official source versions/hashes and the legacy SGG oracle revision.
- Reuse the portable attachment primitive and declare ordered slot cardinality, labels, instructions, and mappings without fifteen copied component implementations.
- Exercise empty, single, maximum, ordering, replacement/removal, invalid attachment, save/reload, locked/print, and submission cases against legacy and portable implementations.
- Generate minimal and fully populated Grants.gov XML and validate against the exact official XSD.
- Classify all parity differences and preserve unresolved source or product decisions explicitly.
- Add no Attachment-Form-specific compiler or adapter branch.
- Cut registration over only after applicable accessibility, semantic, instruction, and release gates pass.

# Exit evidence

Publish the reusable attachment composition and fixtures needed by PHS 398 Research Plan.

[depends on](release-rr-key-person-expanded-canary.md)

[depends on](build-generic-xml-xsd-conformance-harness.md)

[depends on](enforce-rule-evidence-target-coverage.md)

[depends on](automate-cross-repo-form-promotion.md)
