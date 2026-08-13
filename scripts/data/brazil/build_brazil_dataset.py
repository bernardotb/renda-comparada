"""CLI de construção do dataset intermediário brasileiro."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline import DEFAULT_CONFIG_PATH, DEFAULT_OUTPUT_DIR, PipelineError, build_dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Constrói o dataset intermediário determinístico da PNAD 2025."
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = build_dataset(args.config, args.output_dir)
    except PipelineError as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "PASS", **result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
