"""Gera e valida o contrato de produção do motor de renda Brasil.

O módulo promove apenas decisões já canonizadas (D063, D065, D071 e D072),
preserva a CDF histórica byte a byte e falha quando qualquer dependência diverge.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from decimal import Decimal, getcontext, localcontext
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from cdf import IncomeCdf, load_cdf_artifact
from pipeline import ROOT, PipelineError, canonical_json, sha256_file
from price_alignment import (
    income_current_to_base,
    load_price_alignment_proposal,
    normalized_series,
    validate_proposal,
)


RELEASE_DATE = "2026-08-15"
CDF_PATH = ROOT / "data/production/brazil/brazil-income-cdf-2025.json"
PRICE_PATH = ROOT / "data/production/brazil/brazil-price-alignment.json"
ENGINE_PATH = ROOT / "data/production/brazil/brazil-income-engine-manifest.json"
PROPOSAL_PATH = ROOT / "validation/brazil/brazil-price-alignment-proposal.json"
GOLDEN_PATH = ROOT / "validation/brazil/brazil-income-golden-cases.json"
PRICE_SCHEMA_PATH = ROOT / "config/schemas/brazil-price-alignment.schema.json"
ENGINE_SCHEMA_PATH = ROOT / "config/schemas/brazil-income-engine-manifest.schema.json"
REPORT_JSON_PATH = ROOT / "validation/brazil/brazil-production-package-validation.json"
REPORT_MD_PATH = ROOT / "validation/brazil/brazil-production-package-validation.md"

EXPECTED_CDF_SHA256 = "5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5"
EXPECTED_CDF_SIZE_BYTES = 3_955_036
EXPECTED_SOURCE_SHA256 = "8A44A26C47F16BE54DE787D215145C60B82E33319F806A0F890411B799EDA469"
EXPECTED_TEMPORAL_SHARE_BELOW = 0.6866910622833815

getcontext().prec = 50


def repository_relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def require_file(path: Path) -> Path:
    if not path.is_file():
        raise PipelineError(f"Artefato obrigatório ausente: {path}")
    return path


def load_json(path: Path) -> dict[str, Any]:
    require_file(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PipelineError(f"JSON inválido: {path}") from error
    if not isinstance(payload, dict):
        raise PipelineError(f"Objeto JSON esperado: {path}")
    return payload


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest().upper()


def _schema_type_matches(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise PipelineError(f"Tipo de schema não suportado: {expected}")


def _resolve_local_ref(root_schema: Mapping[str, Any], reference: str) -> Mapping[str, Any]:
    if not reference.startswith("#/"):
        raise PipelineError(f"Referência externa de schema não suportada: {reference}")
    node: Any = root_schema
    for part in reference[2:].split("/"):
        if not isinstance(node, Mapping) or part not in node:
            raise PipelineError(f"Referência de schema inválida: {reference}")
        node = node[part]
    if not isinstance(node, Mapping):
        raise PipelineError(f"Referência de schema não aponta para objeto: {reference}")
    return node


def validate_schema(
    value: object,
    schema: Mapping[str, Any],
    *,
    root_schema: Mapping[str, Any] | None = None,
    location: str = "$",
) -> None:
    """Valida o subconjunto de JSON Schema usado pelos dois contratos."""

    root = root_schema or schema
    if "$ref" in schema:
        validate_schema(
            value,
            _resolve_local_ref(root, str(schema["$ref"])),
            root_schema=root,
            location=location,
        )
        return

    expected_type = schema.get("type")
    if expected_type is not None and not _schema_type_matches(value, str(expected_type)):
        raise PipelineError(f"{location}: tipo {expected_type} esperado")
    if "const" in schema and value != schema["const"]:
        raise PipelineError(f"{location}: valor deve ser {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise PipelineError(f"{location}: valor fora do enum")
    if isinstance(value, str):
        if len(value) < int(schema.get("minLength", 0)):
            raise PipelineError(f"{location}: texto curto demais")
        pattern = schema.get("pattern")
        if pattern is not None and re.fullmatch(str(pattern), value) is None:
            raise PipelineError(f"{location}: texto não corresponde a {pattern}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise PipelineError(f"{location}: valor abaixo do mínimo")
    if isinstance(value, list):
        if len(value) < int(schema.get("minItems", 0)):
            raise PipelineError(f"{location}: itens insuficientes")
        item_schema = schema.get("items")
        if isinstance(item_schema, Mapping):
            for index, item in enumerate(value):
                validate_schema(
                    item,
                    item_schema,
                    root_schema=root,
                    location=f"{location}[{index}]",
                )
    if isinstance(value, dict):
        required = set(schema.get("required", []))
        missing = sorted(required - set(value))
        if missing:
            raise PipelineError(f"{location}: campos ausentes: {missing}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            if extras:
                raise PipelineError(f"{location}: campos não permitidos: {extras}")
        if isinstance(properties, Mapping):
            for key, child_schema in properties.items():
                if key in value and isinstance(child_schema, Mapping):
                    validate_schema(
                        value[key],
                        child_schema,
                        root_schema=root,
                        location=f"{location}.{key}",
                    )


def validate_file_hash(path: Path, expected_sha256: str) -> str:
    require_file(path)
    observed = sha256_file(path)
    if observed != expected_sha256.upper():
        raise PipelineError(
            f"SHA-256 divergente para {path}: esperado {expected_sha256}, observado {observed}"
        )
    return observed


def build_price_manifest(proposal: Mapping[str, Any]) -> dict[str, Any]:
    reproduced = validate_proposal(proposal)
    factor = Decimal(str(reproduced["factorBaseToCurrent"]))
    with localcontext() as context:
        context.prec = 50
        multiplier = Decimal(1) / factor
    declared_multiplier = Decimal(str(proposal["multiplierCurrentToBase"]))
    if multiplier != declared_multiplier:
        raise PipelineError("Multiplicador current-to-base diverge da proposta validada")

    return {
        "schemaVersion": "1.0.0",
        "schema": repository_relative(PRICE_SCHEMA_PATH),
        "schemaSha256": sha256_file(PRICE_SCHEMA_PATH),
        "dataset": "brazil-income-price-alignment",
        "version": "2025-2026-07-v1",
        "status": "CANONICAL_APPROVED",
        "decisionId": "D065",
        "generatedAt": RELEASE_DATE,
        "generatedBy": "scripts/data/brazil/production_package.py",
        "sourceProposal": repository_relative(PROPOSAL_PATH),
        "sourceProposalSha256": sha256_file(PROPOSAL_PATH),
        "source": proposal["source"],
        "sourceUrl": proposal["sourceUrl"],
        "sidraTable": proposal["sidraTable"],
        "sidraVariable": proposal["sidraVariable"],
        "territory": proposal["territory"],
        "index": proposal["index"],
        "indexDescription": proposal["indexDescription"],
        "basePriceReference": proposal["basePriceReference"],
        "baseYear": proposal["baseYear"],
        "baseCalculation": proposal["baseCalculation"],
        "baseIndex": str(proposal["baseIndex"]),
        "inputIncomePeriod": "renda mensal nominal vigente na data do cálculo",
        "priceIndexReferenceMonth": proposal["priceIndexReferenceMonth"],
        "currentIndex": str(proposal["currentIndex"]),
        "factorBaseToCurrent": str(proposal["factorBaseToCurrent"]),
        "multiplierCurrentToBase": str(proposal["multiplierCurrentToBase"]),
        "conversion": {
            "currentToBase": "incomeComparable2025 = incomeCurrent * baseIndex / currentIndex",
            "baseToCurrent": "incomeCurrentEquivalent = income2025 * currentIndex / baseIndex",
            "lookupOrder": "converter renda domiciliar corrente; dividir por moradores elegíveis; consultar CDF 2025",
        },
        "precision": {
            "decimalDigits": 50,
            "storage": "decimal strings",
            "rounding": "nenhum arredondamento antes do lookup; arredondamento apenas na apresentação",
        },
        "accessedAt": proposal["accessedAt"],
        "cdfSha256": proposal["cdfSha256"],
        "monthlyIndex": proposal["monthlyIndex"],
        "integration": {
            "frontendIntegrationAllowed": False,
            "authorizationSource": repository_relative(ENGINE_PATH),
        },
    }


def _golden_case(golden: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    for case in golden.get("cases", []):
        if case.get("name") == name:
            return case
    raise PipelineError(f"Golden case ausente: {name}")


def build_engine_manifest(
    price_manifest: Mapping[str, Any], price_sha256: str
) -> dict[str, Any]:
    validate_file_hash(CDF_PATH, EXPECTED_CDF_SHA256)
    if CDF_PATH.stat().st_size != EXPECTED_CDF_SIZE_BYTES:
        raise PipelineError("Tamanho da CDF histórica divergiu")
    cdf, cdf_metadata = load_cdf_artifact(CDF_PATH)
    golden = load_json(GOLDEN_PATH)
    base_case = _golden_case(golden, "householdIncome6500Residents3")

    factor = Decimal(str(price_manifest["factorBaseToCurrent"]))
    nominal_household_income = Decimal("6500")
    residents = Decimal("3")
    comparable_household_income = income_current_to_base(
        nominal_household_income, factor
    )
    comparable_rdpc = comparable_household_income / residents
    position = cdf.get_brazil_income_position(comparable_rdpc)

    return {
        "schemaVersion": "1.0.0",
        "schema": repository_relative(ENGINE_SCHEMA_PATH),
        "schemaSha256": sha256_file(ENGINE_SCHEMA_PATH),
        "dataset": "brazil-income-engine",
        "version": "1.0.0",
        "status": "CANONICAL_APPROVED_FOR_INTEGRATION",
        "generatedAt": RELEASE_DATE,
        "generatedBy": "scripts/data/brazil/production_package.py",
        "decisionIds": ["D063", "D065", "D071", "D072"],
        "artifacts": {
            "cdf": {
                "path": repository_relative(CDF_PATH),
                "sha256": EXPECTED_CDF_SHA256,
                "sizeBytes": EXPECTED_CDF_SIZE_BYTES,
                "version": cdf_metadata["brazilDatasetVersion"],
                "schema": "scripts/data/brazil/cdf.py::load_cdf_artifact",
            },
            "priceAlignment": {
                "path": repository_relative(PRICE_PATH),
                "sha256": price_sha256,
                "sizeBytes": len(canonical_json(price_manifest).encode("utf-8")),
                "version": price_manifest["version"],
                "schema": repository_relative(PRICE_SCHEMA_PATH),
            },
        },
        "methodology": {
            "version": "1.0.0",
            "priceReference": "preços médios de 2025",
            "populationUnit": "pessoas elegíveis",
            "weight": "V1032",
            "formula": "soma_domiciliar(VD4019 × CO1 + VD4048 × CO1e) ÷ VD2003",
            "lookupSemantics": {
                "shareBelow": "peso com RDPC < x / peso total",
                "shareAtOrBelow": "peso com RDPC <= x / peso total",
                "topShare": "1 - shareBelow",
                "interpolation": "nenhuma; CDF empírica em degraus",
            },
        },
        "precision": {
            "calculation": "Decimal com 50 dígitos; sem arredondamento prematuro",
            "moneyDisplay": "duas casas decimais quando exibido",
            "rankingDisplay": "D071",
        },
        "displayPolicy": {
            "mainRange": "percentil inteiro e TOP inteiro complementar",
            "topBetween0_1And1": "uma casa decimal",
            "topBelow0_1": "exibir menos de 0,1%; não exibir TOP 0%",
            "aboveObservedMaximum": "não extrapolar; informar limite da distribuição observada",
            "zeroRdpc": "linguagem neutra; não usar TOP 100% como headline",
        },
        "delivery": {
            "initialBundleContainsCdf": False,
            "loadTrigger": "primeiro cálculo",
            "reuse": "memória na mesma sessão e cache HTTP normal",
            "requestData": "nenhuma renda, moradores ou resultado em URL, query, headers, analytics ou logs",
            "failSafe": "indisponibilidade e nova tentativa; sem fallback estatístico legado",
        },
        "goldenCases": {
            "source": repository_relative(GOLDEN_PATH),
            "sourceSha256": sha256_file(GOLDEN_PATH),
            "basePriceCase": {
                "name": base_case["name"],
                "householdIncome2025": str(base_case["householdIncome"]),
                "eligibleResidents": base_case["householdSize"],
                "rdpc2025": base_case["rdpcExact"],
                "shareBelow": base_case["shareBelow"],
                "shareAtOrBelow": base_case["shareAtOrBelow"],
                "topShare": base_case["topShare"],
            },
            "currentNominalCase": {
                "name": "currentHouseholdIncome6500Residents3At2026-07",
                "nominalHouseholdIncome": "6500",
                "eligibleResidents": 3,
                "nominalRdpc": str(nominal_household_income / residents),
                "comparableHouseholdIncome2025": str(comparable_household_income),
                "comparableRdpc2025": str(comparable_rdpc),
                "shareBelow": position.share_below,
                "shareAtOrBelow": position.share_at_or_below,
                "topShare": position.top_share,
                "displayPercentile": 69,
                "displayTop": 31,
            },
        },
        "integration": {
            "brazilFrontendIntegrationAllowed": True,
            "worldFrontendIntegrationAllowed": False,
            "authorization": "este manifesto resolve a promoção posterior sem reescrever a CDF histórica",
            "cdfHistoricalState": {
                "frontendIntegrationAllowed": False,
                "userIncomePriceAlignmentMethod": None,
            },
        },
    }


def build_manifests() -> tuple[dict[str, Any], dict[str, Any]]:
    proposal = load_price_alignment_proposal(PROPOSAL_PATH)
    price = build_price_manifest(proposal)
    price_schema = load_json(PRICE_SCHEMA_PATH)
    validate_schema(price, price_schema)
    price_sha = sha256_bytes(canonical_json(price).encode("utf-8"))
    engine = build_engine_manifest(price, price_sha)
    engine_schema = load_json(ENGINE_SCHEMA_PATH)
    validate_schema(engine, engine_schema)
    return price, engine


def write_manifests(
    price: Mapping[str, Any],
    engine: Mapping[str, Any],
    output_dir: Path = PRICE_PATH.parent,
) -> tuple[Path, Path]:
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="brazil-package-", dir=output_dir.parent) as temporary:
        temporary_dir = Path(temporary)
        temporary_price = temporary_dir / PRICE_PATH.name
        temporary_engine = temporary_dir / ENGINE_PATH.name
        temporary_price.write_text(canonical_json(price), encoding="utf-8", newline="\n")
        temporary_engine.write_text(canonical_json(engine), encoding="utf-8", newline="\n")
        final_price = output_dir / PRICE_PATH.name
        final_engine = output_dir / ENGINE_PATH.name
        os.replace(temporary_price, final_price)
        os.replace(temporary_engine, final_engine)
    return final_price, final_engine


def _record(
    checks: list[dict[str, Any]],
    check_id: str,
    expected: object,
    observed: object,
    passed: bool,
    evidence: str,
) -> None:
    checks.append(
        {
            "id": check_id,
            "expected": expected,
            "observed": observed,
            "status": "PASS" if passed else "FAIL",
            "evidence": evidence,
        }
    )


def _expected_failure(action: Callable[[], object]) -> str:
    try:
        action()
    except PipelineError as error:
        return str(error)
    raise PipelineError("Operação inválida foi aceita")


def validate_package(
    cdf_path: Path = CDF_PATH,
    price_path: Path = PRICE_PATH,
    engine_path: Path = ENGINE_PATH,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    for check_id, path in (
        ("artifact.cdf.exists", cdf_path),
        ("artifact.price.exists", price_path),
        ("artifact.engine.exists", engine_path),
    ):
        _record(checks, check_id, True, path.is_file(), path.is_file(), str(path))
    if not all(path.is_file() for path in (cdf_path, price_path, engine_path)):
        raise PipelineError("Pacote Brasil incompleto")

    cdf_sha = sha256_file(cdf_path)
    price_sha = sha256_file(price_path)
    engine_sha = sha256_file(engine_path)
    cdf, cdf_metadata = load_cdf_artifact(cdf_path)
    price = load_json(price_path)
    engine = load_json(engine_path)
    price_schema = load_json(PRICE_SCHEMA_PATH)
    engine_schema = load_json(ENGINE_SCHEMA_PATH)
    validate_schema(price, price_schema)
    validate_schema(engine, engine_schema)

    equality_checks: Sequence[tuple[str, object, object, str]] = (
        ("cdf.sha256", EXPECTED_CDF_SHA256, cdf_sha, repository_relative(cdf_path)),
        ("cdf.size", EXPECTED_CDF_SIZE_BYTES, cdf_path.stat().st_size, repository_relative(cdf_path)),
        ("cdf.uniqueValues", 83_358, len(cdf.rdpc), "vetor rdpc"),
        ("cdf.sourceSha256", EXPECTED_SOURCE_SHA256, cdf_metadata.get("sourceDatasetSha256"), "metadados CDF"),
        ("cdf.historicalFrontendFlag", False, cdf_metadata.get("frontendIntegrationAllowed"), "metadados CDF"),
        ("cdf.historicalPriceAlignment", None, cdf_metadata.get("userIncomePriceAlignmentMethod"), "metadados CDF"),
        ("price.schemaVersion", "1.0.0", price.get("schemaVersion"), repository_relative(PRICE_SCHEMA_PATH)),
        ("price.schemaSha256", sha256_file(PRICE_SCHEMA_PATH), price.get("schemaSha256"), repository_relative(PRICE_SCHEMA_PATH)),
        ("price.sourceProposalSha256", sha256_file(PROPOSAL_PATH), price.get("sourceProposalSha256"), repository_relative(PROPOSAL_PATH)),
        ("price.cdfSha256", cdf_sha, price.get("cdfSha256"), repository_relative(price_path)),
        ("price.index", "IPCA", price.get("index"), "D065"),
        ("price.sidraTable", 1737, price.get("sidraTable"), "D065"),
        ("price.sidraVariable", 2266, price.get("sidraVariable"), "D065"),
        ("price.referenceMonth", "2026-07", price.get("priceIndexReferenceMonth"), "manifesto congelado"),
        ("price.baseIndex", "7300.8416666666666666666666666666666666666666666667", price.get("baseIndex"), "série mensal versionada"),
        ("price.currentIndex", "7657.73", price.get("currentIndex"), "série mensal versionada"),
        ("price.status", "CANONICAL_APPROVED", price.get("status"), "D065"),
        ("engine.schemaVersion", "1.0.0", engine.get("schemaVersion"), repository_relative(ENGINE_SCHEMA_PATH)),
        ("engine.schemaSha256", sha256_file(ENGINE_SCHEMA_PATH), engine.get("schemaSha256"), repository_relative(ENGINE_SCHEMA_PATH)),
        ("engine.status", "CANONICAL_APPROVED_FOR_INTEGRATION", engine.get("status"), "contrato de produção"),
        ("engine.decisions", ["D063", "D065", "D071", "D072"], engine.get("decisionIds"), "docs/decisoes.md"),
        ("engine.cdfSha256", cdf_sha, engine["artifacts"]["cdf"].get("sha256"), repository_relative(engine_path)),
        ("engine.priceSha256", price_sha, engine["artifacts"]["priceAlignment"].get("sha256"), repository_relative(engine_path)),
        ("engine.brazilIntegration", True, engine["integration"].get("brazilFrontendIntegrationAllowed"), "manifesto de motor"),
        ("engine.worldIntegration", False, engine["integration"].get("worldFrontendIntegrationAllowed"), "D068-D070 bloqueadas"),
        ("delivery.initialBundle", False, engine["delivery"].get("initialBundleContainsCdf"), "D072"),
        ("delivery.loadTrigger", "primeiro cálculo", engine["delivery"].get("loadTrigger"), "D072"),
    )
    for check_id, expected, observed, evidence in equality_checks:
        _record(checks, check_id, expected, observed, observed == expected, evidence)

    series = normalized_series(price["monthlyIndex"])
    factor = Decimal(price["factorBaseToCurrent"])
    multiplier = Decimal(price["multiplierCurrentToBase"])
    calculated_factor = series["2026-07"] / (
        sum((series[f"2025-{month:02d}"] for month in range(1, 13)), Decimal(0))
        / Decimal(12)
    )
    _record(checks, "price.factor", str(factor), str(calculated_factor), factor == calculated_factor, "IPCA mensal versionado")
    _record(checks, "price.multiplier", str(multiplier), str(Decimal(1) / factor), multiplier == Decimal(1) / factor, "inverso do fator")
    round_trip = income_current_to_base(Decimal("6500"), factor) / multiplier
    _record(checks, "price.roundTrip", "6500", str(round_trip), round_trip == Decimal("6500"), "aritmética Decimal")

    base_case = engine["goldenCases"]["basePriceCase"]
    base_position = cdf.get_brazil_income_position(Decimal(base_case["rdpc2025"]))
    _record(checks, "golden.base.shareBelow", base_case["shareBelow"], base_position.share_below, base_position.share_below == base_case["shareBelow"], repository_relative(GOLDEN_PATH))

    current_case = engine["goldenCases"]["currentNominalCase"]
    comparable_household = income_current_to_base(Decimal("6500"), factor)
    comparable_rdpc = comparable_household / Decimal(3)
    current_position = cdf.get_brazil_income_position(comparable_rdpc)
    _record(checks, "golden.current.householdComparable", current_case["comparableHouseholdIncome2025"], str(comparable_household), str(comparable_household) == current_case["comparableHouseholdIncome2025"], "D065")
    _record(checks, "golden.current.rdpcComparable", current_case["comparableRdpc2025"], str(comparable_rdpc), str(comparable_rdpc) == current_case["comparableRdpc2025"], "D065")
    _record(checks, "golden.current.shareBelow", EXPECTED_TEMPORAL_SHARE_BELOW, current_position.share_below, current_position.share_below == EXPECTED_TEMPORAL_SHARE_BELOW, "CDF + D065")

    zero = cdf.get_brazil_income_position(Decimal(0))
    maximum = cdf.get_brazil_income_position(cdf.rdpc[-1])
    above = cdf.get_brazil_income_position(cdf.rdpc[-1] + Decimal(1))
    median_value = Decimal("1489.9901921271")
    tied = cdf.get_brazil_income_position(median_value)
    _record(checks, "lookup.tieSemantics", "shareBelow < shareAtOrBelow", {"shareBelow": tied.share_below, "shareAtOrBelow": tied.share_at_or_below}, tied.share_below < tied.share_at_or_below, "CDF empírica")
    _record(checks, "lookup.lowerTail", {"shareBelow": 0.0, "shareAtOrBelowGreaterThan": 0.0}, zero.as_dict(), zero.share_below == 0 and zero.share_at_or_below > 0, "D071")
    _record(checks, "lookup.maximum", {"shareBelowLessThan": 1.0, "shareAtOrBelow": 1.0}, maximum.as_dict(), maximum.share_below < 1 and maximum.share_at_or_below == 1, "D071")
    _record(checks, "lookup.aboveMaximum", {"shareBelow": 1.0, "shareAtOrBelow": 1.0}, above.as_dict(), above.share_below == 1 and above.share_at_or_below == 1, "D071")

    negative_error = _expected_failure(lambda: income_current_to_base(-1, factor))
    missing_error = _expected_failure(lambda: require_file(ROOT / "validation/brazil/__g0_missing__.json"))
    invalid_schema_error = _expected_failure(lambda: validate_schema({}, price_schema))
    _record(checks, "failure.negativeIncome", "rejeitar", negative_error, True, "price_alignment.py")
    _record(checks, "failure.missingArtifact", "rejeitar", missing_error, True, "production_package.py")
    _record(checks, "failure.invalidSchema", "rejeitar", invalid_schema_error, True, repository_relative(PRICE_SCHEMA_PATH))

    pass_count = sum(check["status"] == "PASS" for check in checks)
    fail_count = len(checks) - pass_count
    return {
        "schemaVersion": "1.0.0",
        "dataset": "brazil-production-package-validation",
        "version": "g0-2026-08-15-v1",
        "generatedAt": RELEASE_DATE,
        "generatedBy": "scripts/data/brazil/production_package.py",
        "historicalClaim": {
            "claim": "21/21 PASS",
            "status": "NOT_REPRODUCIBLE_AS_HISTORICAL_SUITE",
            "reason": "os 21 checks individuais e os relatórios históricos não foram encontrados; esta suíte é nova e explícita",
        },
        "artifacts": {
            "cdf": {"path": repository_relative(cdf_path), "sha256": cdf_sha},
            "priceAlignment": {"path": repository_relative(price_path), "sha256": price_sha},
            "engine": {"path": repository_relative(engine_path), "sha256": engine_sha},
        },
        "summary": {
            "total": len(checks),
            "pass": pass_count,
            "fail": fail_count,
            "status": "PASS" if fail_count == 0 else "FAIL",
        },
        "checks": checks,
    }


def report_markdown(report: Mapping[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Validação do pacote de produção Brasil — Gate G0",
        "",
        f"**Versão:** `{report['version']}`",
        f"**Gerado em:** {report['generatedAt']}",
        f"**Resultado:** **{summary['status']} — {summary['pass']}/{summary['total']} checks**",
        "",
        "A alegação histórica `21/21 PASS` não foi preservada: os 21 checks individuais e os relatórios originais não foram encontrados. Este relatório deriva de uma suíte nova, explícita e reproduzível.",
        "",
        "| Check | Esperado | Observado | Status | Evidência |",
        "|---|---|---|---|---|",
    ]
    for check in report["checks"]:
        expected = json.dumps(check["expected"], ensure_ascii=False, sort_keys=True).replace("|", "\\|")
        observed = json.dumps(check["observed"], ensure_ascii=False, sort_keys=True).replace("|", "\\|")
        evidence = str(check["evidence"]).replace("|", "\\|")
        lines.append(f"| `{check['id']}` | `{expected}` | `{observed}` | **{check['status']}** | {evidence} |")
    lines.extend(
        [
            "",
            "## Reprodução",
            "",
            "```powershell",
            "python scripts/data/brazil/production_package.py --validate-only",
            "```",
            "",
            "O validador não altera a CDF histórica e falha se hash, schema, golden cases ou referências cruzadas divergirem.",
            "",
        ]
    )
    return "\n".join(lines)


def write_reports(
    report: Mapping[str, Any],
    json_path: Path = REPORT_JSON_PATH,
    markdown_path: Path = REPORT_MD_PATH,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(canonical_json(report), encoding="utf-8", newline="\n")
    markdown_path.write_text(report_markdown(report), encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="não regenera manifestos; apenas valida e atualiza os relatórios",
    )
    args = parser.parse_args()

    cdf_before = validate_file_hash(CDF_PATH, EXPECTED_CDF_SHA256)
    if not args.validate_only:
        price, engine = build_manifests()
        write_manifests(price, engine)
    report = validate_package()
    write_reports(report)
    cdf_after = validate_file_hash(CDF_PATH, EXPECTED_CDF_SHA256)
    if cdf_before != cdf_after:
        raise PipelineError("A CDF histórica mudou durante a execução")
    print(
        canonical_json(
            {
                "status": report["summary"]["status"],
                "checks": report["summary"],
                "cdfSha256Before": cdf_before,
                "cdfSha256After": cdf_after,
                "priceAlignmentSha256": report["artifacts"]["priceAlignment"]["sha256"],
                "engineManifestSha256": report["artifacts"]["engine"]["sha256"],
            }
        ),
        end="",
    )
    return 0 if report["summary"]["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
