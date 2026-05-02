"""Initiative 48 P7 — dossier_run_writer + local index."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from akos.dossier import dossier_run_writer as drw


def test_compute_rollup_from_section_metrics_eval_pass_rate() -> None:
    sm = {
        "section_03": {"metrics": {"rows_total": 10, "rows_passed": 8, "cost_total_usd": 0.02}},
        "section_04": {"metrics": {"overall_within_tolerance": True}},
        "section_07": {"metrics": {"drift_canary_total_drift": 2}},
    }
    r = drw.compute_rollup_from_section_metrics(sm)
    assert r["eval_pass_rate"] == pytest.approx(0.8)
    assert r["calibration_ok"] == 1.0
    assert r["drift_canary_total"] == 2
    assert r["cost_total_usd"] == pytest.approx(0.02)


def test_write_dossier_run_row_skips_remote_without_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    monkeypatch.setattr(drw, "LOCAL_INDEX_PATH", tmp_path / "index.json")

    stats = drw.write_dossier_run_row(
        run_id="t1",
        started_at="2026-05-02T00:00:00+00:00",
        mode="snapshot",
        git_sha="abc",
        section_metrics={"section_03": {"metrics": {"rows_total": 4, "rows_passed": 4}}},
        manifest_sha256="deadbeef",
    )
    assert stats["written"] == 0
    assert stats["skipped"] == 1
    assert drw.LOCAL_INDEX_PATH.is_file()
    data = json.loads(drw.LOCAL_INDEX_PATH.read_text(encoding="utf-8"))
    assert len(data["runs"]) == 1
    assert data["runs"][0]["rollup"]["eval_pass_rate"] == pytest.approx(1.0)


def test_gather_trend_sparklines_insufficient_without_history(monkeypatch: pytest.MonkeyPatch) -> None:
    from akos.dossier.sources import gather_trend_sparklines

    monkeypatch.setattr("akos.dossier.sources._fetch_dossier_run_remote", lambda limit: [])
    monkeypatch.setattr("akos.dossier.sources._load_local_index_runs", lambda limit: [])

    d = gather_trend_sparklines(
        trend_window=10,
        since=None,
        prior_section_results=None,
        current_started_at=None,
    )
    assert d.payload.get("insufficient_data") is True


def test_gather_trend_sparklines_two_points_current_and_history(monkeypatch: pytest.MonkeyPatch) -> None:
    from akos.dossier.sources import gather_trend_sparklines
    from akos.dossier.run import DossierSectionResult

    monkeypatch.setattr("akos.dossier.sources._fetch_dossier_run_remote", lambda limit: [])
    monkeypatch.setattr(
        "akos.dossier.sources._load_local_index_runs",
        lambda limit: [
            {
                "started_at": "2026-05-01T12:00:00Z",
                "rollup": {
                    "eval_pass_rate": 0.5,
                    "calibration_ok": 1.0,
                    "drift_canary_total": 0,
                    "cost_total_usd": 0.01,
                },
            },
        ],
    )

    fake_prior = [
        DossierSectionResult(
            section_id=3,
            name="Eval health",
            metrics={"rows_total": 4, "rows_passed": 4, "cost_total_usd": 0.0},
        ),
        DossierSectionResult(
            section_id=4,
            name="Persona library + calibration",
            metrics={"overall_within_tolerance": True},
        ),
        DossierSectionResult(
            section_id=7,
            name="Drift canaries",
            metrics={"drift_canary_total_drift": 1},
        ),
    ]

    d = gather_trend_sparklines(
        trend_window=10,
        since=None,
        prior_section_results=fake_prior,
        current_started_at="2026-05-02T12:00:00Z",
    )
    assert d.payload.get("insufficient_data") is False
    spark = d.payload.get("sparklines") or {}
    assert len(spark) == 4
    assert "<svg" in next(iter(spark.values()))


def test_i48_migration_defines_dossier_run_table() -> None:
    mig = (
        Path(__file__).resolve().parent.parent
        / "supabase"
        / "migrations"
        / "20260502140000_i48_dossier_run_mirror.sql"
    )
    text = mig.read_text(encoding="utf-8")
    assert "CREATE TABLE IF NOT EXISTS compliance.dossier_run" in text
    assert "manifest_sha256" in text
    assert "section_metrics JSONB" in text


def test_policy_register_has_dossier_retention_row() -> None:
    csv_path = (
        Path(__file__).resolve().parent.parent
        / "docs"
        / "references"
        / "hlk"
        / "compliance"
        / "dimensions"
        / "POLICY_REGISTER.csv"
    )
    txt = csv_path.read_text(encoding="utf-8")
    assert "POL-DOSSIER-RUN-RETENTION-V1" in txt
    assert ",retention," in txt
