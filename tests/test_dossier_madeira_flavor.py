"""Initiative 49 P9 — MADEIRA dossier flavor tests.

Coverage:
- DossierFilter.flavor + skill_id round-trip + manifest serialisation
- Saved preset (--filter madeira) composes persona/initiative/skill roster
- Section01ExecutiveSummaryMadeira computes three-light verdict from prior_results
- compute_madeira_three_lights honours Section 8 madeira_surface_ship hint
- single_persona_for_cli + persona_id_set helpers behave on rosters
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.dossier import (
    MADEIRA_DOSSIER_INITIATIVE_IDS,
    MADEIRA_DOSSIER_PERSONA_IDS,
    MADEIRA_DOSSIER_SKILL_ID,
    DossierFilter,
    DossierRun,
    DossierSectionResult,
    Section01ExecutiveSummary,
    Section01ExecutiveSummaryMadeira,
    compute_madeira_three_lights,
    dossier_filter_madeira_preset,
    persona_id_set,
    single_persona_for_cli,
)


def test_dossier_filter_default_flavor() -> None:
    f = DossierFilter()
    assert f.flavor == "default"
    assert f.skill_id is None


def test_madeira_preset_roster_constants_match_plan() -> None:
    assert "PERSONA-INVESTOR-COLD" in MADEIRA_DOSSIER_PERSONA_IDS
    assert "OPERATOR" in MADEIRA_DOSSIER_PERSONA_IDS
    assert "47" in MADEIRA_DOSSIER_INITIATIVE_IDS.split(",")
    assert "49" in MADEIRA_DOSSIER_INITIATIVE_IDS.split(",")
    assert MADEIRA_DOSSIER_SKILL_ID == "skill_madeira_lookup_v1"


def test_dossier_filter_madeira_preset_composition() -> None:
    f = dossier_filter_madeira_preset()
    assert f.flavor == "madeira"
    assert f.persona_id == MADEIRA_DOSSIER_PERSONA_IDS
    assert f.initiative == MADEIRA_DOSSIER_INITIATIVE_IDS
    assert f.skill_id == MADEIRA_DOSSIER_SKILL_ID


def test_single_persona_for_cli_returns_id_when_singleton() -> None:
    assert single_persona_for_cli("PERSONA-INVESTOR-COLD") == "PERSONA-INVESTOR-COLD"


def test_single_persona_for_cli_returns_none_for_roster() -> None:
    assert single_persona_for_cli(MADEIRA_DOSSIER_PERSONA_IDS) is None


def test_single_persona_for_cli_handles_blank_input() -> None:
    assert single_persona_for_cli(None) is None
    assert single_persona_for_cli("") is None


def test_persona_id_set_splits_csv_roster() -> None:
    s = persona_id_set(MADEIRA_DOSSIER_PERSONA_IDS)
    assert "PERSONA-INVESTOR-COLD" in s
    assert "OPERATOR" in s
    assert len(s) == 5


def test_to_manifest_filter_block_carries_flavor_and_skill() -> None:
    r = DossierRun(filter=dossier_filter_madeira_preset())
    m = r.to_manifest(md_text="# test")
    f = m["filter"]
    assert f["flavor"] == "madeira"
    assert f["skill_id"] == MADEIRA_DOSSIER_SKILL_ID
    assert f["persona_id"] == MADEIRA_DOSSIER_PERSONA_IDS


def test_to_markdown_emits_flavor_in_filter_block() -> None:
    r = DossierRun(filter=dossier_filter_madeira_preset())
    out = r.to_markdown()
    assert "## Filter" in out
    assert "flavor: `madeira`" in out
    assert f"skill_id: `{MADEIRA_DOSSIER_SKILL_ID}`" in out


def _result(sid: int, status: str, *, metrics: dict | None = None) -> DossierSectionResult:
    return DossierSectionResult(
        section_id=sid, name=f"Section {sid}", status=status,
        markdown=f"## Section {sid} — Section {sid}\n", metrics=metrics or {},
    )


def test_three_lights_all_green_yields_ship_go_when_section8_signals_green() -> None:
    prior = [
        _result(3, "PASS"), _result(4, "PASS"),
        _result(5, "PASS"), _result(6, "PASS"),
        _result(8, "PASS", metrics={"madeira_surface_ship": "GREEN"}),
    ]
    lights = compute_madeira_three_lights(prior_results=prior)
    assert lights["light_conversational"] == "GREEN"
    assert lights["light_operator"] == "GREEN"
    assert lights["light_surface"] == "GREEN"
    assert lights["madeira_ship_go"] is True


def test_three_lights_amber_surface_when_section8_silent() -> None:
    prior = [_result(sid, "PASS") for sid in (3, 4, 5, 6, 8)]
    lights = compute_madeira_three_lights(prior_results=prior)
    assert lights["light_surface"] == "AMBER"
    assert lights["madeira_ship_go"] is False


def test_three_lights_red_conversational_on_fail() -> None:
    prior = [
        _result(3, "FAIL"), _result(4, "PASS"),
        _result(5, "PASS"), _result(6, "PASS"),
        _result(8, "PASS", metrics={"madeira_surface_ship": "GREEN"}),
    ]
    lights = compute_madeira_three_lights(prior_results=prior)
    assert lights["light_conversational"] == "RED"
    assert lights["madeira_ship_go"] is False


def test_three_lights_amber_operator_on_skip_section8() -> None:
    prior = [
        _result(3, "PASS"), _result(4, "PASS"),
        _result(5, "PASS"), _result(6, "PASS"),
        _result(8, "SKIP"),
    ]
    lights = compute_madeira_three_lights(prior_results=prior)
    assert lights["light_operator"] == "AMBER"
    assert lights["madeira_ship_go"] is False


def test_madeira_section1_render_emits_three_light_rows_and_legacy_table() -> None:
    s1 = Section01ExecutiveSummaryMadeira()
    prior = [
        _result(3, "PASS"), _result(4, "PASS"),
        _result(5, "PASS"), _result(6, "PASS"),
        _result(8, "PASS", metrics={"madeira_surface_ship": "GREEN"}),
    ]
    data = s1.gather(mode="snapshot", prior_results=prior)
    md = s1.render_markdown(data)
    assert "MADEIRA release verdict" in md
    assert "Conversational" in md
    assert "Operator" in md
    assert "Surface" in md
    assert "GREEN" in md
    assert "Section 1 —" in md or "Section 1 -" in md  # legacy table heading appears


def test_madeira_section1_metrics_include_lights_and_flavor() -> None:
    s1 = Section01ExecutiveSummaryMadeira()
    prior = [
        _result(3, "PASS"), _result(4, "PASS"),
        _result(5, "PASS"), _result(6, "PASS"),
        _result(8, "PASS", metrics={"madeira_surface_ship": "GREEN"}),
    ]
    data = s1.gather(mode="snapshot", prior_results=prior)
    metrics = s1.metrics_for_trend(data)
    assert metrics["flavor"] == "madeira"
    assert metrics["madeira_ship_go"] is True
    assert metrics["light_conversational"] == "GREEN"
    assert metrics["light_operator"] == "GREEN"
    assert metrics["light_surface"] == "GREEN"


def test_madeira_section1_render_no_prior_results_is_no_go() -> None:
    s1 = Section01ExecutiveSummaryMadeira()
    data = s1.gather(mode="snapshot", prior_results=None)
    md = s1.render_markdown(data)
    assert "NO-GO" in md
    assert "AMBER" in md


def test_default_section1_unchanged_for_non_madeira_flavor() -> None:
    s1 = Section01ExecutiveSummary()
    prior = [_result(3, "PASS"), _result(4, "PASS")]
    data = s1.gather(mode="snapshot", prior_results=prior)
    md = s1.render_markdown(data)
    assert "MADEIRA release verdict" not in md


# ──────────────────────────────────────────────────────────────────────────────
# P16 — Section 8 Surface UX subsection (flavor='madeira')
# ──────────────────────────────────────────────────────────────────────────────


def test_section8_surface_ux_block_emits_for_madeira_flavor() -> None:
    """Section 8 must surface the MADEIRA Surface UX subsection when flavor='madeira'.

    Reads the live Initiative 49 reports folder (P14 shape + P15 critique are
    on disk after this initiative ships); verifies the rendered markdown
    contains the subsection heading and a ship signal value.
    """
    from akos.dossier import (
        DossierFilter,
        Section08OperationalHealth,
    )
    s8 = Section08OperationalHealth()
    filt = DossierFilter(flavor="madeira")
    data = s8.gather(mode="snapshot", filter=filt)
    md = s8.render_markdown(data)
    assert "MADEIRA Surface UX" in md
    assert "ship signal" in md
    assert data.payload.get("madeira_surface_ship") in {"GREEN", "AMBER", "RED"}


def test_section8_surface_ux_metrics_propagate_to_three_lights() -> None:
    """Trend metrics emit `madeira_surface_ship` for downstream Section 1 light computation."""
    from akos.dossier import DossierFilter, Section08OperationalHealth
    s8 = Section08OperationalHealth()
    filt = DossierFilter(flavor="madeira")
    data = s8.gather(mode="snapshot", filter=filt)
    metrics = s8.metrics_for_trend(data)
    assert "madeira_surface_ship" in metrics


def test_section8_madeira_cost_rollup_subsection_present_for_madeira() -> None:
    from akos.dossier import DossierFilter, Section08OperationalHealth
    s8 = Section08OperationalHealth()
    filt = DossierFilter(flavor="madeira")
    data = s8.gather(mode="snapshot", filter=filt)
    md = s8.render_markdown(data)
    assert "MADEIRA cost rollup" in md


def test_section8_no_madeira_subsections_for_default_flavor() -> None:
    from akos.dossier import DossierFilter, Section08OperationalHealth
    s8 = Section08OperationalHealth()
    filt = DossierFilter()
    data = s8.gather(mode="snapshot", filter=filt)
    md = s8.render_markdown(data)
    assert "MADEIRA Surface UX" not in md
    assert "MADEIRA cost rollup" not in md
