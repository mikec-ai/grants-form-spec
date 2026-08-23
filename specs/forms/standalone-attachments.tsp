import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/application/index.tsp";
import "../question-bank/budget/index.tsp";
import "../question-bank/project/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.Application;
using QuestionBank.Budget;
using QuestionBank.Project;

namespace Forms.ProjectNarrativeAttachments {

enum ProjectNarrativeSection {
  projectNarrativeFiles: "1. Project Narrative File(s)",
}

/** Project Narrative Attachment Form (Grants.gov FID 539, v1.2). */
@Form.meta(#{
  id: "project-narrative-attachments",
  legacyFormId: 539,
  formName: "Project Narrative Attachment Form",
  shortFormName: "ProjectNarrativeAttachments_1_2",
  formVersion: "1.2",
  agencyCode: "SGG",
  ombNumber: "",
})
@UI.sections(ProjectNarrativeSection)
model ProjectNarrativeAttachments {
  /** At least one file must be attached */
  @UI.label("Project Narrative Files")
  @UI.section(ProjectNarrativeSection.projectNarrativeFiles)
  @UI.widget(WidgetName.AttachmentArray)
  @minItems(1)
  @maxItems(100)
  attachments: ProjectNarrative[];
}
}

namespace Forms.BudgetNarrativeAttachments {

enum BudgetNarrativeSection {
  budgetNarrativeFiles: "1. Budget Narrative File(s)",
}

/** Budget Narrative Attachment Form (Grants.gov FID 543, v1.2). */
@Form.meta(#{
  id: "budget-narrative-attachments",
  legacyFormId: 543,
  formName: "Budget Narrative Attachment Form",
  shortFormName: "BudgetNarrativeAttachments_1_2",
  formVersion: "1.2",
  agencyCode: "SGG",
  ombNumber: "",
})
@UI.sections(BudgetNarrativeSection)
model BudgetNarrativeAttachments {
  /** At least one file must be attached */
  @UI.label("Budget Narrative Files")
  @UI.section(BudgetNarrativeSection.budgetNarrativeFiles)
  @UI.widget(WidgetName.AttachmentArray)
  @minItems(1)
  @maxItems(100)
  attachments: BudgetNarrative[];
}
}

namespace Forms.OtherNarrativeAttachments {

enum OtherNarrativeSection {
  otherNarrativeFiles: "1. Other Narrative File(s)",
}

/** Other Narrative Attachments (Grants.gov FID 542, v1.2). */
@Form.meta(#{
  id: "other-narrative-attachments",
  legacyFormId: 542,
  formName: "Other Narrative Attachments",
  shortFormName: "OtherNarrativeAttachments",
  formVersion: "1.2",
  agencyCode: "SGG",
  ombNumber: "",
})
@UI.sections(OtherNarrativeSection)
model OtherNarrativeAttachments {
  /** At least one file must be attached */
  @UI.label("Other Narrative Files")
  @UI.section(OtherNarrativeSection.otherNarrativeFiles)
  @UI.widget(WidgetName.AttachmentArray)
  @minItems(1)
  @maxItems(100)
  attachments: OtherNarrative[];
}
}
