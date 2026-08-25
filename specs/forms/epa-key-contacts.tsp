import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace Forms.EPAKeyContacts;

/** Fixed EPA contact roles, in official paper-form order. */
enum EPAKeyContactsSection {
  authorizedRepresentative: "Authorized Representative",
  payee: "Payee",
  administrativeContact: "Administrative Contact",
  projectManager: "Project Manager",
}

/**
 * One source-defined EPA contact person.
 *
 * The optional role object carries the DAT's any-field completeness boundary: once a role
 * exists, first and last name, street 1, city, country, and phone are required. Email remains
 * optional even though other shared contact compositions require it.
 */
@UI.label("Contact Person")
@UI.order(
  EPAKeyContactPerson.name,
  EPAKeyContactPerson.title,
  EPAKeyContactPerson.address,
  EPAKeyContactPerson.phone,
  EPAKeyContactPerson.fax,
  EPAKeyContactPerson.email
)
model EPAKeyContactPerson {
  @UI.label("Name")
  @Validation.requiredPaths("firstName", "lastName")
  name: QuestionPersonName;

  @UI.label("Title")
  title?: ContactTitle;

  @UI.label("Complete Address")
  @Validation.requiredPaths("street1", "city", "country")
  @Validation.requiredPathWhen("state", "country", CountryCode.USA)
  @Validation.requiredPathWhen("zipCode", "country", CountryCode.USA)
  address: QuestionAddress;

  @UI.label("Phone Number")
  phone: PhoneNumber;

  @UI.label("Fax Number")
  fax?: PhoneNumber;

  @UI.label("E-mail Address")
  email?: EmailAddress;
}

/** EPA KEY CONTACTS FORM, Grants.gov version 2.0. */
@Form.meta(#{
  id: "epa-key-contacts",
  legacyFormId: 674,
  formName: "EPA KEY CONTACTS FORM",
  shortFormName: "EPA_KeyContacts",
  formVersion: "2.0",
  agencyCode: "SGG",
  ombNumber: "2030-0020",
})
@UI.sections(EPAKeyContactsSection)
// ContactPersonDataTypeV3 permits County and Province, but neither is presented in the
// current official read-only PDF or the existing SGG form. Keep the canonical address shape
// and XML capacity while omitting only these form occurrences from applicant presentation.
@UI.overrides(#{
  `authorizedRepresentative.address.county`: #{ omit: true },
  `authorizedRepresentative.address.province`: #{ omit: true },
  `payee.address.county`: #{ omit: true },
  `payee.address.province`: #{ omit: true },
  `administrativeContact.address.county`: #{ omit: true },
  `administrativeContact.address.province`: #{ omit: true },
  `projectManager.address.county`: #{ omit: true },
  `projectManager.address.province`: #{ omit: true },
})
model EPAKeyContacts {
  /** Original awards and amendments will be sent to this individual for review and acceptance, unless otherwise indicated. */
  @UI.label("Authorized Representative")
  @UI.helpText("Original awards and amendments will be sent to this individual for review and acceptance, unless otherwise indicated.")
  @UI.section(EPAKeyContactsSection.authorizedRepresentative)
  authorizedRepresentative?: EPAKeyContactPerson;

  /** Individual authorized to accept payments. */
  @UI.label("Payee")
  @UI.helpText("Individual authorized to accept payments.")
  @UI.section(EPAKeyContactsSection.payee)
  payee?: EPAKeyContactPerson;

  /** Individual from the Sponsored Programs Office to contact concerning administrative matters. */
  @UI.label("Administrative Contact")
  @UI.helpText("Individual from Sponsored Programs Office to contact concerning administrative matters (i.e., indirect cost rate computation, rebudgeting requests etc).")
  @UI.section(EPAKeyContactsSection.administrativeContact)
  administrativeContact?: EPAKeyContactPerson;

  /** Individual responsible for the technical completion of the proposed work. */
  @UI.label("Project Manager")
  @UI.helpText("Individual responsible for the technical completion of the proposed work.")
  @UI.section(EPAKeyContactsSection.projectManager)
  projectManager?: EPAKeyContactPerson;
}
