import { expectDiagnosticEmpty, expectDiagnostics } from "@typespec/compiler/testing";
import { describe, it } from "vitest";
import { Tester, bank, form, formMeta } from "./tester.js";

/**
 * Each check gets a fixture that must fail and one that must not. A check that cannot fire
 * is worse than no check: it reads as coverage and provides none.
 */
describe("$onValidate", () => {
  describe("calculation-path-unresolved", () => {
    it("rejects a misspelled path across a repeated boundary", async () => {
      const diagnostics = await Tester.diagnose(
        form(`
          /** Money. */
          @Question.meta(#{ id: "budget/money" })
          @Catalog.tag(TagName.money)
          scalar Money extends string;

          model Period { amount?: Money; }
          model Summary {
            @Validation.computedFrom(Op.Sum, "/periods[*].amunt")
            total?: Money;
          }
          enum Section { only: "Only" }
          ${formMeta("path-check")}
          @UI.sections(Section)
          model PathCheck {
            @UI.section(Section.only) periods?: Period[];
            @UI.section(Section.only) summary?: Summary;
          }
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/calculation-path-unresolved",
      });
    });

    it("accepts an existing path across a repeated boundary", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          form(`
            /** Money. */
            @Question.meta(#{ id: "budget/money" })
            @Catalog.tag(TagName.money)
            scalar Money extends string;

            model Period { amount?: Money; }
            model Summary {
              @Validation.computedFrom(Op.Sum, "/periods[*].amount")
              total?: Money;
            }
            enum Section { only: "Only" }
            ${formMeta("path-check")}
            @UI.sections(Section)
            model PathCheck {
              @UI.section(Section.only) periods?: Period[];
              @UI.section(Section.only) summary?: Summary;
            }
          `),
        ),
      );
    });

    it("accepts a parent-scoped path inside a reusable nested composition", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          form(`
            model Period { amount?: string; }
            model Summary {
              @Validation.computedFrom(Op.Sum, "../periods[*].amount")
              total?: string;
            }
            model BudgetDetails {
              periods?: Period[];
              summary?: Summary;
            }
            ${formMeta("nested-budget")}
            model NestedBudget { budgets?: BudgetDetails[]; }
          `),
        ),
      );
    });

    it("rejects a misspelled parent-scoped path", async () => {
      const diagnostics = await Tester.diagnose(
        form(`
          model Period { amount?: string; }
          model Summary {
            @Validation.computedFrom(Op.Sum, "../periods[*].amunt")
            total?: string;
          }
          model BudgetDetails {
            periods?: Period[];
            summary?: Summary;
          }
          ${formMeta("nested-budget")}
          model NestedBudget { budgets?: BudgetDetails[]; }
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/calculation-path-unresolved",
      });
    });
  });

  describe("form-scoped-question-id", () => {
    it("rejects a question named after a form", async () => {
      const diagnostics = await Tester.diagnose(
        bank(`
          /** Named for a form. */
          @Question.meta(#{ id: "sf424/applicant-profile" })
          @Catalog.tag(TagName.name)
          scalar FormScoped extends string;
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/form-scoped-question-id",
      });
    });

    it("accepts a question named for what it means", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          bank(`
            /** The organization's legal name. */
            @Question.meta(#{ id: "primary-org/legal-name" })
            @Catalog.tag(TagName.name)
            scalar LegalName extends string;
          `),
        ),
      );
    });

    it("does not confuse letters inside a semantic word with a form abbreviation", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          bank(`
            /** A narrative supplied by the applicant. */
            @Question.meta(#{ id: "project/narrative" })
            @Catalog.tag(TagName.narrative)
            scalar ProjectNarrative extends string;
          `),
        ),
      );
    });
  });

  describe("duplicate-block-id", () => {
    it("rejects two blocks claiming one id", async () => {
      const diagnostics = await Tester.diagnose(
        bank(`
          /** First. */
          @Question.meta(#{ id: "generics/clash" })
          @Catalog.tag(TagName.name)
          scalar ClashA extends string;

          /** Second. */
          @Question.meta(#{ id: "generics/clash" })
          @Catalog.tag(TagName.name)
          scalar ClashB extends string;
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/duplicate-block-id",
      });
    });

    it("rejects `is`, which copies the base's identity", async () => {
      const diagnostics = await Tester.diagnose(
        bank(`
          /** A point of contact. */
          @Question.meta(#{ id: "poc/details" })
          @Catalog.tag(TagName.person)
          model Poc {
            name: string;
          }

          model FormLocal is Poc {}
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/duplicate-block-id",
      });
    });

    it("accepts `extends`, which carries no identity", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          bank(`
            /** A point of contact. */
            @Question.meta(#{ id: "poc/details" })
            @Catalog.tag(TagName.person)
            model Poc {
              name: string;
            }

            model FormLocal extends Poc {
              role: string;
            }
          `),
        ),
      );
    });
  });

  describe("condition-value-not-in-enum", () => {
    it("rejects a comparison against a value the source cannot hold", async () => {
      const diagnostics = await Tester.diagnose(
        bank(`
          enum Country {
            usa: "USA: UNITED STATES",
          }

          /** An address. */
          @Question.meta(#{ id: "generics/address" })
          @Catalog.tag(TagName.address)
          model Address {
            country: Country;

            @Validation.requiredWhen(Address.country, "USA: UNITED STATE")
            state?: string;
          }
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/condition-value-not-in-enum",
      });
    });

    it("accepts a comparison against a member", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          bank(`
            enum Country {
              usa: "USA: UNITED STATES",
            }

            /** An address. */
            @Question.meta(#{ id: "generics/address" })
            @Catalog.tag(TagName.address)
            model Address {
              country: Country;

              @Validation.requiredWhen(Address.country, Country.usa)
              state?: string;
            }
          `),
        ),
      );
    });
  });

  describe("condition-path-unresolved", () => {
    it("rejects a misspelled nested condition path", async () => {
      const diagnostics = await Tester.diagnose(
        form(`
          enum Section { only: "Only" }
          enum Choice { yes: "Yes", no: "No" }
          model Details { choice: Choice; }

          ${formMeta("nested-condition")}
          @UI.sections(Section)
          model NestedCondition {
            @UI.section(Section.only)
            details: Details;

            @UI.section(Section.only)
            @Validation.requiredWhenPath("details.choce", Choice.yes)
            explanation?: string;
          }
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/condition-path-unresolved",
      });
    });

    it("accepts an existing nested condition path and enum member", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          form(`
            enum Section { only: "Only" }
            enum Choice { yes: "Yes", no: "No" }
            model Details { choice: Choice; }

            ${formMeta("nested-condition")}
            @UI.sections(Section)
            model NestedCondition {
              @UI.section(Section.only)
              details: Details;

              @UI.section(Section.only)
              @Validation.requiredWhenPath("details.choice", Choice.yes)
              explanation?: string;
            }
          `),
        ),
      );
    });
  });

  describe("calculation-cycle", () => {
    it("rejects a calculation that depends on itself", async () => {
      const diagnostics = await Tester.diagnose(
        bank(`
          /** A budget. */
          @Question.meta(#{ id: "budget/cyclic" })
          @Catalog.tag(TagName.money)
          model Cyclic {
            @Validation.computed(Op.Sum, Cyclic.b)
            a?: string;

            @Validation.computed(Op.Sum, Cyclic.a)
            b?: string;
          }
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/calculation-cycle",
      });
    });

    it("accepts a chain", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          bank(`
            /** A budget. */
            @Question.meta(#{ id: "budget/chained" })
            @Catalog.tag(TagName.money)
            model Chained {
              leaf?: string;

              @Validation.computed(Op.Sum, Chained.leaf)
              mid?: string;

              @Validation.computed(Op.Sum, Chained.mid)
              top?: string;
            }
          `),
        ),
      );
    });
  });

  describe("required-but-unreachable", () => {
    it("rejects a field that is always required but only sometimes visible", async () => {
      const diagnostics = await Tester.diagnose(
        form(`
          enum Section { only: "Only" }
          enum Choice { yes: "Yes", no: "No" }

          /** A form. */
          ${formMeta("contradiction")}
          @UI.sections(Section)
          model Contradiction {
            @UI.section(Section.only)
            choice: Choice;

            @UI.section(Section.only)
            @UI.visibleWhen(Contradiction.choice, Choice.yes)
            explanation: string;
          }
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/required-but-unreachable",
      });
    });

    it("accepts the same field made conditionally required", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          form(`
            enum Section { only: "Only" }
            enum Choice { yes: "Yes", no: "No" }

            /** A form. */
            ${formMeta("consistent")}
            @UI.sections(Section)
            model Consistent {
              @UI.section(Section.only)
              choice: Choice;

              @UI.section(Section.only)
              @UI.visibleWhen(Consistent.choice, Choice.yes)
              @Validation.requiredWhen(Consistent.choice, Choice.yes)
              explanation?: string;
            }
          `),
        ),
      );
    });
  });

  describe("section-orphan", () => {
    it("rejects a field in no section", async () => {
      const diagnostics = await Tester.diagnose(
        form(`
          enum Section { only: "Only" }

          /** A form. */
          ${formMeta("orphan")}
          @UI.sections(Section)
          model Orphan {
            @UI.section(Section.only)
            placed: string;

            unplaced: string;
          }
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/section-orphan",
      });
    });

    it("accepts a field deliberately omitted from the UI", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          form(`
            enum Section { only: "Only" }

            /** A form. */
            ${formMeta("omitted")}
            @UI.sections(Section)
            model Omitted {
              @UI.section(Section.only)
              placed: string;

              @UI.omit
              hidden?: string;
            }
          `),
        ),
      );
    });
  });

  describe("override-path-unresolved", () => {
    it("rejects an override addressing a property that does not exist", async () => {
      const diagnostics = await Tester.diagnose(
        form(`
          enum Section { only: "Only" }

          /** An address. */
          @Question.meta(#{ id: "generics/address" })
          @Catalog.tag(TagName.address)
          model Address {
            city: string;
          }

          /** A form. */
          ${formMeta("typo")}
          @UI.sections(Section)
          @UI.overrides(#{ \`applicant.citty\`: #{ omit: true } })
          model Typo {
            @UI.section(Section.only)
            applicant: Address;
          }
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/override-path-unresolved",
      });
    });

    it("accepts an override that resolves", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          form(`
            enum Section { only: "Only" }

            /** An address. */
            @Question.meta(#{ id: "generics/address" })
            @Catalog.tag(TagName.address)
            model Address {
              city: string;
            }

            /** A form. */
            ${formMeta("resolves")}
            @UI.sections(Section)
            @UI.overrides(#{ \`applicant.city\`: #{ omit: true } })
            model Resolves {
              @UI.section(Section.only)
              applicant: Address;
            }
          `),
        ),
      );
    });
  });

  describe("sgg-outside-forms", () => {
    it("rejects a target vocabulary inside the bank", async () => {
      const diagnostics = await Tester.diagnose(
        bank(`
          /** Leaky. */
          @Question.meta(#{ id: "primary-org/uei" })
          @Catalog.tag(TagName.identifier)
          @Sgg.prePopulate(#{ \`uei\`: SggPrePop.uei })
          model Leaky {
            uei?: string;
          }
        `),
      );
      expectDiagnostics(diagnostics, {
        code: "@simpler-grants/form-spec/sgg-outside-forms",
      });
    });

    it("accepts it on a form", async () => {
      expectDiagnosticEmpty(
        await Tester.diagnose(
          form(`
            enum Section { only: "Only" }

            /** A form. */
            ${formMeta("prepopulated")}
            @UI.sections(Section)
            @Sgg.prePopulate(#{ \`samUei\`: SggPrePop.uei })
            model Prepopulated {
              @UI.section(Section.only)
              samUei?: string;
            }
          `),
        ),
      );
    });
  });
});
