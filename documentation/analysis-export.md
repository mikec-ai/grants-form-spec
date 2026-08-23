# Form analysis export

The analysis exporter turns the emitted artifact graph into one normalized read model and a set of
spreadsheet-ready CSV tables. It exists to answer two different questions without conflating them:

1. Which accepted semantic questions do forms ask in common?
2. Which implementation capabilities does each successive form reuse or introduce?

Run it after emitting and projecting evidence:

```shell
npm run emit
npm run project-evidence
python3 scripts/analyze.py --json --output-dir build/analysis
```

The output directory contains:

| File | Purpose |
| --- | --- |
| `form-analysis.json` | Complete machine-readable projection, including legacy analysis keys |
| `question-inventory.csv` | Canonical question catalogue, usage frequency, and reviewed usage |
| `form-question-associations.csv` | One role-qualified occurrence per form/question/path with evidence and XML metadata |
| `unclassified-form-fields.csv` | Form-local fields that are deliberately excluded from question metrics pending classification |
| `pairwise-exploratory.csv` | Implementation-derived similarity using authored canonical identities |
| `pairwise-reviewed.csv` | Published-eligible similarity using only explicitly accepted occurrence mappings |
| `capability-occurrences.csv` | Questions, capture mechanisms, and portable runtime behaviors used by each form |
| `marginal-capability-reuse.csv` | New versus reused capabilities in the versioned authoring sequence |

## Review boundary

The two pairwise exports are intentionally separate. `pairwise-exploratory.csv` is useful for
architecture learning and prioritization, but its scope is
`implementation-derived-unreviewed`. `pairwise-reviewed.csv` includes only occurrence mappings
whose evidence record has `status: accepted` at the exact canonical pointer. When neither form in
a pair has accepted occurrences, similarity and directional coverage are blank rather than zero:
absence of reviewed evidence is not evidence of dissimilarity.

The question inventory likewise reports `formsCount` separately from `reviewedFormsCount`, and
each association carries `mappingStatus` and `publishable`. Similar wording, matching JSON types,
or shared rendering never establishes semantic equivalence.

## What is counted

Semantic similarity counts only blocks classified as `semanticQuestion`. Capture mechanisms are
reported separately, so reuse of the attachment control does not make Project Narrative and Budget
Narrative the same question. Runtime behavior capabilities are derived from the emitted rule
artifact and reported separately again. This permits a form to have low semantic overlap but low
implementation cost.

The portable `@Response.role` vocabulary classifies an authored block or occurrence as applicant
input, calculated output, system value, technical field, attestation, or static content. Roles are
emitted in block indexes and the form's path-qualified `fieldOccurrences`; the exporter reads those
facts rather than inferring from `readOnly`, a widget, a label, or an XML path. An occurrence with no
canonical block lineage and no explicit non-question role is emitted in
`unclassified-form-fields.csv` with `countedAsQuestion: false`. Applicant input likewise requires a
canonical semantic question before it enters similarity. Unknown information therefore remains
visible rather than being silently omitted or misclassified.

`analysis/unclassified-fields-baseline.v1.json` is the temporary debt ratchet. Its `initial` set is
the 76 path-qualified occurrences remaining after canonical lineage repair; resolved identities move
to `resolved`. CI rejects new identities, unresolved removals, and the return of resolved debt. When
the remaining set reaches zero, the baseline can be replaced by the permanent zero-unclassified
gate.

## Resolving the ratchet

For each new or existing form field, author one of the following facts:

1. Type the field with an existing `@Question.meta` block when it asks an existing semantic
   question.
2. Add a source-evidenced canonical question block when the semantic requirement is genuinely new.
3. Apply `@Response.role(ResponseRole.calculatedOutput)`, `systemValue`, `technicalField`,
   `attestation`, or `staticContent` when the value is explicitly not an applicant question.

`@Response.role(ResponseRole.applicantInput)` documents ownership but does not bypass canonical
identity: applicant input without a question-bank block remains unclassified. Do not create a
duplicate question merely to clear the report. When a baseline identity is legitimately resolved,
move it from `initial` to `resolved` in the same pull request; the ratchet rejects both an unrecorded
removal and a later return.

## Provenance and XML metadata

Association rows join the following facts when the emitted artifacts provide them:

- canonical question identity, label, description, entity, and tags;
- form identity, version, legacy identifier, occurrence path, and schema constraints;
- accepted source mapping and reviewer attribution;
- deterministic extraction repository, revision, artifact, and source-set hash;
- XSD URI, `xsdNativeVersion`, and hash; and
- XML element path resolved through the portable Grants.gov XML profile.

Portable XML profiles currently describe element projection but do not carry the source XSD
`type` and `type_source` values. Consequently `xmlType` and `xmlTypeSource` are emitted as blank,
not inferred. Adding those exact source facts to a later portable profile contract will populate
the columns without changing the workbook shape.

## Marginal reuse sequence

`analysis/form-sequence.v1.json` is the versioned historical ordering used for the marginal curve.
The exporter fails if the sequence omits an emitted form or names a form that is not emitted. A
different analytical ordering requires a new sequence version rather than silently rewriting the
existing measurement.

The curve currently counts semantic questions, capture mechanisms, and normalized portable rule
capabilities. It is explicitly labeled `implementation-derived-unreviewed`: it measures what the
architecture reused, not accepted semantic coverage or production readiness.
