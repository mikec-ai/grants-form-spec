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

A mapping node may declare an absolute `source` JSON pointer. This is primarily used inside
`group` nodes when the official XSD introduces structure that applicants never answer as an
object. For example, R&R SF-424 asks for one applicant congressional district while its XML
wraps that value in a `CongressionalDistrict` element. The target profile owns that wrapper;
the canonical form remains a scalar question.

The standard Grants.gov attached-file wire children are data as well. Profiles that map an
`attachment` compose the shared `attached-file-data-1.0.json` declaration, which names
`FileName`, `MimeType`, `FileLocation`, `HashValue`, and their namespaces. Consumers resolve
the attachment reference and mechanically project those declared fields; they do not hardcode
the Grants.gov child vocabulary.

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
