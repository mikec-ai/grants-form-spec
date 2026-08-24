---
type: Task
title: Model generic operational behavior evidence
priority: P1
description: >-
  Represent prefill, protected/read-only, and externally derived behavior
  generically and project it into analysis.
superbee_progress_status: in_progress
superbee_updated_by: review_cover_page
generated:
  by: 'process:superbee'
  at: '2026-08-24T04:10:20.367Z'
assignee: review_cover_page
---
# Goal

Design a generic, portable evidence representation for non-rule operational field behavior such as prefill, read-only/protected presentation, and externally derived values, then project that evidence into portfolio analysis without form-specific compiler or analyzer branches.

# Starting evidence

R&R Personal Data provides a bounded canary: its five PD/PI name fields are identified by the official DAT as `Forward-populated` from R&R SF-424 fields 14-1 through 14-5, and the pinned official XFA initializes each field from an R&R SF-424 value before setting its access to `protected`. These records remain source-bound and uncompiled in the current form audit.

# Acceptance criteria

- Define a generic evidence vocabulary that distinguishes operational behavior from calculations and conditions.
- Represent source and destination paths, operation kind, editability/protection, execution status, and exact source provenance without embedding form-specific logic.
- Project the evidence into analysis so prefill and protected-field dependencies are visible and filterable.
- Preserve the existing behavior-evidence contract until the generic design is reviewed.
- Add contract, projection, and negative tests; do not infer runtime behavior from source wording.

[depends on](correct-rr-personal-data-source-parity.md)
