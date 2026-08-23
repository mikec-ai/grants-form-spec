import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/project/index.tsp";
import "../question-bank/research-project/index.tsp";

using SimplerForms;
using QuestionBank.Project;
using QuestionBank.ResearchProject;

namespace Forms.RROtherProjectInformation;

enum RROtherProjectInformationSection {
  humanSubjects: "1. Human Subjects",
  vertebrateAnimals: "2. Vertebrate Animals",
  proprietaryInformation: "3. Proprietary or Privileged Information",
  environmentalImpact: "4. Environmental Impact",
  historicPlaces: "5. Historic Places",
  internationalActivities: "6. International Activities",
  supportingDocuments: "7. Supporting Documents",
}

/** Research & Related Other Project Information, Grants.gov form version 1.4. */
@Form.meta(#{
  id: "rr-other-project-information",
  legacyFormId: 619,
  formName: "Research & Related Other Project Information",
  shortFormName: "RR_OtherProjectInfo_1_4",
  formVersion: "1.4",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
})
@UI.sections(RROtherProjectInformationSection)
model RROtherProjectInformation {
  @UI.label("Human Subjects")
  @UI.section(RROtherProjectInformationSection.humanSubjects)
  humanSubjects: QuestionHumanSubjects;

  @UI.label("Vertebrate Animals")
  @UI.section(RROtherProjectInformationSection.vertebrateAnimals)
  vertebrateAnimals: QuestionVertebrateAnimals;

  @UI.section(RROtherProjectInformationSection.proprietaryInformation)
  @UI.label("Proprietary or Privileged Information")
  proprietaryInformation: QuestionProprietaryInformation;

  @UI.label("Environmental Impact")
  @UI.section(RROtherProjectInformationSection.environmentalImpact)
  environmentalImpact: QuestionEnvironmentalImpact;

  @UI.label("Historic Places")
  @UI.section(RROtherProjectInformationSection.historicPlaces)
  historicPlaces: QuestionHistoricDesignation;

  @UI.label("International Activities")
  @UI.section(RROtherProjectInformationSection.internationalActivities)
  internationalActivities: QuestionInternationalActivities;

  // The DAT makes the summary and narrative required unless the R&R SF-424 submission type is
  // Preapplication. That dependency crosses form boundaries, so these remain optional in this
  // standalone declaration until the portable contract has application-level composition rules.
  @UI.label("Project Summary / Abstract")
  @UI.section(RROtherProjectInformationSection.supportingDocuments)
  @UI.widget(WidgetName.Attachment)
  projectSummaryAbstract?: ProjectSummaryAbstractDocument;

  @UI.label("Project Narrative")
  @UI.section(RROtherProjectInformationSection.supportingDocuments)
  @UI.widget(WidgetName.Attachment)
  projectNarrative?: ProjectNarrative;

  @UI.label("Bibliography & References Cited")
  @UI.section(RROtherProjectInformationSection.supportingDocuments)
  @UI.widget(WidgetName.Attachment)
  bibliographyReferences?: ProjectBibliographyReferences;

  @UI.label("Facilities & Other Resources")
  @UI.section(RROtherProjectInformationSection.supportingDocuments)
  @UI.widget(WidgetName.Attachment)
  facilitiesResources?: ProjectFacilitiesResources;

  @UI.label("Equipment")
  @UI.section(RROtherProjectInformationSection.supportingDocuments)
  @UI.widget(WidgetName.Attachment)
  equipment?: ProjectEquipment;

  @UI.label("Other Attachments")
  @UI.section(RROtherProjectInformationSection.supportingDocuments)
  @UI.widget(WidgetName.AttachmentArray)
  otherAttachments?: ProjectOtherSupportingDocument[];
}
