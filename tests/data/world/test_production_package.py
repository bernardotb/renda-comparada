from __future__ import annotations

import bisect
import json
import shutil
import sys
import tempfile
import unittest
from copy import deepcopy
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WORLD_SCRIPTS = ROOT / "scripts/data/world"
sys.path.insert(0, str(WORLD_SCRIPTS))

from production_package import (  # noqa: E402
    CDF_CANDIDATE_SHA256,
    GOLDEN_CASES_SHA256,
    WorldProductionError,
    build_package,
    canonical_json,
    sha256_file,
    validate_cdf,
    validate_engine_manifest,
    validate_negative_mutations,
    validate_price_alignment,
    verify_artifact,
)


class WorldProductionPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.first_result = build_package()
        cls.cdf_path = ROOT / "data/production/world/world-income-cdf-2024.json"
        cls.price_path = ROOT / "data/production/world/world-price-alignment.json"
        cls.manifest_path = ROOT / "data/production/world/world-income-engine-manifest.json"
        cls.golden_path = ROOT / "validation/world/world-income-golden-cases-d070-candidate.json"
        cls.cdf = json.loads(cls.cdf_path.read_text(encoding="utf-8"))
        cls.price = json.loads(cls.price_path.read_text(encoding="utf-8"))
        cls.manifest = json.loads(cls.manifest_path.read_text(encoding="utf-8"))
        cls.golden = json.loads(cls.golden_path.read_text(encoding="utf-8"))

    def lookup(self, value: Decimal) -> tuple[float, float, float]:
        welfare = [Decimal(point[0]) for point in self.cdf["points"]]
        cumulative = [Decimal(point[1]) for point in self.cdf["points"]]
        total = cumulative[-1]
        left = bisect.bisect_left(welfare, value)
        right = bisect.bisect_right(welfare, value)
        below = Decimal(0) if left == 0 else cumulative[left - 1]
        at_or_below = Decimal(0) if right == 0 else cumulative[right - 1]
        return float(below / total), float(at_or_below / total), float(Decimal(1) - below / total)

    def test_contracts_and_schemas_validate(self) -> None:
        validate_cdf(self.cdf)
        validate_price_alignment(self.price)
        validate_engine_manifest(self.manifest)
        validate_negative_mutations()
        for path in (
            "config/schemas/world-income-cdf.schema.json",
            "config/schemas/world-price-alignment.schema.json",
            "config/schemas/world-income-engine-manifest.schema.json",
        ):
            schema = json.loads((ROOT / path).read_text(encoding="utf-8"))
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertFalse(schema["additionalProperties"])

    def test_hashes_sizes_and_cross_references_validate(self) -> None:
        for name, path in (
            ("cdf", self.cdf_path),
            ("priceAlignment", self.price_path),
            ("goldenCases", self.golden_path),
        ):
            verify_artifact(path, self.manifest["artifacts"][name])
        self.assertEqual(self.cdf["source"]["candidateSha256"], CDF_CANDIDATE_SHA256)
        self.assertEqual(self.manifest["artifacts"]["goldenCases"]["sha256"], GOLDEN_CASES_SHA256)

    def test_cdf_preserves_origin_counts_support_and_population(self) -> None:
        stats = self.cdf["statistics"]
        self.assertEqual(stats["sourceBinCount"], 218000)
        self.assertEqual(stats["economyCount"], 218)
        self.assertEqual(stats["pointCount"], 216790)
        self.assertEqual(stats["totalPopulationMillions"], "8141.808945")
        self.assertEqual(stats["minWelfare"], "0.2799999999999999")
        self.assertEqual(stats["maxWelfare"], "3822.84090639671")

    def test_cdf_is_strictly_monotonic_and_has_no_reduction(self) -> None:
        points = self.cdf["points"]
        self.assertEqual(len(points), 216790)
        for previous, current in zip(points, points[1:]):
            self.assertLess(Decimal(previous[0]), Decimal(current[0]))
            self.assertLess(Decimal(previous[1]), Decimal(current[1]))

    def test_all_eleven_golden_cases_reproduce_exact_lookup_semantics(self) -> None:
        self.assertEqual(len(self.golden["cases"]), 11)
        for case in self.golden["cases"]:
            observed = self.lookup(Decimal(case["internationalPppDaily"]))
            self.assertAlmostEqual(observed[0], case["shareBelow"], places=15, msg=case["name"])
            self.assertAlmostEqual(observed[1], case["shareAtOrBelow"], places=15, msg=case["name"])
            self.assertAlmostEqual(observed[2], case["topShare"], places=15, msg=case["name"])

    def test_tie_semantics_are_preserved_without_interpolation(self) -> None:
        tie = next(case for case in self.golden["cases"] if case["kind"] == "tie")
        below, at_or_below, _ = self.lookup(Decimal(tie["internationalPppDaily"]))
        self.assertLess(below, at_or_below)
        between = next(case for case in self.golden["cases"] if case["kind"] == "between-points")
        self.assertEqual(between["shareBelow"], between["shareAtOrBelow"])
        self.assertEqual(self.cdf["methodology"]["interpolation"], "none")
        self.assertEqual(self.cdf["methodology"]["extrapolation"], "none")

    def test_combined_factor_is_derived_from_exact_d069_values(self) -> None:
        combined = Decimal(self.price["brazilPipPpp2021"]) * Decimal(self.price["brazilPipCpi2024Base2021"])
        self.assertEqual(combined, Decimal(self.price["brlPerIntl2024Derived"]))
        self.assertEqual(self.price["combinedFactorState"], "DERIVED")

    def test_frontend_integration_remains_blocked_everywhere(self) -> None:
        self.assertFalse(self.cdf["integration"]["worldFrontendIntegrationAllowed"])
        self.assertFalse(self.price["integration"]["worldFrontendIntegrationAllowed"])
        self.assertFalse(self.manifest["integration"]["worldFrontendIntegrationAllowed"])
        self.assertFalse(self.first_result["worldFrontendIntegrationAllowed"])

    def test_one_byte_change_fails_integrity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            changed = Path(temporary) / self.price_path.name
            payload = bytearray(self.price_path.read_bytes())
            payload[len(payload) // 2] ^= 1
            changed.write_bytes(payload)
            with self.assertRaises(WorldProductionError):
                verify_artifact(changed, self.manifest["artifacts"]["priceAlignment"])

    def test_missing_artifact_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing.json"
            with self.assertRaises(WorldProductionError):
                verify_artifact(missing, self.manifest["artifacts"]["cdf"])

    def test_wrong_pip_year_ppp_and_authorization_are_rejected(self) -> None:
        for field, value in (("pipVersion", "wrong"), ("referenceYear", 2025), ("pppBase", 2017)):
            changed = deepcopy(self.manifest)
            changed["methodology"][field] = value
            with self.assertRaises(WorldProductionError):
                validate_engine_manifest(changed)
        changed = deepcopy(self.manifest)
        changed["integration"]["worldFrontendIntegrationAllowed"] = True
        with self.assertRaises(WorldProductionError):
            validate_engine_manifest(changed)

    def test_generation_is_byte_deterministic(self) -> None:
        before = {path: sha256_file(path) for path in (self.cdf_path, self.price_path, self.manifest_path)}
        second = build_package()
        after = {path: sha256_file(path) for path in before}
        self.assertEqual(before, after)
        self.assertEqual(self.first_result, second)

    def test_canonical_json_rejects_nonfinite_by_validation(self) -> None:
        changed = deepcopy(self.price)
        changed["currentIndex"] = "NaN"
        with self.assertRaises(WorldProductionError):
            validate_price_alignment(changed)
        self.assertTrue(canonical_json(self.manifest).endswith(b"\n"))

    def test_no_legacy_fallback_or_network_calculation_contract(self) -> None:
        manifest_text = self.manifest_path.read_text(encoding="utf-8")
        source_text = (ROOT / "src/world/domain.ts").read_text(encoding="utf-8")
        self.assertEqual(self.manifest["delivery"]["legacyFallback"], "forbidden")
        self.assertNotIn("fetch(", source_text)
        self.assertNotIn("WORLD_CURVE", source_text)
        self.assertNotIn("World Bank", source_text)
        self.assertNotIn("IBGE", source_text)
        self.assertIn('"requestData"', manifest_text)


if __name__ == "__main__":
    unittest.main()
