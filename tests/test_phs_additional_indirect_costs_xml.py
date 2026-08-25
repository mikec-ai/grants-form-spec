from __future__ import annotations

import json
import unittest
from pathlib import Path

from conformance.grants_gov_xml import (
    ExactXsdFixture,
    PinnedXsdFile,
    render_profile_xml,
    validate_exact_xsd,
)


ROOT = Path(__file__).parents[1]
PROFILE = json.loads(
    (
        ROOT
        / "dist/forms/phs-additional-indirect-costs/targets/grants-gov-xml.json"
    ).read_text()
)
FORM_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/phs-additional-indirect-costs-2.0"
SHARED_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_SET = ExactXsdFixture(
    entrypoint="PHS_Additional_IndirectCosts_2_0-V2.0.xsd",
    files=(
        PinnedXsdFile(
            "PHS_Additional_IndirectCosts_2_0-V2.0.xsd",
            FORM_XSDS / "PHS_Additional_IndirectCosts_2_0-V2.0.xsd",
            "ba38a3500b025b0414edbcdbffe80dc12165ceb7a7fb657012d450b2e9682b66",
        ),
        PinnedXsdFile(
            "Attachments-V1.0.xsd",
            SHARED_XSDS / "Attachments-V1.0.xsd",
            "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d",
        ),
        PinnedXsdFile(
            "Global-V1.0.xsd",
            SHARED_XSDS / "Global-V1.0.xsd",
            "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb",
        ),
        PinnedXsdFile(
            "GlobalLibrary-V2.0.xsd",
            SHARED_XSDS / "GlobalLibrary-V2.0.xsd",
            "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
        ),
        PinnedXsdFile(
            "UniversalCodes-V2.0.xsd",
            SHARED_XSDS / "UniversalCodes-V2.0.xsd",
            "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
        ),
    ),
    official_sha256=(
        "ba38a3500b025b0414edbcdbffe80dc12165ceb7a7fb657012d450b2e9682b66"
    ),
)


def response(cost_type: str) -> dict[str, object]:
    return {
        "budgetYears": [
            {
                "budgetPeriodStartDate": "2026-01-01",
                "budgetPeriodEndDate": "2026-12-31",
                "indirectCosts": {
                    "indirectCost": [
                        {
                            "costType": cost_type,
                            "fundRequested": "100.00",
                        }
                    ],
                    "totalIndirectCosts": "100.00",
                },
            }
        ],
        "budgetSummary": {
            "cumulativeTotalFundsRequestedIndirectCost": "100.00"
        },
    }


class PHSAdditionalIndirectCostsXmlTests(unittest.TestCase):
    def test_nonempty_cost_type_validates_against_exact_official_xsd(self) -> None:
        result = validate_exact_xsd(
            render_profile_xml(PROFILE, response("MTDC")), XSD_SET, profile=PROFILE
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_empty_cost_type_fails_exact_official_xsd(self) -> None:
        result = validate_exact_xsd(
            render_profile_xml(PROFILE, response("")), XSD_SET, profile=PROFILE
        )
        self.assertNotEqual(result.returncode, 0, "source XSD accepted empty CostType")


if __name__ == "__main__":
    unittest.main()
