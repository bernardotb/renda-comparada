from __future__ import annotations

import json

from pipeline import run_pipeline


if __name__ == "__main__":
    report = run_pipeline()
    print(
        json.dumps(
            {
                "status": report["status"],
                "sourceSha256": report["source"]["sha256"],
                "candidateSha256": report["candidate"]["sha256"],
                "maxAbsErrorPp": report["validationMetrics"]["maxAbsErrorPp"],
                "decisionGate": report["decisionGate"]["status"],
            },
            indent=2,
        )
    )
