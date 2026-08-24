---
type: Task
title: Author and integrate PHS Inclusion Enrollment Report
priority: P1
description: >-
  Reuse the Human Subjects dimensional enrollment model as a derivative form and
  resolve its source-backed conditions and calculations.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T01:19:11.643Z'
assignee: enrollment_derivative_agent
---
# Goal

Author PHS Inclusion Enrollment Report as a derivative of the Human Subjects dimensional enrollment foundation, demonstrating that a complex sibling becomes substantially cheaper.

# Evidence starting point

- Exact FID 791 v1.0 XSD, DAT, read-only PDF, XFA PDF, and NIH Forms I guide are pinned by physical SHA-256. No OCR was used.
- Exact XSD closure is GlobalLibrary V2.0 plus UniversalCodes V2.0 only.
- The physical XSD digest and legacy extraction-lineage digest remain explicitly distinct.

# Acceptance criteria

- Complete in producer PR. The standalone form composes the existing clinical-study/inclusion-enrollment-report core at 1..20 occurrences.
- The shared core contains the 6 context fields and 115 coordinate-qualified leaves once. An embedded-only wrapper adds the technical reportId used by Human Subjects; standalone cannot emit IER_id.
- All 8 F791 DAT navigation/capture behaviors and all 28 calculation targets are retained as exact source-bound uncompiled evidence. No operands, blank semantics, defaults, conditions, calculations, or read-only outputs were inferred.
- Exact XML root, namespace, sequence, direct report/country repetition, cardinalities, string/enum/numeric boundaries, comprehensive 115-coordinate serialization, and XSD closure validate.
- Analysis reports 121 exact associations, one reused semantic composite, zero new semantic questions, and no reviewed/published semantic mapping.
- No form-specific compiler, adapter, or runtime branch was added.

# Scope boundary

The standalone source proves calculated targets but does not pin exact operands or blank handling. Human Subjects behavior remains unchanged. Accessible dimensional grid headers, keyboard navigation, screen-reader coordinate context, focus/error movement, repeating-report controls, save/reload, locked, and print behavior remain explicit consumer and human-review gates rather than producer claims.

# Delivery receipt

- Branch: codex/phs-inclusion-enrollment-report
- Base: producer main 94a4d232f8b96ef09b09f36d4637156d62a25b65
- Verification: full preflight passed; 108 TypeScript tests and 228 Python tests passed with one existing skip.
- Marginal reuse: 1 reused semantic question, 0 new semantic questions, 121 source-qualified associations.
- Generic contract delta: none. The only refactor separates the reusable report core from its embedded-only technical identifier wrapper.

[depends on](author-integrate-phs-human-subjects.md)
