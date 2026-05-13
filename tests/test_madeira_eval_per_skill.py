"""Tests for the per-skill eval scorecard + 5 drift canaries (Initiative 32 P9).

Locks the contract that:
1. The scorecard generator runs cleanly against the 5 baseline JSONs (canary 2 silent).
2. The 5 baseline JSONs exist and parse with the expected fields.
3. Each baseline matches the SKILL_REGISTRY.csv eval_baseline_pct.
4. The synthetic regression test trips canary 2 when a 3pp drop is injected on the
   highest-baseline skill (validator drift = highest-impact).
5. Json output mode emits a valid structured report with overall_status field.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "eval_per_skill.py"
BASELINES_DIR = REPO_ROOT / "config" / "eval-baselines"
SKILL_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "SKILL_REGISTRY.csv"


def test_baseline_directory_exists() -> None:
    assert BASELINES_DIR.is_dir()


def test_five_baseline_files_exist() -> None:
    baselines = sorted(BASELINES_DIR.glob("skill_*.json"))
    assert len(baselines) == 5, f"expected 5 skill baseline JSONs, got {len(baselines)}"


def test_baseline_files_parse_with_required_fields() -> None:
    required_fields = {"skill_id", "name", "eval_baseline_pct", "frozen_at", "agents_supported", "axes_consumed"}
    for p in BASELINES_DIR.glob("skill_*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        missing = required_fields - set(data.keys())
        assert not missing, f"{p.name}: missing fields {missing}"


def test_baselines_match_skill_registry_csv() -> None:
    """Each baseline JSON's eval_baseline_pct equals the SKILL_REGISTRY.csv value."""
    with SKILL_CSV.open(encoding="utf-8", newline="") as fh:
        registry = {r["skill_id"]: float(r["eval_baseline_pct"]) for r in csv.DictReader(fh)}
    for p in BASELINES_DIR.glob("skill_*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        sid = data["skill_id"]
        assert sid in registry, f"baseline {sid!r} not in SKILL_REGISTRY.csv"
        assert data["eval_baseline_pct"] == registry[sid], (
            f"baseline {sid}: JSON {data['eval_baseline_pct']} != CSV {registry[sid]}"
        )


def test_scorecard_runs_clean_at_baseline() -> None:
    """Default invocation: 5 skills + 5 baselines, no current overrides → all PASS."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r.returncode == 0, f"eval_per_skill.py exited {r.returncode}; stderr: {r.stderr}"
    assert "OVERALL: PASS" in r.stdout
    assert "canary 2 trips:        0" in r.stdout


def test_scorecard_json_emits_valid_structure() -> None:
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r.returncode == 0
    payload = json.loads(r.stdout)
    assert payload["overall_status"] == "pass"
    assert payload["skills_total"] == 5
    assert payload["skills_with_baseline_json"] == 5
    assert payload["canary_2_trips_count"] == 0
    assert isinstance(payload["scorecard"], list)
    for row in payload["scorecard"]:
        for field in ("skill_id", "baseline_pct", "current_pct", "delta_pp", "canary_2_tripped"):
            assert field in row


def test_synthetic_regression_trips_canary_2_at_3pp_drop() -> None:
    """KEYSTONE: inject a 3pp drop on the verifier skill (highest baseline = highest impact)
    and assert canary 2 trips."""
    r = subprocess.run(
        [
            sys.executable, str(SCRIPT),
            "--json",
            "--current", "SKILL-VERIFIER-CHECK-V1=92.0",  # baseline 95.0 → -3.0pp drop
        ],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r.returncode != 0, "expected canary 2 to trip exit code"
    payload = json.loads(r.stdout)
    assert payload["overall_status"] == "fail"
    assert payload["canary_2_trips_count"] >= 1
    assert "SKILL-VERIFIER-CHECK-V1" in payload["canary_2_trips"]
    # The skill row should be marked tripped.
    by_id = {row["skill_id"]: row for row in payload["scorecard"]}
    assert by_id["SKILL-VERIFIER-CHECK-V1"]["canary_2_tripped"] is True
    assert by_id["SKILL-VERIFIER-CHECK-V1"]["delta_pp"] == -3.0


def test_threshold_override_changes_canary_sensitivity() -> None:
    """A drop of 1.5pp does not trip the default 2.0pp threshold but does trip 1.0pp."""
    # 1.5pp drop on madeira (baseline 92.0 → 90.5)
    # Default 2.0pp threshold: should NOT trip.
    r1 = subprocess.run(
        [sys.executable, str(SCRIPT), "--json", "--current", "SKILL-MADEIRA-LOOKUP-V1=90.5"],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r1.returncode == 0
    p1 = json.loads(r1.stdout)
    assert p1["canary_2_trips_count"] == 0

    # Same drop, threshold lowered to 1.0pp: SHOULD trip.
    r2 = subprocess.run(
        [
            sys.executable, str(SCRIPT), "--json",
            "--threshold", "1.0",
            "--current", "SKILL-MADEIRA-LOOKUP-V1=90.5",
        ],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r2.returncode != 0
    p2 = json.loads(r2.stdout)
    assert "SKILL-MADEIRA-LOOKUP-V1" in p2["canary_2_trips"]


def test_canary_4_documented_in_skill_validator() -> None:
    """Canary 4 (validator FK reject) is the existing P2 validator; smoke-check it loads.

    The full validator behaviour is locked in tests/test_skill_registry.py — here we
    confirm Canary 4 is a real artefact (the validator script exists and runs)."""
    validator = REPO_ROOT / "scripts" / "validate_skill_registry.py"
    assert validator.is_file()
    r = subprocess.run(
        [sys.executable, str(validator)],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r.returncode == 0
    assert "PASS" in r.stdout
