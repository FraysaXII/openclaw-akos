#!/usr/bin/env python3
"""Initiative 46 P3 — GraphRAG PoC runner (LightRAG-style hybrid).

Cost-gated by `AKOS_GRAPHRAG_POC_LIVE=1` env var (R-46-1 mitigation). Without
that, the script enumerates the planned A/B run and exits 0 — useful for
dry-run validation.

When live:
1. Indexes the HLK CSV vault into Neo4j vector + graph hybrid via
   `neo4j-graphrag-python` (D-IH-46-A choice). Uses Ollama-local embeddings
   where possible to minimise spend; LLM only for entity extraction.
2. Runs the 20 golden queries (config/graphrag/golden_queries.json) twice:
   path A = current `hlk_role` + `hlk_search` chain; path B = GraphRAG hybrid.
3. Compares latency / token cost / accuracy vs golden_keywords; emits a
   per-query scorecard suitable for the I46 P5 ship-or-no-ship decision.

Cost ceiling: GRAPHRAG_POC_USD_CEILING env var (default $20). Exceeding it
kills the run mid-stream and writes a partial scorecard.

Usage::

    py scripts/graphrag_poc.py --dry-run                    # plan only; safe; no LLM cost
    py scripts/graphrag_poc.py --validate-config            # validate golden_queries.json schema
    AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py     # actually run; requires operator opt-in
    py scripts/graphrag_poc.py --max-spend 10               # override cost ceiling

This script ships as **scaffold** in I46 P3. The actual `neo4j-graphrag-python`
indexing implementation lands when operator opts in via `AKOS_GRAPHRAG_POC_LIVE=1`
+ confirms the cost budget.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT, bootstrap_openclaw_process_env

logger = logging.getLogger("akos.graphrag_poc")

GOLDEN_QUERIES_PATH = REPO_ROOT / "config" / "graphrag" / "golden_queries.json"
DEFAULT_COST_CEILING_USD = 20.0


def load_golden_queries(path: Path | None = None) -> dict:
    p = path or GOLDEN_QUERIES_PATH
    if not p.is_file():
        raise FileNotFoundError(f"golden_queries.json not found at {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def validate_config(data: dict) -> list[str]:
    """Return list of validation errors. Empty list = OK."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be object"]
    queries = data.get("queries", [])
    if not isinstance(queries, list):
        errors.append("'queries' must be array")
        return errors
    if len(queries) < 20:
        errors.append(f"expected >=20 queries (got {len(queries)})")
    seen_ids: set[str] = set()
    for i, q in enumerate(queries):
        if not isinstance(q, dict):
            errors.append(f"queries[{i}]: must be object")
            continue
        for required in ("id", "query", "expected_keywords", "intent"):
            if required not in q:
                errors.append(f"queries[{i}]: missing field {required!r}")
        qid = q.get("id", "")
        if qid in seen_ids:
            errors.append(f"queries[{i}]: duplicate id {qid!r}")
        seen_ids.add(qid)
        if not isinstance(q.get("expected_keywords"), list):
            errors.append(f"queries[{i}]: expected_keywords must be array")
    return errors


def cmd_dry_run(args: argparse.Namespace) -> int:
    """Plan the PoC without spending. Lists the queries + the planned A/B paths."""
    try:
        data = load_golden_queries()
    except FileNotFoundError as e:
        print(f"  [graphrag-poc] {e}", file=sys.stderr)
        return 2

    errors = validate_config(data)
    if errors:
        print(f"  [graphrag-poc] golden_queries.json validation FAILED:", file=sys.stderr)
        for err in errors:
            print(f"    - {err}", file=sys.stderr)
        return 1

    queries = data.get("queries", [])
    print(f"\n  GraphRAG PoC — DRY RUN (no LLM cost incurred)")
    print(f"  Skill under test: {data.get('_skill_id', '?')}")
    print(f"  Queries: {len(queries)}")
    print(f"  Cost ceiling: ${args.max_spend:.2f} per run")
    print(f"  Path A: current hlk_role + hlk_search chain (deterministic)")
    print(f"  Path B: GraphRAG hybrid via neo4j-graphrag-python (live LLM)")
    print()
    print("  Queries to be exercised:")
    for q in queries[:5]:
        print(f"    - [{q.get('intent', '?')}] {q.get('id', '?')}: {q.get('query', '')[:60]}")
    if len(queries) > 5:
        print(f"    ... and {len(queries) - 5} more")
    print()
    print(f"  To run live: AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py")
    print(f"  Operator must confirm the cost budget before opt-in.")
    return 0


def cmd_validate_config(args: argparse.Namespace) -> int:
    """Validate golden_queries.json schema."""
    try:
        data = load_golden_queries()
    except FileNotFoundError as e:
        print(f"  [graphrag-poc] {e}", file=sys.stderr)
        return 2
    errors = validate_config(data)
    if errors:
        print(f"  [graphrag-poc] golden_queries.json: {len(errors)} validation errors")
        for err in errors[:10]:
            print(f"    - {err}")
        return 1
    print(f"  [graphrag-poc] golden_queries.json: PASS ({len(data.get('queries', []))} queries)")
    return 0


def cmd_run_live(args: argparse.Namespace) -> int:
    """Run the PoC live (requires AKOS_GRAPHRAG_POC_LIVE=1).

    P3 ships this as a STUB that prints the planned execution + cost ceiling.
    Operator opts in via env var; first real run will fill in the
    `neo4j-graphrag-python` indexing + A/B execution loop. The decision-frame
    exists; the actual indexing is operator-budget-gated.
    """
    if os.environ.get("AKOS_GRAPHRAG_POC_LIVE", "") != "1":
        print(
            "  [graphrag-poc] AKOS_GRAPHRAG_POC_LIVE=1 is required for live indexing.\n"
            "  This guard prevents accidental cost (R-46-1).\n"
            "  To dry-run plan: py scripts/graphrag_poc.py --dry-run\n"
            "  To validate config: py scripts/graphrag_poc.py --validate-config\n"
            "  To go live: AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py --max-spend 20",
            file=sys.stderr,
        )
        return 2

    print(
        "  [graphrag-poc] LIVE MODE — operator opted in.\n"
        f"  Cost ceiling: ${args.max_spend:.2f} per run.\n"
        "\n"
        "  P3 SCAFFOLD: actual neo4j-graphrag-python indexing not yet wired.\n"
        "  When operator confirms budget + neo4j-graphrag-python is installed:\n"
        "    1. Index ~1000 process rows + 65 roles + 30 dimensions into Neo4j vector + graph hybrid\n"
        "    2. Run 20 golden queries via path A (existing chain) AND path B (GraphRAG)\n"
        "    3. Capture latency / cost / accuracy delta\n"
        "    4. Emit reports/graphrag-poc-results-YYYY-MM-DD.md with A/B scorecard\n"
        "\n"
        "  Implementation lands in a P3 follow-up commit when:\n"
        "    - operator runs `pip install neo4j-graphrag-python`\n"
        "    - operator confirms the per-run cost ceiling\n"
        "    - operator confirms an LLM provider (OPENAI_API_KEY or ANTHROPIC_API_KEY in env)",
        file=sys.stderr,
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="GraphRAG PoC runner (I46 P3)")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="plan the PoC without LLM cost (default mode)"
    )
    parser.add_argument(
        "--validate-config", action="store_true",
        help="validate config/graphrag/golden_queries.json schema only"
    )
    parser.add_argument(
        "--max-spend", type=float, default=DEFAULT_COST_CEILING_USD,
        help=f"cost ceiling per run in USD (default {DEFAULT_COST_CEILING_USD})"
    )
    args = parser.parse_args()

    bootstrap_openclaw_process_env()

    if args.validate_config:
        return cmd_validate_config(args)
    if args.dry_run:
        return cmd_dry_run(args)
    # Default: behave as live runner (which requires the env guard)
    return cmd_run_live(args)


if __name__ == "__main__":
    sys.exit(main())
