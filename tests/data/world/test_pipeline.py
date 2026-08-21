from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PIPELINE_DIR = ROOT / "scripts/data/world"
sys.path.insert(0, str(PIPELINE_DIR))

from pipeline import (  # noqa: E402
    WorldCdf,
    WorldPipelineError,
    build_cdf,
    candidate_document,
    canonical_json,
    compare_checkpoints,
    distribution_statistics,
    process_source,
)


class WorldPipelineTests(unittest.TestCase):
    def fixture(self) -> WorldCdf:
        return WorldCdf(
            welfare=(Decimal("0"), Decimal("2"), Decimal("5")),
            weight_at=(Decimal("10"), Decimal("30"), Decimal("60")),
            cumulative_at_or_below=(Decimal("10"), Decimal("40"), Decimal("100")),
            total_weight=Decimal("100"),
        )

    def test_lookup_preserves_ties_and_boundaries(self) -> None:
        cdf = self.fixture()
        self.assertEqual(cdf.lookup(-1), {"shareBelow": 0.0, "shareAtOrBelow": 0.0, "topShare": 1.0})
        self.assertEqual(cdf.lookup(0), {"shareBelow": 0.0, "shareAtOrBelow": 0.1, "topShare": 1.0})
        self.assertEqual(cdf.lookup(2), {"shareBelow": 0.1, "shareAtOrBelow": 0.4, "topShare": 0.9})
        self.assertEqual(cdf.lookup(6), {"shareBelow": 1.0, "shareAtOrBelow": 1.0, "topShare": 0.0})

    def test_weighted_quantiles_use_empirical_inverse(self) -> None:
        cdf = self.fixture()
        self.assertEqual(cdf.weighted_quantile("0"), Decimal("0"))
        self.assertEqual(cdf.weighted_quantile("0.1"), Decimal("0"))
        self.assertEqual(cdf.weighted_quantile("0.11"), Decimal("2"))
        self.assertEqual(cdf.weighted_quantile("0.4"), Decimal("2"))
        self.assertEqual(cdf.weighted_quantile("0.41"), Decimal("5"))

    def test_build_groups_equal_welfare(self) -> None:
        cdf = build_cdf({Decimal("2"): Decimal("10"), Decimal("5"): Decimal("20")})
        self.assertEqual(cdf.total_weight, Decimal("30"))
        self.assertEqual(cdf.cumulative_at_or_below, (Decimal("10"), Decimal("30")))

    def test_invalid_support_or_weight_fails(self) -> None:
        with self.assertRaises(WorldPipelineError):
            build_cdf({Decimal("1"): Decimal("0")})
        with self.assertRaises(WorldPipelineError):
            self.fixture().weighted_quantile("1.1")

    def test_checkpoint_comparison_is_independent(self) -> None:
        official = [
            {"povertyLine": 2, "headcount": 0.12},
            {"povertyLine": 5, "headcount": 0.41},
        ]
        rows, metrics = compare_checkpoints(self.fixture(), official)
        self.assertAlmostEqual(rows[0]["candidateShareBelow"], 0.1)
        self.assertAlmostEqual(rows[0]["errorSignedPp"], -2)
        self.assertAlmostEqual(rows[1]["candidateShareBelow"], 0.4)
        self.assertAlmostEqual(metrics["maxAbsErrorPp"], 2)

    def test_process_source_validates_year_keys_and_bins(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            raw = Path(temporary) / "raw.csv"
            processed = Path(temporary) / "processed.csv"
            columns = ["year", "code", "region_name", "region_code", "regionpcn_name", "regionpcn_code", "quantile", "welf", "pop", "pipvintage"]
            with raw.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
                writer.writeheader()
                for quantile in range(1, 1001):
                    writer.writerow({"year": 2024, "code": "AAA", "region_name": "A", "region_code": "A", "regionpcn_name": "A", "regionpcn_code": "A", "quantile": quantile, "welf": quantile, "pop": "0.001", "pipvintage": "BUILD"})
                writer.writerow({"year": 2025, "code": "AAA", "region_name": "A", "region_code": "A", "regionpcn_name": "A", "regionpcn_code": "A", "quantile": 1, "welf": 1, "pop": "0.001", "pipvintage": "BUILD"})
                for quantile in range(1, 1001):
                    writer.writerow({"year": 2024, "code": "BBB", "region_name": "B", "region_code": "B", "regionpcn_name": "B", "regionpcn_code": "B", "quantile": quantile, "welf": quantile, "pop": "0.002", "pipvintage": "BUILD"})
            cdf, diagnostics = process_source(raw, processed, {"referenceYear": 2024, "productionBuild": "BUILD", "sourceColumns": columns})
            self.assertEqual(diagnostics["sourceRows2024"], 2000)
            self.assertEqual(diagnostics["economies2024"], 2)
            self.assertEqual(cdf.total_weight, Decimal("3.000"))

    def test_candidate_is_deterministic_and_blocks_frontend(self) -> None:
        cdf = self.fixture()
        diagnostics = {"sourceRows2024": 3, "economies2024": 1, "binsPerEconomy": 1000, "duplicateKeys": 0, "zeroWelfareRows": 1, "uniqueWelfarePoints": 3, "totalPopulationMillions": 100.0, "minWelfare": 0.0, "maxWelfare": 5.0, "processedSha256": "B" * 64, "processedSizeBytes": 10}
        config = {"provider": "World Bank", "dataset": "fixture", "catalogUrl": "https://example.test", "resourceId": "R", "sourceFileName": "fixture.csv", "sourceUrl": "https://example.test/file", "sourceLastUpdated": "2026-01-01", "accessedAt": "2026-01-02", "license": "CC0", "pipVersion": "v", "productionBuild": "b", "referenceYear": 2024, "pppBase": 2021, "unit": "unit", "populationUnit": "millions"}
        source = {"sizeBytes": 10, "sha256": "A" * 64}
        first = candidate_document(cdf, diagnostics, distribution_statistics(cdf), source, config)
        second = candidate_document(cdf, diagnostics, distribution_statistics(cdf), source, config)
        self.assertEqual(canonical_json(first), canonical_json(second))
        self.assertFalse(first["frontendIntegrationAllowed"])
        self.assertEqual(json.loads(canonical_json(first))["status"], "CANDIDATE")


if __name__ == "__main__":
    unittest.main()
