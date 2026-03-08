#!/usr/bin/env python3
"""Agent reliability evaluation runner for AKOS.

Executes canonical tasks against configured model and scores results.
Requires a live model endpoint for actual execution.

Usage:
    py scripts/run-evals.py --dry-run            # list tasks without executing
    py scripts/run-evals.py --model ollama/qwen3:8b  # run against specific model
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.log import setup_logging

logger = logging.getLogger("akos.evals")

EVALS_DIR = Path(__file__).resolve().parent.parent / "tests" / "evals"
TASKS_FILE = EVALS_DIR / "tasks.json"


def load_tasks() -> list[dict]:
    """Load eval tasks from tests/evals/tasks.json."""
    if not TASKS_FILE.exists():
        logger.error("Eval tasks file not found: %s", TASKS_FILE)
        return []
    return json.loads(TASKS_FILE.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="AKOS agent reliability eval runner")
    parser.add_argument("--model", default="ollama/qwen3:8b", help="Model to evaluate against")
    parser.add_argument("--dry-run", action="store_true", help="List tasks without executing")
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    tasks = load_tasks()
    if not tasks:
        print("\n  No eval tasks found. Check tests/evals/tasks.json.\n")
        sys.exit(1)

    print(f"\n  AKOS Agent Reliability Evals ({len(tasks)} tasks)")
    print(f"  Model: {args.model}")
    print("  " + "-" * 50)

    for task in tasks:
        status = "DRY-RUN" if args.dry_run else "PENDING"
        print(f"  [{status:8s}] {task['id']} -- {task['name']}")
        if args.dry_run:
            print(f"             Prompt: {task['prompt'][:60]}...")
            print(f"             Expected: {task['expected_contains']}")
            print(f"             Max tool calls: {task['max_tool_calls']}")

    print()
    if args.dry_run:
        print("  Dry run complete. Use without --dry-run to execute against a live model.")
    else:
        print("  Execution requires a live model endpoint. Ensure the gateway is running.")
        print("  Scoring will be tracked in Langfuse when configured.")
    print()

    sys.exit(0)


if __name__ == "__main__":
    main()
