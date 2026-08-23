from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import (
    ExactXsdFixture,
    PinnedXsdFile,
    render_profile_xml,
    validate_exact_xsd,
)


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/AttachmentForm_1_2-V1.2"
ATT_NS = "http://apply.grants.gov/system/Attachments-V1.0"
GLOBAL_NS = "http://apply.grants.gov/system/Global-V1.0"
PROFILE = json.loads(
    (ROOT / "dist/forms/attachment-form/targets/grants-gov-xml.json").read_text()
)
FORM_XSD = (
    ROOT / "tests/fixtures/grants-gov-xsd/attachment-form-1.2/"
    "AttachmentForm_1_2-V1.2.xsd"
)
SHARED_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FILES = {
    "AttachmentForm_1_2-V1.2.xsd": (
        FORM_XSD,
        "dc3ae0af03a52b3a062dc74745b2e355a6c6ce1cc1b53a6c955cd2f972f11466",
    ),
    "Attachments-V1.0.xsd": (
        SHARED_XSDS / "Attachments-V1.0.xsd",
        "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d",
    ),
    "Global-V1.0.xsd": (
        SHARED_XSDS / "Global-V1.0.xsd",
        "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb",
    ),
    "GlobalLibrary-V2.0.xsd": (
        SHARED_XSDS / "GlobalLibrary-V2.0.xsd",
        "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
    ),
    "UniversalCodes-V2.0.xsd": (
        SHARED_XSDS / "UniversalCodes-V2.0.xsd",
        "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
    ),
}
XSD_SET = ExactXsdFixture(
    entrypoint="AttachmentForm_1_2-V1.2.xsd",
    files=tuple(PinnedXsdFile(name, path, digest) for name, (path, digest) in FILES.items()),
    official_sha256="c6b7f40614a2077818f5f3b5df72959f867611b887c5b888005df8adeaa5e8e9",
)


def attachment(number: int) -> dict[str, str]:
    return {
        "fileName": f"attachment-{number}.pdf",
        "mimeType": "application/pdf",
        "fileLocation": f"files/attachment-{number}.pdf",
        "hashValue": hashlib.sha256(f"attachment-{number}".encode()).hexdigest(),
    }


class AttachmentFormXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_empty_form_is_valid_and_emits_no_empty_attachment_wrapper(self) -> None:
        xml = render_profile_xml(PROFILE, {})
        root = ET.fromstring(xml)

        self.assertEqual(root.tag, f"{{{FORM_NS}}}AttachmentForm_1_2")
        self.assertEqual(root.attrib, {f"{{{FORM_NS}}}FormVersion": "1.2"})
        self.assertEqual(list(root), [])
        self.assert_valid(xml)

    def test_single_attachment_uses_the_required_leaf_inside_its_optional_wrapper(self) -> None:
        attachments = {"one": attachment(1)}
        xml = render_profile_xml(PROFILE, {"att1": "one"}, attachments)
        root = ET.fromstring(xml)

        self.assertEqual([child.tag for child in root], [f"{{{FORM_NS}}}ATT1"])
        leaf = root[0][0]
        self.assertEqual(leaf.tag, f"{{{FORM_NS}}}ATT1File")
        self.assertEqual(
            [child.tag for child in leaf],
            [
                f"{{{ATT_NS}}}FileName",
                f"{{{ATT_NS}}}MimeType",
                f"{{{ATT_NS}}}FileLocation",
                f"{{{GLOBAL_NS}}}HashValue",
            ],
        )
        self.assert_valid(xml)

    def test_sparse_and_full_payloads_preserve_source_sequence(self) -> None:
        attachment_map = {f"id-{i}": attachment(i) for i in range(1, 16)}
        sparse = render_profile_xml(
            PROFILE,
            {"att15": "id-15", "att5": "id-5", "att1": "id-1"},
            attachment_map,
        )
        self.assertEqual(
            [child.tag for child in ET.fromstring(sparse)],
            [f"{{{FORM_NS}}}ATT1", f"{{{FORM_NS}}}ATT5", f"{{{FORM_NS}}}ATT15"],
        )
        self.assert_valid(sparse)

        full = render_profile_xml(
            PROFILE,
            {f"att{i}": f"id-{i}" for i in range(1, 16)},
            attachment_map,
        )
        root = ET.fromstring(full)
        self.assertEqual(
            [child.tag for child in root],
            [f"{{{FORM_NS}}}ATT{i}" for i in range(1, 16)],
        )
        self.assertEqual(
            [child[0].tag for child in root],
            [f"{{{FORM_NS}}}ATT{i}File" for i in range(1, 16)],
        )
        self.assert_valid(full)

    def test_removal_and_replacement_are_pure_response_changes(self) -> None:
        attachment_map = {"old": attachment(1), "new": attachment(2)}
        before = ET.fromstring(
            render_profile_xml(PROFILE, {"att3": "old"}, attachment_map)
        )
        replaced = ET.fromstring(
            render_profile_xml(PROFILE, {"att3": "new"}, attachment_map)
        )
        removed = ET.fromstring(render_profile_xml(PROFILE, {}, attachment_map))

        self.assertEqual(before[0][0][0].text, "attachment-1.pdf")
        self.assertEqual(replaced[0][0][0].text, "attachment-2.pdf")
        self.assertEqual(list(removed), [])

    def test_unknown_attachment_reference_fails_closed(self) -> None:
        with self.assertRaisesRegex(AssertionError, "attachment"):
            render_profile_xml(PROFILE, {"att1": "missing"}, {})


if __name__ == "__main__":
    unittest.main()
