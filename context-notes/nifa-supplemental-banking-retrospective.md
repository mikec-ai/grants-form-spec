---
type: Context Note
title: NIFA Supplemental measured banking retrospective
description: >-
  What the 2026-08-23 NIFA banking run cost, which work was valuable, which
  cycles were avoidable, and the standard operating procedure for later forms.
tags:
  - measurement
  - form-authoring
  - promotion
  - provenance
timestamp: '2026-08-24T01:38:10.000Z'
superbee_updated_by: codex
---
# Summary

The NIFA Supplemental form was not a one-day form. It reached a producer-merged, consumer-PR-open state in about 42 minutes from the explicit 20:52 ET start, but the elapsed time was longer than it needed to be. The research importer itself took about 0.4 seconds; source reconciliation and declarative authoring were the real form work. Cross-repository process mistakes, repeated full preflights, and one incorrect local test selection added avoidable time and output.

This run should not be summarized as “generation took 42 minutes.” It should be summarized as:

- roughly 23 minutes to reconcile, author, test, rebase, and merge the producer package;
- roughly 6 minutes to correct a provenance defect that a producer gate should have caught;
- roughly 9–12 minutes to promote, test, and open the consumer banking PR;
- additional hosted-CI time after the PR opened;
- several minutes of avoidable local retries and investigation described below.

## Delivered shape

- Source extraction: 32 structure records, 31 behavior records, 22 applicant fields, eight presentation groups, four runtime effects from two source conditions, and 39 open review gates.
- Portable form: nine canonical questions, of which two were reused and seven were new; one existing generic attachment capture mechanism; three existing behavior capabilities; zero unclassified fields and zero classification exceptions.
- Producer: PR #63 merged as `c1c2150f54fff4131119857ae46950cf2fd6ed22`; exact-XSD correction PR #65 merged as `3a6e51127e66d5555f3ef677cb21c4b9f7751e9a`.
- Consumer: banking PR #54 opened from `783572de7`; NIFA remains banked-only with no runtime identity, registration, or form-specific projection.
- Explicit remaining gate: the DAT narrows the Additional Applicant Type choices for applicant type H. The portable package preserves the complete XSD vocabulary and does not claim that narrower presentation policy is release-ready.

## Valuable work that should remain

1. The classified-field gate rejected a flat applicant-type occurrence that reused only an enum, not a canonical question. Adding `primary-org/applicant-type-code` created real question lineage.
2. Exact-XSD validation caught the actual legacy wire values `Y: Yes` and `N: No`; emitting `Y` and `N` would have produced invalid submission XML.
3. Source reconciliation corrected a compound UI condition so H or X enables Additional Applicant Type. Two independently authored conditions would have composed as an impossible AND.
4. The producer was rebased over the concurrently landed Human Subjects work, and the combined suite remained green. This was a useful concurrency proof.
5. The consumer digest gate rejected a normalized XSD whose bytes did not match the official hash. That fail-closed behavior is valuable.
6. The consumer remained additive and unregistered, proving the intended producer/consumer boundary.

## Avoidable cycles

1. **Normalized instead of exact XSD.** The task required an exact official source, but the initial fixture was a normalized copy while the profile pinned the official-byte hash. This forced a second producer PR and a repeated consumer promotion. Producer preflight should compare every profile digest to its vendored exact fixture.
2. **Wrong promotion mode.** The existing updater already supports `--add-forms`; using repeated `--form` arguments means exact replacement. Manually rebuilding the selection from a stale local branch initially proposed deleting 12 already-banked forms. The deletion was caught before commit, but it forced another full promotion run. Routine banking must use `--add-forms` from a clean, fetched consumer `origin/main` checkout.
3. **Repeated producer preflight.** Producer preflight ran locally several times and then inside each promotion attempt. Correctness requires one verified bundle per immutable producer SHA, not rebuilding the same SHA for every retry. Cache or download the CI-verified bundle where practical.
4. **Over-broad local test glob.** A broad XML test selection invoked database-backed fixtures without a local `grants-db`, generated 30 identical setup errors, took about 84 seconds, and produced very large logs. Use the focused form-spec suite first and run DB-backed suites only in the configured environment.
5. **Wrong formatter gate.** Ruff passed, but hosted CI uses repository-native `isort` and Black through `make format-check`. One retry fixed only `isort`; the next exposed Black drift in the changed registration test and two already-unformatted baseline tests. Always run the complete repository-native format target, not guessed substitutes one at a time.
6. **Unsupported test flag.** Passing Jest's `--runInBand` to Vitest produced an immediate, low-cost failure. Use package-defined commands without cross-runner flags.
7. **Shared-hotspot rebase.** Human Subjects landed during the run and touched README counts, form sequence, analysis goldens, XML profile tests, and the UI emitter. Checking open PR overlap before authoring and rebasing immediately before full preflight reduces conflict handling, though it cannot eliminate active parallel change.

## Standard operating procedure for the next bounded form

### Before authoring

1. Fetch producer and consumer `origin/main`; create clean worktrees from those exact refs.
2. Check open PRs for overlap in `specs/main.tsp`, form sequence, analysis goldens, XML-profile tests, emitter code, and consumer artifact manifests.
3. Claim the Superbee task and record an explicit wall-clock start.
4. Run the research importer once and save its receipt: source revision, source-set hash, record counts, behavior counts, rule effects, proposals, and open gates.
5. Download official sources byte-for-byte. Record both official and any derived/normalized hashes; never use a derived fixture where a profile pins official bytes.

### Authoring and producer gates

1. Reconcile the 22 or other applicant-visible fields against existing canonical question identities before writing form-local declarations.
2. Author form-local semantic blocks only when equivalence is unproven; do not infer reuse from names or validation shape.
3. Express UI, validation, prepopulation, attachment, and XML behavior declaratively. Add a generic capability only when the concrete form requires it and a second consumer is credible.
4. Run focused emit/evidence/classification/exact-XSD tests during iteration.
5. Rebase once onto the latest producer `origin/main`, then run one full `npm run preflight` and open the producer PR.

### Consumer banking

1. Merge the producer and use its full immutable merge SHA.
2. Prefer the supervised promotion workflow. Locally, use `--add-forms <form-id>`; never use exact `--form` selection for ordinary additive banking.
3. Require a zero-deletion receipt unless the task explicitly authorizes selection replacement.
4. Verify exact XSD bytes, artifact digests, selection membership, and registration isolation.
5. Run focused non-DB form-spec tests plus repository-native lint and format targets. Run DB/browser suites only in their configured environment.
6. Open the consumer PR, leave runtime registration unchanged, and record producer SHA, consumer head/merge SHA, artifact count, test counts, and wall-clock end.

## Measurement interpretation

The run falsified the idea that NIFA was “almost free” at the semantic-question level: only two of nine canonical questions were reused. It still supports falling marginal runtime cost: the attachment mechanism, three behavior capabilities, compiler, artifact contract, XML renderer, consumer adapter, loader, promotion path, and registration boundary were reused without a form-specific runtime branch. Future estimates should distinguish semantic authoring cost from runtime/platform cost.

[measures](../tasks/author-integrate-nifa-supplemental.md)

[motivates](../tasks/enforce-exact-producer-xsd-fixture-digests.md)

[motivates](../tasks/make-form-banking-safe-and-measured-by-default.md)

[motivates](../decisions/tiered-portable-form-ci.md)
