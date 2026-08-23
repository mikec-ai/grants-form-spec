---
type: Task
title: Build a generic XML/XSD conformance harness
description: >-
  The reviewed generic XML/XSD conformance harness is merged, with mandatory
  official-digest linkage and fail-closed contract handling.
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:54:52.143Z'
superbee_progress_status: done
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

[uses producer output from](migrate-sf424c-parity-oracle.md)

# Delivery receipt

- Open producer PR: [mikec-ai/grants-form-spec#56](https://github.com/mikec-ai/grants-form-spec/pull/56)
- Branch: `codex/generic-xml-xsd-conformance`
- Rebased commits: `0b8fdcfef`, `cf8bae6ff`; exact head `cf8bae6fffb1fcacdb6cd936ab116772e83149dc`.
- Base includes producer main `b6298fd39` from PR #57.
- Added one resolved-profile reference interpreter with no form IDs or form-specific branches.
- Added digest-pinned offline XSD validation using `xmllint --nonet` and local dependency rewriting.
- Migrated SF-424C, SF-LLL, and R&R Senior/Key Person Profile (Expanded), including repeated people and attachments.
- Preserved form-specific representative responses, semantic XML assertions, exact source digests, and positive/negative XSD expectations.
- Independent review findings addressed: profile contract versions fail closed; declarative null constants and null value-map outputs fail closed; official profile digest and URI filename must match the pinned XSD entrypoint.
- Added three bounded negative-test groups for those review findings.
- Full `npm run preflight` passed after rebase: 102 TypeScript tests; 163 Python tests with one existing skip; 1,010 artifacts and 180 blocks validated; zero unclassified fields and zero exceptions.
- Status remains `in_progress` until independent review and merge.
