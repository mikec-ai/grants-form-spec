# EPA Key Contacts behavior closure plan

Status: producer analysis and bounded implementation plan  
Form: EPA Key Contacts 2.0 (FID 674)  
Evidence boundary: official DAT/XSD/PDF sources pinned; semantic mappings remain proposed

## Decision summary

The 36 source-bound DAT effects do not require one undifferentiated runtime project.

| Cohort | Count | Current portable representation | Disposition |
|---|---:|---|---|
| State required when Country is USA | 4 | `@Validation.requiredPathWhen` on the form-local contact address occurrence | Existing generic contract; exact emitted targets are compiled |
| ZIP/Postal Code required when Country is USA | 4 | `@Validation.requiredPathWhen` on the form-local contact address occurrence | Existing generic contract; exact emitted targets are compiled |
| Six required fields when any role field is entered | 24 | Optional role object whose nested contact composition requires First Name, Last Name, Street1, City, Country, and Phone | Existing JSON Schema semantics; exact emitted targets are compiled through generic evidence recognition |
| State initially active/optional, then active+required for USA or inactive for non-USA after Country exit | 4 | Requiredness is represented; interaction timing/state is not | Requires a generic event-aware interaction extension or a separately reviewed intentional delta |

No row changes semantic-review status. A compiled behavior disposition means only that an exact source-backed behavior has an executable portable artifact target; it does not accept a semantic mapping or establish browser, accessibility, policy, or release readiness.

## Existing-contract result: eight compiled requiredness effects

The emitted schema contains one country-guarded `allOf` branch for `state` and one for `zipCode` in the reusable form-local contact composition. The four role occurrences resolve those branches to eight stable canonical targets. The evidence projector recognizes the dot-qualified targets and requires one official-source disposition for each target.

This is producer-level execution evidence. Consumer registration is not required to establish that the portable schema carries the rule, and no form-specific adapter branch is needed.

## Existing-schema result: 24 compiled role-completeness effects

Each role is optional at the form root. Once its object exists, the portable contact composition requires:

1. `name.firstName`;
2. `name.lastName`;
3. `address.street1`;
4. `address.city`;
5. `address.country`; and
6. `phone`.

That is the standard JSON Schema expression of the DAT's any-present completeness boundary: an absent role is valid; a present partial role is invalid. It is not a new UI-rule vocabulary and does not require a form-specific runtime branch.

The producer evidence verifier generically recognizes these 24 required descendants beneath optional object occurrences. It resolves local and external `$ref` composition, merges unconditional `allOf` constraints, requires an exact emitted leaf occurrence, and only treats a target as an executable condition when evidence explicitly claims it as compiled. Generic positive and negative regressions prove that required root objects are not misclassified and that unclaimed optional-object constraints do not create evidence obligations. No EPA, role, or contact identifier is special-cased.

An **unregistered consumer validation** remains a separate integration receipt: load the portable artifact through the generic adapter without registering the form, prove an absent role is valid, a role containing one optional field is invalid with all six source-required targets, and a complete role is valid, and verify the renderer does not materialize four empty role objects on initial load. This is not required to establish the producer artifact target and is not claimed by this slice.

If the consumer materializes empty role objects, do not weaken requiredness. Fix the generic optional-object materialization boundary or record a reviewed intentional delta.

## Genuine contract gap: four State interaction transitions

The DAT distinguishes three states over time:

1. when the form first opens, State is active and optional;
2. after the applicant exits Country with USA selected, State is active and required; and
3. after the applicant exits Country with a non-USA value, State is inactive and optional.

Current `@UI.enabledWhen` is a value-only condition with one `then` and one `otherwise` interaction. It has no event trigger and no separately declared initial effect. Applying it directly would disable State while Country is absent, contradicting the official initial state. The existing `@Validation.requiredPathWhen` correctly handles requiredness but cannot express interaction timing.

There are two honest paths:

### Exact generic extension

Add a target-neutral interaction rule that declares:

- an exact source reference;
- an initial interaction effect;
- a transition trigger such as `source-blur`;
- a predicate evaluated at that trigger; and
- `then` and `otherwise` effects.

This requires coordinated changes to the TypeSpec decorator contract, canonical UI artifact, SGG projection, artifact validators, generic consumer execution, and tests. The contract must be useful beyond EPA Key Contacts and must not branch on form ID.

### Reviewed intentional delta

If product/human review concludes blur timing is immaterial, adopt a value-driven rule that keeps State enabled while Country is absent or USA and disables it for a present non-USA value. This would still require a small generic `absent-or-equals`/inverse predicate capability. The source-versus-runtime timing difference must be recorded and accepted; it cannot be silently presented as parity.

Until one path is selected, the four interaction records remain `source-bound-uncompiled` and `authority: unresolved`.

## Bounded implementation sequence

1. Bank the eight exact State/ZIP requiredness dispositions with producer tests. **Complete.**
2. Add generic optional-object required-descendant recognition to the evidence verifier, with fail-closed tests, and bank the 24 exact completeness dispositions. **Complete.**
3. Run unregistered generic-adapter schema and initial-render checks as a separate integration receipt; do not register the form.
4. Present the event-aware extension versus intentional-delta choice for human/architecture review.
5. If the exact extension is selected, implement it once generically and close the four interaction receipts across all affected roles.
6. Keep consumer registration, browser/lifecycle closure, semantic acceptance, and production release as later separate gates.

## Explicit non-goals

- accepting or publishing any semantic mapping;
- inferring role equivalence from identical contact shapes;
- form-specific compiler, adapter, or renderer branches;
- consumer registration;
- privacy, accessibility, policy, operations, or production approval.
