---
type: Task
title: Migrate Attachment Form through the portable parity oracle
priority: P1
description: >-
  Replace the legacy SGG Attachment Form with portable ordered-attachment
  composition and differential XML/lifecycle parity.
superbee_progress_status: in_progress
superbee_updated_by: attachment_form_agent
generated:
  by: 'process:superbee'
  at: '2026-08-23T22:23:00.542Z'
assignee: attachment_form_agent
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

# Producer implementation receipt

Draft producer PR: https://github.com/mikec-ai/grants-form-spec/pull/59

Commit `3822da0a9` authors Attachment Form (FID 540, version 1.2) as fifteen optional, positional uses of one reusable `generics/ordered-attachment-slot` capture mechanism. That mechanism composes `generics/attachment`; neither block is counted as a semantic question. The prior generic-ordered semantic concept remains unreviewed and excluded from published coverage.

Exact authority is pinned in `evidence/forms/attachment-form/evidence.json`:

- official form XSD SHA-256 `c6b7f40614a2077818f5f3b5df72959f867611b887c5b888005df8adeaa5e8e9`;
- DAT FID 540 SHA-256 `e5d664667c014948b9cc6f35d3b0b61e26b3b9c247d42fbace3067588d013586`;
- instructions, read-only, and sample PDF SHA-256 digests;
- the complete dependency XSD closure, including UniversalCodes v2.0 at official SHA-256 `78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a`; and
- pre-prototype upstream SGG oracle revision `f84313418e237526adb90c5e57edef0b1bef0490`, whose pinned form declaration hashes to `6ad13ad5a6a2b02b17116d5922c623892c6ded7cad08c514290bb5bc758d3e79`.

The producer adds no form-ID branch. A generic presentation rule now treats a documented empty section declaration as static content, emitting a portable JSON Forms `Label` and an empty SGG informational section. This preserves the source instructions in reviewable data and retains the existing unused-section warning for undocumented mistakes.

The declarative XML profile uses the shared attached-file wire fragment and maps the canonical slots to the exact ordered `ATT1` through `ATT15` wrappers. Empty, single, sparse, fully populated, replacement, removal, and missing-reference cases run through the generic reference interpreter. Minimal and full output validate offline against the pinned exact-XSD contract. The checked-in form fixture is whitespace-normalized and has a separately asserted local digest; profile linkage still requires the physical official digest.

Independent review found that the evidence sidecar omitted UniversalCodes v2.0 even though the pinned GlobalLibrary dependency imports it and the exact-XSD fixture already used it. Commit `3822da0a9` adds the official source URI, native version, and exact SHA-256 plus a source-pin regression assertion. This is a provenance-closure correction only; the declarative architecture and runtime behavior are unchanged.

Full preflight passed on commit `3822da0a9`:

- 103 TypeScript tests;
- 173 Python tests passed, 1 skipped;
- 182 blocks and 1,024 artifacts validated;
- reproducible artifact package created and verified;
- 31 evidence sidecars projected;
- zero unclassified fields and zero classification exceptions; and
- analysis reconciled across 31 forms with Attachment Form adding capture-mechanism occurrences and zero semantic-question associations.

# Remaining gates

The producer slice is ready for independent review, but this task remains in progress. Save/reload, locked/print, attachment ownership/audit, and submission are consumer runtime concerns. The supervised producer-to-SGG promotion must exercise those cases against the portable package before registration. Accessibility review, semantic acceptance, instructions review, and production release also remain separate gates.

# Exit evidence

Publish the reusable attachment composition and fixtures needed by PHS 398 Research Plan.

[depends on](release-rr-key-person-expanded-canary.md)

[depends on](build-generic-xml-xsd-conformance-harness.md)

[depends on](enforce-rule-evidence-target-coverage.md)

[consumer delivery follows](automate-cross-repo-form-promotion.md)
