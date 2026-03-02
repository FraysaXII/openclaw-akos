#!/usr/bin/env python3
"""Tail the OpenCLAW gateway log and push traces to Langfuse.

Parses JSON log entries from the gateway, pushes agent activity to
Langfuse for tracing/evaluation, and evaluates real-time alerts.

Usage:
    python scripts/log-watcher.py                 # foreground watcher
    python scripts/log-watcher.py --once           # single pass (CI/test)
    python scripts/log-watcher.py --json-log       # structured JSON output

Environment:
    LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY  (from config/eval/langfuse.env.example)
    LOG_WATCHER_POLL_INTERVAL                 (seconds between polls, default 2)

Requires: Python 3.10+, langfuse (optional for telemetry).
"""

import argparse
import json
import logging
import os
import sys
import tempfile
import time
from collections.abc import Iterator
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.alerts import AlertEvaluator
from akos.io import REPO_ROOT
from akos.log import setup_logging
from akos.telemetry import LangfuseReporter

logger = logging.getLogger("akos.log-watcher")


def get_log_path() -> Path:
    """Determine the OpenCLAW gateway log file path for today."""
    today = date.today().isoformat()
    base = Path(tempfile.gettempdir())
    return base / "openclaw" / f"openclaw-{today}.log"


def parse_log_line(line: str) -> dict | None:
    """Try to parse a JSON log line, returning None on failure."""
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def tail_file(path: Path, poll_interval: float, *, once: bool = False) -> Iterator[str]:
    """Yield new lines from a file, optionally looping forever."""
    if not path.exists():
        logger.warning("Log file not found: %s", path)
        if once:
            return
        logger.info("Waiting for log file to appear...")
        while not path.exists():
            time.sleep(poll_interval)

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        f.seek(0, 2)  # start at end of file
        if once:
            return

        while True:
            line = f.readline()
            if line:
                yield line
            else:
                time.sleep(poll_interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenCLAW log watcher + Langfuse telemetry")
    parser.add_argument("--once", action="store_true", help="Single pass then exit (for CI/tests)")
    parser.add_argument("--json-log", action="store_true", help="Structured JSON log output")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    poll_interval = float(os.environ.get("LOG_WATCHER_POLL_INTERVAL", "2"))
    log_path = get_log_path()
    logger.info("Watching: %s (poll every %.1fs)", log_path, poll_interval)

    reporter = LangfuseReporter()
    if reporter.enabled:
        logger.info("Langfuse telemetry enabled")
    else:
        logger.info("Langfuse telemetry disabled (no credentials or package)")

    alerts_path = REPO_ROOT / "config" / "eval" / "alerts.json"
    baselines_path = REPO_ROOT / "config" / "eval" / "baselines.json"
    try:
        alert_evaluator = AlertEvaluator(alerts_path, baselines_path)
    except Exception as exc:
        logger.warning("Could not load alert configs: %s", exc)
        alert_evaluator = None

    entries_processed = 0

    try:
        for line in tail_file(log_path, poll_interval, once=args.once):
            entry = parse_log_line(line)
            if not entry:
                continue

            entries_processed += 1

            reporter.trace_request(entry)

            if alert_evaluator is not None:
                alert_evaluator.check_realtime(entry)

            if entries_processed % 100 == 0:
                reporter.flush()
                logger.debug("Processed %d entries", entries_processed)

    except KeyboardInterrupt:
        logger.info("Shutting down (processed %d entries)", entries_processed)
    finally:
        reporter.flush()
        logger.info("Final flush complete (%d entries total)", entries_processed)


if __name__ == "__main__":
    main()
