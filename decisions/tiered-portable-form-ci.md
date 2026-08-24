---
type: Architecture Decision
title: Risk-tiered CI for portable form banking
superbee_updated_by: codex-root
---
# Decision

Portable-form delivery uses risk-tiered CI. A pull request that only adds or updates vendored portable artifacts and exact XSD fixtures may use a lightweight bank-only lane. The classifier is fail-closed: any consumer code, test, registration, runtime identity, projection, workflow, unexpected path, or deletion selects full API and browser CI.

# Bank-only gates

- Verify the complete selected artifact tree against its immutable manifest digests.
- Verify every declared Grants.gov XML profile against the exact vendored XSD digest.
- Require the prior selected-form set to be a subset of the new selection.
- Require the prior selected-artifact closure to be a subset of the new closure.
- Preserve the separation between banking and runtime enablement or registration.

Bank-only validation must be dependency-free and must not initialize the API database or browser environment. It proves that inert declarative inputs were banked intact; it does not claim runtime or UI parity.

# Escalation and release boundary

Full API and browser CI remains mandatory for executable consumer changes, runtime enablement, registration, production release, and an upstream contribution. Pull requests fail closed to that tier whenever they cross the additive banking boundary. The public prototype fork does not repeat deployment, image publication, infrastructure validation, or local and deployed E2E automatically after a reviewed change merges to `main`; those workflows remain manually dispatchable or reusable as an explicit upstream preflight. Catalog-wide browser conformance remains a separately scheduled milestone rather than a per-form banking cost.

# Rationale

The measured NIFA Supplemental run reached a green producer in about 23 minutes and an open consumer PR in about 42 minutes, but generic SGG API and four-shard browser CI dominated the remaining wait despite the form being banked and unregistered. The tier preserves evidence-bearing gates at the boundary actually changed while escalating any broader change automatically.

Consumer PR #70 implemented the prototype-fork post-merge boundary at merge commit `270f438ef47c4f0a0567598a482c620421d74f0e`. It removed only automatic `main` push triggers from the expensive workflows and preserved pull-request and manual/reusable entry points. No HHS upstream workflow was changed.

[constrained by](canonical-form-architecture.md)
