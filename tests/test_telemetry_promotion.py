"""Initiative 49 P11 — promote_telemetry_to_scenario tests.

Coverage:
- iter_telemetry_files honours mtime window
- load_records tolerates blank + malformed jsonl lines
- cluster_records skips clean records (no residual flags + quality_score>=1.0)
- cluster_records emits one proposal per (route_kind, dominant flag) combo
- build_artifact emits stable structure + policy anchor
- main() writes a JSON artifact with `proposals` array when run end-to-end
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _load_module():
    path = REPO_ROOT / "scripts" / "promote_telemetry_to_scenario.py"
    spec = importlib.util.spec_from_file_location("scripts.promote_telemetry_to_scenario", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["scripts.promote_telemetry_to_scenario"] = mod
    spec.loader.exec_module(mod)
    return mod


promo = _load_module()


def _record(**kw):
    base = {
        "agent_role": "madeira",
        "session_id": "S-1",
        "user_text": "where is X policy?",
        "assistant_text": "...",
        "tool_calls": [],
        "tool_backed": False,
        "route_kind": "hlk_lookup",
        "citation_asset": "",
        "residual_flags": ["missing_citation_asset"],
        "quality_score": 0.4,
        "provider": "openai",
        "model": "gpt-x",
    }
    base.update(kw)
    return base


def _write_jsonl(path: Path, records) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")


def test_load_records_skips_blank_and_malformed_lines(tmp_path: Path) -> None:
    p = tmp_path / "madeira-answer-quality-2026-05-03.jsonl"
    p.write_text(
        "\n"
        + json.dumps(_record(session_id="A")) + "\n"
        + "{not json}\n"
        + json.dumps(_record(session_id="B")) + "\n",
        encoding="utf-8",
    )
    records = promo.load_records([p])
    assert len(records) == 2
    assert records[0]["session_id"] == "A"


def test_iter_telemetry_files_window(tmp_path: Path) -> None:
    fresh = tmp_path / "madeira-answer-quality-fresh.jsonl"
    fresh.write_text("", encoding="utf-8")
    stale = tmp_path / "madeira-answer-quality-stale.jsonl"
    stale.write_text("", encoding="utf-8")
    old_ts = (datetime.now() - timedelta(days=30)).timestamp()
    import os
    os.utime(stale, (old_ts, old_ts))
    files = list(promo.iter_telemetry_files(tmp_path, since_days=7))
    assert fresh in files
    assert stale not in files


def test_cluster_records_skips_clean_traces() -> None:
    clean = _record(residual_flags=[], quality_score=1.0)
    proposals = promo.cluster_records([clean])
    assert proposals == []


def test_cluster_records_groups_by_route_and_primary_flag() -> None:
    rs = [
        _record(residual_flags=["missing_citation_asset"], route_kind="hlk_lookup"),
        _record(residual_flags=["missing_citation_asset"], route_kind="hlk_lookup"),
        _record(residual_flags=["internal_tool_leak"], route_kind="hlk_lookup"),
        _record(residual_flags=["missing_explicit_escalation"], route_kind="admin"),
    ]
    proposals = promo.cluster_records(rs)
    keys = {p["cluster_key"] for p in proposals}
    assert keys == {
        "hlk_lookup|missing_citation_asset",
        "hlk_lookup|internal_tool_leak",
        "admin|missing_explicit_escalation",
    }


def test_cluster_records_assigns_outcome_per_flag() -> None:
    proposals = promo.cluster_records([
        _record(residual_flags=["missing_citation_asset"], route_kind="hlk_lookup"),
        _record(residual_flags=["internal_tool_leak"], route_kind="hlk_lookup"),
        _record(residual_flags=["missing_explicit_escalation"], route_kind="admin"),
    ])
    by_key = {p["cluster_key"]: p for p in proposals}
    assert by_key["hlk_lookup|missing_citation_asset"]["suggested_expected_outcome_class"] == "GROUND"
    assert by_key["hlk_lookup|internal_tool_leak"]["suggested_expected_outcome_class"] == "REFUSE"
    assert by_key["admin|missing_explicit_escalation"]["suggested_expected_outcome_class"] == "ESCALATE"


def test_build_artifact_carries_policy_anchor() -> None:
    artifact = promo.build_artifact([_record()], since_days=3, telemetry_dir=Path("/tmp"))
    assert "SOP-MADEIRA_SCENARIO_LIFECYCLE_001" in artifact["policy_anchor"]
    assert artifact["scanned_records"] == 1
    assert artifact["proposal_count"] >= 1


def test_main_writes_artifact_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    telemetry_dir = tmp_path / "telemetry"
    _write_jsonl(
        telemetry_dir / "madeira-answer-quality-2026-05-03.jsonl",
        [_record(), _record(residual_flags=["internal_tool_leak"])],
    )
    out_dir = tmp_path / "proposals"
    rc = promo.main([
        "--telemetry-dir", str(telemetry_dir),
        "--output-dir", str(out_dir),
        "--quiet",
    ])
    assert rc == 0
    artifacts = list(out_dir.glob("telemetry-proposals-*.json"))
    assert len(artifacts) == 1
    payload = json.loads(artifacts[0].read_text(encoding="utf-8"))
    assert payload["proposal_count"] >= 1
    assert "proposals" in payload


def test_main_with_json_flag_emits_to_stdout(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    telemetry_dir = tmp_path / "telemetry"
    _write_jsonl(
        telemetry_dir / "madeira-answer-quality-2026-05-03.jsonl",
        [_record()],
    )
    rc = promo.main([
        "--telemetry-dir", str(telemetry_dir),
        "--output-dir", str(tmp_path / "ignored"),
        "--json",
    ])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["scanned_records"] == 1
    assert "proposals" in payload
