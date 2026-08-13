"""Reproduz os diagnósticos da proposta temporal da Fase 1F."""

from __future__ import annotations

import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PIPELINE_DIR = ROOT / "scripts/data/brazil"
sys.path.insert(0, str(PIPELINE_DIR))

from cdf import load_cdf_artifact, sha256_file  # noqa: E402
from pipeline import PipelineError  # noqa: E402
from price_alignment import (  # noqa: E402
    income_current_to_base,
    load_price_alignment_proposal,
    validate_proposal,
)


getcontext().prec = 50


def main() -> None:
    proposal = load_price_alignment_proposal()
    diagnostics = validate_proposal(proposal)

    cdf_path = ROOT / "data/production/brazil/brazil-income-cdf-2025.json"
    actual_cdf_sha = sha256_file(cdf_path)
    if actual_cdf_sha != proposal["cdfSha256"]:
        raise PipelineError("Checksum da CDF canônica diverge da Fase 1E")
    cdf, _ = load_cdf_artifact(cdf_path)

    current_household_income = Decimal("6500")
    household_size = Decimal("3")
    factor = diagnostics["factorBaseToCurrent"]
    if not isinstance(factor, Decimal):
        raise PipelineError("Fator temporal não foi reproduzido como Decimal")
    comparable_income = income_current_to_base(current_household_income, factor)
    comparable_rdpc = comparable_income / household_size
    position = cdf.get_brazil_income_position(comparable_rdpc)

    result = {
        "status": "PASS",
        "proposalStatus": proposal["status"],
        "baseIndex": str(diagnostics["baseIndex"]),
        "latestOfficialMonth": diagnostics["latestOfficialMonth"],
        "currentIndex": str(diagnostics["currentIndex"]),
        "factorBaseToCurrent": str(factor),
        "example": {
            "householdIncomeCurrent": str(current_household_income),
            "householdSize": str(household_size),
            "comparableIncome2025": str(comparable_income),
            "comparableRdpc2025": str(comparable_rdpc),
            **position.as_dict(),
        },
        "cdfSha256": actual_cdf_sha,
        "frontendIntegrationAllowed": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
