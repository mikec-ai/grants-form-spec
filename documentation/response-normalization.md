# Response normalization boundary

Canonical form schemas describe source-valid responses. They do not absorb legacy capture or
persistence conventions. When an independently reviewed source audit establishes that a legacy
representation has one exact canonical meaning, a form package may carry a versioned
`response-normalization.json` sibling artifact.

The first contract supports one operation: `empty-string-to-absent`. Each declaration names an
exact RFC 6901 form-occurrence path and a reviewed evidence record. Paths, decisions, and evidence
live in portable data. The projector and consumers are generic and contain no form identifiers.

The producer fails closed unless every target:

- resolves to an exact object property in the emitted canonical schema;
- is optional;
- is a non-null scalar string;
- rejects a present empty string through a minimum length of at least one;
- does not require an array or wildcard traversal; and
- has a reviewed evidence record for the same path and operation.

The emitted artifact is content-hashed in the form manifest. Unknown operators, stale paths,
ambiguous schema composition, evidence mismatches, and digest mismatches are package errors.

A consumer applies normalization after any transport-name projection and before canonical schema
validation, rule evaluation, and wire projection. It operates on a copy of the response. The
`empty-string-to-absent` operation removes only a value that is exactly the zero-length string.
Whitespace is preserved, null is not normalized, and undeclared paths are untouched. Direct
canonical validation therefore continues to reject a present empty string.

SF-424A is the initial canary. Its three Section F narrative fields are optional XML elements whose
present values require at least one character. The official XFA excludes null values and removes
the empty `OtherInformation` wrapper before submission. The portable policy converts the legacy
empty-string capture representation to those source-valid omissions without weakening the shared
budget questions.

Response-normalization evidence is operational compatibility evidence. It is separate from
semantic question mappings and does not contribute to form-reuse coverage metrics.
