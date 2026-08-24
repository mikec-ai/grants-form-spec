#!/usr/bin/env node

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const schema = JSON.parse(
  await readFile(resolve(root, "contract/v1/parity-delta-ledger.schema.json"), "utf8"),
);
const ledger = JSON.parse(
  await readFile(resolve(root, "parity/legacy-deltas.v1.json"), "utf8"),
);
const ajv = new Ajv2020({ allErrors: true, strict: true });
addFormats(ajv);
const validate = ajv.compile(schema);
if (!validate(ledger)) {
  const details = (validate.errors ?? [])
    .map((error) => `${error.instancePath || "/"} ${error.message}`)
    .join("; ");
  process.stderr.write(`error: parity delta ledger contract failed: ${details}\n`);
  process.exitCode = 1;
}
