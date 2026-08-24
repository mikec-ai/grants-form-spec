---
type: Task
title: Project flattened scalar-array XML in SGG
priority: P0
description: >-
  Merged consumer PR 78: generic flattened scalar and attachment item-node XML
  execution, reviewed fail-closed metadata propagation, and fully offline
  exact-XSD validation for representative PHS forms.
superbee_progress_status: done
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T18:55:16.234Z'
assignee: flattened_xml
---
# Goal

Project portable flattened scalar-array items into the existing Simpler XML runtime so repeated simple-content elements such as EnrollmentCountry execute generically and validate against their exact source XSDs.

# Starting evidence

The producer contract and reference runtime already validate this shape. The manifest-driven preview spike found that Simpler currently rejects a value item with flatten=true at reports.enrollmentCountries[*]. Preview therefore omits XML explicitly rather than claiming unsupported execution.

# Acceptance criteria

- Extend the generic portable-to-SGG XML projection and, only if required, the shared serializer vocabulary for flattened scalar-array items.
- Preserve fail-closed validation for illegal flatten contexts and ignored properties.
- Add positive tests for direct repeated simple-content elements and negative contract tests.
- Validate representative PHS Inclusion Enrollment Report and PHS Human Subjects XML against their pinned exact XSDs.
- Add no form-id, element-name, or namespace branches.
- Keep banking, preview, runtime enablement, and production release gates separate.

# Implementation outcome

- Producer authority remains the already-merged and consumer-pinned `grants-form-spec` revision `563e7d8b5a38c7b5d66723bfbc1607caeeff4aad`. It contains the fail-closed flattened-item contract and both representative PHS profiles.
- Consumer implementation: [mikec-ai/simpler-grants-gov PR 78](https://github.com/mikec-ai/simpler-grants-gov/pull/78), commit `ae202aaf4`.
- The adapter now projects flattened scalar array items generically. The shared transformer emits either direct repeated simple-content elements or one container with declared item elements, based only on the portable declaration.
- Illegal flatten contexts and declarations with ignored properties remain rejected. No form IDs, element names, or namespaces are encoded in the implementation.
- PHS Inclusion Enrollment Report and nested PHS Human Subjects enrollment countries both validate against their exact pinned form XSD digests. The Human Subjects proof also executes its flattened attachment declaration and verifies the emitted `AttachedFile`, preventing an untested prerequisite capability.
- Independent review found and the implementation now closes two generic item-node metadata gaps: scalar and attachment arrays propagate `repeatElementPerItem` and `itemAttributes`, with positive execution tests for both.
- The exact-XSD proof vendors `HumanSubjectStudy_3_0-V3.0.xsd`, asserts all seven files in the PHS/Inclusion dependency closure by their official SHA-256 digests, and constructs both schemas with network access forbidden.
- Verification: 27 focused tests passed; Ruff and mypy passed. The earlier broader form-spec/XML cohort had 798 passing tests and 106 database setup errors because `grants-db` was unavailable, with no assertion failures.

# Remaining gate

Merge PR 78 after fork CI/review. This capability alone does not grant runtime identity or production approval to either PHS form.

[depends on](add-portable-form-preview-registration.md)
