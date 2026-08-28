---
type: Task
title: Reconcile source occurrences with the reusable question bank
priority: P0
assignee: Codex
description: >-
  Implement a provider-neutral, review-gated change-set workflow for proposing
  question reuse, bounded occurrence mappings, and genuinely new canonical
  questions.
superbee_progress_status: in_progress
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-28T14:38:49.455Z'
---
# Objective

Close the learning loop between source-backed form authoring and the reusable question bank. For each exact source occurrence, a compatible agent or human must be able to propose reuse of an existing question, a bounded occurrence override, or a genuinely new canonical question definition. Semantic authority remains human-reviewed and separate from operational draft acceptance.

# First vertical proof

Use EPA Key Contacts if its exact source dossier and SGG parity oracle are locally available; otherwise use the nearest identity/contact form with the same evidence properties. The proof must exercise both safe reuse and at least one proposed new question without adding form-specific renderer, compiler, or adapter branches.

# Acceptance criteria

- Add provider-neutral proposal operations for existing-question reuse, proposed question definition, and exact occurrence binding.
- Preserve role, dimensional context, cardinality, source path, source version, artifact digest, rationale, and review state.
- Keep operational draft acceptance distinct from semantic review acceptance.
- Require a separate attributed semantic-review receipt before a mapping or new definition becomes eligible for the reviewed bank projection.
- Produce a deterministic, versioned bank change set; never let the browser or agent mutate the authoritative bank directly.
- Fail closed on stale baselines, duplicate identities, conflicting definitions, unknown evidence, and unsupported schema facets.
- Compile and render the candidate form through the existing portable package boundary with no consumer/runtime changes.
- Add tests for similar wording with different roles, accepted reuse, rejected reuse, proposed new questions, semantic-review gating, tampering, and deterministic export.

# Boundaries

This is design-time authoring and semantic-review infrastructure. Do not change renderer behavior, SGG runtime behavior, published coverage, or accepted mappings without an explicit qualified review receipt.

# Implementation checkpoint — 2026-08-28

Merged [grants-form-workbench PR #51](https://github.com/mikec-ai/grants-form-workbench/pull/51) at commit `330d8691a047bdf5097da184557c88c89830b84c`.

Delivered:

- `packages/question-reconciliation`, with four versioned contracts for requests, provider-neutral proposals, independent semantic-review receipts, and reviewed bank change sets.
- Exact binding for source path, source version and digest, occurrence digest, role, dimensions, cardinality, evidence references, question digest, proposal digest, and review authority.
- Deterministic reviewed projection and pure application to a candidate bank; no direct authoritative-bank write.
- Integration into the neutral authoring workspace and existing portable compiler boundary.
- Fail-closed checks for stale requests and baselines, altered receipts, altered accepted bindings, duplicate decisions and identities, false role equivalence, unknown or repeated evidence, unsupported proposal differences, and competing accepted resolutions.
- Architecture enforcement forbidding renderer, Simpler, React, WYSIWYG, and form-identity coupling.

Verification receipts:

- Typecheck, workspace build, and 152-question catalog-integrity check passed.
- 10 reconciliation tests and 8 architecture tests passed.
- Broader Vitest suite: 430 of 431 passed; the remaining existing test is blocked because the local producer checkout does not match its configured pinned revision.
- Agent-tools suite: 62 of 70 passed; eight existing golden artifacts have digest drift, with no dependency path from agent-tools to the new package.
- GitHub Actions did not start because the account spending limit is exhausted; this is an infrastructure failure, not a test result.

Remaining before this task is complete:

- Run the workflow against the checked-in exact EPA Key Contacts dossier/package rather than only the isolated identity/contact contract proof.
- Carry the reviewed candidate through the browser renderer and record the usability/parity receipt.
- Keep any real semantic decisions proposed or unreviewed until a qualified reviewer supplies the separate authority receipt.

# Browser dogfood — 2026-08-28

Codex acted as the human reviewer in the standalone workbench at `http://127.0.0.1:5177/`.

Verified in the browser:

- The plain-language request produced four proposed questions and one proposed visibility rule.
- Adding the suggestions created a resumable local project without marking semantic mappings reviewed.
- The live preview hid Email until Project Title equaled `Research`, then displayed it immediately; the condition counter changed from 0/1 to 1/1.
- The source-backed PHS Assignment Request dossier exposed pinned XSD, DAT/XLS, read-only PDF, instructions, exact digests, 13 source occurrences, five question concepts, and a statement that the oracle is withheld.
- Starting the source-backed Codex review visibly distinguished dossier loading from agent work and exposed cancellation.

Observed reviewer gaps:

- Selected questions and rules are labeled `Needs review`, but the compose screen provides no clear accept, reject, revise, or defer action and no way to record review authority or rationale.
- `Use suggested questions` is operational draft inclusion, but its label can be mistaken for semantic acceptance. The UI needs explicit copy separating `Add to draft` from `Approve semantic mapping`.
- The generic question list is cognitively expensive at 185 items and shows many unreviewed recurrence counts before the reviewer sees the small proposed decision queue.
- Agent rationale and evidence are collapsed behind generic details controls; a reviewer needs an opinionated decision card that leads with the agent recommendation, material differences, evidence summary, confidence, and the consequence of accepting it.
- The source-backed agent run remained in progress long enough for the browser-control session to time out. The page showed only rotating status language, without elapsed time, durable job identity, or a safely resumable progress receipt.

Next implementation should connect the merged question-reconciliation contracts to a focused review queue in the authoring UI. Each proposal needs Accept, Reject, Revise, and Defer; accepting must collect the separate reviewer identity, authority, rationale, and evidence receipt required by the contract. Draft inclusion must remain a different action. The browser should then materialize only reviewed bindings into the candidate preview while leaving the authoritative bank unchanged.

# Semantic review queue checkpoint — 2026-08-28

Implemented and merged in [grants-form-workbench PR #52](https://github.com/mikec-ai/grants-form-workbench/pull/52), source commit `48df69cbc2c05b8e72c5da3f7b92ef2607235abc`, merge commit `9f90e81b27be5f3eae7350e17ee97a66917f034f`.

Delivered:

- Added a source-backed semantic reconciliation projection that preserves every exact occurrence, canonical question digest, source/version/digest, role, dimensions, cardinality, recorded difference, agent rationale, confidence, and pinned evidence reference.
- Added a focused human queue with separate `Approve semantic mapping`, `Reject semantic mapping`, `Request revision`, and `Decide later` actions. Revision and deferral create no semantic receipt and do not affect coverage.
- Required reviewer identity, review authority, evidence URI, and rationale before acceptance or rejection can create a digest-bound receipt.
- Added deterministic change-set download and a pure application seam that annotates only accepted mappings in the candidate preview. The authoritative question bank remains unchanged.
- Renamed operational actions to `Add suggested questions to draft` and `Accept implementation changes and preview` so form construction cannot be mistaken for semantic approval.
- Preserved the source form's presentation order in the semantic queue, including repeated occurrences of one proposed canonical concept.

Verification receipts:

- Targeted reconciliation, deterministic projection, and browser integration tests passed.
- Typecheck, 152-question catalog-integrity check, and production build passed.
- Broader Vitest suite: 434 of 435 passed. The existing remaining failure is the intended provenance guard rejecting a local producer checkout at `273d1ba8...` against configured revision `a97da371...`.
- Existing agent-tools golden drift remains 8 of 70 tests and is unrelated to the new package/UI dependency path.
- GitHub Actions again failed before executing any steps because of the account spending limit.

Live browser dogfood receipt:

- Resumed the exact PHS Assignment Request project, completed the independent operational decision queue, and reached a second semantic gate.
- The queue clearly stated that semantic approval differs from adding a field, exposed 13 exact occurrences and five pinned evidence references per proposal, and showed material title/description differences before a decision.
- Approved one exact mapping and applied it to the preview. The UI then showed exactly one `Semantically accepted` occurrence and 12 `Needs semantic review` occurrences.
- Dogfood exposed and corrected one UX defect: internal proposal sorting initially alphabetized paths; stable index-prefixed occurrence IDs now preserve applicant presentation order without weakening identity or digest checks.

Remaining scope:

- Exercise a genuine `new-question` proposal in the full browser flow using EPA Key Contacts or another exact identity/contact dossier.
- Have a qualified domain reviewer provide any real semantic authority receipts before published coverage changes.

# Durable semantic workflow checkpoint — 2026-08-28

Implemented and merged in [grants-form-workbench PR #53](https://github.com/mikec-ai/grants-form-workbench/pull/53), source commit `6415e09d4d258e738158dbce9afaa817fe5641a3`, merge commit `7ab799e94d541555a242678aecc5c43b62520114`.

Delivered:

- Added the versioned `portable-semantic-review-workflow/v1` contract. It embeds the exact digest-bound reconciliation request and proposal package and records decisions as a contiguous, append-only revision history.
- Persisted accepted, rejected, revision-requested, and deferred outcomes with the authoring project. The same workflow now survives automatic local saves, project resume, and project transfer/export-import.
- Preserved exact authority receipts only for accepted and rejected decisions. Revision requests and deferrals retain actor, timestamp, and rationale where required but cannot carry an authority receipt.
- Derived the active question-bank change set from the latest revision for each proposal. A later deferral or revision request withdraws an earlier approval from the active projection without erasing its history.
- Restored the exact stored reconciliation request and proposal package on resume rather than recomputing it from mutable agent/contributor context.
- Changed the semantic download from a transient change set to the complete durable review workflow.

Verification receipts:

- The 152-question catalog-integrity check, production build, typecheck, and diff-integrity check passed.
- The new reconciliation and authoring-lifecycle tests passed, including append-only sequencing, tamper rejection, transfer round-trip, and active-change-set behavior.
- The expanded browser integration test passed in the complete initial run. In a later combined run, one unrelated StrictMode attachment-session test flaked and then passed immediately when rerun alone.
- Browser dogfood recorded one approval, one rejection, one revision request, and one deferral on the PHS Assignment Request project; all four exact outcomes survived leaving the composer and resuming the saved project. The UI correctly exposed only one approved mapping and one rejected mapping, with revision and deferral remaining outside semantic coverage.
- GitHub Actions failed before starting any step because the account payment/spending limit blocked execution; the PR was merged with the complete local verification receipts above.

Remaining scope:

- Exercise a genuine `new-question` proposal in the full browser flow using an exact source dossier, preferably EPA Key Contacts if its evidence boundary is sufficient.
- Obtain qualified domain review before treating any real mapping as authoritative or changing published coverage.

# Exact new-question proof — 2026-08-28

Implemented and merged in [grants-form-workbench PR #54](https://github.com/mikec-ai/grants-form-workbench/pull/54), source commit `4ef84dc9ee9c5ce4fcc413c7aee316e7084f0cb0`, merge commit `bbd36ab32c6193f63453485b987d0275b31b5f4b`.

Delivered:

- Added an exact source-authoring dossier for EPA Key Contacts 2.0 with pinned XSD, DAT/XLS, read-only PDF, sample PDF, global-library XSD, and universal-code XSD evidence digests.
- Added a draft-local candidate question, `epa/key-contact-person`, assembled from existing person-name, title, address, phone, and email questions. It remains outside the baseline and published banks until separately reviewed.
- Preserved four distinct source occurrences and roles: Authorized Representative, Payee, Administrative Contact, and Project Manager. Similar structure does not erase their role distinctions.
- Extended the provider-neutral exchange and authoring boundaries to preserve role and dimensions without adding a form-specific consumer, compiler, adapter, or renderer branch.
- Allowed repeated exact new-question proposals to add one canonical question once, while failing closed on conflicting definitions, stale baselines, or candidates that do not match the exact draft-local digest and URI.
- Made new canonical definitions explicit in the semantic review UI, including the proposed definition, provenance, review state, and consequence of approval.

Verification receipts:

- Catalog integrity, production build, typecheck, and diff-integrity checks passed.
- 51 change-specific tests passed, including the full browser integration scenario.
- Live browser dogfood completed the full loop: the agent authored four role-qualified fields; operational review opened the SGG-style preview; the semantic queue presented four independent `new-question` proposals; four attributed approvals produced one added question and four accepted bindings; the preview remained functional.
- Oracle differences were surfaced as intentional review items rather than hidden or mislabeled as parity.
- The repository-wide architecture test still reports the pre-existing `authoring-lifecycle -> question-reconciliation` dependency; this slice did not modify either offending file.
- GitHub Actions failed before executing any steps because the account payment/spending limit blocked the job.

Remaining authority boundary:

- This proves the engineering and review workflow, not the semantic correctness of `epa/key-contact-person`. A qualified domain reviewer must supply the authority receipt before the definition or its four bindings can affect the authoritative bank or published coverage.

# Mixed package projection checkpoint — 2026-08-28

Implemented and merged in [grants-form-workbench PR #55](https://github.com/mikec-ai/grants-form-workbench/pull/55), source commit `266b3f3cf276df88ac2163533aff0d54150a15ca`, merge commit `d5172e07f5270f9b28e39457784a202673cf8ccd`.

Delivered:

- Added a provider-neutral projection from an exact portable form package plus an explicitly pinned question baseline into the existing semantic-review request and proposal contracts.
- EPA Form 4700-4 now proves mixed classification in one agent-authored artifact: 28 nested source occurrences become seven reuse proposals and 21 genuinely new-question proposals.
- Reuse requires canonical question ID plus the exact schema digest. Revision-addressed artifact URLs may differ when content is identical; both remain pinned evidence rather than being mistaken for a semantic conflict.
- Package-local questions absent from the baseline remain explicit proposals. Conflicting schemas, shadowed URIs, invalid pointers, and unavailable questions fail closed.
- Regenerated the stale EPA package and refreshed its definition, package, catalog, and cohort receipts. The new test exposed that the prior package receipt no longer matched the current authoring definition/compiler output.

Verification receipts:

- 16 reconciliation tests passed, including exact EPA classification, deterministic 28-binding/21-addition fixture review, conflicting-schema rejection, and revision-URI tolerance.
- The focused EPA compiler and proof-receipt tests passed.
- Catalog integrity, browser-catalog integrity, typecheck, production build, and diff-integrity checks passed.
- GitHub Actions executed zero steps because the account payment/spending limit blocked the job.

Next boundary:

- The workbench consumer can now receive the projection, but it still needs an explicit baseline-catalog provider before the verified-form screen can open the 28-item human semantic queue. The combined runtime catalog cannot safely infer which questions were baseline versus package-local.

# Verified-package browser review checkpoint — 2026-08-28

Implemented and merged in [grants-form-workbench PR #56](https://github.com/mikec-ai/grants-form-workbench/pull/56), source commit `cb21c5775c4031a78f289704972f286a2e55d93f`, merge commit `99af82b43a7fab46ef4b47b9fe5c83e27538a90f`.

Delivered:

- Extended the browser catalog with an explicit, digest-verified question-baseline provider. The consumer no longer infers an authoring baseline from the combined runtime catalog.
- Published the exact 152-question `producer-77fcbe1d` baseline at SHA-256 `670428059f0d9a0391aeb07955be27e850709e73be7d641a32a3008a7249b115` and linked EPA 4700-4 to it through generic catalog metadata.
- Opened the existing independent semantic-review workflow directly from a verified portable package: EPA 4700-4 yields 28 decisions, separated into seven reuse candidates and 21 new-question candidates.
- Added a pure application seam that promotes only exact attributed approvals into the candidate package's occurrence review receipts. It does not alter the package schema, question definitions, authoritative bank, or published coverage.
- Added focused All / Reuse / New questions views. Browser dogfood exposed a crushed two-column decision-card layout; the review queue now uses a readable single-column evidence and action layout at normal workbench width.
- Reconciled the architecture guard with the already-merged durable semantic-workflow dependency and removed a generic form-identity identifier violation. All architecture tests now pass.

Verification receipts:

- 20 focused catalog, reconciliation, architecture, browser-transport, and browser-integration tests passed.
- Package typechecks, production build, browser-catalog check, 152-question catalog check, and diff-integrity check passed.
- Broad local suite: 397 of 400 passed under concurrent execution; the three failures were existing timing/control issues outside this change. The two timing failures passed immediately when isolated; the pre-existing USWDS invalid-number blur test still fails independently and has no dependency on this slice.
- Browser dogfood loaded the exact EPA package `e36d350b00c1cf049ecc08d338da8c94c2e9140a29123fb99b29d6210618fad7`, authenticated the baseline, showed seven reuse proposals after filtering, and applied one explicitly fixture-only approval. The preview receipt changed from `0 accepted / 7 proposed / 21 unreviewed` to `1 accepted / 6 proposed / 21 unreviewed` without changing form structure.
- GitHub Actions failed before executing any step because the account payment/spending limit blocked the job. PR #56 was administratively merged using the complete local receipts above.

Remaining authority boundary:

- The end-to-end mechanism is complete. Any real acceptance of the seven reuse mappings or 21 new definitions still requires a qualified domain reviewer and must remain outside published coverage until those separate authority receipts exist.

# Second-form and repeated-section canary — 2026-08-28

Implemented and merged in [grants-form-workbench PR #57](https://github.com/mikec-ai/grants-form-workbench/pull/57), source commit `28d6dd7455e226cf9430df9dc7aaed7b8582c65a`, merge commit `71ac06467fa10af0808058b4348dfc14e5199c5e`.

Delivered:

- Linked the independently authored PHS Additional Indirect Costs 2.0 package to the same explicit, digest-verified `producer-77fcbe1d` baseline without changing the package digest `12b18d19d4977d963fd8ded89c0964cda6bcab3b0ae2a0402d46b7995ebd4135`.
- Extended the generic occurrence resolver to traverse `*` path segments through JSON Schema array `items`, including nested repeated indirect-cost rows. Wildcards outside array schemas fail closed.
- Ran all 12 exact PHS source occurrences through the same review projection used by EPA 4700-4. The deterministic result is zero exact reuse candidates and 12 proposed new questions.
- Preserved the negative result as evidence: the system does not manufacture reuse from similar budget wording, repeated structure, or the fact that both packages use the same authoring workflow.
- Added actual app-level review coverage showing the human queue exposes all 12 items under `New questions`, with no accepted semantic decision and no published coverage change.

Verification receipts:

- The question-reconciliation package build and demo-portal typecheck passed.
- All 35 focused reconciliation and app tests passed across the two files; one unrelated timing-sensitive project-transfer test timed out only in the combined concurrent run and passed when isolated.
- Portable browser catalog verification passed with 30 forms, three cohorts, one baseline, and 32 exact files; diff-integrity checks passed.
- The in-app browser local reload was blocked by its URL policy. The equivalent selection, queue opening, classification, filtering, and decision-count flow is exercised by the app integration test.
- GitHub Actions failed before executing any steps because the account payment/spending limit blocked the job. PR #57 was administratively merged using the complete local receipts above.

Remaining authority boundary:

- Zero reuse is the deterministic implementation-level classification against this exact pinned baseline, not a policy conclusion that these questions can never be harmonized. Any broader semantic equivalence or new canonical definitions still require qualified review and separate authority receipts.

# Quad 7 reference-form review activation — 2026-08-28

Implemented and merged in [grants-form-workbench PR #58](https://github.com/mikec-ai/grants-form-workbench/pull/58), source commit `e12a4ad3e21006ad5a5248e0816289a5f71618d6`, merge commit `38d37979c8e733de3a2f908d9bb21510dc6c5074`.

Delivered:

- Activated the existing digest-bound review queue for SF-424 4.0, R&R SF-424 5.0, and R&R Budget 3.0 through catalog configuration only.
- The three exact producer packages expose 48, 21, and five source occurrences respectively: 74 decisions through one generic consumer workflow.
- All 74 are exact implementation-level reuse candidates against the pinned producer question catalog. They remain proposals; this activation creates no semantic authority receipt and changes no published coverage.
- Added an app integration test that selects each form, opens the common review queue, and verifies the exact candidate and occurrence counts.

Verification receipts:

- The targeted app integration test, demo-portal typecheck, portable catalog check, and diff-integrity check passed.
- The portable catalog remains 30 forms, three cohorts, one exact baseline, and 32 files.
- GitHub Actions again executed zero steps because the account payment/spending limit blocked the job. PR #58 was administratively merged using the local receipts above.
