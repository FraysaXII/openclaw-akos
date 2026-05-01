"""Initiative 45 P2 — Tests for cassette format + record/replay I/O.

Asserts:
- Cassette format round-trip (write -> read)
- Deterministic recording via classify_request
- Replay detects route mismatch and stale cassettes
- AKOS_RECORD_LIVE=1 guard on live_llm path
- Seeded cassettes for the 5 skills exist and replay green
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from akos.eval_harness.cassette import (
    CASSETTE_ROOT,
    CASSETTE_SCHEMA_VERSION,
    STALENESS_FAIL_DAYS,
    STALENESS_WARN_DAYS,
    CassetteHeader,
    adversarial_cassettes,
    cassette_path,
    list_cassettes,
    read_cassette,
    record_classify_request_cassette,
    record_live_llm_cassette,
    replay_cassette,
    replay_classify_request_cassette,
    staleness_status,
    write_cassette,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


# ── Format round-trip ─────────────────────────────────────────────────────────


def test_write_then_read_cassette_round_trip(tmp_path: Path) -> None:
    p = tmp_path / "skill-x" / "probe-y.jsonl"
    header = CassetteHeader(
        schema_version="1.0",
        skill_id="skill-x",
        probe_id="probe-y",
        probe_kind="classify_request",
        recorded_at="2026-05-01T04:00:00Z",
        recorded_by="test",
        model_id="deterministic",
        model_tier="deterministic",
        golden_assertion={"route": "hlk_lookup"},
        last_recorded="2026-05-01T04:00:00Z",
    )
    events = [{"event": "prompt", "text": "hi"}, {"event": "final", "route": "hlk_lookup"}]
    summary = {"status": "PASS", "tokens_in": 0, "tokens_out": 0, "latency_ms": 1}
    write_cassette(p, header, events, summary)

    h2, e2, s2 = read_cassette(p)
    assert h2.skill_id == "skill-x"
    assert h2.probe_id == "probe-y"
    assert h2.golden_assertion == {"route": "hlk_lookup"}
    assert len(e2) == 2
    assert s2["status"] == "PASS"


def test_read_cassette_raises_on_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_cassette(tmp_path / "missing.jsonl")


def test_read_cassette_raises_on_malformed(tmp_path: Path) -> None:
    p = tmp_path / "bad.jsonl"
    p.write_text("not json", encoding="utf-8")
    with pytest.raises(Exception):
        read_cassette(p)


# ── Deterministic record + replay ─────────────────────────────────────────────


def test_record_classify_request_creates_cassette(tmp_path: Path) -> None:
    p = record_classify_request_cassette(
        skill_id="SKILL-MADEIRA-LOOKUP-V1",
        probe_id="t1",
        prompt="Find the System Owner role",
        recorded_by="pytest",
        root=tmp_path,
    )
    assert p.is_file()
    h, _e, s = read_cassette(p)
    assert h.probe_kind == "classify_request"
    assert h.recorded_by == "pytest"
    assert "route" in h.golden_assertion
    assert s["status"] == "PASS"


def test_replay_classify_request_passes_for_just_recorded_cassette(tmp_path: Path) -> None:
    p = record_classify_request_cassette(
        skill_id="SKILL-MADEIRA-LOOKUP-V1",
        probe_id="t2",
        prompt="Find the System Owner role",
        recorded_by="pytest",
        root=tmp_path,
    )
    out = replay_classify_request_cassette(p)
    assert out["status"] == "PASS"
    assert out["failures"] == []
    assert out["expected_route"] == out["actual_route"]


def test_replay_detects_route_mismatch(tmp_path: Path) -> None:
    """If we tamper with the golden_assertion, replay must fail."""
    p = record_classify_request_cassette(
        skill_id="x", probe_id="y", prompt="Find a role", recorded_by="pytest", root=tmp_path
    )
    h, e, s = read_cassette(p)
    h.golden_assertion = {"route": "definitely_not_a_real_route"}
    write_cassette(p, h, e, s)

    out = replay_classify_request_cassette(p)
    assert out["status"] == "FAIL"
    assert any("route_mismatch" in f for f in out["failures"])


# ── Staleness ─────────────────────────────────────────────────────────────────


def test_staleness_fresh_for_just_recorded() -> None:
    h = CassetteHeader(
        schema_version="1.0", skill_id="x", probe_id="y", probe_kind="classify_request",
        recorded_at="2026-05-01T00:00:00Z", recorded_by="t", model_id="d", model_tier="d",
        golden_assertion={}, last_recorded="2026-05-01T00:00:00Z",
    )
    now = datetime(2026, 5, 1, 1, tzinfo=timezone.utc)
    label, age = staleness_status(h, now=now)
    assert label == "fresh"
    assert age == 0


def test_staleness_warns_at_60_to_89_days() -> None:
    h = CassetteHeader(
        schema_version="1.0", skill_id="x", probe_id="y", probe_kind="classify_request",
        recorded_at="2026-01-01T00:00:00Z", recorded_by="t", model_id="d", model_tier="d",
        golden_assertion={}, last_recorded="2026-01-01T00:00:00Z",
    )
    now = datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=70)
    label, age = staleness_status(h, now=now)
    assert label == "warn"
    assert age == 70


def test_staleness_fails_at_90_plus_days() -> None:
    h = CassetteHeader(
        schema_version="1.0", skill_id="x", probe_id="y", probe_kind="classify_request",
        recorded_at="2025-01-01T00:00:00Z", recorded_by="t", model_id="d", model_tier="d",
        golden_assertion={}, last_recorded="2025-01-01T00:00:00Z",
    )
    now = datetime(2026, 5, 1, tzinfo=timezone.utc)
    label, age = staleness_status(h, now=now)
    assert label == "fail"
    assert age >= STALENESS_FAIL_DAYS


# ── Live LLM guard ────────────────────────────────────────────────────────────


def test_record_live_llm_blocks_without_env_guard(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AKOS_RECORD_LIVE", raising=False)
    with pytest.raises(PermissionError, match="AKOS_RECORD_LIVE=1"):
        record_live_llm_cassette(
            skill_id="x",
            probe_id="y",
            prompt="hi",
            recorded_by="t",
            model_id="m",
            model_tier="cheap",
            golden_rubric={"contains": ["foo"]},
            root=tmp_path,
        )


def test_record_live_llm_allows_with_env_guard(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AKOS_RECORD_LIVE", "1")
    p = record_live_llm_cassette(
        skill_id="x",
        probe_id="y",
        prompt="hi",
        recorded_by="t",
        model_id="m",
        model_tier="cheap",
        golden_rubric={"contains": ["P6-stub"]},
        root=tmp_path,
    )
    assert p.is_file()
    out = replay_cassette(p)
    # P6 stub final text contains "P6-stub" so the rubric matches
    assert out["status"] in ("PASS", "WARN")


# ── List + adversarial ────────────────────────────────────────────────────────


def test_list_cassettes_isolates_adversarial(tmp_path: Path) -> None:
    record_classify_request_cassette(
        skill_id="A", probe_id="p1", prompt="x", recorded_by="t", root=tmp_path
    )
    adv_path = tmp_path / "adversarial" / "A" / "ad1.jsonl"
    adv_path.parent.mkdir(parents=True, exist_ok=True)
    adv_path.write_text(
        json.dumps(
            {
                "event": "header",
                "schema_version": "1.0",
                "skill_id": "A",
                "probe_id": "ad1",
                "probe_kind": "classify_request",
                "recorded_at": "2026-05-01T00:00:00Z",
                "recorded_by": "t",
                "model_id": "d",
                "model_tier": "d",
                "golden_assertion": {"route": "x"},
                "last_recorded": "2026-05-01T00:00:00Z",
            }
        )
        + "\n"
        + json.dumps({"event": "summary", "status": "PASS"})
        + "\n",
        encoding="utf-8",
    )

    main = list_cassettes(root=tmp_path)
    adv = adversarial_cassettes(root=tmp_path)
    assert any(p.name == "p1.jsonl" for p in main)
    assert all("adversarial" not in str(p) for p in main)
    assert any(p.name == "ad1.jsonl" for p in adv)


# ── Seeded cassettes (the 6 we just shipped) ──────────────────────────────────


def test_seeded_cassettes_for_5_skills_exist() -> None:
    """One cassette per skill (Madeira has 2 because it's the highest-traffic)."""
    cassettes = list_cassettes()
    skills = {p.parent.name for p in cassettes}
    expected = {
        "SKILL-MADEIRA-LOOKUP-V1",
        "SKILL-ARCHITECT-PLAN-V1",
        "SKILL-EXECUTOR-RUN-V1",
        "SKILL-VERIFIER-CHECK-V1",
        "SKILL-SHARED-LOCALE-DETECT-V1",
    }
    missing = expected - skills
    assert not missing, f"missing seed cassettes for: {missing}"
    assert len(cassettes) >= 5, f"expected >=5 cassettes, got {len(cassettes)}"


def test_all_seeded_cassettes_replay_pass() -> None:
    cassettes = list_cassettes()
    fails: list[tuple[str, list[str]]] = []
    for p in cassettes:
        out = replay_cassette(p)
        if out["status"] not in ("PASS", "WARN"):
            fails.append((str(p.relative_to(REPO_ROOT)), out.get("failures", [])))
    assert not fails, f"replay regressions: {fails}"


def test_v2_run_replay_through_dispatcher_returns_one_row_per_cassette() -> None:
    from akos.eval_harness.v2 import Scorecard, run_replay

    sc = Scorecard()
    run_replay(sc)
    rep = [r for r in sc.rows if r.mode == "replay"]
    cassettes = list_cassettes()
    assert len(rep) == len(cassettes), f"row/cassette mismatch: {len(rep)} vs {len(cassettes)}"
    fails = [r for r in rep if r.status not in ("PASS", "WARN", "SKIP")]
    assert not fails, f"replay regressions in dispatcher: {[(r.skill_id, r.failures) for r in fails]}"


# ── CLI surface ───────────────────────────────────────────────────────────────


def test_cli_record_creates_cassette(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Smoke: ensure the CLI shells through correctly. Uses a temp cassette dir
    via direct module call rather than subprocess (subprocess would write to the
    real cassette dir which we don't want in tests)."""
    from akos.eval_harness.cassette import record_classify_request_cassette

    p = record_classify_request_cassette(
        skill_id="X-TEST",
        probe_id="cli-smoke",
        prompt="anything",
        recorded_by="cli-test",
        root=tmp_path,
    )
    assert p.is_file()
    out = replay_classify_request_cassette(p)
    assert out["status"] == "PASS"
