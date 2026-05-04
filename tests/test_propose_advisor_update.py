"""Tests for scripts/propose_advisor_update.py (Initiative 55 P6/P7).

Covers:
- threshold parsing from policy_text (key=value tokens, mixed separators).
- evaluate_thresholds: trips/no-trips across the four metric families.
- proposal markdown structure (operator pre-flight checklist).
- loop-history append (D-IH-55-E both-signal-and-silence telemetry).
- --use-defaults bypasses POLICY lookup (CI-friendly path).
- --force-proposal and --allow-first-cycle override silence path.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propose_advisor_update as mod  # type: ignore  # noqa: E402


def _no_change_diff_record() -> dict:
    return {
        "is_first_cycle": False,
        "current": {"run_id": "cur-1", "git_sha": "deadbeef", "started_at": "t", "mode": "snapshot"},
        "baseline": {"run_id": "base-1", "git_sha": "cafebabe", "started_at": "t-1", "mode": "snapshot"},
        "cite_counts": {
            "total_scenarios": {"status": "unchanged", "current": 329, "baseline": 329, "delta": 0},
            "total_personas": {"status": "unchanged", "current": 16, "baseline": 16, "delta": 0},
            "total_topics": {"status": "unchanged", "current": 28, "baseline": 28, "delta": 0},
            "total_skills": {"status": "unchanged", "current": 5, "baseline": 5, "delta": 0},
            "total_policies": {"status": "unchanged", "current": 32, "baseline": 32, "delta": 0},
        },
        "scenario_deltas": {
            "total_scenarios": {"status": "unchanged", "current": 55, "baseline": 55, "delta": 0},
            "personas_outside_tolerance_count": {"status": "unchanged", "current": 0, "baseline": 0, "delta": 0},
            "quarantined_scenarios_count": {"status": "unchanged", "current": 0, "baseline": 0, "delta": 0},
        },
        "judge_axes": {
            "judge_score_brand_voice_mean": {"status": "unchanged", "current": 0.80, "baseline": 0.80, "delta": 0},
            "judge_score_citation_mean": {"status": "unchanged", "current": 0.75, "baseline": 0.75, "delta": 0},
            "judge_score_persona_fit_mean": {"status": "unchanged", "current": 0.70, "baseline": 0.70, "delta": 0},
            "judge_axis_fail_brand_voice": {"status": "unchanged", "current": 0, "baseline": 0, "delta": 0},
            "judge_axis_fail_citation": {"status": "unchanged", "current": 0, "baseline": 0, "delta": 0},
            "judge_axis_fail_persona_fit": {"status": "unchanged", "current": 0, "baseline": 0, "delta": 0},
            "judge_worst_axis_fail_count": {"status": "unchanged", "current": 0, "baseline": 0, "delta": 0},
        },
        "endpoint_cost": {},
        "brand_voice": {},
        "files": {
            "dossier.md": {"status": "unchanged", "current_sha256": "AAA", "baseline_sha256": "AAA"},
        },
    }


def _scenario_change_diff(delta: int = 5) -> dict:
    rec = _no_change_diff_record()
    rec["cite_counts"]["total_scenarios"] = {
        "status": "changed",
        "current": 329 + delta,
        "baseline": 329,
        "delta": delta,
    }
    return rec


def _judge_movement_diff(score_delta: float = 0.05) -> dict:
    rec = _no_change_diff_record()
    rec["judge_axes"]["judge_score_brand_voice_mean"] = {
        "status": "changed",
        "current": 0.80 + score_delta,
        "baseline": 0.80,
        "delta": score_delta,
    }
    return rec


def _files_change_diff(n: int = 3) -> dict:
    rec = _no_change_diff_record()
    files = {}
    for i in range(n):
        files[f"changed-{i}.md"] = {"status": "changed", "current_sha256": f"NEW-{i}", "baseline_sha256": f"OLD-{i}"}
    files["dossier.md"] = {"status": "unchanged", "current_sha256": "AAA", "baseline_sha256": "AAA"}
    rec["files"] = files
    return rec


def _register_growth_diff(persona_delta: int = 2) -> dict:
    rec = _no_change_diff_record()
    rec["cite_counts"]["total_personas"] = {
        "status": "changed",
        "current": 16 + persona_delta,
        "baseline": 16,
        "delta": persona_delta,
    }
    return rec


# -------------------- _parse_policy_text --------------------


def test_parse_policy_text_handles_whitespace_separators() -> None:
    text = "min_changed_scenarios=3 min_judge_axis_movement_pp=2 min_register_rows_added=1 min_files_changed=2"
    parsed = mod._parse_policy_text(text)
    assert parsed["min_changed_scenarios"] == 3
    assert parsed["min_judge_axis_movement_pp"] == 2
    assert parsed["min_register_rows_added"] == 1
    assert parsed["min_files_changed"] == 2


def test_parse_policy_text_handles_commas_and_semicolons() -> None:
    text = "min_changed_scenarios=3, min_judge_axis_movement_pp=2; min_files_changed=4"
    parsed = mod._parse_policy_text(text)
    assert parsed["min_files_changed"] == 4
    assert parsed["min_judge_axis_movement_pp"] == 2


def test_parse_policy_text_skips_non_kv_prose() -> None:
    text = "I55 P7 thresholds. min_changed_scenarios=3. Operator may tune per advisor."
    parsed = mod._parse_policy_text(text)
    assert parsed == {"min_changed_scenarios": 3}


def test_parse_policy_text_floats() -> None:
    text = "min_judge_axis_movement_pp=2.5"
    parsed = mod._parse_policy_text(text)
    assert parsed["min_judge_axis_movement_pp"] == pytest.approx(2.5)


# -------------------- evaluate_thresholds --------------------


def test_evaluate_no_change_does_not_trip() -> None:
    rec = _no_change_diff_record()
    out = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    assert out["should_propose"] is False
    assert out["trips"] == []
    assert out["metrics"]["changed_scenarios"] == 0
    assert out["metrics"]["judge_axis_movement_pp"] == 0
    assert out["metrics"]["files_changed"] == 0


def test_evaluate_scenario_delta_trips() -> None:
    rec = _scenario_change_diff(delta=5)
    out = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    assert out["should_propose"] is True
    trips = {name for name, *_ in out["trips"]}
    assert "min_changed_scenarios" in trips
    assert out["metrics"]["changed_scenarios"] == 5


def test_evaluate_judge_movement_trips() -> None:
    rec = _judge_movement_diff(score_delta=0.05)  # 5pp
    out = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    assert out["should_propose"] is True
    assert out["metrics"]["judge_axis_movement_pp"] == pytest.approx(5.0)
    trips = {name for name, *_ in out["trips"]}
    assert "min_judge_axis_movement_pp" in trips


def test_evaluate_files_changed_trips() -> None:
    rec = _files_change_diff(n=3)
    out = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    assert out["should_propose"] is True
    assert out["metrics"]["files_changed"] == 3
    trips = {name for name, *_ in out["trips"]}
    assert "min_files_changed" in trips


def test_evaluate_register_growth_trips() -> None:
    rec = _register_growth_diff(persona_delta=2)
    out = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    assert out["should_propose"] is True
    assert out["metrics"]["register_rows_added"] == 2
    trips = {name for name, *_ in out["trips"]}
    assert "min_register_rows_added" in trips


def test_evaluate_below_threshold_does_not_trip() -> None:
    rec = _scenario_change_diff(delta=2)  # below default min=3
    out = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    assert out["should_propose"] is False
    assert out["metrics"]["changed_scenarios"] == 2


def test_evaluate_first_cycle_carries_through() -> None:
    rec = _no_change_diff_record()
    rec["is_first_cycle"] = True
    out = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    assert out["is_first_cycle"] is True


# -------------------- render_proposal_md --------------------


def test_render_proposal_md_threshold_path() -> None:
    rec = _scenario_change_diff(delta=5)
    out = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    md = mod.render_proposal_md(rec, out, recipient_ref_id="POI-LEG-ENISA-LEAD-2026", forced=False, first_cycle_explicit=False)
    assert "Material-change proposal" in md
    assert "POI-LEG-ENISA-LEAD-2026" in md
    assert "min_changed_scenarios" in md
    # Must surface IRREVERSIBLE per-fire G-24-3 doctrine.
    assert "G-24-3" in md
    assert "IRREVERSIBLE" in md
    # Must not inline real recipient email patterns.
    assert "@" not in md.split("Recipient")[1].split("\n")[0]


def test_render_proposal_md_force_path() -> None:
    rec = _no_change_diff_record()
    out = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    md = mod.render_proposal_md(rec, out, recipient_ref_id=None, forced=True, first_cycle_explicit=False)
    assert "Forced proposal" in md
    assert "R-55-5" in md


def test_render_proposal_md_first_cycle_path() -> None:
    rec = _no_change_diff_record()
    rec["is_first_cycle"] = True
    out = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    md = mod.render_proposal_md(rec, out, recipient_ref_id=None, forced=False, first_cycle_explicit=True)
    assert "First-cycle proposal" in md
    assert "no last-sent baseline" in md.lower()


# -------------------- loop-history append --------------------


def test_append_loop_history_creates_file_with_header(tmp_path: Path) -> None:
    rec = _no_change_diff_record()
    evaluation = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    history = mod.append_loop_history(tmp_path, rec, evaluation, proposed=False, proposal_path=None)
    text = history.read_text(encoding="utf-8")
    assert "# Loop history" in text
    assert "D-IH-55-E" in text
    # Single row appended.
    rows = [line for line in text.splitlines() if line.startswith("|") and not line.startswith("|:") and not line.startswith("| date")]
    assert len(rows) == 1
    assert "no" in rows[0]


def test_append_loop_history_records_proposed_yes(tmp_path: Path) -> None:
    rec = _scenario_change_diff(delta=5)
    evaluation = mod.evaluate_thresholds(rec, dict(mod.DEFAULT_THRESHOLDS))
    proposal = tmp_path / "proposal-advisor-send-2026-05-03.md"
    proposal.write_text("dummy", encoding="utf-8")
    history = mod.append_loop_history(tmp_path, rec, evaluation, proposed=True, proposal_path=proposal)
    text = history.read_text(encoding="utf-8")
    assert "YES" in text
    assert "proposal-advisor-send-2026-05-03.md" in text


# -------------------- main() integration --------------------


def test_main_use_defaults_no_change_logs_silence(tmp_path: Path) -> None:
    rec = _no_change_diff_record()
    diff_path = tmp_path / "diff.json"
    diff_path.write_text(json.dumps(rec), encoding="utf-8")
    out_dir = tmp_path / "reports"
    rc = mod.main(["--diff", str(diff_path), "--out-dir", str(out_dir), "--use-defaults"])
    assert rc == 0
    history = out_dir / "loop-history.md"
    assert history.is_file()
    text = history.read_text(encoding="utf-8")
    # Silence path: no proposal file, "no" recorded.
    proposals = list(out_dir.glob("proposal-advisor-send-*.md"))
    assert proposals == []
    assert "no" in text


def test_main_use_defaults_change_emits_proposal(tmp_path: Path) -> None:
    rec = _scenario_change_diff(delta=5)
    diff_path = tmp_path / "diff.json"
    diff_path.write_text(json.dumps(rec), encoding="utf-8")
    out_dir = tmp_path / "reports"
    rc = mod.main(
        [
            "--diff",
            str(diff_path),
            "--out-dir",
            str(out_dir),
            "--use-defaults",
            "--recipient",
            "POI-LEG-ENISA-LEAD-2026",
        ]
    )
    assert rc == 0
    proposals = list(out_dir.glob("proposal-advisor-send-*.md"))
    assert len(proposals) == 1
    body = proposals[0].read_text(encoding="utf-8")
    assert "POI-LEG-ENISA-LEAD-2026" in body
    history = (out_dir / "loop-history.md").read_text(encoding="utf-8")
    assert "YES" in history


def test_main_force_proposal_overrides_silence(tmp_path: Path) -> None:
    rec = _no_change_diff_record()
    diff_path = tmp_path / "diff.json"
    diff_path.write_text(json.dumps(rec), encoding="utf-8")
    out_dir = tmp_path / "reports"
    rc = mod.main(
        [
            "--diff",
            str(diff_path),
            "--out-dir",
            str(out_dir),
            "--use-defaults",
            "--force-proposal",
        ]
    )
    assert rc == 0
    proposals = list(out_dir.glob("proposal-advisor-send-*.md"))
    assert len(proposals) == 1
    assert "Forced proposal" in proposals[0].read_text(encoding="utf-8")


def test_main_first_cycle_proposes_only_when_allowed(tmp_path: Path) -> None:
    rec = _no_change_diff_record()
    rec["is_first_cycle"] = True
    diff_path = tmp_path / "diff.json"
    diff_path.write_text(json.dumps(rec), encoding="utf-8")
    out_dir = tmp_path / "reports"

    # Without --allow-first-cycle: silence path.
    rc = mod.main(["--diff", str(diff_path), "--out-dir", str(out_dir), "--use-defaults"])
    assert rc == 0
    assert list(out_dir.glob("proposal-advisor-send-*.md")) == []

    # With --allow-first-cycle: proposal path.
    out_dir2 = tmp_path / "reports2"
    rc = mod.main(
        ["--diff", str(diff_path), "--out-dir", str(out_dir2), "--use-defaults", "--allow-first-cycle"]
    )
    assert rc == 0
    proposals = list(out_dir2.glob("proposal-advisor-send-*.md"))
    assert len(proposals) == 1
    assert "First-cycle proposal" in proposals[0].read_text(encoding="utf-8")


def test_main_dry_run_writes_nothing(tmp_path: Path) -> None:
    rec = _scenario_change_diff(delta=5)
    diff_path = tmp_path / "diff.json"
    diff_path.write_text(json.dumps(rec), encoding="utf-8")
    out_dir = tmp_path / "reports"
    rc = mod.main(
        ["--diff", str(diff_path), "--out-dir", str(out_dir), "--use-defaults", "--dry-run"]
    )
    assert rc == 0
    # --dry-run must not create any files.
    assert not out_dir.exists() or list(out_dir.glob("**/*")) == []


def test_main_returns_1_on_unreadable_diff(tmp_path: Path) -> None:
    rc = mod.main(["--diff", str(tmp_path / "missing.json"), "--use-defaults"])
    assert rc == 1


def test_main_returns_1_when_policy_id_unknown(tmp_path: Path) -> None:
    """When --use-defaults is NOT set and the policy_id is not in the CSV."""
    rec = _no_change_diff_record()
    diff_path = tmp_path / "diff.json"
    diff_path.write_text(json.dumps(rec), encoding="utf-8")
    fake_csv = tmp_path / "fake.csv"
    fake_csv.write_text(
        "policy_id,policy_class,applies_to_schema,applies_to_table,policy_text,cadence,owner_role,last_review,next_review,topic_ids,notes\n",
        encoding="utf-8",
    )
    rc = mod.main(
        [
            "--diff",
            str(diff_path),
            "--policy",
            "POL-NOT-PRESENT",
            "--policy-csv",
            str(fake_csv),
            "--out-dir",
            str(tmp_path / "reports"),
        ]
    )
    assert rc == 1
