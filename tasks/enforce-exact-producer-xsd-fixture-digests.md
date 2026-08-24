---
type: Task
title: Enforce exact producer XSD fixture digests
priority: P0
description: >-
  Make producer preflight fail whenever a portable XML profile's official XSD
  digest does not match the byte-exact vendored fixture used for conformance.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T01:38:10Z'
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

[depends on](build-generic-xml-xsd-conformance-harness.md)

[informed by](../context-notes/nifa-supplemental-banking-retrospective.md)
