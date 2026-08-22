---
type: Architecture Decision
title: Canonical portable form architecture
description: >-
  The standalone artifact graph and Billy Daly’s question-bank architecture
  govern implementation.
tags:
  - architecture
  - public
superbee_updated_by: mikec-ai
---
# Decision

This repository is the canonical public home for the portable grants form specification. Billy Daly's declarative question-bank architecture is the governing design.

TypeSpec is the first typed producer. Emitted JSON Schema, presentation, behavior, catalog, and evidence artifacts are the replaceable contract. Questions and forms compose recursively as semantic blocks through standard `$ref` relationships.

# Boundaries

- Canonical artifacts remain independent of Simpler.Grants.gov and every other delivery target.
- Per-form legacy projections, runtime rule-name mappings, and XML integration belong in consumer adapters.
- Large resolved snapshots, parity oracles, reports, and workbooks are build artifacts rather than runtime source.
- Internal transcripts, private evidence bundles, and personnel-specific context do not belong in this public bundle.
- Similar labels or validation shapes do not establish semantic equivalence. Only reviewed mappings contribute to published reuse metrics.

# Compatibility

Each migrated form must prove applicant-visible rendering and submission-validation parity through an explicit consumer projection. Known semantic disagreements remain visible review findings rather than hidden exceptions.

The governing design is documented in `documentation/architecture.md`, `documentation/authoring-model.md`, and `documentation/deferred-designs.md`.

[documented by](../architecture/form-architecture.md)

[documented by](../architecture/authoring-model.md)

[documented by](../architecture/deferred-designs.md)

[operationalized by](../architecture/guiding-principles.md)
