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
import csv
import itertools
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DIST = REPO / "dist"
SEQUENCE = REPO / "analysis" / "form-sequence.v1.json"


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text()) if path.is_file() else {}


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


def form_file(form_id: str, relative: str) -> dict:
    return read_json(DIST / "forms" / form_id / relative)


def occurrence_index(form_index: dict) -> dict[str, dict]:
    """Portable field attribution keyed by canonical response path."""
    return {
        row["path"]: row
        for row in form_index.get("fieldOccurrences", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }


def canonical_pointer(path: str) -> str:
    """Translate an emitted occurrence path to the evidence contract's JSON pointer."""
    parts = [part for part in path.split("/") if part]
    pointer = "#"
    for part in parts:
        if part == "[]":
            pointer += "/items"
        else:
            pointer += "/properties/" + part.replace("~", "~0").replace("/", "~1")
    return pointer


def accepted_mapping(evidence: dict, path: str) -> dict | None:
    pointer = canonical_pointer(path)
    for mapping in evidence.get("semanticReview", {}).get("mappings", []):
        if mapping.get("canonicalPointer") == pointer and mapping.get("status") == "accepted":
            return mapping
    return None


def primary_xsd(evidence: dict, profile: dict) -> dict:
    target = profile.get("xsd", {})
    sources = evidence.get("sources", [])
    match = next(
        (source for source in sources if source.get("type") == "xsd" and source.get("uri") == target.get("uri")),
        None,
    )
    if match is None:
        match = next((source for source in sources if source.get("type") == "xsd"), {})
    return {
        "uri": target.get("uri") or match.get("uri"),
        "nativeVersion": match.get("nativeVersion", match.get("version")),
        "sha256": target.get("sha256") or match.get("sha256"),
    }


def xml_path(profile: dict, occurrence_path: str) -> str | None:
    """Resolve an emitted JSON occurrence path through a portable XML profile."""
    root = profile.get("root", {})
    node = profile.get("mapping", {})
    if not root or not node:
        return None
    root_prefix = root.get("namespacePrefix") or "default"
    parts = [f"{root_prefix}:{root.get('element')}"]
    for segment in (part for part in occurrence_path.split("/") if part and part != "[]"):
        node = node.get("fields", {}).get(segment)
        if not isinstance(node, dict):
            return None
        element = node.get("element")
        if element:
            namespace = node.get("namespace", "default")
            prefix = root_prefix if namespace == "default" else namespace
            parts.append(f"{prefix}:{element}")
    return "/" + "/".join(parts)


def schema_shape(schema: dict) -> dict:
    shape = {
        "schemaType": schema.get("type"),
        "minimum": schema.get("minimum"),
        "maximum": schema.get("maximum"),
        "minLength": schema.get("minLength"),
        "maxLength": schema.get("maxLength"),
        "minItems": schema.get("minItems"),
        "maxItems": schema.get("maxItems"),
        "format": schema.get("format"),
    }
    return shape


def occurrence_shape(form_schema: dict, path: str, bank: dict[str, dict]) -> dict:
    """Return constraints visible at one form occurrence, resolving published refs.

    Requiredness is reported only after resolving the property in the emitted graph. A missing
    path remains unknown instead of being misreported as optional.
    """
    local_defs = form_schema.get("$defs", {})

    def variants(node: dict, seen: set[str] | None = None) -> list[dict]:
        seen = set() if seen is None else seen
        out = [node]
        ref = node.get("$ref")
        target = None
        marker = None
        if isinstance(ref, str) and "question-bank/" in ref:
            block_id = bank_ref(ref)
            target = bank.get(block_id or "")
            marker = f"bank:{block_id}"
        elif isinstance(ref, str) and ref.startswith("#/$defs/"):
            name = ref.removeprefix("#/$defs/")
            target = local_defs.get(name)
            marker = f"local:{name}"
        if isinstance(target, dict) and marker not in seen:
            out.extend(variants(target, {*seen, marker}))
        for branch in node.get("allOf", []):
            if isinstance(branch, dict):
                out.extend(variants(branch, seen))
        return out

    current = form_schema
    required: bool | None = None
    array_shape: dict | None = None
    for segment in (part for part in path.split("/") if part):
        available = variants(current)
        if segment == "[]":
            container = next((item for item in available if isinstance(item.get("items"), dict)), None)
            if container is None:
                return {**schema_shape({}), "required": required}
            array_shape = schema_shape(container)
            current = container["items"]
            continue
        owner = next(
            (item for item in available if segment in item.get("properties", {})),
            None,
        )
        if owner is None:
            return {**schema_shape({}), "required": None}
        required = any(segment in item.get("required", []) for item in available)
        current = owner["properties"][segment]

    resolved = {}
    for item in variants(current):
        for key, value in schema_shape(item).items():
            if value is not None and key not in resolved:
                resolved[key] = value
    shape = schema_shape({})
    shape.update(resolved)
    if array_shape is not None:
        for key in ("minItems", "maxItems"):
            if array_shape.get(key) is not None:
                shape[key] = array_shape[key]
    shape["required"] = required
    return shape


def behavior_occurrences(form_id: str) -> list[dict[str, str]]:
    rules = form_file(form_id, "sgg/rule-schema.json")
    found: list[dict[str, str]] = []

    def walk(node: object, path: tuple[str, ...]) -> None:
        if not isinstance(node, dict):
            return
        for key, value in node.items():
            if key.startswith("gg_") and isinstance(value, dict):
                rule = str(value.get("rule", "unspecified"))
                found.append({
                    "formId": form_id,
                    "capabilityId": f"behavior/{key.removeprefix('gg_')}:{rule}",
                    "path": "/" + "/".join(path) if path else "/",
                    "kind": "behavior",
                })
            elif isinstance(value, dict):
                walk(value, (*path, key))

    walk(rules, ())
    return sorted(found, key=lambda row: (row["capabilityId"], row["path"]))


def pairwise_rows(asked: dict[str, set[str]], *, scope: str, null_empty: bool = False) -> list[dict]:
    rows = []
    for a, b in itertools.combinations(sorted(asked), 2):
        qa, qb = asked[a], asked[b]
        both, either = qa & qb, qa | qb
        empty = not either
        rows.append({
            "formA": a,
            "formB": b,
            "scope": scope,
            "similarity": None if empty and null_empty else (len(both) / len(either) if either else 0.0),
            "questionsInCommon": len(both),
            "questionsInA": len(qa),
            "questionsInB": len(qb),
            "shareOfA": None if not qa and null_empty else (len(both) / len(qa) if qa else 0.0),
            "shareOfB": None if not qb and null_empty else (len(both) / len(qb) if qb else 0.0),
            "eligible": bool(either),
        })
    return rows


def csv_value(value: object) -> object:
    if isinstance(value, (list, tuple, set)):
        return "|".join(str(item) for item in value)
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else value


def write_csv(path: pathlib.Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field)) for field in fields})


def write_workbook(output_dir: pathlib.Path, analysis: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "form-analysis.json").write_text(json.dumps(analysis, indent=2) + "\n")
    specs = {
        "question-inventory.csv": (
            analysis["questionInventory"],
            ["questionId", "name", "description", "entity", "tags", "classification", "responseRole", "formsCount", "forms", "reviewedFormsCount", "reviewedForms"],
        ),
        "form-question-associations.csv": (
            analysis["formQuestionWorkbook"],
            ["formId", "formName", "formVersion", "legacyFormId", "questionId", "questionName", "questionDescription", "entity", "tags", "classification", "responseRole", "occurrencePath", "relationship", "schemaType", "required", "minimum", "maximum", "minLength", "maxLength", "minItems", "maxItems", "format", "formSemanticReviewStatus", "mappingStatus", "publishable", "countedInExploratorySimilarity", "countedInPublishedSimilarity", "sourceId", "sourcePath", "reviewedBy", "reviewedAt", "xmlPath", "xmlType", "xmlTypeSource", "xsdUri", "xsdNativeVersion", "xsdSha256", "extractionRepository", "extractionRevision", "extractionArtifact", "sourceSetSha256"],
        ),
        "unclassified-form-fields.csv": (
            analysis["unclassifiedFormFields"],
            ["formId", "fieldPath", "fieldName", "responseRole", "classification", "countedAsQuestion", "reason"],
        ),
        "pairwise-exploratory.csv": (
            analysis["pairwiseExploratory"],
            ["formA", "formB", "scope", "eligible", "similarity", "questionsInCommon", "questionsInA", "questionsInB", "shareOfA", "shareOfB"],
        ),
        "pairwise-reviewed.csv": (
            analysis["pairwiseReviewed"],
            ["formA", "formB", "scope", "eligible", "similarity", "questionsInCommon", "questionsInA", "questionsInB", "shareOfA", "shareOfB"],
        ),
        "capability-occurrences.csv": (
            analysis["capabilityOccurrences"],
            ["formId", "capabilityId", "kind", "path", "relationship"],
        ),
        "marginal-capability-reuse.csv": (
            analysis["marginalCapabilityReuse"],
            ["sequence", "formId", "measurementStatus", "questionCount", "newQuestionCount", "reusedQuestionCount", "newQuestions", "reusedQuestions", "captureMechanismCount", "newCaptureMechanismCount", "reusedCaptureMechanismCount", "newCaptureMechanisms", "reusedCaptureMechanisms", "behaviorCount", "newBehaviorCount", "reusedBehaviorCount", "newBehaviors", "reusedBehaviors"],
        ),
    }
    for name, (rows, fields) in specs.items():
        write_csv(output_dir / name, rows, fields)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze emitted form and question artifacts.")
    parser.add_argument("--json", action="store_true", help="Emit the machine-readable analysis projection.")
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        help="Write the complete JSON projection and spreadsheet-ready CSV tables to this directory.",
    )
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

    pairwise = pairwise_rows(asked, scope="implementation-derived-unreviewed")

    form_metadata = {
        form_id: form_file(form_id, "manifest.json").get("form", {})
        for form_id in forms
    }
    form_indexes = {form_id: form_file(form_id, "index.json") for form_id in forms}
    field_occurrences = {
        form_id: occurrence_index(form_indexes[form_id]) for form_id in forms
    }
    form_evidence = {form_id: form_file(form_id, "evidence.json") for form_id in forms}
    form_profiles = {
        form_id: form_file(form_id, "targets/grants-gov-xml.json")
        for form_id in forms
    }

    workbook_associations: list[dict] = []
    reviewed_asked: dict[str, set[str]] = {form_id: set() for form_id in forms}
    for row in question_associations:
        form_id = row["formId"]
        question_id = row["questionId"]
        entry = entries[question_id]
        evidence = form_evidence[form_id]
        profile = form_profiles[form_id]
        accepted = accepted_mapping(evidence, row["path"])
        if accepted:
            reviewed_asked[form_id].add(question_id)
        review = evidence.get("semanticReview", {})
        extraction = evidence.get("extraction", {})
        xsd = primary_xsd(evidence, profile)
        shape = occurrence_shape(forms[form_id], row["path"], bank)
        fallback_shape = schema_shape(bank[question_id])
        for key, value in fallback_shape.items():
            if shape.get(key) is None and value is not None:
                shape[key] = value
        workbook_associations.append({
            "formId": form_id,
            "formName": form_metadata[form_id].get("formName") or catalogue("forms", form_id).get("description"),
            "formVersion": form_metadata[form_id].get("formVersion"),
            "legacyFormId": form_metadata[form_id].get("legacyFormId"),
            "questionId": question_id,
            "questionName": entry.get("name"),
            "questionDescription": entry.get("description"),
            "entity": entry.get("entity"),
            "tags": entry.get("tags", []),
            "classification": entry.get("classification", "semanticQuestion"),
            "responseRole": (
                field_occurrences[form_id].get(row["path"], {}).get("responseRole")
                or entry.get("responseRole")
                or "unclassified"
            ),
            "occurrencePath": row["path"],
            "relationship": row["relationship"],
            **shape,
            "formSemanticReviewStatus": review.get("status", "unreviewed"),
            "mappingStatus": accepted.get("status") if accepted else (
                "unreviewed" if review.get("status", "unreviewed") == "unreviewed" else "unmapped"
            ),
            "publishable": accepted is not None,
            "countedInExploratorySimilarity": True,
            "countedInPublishedSimilarity": accepted is not None,
            "sourceId": accepted.get("sourceId") if accepted else None,
            "sourcePath": accepted.get("sourcePath") if accepted else None,
            "reviewedBy": accepted.get("reviewedBy") if accepted else None,
            "reviewedAt": accepted.get("reviewedAt") if accepted else None,
            "xmlPath": xml_path(profile, row["path"]),
            # Portable XML profiles currently describe element projection but not source XSD types.
            "xmlType": None,
            "xmlTypeSource": None,
            "xsdUri": xsd["uri"],
            "xsdNativeVersion": xsd["nativeVersion"],
            "xsdSha256": xsd["sha256"],
            "extractionRepository": extraction.get("repository"),
            "extractionRevision": extraction.get("revision"),
            "extractionArtifact": extraction.get("artifact"),
            "sourceSetSha256": extraction.get("sourceSetSha256"),
        })
    workbook_associations.sort(
        key=lambda row: (row["formId"], row["questionId"], row["occurrencePath"])
    )

    question_inventory = []
    for question_id in sorted(semantic):
        entry = entries[question_id]
        using = sorted(form_id for form_id in asked if question_id in asked[form_id])
        reviewed_using = sorted(
            form_id for form_id in reviewed_asked if question_id in reviewed_asked[form_id]
        )
        question_inventory.append({
            "questionId": question_id,
            "name": entry.get("name"),
            "description": entry.get("description"),
            "entity": entry.get("entity"),
            "tags": entry.get("tags", []),
            "classification": entry.get("classification", "semanticQuestion"),
            "responseRole": entry.get("responseRole") or "unclassified",
            "formsCount": len(using),
            "forms": using,
            "reviewedFormsCount": len(reviewed_using),
            "reviewedForms": reviewed_using,
        })
    question_inventory.sort(key=lambda row: (-row["formsCount"], row["questionId"]))

    behavior_rows = [
        row
        for form_id in sorted(forms)
        for row in behavior_occurrences(form_id)
    ]
    capability_occurrences = [
        {
            "formId": row["formId"],
            "capabilityId": row["questionId"],
            "kind": "semanticQuestion",
            "path": row["path"],
            "relationship": row["relationship"],
        }
        for row in question_associations
    ] + [
        {
            "formId": row["formId"],
            "capabilityId": row["mechanismId"],
            "kind": "captureMechanism",
            "path": row["path"],
            "relationship": row["relationship"],
        }
        for row in mechanism_associations
    ] + behavior_rows
    capability_occurrences.sort(
        key=lambda row: (row["formId"], row["kind"], row["capabilityId"], row["path"])
    )

    unclassified_form_fields = []
    known_blocks = set(entries)
    for form_id in sorted(forms):
        occurrences_for_form = form_indexes[form_id].get("fieldOccurrences", [])
        for occurrence in sorted(occurrences_for_form, key=lambda row: row.get("path", "")):
            if not occurrence.get("leaf"):
                continue
            if set(occurrence.get("blockIds", [])) & known_blocks:
                continue
            response_role = occurrence.get("responseRole")
            if response_role and response_role != "applicantInput":
                continue
            path = occurrence["path"]
            unclassified_form_fields.append({
                "formId": form_id,
                "fieldPath": path,
                "fieldName": path.rsplit("/", 1)[-1],
                "responseRole": response_role or "unclassified",
                "classification": "unclassified",
                "countedAsQuestion": False,
                "reason": (
                    "Applicant input is not composed from a classified question-bank block."
                    if response_role == "applicantInput"
                    else "Form-local field has neither canonical question lineage nor an explicit response role."
                ),
            })

    sequence_contract = read_json(SEQUENCE)
    declared_sequence = sequence_contract.get("forms", [])
    undeclared = sorted(set(forms) - set(declared_sequence))
    unknown = sorted(set(declared_sequence) - set(forms))
    if undeclared or unknown:
        details = []
        if undeclared:
            details.append(f"undeclared emitted forms: {', '.join(undeclared)}")
        if unknown:
            details.append(f"sequence entries without emitted forms: {', '.join(unknown)}")
        raise ValueError("form sequence does not reconcile with emitted artifacts (" + "; ".join(details) + ")")

    behaviors_by_form = {
        form_id: {row["capabilityId"] for row in behavior_rows if row["formId"] == form_id}
        for form_id in forms
    }
    marginal = []
    known_questions: set[str] = set()
    known_mechanisms: set[str] = set()
    known_behaviors: set[str] = set()
    for position, form_id in enumerate(declared_sequence, start=1):
        dimensions = {
            "Question": (asked[form_id], known_questions),
            "CaptureMechanism": (capture[form_id], known_mechanisms),
            "Behavior": (behaviors_by_form[form_id], known_behaviors),
        }
        row = {
            "sequence": position,
            "formId": form_id,
            "measurementStatus": "implementation-derived-unreviewed",
        }
        for label, (current, known) in dimensions.items():
            new = sorted(current - known)
            reused = sorted(current & known)
            stem = label[0].lower() + label[1:]
            row[f"{stem}Count"] = len(current)
            row[f"new{label}Count"] = len(new)
            row[f"reused{label}Count"] = len(reused)
            row[f"new{label}s"] = new
            row[f"reused{label}s"] = reused
            known |= current
        marginal.append(row)

    analysis = {
        "contract": "grants-form-analysis/v1",
        "status": {
            "exploratory": "Implementation-derived canonical identities; semantic evidence may be unreviewed.",
            "published": "Only occurrence mappings explicitly accepted in evidence sidecars contribute.",
            "reviewedAssociationCount": sum(
                1 for row in workbook_associations if row["publishable"]
            ),
            "exploratoryAssociationCount": len(question_associations),
            "unclassifiedFormFieldCount": len(unclassified_form_fields),
        },
        "sequence": sequence_contract,
        "blocks": sorted(bank),
        "questions": sorted(semantic),
        "captureMechanisms": sorted(mechanisms),
        "asks": {f: sorted(q) for f, q in asked.items()},
        "asksDirectly": {f: sorted(q) for f, q in direct_questions.items()},
        "reviewedAsks": {f: sorted(q) for f, q in reviewed_asked.items()},
        "usesCaptureMechanisms": {f: sorted(q) for f, q in capture.items()},
        "formQuestionAssociations": question_associations,
        "formCaptureMechanisms": mechanism_associations,
        "pairwise": pairwise,
        "questionInventory": question_inventory,
        "formQuestionWorkbook": workbook_associations,
        "pairwiseExploratory": pairwise,
        "pairwiseReviewed": pairwise_rows(
            reviewed_asked,
            scope="accepted-semantic-mappings-only",
            null_empty=True,
        ),
        "capabilityOccurrences": capability_occurrences,
        "unclassifiedFormFields": unclassified_form_fields,
        "marginalCapabilityReuse": marginal,
    }

    if args.output_dir:
        write_workbook(args.output_dir, analysis)

    if args.json:
        print(json.dumps(analysis, indent=2))
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
    for row in unclassified_form_fields:
        local.setdefault(row["fieldName"], set()).add(row["formId"])
    shared = {name: where for name, where in local.items() if len(where) > 1}
    print(
        f"{len(unclassified_form_fields)} field occurrences ({len(local)} distinct names) "
        "are not yet attributed to a canonical question or an explicit non-applicant role; "
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
        "rr-subaward-budget",
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
