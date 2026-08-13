"""CDF empírica ponderada e lookup brasileiro, independentes do frontend."""

from __future__ import annotations

import bisect
import csv
import json
import math
import os
import tempfile
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Mapping

from pipeline import ROOT, PipelineError, canonical_json, sha256_file


DEFAULT_CDF_CONFIG_PATH = ROOT / "config/brazil-cdf-2025.json"
DEFAULT_CDF_OUTPUT_DIR = ROOT / "data/production/brazil"


@dataclass(frozen=True)
class IncomePosition:
    share_below: float
    share_at_or_below: float
    top_share: float

    def as_dict(self) -> dict[str, float]:
        return {
            "shareBelow": self.share_below,
            "shareAtOrBelow": self.share_at_or_below,
            "topShare": self.top_share,
        }


@dataclass(frozen=True)
class IncomeCdf:
    rdpc: tuple[Decimal, ...]
    weight_at: tuple[Decimal, ...]
    cumulative_at_or_below: tuple[Decimal, ...]
    total_weight: Decimal

    def __post_init__(self) -> None:
        size = len(self.rdpc)
        if not size or len(self.weight_at) != size or len(self.cumulative_at_or_below) != size:
            raise PipelineError("Vetores da CDF ausentes ou com tamanhos divergentes")
        if any(left >= right for left, right in zip(self.rdpc, self.rdpc[1:])):
            raise PipelineError("Valores de RDPC da CDF não estão estritamente ordenados")
        if any(weight <= 0 for weight in self.weight_at):
            raise PipelineError("CDF contém peso não positivo")
        if any(
            left >= right
            for left, right in zip(
                self.cumulative_at_or_below, self.cumulative_at_or_below[1:]
            )
        ):
            raise PipelineError("Peso acumulado da CDF não é estritamente crescente")
        if self.cumulative_at_or_below[-1] != self.total_weight:
            raise PipelineError("Peso acumulado final não corresponde ao peso total")

    def get_brazil_income_position(self, value: float | Decimal | str) -> IncomePosition:
        income = decimal_value(value, "rdpc")
        left = bisect.bisect_left(self.rdpc, income)
        right = bisect.bisect_right(self.rdpc, income)
        below_weight = Decimal(0) if left == 0 else self.cumulative_at_or_below[left - 1]
        at_or_below_weight = (
            Decimal(0) if right == 0 else self.cumulative_at_or_below[right - 1]
        )
        share_below = float(below_weight / self.total_weight)
        share_at_or_below = float(at_or_below_weight / self.total_weight)
        top_share = 1.0 - share_below
        position = IncomePosition(share_below, share_at_or_below, top_share)
        validate_position(position)
        return position

    def weighted_quantile(self, probability: float | Decimal) -> Decimal:
        p = decimal_value(probability, "probabilidade")
        if p < 0 or p > 1:
            raise PipelineError("Probabilidade do quantil deve estar entre 0 e 1")
        if p == 0:
            return self.rdpc[0]
        target = p * self.total_weight
        index = bisect.bisect_left(self.cumulative_at_or_below, target)
        return self.rdpc[min(index, len(self.rdpc) - 1)]


def load_cdf_config(path: Path = DEFAULT_CDF_CONFIG_PATH) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "dataset",
        "brazilDatasetVersion",
        "methodologyVersion",
        "sourceYear",
        "sourceRelease",
        "priceReference",
        "sourceDatasetPath",
        "sourceDatasetManifestPath",
        "sourceDatasetSha256",
        "sourceRecordCount",
        "sourceColumns",
        "expected",
        "tolerances",
        "quantiles",
    }
    missing = sorted(required - set(config))
    if missing:
        raise PipelineError(f"Configuração da CDF incompleta: {missing}")
    return config


def repository_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise PipelineError(f"Caminho fora da raiz canônica: {relative}")
    return path


def decimal_value(value: float | Decimal | str, label: str) -> Decimal:
    try:
        parsed = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise PipelineError(f"{label} não numérico: {value!r}") from error
    if not parsed.is_finite():
        raise PipelineError(f"{label} não finito: {value!r}")
    return parsed


def verify_source_dataset(config: Mapping[str, Any]) -> tuple[Path, Mapping[str, Any]]:
    source_path = repository_path(config["sourceDatasetPath"])
    manifest_path = repository_path(config["sourceDatasetManifestPath"])
    if not source_path.is_file() or not manifest_path.is_file():
        raise PipelineError("Dataset intermediário ou manifesto da Fase 1D ausente")
    checksum = sha256_file(source_path)
    expected_checksum = str(config["sourceDatasetSha256"]).upper()
    if checksum != expected_checksum:
        raise PipelineError(f"SHA-256 do dataset fonte divergiu: {checksum}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checks = {
        "datasetSha256": expected_checksum,
        "recordCount": int(config["sourceRecordCount"]),
        "priceReference": config["priceReference"],
        "methodologyVersion": config["methodologyVersion"],
    }
    for field, expected in checks.items():
        if manifest.get(field) != expected:
            raise PipelineError(
                f"Manifesto intermediário divergiu em {field}: {manifest.get(field)!r}"
            )
    return source_path, manifest


def group_source_dataset(
    source_path: Path, config: Mapping[str, Any]
) -> tuple[IncomeCdf, dict[str, Any]]:
    grouped: dict[Decimal, Decimal] = {}
    records = 0
    zero_records = 0
    with source_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(config["sourceColumns"]):
            raise PipelineError(f"Schema do dataset fonte divergiu: {reader.fieldnames}")
        for row_number, row in enumerate(reader, start=2):
            income = decimal_value(row["rdpc_real_2025"], "rdpc_real_2025")
            weight = decimal_value(row["weight"], "weight")
            if income < 0:
                raise PipelineError(f"RDPC negativo na linha {row_number}")
            if weight <= 0:
                raise PipelineError(f"Peso não positivo na linha {row_number}")
            try:
                int(row["UF"])
            except ValueError as error:
                raise PipelineError(f"UF inválida na linha {row_number}") from error
            grouped[income] = grouped.get(income, Decimal(0)) + weight
            records += 1
            zero_records += int(income == 0)
    if records != int(config["sourceRecordCount"]):
        raise PipelineError(f"Contagem fonte divergiu: {records}")

    incomes = tuple(sorted(grouped))
    weights = tuple(grouped[income] for income in incomes)
    cumulative: list[Decimal] = []
    running = Decimal(0)
    for weight in weights:
        running += weight
        cumulative.append(running)
    cdf = IncomeCdf(incomes, weights, tuple(cumulative), running)
    diagnostics = {
        "sourceRecords": records,
        "uniqueIncomeValues": len(incomes),
        "zeroRecords": zero_records,
        "zeroWeight": float(grouped.get(Decimal(0), Decimal(0))),
        "minRdpc": float(incomes[0]),
        "maxRdpc": float(incomes[-1]),
    }
    return cdf, diagnostics


def validate_position(position: IncomePosition) -> None:
    values = (position.share_below, position.share_at_or_below, position.top_share)
    if any(not math.isfinite(value) or value < 0 or value > 1 for value in values):
        raise PipelineError(f"Posição fora dos limites: {position}")
    if position.share_below > position.share_at_or_below:
        raise PipelineError("shareBelow excede shareAtOrBelow")
    if not math.isclose(position.top_share, 1 - position.share_below, abs_tol=1e-15):
        raise PipelineError("topShare não corresponde a 1 - shareBelow")


def aggregate_metrics(cdf: IncomeCdf) -> dict[str, Any]:
    total_income = sum(
        (income * weight for income, weight in zip(cdf.rdpc, cdf.weight_at)),
        Decimal(0),
    )
    mean = total_income / cdf.total_weight
    cumulative_income = Decimal(0)
    lorenz_sum = Decimal(0)
    for income, weight in zip(cdf.rdpc, cdf.weight_at):
        previous = cumulative_income
        cumulative_income += income * weight
        lorenz_sum += weight * (cumulative_income + previous)
    gini = Decimal(1) - lorenz_sum / (total_income * cdf.total_weight)
    zero_position = cdf.get_brazil_income_position(0)
    return {
        "uniqueIncomeValues": len(cdf.rdpc),
        "totalWeight": float(cdf.total_weight),
        "mean": float(mean),
        "gini": float(gini),
        "minRdpc": float(cdf.rdpc[0]),
        "maxRdpc": float(cdf.rdpc[-1]),
        "zeroWeight": float(cdf.weight_at[0]) if cdf.rdpc[0] == 0 else 0.0,
        "zeroWeightShare": zero_position.share_at_or_below,
    }


def validate_cdf(
    cdf: IncomeCdf, diagnostics: Mapping[str, Any], config: Mapping[str, Any]
) -> dict[str, Any]:
    metrics = aggregate_metrics(cdf)
    expected = config["expected"]
    tolerances = config["tolerances"]
    exact_checks = {
        "uniqueIncomeValues": int(expected["uniqueIncomeValues"]),
        "zeroRecords": int(expected["zeroRecords"]),
    }
    for name, expected_value in exact_checks.items():
        actual = metrics[name] if name in metrics else diagnostics[name]
        if actual != expected_value:
            raise PipelineError(f"Validação exata falhou para {name}: {actual}")
    tolerance_checks = {
        "totalWeight": (metrics["totalWeight"], expected["totalWeight"], tolerances["weight"]),
        "mean": (metrics["mean"], expected["mean"], tolerances["mean"]),
        "gini": (metrics["gini"], expected["gini"], tolerances["gini"]),
        "zeroWeight": (metrics["zeroWeight"], expected["zeroWeight"], tolerances["weight"]),
        "minRdpc": (metrics["minRdpc"], expected["minRdpc"], tolerances["mean"]),
        "maxRdpc": (metrics["maxRdpc"], expected["maxRdpc"], tolerances["mean"]),
    }
    for name, (actual, expected_value, tolerance) in tolerance_checks.items():
        if abs(actual - expected_value) > tolerance:
            raise PipelineError(f"Benchmark da CDF falhou para {name}: {actual}")

    quantiles: dict[str, float] = {}
    for label, expected_value in config["quantiles"].items():
        probability = Decimal(label[1:]) / Decimal(100)
        calculated = float(cdf.weighted_quantile(probability))
        quantiles[label] = calculated
        if expected_value is not None and abs(calculated - float(expected_value)) > 1e-9:
            raise PipelineError(f"Quantil {label} divergiu: {calculated}")

    sample_count = min(10000, len(cdf.rdpc))
    step = max(1, len(cdf.rdpc) // sample_count)
    sample_values = list(cdf.rdpc[::step])
    sample_values.extend(
        [cdf.rdpc[0] - Decimal(1), Decimal(0), cdf.rdpc[-1], cdf.rdpc[-1] + Decimal(1)]
    )
    previous_below = -1.0
    previous_at_or_below = -1.0
    for value in sorted(set(sample_values)):
        position = cdf.get_brazil_income_position(value)
        if position.share_below < previous_below or position.share_at_or_below < previous_at_or_below:
            raise PipelineError("Monotonicidade da CDF falhou")
        previous_below = position.share_below
        previous_at_or_below = position.share_at_or_below

    zero = cdf.get_brazil_income_position(0)
    maximum = cdf.get_brazil_income_position(cdf.rdpc[-1])
    above = cdf.get_brazil_income_position(cdf.rdpc[-1] + Decimal(1))
    if zero.share_below != 0 or zero.share_at_or_below <= 0:
        raise PipelineError("Semântica de renda zero falhou")
    if maximum.share_below >= 1 or maximum.share_at_or_below != 1:
        raise PipelineError("Semântica do máximo observado falhou")
    if above.share_below != 1 or above.share_at_or_below != 1:
        raise PipelineError("Semântica acima do máximo falhou")
    return {"status": "PASS", "metrics": metrics, "quantiles": quantiles}


def decimal_text(value: Decimal, places: int) -> str:
    text = f"{value:.{places}f}".rstrip("0").rstrip(".")
    return text if text and text != "-0" else "0"


def write_decimal_array(handle: Any, values: Iterable[Decimal], places: int) -> None:
    handle.write("[")
    first = True
    for value in values:
        if not first:
            handle.write(",")
        handle.write(decimal_text(value, places))
        first = False
    handle.write("]")


def write_cdf_artifact(
    path: Path, cdf: IncomeCdf, config: Mapping[str, Any], source_sha: str
) -> None:
    metadata = {
        "dataset": config["dataset"],
        "brazilDatasetVersion": config["brazilDatasetVersion"],
        "methodologyVersion": config["methodologyVersion"],
        "sourceDatasetSha256": source_sha,
        "sourceYear": config["sourceYear"],
        "sourceRelease": config["sourceRelease"],
        "priceReference": config["priceReference"],
        "populationUnit": "pessoas elegíveis ponderadas por V1032",
        "inputUnit": "RDPC mensal em reais, a preços médios de 2025",
        "lookupSemantics": {
            "shareBelow": "peso com RDPC < x / peso total",
            "shareAtOrBelow": "peso com RDPC <= x / peso total",
            "topShare": "1 - shareBelow",
            "interpolation": "nenhuma; CDF empírica em degraus",
        },
        "userIncomePriceAlignmentMethod": None,
        "frontendIntegrationAllowed": False,
        "uniqueIncomeValues": len(cdf.rdpc),
        "totalWeight": float(cdf.total_weight),
        "representation": {
            "rdpc": "valores únicos crescentes",
            "weightAt": "peso exatamente no valor",
            "cumAtOrBelow": "peso acumulado até e inclusive o valor; cumBelow é o item anterior",
        },
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("{")
        for index, (key, value) in enumerate(metadata.items()):
            if index:
                handle.write(",")
            handle.write(json.dumps(key, ensure_ascii=False))
            handle.write(":")
            handle.write(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
        handle.write(',"rdpc":')
        write_decimal_array(handle, cdf.rdpc, int(config["rdpcDecimalPlaces"]))
        handle.write(',"weightAt":')
        write_decimal_array(handle, cdf.weight_at, int(config["weightDecimalPlaces"]))
        handle.write(',"cumAtOrBelow":')
        write_decimal_array(
            handle, cdf.cumulative_at_or_below, int(config["weightDecimalPlaces"])
        )
        handle.write("}\n")


def load_cdf_artifact(path: Path) -> tuple[IncomeCdf, Mapping[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"), parse_float=Decimal)
    required = {"rdpc", "weightAt", "cumAtOrBelow", "totalWeight"}
    missing = sorted(required - set(payload))
    if missing:
        raise PipelineError(f"Artefato CDF incompleto: {missing}")
    cdf = IncomeCdf(
        tuple(decimal_value(value, "rdpc") for value in payload["rdpc"]),
        tuple(decimal_value(value, "weightAt") for value in payload["weightAt"]),
        tuple(decimal_value(value, "cumAtOrBelow") for value in payload["cumAtOrBelow"]),
        decimal_value(payload["totalWeight"], "totalWeight"),
    )
    return cdf, payload


def build_cdf(
    config_path: Path = DEFAULT_CDF_CONFIG_PATH,
    output_dir: Path = DEFAULT_CDF_OUTPUT_DIR,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    output_dir = output_dir.resolve()
    config = load_cdf_config(config_path)
    source_path, _ = verify_source_dataset(config)
    source_sha = sha256_file(source_path)
    cdf, diagnostics = group_source_dataset(source_path, config)
    validation = validate_cdf(cdf, diagnostics, config)

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="brazil-cdf-", dir=output_dir.parent) as temporary:
        temporary_dir = Path(temporary)
        cdf_path = temporary_dir / config["cdfFileName"]
        manifest_path = temporary_dir / config["cdfManifestFileName"]
        write_cdf_artifact(cdf_path, cdf, config, source_sha)
        cdf_sha = sha256_file(cdf_path)
        cdf_size = cdf_path.stat().st_size
        source_size = source_path.stat().st_size
        manifest = {
            "dataset": config["dataset"],
            "brazilDatasetVersion": config["brazilDatasetVersion"],
            "sourceDatasetSha256": source_sha,
            "sourceYear": config["sourceYear"],
            "sourceRelease": config["sourceRelease"],
            "priceReference": config["priceReference"],
            "methodologyVersion": config["methodologyVersion"],
            "sourceRecords": diagnostics["sourceRecords"],
            "uniqueIncomeValues": len(cdf.rdpc),
            "totalWeight": validation["metrics"]["totalWeight"],
            "minRdpc": validation["metrics"]["minRdpc"],
            "maxRdpc": validation["metrics"]["maxRdpc"],
            "cdfSha256": cdf_sha,
            "cdfSizeBytes": cdf_size,
            "sourceDatasetSizeBytes": source_size,
            "recordReductionPercent": (1 - len(cdf.rdpc) / diagnostics["sourceRecords"]) * 100,
            "byteReductionPercent": (1 - cdf_size / source_size) * 100,
            "generatedBy": "scripts/data/brazil/build_brazil_cdf.py",
            "generatedAt": None,
            "generatedAtPolicy": "omitido do artefato determinístico",
            "containsIndividualData": False,
            "userIncomePriceAlignmentMethod": None,
            "frontendIntegrationBlocked": True,
            "validation": validation,
        }
        manifest_path.write_text(canonical_json(manifest), encoding="utf-8", newline="\n")
        manifest_sha = sha256_file(manifest_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        final_cdf = output_dir / cdf_path.name
        final_manifest = output_dir / manifest_path.name
        os.replace(cdf_path, final_cdf)
        os.replace(manifest_path, final_manifest)

    return {
        "cdfPath": str(final_cdf.relative_to(ROOT)),
        "manifestPath": str(final_manifest.relative_to(ROOT)),
        "cdfSha256": cdf_sha,
        "manifestSha256": manifest_sha,
        "cdfSizeBytes": cdf_size,
        "metrics": validation["metrics"],
        "quantiles": validation["quantiles"],
        "diagnostics": diagnostics,
    }
