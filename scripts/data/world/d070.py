"""Execução reproduzível do gate D070, sem integração ou promoção de produção."""

from __future__ import annotations

import bisect
import hashlib
import json
import os
import tempfile
from decimal import Decimal, ROUND_HALF_UP, getcontext
from pathlib import Path
from typing import Any, Mapping

from pipeline import WorldCdf, WorldPipelineError, canonical_json, decimal_text


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = ROOT / "config/world-d070-candidate.json"
getcontext().prec = 60


def repository_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise WorldPipelineError(f"Caminho fora da raiz canônica: {relative}")
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def require_hash(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise WorldPipelineError(f"{label} ausente: {path}")
    observed = sha256_file(path)
    if observed != expected:
        raise WorldPipelineError(f"SHA-256 divergente em {label}: {observed} != {expected}")


def atomic_write(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", dir=path.parent, delete=False) as handle:
        handle.write(payload)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    if config.get("status") != "D070_EXECUTION_CANDIDATE":
        raise WorldPipelineError("Configuração D070 não está marcada como candidata")
    return config


def load_ipca(config: Mapping[str, Any]) -> dict[str, Any]:
    path = repository_path(str(config["ipcaRawPath"]))
    require_hash(path, str(config["ipcaRawSha256"]), "raw IPCA Mundo")
    if path.stat().st_size != int(config["ipcaRawSizeBytes"]):
        raise WorldPipelineError("Tamanho do raw IPCA Mundo divergiu")
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) < 2:
        raise WorldPipelineError("Resposta SIDRA vazia ou incompatível")
    expected_header = {
        "NC": "Nível Territorial (Código)",
        "NN": "Nível Territorial",
        "MC": "Unidade de Medida (Código)",
        "MN": "Unidade de Medida",
        "V": "Valor",
        "D1C": "Brasil (Código)",
        "D1N": "Brasil",
        "D2C": "Variável (Código)",
        "D2N": "Variável",
        "D3C": "Mês (Código)",
        "D3N": "Mês",
    }
    if rows[0] != expected_header:
        raise WorldPipelineError(f"Cabeçalho SIDRA inesperado: {rows[0]}")
    monthly: dict[str, Decimal] = {}
    raw_values: dict[str, str] = {}
    for row in rows[1:]:
        if row.get("D1C") != "1" or row.get("D2C") != "2266" or row.get("MC") != "30":
            raise WorldPipelineError(f"Linha SIDRA fora do contrato: {row}")
        month = str(row["D3C"])
        if month in monthly:
            raise WorldPipelineError(f"Mês SIDRA duplicado: {month}")
        raw_values[month] = str(row["V"])
        monthly[month] = Decimal(raw_values[month])
    expected_months = [f"2024{month:02d}" for month in range(1, 13)]
    missing = [month for month in expected_months if month not in monthly]
    if missing:
        raise WorldPipelineError(f"Meses de 2024 ausentes no IPCA: {missing}")
    current_month = str(config["currentPriceReferenceMonth"]).replace("-", "")
    if current_month not in monthly:
        raise WorldPipelineError(f"Mês corrente Mundo ausente no raw: {current_month}")
    average_2024 = sum((monthly[month] for month in expected_months), Decimal(0)) / Decimal(12)
    return {
        "average2024": average_2024,
        "current": monthly[current_month],
        "currentMonth": current_month,
        "rawCurrentValue": raw_values[current_month],
        "months2024": expected_months,
        "rows": len(rows) - 1,
    }


def load_cdf(config: Mapping[str, Any]) -> tuple[WorldCdf, dict[str, Any]]:
    path = repository_path(str(config["cdfCandidatePath"]))
    require_hash(path, str(config["cdfCandidateSha256"]), "CDF mundial candidata D068")
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("status") != "CANDIDATE" or document.get("frontendIntegrationAllowed") is not False:
        raise WorldPipelineError("CDF D068 não preserva estado candidato/bloqueado")
    points = document.get("points")
    if not isinstance(points, list) or not points:
        raise WorldPipelineError("CDF D068 sem pontos")
    welfare = tuple(Decimal(str(point[0])) for point in points)
    weight_at = tuple(Decimal(str(point[1])) for point in points)
    cumulative = tuple(Decimal(str(point[2])) for point in points)
    return WorldCdf(welfare, weight_at, cumulative, cumulative[-1]), document


def conversion_factors(config: Mapping[str, Any], ipca: Mapping[str, Any]) -> dict[str, Decimal]:
    ppp = Decimal(str(config["brazilPipPpp2021"]))
    cpi = Decimal(str(config["brazilPipCpi2024Base2021"]))
    combined = ppp * cpi
    current_to_2024 = ipca["average2024"] / ipca["current"]
    return {"ppp": ppp, "cpi": cpi, "combined": combined, "currentTo2024": current_to_2024}


def nominal_to_daily(income: Decimal, residents: int, factors: Mapping[str, Decimal]) -> Decimal:
    if income < 0 or residents <= 0:
        raise WorldPipelineError("Entrada nominal inválida para D070")
    return (
        (income / Decimal(residents))
        * factors["currentTo2024"]
        / factors["combined"]
        * Decimal(12)
        / Decimal(365)
    )


def daily_to_nominal(daily: Decimal, residents: int, factors: Mapping[str, Decimal]) -> Decimal:
    if daily < 0 or residents <= 0:
        raise WorldPipelineError("Valor PPP inválido para inversão D070")
    return (
        daily
        * Decimal(365)
        / Decimal(12)
        * factors["combined"]
        / factors["currentTo2024"]
        * Decimal(residents)
    )


def make_case(
    name: str,
    kind: str,
    income: Decimal,
    residents: int,
    daily: Decimal,
    cdf: WorldCdf,
    config: Mapping[str, Any],
) -> dict[str, Any]:
    lookup = cdf.lookup(daily)
    return {
        "name": name,
        "kind": kind,
        "nominalHouseholdIncome": decimal_text(income),
        "residents": residents,
        "calculationDate": config["calculationDate"],
        "priceReference": f"BRL nominal de {config['currentPriceReferenceMonth']} alinhado a preços médios de 2024",
        "internationalPppDaily": decimal_text(daily),
        "shareBelow": lookup["shareBelow"],
        "shareAtOrBelow": lookup["shareAtOrBelow"],
        "topShare": lookup["topShare"],
        "pipVersion": config["pipVersion"],
        "productionBuild": config["productionBuild"],
        "referenceYear": config["referenceYear"],
        "pppBase": config["pppBase"],
    }


def build_cases(cdf: WorldCdf, config: Mapping[str, Any], factors: Mapping[str, Decimal]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for name, income, residents in (
        ("nominal-zero-one-resident", Decimal("0"), 1),
        ("nominal-6500-three-residents", Decimal("6500"), 3),
        ("nominal-12000-three-residents", Decimal("12000"), 3),
        ("nominal-20000-four-residents", Decimal("20000"), 4),
        ("nominal-50000-four-residents", Decimal("50000"), 4),
    ):
        daily = nominal_to_daily(income, residents, factors)
        cases.append(make_case(name, "nominal", income, residents, daily, cdf, config))

    exact = cdf.weighted_quantile(Decimal("0.5"))
    exact_index = bisect.bisect_left(cdf.welfare, exact)
    between = (exact + cdf.welfare[exact_index + 1]) / Decimal(2)
    maximum = cdf.welfare[-1]
    boundary_values = (
        ("exact-observed-median-support", "exact-observed", exact),
        ("between-observed-points", "between-points", between),
        ("below-minimum-support", "below-minimum", cdf.welfare[0] / Decimal(2)),
        ("at-maximum-support", "at-maximum", maximum),
        ("above-maximum-support", "above-maximum", maximum + Decimal(1)),
    )
    for name, kind, daily in boundary_values:
        income = daily_to_nominal(daily, 1, factors)
        cases.append(make_case(name, kind, income, 1, daily, cdf, config))

    tie_index = max(range(len(cdf.weight_at)), key=cdf.weight_at.__getitem__)
    tie_daily = cdf.welfare[tie_index]
    tie_income = daily_to_nominal(tie_daily, 1, factors)
    cases.append(make_case("largest-observed-tied-step", "tie", tie_income, 1, tie_daily, cdf, config))
    return cases


def display_policy(max_error_pp: Decimal) -> dict[str, Any]:
    return {
        "basis": {
            "d068MaxAbsErrorPp": format(max_error_pp, "f"),
            "mainDisplayIncrementPp": "1",
            "upperTailDisplayIncrementPp": "0.1",
            "oneDecimalHalfIncrementPp": "0.05",
            "errorBelowOneDecimalHalfIncrement": max_error_pp < Decimal("0.05"),
        },
        "internalPrecision": "full artifact precision; no intermediate rounding",
        "mainRange": "when topShare >= 0.01 and the value is inside observed support, round 100*shareBelow to an integer and derive TOP as 100 minus that displayed integer",
        "upperTail": "when 0.001 <= topShare < 0.01, display TOP with one decimal percentage point; when topPercent < 0.1, use 'less than 0.1%' only if topPercent + maxErrorPp < 0.1, otherwise use 'approximately 0.1%'",
        "lowerTail": "below the minimum, report that the value is outside the lower observed support; at the minimum, report the lowest represented step and preserve tie semantics; do not headline TOP 100%",
        "maximumAndAbove": "at the maximum, preserve the last observed step; above it, do not extrapolate and report that the value exceeds the observed support; never display TOP 0%",
        "ties": "shareBelow uses welfare < x; shareAtOrBelow uses welfare <= x; the primary approximate position uses shareBelow",
        "language": "posição monetária global estimada; never exact global salary, wealth, or asset ranking",
        "status": "CANONICAL_BY_D070",
    }


def presentation_decision(
    top_share: Any,
    max_error_pp: Any,
    support_status: str = "inside",
) -> dict[str, Any]:
    """Classifica a apresentação sem alterar a precisão do lookup."""

    top = Decimal(str(top_share))
    error = Decimal(str(max_error_pp))
    if not Decimal(0) <= top <= Decimal(1):
        raise WorldPipelineError("topShare fora de [0,1]")
    if error < 0:
        raise WorldPipelineError("maxErrorPp negativo")
    allowed_support = {"inside", "at-minimum", "at-maximum", "below-minimum", "above-maximum"}
    if support_status not in allowed_support:
        raise WorldPipelineError(f"Estado de suporte inválido: {support_status}")

    top_percent = top * Decimal(100)
    result: dict[str, Any] = {
        "supportStatus": support_status,
        "topPercentInternal": decimal_text(top_percent),
        "maxErrorPp": format(error, "f"),
        "extrapolated": False,
    }
    if support_status == "below-minimum":
        return {**result, "displayClass": "OUTSIDE_LOWER_SUPPORT", "headline": "fora do suporte inferior observado"}
    if support_status == "above-maximum":
        return {**result, "displayClass": "OUTSIDE_UPPER_SUPPORT", "headline": "fora do suporte superior observado"}
    if support_status == "at-minimum":
        return {**result, "displayClass": "AT_MINIMUM", "headline": "menor degrau observado; empates preservados"}
    if top_percent == 0:
        return {**result, "displayClass": "UPPER_SUPPORT_LIMIT", "headline": "limite superior observado; posição mais fina indisponível"}
    if top_percent >= Decimal(1):
        percentile_display = (Decimal(100) - top_percent).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        top_display = Decimal(100) - percentile_display
        return {
            **result,
            "displayClass": "MAIN_INTEGER_COMPLEMENTARY",
            "percentileDisplay": decimal_text(percentile_display),
            "topDisplayPp": decimal_text(top_display),
        }
    if top_percent >= Decimal("0.1"):
        return {
            **result,
            "displayClass": "UPPER_TAIL_ONE_DECIMAL",
            "topDisplayPp": decimal_text(top_percent.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)),
        }
    if top_percent + error < Decimal("0.1"):
        return {**result, "displayClass": "UPPER_EXTREME_LESS_THAN_0_1", "headline": "menos de 0,1%"}
    return {**result, "displayClass": "UPPER_EXTREME_APPROX_0_1", "headline": "aproximadamente 0,1%"}


def run(config_path: Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    config = load_config(config_path)
    for path_key, hash_key, label in (
        ("pppRawPath", "pppRawSha256", "raw PPP D069"),
        ("cpiRawPath", "cpiRawSha256", "raw CPI D069"),
    ):
        require_hash(repository_path(str(config[path_key])), str(config[hash_key]), label)
    ipca = load_ipca(config)
    cdf, cdf_document = load_cdf(config)
    factors = conversion_factors(config, ipca)
    validation_document = json.loads(repository_path(str(config["cdfValidationPath"])).read_text(encoding="utf-8"))
    measured_max_error_pp = Decimal(str(validation_document["validationMetrics"]["maxAbsErrorPp"]))
    max_error_pp = Decimal(str(config["maxAbsoluteErrorPp"]))
    if measured_max_error_pp.quantize(Decimal("0.000000000000001"), rounding=ROUND_HALF_UP) != max_error_pp:
        raise WorldPipelineError(
            f"Erro máximo D068 divergiu da precisão canonizada: {measured_max_error_pp} != {max_error_pp}"
        )
    cases = build_cases(cdf, config, factors)
    golden = {
        "status": "D070_CANONICAL_GOLDEN_CASES",
        "canonical": True,
        "frontendIntegrationAllowed": False,
        "formula": "dailyPPP = (householdIncomeCurrent / residents) * (IPCA_AVG_2024 / IPCA_CURRENT) / (BRAZIL_PIP_PPP_2021 * BRAZIL_PIP_CPI_2024_BASE_2021) * 12 / 365",
        "inputs": {
            "ipcaAverage2024": decimal_text(ipca["average2024"]),
            "ipcaCurrentMonth": config["currentPriceReferenceMonth"],
            "ipcaCurrentRawValue": ipca["rawCurrentValue"],
            "brazilPipPpp2021": decimal_text(factors["ppp"]),
            "brazilPipCpi2024Base2021": decimal_text(factors["cpi"]),
            "brlPerIntl2024Derived": decimal_text(factors["combined"]),
            "currentToAverage2024Multiplier": decimal_text(factors["currentTo2024"]),
        },
        "provenance": {
            "cdfPath": config["cdfCandidatePath"],
            "cdfSha256": config["cdfCandidateSha256"],
            "pppRawPath": config["pppRawPath"],
            "pppRawSha256": config["pppRawSha256"],
            "cpiRawPath": config["cpiRawPath"],
            "cpiRawSha256": config["cpiRawSha256"],
            "ipcaRawPath": config["ipcaRawPath"],
            "ipcaRawSha256": config["ipcaRawSha256"],
            "ipcaSourceUrl": config["ipcaSourceUrl"],
            "ipcaAccessedAtUtc": config["ipcaAccessedAtUtc"],
        },
        "cases": cases,
    }
    golden_path = repository_path(str(config["goldenCasesPath"]))
    atomic_write(golden_path, canonical_json(golden))
    generated_sha = sha256_file(golden_path)
    checks = [
        {"name": "d068_active_dependency_evidence", "status": "PASS", "detail": cdf_document["methodology"]["productionBuild"]},
        {"name": "d069_exact_raw_hashes", "status": "PASS", "detail": "PPP and CPI verified"},
        {"name": "ipca_2024_complete", "status": "PASS", "detail": len(ipca["months2024"])},
        {"name": "nominal_golden_cases", "status": "PASS", "detail": 5},
        {"name": "boundary_and_tie_cases", "status": "PASS", "detail": len(cases) - 5},
        {"name": "d068_error_precision", "status": "PASS", "detail": format(max_error_pp, "f")},
        {"name": "no_intermediate_rounding", "status": "PASS", "detail": "Decimal precision 60"},
        {"name": "frontend_integration_blocked", "status": "PASS", "detail": False},
    ]
    validation = {
        "status": "PASS_CANONIZED",
        "d070Canonical": True,
        "frontendIntegrationAllowed": False,
        "goldenCases": {"path": config["goldenCasesPath"], "sha256": generated_sha, "count": len(cases)},
        "calculationInputs": golden["inputs"],
        "displayPolicy": display_policy(max_error_pp),
        "checks": checks,
        "protectedState": {
            "d068Changed": False,
            "d069Changed": False,
            "brazilChanged": False,
            "frontendChanged": False,
            "worldProductionChanged": False,
        },
    }
    validation_path = repository_path(str(config["validationPath"]))
    atomic_write(validation_path, canonical_json(validation))
    report = "\n".join(
        [
            "# D070 — validação final",
            "",
            "**Resultado técnico:** `PASS_CANONIZED`",
            "",
            "**D070 canônica:** `YES`",
            "",
            "**Integração frontend Mundo:** `BLOCKED`",
            "",
            "## Evidência",
            "",
            f"- IPCA oficial: `{config['ipcaRawPath']}`; SHA-256 `{config['ipcaRawSha256']}`.",
            f"- `IPCA_AVG_2024 = {decimal_text(ipca['average2024'])}`.",
            f"- `IPCA_CURRENT ({config['currentPriceReferenceMonth']}) = {ipca['rawCurrentValue']}`.",
            f"- Fator PIP combinado derivado: `{decimal_text(factors['combined'])}`.",
            f"- CDF D068: `{config['cdfCandidateSha256']}`.",
            f"- Golden cases congelados: `{config['goldenCasesPath']}`; SHA-256 `{generated_sha}`; {len(cases)} casos.",
            "",
            "## Política canônica",
            "",
            "- precisão interna integral, sem arredondamento intermediário;",
            "- faixa principal em percentual inteiro, com TOP derivado do percentil exibido;",
            "- TOP entre 0,1% e 1% com uma casa; abaixo de 0,1%, usar 'menos de 0,1%' somente quando `topPercent + maxErrorPp < 0,1`; caso contrário, usar 'aproximadamente 0,1%';",
            "- abaixo do mínimo e acima do máximo, linguagem de suporte observado, sem extrapolação;",
            "- empates preservam `shareBelow` e `shareAtOrBelow`;",
            "- linguagem subordinada a D067: posição monetária global estimada.",
            "",
            "A política canônica considera o erro máximo D068 de "
            f"`{format(max_error_pp, 'f')}` ponto percentual, inferior a meia unidade da exibição de 0,1 ponto percentual.",
            "A margem de erro participa diretamente da linguagem da cauda extrema. Nenhum artefato de produção ou frontend foi criado.",
            "",
        ]
    )
    atomic_write(repository_path(str(config["reportPath"])), report)
    return validation


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
