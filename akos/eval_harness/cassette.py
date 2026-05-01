"""Initiative 45 P2 — Cassette format + record/replay I/O.

Cassette = JSONL file capturing one probe trajectory for one skill. Lives at
``tests/evals/cassettes/<skill_id>/<probe_id>.jsonl``.

Format (one JSON object per line):
- Line 1 (header):   {"event": "header", schema_version, skill_id, probe_id,
                      probe_kind, recorded_at, recorded_by, model_id, model_tier,
                      golden_assertion: {...}, last_recorded}
- Lines 2..N-1:      one of {"event": "prompt"|"tool_call"|"tool_response"|"final"}
- Line N (summary):  {"event": "summary", status, tokens_in, tokens_out,
                      latency_ms}

Two recording paths:
1. ``probe_kind="classify_request"`` (default; deterministic, no LLM):
   - Records the classify_request output for a given prompt.
   - Replay re-runs classify_request and asserts route matches.
2. ``probe_kind="live_llm"`` (P6 territory; requires AKOS_RECORD_LIVE=1):
   - Records actual LLM trajectory.
   - Replay does NOT re-call the LLM; asserts the recorded final response
     against the golden_assertion (substring rubric, similar to I10 score_rubric_task).

Staleness: header carries ``last_recorded``. Replay warns at 60 days, fails at
90 days unless ``--allow-stale`` passed (mirrors LiveBench-style awareness from
``tests/evals/README.md``).
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

logger = logging.getLogger("akos.eval.cassette")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CASSETTE_ROOT = REPO_ROOT / "tests" / "evals" / "cassettes"

CASSETTE_SCHEMA_VERSION = "1.0"
STALENESS_WARN_DAYS = 60
STALENESS_FAIL_DAYS = 90


@dataclass
class CassetteHeader:
    schema_version: str
    skill_id: str
    probe_id: str
    probe_kind: str  # "classify_request" or "live_llm"
    recorded_at: str  # ISO-8601 UTC
    recorded_by: str  # operator handle
    model_id: str  # "deterministic" for classify_request; e.g., "anthropic:claude-3.5-sonnet" for live
    model_tier: str  # "deterministic" / "cheap" / "flagship"
    golden_assertion: dict[str, Any]  # for classify_request: {"route": "<expected>"}; for live_llm: rubric dict
    last_recorded: str  # convenience copy of recorded_at for staleness checks


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cassette_path(skill_id: str, probe_id: str, *, root: Path | None = None) -> Path:
    base = root or CASSETTE_ROOT
    return base / skill_id / f"{probe_id}.jsonl"


def list_cassettes(*, skill_id: str | None = None, root: Path | None = None) -> list[Path]:
    base = root or CASSETTE_ROOT
    if not base.is_dir():
        return []
    if skill_id:
        sub = base / skill_id
        if not sub.is_dir():
            return []
        return sorted(sub.glob("*.jsonl"))
    return sorted(p for p in base.glob("*/*.jsonl") if p.parent.name != "adversarial")


def adversarial_cassettes(*, skill_id: str | None = None, root: Path | None = None) -> list[Path]:
    """Adversarial cassettes live under <root>/adversarial/<skill_id>/. Listed separately."""
    base = (root or CASSETTE_ROOT) / "adversarial"
    if not base.is_dir():
        return []
    if skill_id:
        sub = base / skill_id
        if not sub.is_dir():
            return []
        return sorted(sub.glob("*.jsonl"))
    return sorted(base.glob("*/*.jsonl"))


def write_cassette(path: Path, header: CassetteHeader, events: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write(json.dumps({"event": "header", **header.__dict__}, sort_keys=True) + "\n")
        for ev in events:
            fh.write(json.dumps(ev, sort_keys=True) + "\n")
        fh.write(json.dumps({"event": "summary", **summary}, sort_keys=True) + "\n")


def read_cassette(path: Path) -> tuple[CassetteHeader, list[dict[str, Any]], dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(f"Cassette not found: {path}")
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    if len(lines) < 2:
        raise ValueError(f"Cassette malformed (need header + summary): {path}")
    header_obj = json.loads(lines[0])
    if header_obj.get("event") != "header":
        raise ValueError(f"Cassette missing header event: {path}")
    summary_obj = json.loads(lines[-1])
    if summary_obj.get("event") != "summary":
        raise ValueError(f"Cassette missing summary event: {path}")
    events = [json.loads(line) for line in lines[1:-1]]

    header_obj.pop("event", None)
    summary_obj.pop("event", None)
    header = CassetteHeader(**{k: v for k, v in header_obj.items() if k in CassetteHeader.__dataclass_fields__})
    return header, events, summary_obj


def staleness_status(header: CassetteHeader, *, now: datetime | None = None) -> tuple[str, int]:
    """Return ('fresh'|'warn'|'fail', age_days) per the 60/90 day policy."""
    n = now or datetime.now(timezone.utc)
    try:
        recorded = datetime.fromisoformat(header.last_recorded.replace("Z", "+00:00"))
    except Exception:
        return ("fail", 999)
    age = (n - recorded).days
    if age >= STALENESS_FAIL_DAYS:
        return ("fail", age)
    if age >= STALENESS_WARN_DAYS:
        return ("warn", age)
    return ("fresh", age)


def replay_classify_request_cassette(path: Path) -> dict[str, Any]:
    """Re-run classify_request for the recorded prompt; assert route matches.

    Returns: dict with status (PASS|FAIL|WARN), failures, age_days, expected_route, actual_route.
    """
    header, events, _summary = read_cassette(path)
    if header.probe_kind != "classify_request":
        return {
            "status": "SKIP",
            "failures": [f"unsupported probe_kind for classify replay: {header.probe_kind}"],
            "age_days": 0,
        }

    prompt_event = next((e for e in events if e.get("event") == "prompt"), None)
    if not prompt_event or "text" not in prompt_event:
        return {"status": "FAIL", "failures": ["missing prompt event"], "age_days": 0}

    expected_route = header.golden_assertion.get("route")

    from akos.intent import classify_request

    result = classify_request(prompt_event["text"])
    actual_route = result.get("route", "")

    failures: list[str] = []
    if expected_route and actual_route != expected_route:
        failures.append(f"route_mismatch:expected={expected_route},actual={actual_route}")

    stale, age_days = staleness_status(header)
    if stale == "fail":
        failures.append(f"cassette_stale:{age_days}d>={STALENESS_FAIL_DAYS}d")

    status = "PASS" if not failures else ("WARN" if stale == "warn" and len(failures) == 1 else "FAIL")
    return {
        "status": status,
        "failures": failures,
        "age_days": age_days,
        "expected_route": expected_route,
        "actual_route": actual_route,
        "stale": stale,
    }


def record_classify_request_cassette(
    *,
    skill_id: str,
    probe_id: str,
    prompt: str,
    recorded_by: str = "operator",
    root: Path | None = None,
) -> Path:
    """Capture a deterministic classify_request cassette. No LLM call required.

    Used for routing-layer cassettes that exercise intent.py without live LLM cost.
    Safe to run without AKOS_RECORD_LIVE=1.
    """
    from akos.intent import classify_request

    t0 = time.perf_counter()
    result = classify_request(prompt)
    elapsed = int((time.perf_counter() - t0) * 1000)
    route = result.get("route", "")

    header = CassetteHeader(
        schema_version=CASSETTE_SCHEMA_VERSION,
        skill_id=skill_id,
        probe_id=probe_id,
        probe_kind="classify_request",
        recorded_at=_utc_iso(),
        recorded_by=recorded_by,
        model_id="deterministic:akos.intent.classify_request",
        model_tier="deterministic",
        golden_assertion={"route": route},
        last_recorded=_utc_iso(),
    )
    events = [
        {"event": "prompt", "text": prompt},
        {
            "event": "final",
            "route": route,
            "confidence": result.get("confidence"),
            "method": result.get("method"),
            "must_escalate": result.get("must_escalate"),
            "reason": result.get("reason"),
        },
    ]
    summary = {"status": "PASS", "tokens_in": 0, "tokens_out": 0, "latency_ms": elapsed}

    path = cassette_path(skill_id, probe_id, root=root)
    write_cassette(path, header, events, summary)
    try:
        rel = path.relative_to(REPO_ROOT)
    except ValueError:
        rel = path
    logger.info("recorded cassette: %s -> route=%s", rel, route)
    return path


def record_live_llm_cassette(
    *,
    skill_id: str,
    probe_id: str,
    prompt: str,
    recorded_by: str,
    model_id: str,
    model_tier: str,
    golden_rubric: dict[str, Any],
    root: Path | None = None,
) -> Path:
    """Capture a live LLM trajectory. P6 territory; requires AKOS_RECORD_LIVE=1.

    P2 ships this as a stub: it raises if AKOS_RECORD_LIVE is unset; otherwise it
    captures the prompt + golden rubric without actually calling an LLM (placeholder
    summary). P6 implementation will replace the stub with real LLM invocation +
    Langfuse scrape + tokens_in/out/latency capture.
    """
    if os.environ.get("AKOS_RECORD_LIVE", "") != "1":
        raise PermissionError(
            "live cassette recording requires AKOS_RECORD_LIVE=1 (cost-control guard)"
        )

    header = CassetteHeader(
        schema_version=CASSETTE_SCHEMA_VERSION,
        skill_id=skill_id,
        probe_id=probe_id,
        probe_kind="live_llm",
        recorded_at=_utc_iso(),
        recorded_by=recorded_by,
        model_id=model_id,
        model_tier=model_tier,
        golden_assertion=golden_rubric,
        last_recorded=_utc_iso(),
    )
    events = [
        {"event": "prompt", "text": prompt},
        {"event": "final", "text": "<P6-stub: real LLM call lands in P6>"},
    ]
    summary = {"status": "SKIP", "tokens_in": 0, "tokens_out": 0, "latency_ms": 0, "note": "P6 stub"}

    path = cassette_path(skill_id, probe_id, root=root)
    write_cassette(path, header, events, summary)
    try:
        rel = path.relative_to(REPO_ROOT)
    except ValueError:
        rel = path
    logger.info("recorded LIVE cassette stub (P6 will fill in): %s", rel)
    return path


def replay_live_llm_cassette(path: Path) -> dict[str, Any]:
    """Replay a live_llm cassette by checking the recorded final text against golden_rubric.

    Does NOT re-call the LLM. The whole point of cassettes is to make replay cost-free.
    """
    header, events, _summary = read_cassette(path)
    if header.probe_kind != "live_llm":
        return {
            "status": "SKIP",
            "failures": [f"unsupported probe_kind for live replay: {header.probe_kind}"],
            "age_days": 0,
        }

    final_event = next((e for e in events if e.get("event") == "final"), None)
    if not final_event:
        return {"status": "FAIL", "failures": ["missing final event"], "age_days": 0}

    text = str(final_event.get("text", ""))
    rubric = header.golden_assertion or {}

    failures: list[str] = []
    for needle in rubric.get("contains", []) or []:
        if str(needle) not in text:
            failures.append(f"missing_contains:{needle}")
    for bad in rubric.get("forbidden", []) or []:
        if str(bad) in text:
            failures.append(f"forbidden_present:{bad}")

    stale, age_days = staleness_status(header)
    if stale == "fail":
        failures.append(f"cassette_stale:{age_days}d>={STALENESS_FAIL_DAYS}d")

    status = "PASS" if not failures else ("WARN" if stale == "warn" and len(failures) == 1 else "FAIL")
    return {
        "status": status,
        "failures": failures,
        "age_days": age_days,
        "stale": stale,
        "rubric_matched": not failures,
    }


def replay_cassette(path: Path) -> dict[str, Any]:
    """Dispatch to the right replay path based on cassette probe_kind."""
    header, _events, _summary = read_cassette(path)
    if header.probe_kind == "classify_request":
        return replay_classify_request_cassette(path)
    if header.probe_kind == "live_llm":
        return replay_live_llm_cassette(path)
    if header.probe_kind == "adversarial_classify_request":
        # P5: import here to avoid circular dependency at module load time
        from akos.eval_harness.adversarial import (
            replay_adversarial_classify_request_cassette,
        )
        return replay_adversarial_classify_request_cassette(path)
    return {"status": "SKIP", "failures": [f"unknown probe_kind: {header.probe_kind}"], "age_days": 0}
