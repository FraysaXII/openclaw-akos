#!/usr/bin/env python3
"""Initiative 49 P11 — telemetry to PERSONA_SCENARIO_REGISTRY proposal emitter.

Reads recent ``~/.openclaw/telemetry/madeira-answer-quality-*.jsonl`` records
emitted by ``scripts/log-watcher.py`` and groups them by failure pattern
(``route_kind`` x dominant ``residual_flags``) into deterministic JSON
**proposals**. Operator review remains the merge gate; this script never
mutates ``PERSONA_SCENARIO_REGISTRY.csv``.

Per ``SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md`` §5.4 (telemetry promotion),
proposals carry suggested registry-row fields plus rationale. The operator
applies them via the standard `sync_compliance_mirrors_from_csv.py` path
after manual CSV edits.

Usage::

    py scripts/promote_telemetry_to_scenario.py
    py scripts/promote_telemetry_to_scenario.py --since-days 7
    py scripts/promote_telemetry_to_scenario.py --telemetry-dir <path>
    py scripts/promote_telemetry_to_scenario.py --json     # stdout JSON only
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import logging
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.log import setup_logging

logger = logging.getLogger("scripts.promote_telemetry_to_scenario")


def default_telemetry_dir() -> Path:
    """Match log-watcher.py: ``~/.openclaw/telemetry/``."""
    return Path(os.path.expanduser("~")) / ".openclaw" / "telemetry"


def default_proposals_dir() -> Path:
    return REPO_ROOT / "artifacts" / "telemetry-proposals"


def iter_telemetry_files(directory: Path, *, since_days: int) -> Iterable[Path]:
    """Yield jsonl files newer than ``since_days``; oldest first."""
    if not directory.is_dir():
        return []
    cutoff = _dt.datetime.now() - _dt.timedelta(days=since_days)
    out = []
    for p in sorted(directory.glob("madeira-answer-quality-*.jsonl")):
        try:
            mtime = _dt.datetime.fromtimestamp(p.stat().st_mtime)
        except OSError:
            continue
        if mtime >= cutoff:
            out.append(p)
    return out


def load_records(files: Iterable[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in files:
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        except OSError as exc:
            logger.warning("could not read telemetry file %s: %s", path, exc)
    return records


# Suggestion mapping deliberately stays narrow; operator reviews + adjusts.
_ROUTE_TO_SKILL = {
    "hlk_lookup": "skill_madeira_lookup_v1",
    "hlk_direct_lookup": "skill_madeira_lookup_v1",
    "non_tool_answer": "skill_madeira_lookup_v1",
    "admin": "skill_madeira_lookup_v1",
    "execution": "skill_madeira_lookup_v1",
}

_ROUTE_TO_EXPECTED = {
    "hlk_lookup": "hlk_lookup",
    "hlk_direct_lookup": "hlk_lookup",
    "non_tool_answer": "hlk_lookup",
    "admin": "admin_escalate",
    "execution": "execution_escalate",
}

_OUTCOME_BY_FLAG = {
    "missing_explicit_escalation": "ESCALATE",
    "admin_brainstorm_drift": "ESCALATE",
    "missing_citation_asset": "GROUND",
    "internal_tool_leak": "REFUSE",
    "pseudo_hlk_path_leak": "REFUSE",
    "suspect_hlk_uuid_hallucination": "REFUSE",
    "compaction_interference": "PASS",
    "non_tool_answer": "GROUND",
}


def _summarise_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "user_text": (record.get("user_text") or "")[:240],
        "tool_calls": list(record.get("tool_calls") or []),
        "model": record.get("model") or "",
        "provider": record.get("provider") or "",
        "quality_score": record.get("quality_score"),
        "residual_flags": list(record.get("residual_flags") or []),
        "route_kind": record.get("route_kind") or "",
    }


def cluster_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group records by ``(route_kind, dominant residual_flag)`` and emit proposals.

    Records with no residual flags AND quality_score>=1.0 are skipped (they are
    healthy traces; nothing to promote).
    """
    clusters: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for r in records:
        flags = list(r.get("residual_flags") or [])
        if not flags and float(r.get("quality_score") or 0.0) >= 1.0:
            continue
        primary_flag = flags[0] if flags else "no_flag"
        key = (str(r.get("route_kind") or "unknown"), primary_flag)
        clusters.setdefault(key, []).append(r)

    proposals: list[dict[str, Any]] = []
    for (route_kind, primary_flag), bucket in sorted(clusters.items()):
        sample = bucket[0]
        skill_id = _ROUTE_TO_SKILL.get(route_kind, "skill_madeira_lookup_v1")
        expected_route = _ROUTE_TO_EXPECTED.get(route_kind, "hlk_lookup")
        outcome = _OUTCOME_BY_FLAG.get(primary_flag, "PASS")
        models_seen = sorted({r.get("model") or "" for r in bucket if r.get("model")})
        flag_distribution = Counter(
            f for r in bucket for f in (r.get("residual_flags") or [])
        )
        proposal_id = f"TP-{route_kind[:3].upper()}-{primary_flag[:6].upper()}-{len(bucket):03d}"
        proposals.append({
            "proposal_id": proposal_id,
            "cluster_key": f"{route_kind}|{primary_flag}",
            "match_count": len(bucket),
            "sample": _summarise_record(sample),
            "models_seen": models_seen,
            "flag_distribution": dict(flag_distribution.most_common()),
            "suggested_persona_id": "OPERATOR",
            "suggested_skill_id": skill_id,
            "suggested_scenario_class": "lookup",
            "suggested_difficulty_class": "moderate",
            "suggested_expected_route": expected_route,
            "suggested_expected_outcome_class": outcome,
            "suggested_lifecycle_status": "scaffold",
            "rationale": (
                f"Operator should validate cluster {primary_flag!r} on route "
                f"{route_kind!r} ({len(bucket)} sample(s)); register a "
                f"PERSONA_SCENARIO_REGISTRY row only after triage, do not auto-merge."
            ),
        })
    proposals.sort(key=lambda p: (-int(p["match_count"]), p["cluster_key"]))
    return proposals


def build_artifact(
    records: list[dict[str, Any]],
    *,
    since_days: int,
    telemetry_dir: Path,
) -> dict[str, Any]:
    proposals = cluster_records(records)
    return {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "since_days": since_days,
        "telemetry_dir": str(telemetry_dir),
        "scanned_records": len(records),
        "proposal_count": len(proposals),
        "proposals": proposals,
        "policy_anchor": "SOP-MADEIRA_SCENARIO_LIFECYCLE_001 §5.4 (operator-merged; never auto-applied)",
    }


def write_artifact(artifact: dict[str, Any], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = output_dir / f"telemetry-proposals-{ts}.json"
    path.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument(
        "--telemetry-dir", type=Path, default=default_telemetry_dir(),
        help="Directory holding madeira-answer-quality-*.jsonl files (default ~/.openclaw/telemetry/)",
    )
    ap.add_argument(
        "--since-days", type=int, default=7,
        help="Window in days (file mtime) (default 7)",
    )
    ap.add_argument(
        "--output-dir", type=Path, default=default_proposals_dir(),
        help="Where to write the JSON artifact (default artifacts/telemetry-proposals/)",
    )
    ap.add_argument("--json", action="store_true", help="Emit only JSON to stdout (no artifact write)")
    ap.add_argument("--quiet", action="store_true")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    setup_logging(json_output=False)
    files = list(iter_telemetry_files(args.telemetry_dir, since_days=int(args.since_days)))
    records = load_records(files)
    artifact = build_artifact(records, since_days=int(args.since_days), telemetry_dir=args.telemetry_dir)
    if args.json:
        sys.stdout.write(json.dumps(artifact, indent=2, sort_keys=True))
        sys.stdout.write("\n")
        return 0
    out_path = write_artifact(artifact, args.output_dir)
    if not args.quiet:
        sys.stdout.write(
            f"  Telemetry promotion proposals\n"
            f"  =============================\n"
            f"  scanned files:    {len(files)}\n"
            f"  scanned records:  {artifact['scanned_records']}\n"
            f"  proposals:        {artifact['proposal_count']}\n"
            f"  artifact:         {out_path}\n"
            f"  operator gate:    SOP-MADEIRA_SCENARIO_LIFECYCLE_001 (no auto-merge)\n"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
