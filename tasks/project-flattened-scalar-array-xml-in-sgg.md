---
type: Task
title: Project flattened scalar-array XML in SGG
priority: P0
description: >-
  Teach the generic Simpler XML adapter to execute the producer's fail-closed
  flattened scalar-array item contract without form-specific branches.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T04:31:21.090Z'
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

[depends on](add-portable-form-preview-registration.md)
