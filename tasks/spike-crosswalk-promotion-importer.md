---
type: Task
title: Spike reusable crosswalk-to-form-spec promotion importer
priority: P0
assignee: codex
description: >-
  Completed reusable, review-gated development-time promotion path from pinned
  crosswalk evidence into grants-form-spec staging artifacts; Performance Site
  spike merged in PR #14 with zero accepted semantic mappings.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T19:40:55.071Z'
---
# Objective

Build and prove a reusable, design-time promotion protocol between `grants-question-crosswalk` and `grants-form-spec`, using Project/Performance Site Location(s) as the proving form. Preserve the crosswalk as source-pinned research evidence and keep `grants-form-spec` authoritative for canonical authoring. Create no runtime dependency.

# Delivered

- Merged `grants-form-spec` PR #14: https://github.com/mikec-ai/grants-form-spec/pull/14
- Added the versioned, output-neutral `grants-form-promotion/v1` packet contract.
- Added a revision-pinned exporter that reads crosswalk Git objects rather than the dirty working tree.
- Added a staging-only importer that emits an evidence sidecar, compiling TypeSpec source-shape draft, review queue, and import report.
- Added packet validation, independent staging TypeSpec compilation, reproducibility tests, and full-preflight integration.
- Kept all semantic and component assignments proposed and non-publishable; accepted semantic mappings remain zero.

# Performance Site result

- 34 deterministic XSD records transcribed without manual field-by-field re-entry.
- 33 raw behavior records preserved: 25 applicant-entered and eight presentation records.
- Nine proposed executable conditional rules preserved for review.
- Six exact source identities and hashes assembled.
- 34 component proposals carried into the review queue without promotion to canonical identities.
- 40 explicit review gates: 24 semantic-identity, nine behavior-semantic, six enum wire-value, and one attachment-semantic gate.
- The generated TypeSpec draft compiles independently but is deliberately not imported by `specs/main.tsp`.

# Findings

The reusable seam materially removes repeated source discovery, transcription, constraint reconstruction, provenance assembly, and review-queue setup. It does not remove semantic, policy, behavior, accessibility, or parity review. A potentially confusing 25-versus-33 behavior count was reconciled rather than treated as missing evidence: the 25 are applicant-entered records and the remaining eight are presentation behaviors.

Because the crosswalk checkout contained substantial uncommitted parallel work, the spike kept it read-only and placed the exporter beside the importer in `grants-form-spec`. The packet contract is repository-neutral, so a future native crosswalk export command can replace that implementation without changing the consumer.

# Validation

- GitHub CI passed before merge.
- Full producer preflight passed.
- 52 TypeScript tests and 15 Python tests passed.
- The promotion packet validates against its JSON Schema.
- The staging TypeSpec compiles independently.
- A reproducibility test proves that dirty working-copy changes cannot alter a revision-pinned packet.

# Recommended next use

Use the protocol to bootstrap R&R SF-424 or another complex form after deciding whether to resolve the Performance Site review queue into a canonical form. Treat native crosswalk command placement as a follow-up implementation choice, not a prerequisite to consuming the stable packet.
