# Classified form-field gate

Every emitted leaf field must be attributable to either a canonical question-bank block or an
explicit non-applicant response role. The analysis exporter derives this from each form's
path-qualified `fieldOccurrences`; CI then runs `npm run check-classified-fields` against the
generated analysis.

The default is zero unclassified occurrences and zero exceptions. This keeps implementation reuse
and exploratory similarity grounded in authored identities rather than labels, JSON types, or
renderer structure. It also keeps `technicalField`, `systemValue`, `calculatedOutput`,
`attestation`, and `staticContent` occurrences visible without counting them as semantic questions.
Capture mechanisms remain separately classified and contribute only to capability reuse.

## Resolve a failure

For each reported `formId:fieldPath`, inspect the official source and the emitted occurrence, then
choose one of these paths:

1. Reuse an existing question-bank block when it represents the same meaning. Preserve the
   occurrence's requiredness, validation, and response owner in the form declaration.
2. Add a new source-evidenced question block only when the requirement is genuinely new. Similar
   wording or shape is not evidence of semantic equivalence.
3. Author an explicit `@Response.role` when the field is a calculated output, system value,
   technical control, attestation, or static content. `applicantInput` documents ownership but does
   not replace canonical semantic lineage.

Do not add a duplicate question merely to satisfy the gate, and do not infer a role from `readOnly`,
a widget, a label, or an XML target.

## Temporary exceptions

An exception is a last resort for a source-bound field whose classification cannot be completed in
the same change. Add it to `analysis/unclassified-field-exceptions.v1.json`, sorted by `formId` and
`fieldPath`, with every field below:

```json
{
  "formId": "example-form",
  "fieldPath": "/exampleField",
  "evidenceReferences": [
    "evidence/forms/sf424/evidence.json#/semanticReview/mappings/0"
  ],
  "owner": "named-owner-or-team",
  "reason": "Why neither lineage nor a non-applicant role can be safely authored yet.",
  "removalCondition": {
    "criterion": "The exact evidence or implementation decision that removes this exception.",
    "trackingReference": "tasks/example-classification"
  }
}
```

The gate rejects incomplete, duplicate, unsorted, and stale exceptions. When the occurrence is
classified, remove its exception in the same change. Exception records authorize no semantic
equivalence and never enter similarity or reuse metrics.

Each evidence reference must be a canonical repository-relative `evidence/**/*.json` path followed
by a JSON Pointer to content that exists in that file. A tracking reference must be either a
Superbee task identifier such as `tasks/example-classification` or a complete GitHub issue/PR URL
such as `https://github.com/mikec-ai/grants-form-spec/issues/123`.
