---
type: Task
title: Close R&R Budget family release gates
priority: P0
description: >-
  Close shared DAT-condition, lifecycle, browser, accessibility,
  semantic-review, and production gates across R&R Budget and Subaward Budget
  profiles.
superbee_progress_status: in_progress
generated:
  by: 'process:superbee'
  at: '2026-08-24T21:22:26.332Z'
assignee: root_budget_numeric_string
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

## 2026-08-24: proof-package integration

- [grants-form-spec PR 78](https://github.com/mikec-ai/grants-form-spec/pull/78) carries the merged
  condition inventory into the generated proof-package source at exact producer main revision
  `2bd979045f3dabfd1f77655c92f36fd496b08f65`.
- The family proof states the exact boundary as 64 conditioned occurrences, 50 represented, and 14
  source-bound/uncompiled. It does not describe the 56 DAT calculations as conditions and does not
  claim semantic acceptance.
- Every producer-path claim now uses one package revision, enforced fail-closed by the builder. The
  exact condition inventory is resolved and hashed from that Git tree. Generated proof index and
  manifest remain build artifacts.
- Focused proof-package tests and full producer preflight pass at PR head `4f28d50d1` (118
  TypeScript tests and 323 Python tests, two skipped). The broader release gates remain open.

## 2026-08-24: cross-section condition contract and consumer conformance

- [grants-form-spec PR 79](https://github.com/mikec-ai/grants-form-spec/pull/79) merged at
  `563e7d8b5a38c7b5d66723bfbc1607caeeff4aad`. It compiles the ten exact F-8-1 path occurrences
  through one target-neutral `atLeastOnePathWhenPresent` declaration. The portable artifact uses
  standard JSON Schema `if` plus `then.anyOf`; no form-specific compiler branch was added.
- The exact condition boundary is now 64 conditioned occurrences: 50 represented by existing
  declarations, 10 compiled through the new cross-section primitive, and four source-bound and
  uncompiled. The four unavailable occurrences are two bidirectional attachment/positive-total
  pairs over XSD decimals represented as strings; they require a generic, source-exact
  numeric-string comparison contract rather than a presence-only approximation.
- Every compiled occurrence retains the pinned F770 DAT source URI, version, SHA-256, literal
  extraction provenance, source path, and source record. All mappings and the family semantic
  review remain `unreviewed`; compilation does not claim semantic acceptance.
- Producer full preflight passes at the merged revision: 121 TypeScript tests and 325 Python tests,
  with two repository-default skips. Tests cover absent trigger, missing alternatives, incomplete
  target rows, and a valid non-sequential tenth row. The generic evidence projector now follows
  local emitted `$ref` graphs and fails closed for escaping or unresolved references.
- [simpler-grants-gov PR 77](https://github.com/mikec-ai/simpler-grants-gov/pull/77), merged at
  `9f9ffcb1cd5fd7705bcbd0160df63d2227ffb08c`, pins the consumer artifact bank to the exact producer
  merge revision and proves direct R&R Budget and nested R&R
  Subaward Budget conformance. No Simpler compiler, projector, renderer, or form-specific adapter
  code changed. The focused consumer suite passes 31 tests; Ruff and repository Black checks pass
  at amended head `9d4f4df43`. Hosted API format, lint, migrations, security lint, and the full API
  suite pass. The fork's unrelated full-repository E2E workflow remains red across broad attachment,
  performance-site, SF-424, and SF-424A smoke tests; those failures do not exercise the changed R&R
  Budget artifacts or focused conformance tests and are recorded as an external CI boundary rather
  than attributed to this slice.
- [grants-form-spec PR 80](https://github.com/mikec-ai/grants-form-spec/pull/80), merged at
  `a667b9fa6904f9b12bdf424ac354c66935462631`, refreshes the authored proof-package source to the same
  producer evidence revision and exact 50/10/4 boundary. Four focused
  proof tests and full producer preflight pass at head `4cc63b49d`; generated proof files remain
  build artifacts.
- Generated analysis, proof indexes, manifests, and promotion receipts remain build artifacts. The
  checked consumer artifact bank is the integrity-pinned runtime input documented by the adapter
  contract.

## Merge receipt

- The producer contract merged in grants-form-spec PR 44 at `c36b0173bf1f4a596727a06218e4e423ed5f60ee`.
- The generic Simpler consumer merged in fork PR 38 at `a6a8ec6a062e4c2a9cab207a715d0d37c783cadf` after restacking over the 21-form baseline.
- The broader human semantic, accessibility, instruction, operational, and production-registration gates remain open, so this task remains in progress.

## 2026-08-24: positive-total condition closure

- [grants-form-spec PR 87](https://github.com/mikec-ai/grants-form-spec/pull/87), merged at
  `243e5951b883b9b521c24567a5e362d9bfdd7f19`, closes the last four source-bound/uncompiled
  F770 condition occurrences through two target-neutral declarations. One requires an attachment
  when its decimal-string total is strictly positive; the other requires a strictly positive total
  when the attachment exists. The emitter uses ordinary JSON Schema `if`/`then` constraints and
  intersects the source field's precision and scale with an unsigned decimal lexical pattern that
  contains at least one non-zero digit.
- Both equipment and senior/key-person pairs are declared once in the shared research-budget
  question bank and inherited by all five duration/subaward profiles. The producer retains exact
  A-2-1, A-3-1, C-2-0, and C-2-1 DAT records and their pinned provenance. All remain explicitly
  unreviewed for semantic acceptance.
- [simpler-grants-gov PR 81](https://github.com/mikec-ai/simpler-grants-gov/pull/81), merged at
  `99709f19e45cddbc58d8d5be4d72610fdbe5e61b`, pins the merged producer revision and proves the
  portable conditions through Simpler's resolved direct R&R Budget and nested R&R Subaward Budget
  schemas. No Simpler runtime, compiler, projector, renderer, frontend, or form-specific adapter
  code changed. Forty-nine focused family, integrity, provenance, and bank tests pass locally.
- [grants-form-spec PR 88](https://github.com/mikec-ai/grants-form-spec/pull/88), merged at
  `c78df2351b01eb2331e8d55437e8cb6437001c10`, refreshes the generated proof-package source. The
  technical boundary is now 64 conditioned occurrences: 50 represented by existing declarations,
  10 compiled through the cross-section contract, and four compiled through the positive-decimal
  contracts. Producer preflight and the proof-package artifact check are green.
- This completes the technical DAT-condition representation gate. Semantic acceptance, human
  accessibility review, instruction/policy decisions, operational readiness, and production
  registration remain open, so the broader release-gate task remains in progress.

## 2026-08-24: parallel AI-only hardening wave

Three isolated, independently mergeable slices are claimed under this P0 task:

- `budget_browser_lifecycle`: real-browser direct/nested budget behavior, attachment/positive-total
  validation, save/reload, locked/print, keyboard navigation, error focus, and automated Axe checks.
- `budget_source_content`: deterministic DAT/XSD reconciliation of applicant-visible labels,
  help/instructions, requiredness, grouping, and attachment semantics; only source-exact corrections
  may land, with uncertain items remaining explicit.
- `budget_payload_xml`: shared minimal, maximal, explicit-zero, invalid, and independently nested
  payload corpus across all five profiles, including calculations, XML generation, and pinned
  official-XSD validation.

Each slice uses a fresh branch in the appropriate public fork. Generated receipts remain build
artifacts, and no HHS upstream repository or issue is modified.

## 2026-08-24: AI-only hardening receipts

- [grants-form-spec PR 89](https://github.com/mikec-ai/grants-form-spec/pull/89), merged at
  `e2e257b2723c5d347cee1c6b3067fb0d6835238c`, adds the exact F770 attachment/positive-total help
  text and compiles the source end-date ordering rule through the existing generic
  `date_not_before` contract across all five profiles. Producer preflight passed 123 TypeScript
  tests and 337 Python tests (two skipped).
- Independent review found that PR 89's initial audit artifact overstated untested broad label and
  requiredness coverage. [grants-form-spec PR 90](https://github.com/mikec-ai/grants-form-spec/pull/90),
  merged at `401473c91635f9b28f06e51fb7c311409deb07ec`, narrows the proven label result to the four
  path-specific controls asserted by emitted-artifact tests and marks broader label and requiredness
  reconciliation explicitly unresolved. No semantic mapping was accepted.
- [simpler-grants-gov PR 83](https://github.com/mikec-ai/simpler-grants-gov/pull/83), merged at
  `33f8ac3eec6d22ff6c88b048ee1b1363dfe3142d`, adds one shared 44-case family matrix plus 20
  existing XML canaries. It covers minimal and fully populated lifecycle/XML payloads, explicit
  zero calculations, 20 bidirectional attachment/total failures, independent nested subawards,
  acceptance at every declared period/subaward maximum, and rejection at maximum plus one.
  Every valid XML scenario is checked against its pinned official XSD. The combined 64-test suite,
  isort, Black, Ruff, and mypy passed. The change is test/helper-only; its unrelated full E2E
  fanout was intentionally canceled.
- [simpler-grants-gov PR 84](https://github.com/mikec-ai/simpler-grants-gov/pull/84), merged at
  `ae35fe3bfd0383f3ab5734aefedae80a53cd5332`, promotes the exact PR 89 producer revision across
  all five consumer profiles. Fifty-three focused tests prove source guidance visibility, direct
  and nested date-order scoping, artifact integrity, and immutable provenance. Repository isort,
  Ruff, mypy, and diff checks passed after a review-found import-order defect was corrected. The
  promotion adds no adapter, compiler, renderer, frontend, registration, or form-specific branch.
- A bounded direct-profile browser run exposed three generic consumer gaps before it could exercise
  the form. [simpler-grants-gov PR 89](https://github.com/mikec-ai/simpler-grants-gov/pull/89),
  merged at `a050806bbe5786c04222a838afca291ec3bf84dd`, permits recursive `FieldList` children in the
  generic UI-schema validator. [PR 90](https://github.com/mikec-ai/simpler-grants-gov/pull/90),
  merged at `187ba3f0b1a9c7595baae25ba472240500283bc2`, classifies disjunctive conditional-required
  effects such as `then.anyOf` as non-projectable for frontend required styling while leaving the
  authoritative JSON Schema unchanged and active. [PR 91](https://github.com/mikec-ai/simpler-grants-gov/pull/91),
  merged at `889b52c588a61f686ce7c2d178259dabc711dc66`, allows the already supported calculated/`null`
  field variant inside `FieldList` children. These are generic contract consistency fixes with no
  form identifier branch; their focused and full frontend checks passed.
- [simpler-grants-gov PR 82](https://github.com/mikec-ai/simpler-grants-gov/pull/82), merged at
  `75be12f2d4afe352a9e46ea1ed3268af55b6dfcb`, adds schema-driven implication discovery and a
  reusable browser probe for positive-total/required-attachment behavior, zero reversal,
  calculated-state save/reload, and validation-summary focus. Sixteen focused API tests and 95
  focused frontend tests passed (one skipped), together with TypeScript, focused ESLint, and
  Prettier. The last complete isolated Chrome run over `rr-budget` and `rr-budget-10yr` produced 12
  passes, zero failures, and two focus-only inconclusive probes. The final generic visible-upload
  focus correction is unit-covered but still needs clean-stack browser confirmation; a later rerun
  lacked the isolated frontend's `API_JWT_PUBLIC_KEY` and therefore stopped before application
  creation. Nested Subaward implications are discovered, but browser execution remains explicitly
  not applicable until the harness supports two repeating dimensions. No receipts, traces,
  screenshots, or media were committed.

The independent cross-PR review found no form-specific architecture branch in PRs 82, 83, or 84.
The broader task remains in progress because final visible-upload focus browser confirmation,
nested two-repeater browser execution, human semantic and accessibility acceptance,
lifecycle/prefill ownership, fixed personnel-role defaults, operational readiness, and production
registration are not closed.

## 2026-08-24: next claimed source slice

- `root_budget_fixed_roles` claims the four exact F770 personnel-role defaults at B-1-2, B-2-2,
  B-3-2, and B-4-2. The slice will determine whether the existing portable schema vocabulary can
  express source-owned fixed/read-only values or whether one small target-neutral declaration is
  required; it must apply through the shared research-budget question bank to all five profiles.
- This slice will not modify the shared catalog browser harness, bounded dispatch, test-isolation,
  proof-package, SF-424-family, R&R SF-424, SF-424C, PHS Assignment, or Attachment Form work already
  claimed by other agents. No HHS upstream writes are permitted.

## 2026-08-24: fixed personnel-role slice published

- [grants-form-spec PR 91](https://github.com/mikec-ai/grants-form-spec/pull/91), merged at
  `6ff6048f1061842a7f0f6b184f89e0631e1762a3`, captures the four exact F770 records B-1-2 through B-4-2 as declarative string
  literals with matching defaults and generic read-only annotations in the shared research-budget
  question bank.
- The emitted contract is exact for `Post Doctoral Associates`, `Graduate Students`,
  `Undergraduate Students`, and `Secretarial/Clerical`. The applicant-entered Additional Project
  Role remains a free-form string, so the change does not infer semantic equivalence or broaden
  source ownership.
- The existing TypeSpec and JSON Schema vocabulary was sufficient. No compiler feature,
  target-specific branch, or form-specific generator was added. All five R&R Budget-family
  profiles inherit the read-only presentation contract.
- Full producer preflight passed: 123 TypeScript tests and 338 Python tests (10 skipped), plus
  artifact, promotion, parity-ledger, classified-field, XSD-fixture, package, and independent
  TypeSpec-file verification. Both required GitHub workflows passed before merge.
- Semantic review remains `unreviewed`, and this closes only the four fixed-role source records.
  Lifecycle/prefill ownership, browser confirmation, human semantic/accessibility acceptance,
  operational readiness, and production registration remain outside this increment.

## 2026-08-24: next claimed lifecycle and prefill slice

- `root_budget_lifecycle_prefill` claims only the five remaining F770 lifecycle and prefill records
  at 0-06, 0-07, 0-08, 0-10, and L-1-1.
- The slice will reconcile each exact source record against the existing target-neutral response,
  visibility, cardinality, and prepopulation vocabulary. It will implement only behavior supported
  by exact evidence and portable semantics; consumer-owned or package-context behavior will remain
  explicit rather than being approximated in the question bank.
- This slice will not modify browser harnesses, proof packaging, test isolation, SF-424-family
  work, or the release tasks already owned by other agents. No HHS upstream writes are permitted.

## 2026-08-24: lifecycle and prefill source slice merged

- [grants-form-spec PR 92](https://github.com/mikec-ai/grants-form-spec/pull/92), merged at
  `bac08000460ef457b5970647d0c9019559398e42`, preserves the three exact F770 cross-form prefill
  instructions at 0-06, 0-07, and 0-10. Their value sources are exact canonical R&R SF-424
  occurrences for SAM UEI, organization name, and proposed start date.
- A target-neutral zero-based array-item selector now represents the first-budget-period boundary
  for the proposed start date. The evidence contract also permits `unspecified` editability when
  the official source does not state whether a prefilled value remains editable. The projector
  fails closed when a selected array occurrence is absent or does not contain the destination.
- DAT paths 0-08 and L-1-1 are proven structurally: budget type and the project-wide budget
  justification are each emitted once at the form root rather than once per budget period. This
  does not turn them into semantic mappings or infer broader lifecycle policy.
- All three cross-form operations remain `source-bound-uncompiled`. The current Simpler
  prepopulation runtime has no generic cross-form response-copy rule, so this increment preserves
  exact evidence and exposes it to analysis without claiming execution.
- Full producer preflight passed before merge: 123 TypeScript tests and 342 Python tests (10
  skipped), plus artifact, XML fixture, promotion, parity-ledger, classified-field, package, and
  independent TypeSpec-file checks. Both required GitHub workflows passed.
- The lifecycle/prefill source-modeling sub-slice is complete. Generic cross-form execution,
  remaining browser confirmation, human semantic/accessibility acceptance, operational readiness,
  and production registration remain open; the broader release-gate task therefore remains in
  progress.

## 2026-08-24: next claimed cross-form prefill consumer slice

- `root_budget_cross_form_prefill` claims a bounded Simpler-fork investigation and implementation
  for the three source-exact R&R Budget prefill records delivered in grants-form-spec PR 92.
- The slice may add only a target-neutral consumer mechanism that resolves canonical values from
  another form response in the same application context. It must fail closed when the source form,
  path, target selection, or lifecycle context is unavailable, and it must preserve the producer's
  `source-bound-uncompiled` boundary unless execution is proven end to end.
- The slice will not add an R&R Budget identifier branch, infer editability, modify producer
  semantics, touch HHS upstream, or overlap the active browser, test-isolation, proof-package, or
  other form-release claims. If the existing application model cannot expose the exact source
  response safely, the deliverable will be a tested feasibility boundary rather than an
  approximation.

[depends on](harden-rr-budget-production.md)

[depends on](author-integrate-rr-subaward-budget.md)

[depends on](author-integrate-rr-budget.md)
