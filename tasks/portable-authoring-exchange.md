---
type: Task
title: Add a provider-neutral form authoring exchange
priority: P1
assignee: Codex
description: >-
  Create the immutable work-package and atomic recommendation-package boundary
  that allows any compatible agent or GUI to propose form changes without
  coupling the form product to an agent runtime.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T21:17:56.947Z'
---
# Scope

Implement the first provider-neutral form-authoring exchange boundary, using the proven NOFO Builder review-exchange pattern as a reference without importing Builder-specific concepts.

# Acceptance criteria

- Export an immutable, digest-bound authoring work package containing the exact draft, question-bank records, request, and evidence references.
- Accept a versioned recommendation package containing atomic proposals rather than an opaque replacement form.
- Validate package identity, canonical digests, unique proposal IDs, supported operations, referenced questions, and exact baseline preconditions.
- Apply proposals only to the neutral authoring workspace; expose no renderer, producer publication, model SDK, or authoritative repository mutation capability.
- Preserve proposed semantic status and exact evidence receipts.
- Demonstrate that different agent runtimes can use the same exchange contract.
- Add tests for valid exchange, tampering, stale baselines, unknown questions, duplicate proposals, and unsupported operations.

# Outcome

Merged in `mikec-ai/grants-form-workbench` PR #40. Source commit `4ea8ff5a2961550c9e51313f5a583851afe29fc2`; merge commit `aedc5b8109bc388ac305a212c9c216c4f1cb5c70`.

- Added `@grants-form-workbench/authoring-exchange` as a separate, inward-only package.
- Added complete request-envelope and recommendation-envelope canonical digests.
- Added strict runtime validation for unknown fields, contributor provenance, evidence, supported operations, exact question identities, stale baselines, and operation preconditions.
- Added independent accept, modify, and reject decisions; modified operations are revalidated immediately before application.
- Applied changes remain `proposed` for semantic review and therefore do not contribute to published semantic coverage.
- Added five v1 operations: select, remove, and move question; add and remove condition rule.
- Documented the exchange boundary and explicitly excluded renderers, publication, model SDKs, and authoritative repository mutation.

# Verification receipts

- 15 authoring-exchange tests passed.
- 8 workspace architecture tests passed.
- Workspace TypeScript typecheck passed.
- Production build passed for every package.
- 375 non-agent-tool tests passed, including the exact pinned producer reimport when supplied the configured `a97da3714733566847349efcc013c6a79045b21b` checkout.
- The separate agent-tools suite retains 8 pre-existing canonical-fixture drift failures; no agent-tools files or fixtures changed in this work.
- GitHub Actions created no execution steps because of account infrastructure, so local verification is the authoritative signal for this merge.

# Reference architecture

The design adapts the Builder decision “Isolate the virtual NOFO agent behind a review exchange contract” and its successful clean-context dogfood. Form-specific atomic operations replace Builder text-range operations.

[depends on](implement-human-agent-form-composer.md)
