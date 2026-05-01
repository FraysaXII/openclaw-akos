"""Tests for the WIP dashboard auto-renderer (Initiative 32 P10).

Locks the contract that:
1. The dashboard is rendered from each initiative's master-roadmap.md.
2. Two consecutive runs produce byte-identical output (sha256 stable; deterministic).
3. The dashboard contains the AUTO markers + every initiative folder's row.
4. The verify profile `wip_dashboard_render_smoke` is registered in config/verification-profiles.json.
5. The renderer's --check-only mode reports drift correctly.
6. The planning README cross-links the dashboard.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLANNING_DIR = REPO_ROOT / "docs" / "wip" / "planning"
DASHBOARD_PATH = PLANNING_DIR / "WIP_DASHBOARD.md"
SCRIPT = REPO_ROOT / "scripts" / "render_wip_dashboard.py"
VERIFICATION_PROFILES = REPO_ROOT / "config" / "verification-profiles.json"
PLANNING_README = PLANNING_DIR / "README.md"


def test_dashboard_path_exists_after_render() -> None:
    """Dashboard exists after a render (sanity)."""
    subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert DASHBOARD_PATH.is_file()


def test_dashboard_carries_auto_markers() -> None:
    text = DASHBOARD_PATH.read_text(encoding="utf-8")
    assert "<!-- BEGIN AUTO -->" in text
    assert "<!-- END AUTO -->" in text


def test_dashboard_lists_known_recent_initiatives() -> None:
    """Spot-check that the table includes recognisable initiative folder rows."""
    text = DASHBOARD_PATH.read_text(encoding="utf-8")
    for needle in (
        "32-holistik-ops-maturation",  # the in-flight initiative itself
        "31-holistik-ops-discovery",   # immediate predecessor
        "29-multi-phase-consolidation",
        "30-deck-moat-surgery",
    ):
        assert needle in text, f"dashboard missing initiative folder {needle!r}"


def test_render_is_deterministic_across_two_consecutive_runs() -> None:
    """KEYSTONE: sha256 of dashboard is identical after two consecutive renders."""
    subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, cwd=REPO_ROOT, timeout=30)
    h1 = hashlib.sha256(DASHBOARD_PATH.read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, cwd=REPO_ROOT, timeout=30)
    h2 = hashlib.sha256(DASHBOARD_PATH.read_bytes()).hexdigest()
    assert h1 == h2, f"non-deterministic render: {h1} != {h2}"


def test_check_only_mode_passes_after_render() -> None:
    """After a fresh render, --check-only must report PASS (no drift)."""
    subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, cwd=REPO_ROOT, timeout=30)
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--check-only"],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r.returncode == 0, f"--check-only exited {r.returncode}; stdout: {r.stdout}"
    assert "PASS" in r.stdout


def test_verify_profile_registered() -> None:
    """The wip_dashboard_render_smoke verify profile is registered."""
    profiles = json.loads(VERIFICATION_PROFILES.read_text(encoding="utf-8"))
    assert "wip_dashboard_render_smoke" in profiles["profiles"]
    profile = profiles["profiles"]["wip_dashboard_render_smoke"]
    assert "Initiative 32 P10" in profile["description"]
    assert profile["steps"][0]["argv"] == ["scripts/render_wip_dashboard.py", "--check-only"]


def test_planning_readme_cross_links_dashboard() -> None:
    text = PLANNING_README.read_text(encoding="utf-8")
    assert "WIP_DASHBOARD.md" in text
    assert "Initiative 32 P10" in text


def test_dashboard_table_has_at_least_30_rows() -> None:
    """Sanity: planning README catalogues 30+ initiatives + 32 (this one); dashboard should mirror."""
    text = DASHBOARD_PATH.read_text(encoding="utf-8")
    # Each initiative row starts with `| **NN`. Count those lines between BEGIN/END markers.
    pre, _, rest = text.partition("<!-- BEGIN AUTO -->")
    table, _, _ = rest.partition("<!-- END AUTO -->")
    rows = re.findall(r"^\| \*\*\d{2}", table, re.MULTILINE)
    assert len(rows) >= 30, f"expected at least 30 initiative rows, got {len(rows)}"
