---
type: Task
title: Close R&R SF-424 release gates
priority: P0
assignee: codex
description: >-
  Build generic lifecycle conformance evidence for R&R SF-424; close
  high-confidence conditional validation, save/reload, locked/print, XML/XSD,
  and accessibility gates; register only after the relevant gates pass.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T14:06:53.831Z'
---
# Scope

- Keep the portable producer authoritative and the Simpler integration generic.
- Add reusable lifecycle and wire conformance rather than form-specific runtime shortcuts.
- Preserve unresolved source conflicts and human approval gates explicitly.
- Work only in mikec-ai public repositories; do not modify HHS upstream.

## Completed

- Added the missing RRSF424 Simpler runtime type.
- Added a reusable lifecycle conformance helper that executes the production registry, validator, and rule processor.
- Proved JSON save/reload preservation, corrected-application and renewal requirements, and submit-time signature/date population.
- Added a declarative Grants.gov XML profile covering all 28 top-level response fields, nested structures, and three attachments.
- Pinned the official RR_SF424 5.0 XSD by URL and SHA-256.
- Added generic wire-only output groups with absolute source pointers, keeping CongressionalDistrict out of the canonical question model.
- Fixed path-local scalar namespace handling generically after XSD execution exposed an element-name collision.
- Corrected form namespace selection and XSD sequence order in the declarative producer mapping.
- Proved a representative submit-populated response validates against the pinned official XSD.
- Merged producer PRs 28 and 29 and adapter PRs 25, 26, and 27 to main.
- Verification: 22 focused tests pass; 458 broader XML tests pass. The other 103 XML-suite cases cannot initialize without the local grants-db service.

## Remaining

- Human review of the source-bound XML mapping and semantic/policy decisions. Current evidence remains source-bound-unreviewed and does not count as reviewed coverage.
- Form-specific rendered and locked/print evidence.
- Accessibility review and final release acceptance.
- Runtime registration only after the relevant release gates are accepted.

## Architectural evidence

R&R SF-424 validated the intended boundary: canonical questions remain independent of Grants.gov wire wrappers, portable targets declare the wire contract, and the Simpler adapter compiles those declarations generically. Exact XSD execution caught reusable namespace and ordering defects without introducing form-specific Python logic.

[depends on](author-integrate-rr-sf424.md)
