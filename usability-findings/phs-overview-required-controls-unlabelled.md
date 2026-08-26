---
type: Usability Finding
title: PHS overview required controls are unlabeled
superbee_progress_status: triaged
severity: blocker
category: accessibility
affected_layer: form_spec
form_id: phs-human-subjects
stable_field_path: /properties/involvesHumanSubjects
reproduction: >-
  Open the form, inspect the overview, and trigger requiredness by adding a
  study.
evidence_ref: local application 97b7c1b5-7a6b-4bbc-997d-413d6d5eb296
superbee_updated_by: codex
---
# Observation

On the ordinary Simpler application-form route, the `Use of Human Specimens and/or Data` section
rendered its first four applicant controls as empty text boxes with no visible label and no
accessible name. The form simultaneously reported required-field errors, so an applicant could
not determine which question each control answered or how to correct the error.

# Reproduction

1. Open the portable PHS Human Subjects form in a local Simpler application.
2. Inspect the first section before adding a study.
3. Observe four visually blank text boxes; the DOM exposes each only as `textbox`.
4. Add a study to trigger validation and observe required-field errors adjacent to still-unlabelled controls.

# Evidence boundary

Observed against consumer commit `e34c1478593c8e09925643dc354b50cf80837932`, producer commit
`273d1ba8da96a958448d9c19209a50b8cbe2c0dc`, and manifest SHA-256
`c31c759743a5266cd9ea941df73bc7edaf0d5ae68bb4250265ac44e7d86892f9`. Root-cause ownership is
not yet assigned: the portable schema mixes local `allOf` definitions and question-bank `$ref`
definitions, and the rendered symptom must be traced through both projection and runtime resolution.

# Triage

Producer PR [#119](https://github.com/mikec-ai/grants-form-spec/pull/119) adds explicit
source-shaped labels to the three system-owned determinations and the specimens/data question.
Keep this finding open until those artifacts are promoted into the consumer and the exact browser
scenario verifies accessible names.
