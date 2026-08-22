#!/usr/bin/env python3
"""Create and verify a reproducible portable form-artifact bundle."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import Any

BUNDLE_CONTRACT = "grants-form-artifacts/v1"
SOURCE_REPOSITORY = "https://github.com/mikec-ai/grants-form-spec.git"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _artifact_files(dist: Path) -> list[Path]:
    published_roots = (dist / "forms", dist / "question-bank")
    files = sorted(
        path
        for published_root in published_roots
        if published_root.is_dir()
        for path in published_root.rglob("*")
        if path.is_file()
    )
    if not files:
        raise ValueError(f"no emitted artifacts found under {dist}")
    return files


def build_bundle(
    *,
    root: Path,
    output: Path,
    revision: str | None = None,
) -> dict[str, Any]:
    """Package ``dist`` with normalized archive metadata and an exact file manifest."""
    dist = root / "dist"
    entries: list[tuple[str, bytes]] = []
    files: list[dict[str, Any]] = []
    for path in _artifact_files(dist):
        relative = path.relative_to(root).as_posix()
        data = path.read_bytes()
        entries.append((relative, data))
        files.append({"path": relative, "sha256": _sha256(data), "size": len(data)})

    manifest = {
        "contract": BUNDLE_CONTRACT,
        "source": {
            "repository": SOURCE_REPOSITORY,
            "revision": revision or _revision(root),
        },
        "files": files,
    }
    manifest_data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    entries.insert(0, ("artifact-manifest.json", manifest_data))

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.GNU_FORMAT) as archive:
                for name, data in entries:
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    info.mode = 0o644
                    info.mtime = 0
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    archive.addfile(info, io.BytesIO(data))

    digest_path = output.with_suffix(output.suffix + ".sha256")
    digest_path.write_text(f"{_sha256(output.read_bytes())}  {output.name}\n")
    return manifest


def verify_bundle(bundle: Path) -> dict[str, Any]:
    """Verify the contract, membership, and digest of every bundled artifact."""
    with tarfile.open(bundle, mode="r:gz") as archive:
        members = {member.name: member for member in archive.getmembers() if member.isfile()}
        manifest_member = members.pop("artifact-manifest.json", None)
        if manifest_member is None:
            raise ValueError("bundle has no artifact-manifest.json")
        extracted = archive.extractfile(manifest_member)
        assert extracted is not None
        manifest = json.load(extracted)
        if manifest.get("contract") != BUNDLE_CONTRACT:
            raise ValueError(f"unsupported bundle contract: {manifest.get('contract')!r}")

        expected = {entry["path"]: entry for entry in manifest.get("files", [])}
        if set(members) != set(expected):
            raise ValueError("bundle membership does not match artifact manifest")
        for name, member in members.items():
            extracted = archive.extractfile(member)
            assert extracted is not None
            data = extracted.read()
            record = expected[name]
            if len(data) != record["size"] or _sha256(data) != record["sha256"]:
                raise ValueError(f"artifact digest mismatch: {name}")
    return manifest


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="archive path to create")
    parser.add_argument("--verify", type=Path, help="archive path to verify")
    return parser


def main() -> int:
    args = _parser().parse_args()
    if bool(args.output) == bool(args.verify):
        _parser().error("provide exactly one of --output or --verify")

    root = Path(__file__).resolve().parent.parent
    try:
        if args.output:
            manifest = build_bundle(root=root, output=args.output)
            print(
                "bundle:\n"
                f"  status: created\n  path: {args.output}\n"
                f"  artifacts: {len(manifest['files'])}\n"
                f"  revision: {manifest['source']['revision']}"
            )
        else:
            manifest = verify_bundle(args.verify)
            print(
                "bundle:\n"
                f"  status: verified\n  path: {args.verify}\n"
                f"  artifacts: {len(manifest['files'])}\n"
                f"  revision: {manifest['source']['revision']}"
            )
    except (OSError, ValueError, tarfile.TarError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
