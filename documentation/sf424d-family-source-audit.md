# SF-424D family official-source audit

This audit pins the three active Grants.gov SF-424D version 1.1 profiles before they are
implemented over the shared policy and attestation foundation. It is research evidence, not a
production form contract or a semantic-review approval.

## Profiles checked

| Profile | FID | Current status | XSD namespace | Title and organization ownership |
| --- | ---: | --- | --- | --- |
| SF-424D | 238 | Active | `http://apply.grants.gov/forms/SF424D-V1.1` | Prefilled |
| Individual SF-424D | 522 | Active | `http://apply.grants.gov/forms/Individual_SF424D-V1.1` | Applicant input |
| Mandatory SF-424D | 329 | Active | `http://apply.grants.gov/forms/Mandatory_SF424D-V1.1` | Prefilled |

The status checks were performed against each official Grants.gov Form Items Description page on
2026-08-23. The exact artifact URLs and SHA-256 digests are recorded in
`research/sf424d-family/official-source-audit.json`.

## Shared kernel

All three official DAT workbooks contain the same twenty construction assurances. The canonical
JSON array of assurance text has SHA-256
`89c82c4e717dab69a9a751259e9148b97d6b092e88d1a57e8537953c5ee1c4be` for each profile. These
assurances belong in one separately versioned policy bundle; they are not ordinary question-bank
questions and do not appear in the XML payload.

The response surface is also shared: platform signature, representative title, applicant
organization name, and platform submission date. The DAT workbooks mark all four required. The
signature and date are generated at submission. The official instructions establish that title and
organization are prefilled for base and Mandatory but entered by the applicant for Individual.

## Profile differences

Individual and Mandatory have the same XML structure after namespace substitution. Both use a
local fixed `FormVersion="1.1"` root attribute. The base profile instead requires a
`glob:FormVersionIdentifier` child and a namespaced fixed `glob:coreSchemaVersion="1.1"`
attribute. Each profile also has its own target namespace and prefix. Those facts must remain
declarative profile data rather than adapter branches.

The Individual presentation labels the organization value `Applicant Name`; base and Mandatory
use `Applicant Organization`. These labels do not change the underlying organization-name
semantics.

## Provenance note

The prior research repository is pinned at
`4312f6504b060e2b9ffdbd2307fc41130c3123a0`. Its cached DAT files match fresh downloads from the
official URLs byte for byte. The policy text in the staged JSON was independently checked against
the official read-only PDFs and current Form Items Description data.
