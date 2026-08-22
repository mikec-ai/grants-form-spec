import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace QuestionBank.Project;

/** Provide the project narrative requested by the funding opportunity. */
@Question.meta(#{ id: "project/narrative" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
@UI.label("Project Narrative")
scalar ProjectNarrative extends AttachmentRef;

/** Provide the geographic areas affected by the proposed project. */
@Question.meta(#{ id: "project/areas-affected" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.attachment)
scalar ProjectAreasAffected extends AttachmentRef;

/** Provide additional project titles when the application needs more than one. */
@Question.meta(#{ id: "project/additional-titles" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.title, TagName.attachment)
scalar AdditionalProjectTitle extends AttachmentRef;

/** Provide additional congressional districts affected by the proposed project. */
@Question.meta(#{ id: "project/additional-congressional-districts" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.identifier, TagName.attachment)
scalar AdditionalCongressionalDistricts extends AttachmentRef;

/** Enter a brief, descriptive title of the project. */
@Question.meta(#{ id: "project/title" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.title)
@UI.label("Project Title")
@minLength(1)
scalar ProjectTitle extends string;

/**
 * Summarize the proposed project in plain language suitable for public release. Do not include
 * personally identifiable, sensitive, or proprietary information.
 */
@Question.meta(#{ id: "project/abstract" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative)
@UI.label("Project Abstract")
@minLength(1)
@maxLength(4000)
scalar ProjectAbstract extends string;

/**
 * A congressional district, as a two-character state abbreviation and a three-character
 * district number: `CA-005`.
 */
@Question.meta(#{ id: "project/congressional-district" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.identifier)
@minLength(1)
@maxLength(6)
scalar CongressionalDistrict extends string;

/** Enter the date in the format MM/DD/YYYY. */
@Question.meta(#{ id: "project/start-date" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.date)
@UI.label("Project Start Date")
scalar ProjectStartDate extends plainDate;

/** Enter the date in the format MM/DD/YYYY. */
@Question.meta(#{ id: "project/end-date" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.date)
@UI.label("Project End Date")
scalar ProjectEndDate extends plainDate;
