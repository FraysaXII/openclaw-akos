"""Initiative 48 — Operator Console (qualitative companion) tests.

Covers ``akos.dossier.console_render.render_console_html`` end-to-end:
- standalone-file invariant (no <script>, no remote URLs, no remote fonts)
- panel presence (A..I anchors) when full SSOT is available
- graceful degradation (missing index.json -> "INSUFFICIENT-DATA" message; not crash)
- brand SSOT reused (CSS variables present)
- persona heatmap renders 17 PERSONA_SCENARIO_REGISTRY rows when CSV available
- scenario sample cards include real prompt text from the registry
- decision table includes at least one D-IH-48 row when decision-log.md exists
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from akos.dossier.console_render import (
    REPO_ROOT,
    PERSONA_SCENARIO_CSV,
    PLANNING_DIR,
    render_console_html,
)
from akos.dossier.run import DossierFilter, DossierRun, DossierSectionResult


# -------------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------------


def _mk_run(*, run_id: str = "dossier-test-console") -> DossierRun:
    run = DossierRun(
        run_id=run_id,
        git_sha="testgitsha000000",
        mode="snapshot",
        formats=("html",),
        filter=DossierFilter(),
    )
    base_sections = [
        ("Executive summary", "PASS"),
        ("Schema + governance", "PASS"),
        ("Eval health", "SKIP"),
        ("Persona library + calibration", "PASS"),
        ("Adversarial coverage", "SKIP"),
        ("Recovery + chaos", "PASS"),
        ("Drift canaries", "SKIP"),
        ("Operational health", "PASS"),
        ("External repo health", "PASS"),
        ("Open governance debt", "PASS"),
        ("Trend lines", "INFO"),
        ("Appendix", "INFO"),
    ]
    for sid, (name, status) in enumerate(base_sections, start=1):
        run.add(DossierSectionResult(
            section_id=sid,
            name=name,
            status=status,
            data_age_seconds=float(sid * 60),
            metrics={},
        ))
    run.elapsed_ms = 423
    return run


@pytest.fixture
def empty_index(tmp_path: Path) -> Path:
    p = tmp_path / "index.json"
    p.write_text(json.dumps({"runs": []}), encoding="utf-8")
    return p


@pytest.fixture
def populated_index(tmp_path: Path) -> Path:
    runs = []
    for i in range(6):
        runs.append({
            "run_id": f"dossier-fake-{i:02d}",
            "started_at": f"2026-05-02T0{i}:00:00+00:00",
            "mode": "snapshot",
            "git_sha": "abcdef0123456789",
            "rollup": {
                "eval_pass_rate": 0.5 + i * 0.05,
                "calibration_ok": 1.0,
                "drift_canary_total": max(0, 3 - i),
                "cost_total_usd": 0.001 * i,
            },
        })
    p = tmp_path / "index.json"
    p.write_text(json.dumps({"runs": runs}), encoding="utf-8")
    return p


# -------------------------------------------------------------------------
# Core invariants
# -------------------------------------------------------------------------


def test_render_returns_non_empty_html(empty_index: Path) -> None:
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=empty_index)
    assert out.startswith("<!doctype html>")
    assert "</html>" in out
    assert len(out) > 4000


def test_no_external_references_csp_safe(empty_index: Path) -> None:
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=empty_index)
    # No remote scheme references inside the document body.
    assert "<script" not in out.lower()
    assert "cdn." not in out.lower()
    assert "fonts.googleapis" not in out.lower()
    assert "<link rel=\"stylesheet\"" not in out.lower()
    # Allow https links inside the decisions table (gh repo links) but never
    # in <script> / <link> / <img> tags. Spot-check no @import remote.
    assert "@import url(" not in out


def test_brand_css_variables_inlined(empty_index: Path) -> None:
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=empty_index)
    assert "--c-accent-primary" in out
    assert "hsl(168 55% 38%)" in out
    assert "Inter" in out


def test_all_panels_present(empty_index: Path) -> None:
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=empty_index)
    for anchor in ("panel-a", "panel-b", "panel-c", "panel-d", "panel-e",
                   "panel-f", "panel-g", "panel-h", "panel-i"):
        assert f'id="{anchor}"' in out, f"missing {anchor}"


def test_panel_b_pills_for_all_12_sections(empty_index: Path) -> None:
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=empty_index)
    for sid in range(1, 13):
        assert f"#section-{sid:02d}" in out, f"missing pill link for section {sid}"


def test_panel_c_insufficient_data_when_index_empty(empty_index: Path) -> None:
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=empty_index)
    assert "INSUFFICIENT-DATA" in out


def test_panel_c_renders_sparklines_when_index_populated(populated_index: Path) -> None:
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=populated_index)
    assert "INSUFFICIENT-DATA" not in out
    # 4 mini-cards expected
    assert out.count("class=\"mini-card\"") == 4
    # Each mini-card contains an inline svg
    assert out.count("<svg") >= 4


# -------------------------------------------------------------------------
# Qualitative panel coverage (require SSOT files)
# -------------------------------------------------------------------------


def test_panel_d_heatmap_when_persona_scenario_csv_available(empty_index: Path) -> None:
    if not PERSONA_SCENARIO_CSV.is_file():
        pytest.skip("PERSONA_SCENARIO_REGISTRY.csv not present in test env")
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=empty_index)
    assert 'class="heatmap"' in out
    # 4 difficulty columns from DIFFICULTY_ORDER
    assert "trivial" in out and "moderate" in out and "hard" in out and "impossible" in out
    # Real persona ids should appear
    assert "PERSONA-INVESTOR-COLD" in out or "OPERATOR" in out


def test_panel_e_scenario_cards_show_real_prompt_text(empty_index: Path) -> None:
    if not PERSONA_SCENARIO_CSV.is_file():
        pytest.skip("PERSONA_SCENARIO_REGISTRY.csv not present in test env")
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=empty_index)
    assert "scenario" in out.lower()
    # At least one scenario card with prompt block
    assert 'class="prompt"' in out
    assert "SCN-" in out


def test_panel_f_decisions_table_includes_i48_row(empty_index: Path) -> None:
    decision_log = PLANNING_DIR / "48-operator-dossier" / "decision-log.md"
    if not decision_log.is_file():
        pytest.skip("I48 decision-log not present")
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=empty_index)
    assert "D-IH-48-A" in out


def test_panel_h_recent_runs_table_when_index_populated(populated_index: Path) -> None:
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=populated_index)
    assert 'class="runs"' in out
    # Each run row should have an eval pct label like "55.0%" or similar
    assert re.search(r"\d{1,3}\.\d%", out)


def test_panel_i_cassette_samples_include_at_least_one_real_skill(empty_index: Path) -> None:
    cassettes = REPO_ROOT / "tests" / "evals" / "cassettes"
    if not cassettes.is_dir():
        pytest.skip("cassettes dir not present")
    run = _mk_run()
    out = render_console_html(run, dossier_run_index_path=empty_index)
    assert "SKILL-MADEIRA-LOOKUP-V1" in out or "SKILL-EXECUTOR-RUN-V1" in out
    assert 'class="cassette-prompt"' in out
