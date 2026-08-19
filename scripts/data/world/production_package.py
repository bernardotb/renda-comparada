"""Materializa e valida o pacote canônico Mundo sem habilitar o frontend."""

from __future__ import annotations

import hashlib
import json
import math
import os
import tempfile
from copy import deepcopy
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
GENERATED_AT = "2026-08-19"
METHODOLOGY_VERSION = "D066-D070-v1"
PIP_VERSION = "20260324_2021"
PRODUCTION_BUILD = "20260324_2021_01_02_PROD"
REFERENCE_YEAR = 2024
PPP_BASE = 2021
CDF_CANDIDATE_SHA256 = "56C53483744176A50090E16058A0CF4FC6221C83D1D80A60060B931110C54DC2"
GOLDEN_CASES_SHA256 = "6EA8FB10D9BCE16380E5F311EFA789AC22EEA44BEFF119C33C61B1B0578FF779"
SOURCE_SHA256 = "99FC4B99BD6D77770DA78A5BFC90516F5FE35742C7A29968F2FD148B323B48A2"
PROCESSED_SHA256 = "2CA102013BDF9D3EA22C9642326544B32D45EF61407F81C6B71324BC5B072F52"
MAX_ABSOLUTE_ERROR_PP = "0.022516991848920"
getcontext().prec = 60


class WorldProductionError(RuntimeError):
    pass


def repository_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise WorldProductionError(f"Caminho fora da raiz canônica: {relative}")
    return path


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest().upper()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        handle.write(payload)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def require_file(path: Path, expected_sha256: str, expected_size: int | None = None) -> None:
    if not path.is_file():
        raise WorldProductionError(f"Artefato ausente: {path}")
    if expected_size is not None and path.stat().st_size != expected_size:
        raise WorldProductionError(f"Tamanho divergente: {path}")
    observed = sha256_file(path)
    if observed != expected_sha256:
        raise WorldProductionError(f"SHA-256 divergente: {path}: {observed} != {expected_sha256}")


def decimal_string(value: Any, label: str) -> str:
    try:
        parsed = Decimal(str(value))
    except Exception as error:
        raise WorldProductionError(f"{label} não numérico") from error
    if not parsed.is_finite():
        raise WorldProductionError(f"{label} não finito")
    return str(value)


def validate_cdf(document: Mapping[str, Any]) -> None:
    if document.get("schemaVersion") != "1.0.0" or document.get("dataset") != "world-income-cdf":
        raise WorldProductionError("Contrato da CDF Mundo inválido")
    if document.get("status") != "CANONICAL_PRODUCTION_FRONTEND_BLOCKED":
        raise WorldProductionError("Status da CDF Mundo inválido")
    if document.get("integration", {}).get("worldFrontendIntegrationAllowed") is not False:
        raise WorldProductionError("CDF Mundo não pode autorizar o frontend")
    methodology = document.get("methodology", {})
    if (
        methodology.get("pipVersion") != PIP_VERSION
        or methodology.get("productionBuild") != PRODUCTION_BUILD
        or methodology.get("referenceYear") != REFERENCE_YEAR
        or methodology.get("pppBase") != PPP_BASE
        or methodology.get("interpolation") != "none"
        or methodology.get("extrapolation") != "none"
    ):
        raise WorldProductionError("Metodologia da CDF Mundo divergente")
    points = document.get("points")
    stats = document.get("statistics", {})
    if not isinstance(points, list) or len(points) != 216_790 or stats.get("pointCount") != len(points):
        raise WorldProductionError("Contagem de pontos da CDF Mundo inválida")
    previous_welfare = Decimal("-Infinity")
    previous_cumulative = Decimal(0)
    for index, point in enumerate(points):
        if not isinstance(point, list) or len(point) != 2:
            raise WorldProductionError(f"Ponto CDF inválido: {index}")
        welfare = Decimal(decimal_string(point[0], f"welfare[{index}]"))
        cumulative = Decimal(decimal_string(point[1], f"cumulative[{index}]"))
        if welfare < 0 or welfare <= previous_welfare or cumulative <= previous_cumulative:
            raise WorldProductionError(f"CDF Mundo não monotônica: {index}")
        previous_welfare = welfare
        previous_cumulative = cumulative
    if str(points[0][0]) != stats.get("minWelfare") or str(points[-1][0]) != stats.get("maxWelfare"):
        raise WorldProductionError("Suporte da CDF Mundo divergente")
    if str(points[-1][1]) != stats.get("totalPopulationMillions"):
        raise WorldProductionError("População final da CDF Mundo divergente")


def validate_price_alignment(document: Mapping[str, Any]) -> None:
    required_strings = (
        "baseIndex",
        "currentIndex",
        "brazilPipPpp2021",
        "brazilPipCpi2024Base2021",
        "brlPerIntl2024Derived",
    )
    if document.get("schemaVersion") != "1.0.0" or document.get("dataset") != "world-price-alignment":
        raise WorldProductionError("Contrato de alinhamento Mundo inválido")
    if document.get("status") != "CANONICAL_PRODUCTION_FRONTEND_BLOCKED":
        raise WorldProductionError("Status do alinhamento Mundo inválido")
    if document.get("integration", {}).get("worldFrontendIntegrationAllowed") is not False:
        raise WorldProductionError("Alinhamento Mundo não pode autorizar o frontend")
    if document.get("pipVersion") != PIP_VERSION or document.get("productionBuild") != PRODUCTION_BUILD:
        raise WorldProductionError("Versão PIP do alinhamento Mundo divergente")
    if document.get("referenceYear") != REFERENCE_YEAR or document.get("pppBase") != PPP_BASE:
        raise WorldProductionError("Ano/base PPP do alinhamento Mundo divergente")
    if document.get("priceIndexReferenceMonth") != "2026-07":
        raise WorldProductionError("Mês corrente Mundo divergente")
    values = {key: Decimal(decimal_string(document.get(key), key)) for key in required_strings}
    if any(value <= 0 for value in values.values()):
        raise WorldProductionError("Fator não positivo no alinhamento Mundo")
    if values["baseIndex"] != Decimal("6952.07333333333333333333333333333333333333333333333333333333"):
        raise WorldProductionError("IPCA médio 2024 divergente")
    if values["currentIndex"] != Decimal("7657.7300000000000"):
        raise WorldProductionError("IPCA corrente divergente")
    if values["brazilPipPpp2021"] * values["brazilPipCpi2024Base2021"] != values["brlPerIntl2024Derived"]:
        raise WorldProductionError("Fator combinado Mundo não foi derivado dos fatores PIP")
    if document.get("combinedFactorState") != "DERIVED":
        raise WorldProductionError("Fator combinado Mundo deve ser DERIVED")
    raws = document.get("rawSources")
    if not isinstance(raws, list) or len(raws) != 3:
        raise WorldProductionError("Proveniência raw do alinhamento Mundo incompleta")
    for raw in raws:
        if not isinstance(raw, dict) or not raw.get("path") or not _is_sha256(raw.get("sha256")) or not raw.get("accessedAtUtc"):
            raise WorldProductionError("Referência raw do alinhamento Mundo inválida")


def validate_engine_manifest(document: Mapping[str, Any]) -> None:
    if document.get("schemaVersion") != "1.0.0" or document.get("dataset") != "world-income-engine":
        raise WorldProductionError("Contrato do manifesto Mundo inválido")
    if document.get("status") != "CANONICAL_APPROVED_FOR_INTEGRATION":
        raise WorldProductionError("Status do manifesto Mundo inválido")
    if document.get("integration", {}).get("worldFrontendIntegrationAllowed") is not True:
        raise WorldProductionError("Manifesto Mundo deve autorizar explicitamente o frontend")
    if document.get("decisionIds") != ["D066", "D067", "D068", "D069", "D070"]:
        raise WorldProductionError("Decisões canônicas do manifesto Mundo divergentes")
    methodology = document.get("methodology", {})
    if (
        methodology.get("version") != METHODOLOGY_VERSION
        or methodology.get("pipVersion") != PIP_VERSION
        or methodology.get("productionBuild") != PRODUCTION_BUILD
        or methodology.get("referenceYear") != REFERENCE_YEAR
        or methodology.get("pppBase") != PPP_BASE
    ):
        raise WorldProductionError("Metodologia do manifesto Mundo divergente")
    artifacts = document.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != {"cdf", "priceAlignment", "goldenCases"}:
        raise WorldProductionError("Referências de artefatos Mundo incompletas")
    for artifact in artifacts.values():
        if (
            not isinstance(artifact, dict)
            or not artifact.get("path")
            or not _is_sha256(artifact.get("sha256"))
            or not isinstance(artifact.get("sizeBytes"), int)
            or artifact["sizeBytes"] <= 0
        ):
            raise WorldProductionError("Referência de artefato Mundo inválida")
    if Decimal(str(document.get("maxAbsoluteErrorPp"))) != Decimal(MAX_ABSOLUTE_ERROR_PP):
        raise WorldProductionError("Erro máximo D068 divergente")


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(character in "0123456789ABCDEF" for character in value)


def verify_artifact(path: Path, contract: Mapping[str, Any]) -> None:
    require_file(path, str(contract["sha256"]), int(contract["sizeBytes"]))


def _artifact_contract(path: str, schema: str, version: str) -> dict[str, Any]:
    artifact_path = repository_path(path)
    return {
        "path": path,
        "schema": schema,
        "sha256": sha256_file(artifact_path),
        "sizeBytes": artifact_path.stat().st_size,
        "version": version,
    }


def build_package() -> dict[str, Any]:
    candidate_path = repository_path("validation/world/world-income-cdf-2024-candidate.json")
    golden_path = repository_path("validation/world/world-income-golden-cases-d070-candidate.json")
    source_path = repository_path("data/raw/world/pip-20260324-2021/GlobalDist1000bins_1990_2026_20260324_2021_01_02_PROD.csv")
    processed_path = repository_path("data/processed/world/pip-20260324-2021/world-bins-2024.csv")
    require_file(candidate_path, CDF_CANDIDATE_SHA256, 11_372_630)
    require_file(golden_path, GOLDEN_CASES_SHA256, 6_956)
    require_file(source_path, SOURCE_SHA256, 994_875_992)
    require_file(processed_path, PROCESSED_SHA256, 8_196_471)

    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    stats = candidate.get("statistics", {})
    methodology = candidate.get("methodology", {})
    if (
        candidate.get("status") != "CANDIDATE"
        or candidate.get("frontendIntegrationAllowed") is not False
        or methodology.get("pipVersion") != PIP_VERSION
        or methodology.get("productionBuild") != PRODUCTION_BUILD
        or methodology.get("referenceYear") != REFERENCE_YEAR
        or methodology.get("pppBase") != PPP_BASE
        or stats.get("sourceRows2024") != 218_000
        or stats.get("economies2024") != 218
        or stats.get("uniqueWelfarePoints") != 216_790
        or len(candidate.get("points", [])) != 216_790
    ):
        raise WorldProductionError("CDF candidata não satisfaz o contrato D068")

    schema_paths = {
        "cdf": "config/schemas/world-income-cdf.schema.json",
        "price": "config/schemas/world-price-alignment.schema.json",
        "engine": "config/schemas/world-income-engine-manifest.schema.json",
    }
    schema_hashes = {key: sha256_file(repository_path(path)) for key, path in schema_paths.items()}

    cdf = {
        "schemaVersion": "1.0.0",
        "schema": schema_paths["cdf"],
        "schemaSha256": schema_hashes["cdf"],
        "dataset": "world-income-cdf",
        "version": "2024-pip-20260324_2021-v1",
        "status": "CANONICAL_PRODUCTION_FRONTEND_BLOCKED",
        "generatedAt": GENERATED_AT,
        "generatedBy": "scripts/data/world/production_package.py",
        "source": {
            "provider": "World Bank",
            "dataset": "1000 Binned Global Distribution",
            "resource": "DR0094423",
            "rawPath": "data/raw/world/pip-20260324-2021/GlobalDist1000bins_1990_2026_20260324_2021_01_02_PROD.csv",
            "rawSha256": SOURCE_SHA256,
            "candidatePath": "validation/world/world-income-cdf-2024-candidate.json",
            "candidateSha256": CDF_CANDIDATE_SHA256,
        },
        "methodology": {
            "version": METHODOLOGY_VERSION,
            "pipVersion": PIP_VERSION,
            "productionBuild": PRODUCTION_BUILD,
            "referenceYear": REFERENCE_YEAR,
            "pppBase": PPP_BASE,
            "unit": "international_2021_ppp_per_person_per_day",
            "populationUnit": "millions_of_people",
            "lookup": "empirical_step_cdf",
            "tieSemantics": "equal welfare values form one step",
            "interpolation": "none",
            "extrapolation": "none",
        },
        "statistics": {
            "sourceBinCount": stats["sourceRows2024"],
            "economyCount": stats["economies2024"],
            "pointCount": stats["uniqueWelfarePoints"],
            "totalPopulationMillions": str(candidate["points"][-1][2]),
            "minWelfare": str(candidate["points"][0][0]),
            "maxWelfare": str(candidate["points"][-1][0]),
        },
        "pointColumns": ["welfare", "cumulativePopulationMillionsAtOrBelow"],
        "points": [[str(point[0]), str(point[2])] for point in candidate["points"]],
        "integration": {"worldFrontendIntegrationAllowed": False},
    }
    validate_cdf(cdf)
    cdf_path = repository_path("data/production/world/world-income-cdf-2024.json")
    atomic_write(cdf_path, canonical_json(cdf))

    provenance = json.loads(repository_path("validation/world/d069-pip-aux-provenance-production-build-retry.json").read_text(encoding="utf-8"))
    d070_config = json.loads(repository_path("config/world-d070-candidate.json").read_text(encoding="utf-8"))
    price = {
        "schemaVersion": "1.0.0",
        "schema": schema_paths["price"],
        "schemaSha256": schema_hashes["price"],
        "dataset": "world-price-alignment",
        "version": "2024-2026-07-pip-20260324_2021-v1",
        "status": "CANONICAL_PRODUCTION_FRONTEND_BLOCKED",
        "generatedAt": GENERATED_AT,
        "generatedBy": "scripts/data/world/production_package.py",
        "decisionIds": ["D069", "D070"],
        "source": "IBGE SIDRA",
        "sidraTable": 1737,
        "sidraVariable": 2266,
        "basePriceReference": "preços médios de 2024",
        "baseIndex": "6952.07333333333333333333333333333333333333333333333333333333",
        "priceIndexReferenceMonth": "2026-07",
        "currentIndex": "7657.7300000000000",
        "pipVersion": PIP_VERSION,
        "productionBuild": PRODUCTION_BUILD,
        "referenceYear": REFERENCE_YEAR,
        "pppBase": PPP_BASE,
        "brazilPipPpp2021": "2.44986319541931",
        "brazilPipCpi2024Base2021": "1.192919586578344",
        "brlPerIntl2024Derived": "2.92248979025310406149724542264",
        "combinedFactorState": "DERIVED",
        "formula": "dailyPPP = (householdIncomeCurrent / residents) * (baseIndex / currentIndex) / (brazilPipPpp2021 * brazilPipCpi2024Base2021) * 12 / 365",
        "temporalUpdateRule": "mês posterior exige evidência oficial preservada, atualização explícita, regeneração de golden cases, testes e promoção autorizada",
        "rawSources": [
            {
                "kind": "PIP_PPP",
                "path": d070_config["pppRawPath"],
                "sha256": d070_config["pppRawSha256"],
                "sizeBytes": repository_path(d070_config["pppRawPath"]).stat().st_size,
                "accessedAtUtc": provenance["ppp"]["accessedAtUtc"],
            },
            {
                "kind": "PIP_CPI",
                "path": d070_config["cpiRawPath"],
                "sha256": d070_config["cpiRawSha256"],
                "sizeBytes": repository_path(d070_config["cpiRawPath"]).stat().st_size,
                "accessedAtUtc": provenance["cpi"]["accessedAtUtc"],
            },
            {
                "kind": "IBGE_IPCA",
                "path": d070_config["ipcaRawPath"],
                "sha256": d070_config["ipcaRawSha256"],
                "sizeBytes": d070_config["ipcaRawSizeBytes"],
                "accessedAtUtc": d070_config["ipcaAccessedAtUtc"],
            },
        ],
        "precision": {"storage": "decimal_strings", "intermediateRounding": "none"},
        "integration": {"worldFrontendIntegrationAllowed": False},
    }
    validate_price_alignment(price)
    price_path = repository_path("data/production/world/world-price-alignment.json")
    atomic_write(price_path, canonical_json(price))

    manifest = {
        "schemaVersion": "1.0.0",
        "schema": schema_paths["engine"],
        "schemaSha256": schema_hashes["engine"],
        "dataset": "world-income-engine",
        "version": "1.0.0",
        "status": "CANONICAL_APPROVED_FOR_INTEGRATION",
        "generatedAt": GENERATED_AT,
        "generatedBy": "scripts/data/world/production_package.py",
        "decisionIds": ["D066", "D067", "D068", "D069", "D070"],
        "artifacts": {
            "cdf": _artifact_contract("data/production/world/world-income-cdf-2024.json", schema_paths["cdf"], cdf["version"]),
            "priceAlignment": _artifact_contract("data/production/world/world-price-alignment.json", schema_paths["price"], price["version"]),
            "goldenCases": {
                "path": "validation/world/world-income-golden-cases-d070-candidate.json",
                "schema": "scripts/data/world/d070.py::run",
                "sha256": GOLDEN_CASES_SHA256,
                "sizeBytes": golden_path.stat().st_size,
                "version": "D070-v1",
            },
        },
        "methodology": {
            "version": METHODOLOGY_VERSION,
            "pipVersion": PIP_VERSION,
            "productionBuild": PRODUCTION_BUILD,
            "referenceYear": REFERENCE_YEAR,
            "pppBase": PPP_BASE,
            "source": "World Bank Poverty and Inequality Platform",
            "resource": "DR0094423",
            "unit": "international_2021_ppp_per_person_per_day",
            "lookup": {
                "shareBelow": "population with welfare < x / total population",
                "shareAtOrBelow": "population with welfare <= x / total population",
                "topShare": "1 - shareBelow",
                "interpolation": "none",
                "extrapolation": "none",
            },
        },
        "displayPolicy": {
            "decisionId": "D070",
            "language": "posição monetária global estimada",
            "mainRange": "integer complementary percentile and TOP",
            "upperTail": "one decimal from 0.1% through below 1%",
            "extremeTail": "less than 0.1% only when topPercent + maxAbsoluteErrorPp < 0.1; otherwise approximately 0.1%",
            "support": "no TOP 100% headline, no TOP 0%, no interpolation or extrapolation",
        },
        "maxAbsoluteErrorPp": MAX_ABSOLUTE_ERROR_PP,
        "delivery": {
            "failSafe": "unavailable on any missing, malformed, size/hash or cross-reference failure",
            "requestData": "static artifact paths only; no income, residents, percentile or result",
            "persistence": "none",
            "legacyFallback": "forbidden",
        },
        "integration": {"worldFrontendIntegrationAllowed": True},
    }
    validate_engine_manifest(manifest)
    manifest_path = repository_path("data/production/world/world-income-engine-manifest.json")
    atomic_write(manifest_path, canonical_json(manifest))

    loaded_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_engine_manifest(loaded_manifest)
    verify_artifact(cdf_path, loaded_manifest["artifacts"]["cdf"])
    verify_artifact(price_path, loaded_manifest["artifacts"]["priceAlignment"])
    verify_artifact(golden_path, loaded_manifest["artifacts"]["goldenCases"])
    validate_cdf(json.loads(cdf_path.read_text(encoding="utf-8")))
    validate_price_alignment(json.loads(price_path.read_text(encoding="utf-8")))
    return {
        "status": "PASS",
        "cdf": {**loaded_manifest["artifacts"]["cdf"], "pointCount": 216_790},
        "priceAlignment": loaded_manifest["artifacts"]["priceAlignment"],
        "manifest": {
            "path": "data/production/world/world-income-engine-manifest.json",
            "sha256": sha256_file(manifest_path),
            "sizeBytes": manifest_path.stat().st_size,
        },
        "worldFrontendIntegrationAllowed": True,
    }


def validate_negative_mutations() -> None:
    manifest = json.loads(repository_path("data/production/world/world-income-engine-manifest.json").read_text(encoding="utf-8"))
    price = json.loads(repository_path("data/production/world/world-price-alignment.json").read_text(encoding="utf-8"))
    mutations = []
    for key, value in (("worldFrontendIntegrationAllowed", False),):
        changed = deepcopy(manifest)
        changed["integration"][key] = value
        mutations.append((validate_engine_manifest, changed))
    for field, value in (("pipVersion", "wrong"), ("referenceYear", 2025), ("pppBase", 2017)):
        changed = deepcopy(manifest)
        changed["methodology"][field] = value
        mutations.append((validate_engine_manifest, changed))
    changed = deepcopy(price)
    changed["brlPerIntl2024Derived"] = "2.9"
    mutations.append((validate_price_alignment, changed))
    for validator, document in mutations:
        try:
            validator(document)
        except WorldProductionError:
            continue
        raise WorldProductionError("Mutação inválida foi aceita pelo contrato Mundo")


if __name__ == "__main__":
    result = build_package()
    validate_negative_mutations()
    print(json.dumps(result, ensure_ascii=False, indent=2))
