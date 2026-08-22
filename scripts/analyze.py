#!/usr/bin/env python3
"""The three tables: what the bank holds, which forms ask what, and how forms overlap.

Reads the emitted artifacts, never the specs. That is the point of the contract: this
script would work identically against artifacts produced by a form builder, and it is the
read model a question browser would use.

A form composes a question directly or through another question -- Key Contacts reaches
`generics/person-name` through `poc/details` -- and it asks for a person's name either
way, so the tables count the transitive closure. The direct count is reported alongside,
because the difference is what says how much of the bank is built out of the rest of it.

Usage (from the repo root):
    python3 scripts/analyze.py [--json]
"""

from __future__ import annotations

import argparse
import itertools
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DIST = REPO / "dist"


def blocks(kind: str) -> dict[str, dict]:
    root = DIST / kind
    return {
        str(path.parent.relative_to(root)): json.loads(path.read_text())
        for path in sorted(root.rglob("schema.json"))
    }


def refs(node: object) -> set[str]:
    """Every bank question a schema references, by id."""
    found: set[str] = set()
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str) and "question-bank/" in value:
                found.add(value.split("question-bank/", 1)[1].removesuffix("/schema.json"))
            else:
                found |= refs(value)
    elif isinstance(node, list):
        for item in node:
            found |= refs(item)
    return found


def bank_ref(value: str) -> str | None:
    """Return the bank block id addressed by a published artifact reference."""
    if "question-bank/" not in value:
        return None
    return value.split("question-bank/", 1)[1].removesuffix("/schema.json")


def form_local_leaves(schema: dict, defs: dict) -> set[str]:
    """Field names a form declares itself rather than composing from the bank.

    A field two forms both declare themselves is a question waiting to be named: the same
    thing asked twice, with the labels and limits kept in step by hand. That number should
    stay at zero, which is what makes the bank worth having rather than merely present.
    """
    out: set[str] = set()

    def walk(node: object, path: tuple[str, ...]) -> bool:
        """True when this subtree reaches the bank; collects the leaves that do not."""
        if not isinstance(node, dict):
            return False
        ref = node.get("$ref")
        if isinstance(ref, str):
            if "question-bank/" in ref:
                return True
            if ref.startswith("#/$defs/"):
                return walk(defs.get(ref.removeprefix("#/$defs/"), {}), path)
        banked = any(
            walk(branch, path)
            for branch in node.get("allOf", [])
            if isinstance(branch, dict) and "if" not in branch
        )
        properties = node.get("properties")
        if properties:
            for name, sub in properties.items():
                walk(sub, (*path, name))
            return True
        items = node.get("items")
        if isinstance(items, dict):
            return walk(items, path) or banked
        if path and not banked:
            out.add(path[-1])
        return banked

    walk(schema, ())
    return out


def closure(direct: set[str], bank_refs: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    queue = list(direct)
    while queue:
        current = queue.pop()
        if current in seen:
            continue
        seen.add(current)
        queue.extend(bank_refs.get(current, set()))
    return seen


def occurrences(
    schema: dict,
    bank: dict[str, dict],
    entries: dict[str, dict],
) -> list[dict[str, str]]:
    """Every role-qualified bank occurrence, preserving its form data path.

    JSON Schema references carry structural composition. The block index additionally
    carries scalar inheritance, which the stock JSON Schema emitter otherwise flattens.
    Walking both produces one graph without confusing a semantic requirement with the
    mechanism used to capture its answer.
    """
    found: dict[tuple[str, str], str] = {}

    def path_text(path: tuple[str, ...]) -> str:
        return "/" + "/".join(path) if path else "/"

    def record(block_id: str, path: tuple[str, ...], depth: int) -> None:
        key = (block_id, path_text(path))
        relationship = "direct" if depth == 0 else "transitive"
        if found.get(key) != "direct":
            found[key] = relationship

    def composed(block_id: str, path: tuple[str, ...], depth: int, seen: set[str]) -> None:
        if block_id in seen:
            return
        next_seen = {*seen, block_id}
        for parent in entries.get(block_id, {}).get("composes", []):
            record(parent, path, depth)
            composed(parent, path, depth + 1, next_seen)

    def walk(
        node: object,
        path: tuple[str, ...],
        depth: int,
        defs: dict,
        seen: set[tuple[str, tuple[str, ...]]],
    ) -> None:
        if not isinstance(node, dict):
            return
        ref = node.get("$ref")
        if isinstance(ref, str):
            block_id = bank_ref(ref)
            if block_id is not None and block_id in bank:
                marker = (block_id, path)
                record(block_id, path, depth)
                composed(block_id, path, depth + 1, set())
                if marker not in seen:
                    target = bank[block_id]
                    walk(
                        target,
                        path,
                        depth + 1,
                        target.get("$defs", {}),
                        {*seen, marker},
                    )
            elif ref.startswith("#/$defs/"):
                target = defs.get(ref.removeprefix("#/$defs/"))
                if isinstance(target, dict):
                    walk(target, path, depth, defs, seen)

        for name, child in node.get("properties", {}).items():
            walk(child, (*path, name), depth, defs, seen)
        items = node.get("items")
        if isinstance(items, dict):
            walk(items, (*path, "[]"), depth, defs, seen)
        for keyword in ("allOf", "anyOf", "oneOf"):
            for branch in node.get(keyword, []):
                walk(branch, path, depth, defs, seen)

    walk(schema, (), 0, schema.get("$defs", {}), set())
    return [
        {
            "blockId": block_id,
            "path": path,
            "relationship": relationship,
        }
        for (block_id, path), relationship in sorted(found.items())
    ]


def catalogue(kind: str, block_id: str) -> dict:
    path = DIST / kind / block_id / "index.json"
    return json.loads(path.read_text()) if path.is_file() else {}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze emitted form and question artifacts.")
    parser.add_argument("--json", action="store_true", help="Emit the machine-readable analysis projection.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bank = blocks("question-bank")
    forms = blocks("forms")
    entries = {block_id: catalogue("question-bank", block_id) for block_id in bank}
    semantic = {
        block_id
        for block_id, entry in entries.items()
        if entry.get("classification", "semanticQuestion") == "semanticQuestion"
    }
    mechanisms = {
        block_id
        for block_id, entry in entries.items()
        if entry.get("classification") == "captureMechanism"
    }
    bank_refs = {
        block_id: refs(schema) | set(entries[block_id].get("composes", []))
        for block_id, schema in bank.items()
    }
    direct = {form_id: refs(schema) for form_id, schema in forms.items()}
    used = {form_id: closure(blocks_used, bank_refs) for form_id, blocks_used in direct.items()}
    asked = {form_id: block_ids & semantic for form_id, block_ids in used.items()}
    capture = {form_id: block_ids & mechanisms for form_id, block_ids in used.items()}
    direct_questions = {form_id: block_ids & semantic for form_id, block_ids in direct.items()}
    occurrence_rows = {
        form_id: occurrences(schema, bank, entries) for form_id, schema in forms.items()
    }
    question_associations = [
        {"formId": form_id, "questionId": row["blockId"], **{k: row[k] for k in ("path", "relationship")}}
        for form_id, rows in occurrence_rows.items()
        for row in rows
        if row["blockId"] in semantic
    ]
    mechanism_associations = [
        {"formId": form_id, "mechanismId": row["blockId"], **{k: row[k] for k in ("path", "relationship")}}
        for form_id, rows in occurrence_rows.items()
        for row in rows
        if row["blockId"] in mechanisms
    ]

    pairwise = []
    for a, b in itertools.combinations(sorted(forms), 2):
        qa, qb = asked[a], asked[b]
        both, either = qa & qb, qa | qb
        pairwise.append({
            "formA": a,
            "formB": b,
            "similarity": len(both) / len(either) if either else 0.0,
            "questionsInCommon": len(both),
            "shareOfA": len(both) / len(qa) if qa else 0.0,
            "shareOfB": len(both) / len(qb) if qb else 0.0,
        })

    if args.json:
        print(
            json.dumps(
                {
                    "blocks": sorted(bank),
                    "questions": sorted(semantic),
                    "captureMechanisms": sorted(mechanisms),
                    "asks": {f: sorted(q) for f, q in asked.items()},
                    "asksDirectly": {f: sorted(q) for f, q in direct_questions.items()},
                    "usesCaptureMechanisms": {f: sorted(q) for f, q in capture.items()},
                    "formQuestionAssociations": question_associations,
                    "formCaptureMechanisms": mechanism_associations,
                    "pairwise": pairwise,
                },
                indent=2,
            )
        )
        return 0

    print("## Question inventory\n")
    print("| Question | Entity | Tags | Forms | Asked by |")
    print("| --- | --- | --- | --- | --- |")
    for block_id in sorted(semantic, key=lambda q: (-len([f for f in asked if q in asked[f]]), q)):
        entry = entries[block_id]
        using = sorted(f for f in asked if block_id in asked[f])
        tags = ", ".join(entry.get("tags", [])) or "—"
        print(
            f"| `{block_id}` | {entry.get('entity', '—')} | {tags} | "
            f"{len(using)} | {', '.join(using) or '—'} |"
        )

    print("\n## Capture mechanisms\n")
    print("| Mechanism | Forms | Used by |")
    print("| --- | --- | --- |")
    for block_id in sorted(mechanisms):
        using = sorted(form_id for form_id in capture if block_id in capture[form_id])
        print(f"| `{block_id}` | {len(using)} | {', '.join(using) or '—'} |")

    print("\n## Form to question\n")
    print("| Form | Questions asked | Composed directly | Reached through another question |")
    print("| --- | --- | --- | --- |")
    for form_id in sorted(forms):
        print(
            f"| {form_id} | {len(asked[form_id])} | {len(direct_questions[form_id])} | "
            f"{len(asked[form_id]) - len(direct_questions[form_id])} |"
        )

    print("\n## Pairwise similarity\n")
    print("| Form A | Form B | Similarity | In common | Share of A | Share of B |")
    print("| --- | --- | --- | --- | --- | --- |")
    for row in sorted(pairwise, key=lambda item: item["similarity"], reverse=True):
        print(
            f"| {row['formA']} | {row['formB']} | {row['similarity']:.0%} | "
            f"{row['questionsInCommon']} | {row['shareOfA']:.0%} | "
            f"{row['shareOfB']:.0%} |"
        )

    print("\n## Fields not yet in the bank\n")
    local: dict[str, set[str]] = {}
    for form_id, schema in sorted(forms.items()):
        for name in form_local_leaves(schema, schema.get("$defs", {})):
            local.setdefault(name, set()).add(form_id)
    shared = {name: where for name, where in local.items() if len(where) > 1}
    print(
        f"{len(local)} field names are declared by a form rather than composed from the bank; "
        f"**{len(shared)}** of them by more than one form."
    )
    if shared:
        print("\n| Field | Declared by | ")
        print("| --- | --- |")
        for name, where in sorted(shared.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            print(f"| `{name}` | {', '.join(sorted(where))} |")

    print("\n## Reuse\n")
    print("| Form | Questions asked | New to the bank | Already in the bank |")
    print("| --- | --- | --- | --- |")
    # In the order the forms were migrated, which is the order the curve is claimed in.
    known: set[str] = set()
    for form_id in (
        "key-contacts",
        "sf424",
        "sf424a",
        "sf424-short",
        "project-narrative-attachments",
        "budget-narrative-attachments",
        "other-narrative-attachments",
        "rr-budget",
    ):
        if form_id not in asked:
            continue
        new = asked[form_id] - known
        print(
            f"| {form_id} | {len(asked[form_id])} | {len(new)} | {len(asked[form_id]) - len(new)} |"
        )
        known |= asked[form_id]
    return 0


if __name__ == "__main__":
    sys.exit(main())
