---
type: Roadmap Item
title: Simplify reusable form authoring before the next expansion wave
description: >-
  A bounded architecture leverage pass focused on proven duplication seams and
  fast conformance-preserving reductions.
sequence: '4'
superbee_progress_status: active
superbee_updated_by: codex
---
# Outcome

Make the next form expansion wave cheaper and easier to review by removing duplication at three proven seams, while preserving the portable artifact contract and current runtime behavior.

# Assessment

- The budget sibling forms already demonstrate the desired shape: each form declaration is 25 to 40 lines and composes shared budget blocks and target profiles.
- R&R SF-424 Multi-Project Cover is the clearest schema-composition exception. Its 479-line declaration contains 14 form-local `MultiProject*` models, largely to express optional cardinality over concepts already present in R&R SF-424.
- Grants.gov XML profiles already resolve ordinary JSON `$ref` fragments, but the two largest mapping files remain 681 and 823 lines. Repeated person, address, organization, contact, and attachment structures can use the mechanism that already works for budget profiles.
- The Simpler adapter correctly quarantines consumer-specific naming, but its UI pointers and calculation references perform parallel path parsing and renaming. One tested path-projection primitive would reduce code and projection drift.

# Scope boundary

This is a short leverage pass, not an architecture rewrite. Each task must preserve source semantics, standard `$ref` relationships, emitted artifacts or demonstrated behavioral parity, and the rule that no form-specific compiler or adapter branch becomes the source of truth.

# Exit condition

Complete the three bounded tasks below, record before-and-after evidence, and then resume representative-form expansion. Defer any broader compiler intermediate representation, new authoring language, or target distribution redesign until a concrete form demonstrates the need.

[contains](../tasks/simplify-multi-project-cardinality-reuse.md)

[contains](../tasks/factor-grants-gov-xml-fragments.md)

[contains](../tasks/unify-simpler-path-projection.md)
