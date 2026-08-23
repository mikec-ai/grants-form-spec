import { describe, expect, it } from "vitest";
import { emitSggRules } from "../src/emitters/rules-sgg.js";
import { allBlocks } from "../src/model.js";
import { Tester, form, formMeta } from "./tester.js";

describe("calculation rule emission", () => {
  it("emits percentage operands and source-aware materialization declaratively", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        ${formMeta("percentage-materialization")}
        model PercentageMaterialization {
          amount?: decimal;
          percentage?: int32;

          @Validation.materializeWhenAnySourcePresent
          @Validation.computed(
            Op.PercentOf,
            PercentageMaterialization.amount,
            PercentageMaterialization.percentage
          )
          total?: decimal;
        }
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "percentage-materialization",
    );
    expect(block).toBeDefined();

    expect(emitSggRules(instance.program, block!)).toEqual({
      total: {
        gg_pre_population: {
          rule: "multiply_by_percentage",
          amount: "amount",
          percentage: "percentage",
          materialize: "when_any_source_present",
          presence_fields: ["amount", "percentage"],
        },
      },
    });
  });
});
