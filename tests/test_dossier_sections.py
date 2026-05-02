"""Initiative 48 P1 tests — Section ABC + 12 subclasses skeleton.

Coverage:
- SECTION_CLASSES tuple has exactly 12 entries
- Each subclass declares correct section_id (1..12)
- D-IH-48-D ordering invariant (SECTION_CLASSES[i].section_id == i+1)
- Each subclass: gather() returns SectionData; render_markdown() emits the
  `## Section N — <Name>` header; metrics_for_trend() returns dict
- Section 1 + Section 11 + Section 12 special-case behavior
- Default-open HTML state per section (D-IH-48-I)
- PLACEHOLDER text appears when SectionData.placeholder=True
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pytest

from akos.dossier.run import DossierFilter
from akos.dossier.sections import (
    SECTION_CLASSES,
    Section,
    Section01ExecutiveSummary,
    Section02SchemaGovernance,
    Section06Recovery,
    Section10GovernanceDebt,
    Section11TrendLines,
    Section12Appendix,
    SectionData,
)


# ---------------------------------------------------------------------------
# SECTION_CLASSES ordering invariant (D-IH-48-D)
# ---------------------------------------------------------------------------

def test_section_classes_has_exactly_12() -> None:
    assert len(SECTION_CLASSES) == 12


def test_section_classes_in_strict_1_to_12_order() -> None:
    """D-IH-48-D: SECTION_CLASSES[i].section_id == i + 1."""
    for i, cls in enumerate(SECTION_CLASSES):
        assert cls.section_id == i + 1, (
            f"SECTION_CLASSES[{i}] is {cls.__name__} with section_id={cls.section_id}; "
            f"expected {i+1}"
        )


def test_section_classes_have_unique_ids() -> None:
    ids = [cls.section_id for cls in SECTION_CLASSES]
    assert len(set(ids)) == 12


def test_section_classes_have_non_empty_names() -> None:
    for cls in SECTION_CLASSES:
        assert cls.name and isinstance(cls.name, str), f"{cls.__name__} has empty name"


# ---------------------------------------------------------------------------
# Each subclass: gather + render_markdown + metrics_for_trend
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cls", SECTION_CLASSES)
def test_each_section_gather_returns_section_data(cls: type[Section]) -> None:
    inst = cls()
    data = inst.gather(mode="snapshot", filter=DossierFilter())
    assert isinstance(data, SectionData)


@pytest.mark.parametrize("cls", SECTION_CLASSES)
def test_each_section_render_markdown_emits_header(cls: type[Section]) -> None:
    inst = cls()
    data = inst.gather(mode="snapshot")
    md = inst.render_markdown(data)
    assert f"## Section {inst.section_id} —" in md, (
        f"{cls.__name__} did not emit '## Section {inst.section_id} —' header; got {md[:120]!r}"
    )


@pytest.mark.parametrize("cls", SECTION_CLASSES)
def test_each_section_metrics_for_trend_returns_dict(cls: type[Section]) -> None:
    inst = cls()
    data = inst.gather(mode="snapshot")
    metrics = inst.metrics_for_trend(data)
    assert isinstance(metrics, dict)


@pytest.mark.parametrize("cls", SECTION_CLASSES)
def test_each_section_execute_returns_dossier_section_result(cls: type[Section]) -> None:
    inst = cls()
    result = inst.execute(mode="snapshot")
    assert result.section_id == cls.section_id
    assert result.name == cls.name
    assert isinstance(result.markdown, str) and result.markdown
    assert isinstance(result.metrics, dict)


# ---------------------------------------------------------------------------
# Special-case behavior
# ---------------------------------------------------------------------------

def test_section_01_executive_summary_default_open() -> None:
    """D-IH-48-I + dossier-section-spec.md: Section 1 default_open."""
    assert Section01ExecutiveSummary.default_open_html is True
    assert Section01ExecutiveSummary.staleness_threshold_hours == 0


def test_section_06_recovery_never_auto_refresh() -> None:
    """dossier-section-spec.md: Section 6 staleness_threshold_hours=None (never auto-refresh chaos)."""
    assert Section06Recovery.staleness_threshold_hours is None
    assert Section06Recovery.default_open_html is False


def test_section_11_trendlines_status_is_info() -> None:
    """Section 11 emits INFO status (not PASS/FAIL); trend lines are diagnostic."""
    inst = Section11TrendLines()
    result = inst.execute(mode="snapshot")
    assert result.status == "INFO"


def test_section_11_trendlines_emits_insufficient_data_placeholder_at_run_1(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Section 11 returns INSUFFICIENT-DATA when no prior runs exist."""
    from akos.dossier import sources as dossier_sources

    monkeypatch.setattr(dossier_sources, "_fetch_dossier_run_remote", lambda limit: [])
    monkeypatch.setattr(dossier_sources, "_load_local_index_runs", lambda limit: [])

    inst = Section11TrendLines()
    md = inst.render_markdown(inst.gather(mode="snapshot"))
    assert "INSUFFICIENT-DATA" in md


def test_section_11_trendlines_emits_no_metrics() -> None:
    """Section 11 CONSUMES trend metrics; emits none."""
    inst = Section11TrendLines()
    metrics = inst.metrics_for_trend(inst.gather(mode="snapshot"))
    assert metrics == {}


def test_section_12_appendix_status_is_info() -> None:
    inst = Section12Appendix()
    result = inst.execute(mode="snapshot")
    assert result.status == "INFO"


def test_section_12_appendix_default_collapsed() -> None:
    assert Section12Appendix.default_open_html is False


def test_section_10_governance_debt_always_re_parses() -> None:
    """staleness=0: always re-parses markdown files (cheap)."""
    assert Section10GovernanceDebt.staleness_threshold_hours == 0


# ---------------------------------------------------------------------------
# PLACEHOLDER text appears when SectionData.placeholder=True
# ---------------------------------------------------------------------------

def test_section_07_drift_canaries_emits_placeholder_in_snapshot_mode() -> None:
    """Section 07 (drift canaries) is the only remaining placeholder in snapshot mode
    after P2 wired sources (live mode P3 will invoke graphrag_drift_canary.py)."""
    inst = SECTION_CLASSES[6]()  # Section 07
    md = inst.render_markdown(inst.gather(mode="snapshot"))
    assert "[STALE / UNAVAILABLE]" in md


def test_placeholder_includes_actionable_run_command() -> None:
    """PLACEHOLDER text must point operator at the live mode CLI."""
    from akos.dossier.sections import Section07DriftCanaries
    inst = Section07DriftCanaries()
    md = inst.render_markdown(inst.gather(mode="snapshot"))
    assert "py scripts/render_uat_dossier.py" in md
    assert "--mode live" in md


# ---------------------------------------------------------------------------
# Section ABC contract
# ---------------------------------------------------------------------------

def test_section_abc_cannot_be_instantiated_directly() -> None:
    """Section is ABC; must subclass."""
    with pytest.raises(TypeError):
        Section()  # type: ignore[abstract]
