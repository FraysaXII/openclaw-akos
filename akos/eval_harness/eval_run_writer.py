"""Write Scorecard rows to ``compliance.eval_run`` (Initiative 47 P13 item 4).

Best-effort: silently no-ops when ``SUPABASE_URL`` / ``SUPABASE_SERVICE_ROLE_KEY``
env vars are missing. Uses stdlib ``urllib.request`` so we don't pin a new
dependency. Each invocation appends one row per ``ScoreRow`` to the
``compliance.eval_run`` mirror table (BIGSERIAL id; INSERTs are append-only;
UPDATE/DELETE blocked by RLS).

Per the I45 P4 + I47 P10 schema: rows carry ``run_id`` (operator-correlation),
``mode`` / ``skill_id`` / ``status`` / ``current_pct`` / ``baseline_pct`` /
``delta_pp`` / ``cost_usd`` / ``latency_ms_p50/p95`` / ``failures`` / ``notes``,
plus the I47 P10 extension fields ``persona_id`` / ``difficulty_class`` /
``scenario_class`` / ``judge_scores`` (JSONB).

## Activation

The writer activates ONLY when both ``SUPABASE_URL`` AND
``SUPABASE_SERVICE_ROLE_KEY`` are set. This is the standard service-role
posture for I26-vintage write paths. The writer is invoked by ``scripts/eval.py``
after every successful ``run_modes()`` call.

For Tier B GitHub Action runs, the secrets are operator-managed (per I45 P6).

## Failure mode

HTTP failures are logged at WARNING level but do NOT raise — the eval run
itself remains the primary surface; observability writes are advisory.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
import uuid
from dataclasses import asdict
from typing import Any

logger = logging.getLogger("akos.eval_harness.eval_run_writer")

EVAL_RUN_PATH = "/rest/v1/eval_run"
COMPLIANCE_SCHEMA = "compliance"


def _resolve_endpoint() -> tuple[str, str] | None:
    """Return (url, service_role_key) when both are present, else None."""
    url = (os.environ.get("SUPABASE_URL") or "").rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or ""
    if not url or not key:
        return None
    return url, key


def _row_to_payload(row: Any, run_id: str, source_git_sha: str) -> dict[str, Any]:
    """Convert a ScoreRow into a JSON-serialisable INSERT payload.

    Handles both dataclass instances (with ``__dataclass_fields__``) and
    duck-typed objects with the same attributes.
    """
    if hasattr(row, "__dataclass_fields__"):
        d = asdict(row)
    else:
        d = {
            attr: getattr(row, attr, None)
            for attr in (
                "mode", "skill_id", "name", "status",
                "baseline_pct", "current_pct", "delta_pp",
                "cost_usd", "latency_ms_p50", "latency_ms_p95",
                "failures", "notes",
                "persona_id", "difficulty_class", "scenario_class", "judge_scores",
            )
        }

    return {
        "run_id": run_id,
        "schema_version": "1.0",
        "mode": d.get("mode") or "unknown",
        "skill_id": d.get("skill_id") or "__unknown__",
        "status": d.get("status") or "PASS",
        "current_pct": d.get("current_pct"),
        "baseline_pct": d.get("baseline_pct"),
        "delta_pp": d.get("delta_pp"),
        "cost_usd": d.get("cost_usd"),
        "latency_ms_p50": d.get("latency_ms_p50"),
        "latency_ms_p95": d.get("latency_ms_p95"),
        "failures": "; ".join(d.get("failures") or []) if isinstance(d.get("failures"), list) else d.get("failures"),
        "notes": d.get("notes") or "",
        "source_git_sha": source_git_sha,
        # I47 P10 extension columns (defaults to None for old rows)
        "persona_id": d.get("persona_id"),
        "difficulty_class": d.get("difficulty_class"),
        "scenario_class": d.get("scenario_class"),
        # I47 P12: JSONB column; pass dict not string
        "judge_scores": d.get("judge_scores") or None,
    }


def write_scorecard_rows(
    scorecard: Any,
    *,
    run_id: str | None = None,
    source_git_sha: str = "unknown",
    timeout: float = 5.0,
) -> dict[str, int]:
    """Write Scorecard.rows to compliance.eval_run.

    Returns ``{written: N, skipped: M, errors: K}``.
    Skipped means env vars missing (writer disabled by config).
    """
    endpoint = _resolve_endpoint()
    if endpoint is None:
        logger.debug("eval_run_writer: SUPABASE_URL/KEY not set; skipping live writes")
        return {"written": 0, "skipped": len(scorecard.rows), "errors": 0}

    url, key = endpoint
    rid = run_id or f"run-{uuid.uuid4().hex[:12]}"
    payloads = [_row_to_payload(r, rid, source_git_sha) for r in scorecard.rows]
    body = json.dumps(payloads).encode("utf-8")

    req = urllib.request.Request(
        url + EVAL_RUN_PATH,
        data=body,
        method="POST",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept-Profile": COMPLIANCE_SCHEMA,
            "Content-Profile": COMPLIANCE_SCHEMA,
            "Prefer": "return=minimal",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if 200 <= resp.status < 300:
                logger.info("eval_run_writer: wrote %d rows (run_id=%s)", len(payloads), rid)
                return {"written": len(payloads), "skipped": 0, "errors": 0}
            logger.warning("eval_run_writer: unexpected status %d", resp.status)
            return {"written": 0, "skipped": 0, "errors": len(payloads)}
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")[:500]
        logger.warning("eval_run_writer: HTTPError %d: %s", exc.code, body_text)
        return {"written": 0, "skipped": 0, "errors": len(payloads)}
    except (OSError, urllib.error.URLError) as exc:
        logger.warning("eval_run_writer: network error: %s", exc)
        return {"written": 0, "skipped": 0, "errors": len(payloads)}
