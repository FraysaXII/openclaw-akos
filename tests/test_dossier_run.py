"""Initiative 48 P1 tests — DossierRun + DossierFilter + section assembly.

Coverage:
- DossierRun dataclass shape + defaults
- DossierFilter dataclass
- DossierSectionResult dataclass
- to_markdown emits Sections 1..12 in order (D-IH-48-D invariant)
- to_manifest produces sha256 + section_metrics
- to_json round-trips
- resolve_run_dir produces UTC-stamped path
- resolve_max_dossier_usd reads MAX_DOSSIER_USD env (D-IH-48-L)
- is_tier_b_opted_in checks AKOS_DOSSIER_TIER_B=1 env (D-IH-48-L)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.dossier.run import (
    ARTIFACTS_BASE,
    DEFAULT_MAX_DOSSIER_USD,
    DEFAULT_MAX_STALENESS_HOURS,
    DEFAULT_TREND_WINDOW,
    VALID_FORMATS,
    VALID_MODES,
    DossierFilter,
    DossierRun,
    DossierSectionResult,
    is_tier_b_opted_in,
    resolve_max_dossier_usd,
    resolve_run_dir,
)


# ---------------------------------------------------------------------------
# Constants + dataclass shape
# ---------------------------------------------------------------------------

def test_valid_modes_constant() -> None:
    """D-IH-48-C: snapshot|live|tier-b."""
    assert VALID_MODES == ("snapshot", "live", "tier-b")


def test_valid_formats_constant() -> None:
    """D-IH-48-B: md|pdf|html|all."""
    assert set(VALID_FORMATS) == {"md", "pdf", "html", "all"}


def test_default_max_dossier_usd_is_two() -> None:
    """D-IH-48-L: default $2/run."""
    assert DEFAULT_MAX_DOSSIER_USD == 2.0


def test_default_max_staleness_24h() -> None:
    """D-IH-48-E: default 24h cache freshness."""
    assert DEFAULT_MAX_STALENESS_HOURS == 24


def test_default_trend_window_10() -> None:
    """Section 11 default N=10."""
    assert DEFAULT_TREND_WINDOW == 10


def test_dossier_filter_defaults_all_none() -> None:
    f = DossierFilter()
    assert f.initiative is None
    assert f.persona_id is None
    assert f.since is None


def test_dossier_run_default_run_id_format() -> None:
    r = DossierRun()
    assert r.run_id.startswith("dossier-")
    assert len(r.run_id) > len("dossier-")


def test_dossier_run_default_overall_pass() -> None:
    r = DossierRun()
    assert r.overall_status == "PASS"


def test_dossier_run_add_failure_propagates() -> None:
    r = DossierRun()
    r.add(DossierSectionResult(section_id=2, name="Schema", status="FAIL"))
    assert r.overall_status == "FAIL"


def test_dossier_run_add_pass_does_not_change_status() -> None:
    r = DossierRun()
    r.add(DossierSectionResult(section_id=1, name="Exec", status="PASS"))
    assert r.overall_status == "PASS"


def test_dossier_run_section_by_id_lookup() -> None:
    r = DossierRun()
    r.add(DossierSectionResult(section_id=3, name="Eval", status="PASS"))
    assert r.section_by_id(3).name == "Eval"
    assert r.section_by_id(99) is None


# ---------------------------------------------------------------------------
# to_markdown ordering (D-IH-48-D invariant)
# ---------------------------------------------------------------------------

def test_to_markdown_renders_sections_in_order_1_to_12() -> None:
    """Sections must render 1..12 regardless of add() order."""
    r = DossierRun()
    # Add OUT OF ORDER intentionally
    for sid in [3, 1, 12, 7, 5, 2, 9, 4, 6, 8, 11, 10]:
        r.add(DossierSectionResult(
            section_id=sid, name=f"Section {sid}",
            markdown=f"## Section {sid} — Section {sid}\n\nbody-{sid}\n",
        ))
    out = r.to_markdown()
    # Find positions of each "## Section N" header; assert ascending
    positions = []
    for sid in range(1, 13):
        pos = out.find(f"## Section {sid} — Section {sid}")
        assert pos > 0, f"section {sid} header missing"
        positions.append(pos)
    assert positions == sorted(positions)


def test_to_markdown_emits_filter_block_when_set() -> None:
    r = DossierRun(filter=DossierFilter(initiative="47", persona_id="PERSONA-INVESTOR-COLD"))
    out = r.to_markdown()
    assert "## Filter" in out
    assert "initiative: `47`" in out
    assert "persona_id: `PERSONA-INVESTOR-COLD`" in out


def test_to_markdown_omits_filter_block_when_unset() -> None:
    r = DossierRun()
    out = r.to_markdown()
    assert "## Filter" not in out


def test_to_markdown_includes_required_headers() -> None:
    r = DossierRun()
    out = r.to_markdown()
    assert "# AKOS Operator UAT Dossier" in out
    assert "run_id:" in out
    assert "started_at:" in out
    assert "git_sha:" in out
    assert "mode:" in out
    assert "overall_status:" in out


# ---------------------------------------------------------------------------
# to_manifest sha256 + section metrics
# ---------------------------------------------------------------------------

def test_to_manifest_includes_required_top_level_keys() -> None:
    r = DossierRun()
    m = r.to_manifest(md_text="# test")
    for key in ("run_id", "started_at", "git_sha", "mode", "formats",
                "overall_status", "section_metrics", "files"):
        assert key in m


def test_to_manifest_md_sha256_consistent() -> None:
    r = DossierRun()
    m1 = r.to_manifest(md_text="# test")
    m2 = r.to_manifest(md_text="# test")
    assert m1["files"]["dossier.md"]["sha256"] == m2["files"]["dossier.md"]["sha256"]
    assert m1["files"]["dossier.md"]["char_count"] == 6


def test_to_manifest_section_metrics_keyed_by_padded_id() -> None:
    r = DossierRun()
    r.add(DossierSectionResult(section_id=1, name="Exec", metrics={"x": 1}))
    r.add(DossierSectionResult(section_id=12, name="Appx", metrics={"y": 2}))
    m = r.to_manifest()
    assert "section_01" in m["section_metrics"]
    assert "section_12" in m["section_metrics"]
    assert m["section_metrics"]["section_01"]["metrics"] == {"x": 1}


def test_to_json_round_trip() -> None:
    r = DossierRun()
    r.add(DossierSectionResult(section_id=1, name="Exec"))
    parsed = json.loads(r.to_json())
    assert parsed["overall_status"] == "PASS"
    assert isinstance(parsed["section_results"], list)
    assert parsed["section_results"][0]["section_id"] == 1


# ---------------------------------------------------------------------------
# resolve_run_dir
# ---------------------------------------------------------------------------

def test_resolve_run_dir_uses_artifacts_base() -> None:
    r = DossierRun()
    out = resolve_run_dir(r)
    assert out.parent == ARTIFACTS_BASE
    assert out.name.startswith("uat-dossier-")


def test_resolve_run_dir_uses_started_at_utc() -> None:
    """The folder name encodes the UTC timestamp from started_at."""
    fixed_iso = "2026-05-02T03:30:45+00:00"
    r = DossierRun(started_at=fixed_iso)
    out = resolve_run_dir(r)
    assert out.name == "uat-dossier-20260502T033045Z"


# ---------------------------------------------------------------------------
# Env var helpers (D-IH-48-L)
# ---------------------------------------------------------------------------

def test_resolve_max_dossier_usd_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MAX_DOSSIER_USD", raising=False)
    assert resolve_max_dossier_usd() == 2.0


def test_resolve_max_dossier_usd_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MAX_DOSSIER_USD", "5.5")
    assert resolve_max_dossier_usd() == 5.5


def test_resolve_max_dossier_usd_invalid_falls_to_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MAX_DOSSIER_USD", "abc")
    assert resolve_max_dossier_usd() == 2.0


def test_is_tier_b_opted_in_requires_exact_one(monkeypatch: pytest.MonkeyPatch) -> None:
    """D-IH-48-L: must be exactly '1' (not 'true', not '0')."""
    monkeypatch.delenv("AKOS_DOSSIER_TIER_B", raising=False)
    assert is_tier_b_opted_in() is False
    monkeypatch.setenv("AKOS_DOSSIER_TIER_B", "1")
    assert is_tier_b_opted_in() is True
    monkeypatch.setenv("AKOS_DOSSIER_TIER_B", "true")
    assert is_tier_b_opted_in() is False
    monkeypatch.setenv("AKOS_DOSSIER_TIER_B", "0")
    assert is_tier_b_opted_in() is False
