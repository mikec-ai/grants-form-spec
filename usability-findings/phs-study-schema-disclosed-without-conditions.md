---
type: Usability Finding
title: PHS study entry exposes the full unconditioned schema
superbee_progress_status: triaged
severity: major
category: conditional_behavior
affected_layer: form_spec
form_id: phs-human-subjects
stable_field_path: /properties/studies/items
reproduction: Add one Human Subject Study record.
evidence_ref: local application 97b7c1b5-7a6b-4bbc-997d-413d6d5eb296
superbee_updated_by: codex
---
# Observation

Adding one study immediately exposed the complete nested study schema: exemption questions,
clinical-trial determinations, population characteristics, every attachment role, protocol fields,
interventions, outcomes, and enrollment reports. Labels were mostly mechanically title-cased paths
such as `Clinical Trial Questionnaire Prospectively Assigned Intervention`, rather than an
applicant-oriented conditional flow.

# Reproduction

1. Open the PHS Human Subjects form.
2. Select `Add another entry` under Human Subject Study Records.
3. Observe the entire nested workflow displayed at once, including questions that should depend on
   earlier determinations.

# Evidence boundary

The producer record already identifies eleven source-bound conditions as uncompiled. This finding
records the visible applicant consequence; it does not infer missing policy behavior beyond those
known gates.

# Triage

Producer PR [#119](https://github.com/mikec-ai/grants-form-spec/pull/119) adds generic conditional
support for repeatable groups and compiles the two exact F705 `HumanSubjectsIndicator` gates for
study and delayed-onset lists. Nine other F705 conditions and the embedded-study field-level
condition set remain explicitly uncompiled. This finding therefore remains open and must be
retested as a partial improvement, not marked resolved.

The primary-agent consumer verification in
`usability-runs/phs-human-subjects-first-fix-verification` confirms that the two top-level gates now
execute: study and delayed-onset controls are disabled until `HumanSubjectsIndicator` is Yes and
enable immediately afterward. The full nested study schema remains visible when a study exists,
so the nine F705 conditions and embedded-study flow still block resolution.
