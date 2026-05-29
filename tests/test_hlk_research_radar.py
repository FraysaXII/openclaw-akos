"""Tests for akos.hlk_research_radar."""

from __future__ import annotations

import pytest

from akos.hlk_research_radar import (
    IntelligenceOpsRadarRow,
    SubstrateFreshnessProfile,
    fixture_intelligenceops_radar_row,
)


def test_fixture_row_validates() -> None:
    row = fixture_intelligenceops_radar_row()
    assert row.register_id.startswith("IO-")


def test_staleness_posture_none_requires_empty_days() -> None:
    with pytest.raises(ValueError):
        IntelligenceOpsRadarRow(
            register_id="IO-X",
            target_id="T",
            target_class="regulator",
            cadence="scheduled",
            source_type="OSINT",
            reliability="B",
            responsible_role="Lead Researcher",
            lifecycle_status="active",
            volatility_class="slow",
            staleness_days="90",
            staleness_posture="none",
            next_verify_by="",
        )


def test_substrate_profile_defaults_days() -> None:
    profile = SubstrateFreshnessProfile(
        substrate_id="SUBS-TEST",
        volatility_class="medium",
    )
    assert profile.staleness_days == 90
