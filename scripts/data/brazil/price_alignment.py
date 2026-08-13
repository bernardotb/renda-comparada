"""Validação experimental do alinhamento monetário da renda brasileira.

Este módulo não integra o frontend e não canoniza a decisão metodológica.
Ele preserva aritmética decimal para tornar a proposta da Fase 1F auditável.
"""

from __future__ import annotations

import json
import re
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
from typing import Any, Mapping, Sequence

from pipeline import ROOT, PipelineError


DEFAULT_PROPOSAL_PATH = (
    ROOT / "validation/brazil/brazil-price-alignment-proposal.json"
)
MONTH_PATTERN = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])$")
DECIMAL_PRECISION = 50


def decimal_value(value: object, label: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise PipelineError(f"{label} não é numérico") from error
    if not result.is_finite():
        raise PipelineError(f"{label} não é finito")
    return result


def load_price_alignment_proposal(
    path: Path = DEFAULT_PROPOSAL_PATH,
) -> dict[str, Any]:
    try:
        proposal = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PipelineError(f"Não foi possível ler a proposta: {path}") from error

    required = {
        "status",
        "index",
        "territory",
        "baseYear",
        "baseIndex",
        "priceIndexReferenceMonth",
        "priceIndexLatestAvailableMonth",
        "latestOfficialMonth",
        "currentIndex",
        "factorBaseToCurrent",
        "monthlyIndex",
        "cdfSha256",
        "accessedAt",
    }
    missing = sorted(required - set(proposal))
    if missing:
        raise PipelineError(f"Proposta de alinhamento incompleta: {missing}")
    return proposal


def normalized_series(
    monthly_index: Sequence[Mapping[str, object]],
) -> dict[str, Decimal]:
    if not monthly_index:
        raise PipelineError("Série de preços ausente")

    series: dict[str, Decimal] = {}
    for point in monthly_index:
        month = str(point.get("month", ""))
        if not MONTH_PATTERN.fullmatch(month):
            raise PipelineError(f"Mês inválido na série: {month!r}")
        if month in series:
            raise PipelineError(f"Mês duplicado na série: {month}")
        value = decimal_value(point.get("value"), f"índice de {month}")
        if value <= 0:
            raise PipelineError(f"Índice de {month} deve ser positivo")
        series[month] = value
    return dict(sorted(series.items()))


def annual_average_index(series: Mapping[str, Decimal], year: int) -> Decimal:
    expected = [f"{year}-{month:02d}" for month in range(1, 13)]
    missing = [month for month in expected if month not in series]
    if missing:
        raise PipelineError(
            f"Série incompleta para a média de {year}: {', '.join(missing)}"
        )
    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        return sum((series[month] for month in expected), Decimal(0)) / Decimal(12)


def index_for_official_month(
    series: Mapping[str, Decimal], month: str
) -> Decimal:
    if not MONTH_PATTERN.fullmatch(month):
        raise PipelineError(f"Mês de referência inválido: {month!r}")
    if month not in series:
        raise PipelineError(
            f"IPCA oficial indisponível para {month}; projeção é proibida"
        )
    return series[month]


def factor_base_to_month(
    series: Mapping[str, Decimal], base_year: int, month: str
) -> Decimal:
    base_index = annual_average_index(series, base_year)
    current_index = index_for_official_month(series, month)
    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        factor = current_index / base_index
    if factor <= 0 or not factor.is_finite():
        raise PipelineError("Fator temporal inválido")
    return factor


def income_current_to_base(
    income_current: object, factor_base_to_current: Decimal
) -> Decimal:
    income = decimal_value(income_current, "renda corrente")
    if income < 0:
        raise PipelineError("Renda corrente não pode ser negativa")
    if factor_base_to_current <= 0 or not factor_base_to_current.is_finite():
        raise PipelineError("Fator temporal deve ser positivo e finito")
    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        return income / factor_base_to_current


def income_base_to_current(
    income_base: object, factor_base_to_current: Decimal
) -> Decimal:
    income = decimal_value(income_base, "renda na base")
    if income < 0:
        raise PipelineError("Renda na base não pode ser negativa")
    if factor_base_to_current <= 0 or not factor_base_to_current.is_finite():
        raise PipelineError("Fator temporal deve ser positivo e finito")
    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        return income * factor_base_to_current


def validate_proposal(proposal: Mapping[str, Any]) -> dict[str, Decimal | str]:
    if proposal["status"] != "PROPOSTA_PENDENTE_DE_CANONIZACAO":
        raise PipelineError("A Fase 1F não pode marcar a proposta como canônica")
    if proposal["index"] != "IPCA" or proposal["territory"] != "Brasil":
        raise PipelineError("A proposta experimental deve usar IPCA nacional")

    series = normalized_series(proposal["monthlyIndex"])
    base_year = int(proposal["baseYear"])
    base_index = annual_average_index(series, base_year)
    latest_month = max(series)
    if latest_month != proposal["latestOfficialMonth"]:
        raise PipelineError("latestOfficialMonth diverge da série versionada")
    if latest_month != proposal["priceIndexLatestAvailableMonth"]:
        raise PipelineError(
            "priceIndexLatestAvailableMonth diverge da série versionada"
        )
    if proposal["priceIndexReferenceMonth"] != latest_month:
        raise PipelineError("A proposta deve explicitar o mês efetivamente usado")
    try:
        accessed_month = date.fromisoformat(str(proposal["accessedAt"])).strftime(
            "%Y-%m"
        )
    except ValueError as error:
        raise PipelineError("accessedAt não é uma data ISO válida") from error
    if latest_month > accessed_month:
        raise PipelineError("Série contém mês posterior à data de acesso")

    current_index = index_for_official_month(series, latest_month)
    factor = factor_base_to_month(series, base_year, latest_month)
    expected = {
        "baseIndex": base_index,
        "currentIndex": current_index,
        "factorBaseToCurrent": factor,
    }
    for key, actual in expected.items():
        declared = decimal_value(proposal[key], key)
        if declared != actual:
            raise PipelineError(f"{key} declarado diverge do cálculo reproduzido")

    return {
        "baseIndex": base_index,
        "latestOfficialMonth": latest_month,
        "currentIndex": current_index,
        "factorBaseToCurrent": factor,
    }
