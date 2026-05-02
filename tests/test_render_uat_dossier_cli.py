"""Initiative 48 P2 tests — scripts/render_uat_dossier.py CLI surface.

Coverage:
- --help shows expected flags
- --mode tier-b refused without AKOS_DOSSIER_TIER_B=1 env (D-IH-48-L)
- --mode snapshot writes dossier.md + manifest.json to per-run dir
- --format all writes md + html (PDF placeholder until P4)
- --quiet suppresses per-section progress (stdout has DONE block)
- --json emits manifest to stdout instead of progress prose
- --persona filter propagates to dossier filter section
- --initiative filter propagates to dossier filter section
- Output dir name pattern artifacts/uat-dossier/uat-dossier-<UTC>/
- Manifest contains required keys (sha256 + section_metrics + run_id + git_sha)
- HTML output is valid (contains <html>, <body>, brand CSS variables, <details>)
- Section ordering invariant in dossier.md (Section 1..12 in order)
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "render_uat_dossier.py"


def _run(args: list[str], env: dict | None = None) -> subprocess.CompletedProcess:
    full_env = dict(os.environ)
    if env is not None:
        full_env.update(env)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8",
        env=full_env, timeout=60,
    )


# ---------------------------------------------------------------------------
# CLI surface
# ---------------------------------------------------------------------------

def test_help_includes_required_flags() -> None:
    res = _run(["--help"])
    assert res.returncode == 0
    for flag in ("--mode", "--format", "--initiative", "--persona", "--since",
                 "--max-staleness-hours", "--max-spend", "--screenshots",
                 "--gh-pr-comment", "--out-dir", "--quiet", "--json"):
        assert flag in res.stdout, f"missing flag {flag}"


# ---------------------------------------------------------------------------
# Tier B opt-in (D-IH-48-L)
# ---------------------------------------------------------------------------

def test_tier_b_refused_without_optin(monkeypatch: pytest.MonkeyPatch) -> None:
    """D-IH-48-L: --mode tier-b requires AKOS_DOSSIER_TIER_B=1."""
    monkeypatch.delenv("AKOS_DOSSIER_TIER_B", raising=False)
    res = _run(["--mode", "tier-b", "--quiet"], env={"AKOS_DOSSIER_TIER_B": ""})
    assert res.returncode == 10
    assert "REFUSED" in res.stderr or "REFUSED" in res.stdout
    assert "AKOS_DOSSIER_TIER_B" in res.stderr or "AKOS_DOSSIER_TIER_B" in res.stdout


# ---------------------------------------------------------------------------
# Snapshot mode --format md
# ---------------------------------------------------------------------------

def test_snapshot_md_writes_files(tmp_path: Path) -> None:
    out_dir = tmp_path / "test-dossier"
    res = _run(["--mode", "snapshot", "--format", "md", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0, res.stderr + res.stdout
    assert (out_dir / "dossier.md").is_file()
    assert (out_dir / "manifest.json").is_file()


def test_snapshot_md_completes_under_30s(tmp_path: Path) -> None:
    """P2 acceptance: snapshot mode <30s on operator laptop."""
    import time
    out_dir = tmp_path / "perf-test"
    started = time.perf_counter()
    res = _run(["--mode", "snapshot", "--format", "md", "--out-dir", str(out_dir), "--quiet"])
    elapsed = time.perf_counter() - started
    assert res.returncode == 0
    assert elapsed < 30, f"snapshot mode took {elapsed:.1f}s; should be <30s"


# ---------------------------------------------------------------------------
# Multi-format --format all
# ---------------------------------------------------------------------------

def test_format_all_writes_md_pdf_html(tmp_path: Path) -> None:
    """P5: --format all writes md + html + pdf (or pdf sidecar fallback)."""
    out_dir = tmp_path / "all-formats"
    res = _run(["--mode", "snapshot", "--format", "all", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0, res.stderr
    assert (out_dir / "dossier.md").is_file()
    assert (out_dir / "dossier.html").is_file()
    # PDF (or sidecar fallback when WeasyPrint unavailable)
    assert (out_dir / "dossier.pdf").is_file() or (out_dir / "dossier.pdf.md").is_file()
    assert (out_dir / "manifest.json").is_file()


# ---------------------------------------------------------------------------
# --json output
# ---------------------------------------------------------------------------

def test_json_flag_emits_manifest_to_stdout(tmp_path: Path) -> None:
    out_dir = tmp_path / "json-test"
    res = _run(["--mode", "snapshot", "--format", "md", "--out-dir", str(out_dir), "--quiet", "--json"])
    assert res.returncode == 0
    payload = json.loads(res.stdout)
    for key in ("run_id", "started_at", "git_sha", "mode", "section_metrics", "files"):
        assert key in payload


# ---------------------------------------------------------------------------
# Filter propagation
# ---------------------------------------------------------------------------

def test_persona_filter_in_dossier_md(tmp_path: Path) -> None:
    out_dir = tmp_path / "persona-test"
    res = _run(["--mode", "snapshot", "--format", "md", "--out-dir", str(out_dir),
                "--persona", "PERSONA-INVESTOR-COLD", "--quiet"])
    assert res.returncode == 0
    md = (out_dir / "dossier.md").read_text(encoding="utf-8")
    assert "## Filter" in md
    assert "PERSONA-INVESTOR-COLD" in md


def test_initiative_filter_in_dossier_md(tmp_path: Path) -> None:
    out_dir = tmp_path / "init-test"
    res = _run(["--mode", "snapshot", "--format", "md", "--out-dir", str(out_dir),
                "--initiative", "47", "--quiet"])
    assert res.returncode == 0
    md = (out_dir / "dossier.md").read_text(encoding="utf-8")
    assert "## Filter" in md
    assert "initiative: `47`" in md


# ---------------------------------------------------------------------------
# Manifest shape
# ---------------------------------------------------------------------------

def test_manifest_has_section_metrics_for_all_12(tmp_path: Path) -> None:
    out_dir = tmp_path / "manifest-test"
    res = _run(["--mode", "snapshot", "--format", "md", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0
    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    section_metrics = manifest["section_metrics"]
    for sid in range(1, 13):
        key = f"section_{sid:02d}"
        assert key in section_metrics, f"missing {key} in manifest section_metrics"


def test_manifest_md_sha256_matches_file_content(tmp_path: Path) -> None:
    import hashlib
    out_dir = tmp_path / "sha-test"
    res = _run(["--mode", "snapshot", "--format", "md", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0
    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    md_content = (out_dir / "dossier.md").read_text(encoding="utf-8")
    expected_sha = hashlib.sha256(md_content.encode("utf-8")).hexdigest()
    assert manifest["files"]["dossier.md"]["sha256"] == expected_sha


# ---------------------------------------------------------------------------
# Section ordering invariant (D-IH-48-D)
# ---------------------------------------------------------------------------

def test_dossier_md_sections_in_1_to_12_order(tmp_path: Path) -> None:
    out_dir = tmp_path / "order-test"
    res = _run(["--mode", "snapshot", "--format", "md", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0
    md = (out_dir / "dossier.md").read_text(encoding="utf-8")
    positions = []
    for sid in range(1, 13):
        # Match either "## Section N — <name>" or as STALE/PLACEHOLDER same header
        m = re.search(rf"^## Section {sid} — ", md, re.MULTILINE)
        assert m, f"Section {sid} header missing"
        positions.append(m.start())
    assert positions == sorted(positions), "sections must render in 1..12 order"


# ---------------------------------------------------------------------------
# HTML output validity
# ---------------------------------------------------------------------------

def test_html_output_contains_brand_css_vars(tmp_path: Path) -> None:
    out_dir = tmp_path / "html-test"
    res = _run(["--mode", "snapshot", "--format", "all", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0
    html = (out_dir / "dossier.html").read_text(encoding="utf-8")
    assert "<!doctype html>" in html.lower()
    assert "<html" in html.lower()
    assert "<body>" in html
    assert "--c-accent-primary" in html  # brand CSS variable derived from BRAND_TOKENS_LIGHT
    assert "<details" in html  # collapsible sections (D-IH-48-I)


def test_html_output_no_external_references(tmp_path: Path) -> None:
    """R-48-3 + D-IH-48-I: standalone-file invariant. No CDN / JS / external fonts."""
    out_dir = tmp_path / "no-cdn-test"
    res = _run(["--mode", "snapshot", "--format", "all", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0
    html = (out_dir / "dossier.html").read_text(encoding="utf-8")
    # No external script/style/img/link href to remote URL
    for forbidden in ("<script", "https://cdn.", "https://fonts.googleapis", "<link rel=\"stylesheet\""):
        assert forbidden not in html, f"standalone-file invariant violated: {forbidden!r} in HTML"


def test_html_output_includes_section_summary_strings(tmp_path: Path) -> None:
    out_dir = tmp_path / "html-sum-test"
    res = _run(["--mode", "snapshot", "--format", "all", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0
    html = (out_dir / "dossier.html").read_text(encoding="utf-8")
    # All 12 section headers should appear as <summary> contents
    for sid in range(1, 13):
        assert f"Section {sid}" in html


# ---------------------------------------------------------------------------
# --quiet flag
# ---------------------------------------------------------------------------

def test_quiet_flag_suppresses_section_progress(tmp_path: Path) -> None:
    """With --quiet, the per-section gathering log lines are suppressed."""
    out_dir = tmp_path / "quiet-test"
    res = _run(["--mode", "snapshot", "--format", "md", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0
    # The "[Section NN] gathering" prefix should NOT appear when --quiet
    assert "[Section 02]" not in res.stderr


def test_no_quiet_emits_per_section_progress(tmp_path: Path) -> None:
    out_dir = tmp_path / "verbose-test"
    res = _run(["--mode", "snapshot", "--format", "md", "--out-dir", str(out_dir)])
    assert res.returncode == 0
    # Per-section progress lines emit on stderr
    assert "[Section 02]" in res.stderr
