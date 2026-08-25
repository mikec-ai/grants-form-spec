const PROJECTION_MEMBERS = new Set(["$ref", "$rename", "$overlay", "$moveAfter"]);

export function validateProjectionSiblings(projection, from) {
  const unexpected = Object.keys(projection).filter(
    (member) => !PROJECTION_MEMBERS.has(member),
  );
  if (unexpected.length > 0) {
    throw new Error(`${from}: $ref has unsupported sibling ${unexpected[0]}`);
  }
}

export function applyObjectProjection(targetValue, projection, from) {
  validateProjectionSiblings(projection, from);
  if (!targetValue || Array.isArray(targetValue) || typeof targetValue !== "object") {
    throw new Error(
      `${from}: $rename, $overlay, and $moveAfter require an object reference target`,
    );
  }

  const renames = projection.$rename ?? {};
  if (!renames || Array.isArray(renames) || typeof renames !== "object") {
    throw new Error(`${from}: $rename must be an object`);
  }
  const destinations = new Set(Object.values(renames));
  if (
    Object.values(renames).some((member) => typeof member !== "string" || !member) ||
    destinations.size !== Object.keys(renames).length
  ) {
    throw new Error(`${from}: $rename destinations must be unique non-empty strings`);
  }
  for (const [member, replacement] of Object.entries(renames)) {
    if (!(member in targetValue)) {
      throw new Error(`${from}: $rename source ${member} is absent`);
    }
    if (replacement in targetValue && !(replacement in renames)) {
      throw new Error(`${from}: $rename destination ${replacement} already exists`);
    }
  }
  const resolved = Object.fromEntries(
    Object.entries(targetValue).map(([member, child]) => [renames[member] ?? member, child]),
  );

  const overlay = projection.$overlay ?? {};
  if (!overlay || Array.isArray(overlay) || typeof overlay !== "object") {
    throw new Error(`${from}: $overlay must be an object`);
  }
  for (const [member, replacement] of Object.entries(overlay)) {
    if (replacement === null) delete resolved[member];
    else resolved[member] = replacement;
  }

  const moves = projection.$moveAfter ?? {};
  if (!moves || Array.isArray(moves) || typeof moves !== "object") {
    throw new Error(`${from}: $moveAfter must be an object`);
  }
  let ordered = resolved;
  for (const [member, anchor] of Object.entries(moves)) {
    if (typeof anchor !== "string" || !anchor) {
      throw new Error(`${from}: $moveAfter anchors must be non-empty strings`);
    }
    if (member === anchor) {
      throw new Error(`${from}: $moveAfter cannot place ${member} after itself`);
    }
    if (!(member in ordered)) {
      throw new Error(`${from}: $moveAfter member ${member} is absent`);
    }
    if (!(anchor in ordered)) {
      throw new Error(`${from}: $moveAfter anchor ${anchor} is absent`);
    }
    const child = ordered[member];
    const entries = Object.entries(ordered).filter(([name]) => name !== member);
    const anchorIndex = entries.findIndex(([name]) => name === anchor);
    entries.splice(anchorIndex + 1, 0, [member, child]);
    ordered = Object.fromEntries(entries);
  }
  return ordered;
}
