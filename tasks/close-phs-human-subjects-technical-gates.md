---
type: Task
title: Close PHS Human Subjects technical gates
description: >-
  Gather dedicated adapter/runtime, exact XML/XSD, dimensional enrollment,
  repeat, and bounded browser evidence for the unregistered PHS Human Subjects
  form.
superbee_updated_by: codex_phs_human_subjects_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T18:11:21.683Z'
priority: P1
assignee: codex_phs_human_subjects_closure
superbee_progress_status: in_progress
---
# Goal

Close the smallest automated technical handoff for the already-banked, unregistered PHS Human Subjects and Clinical Trials Information form through the generic portable adapter and Simpler runtime.

# Bounded first step

- Start from private-fork main after NIFA, PHS 398 Research Plan, PHS 398 Cover Page Supplement, and focused-CI merges.
- Collision-check active SBIR/STTR PR #122, lobbying cohort PR #125, and the externally owned R&R Subaward Budget 10YR/30 lane.
- Inventory existing producer and consumer evidence for read-only controls, booleans, flattened and nested arrays, repeating studies, the 115-coordinate enrollment composite, conditions, attachments, exact provenance, XML/XSD, and unresolved semantics.
- Do not add shared runtime behavior until a concrete generic defect is isolated and reported.

# Technical acceptance criteria

- Dedicated consumer tests load the banked artifact through the generic adapter without registration or form-specific branches.
- Exact artifact/source/XSD provenance and representative parent-plus-embedded-study XML validate offline against the pinned closure.
- All executable behavior is proved from compiled rules; source-bound-uncompiled conditions and unresolved calculations remain explicit.
- Repeating studies, flattened scalar arrays, nested arrays, dimensional enrollment coordinates, read-only projections, booleans, and attachment rules receive bounded positive and negative coverage proportional to risk.
- Four-browser bounded evidence covers preview registration, adapter preflight, render, deterministic save/reload, automated accessibility scan, and print; attachment behavior remains separately attributable.

# Required open gates

- The eleven F705 source conditions remain uncompiled unless accepted source-backed rules are present.
- The 28 total-like enrollment coordinates remain applicant-entered/observed; no arithmetic is inferred.
- Semantic mappings remain proposed and contribute nothing to reviewed coverage.
- Dimensional-grid usability, keyboard navigation, focus/error behavior, screen-reader behavior, agency-profile behavior, instructions, privacy/security, policy, human semantic review, visual/content review, operational review, UAT, registration, and production release remain open.

[depends on](author-integrate-phs-human-subjects.md)

[consumer delivery follows](automate-cross-repo-form-promotion.md)
