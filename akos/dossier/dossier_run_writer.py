"""Append dossier runs to ``compliance.dossier_run`` + local index (Initiative 48 P7).

Best-effort Supabase INSERT via stdlib urllib (same posture as ``eval_run_writer``).
Always appends a summary row to ``artifacts/uat-dossier/index.json`` for offline
sparklines when the mirror is empty or unreachable.

Roll-up metrics (4 sparkline series) are derived from ``section_metrics`` keys
``section_03``, ``section_04``, ``section_07`` plus cost from section 03.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

logger = logging.getLogger("akos.dossier.dossier_run_writer")

DOSSIER_RUN_PATH = "/rest/v1/dossier_run"
COMPLIANCE_SCHEMA = "compliance"
INDEX_VERSION = 1
MAX_LOCAL_RUNS = 1000

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOCAL_INDEX_PATH = REPO_ROOT / "artifacts" / "uat-dossier" / "index.json"


def _endpoint() -> tuple[str, str] | None:
    url = (os.environ.get("SUPABASE_URL") or "").rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or ""
    if not url or not key:
        return None
    return url, key


def compute_rollup_from_section_metrics(section_metrics: dict[str, Any]) -> dict[str, float | int]:
    """Derive the four P7 trend scalars from manifest ``section_metrics``."""

    def _metrics(section_key: str) -> dict[str, Any]:
        block = section_metrics.get(section_key) or {}
        m = block.get("metrics")
        return m if isinstance(m, dict) else {}

    m3 = _metrics("section_03")
    rt = max(int(m3.get("rows_total") or 0), 1)
    rp = int(m3.get("rows_passed") or 0)
    eval_pass_rate = rp / rt

    m4 = _metrics("section_04")
    cal_ok = 1.0 if m4.get("overall_within_tolerance") else 0.0

    m7 = _metrics("section_07")
    drift_total = int(m7.get("drift_canary_total_drift") or 0)

    cost = float(m3.get("cost_total_usd") or 0.0)

    return {
        "eval_pass_rate": round(float(eval_pass_rate), 6),
        "calibration_ok": float(cal_ok),
        "drift_canary_total": drift_total,
        "cost_total_usd": round(cost, 6),
    }


def compute_rollup_from_section_results(section_results: list[Any]) -> dict[str, float | int]:
    """Build minimal section_metrics-like dict from ``DossierSectionResult`` rows."""

    fake_metrics: dict[str, Any] = {}
    for r in section_results:
        sid = f"section_{int(r.section_id):02d}"
        fake_metrics[sid] = {"metrics": dict(r.metrics or {})}
    return compute_rollup_from_section_metrics(fake_metrics)


def append_local_dossier_index(
    *,
    run_id: str,
    started_at: str,
    mode: str,
    git_sha: str,
    manifest_sha256: str,
    rollup: dict[str, float | int],
) -> None:
    """Append one entry to ``artifacts/uat-dossier/index.json`` (trim to MAX_LOCAL_RUNS)."""

    LOCAL_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, Any]
    if LOCAL_INDEX_PATH.is_file():
        try:
            data = json.loads(LOCAL_INDEX_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {"version": INDEX_VERSION, "runs": []}
    else:
        data = {"version": INDEX_VERSION, "runs": []}

    runs = data.setdefault("runs", [])
    runs.append(
        {
            "run_id": run_id,
            "started_at": started_at,
            "mode": mode,
            "git_sha": git_sha,
            "manifest_sha256": manifest_sha256,
            "rollup": rollup,
        }
    )
    if len(runs) > MAX_LOCAL_RUNS:
        del runs[: len(runs) - MAX_LOCAL_RUNS]
    LOCAL_INDEX_PATH.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def write_dossier_run_row(
    *,
    run_id: str,
    started_at: str,
    mode: str,
    git_sha: str,
    section_metrics: dict[str, Any],
    manifest_sha256: str,
    timeout: float = 8.0,
) -> dict[str, int]:
    """INSERT one row into compliance.dossier_run. Returns written/skipped/errors counts."""

    endpoint = _endpoint()
    rollup = compute_rollup_from_section_metrics(section_metrics)
    append_local_dossier_index(
        run_id=run_id,
        started_at=started_at,
        mode=mode,
        git_sha=git_sha,
        manifest_sha256=manifest_sha256,
        rollup=rollup,
    )

    if endpoint is None:
        logger.debug("dossier_run_writer: SUPABASE_URL/KEY not set; local index only")
        return {"written": 0, "skipped": 1, "errors": 0}

    url, key = endpoint
    payload = {
        "run_id": run_id,
        "started_at": started_at,
        "mode": mode,
        "git_sha": git_sha,
        "section_metrics": section_metrics,
        "manifest_sha256": manifest_sha256,
    }
    body = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url + DOSSIER_RUN_PATH,
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
                logger.info("dossier_run_writer: wrote row run_id=%s", run_id)
                return {"written": 1, "skipped": 0, "errors": 0}
            logger.warning("dossier_run_writer: unexpected status %d", resp.status)
            return {"written": 0, "skipped": 0, "errors": 1}
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")[:500]
        logger.warning("dossier_run_writer: HTTPError %d: %s", exc.code, body_text)
        return {"written": 0, "skipped": 0, "errors": 1}
    except (OSError, urllib.error.URLError) as exc:
        logger.warning("dossier_run_writer: network error: %s", exc)
        return {"written": 0, "skipped": 0, "errors": 1}
