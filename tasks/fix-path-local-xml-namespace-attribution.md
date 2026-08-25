---
type: Task
title: Fix path-local XML namespace attribution
description: >-
  Preserve explicit mapping namespaces for colliding attachment and array
  element names across parent and imported schemas.
superbee_updated_by: codex_phs_human_subjects_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T19:33:20.956Z'
superbee_progress_status: in_progress
assignee: codex_phs_human_subjects_closure
---
# Defect

Portable XML generation used a flat last-write-wins `local element name -> namespace` index as a fallback. PHS Human Subjects reuses `attFile` and `ExemptionNumbers` in both the parent form namespace and the embedded Human Subject Study namespace. When both paths were populated, nested study mappings overwrote the parent namespace and produced XSD-invalid parent elements.

# Exact evidence

- Parent `Explanation/attFile`, `OtherRequestedInformation/attFile`, and delayed-onset `Justification/attFile` emitted in the embedded study namespace even though their mapping nodes declare `default`.
- Parent `ExemptionNumbers` emitted in the embedded study namespace when a study exemption mapping was present.
- The prior sparse Human Subjects XML test exercised only an embedded study attachment, so it did not expose the collision.
- Artifact scan found same-local-name multi-namespace mappings in PHS Human Subjects and R&R SF-424 variants. Existing scalar/object in-band metadata protects the R&R paths; attachment dictionaries and array containers lacked equivalent path-local attribution.

# Generic resolution

- Preserve each structured attachment mapping's explicit namespace in-band.
- Preserve each array container's explicit namespace as field-local metadata.
- Make that path-local metadata authoritative in the XML writer; retain the flat local-name map only as a legacy fallback.
- Add a generic default-versus-imported collision regression covering both arrays and attachments.
- Add a combined PHS parent, embedded-study, and delayed-onset regression that validates offline against the exact pinned parent/embedded XSD closure.

# Implementation checkpoint

Private-fork PR #131 is open at exact head `751c6fae36d1d78af005eaf26484b657f556698e`. It contains exactly two runtime files and three generic/shared/PHS regression files, with no form-ID branch or artifact mutation. Fifty-two attributable tests, Ruff, and targeted mypy are green. An unrelated amd64/QEMU browser-plan CLI subprocess segfault is explicitly excluded from the green claim. The PR is held for independent review.

# Boundaries

This task changes XML namespace attribution only. It does not accept semantic mappings, compile the eleven F705 conditions, infer the unresolved enrollment calculations, register the form, or close human semantic, visual, accessibility, privacy/policy, operational, UAT, or release gates.

[blocks](close-phs-human-subjects-technical-gates.md)
