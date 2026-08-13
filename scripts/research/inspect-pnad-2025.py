"""Inspeção reproduzível da PNAD Contínua 2025 — Fase 1C.

Lê seletivamente o TXT de largura fixa diretamente do ZIP oficial, cruza os
deflatores por ano/trimestre/UF e produz somente diagnósticos agregados. Não
gera CDF, lookup, percentis de usuário ou dataset de produção.
"""

from __future__ import annotations

import csv
import json
import math
import platform
import re
import sys
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import xlrd


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/ibge/pnadc/2025/20260508"
DOC = RAW / "documentation"
ARTIFACTS = ROOT / "docs/research/artifacts"
ZIP_PATH = RAW / "PNADC_2025_visita1_20260508.zip"
LAYOUT_PATH = DOC / "input_PNADC_2025_visita1_20260508.txt"
DICTIONARY_PATH = DOC / "dicionario_PNADC_microdados_2025_visita1_20260508.xls"
DEFLATOR_PATH = DOC / "deflator_PNADC_2025.xls"

SELECTED = (
    "Ano",
    "Trimestre",
    "UF",
    "UPA",
    "Estrato",
    "V1008",
    "V1014",
    "V1032",
    "V2003",
    "V2005",
    "V2009",
    "VD2003",
    "VD4019",
    "VD4048",
    "VD4052",
    "VD5002",
    "VD5005",
    "VD5007",
    "VD5008",
    "VD5010",
    "VD5011",
)

SIDRA_URLS = {
    "quantile_limits": "https://apisidra.ibge.gov.br/values/t/7526/n1/all/v/10838/p/2025/c1019/all",
    "accumulated_means": "https://apisidra.ibge.gov.br/values/t/7534/n1/all/v/10816/p/2025/c1042/all",
    "accumulated_population": "https://apisidra.ibge.gov.br/values/t/7564/n1/all/v/606/p/2025/c1042/all",
    "simple_population": "https://apisidra.ibge.gov.br/values/t/7529/n1/all/v/606/p/2025/c1019/all",
    "uf_mean": "https://apisidra.ibge.gov.br/values/t/7534/n3/all/v/10816/p/2025/c1042/49283",
}


def parse_layout() -> dict[str, dict[str, Any]]:
    text = LAYOUT_PATH.read_text(encoding="latin-1")
    pattern = re.compile(
        r"^@(\d+)\s+(\w+)\s+(\$?)(\d+)\.\s+/\*\s*(.*?)\s*\*/",
        re.MULTILINE,
    )
    fields: dict[str, dict[str, Any]] = {}
    for start, name, char_flag, width, description in pattern.findall(text):
        fields[name] = {
            "start_1_based": int(start),
            "width": int(width),
            "type": "character" if char_flag else "numeric",
            "description": description,
        }
    missing = [name for name in SELECTED if name not in fields]
    if missing:
        raise RuntimeError(f"Variáveis ausentes no layout: {missing}")
    return fields


def dictionary_rows() -> tuple[list[list[Any]], dict[str, dict[str, Any]]]:
    workbook = xlrd.open_workbook(DICTIONARY_PATH)
    sheet = workbook.sheet_by_index(0)
    rows = [sheet.row_values(row) for row in range(sheet.nrows)]
    found: dict[str, dict[str, Any]] = {}
    for row_number, row in enumerate(rows, start=1):
        code = str(row[2]).strip() if len(row) > 2 else ""
        if code in SELECTED:
            found[code] = {
                "row": row_number,
                "position": row[0],
                "width": row[1],
                "description": row[4],
                "domain": row[5],
                "label": row[6],
                "period": row[7],
            }
    return rows, found


def dictionary_v2005_categories(rows: list[list[Any]]) -> dict[str, str]:
    start = next(i for i, row in enumerate(rows) if str(row[2]).strip() == "V2005")
    categories: dict[str, str] = {}
    for row in rows[start:]:
        if row is not rows[start] and str(row[2]).strip():
            break
        value = row[5]
        label = str(row[6]).strip()
        if value != "" and label:
            if isinstance(value, float) and value.is_integer():
                code = f"{int(value):02d}"
            else:
                code = str(value).strip().zfill(2)
            categories[code] = label
    return categories


def read_deflators() -> tuple[dict[tuple[int, int, int], dict[str, float]], dict[str, Any]]:
    workbook = xlrd.open_workbook(DEFLATOR_PATH)
    sheet = workbook.sheet_by_index(0)
    headers = [str(sheet.cell_value(0, column)).strip() for column in range(sheet.ncols)]
    records: dict[tuple[int, int, int], dict[str, float]] = {}
    all_rows = []
    for row_number in range(1, sheet.nrows):
        row = dict(zip(headers, sheet.row_values(row_number), strict=True))
        all_rows.append(row)
        if int(row["ano"]) == 2025:
            key = (int(row["ano"]), int(row["trim"]), int(row["uf"]))
            records[key] = {name: float(row[name]) for name in ("CO1", "CO1e", "CO2", "CO2e", "CO3")}
    expected = {(2025, quarter, uf) for quarter in range(1, 5) for uf in (
        11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27,
        28, 29, 31, 32, 33, 35, 41, 42, 43, 50, 51, 52, 53,
    )}
    if set(records) != expected:
        raise RuntimeError("Cobertura inesperada do deflator para 2025")
    metadata = {
        "sheet": sheet.name,
        "rows_total": len(all_rows),
        "rows_2025": len(records),
        "columns": headers,
        "co1_equals_co2_in_2025": all(
            math.isclose(row["CO1"], row["CO2"], rel_tol=0, abs_tol=1e-15)
            for row in records.values()
        ),
        "co1e_equals_co2e_in_2025": all(
            math.isclose(row["CO1e"], row["CO2e"], rel_tol=0, abs_tol=1e-15)
            for row in records.values()
        ),
        "ranges_2025": {
            name: {
                "min": min(row[name] for row in records.values()),
                "max": max(row[name] for row in records.values()),
            }
            for name in ("CO1", "CO1e", "CO2", "CO2e", "CO3")
        },
    }
    return records, metadata


def field_value(line: bytes, field: dict[str, Any]) -> str:
    start = field["start_1_based"] - 1
    return line[start : start + field["width"]].decode("ascii").strip()


def as_int(value: str, missing: int = -1) -> int:
    return int(value) if value else missing


def as_float(value: str) -> float:
    return float(value) if value else math.nan


def read_microdata(layout: dict[str, dict[str, Any]]) -> dict[str, Any]:
    columns: dict[str, list[Any]] = {name: [] for name in (
        "year", "quarter", "uf", "weight", "condition", "age",
        "household_index", "household_components", "work_income", "other_income",
        "personal_income", "vd5002", "vd5005",
        "vd5007", "vd5008", "vd5010", "rdpc",
    )}
    person_keys: set[tuple[str, str, str, str]] = set()
    household_keys: set[tuple[str, str, str]] = set()
    household_ids: dict[tuple[str, str, str], int] = {}
    duplicate_person_keys = 0
    line_lengths: Counter[int] = Counter()

    with zipfile.ZipFile(ZIP_PATH) as archive:
        members = archive.infolist()
        if len(members) != 1:
            raise RuntimeError(f"ZIP deveria conter um membro; contém {len(members)}")
        with archive.open(members[0]) as stream:
            for line in stream:
                line = line.rstrip(b"\r\n")
                line_lengths[len(line)] += 1
                values = {name: field_value(line, layout[name]) for name in SELECTED}
                household_key = (values["UPA"], values["V1008"], values["V1014"])
                person_key = household_key + (values["V2003"],)
                household_keys.add(household_key)
                if household_key not in household_ids:
                    household_ids[household_key] = len(household_ids)
                if person_key in person_keys:
                    duplicate_person_keys += 1
                person_keys.add(person_key)
                columns["year"].append(as_int(values["Ano"]))
                columns["quarter"].append(as_int(values["Trimestre"]))
                columns["uf"].append(as_int(values["UF"]))
                columns["weight"].append(as_float(values["V1032"]))
                columns["condition"].append(as_int(values["V2005"]))
                columns["age"].append(as_int(values["V2009"]))
                columns["household_index"].append(household_ids[household_key])
                columns["household_components"].append(as_int(values["VD2003"]))
                columns["work_income"].append(as_float(values["VD4019"]))
                columns["other_income"].append(as_float(values["VD4048"]))
                columns["personal_income"].append(as_float(values["VD4052"]))
                columns["vd5002"].append(as_float(values["VD5002"]))
                columns["vd5005"].append(as_float(values["VD5005"]))
                columns["vd5007"].append(as_float(values["VD5007"]))
                columns["vd5008"].append(as_float(values["VD5008"]))
                columns["vd5010"].append(as_float(values["VD5010"]))
                columns["rdpc"].append(as_float(values["VD5011"]))

    arrays = {
        "year": np.asarray(columns["year"], dtype=np.int16),
        "quarter": np.asarray(columns["quarter"], dtype=np.int8),
        "uf": np.asarray(columns["uf"], dtype=np.int8),
        "weight": np.asarray(columns["weight"], dtype=np.float64),
        "condition": np.asarray(columns["condition"], dtype=np.int8),
        "age": np.asarray(columns["age"], dtype=np.int16),
        "household_index": np.asarray(columns["household_index"], dtype=np.int32),
        "household_components": np.asarray(columns["household_components"], dtype=np.int8),
        "work_income": np.asarray(columns["work_income"], dtype=np.float64),
        "other_income": np.asarray(columns["other_income"], dtype=np.float64),
        "personal_income": np.asarray(columns["personal_income"], dtype=np.float64),
        "vd5002": np.asarray(columns["vd5002"], dtype=np.float64),
        "vd5005": np.asarray(columns["vd5005"], dtype=np.float64),
        "vd5007": np.asarray(columns["vd5007"], dtype=np.float64),
        "vd5008": np.asarray(columns["vd5008"], dtype=np.float64),
        "vd5010": np.asarray(columns["vd5010"], dtype=np.float64),
        "rdpc": np.asarray(columns["rdpc"], dtype=np.float64),
    }
    arrays["structural"] = {
        "rows": len(arrays["rdpc"]),
        "line_lengths": {str(key): value for key, value in sorted(line_lengths.items())},
        "unique_households": len(household_keys),
        "unique_person_keys": len(person_keys),
        "duplicate_person_keys": duplicate_person_keys,
    }
    return arrays


def weighted_quantile(values: np.ndarray, weights: np.ndarray, probability: float) -> float:
    order = np.argsort(values, kind="stable")
    ordered_values = values[order]
    ordered_weights = weights[order]
    cumulative = np.cumsum(ordered_weights)
    index = int(np.searchsorted(cumulative, probability * cumulative[-1], side="left"))
    return float(ordered_values[min(index, len(ordered_values) - 1)])


def weighted_quantiles(
    values: np.ndarray, weights: np.ndarray, probabilities: list[float]
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
    previous_income = np.concatenate(([0.0], cumulative_income[:-1]))
    return float(1.0 - np.sum(w * (cumulative_income + previous_income)) / (total_income * total_weight))


def sidra(url: str) -> list[dict[str, str]]:
    request = urllib.request.Request(url, headers={"User-Agent": "Renda-Comparada-Research/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)
    return payload[1:]


def numeric_sidra(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        if row["V"] in {"-", "..", "...", "X"}:
            continue
        output.append({**row, "value": float(row["V"])})
    return output


def profile_numeric(values: np.ndarray) -> dict[str, Any]:
    valid = np.isfinite(values)
    selected = values[valid]
    return {
        "records": int(values.size),
        "valid": int(valid.sum()),
        "missing_or_non_finite": int((~valid).sum()),
        "zero": int(np.sum(selected == 0)),
        "negative": int(np.sum(selected < 0)),
        "minimum": float(np.min(selected)) if selected.size else None,
        "maximum": float(np.max(selected)) if selected.size else None,
        "mean": float(np.mean(selected)) if selected.size else None,
        "sum": float(np.sum(selected)) if selected.size else None,
        "distinct": int(np.unique(selected).size),
    }


def top_frequencies(
    values: np.ndarray, weights: np.ndarray, limit: int = 15
) -> list[dict[str, Any]]:
    counter: dict[float, list[float]] = {}
    for value, item_weight in zip(values, weights, strict=True):
        if value not in counter:
            counter[value] = [0.0, 0.0]
        counter[value][0] += 1
        counter[value][1] += float(item_weight)
    return [
        {"value": value, "records": int(stats[0]), "weight": stats[1]}
        for value, stats in sorted(counter.items(), reverse=True)[:limit]
    ]


def main() -> None:
    layout = parse_layout()
    dictionary, dictionary_variables = dictionary_rows()
    v2005_categories = dictionary_v2005_categories(dictionary)
    deflators, deflator_metadata = read_deflators()
    arrays = read_microdata(layout)

    year = arrays["year"]
    quarter = arrays["quarter"]
    uf = arrays["uf"]
    weight = arrays["weight"]
    condition = arrays["condition"]
    age = arrays["age"]
    household_index = arrays["household_index"]
    household_components = arrays["household_components"]
    work_income = arrays["work_income"]
    other_income = arrays["other_income"]
    personal_income = arrays["personal_income"]
    vd5002 = arrays["vd5002"]
    vd5005 = arrays["vd5005"]
    vd5007 = arrays["vd5007"]
    vd5008 = arrays["vd5008"]
    vd5010 = arrays["vd5010"]
    rdpc = arrays["rdpc"]

    documented_eligible = ~np.isin(condition, [17, 18, 19])
    rdpc_present = np.isfinite(rdpc)
    valid_weight = np.isfinite(weight) & (weight > 0)
    analysis_mask = documented_eligible & rdpc_present & valid_weight

    factors = {
        name: np.fromiter(
            (deflators[(int(y), int(q), int(state))][name] for y, q, state in zip(year, quarter, uf, strict=True)),
            dtype=np.float64,
            count=len(year),
        )
        for name in ("CO1", "CO1e", "CO2", "CO2e")
    }
    real_variants = {name: rdpc[analysis_mask] * factor[analysis_mask] for name, factor in factors.items()}
    selected_weight = weight[analysis_mask]
    real_rdpc = real_variants["CO1"]

    mean_variants = {
        "nominal": float(np.average(rdpc[analysis_mask], weights=selected_weight)),
        **{
            name: float(np.average(values, weights=selected_weight))
            for name, values in real_variants.items()
        },
    }

    probabilities = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99, 0.995, 0.999]
    quantiles = weighted_quantiles(real_rdpc, selected_weight, probabilities)

    official_quantiles = {
        row["D4N"]: row["value"]
        for row in numeric_sidra(sidra(SIDRA_URLS["quantile_limits"]))
        if row["D4N"] != "Total"
    }
    household_count = arrays["structural"]["unique_households"]
    work_zero = np.nan_to_num(work_income, nan=0.0)
    other_zero = np.nan_to_num(other_income, nan=0.0)
    nominal_components = work_zero + other_zero
    component_real = work_zero * factors["CO1"] + other_zero * factors["CO1e"]
    household_nominal = np.bincount(
        household_index[documented_eligible],
        weights=nominal_components[documented_eligible],
        minlength=household_count,
    )
    household_real = np.bincount(
        household_index[documented_eligible],
        weights=component_real[documented_eligible],
        minlength=household_count,
    )
    household_size = np.bincount(
        household_index[documented_eligible], minlength=household_count
    )
    reconstructed_real_pc_by_household = np.divide(
        household_real,
        household_size,
        out=np.full(household_count, np.nan),
        where=household_size > 0,
    )
    reconstructed_real_pc = reconstructed_real_pc_by_household[household_index]
    declared_household_nominal = vd5007[documented_eligible]
    recomposed_household_nominal = household_nominal[household_index[documented_eligible]]
    nominal_recomposition_difference = recomposed_household_nominal - declared_household_nominal
    candidate_specs = {
        "VD5002_CO1e": (vd5002, "CO1e"),
        "VD5005_CO1e": (vd5005, "CO1e"),
        "VD5008_CO1": (vd5008, "CO1"),
        "VD5011_CO1": (rdpc, "CO1"),
        "VD5007_div_VD2003_CO1": (
            np.divide(
                vd5007,
                household_components,
                out=np.full_like(vd5007, np.nan),
                where=household_components > 0,
            ),
            "CO1",
        ),
        "VD5010_div_VD2003_CO1": (
            np.divide(
                vd5010,
                household_components,
                out=np.full_like(vd5010, np.nan),
                where=household_components > 0,
            ),
            "CO1",
        ),
        "VD4019_CO1_plus_VD4048_CO1e_by_household": (
            reconstructed_real_pc,
            None,
        ),
    }
    candidate_diagnostics = []
    for candidate_name, (candidate, factor_name) in candidate_specs.items():
        candidate_mask = documented_eligible & np.isfinite(candidate) & valid_weight
        candidate_weights = weight[candidate_mask]
        candidate_real = (
            candidate[candidate_mask]
            if factor_name is None
            else candidate[candidate_mask] * factors[factor_name][candidate_mask]
        )
        candidate_quantiles = weighted_quantiles(candidate_real, candidate_weights, probabilities[:12])
        comparisons = {
            label: int(round(value)) - official_quantiles[label]
            for label, value in candidate_quantiles.items()
        }
        candidate_mean = float(np.average(candidate_real, weights=candidate_weights))
        candidate_diagnostics.append({
            "candidate": candidate_name,
            "variable": candidate_name.split("_")[0],
            "deflator": factor_name,
            "records": int(candidate_mask.sum()),
            "population_weight": float(np.sum(candidate_weights)),
            "nominal_mean": (
                None
                if factor_name is None
                else float(np.average(candidate[candidate_mask], weights=candidate_weights))
            ),
            "real_mean_unrounded": candidate_mean,
            "real_mean_rounded": int(round(candidate_mean)),
            "difference_from_2264_unrounded": candidate_mean - 2264,
            "gini": weighted_gini(candidate_real, candidate_weights),
            "quantiles": candidate_quantiles,
            "quantile_rounded_differences": comparisons,
            "quantile_exact_rounded_matches": sum(value == 0 for value in comparisons.values()),
        })
    quantile_comparison = []
    for label, official in official_quantiles.items():
        calculated = quantiles[label]
        quantile_comparison.append({
            "quantile": label,
            "calculated_unrounded": calculated,
            "calculated_rounded": int(round(calculated)),
            "official": official,
            "difference_rounded": int(round(calculated)) - official,
        })

    official_accumulated_means = {
        row["D4N"]: row["value"]
        for row in numeric_sidra(sidra(SIDRA_URLS["accumulated_means"]))
    }
    accumulated_mean_comparison = []
    for probability in probabilities[:12]:
        label = f"P{probability * 100:g}"
        official_label = f"até o {label}"
        threshold = quantiles[label]
        mask = real_rdpc <= threshold
        calculated = float(np.average(real_rdpc[mask], weights=selected_weight[mask]))
        official = official_accumulated_means.get(official_label)
        accumulated_mean_comparison.append({
            "class": official_label,
            "calculated_unrounded": calculated,
            "calculated_rounded": int(round(calculated)),
            "official": official,
            "difference_rounded": None if official is None else int(round(calculated)) - official,
        })

    compatible_real = reconstructed_real_pc[analysis_mask]
    compatible_quantiles = weighted_quantiles(
        compatible_real, selected_weight, probabilities
    )
    compatible_accumulated_mean_comparison = []
    for probability in probabilities[:12]:
        label = f"P{probability * 100:g}"
        official_label = f"até o {label}"
        threshold = compatible_quantiles[label]
        mask = compatible_real <= threshold
        calculated = float(
            np.average(compatible_real[mask], weights=selected_weight[mask])
        )
        official = official_accumulated_means.get(official_label)
        compatible_accumulated_mean_comparison.append({
            "class": official_label,
            "calculated_unrounded": calculated,
            "calculated_rounded": int(round(calculated)),
            "official": official,
            "difference_rounded": (
                None if official is None else int(round(calculated)) - official
            ),
        })

    official_population_rows = numeric_sidra(sidra(SIDRA_URLS["accumulated_population"]))
    official_population_total = next(row["value"] * 1000 for row in official_population_rows if row["D4N"] == "Total")
    calculated_population = float(np.sum(selected_weight))

    official_uf_rows = numeric_sidra(sidra(SIDRA_URLS["uf_mean"]))
    official_uf_means = {int(row["D1C"]): row["value"] for row in official_uf_rows}
    uf_comparison = []
    compatible_uf_comparison = []
    for state in sorted(official_uf_means):
        mask = analysis_mask & (uf == state)
        calculated = float(np.average(rdpc[mask] * factors["CO1"][mask], weights=weight[mask]))
        official = official_uf_means[state]
        uf_comparison.append({
            "uf": state,
            "calculated_unrounded": calculated,
            "calculated_rounded": int(round(calculated)),
            "official": official,
            "difference_rounded": int(round(calculated)) - official,
        })
        compatible_calculated = float(
            np.average(reconstructed_real_pc[mask], weights=weight[mask])
        )
        compatible_uf_comparison.append({
            "uf": state,
            "calculated_unrounded": compatible_calculated,
            "calculated_rounded": int(round(compatible_calculated)),
            "official": official,
            "difference_rounded": int(round(compatible_calculated)) - official,
        })

    condition_profile = []
    for code in sorted(np.unique(condition)):
        mask = condition == code
        condition_profile.append({
            "code": f"{int(code):02d}",
            "label": v2005_categories.get(f"{int(code):02d}", ""),
            "records": int(mask.sum()),
            "weight": float(np.sum(weight[mask & valid_weight])),
            "rdpc_present": int(np.sum(mask & rdpc_present)),
            "rdpc_missing": int(np.sum(mask & ~rdpc_present)),
        })

    children = analysis_mask & (age >= 0) & (age < 14)
    no_personal_income = analysis_mask & ((~np.isfinite(personal_income)) | (personal_income == 0))
    positive_household_rdpc = rdpc > 0

    top_values = top_frequencies(real_rdpc, selected_weight)

    mean_2264 = mean_variants["CO1"]
    gini = weighted_gini(real_rdpc, selected_weight)
    summary = {
        "phase": "1C",
        "generated_at": pd.Timestamp.now(tz="America/Sao_Paulo").isoformat(),
        "environment": {
            "os": platform.platform(),
            "python": sys.version.split()[0],
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "xlrd": xlrd.__version__,
            "zip_strategy": "streaming seletivo; TXT integral não extraído",
            "text_encoding": "ASCII para campos selecionados; layout latin-1",
        },
        "layout": {name: layout[name] for name in SELECTED},
        "dictionary": {
            "sheet": xlrd.open_workbook(DICTIONARY_PATH).sheet_names()[0],
            "selected_variables": dictionary_variables,
            "v2005_categories": v2005_categories,
            "vd5011_missing_representation": "campo vazio/blank; dicionário rotula como Não aplicável sem código numérico",
            "v1032_missing_representation": "campo vazio/blank; nenhum código numérico especial documentado",
        },
        "deflator": deflator_metadata,
        "structural": arrays["structural"],
        "rdpc_profile_all_records": profile_numeric(rdpc),
        "weight_profile_all_records": profile_numeric(weight),
        "weight_profile_eligible": profile_numeric(weight[analysis_mask]),
        "eligibility": {
            "documented_eligible_records": int(documented_eligible.sum()),
            "rdpc_present_records": int(rdpc_present.sum()),
            "analysis_records": int(analysis_mask.sum()),
            "eligible_without_rdpc": int(np.sum(documented_eligible & ~rdpc_present)),
            "excluded_with_rdpc": int(np.sum(~documented_eligible & rdpc_present)),
            "condition_profile": condition_profile,
        },
        "sanity_checks": {
            "eligible_children_records": int(children.sum()),
            "eligible_children_weight": float(np.sum(weight[children])),
            "eligible_children_with_positive_rdpc_records": int(np.sum(children & positive_household_rdpc)),
            "no_personal_income_with_positive_rdpc_records": int(np.sum(no_personal_income & positive_household_rdpc)),
            "no_personal_income_with_positive_rdpc_weight": float(np.sum(weight[no_personal_income & positive_household_rdpc])),
        },
        "mean_variants": mean_variants,
        "candidate_diagnostics": candidate_diagnostics,
        "mixed_component_reconstruction": {
            "formula": "sum(VD4019 * CO1 + VD4048 * CO1e) por domicílio / VD2003",
            "work_component": "VD4019",
            "other_sources_component": "VD4048",
            "work_deflator": "CO1",
            "other_sources_deflator": "CO1e",
            "households": int(household_count),
            "nominal_recomposition_nonzero_differences": int(
                np.sum(np.abs(nominal_recomposition_difference) > 1e-9)
            ),
            "nominal_recomposition_max_absolute_difference": float(
                np.max(np.abs(nominal_recomposition_difference))
            ),
            "component_blank_treatment": "blank estrutural tratado como ausência do componente; validado contra VD5007 nominal",
        },
        "official_compatible_diagnostic": {
            "formula": "sum(VD4019 * CO1 + VD4048 * CO1e) por domicílio / VD2003",
            "mean": float(np.average(compatible_real, weights=selected_weight)),
            "gini": weighted_gini(compatible_real, selected_weight),
            "zeros_records": int(np.sum(compatible_real == 0)),
            "zeros_weight": float(np.sum(selected_weight[compatible_real == 0])),
            "minimum": float(np.min(compatible_real)),
            "maximum": float(np.max(compatible_real)),
            "quantiles": compatible_quantiles,
            "top_values": top_frequencies(compatible_real, selected_weight),
            "quantile_comparison": [
                {
                    "quantile": label,
                    "calculated_unrounded": compatible_quantiles[label],
                    "calculated_rounded": int(round(compatible_quantiles[label])),
                    "official": official,
                    "difference_rounded": int(round(compatible_quantiles[label])) - official,
                }
                for label, official in official_quantiles.items()
            ],
            "accumulated_mean_comparison": compatible_accumulated_mean_comparison,
            "uf_mean_comparison": compatible_uf_comparison,
        },
        "benchmark_2264": {
            "calculated_unrounded": mean_2264,
            "calculated_rounded": int(round(mean_2264)),
            "official": 2264,
            "absolute_difference_unrounded": mean_2264 - 2264,
            "relative_difference": (mean_2264 - 2264) / 2264,
        },
        "population": {
            "calculated": calculated_population,
            "official": official_population_total,
            "absolute_difference": calculated_population - official_population_total,
            "relative_difference": (calculated_population - official_population_total) / official_population_total,
            "calculated_thousand_rounded": int(round(calculated_population / 1000)),
            "official_thousand": int(official_population_total / 1000),
            "all_records_weight": float(np.sum(weight[valid_weight])),
        },
        "zeros": {
            "records": int(np.sum(analysis_mask & (rdpc == 0))),
            "weight": float(np.sum(weight[analysis_mask & (rdpc == 0)])),
            "share_weight": float(np.sum(weight[analysis_mask & (rdpc == 0)]) / calculated_population),
        },
        "negatives": {
            "records": int(np.sum(analysis_mask & (rdpc < 0))),
            "weight": float(np.sum(weight[analysis_mask & (rdpc < 0)])),
        },
        "extremes": {
            "nominal_min": float(np.min(rdpc[analysis_mask])),
            "nominal_max": float(np.max(rdpc[analysis_mask])),
            "real_min": float(np.min(real_rdpc)),
            "real_max": float(np.max(real_rdpc)),
            "quantiles": quantiles,
            "top_values": top_values,
        },
        "gini": {
            "calculated": gini,
            "calculated_rounded_3": round(gini, 3),
            "official": 0.511,
            "difference_rounded_3": round(gini, 3) - 0.511,
        },
        "sidra": {
            "urls": SIDRA_URLS,
            "quantile_comparison": quantile_comparison,
            "accumulated_mean_comparison": accumulated_mean_comparison,
            "uf_mean_comparison": uf_comparison,
            "official_simple_population": [
                {"class": row["D4N"], "value_thousand": row["value"]}
                for row in numeric_sidra(sidra(SIDRA_URLS["simple_population"]))
            ],
            "official_accumulated_population": [
                {"class": row["D4N"], "value_thousand": row["value"]}
                for row in official_population_rows
            ],
        },
    }

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    summary_path = ARTIFACTS / "fase-1c-validation-summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    csv_path = ARTIFACTS / "fase-1c-variable-profile.csv"
    rows = [
        {"variable": "VD5011", "scope": "all records", **summary["rdpc_profile_all_records"]},
        {"variable": "V1032", "scope": "all records", **summary["weight_profile_all_records"]},
        {"variable": "V1032", "scope": "eligible analysis", **summary["weight_profile_eligible"]},
    ]
    columns = ["variable", "scope", "records", "valid", "missing_or_non_finite", "zero", "negative", "minimum", "maximum", "mean", "sum", "distinct"]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({
        "rows": arrays["structural"]["rows"],
        "analysis_records": int(analysis_mask.sum()),
        "mean_co1": mean_2264,
        "mean_co1_rounded": int(round(mean_2264)),
        "population": calculated_population,
        "population_thousand_rounded": int(round(calculated_population / 1000)),
        "gini": gini,
        "zero_records": summary["zeros"]["records"],
        "negative_records": summary["negatives"]["records"],
        "real_max": summary["extremes"]["real_max"],
        "quantile_matches": sum(item["difference_rounded"] == 0 for item in quantile_comparison),
        "quantile_total": len(quantile_comparison),
        "uf_mean_matches": sum(item["difference_rounded"] == 0 for item in uf_comparison),
        "uf_mean_total": len(uf_comparison),
        "compatible_quantile_matches": sum(
            int(round(compatible_quantiles[label])) == official
            for label, official in official_quantiles.items()
        ),
        "compatible_uf_mean_matches": sum(
            item["difference_rounded"] == 0 for item in compatible_uf_comparison
        ),
        "candidate_diagnostics": [
            {
                "candidate": item["candidate"],
                "mean": item["real_mean_unrounded"],
                "mean_rounded": item["real_mean_rounded"],
                "quantile_matches": item["quantile_exact_rounded_matches"],
            }
            for item in candidate_diagnostics
        ],
        "summary": str(summary_path.relative_to(ROOT)),
        "profile": str(csv_path.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
