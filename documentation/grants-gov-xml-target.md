# Grants.gov XML target profiles

Canonical questions and forms remain independent of any delivery target. Grants.gov XML is
published as an optional target extension: declarative JSON that maps canonical form response
fields to a specific XSD wire contract.

```text
canonical form artifacts
        +
targets/grants-gov-xml profile
        |
        v
self-contained targets/grants-gov-xml.json
        |
        v
generic consumer adapter -> XML
```

Producer-side artifact checks use the target-neutral
[XML/XSD conformance harness](xml-xsd-conformance-harness.md). That reference interpreter is
test infrastructure, not a production adapter.

The source mapping vocabulary contains five node kinds:

- `value`: one response value becomes one XML element;
- `object`: child response fields become child elements;
- `group`: a wire-only wrapper collects explicitly sourced canonical values without adding
  the wrapper to the question model;
- `array`: each item is mapped with one reusable item mapping;
- `attachment`: a consumer resolves an attachment reference into the standard Grants.gov
  attachment wire structure.

Wire structure is also data. Groups may nest to declare XSD-only parent elements without
forcing those containers into the canonical response model. A flattened group collects
explicitly sourced values but emits no wrapper of its own, which lets one canonical object
produce ordered sibling elements. Arrays may map either object fields or one scalar/attachment
`node`. These generic composition features cover nested supplements, shared justification
containers, and repeated scalar or attachment elements without form-specific adapter code.

Profiles contain only data: root element and attributes, namespaces, a pinned XSD URI and
digest, and the mapping. An array may additionally declare an imported item element,
namespace, and fixed attributes. Consumers must not branch on a form id.

When `itemElement` is present, the default wire shape is one `element` collection wrapper
containing one `itemElement` for each array item. An array may set
`repeatElementPerItem: true` when the XSD instead repeats `element` and gives each occurrence
one `itemElement`. The distinction is explicit profile data; consumers must not infer it from
element names, namespaces, or form identity.

A scalar array item may declare exactly `{ "kind": "value", "flatten": true }`. The
consumer writes each scalar directly into the array-created element instead of inventing a
nested value element. PHS Human Subjects 3.0 demonstrates both official source shapes that
require this generic operation: `EnrollmentCountry` and `StudyConditions` repeat directly,
while `ExemptionNumbers` is one wrapper containing repeated `ExemptionNumber` values. The
profile still declares the wrapper and item element where the XSD has them; `flatten` changes
only where the scalar text is written.

Flattened scalar items are valid only in an array `items.node`. They cannot declare an
element, namespace, source, constant, value map, attributes, children, or item metadata.
The contract schema rejects those additions, and the reference runtime independently rejects
illegal context or ignored properties. This is a versioned, fail-closed operation; consumers
must not interpret `flatten` on any other value node or infer it from a form id.

A mapping node may declare an absolute `source` JSON pointer. This is primarily used inside
`group` nodes when the official XSD introduces structure that applicants never answer as an
object. For example, R&R SF-424 asks for one applicant congressional district while its XML
wraps that value in a `CongressionalDistrict` element. The target profile owns that wrapper;
the canonical form remains a scalar question.

The reference interpreter rejects every response property that no mapping node consumes,
recursively through objects and object arrays. This prevents a profile from silently dropping
canonical data during XML projection. A schema-backed consumer or UI control that intentionally
does not enter the source wire may be declared by its exact JSON pointer in
`mapping.nonEmittingResponsePaths`. Those pointers are validated against the canonical form
schema and must identify exact scalar leaves that neither overlap a mapped path nor overlap
another non-emitting path. Object and array containers are never valid exceptions. These paths
are not an open-ended additional-properties escape hatch. Constants and `source` overrides
consume only their declared values. An object- or object-array-valued `source` still validates
recursively against the node's declared children; it does not make the source subtree opaque.
Omitted optional or conditional fields require no exception.

An `object` node may declare `emitWhenParentPresent: true` when the pinned XSD requires its
element whenever the parent object is emitted, even if the canonical child object is absent.
The consumer emits the declared object with no child values in that case. This is wire
cardinality data, not a default answer and not a form-specific adapter decision. The option is
valid only for object nodes whose XSD permits an empty content model at that point.

The standard Grants.gov attached-file wire children are data as well. Profiles that map an
`attachment` compose the shared `attached-file-data-1.0.json` declaration, which names
`FileName`, `MimeType`, `FileLocation`, `HashValue`, and their namespaces. Consumers resolve
the attachment reference and mechanically project those declared fields; they do not hardcode
the Grants.gov child vocabulary.

A `value` or `attachment` leaf may declare one `container` with an element and explicit
namespace. The container is emitted only when the leaf is emitted, and wraps only that leaf.
It does not select data, add a presence condition, or apply to objects, groups, or arrays. This
small wire-only feature covers official contracts such as
`BioSketchsAttached/BioSketchAttached` without changing a semantic attachment question into an
object or teaching a consumer about a particular form. Deeper or conditional wire structures
continue to use the separately declared group vocabulary.

`globLib:AddressDataTypeV3` defines State and Province as an XSD choice. A portable profile
maps both source-backed fields in their declared sequence and never silently chooses one when
both are present. Normal form interaction disables State outside the United States and makes
Province read-only for a United States address. The canonical schema can still retain a stale
disabled value, so State and Province can coexist in stored canonical data. Until portable
mutual-exclusion validation is implemented, every consumer must run mandatory validation
against the exact pinned XSD before submission or release. That validation remains a consumer
and release gate and rejects a payload containing both.

Mappings address the canonical camelCase response shape. A consumer that stores another shape
projects these source keys at its boundary. In particular, Simpler owns `samUei -> samuei` and
the historical numbered-cost spellings; those aliases do not appear in the portable target.

## Authoring and emission

Reusable fragments live in `targets/grants-gov-xml/mappings/`; form profiles live in
`targets/grants-gov-xml/profiles/`. Source profiles compose mappings with local `$ref`. The
projection step resolves those references and emits one self-contained artifact under each
form package:

```text
dist/forms/<form-id>/targets/grants-gov-xml.json
```

The artifact is declared in the form manifest, validated against
`contract/v1/grants-gov-xml-profile.schema.json`, checked for complete canonical field
coverage, and included in the reproducible artifact bundle.

Producer preflight also requires every emitted profile's pinned root XSD URI, native version,
root role, SHA-256, and fixture path to match one row in the machine-readable root-fixture
manifest and resolve to exactly one byte-identical conformance fixture. A normalized,
dependency-rewritten, or otherwise derived file cannot satisfy that physical-source gate merely
because it has the same filename or validates the same XML. Fixture sharing is not implicit:
each manifest path and source identity may be claimed by only one profile. The current
reconciliation is recorded in
[`xsd-fixture-reconciliation.md`](xsd-fixture-reconciliation.md).

The initial R&R Budget family proves that one authored payload mapping serves the 5-year,
10-year, and three subaward profiles. Their only differences are declarative wire-contract
metadata.

## Source-identical mapping fragments

Mapping fragments are extracted only when the source XSD establishes the same named type,
namespace, version, element sequence, and leaf types. Similar JSON shape is not sufficient.
The first pass extracts two Global Library V2 structures used by R&R SF-424:

- `globLib:HumanNameDataType`, used by applicant contact, PD/PI, and AOR names; and
- `globLib:AddressDataTypeV3`, used by applicant organization, applicant contact, PD/PI, and
  AOR addresses.

This replaces 47 repeated field-node declarations with 13 declarations and seven local
references, eliminating 34 duplicate field-node definitions while leaving every resolved
profile byte-identical. The existing `att:AttachedFileDataType` fragment remains the shared
attachment-wire declaration for every profile.

Whole contact objects are deliberately not factored. `ContactPersonInfo`,
`OrganizationContactPersonDataType`, and `AORInfoType` have different source types and
requiredness, including different `Title` and `Email` cardinalities. Their similar mapping
shape does not establish semantic equivalence. The Research Budget key-person name is also
left inline for now because that profile does not yet carry the explicit Global Library
namespace annotations used by R&R SF-424; sharing it would change the resolved target rather
than perform a byte-preserving refactor.

Likely future consumers are forms whose pinned XSD imports the exact same Global Library V2
types. Research Budget can consume the human-name fragment after its namespace profile is
reconciled as a separately reviewed semantic change. Contact structures may become reusable
only if a later fragment contract represents their cardinality differences explicitly.

The fragment `evidence.xsd.version` and each form evidence source's `nativeVersion` are the native
versions encoded by their official XSD URIs. A form evidence sidecar records its separate canonical
form version in `block.formVersion`; dependency records do not inherit that value. See
`source-version-provenance.md` for the version and unknown-source rules.

## Boundary

This is a target extension, not a canonical form keyword. TypeSpec and JSON Schema remain
free of Grants.gov XML names. A renderer that does not submit to Grants.gov can ignore the
artifact. A Grants.gov consumer supplies only generic execution capabilities: loading,
canonical-name projection, attachment resolution, XML construction, and XSD validation.
