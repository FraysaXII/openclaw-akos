"""Tests for scripts/regression_artifact_diff.py (Initiative 55 P6).

Covers:
- first-cycle (no baseline) emits ``is_first_cycle=True`` and ``new`` statuses.
- changed/unchanged/new/removed/file-level diff vocabulary.
- numeric delta calculation for judge axes.
- summary changed-field counts (canonical input for I55 P7 threshold POLICY).
- markdown rendering shape.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import regression_artifact_diff as mod  # type: ignore  # noqa: E402


def _make_manifest(
    *,
    run_id: str = "dossier-current",
    git_sha: str = "deadbeef",
    started_at: str = "2026-05-03T19:18:55+00:00",
    files: dict | None = None,
    s01: dict | None = None,
    s02: dict | None = None,
    s03: dict | None = None,
    s04: dict | None = None,
    s08: dict | None = None,
) -> dict:
    return {
        "run_id": run_id,
        "git_sha": git_sha,
        "started_at": started_at,
        "mode": "snapshot",
        "filter": {"flavor": "madeira"},
        "files": files
        or {
            "dossier.md": {"sha256": "aaa111", "char_count": 8076},
            "dossier.html": {"sha256": "bbb222", "char_count": 19407},
        },
        "section_metrics": {
            "section_01": {"name": "Executive summary", "status": "PASS", "metrics": s01 or {}},
            "section_02": {"name": "Schema + governance", "status": "PASS", "metrics": s02 or {}},
            "section_03": {"name": "Eval health", "status": "PASS", "metrics": s03 or {}},
            "section_04": {"name": "Persona library", "status": "PASS", "metrics": s04 or {}},
            "section_05": {"name": "Adversarial", "status": "PASS", "metrics": {}},
            "section_06": {"name": "Recovery", "status": "PASS", "metrics": {}},
            "section_07": {"name": "Drift", "status": "PASS", "metrics": {}},
            "section_08": {"name": "Operational health", "status": "PASS", "metrics": s08 or {}},
            "section_09": {"name": "External", "status": "PASS", "metrics": {}},
            "section_10": {"name": "Open ops", "status": "PASS", "metrics": {}},
            "section_11": {"name": "Trends", "status": "INFO", "metrics": {}},
            "section_12": {"name": "Appendix", "status": "INFO", "metrics": {}},
        },
    }


def test_first_cycle_when_no_baseline(tmp_path: Path) -> None:
    current = _make_manifest(s02={"total_scenarios": 329, "total_personas": 16})
    cur_path = tmp_path / "manifest.json"
    cur_path.write_text(json.dumps(current), encoding="utf-8")
    record = mod.build_diff_record(current, None, cur_path, None)
    assert record["is_first_cycle"] is True
    assert record["baseline"] is None
    cite = record["cite_counts"]
    assert cite["total_scenarios"]["status"] == "new"
    assert cite["total_scenarios"]["current"] == 329


def test_unchanged_when_metrics_equal(tmp_path: Path) -> None:
    current = _make_manifest(s02={"total_scenarios": 329, "total_personas": 16})
    baseline = _make_manifest(s02={"total_scenarios": 329, "total_personas": 16})
    cur_path = tmp_path / "current.json"
    base_path = tmp_path / "baseline.json"
    cur_path.write_text(json.dumps(current), encoding="utf-8")
    base_path.write_text(json.dumps(baseline), encoding="utf-8")
    record = mod.build_diff_record(current, baseline, cur_path, base_path)
    assert record["is_first_cycle"] is False
    cite = record["cite_counts"]
    for field in ("total_scenarios", "total_personas"):
        assert cite[field]["status"] == "unchanged"
        assert cite[field]["delta"] == 0


def test_changed_emits_signed_delta(tmp_path: Path) -> None:
    current = _make_manifest(s02={"total_scenarios": 332})
    baseline = _make_manifest(s02={"total_scenarios": 329})
    record = mod.build_diff_record(current, baseline, tmp_path / "c.json", tmp_path / "b.json")
    cite = record["cite_counts"]
    assert cite["total_scenarios"]["status"] == "changed"
    assert cite["total_scenarios"]["delta"] == 3


def test_judge_axis_merged_from_03_and_04(tmp_path: Path) -> None:
    """Section 04 wins on overlap (merged_03_04_current = {**s03, **s04})."""
    current = _make_manifest(
        s03={"judge_score_brand_voice_mean": 0.78},
        s04={"judge_score_brand_voice_mean": 0.82, "judge_axis_fail_brand_voice": 1},
    )
    baseline = _make_manifest(
        s03={"judge_score_brand_voice_mean": 0.78},
        s04={"judge_score_brand_voice_mean": 0.80, "judge_axis_fail_brand_voice": 0},
    )
    record = mod.build_diff_record(current, baseline, tmp_path / "c.json", tmp_path / "b.json")
    judge = record["judge_axes"]
    # Section 04 wins on merge
    assert judge["judge_score_brand_voice_mean"]["current"] == 0.82
    assert judge["judge_score_brand_voice_mean"]["baseline"] == 0.80
    assert judge["judge_score_brand_voice_mean"]["status"] == "changed"
    assert judge["judge_score_brand_voice_mean"]["delta"] == pytest.approx(0.02)
    assert judge["judge_axis_fail_brand_voice"]["delta"] == 1


def test_file_diff_status_vocab(tmp_path: Path) -> None:
    current = _make_manifest(
        files={
            "dossier.md": {"sha256": "AAA"},
            "dossier.html": {"sha256": "BBB"},
            "new-only.txt": {"sha256": "CCC"},
        }
    )
    baseline = _make_manifest(
        files={
            "dossier.md": {"sha256": "AAA"},  # unchanged
            "dossier.html": {"sha256": "BBB-OLD"},  # changed
            "removed-only.txt": {"sha256": "DDD"},  # removed
        }
    )
    record = mod.build_diff_record(current, baseline, tmp_path / "c.json", tmp_path / "b.json")
    files = record["files"]
    assert files["dossier.md"]["status"] == "unchanged"
    assert files["dossier.html"]["status"] == "changed"
    assert files["new-only.txt"]["status"] == "new"
    assert files["removed-only.txt"]["status"] == "removed"
    summary = record["summary"]["files"]
    assert summary["files_compared"] == 4
    assert summary["files_changed"] == 3  # changed + new + removed


def test_summary_counts_changed_only(tmp_path: Path) -> None:
    current = _make_manifest(
        s02={"total_scenarios": 332, "total_personas": 16, "total_topics": 28, "total_skills": 5, "total_policies": 32}
    )
    baseline = _make_manifest(
        s02={"total_scenarios": 329, "total_personas": 16, "total_topics": 28, "total_skills": 5, "total_policies": 32}
    )
    record = mod.build_diff_record(current, baseline, tmp_path / "c.json", tmp_path / "b.json")
    cite_summary = record["summary"]["cite_counts"]
    assert cite_summary["fields_compared"] == 5
    assert cite_summary["fields_changed"] == 1
    assert cite_summary["changed_field_names"] == ["total_scenarios"]


def test_render_markdown_contains_required_sections(tmp_path: Path) -> None:
    current = _make_manifest(s02={"total_scenarios": 332})
    baseline = _make_manifest(s02={"total_scenarios": 329})
    record = mod.build_diff_record(current, baseline, tmp_path / "c.json", tmp_path / "b.json")
    md = mod.render_markdown(record)
    assert "# Regression artifact diff" in md
    assert "Summary (changed-field counts)" in md
    assert "Changed fields by family" in md
    assert "total_scenarios" in md


def test_main_writes_outputs(tmp_path: Path) -> None:
    current = _make_manifest(s02={"total_scenarios": 332})
    baseline = _make_manifest(s02={"total_scenarios": 329})
    cur_path = tmp_path / "cur.json"
    base_path = tmp_path / "base.json"
    cur_path.write_text(json.dumps(current), encoding="utf-8")
    base_path.write_text(json.dumps(baseline), encoding="utf-8")
    out_json = tmp_path / "diff.json"
    out_md = tmp_path / "diff.md"

    rc = mod.main(
        [
            "--current",
            str(cur_path),
            "--last-sent",
            str(base_path),
            "--out",
            str(out_json),
            "--md",
            str(out_md),
            "--quiet",
        ]
    )
    assert rc == 0
    assert out_json.is_file()
    assert out_md.is_file()
    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload["is_first_cycle"] is False
    assert payload["cite_counts"]["total_scenarios"]["delta"] == 3


def test_main_first_cycle_when_baseline_missing(tmp_path: Path) -> None:
    current = _make_manifest(s02={"total_scenarios": 329})
    cur_path = tmp_path / "cur.json"
    cur_path.write_text(json.dumps(current), encoding="utf-8")
    out_json = tmp_path / "diff.json"
    rc = mod.main(["--current", str(cur_path), "--out", str(out_json), "--quiet"])
    assert rc == 0
    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload["is_first_cycle"] is True
    assert payload["baseline"] is None


def test_main_first_cycle_when_baseline_path_does_not_exist(tmp_path: Path) -> None:
    """``--last-sent`` pointing at a nonexistent file is treated as first-cycle."""
    current = _make_manifest(s02={"total_scenarios": 329})
    cur_path = tmp_path / "cur.json"
    cur_path.write_text(json.dumps(current), encoding="utf-8")
    missing = tmp_path / "does-not-exist.json"
    out_json = tmp_path / "diff.json"
    rc = mod.main(
        [
            "--current",
            str(cur_path),
            "--last-sent",
            str(missing),
            "--out",
            str(out_json),
            "--quiet",
        ]
    )
    assert rc == 0
    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload["is_first_cycle"] is True


def test_main_returns_1_on_unreadable_current(tmp_path: Path) -> None:
    rc = mod.main(["--current", str(tmp_path / "missing.json"), "--quiet"])
    assert rc == 1
