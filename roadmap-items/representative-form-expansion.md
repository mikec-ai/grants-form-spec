---
type: Roadmap Item
title: Expand through representative forms
description: >-
  Thirty portable forms are delivered; complete three bounded delivery-cost
  tasks, then resume Attachment, Assignment Request, Research Plan, and PHS
  foundation work.
sequence: '3'
superbee_progress_status: active
superbee_updated_by: codex
---
# Strategy

Use two complementary delivery lanes across the current 30-form baseline and the next expansion sequence:

1. **Oracle-backed migrations.** Replace an existing SGG form definition with portable artifacts while retaining the legacy schema, UI, rules, XML, XSD, fixtures, and lifecycle behavior as a differential parity oracle.
2. **Coverage-building foundations.** Add high-volume forms that establish reusable capabilities missing from SGG and then immediately exercise those capabilities through a derivative form.

The official XSD, DAT, PDF/XFA, instructions, and versioned policy sources remain authoritative. An existing SGG implementation is evidence of compatibility behavior, not proof of source completeness or semantic correctness. Similar wording, paths, or shapes remain proposed reuse until semantic review accepts them.

# Delivered baseline

The producer now contains 30 portable forms. Forms 20 through 30 delivered SF-LLL, CD-511, Grants.gov Lobbying, four SF-424B profiles, three SF-424D profiles, and SF-424C. The baseline has zero unclassified field occurrences and zero field-classification exceptions.

Current cross-repository snapshot: the public consumer fork banks 28 forms at producer revision `e0b0fb24`; `rr-sf424b` and `sf424c` remain producer-only. Five R&R Budget-family profiles are registered in the fork; the other banked forms remain intentionally unregistered.

Producer completion does not imply production registration or human semantic, policy, instruction, accessibility, or operational approval. Proposed mappings remain unpublished.

# Immediate leverage gate before forms 31+

Complete three bounded, independent delivery-cost improvements:

1. A generic producer XML/XSD conformance harness.
2. Exact rule-target-to-behavior-evidence coverage enforcement.
3. A supervised, consumer-owned producer-to-SGG promotion workflow.

These changes do not reopen the compiler, adapter, authoring language, or runtime architecture.

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
3. SBIR/STTR Information
4. EPA Key Contacts as an identity/contact oracle migration
5. R&R Federal/Non-Federal Budget
6. R&R Personal Data after privacy and policy review

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

[contains](../tasks/migrate-gg-lobbying-parity-oracle.md)

[contains](../tasks/author-integrate-phs-assignment-request.md)

[contains](../tasks/migrate-sf424c-parity-oracle.md)

[contains](../tasks/author-integrate-phs398-cover-page-supplement.md)

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
