#!/usr/bin/env python3
"""Verify the one-to-one manifest for emitted XML-profile root XSD fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlparse

SHA256 = re.compile(r"[0-9a-f]{64}")
NATIVE_VERSION = re.compile(r"-V([0-9]+(?:\.[0-9]+)+)\.xsd$")
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIST = ROOT / "dist" / "forms"
DEFAULT_FIXTURES = ROOT / "tests" / "fixtures" / "grants-gov-xsd"
DEFAULT_MANIFEST = DEFAULT_FIXTURES / "root-fixture-manifest.json"
CONTRACT = "grants-gov-root-xsd-fixtures/v1"
OFFICIAL_SCHEME = "https"
OFFICIAL_HOST = "apply07.grants.gov"
OFFICIAL_PATH_PREFIX = "/apply/forms/schemas/"
ROW_KEYS = {"formId", "uri", "nativeVersion", "role", "sha256", "path"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def official_root_identity(uri: str, *, owner: str) -> tuple[str, str]:
    parsed = urlparse(uri)
    if (
        parsed.scheme != OFFICIAL_SCHEME
        or parsed.netloc != OFFICIAL_HOST
        or not parsed.path.startswith(OFFICIAL_PATH_PREFIX)
        or parsed.params
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            f"{owner} root XSD URI must be an exact official forms/schema URI: {uri}"
        )
    filename = PurePosixPath(unquote(parsed.path)).name
    if not filename or filename in {".", ".."}:
        raise ValueError(f"{owner} root XSD URI has no filename: {uri}")
    version = NATIVE_VERSION.search(filename)
    if version is None:
        raise ValueError(f"{owner} root XSD URI filename has no native version suffix: {uri}")
    return filename, version.group(1)


def manifest_rows(manifest: Path) -> list[dict[str, Any]]:
    document = read_json(manifest)
    if not isinstance(document, dict) or set(document) != {"contract", "fixtures"}:
        raise ValueError(f"{manifest} must contain only contract and fixtures")
    if document["contract"] != CONTRACT:
        raise ValueError(f"{manifest} has unsupported contract {document['contract']!r}")
    rows = document["fixtures"]
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{manifest} has no fixture rows")
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != ROW_KEYS:
            raise ValueError(f"{manifest} fixture row {index} has invalid fields")
    return rows


def verify_profiles(dist: Path, fixtures: Path, manifest: Path | None = None) -> tuple[int, int]:
    profiles = sorted(dist.glob("*/targets/grants-gov-xml.json"))
    if not profiles:
        raise ValueError(f"no emitted XML profiles found under {dist}")
    if not fixtures.is_dir():
        raise ValueError(f"XSD fixture directory does not exist: {fixtures}")
    manifest = manifest or fixtures / "root-fixture-manifest.json"
    rows = manifest_rows(manifest)

    fixture_files = sorted(path for path in fixtures.rglob("*.xsd") if path.is_file())
    by_name: dict[str, list[Path]] = {}
    for path in fixture_files:
        by_name.setdefault(path.name, []).append(path)

    rows_by_form: dict[str, dict[str, Any]] = {}
    claimed_paths: dict[Path, str] = {}
    claimed_sources: dict[tuple[str, str], str] = {}
    for row in rows:
        form_id = row["formId"]
        if not isinstance(form_id, str) or not form_id:
            raise ValueError("fixture manifest formId must be a non-empty string")
        if form_id in rows_by_form:
            raise ValueError(f"duplicate fixture manifest row for {form_id}")
        rows_by_form[form_id] = row
        if row["role"] != "root":
            raise ValueError(f"{form_id} fixture role must be root, got {row['role']!r}")
        if not isinstance(row["nativeVersion"], str) or not row["nativeVersion"]:
            raise ValueError(f"{form_id} fixture nativeVersion must be a non-empty string")
        if not isinstance(row["sha256"], str) or SHA256.fullmatch(row["sha256"]) is None:
            raise ValueError(f"{form_id} fixture has no valid SHA-256")
        filename, uri_version = official_root_identity(row["uri"], owner=form_id)
        if row["nativeVersion"] != uri_version:
            raise ValueError(
                f"{form_id} fixture nativeVersion {row['nativeVersion']!r} does not match "
                f"official URI version {uri_version!r}"
            )

        relative = PurePosixPath(row["path"])
        if relative.is_absolute() or ".." in relative.parts or relative.name != filename:
            raise ValueError(f"{form_id} fixture path does not match its official URI: {row['path']}")
        path = fixtures.joinpath(*relative.parts)
        candidates = by_name.get(filename, [])
        if len(candidates) != 1:
            locations = ", ".join(str(item.relative_to(fixtures)) for item in candidates)
            raise ValueError(
                f"{form_id} root basename {filename} must resolve to exactly one candidate; "
                f"found {len(candidates)}{': ' + locations if locations else ''}"
            )
        if candidates[0] != path:
            raise ValueError(f"{form_id} fixture manifest path does not resolve to {filename}")
        if sha256(path) != row["sha256"]:
            raise ValueError(f"{form_id} fixture bytes do not match manifest SHA-256")
        if path in claimed_paths:
            raise ValueError(
                f"fixture {row['path']} is claimed by both {claimed_paths[path]} and {form_id}"
            )
        claimed_paths[path] = form_id
        source_key = (row["uri"], row["sha256"])
        if source_key in claimed_sources:
            raise ValueError(
                f"root source {row['uri']} is claimed by both "
                f"{claimed_sources[source_key]} and {form_id}"
            )
        claimed_sources[source_key] = form_id

    profile_forms: set[str] = set()
    for profile_path in profiles:
        profile = read_json(profile_path)
        form_id = profile.get("formId")
        xsd = profile.get("xsd")
        if not isinstance(form_id, str) or not isinstance(xsd, dict):
            raise ValueError(f"{profile_path} has no formId/XSD declaration")
        if form_id in profile_forms:
            raise ValueError(f"duplicate emitted XML profile for {form_id}")
        profile_forms.add(form_id)
        row = rows_by_form.get(form_id)
        if row is None:
            raise ValueError(f"{form_id} has no root fixture manifest row")
        uri = xsd.get("uri")
        expected = xsd.get("sha256")
        if uri != row["uri"] or expected != row["sha256"]:
            raise ValueError(f"{form_id} profile XSD identity does not match its fixture manifest")
        official_root_identity(uri, owner=form_id)

        evidence_path = profile_path.parents[1] / "evidence.json"
        evidence = read_json(evidence_path)
        sources = [
            source
            for source in evidence.get("sources", [])
            if source.get("type") == "xsd" and source.get("uri") == uri
        ]
        if len(sources) != 1:
            raise ValueError(
                f"{form_id} root XSD URI must resolve to exactly one XSD evidence source"
            )
        source = sources[0]
        if source.get("sha256") != expected or source.get("nativeVersion") != row["nativeVersion"]:
            raise ValueError(f"{form_id} root XSD evidence does not match its fixture manifest")

    stale = sorted(set(rows_by_form) - profile_forms)
    if stale:
        raise ValueError(f"fixture manifest has stale rows: {', '.join(stale)}")
    return len(profiles), len(claimed_paths)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    result.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    result.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        profiles, fixtures = verify_profiles(args.dist, args.fixtures, args.manifest)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1
    sys.stdout.write(
        "xsd_fixture_gate:\n"
        "  status: passed\n"
        f"  profiles: {profiles}\n"
        f"  fixtures: {fixtures}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
