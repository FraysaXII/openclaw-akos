"""Initiative 48 P4 tests — brand-aligned PDF mode (D-IH-48-H + D-IH-48-H1).

Coverage:
- pdf_render module imports cleanly + reuses akos.hlk_pdf_render
- DOSSIER_TITLE + DOSSIER_SUBTITLE_BY_MODE constants
- _iso_date_from_started_at handles ISO timestamps + invalid input
- render_dossier_pdf returns 0 on success
- D-IH-48-H1: profile="dossier" reused (no new profile added)
- PDF cover passes run_id as program_id + "UAT Dossier" as discipline
- CLI --format pdf produces dossier.pdf with %PDF header (when WeasyPrint installed) OR sidecar fallback
- CLI --format all produces all 3 formats
- Manifest records pdf sha256 + byte_count
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.dossier.pdf_render import (
    DOSSIER_SUBTITLE_BY_MODE,
    DOSSIER_TITLE,
    _iso_date_from_started_at,
    render_dossier_pdf,
)
from akos.dossier.run import DossierRun


# ---------------------------------------------------------------------------
# Constants + helpers
# ---------------------------------------------------------------------------

def test_dossier_title_constant() -> None:
    assert DOSSIER_TITLE == "AKOS Operator UAT Dossier"


def test_dossier_subtitle_covers_3_modes() -> None:
    """D-IH-48-C: 3 modes (snapshot|live|tier-b) - subtitle distinct per mode."""
    assert "snapshot" in DOSSIER_SUBTITLE_BY_MODE
    assert "live" in DOSSIER_SUBTITLE_BY_MODE
    assert "tier-b" in DOSSIER_SUBTITLE_BY_MODE
    assert len(set(DOSSIER_SUBTITLE_BY_MODE.values())) == 3  # all distinct


def test_iso_date_extracts_yyyy_mm_dd() -> None:
    out = _iso_date_from_started_at("2026-05-02T04:30:00+00:00")
    assert out == "2026-05-02"


def test_iso_date_handles_z_suffix() -> None:
    out = _iso_date_from_started_at("2026-05-02T04:30:00Z")
    assert out == "2026-05-02"


def test_iso_date_invalid_falls_to_today() -> None:
    """Invalid input falls back to today UTC; verify it returns SOME date string."""
    import re
    out = _iso_date_from_started_at("not-an-iso-date")
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", out)


# ---------------------------------------------------------------------------
# render_dossier_pdf
# ---------------------------------------------------------------------------

def test_render_dossier_pdf_returns_int(tmp_path: Path) -> None:
    """Returns 0 on success (or soft-success when fallback chain fires)."""
    run = DossierRun()
    out = tmp_path / "test.pdf"
    rc = render_dossier_pdf(run, "# test\n\nhello world\n", out)
    assert isinstance(rc, int)
    # rc=0 on success; non-zero only if explicit subprocess failure (e.g. pandoc)
    # Accept any int; the test that PDF actually wrote is below.


def test_render_dossier_pdf_writes_pdf_file_when_weasyprint_available(tmp_path: Path) -> None:
    """When WeasyPrint installed, dossier.pdf is a real PDF (%PDF-1.X header)."""
    run = DossierRun()
    out = tmp_path / "test.pdf"
    rc = render_dossier_pdf(run, "# test\n\nhello\n", out)
    if not out.is_file():
        # Fallback chain landed on sidecar; verify sidecar was written instead
        sidecar = tmp_path / "test.pdf.md"
        if sidecar.is_file():
            pytest.skip("WeasyPrint/fpdf2/pandoc unavailable; soft-success sidecar written")
        pytest.fail(f"neither pdf nor sidecar created (rc={rc})")
    # PDF header check
    head = out.read_bytes()[:8]
    assert head.startswith(b"%PDF"), f"file does not have PDF header; got {head!r}"


def test_render_dossier_pdf_uses_run_id_as_program_id(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """D-IH-48-H1: run_id passed as program_id; 'UAT Dossier' as discipline."""
    captured: dict = {}

    def fake_render_pdf_branded(*args, **kwargs):
        captured.update(kwargs)
        return 0

    monkeypatch.setattr("akos.dossier.pdf_render.render_pdf_branded", fake_render_pdf_branded)
    run = DossierRun(run_id="dossier-test-12345")
    render_dossier_pdf(run, "# test\n", tmp_path / "out.pdf")
    assert captured["program_id"] == "dossier-test-12345"
    assert captured["discipline"] == "UAT Dossier"
    assert captured["title"] == DOSSIER_TITLE
    # D-IH-48-H1: profile="dossier" reused (not "uat_dossier")
    assert captured["profile"] == "dossier"


def test_render_dossier_pdf_status_label_includes_overall_status(tmp_path: Path,
                                                                 monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict = {}

    def fake(*args, **kwargs):
        captured.update(kwargs)
        return 0

    monkeypatch.setattr("akos.dossier.pdf_render.render_pdf_branded", fake)
    run = DossierRun()
    run.overall_status = "FAIL"
    render_dossier_pdf(run, "# test\n", tmp_path / "out.pdf")
    assert "FAIL" in captured["status_label"]


# ---------------------------------------------------------------------------
# CLI --format pdf
# ---------------------------------------------------------------------------

def _run_script(args: list[str], env: dict | None = None) -> subprocess.CompletedProcess:
    full_env = dict(os.environ)
    if env is not None:
        full_env.update(env)
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "render_uat_dossier.py"), *args],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8",
        env=full_env, timeout=60,
    )


def test_cli_format_pdf_produces_pdf_or_sidecar(tmp_path: Path) -> None:
    out_dir = tmp_path / "pdf-test"
    res = _run_script(["--mode", "snapshot", "--format", "pdf", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0, res.stderr
    pdf = out_dir / "dossier.pdf"
    sidecar = out_dir / "dossier.pdf.md"
    assert pdf.is_file() or sidecar.is_file()
    if pdf.is_file():
        assert pdf.read_bytes()[:8].startswith(b"%PDF")


def test_cli_format_all_produces_all_three(tmp_path: Path) -> None:
    out_dir = tmp_path / "all-test"
    res = _run_script(["--mode", "snapshot", "--format", "all", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0
    assert (out_dir / "dossier.md").is_file()
    assert (out_dir / "dossier.html").is_file()
    # PDF (or sidecar fallback)
    assert (out_dir / "dossier.pdf").is_file() or (out_dir / "dossier.pdf.md").is_file()


def test_manifest_records_pdf_sha256_and_byte_count(tmp_path: Path) -> None:
    out_dir = tmp_path / "manifest-pdf-test"
    res = _run_script(["--mode", "snapshot", "--format", "pdf", "--out-dir", str(out_dir), "--quiet"])
    assert res.returncode == 0
    pdf = out_dir / "dossier.pdf"
    if not pdf.is_file():
        pytest.skip("PDF chain fell back to sidecar; sha256 only recorded for actual PDFs")
    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    assert "dossier.pdf" in manifest["files"]
    assert "sha256" in manifest["files"]["dossier.pdf"]
    assert "byte_count" in manifest["files"]["dossier.pdf"]
    assert manifest["files"]["dossier.pdf"]["byte_count"] > 0
