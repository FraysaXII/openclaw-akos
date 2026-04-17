#!/usr/bin/env python3
"""Print intent routing table for golden corpus (regex + optional embedding).

Used for Initiative 13 before/after benchmarks. Does not mutate config.

Usage::

    py scripts/intent_benchmark.py

With Ollama + nomic-embed-text running, shows embedding path; otherwise embedding
column shows ``(unavailable)``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from akos.intent import _classify_regex, classify_request  # noqa: E402


def main() -> int:
    golden = _REPO / "tests" / "fixtures" / "intent_golden.json"
    cases = json.loads(golden.read_text(encoding="utf-8"))["cases"]
    print("id\tquery\tregex_route\tfull_route\tmethod")
    for c in cases:
        q = c["query"]
        reg = _classify_regex(q)
        full = classify_request(q)
        print(
            f"{c['id']}\t{q[:80]!r}\t{reg}\t{full['route']}\t{full['method']}",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
