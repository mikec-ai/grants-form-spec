---
type: Task
title: Enforce exact producer XSD fixture digests
priority: P0
description: >-
  Make producer preflight fail whenever a portable XML profile's official XSD
  digest does not match the byte-exact vendored fixture used for conformance.
superbee_progress_status: in_progress
superbee_updated_by: promote_new_forms
generated:
  by: 'process:superbee'
  at: '2026-08-24T02:40:07.789Z'
---
# Goal

Catch official-versus-normalized XSD drift in the producer before a package can merge or reach consumer promotion.

# Acceptance criteria

- Every emitted Grants.gov XML profile resolves its XSD URI basename to one byte-exact producer fixture.
- Producer preflight compares the fixture SHA-256 to the profile's official digest and fails on absence or mismatch.
- Derived, normalized, or dependency-rewritten fixtures may exist only with distinct provenance and may not satisfy the official-byte gate.
- The gate covers all profiles generically and adds no form-name list.
- A regression test reproduces the NIFA mismatch: normalized XML is rejected even when it is semantically equivalent and validates.
- Documentation tells authors to preserve original bytes and record separate hashes for transformations.

# Evidence

NIFA producer PR #63 passed exact-XSD semantic validation with a normalized fixture while the profile pinned official bytes. Consumer ingestion correctly rejected it, requiring producer PR #65.

# Delivery receipt, 2026-08-23

- Draft producer PR: https://github.com/mikec-ai/grants-form-spec/pull/66
- Final reviewed head: `5ba3dee844fdf0149a045d413014de7e279290ab` on `codex/enforce-profile-xsd-fixtures`
- Baseline producer revision: `a237bc9bdbc34784652840946faf46d53e10e3a4`
- Reconciliation: all 27 emitted XML profiles now resolve to exactly one byte-identical root fixture; 13 prior missing or normalized fixture debts were closed without changing any profile or semantic declaration.
- Machine-readable manifest binds each form to the exact official URI, native version, root role, SHA-256, and fixture path. The gate cross-checks the emitted profile and root-XSD evidence sidecar.
- Generic negative gates cover missing or normalized bytes, multiple same-basename candidates, wrong/relative/system URIs, wrong native version or path, non-root roles, duplicate path/source claims, and stale manifest rows. Native version is parsed independently from the official URI filename, so a manifest and evidence sidecar cannot agree on the same incorrect version. Sharing is not implicit.
- R&R Budget 10YR preserves two distinct lineages: physical official XSD SHA `e9d004c1...` and historical extraction source-set SHA `cccce035...` at authoritative extraction revision `dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef`; neither is rewritten to resemble the other.
- Full preflight: 109 TypeSpec tests passed; 250 Python tests passed with 2 skipped; 906-artifact bundle created and verified; classified-field gate reported 0 unclassified fields and 0 exceptions.
- Status: implementation complete and left unmerged for independent review.

[depends on](build-generic-xml-xsd-conformance-harness.md)

[informed by](../context-notes/nifa-supplemental-banking-retrospective.md)
