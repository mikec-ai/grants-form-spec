---
type: Task
title: Author and integrate R&R SF-424
priority: P0
assignee: codex
description: >-
  R&R SF-424 is now declaratively authored and merged in grants-form-spec; its
  public Simpler canary and typed conditional-UI runtime are merged. The
  remaining generic gates are encoded revision-checkbox semantics,
  conditional-requiredness presentation, lifecycle population, date comparison,
  exact XML, and release validation.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T21:20:58.086Z'
---
# Objective

Author and integrate the R&R SF-424 form as a production-oriented portable form, using shared questions only where source evidence supports the same semantic identity.

# Review dimensions

- Exact form/version identity and authoritative XSD, instruction, PDF, and existing implementation sources.
- Applicant questions, calculated or supplied values, conditions, attachments, repeating groups, validation, XML mappings, save/reload, print, and accessibility behavior.
- Reuse with SF-424, R&R Budget, and existing question-bank blocks.

# Agent validation findings

- Source identity is `RR_SF424_5_0`, version 5.0, Grants.gov FID 768, namespace `http://apply.grants.gov/forms/RR_SF424_5_0-V5.0`, and OMB 4040-0001.
- Deterministic extraction currently yields 139 XSD records and 145 DAT behavior records without warnings, plus an exact XML plan.
- Strong reuse candidates include applicant organization identity and address, opportunity identifiers, project identity and dates, congressional district, and authorized representative data.
- Similar-looking fields that require explicit profiles include the point-of-contact email, applicant-type cardinality, submission type, and state-review semantics.
- New content includes workflow identifiers, expanded application and revision types, small-business flags, principal-investigator data, funding questions, certification, and three semantic attachments.
- Generic capabilities needed before integration include encoded checkbox groups, copy-if-missing, clear-unless-all-equal, date-not-before, form registration, and exact wire sequencing.
- Source conflicts, including expiration metadata and state-review values, must remain explicit until resolved.

# Acceptance criteria

- The form is declaratively authored without a form-specific compiler or adapter branch.
- Semantic review distinguishes shared meaning from merely similar labels.
- Source and version provenance accompanies emitted evidence.
- The generic Simpler adapter loads the form and focused parity/behavior tests pass.
- Remaining human review, policy, accessibility, and release work is explicit.

# Promotion path

If the Performance Site promotion spike is reviewed and merged, use its generic importer to stage R&R SF-424's deterministic source facts, provenance, behavior evidence, and review gates. Do not import proposed semantic identities as accepted reuse. The canonical R&R SF-424 declaration remains authored and reviewed in this repository.
