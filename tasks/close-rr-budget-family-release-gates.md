---
type: Task
title: Close R&R Budget family release gates
priority: P0
description: >-
  Close shared DAT-condition, lifecycle, browser, accessibility,
  semantic-review, and production gates across R&R Budget and Subaward Budget
  profiles.
superbee_progress_status: in_progress
superbee_updated_by: rr_budget_conditions
generated:
  by: 'process:superbee'
  at: '2026-08-24T16:21:30.123Z'
assignee: rr_budget_conditions
---
# Goal

Close the remaining shared and form-specific release gates for R&R Budget, R&R Subaward Budget, and
their published duration/cardinality profiles while preserving one portable budget architecture.

# Delivered baseline

- The family composes shared research-budget question blocks with no form-specific compiler branch.
- All 56 DAT-defined calculations execute for root and nested subaward contexts with source-faithful
  numeric profiles.
- The generic Simpler adapter renders nested repeaters and parent-scoped rules.
- Five portable XML profiles reuse one declarative mapping and emit maximal payloads valid against
  their pinned official XSDs; the adapter contains no budget-family or duration branch.

# Acceptance criteria

- Decide and source the materialization policy for calculated outputs when every operand is absent
  versus explicitly zero; implement it generically and test both root and nested contexts.
- Reconcile and classify all non-empty DAT conditions, then author and exhaustively test only the
  source-exact executable subset without treating similar wording as accepted semantic equivalence
  or introducing a form-specific expression engine. The deterministic inventory corrects the
  earlier conflation of 56 calculated behaviors with conditioned records.
- Exercise calculations, validation, nested attachment auditing, save/reload, locked/print,
  submission, and official-XSD XML for representative minimal, maximal, invalid, and nested
  subaward payloads across every published family profile.
- Run browser-level editing, keyboard, and automated accessibility checks for nested repeaters and
  record human accessibility review separately.
- Record semantic-review, policy, instruction-asset, identifier, and production-registration gates;
  proposed mappings remain unpublished until accepted.
- Preserve zero form-specific compiler/adapter branches. Any genuinely reusable runtime extension
  must be bounded, portable, and exercised by more than one family member.

# Boundary

This task closes release evidence and policy gaps; it does not rewrite the already-delivered form
architecture or silently claim human approval.

# Implementation progress

## 2026-08-23: calculated-output materialization slice

- Source review found 20 of the 56 R&R Budget DAT calculations with non-empty conditions stating
  that the calculated output is required only when corresponding data is entered. The official
  XSD and DAT hashes remain pinned in the form evidence sidecar.
- Chosen portable policy: all declared sources absent or null leaves/removes the output; an
  explicitly entered zero is present and materializes zero. The policy is opt-in and changes
  neither formulas nor requiredness.
- Producer implementation is ready in [grants-form-spec PR 44](https://github.com/mikec-ai/grants-form-spec/pull/44):
  one declarative decorator, generic SGG projection, exactly 20 source-bound annotations,
  diagnostic coverage, and a source-bound decision record. Each annotation now declares explicit
  presence inputs. The producer also records the 20 exact F770 DAT behavior records and carries
  only those records into the four derived profiles, without changing their unreviewed semantic
  status. Derived forms now declare an occurrence mount for inherited behavior evidence;
  Subaward records resolve under `budgetAttachments[*]`, and the projector rejects behavior paths
  absent from emitted form occurrences and rule targets. PercentOf calculations emit their amount
  and percentage operands under the same portable materialization contract. Producer revision
  `5800390ea315dac05b4f1842d57b2094bb8b29d3` passes preflight (94 TypeSpec tests, 78 Python
  tests, 660 artifact validations, and the unclassified-field ratchet), and GitHub CI is green.
- Adapter implementation is ready in [simpler-grants-gov PR 38](https://github.com/mikec-ai/simpler-grants-gov/pull/38):
  generic server-side monetary-sum, integer-sum, and subtraction handling plus the exact producer
  revision pinned across all five family profiles. Presence resolution follows calculated
  dependencies to entered leaf inputs, including percentage calculations, so eagerly derived zeroes
  cannot make optional cumulative outputs appear. Unknown, incomplete, or non-calculation
  materialization policies fail closed during artifact projection. Materialized sums and
  subtraction require nonempty string `fields`; PercentOf requires nonempty string `amount` and
  `percentage` paths, so malformed artifacts cannot fall through to a swallowed runtime error. The
  focused 164-test rule-processing, root-budget, nested-subaward, provenance, malformed-contract,
  and artifact-integrity suite passes
  against the local test database; lint, formatting, and targeted mypy pass at adapter commit
  `68c001cc62dac7cf8d0d957f48407c2ce9f08f25`. The branch is rebased on fork main
  `f6affacded160c1585a9e148091b27d45eb7689c`, preserving its generic CD-511 consumer.
  The fork's 21-form artifact selection is pinned to producer
  `a7f900c636d8eeaad68a4069e745e397593c9459`; budget artifacts therefore include the merged
  materialization contract without carrying a stale generated-manifest commit. The corrected
  SF-424A lifecycle fixture and the CD-511 focused suites pass in the same run. This fork currently
  reports no GitHub checks for
  the branch.
- Regression coverage proves that absent optional Other Personnel input leaves cumulative count and
  funds outputs absent, while explicitly entered integer and monetary zeroes materialize zero. The
  same assertion runs at the root and across independent nested subaward instances.
- Provenance coverage proves that all five family profiles expose 20 exact F770 source records at
  occurrence-correct canonical property paths. Derived profiles identify `rr-budget` as the
  inheritance source, Subaward paths carry their `budgetAttachments[*]` mount, and every profile
  remains explicitly `unreviewed` for semantic acceptance.
- Percentage coverage proves both direct absence-versus-zero materialization and transitive
  presence through an eagerly calculated percentage. Materialization is rejected on
  non-calculation rules.
- SGG executes this portable calculation contract in its server-side rule processor. This slice does
  not add or claim a client-side calculation implementation.
- This slice has no lifecycle/residual-normalization overlap and adds no budget-family branch.

## 2026-08-24: deterministic DAT condition inventory

- [grants-form-spec PR 77](https://github.com/mikec-ai/grants-form-spec/pull/77) corrects the count
  model and publishes a provenance-pinned machine-readable inventory. The official F770 DAT has
  159 behavior occurrences, including 56 calculated behaviors. Across all roles, 64 path
  occurrences have non-empty conditions, representing 46 unique behavior-key records and 27 exact
  condition texts. Twenty calculated behaviors have conditions. The 18 occurrence-to-record delta
  comes only from F-8-1 and F-8-2, each expanded deterministically over ten Other Direct Cost paths.
- Closed exact-text classification identifies five recurring operator/path shapes. Unknown wording
  fails rather than falling into a nearest-looking class. Every occurrence retains the official DAT
  URI, version, SHA-256, literal extraction provenance, extraction repository/revision/artifact,
  behavior key, DAT field number, and occurrence path. Every disposition remains `unreviewed`.
- Fifty occurrences need no new primitive: 20 use the existing calculated-output materialization
  declaration, 16 are optional-row member requiredness, and 14 are paired-member requiredness
  within an optional object.
- Fourteen occurrences remain precisely source-bound and uncompiled. Four attachment/total rules
  require bidirectional presence plus a strict positive comparison over an XSD decimal represented
  portably as a string. Ten occurrence paths from one F-8-1 record require a cross-section minimum
  of one among ten distinct optional objects. Implementing either exactly requires an explicit,
  consumer-validated portable contract; a producer-only presence approximation would weaken the
  source rule. No new primitive was introduced in this slice.
- Producer commit `80b80a58a` passes eight focused regression tests and full preflight: 118
  TypeScript tests and 319 Python tests (two skipped), all artifact and fixture gates, and
  `git diff --check`. The source enriched-JSONL input digest is
  `0f3e71fd70e470e3b2ce3e35be300bc8c7f240369a51aca855ea618c83d508bb`; the official DAT digest is
  `c85158ce7ddcc756d6e8a55a050e00b4a95cdfc8d9a2d91b7bd94c7f8bdb1035`.
- This closes the deterministic inventory/classification sub-slice only. Consumer conformance for
  any future numeric-string or cross-object aggregate primitive, human semantic acceptance,
  accessibility, instruction, operational, and production-registration gates remain open.

## Merge receipt

- The producer contract merged in grants-form-spec PR 44 at `c36b0173bf1f4a596727a06218e4e423ed5f60ee`.
- The generic Simpler consumer merged in fork PR 38 at `a6a8ec6a062e4c2a9cab207a715d0d37c783cadf` after restacking over the 21-form baseline.
- The broader human semantic, accessibility, instruction, operational, and production-registration gates remain open, so this task remains in progress.

[depends on](harden-rr-budget-production.md)

[depends on](author-integrate-rr-subaward-budget.md)

[depends on](author-integrate-rr-budget.md)
