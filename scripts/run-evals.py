#!/usr/bin/env python3
"""Agent reliability evaluation runner for AKOS.

Supports suite manifests under ``tests/evals/suites/<id>/`` and optional
Langfuse v4 scoring via ``akos.telemetry.LangfuseReporter``.

Usage:
    py scripts/run-evals.py list
    py scripts/run-evals.py run --suite pathc-research-spine --dry-run
    py scripts/run-evals.py run --suite pathc-research-spine --mode rubric
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.eval_harness import list_suite_ids as _list_suite_ids
from akos.eval_harness import load_suite as _load_suite
from akos.eval_harness import score_rubric_task
from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults
from akos.log import setup_logging
from akos.telemetry import LangfuseReporter

logger = logging.getLogger("akos.evals")

EVALS_DIR = Path(__file__).resolve().parent.parent / "tests" / "evals"
LEGACY_TASKS = EVALS_DIR / "tasks.json"


def _load_legacy_tasks() -> list[dict]:
    if not LEGACY_TASKS.exists():
        return []
    data = json.loads(LEGACY_TASKS.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def cmd_list(_args: argparse.Namespace | None = None) -> int:
    suites = _list_suite_ids()
    print("\n  AKOS eval suites")
    if suites:
        for s in suites:
            print(f"    - {s}")
    else:
        print("    (no suites under tests/evals/suites/)")
    legacy = _load_legacy_tasks()
    if legacy:
        print(f"\n  Legacy tasks.json: {len(legacy)} task(s)\n")
    else:
        print()
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    setup_logging(json_output=args.json_log)
    set_process_env_defaults(load_runtime_env(resolve_openclaw_home()))
    reporter = LangfuseReporter()

    if args.suite:
        manifest, tasks = _load_suite(args.suite)
        suite_id = str(manifest.get("suite_id") or args.suite)
    else:
        tasks = _load_legacy_tasks()
        suite_id = "legacy-tasks-json"
        manifest = {"suite_id": suite_id, "version": "0"}

    if not tasks:
        print("\n  No tasks to run.\n")
        return 1

    print(f"\n  Suite: {suite_id} ({len(tasks)} tasks)")
    print(f"  Mode: {args.mode}")
    if reporter.enabled:
        print("  Langfuse: enabled")
    print("  " + "-" * 50)

    exit_code = 0
    for task in tasks:
        tid = str(task.get("id", "<no-id>"))
        name = str(task.get("name", ""))
        if args.dry_run:
            print(f"  [DRY-RUN ] {tid} -- {name}")
            if reporter.enabled:
                reporter.trace_eval_outcome(
                    suite_id=suite_id,
                    task_id=tid,
                    mode="dry-run",
                    pass_fail="PASS",
                    trials=args.trials,
                    dimension_id=str(task.get("dimension_id") or ""),
                    research_surface=str(task.get("research_surface") or "none"),
                )
            continue

        if args.mode == "rubric":
            golden = task.get("golden_answer")
            if not golden:
                print(f"  [SKIP   ] {tid} -- no golden_answer for rubric mode")
                continue
            status, reasons = score_rubric_task(task, str(golden))
            detail = "" if status == "PASS" else " :: " + "; ".join(reasons)
            print(f"  [{status:8s}] {tid} -- {name}{detail}")
            if status != "PASS":
                exit_code = 1
            if reporter.enabled:
                reporter.trace_eval_outcome(
                    suite_id=suite_id,
                    task_id=tid,
                    mode="rubric",
                    pass_fail=status,
                    trials=args.trials,
                    dimension_id=str(task.get("dimension_id") or ""),
                    research_surface=str(task.get("research_surface") or "none"),
                )
        else:
            print(f"  [PENDING] {tid} -- live execution not implemented in CI (use gateway worker)")
            if reporter.enabled:
                reporter.trace_eval_outcome(
                    suite_id=suite_id,
                    task_id=tid,
                    mode="live-pending",
                    pass_fail="SKIP",
                    trials=args.trials,
                    dimension_id=str(task.get("dimension_id") or ""),
                    research_surface=str(task.get("research_surface") or "none"),
                )

    print()
    if args.dry_run:
        print("  Dry run complete.\n")
    elif args.mode == "rubric":
        print("  Rubric run complete.\n")
    else:
        print("  Configure gateway + model for live evals.\n")

    reporter.flush()
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description="AKOS agent reliability eval runner")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List eval suites")
    p_list.set_defaults(func=cmd_list)

    p_run = sub.add_parser("run", help="Run an eval suite")
    p_run.add_argument("--suite", required=True, help="Suite directory name under tests/evals/suites/")
    p_run.add_argument("--dry-run", action="store_true", help="Enumerate tasks without scoring")
    p_run.add_argument("--mode", default="rubric", choices=("rubric", "live"), help="Evaluation mode")
    p_run.add_argument("--trials", type=int, default=1, help="Trial count metadata for Langfuse (M2)")
    p_run.add_argument("--json-log", action="store_true", help="JSON logging output")
    p_run.set_defaults(func=cmd_run)

    args = parser.parse_args()
    fn = getattr(args, "func", None)
    if fn is None:
        return 1
    return int(fn(args))


if __name__ == "__main__":
    raise SystemExit(main())
