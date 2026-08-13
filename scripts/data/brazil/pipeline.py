"""Pipeline determinístico da distribuição brasileira de renda — PNAD 2025.

Implementa D063 sem integrar artefatos ao frontend. O módulo falha antes de
promover saídas quando fonte, estrutura, pesos, deflatores ou benchmarks não
correspondem à configuração versionada.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import xlrd


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = ROOT / "config/brazil-pnad-2025.json"
DEFAULT_OUTPUT_DIR = ROOT / "data/processed/brazil/pnad-2025"


class PipelineError(RuntimeError):
    """Erro de validação que impede a promoção de um artefato."""


@dataclass(frozen=True)
class LayoutField:
    start_1_based: int
    width: int
    field_type: str
    description: str


@dataclass
class HouseholdState:
    declared_components: int
    declared_nominal_income: float
    eligible_count: int = 0
    nominal_income: float = 0.0
    real_work_income: float = 0.0
    real_other_income: float = 0.0


@dataclass(frozen=True)
class DatasetArrays:
    rdpc: np.ndarray
    weight: np.ndarray
    uf: np.ndarray
    structural: dict[str, Any]


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "dataset",
        "methodologyVersion",
        "year",
        "release",
        "visit",
        "sourceFile",
        "sourceSha256",
        "paths",
        "requiredVariables",
        "householdKeyVariables",
        "benchmarks",
        "output",
    }
    missing = sorted(required - set(config))
    if missing:
        raise PipelineError(f"Configuração incompleta: {missing}")
    return config


def root_path(relative: str) -> Path:
    resolved = (ROOT / relative).resolve()
    if not resolved.is_relative_to(ROOT.resolve()):
        raise PipelineError(f"Caminho fora da raiz canônica: {relative}")
    return resolved


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest().upper()


def canonical_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def verify_source(config: Mapping[str, Any]) -> dict[str, Any]:
    zip_path = root_path(config["paths"]["rawZip"])
    if not zip_path.is_file():
        raise PipelineError(f"Raw oficial ausente: {zip_path}")
    if zip_path.name != config["sourceFile"]:
        raise PipelineError(
            f"Nome de fonte inesperado: {zip_path.name} != {config['sourceFile']}"
        )
    size = zip_path.stat().st_size
    if size != config["sourceSizeBytes"]:
        raise PipelineError(
            f"Tamanho da fonte divergente: {size} != {config['sourceSizeBytes']}"
        )
    checksum = sha256_file(zip_path)
    expected_checksum = str(config["sourceSha256"]).upper()
    if checksum != expected_checksum:
        raise PipelineError(
            f"SHA-256 da fonte divergente: {checksum} != {expected_checksum}"
        )
    with zipfile.ZipFile(zip_path) as archive:
        members = archive.infolist()
        if len(members) != 1:
            raise PipelineError(f"ZIP deve conter um membro; contém {len(members)}")
        member = members[0]
        if member.filename != config["sourceMember"]:
            raise PipelineError(
                f"Membro inesperado: {member.filename} != {config['sourceMember']}"
            )
        if member.file_size != config["sourceMemberSizeBytes"]:
            raise PipelineError(
                "Tamanho descomprimido do membro não corresponde à configuração"
            )
    return {
        "path": zip_path,
        "sha256": checksum,
        "sizeBytes": size,
        "member": config["sourceMember"],
        "memberSizeBytes": config["sourceMemberSizeBytes"],
    }


def parse_layout(path: Path, required_variables: Sequence[str]) -> dict[str, LayoutField]:
    if not path.is_file():
        raise PipelineError(f"Layout oficial ausente: {path}")
    text = path.read_text(encoding="latin-1")
    pattern = re.compile(
        r"^@(\d+)\s+(\w+)\s+(\$?)(\d+)\.\s+/\*\s*(.*?)\s*\*/",
        re.MULTILINE,
    )
    fields: dict[str, LayoutField] = {}
    for start, name, character, width, description in pattern.findall(text):
        fields[name] = LayoutField(
            start_1_based=int(start),
            width=int(width),
            field_type="character" if character else "numeric",
            description=description,
        )
    missing = sorted(set(required_variables) - set(fields))
    if missing:
        raise PipelineError(f"Variáveis obrigatórias ausentes no layout: {missing}")
    return fields


def read_deflators(config: Mapping[str, Any]) -> dict[tuple[int, int, int], dict[str, float]]:
    path = root_path(config["paths"]["deflator"])
    if not path.is_file():
        raise PipelineError(f"Deflator oficial ausente: {path}")
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    headers = [str(sheet.cell_value(0, column)).strip() for column in range(sheet.ncols)]
    required_columns = {
        "ano",
        "trim",
        "uf",
        config["workDeflator"],
        config["otherIncomeDeflator"],
    }
    missing_columns = sorted(required_columns - set(headers))
    if missing_columns:
        raise PipelineError(f"Colunas ausentes no deflator: {missing_columns}")

    records: dict[tuple[int, int, int], dict[str, float]] = {}
    for row_number in range(1, sheet.nrows):
        row = dict(zip(headers, sheet.row_values(row_number), strict=True))
        if int(row["ano"]) != config["year"]:
            continue
        key = (int(row["ano"]), int(row["trim"]), int(row["uf"]))
        if key in records:
            raise PipelineError(f"Deflator duplicado para chave {key}")
        factors = {
            config["workDeflator"]: float(row[config["workDeflator"]]),
            config["otherIncomeDeflator"]: float(row[config["otherIncomeDeflator"]]),
        }
        if any(not math.isfinite(value) or value <= 0 for value in factors.values()):
            raise PipelineError(f"Fator inválido para chave {key}: {factors}")
        records[key] = factors

    expected_ufs = {int(value) for value in config["benchmarks"]["ufMeansRounded"]}
    expected_keys = {
        (config["year"], quarter, uf)
        for quarter in range(1, 5)
        for uf in expected_ufs
    }
    if set(records) != expected_keys:
        missing = sorted(expected_keys - set(records))
        extra = sorted(set(records) - expected_keys)
        raise PipelineError(f"Cobertura do deflator divergente; missing={missing}, extra={extra}")
    if len(records) != config["expectedStructure"]["deflatorKeys"]:
        raise PipelineError("Quantidade de chaves do deflator divergente")
    return records


def field_value(line: bytes, field: LayoutField) -> str:
    start = field.start_1_based - 1
    return line[start : start + field.width].decode("ascii").strip()


def parse_required_int(value: str, variable: str) -> int:
    if not value:
        raise PipelineError(f"{variable} vazio em registro obrigatório")
    try:
        return int(value)
    except ValueError as error:
        raise PipelineError(f"{variable} não inteiro: {value!r}") from error


def parse_required_float(value: str, variable: str) -> float:
    if not value:
        raise PipelineError(f"{variable} vazio em registro obrigatório")
    try:
        parsed = float(value)
    except ValueError as error:
        raise PipelineError(f"{variable} não numérico: {value!r}") from error
    if not math.isfinite(parsed):
        raise PipelineError(f"{variable} não finito: {value!r}")
    return parsed


def structural_component(value: str, variable: str) -> float:
    if value == "":
        return 0.0
    return parse_required_float(value, variable)


def resolve_deflator(
    deflators: Mapping[tuple[int, int, int], Mapping[str, float]],
    year: int,
    quarter: int,
    uf: int,
) -> Mapping[str, float]:
    key = (year, quarter, uf)
    try:
        return deflators[key]
    except KeyError as error:
        raise PipelineError(f"Deflator ausente para chave {key}") from error


class PipelineAccumulator:
    """Agrega componentes por domicílio e preserva pessoas elegíveis."""

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config
        self.excluded = {int(value) for value in config["excludedConditionCodes"]}
        self.household_ids: dict[tuple[str, ...], int] = {}
        self.households: list[HouseholdState] = []
        self.person_keys: set[tuple[str, ...]] = set()
        self.person_household: list[int] = []
        self.person_weight: list[float] = []
        self.person_uf: list[int] = []
        self.source_records = 0

    def add(self, values: Mapping[str, str], factors: Mapping[str, float]) -> None:
        self.source_records += 1
        household_key = tuple(values[name] for name in self.config["householdKeyVariables"])
        if any(value == "" for value in household_key):
            raise PipelineError("Chave domiciliar contém campo vazio")
        person_key = household_key + (values[self.config["personKeyVariable"]],)
        if not person_key[-1]:
            raise PipelineError("Chave da pessoa contém número de ordem vazio")
        if person_key in self.person_keys:
            raise PipelineError(f"Chave de pessoa duplicada: {person_key}")
        self.person_keys.add(person_key)

        weight = parse_required_float(
            values[self.config["weightVariable"]], self.config["weightVariable"]
        )
        if weight <= 0:
            raise PipelineError(f"Peso inválido: {weight}")
        condition = parse_required_int(
            values[self.config["conditionVariable"]], self.config["conditionVariable"]
        )
        if condition in self.excluded:
            return

        components = parse_required_int(
            values[self.config["eligibleComponentsVariable"]],
            self.config["eligibleComponentsVariable"],
        )
        if components <= 0:
            raise PipelineError(f"Número de componentes elegíveis inválido: {components}")
        declared_nominal = parse_required_float(
            values[self.config["nominalHouseholdValidationVariable"]],
            self.config["nominalHouseholdValidationVariable"],
        )
        work = structural_component(
            values[self.config["workIncomeVariable"]], self.config["workIncomeVariable"]
        )
        other = structural_component(
            values[self.config["otherIncomeVariable"]], self.config["otherIncomeVariable"]
        )

        if household_key not in self.household_ids:
            self.household_ids[household_key] = len(self.households)
            self.households.append(
                HouseholdState(
                    declared_components=components,
                    declared_nominal_income=declared_nominal,
                )
            )
        household_id = self.household_ids[household_key]
        state = self.households[household_id]
        if state.declared_components != components:
            raise PipelineError(f"VD2003 inconsistente no domicílio {household_key}")
        if not math.isclose(
            state.declared_nominal_income, declared_nominal, rel_tol=0, abs_tol=1e-9
        ):
            raise PipelineError(f"VD5007 inconsistente no domicílio {household_key}")

        state.eligible_count += 1
        state.nominal_income += work + other
        state.real_work_income += work * factors[self.config["workDeflator"]]
        state.real_other_income += other * factors[self.config["otherIncomeDeflator"]]
        self.person_household.append(household_id)
        self.person_weight.append(weight)
        self.person_uf.append(parse_required_int(values[self.config["ufVariable"]], "UF"))

    def finalize(self) -> DatasetArrays:
        expected = self.config["expectedStructure"]
        if self.source_records != expected["sourceRecords"]:
            raise PipelineError(
                f"Contagem da fonte divergente: {self.source_records} != {expected['sourceRecords']}"
            )
        if len(self.person_keys) != self.source_records:
            raise PipelineError("Quantidade de chaves de pessoa não corresponde aos registros")
        if len(self.households) != expected["eligibleHouseholds"]:
            raise PipelineError(
                f"Domicílios elegíveis divergentes: {len(self.households)} != {expected['eligibleHouseholds']}"
            )
        if len(self.person_household) != expected["eligiblePersons"]:
            raise PipelineError(
                f"Pessoas elegíveis divergentes: {len(self.person_household)} != {expected['eligiblePersons']}"
            )

        household_rdpc = np.empty(len(self.households), dtype=np.float64)
        nominal_mismatches = 0
        maximum_nominal_difference = 0.0
        for household_id, state in enumerate(self.households):
            if state.eligible_count != state.declared_components:
                raise PipelineError(
                    "Contagem elegível não corresponde a VD2003 no domicílio "
                    f"{household_id}: {state.eligible_count} != {state.declared_components}"
                )
            difference = abs(state.nominal_income - state.declared_nominal_income)
            maximum_nominal_difference = max(maximum_nominal_difference, difference)
            if difference > 1e-9:
                nominal_mismatches += 1
            household_rdpc[household_id] = (
                state.real_work_income + state.real_other_income
            ) / state.declared_components
        if nominal_mismatches:
            raise PipelineError(
                f"Reconstrução nominal divergiu de VD5007 em {nominal_mismatches} domicílios"
            )

        person_household = np.asarray(self.person_household, dtype=np.int32)
        rdpc = household_rdpc[person_household]
        weight = np.asarray(self.person_weight, dtype=np.float64)
        uf = np.asarray(self.person_uf, dtype=np.int16)
        decimals = int(self.config["output"]["rdpcDecimalPlaces"])
        weight_decimals = int(self.config["output"]["weightDecimalPlaces"])
        rdpc = np.round(rdpc, decimals=decimals)
        weight = np.round(weight, decimals=weight_decimals)

        if np.any(~np.isfinite(rdpc)) or np.any(rdpc < 0):
            raise PipelineError("RDPC final contém valor negativo ou não finito")
        if np.any(~np.isfinite(weight)) or np.any(weight <= 0):
            raise PipelineError("Peso final contém valor inválido")
        return DatasetArrays(
            rdpc=rdpc,
            weight=weight,
            uf=uf,
            structural={
                "sourceRecords": self.source_records,
                "eligiblePersons": len(self.person_household),
                "eligibleHouseholds": len(self.households),
                "uniquePersonKeys": len(self.person_keys),
                "nominalRecompositionMismatches": nominal_mismatches,
                "nominalRecompositionMaxAbsoluteDifference": maximum_nominal_difference,
            },
        )


def process_microdata(
    config: Mapping[str, Any],
    source: Mapping[str, Any],
    layout: Mapping[str, LayoutField],
    deflators: Mapping[tuple[int, int, int], Mapping[str, float]],
) -> DatasetArrays:
    accumulator = PipelineAccumulator(config)
    required = list(config["requiredVariables"])
    expected_line_length = int(config["sourceLineLength"])
    with zipfile.ZipFile(source["path"]) as archive:
        with archive.open(config["sourceMember"]) as stream:
            for line_number, raw_line in enumerate(stream, start=1):
                line = raw_line.rstrip(b"\r\n")
                if len(line) != expected_line_length:
                    raise PipelineError(
                        f"Linha {line_number} com largura {len(line)}; esperado {expected_line_length}"
                    )
                values = {name: field_value(line, layout[name]) for name in required}
                year = parse_required_int(values["Ano"], "Ano")
                quarter = parse_required_int(values["Trimestre"], "Trimestre")
                uf = parse_required_int(values[config["ufVariable"]], config["ufVariable"])
                if year != config["year"] or quarter not in {1, 2, 3, 4}:
                    raise PipelineError(
                        f"Referência temporal inesperada na linha {line_number}: {year}/{quarter}"
                    )
                factors = resolve_deflator(deflators, year, quarter, uf)
                accumulator.add(values, factors)
    return accumulator.finalize()


def weighted_quantiles(
    values: np.ndarray, weights: np.ndarray, probabilities: Sequence[float]
) -> dict[str, float]:
    order = np.argsort(values, kind="stable")
    ordered_values = values[order]
    cumulative = np.cumsum(weights[order])
    total = cumulative[-1]
    output: dict[str, float] = {}
    for probability in probabilities:
        index = int(np.searchsorted(cumulative, probability * total, side="left"))
        output[f"P{probability * 100:g}"] = float(
            ordered_values[min(index, len(ordered_values) - 1)]
        )
    return output


def weighted_gini(values: np.ndarray, weights: np.ndarray) -> float:
    order = np.argsort(values, kind="stable")
    x = values[order]
    w = weights[order]
    cumulative_income = np.cumsum(x * w)
    total_income = cumulative_income[-1]
    total_weight = np.sum(w)
    if total_income <= 0 or total_weight <= 0:
        raise PipelineError("Gini indefinido para renda ou peso total não positivo")
    previous_income = np.concatenate(([0.0], cumulative_income[:-1]))
    return float(
        1.0
        - np.sum(w * (cumulative_income + previous_income))
        / (total_income * total_weight)
    )


def calculate_metrics(dataset: DatasetArrays) -> dict[str, Any]:
    mean = float(np.average(dataset.rdpc, weights=dataset.weight))
    population = float(np.sum(dataset.weight))
    gini = weighted_gini(dataset.rdpc, dataset.weight)
    probabilities = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99, 0.995, 0.999]
    quantiles = weighted_quantiles(dataset.rdpc, dataset.weight, probabilities)
    uf_means = {
        str(int(uf)): float(
            np.average(dataset.rdpc[dataset.uf == uf], weights=dataset.weight[dataset.uf == uf])
        )
        for uf in sorted(np.unique(dataset.uf))
    }
    zero_mask = dataset.rdpc == 0
    return {
        "records": int(dataset.rdpc.size),
        "mean": mean,
        "meanRounded": int(round(mean)),
        "gini": gini,
        "giniRounded3": round(gini, 3),
        "population": population,
        "populationThousandRounded": int(round(population / 1000)),
        "zeroRecords": int(np.sum(zero_mask)),
        "zeroWeight": float(np.sum(dataset.weight[zero_mask])),
        "negativeRecords": int(np.sum(dataset.rdpc < 0)),
        "minimum": float(np.min(dataset.rdpc)),
        "maximum": float(np.max(dataset.rdpc)),
        "quantiles": quantiles,
        "ufMeans": uf_means,
    }


def validate_benchmarks(
    config: Mapping[str, Any], dataset: DatasetArrays, metrics: Mapping[str, Any]
) -> dict[str, Any]:
    expected = config["expectedStructure"]
    if metrics["records"] != expected["eligiblePersons"]:
        raise PipelineError("Quantidade de pessoas elegíveis falhou")
    if metrics["zeroRecords"] != expected["zeroRecords"]:
        raise PipelineError("Quantidade de rendas zero falhou")
    if metrics["negativeRecords"] != expected["negativeRecords"]:
        raise PipelineError("Foram observadas rendas negativas inesperadas")
    if dataset.structural["nominalRecompositionMismatches"] != 0:
        raise PipelineError("Reconstrução nominal contra VD5007 falhou")

    benchmarks = config["benchmarks"]
    mean_spec = benchmarks["mean"]
    if abs(metrics["mean"] - mean_spec["diagnostic"]) > mean_spec["absoluteTolerance"]:
        raise PipelineError("Média nacional divergiu do diagnóstico validado")
    if metrics["meanRounded"] != mean_spec["publishedRounded"]:
        raise PipelineError("Média nacional arredondada divergiu da publicação")

    gini_spec = benchmarks["gini"]
    if abs(metrics["gini"] - gini_spec["diagnostic"]) > gini_spec["absoluteTolerance"]:
        raise PipelineError("Gini divergiu do diagnóstico validado")
    if metrics["giniRounded3"] != gini_spec["publishedRounded3"]:
        raise PipelineError("Gini arredondado divergiu da publicação")

    population_spec = benchmarks["population"]
    if (
        abs(metrics["population"] - population_spec["diagnostic"])
        > population_spec["absoluteTolerance"]
    ):
        raise PipelineError("População ponderada divergiu do diagnóstico validado")
    if metrics["populationThousandRounded"] != population_spec["publishedThousand"]:
        raise PipelineError("População em milhares divergiu da publicação")

    uf_results: dict[str, Any] = {}
    for uf, published in benchmarks["ufMeansRounded"].items():
        if uf not in metrics["ufMeans"]:
            raise PipelineError(f"UF ausente no resultado: {uf}")
        calculated = metrics["ufMeans"][uf]
        difference = int(round(calculated)) - int(published)
        if difference != 0:
            raise PipelineError(f"Média da UF {uf} divergiu: {difference}")
        uf_results[uf] = {
            "calculated": calculated,
            "calculatedRounded": int(round(calculated)),
            "published": int(published),
            "differenceRounded": difference,
        }

    quantile_results: dict[str, Any] = {}
    for label, spec in benchmarks["quantiles"].items():
        calculated = metrics["quantiles"][label]
        difference = int(round(calculated)) - int(spec["published"])
        if difference != int(spec["expectedRoundedDifference"]):
            raise PipelineError(
                f"Resíduo do quantil {label} mudou: {difference} != {spec['expectedRoundedDifference']}"
            )
        quantile_results[label] = {
            "calculated": calculated,
            "calculatedRounded": int(round(calculated)),
            "published": int(spec["published"]),
            "differenceRounded": difference,
        }
    return {
        "mean": "PASS",
        "gini": "PASS",
        "population": "PASS",
        "ufMeans": {"status": "PASS", "matches": len(uf_results), "total": len(uf_results)},
        "quantiles": quantile_results,
    }


def write_dataset(path: Path, config: Mapping[str, Any], dataset: DatasetArrays) -> None:
    order = np.lexsort((dataset.weight, dataset.rdpc, dataset.uf))
    rdpc_decimals = int(config["output"]["rdpcDecimalPlaces"])
    weight_decimals = int(config["output"]["weightDecimalPlaces"])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(config["output"]["columns"])
        for index in order:
            writer.writerow(
                (
                    f"{dataset.rdpc[index]:.{rdpc_decimals}f}",
                    f"{dataset.weight[index]:.{weight_decimals}f}",
                    f"{int(dataset.uf[index]):02d}",
                )
            )


def load_dataset(path: Path, config: Mapping[str, Any]) -> DatasetArrays:
    rdpc: list[float] = []
    weight: list[float] = []
    uf: list[int] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header != config["output"]["columns"]:
            raise PipelineError(f"Cabeçalho do dataset divergente: {header}")
        for line_number, row in enumerate(reader, start=2):
            if len(row) != 3:
                raise PipelineError(f"Linha {line_number} do dataset com {len(row)} campos")
            rdpc.append(parse_required_float(row[0], "rdpc_real_2025"))
            weight.append(parse_required_float(row[1], "weight"))
            uf.append(parse_required_int(row[2], "UF"))
    return DatasetArrays(
        rdpc=np.asarray(rdpc, dtype=np.float64),
        weight=np.asarray(weight, dtype=np.float64),
        uf=np.asarray(uf, dtype=np.int16),
        structural={},
    )


def build_dataset(
    config_path: Path = DEFAULT_CONFIG_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    output_dir = output_dir.resolve()
    config = load_config(config_path)
    source = verify_source(config)
    layout = parse_layout(root_path(config["paths"]["layout"]), config["requiredVariables"])
    deflators = read_deflators(config)
    dataset = process_microdata(config, source, layout, deflators)
    metrics = calculate_metrics(dataset)
    benchmark_results = validate_benchmarks(config, dataset, metrics)

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pnad-2025-", dir=output_dir.parent) as temporary:
        temporary_dir = Path(temporary)
        dataset_path = temporary_dir / config["output"]["fileName"]
        manifest_path = temporary_dir / config["output"]["manifestFileName"]
        write_dataset(dataset_path, config, dataset)
        dataset_sha = sha256_file(dataset_path)
        manifest = {
            "dataset": "brazil-income-distribution",
            "source": "IBGE PNAD Contínua",
            "sourceYear": config["year"],
            "sourceRelease": config["release"],
            "sourceFile": config["sourceFile"],
            "sourceSha256": source["sha256"],
            "visit": config["visit"],
            "priceReference": config["priceReference"],
            "workIncomeVariable": config["workIncomeVariable"],
            "workDeflator": config["workDeflator"],
            "otherIncomeVariable": config["otherIncomeVariable"],
            "otherIncomeDeflator": config["otherIncomeDeflator"],
            "eligibleComponentsVariable": config["eligibleComponentsVariable"],
            "weightVariable": config["weightVariable"],
            "ufVariable": config["ufVariable"],
            "methodologyVersion": config["methodologyVersion"],
            "processedAt": None,
            "processedAtPolicy": "omitido do artefato determinístico",
            "datasetFormat": {
                "type": "CSV UTF-8",
                "columns": config["output"]["columns"],
                "ordering": ["UF", "rdpc_real_2025", "weight"],
                "lineTerminator": "LF",
                "rdpcDecimalPlaces": config["output"]["rdpcDecimalPlaces"],
                "weightDecimalPlaces": config["output"]["weightDecimalPlaces"],
            },
            "recordCount": metrics["records"],
            "datasetSha256": dataset_sha,
            "configSha256": sha256_file(config_path),
            "metrics": metrics,
            "structuralValidation": dataset.structural,
            "benchmarkValidation": benchmark_results,
        }
        manifest_path.write_text(canonical_json(manifest), encoding="utf-8", newline="\n")
        manifest_sha = sha256_file(manifest_path)

        output_dir.mkdir(parents=True, exist_ok=True)
        final_dataset = output_dir / dataset_path.name
        final_manifest = output_dir / manifest_path.name
        os.replace(dataset_path, final_dataset)
        os.replace(manifest_path, final_manifest)

    return {
        "datasetPath": str(final_dataset.relative_to(ROOT)),
        "manifestPath": str(final_manifest.relative_to(ROOT)),
        "datasetSizeBytes": final_dataset.stat().st_size,
        "datasetSha256": dataset_sha,
        "manifestSha256": manifest_sha,
        "metrics": metrics,
        "structural": dataset.structural,
        "benchmarks": benchmark_results,
    }


def validate_existing_output(
    config_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    config = load_config(config_path)
    dataset_path = output_dir / config["output"]["fileName"]
    manifest_path = output_dir / config["output"]["manifestFileName"]
    if not dataset_path.is_file() or not manifest_path.is_file():
        raise PipelineError(f"Saída incompleta em {output_dir}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    dataset_sha = sha256_file(dataset_path)
    if dataset_sha != manifest["datasetSha256"]:
        raise PipelineError("Checksum do dataset não corresponde ao manifesto")
    loaded = load_dataset(dataset_path, config)
    dataset = DatasetArrays(
        rdpc=loaded.rdpc,
        weight=loaded.weight,
        uf=loaded.uf,
        structural=manifest["structuralValidation"],
    )
    metrics = calculate_metrics(dataset)
    benchmark_results = validate_benchmarks(config, dataset, metrics)
    return {
        "datasetPath": str(dataset_path.relative_to(ROOT)),
        "manifestPath": str(manifest_path.relative_to(ROOT)),
        "datasetSizeBytes": dataset_path.stat().st_size,
        "datasetSha256": dataset_sha,
        "manifestSha256": sha256_file(manifest_path),
        "metrics": metrics,
        "benchmarks": benchmark_results,
    }
