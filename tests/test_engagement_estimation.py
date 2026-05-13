"""Tests for akos/engagement_estimation.py + scripts/estimate_engagement.py."""

from __future__ import annotations

import csv
import math
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.engagement_estimation import (
    METHODS,
    MULTIPLIERS,
    CountryCalendar,
    EngagementScope,
    PackageResult,
    RoleRate,
    TriEstimate,
    WorkPackage,
    blend_rate,
    estimate_engagement,
    estimate_package,
    load_calendar,
    load_role_rates,
    project_end_date,
    render_commercial_schedule_markdown,
    render_mermaid_gantt,
    working_days_for_hours,
)


# ── PERT math ──────────────────────────────────────────────────────────


def test_tri_estimate_pert_expected() -> None:
    t = TriEstimate(min=10, par=20, max=40)
    assert math.isclose(t.expected, (10 + 80 + 40) / 6.0)
    assert math.isclose(t.sigma, (40 - 10) / 6.0)


def test_tri_estimate_rejects_misordered() -> None:
    with pytest.raises(ValueError):
        TriEstimate(min=10, par=5, max=20)


def test_tri_estimate_scale() -> None:
    t = TriEstimate(min=10, par=20, max=40).scale(2.5)
    assert (t.min, t.par, t.max) == (25.0, 50.0, 100.0)


# ── Method library invariants ──────────────────────────────────────────


@pytest.mark.parametrize("method_id, method", list(METHODS.items()))
def test_method_role_mix_sums_to_one(method_id: str, method) -> None:
    total = sum(method.default_role_mix.values())
    assert 0.99 <= total <= 1.01, f"{method_id}: role_mix sum = {total}"


def test_method_library_completeness() -> None:
    expected = {
        "discovery_kickoff",
        "discovery_interviews",
        "discovery_synthesis",
        "design_workshop",
        "design_specification",
        "build_prototype_excel",
        "build_webapp",
        "build_integration_study",
        "transfer_training",
        "transfer_documentation",
        "close_review",
        "ongoing_support_month",
    }
    assert set(METHODS) == expected


# ── Role rate / blending ───────────────────────────────────────────────


def _toy_rates() -> dict[str, RoleRate]:
    return {
        "O5-1": RoleRate(role_name="O5-1", min_eur_per_hour=100, par_eur_per_hour=130, max_eur_per_hour=165),
        "Project Manager": RoleRate(role_name="Project Manager", min_eur_per_hour=45, par_eur_per_hour=60, max_eur_per_hour=75),
        "Tech Lead": RoleRate(role_name="Tech Lead", min_eur_per_hour=70, par_eur_per_hour=90, max_eur_per_hour=115),
        "Holistik Researcher": RoleRate(role_name="Holistik Researcher", min_eur_per_hour=60, par_eur_per_hour=80, max_eur_per_hour=100),
        "AIC": RoleRate(role_name="AIC", min_eur_per_hour=None, par_eur_per_hour=None, max_eur_per_hour=None),
    }


def test_role_rate_rejects_partial_triple() -> None:
    with pytest.raises(ValueError):
        RoleRate(role_name="Foo", min_eur_per_hour=10, par_eur_per_hour=None, max_eur_per_hour=20)


def test_role_rate_rejects_misordered() -> None:
    with pytest.raises(ValueError):
        RoleRate(role_name="Foo", min_eur_per_hour=20, par_eur_per_hour=10, max_eur_per_hour=30)


def test_blend_rate_50_50() -> None:
    rates = _toy_rates()
    blended = blend_rate({"O5-1": 0.5, "Project Manager": 0.5}, rates)
    assert blended.min == (100 + 45) / 2
    assert blended.par == (130 + 60) / 2
    assert blended.max == (165 + 75) / 2


def test_blend_rate_rejects_unknown_role() -> None:
    with pytest.raises(KeyError):
        blend_rate({"Unknown": 1.0}, _toy_rates())


def test_blend_rate_rejects_non_billable_role() -> None:
    with pytest.raises(ValueError):
        blend_rate({"AIC": 1.0}, _toy_rates())


def test_blend_rate_rejects_share_drift() -> None:
    with pytest.raises(ValueError):
        blend_rate({"O5-1": 0.8, "Project Manager": 0.5}, _toy_rates())


# ── Calendar loading + duration math ──────────────────────────────────


def _toy_calendars() -> dict[str, CountryCalendar]:
    return {
        "ES": CountryCalendar(country_code="ES", legal_hours_per_day=8, public_holidays_per_year_avg=14, locale_uplift_pct=0),
        "FR": CountryCalendar(country_code="FR", legal_hours_per_day=7, public_holidays_per_year_avg=11, locale_uplift_pct=20),
    }


def test_working_days_for_hours_es_baseline() -> None:
    cal = _toy_calendars()["ES"]
    days = working_days_for_hours(TriEstimate(min=80, par=160, max=240), cal)
    assert days.min == 10
    assert days.par == 20
    assert days.max == 30


def test_working_days_for_hours_fr_uplift_extends_duration() -> None:
    cal = _toy_calendars()["FR"]
    days = working_days_for_hours(TriEstimate(min=70, par=140, max=210), cal)
    assert days.par == 20.0  # 140/7 = 20
    es_cal = _toy_calendars()["ES"]
    days_es = working_days_for_hours(TriEstimate(min=80, par=160, max=240), es_cal)
    assert days_es.par == 20.0


def test_project_end_date_skips_weekends() -> None:
    # 2026-05-11 is a Monday
    cal = _toy_calendars()["ES"]
    end = project_end_date(date(2026, 5, 11), 5, cal)
    assert end >= date(2026, 5, 16)  # 5 working days lands at Mon 18 + bank-holiday bump


def test_project_end_date_zero_returns_start() -> None:
    cal = _toy_calendars()["ES"]
    assert project_end_date(date(2026, 5, 11), 0, cal) == date(2026, 5, 11)


# ── Multiplier compounding ─────────────────────────────────────────────


def test_estimate_package_applies_multipliers() -> None:
    rates = _toy_rates()
    cal = _toy_calendars()["FR"]
    pkg = WorkPackage(
        package_id="WP-1",
        method_id="discovery_kickoff",
        role_mix_override={"Project Manager": 0.5, "O5-1": 0.5},
        multiplier_ids=["enterprise_premium", "locale_uplift_fr"],
    )
    res = estimate_package(pkg, rates, cal)
    expected_factor = MULTIPLIERS["enterprise_premium"].factor * MULTIPLIERS["locale_uplift_fr"].factor
    assert math.isclose(res.multiplier_factor, expected_factor)
    assert math.isclose(
        res.cost_eur_final.par,
        res.cost_eur_pre_multiplier.par * expected_factor,
        rel_tol=1e-9,
    )


def test_estimate_package_unknown_multiplier_raises() -> None:
    rates = _toy_rates()
    cal = _toy_calendars()["ES"]
    pkg = WorkPackage(
        package_id="WP-1",
        method_id="close_review",
        multiplier_ids=["nonexistent_multiplier"],
    )
    with pytest.raises(KeyError):
        estimate_package(pkg, rates, cal)


# ── End-to-end engagement estimation ──────────────────────────────────


def test_estimate_engagement_aggregates_totals() -> None:
    rates = _toy_rates()
    cals = _toy_calendars()
    scope = EngagementScope(
        engagement_slug="test-scope",
        counterparty_label="Toy counterparty",
        country_code="FR",
        start_date=date(2026, 5, 11),
        packages=[
            WorkPackage(
                package_id="WP-1",
                method_id="close_review",
                role_mix_override={"Project Manager": 0.5, "O5-1": 0.5},
                multiplier_ids=["enterprise_premium"],
            ),
            WorkPackage(
                package_id="WP-2",
                method_id="transfer_training",
                role_mix_override={"Project Manager": 0.6, "Tech Lead": 0.4},
                multiplier_ids=[],
            ),
        ],
    )
    est = estimate_engagement(scope, rates, cals)
    assert len(est.package_results) == 2
    assert est.calendar.country_code == "FR"
    assert est.total_effort_hours.par > 0
    assert est.total_cost_eur.par > 0
    assert est.total_duration_working_days.par > 0


def test_estimate_engagement_unknown_country_raises() -> None:
    rates = _toy_rates()
    cals = _toy_calendars()
    scope = EngagementScope(
        engagement_slug="test", counterparty_label="x", country_code="DE",
        packages=[WorkPackage(package_id="WP-1", method_id="close_review")],
    )
    with pytest.raises(KeyError):
        estimate_engagement(scope, rates, cals)


# ── Mermaid Gantt rendering ───────────────────────────────────────────


def test_render_mermaid_gantt_includes_required_blocks() -> None:
    rates = _toy_rates()
    cals = _toy_calendars()
    scope = EngagementScope(
        engagement_slug="test", counterparty_label="Toy",
        country_code="ES", start_date=date(2026, 5, 11),
        packages=[WorkPackage(package_id="WP-1", method_id="discovery_kickoff",
                              role_mix_override={"O5-1": 0.5, "Project Manager": 0.5})],
    )
    est = estimate_engagement(scope, rates, cals)
    block = render_mermaid_gantt(est)
    assert block.startswith("```mermaid\ngantt")
    assert "dateFormat  YYYY-MM-DD" in block
    assert "section Engagement" in block
    assert block.rstrip().endswith("```")


def test_render_commercial_schedule_markdown_snapshot_shape() -> None:
    rates = _toy_rates()
    cals = _toy_calendars()
    scope = EngagementScope(
        engagement_slug="test", counterparty_label="Toy",
        country_code="FR", start_date=date(2026, 5, 11),
        packages=[
            WorkPackage(package_id="WP-1", method_id="discovery_kickoff",
                        role_mix_override={"O5-1": 0.5, "Project Manager": 0.5},
                        multiplier_ids=["locale_uplift_fr"]),
            WorkPackage(package_id="WP-2", method_id="close_review",
                        role_mix_override={"O5-1": 0.5, "Project Manager": 0.5},
                        multiplier_ids=[]),
        ],
    )
    est = estimate_engagement(scope, rates, cals)
    body = render_commercial_schedule_markdown(est)
    assert "# Commercial schedule — Toy" in body
    assert "## Per-package estimate" in body
    assert "## Totals" in body
    assert "## Visual schedule" in body
    assert "```mermaid" in body
    assert "WP-1" in body and "WP-2" in body


# ── CSV loaders (integration with canonical CSVs once P3b lands) ──────


def test_load_role_rates_from_canonical_csv_is_well_formed() -> None:
    csv_path = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"
    rates = load_role_rates(csv_path)
    assert "Project Manager" in rates
    assert "O5-1" in rates
    pm = rates["Project Manager"]
    if pm.is_billable:
        assert pm.min_eur_per_hour <= pm.par_eur_per_hour <= pm.max_eur_per_hour


def test_load_calendar_returns_es_and_fr() -> None:
    csv_path = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "COUNTRY_WORK_CALENDAR.csv"
    if not csv_path.exists():
        pytest.skip("COUNTRY_WORK_CALENDAR.csv not yet seeded (P3b in progress)")
    cals = load_calendar(csv_path)
    assert "ES" in cals
    assert "FR" in cals
    assert cals["FR"].locale_uplift_pct >= 15


# ── SUEZ-specific integration smoke (requires P3b CSV extensions) ─────


def test_suez_application_produces_a_full_schedule() -> None:
    """End-to-end smoke: parse the SUEZ scope.yaml + canonical CSVs, render schedule."""
    pytest.importorskip("akos.engagement_estimation")
    scope_path = (
        REPO_ROOT
        / "docs"
        / "wip"
        / "intelligence"
        / "2026-05-10-suez-webuy-procure-to-pay"
        / "scope.yaml"
    )
    rates_path = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"
    cal_path = (
        REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "COUNTRY_WORK_CALENDAR.csv"
    )
    if not (scope_path.exists() and cal_path.exists()):
        pytest.skip("SUEZ scope.yaml or COUNTRY_WORK_CALENDAR.csv not yet authored")

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import estimate_engagement as ee  # type: ignore[import-not-found]

    rates = load_role_rates(rates_path)
    cals = load_calendar(cal_path)
    scope_dict = ee._load_yaml(scope_path)
    scope = ee._scope_from_dict(scope_dict)
    est = estimate_engagement(scope, rates, cals)
    assert est.total_cost_eur.par > 0
    body = render_commercial_schedule_markdown(est)
    assert "Toy" not in body
    assert "```mermaid" in body
