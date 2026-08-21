from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PIPELINE_DIR = ROOT / "scripts/data/world"
sys.path.insert(0, str(PIPELINE_DIR))

from d070 import (  # noqa: E402
    conversion_factors,
    daily_to_nominal,
    display_policy,
    load_config,
    load_ipca,
    nominal_to_daily,
    presentation_decision,
    run,
)


GOLDEN_SHA256 = "6EA8FB10D9BCE16380E5F311EFA789AC22EEA44BEFF119C33C61B1B0578FF779"
GOLDEN_PATH = ROOT / "validation/world/world-income-golden-cases-d070-candidate.json"
D070_CONFIG = load_config()
EXTERNAL_INPUT_KEYS = ("pppRawPath", "cpiRawPath", "ipcaRawPath")
EXTERNAL_INPUTS_HYDRATED = all((ROOT / D070_CONFIG[key]).is_file() for key in EXTERNAL_INPUT_KEYS)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_frozen_golden() -> dict[str, object]:
    return json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))


class D070ContractTests(unittest.TestCase):
    def test_frozen_golden_fixture_has_canonical_hash_and_case_count(self) -> None:
        self.assertEqual(sha256_file(GOLDEN_PATH), GOLDEN_SHA256)
        golden = load_frozen_golden()
        self.assertEqual(len(golden["cases"]), 11)
        kinds = {case["kind"] for case in golden["cases"]}
        self.assertTrue(
            {"nominal", "exact-observed", "between-points", "below-minimum", "at-maximum", "above-maximum", "tie"}
            <= kinds
        )
        above = next(case for case in golden["cases"] if case["kind"] == "above-maximum")
        self.assertEqual(above["shareBelow"], 1.0)
        self.assertEqual(above["topShare"], 0.0)

    def test_conversion_round_trip_uses_exact_d069_factors(self) -> None:
        ipca = {
            "average2024": Decimal("6952.07333333333333333333333333333333333333333333333333333333"),
            "current": Decimal("7657.7300000000000"),
        }
        factors = conversion_factors(D070_CONFIG, ipca)
        income = Decimal("6500")
        daily = nominal_to_daily(income, 3, factors)
        self.assertLess(abs(daily_to_nominal(daily, 3, factors) - income), Decimal("1e-50"))
        self.assertEqual(factors["combined"], Decimal("2.92248979025310406149724542264"))

    def test_display_policy_is_derived_from_error_and_never_emits_top_zero(self) -> None:
        policy = display_policy(Decimal("0.022516991848919865"))
        self.assertTrue(policy["basis"]["errorBelowOneDecimalHalfIncrement"])
        self.assertEqual(policy["basis"]["d068MaxAbsErrorPp"], "0.022516991848919865")
        self.assertIn("never display TOP 0%", policy["maximumAndAbove"])
        self.assertEqual(policy["status"], "CANONICAL_BY_D070")

    def test_display_top_greater_than_one_percent(self) -> None:
        result = presentation_decision("0.0101", "0.022516991848920")
        self.assertEqual(result["displayClass"], "MAIN_INTEGER_COMPLEMENTARY")

    def test_display_top_equal_one_percent(self) -> None:
        result = presentation_decision("0.01", "0.022516991848920")
        self.assertEqual(result["displayClass"], "MAIN_INTEGER_COMPLEMENTARY")
        self.assertEqual(result["topDisplayPp"], "1")

    def test_display_top_immediately_below_one_percent(self) -> None:
        result = presentation_decision("0.009999", "0.022516991848920")
        self.assertEqual(result["displayClass"], "UPPER_TAIL_ONE_DECIMAL")

    def test_display_top_greater_than_point_one_percent(self) -> None:
        result = presentation_decision("0.001001", "0.022516991848920")
        self.assertEqual(result["displayClass"], "UPPER_TAIL_ONE_DECIMAL")

    def test_display_top_equal_point_one_percent(self) -> None:
        result = presentation_decision("0.001", "0.022516991848920")
        self.assertEqual(result["displayClass"], "UPPER_TAIL_ONE_DECIMAL")
        self.assertEqual(result["topDisplayPp"], "0.1")

    def test_display_top_below_point_one_without_uncertainty_margin(self) -> None:
        result = presentation_decision("0.0009", "0.022516991848920")
        self.assertEqual(result["displayClass"], "UPPER_EXTREME_APPROX_0_1")
        self.assertEqual(result["headline"], "aproximadamente 0,1%")

    def test_display_top_safely_below_point_one_with_uncertainty_margin(self) -> None:
        result = presentation_decision("0.0007", "0.022516991848920")
        self.assertLess(Decimal(result["topPercentInternal"]) + Decimal(result["maxErrorPp"]), Decimal("0.1"))
        self.assertEqual(result["displayClass"], "UPPER_EXTREME_LESS_THAN_0_1")
        self.assertEqual(result["headline"], "menos de 0,1%")

    def test_display_never_produces_top_zero(self) -> None:
        result = presentation_decision("0", "0.022516991848920", "at-maximum")
        self.assertEqual(result["displayClass"], "UPPER_SUPPORT_LIMIT")
        self.assertNotIn("TOP 0%", result["headline"])

    def test_display_never_uses_top_one_hundred_as_headline(self) -> None:
        result = presentation_decision("1", "0.022516991848920", "at-minimum")
        self.assertEqual(result["displayClass"], "AT_MINIMUM")
        self.assertNotIn("TOP 100%", result["headline"])

    def test_display_above_maximum_does_not_extrapolate(self) -> None:
        result = presentation_decision("0", "0.022516991848920", "above-maximum")
        self.assertEqual(result["displayClass"], "OUTSIDE_UPPER_SUPPORT")
        self.assertFalse(result["extrapolated"])

    def test_display_below_minimum_does_not_extrapolate(self) -> None:
        result = presentation_decision("1", "0.022516991848920", "below-minimum")
        self.assertEqual(result["displayClass"], "OUTSIDE_LOWER_SUPPORT")
        self.assertFalse(result["extrapolated"])

    def test_frozen_tie_fixture_preserves_below_and_at_or_below(self) -> None:
        golden = load_frozen_golden()
        tie = next(case for case in golden["cases"] if case["kind"] == "tie")
        self.assertLess(tie["shareBelow"], tie["shareAtOrBelow"])


@unittest.skipUnless(EXTERNAL_INPUTS_HYDRATED, "external source inputs not hydrated")
class D070ReproductionTests(unittest.TestCase):
    def test_hydrated_ipca_evidence_has_exact_average_and_current_month(self) -> None:
        ipca = load_ipca(D070_CONFIG)
        self.assertEqual(ipca["average2024"], Decimal("6952.07333333333333333333333333333333333333333333333333333333"))
        self.assertEqual(ipca["current"], Decimal("7657.7300000000000"))
        self.assertEqual(ipca["rawCurrentValue"], "7657.7300000000000")

    def test_hydrated_generation_uses_temporary_outputs_and_matches_frozen_fixture(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".d070-reproduction-", dir=ROOT) as temporary:
            temporary_path = Path(temporary)
            relative = temporary_path.relative_to(ROOT).as_posix()
            config = dict(D070_CONFIG)
            config.update(
                {
                    "goldenCasesPath": f"{relative}/golden.json",
                    "validationPath": f"{relative}/validation.json",
                    "reportPath": f"{relative}/validation.md",
                }
            )
            config_path = temporary_path / "config.json"
            config_path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")

            report = run(config_path)
            generated_golden = temporary_path / "golden.json"
            self.assertEqual(generated_golden.read_bytes(), GOLDEN_PATH.read_bytes())
            self.assertEqual(sha256_file(generated_golden), GOLDEN_SHA256)
            self.assertEqual(report["status"], "PASS_CANONIZED")
            self.assertEqual(report["goldenCases"]["count"], 11)
            self.assertTrue(all(value is False for value in report["protectedState"].values()))


if __name__ == "__main__":
    unittest.main()
