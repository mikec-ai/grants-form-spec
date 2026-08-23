# SF-424C portable parity boundary

This migration makes Budget Information for Construction Programs (SF-424C), version 2.0, a portable declarative form. It composes distinct construction-budget questions, emits Simpler-compatible UI and calculation rules, and supplies a Grants.gov XML profile without adding form-specific compiler or adapter logic.

## Evidence boundary

The official Grants.gov XSD, DAT workbook, read-only PDF, and instructions PDF are pinned by URL, native version, and SHA-256 digest in `evidence/forms/sf424c/evidence.json`. Every calculation behavior record cites one of those official sources, including the eligible-cost copy identified on PDF page 1, line 17. The existing implementation in the public `mikec-ai/simpler-grants-gov` fork is pinned only as a differential parity oracle. It is useful for confirming runtime behavior, but it is not source or semantic authority for the form.

The declarative calculation graph covers 24 source-bound behaviors:

- allowable cost for 11 ordinary cost rows, contingencies, and program income;
- three values in the subtotal before contingencies;
- three values in the subtotal after contingencies;
- three total-project-cost values after program income;
- the eligible-cost display copy and federal percentage calculation. The applicant-entered
  federal percentage is source-bound form data, but it is not counted as calculated behavior.

All computed fields use `when_any_source_present`. This preserves the calculations while avoiding phantom zero-valued structures in an untouched draft. The older SGG oracle eagerly materializes some zeroes, so empty-draft materialization is an intentional bounded difference. Populated calculation results and ordering remain aligned.

The XML profile preserves the official element order, namespace-qualified fixed attributes,
amount constraints, and the source's flattened federal-funding elements. It declares both
XSD-required subtotal containers with `emitWhenParentPresent`, so contingencies-only,
program-income-only, and explicitly empty budget objects still produce valid `ProjectCosts`.
`federalFunding.totalProjectCosts` is a UI-only calculated copy and is intentionally excluded
from XML.

## Semantic review boundary

The source's cost classifications remain distinct questions even where their three-column capture structure is identical. Similar monetary shape is not treated as proof of semantic equivalence. The 18 proposed source-to-question mappings remain explicitly `proposed`; none contribute to published overlap or coverage metrics until a human accepts them.

## Remaining production gates

This producer-side migration does not itself establish production readiness. The remaining gates are:

- human acceptance or revision of proposed semantic mappings;
- instruction-content and accessibility review;
- downstream adapter verification for create, save, reload, locked, and print states;
- end-to-end submission XML validation in the consuming runtime;
- production form registration and release approval.

These gates should be closed in the consuming SGG fork or by human review. They should not be encoded as SF-424C-specific compiler behavior.
