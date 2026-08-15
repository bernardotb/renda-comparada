from __future__ import annotations

import json
import sys
import tempfile
import unittest
from copy import deepcopy
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PIPELINE_DIR = ROOT / "scripts/data/brazil"
sys.path.insert(0, str(PIPELINE_DIR))

from pipeline import PipelineError, canonical_json, sha256_file  # noqa: E402
from production_package import (  # noqa: E402
    CDF_PATH,
    ENGINE_PATH,
    ENGINE_SCHEMA_PATH,
    EXPECTED_CDF_SHA256,
    EXPECTED_TEMPORAL_SHARE_BELOW,
    PRICE_PATH,
    PRICE_SCHEMA_PATH,
    REPORT_JSON_PATH,
    REPORT_MD_PATH,
    build_manifests,
    load_json,
    require_file,
    validate_file_hash,
    validate_package,
    validate_schema,
)


class ProductionPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.price_schema = load_json(PRICE_SCHEMA_PATH)
        cls.engine_schema = load_json(ENGINE_SCHEMA_PATH)

    def test_generated_manifests_are_deterministic_and_match_files(self) -> None:
        price_first, engine_first = build_manifests()
        price_second, engine_second = build_manifests()
        self.assertEqual(price_first, price_second)
        self.assertEqual(engine_first, engine_second)
        self.assertEqual(canonical_json(price_first), PRICE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(canonical_json(engine_first), ENGINE_PATH.read_text(encoding="utf-8"))

    def test_manifests_validate_against_versioned_schemas(self) -> None:
        validate_schema(load_json(PRICE_PATH), self.price_schema)
        validate_schema(load_json(ENGINE_PATH), self.engine_schema)

    def test_cross_hashes_and_integration_authorization_match(self) -> None:
        engine = load_json(ENGINE_PATH)
        self.assertEqual(engine["artifacts"]["cdf"]["sha256"], sha256_file(CDF_PATH))
        self.assertEqual(engine["artifacts"]["priceAlignment"]["sha256"], sha256_file(PRICE_PATH))
        self.assertTrue(engine["integration"]["brazilFrontendIntegrationAllowed"])
        self.assertFalse(engine["integration"]["worldFrontendIntegrationAllowed"])

    def test_cdf_historical_bytes_and_flags_remain_immutable(self) -> None:
        self.assertEqual(sha256_file(CDF_PATH), EXPECTED_CDF_SHA256)
        payload = json.loads(CDF_PATH.read_text(encoding="utf-8"))
        self.assertFalse(payload["frontendIntegrationAllowed"])
        self.assertIsNone(payload["userIncomePriceAlignmentMethod"])

    def test_current_nominal_golden_case_is_reproduced(self) -> None:
        engine = load_json(ENGINE_PATH)
        case = engine["goldenCases"]["currentNominalCase"]
        self.assertEqual(case["nominalHouseholdIncome"], "6500")
        self.assertEqual(case["eligibleResidents"], 3)
        self.assertEqual(
            Decimal(case["comparableRdpc2025"]),
            Decimal("2065.6892157046249708174325521763992433498932161068"),
        )
        self.assertEqual(case["shareBelow"], EXPECTED_TEMPORAL_SHARE_BELOW)
        self.assertEqual((case["displayPercentile"], case["displayTop"]), (69, 31))

    def test_schema_rejects_missing_required_field(self) -> None:
        invalid = deepcopy(load_json(PRICE_PATH))
        del invalid["factorBaseToCurrent"]
        with self.assertRaisesRegex(PipelineError, "campos ausentes"):
            validate_schema(invalid, self.price_schema)

    def test_hash_validator_rejects_tampered_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "tampered.json"
            path.write_text("{}\n", encoding="utf-8", newline="\n")
            with self.assertRaisesRegex(PipelineError, "SHA-256 divergente"):
                validate_file_hash(path, "A" * 64)

    def test_missing_artifact_fails_safely(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing.json"
            with self.assertRaisesRegex(PipelineError, "obrigatório ausente"):
                require_file(missing)

    def test_validation_report_is_derived_from_explicit_checks(self) -> None:
        report = validate_package()
        stored = load_json(REPORT_JSON_PATH)
        self.assertEqual(report, stored)
        self.assertEqual(report["summary"], {"total": 44, "pass": 44, "fail": 0, "status": "PASS"})
        self.assertEqual(
            report["historicalClaim"]["status"],
            "NOT_REPRODUCIBLE_AS_HISTORICAL_SUITE",
        )
        markdown = REPORT_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("PASS — 44/44 checks", markdown)
        self.assertEqual(len(report["checks"]), len({check["id"] for check in report["checks"]}))


if __name__ == "__main__":
    unittest.main()
