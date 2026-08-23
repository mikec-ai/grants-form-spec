# Delivery-target runtime identity

The portable form package identifies a form by its stable semantic `id`. `FormMeta` also
records source-facing names, the source form version, agency and OMB metadata, and the
optional legacy Grants.gov FID. None of those fields requires a particular application
runtime.

Runtime identity belongs to the consumer that registers the form. In the
Simpler.Grants.gov adapter, the following values are therefore declared in a versioned,
SGG-owned target record rather than in `FormMeta`:

| Field | Owner | Reason |
|---|---|---|
| form UUID | SGG adapter | SGG generates and uses it as the runtime registry and persistence key. |
| `FormType` value | SGG adapter | It is an enum in the SGG runtime, not a portable form concept. |
| SGG schema version | SGG adapter | It versions the current SGG runtime representation. |
| instruction UUID | SGG registration | It addresses an SGG instruction record and object-store path; forms without an instruction may omit it. |

The legacy Grants.gov FID remains in portable metadata because it identifies the official
source form, not an SGG runtime row. The portable `id` remains the join key between the
artifact package and any target record.

This boundary removes three SGG-specific fields (`formId`, `formType`, and `sggVersion`) from
each canonical form declaration. The compatibility migration covers all 19 emitted forms;
the SGG adapter preserves its five currently opted-in registrations through one generic
loader. A future consumer can assign its own runtime identity without editing the portable
package.

Runtime identity data must not affect schema, presentation, rules, XML mappings, question
composition, or analysis. Adding a form to a target may add a target record, but it must not
add a form-specific compiler or adapter branch.
