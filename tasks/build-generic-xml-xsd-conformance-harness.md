---
type: Task
title: Build a generic XML/XSD conformance harness
description: >-
  Replace repeated producer XML rendering and exact-XSD helpers with one
  profile-driven reference harness.
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:33:49.431Z'
superbee_progress_status: in_progress
priority: P0
assignee: xml_conformance_agent
---
# Goal

Replace repeated producer-side XML rendering and exact-XSD validation helpers with one target-neutral reference conformance harness driven by portable XML profiles and form-specific fixtures.

# Evidence

At least seven current producer test modules separately implement `render_xml` and/or `validate_exact_xsd`, including SF-424C, SF-424B, SF-424D, SF-LLL, CD-511, Grants.gov Lobbying, and R&R Key Person Expanded.

# Acceptance criteria

- Implement one test/reference XML projector that consumes the existing portable Grants.gov XML profile contract; it must not become a second production runtime or contain form IDs.
- Support the profile capabilities already demonstrated by the selected migrations: namespaces, fixed attributes, values, nested objects, arrays and wrapper cardinality, reusable mapping references, ordering, attachments, and declarative required-empty-object emission.
- Centralize exact-XSD validation, pinned digest checks, and local dependency rewriting without network access during tests.
- Migrate at least three structurally different existing forms, including SF-424C and one repeated/array form, to the harness while preserving their form-specific fixtures and semantic assertions.
- Make a new form test supply only representative responses, expected semantic XML assertions, pinned dependency information, and expected validity.
- Preserve exact source/version provenance and add or update tests for every behavior change.
- Add no form-specific compiler, adapter, or harness branch.

# Boundary

This is conformance infrastructure. It does not decide form semantics, generate canonical questions, or replace the portable XML declarations.

[depends on](migrate-sf424c-parity-oracle.md)
