import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace Forms.ProjectNarrativeAttachments {

enum ProjectNarrativeSection {
  projectNarrativeFiles: "1. Project Narrative File(s)",
}

/** Project Narrative Attachment Form (Grants.gov FID 539, v1.2). */
@Form.meta(#{
  id: "project-narrative-attachments",
  formId: "32165da2-354d-42c0-a986-cf4f2f350039",
  legacyFormId: 539,
  formName: "Project Narrative Attachment Form",
  shortFormName: "ProjectNarrativeAttachments_1_2",
  formVersion: "1.2",
  agencyCode: "SGG",
  ombNumber: "",
  formType: "PROJECT_NARRATIVE_ATTACHMENT",
  sggVersion: "1.0",
})
@UI.sections(ProjectNarrativeSection)
model ProjectNarrativeAttachments {
  /** At least one file must be attached */
  @UI.label("Project Narrative Files")
  @UI.section(ProjectNarrativeSection.projectNarrativeFiles)
  @UI.widget(WidgetName.AttachmentArray)
  @minItems(1)
  @maxItems(100)
  attachments: AttachmentRef[];
}
}

namespace Forms.BudgetNarrativeAttachments {

enum BudgetNarrativeSection {
  budgetNarrativeFiles: "1. Budget Narrative File(s)",
}

/** Budget Narrative Attachment Form (Grants.gov FID 543, v1.2). */
@Form.meta(#{
  id: "budget-narrative-attachments",
  formId: "66092260-d3c2-4427-8fd2-bb14e1590aff",
  legacyFormId: 543,
  formName: "Budget Narrative Attachment Form",
  shortFormName: "BudgetNarrativeAttachments_1_2",
  formVersion: "1.2",
  agencyCode: "SGG",
  ombNumber: "",
  formType: "BUDGET_NARRATIVE_ATTACHMENT",
  sggVersion: "1.0",
})
@UI.sections(BudgetNarrativeSection)
model BudgetNarrativeAttachments {
  /** At least one file must be attached */
  @UI.label("Budget Narrative Files")
  @UI.section(BudgetNarrativeSection.budgetNarrativeFiles)
  @UI.widget(WidgetName.AttachmentArray)
  @minItems(1)
  @maxItems(100)
  attachments: AttachmentRef[];
}
}

namespace Forms.OtherNarrativeAttachments {

enum OtherNarrativeSection {
  otherNarrativeFiles: "1. Other Narrative File(s)",
}

/** Other Narrative Attachments (Grants.gov FID 542, v1.2). */
@Form.meta(#{
  id: "other-narrative-attachments",
  formId: "8899954c-2919-4398-96aa-73961179fe16",
  legacyFormId: 542,
  formName: "Other Narrative Attachments",
  shortFormName: "OtherNarrativeAttachments",
  formVersion: "1.2",
  agencyCode: "SGG",
  ombNumber: "",
  formType: "OTHER_NARRATIVE_ATTACHMENT",
  sggVersion: "1.0",
})
@UI.sections(OtherNarrativeSection)
model OtherNarrativeAttachments {
  /** At least one file must be attached */
  @UI.label("Other Narrative Files")
  @UI.section(OtherNarrativeSection.otherNarrativeFiles)
  @UI.widget(WidgetName.AttachmentArray)
  @minItems(1)
  @maxItems(100)
  attachments: AttachmentRef[];
}
}
