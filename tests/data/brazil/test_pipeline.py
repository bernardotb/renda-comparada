from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
PIPELINE_DIR = ROOT / "scripts/data/brazil"
sys.path.insert(0, str(PIPELINE_DIR))

from pipeline import (  # noqa: E402
    DatasetArrays,
    PipelineAccumulator,
    PipelineError,
    load_config,
    parse_layout,
    resolve_deflator,
    sha256_file,
    structural_component,
    weighted_gini,
    write_dataset,
)


class PipelineUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_config = load_config()

    def fixture_config(self, *, records: int = 2, households: int = 1) -> dict:
        config = copy.deepcopy(self.base_config)
        config["expectedStructure"] = {
            "sourceRecords": records,
            "eligiblePersons": records,
            "eligibleHouseholds": households,
            "zeroRecords": 0,
            "negativeRecords": 0,
            "deflatorKeys": 108,
        }
        return config

    def person(
        self,
        order: str,
        *,
        weight: str = "1",
        work: str = "100",
        other: str = "50",
        condition: str = "1",
        components: str = "2",
        nominal: str = "300",
    ) -> dict[str, str]:
        return {
            "Ano": "2025",
            "Trimestre": "1",
            "UF": "35",
            "UPA": "000001",
            "Estrato": "0001",
            "V1008": "01",
            "V1014": "1",
            "V2003": order,
            "V2005": condition,
            "V1032": weight,
            "VD2003": components,
            "VD4019": work,
            "VD4048": other,
            "VD5007": nominal,
        }

    def test_structural_blank_is_zero_but_invalid_text_fails(self) -> None:
        self.assertEqual(structural_component("", "VD4019"), 0.0)
        with self.assertRaises(PipelineError):
            structural_component("abc", "VD4019")

    def test_missing_deflator_fails_safely(self) -> None:
        with self.assertRaises(PipelineError):
            resolve_deflator({}, 2025, 1, 35)

    def test_layout_parser_requires_configured_variables(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            layout = Path(temporary) / "layout.txt"
            layout.write_text(
                "@1 Ano 4. /* Ano */\n@5 UF 2. /* Unidade da Federação */\n",
                encoding="latin-1",
            )
            parsed = parse_layout(layout, ["Ano", "UF"])
            self.assertEqual(parsed["Ano"].start_1_based, 1)
            self.assertEqual(parsed["UF"].width, 2)
            with self.assertRaises(PipelineError):
                parse_layout(layout, ["Ano", "V1032"])

    def test_components_use_distinct_deflators_and_return_to_people(self) -> None:
        config = self.fixture_config()
        accumulator = PipelineAccumulator(config)
        factors = {"CO1": 2.0, "CO1e": 3.0}
        accumulator.add(self.person("01"), factors)
        accumulator.add(self.person("02", weight="2"), factors)
        dataset = accumulator.finalize()
        # (200 de trabalho × 2 + 100 de outras fontes × 3) / 2 pessoas
        np.testing.assert_allclose(dataset.rdpc, [350.0, 350.0])
        np.testing.assert_allclose(dataset.weight, [1.0, 2.0])

    def test_excluded_condition_does_not_enter_household_or_distribution(self) -> None:
        config = self.fixture_config(records=3)
        config["expectedStructure"]["eligiblePersons"] = 2
        accumulator = PipelineAccumulator(config)
        factors = {"CO1": 1.0, "CO1e": 1.0}
        accumulator.add(self.person("01"), factors)
        accumulator.add(self.person("02"), factors)
        accumulator.add(
            self.person("03", condition="17", components="", nominal="", work="", other=""),
            factors,
        )
        dataset = accumulator.finalize()
        self.assertEqual(len(dataset.rdpc), 2)

    def test_inconsistent_declared_household_size_fails(self) -> None:
        config = self.fixture_config()
        accumulator = PipelineAccumulator(config)
        factors = {"CO1": 1.0, "CO1e": 1.0}
        accumulator.add(self.person("01"), factors)
        with self.assertRaises(PipelineError):
            accumulator.add(self.person("02", components="3"), factors)

    def test_invalid_weight_fails(self) -> None:
        accumulator = PipelineAccumulator(self.fixture_config(records=1))
        with self.assertRaises(PipelineError):
            accumulator.add(self.person("01", weight="0", components="1", nominal="150"), {"CO1": 1.0, "CO1e": 1.0})

    def test_zero_income_is_preserved(self) -> None:
        config = self.fixture_config(records=1)
        config["expectedStructure"]["zeroRecords"] = 1
        accumulator = PipelineAccumulator(config)
        accumulator.add(
            self.person("01", work="", other="", components="1", nominal="0"),
            {"CO1": 1.0, "CO1e": 1.0},
        )
        dataset = accumulator.finalize()
        self.assertEqual(dataset.rdpc[0], 0.0)

    def test_deterministic_csv_has_identical_checksum(self) -> None:
        config = self.fixture_config()
        dataset = DatasetArrays(
            rdpc=np.asarray([2.0, 1.0]),
            weight=np.asarray([3.0, 4.0]),
            uf=np.asarray([35, 11]),
            structural={},
        )
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.csv"
            second = Path(temporary) / "second.csv"
            write_dataset(first, config, dataset)
            write_dataset(second, config, dataset)
            self.assertEqual(sha256_file(first), sha256_file(second))
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_weighted_gini_properties(self) -> None:
        equal = weighted_gini(np.asarray([5.0, 5.0]), np.asarray([1.0, 2.0]))
        unequal = weighted_gini(np.asarray([0.0, 10.0]), np.asarray([1.0, 1.0]))
        self.assertAlmostEqual(equal, 0.0)
        self.assertAlmostEqual(unequal, 0.5)


if __name__ == "__main__":
    unittest.main()
