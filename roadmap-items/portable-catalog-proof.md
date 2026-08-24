---
type: Roadmap Item
title: Prove the portable catalog through SGG and close legacy coverage
superbee_progress_status: queued
description: >-
  Post-expansion tranche for real-frontend proof, uniform legacy differential
  parity, governed deltas, and remaining legacy coverage.
sequence: '7'
actor: Codex
timestamp: '2026-08-23T22:26:31.769Z'
superbee_updated_by: codex
---
# Outcome

Turn the post-expansion portable catalog into a proven SGG conformance corpus: render every banked form through the real SGG frontend, establish uniform legacy-oracle parity where an SGG implementation exists, record every intentional departure with evidence, and close the remaining legacy coverage gap.

# Background

The expected near-term baseline is 36 producer forms and 35 SGG-banked forms; `rr-sf424b` remains intentionally excluded from the SGG bank. Of those 35 banked forms, 21 should overlap a hand-written SGG legacy implementation after Attachment Form lands, while 14 will rely primarily on authoritative source artifacts rather than a legacy oracle. Only five portable forms are currently production-registered.

These states are deliberately distinct:

- **Authored**: the portable source and generated artifact exist.
- **Banked**: SGG has consumed and verified the promoted artifact.
- **Registered**: the portable form is enabled in production routing.
- **Oracle-proven**: the portable form has passed uniform differential checks against the legacy implementation.
- **UI-proven**: the portable form has passed real-browser conformance through SGG's actual renderer and lifecycle surfaces.

The 35-form bank is therefore a conformance corpus, not an assertion that all 35 forms are production-ready. Legacy behavior is compatibility evidence, not semantic authority: official XSDs, DAT files, PDFs, instructions, and policy remain authoritative. Any intentional difference from legacy must be explicit and evidence-backed.

# Architectural constraints

- Exercise the real SGG runtime and renderer through a test/dev-only seam; do not create a second reference consumer or runtime.
- Keep production registration a separate, human-governed release decision.
- Generate catalog-wide tests and fixtures from manifests and declarative capabilities; do not add per-form runtime branches.
- Treat portable-versus-legacy differences as governed data with provenance, review state, and stale-entry detection.

# Exit criteria

- Every banked portable form has a browser-conformance receipt covering its applicable capabilities.
- Every portable form with a legacy counterpart has a uniform differential-parity receipt.
- Every accepted difference from legacy is explicitly classified, evidenced, reviewed, and exercised.
- The four remaining legacy-only SGG forms are represented in the portable architecture and pass the same release gates.
- Production registrations are unchanged unless separately approved.

[contains](../tasks/add-portable-form-preview-registration.md)

[contains](../tasks/run-portable-catalog-browser-matrix.md)

[contains](../tasks/enforce-evidence-backed-parity-deltas.md)

[contains](../tasks/build-uniform-legacy-differential-parity.md)

[contains](../tasks/migrate-remaining-sgg-legacy-forms.md)

[contains](../tasks/separate-banked-from-runtime-enabled-forms.md)

[contains](../tasks/resolve-rr-sf424b-xsd-version-defect.md)

[contains](../tasks/close-phs-assignment-request-release-gates.md)

[contains](../tasks/close-attachment-form-release-gates.md)

[contains](../tasks/close-sf424c-release-gates.md)
