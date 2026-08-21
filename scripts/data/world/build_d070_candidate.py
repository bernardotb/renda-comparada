from __future__ import annotations

import json

from d070 import run


if __name__ == "__main__":
    result = run()
    print(
        json.dumps(
            {
                "status": result["status"],
                "d070Canonical": result["d070Canonical"],
                "frontendIntegrationAllowed": result["frontendIntegrationAllowed"],
                "goldenCases": result["goldenCases"],
            },
            indent=2,
        )
    )
