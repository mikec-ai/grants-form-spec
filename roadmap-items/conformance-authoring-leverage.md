---
type: Roadmap Item
title: Reduce conformance and delivery cost for forms 31+
description: >-
  The producer authoring gates are complete; supervised consumer promotion
  remains active in parallel.
superbee_updated_by: codex
superbee_progress_status: active
sequence: '6'
---
# Outcome

Reduce repeated conformance-test, evidence-audit, and consumer-promotion work for portable forms 31 and later, without changing the portable authoring architecture or creating a second runtime.

# Why this is now justified

- Seven producer test modules independently implement XML rendering and exact-XSD validation helpers.
- SF-424C review proved that count-only behavior-evidence tests can miss a swapped input/target record and an implementation-oracle citation where an official source exists.
- The runtime and adapter seams are already generic. The remaining repeated cost is conformance authoring and evidence coverage, not form semantics.

# Bounded scope

1. Build one producer-side reference XML/XSD conformance harness driven by existing declarative XML profiles and per-form fixtures.
2. Enforce exact rule-target-to-behavior-evidence disposition coverage generically.
3. Automate supervised consumer promotion without making the consumer workflow a prerequisite for producer authoring.

These changes must remain test and validation infrastructure. Do not add a new authoring language, compiler intermediate representation, workflow engine, policy DSL, form-specific branch, or production runtime.

# Exit condition

- At least three structurally different existing forms use the shared XML/XSD harness with unchanged conformance results.
- Every emitted calculation and condition target is matched by exact-path official evidence, explicitly typed parity-only evidence, or an explicit unresolved disposition.
- Full producer preflight remains green with 30 forms, zero unclassified fields, and zero field-classification exceptions.
- The two producer authoring gates are complete, so Attachment Form and PHS Assignment Request may resume. Consumer banking should use the promotion workflow once it lands; later forms drive any further generic capability only when demonstrated.

[contains](../tasks/build-generic-xml-xsd-conformance-harness.md)

[contains](../tasks/enforce-rule-evidence-target-coverage.md)

[contains](../tasks/automate-cross-repo-form-promotion.md)
