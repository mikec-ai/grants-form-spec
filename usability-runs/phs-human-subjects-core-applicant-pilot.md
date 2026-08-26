---
type: Form Usability Run
title: PHS Human Subjects — core applicant pilot
form_id: phs-human-subjects
scenario: core-applicant-path-v1
environment: local-simpler-private-fork
runtime_commit: e34c1478593c8e09925643dc354b50cf80837932
producer_commit: 273d1ba8da96a958448d9c19209a50b8cbe2c0dc
artifact_manifest_digest: c31c759743a5266cd9ea941df73bc7edaf0d5ae68bb4250265ac44e7d86892f9
browser_scope: desktop-chromium-calibration
result: fail
superbee_progress_status: complete
assignee: codex-primary-usability
---
# Intent

Calibrate the manual agent-usability protocol against PHS Human Subjects and Clinical Trials
Information. The applicant goal is to determine applicability, add one representative study,
enter a small subset of structured enrollment information, attach one required narrative where
the scenario calls for it, save/reload, recover from one intentional validation error, and inspect
the printable form.

# Preconditions and provenance

- Executed August 25, 2026 against the exact build below.
- Portable form id: `phs-human-subjects`.
- Producer repository commit: `273d1ba8da96a958448d9c19209a50b8cbe2c0dc`.
- Producer form-manifest SHA-256: `c31c759743a5266cd9ea941df73bc7edaf0d5ae68bb4250265ac44e7d86892f9`.
- Consumer private-fork commit: `e34c1478593c8e09925643dc354b50cf80837932`.
- Prior technical handoff is linked below; it is not a usability result.
- Eleven source-bound conditions and the unresolved 28-coordinate calculation remain open. The
  agent must record visible consequences without inventing policy or arithmetic.

# Scenario steps

1. Open the ordinary local Simpler application-form route and orient using the displayed title,
   instructions, sections, and navigation.
2. Attempt the human-subjects applicability flow and observe whether dependent study content is
   understandable and appropriately available.
3. Add one study and complete a representative path through nested study information.
4. Exercise one enrollment row and one applicable attachment role; do not attempt exhaustive entry
   of all 115 coordinates or all 15 attachment roles in this calibration run.
5. Trigger one validation error, identify and correct it using the UI, then save and reload.
6. Inspect keyboard movement through the exercised path and inspect the printable representation.
7. Record findings as symptoms first. Do not diagnose a shared defect without corroborating
   evidence.

# Evidence

- Browser: Codex in-app Chromium, desktop viewport calibration.
- Local application: `97b7c1b5-7a6b-4bbc-997d-413d6d5eb296`.
- Application-form route: `/workspace/applications/97b7c1b5-7a6b-4bbc-997d-413d6d5eb296/form/3479f537-e8ec-45a9-bec0-4a88030564a3`.
- The form loaded through Simpler's ordinary application workflow with correct form title,
  breadcrumbs, three-section navigation, save/return controls, and the ordinary print route.
- The overview section exposed four blank text boxes with neither visible labels nor accessible
  names. Triggered required-field errors did not identify the questions those controls represented.
- Adding one study worked, but immediately exposed the entire nested clinical-study schema rather
  than an applicant-oriented conditional path. Most nested labels were mechanically derived from
  property paths.
- Added one inclusion-enrollment row. Repeaters functioned, but displayed internal names such as
  `studies` and `inclusionEnrollmentReports`; the blank enrollment row exposed the complete
  115-coordinate matrix.
- Entered study title `Pilot clinical study` and selected `N: No` for federal-regulation exemption.
  Save completed and both values survived a full browser reload.
- Attachment entry was not attempted because the scenario could not establish a defensible
  applicable path while the controlling determinations were unlabeled and known conditions remain
  uncompiled. No file-transfer evidence is claimed.
- The ordinary print route loaded and preserved saved values, but printed the full inactive nested
  structure and blank enrollment matrix. Keyboard completion was not claimed after the unlabeled
  required controls blocked a meaningful applicant path.

# Outcome and follow-up

Result: **fail** for this core applicant scenario. Repetition, persistence, and print-route loading
worked, but an applicant cannot defensibly complete the controlling overview questions because the
required controls are unlabeled, and the missing conditional flow expands the form into an
unmanageable full-schema presentation.

Four scoped usability findings were recorded: overview labels/control semantics, unconditioned
nested study disclosure, internal repeater headings, and over-expanded print output. These remain
symptoms until triage establishes shared ownership. The eleven source-bound conditions and the
unresolved 28-coordinate calculation remain explicit gates; this run does not infer either.

[validates](../tasks/close-phs-human-subjects-technical-gates.md)

[discovers](../usability-findings/phs-overview-required-controls-unlabelled.md)

[discovers](../usability-findings/phs-study-schema-disclosed-without-conditions.md)

[discovers](../usability-findings/phs-repeaters-display-internal-identifiers.md)

[discovers](../usability-findings/phs-print-renders-full-inactive-nested-schema.md)
