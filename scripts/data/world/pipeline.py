"""Pipeline de pesquisa da CDF mundial candidata, sem integração de produção."""

from __future__ import annotations

import bisect
import csv
import hashlib
import json
import math
import os
import statistics
import tempfile
import urllib.request
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = ROOT / "config/world-pip-2024-candidate.json"
DOWNLOAD_CHUNK_SIZE = 4 * 1024 * 1024


class WorldPipelineError(RuntimeError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(DOWNLOAD_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def repository_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise WorldPipelineError(f"Caminho fora da raiz canônica: {relative}")
    return path


def repository_display_path(path: Path) -> str:
    resolved = path.resolve()
    if resolved.is_relative_to(ROOT.resolve()):
        return resolved.relative_to(ROOT.resolve()).as_posix()
    return str(resolved)


def decimal_value(value: Any, label: str) -> Decimal:
    try:
        parsed = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise WorldPipelineError(f"{label} não numérico: {value!r}") from error
    if not parsed.is_finite():
        raise WorldPipelineError(f"{label} não finito: {value!r}")
    return parsed


def decimal_text(value: Decimal) -> str:
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
        temporary.write(payload)
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, path)


def atomic_write_text(path: Path, payload: str) -> None:
    atomic_write_bytes(path, payload.encode("utf-8"))


def official_evidence_contract(
    config: Mapping[str, Any],
) -> tuple[Mapping[str, Any], dict[str, Mapping[str, Any]]]:
    evidence = config.get("officialEvidence")
    if not isinstance(evidence, Mapping):
        raise WorldPipelineError("Contrato de evidência oficial ausente ou inválido")
    citation = evidence.get("citation")
    checkpoints = evidence.get("checkpoints")
    if not isinstance(citation, Mapping) or not isinstance(checkpoints, list):
        raise WorldPipelineError("Contrato de citation/checkpoints ausente ou inválido")

    def validate_item(item: Mapping[str, Any], label: str) -> None:
        required = {"path", "url", "sizeBytes", "sha256"}
        missing = sorted(required - set(item))
        if missing:
            raise WorldPipelineError(f"Contrato de {label} incompleto: {missing}")
        size = item["sizeBytes"]
        expected_hash = str(item["sha256"])
        if not isinstance(size, int) or size <= 0:
            raise WorldPipelineError(f"Tamanho esperado inválido para {label}: {size!r}")
        if len(expected_hash) != 64 or any(character not in "0123456789ABCDEF" for character in expected_hash):
            raise WorldPipelineError(f"SHA-256 esperado inválido para {label}")

    validate_item(citation, "citation")
    raw_directory = str(config["rawOfficialDirectory"]).rstrip("/")
    expected_citation_path = f"{raw_directory}/citation-ppp-2021.json"
    if citation["path"] != expected_citation_path or citation["url"] != config["citationEndpoint"]:
        raise WorldPipelineError("Contrato de citation diverge dos paths/endpoints canônicos")

    by_line: dict[str, Mapping[str, Any]] = {}
    for item in checkpoints:
        if not isinstance(item, Mapping) or "povertyLine" not in item:
            raise WorldPipelineError("Contrato de checkpoint sem povertyLine")
        key = decimal_text(decimal_value(item["povertyLine"], "povertyLine contratada"))
        if key in by_line:
            raise WorldPipelineError(f"Checkpoint contratado em duplicidade: {key}")
        validate_item(item, f"checkpoint {key}")
        expected_path = f"{raw_directory}/pc-regional-aggregates-{key.replace('.', '_')}.json"
        expected_url = str(config["checkpointEndpointTemplate"]).format(poverty_line=key)
        if item["path"] != expected_path or item["url"] != expected_url:
            raise WorldPipelineError(f"Contrato de checkpoint diverge para {key}")
        by_line[key] = item

    expected_lines = [decimal_text(decimal_value(value, "validation line")) for value in config["validationLines"]]
    if len(expected_lines) != len(set(expected_lines)) or set(by_line) != set(expected_lines):
        raise WorldPipelineError(
            f"Conjunto de checkpoints contratados divergiu: {sorted(by_line)} != {sorted(expected_lines)}"
        )
    return citation, by_line


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "status",
        "provider",
        "dataset",
        "catalogUrl",
        "resourceId",
        "sourceFileName",
        "sourceUrl",
        "sourceContentLength",
        "sourceSha256",
        "accessedAt",
        "pipVersion",
        "productionBuild",
        "referenceYear",
        "pppBase",
        "unit",
        "populationUnit",
        "sourceColumns",
        "validationLines",
        "citationEndpoint",
        "checkpointEndpointTemplate",
        "officialEvidence",
        "rawSourcePath",
        "rawOfficialDirectory",
        "processedPath",
        "candidatePath",
        "validationJsonPath",
        "validationMarkdownPath",
        "checkpointCsvPath",
    }
    missing = sorted(required - set(config))
    if missing:
        raise WorldPipelineError(f"Configuração Mundo incompleta: {missing}")
    if config["status"] != "CANDIDATE_RESEARCH":
        raise WorldPipelineError("Configuração Mundo não está marcada como pesquisa candidata")
    official_evidence_contract(config)
    return config


def download_file(
    url: str,
    path: Path,
    expected_size: int | None = None,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    expected_hash = expected_sha256.upper() if expected_sha256 is not None else None
    if path.is_file():
        observed_size = path.stat().st_size
        observed_hash = sha256_file(path)
        if expected_size is not None and observed_size != expected_size:
            raise WorldPipelineError(
                f"Tamanho da evidência local divergiu para {path.name}: {observed_size} != {expected_size}"
            )
        if expected_hash is not None and observed_hash != expected_hash:
            raise WorldPipelineError(
                f"SHA-256 da evidência local divergiu para {path.name}: {observed_hash} != {expected_hash}"
            )
        return {"path": repository_display_path(path), "sizeBytes": observed_size, "sha256": observed_hash, "reused": True}

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "RendaComparada-D068-Research/1.0"})
    downloaded = 0
    digest = hashlib.sha256()
    try:
        with urllib.request.urlopen(request, timeout=120) as response, temporary.open("wb") as output:
            announced = response.headers.get("Content-Length")
            if expected_size is not None and announced and int(announced) != expected_size:
                raise WorldPipelineError(
                    f"Tamanho anunciado divergiu para {path.name}: {announced} != {expected_size}"
                )
            while True:
                chunk = response.read(DOWNLOAD_CHUNK_SIZE)
                if not chunk:
                    break
                output.write(chunk)
                digest.update(chunk)
                downloaded += len(chunk)
                if downloaded and downloaded % (100 * 1024 * 1024) < DOWNLOAD_CHUNK_SIZE:
                    print(f"download {path.name}: {downloaded / 1024 / 1024:.0f} MiB", flush=True)
        if expected_size is not None and downloaded != expected_size:
            raise WorldPipelineError(
                f"Download incompleto de {path.name}: {downloaded} != {expected_size}"
            )
        observed_hash = digest.hexdigest().upper()
        if expected_hash is not None and observed_hash != expected_hash:
            raise WorldPipelineError(
                f"SHA-256 da evidência obtida divergiu para {path.name}: {observed_hash} != {expected_hash}"
            )
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return {"path": repository_display_path(path), "sizeBytes": downloaded, "sha256": observed_hash, "reused": False}


@dataclass(frozen=True)
class WorldCdf:
    welfare: tuple[Decimal, ...]
    weight_at: tuple[Decimal, ...]
    cumulative_at_or_below: tuple[Decimal, ...]
    total_weight: Decimal

    def __post_init__(self) -> None:
        size = len(self.welfare)
        if size == 0 or len(self.weight_at) != size or len(self.cumulative_at_or_below) != size:
            raise WorldPipelineError("Vetores da CDF mundial ausentes ou divergentes")
        if any(left >= right for left, right in zip(self.welfare, self.welfare[1:])):
            raise WorldPipelineError("Suporte da CDF mundial não está estritamente ordenado")
        if any(weight <= 0 for weight in self.weight_at):
            raise WorldPipelineError("CDF mundial contém peso não positivo")
        if any(left >= right for left, right in zip(self.cumulative_at_or_below, self.cumulative_at_or_below[1:])):
            raise WorldPipelineError("CDF mundial não é estritamente crescente em peso")
        if self.cumulative_at_or_below[-1] != self.total_weight:
            raise WorldPipelineError("Peso acumulado final diverge da população total")

    def lookup(self, value: Any) -> dict[str, float]:
        target = decimal_value(value, "welfare")
        left = bisect.bisect_left(self.welfare, target)
        right = bisect.bisect_right(self.welfare, target)
        below = Decimal(0) if left == 0 else self.cumulative_at_or_below[left - 1]
        at_or_below = Decimal(0) if right == 0 else self.cumulative_at_or_below[right - 1]
        result = {
            "shareBelow": float(below / self.total_weight),
            "shareAtOrBelow": float(at_or_below / self.total_weight),
            "topShare": float(Decimal(1) - below / self.total_weight),
        }
        if any(not math.isfinite(item) or item < 0 or item > 1 for item in result.values()):
            raise WorldPipelineError(f"Lookup mundial fora dos limites: {result}")
        return result

    def weighted_quantile(self, probability: Any) -> Decimal:
        p = decimal_value(probability, "probabilidade")
        if p < 0 or p > 1:
            raise WorldPipelineError("Probabilidade fora de [0,1]")
        if p == 0:
            return self.welfare[0]
        index = bisect.bisect_left(self.cumulative_at_or_below, p * self.total_weight)
        return self.welfare[min(index, len(self.welfare) - 1)]


def build_cdf(grouped: Mapping[Decimal, Decimal]) -> WorldCdf:
    if not grouped:
        raise WorldPipelineError("Nenhum ponto mundial válido foi encontrado")
    welfare = tuple(sorted(grouped))
    weights = tuple(grouped[item] for item in welfare)
    cumulative: list[Decimal] = []
    running = Decimal(0)
    for weight in weights:
        running += weight
        cumulative.append(running)
    return WorldCdf(welfare, weights, tuple(cumulative), running)


def process_source(source_path: Path, processed_path: Path, config: Mapping[str, Any]) -> tuple[WorldCdf, dict[str, Any]]:
    reference_year = int(config["referenceYear"])
    expected_build = str(config["productionBuild"])
    expected_columns = list(config["sourceColumns"])
    grouped: dict[Decimal, Decimal] = {}
    keys: set[tuple[str, int]] = set()
    bins_by_economy: dict[str, int] = {}
    rows = 0
    zero_rows = 0
    duplicate_keys = 0

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = processed_path.with_suffix(processed_path.suffix + ".part")
    with source_path.open("r", encoding="utf-8-sig", newline="") as source, temporary.open(
        "w", encoding="utf-8", newline=""
    ) as output:
        reader = csv.DictReader(source)
        if reader.fieldnames != expected_columns:
            raise WorldPipelineError(f"Schema bruto divergiu: {reader.fieldnames}")
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(["code", "quantile", "welf", "pop"])
        for row_number, row in enumerate(reader, start=2):
            try:
                year = int(row["year"])
            except ValueError as error:
                raise WorldPipelineError(f"Ano inválido na linha {row_number}") from error
            if year < reference_year:
                continue
            if year > reference_year:
                continue
            if row["pipvintage"] != expected_build:
                raise WorldPipelineError(f"Vintage divergente na linha {row_number}: {row['pipvintage']}")
            code = row["code"].strip()
            try:
                quantile = int(row["quantile"])
            except ValueError as error:
                raise WorldPipelineError(f"Quantil inválido na linha {row_number}") from error
            welfare = decimal_value(row["welf"], "welf")
            population = decimal_value(row["pop"], "pop")
            if not code or not 1 <= quantile <= 1000:
                raise WorldPipelineError(f"Chave inválida na linha {row_number}")
            if welfare < 0:
                raise WorldPipelineError(f"Welfare negativo na linha {row_number}")
            if population <= 0:
                raise WorldPipelineError(f"População não positiva na linha {row_number}")
            key = (code, quantile)
            if key in keys:
                duplicate_keys += 1
                raise WorldPipelineError(f"Chave code+year+quantile duplicada: {key}")
            keys.add(key)
            bins_by_economy[code] = bins_by_economy.get(code, 0) + 1
            grouped[welfare] = grouped.get(welfare, Decimal(0)) + population
            writer.writerow([code, quantile, decimal_text(welfare), decimal_text(population)])
            rows += 1
            zero_rows += int(welfare == 0)
    os.replace(temporary, processed_path)

    incomplete = {code: count for code, count in bins_by_economy.items() if count != 1000}
    if incomplete:
        raise WorldPipelineError(f"Economias sem 1000 bins em 2024: {incomplete}")
    cdf = build_cdf(grouped)
    diagnostics = {
        "sourceRows2024": rows,
        "economies2024": len(bins_by_economy),
        "binsPerEconomy": 1000,
        "duplicateKeys": duplicate_keys,
        "zeroWelfareRows": zero_rows,
        "uniqueWelfarePoints": len(cdf.welfare),
        "totalPopulationMillions": float(cdf.total_weight),
        "minWelfare": float(cdf.welfare[0]),
        "maxWelfare": float(cdf.welfare[-1]),
        "processedSha256": sha256_file(processed_path),
        "processedSizeBytes": processed_path.stat().st_size,
    }
    return cdf, diagnostics


def distribution_statistics(cdf: WorldCdf) -> dict[str, Any]:
    total_income = sum((value * weight for value, weight in zip(cdf.welfare, cdf.weight_at)), Decimal(0))
    mean = total_income / cdf.total_weight
    cumulative_income = Decimal(0)
    lorenz_sum = Decimal(0)
    for value, weight in zip(cdf.welfare, cdf.weight_at):
        previous = cumulative_income
        cumulative_income += value * weight
        lorenz_sum += weight * (cumulative_income + previous)
    gini = Decimal(1) - lorenz_sum / (cdf.total_weight * total_income)
    probabilities = ["0.01", "0.05", "0.10", "0.25", "0.50", "0.75", "0.90", "0.95", "0.99", "0.995", "0.999"]
    quantiles = {f"P{float(p) * 100:g}": float(cdf.weighted_quantile(p)) for p in probabilities}
    zero = cdf.lookup(0)
    return {
        "mean": float(mean),
        "median": quantiles["P50"],
        "giniFromBinnedCandidate": float(gini),
        "quantiles": quantiles,
        "zeroShareAtOrBelow": zero["shareAtOrBelow"],
        "min": float(cdf.welfare[0]),
        "max": float(cdf.welfare[-1]),
    }


def fetch_official_evidence(config: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    raw_directory = repository_path(config["rawOfficialDirectory"])
    citation_contract, checkpoint_contracts = official_evidence_contract(config)
    citation_path = repository_path(str(citation_contract["path"]))
    citation_download = download_file(
        str(citation_contract["url"]),
        citation_path,
        int(citation_contract["sizeBytes"]),
        str(citation_contract["sha256"]),
    )
    citation = json.loads(citation_path.read_text(encoding="utf-8-sig"))
    versions = citation.get("version_id", [])
    if versions != [config["productionBuild"]]:
        raise WorldPipelineError(f"Build da citação PIP divergiu: {versions}")

    checkpoints: list[dict[str, Any]] = []
    raw_hashes: dict[str, str] = {citation_path.name: citation_download["sha256"]}
    for poverty_line in config["validationLines"]:
        line_text = decimal_text(decimal_value(poverty_line, "validation line"))
        contract = checkpoint_contracts[line_text]
        url = str(contract["url"])
        path = repository_path(str(contract["path"]))
        if path.parent != raw_directory:
            raise WorldPipelineError(f"Diretório de checkpoint divergiu para {line_text}")
        downloaded = download_file(
            url,
            path,
            int(contract["sizeBytes"]),
            str(contract["sha256"]),
        )
        raw_hashes[path.name] = downloaded["sha256"]
        response = json.loads(path.read_text(encoding="utf-8-sig"))
        matches = [
            row
            for row in response
            if row.get("region_code") == "WLD"
            and int(row.get("reporting_year", -1)) == int(config["referenceYear"])
            and decimal_value(row.get("poverty_line"), "poverty_line") == decimal_value(poverty_line, "validation line")
        ]
        if len(matches) != 1:
            raise WorldPipelineError(f"Checkpoint oficial ambíguo para {poverty_line}: {len(matches)}")
        row = matches[0]
        checkpoints.append(
            {
                "povertyLine": float(poverty_line),
                "headcount": float(row["headcount"]),
                "reportingPopulationMillions": float(row["reporting_pop"]),
                "populationBelowMillions": float(row["pop_in_poverty"]),
                "estimateType": row["estimate_type"],
                "sourceUrl": url,
                "rawResponseSha256": downloaded["sha256"],
            }
        )
    provenance = {
        "citation": citation["citation"][0],
        "versionId": versions[0],
        "accessedAt": citation["date_accessed"][0],
        "citationUrl": config["citationEndpoint"],
        "rawResponseHashes": raw_hashes,
    }
    return checkpoints, provenance


def compare_checkpoints(cdf: WorldCdf, official: Iterable[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, float]]:
    comparisons: list[dict[str, Any]] = []
    signed_errors: list[float] = []
    for item in official:
        candidate = cdf.lookup(item["povertyLine"])["shareBelow"]
        signed = candidate - float(item["headcount"])
        signed_errors.append(signed * 100)
        comparisons.append(
            {
                **item,
                "candidateShareBelow": candidate,
                "errorSignedPp": signed * 100,
                "errorAbsPp": abs(signed) * 100,
            }
        )
    absolute = [abs(value) for value in signed_errors]
    metrics = {
        "maxAbsErrorPp": max(absolute),
        "meanAbsErrorPp": statistics.fmean(absolute),
        "medianAbsErrorPp": statistics.median(absolute),
        "rmsePp": math.sqrt(statistics.fmean(value * value for value in signed_errors)),
        "signedMeanErrorPp": statistics.fmean(signed_errors),
    }
    return comparisons, metrics


def structural_checks(cdf: WorldCdf, diagnostics: Mapping[str, Any], config: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [
        ("reference_year_isolated", diagnostics["sourceRows2024"] > 0, config["referenceYear"]),
        ("unique_code_year_quantile", diagnostics["duplicateKeys"] == 0, diagnostics["duplicateKeys"]),
        ("one_thousand_bins_per_economy", diagnostics["binsPerEconomy"] == 1000, diagnostics["economies2024"]),
        ("finite_nonnegative_welfare", all(value.is_finite() and value >= 0 for value in cdf.welfare), diagnostics["minWelfare"]),
        ("finite_positive_population", all(value.is_finite() and value > 0 for value in cdf.weight_at), diagnostics["totalPopulationMillions"]),
        ("strictly_ordered_support", all(left < right for left, right in zip(cdf.welfare, cdf.welfare[1:])), diagnostics["uniqueWelfarePoints"]),
        ("strictly_increasing_cumulative_weight", all(left < right for left, right in zip(cdf.cumulative_at_or_below, cdf.cumulative_at_or_below[1:])), None),
        ("cdf_final_weight_equals_population", cdf.cumulative_at_or_below[-1] == cdf.total_weight, decimal_text(cdf.total_weight)),
        ("frontend_integration_blocked", True, False),
    ]
    return [{"name": name, "status": "PASS" if passed else "FAIL", "detail": detail} for name, passed, detail in checks]


def candidate_document(cdf: WorldCdf, diagnostics: Mapping[str, Any], statistics_value: Mapping[str, Any], source: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": "1.0.0-candidate",
        "status": "CANDIDATE",
        "frontendIntegrationAllowed": False,
        "source": {
            "provider": config["provider"],
            "dataset": config["dataset"],
            "catalogUrl": config["catalogUrl"],
            "resourceId": config["resourceId"],
            "fileName": config["sourceFileName"],
            "url": config["sourceUrl"],
            "sizeBytes": source["sizeBytes"],
            "sha256": source["sha256"],
            "lastUpdated": config["sourceLastUpdated"],
            "accessedAt": config["accessedAt"],
            "license": config["license"],
        },
        "methodology": {
            "pipVersion": config["pipVersion"],
            "productionBuild": config["productionBuild"],
            "referenceYear": config["referenceYear"],
            "pppBase": config["pppBase"],
            "unit": config["unit"],
            "populationUnit": config["populationUnit"],
            "construction": "year=2024; group equal welf; weight by pop; empirical step CDF; no interpolation",
            "tieSemantics": "equal welf values are grouped into one population-weighted step",
            "missingTreatment": "missing/non-numeric required values fail the pipeline",
            "zeroTreatment": "zero is preserved as an observed support value",
            "aboveMaximum": "no extrapolation",
        },
        "statistics": {**diagnostics, **statistics_value},
        "pointColumns": ["welfare", "weightAtMillions", "cumulativeAtOrBelowMillions"],
        "points": [
            [decimal_text(welfare), decimal_text(weight), decimal_text(cumulative)]
            for welfare, weight, cumulative in zip(cdf.welfare, cdf.weight_at, cdf.cumulative_at_or_below)
        ],
    }


def markdown_report(report: Mapping[str, Any]) -> str:
    stats = report["statistics"]
    errors = report["validationMetrics"]
    lines = [
        "# Validação da CDF mundial candidata — D068",
        "",
        "> Artefato de pesquisa. Não canônico. Integração frontend bloqueada.",
        "",
        f"- Build PIP: `{report['provenance']['versionId']}`",
        f"- Ano: `{report['referenceYear']}`",
        f"- Fonte SHA-256: `{report['source']['sha256']}`",
        f"- CDF candidata SHA-256: `{report['candidate']['sha256']}`",
        f"- População: `{stats['totalPopulationMillions']:.4f}` milhões",
        f"- Economias: `{stats['economies2024']}`",
        f"- Pontos únicos: `{stats['uniqueWelfarePoints']}`",
        "",
        "## Checks estruturais",
        "",
        "| Check | Status | Detalhe |",
        "|---|---|---|",
    ]
    lines.extend(f"| {item['name']} | {item['status']} | {item['detail']} |" for item in report["structuralChecks"])
    lines.extend([
        "",
        "## Checkpoints oficiais",
        "",
        "| Linha PPP/dia | PIP | CDF candidata | Erro abs. (pp) |",
        "|---:|---:|---:|---:|",
    ])
    lines.extend(
        f"| {item['povertyLine']:.2f} | {item['headcount']:.6f} | {item['candidateShareBelow']:.6f} | {item['errorAbsPp']:.6f} |"
        for item in report["checkpoints"]
    )
    lines.extend([
        "",
        "## Perfil de erro",
        "",
        f"- máximo absoluto: `{errors['maxAbsErrorPp']:.6f}` pp",
        f"- médio absoluto: `{errors['meanAbsErrorPp']:.6f}` pp",
        f"- RMSE: `{errors['rmsePp']:.6f}` pp",
        f"- viés médio: `{errors['signedMeanErrorPp']:.6f}` pp",
        "",
        "A tolerância de produto não é definida por esta execução; deve ser decidida após revisão humana do erro medido e antes de D070.",
        "",
        "## Limitação material",
        "",
        "A base representa cada bin pela média de welfare e perde desigualdade dentro do bin. Os quantis e o Gini abaixo são diagnósticos da candidata, não estatísticas oficiais publicadas diretamente pelo PIP.",
        "",
        "## Estatísticas diagnósticas",
        "",
        f"- média: `{stats['mean']:.8f}`",
        f"- mediana: `{stats['median']:.8f}`",
        f"- Gini binned: `{stats['giniFromBinnedCandidate']:.8f}`",
        f"- mínimo: `{stats['min']:.8f}`",
        f"- máximo: `{stats['max']:.8f}`",
        "",
        "| Quantil | Welfare PPP 2021/dia |",
        "|---|---:|",
    ])
    lines.extend(f"| {name} | {value:.8f} |" for name, value in stats["quantiles"].items())
    return "\n".join(lines) + "\n"


def run_pipeline(config_path: Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    config = load_config(config_path)
    source_path = repository_path(config["rawSourcePath"])
    source = download_file(str(config["sourceUrl"]), source_path, int(config["sourceContentLength"]))
    if source["sha256"] != config["sourceSha256"]:
        raise WorldPipelineError(
            f"SHA-256 da fonte divergiu: {source['sha256']} != {config['sourceSha256']}"
        )
    processed_path = repository_path(config["processedPath"])
    cdf, diagnostics = process_source(source_path, processed_path, config)
    stats = distribution_statistics(cdf)
    official, provenance = fetch_official_evidence(config)
    comparisons, validation_metrics = compare_checkpoints(cdf, official)
    checks = structural_checks(cdf, diagnostics, config)
    if any(item["status"] != "PASS" for item in checks):
        raise WorldPipelineError("Validação estrutural falhou")

    candidate_path = repository_path(config["candidatePath"])
    candidate = candidate_document(cdf, diagnostics, stats, source, config)
    atomic_write_text(candidate_path, canonical_json(candidate))
    candidate_hash = sha256_file(candidate_path)

    population_differences = [
        abs(float(item["reportingPopulationMillions"]) - float(diagnostics["totalPopulationMillions"]))
        for item in comparisons
    ]
    report = {
        "status": "CANDIDATE_VALIDATED_NOT_CANONICAL",
        "frontendIntegrationAllowed": False,
        "referenceYear": config["referenceYear"],
        "source": source,
        "processed": {
            "path": config["processedPath"],
            "sizeBytes": diagnostics["processedSizeBytes"],
            "sha256": diagnostics["processedSha256"],
        },
        "candidate": {
            "path": config["candidatePath"],
            "sizeBytes": candidate_path.stat().st_size,
            "sha256": candidate_hash,
        },
        "provenance": provenance,
        "statistics": {**diagnostics, **stats},
        "structuralChecks": checks,
        "checkpoints": comparisons,
        "validationMetrics": validation_metrics,
        "populationReconciliation": {
            "candidateMillions": diagnostics["totalPopulationMillions"],
            "officialMillions": comparisons[0]["reportingPopulationMillions"],
            "maxAbsoluteDifferenceMillions": max(population_differences),
        },
        "decisionGate": {
            "status": "PENDING_HUMAN_TOLERANCE_AND_REVIEW",
            "reason": "erro medido; tolerância e precisão de D070 ainda não decididas",
        },
    }
    validation_json_path = repository_path(config["validationJsonPath"])
    atomic_write_text(validation_json_path, canonical_json(report))
    atomic_write_text(repository_path(config["validationMarkdownPath"]), markdown_report(report))

    checkpoint_path = repository_path(config["checkpointCsvPath"])
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=checkpoint_path.parent, delete=False) as temporary:
        writer = csv.DictWriter(
            temporary,
            fieldnames=["povertyLine", "headcount", "candidateShareBelow", "errorSignedPp", "errorAbsPp", "reportingPopulationMillions", "populationBelowMillions", "estimateType", "sourceUrl", "rawResponseSha256"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(comparisons)
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, checkpoint_path)
    report["checkpointCsvSha256"] = sha256_file(checkpoint_path)
    atomic_write_text(validation_json_path, canonical_json(report))
    return report
