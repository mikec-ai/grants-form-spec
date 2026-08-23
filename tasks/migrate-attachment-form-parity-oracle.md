---
type: Task
title: Migrate Attachment Form through the portable parity oracle
priority: P1
description: >-
  Replace the legacy SGG Attachment Form with portable ordered-attachment
  composition and differential XML/lifecycle parity.
superbee_progress_status: in_progress
superbee_updated_by: promote_new_forms
generated:
  by: 'process:superbee'
  at: '2026-08-23T23:44:51.891Z'
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

Commit `47df8fcd4` authors Attachment Form (FID 540, version 1.2) as fifteen optional, positional uses of one reusable `generics/ordered-attachment-slot` capture mechanism. That mechanism composes `generics/attachment`; neither block is counted as a semantic question. The prior generic-ordered semantic concept remains unreviewed and excluded from published coverage.

Exact authority is pinned in `evidence/forms/attachment-form/evidence.json`:

- official form XSD SHA-256 `c6b7f40614a2077818f5f3b5df72959f867611b887c5b888005df8adeaa5e8e9`;
- DAT FID 540 SHA-256 `e5d664667c014948b9cc6f35d3b0b61e26b3b9c247d42fbace3067588d013586`;
- instructions, read-only, and sample PDF SHA-256 digests;
- the complete dependency XSD closure, including UniversalCodes v2.0 at official SHA-256 `78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a`; and
- pre-prototype upstream SGG oracle revision `f84313418e237526adb90c5e57edef0b1bef0490`, whose pinned form declaration hashes to `6ad13ad5a6a2b02b17116d5922c623892c6ded7cad08c514290bb5bc758d3e79`.

The producer adds no form-ID branch. A generic presentation rule now treats a documented empty section declaration as static content, emitting a portable JSON Forms `Label` and an empty SGG informational section. This preserves the source instructions in reviewable data and retains the existing unused-section warning for undocumented mistakes.

The declarative XML profile uses the shared attached-file wire fragment and maps the canonical slots to the exact ordered `ATT1` through `ATT15` wrappers. Empty, single, sparse, fully populated, replacement, removal, and missing-reference cases run through the generic reference interpreter. Minimal and full output validate offline against the pinned exact-XSD contract. The checked-in form fixture is whitespace-normalized and has a separately asserted local digest; profile linkage still requires the physical official digest.

Independent review found that the evidence sidecar omitted UniversalCodes v2.0 even though the pinned GlobalLibrary dependency imports it and the exact-XSD fixture already used it. Commit `47df8fcd4` includes the official source URI, native version, and exact SHA-256 plus a source-pin regression assertion. This is a provenance-closure correction only; the declarative architecture and runtime behavior are unchanged.

After PHS Assignment Request merged to producer main at `abb119400`, the Attachment Form branch was rebased and the form sequence and aggregate analysis expectations were reconciled mechanically so both forms remain. No form semantics or architecture changed in the rebase.

Final re-review found a stale README aggregate after the rebase. Commit `47df8fcd4` documents all 32 reference forms, explicitly includes PHS Assignment Request and Attachment Form, and adds a regression assertion tying the README count to the canonical form sequence.

Full preflight passed on final commit `47df8fcd4`:

- 103 TypeScript tests;
- 182 Python tests passed, 1 skipped;
- 188 blocks and 1,054 artifacts validated;
- reproducible artifact package created and verified;
- 32 evidence sidecars projected;
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

# Consumer banking receipt

Consumer PR [#51](https://github.com/mikec-ai/simpler-grants-gov/pull/51) banks Attachment Form from immutable producer revision `2fde5118f440f31c7527fde784d573bb3ab3d912` without adding a runtime identity or registration. The 31-form selection contains 342 digest-verified artifacts and pins producer bundle SHA-256 `72aee82f3d5d04ff7862a978a5953e876489622c219d9482f2b712347e5a622e`.

The first hosted promotion run [32670976757](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32670976757) failed closed because the consumer stored an LF-normalized copy of the Attachment XSD (`ac392f51bdeb17ffe734f3008e2c2ad67a71a46c9051829f39ee02ce136a4a20`) while the producer correctly pins official raw bytes `c6b7f40614a2077818f5f3b5df72959f867611b887c5b888005df8adeaa5e8e9`. PR #51 vendors the exact official bytes and preserves them as binary; the producer offline conformance fixture remains a separately declared reformatted lineage (`dc3ae0af03a52b3a062dc74745b2e355a6c6ce1cc1b53a6c955cd2f972f11466`). No provenance check was weakened.

Generic artifact/XSD integrity, 25 focused tests, 225 non-DB form-spec and legacy Attachment XML tests, Ruff, and changed-loader mypy pass. `registrations.json` is unchanged. The form remains banked-only, unavailable to runtime projection or preview, and unregistered pending explicit consumer identity/projection plus the existing human and release gates.

## Formatting baseline and rebased review head

Public-fork formatting baseline [#52](https://github.com/mikec-ai/simpler-grants-gov/pull/52) isolated the pre-existing repository format debt from the promotion: formatting head `746b3350461b43211f5975943a8c7e12415fcca0`, merged to public-fork main as `caa617c1d1ee4aaebb016ed76c048f02cb5515ca`. Promotion PR [#51](https://github.com/mikec-ai/simpler-grants-gov/pull/51) then rebased cleanly at review head `b2c647a395dc8b133fec92941e9b3a60eec84ef2`. Repository-wide isort, Black, and Ruff checks pass locally; 32 focused promotion/provenance/runtime tests pass. Hosted API and E2E comparisons are recorded below.

### Hosted CI classification

At PR #51 head `b2c647a395dc8b133fec92941e9b3a60eec84ef2`, all hosted formatting, lint, migration, and security stages pass. The full API suite records 4,502 passed, 1 skipped, and 23 failures. Public-fork main at formatting baseline #52 records 4,499 passed, 1 skipped, and the exact same 23 failures; the three additional passing tests are the promotion’s banked-only fail-closed coverage. Both heads also fail before Playwright because the detached API server does not become ready within the workflow’s 800-second wait. No E2E assertion executes. These hosted failures are therefore classified as existing main-branch debt, not a promotion regression. After independent review and the baseline comparison, PR #51 was merged by the repository owner at  as public-fork main commit . The promotion agent did not issue the merge.
