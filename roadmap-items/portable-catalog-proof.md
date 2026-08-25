---
type: Roadmap Item
title: 'Prove compatibility, reuse, and new-form delivery'
superbee_progress_status: active
description: >-
  Proof-first tranche: three deep compatibility canaries, a broader automated
  cohort, one new-form validation, and a reproducible evidence package.
sequence: '7'
actor: Codex
timestamp: '2026-08-23T22:26:31.769Z'
---
# Outcome

Turn the 39-form portable catalog into a credible delivery proof: demonstrate that the declarative authoring model can reproduce existing forms through the real Simpler runtime, quantify compatibility gaps, and extend the same architecture to a new form whose correctness is checked against authoritative sources.

# Current baseline

- Thirty-nine forms are authored in the portable producer and banked in the consumer.
- The catalog separates authored, banked, registered, compatibility-proven, source-proven, and UI-proven states.
- Existing implementations are compatibility oracles. Official XSDs, DAT files, PDFs, instructions, and policy sources remain semantic authorities.
- Similar labels, paths, and JSON shapes do not establish semantic equivalence. Proposed mappings remain outside published coverage metrics until accepted.

# Priority sequence

## P0: prove three representative existing forms deeply

Use SF-424, SF-424 Short, and SF-424A as the primary compatibility canaries.

- Resolve known portable-versus-existing schema and validation deltas without adding form-specific adapter behavior.
- Compare the rendered forms side by side through the real Simpler frontend.
- Exercise the same payload corpus against both implementations and compare validation verdicts, calculations, rules, persistence, locked/print behavior, and XML where applicable.
- Record every difference as parity, an evidence-backed intentional departure, an unresolved review item, or a defect.
- Do not describe a form as visually or behaviorally equivalent until the corresponding checks have passed.

## P0: prove the automated checking method beyond the canaries

Apply the uniform differential harness to an initial cohort of at least seven and preferably ten forms with existing counterparts. Manual inspection of every form is not required for this slice; the goal is to show that the automated pipeline produces comparable, reproducible receipts and quantifies remaining gaps.

## P0: validate one new priority form end to end

Use R&R SF-424 as the first new-form proof, with the R&R Budget family as the next complementary foundation.

- Validate structure, behavior, UI, persistence, XML/XSD output, and source provenance.
- Use authoritative source artifacts because no existing implementation is available as a complete oracle.
- Keep human semantic, accessibility, instruction, policy, and production-registration gates explicit.

## P0: assemble the proof package

Produce a concise, reproducible package containing the three-form side-by-side evidence, automated parity receipts for the broader cohort, one new-form source-validation receipt, catalog and reuse metrics, and instructions or a short recording showing how to run the comparison.

## P1: widen compatibility and source validation

After the first package is coherent, extend automated parity across the remaining overlap forms and apply the same source-validation pattern to additional priority forms.

## P2: resume broad expansion and catalog-wide browser evidence

Continue adding forms and run the optional full browser matrix after the proof-first slices are stable. New form work should alternate between reusable foundations and cheap derivatives so each wave both creates and demonstrates leverage.

# Architectural constraints

- Keep the portable contract as the stable interface between authoring tools and consumers.
- Treat TypeSpec as one authoring interface, not as a runtime dependency or the only possible authoring experience.
- Keep emitters generic and form semantics declarative.
- Exercise the real Simpler runtime and renderer through test/dev-only seams; do not create a parallel runtime.
- Preserve intentional differences from existing behavior as reviewed, evidence-backed data.
- Keep production registration a separate human-governed release decision.

# Exit criteria for the initial proof

- SF-424, SF-424 Short, and SF-424A have both manual visual receipts and automated behavioral receipts, with every known difference classified.
- At least seven overlap forms have uniform automated compatibility receipts, with a target of ten if the harness supports it without form-specific logic.
- R&R SF-424 has an end-to-end source-validation receipt and can be demonstrated through the real consumer.
- The evidence package is reproducible from pinned producer and consumer revisions.
- Claims distinguish technical proof from semantic review, accessibility approval, policy decisions, and production readiness.

[contains](../tasks/add-portable-form-preview-registration.md)

[contains](../tasks/prove-sf424-family-visual-and-behavioral-parity.md)

[contains](../tasks/reconcile-sf424-family-portable-cutover-deltas.md)

[contains](../tasks/build-uniform-legacy-differential-parity.md)

[contains](../tasks/enforce-evidence-backed-parity-deltas.md)

[contains](../tasks/close-rr-sf424-release-gates.md)

[contains](../tasks/close-rr-budget-family-release-gates.md)

[contains](../tasks/assemble-portable-form-proof-package.md)

[contains](../tasks/run-portable-catalog-browser-matrix.md)

[contains](../tasks/migrate-remaining-sgg-legacy-forms.md)

[contains](../tasks/separate-banked-from-runtime-enabled-forms.md)

[contains](../tasks/resolve-rr-sf424b-xsd-version-defect.md)

[contains](../tasks/close-phs-assignment-request-release-gates.md)

[contains](../tasks/close-attachment-form-release-gates.md)

[contains](../tasks/close-sf424c-release-gates.md)

[contains](../tasks/project-flattened-scalar-array-xml-in-sgg.md)

[contains](../tasks/implement-exact-empty-string-to-absent-normalization.md)

[contains](../tasks/correct-sf424-short-readonly-semantics.md)

[contains](../tasks/repair-pairwise-reviewed-similarity.md)

[contains](../tasks/design-parity-delta-ledger-contract.md)

[contains](../tasks/audit-seven-form-parity-deltas.md)

[contains](../tasks/define-independent-parity-decision-receipt.md)

[contains](../tasks/enable-parallel-worktree-test-isolation.md)

[contains](../tasks/close-project-abstract-summary-release-gates.md)

[contains](../tasks/close-rr-personal-data-technical-gates.md)
