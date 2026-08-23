---
type: Roadmap Item
title: Simplify reusable form authoring before the next expansion wave
description: >-
  A bounded architecture leverage and SGG target-boundary pass with an explicit
  stop condition before representative expansion resumes.
sequence: '4'
superbee_progress_status: done
superbee_updated_by: codex
---
---
type: Roadmap Item
title: Simplify reusable form authoring before the next expansion wave
description: >-
  A bounded architecture leverage and SGG target-boundary pass with an explicit
  stop condition before representative expansion resumes.
sequence: '4'
superbee_progress_status: active
superbee_updated_by: codex
---
# Outcome

Make the next form expansion wave cheaper and easier to review by removing duplication at three proven seams, correcting one demonstrated target-identity leak, and isolating one source-version provenance migration, while preserving the portable artifact contract and current runtime behavior.

# Assessment

- The budget sibling forms already demonstrate the desired shape: each form declaration is 25 to 40 lines and composes shared budget blocks and target profiles.
- R&R SF-424 Multi-Project Cover is the clearest schema-composition exception. Its 479-line declaration contains 14 form-local `MultiProject*` models, largely to express optional cardinality over concepts already present in R&R SF-424.
- Grants.gov XML profiles already resolve ordinary JSON `$ref` fragments, but the two largest mapping files remain 681 and 823 lines. Repeated person, address, organization, contact, and attachment structures can use the mechanism that already works for budget profiles.
- The Simpler adapter correctly quarantines consumer-specific naming, but its UI pointers and calculation references perform parallel path parsing and renaming. One tested path-projection primitive would reduce code and projection drift.
- The canonical form-package contract currently requires SGG runtime identity fields such as `formType` and `sggVersion`. Real forms have already demonstrated that these values can disagree with the Simpler runtime enum, so they need a small explicit target boundary.
- Evidence sidecars historically use one `version` field for both enclosing form context and native source versions. XML fragment review proved that this must become a separate, explicit provenance-contract task rather than a partial change hidden inside a mapping refactor.

# Scope boundary

This is a short leverage pass, not an architecture rewrite. Each task must preserve source semantics, standard `$ref` relationships, emitted artifacts or demonstrated behavioral parity, and the rule that no form-specific compiler or adapter branch becomes the source of truth.

Defer the independent reference consumer, application-level cross-form condition contract, `@Sgg.prePopulate` to `@Map.from` migration, wholesale `@Sgg.*` relocation, broader compiler intermediate representation, new authoring language, form builder, and target distribution redesign. Revisit one only after a concrete form and consumer demonstrate the need.

# Exit condition

Complete the five bounded tasks below, record before-and-after evidence, and require producer, Simpler parity, XML, and XSD tests to remain green with zero new form-specific compiler or adapter branches. Then stop architectural cleanup and run the existing R&R Key Person Expanded form as the vertical release canary.

If any task requires a general override language, application orchestration engine, new intermediate representation, or applicant-visible behavior change, stop and re-scope it instead of expanding the abstraction.

[contains](../tasks/simplify-multi-project-cardinality-reuse.md)

[contains](../tasks/factor-grants-gov-xml-fragments.md)

[contains](../tasks/unify-simpler-path-projection.md)

[contains](../tasks/separate-sgg-runtime-identity-metadata.md)

[contains](../tasks/normalize-native-source-version-provenance.md)

# Result

The bounded five-task leverage pass is complete.

- Multi-project cardinality variants now compose existing blocks rather than duplicating form-local models.
- Grants.gov XML profiles compose reviewed reusable fragments.
- Simpler uses one generic path projection primitive.
- SGG runtime identity is owned by a versioned adapter record rather than portable FormMeta.
- Canonical form version and source-native version are separate, with unknown native versions represented explicitly.

Producer, adapter, XML, XSD, lifecycle, and parity checks remained green. No new form-specific compiler or adapter branch was introduced. Per the stop condition, further general architecture cleanup is deferred and the R&R Key Person Expanded vertical canary becomes the next delivery focus.
