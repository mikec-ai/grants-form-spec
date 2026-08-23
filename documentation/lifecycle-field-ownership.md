# Lifecycle, attestation, and control field ownership

Eighteen form-local occurrences require explicit lifecycle roles. Response role is orthogonal to
semantic identity: an externally owned value can still have a source-bound canonical identity. The
identities below are exploratory proposals only; this decision accepts no semantic mapping.

## Disposition

| Occurrences | Response role | Lifecycle owner | Analysis treatment |
| --- | --- | --- | --- |
| R&R `agencyRoutingNumber` in both covers | `systemValue` | Federal awarding agency | Proposed R&R-family canonical identity; exploratory and unpublished |
| Multi-Project `grantsTrackingNumber` | `systemValue` | Grants.gov, with the applicant transcribing a prior identifier | Form-specific canonical identity; exploratory and unpublished |
| SF-424 `stateReceiveDate` and `stateApplicationId`; R&R `stateReceivedDate` and `stateId` in both covers | `systemValue` | State review process, with the applicant able to transmit the assigned values | Proposed shared State-owned identities; exploratory and unpublished |
| Multi-Project `submittedDate` | `applicantInput` | Applicant or authorized representative | Canonical `application/submission-date-entered` question; included only in exploratory metrics until reviewed |
| Multi-Project `aorSignature` and `aorSignedDate` | `attestation` | Authorized organization representative | Visible field occurrences; excluded pending accepted semantic identity |
| SF-424 `certificationAgree`, SF-424 Short `applicationCertification`, and R&R `trustAgree` in both covers | `attestation` | Authorized organization representative | Visible field occurrences; excluded pending accepted semantic identity |
| SF-424 Short `sameAsProjectDirector` | `technicalField` | Form interaction owned by the applicant runtime | Visible field occurrence; excluded |
| SF-424A `confirmation` | `technicalField` | Simpler form-completion workflow | Visible field occurrence; excluded |

The applicant-entry versus lifecycle-owner distinction is intentional. The R&R instructions tell
an applicant to enter an agency-assigned routing identifier, a prior Grants.gov tracking identifier,
and state-assigned values. The person operating the form is the capture actor; the agency, Grants.gov,
or State remains the authority for the value.

The R&R 5.0 and Multi-Project 4.0 XSDs use the same elements for agency routing and State-owned
values. SF-424 uses `StateReceiveDate` and `StateApplicationID`; the R&R sources use
`StateReceivedDate` and `StateID`. Their pinned source definitions identify the same external facts:
the date the State received the application and the identifier assigned by that State. The shared
State identities are therefore explicit proposals rather than conclusions drawn from labels. They
remain unaccepted and cannot enter published similarity.

## Multi-Project signature review

The Multi-Project signature and signed date are not inferred from the standalone R&R cover:

- The Multi-Project 4.0 XSD makes `AOR_Signature` and `AOR_SignedDate` optional.
- Its DAT classifies both controls as applicant-entered fields.
- Its read-only PDF presents blank signature and date boxes and omits the standalone form's
  "Completed on submission to Grants.gov" text.
- The standalone 5.0 instructions instead say to leave the signature blank for Grants.gov
  submission and say the system generates the signed date. Hard-copy submission remains the AOR's
  responsibility.

The Multi-Project occurrences are therefore explicit attestations owned by the AOR. They remain
form-local because reusing the standalone bank blocks would import a contradictory lifecycle
description and `systemValue` default.

## Certification boundary

All four certification controls are attestations. They are not assigned one canonical semantic id
in this change. SF-424 and SF-424 Short currently use booleans, while both R&R covers preserve the
source `Y: Yes` code and have different requiredness. Normalizing that representation requires a
portable answer-shape decision and explicit semantic review. Matching certification prose is
evidence for a future proposed mapping, not acceptance.

## Technical controls

`sameAsProjectDirector` is present in the SF-424 Short XSD and XML. The official 3.0 DAT says that
checking it skips the Primary Contact section and gives rows 8-04 through 8-20 a rule that disables
the corresponding contact fields when the value is `Y`. The field remains a `technicalField`
because it controls interaction rather than asking for submitted information. The current portable
form does not emit that disable behavior, so source parity is explicitly unresolved; the control
must not be described as merely informational.

`confirmation` does not exist in the SF-424A XSD. Simpler requires the constant value `true` only to
mark the form complete. It is therefore a runtime completion control, not an SF-424A question.

## Pinned evidence

- R&R SF-424 5.0 XSD: `f140f32afed9d7efbe30fc8f299542bbbc3121dbc87a79aa351fcf096163d3bc`
- R&R SF-424 5.0 DAT: `532938a75c587bdc8813fd3af625be4338281d0491999fc39aeaaac51b79c9c1`
- R&R SF-424 5.0 instructions: `666647fdeb7d9d69f2d36dedc74f09ff6a9540776f87c5a5c5b0593219736bd1`
- R&R SF-424 5.0 read-only PDF: `592a1faf1cfdac3e350a22c6fbae3b8c6f229b6c7de29ec18273b60c9235dd6b`
- Multi-Project Cover 4.0 XSD: `5d5599068d721e6554fa442df88711f8d9386a5fafc18b01cb1d1becc41f84e7`
- Multi-Project Cover 4.0 DAT: `361e00da500cb092997dadefcac9723cba3be63417a46375d2a5845797beae8e`
- Multi-Project Cover 4.0 read-only PDF: `6aeef5a73890e2b4bfeaa4ece2f1cb2eff3d90c729f9ed1de6fdb5447bb634bb`
- SF-424 4.0 XSD: `21670776cc2751c806b1ec43a59d6296628e219733bc654cf518ede5b9ae0364`
- SF-424 Short 3.0 XSD: `82b0f2a0ddbbcfae4ec7e083188287fb05700e201ade3b2f69684241bf8baabd`
- SF-424 Short 3.0 DAT: `a905f905928a730b10d48d0b77cbb59397edb3ad3c99770391e1e160c3fb06df`
- SF-424A 1.0 XSD: `d5a636733d72c1e4cc9087ffc59b3d10000ee51f80da0dde3150ff91bcad0b5c`

The nine source-bound lifecycle mappings are `proposed`, never `accepted`, and have no reviewer
attribution. They remain unpublished; other mapping states are unchanged. XML profiles, schemas, UI
presentation, and legacy behavior are unchanged by these analytical classifications; the SF-424
Short disable behavior remains an explicit parity gap.
