---
type: Form Usability Run
title: PHS Human Subjects — core applicant pilot
form_id: phs-human-subjects
scenario: core-applicant-path-v1
environment: local-simpler-private-fork
runtime_commit: 5ef1589b971cb685780f902b782c3cf6ef65e953
producer_commit: 273d1ba8da96a958448d9c19209a50b8cbe2c0dc
artifact_manifest_digest: c31c759743a5266cd9ea941df73bc7edaf0d5ae68bb4250265ac44e7d86892f9
browser_scope: desktop-chromium-calibration
result: not_run
superbee_progress_status: queued
superbee_updated_by: codex
---
# Intent

Calibrate the manual agent-usability protocol against PHS Human Subjects and Clinical Trials
Information. The applicant goal is to determine applicability, add one representative study,
enter a small subset of structured enrollment information, attach one required narrative where
the scenario calls for it, save/reload, recover from one intentional validation error, and inspect
the printable form.

# Preconditions and provenance

- Status at creation: queued and not run.
- Portable form id: `phs-human-subjects`.
- Producer repository commit: `273d1ba8da96a958448d9c19209a50b8cbe2c0dc`.
- Producer form-manifest SHA-256: `c31c759743a5266cd9ea941df73bc7edaf0d5ae68bb4250265ac44e7d86892f9`.
- Consumer private-fork commit at creation: `5ef1589b971cb685780f902b782c3cf6ef65e953`.
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

Not run. The executing agent must add browser/viewport, local application identifier, safe route
reference, timestamps, screenshots or trace locations, and step-level observations here.

# Outcome and follow-up

Not run. Set the result and terminal status only after the evidence above is complete. Any blocked
source condition, calculation, policy, privacy, or semantic question remains an explicit gate and
must not be converted into inferred behavior.

[validates](../tasks/close-phs-human-subjects-technical-gates.md)
