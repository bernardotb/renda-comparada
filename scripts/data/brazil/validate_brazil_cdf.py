"""Validação integral, dois runs e golden cases da CDF brasileira."""

from __future__ import annotations

import json
import bisect
import shutil
import subprocess
import sys
import time
from decimal import Decimal
from typing import Any, Mapping

from cdf import (
    DEFAULT_CDF_CONFIG_PATH,
    IncomeCdf,
    build_cdf,
    load_cdf_artifact,
    load_cdf_config,
    repository_path,
)
from pipeline import ROOT, PipelineError, canonical_json, sha256_file


PROCESSED_ROOT = ROOT / "data/processed"
RUN_ROOT = PROCESSED_ROOT / "brazil/cdf-validation-runs"
PRODUCTION_ROOT = ROOT / "data/production/brazil"
VALIDATION_ROOT = ROOT / "validation/brazil"


def reset_processed(path: Path) -> None:
    resolved = path.resolve()
    base = PROCESSED_ROOT.resolve()
    if not resolved.is_relative_to(base) or resolved == base:
        raise PipelineError(f"Recusa de limpar caminho fora de data/processed: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def run_tests() -> dict[str, Any]:
    command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests/data/brazil",
        "-p",
        "test_*.py",
        "-v",
    ]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    transcript = (completed.stdout + completed.stderr).strip()
    if completed.returncode != 0:
        raise PipelineError(f"Testes automatizados falharam:\n{transcript}")
    return {
        "status": "PASS",
        "command": ["python", *command[1:]],
        "transcript": transcript,
    }


def golden_case(
    name: str,
    rdpc: Decimal,
    cdf: IncomeCdf,
    config: Mapping[str, Any],
    cdf_sha: str,
    **extra: Any,
) -> dict[str, Any]:
    position = cdf.get_brazil_income_position(rdpc)
    return {
        "name": name,
        **extra,
        "rdpc": float(rdpc),
        "rdpcExact": format(rdpc, "f"),
        **position.as_dict(),
        "methodologyVersion": config["methodologyVersion"],
        "brazilDatasetVersion": config["brazilDatasetVersion"],
        "datasetSha256": config["sourceDatasetSha256"],
        "cdfSha256": cdf_sha,
    }


def quantile_convention_diagnostics(
    cdf: IncomeCdf, config: Mapping[str, Any]
) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {}
    midpoint_ranks = [
        (cumulative - weight / Decimal(2)) / cdf.total_weight
        for cumulative, weight in zip(cdf.cumulative_at_or_below, cdf.weight_at)
    ]
    for label in ("P90", "P99"):
        probability = Decimal(label[1:]) / Decimal(100)
        target = probability * cdf.total_weight
        index = bisect.bisect_left(cdf.cumulative_at_or_below, target)
        current = cdf.rdpc[index]
        previous = cdf.rdpc[index - 1]
        previous_midpoint = midpoint_ranks[index - 1]
        current_midpoint = midpoint_ranks[index]
        fraction = (probability - previous_midpoint) / (
            current_midpoint - previous_midpoint
        )
        centered_interpolation = previous + fraction * (current - previous)
        midrank_index = bisect.bisect_right(midpoint_ranks, probability) - 1
        midrank_upper = cdf.rdpc[midrank_index]
        published = int(config["sidraPublishedQuantiles"][label])
        diagnostics[label] = {
            "published": published,
            "empiricalInverse": float(current),
            "empiricalInverseRounded": round(float(current)),
            "previousObserved": float(previous),
            "previousObservedRounded": round(float(previous)),
            "centeredWeightInterpolation": float(centered_interpolation),
            "centeredWeightInterpolationRounded": round(float(centered_interpolation)),
            "midrankClassUpper": float(midrank_upper),
            "midrankClassUpperRounded": round(float(midrank_upper)),
        }
    return diagnostics


def build_golden_cases(
    cdf: IncomeCdf, config: Mapping[str, Any], cdf_sha: str
) -> dict[str, Any]:
    mean = Decimal(str(config["expected"]["mean"]))
    maximum = cdf.rdpc[-1]
    cases = [
        golden_case("zero", Decimal(0), cdf, config, cdf_sha, category="statistical"),
        golden_case("P10", cdf.weighted_quantile(Decimal("0.10")), cdf, config, cdf_sha, category="statistical"),
        golden_case("P25", cdf.weighted_quantile(Decimal("0.25")), cdf, config, cdf_sha, category="statistical"),
        golden_case("median", cdf.weighted_quantile(Decimal("0.50")), cdf, config, cdf_sha, category="statistical"),
        golden_case("mean", mean, cdf, config, cdf_sha, category="statistical"),
        golden_case("P75", cdf.weighted_quantile(Decimal("0.75")), cdf, config, cdf_sha, category="statistical"),
        golden_case("P90", cdf.weighted_quantile(Decimal("0.90")), cdf, config, cdf_sha, category="statistical"),
        golden_case("P95", cdf.weighted_quantile(Decimal("0.95")), cdf, config, cdf_sha, category="statistical"),
        golden_case("P99", cdf.weighted_quantile(Decimal("0.99")), cdf, config, cdf_sha, category="statistical"),
        golden_case("P99.9", cdf.weighted_quantile(Decimal("0.999")), cdf, config, cdf_sha, category="statistical"),
        golden_case("maximum", maximum, cdf, config, cdf_sha, category="statistical"),
        golden_case("aboveMaximum", maximum + Decimal(1), cdf, config, cdf_sha, category="statistical"),
        golden_case(
            "householdIncome6500Residents3",
            Decimal(6500) / Decimal(3),
            cdf,
            config,
            cdf_sha,
            category="mathematical-and-statistical",
            householdIncome=6500,
            householdSize=3,
        ),
    ]
    return {
        "dataset": "brazil-income-golden-cases",
        "methodologyVersion": config["methodologyVersion"],
        "brazilDatasetVersion": config["brazilDatasetVersion"],
        "datasetSha256": config["sourceDatasetSha256"],
        "cdfSha256": cdf_sha,
        "priceReference": config["priceReference"],
        "userIncomePriceAlignmentMethod": None,
        "frontendIntegrationBlocked": True,
        "cases": cases,
    }


def benchmark_lookup(cdf: IncomeCdf, queries: int = 100000) -> dict[str, Any]:
    minimum = float(cdf.rdpc[0])
    maximum = float(cdf.rdpc[-1])
    values = [minimum + (maximum - minimum) * index / (queries - 1) for index in range(queries)]
    started = time.perf_counter()
    checksum = 0.0
    for value in values:
        checksum += cdf.get_brazil_income_position(value).share_below
    elapsed = time.perf_counter() - started
    return {
        "queries": queries,
        "elapsedMilliseconds": elapsed * 1000,
        "microsecondsPerLookup": elapsed * 1_000_000 / queries,
        "resultChecksum": checksum,
        "algorithm": "binary search (bisect) over sorted unique RDPC values",
    }


def markdown_report(report: Mapping[str, Any]) -> str:
    metrics = report["distribution"]
    quantiles = report["quantiles"]
    cases = {case["name"]: case for case in report["goldenCases"]["cases"]}
    ordered_quantiles = ["P5", "P10", "P20", "P25", "P30", "P40", "P50", "P60", "P70", "P75", "P80", "P90", "P95", "P99", "P99.5", "P99.9"]
    quantile_rows = "\n".join(
        f"| {label} | {quantiles[label]:.10f} |"
        for label in ordered_quantiles
    )
    selected = ["zero", "median", "mean", "P90", "P99", "householdIncome6500Residents3", "maximum", "aboveMaximum"]
    convention = report["p90P99Investigation"]["testedConventions"]
    case_rows = "\n".join(
        f"| {name} | {cases[name]['rdpc']:.10f} | {cases[name]['shareBelow']:.15f} | {cases[name]['shareAtOrBelow']:.15f} | {cases[name]['topShare']:.15f} |"
        for name in selected
    )
    return f"""# Validação final da CDF brasileira — PNAD Contínua 2025

**Resultado:** `{report['status']}`

**Versão da distribuição:** `{report['brazilDatasetVersion']}`

**Metodologia:** `{report['methodologyVersion']}`

## Fonte e referência

- Dataset intermediário: `data/processed/brazil/pnad-2025/brazil-income-distribution-2025.csv`
- SHA-256 fonte: `{report['sourceDatasetSha256']}`
- Referência monetária: **preços médios de 2025**.
- Unidade: pessoas elegíveis ponderadas por `V1032`.
- Integração ao frontend: **bloqueada** até definição do alinhamento temporal da renda digitada.

## Artefato

- Formato: JSON UTF-8 determinístico, representação agregada por RDPC único.
- Caminho: `data/production/brazil/brazil-income-cdf-2025.json`.
- SHA-256: `{report['cdf']['sha256']}`
- Tamanho: {report['cdf']['sizeBytes']} bytes.
- Linhas fonte: {report['cdf']['sourceRecords']}.
- Valores únicos: {report['cdf']['uniqueIncomeValues']}.
- Redução de registros: {report['cdf']['recordReductionPercent']:.6f}%.
- Redução de bytes: {report['cdf']['byteReductionPercent']:.6f}%.

O artefato guarda `rdpc`, `weightAt` e `cumAtOrBelow`. Para um ponto observado, `cumBelow` é zero no primeiro ponto ou o acumulado do item anterior; não existe coluna redundante nem perda estatística.

## Distribuição reconstruída

- Peso total: {metrics['totalWeight']:.8f}.
- Média: {metrics['mean']:.10f}.
- Gini: {metrics['gini']:.10f}.
- RDPC mínimo: {metrics['minRdpc']:.10f}.
- RDPC máximo: {metrics['maxRdpc']:.10f}.
- Peso com RDPC zero: {metrics['zeroWeight']:.8f} ({metrics['zeroWeightShare'] * 100:.6f}%).

## Quantis empíricos

| Quantil | RDPC |
| --- | ---: |
{quantile_rows}

## P90 e P99

A investigação confirmou em documentação oficial do IBGE que pessoas com o mesmo rendimento são alocadas no mesmo percentil, ainda que a proporção final da classe seja apenas aproximada. Essa regra é compatível com a CDF empírica em degraus implementada.

Não foi localizada documentação oficial suficiente para reproduzir exatamente os R$ 1 residuais. A inversa empírica ponderada produz P90 = R$ {quantiles['P90']:.10f} e P99 = R$ {quantiles['P99']:.10f}; após arredondamento usual, R$ 4.610 e R$ 15.215, enquanto o SIDRA publica R$ 4.609 e R$ 15.214. A diferença permanece pendente e não altera a CDF principal.

Foram testadas, sem canonização, três convenções adicionais. No P90, a fronteira por posto médio arredonda para {convention['P90']['midrankClassUpperRounded']} e a interpolação centrada para {convention['P90']['centeredWeightInterpolationRounded']}; no P99, elas arredondam para {convention['P99']['midrankClassUpperRounded']} e {convention['P99']['centeredWeightInterpolationRounded']}. Nenhuma reproduz simultaneamente os dois cortes publicados, portanto não há base para substituir a inversa empírica.

Fontes oficiais consultadas:

- Informativo IBGE 2024, que remete ao Anexo 10 das Notas técnicas versão 1.19 e explicita a regra de empates.
- Anexo 10 das Notas técnicas versão 1.7, consultado como histórico do procedimento anterior.
- SIDRA tabela 7526, com os limites publicados de 2025.

## Golden cases selecionados

| Caso | RDPC | shareBelow | shareAtOrBelow | topShare |
| --- | ---: | ---: | ---: | ---: |
{case_rows}

O caso `R$ 6.500 / 3` usa RDPC exato registrado como `{cases['householdIncome6500Residents3']['rdpcExact']}`; ele é fixture da distribuição e não foi integrado ao site.

## Empates e limites

- `shareBelow(x)` usa exclusivamente `RDPC < x`.
- `shareAtOrBelow(x)` usa `RDPC <= x`.
- `topShare(x) = 1 - shareBelow(x)`.
- Entre valores observados, o resultado permanece constante; nenhuma interpolação é aplicada.
- Em `x = 0`, `shareBelow = 0` e `shareAtOrBelow > 0`.
- No máximo, `shareBelow < 1` e `shareAtOrBelow = 1`.
- Acima do máximo, ambas as participações acumuladas são 1.

## Reprodutibilidade

| Métrica | Run 1 | Run 2 |
| --- | ---: | ---: |
| Valores únicos | {report['runs']['run1']['metrics']['uniqueIncomeValues']} | {report['runs']['run2']['metrics']['uniqueIncomeValues']} |
| Peso | {report['runs']['run1']['metrics']['totalWeight']:.8f} | {report['runs']['run2']['metrics']['totalWeight']:.8f} |
| Média | {report['runs']['run1']['metrics']['mean']:.10f} | {report['runs']['run2']['metrics']['mean']:.10f} |
| Gini | {report['runs']['run1']['metrics']['gini']:.10f} | {report['runs']['run2']['metrics']['gini']:.10f} |
| CDF SHA-256 | `{report['runs']['run1']['cdfSha256']}` | `{report['runs']['run2']['cdfSha256']}` |

## Performance

- Algoritmo: busca binária.
- Consultas: {report['performance']['queries']}.
- Tempo observado: {report['performance']['elapsedMilliseconds']:.3f} ms.
- Média observada: {report['performance']['microsecondsPerLookup']:.3f} µs por lookup.

O tempo é diagnóstico local e não integra o checksum determinístico.

## Testes e escopo

- Testes automatizados: `{report['tests']['status']}`.
- Monotonicidade, limites, empates, média, Gini, quantis, determinismo e golden cases: `PASS`.
- Nenhum dado individual foi incluído.
- `src/` não foi alterado.
- Nenhuma CDF mundial, transformação temporal ou integração ao frontend foi executada.
"""


def main() -> int:
    try:
        config = load_cdf_config(DEFAULT_CDF_CONFIG_PATH)
        tests = run_tests()
        reset_processed(RUN_ROOT)
        run1_dir = RUN_ROOT / "run-1"
        run2_dir = RUN_ROOT / "run-2"
        run1 = build_cdf(DEFAULT_CDF_CONFIG_PATH, run1_dir)
        run2 = build_cdf(DEFAULT_CDF_CONFIG_PATH, run2_dir)
        if run1["cdfSha256"] != run2["cdfSha256"]:
            raise PipelineError("Dois runs produziram CDFs diferentes")
        if run1["manifestSha256"] != run2["manifestSha256"]:
            raise PipelineError("Dois runs produziram manifestos diferentes")

        PRODUCTION_ROOT.mkdir(parents=True, exist_ok=True)
        cdf_name = config["cdfFileName"]
        production_cdf = PRODUCTION_ROOT / cdf_name
        shutil.copyfile(run1_dir / cdf_name, production_cdf)
        if sha256_file(production_cdf) != run1["cdfSha256"]:
            raise PipelineError("Promoção da CDF alterou o artefato")
        cdf, _ = load_cdf_artifact(production_cdf)

        golden = build_golden_cases(cdf, config, run1["cdfSha256"])
        regenerated = build_golden_cases(cdf, config, run1["cdfSha256"])
        if canonical_json(golden) != canonical_json(regenerated):
            raise PipelineError("Golden cases não são determinísticos")
        performance = benchmark_lookup(cdf)
        convention_diagnostics = quantile_convention_diagnostics(cdf, config)
        source_path = repository_path(config["sourceDatasetPath"])
        cdf_manifest = json.loads(
            (run1_dir / config["cdfManifestFileName"]).read_text(encoding="utf-8")
        )
        report = {
            "status": "PASS",
            "brazilDatasetVersion": config["brazilDatasetVersion"],
            "methodologyVersion": config["methodologyVersion"],
            "priceReference": config["priceReference"],
            "sourceDatasetSha256": sha256_file(source_path),
            "cdf": {
                "path": "data/production/brazil/brazil-income-cdf-2025.json",
                "sha256": run1["cdfSha256"],
                "sizeBytes": run1["cdfSizeBytes"],
                "sourceRecords": run1["diagnostics"]["sourceRecords"],
                "uniqueIncomeValues": run1["metrics"]["uniqueIncomeValues"],
                "recordReductionPercent": cdf_manifest["recordReductionPercent"],
                "byteReductionPercent": cdf_manifest["byteReductionPercent"],
                "containsIndividualData": False,
            },
            "distribution": run1["metrics"],
            "quantiles": run1["quantiles"],
            "runs": {"run1": run1, "run2": run2},
            "goldenCases": golden,
            "performance": performance,
            "p90P99Investigation": {
                "status": "PENDENTE",
                "officialTieRuleConfirmed": True,
                "exactOneRealResidualExplained": False,
                "conclusion": "Preservar a CDF empírica e não ajustar artificialmente os cortes.",
                "testedConventions": convention_diagnostics,
                "officialSources": [
                    "https://biblioteca.ibge.gov.br/visualizacao/livros/liv101708_notas_tecnicas.pdf",
                    "https://biblioteca.ibge.gov.br/visualizacao/livros/liv102174_informativo.pdf",
                    "https://sidra.ibge.gov.br/tabela/7526",
                ],
            },
            "tests": tests,
            "scope": {
                "frontendChanged": False,
                "deployed": False,
                "globalMethodologyStarted": False,
                "currentIncomeTransformed": False,
                "individualDataIncluded": False,
                "userIncomePriceAlignmentMethod": None,
            },
        }
        VALIDATION_ROOT.mkdir(parents=True, exist_ok=True)
        (VALIDATION_ROOT / "brazil-income-cdf-manifest.json").write_text(
            canonical_json(cdf_manifest), encoding="utf-8", newline="\n"
        )
        golden_path = VALIDATION_ROOT / config["goldenCasesFileName"]
        golden_path.write_text(
            canonical_json(golden), encoding="utf-8", newline="\n"
        )
        if json.loads(golden_path.read_text(encoding="utf-8")) != golden:
            raise PipelineError("Golden cases gravados não correspondem aos gerados")
        (VALIDATION_ROOT / "pnad-2025-cdf.json").write_text(
            canonical_json(report), encoding="utf-8", newline="\n"
        )
        (VALIDATION_ROOT / "pnad-2025-cdf.md").write_text(
            markdown_report(report), encoding="utf-8", newline="\n"
        )
        print(
            canonical_json(
                {
                    "status": "PASS",
                    "cdfSha256": run1["cdfSha256"],
                    "cdfSizeBytes": run1["cdfSizeBytes"],
                    "uniqueIncomeValues": run1["metrics"]["uniqueIncomeValues"],
                    "goldenCases": len(golden["cases"]),
                }
            ),
            end="",
        )
        return 0
    except (PipelineError, OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
