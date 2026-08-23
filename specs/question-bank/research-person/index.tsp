import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace QuestionBank.ResearchPerson;

enum ResearchPersonPrefix {
  mr: "Mr.",
  mrs: "Mrs.",
  miss: "Miss",
  ms: "Ms.",
  doctor: "Dr.",
  reverend: "Rev.",
  professor: "Prof.",
}

enum ResearchPersonSuffix {
  junior: "Jr.",
  senior: "Sr.",
  medicalDoctor: "M.D.",
  doctorOfPhilosophy: "Ph.D",
  jurisDoctor: "JD",
}

enum ResearchProjectRole {
  projectDirectorPrincipalInvestigator: "PD/PI",
  coProjectDirectorPrincipalInvestigator: "Co-PD/PI",
  faculty: "Faculty",
  postDoctoral: "Post Doctoral",
  postDoctoralAssociate: "Post Doctoral Associate",
  postDoctoralScholar: "Post Doctoral Scholar",
  otherProfessional: "Other Professional",
  graduateStudent: "Graduate Student",
  undergraduateStudent: "Undergraduate Student",
  technician: "Technician",
  consultant: "Consultant",
  coInvestigator: "Co-Investigator",
  other: "Other (Specify)",
}

/** Enter the research person's name as it appears in official records. */
@Question.meta(#{ id: "research-person/name" })
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.name)
@UI.label("Name")
model QuestionResearchPersonName {
  @UI.label("Prefix")
  prefix?: ResearchPersonPrefix;

  @UI.label("First Name")
  @minLength(1)
  @maxLength(35)
  firstName: string;

  @UI.label("Middle Name")
  @minLength(1)
  @maxLength(25)
  middleName?: string;

  @UI.label("Last Name")
  @minLength(1)
  @maxLength(60)
  lastName: string;

  @UI.label("Suffix")
  suffix?: ResearchPersonSuffix;
}

/** Enter the research person's agency credential or login, when applicable. */
@Question.meta(#{ id: "research-person/credential" })
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.identifier)
@minLength(1)
@maxLength(60)
scalar ResearchPersonCredential extends string;

/** Specify the research person's project role when an Other role is selected. */
@Question.meta(#{ id: "research-person/other-project-role" })
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.role)
@minLength(1)
@maxLength(40)
scalar ResearchPersonOtherProjectRole extends string;

/** Enter the type of degree held by the research person. */
@Question.meta(#{ id: "research-person/degree-type" })
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details)
@minLength(1)
@maxLength(75)
scalar ResearchPersonDegreeType extends string;

/** Enter the year in which the research person's degree was awarded. */
@Question.meta(#{ id: "research-person/degree-year" })
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.date)
@minLength(1)
@maxLength(25)
scalar ResearchPersonDegreeYear extends string;

/** Attach this person's biographical sketch. */
@Question.meta(#{ id: "research-person/biographical-sketch" })
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.attachment)
scalar ResearchPersonBiographicalSketch extends AttachmentRef;

/** Attach this person's current and pending support information. */
@Question.meta(#{ id: "research-person/current-pending-support" })
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.attachment)
scalar ResearchPersonCurrentPendingSupport extends AttachmentRef;

/** Reusable identity, affiliation, contact, role, and credential questions for research staff. */
@Question.meta(#{ id: "research-person/details" })
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details)
model QuestionResearchPersonProfile {
  @UI.label("Name")
  name: QuestionResearchPersonName;

  @UI.label("Position / Title")
  title?: ContactTitle;

  @UI.label("Department")
  @minLength(1)
  @maxLength(100)
  department?: string;

  @UI.label("Organization Name")
  organizationName?: OrganizationName;

  @UI.label("Division")
  @minLength(1)
  @maxLength(100)
  division?: string;

  @UI.label("Address")
  @Validation.requiredPaths("street1", "city", "country")
  @Validation.requiredPathWhen("state", "country", CountryCode.USA)
  @Validation.requiredPathWhen("zipCode", "country", CountryCode.USA)
  address: QuestionAddress;

  @UI.label("Phone Number")
  phone: PhoneNumber;

  @UI.label("Fax Number")
  fax?: PhoneNumber;

  @UI.label("Email")
  email: EmailAddress;

  @UI.label("Credential, e.g., agency login")
  credential?: ResearchPersonCredential;

  @UI.label("Project Role")
  projectRole: ResearchProjectRole;

  @UI.label("Other Project Role Category")
  @Validation.requiredWhen(QuestionResearchPersonProfile.projectRole, ResearchProjectRole.otherProfessional)
  @Validation.requiredWhen(QuestionResearchPersonProfile.projectRole, ResearchProjectRole.other)
  @UI.enabledWhenAny(
    QuestionResearchPersonProfile.projectRole,
    ResearchProjectRole.otherProfessional,
    ResearchProjectRole.other
  )
  otherProjectRole?: ResearchPersonOtherProjectRole;

  @UI.label("Degree Type")
  degreeType?: ResearchPersonDegreeType;

  @UI.label("Degree Year")
  degreeYear?: ResearchPersonDegreeYear;

  @UI.label("Attach Biographical Sketch")
  @UI.widget(WidgetName.Attachment)
  biographicalSketch?: ResearchPersonBiographicalSketch;

  @UI.label("Attach Current & Pending Support")
  @UI.widget(WidgetName.Attachment)
  currentPendingSupport?: ResearchPersonCurrentPendingSupport;
}
