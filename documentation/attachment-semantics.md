# Attachment semantics and capture mechanisms

## Decision

An attachment is a reusable mechanism for capturing an answer. It is not, by itself, the
semantic information a form requests.

The portable model records these as separate, related blocks:

- A semantic question identifies the information requirement, such as
  `project/narrative`, `budget/narrative`, or `budget/justification`.
- A capture mechanism identifies how the answer is supplied. `generics/attachment`
  represents an uploaded-file reference.
- A form occurrence records the semantic question's data path, cardinality, structural
  relationship, and source evidence.

The semantic question composes the capture mechanism. Runtime emitters may therefore infer
attachment validation from the mechanism while analysis counts the semantic question.

## Why one classification is insufficient

Meaning, interaction, and representation are independent facets:

| Facet | Examples | Analytical use |
| --- | --- | --- |
| Semantic identity | project narrative, budget justification | question inventory, similarity, coverage |
| Response role | applicant input, calculated output, system-supplied value, technical field, static content | distinguish questions asked from values displayed or managed |
| Capture mechanism | attachment, text, date, choice, structured group | implementation and capability reuse |

Block classification distinguishes semantic questions from capture mechanisms. Response-role
classification is resolved per form occurrence because the same semantic value can be entered by
an applicant in one context and calculated or supplied by a system in another. Authors may place a
default role on a reusable block and override it on a form property; the emitted
`fieldOccurrences` inventory records the effective role at each canonical response path.

## Alternatives considered

### Treat the attachment control as the question

This preserves a very small bank and accurately reports renderer reuse. It causes Project
Narrative, Budget Narrative, and Other Narrative to appear semantically identical, so it cannot
answer the portfolio-analysis question.

### Store semantic meaning only as form-property metadata

This preserves the runtime schema shape, but semantic identity no longer has an independently
renderable, referenceable bank block. Reuse becomes a string convention rather than composition.

### Compose a semantic question with a classified mechanism

This is the selected model. The form references a role-specific semantic question. Its emitted
index records composition of `generics/attachment`, even where scalar inheritance is flattened by
the standard JSON Schema emitter. The form's resolved value remains a UUID or UUID array, so the
runtime contract does not change.

## Analysis rules

- Question inventory includes blocks classified as `semanticQuestion`.
- Capture mechanisms have a separate inventory and form association export.
- Form-to-question associations preserve the form, semantic question, occurrence path, and direct
  or transitive relationship.
- Pairwise similarity uses semantic-question identities only.
- Mechanism overlap is reported separately and may support implementation estimates.
- Coverage metrics may use accepted canonical identities and reviewed mappings. Proposed or
  unreviewed mappings never contribute to published coverage.
- Deprecating a semantic question depends on semantic occurrences. Deprecating a mechanism depends
  on all structural consumers, regardless of their semantic identity.
- Prefill analysis applies to semantic values and response roles. Reusing an attachment control
  does not imply that attachment content can be prefilled.

For the three standalone narrative forms, semantic overlap is zero while attachment-mechanism
overlap is complete. This expresses both the distinct information requirements and the low
incremental implementation cost.

## Migration scope

The initial migration covers:

- Project Narrative, Budget Narrative, and Other Narrative;
- SF-424 areas affected, additional project titles, additional congressional districts, and
  delinquent federal debt explanation; and
- R&R Budget justification, additional equipment, and additional key-person information.

The generic Simpler adapter continues consuming schema, UI, and rule artifacts. It does not
classify semantics or calculate similarity.
