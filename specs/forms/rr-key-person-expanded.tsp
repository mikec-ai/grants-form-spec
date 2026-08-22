import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/research-person/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.ResearchPerson;

namespace Forms.RRKeyPersonExpanded;

enum RRKeyPersonExpandedSection {
  principalInvestigator: "Project Director / Principal Investigator",
  seniorKeyPersons: "Senior / Key Persons",
  overflowAttachments: "Additional Senior / Key Person Attachments",
}

model ResearchPersonAddress extends QuestionAddress {
  @UI.label("State")
  @UI.enabledWhen(ResearchPersonAddress.country, CountryCode.USA)
  @Validation.requiredWhen(ResearchPersonAddress.country, CountryCode.USA)
  state?: StateCode;

  @UI.label("Province")
  @minLength(1)
  @maxLength(30)
  @UI.readOnlyWhen(ResearchPersonAddress.country, CountryCode.USA)
  province?: string;
}

model ResearchPersonProfile extends QuestionResearchPersonProfile {
  @UI.label("Address")
  address: ResearchPersonAddress;
}

model PrincipalInvestigatorProfile extends ResearchPersonProfile {
  @UI.label("Attach Biographical Sketch")
  @UI.widget(WidgetName.Attachment)
  biographicalSketch: ResearchPersonBiographicalSketch;
}

/** Overflow file for additional senior/key person profiles after structured entry capacity is reached. */
@Question.meta(#{
  id: "research-person/additional-profiles-upload",
  classification: BlockClassification.captureMechanism,
})
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.attachment)
scalar AdditionalResearchPersonProfiles extends AttachmentRef;

/** Overflow file for additional biographical sketches after structured entry capacity is reached. */
@Question.meta(#{
  id: "research-person/additional-biographical-sketches-upload",
  classification: BlockClassification.captureMechanism,
})
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.attachment)
scalar AdditionalResearchPersonBiographicalSketches extends AttachmentRef;

/** Overflow file for additional support records after structured entry capacity is reached. */
@Question.meta(#{
  id: "research-person/additional-support-upload",
  classification: BlockClassification.captureMechanism,
})
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.attachment)
scalar AdditionalResearchPersonSupport extends AttachmentRef;

/** Research & Related Senior/Key Person Profile (Expanded), Grants.gov version 4.0. */
@Form.meta(#{
  id: "rr-key-person-expanded",
  formId: "2a638e46-7680-55ba-a11a-4d152f37ca1e",
  legacyFormId: 774,
  formName: "Research & Related Senior/Key Person Profile (Expanded)",
  shortFormName: "RR_KeyPersonExpanded_4_0",
  formVersion: "4.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
  formType: "RRKeyPersonExpanded",
  sggVersion: "1.0",
})
@UI.sections(RRKeyPersonExpandedSection)
model RRKeyPersonExpanded {
  @UI.label("Project Director / Principal Investigator")
  @UI.section(RRKeyPersonExpandedSection.principalInvestigator)
  principalInvestigator: PrincipalInvestigatorProfile;

  @UI.label("Senior / Key Person")
  @UI.section(RRKeyPersonExpandedSection.seniorKeyPersons)
  @maxItems(99)
  seniorKeyPersons?: ResearchPersonProfile[];

  @UI.label("Additional Senior / Key Person Profiles")
  @UI.section(RRKeyPersonExpandedSection.overflowAttachments)
  @UI.widget(WidgetName.Attachment)
  additionalProfiles?: AdditionalResearchPersonProfiles;

  @UI.label("Additional Biographical Sketches")
  @UI.section(RRKeyPersonExpandedSection.overflowAttachments)
  @UI.widget(WidgetName.Attachment)
  additionalBiographicalSketches?: AdditionalResearchPersonBiographicalSketches;

  @UI.label("Additional Current and Pending Support")
  @UI.section(RRKeyPersonExpandedSection.overflowAttachments)
  @UI.widget(WidgetName.Attachment)
  additionalCurrentPendingSupport?: AdditionalResearchPersonSupport;
}
