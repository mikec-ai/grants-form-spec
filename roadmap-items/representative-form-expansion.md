---
type: Roadmap Item
title: Expand through representative forms
description: >-
  Thirty-six producer forms and thirty-three banked consumer forms are
  delivered; Research Plan and Human Subjects consumer promotion plus a measured
  cheap-form lane now test whether marginal delivery cost is falling.
sequence: '3'
superbee_progress_status: active
superbee_updated_by: codex
---
# Strategy

Use two complementary delivery lanes across the current 36-form producer baseline and the next expansion sequence:

1. **Oracle-backed migrations.** Replace an existing SGG form definition with portable artifacts while retaining the legacy schema, UI, rules, XML, XSD, fixtures, and lifecycle behavior as a differential parity oracle.
2. **Coverage-building foundations.** Add high-volume forms that establish reusable capabilities missing from SGG and then immediately exercise those capabilities through a derivative form.

The official XSD, DAT, PDF/XFA, instructions, and versioned policy sources remain authoritative. An existing SGG implementation is evidence of compatibility behavior, not proof of source completeness or semantic correctness. Similar wording, paths, or shapes remain proposed reuse until semantic review accepts them.

# Delivered baseline

The producer now contains 36 portable forms. Forms 20 through 30 delivered SF-LLL, CD-511, Grants.gov Lobbying, four SF-424B profiles, three SF-424D profiles, and SF-424C. Forms 31 and 32 delivered PHS Assignment Request and Attachment Form. Form 33 delivered PHS 398 Research Plan as thirteen role-specific semantic questions over one reusable attachment capture mechanism. Form 34 delivered PHS Human Subjects and Clinical Trials as a structured clinical-study foundation with one 115-coordinate enrollment composite, exact nested XML/XSD conformance, and zero inferred calculations. Form 35 delivered NIFA Supplemental, and form 36 delivered standalone PHS Inclusion Enrollment Report by reusing one existing semantic composite across 121 exact associations with zero new semantic questions. The baseline has zero unclassified field occurrences and zero field-classification exceptions.

Current cross-repository snapshot: the public consumer fork banks 33 forms at consumer revision `91a01b0c5`. PHS Assignment Request, Attachment Form, R&R SF-424B, and NIFA Supplemental have landed since the prior snapshot. `phs398-research-plan`, `phs-human-subjects`, and `phs-inclusion-enrollment-report` are producer-only. Five R&R Budget-family profiles are registered in the fork; the other banked forms remain intentionally unregistered.

Producer completion does not imply production registration or human semantic, policy, instruction, accessibility, or operational approval. Proposed mappings remain unpublished.

# Immediate leverage work for forms 31+

The two authoring gates are complete:

1. A generic producer XML/XSD conformance harness.
2. Exact rule-target-to-behavior-evidence coverage enforcement.

Authoring can resume now. A supervised, consumer-owned producer-to-SGG promotion workflow proceeds in parallel and gates repeatable consumer banking, not portable form authoring. None of these changes reopens the compiler, adapter, authoring language, or runtime architecture.

# Prioritization model

Rank the next cohort using these decision weights:

- 30% reuse leverage
- 25% strength of an existing SGG parity oracle
- 20% two-year form-instance volume
- 15% maturity of source-pinned factory evidence
- 10% architectural diversity, policy risk, and ability to falsify the reuse thesis

The weights determine the cohort, not semantic equivalence. Submission counts are overlapping form instances rather than unique applications. Factory components and mappings remain agent-proposed until reviewed.

# Next delivery sequence

1. **Attachment Form** establishes ordered reusable attachment composition and generic attachment XML.
2. **PHS Assignment Request** proceeds in parallel as a bounded high-volume form expected to require no runtime extension.
3. **PHS 398 Research Plan** immediately consumes the Attachment Form foundation through thirteen typed attachment roles.
4. **PHS Human Subjects and Clinical Trials** establishes the dimensional enrollment and deeply nested conditional foundation.
5. **PHS Inclusion Enrollment Report** proves reuse of the Human Subjects dimensional model.
6. **PHS 398 Cover Page Supplement** composes existing application, identity, budget, attachment, and versioned-policy foundations.

Do not pre-build a general workflow engine, policy DSL, new intermediate representation, or generalized PHS framework. A concrete form must demonstrate any additional generic capability.

# Cheap, high-use banking lane

Run this bounded lane alongside—not instead of—the committed sequence:

1. **Bank PHS 398 Research Plan in SGG.** The producer work is complete; promotion should now be a short generic consumer operation.
2. **Author NIFA Supplemental.** This is the genuinely missing bounded candidate: 18,405 recorded two-year instances, 32 source structure records, 31 behaviors, and only four conditions.
3. **Author R&R Personal Data.** Its 39,237 instances make it valuable, but source-conformant banking must remain separate from privacy-gated runtime release.
4. **Author SBIR/STTR Information.** Its 22,853 instances and moderate conditional surface make it a useful follow-on composition test, not an excuse for a general policy engine.

Human Subjects, Inclusion Enrollment, and Cover Page Supplement remain in the committed sequence above and are not duplicated in this lane. Each lane task must record elapsed effort and reuse so the roadmap measures marginal economics instead of merely accumulating form count.

# Oracle protocol

For every oracle-backed migration:

1. Pin the legacy SGG implementation revision before changing registration.
2. Extract representative minimal, maximal, conditional, invalid, and XML fixtures from existing behavior and official sources.
3. Run the legacy and portable implementations against the same fixtures.
4. Classify every difference as a source correction, intentional presentation change, unresolved policy decision, or regression.
5. Preserve approved exceptions explicitly; never add a form-specific adapter or compiler branch to force superficial parity.
6. Cut registration over only after portable lifecycle, XML/XSD, accessibility, and applicable human gates pass.

# Cohort success measures

Record for every form:

- source and evidence revisions and hashes;
- factory records and behaviors reused versus re-reviewed;
- reusable questions, blocks, rules, XML fragments, and target profiles added;
- production compiler/adapter lines changed and form-specific branch count;
- differential parity results when an SGG oracle exists;
- schema, UI, validation, calculation, XML/XSD, save/reload, locked/print, and submission results;
- accessibility findings and unresolved semantic, policy, instruction, or operational gates;
- elapsed implementation effort and marginal effort compared with the prior form.

The next sequence validates next-form economics when its final forms require no form-specific adapter branches and no more than two genuinely reusable runtime extensions. Failure to meet that condition triggers a bounded architecture review before continuing beyond the committed sequence.

# Later candidates

Keep these behind the committed next sequence rather than silently expanding scope:

1. PHS Fellowship Supplemental
2. SF-425 Federal Financial Report
3. EPA Key Contacts as an identity/contact oracle migration
4. R&R Federal/Non-Federal Budget
5. PHS Career Development Supplemental

# Work governed by this roadmap item

[contains](../tasks/migrate-next-reference-form.md)

[contains](../tasks/implement-simpler-key-contacts-adapter.md)

[contains](../tasks/integrate-sf424a-reference-form.md)

[contains](../tasks/integrate-sf424-short-reference-form.md)

[contains](../tasks/integrate-standalone-attachment-forms.md)

[contains](../tasks/author-integrate-rr-budget.md)

[contains](../tasks/research-attachment-semantic-classification.md)

[contains](../tasks/author-integrate-rr-subaward-budget.md)

[contains](../tasks/harden-rr-budget-production.md)

[contains](../tasks/author-integrate-rr-sf424.md)

[contains](../tasks/improve-sf424a-budget-experience.md)

[contains](../tasks/spike-crosswalk-promotion-importer.md)

[contains](../tasks/harvest-rr-budget-10yr.md)

[contains](../tasks/harvest-rr-subaward-budget-30.md)

[contains](../tasks/promote-rr-subaward-budget-10-30.md)

[contains](../tasks/promote-project-abstract-summary.md)

[contains](../tasks/harvest-rr-sf424-multi-project-cover.md)

[contains](../tasks/harvest-rr-key-person-expanded.md)

[contains](../tasks/harvest-performance-site.md)

[contains](../tasks/grants-form-data-driven-registration.md)

[contains](../tasks/harvest-rr-other-project-information.md)

[contains](../tasks/harvest-phs398-modular-budget.md)

[contains](../tasks/close-rr-sf424-release-gates.md)

[contains](../tasks/release-rr-key-person-expanded-canary.md)

[contains](../tasks/fix-repeated-attachment-audit.md)

[contains](../tasks/migrate-sflll-parity-oracle.md)

[contains](../tasks/author-integrate-phs-human-subjects.md)

[contains](../tasks/migrate-attachment-form-parity-oracle.md)

[contains](../tasks/author-integrate-phs-inclusion-enrollment-report.md)

[contains](../tasks/migrate-sf424b-parity-oracle.md)

[contains](../tasks/author-integrate-phs398-research-plan.md)

[contains](../tasks/bank-phs398-research-plan-in-sgg.md)

[contains](../tasks/migrate-gg-lobbying-parity-oracle.md)

[contains](../tasks/author-integrate-phs-assignment-request.md)

[contains](../tasks/migrate-sf424c-parity-oracle.md)

[contains](../tasks/author-integrate-phs398-cover-page-supplement.md)

[contains](../tasks/author-integrate-nifa-supplemental.md)

[contains](../tasks/author-integrate-rr-personal-data.md)

[contains](../tasks/author-integrate-sbir-sttr-information.md)

[contains](../tasks/complete-key-person-declaration-xml.md)

[contains](../tasks/add-composable-presence-conditions.md)

[contains](../tasks/prove-key-person-sgg-lifecycle.md)

[contains](../tasks/unified-form-analysis-export.md)

[contains](../tasks/project-key-person-xml-in-sgg.md)

[contains](../tasks/distinguish-xml-array-wrapper-cardinality.md)

[contains](../tasks/integrate-key-person-overflow-gating.md)

[contains](../tasks/close-sf424a-release-gates.md)

[contains](../tasks/close-rr-budget-family-release-gates.md)

[contains](../tasks/migrate-sf424b-profile-family.md)

[contains](../tasks/migrate-sf424d-assurance-family.md)

[contains](../tasks/migrate-cd511-parity-oracle.md)

[contains](../tasks/build-generic-xml-xsd-conformance-harness.md)

[contains](../tasks/enforce-rule-evidence-target-coverage.md)

[contains](../tasks/automate-cross-repo-form-promotion.md)

[contains](../tasks/close-policy-form-release-gates.md)

[contains](../tasks/close-performance-site-release-gates.md)

[contains](../tasks/close-rr-other-project-information-release-gates.md)

[contains](../tasks/close-phs398-modular-budget-release-gates.md)

[contains](../tasks/enforce-exact-producer-xsd-fixture-digests.md)

[contains](../tasks/make-form-banking-safe-and-measured-by-default.md)

[contains](../tasks/encode-tiered-portable-form-ci.md)

[contains](../tasks/bank-phs-inclusion-enrollment-report-in-sgg.md)
