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
  at: '2026-08-25T18:14:19.424Z'
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

# Initial consumer gap analysis

- The banked package is substantial and internally coherent: 189 UI fields across 195 nodes, five repeaters (studies, inclusion reports, interventions, outcomes, and delayed-onset studies), 15 distinct attachment mappings, 11 array mappings, five flattened scalar-array mappings, 172 XML value mappings, and exact parent/embedded-study XSD provenance.
- The projected schema contains no native JSON boolean scalar; yes/no determinations use exact source wire strings. The merged generic boolean-to-XML fix is therefore not directly exercised by this form.
- Existing consumer coverage is narrow: two flattened-scalar XML tests pass, including one structured study, two enrollment countries, and one attachment against the pinned parent/embedded XSD closure. It does not yet prove the 115 enrollment coordinates, nested/repeating study boundaries, all 15 attachment roles, comprehensive XML sequencing, validation lifecycle, or four-browser behavior.
- No executable conditions or calculations are declared. The browser plan correctly reports both capabilities not applicable; the eleven F705 conditions and the single unresolved calculation disposition covering 28 total-like coordinates remain source-bound-uncompiled.
- A shared browser-evidence defect blocks a valid bounded run: property-level `allOf` read-only declarations for `involves_human_subjects`, `exempt_from_federal_regulations`, and `exemptions` are missed, so the generic plan incorrectly selects them as editable. The three direct technical IDs are protected. No production or form-specific runtime code has been changed.
- Collision check is clean for a dedicated PHS Human Subjects test/fixture lane. PR #122 owns the portable CI map, so any map update must wait/rebase; PR #125 owns only three lobbying tests. The externally owned subaward lane is disjoint.

[depends on](fix-portable-browser-allof-readonly.md)

[depends on](author-integrate-phs-human-subjects.md)

[consumer delivery follows](automate-cross-repo-form-promotion.md)
