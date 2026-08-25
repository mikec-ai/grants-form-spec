#!/usr/bin/env node

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const ledgerSchema = JSON.parse(
  await readFile(resolve(root, "contract/v1/parity-delta-ledger.schema.json"), "utf8"),
);
const decisionSchema = JSON.parse(
  await readFile(resolve(root, "contract/v1/parity-decision-artifact.schema.json"), "utf8"),
);
const receiptSchema = JSON.parse(
  await readFile(resolve(root, "contract/v1/parity-decision-verification.schema.json"), "utf8"),
);
const ledger = JSON.parse(
  await readFile(resolve(root, "parity/legacy-deltas.v1.json"), "utf8"),
);
const receipt = JSON.parse(
  await readFile(resolve(root, ledger.decisionVerification.receipt), "utf8"),
);
const ajv = new Ajv2020({ allErrors: true, strict: true });
addFormats(ajv);
const validateDocument = (schema, document, label) => {
  const validate = ajv.compile(schema);
  if (validate(document)) return;
  const details = (validate.errors ?? [])
    .map((error) => `${error.instancePath || "/"} ${error.message}`)
    .join("; ");
  process.stderr.write(`error: ${label} contract failed: ${details}\n`);
  process.exitCode = 1;
};
validateDocument(ledgerSchema, ledger, "parity delta ledger");
validateDocument(receiptSchema, receipt, "parity decision verification receipt");
for (const entry of receipt.artifacts ?? []) {
  const artifact = JSON.parse(await readFile(resolve(root, entry.path), "utf8"));
  validateDocument(decisionSchema, artifact, `parity decision artifact ${entry.path}`);
}
