"""Reference execution of the portable Grants.gov XML profile contract.

This module exists only to test producer artifacts.  It deliberately consumes a
resolved profile and caller-supplied fixtures; it is not a submission runtime and
contains no form-specific branches.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from xml.etree import ElementTree as ET


_MISSING = object()
_SOURCE_VALUE = object()
_SUPPORTED_CONTRACT = "grants-gov-xml-profile/v1"
_MAPPING_NODE_KEYS = {
    "element",
    "kind",
    "flatten",
    "emitWhenParentPresent",
    "namespace",
    "container",
    "source",
    "constant",
    "valueMap",
    "attributes",
    "fields",
    "items",
    "itemElement",
    "itemNamespace",
    "itemAttributes",
    "repeatElementPerItem",
}


@dataclass(frozen=True)
class PinnedXsdFile:
    """One locally stored XSD and its exact normalized-fixture digest."""

    name: str
    path: Path
    sha256: str


@dataclass(frozen=True)
class ExactXsdFixture:
    """Offline XSD validation inputs supplied by a form's conformance test."""

    entrypoint: str
    files: tuple[PinnedXsdFile, ...]
    official_sha256: str
    dependency_uri_prefixes: tuple[str, ...] = (
        "https://apply07.grants.gov/apply/system/schemas/",
    )


def _qname(profile: Mapping[str, Any], prefix: str | None, name: str) -> str:
    namespace = profile["namespaces"][prefix or "default"]
    return f"{{{namespace}}}{name}"


def _assert_supported_profile(profile: Mapping[str, Any]) -> None:
    contract = profile.get("contract")
    if contract != _SUPPORTED_CONTRACT:
        raise AssertionError(
            f"unsupported Grants.gov XML profile contract: {contract!r}; "
            f"expected {_SUPPORTED_CONTRACT!r}"
        )
    mapping = profile["mapping"]
    unexpected = set(mapping) - {"fields", "nonEmittingResponsePaths"}
    if unexpected:
        raise AssertionError(
            "unsupported Grants.gov XML mapping properties: "
            + ", ".join(sorted(unexpected))
        )
    paths = mapping.get("nonEmittingResponsePaths", [])
    if not isinstance(paths, list) or any(not isinstance(path, str) for path in paths):
        raise AssertionError("non-emitting response paths must be a unique array")
    if len(paths) != len(set(paths)):
        raise AssertionError("non-emitting response paths must be a unique array")
    for pointer in paths:
        if not isinstance(pointer, str) or not pointer.startswith("/") or pointer == "/":
            raise AssertionError(f"invalid non-emitting response path: {pointer!r}")
        for step in pointer[1:].split("/"):
            if not step:
                raise AssertionError(f"invalid non-emitting response path: {pointer!r}")
            index = 0
            while index < len(step):
                if step[index] == "~":
                    if index + 1 == len(step) or step[index + 1] not in "01":
                        raise AssertionError(
                            f"invalid non-emitting response path: {pointer!r}"
                        )
                    index += 1
                index += 1
    _assert_mapping_fields(mapping["fields"])


def _assert_mapping_fields(fields: Mapping[str, Mapping[str, Any]]) -> None:
    for node in fields.values():
        _assert_mapping_node(node, flattened_attachment_context=False)


def _assert_mapping_node(
    node: Mapping[str, Any], *, flattened_attachment_context: bool
) -> None:
    unexpected = set(node) - _MAPPING_NODE_KEYS
    if unexpected:
        raise AssertionError(
            "unsupported Grants.gov XML mapping node properties: "
            + ", ".join(sorted(unexpected))
        )

    kind = node.get("kind")
    if kind == "value" and node.get("flatten") is True:
        if not flattened_attachment_context:
            raise AssertionError(
                "flattened value mapping is only valid as an array item node"
            )
        ignored = set(node) - {"kind", "flatten"}
        if ignored:
            raise AssertionError(
                "flattened value mapping cannot declare ignored properties: "
                + ", ".join(sorted(ignored))
            )
        return
    if kind == "attachment" and node.get("flatten") is True:
        if not flattened_attachment_context:
            raise AssertionError(
                "flattened attachment mapping is only valid as an array item node "
                "with a declared itemElement"
            )
        ignored = set(node) - {"kind", "flatten"}
        if ignored:
            raise AssertionError(
                "flattened attachment mapping cannot declare ignored properties: "
                + ", ".join(sorted(ignored))
            )
        return

    if kind in {"object", "group"}:
        _assert_mapping_fields(node["fields"])
        return
    if kind == "array":
        items = node["items"]
        if "fields" in items:
            _assert_mapping_fields(items["fields"])
            return
        item_node = items["node"]
        item_is_flattened_attachment = (
            item_node.get("kind") == "attachment"
            and item_node.get("flatten") is True
        )
        item_is_flattened_value = (
            item_node.get("kind") == "value"
            and item_node.get("flatten") is True
        )
        if item_is_flattened_attachment and not node.get("itemElement"):
            raise AssertionError(
                "flattened attachment mapping is only valid as an array item node "
                "with a declared itemElement"
            )
        _assert_mapping_node(
            item_node,
            flattened_attachment_context=(
                item_is_flattened_attachment or item_is_flattened_value
            ),
        )


def _pointer(document: Mapping[str, Any], pointer: str) -> Any:
    value: Any = document
    for encoded_step in pointer.removeprefix("/").split("/"):
        step = encoded_step.replace("~1", "/").replace("~0", "~")
        if isinstance(value, Mapping) and step in value:
            value = value[step]
        else:
            return _MISSING
    return value


def _response_pointer_tree(profile: Mapping[str, Any]) -> dict[str, Any]:
    """Build exact root-response paths consumed or explicitly non-emitting."""

    tree: dict[str, Any] = {}

    def visit(value: Any) -> None:
        if isinstance(value, Mapping):
            source = value.get("source")
            if isinstance(source, str):
                cursor = tree
                for encoded_step in source.removeprefix("/").split("/"):
                    step = encoded_step.replace("~1", "/").replace("~0", "~")
                    cursor = cursor.setdefault(step, {})
                cursor[_SOURCE_VALUE] = True
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(profile["mapping"]["fields"])
    for source in profile["mapping"].get("nonEmittingResponsePaths", []):
        visit({"source": source})
    return tree


def _assert_source_payload(value: Any, tree: Mapping[Any, Any], path: str) -> None:
    if _SOURCE_VALUE in tree:
        return
    if not isinstance(value, Mapping):
        raise AssertionError(f"source override payload at {path} requires an object")
    unknown = set(value) - {key for key in tree if isinstance(key, str)}
    if unknown:
        raise AssertionError(
            f"unmapped response properties at {path}: "
            + ", ".join(sorted(str(key) for key in unknown))
        )
    for name, child_tree in tree.items():
        if not isinstance(name, str) or name not in value or value[name] is None:
            continue
        _assert_source_payload(value[name], child_tree, f"{path.rstrip('/')}/{name}")


def _assert_response_fields(
    fields: Mapping[str, Mapping[str, Any]],
    response: Mapping[str, Any],
    *,
    path: str,
    source_tree: Mapping[Any, Any],
) -> None:
    """Reject payload data the declarative mapping cannot consume.

    Groups consume their children at the current response level. Constants and
    source overrides do not consume a same-named local property. Absolute source
    pointers are accounted for separately through ``source_tree``.
    """

    direct: dict[str, Mapping[str, Any]] = {}

    def collect(declarations: Mapping[str, Mapping[str, Any]]) -> None:
        for name, node in declarations.items():
            if "constant" in node or "source" in node:
                continue
            if node.get("kind") == "group":
                collect(node["fields"])
            else:
                direct[name] = node

    collect(fields)
    source_names = {key for key in source_tree if isinstance(key, str)}
    unknown = set(response) - set(direct) - source_names
    if unknown:
        raise AssertionError(
            f"unmapped response properties at {path}: "
            + ", ".join(sorted(str(key) for key in unknown))
        )

    for name in source_names - set(direct):
        if name in response and response[name] is not None:
            _assert_source_payload(
                response[name], source_tree[name], f"{path.rstrip('/')}/{name}"
            )

    for name, node in direct.items():
        if name not in response or response[name] is None:
            continue
        value = response[name]
        nested_source_tree = source_tree.get(name, {})
        kind = node["kind"]
        if kind in {"object", "group"}:
            if not isinstance(value, Mapping):
                raise AssertionError(f"{kind} mapping requires an object response")
            _assert_response_fields(
                node["fields"],
                value,
                path=f"{path.rstrip('/')}/{name}",
                source_tree=nested_source_tree,
            )
        elif kind == "array":
            if not isinstance(value, list):
                raise AssertionError("array mapping requires a list response")
            items = node["items"]
            if "fields" in items:
                for index, item in enumerate(value):
                    if not isinstance(item, Mapping):
                        raise AssertionError("array field mapping requires object items")
                    _assert_response_fields(
                        items["fields"],
                        item,
                        path=f"{path.rstrip('/')}/{name}/{index}",
                        source_tree={},
                    )


def _value_map_key(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    return str(value)


def _resolved_value(
    declaration: Mapping[str, Any], value: Any, root_response: Mapping[str, Any]
) -> Any:
    if "constant" in declaration:
        value = declaration["constant"]
    elif source := declaration.get("source"):
        value = _pointer(root_response, source)
    if value is _MISSING:
        return value
    if value_map := declaration.get("valueMap"):
        value = value_map[_value_map_key(value)]
    if value is None:
        raise AssertionError(
            "declarative null emission is unsupported; omit the field or define explicit semantics"
        )
    return value


def _text(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _attributes(
    profile: Mapping[str, Any],
    declaration: Mapping[str, Any],
    root_response: Mapping[str, Any],
) -> dict[str, str]:
    attributes: dict[str, str] = {}
    for name, value_declaration in declaration.get("attributes", {}).items():
        value = _resolved_value(value_declaration, None, root_response)
        if value is _MISSING:
            continue
        attributes[_qname(profile, declaration.get("namespace"), name)] = _text(value)
    return attributes


def _static_attributes(
    profile: Mapping[str, Any], prefix: str | None, attributes: Mapping[str, Any]
) -> dict[str, str]:
    return {_qname(profile, prefix, name): _text(value) for name, value in attributes.items()}


def _add_attachment(
    parent: ET.Element,
    profile: Mapping[str, Any],
    node: Mapping[str, Any],
    attachment_id: str,
    attachments: Mapping[str, Mapping[str, Any]],
    root_response: Mapping[str, Any],
) -> None:
    if "attachment" not in profile:
        raise AssertionError("attachment mapping requires a profile attachment declaration")
    try:
        attachment = attachments[attachment_id]
    except KeyError as error:
        raise AssertionError(f"missing attachment fixture: {attachment_id}") from error

    leaf_parent = parent
    if container := node.get("container"):
        leaf_parent = ET.SubElement(
            parent, _qname(profile, container["namespace"], container["element"])
        )
    leaf = leaf_parent if node.get("flatten") else ET.SubElement(
        leaf_parent,
        _qname(profile, node.get("namespace"), node["element"]),
        _attributes(profile, node, root_response),
    )
    fields = profile["attachment"]["fields"]
    for field_name in ("fileName", "mimeType", "fileLocation", "hashValue"):
        declaration = fields[field_name]
        child = ET.SubElement(
            leaf, _qname(profile, declaration["namespace"], declaration["element"])
        )
        if field_name == "fileLocation":
            child.set(
                _qname(profile, declaration["namespace"], "href"),
                _text(attachment[field_name]),
            )
        else:
            child.text = _text(attachment[field_name])
        if field_name == "hashValue":
            child.set(
                _qname(profile, declaration["namespace"], "hashAlgorithm"),
                "SHA-256",
            )


def _add_fields(
    parent: ET.Element,
    profile: Mapping[str, Any],
    fields: Mapping[str, Mapping[str, Any]],
    response: Mapping[str, Any],
    root_response: Mapping[str, Any],
    attachments: Mapping[str, Mapping[str, Any]],
) -> None:
    for name, node in fields.items():
        if "constant" in node:
            value: Any = response
        elif source := node.get("source"):
            value = _pointer(root_response, source)
        elif node["kind"] == "group":
            value = response
        else:
            value = response.get(name, _MISSING)

        if value is _MISSING and node.get("emitWhenParentPresent"):
            value = {}
        if value is _MISSING or value is None:
            continue
        _add_node(parent, profile, node, value, root_response, attachments)


def _add_array(
    parent: ET.Element,
    profile: Mapping[str, Any],
    node: Mapping[str, Any],
    values: list[Any],
    root_response: Mapping[str, Any],
    attachments: Mapping[str, Mapping[str, Any]],
) -> None:
    item_element = node.get("itemElement")
    repeat_outer = not item_element or node.get("repeatElementPerItem", False)
    collection: ET.Element | None = None
    if not repeat_outer:
        collection = ET.SubElement(
            parent,
            _qname(profile, node.get("namespace"), node["element"]),
            _attributes(profile, node, root_response),
        )

    for value in values:
        outer = (
            ET.SubElement(
                parent,
                _qname(profile, node.get("namespace"), node["element"]),
                _attributes(profile, node, root_response),
            )
            if repeat_outer
            else collection
        )
        assert outer is not None
        item_parent = outer
        if item_element:
            item_parent = ET.SubElement(
                outer,
                _qname(profile, node.get("itemNamespace"), item_element),
                _static_attributes(
                    profile, node.get("itemNamespace"), node.get("itemAttributes", {})
                ),
            )
        items = node["items"]
        if "fields" in items:
            if not isinstance(value, Mapping):
                raise AssertionError("array field mapping requires object items")
            _add_fields(
                item_parent,
                profile,
                items["fields"],
                value,
                root_response,
                attachments,
            )
        else:
            _add_node(
                item_parent,
                profile,
                items["node"],
                value,
                root_response,
                attachments,
            )


def _add_node(
    parent: ET.Element,
    profile: Mapping[str, Any],
    node: Mapping[str, Any],
    value: Any,
    root_response: Mapping[str, Any],
    attachments: Mapping[str, Mapping[str, Any]],
) -> None:
    value = _resolved_value(node, value, root_response)
    if value is _MISSING:
        return
    kind = node["kind"]
    if kind == "attachment":
        _add_attachment(parent, profile, node, value, attachments, root_response)
        return
    if kind == "value":
        if node.get("flatten") is True:
            parent.text = _text(value)
            return
        leaf_parent = parent
        if container := node.get("container"):
            leaf_parent = ET.SubElement(
                parent, _qname(profile, container["namespace"], container["element"])
            )
        leaf = ET.SubElement(
            leaf_parent,
            _qname(profile, node.get("namespace"), node["element"]),
            _attributes(profile, node, root_response),
        )
        leaf.text = _text(value)
        return
    if kind == "group" and node.get("flatten"):
        _add_fields(
            parent, profile, node["fields"], value, root_response, attachments
        )
        return
    if kind in {"object", "group"}:
        if not isinstance(value, Mapping):
            raise AssertionError(f"{kind} mapping requires an object response")
        child = ET.SubElement(
            parent,
            _qname(profile, node.get("namespace"), node["element"]),
            _attributes(profile, node, root_response),
        )
        _add_fields(
            child, profile, node["fields"], value, root_response, attachments
        )
        return
    if kind == "array":
        if not isinstance(value, list):
            raise AssertionError("array mapping requires a list response")
        _add_array(parent, profile, node, value, root_response, attachments)
        return
    raise AssertionError(f"unsupported mapping kind: {kind}")


def render_profile_xml(
    profile: Mapping[str, Any],
    response: Mapping[str, Any],
    attachments: Mapping[str, Mapping[str, Any]] | None = None,
) -> bytes:
    """Mechanically render a resolved portable profile for conformance testing."""

    _assert_supported_profile(profile)
    if not isinstance(response, Mapping):
        raise AssertionError("root response must be an object")
    _assert_response_fields(
        profile["mapping"]["fields"],
        response,
        path="/",
        source_tree=_response_pointer_tree(profile),
    )
    root_prefix = profile["root"]["namespacePrefix"]
    for prefix, namespace in profile["namespaces"].items():
        if prefix != "default":
            ET.register_namespace(prefix, namespace)
    if root_prefix not in profile["namespaces"]:
        raise AssertionError(f"unknown root namespace prefix: {root_prefix}")

    root = ET.Element(_qname(profile, root_prefix, profile["root"]["element"]))
    for name, value in profile["root"].get("attributes", {}).items():
        if ":" in name:
            prefix, local_name = name.split(":", 1)
        else:
            prefix, local_name = root_prefix, name
        root.set(_qname(profile, prefix, local_name), _text(value))
    _add_fields(
        root,
        profile,
        profile["mapping"]["fields"],
        response,
        response,
        attachments or {},
    )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def validate_exact_xsd(
    xml: bytes,
    fixture: ExactXsdFixture,
    *,
    profile: Mapping[str, Any],
) -> subprocess.CompletedProcess[str]:
    """Validate XML against digest-pinned local XSDs without network access."""

    _assert_supported_profile(profile)
    files = {item.name: item for item in fixture.files}
    if len(files) != len(fixture.files):
        raise AssertionError("pinned XSD fixture names must be unique")
    if fixture.entrypoint not in files:
        raise AssertionError(f"entrypoint is not pinned: {fixture.entrypoint}")
    for item in fixture.files:
        actual = hashlib.sha256(item.path.read_bytes()).hexdigest()
        if actual != item.sha256:
            raise AssertionError(
                f"pinned XSD digest mismatch for {item.name}: expected {item.sha256}, got {actual}"
            )
    actual = profile["xsd"]["sha256"]
    if actual != fixture.official_sha256:
        raise AssertionError(
            "profile official XSD digest mismatch: "
            f"expected {fixture.official_sha256}, got {actual}"
        )
    profile_xsd_name = Path(urlparse(profile["xsd"]["uri"]).path).name
    if profile_xsd_name != fixture.entrypoint:
        raise AssertionError(
            "profile XSD URI does not identify the pinned entrypoint: "
            f"expected {fixture.entrypoint}, got {profile_xsd_name or '<missing>'}"
        )

    xmllint = shutil.which("xmllint")
    if xmllint is None:
        raise AssertionError("xmllint is required for exact-XSD conformance checks")

    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        for item in fixture.files:
            source = item.path.read_text()
            for dependency_name in files:
                for prefix in fixture.dependency_uri_prefixes:
                    source = source.replace(f"{prefix}{dependency_name}", dependency_name)
            (temp / item.name).write_text(source)
        xml_path = temp / "response.xml"
        xml_path.write_bytes(xml)
        return subprocess.run(
            [
                xmllint,
                "--nonet",
                "--noout",
                "--schema",
                str(temp / fixture.entrypoint),
                str(xml_path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
