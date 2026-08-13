from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from decimal import Decimal, getcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PIPELINE_DIR = ROOT / "scripts/data/brazil"
sys.path.insert(0, str(PIPELINE_DIR))

from cdf import IncomeCdf, PipelineError  # noqa: E402
from price_alignment import (  # noqa: E402
    annual_average_index,
    factor_base_to_month,
    income_base_to_current,
    income_current_to_base,
    index_for_official_month,
    load_price_alignment_proposal,
    normalized_series,
    validate_proposal,
)


getcontext().prec = 50


class PriceAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.proposal = load_price_alignment_proposal()
        cls.series = normalized_series(cls.proposal["monthlyIndex"])

    def test_base_average_matches_official_monthly_indices(self) -> None:
        self.assertEqual(
            annual_average_index(self.series, 2025),
            Decimal("7300.8416666666666666666666666666666666666666666667"),
        )

    def test_reference_against_itself_is_one(self) -> None:
        base = annual_average_index(self.series, 2025)
        self.assertEqual(base / base, Decimal(1))

    def test_factor_is_positive_and_matches_proposal(self) -> None:
        factor = factor_base_to_month(self.series, 2025, "2026-07")
        self.assertGreater(factor, 0)
        self.assertEqual(factor, Decimal(self.proposal["factorBaseToCurrent"]))

    def test_round_trip_preserves_income(self) -> None:
        factor = factor_base_to_month(self.series, 2025, "2026-07")
        original = Decimal("6500")
        comparable = income_current_to_base(original, factor)
        self.assertEqual(income_base_to_current(comparable, factor), original)

    def test_zero_remains_zero(self) -> None:
        factor = factor_base_to_month(self.series, 2025, "2026-07")
        self.assertEqual(income_current_to_base(0, factor), Decimal(0))
        self.assertEqual(income_base_to_current(0, factor), Decimal(0))

    def test_missing_official_month_fails_instead_of_projecting(self) -> None:
        with self.assertRaisesRegex(PipelineError, "projeção é proibida"):
            index_for_official_month(self.series, "2026-08")

    def test_proposal_rejects_future_month(self) -> None:
        future = deepcopy(self.proposal)
        future["monthlyIndex"].append({"month": "2026-09", "value": "7700"})
        future["latestOfficialMonth"] = "2026-09"
        future["priceIndexLatestAvailableMonth"] = "2026-09"
        future["priceIndexReferenceMonth"] = "2026-09"
        with self.assertRaisesRegex(PipelineError, "posterior à data de acesso"):
            validate_proposal(future)

    def test_missing_series_fails_safely(self) -> None:
        with self.assertRaisesRegex(PipelineError, "Série de preços ausente"):
            normalized_series([])

    def test_incomplete_base_year_fails_safely(self) -> None:
        incomplete = dict(self.series)
        del incomplete["2025-06"]
        with self.assertRaisesRegex(PipelineError, "Série incompleta"):
            annual_average_index(incomplete, 2025)

    def test_uniform_scaling_preserves_strict_and_inclusive_ranking(self) -> None:
        base = IncomeCdf(
            rdpc=(Decimal("1000"), Decimal("2000"), Decimal("3000")),
            weight_at=(Decimal("20"), Decimal("50"), Decimal("30")),
            cumulative_at_or_below=(Decimal("20"), Decimal("70"), Decimal("100")),
            total_weight=Decimal("100"),
        )
        factor = factor_base_to_month(self.series, 2025, "2026-07")
        scaled = IncomeCdf(
            rdpc=tuple(value * factor for value in base.rdpc),
            weight_at=base.weight_at,
            cumulative_at_or_below=base.cumulative_at_or_below,
            total_weight=base.total_weight,
        )
        current_incomes = (
            Decimal("0"),
            Decimal("2000") * factor,
            Decimal("2500") * factor,
            Decimal("999999"),
        )
        for current_income in current_incomes:
            by_deflating_income = base.get_brazil_income_position(
                income_current_to_base(current_income, factor)
            )
            by_inflating_thresholds = scaled.get_brazil_income_position(current_income)
            self.assertEqual(by_deflating_income, by_inflating_thresholds)

    def test_decimal_calculation_is_deterministic(self) -> None:
        first = factor_base_to_month(self.series, 2025, "2026-07")
        second = factor_base_to_month(self.series, 2025, "2026-07")
        self.assertEqual(first.as_tuple(), second.as_tuple())
        self.assertEqual(validate_proposal(self.proposal)["factorBaseToCurrent"], first)


if __name__ == "__main__":
    unittest.main()
