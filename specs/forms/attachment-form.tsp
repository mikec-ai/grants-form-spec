import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace Forms.AttachmentForm;

enum AttachmentFormSection {
  /** Instructions: On this form, you will attach the various files that make up your grant application. Please consult with the appropriate Agency Guidelines for more information about each needed file. Please remember that any files you attach must be in the document format and named as specified in the Guidelines. */
  instructions: "",
  /** Important: Please attach your files in the proper sequence. See the appropriate Agency Guidelines for details. */
  important: "",
  attachment1: "1) Attachment 1",
  attachment2: "2) Attachment 2",
  attachment3: "3) Attachment 3",
  attachment4: "4) Attachment 4",
  attachment5: "5) Attachment 5",
  attachment6: "6) Attachment 6",
  attachment7: "7) Attachment 7",
  attachment8: "8) Attachment 8",
  attachment9: "9) Attachment 9",
  attachment10: "10) Attachment 10",
  attachment11: "11) Attachment 11",
  attachment12: "12) Attachment 12",
  attachment13: "13) Attachment 13",
  attachment14: "14) Attachment 14",
  attachment15: "15) Attachment 15",
}

/** Attachment Form, Grants.gov FID 540, version 1.2. */
@Form.meta(#{
  id: "attachment-form",
  legacyFormId: 540,
  formName: "Attachment Form",
  shortFormName: "AttachmentForm_1_2",
  formVersion: "1.2",
  agencyCode: "SGG",
  ombNumber: "",
})
@UI.sections(AttachmentFormSection)
model AttachmentForm {
  /** First attachment file */
  @UI.label("Attachment 1")
  @UI.section(AttachmentFormSection.attachment1)
  @UI.widget(WidgetName.Attachment)
  att1?: OrderedAttachmentSlot;

  /** Second attachment file */
  @UI.label("Attachment 2")
  @UI.section(AttachmentFormSection.attachment2)
  @UI.widget(WidgetName.Attachment)
  att2?: OrderedAttachmentSlot;

  /** Third attachment file */
  @UI.label("Attachment 3")
  @UI.section(AttachmentFormSection.attachment3)
  @UI.widget(WidgetName.Attachment)
  att3?: OrderedAttachmentSlot;

  /** Fourth attachment file */
  @UI.label("Attachment 4")
  @UI.section(AttachmentFormSection.attachment4)
  @UI.widget(WidgetName.Attachment)
  att4?: OrderedAttachmentSlot;

  /** Fifth attachment file */
  @UI.label("Attachment 5")
  @UI.section(AttachmentFormSection.attachment5)
  @UI.widget(WidgetName.Attachment)
  att5?: OrderedAttachmentSlot;

  /** Sixth attachment file */
  @UI.label("Attachment 6")
  @UI.section(AttachmentFormSection.attachment6)
  @UI.widget(WidgetName.Attachment)
  att6?: OrderedAttachmentSlot;

  /** Seventh attachment file */
  @UI.label("Attachment 7")
  @UI.section(AttachmentFormSection.attachment7)
  @UI.widget(WidgetName.Attachment)
  att7?: OrderedAttachmentSlot;

  /** Eighth attachment file */
  @UI.label("Attachment 8")
  @UI.section(AttachmentFormSection.attachment8)
  @UI.widget(WidgetName.Attachment)
  att8?: OrderedAttachmentSlot;

  /** Ninth attachment file */
  @UI.label("Attachment 9")
  @UI.section(AttachmentFormSection.attachment9)
  @UI.widget(WidgetName.Attachment)
  att9?: OrderedAttachmentSlot;

  /** Tenth attachment file */
  @UI.label("Attachment 10")
  @UI.section(AttachmentFormSection.attachment10)
  @UI.widget(WidgetName.Attachment)
  att10?: OrderedAttachmentSlot;

  /** Eleventh attachment file */
  @UI.label("Attachment 11")
  @UI.section(AttachmentFormSection.attachment11)
  @UI.widget(WidgetName.Attachment)
  att11?: OrderedAttachmentSlot;

  /** Twelfth attachment file */
  @UI.label("Attachment 12")
  @UI.section(AttachmentFormSection.attachment12)
  @UI.widget(WidgetName.Attachment)
  att12?: OrderedAttachmentSlot;

  /** Thirteenth attachment file */
  @UI.label("Attachment 13")
  @UI.section(AttachmentFormSection.attachment13)
  @UI.widget(WidgetName.Attachment)
  att13?: OrderedAttachmentSlot;

  /** Fourteenth attachment file */
  @UI.label("Attachment 14")
  @UI.section(AttachmentFormSection.attachment14)
  @UI.widget(WidgetName.Attachment)
  att14?: OrderedAttachmentSlot;

  /** Fifteenth attachment file */
  @UI.label("Attachment 15")
  @UI.section(AttachmentFormSection.attachment15)
  @UI.widget(WidgetName.Attachment)
  att15?: OrderedAttachmentSlot;
}
