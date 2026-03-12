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
from akos.io import REPO_ROOT, load_env_file, load_json, resolve_openclaw_home
from akos.log import setup_logging
from akos.models import RunPodEndpointConfig
from akos.runpod_provider import RunPodProvider
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
        if once:
            for line in f:
                yield line
            return

        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                yield line
            else:
                time.sleep(poll_interval)


def _init_runpod_provider() -> tuple[RunPodProvider | None, RunPodEndpointConfig | None]:
    """Try to create a RunPod provider from the gpu-runpod environment config."""
    config_path = REPO_ROOT / "config" / "environments" / "gpu-runpod.json"
    if not config_path.exists():
        return None, None

    try:
        raw = load_json(config_path)
        runpod_block = raw.get("runpod")
        if not runpod_block:
            return None, None
        rpconfig = RunPodEndpointConfig.model_validate(runpod_block)
        provider = RunPodProvider(rpconfig)
        if provider.enabled:
            logger.info(
                "RunPod health monitoring enabled (every %ds)",
                rpconfig.healthCheck.intervalSeconds,
            )
            return provider, rpconfig
    except Exception as exc:
        logger.debug("RunPod provider init skipped: %s", exc)
    return None, None


def _maybe_check_runpod(
    provider: RunPodProvider | None,
    reporter: LangfuseReporter,
    dry_run: bool,
    interval: float,
    last_check: float,
) -> float:
    """Run a RunPod health check if the interval has elapsed. Returns updated timestamp."""
    if provider is None or not provider.enabled:
        return last_check

    now = time.monotonic()
    if now - last_check < interval:
        return last_check

    health = provider.health_check()
    health_entry = {
        "agent_role": "system",
        "tool_name": "runpod_health_check",
        "outcome": "healthy" if health.healthy else "unhealthy",
        "workers_ready": health.workers_ready,
        "workers_running": health.workers_running,
        "queue_depth": health.queue_depth,
    }

    if dry_run:
        logger.info("[DRY-RUN] RunPod health: %s", health_entry)
    else:
        reporter.trace_request(health_entry)

    if not health.healthy:
        logger.warning(
            "RunPod endpoint unhealthy: ready=%d, running=%d, queue=%d",
            health.workers_ready,
            health.workers_running,
            health.queue_depth,
        )

    return now


def _handle_audit_line(line: str, reporter: LangfuseReporter, dry_run: bool) -> None:
    """Handle a raw (non-JSON) log line containing a Post-Compaction Audit warning."""
    if dry_run:
        logger.info("[DRY-RUN] startup audit FAIL (raw line): %s", line.strip()[:120])
    else:
        reporter.trace_startup_compliance(
            agent_role="unknown",
            files_read=[],
            files_missing=[],
            audit_passed=False,
        )


def main() -> None:
    default_env = str(REPO_ROOT / "config" / "eval" / "langfuse.env")
    parser = argparse.ArgumentParser(description="OpenCLAW log watcher + Langfuse telemetry")
    parser.add_argument("--once", action="store_true", help="Single pass then exit (for CI/tests)")
    parser.add_argument("--json-log", action="store_true", help="Structured JSON log output")
    parser.add_argument("--env-file", default=default_env,
                        help="Path to Langfuse .env file (default: config/eval/langfuse.env)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be sent to Langfuse without calling the SDK")
    parser.add_argument("--environment", "-e",
                        default=os.environ.get("AKOS_ENV", "dev-local"),
                        help="Environment tag for traces (dev-local, gpu-runpod, prod-cloud)")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    # Load Langfuse creds
    env_path = Path(args.env_file)
    env_vars = load_env_file(env_path)
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value
    if env_vars:
        logger.info("Loaded %d vars from %s", len(env_vars), env_path)

    # Load OpenCLAW .env for AKOS_ENV (overrides --environment if set)
    oc_env = resolve_openclaw_home() / ".env"
    oc_vars = load_env_file(oc_env)
    for key, value in oc_vars.items():
        if key not in os.environ:
            os.environ[key] = value
    env_tag = os.environ.get("AKOS_ENV", args.environment)

    poll_interval = float(os.environ.get("LOG_WATCHER_POLL_INTERVAL", "2"))
    log_path = get_log_path()
    logger.info("Watching: %s (poll every %.1fs)", log_path, poll_interval)

    dry_run = args.dry_run
    reporter = LangfuseReporter(environment=env_tag)
    if dry_run:
        logger.info("Dry-run mode: traces will be printed, not sent to Langfuse")
    elif reporter.enabled:
        logger.info("Langfuse telemetry enabled (environment=%s)", env_tag)
    else:
        logger.info("Langfuse telemetry disabled (no credentials or package)")

    alerts_path = REPO_ROOT / "config" / "eval" / "alerts.json"
    baselines_path = REPO_ROOT / "config" / "eval" / "baselines.json"
    try:
        alert_evaluator = AlertEvaluator(alerts_path, baselines_path)
    except Exception as exc:
        logger.warning("Could not load alert configs: %s", exc)
        alert_evaluator = None

    runpod_provider, runpod_config = _init_runpod_provider()
    runpod_interval = runpod_config.healthCheck.intervalSeconds if runpod_config else 60.0
    last_runpod_check = 0.0

    entries_processed = 0
    _AUDIT_MARKER = "Post-Compaction Audit"
    _audit_seen = False
    _gateway_start_time: float | None = None
    _STARTUP_GRACE_SECONDS = 30.0
    _metric_counters: dict[str, int] = {}
    _latency_sum: float = 0.0
    _latency_count: int = 0

    try:
        for line in tail_file(log_path, poll_interval, once=args.once):
            entry = parse_log_line(line)
            if not entry:
                if _AUDIT_MARKER in line:
                    _audit_seen = True
                    _handle_audit_line(line, reporter, dry_run)
                last_runpod_check = _maybe_check_runpod(
                    runpod_provider, reporter, dry_run,
                    runpod_interval, last_runpod_check,
                )
                continue

            outcome_str = str(entry.get("outcome", ""))
            msg_str = str(entry.get("message", ""))

            if "gateway" in msg_str.lower() and "start" in msg_str.lower():
                _gateway_start_time = time.monotonic()
                _audit_seen = False

            if _AUDIT_MARKER in outcome_str or _AUDIT_MARKER in msg_str:
                _audit_seen = True
                files_missing = entry.get("files_missing", [])
                agent = entry.get("agent_role", "unknown")
                if dry_run:
                    logger.info("[DRY-RUN] startup audit FAIL: agent=%s missing=%s", agent, files_missing)
                else:
                    reporter.trace_startup_compliance(
                        agent_role=agent,
                        files_read=[],
                        files_missing=files_missing,
                        audit_passed=False,
                    )

            if (_gateway_start_time is not None
                    and not _audit_seen
                    and (time.monotonic() - _gateway_start_time) >= _STARTUP_GRACE_SECONDS):
                if dry_run:
                    logger.info("[DRY-RUN] startup audit PASS (no audit warning within grace period)")
                else:
                    reporter.trace_startup_compliance(
                        agent_role="system",
                        files_read=[],
                        files_missing=[],
                        audit_passed=True,
                    )
                _gateway_start_time = None

            entries_processed += 1
            agent_role = entry.get("agent_role", "unknown")
            _metric_counters[agent_role] = _metric_counters.get(agent_role, 0) + 1

            exec_time = entry.get("execution_time_ms")
            if exec_time is not None:
                try:
                    _latency_sum += float(exec_time)
                    _latency_count += 1
                except (ValueError, TypeError):
                    pass

            if dry_run:
                logger.info(
                    "[DRY-RUN] trace #%d  agent=%s  tool=%s  outcome=%s",
                    entries_processed,
                    agent_role,
                    entry.get("tool_name", "-"),
                    entry.get("outcome", "-"),
                )
            else:
                reporter.trace_request(entry)

            if alert_evaluator is not None:
                fired = alert_evaluator.check_realtime(entry)
                for alert in fired:
                    if dry_run:
                        logger.info("[DRY-RUN] alert forwarded: %s [%s]", alert.alert_id, alert.severity)
                    else:
                        reporter.trace_alert(alert.alert_id, alert.severity, alert.description)

            if entries_processed % 100 == 0:
                if not dry_run:
                    for role, count in _metric_counters.items():
                        reporter.trace_metric("agent_request_count", float(count), {"agent_role": role})
                    if _latency_count > 0:
                        reporter.trace_metric(
                            "agent_latency_avg_ms",
                            _latency_sum / _latency_count,
                            {"sample_count": _latency_count},
                        )
                    reporter.flush()
                logger.debug("Processed %d entries", entries_processed)

    except KeyboardInterrupt:
        logger.info("Shutting down (processed %d entries)", entries_processed)
    finally:
        if not dry_run:
            reporter.flush()
        logger.info("Final flush complete (%d entries total)", entries_processed)


if __name__ == "__main__":
    main()
