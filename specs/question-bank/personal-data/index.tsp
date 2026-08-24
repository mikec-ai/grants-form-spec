import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace QuestionBank.PersonalData;

/** Sex vocabulary carried by the active R&R Personal Data 1.2 wire contract. */
enum PersonalDataSex {
  male: "Male",
  female: "Female",
  withheld: "Do Not Wish to Provide",
}

/** Race vocabulary carried by the active R&R Personal Data 1.2 wire contract. */
enum PersonalDataRace {
  americanIndianAlaskaNative: "American Indian or Alaska Native",
  asian: "Asian",
  blackAfricanAmerican: "Black or African American",
  nativeHawaiianPacificIslander: "Native Hawaiian or Other Pacific Islander",
  white: "White",
  withheld: "Do Not Wish to Provide",
}

/** Ethnicity vocabulary carried by the active R&R Personal Data 1.2 wire contract. */
enum PersonalDataEthnicity {
  hispanicLatino: "Hispanic or Latino",
  notHispanicLatino: "Non-Hispanic or Latino",
  withheld: "Do Not Wish to Provide",
}

/** Disability vocabulary carried by the active R&R Personal Data 1.2 wire contract. */
enum PersonalDataDisabilityStatus {
  hearing: "Hearing",
  visual: "Visual",
  mobilityOrthopedic: "Mobility/Orthopedic Impairment",
  other: "Other",
  none: "None",
  withheld: "Do Not Wish to Provide",
}

/** Citizenship vocabulary carried by the active R&R Personal Data 1.2 wire contract. */
enum PersonalDataCitizenship {
  usCitizen: "US Citizen",
  permanentResident: "Permanent Resident",
  otherNonUsCitizen: "Other non-US Citizen",
  withheld: "Do Not Wish to Provide",
}

// This unannotated model is a capture shape, not a semantic question. The two role-qualified
// questions below share it without claiming that a PD/PI and a co-PD/PI are the same person.
model PersonalDataDirectorCapture {
  /** Enter the person's name. First and last name are required. */
  @UI.label("Name")
  @Validation.requiredPaths("firstName", "lastName")
  name: QuestionPersonName;

  /** Select the person's sex, or decline to provide it. */
  @UI.label("Sex")
  @UI.widget(WidgetName.Select)
  sex?: PersonalDataSex;

  /** Select every race category that applies, or decline to provide race. */
  @UI.label("Race (check all that apply)")
  @UI.widget(WidgetName.MultiSelect)
  @maxItems(5)
  race?: PersonalDataRace[];

  /** Select the person's ethnicity, or decline to provide it. */
  @UI.label("Ethnicity")
  @UI.widget(WidgetName.Select)
  ethnicity?: PersonalDataEthnicity;

  /** Select every disability status that applies, select None, or decline to provide it. */
  @UI.label("Disability Status (check all that apply)")
  @UI.widget(WidgetName.MultiSelect)
  @maxItems(4)
  disabilityStatus?: PersonalDataDisabilityStatus[];

  /** Select the person's citizenship status, or decline to provide it. */
  @UI.label("Citizenship")
  @UI.widget(WidgetName.Select)
  citizenship?: PersonalDataCitizenship;
}

/** Voluntary personal data for the application's Project Director/Principal Investigator. */
@Question.meta(#{ id: "personal-data/project-director" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details, TagName.role)
@UI.label("Project Director / Principal Investigator")
model QuestionProjectDirectorPersonalData {
  ...PersonalDataDirectorCapture;
}

/** Voluntary personal data for one Co-Project Director/Co-Principal Investigator. */
@Question.meta(#{ id: "personal-data/co-project-director" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details, TagName.role)
@UI.label("Co-Project Director / Co-Principal Investigator")
model QuestionCoProjectDirectorPersonalData {
  ...PersonalDataDirectorCapture;
}
