import assert from "node:assert/strict";
import test from "node:test";

import {
  applyObjectProjection,
  validateProjectionSiblings,
} from "../scripts/lib/project_xml_projection.mjs";

const source = { first: { value: 1 }, second: { value: 2 }, third: { value: 3 } };

test("rename and overlay compose without mutating the referenced object", () => {
  const result = applyObjectProjection(
    source,
    {
      $ref: "fixture.json#/fields",
      $rename: { first: "renamed" },
      $overlay: { renamed: { value: 10 }, second: null, added: { value: 4 } },
    },
    "profile.json",
  );
  assert.deepEqual(result, {
    renamed: { value: 10 },
    third: { value: 3 },
    added: { value: 4 },
  });
  assert.deepEqual(source, {
    first: { value: 1 },
    second: { value: 2 },
    third: { value: 3 },
  });
});

test("rename rejects an absent source", () => {
  assert.throws(
    () => applyObjectProjection(source, { $ref: "x", $rename: { missing: "new" } }, "p"),
    /rename source missing is absent/,
  );
});

test("rename rejects a collision", () => {
  assert.throws(
    () => applyObjectProjection(source, { $ref: "x", $rename: { first: "second" } }, "p"),
    /rename destination second already exists/,
  );
});

test("rename rejects duplicate and empty destinations", () => {
  assert.throws(
    () => applyObjectProjection(source, { $ref: "x", $rename: { first: "x", second: "x" } }, "p"),
    /unique non-empty strings/,
  );
  assert.throws(
    () => applyObjectProjection(source, { $ref: "x", $rename: { first: "" } }, "p"),
    /unique non-empty strings/,
  );
});

test("projection rejects unsupported siblings", () => {
  assert.throws(
    () => validateProjectionSiblings({ $ref: "x", typo: true }, "p"),
    /unsupported sibling typo/,
  );
});

test("projection operators reject non-object targets", () => {
  for (const target of [null, [], "value"]) {
    assert.throws(
      () => applyObjectProjection(target, { $ref: "x", $overlay: {} }, "p"),
      /require an object reference target/,
    );
  }
});

test("moveAfter preserves all members while applying sequential order constraints", () => {
  const result = applyObjectProjection(
    source,
    {
      $ref: "x",
      $moveAfter: { first: "third", second: "first" },
    },
    "p",
  );
  assert.deepEqual(Object.keys(result), ["third", "first", "second"]);
  assert.deepEqual(result, {
    third: { value: 3 },
    first: { value: 1 },
    second: { value: 2 },
  });
});

test("moveAfter rejects invalid members and anchors", () => {
  assert.throws(
    () => applyObjectProjection(source, { $ref: "x", $moveAfter: { missing: "first" } }, "p"),
    /member missing is absent/,
  );
  assert.throws(
    () => applyObjectProjection(source, { $ref: "x", $moveAfter: { first: "missing" } }, "p"),
    /anchor missing is absent/,
  );
  assert.throws(
    () => applyObjectProjection(source, { $ref: "x", $moveAfter: { first: "first" } }, "p"),
    /cannot place first after itself/,
  );
  assert.throws(
    () => applyObjectProjection(source, { $ref: "x", $moveAfter: { first: "" } }, "p"),
    /anchors must be non-empty strings/,
  );
});
