"""Executa dois runs limpos e publica somente relatórios de validação pequenos."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import xlrd

from pipeline import (
    DEFAULT_CONFIG_PATH,
    ROOT,
    PipelineError,
    build_dataset,
    canonical_json,
    load_config,
    sha256_file,
    validate_existing_output,
)


PROCESSED_ROOT = ROOT / "data/processed"
RUN_ROOT = PROCESSED_ROOT / "brazil/validation-runs"
FINAL_OUTPUT = PROCESSED_ROOT / "brazil/pnad-2025"
REPORT_ROOT = ROOT / "validation/brazil"


def reset_generated_directory(path: Path) -> None:
    resolved = path.resolve()
    processed = PROCESSED_ROOT.resolve()
    if not resolved.is_relative_to(processed) or resolved == processed:
        raise PipelineError(f"Recusa de limpar caminho fora de data/processed: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def run_unit_tests() -> dict[str, object]:
    execution_command = [
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
    documented_command = ["python", *execution_command[1:]]
    completed = subprocess.run(execution_command, cwd=ROOT, text=True, capture_output=True)
    transcript = (completed.stdout + completed.stderr).strip()
    if completed.returncode != 0:
        raise PipelineError(f"Testes automatizados falharam:\n{transcript}")
    return {
        "status": "PASS",
        "command": documented_command,
        "transcript": transcript,
    }


def copy_validated_output(source_dir: Path, config: dict[str, object]) -> dict[str, object]:
    reset_generated_directory(FINAL_OUTPUT)
    FINAL_OUTPUT.mkdir(parents=True)
    output = config["output"]
    assert isinstance(output, dict)
    dataset_name = str(output["fileName"])
    manifest_name = str(output["manifestFileName"])
    shutil.copyfile(source_dir / dataset_name, FINAL_OUTPUT / dataset_name)
    shutil.copyfile(source_dir / manifest_name, FINAL_OUTPUT / manifest_name)
    return validate_existing_output(DEFAULT_CONFIG_PATH, FINAL_OUTPUT)


def format_number(value: float, digits: int = 10) -> str:
    return f"{value:.{digits}f}"


def markdown_report(report: dict[str, object]) -> str:
    run1 = report["runs"]["run1"]
    run2 = report["runs"]["run2"]
    metrics = run1["metrics"]
    quantiles = report["benchmarks"]["quantiles"]
    return f"""# Validação do pipeline brasileiro — PNAD Contínua 2025

**Resultado:** `{report['status']}`

**Metodologia:** `{report['methodologyVersion']}`
**Referência monetária:** preços médios de 2025

## Fonte e configuração

- Arquivo: `{report['source']['file']}`
- Release: `{report['source']['release']}`
- SHA-256: `{report['source']['sha256']}`
- Configuração: `config/brazil-pnad-2025.json`
- SHA-256 da configuração: `{report['configSha256']}`

## Fórmula implementada

```text
RDPC_real_2025 =
  soma_domiciliar(VD4019 × CO1 + VD4048 × CO1e)
  ÷ VD2003
```

A distribuição final preserva uma linha por pessoa elegível e usa `V1032` como peso. O join dos deflatores usa `Ano + Trimestre + UF`.

## Reprodutibilidade

| Métrica | Run 1 | Run 2 |
| --- | ---: | ---: |
| Registros | {run1['metrics']['records']} | {run2['metrics']['records']} |
| Média | {format_number(run1['metrics']['mean'])} | {format_number(run2['metrics']['mean'])} |
| Gini | {format_number(run1['metrics']['gini'])} | {format_number(run2['metrics']['gini'])} |
| População ponderada | {format_number(run1['metrics']['population'], 4)} | {format_number(run2['metrics']['population'], 4)} |
| SHA-256 dataset | `{run1['datasetSha256']}` | `{run2['datasetSha256']}` |
| SHA-256 manifesto | `{run1['manifestSha256']}` | `{run2['manifestSha256']}` |

Os dois runs limpos produziram datasets e manifestos byte a byte idênticos.

## Benchmarks

- Média nacional: {format_number(metrics['mean'])}; arredondada: R$ {metrics['meanRounded']} — `PASS`.
- Gini: {format_number(metrics['gini'])}; publicado em três casas: {metrics['giniRounded3']} — `PASS`.
- População ponderada: {format_number(metrics['population'], 4)}; publicação em milhares: {metrics['populationThousandRounded']} — `PASS`.
- Médias por UF: {report['benchmarks']['ufMeans']['matches']} de {report['benchmarks']['ufMeans']['total']} reproduzidas após arredondamento — `PASS`.
- Rendas zero: {metrics['zeroRecords']} registros preservados.
- Rendas negativas: {metrics['negativeRecords']}.
- Máximo observado: R$ {format_number(metrics['maximum'], 4)}.

## Quantis diagnósticos

| Quantil | Calculado | Publicado | Diferença arredondada |
| --- | ---: | ---: | ---: |
{chr(10).join(f"| {label} | {quantiles[label]['calculatedRounded']} | {quantiles[label]['published']} | {quantiles[label]['differenceRounded']:+d} |" for label in sorted(quantiles, key=lambda value: float(value[1:])))}

Os resíduos conhecidos de R$ 1 em P90 e P99 foram reproduzidos e permanecem documentados; nenhuma correção artificial foi aplicada.

## Validações estruturais

- Registros brutos: {report['structural']['sourceRecords']}.
- Pessoas elegíveis: {report['structural']['eligiblePersons']}.
- Domicílios elegíveis: {report['structural']['eligibleHouseholds']}.
- Chaves de pessoa únicas: {report['structural']['uniquePersonKeys']}.
- Divergências na reconstrução nominal contra `VD5007`: {report['structural']['nominalRecompositionMismatches']}.
- Join de deflatores: 108 de 108 chaves oficiais.
- Peso final: numérico, finito e estritamente positivo.
- RDPC final: finito, não negativo e com zeros preservados.

## Testes e ambiente

- Testes automatizados: `{report['tests']['status']}`.
- Python: `{report['environment']['python']}`.
- NumPy: `{report['environment']['numpy']}`.
- xlrd: `{report['environment']['xlrd']}`.

## Limites desta fase

Não foram criados CDF, lookup, golden cases ou integração com o frontend. O alinhamento temporal da renda digitada e a metodologia Mundo continuam pendentes. O dataset intermediário permanece local e ignorado pelo Git; somente o manifesto e os relatórios sem dados individuais são versionados.
"""


def main() -> int:
    try:
        config = load_config(DEFAULT_CONFIG_PATH)
        tests = run_unit_tests()
        reset_generated_directory(RUN_ROOT)
        run1_dir = RUN_ROOT / "run-1"
        run2_dir = RUN_ROOT / "run-2"
        run1 = build_dataset(DEFAULT_CONFIG_PATH, run1_dir)
        run2 = build_dataset(DEFAULT_CONFIG_PATH, run2_dir)
        run1 = validate_existing_output(DEFAULT_CONFIG_PATH, run1_dir)
        run2 = validate_existing_output(DEFAULT_CONFIG_PATH, run2_dir)
        if run1["datasetSha256"] != run2["datasetSha256"]:
            raise PipelineError("Os dois runs produziram checksums diferentes para o dataset")
        if run1["manifestSha256"] != run2["manifestSha256"]:
            raise PipelineError("Os dois runs produziram checksums diferentes para o manifesto")
        final = copy_validated_output(run1_dir, config)
        if final["datasetSha256"] != run1["datasetSha256"]:
            raise PipelineError("A promoção local alterou o dataset validado")

        manifest_name = str(config["output"]["manifestFileName"])
        manifest = json.loads((FINAL_OUTPUT / manifest_name).read_text(encoding="utf-8"))
        report = {
            "status": "PASS",
            "dataset": "brazil-income-distribution",
            "methodologyVersion": config["methodologyVersion"],
            "source": {
                "file": config["sourceFile"],
                "release": config["release"],
                "sha256": config["sourceSha256"],
            },
            "configSha256": sha256_file(DEFAULT_CONFIG_PATH),
            "formula": "sum_household(VD4019 * CO1 + VD4048 * CO1e) / VD2003",
            "runs": {"run1": run1, "run2": run2},
            "reproducibility": {
                "status": "PASS",
                "datasetChecksumsIdentical": True,
                "manifestChecksumsIdentical": True,
            },
            "structural": manifest["structuralValidation"],
            "benchmarks": manifest["benchmarkValidation"],
            "tests": tests,
            "environment": {
                "python": platform.python_version(),
                "numpy": np.__version__,
                "xlrd": xlrd.__version__,
            },
            "generatedArtifacts": {
                "datasetLocalPath": final["datasetPath"],
                "datasetSizeBytes": final["datasetSizeBytes"],
                "datasetSha256": final["datasetSha256"],
                "manifestSha256": final["manifestSha256"],
            },
            "knownDifferences": {
                "P90": "calculado arredondado = publicado + R$ 1",
                "P99": "calculado arredondado = publicado + R$ 1",
            },
            "scope": {
                "cdfCreated": False,
                "lookupCreated": False,
                "frontendChanged": False,
                "deploymentPerformed": False,
                "rawCommitted": False,
            },
        }
        REPORT_ROOT.mkdir(parents=True, exist_ok=True)
        json_path = REPORT_ROOT / "pnad-2025-pipeline.json"
        md_path = REPORT_ROOT / "pnad-2025-pipeline.md"
        manifest_path = REPORT_ROOT / "brazil-income-distribution-manifest.json"
        json_path.write_text(canonical_json(report), encoding="utf-8", newline="\n")
        md_path.write_text(markdown_report(report), encoding="utf-8", newline="\n")
        manifest_path.write_text(canonical_json(manifest), encoding="utf-8", newline="\n")
        print(canonical_json({"status": "PASS", **report["generatedArtifacts"]}), end="")
        return 0
    except (PipelineError, OSError, ValueError, KeyError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
