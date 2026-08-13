"""CLI para gerar a CDF brasileira a partir do dataset validado da Fase 1D."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cdf import DEFAULT_CDF_CONFIG_PATH, DEFAULT_CDF_OUTPUT_DIR, build_cdf
from pipeline import PipelineError


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera a CDF empírica brasileira de 2025.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CDF_CONFIG_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_CDF_OUTPUT_DIR)
    args = parser.parse_args()
    try:
        result = build_cdf(args.config, args.output_dir)
    except (PipelineError, OSError, ValueError, KeyError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "PASS", **result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
