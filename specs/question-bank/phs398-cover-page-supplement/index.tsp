import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";
import "../research-application/index.tsp";
import "../research-budget/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.ResearchApplication;
using QuestionBank.ResearchBudget;

/** Policy-specific questions introduced by the PHS 398 Cover Page Supplement. */
namespace QuestionBank.PHS398CoverPageSupplement;

/** Describe vertebrate-animal euthanasia and any departure from AVMA guidance. */
@Question.meta(#{ id: "hhs-research-policy/vertebrate-animal-euthanasia" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
@UI.label("Vertebrate animal euthanasia")
model QuestionVertebrateAnimalEuthanasia {
  @UI.label("Are vertebrate animals euthanized?")
  animalEuthanized?: YesNoCode;

  @UI.label("Is the method consistent with AVMA guidelines?")
  @UI.enabledWhen(QuestionVertebrateAnimalEuthanasia.animalEuthanized, YesNoCode.yes)
  @Validation.requiredWhen(QuestionVertebrateAnimalEuthanasia.animalEuthanized, YesNoCode.yes)
  avmaConsistent?: YesNoCode;

  @UI.label("Describe the euthanasia method and provide scientific justification")
  @UI.widget(WidgetName.TextArea)
  @maxLength(1000)
  @UI.enabledWhen(QuestionVertebrateAnimalEuthanasia.avmaConsistent, YesNoCode.no)
  @Validation.requiredWhen(QuestionVertebrateAnimalEuthanasia.avmaConsistent, YesNoCode.no)
  methodDescription?: string;
}

/** One period and source of anticipated program income. */
model ProgramIncomePeriod {
  @UI.label("Budget Period")
  @minValue(1)
  @maxValue(10)
  budgetPeriod: int32;

  @UI.label("Anticipated Amount ($)")
  anticipatedAmount: ResearchBudgetAmount14;

  @UI.label("Source(s)")
  @minLength(1)
  @maxLength(150)
  source: string;
}

/** Report whether program income is anticipated and provide its period detail. */
@Question.meta(#{ id: "hhs-research-policy/program-income" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Program income")
model QuestionProgramIncome {
  @UI.label("Is program income anticipated during the requested support periods?")
  anticipated: YesNoCode;

  @UI.label("Program income by budget period")
  @minItems(1)
  @maxItems(10)
  periods?: ProgramIncomePeriod[];
}

/** A four-digit registration number from the NIH human embryonic stem-cell registry. */
@pattern("^[0-9]{4}$")
@minLength(4)
@maxLength(4)
scalar HumanEmbryonicStemCellLine extends string;

/** Report use of human embryonic stem cells and the known registry lines. */
@Question.meta(#{ id: "hhs-research-policy/human-embryonic-stem-cells" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
@UI.label("Human embryonic stem cells")
model QuestionHumanEmbryonicStemCells {
  @UI.label("Does the proposed project involve human embryonic stem cells?")
  involved: YesNoCode;

  @UI.label("A specific stem cell line cannot be referenced at this time")
  @UI.enabledWhen(QuestionHumanEmbryonicStemCells.involved, YesNoCode.yes)
  specificLineUnavailable?: YesNoCode;

  @UI.label("Cell Line(s)")
  @maxItems(200)
  @UI.enabledWhen(QuestionHumanEmbryonicStemCells.involved, YesNoCode.yes)
  cellLines?: HumanEmbryonicStemCellLine[];
}

/** Attach the signed assurance required for research involving qualifying human fetal tissue. */
@Question.meta(#{ id: "hhs-research-policy/human-fetal-tissue-compliance-assurance" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.attachment)
scalar HumanFetalTissueComplianceAssurance extends AttachmentRef;

/** Attach the blank sample IRB consent form required for qualifying human fetal tissue research. */
@Question.meta(#{ id: "hhs-research-policy/human-fetal-tissue-irb-consent" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.attachment)
scalar HumanFetalTissueIrbConsent extends AttachmentRef;

/** Report human fetal tissue use and provide each distinct policy document. */
@Question.meta(#{ id: "hhs-research-policy/human-fetal-tissue" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
@UI.label("Human fetal tissue")
model QuestionHumanFetalTissue {
  @UI.label("Does the proposed project involve human fetal tissue from elective abortions?")
  involved: YesNoCode;

  @UI.label("HFT Compliance Assurance")
  @UI.widget(WidgetName.Attachment)
  @UI.enabledWhen(QuestionHumanFetalTissue.involved, YesNoCode.yes)
  @Validation.requiredWhen(QuestionHumanFetalTissue.involved, YesNoCode.yes)
  complianceAssurance?: HumanFetalTissueComplianceAssurance;

  @UI.label("HFT Sample IRB Consent Form")
  @UI.widget(WidgetName.Attachment)
  @UI.enabledWhen(QuestionHumanFetalTissue.involved, YesNoCode.yes)
  @Validation.requiredWhen(QuestionHumanFetalTissue.involved, YesNoCode.yes)
  irbConsentForm?: HumanFetalTissueIrbConsent;
}

/** Report inventions from the prior support period and whether they were reported. */
@Question.meta(#{ id: "hhs-research-policy/inventions-and-patents" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
@UI.label("Inventions and patents")
model QuestionInventionsAndPatents {
  @UI.label("Were inventions conceived or first reduced to practice?")
  inventions?: YesNoCode;

  @UI.label("Previously Reported")
  @UI.enabledWhen(QuestionInventionsAndPatents.inventions, YesNoCode.yes)
  @Validation.requiredWhen(QuestionInventionsAndPatents.inventions, YesNoCode.yes)
  previouslyReported?: YesNoCode;
}

/** Report whether the application changes its PD/PI or recipient organization. */
@Question.meta(#{ id: "hhs-research-policy/investigator-organization-change" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.person, TagName.organization)
@UI.label("Change of investigator or recipient organization")
model QuestionInvestigatorOrganizationChange {
  @UI.label("Change of Project Director/Principal Investigator")
  changeOfProjectDirector?: YesNoCode;

  @UI.label("Change of Recipient Organization")
  changeOfRecipientOrganization?: YesNoCode;
}

/** Identify the former PD/PI named by a change-of-investigator application. */
@Question.meta(#{ id: "hhs-research-policy/former-project-director-principal-investigator" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person)
@UI.label("Name of former Project Director/Principal Investigator")
model QuestionFormerProjectDirectorPrincipalInvestigator {
  ...QuestionPersonName;
}

/** Identify the former recipient organization named by a change-of-organization application. */
@Question.meta(#{ id: "hhs-research-policy/former-recipient-organization-name" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization)
@UI.label("Name of former organization")
scalar QuestionFormerRecipientOrganizationName extends OrganizationName;
