export { $onEmit } from "./emitter.js";
import * as d from "./decorators.js";

export { $lib } from "./lib.js";
export { $linter } from "./linter.js";
export { $onValidate } from "./validate.js";
export * from "./decorators.js";

export const $decorators = {
  "SimplerForms.Question": { meta: d.$questionMeta },
  "SimplerForms.Form": { meta: d.$formMeta },
  "SimplerForms.Catalog": { tag: d.$tag, entity: d.$entity },
  "SimplerForms.Response": { role: d.$responseRole },
  "SimplerForms.UI": {
    sections: d.$sections,
    section: d.$section,
    overrides: d.$overrides,
    label: d.$label,
    helpText: d.$helpText,
    widget: d.$widget,
    encodedCheckboxGroup: d.$encodedCheckboxGroup,
    order: d.$order,
    omit: d.$omit,
    readOnly: d.$readOnly,
    visibleWhen: d.$visibleWhen,
    enabledWhen: d.$enabledWhen,
    enabledWhenAny: d.$enabledWhenAny,
    enabledWhenCount: d.$enabledWhenCount,
    enabledWhenCountOrPresent: d.$enabledWhenCountOrPresent,
    readOnlyWhen: d.$readOnlyWhen,
  },
  "SimplerForms.Validation": {
    constraints: d.$validationConstraints,
    constraintsWhen: d.$validationConstraintsWhen,
    requiredPaths: d.$requiredPaths,
    requiredPathWhen: d.$requiredPathWhen,
    atLeastOnePathWhenPresent: d.$atLeastOnePathWhenPresent,
    atLeastOneOf: d.$atLeastOneOf,
    requiredWhen: d.$requiredWhen,
    requiredWhenPath: d.$requiredWhenPath,
    notBefore: d.$notBefore,
    computed: d.$computed,
    computedFrom: d.$computedFrom,
    materializeWhenAnySourcePresent: d.$materializeWhenAnySourcePresent,
    evaluationOrder: d.$evaluationOrder,
    totals: d.$totals,
  },
  "SimplerForms.Sgg": {
    prePopulate: d.$prePopulate,
    multiField: d.$multiField,
    fieldList: d.$fieldList,
  },
};
