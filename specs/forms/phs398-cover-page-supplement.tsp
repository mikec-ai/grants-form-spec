import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/phs398-cover-page-supplement/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.ResearchApplication;
using QuestionBank.PHS398CoverPageSupplement;

namespace Forms.PHS398CoverPageSupplement;

enum PHS398CoverPageSupplementSection {
  vertebrateAnimals: "1. Vertebrate Animals",
  programIncome: "2. Program Income",
  stemCells: "3. Human Embryonic Stem Cells",
  fetalTissue: "4. Human Fetal Tissue",
  inventions: "5. Inventions and Patents",
  changes: "6. Change of Investigator / Change of Recipient Organization",
}

/** PHS 398 Cover Page Supplement, Grants.gov FID 698, version 5.0. */
@Form.meta(#{
  id: "phs398-cover-page-supplement",
  legacyFormId: 698,
  formName: "PHS 398 Cover Page Supplement",
  shortFormName: "PHS398_CoverPageSupplement_5_0",
  formVersion: "5.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0925-0001",
})
@UI.sections(PHS398CoverPageSupplementSection)
@UI.overrides(#{
  `formerProjectDirector.prefix`: #{
    enabledWhen: #{ path: "changes.changeOfProjectDirector", equals: YesNoCode.yes }
  },
  `formerProjectDirector.firstName`: #{
    enabledWhen: #{ path: "changes.changeOfProjectDirector", equals: YesNoCode.yes }
  },
  `formerProjectDirector.middleName`: #{
    enabledWhen: #{ path: "changes.changeOfProjectDirector", equals: YesNoCode.yes }
  },
  `formerProjectDirector.lastName`: #{
    enabledWhen: #{ path: "changes.changeOfProjectDirector", equals: YesNoCode.yes }
  },
  `formerProjectDirector.suffix`: #{
    enabledWhen: #{ path: "changes.changeOfProjectDirector", equals: YesNoCode.yes }
  },
  formerOrganizationName: #{
    enabledWhen: #{ path: "changes.changeOfRecipientOrganization", equals: YesNoCode.yes }
  },
})
model PHS398CoverPageSupplement {
  // Applicability depends on the R&R Other Project Information vertebrate-animal answer.
  // That cross-form predicate remains source-bound evidence rather than a fabricated local field.
  @UI.section(PHS398CoverPageSupplementSection.vertebrateAnimals)
  vertebrateAnimals?: QuestionVertebrateAnimalEuthanasia;

  @UI.section(PHS398CoverPageSupplementSection.programIncome)
  programIncome: QuestionProgramIncome;

  @UI.section(PHS398CoverPageSupplementSection.stemCells)
  humanEmbryonicStemCells: QuestionHumanEmbryonicStemCells;

  @UI.section(PHS398CoverPageSupplementSection.fetalTissue)
  humanFetalTissue: QuestionHumanFetalTissue;

  // Renewal/resubmission applicability is a cross-form application lifecycle predicate.
  @UI.section(PHS398CoverPageSupplementSection.inventions)
  inventionsAndPatents?: QuestionInventionsAndPatents;

  @UI.section(PHS398CoverPageSupplementSection.changes)
  changes?: QuestionInvestigatorOrganizationChange;

  @UI.label("Name of former Project Director/Principal Investigator")
  @UI.section(PHS398CoverPageSupplementSection.changes)
  @Validation.requiredWhenPath("changes.changeOfProjectDirector", YesNoCode.yes)
  @Validation.requiredPaths("firstName", "lastName")
  formerProjectDirector?: QuestionFormerProjectDirectorPrincipalInvestigator;

  @UI.label("Name of former organization")
  @UI.section(PHS398CoverPageSupplementSection.changes)
  @Validation.requiredWhenPath("changes.changeOfRecipientOrganization", YesNoCode.yes)
  formerOrganizationName?: QuestionFormerRecipientOrganizationName;
}
