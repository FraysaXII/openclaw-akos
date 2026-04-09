#!/usr/bin/env python3
"""Tail the OpenCLAW gateway log and push traces to Langfuse.

Parses JSON log entries from the gateway, pushes agent activity to
Langfuse for tracing/evaluation, and evaluates real-time alerts.

Usage:
    python scripts/log-watcher.py                 # foreground watcher
    python scripts/log-watcher.py --once           # single pass (CI/test)
    python scripts/log-watcher.py --json-log       # structured JSON output

Environment:
    LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY  (from process env or ~/.openclaw/.env)
    LOG_WATCHER_POLL_INTERVAL                 (derived from diagnostics.logWatcher or env override)

Requires: Python 3.10+, langfuse (optional for telemetry).
"""

import argparse
import json
import logging
import os
import re
import sys
import tempfile
import time
from collections.abc import Iterator
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.alerts import AlertEvaluator
from akos.io import (
    REPO_ROOT,
    get_log_watcher_settings,
    load_json,
    load_runtime_env,
    resolve_openclaw_home,
    set_process_env_defaults,
)
from akos.intent import classify_request
from akos.log import setup_logging
from akos.models import RunPodEndpointConfig
from akos.runpod_provider import RunPodProvider
from akos.telemetry import LangfuseReporter

logger = logging.getLogger("akos.log-watcher")

_CANONICAL_ASSET_RE = re.compile(
    r"\b(baseline_organisation\.csv|process_list\.csv|access_levels\.md|confidence_levels\.md|source_taxonomy\.md|PRECEDENCE\.md)\b",
    re.IGNORECASE,
)
_INTERNAL_TOOL_LEAK_RE = re.compile(
    r"\b(hlk_[a-z_]+|finance_(?:search|quote|sentiment)|best_role|best_process)\b"
)
# User-visible pseudo-paths (tool ladder leakage), linear-time bounded slice in caller.
_PSEUDO_HLK_PATH_RE = re.compile(
    r"hlk_(?:role|process|area|search|process_tree)(?:/|:)",
    re.IGNORECASE,
)
_STD_UUID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)

_ASSISTANT_SCAN_MAX = 8000


def _assistant_scan_slice(text: str) -> str:
    if len(text) <= _ASSISTANT_SCAN_MAX:
        return text
    return text[:_ASSISTANT_SCAN_MAX]

def _parse_session_line(line: str) -> dict | None:
    """Parse a session jsonl line, returning None on failure."""
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def _extract_text_content(blocks: list[dict]) -> str:
    """Join text content blocks from a session message payload."""
    parts = [
        str(block.get("text", ""))
        for block in blocks
        if isinstance(block, dict) and block.get("type") == "text"
    ]
    return "\n".join(part for part in parts if part).strip()


def _parse_tool_result_payload(content_blocks: list[dict]) -> dict | str | None:
    """Parse a toolResult text payload when it contains JSON."""
    for block in content_blocks:
        if not isinstance(block, dict) or block.get("type") != "text":
            continue
        raw = str(block.get("text", "")).strip()
        if not raw:
            continue
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    return None


def _resolve_local_mirror_dir(settings: dict, oc_home: Path) -> Path:
    """Resolve the configured local telemetry mirror directory."""
    raw = str(settings.get("localMirrorDirectory", "~/.openclaw/telemetry")).strip()
    if raw.startswith("~/.openclaw"):
        suffix = raw[len("~/.openclaw"):].lstrip("/\\")
        return oc_home / suffix
    return Path(raw).expanduser()


def _classify_route_kind(user_text: str, tool_calls: list[str]) -> str:
    """Classify the route taken for one user-visible answer."""
    if any(name.startswith("finance_") for name in tool_calls):
        return "finance"
    routed = str(classify_request(user_text).get("route", "other"))
    if routed == "admin_escalate":
        return "admin"
    if routed == "execution_escalate":
        return "execution"
    if routed == "finance_research":
        return "finance"
    if routed == "hlk_search":
        return "hlk_search_explicit"
    if routed == "hlk_lookup":
        return "hlk_direct_lookup"
    lowered = user_text.lower()
    if "hlk_search" in tool_calls:
        if "search" in lowered or "find" in lowered:
            return "hlk_search_explicit"
        return "hlk_search_fallback"
    if any(name.startswith("hlk_") for name in tool_calls):
        return "hlk_direct_lookup"
    return "non_tool_answer"


def _build_answer_quality_record(interaction: dict, assistant_message: dict) -> dict:
    """Build one answer-quality record from a completed session interaction."""
    content = assistant_message.get("content", [])
    assistant_text = _extract_text_content(content if isinstance(content, list) else [])
    tool_calls = [str(name) for name in interaction.get("tool_calls", [])]
    route_kind = _classify_route_kind(str(interaction.get("user_text", "")), tool_calls)
    scan_slice = _assistant_scan_slice(assistant_text)
    citation_match = _CANONICAL_ASSET_RE.search(assistant_text)
    citation_asset = citation_match.group(1) if citation_match else ""
    internal_leak = bool(_INTERNAL_TOOL_LEAK_RE.search(scan_slice))
    pseudo_path_leak = bool(_PSEUDO_HLK_PATH_RE.search(scan_slice))
    hlk_tools_used = any(name.startswith("hlk_") for name in tool_calls)
    uuid_in_answer = bool(_STD_UUID_RE.search(scan_slice))
    escalation_present = "orchestrator" in assistant_text.lower() or "escalat" in assistant_text.lower()
    brainstorm_drift = route_kind == "admin" and (
        "would you like to" in assistant_text.lower()
        or "please specify" in assistant_text.lower()
        or "merge/split" in assistant_text.lower()
    )
    compaction_interference = bool(interaction.get("post_compaction")) and (
        "memory/" in assistant_text.lower()
        or "workflow_auto" in assistant_text.lower()
        or "post-compaction" in assistant_text.lower()
    )

    best_match_present = False
    degraded_status = ""
    for payload in interaction.get("tool_results", []):
        if isinstance(payload, dict):
            if payload.get("best_role") or payload.get("best_process"):
                best_match_present = True
            status = str(payload.get("status", "")).strip()
            if status and status != "ok":
                degraded_status = status

    residual_flags: list[str] = []
    if internal_leak:
        residual_flags.append("internal_tool_leak")
    if pseudo_path_leak:
        residual_flags.append("pseudo_hlk_path_leak")
    if (
        uuid_in_answer
        and route_kind.startswith("hlk_")
        and not hlk_tools_used
    ):
        residual_flags.append("suspect_hlk_uuid_hallucination")
    if route_kind.startswith("hlk_") and not citation_asset:
        residual_flags.append("missing_citation_asset")
    if route_kind in ("admin", "execution") and not escalation_present:
        residual_flags.append("missing_explicit_escalation")
    if brainstorm_drift:
        residual_flags.append("admin_brainstorm_drift")
    if compaction_interference:
        residual_flags.append("compaction_interference")
    if degraded_status:
        residual_flags.append(f"tool_status_{degraded_status}")
    if route_kind == "non_tool_answer":
        residual_flags.append("non_tool_answer")

    quality_score = 1.0 if not residual_flags else 0.4
    return {
        "agent_role": interaction.get("agent_role", "unknown"),
        "session_id": interaction.get("session_id", ""),
        "user_text": interaction.get("user_text", ""),
        "assistant_text": assistant_text,
        "tool_calls": tool_calls,
        "tool_backed": bool(tool_calls),
        "route_kind": route_kind,
        "citation_asset": citation_asset,
        "best_match_present": best_match_present,
        "escalation_present": escalation_present,
        "compaction_interference": compaction_interference,
        "residual_flags": residual_flags,
        "quality_score": quality_score,
        "provider": assistant_message.get("provider", ""),
        "model": assistant_message.get("model", ""),
    }


def _append_local_mirror_record(mirror_dir: Path, record: dict) -> Path:
    """Append one telemetry record to the local mirror jsonl."""
    mirror_dir.mkdir(parents=True, exist_ok=True)
    mirror_path = mirror_dir / f"madeira-answer-quality-{date.today().isoformat()}.jsonl"
    with open(mirror_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return mirror_path


def _emit_answer_quality_alerts(
    record: dict,
    alert_evaluator: AlertEvaluator | None,
    reporter: LangfuseReporter,
    dry_run: bool,
) -> None:
    """Evaluate Madeira answer-quality rows against real-time eval alerts."""
    if alert_evaluator is None:
        return
    flags = record.get("residual_flags") or []
    if not flags:
        return
    eval_entry = {
        "agent_role": str(record.get("agent_role", "madeira")),
        "tool_name": "answer_quality",
        "outcome": "madeira_answer_quality",
        "residual_flags": ",".join(str(f) for f in flags),
        "route_kind": str(record.get("route_kind", "")),
    }
    for alert in alert_evaluator.check_realtime(eval_entry):
        if dry_run:
            logger.info("[DRY-RUN] answer-quality alert: %s [%s]", alert.alert_id, alert.severity)
        else:
            reporter.trace_alert(alert.alert_id, alert.severity, alert.description)


def _process_session_event(
    event: dict,
    session_key_map: dict[str, str],
    interaction_state: dict[str, dict],
    mirror_dir: Path,
    reporter: LangfuseReporter,
    dry_run: bool,
    session_id: str,
    alert_evaluator: AlertEvaluator | None = None,
) -> None:
    """Process one session json event and emit answer-quality telemetry when complete."""
    if event.get("type") != "message":
        return
    message = event.get("message", {})
    if not isinstance(message, dict):
        return
    role = message.get("role")
    event_id = str(event.get("id", ""))
    parent_id = str(event.get("parentId", ""))
    content = message.get("content", [])
    if role == "user":
        interaction_key = event_id
        session_key_map[event_id] = interaction_key
        interaction_state[interaction_key] = {
            "session_id": session_id,
            "agent_role": "madeira",
            "user_text": _extract_text_content(content if isinstance(content, list) else []),
            "tool_calls": [],
            "tool_results": [],
            "post_compaction": "post-compaction audit" in _extract_text_content(content if isinstance(content, list) else []).lower(),
        }
        return

    interaction_key = session_key_map.get(parent_id)
    if interaction_key is None:
        return
    session_key_map[event_id] = interaction_key

    if role == "assistant":
        if isinstance(content, list) and any(block.get("type") == "toolCall" for block in content if isinstance(block, dict)):
            interaction = interaction_state.get(interaction_key)
            if interaction is None:
                return
            interaction["tool_calls"].extend(
                str(block.get("name", ""))
                for block in content
                if isinstance(block, dict) and block.get("type") == "toolCall"
            )
            return

        interaction = interaction_state.pop(interaction_key, None)
        if interaction is None:
            return
        record = _build_answer_quality_record(interaction, message)
        mirror_path = _append_local_mirror_record(mirror_dir, record)
        record["local_mirror_path"] = str(mirror_path)
        if dry_run:
            logger.info("[DRY-RUN] answer-quality: route=%s flags=%s", record["route_kind"], record["residual_flags"])
        else:
            reporter.trace_answer_quality(record)
        _emit_answer_quality_alerts(record, alert_evaluator, reporter, dry_run)
        return

    if role == "toolResult":
        interaction = interaction_state.get(interaction_key)
        if interaction is None:
            return
        payload = _parse_tool_result_payload(content if isinstance(content, list) else [])
        interaction["tool_results"].append(payload)


def _scan_madeira_sessions(
    oc_home: Path,
    offsets: dict[Path, int],
    session_key_maps: dict[Path, dict[str, str]],
    interaction_state: dict[str, dict],
    mirror_dir: Path,
    reporter: LangfuseReporter,
    dry_run: bool,
    alert_evaluator: AlertEvaluator | None = None,
) -> None:
    """Scan Madeira session jsonl files and emit answer-quality telemetry."""
    sessions_dir = oc_home / "agents" / "madeira" / "sessions"
    if not sessions_dir.is_dir():
        return

    for session_file in sorted(sessions_dir.glob("*.jsonl")):
        last_offset = offsets.get(session_file, 0)
        session_map = session_key_maps.setdefault(session_file, {})
        with open(session_file, "r", encoding="utf-8", errors="replace") as f:
            f.seek(last_offset)
            for line in f:
                event = _parse_session_line(line)
                if event is None:
                    continue
                _process_session_event(
                    event,
                    session_map,
                    interaction_state,
                    mirror_dir,
                    reporter,
                    dry_run,
                    session_file.stem,
                    alert_evaluator,
                )
            offsets[session_file] = f.tell()


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
                yield ""


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
    parser = argparse.ArgumentParser(description="OpenCLAW log watcher + Langfuse telemetry")
    parser.add_argument("--once", action="store_true", help="Single pass then exit (for CI/tests)")
    parser.add_argument("--json-log", action="store_true", help="Structured JSON log output")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be sent to Langfuse without calling the SDK")
    parser.add_argument("--environment", "-e",
                        default=os.environ.get("AKOS_ENV", "dev-local"),
                        help="Environment tag for traces (dev-local, gpu-runpod, prod-cloud)")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    oc_home = resolve_openclaw_home()
    set_process_env_defaults(load_runtime_env(oc_home))
    env_tag = os.environ.get("AKOS_ENV", args.environment)

    watcher_settings = get_log_watcher_settings(oc_home)
    poll_interval = float(
        os.environ.get(
            "LOG_WATCHER_POLL_INTERVAL",
            str(watcher_settings.get("pollIntervalSeconds", 2)),
        )
    )
    mirror_dir = _resolve_local_mirror_dir(watcher_settings, oc_home)
    tracked_session_offsets: dict[Path, int] = {}
    session_key_maps: dict[Path, dict[str, str]] = {}
    interaction_state: dict[str, dict] = {}
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
            _scan_madeira_sessions(
                oc_home,
                tracked_session_offsets,
                session_key_maps,
                interaction_state,
                mirror_dir,
                reporter,
                dry_run,
                alert_evaluator,
            )
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
        _scan_madeira_sessions(
            oc_home,
            tracked_session_offsets,
            session_key_maps,
            interaction_state,
            mirror_dir,
            reporter,
            dry_run,
            alert_evaluator,
        )
        if not dry_run:
            reporter.shutdown()
        logger.info("Final shutdown complete (%d entries total)", entries_processed)


if __name__ == "__main__":
    main()
