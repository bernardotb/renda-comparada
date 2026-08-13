from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PIPELINE_DIR = ROOT / "scripts/data/brazil"
sys.path.insert(0, str(PIPELINE_DIR))

from cdf import (  # noqa: E402
    IncomeCdf,
    PipelineError,
    aggregate_metrics,
    group_source_dataset,
    load_cdf_artifact,
    sha256_file,
    write_cdf_artifact,
)
from validate_brazil_cdf import build_golden_cases  # noqa: E402


class CdfUnitTests(unittest.TestCase):
    def tied_fixture(self) -> IncomeCdf:
        return IncomeCdf(
            rdpc=(Decimal("1000"), Decimal("2000"), Decimal("3000")),
            weight_at=(Decimal("20"), Decimal("50"), Decimal("30")),
            cumulative_at_or_below=(Decimal("20"), Decimal("70"), Decimal("100")),
            total_weight=Decimal("100"),
        )

    def artifact_config(self) -> dict:
        return {
            "dataset": "test-cdf",
            "brazilDatasetVersion": "test-v1",
            "methodologyVersion": "1.0.0",
            "sourceYear": 2025,
            "sourceRelease": "test",
            "priceReference": "preços médios de 2025",
            "rdpcDecimalPlaces": 10,
            "weightDecimalPlaces": 8,
        }

    def test_ties_preserve_strict_and_inclusive_semantics(self) -> None:
        position = self.tied_fixture().get_brazil_income_position(2000)
        self.assertAlmostEqual(position.share_below, 0.20)
        self.assertAlmostEqual(position.share_at_or_below, 0.70)
        self.assertAlmostEqual(position.top_share, 0.80)

    def test_between_observed_values_is_step_function(self) -> None:
        position = self.tied_fixture().get_brazil_income_position(2500)
        self.assertAlmostEqual(position.share_below, 0.70)
        self.assertAlmostEqual(position.share_at_or_below, 0.70)

    def test_lower_and_upper_boundaries(self) -> None:
        cdf = self.tied_fixture()
        below = cdf.get_brazil_income_position(999)
        maximum = cdf.get_brazil_income_position(3000)
        above = cdf.get_brazil_income_position(3001)
        self.assertEqual(below.as_dict(), {"shareBelow": 0.0, "shareAtOrBelow": 0.0, "topShare": 1.0})
        self.assertAlmostEqual(maximum.share_below, 0.70)
        self.assertEqual(maximum.share_at_or_below, 1.0)
        self.assertEqual(above.share_below, 1.0)
        self.assertEqual(above.share_at_or_below, 1.0)

    def test_zero_is_preserved(self) -> None:
        cdf = IncomeCdf(
            (Decimal("0"), Decimal("100")),
            (Decimal("10"), Decimal("90")),
            (Decimal("10"), Decimal("100")),
            Decimal("100"),
        )
        position = cdf.get_brazil_income_position(0)
        self.assertEqual(position.share_below, 0.0)
        self.assertAlmostEqual(position.share_at_or_below, 0.1)

    def test_weighted_quantile_uses_empirical_inverse(self) -> None:
        cdf = self.tied_fixture()
        self.assertEqual(cdf.weighted_quantile(0.2), Decimal("1000"))
        self.assertEqual(cdf.weighted_quantile(0.21), Decimal("2000"))
        self.assertEqual(cdf.weighted_quantile(0.7), Decimal("2000"))
        self.assertEqual(cdf.weighted_quantile(0.71), Decimal("3000"))

    def test_aggregate_mean_and_gini_from_unique_values(self) -> None:
        metrics = aggregate_metrics(self.tied_fixture())
        self.assertAlmostEqual(metrics["mean"], 2100.0)
        self.assertAlmostEqual(metrics["gini"], 0.1761904761904762)

    def test_invalid_cdf_and_non_finite_lookup_fail(self) -> None:
        with self.assertRaises(PipelineError):
            IncomeCdf(
                (Decimal("100"), Decimal("100")),
                (Decimal("1"), Decimal("1")),
                (Decimal("1"), Decimal("2")),
                Decimal("2"),
            )
        with self.assertRaises(PipelineError):
            self.tied_fixture().get_brazil_income_position(float("inf"))

    def test_grouping_collapses_equal_income_without_losing_weight(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "source.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle, lineterminator="\n")
                writer.writerow(["rdpc_real_2025", "weight", "UF"])
                writer.writerow(["1000.0000000000", "10.00000000", "35"])
                writer.writerow(["1000.0000000000", "20.00000000", "11"])
                writer.writerow(["2000.0000000000", "30.00000000", "53"])
            config = {"sourceColumns": ["rdpc_real_2025", "weight", "UF"], "sourceRecordCount": 3}
            cdf, diagnostics = group_source_dataset(path, config)
            self.assertEqual(cdf.rdpc, (Decimal("1000.0000000000"), Decimal("2000.0000000000")))
            self.assertEqual(cdf.weight_at, (Decimal("30.00000000"), Decimal("30.00000000")))
            self.assertEqual(diagnostics["uniqueIncomeValues"], 2)

    def test_artifact_is_deterministic_and_round_trips(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.json"
            second = Path(temporary) / "second.json"
            cdf = self.tied_fixture()
            config = self.artifact_config()
            write_cdf_artifact(first, cdf, config, "A" * 64)
            write_cdf_artifact(second, cdf, config, "A" * 64)
            self.assertEqual(sha256_file(first), sha256_file(second))
            loaded, metadata = load_cdf_artifact(first)
            self.assertEqual(loaded, cdf)
            self.assertFalse(metadata["frontendIntegrationAllowed"])

    def test_monotonicity_and_binary_search_match_direct_reference(self) -> None:
        cdf = self.tied_fixture()
        previous = -1.0
        for value in range(0, 4001, 17):
            position = cdf.get_brazil_income_position(value)
            direct_below = sum(
                float(weight)
                for income, weight in zip(cdf.rdpc, cdf.weight_at)
                if income < value
            ) / 100
            direct_at = sum(
                float(weight)
                for income, weight in zip(cdf.rdpc, cdf.weight_at)
                if income <= value
            ) / 100
            self.assertAlmostEqual(position.share_below, direct_below)
            self.assertAlmostEqual(position.share_at_or_below, direct_at)
            self.assertGreaterEqual(position.share_below, previous)
            previous = position.share_below

    def test_golden_cases_carry_versions_hashes_and_exact_math_case(self) -> None:
        config = {
            "methodologyVersion": "1.0.0",
            "brazilDatasetVersion": "test-v1",
            "sourceDatasetSha256": "A" * 64,
            "priceReference": "preços médios de 2025",
            "expected": {"mean": 2100.0},
        }
        golden = build_golden_cases(self.tied_fixture(), config, "B" * 64)
        cases = {case["name"]: case for case in golden["cases"]}
        math_case = cases["householdIncome6500Residents3"]
        self.assertEqual(math_case["householdIncome"], 6500)
        self.assertEqual(math_case["householdSize"], 3)
        self.assertTrue(math_case["rdpcExact"].startswith("2166.666666"))
        self.assertEqual(math_case["datasetSha256"], "A" * 64)
        self.assertEqual(math_case["cdfSha256"], "B" * 64)
        self.assertTrue(golden["frontendIntegrationBlocked"])


if __name__ == "__main__":
    unittest.main()
