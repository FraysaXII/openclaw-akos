#!/usr/bin/env python3
"""LangGraph OSS evaluation spike runner (I76 charter).

Usage::

    py scripts/langgraph_spike_run.py --json
    py scripts/langgraph_spike_run.py --fixture path/to/source-ledger.csv --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from akos.langgraph_spike.runner import run_research_action_spike, write_evidence_artifact
from akos.log import setup_logging


def main() -> int:
    setup_logging()
    parser = argparse.ArgumentParser(description="LangGraph OSS research-action spike")
    parser.add_argument("--fixture", type=Path, default=None, help="source-ledger.csv fixture")
    parser.add_argument("--json", action="store_true", help="emit JSON to stdout")
    parser.add_argument("--write-artifact", action="store_true", help="write artifacts/langgraph-spike/*.json")
    parser.add_argument("--no-langfuse", action="store_true", help="skip Langfuse emit")
    parser.add_argument(
        "--require-langgraph",
        action="store_true",
        help="fail unless real langgraph package runs (CI proof class)",
    )
    args = parser.parse_args()

    result = run_research_action_spike(
        args.fixture,
        emit_langfuse=not args.no_langfuse,
        require_langgraph=args.require_langgraph,
    )
    if args.write_artifact:
        write_evidence_artifact(result)

    payload = result.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"status={result.status} engine={result.engine} validation={result.research_action_validation}")

    return 0 if result.status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
