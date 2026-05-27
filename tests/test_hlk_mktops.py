from __future__ import annotations

import pytest
from pydantic import ValidationError

from akos.hlk_mktops import (
    DIMENSION_DESCRIPTIONS,
    VALID_ADAPTER_STATUSES,
    VALID_FUNNEL_STAGES,
    VALID_LIFECYCLE_STATES,
    VALID_MKTOPS_DIMENSIONS,
    MKTOpsCampaignManifest,
    MKTOpsCampaignReport,
    MKTOpsFindingRow,
    fixture_campaign_manifest,
    fixture_finding_pass,
)


@pytest.mark.hlk
def test_mktops_has_seven_dimensions() -> None:
    assert len(VALID_MKTOPS_DIMENSIONS) == 7
    for code in VALID_MKTOPS_DIMENSIONS:
        assert code.startswith("MKT-0")


@pytest.mark.hlk
def test_dimension_descriptions_cover_all_codes() -> None:
    assert set(DIMENSION_DESCRIPTIONS) == VALID_MKTOPS_DIMENSIONS


@pytest.mark.hlk
def test_funnel_stage_enum_has_five_values() -> None:
    assert VALID_FUNNEL_STAGES == {
        "awareness",
        "consideration",
        "decision",
        "retention",
        "advocacy",
    }


@pytest.mark.hlk
def test_lifecycle_state_enum_has_six_gates() -> None:
    assert VALID_LIFECYCLE_STATES == {
        "brief",
        "creative",
        "review",
        "launch",
        "measure",
        "closed",
    }


@pytest.mark.hlk
def test_adapter_status_enum_has_five_values() -> None:
    assert VALID_ADAPTER_STATUSES == {
        "active",
        "inactive",
        "planned",
        "deprecated",
        "experimental",
    }


@pytest.mark.hlk
def test_fixture_manifest_is_valid() -> None:
    manifest = fixture_campaign_manifest()
    assert manifest.campaign_id == "CAMP-EXAMPLE-001"
    assert manifest.funnel_stage in VALID_FUNNEL_STAGES
    assert manifest.lifecycle_state in VALID_LIFECYCLE_STATES
    assert "PERSONA-INVESTOR-HIGH-CRAFT" in manifest.target_persona_ids


@pytest.mark.hlk
def test_manifest_requires_camp_prefix() -> None:
    data = fixture_campaign_manifest().model_dump()
    data["campaign_id"] = "X-NO-PREFIX"
    with pytest.raises(ValidationError):
        MKTOpsCampaignManifest.model_validate(data)


@pytest.mark.hlk
def test_manifest_requires_persona_and_channel() -> None:
    data = fixture_campaign_manifest().model_dump()
    data["target_persona_ids"] = []
    with pytest.raises(ValidationError):
        MKTOpsCampaignManifest.model_validate(data)

    data = fixture_campaign_manifest().model_dump()
    data["channel_ids"] = []
    with pytest.raises(ValidationError):
        MKTOpsCampaignManifest.model_validate(data)


@pytest.mark.hlk
def test_fixture_finding_round_trips() -> None:
    finding = fixture_finding_pass()
    assert finding.dimension_code in VALID_MKTOPS_DIMENSIONS
    assert finding.status == "PASS"


@pytest.mark.hlk
def test_report_pydantic_round_trip() -> None:
    finding = fixture_finding_pass()
    report = MKTOpsCampaignReport(
        campaign_id="CAMP-EXAMPLE-001",
        funnel_stage="consideration",
        dimensions_fired=[finding.dimension_code],
        pass_count=1,
        warn_count=0,
        fail_count=0,
        info_count=0,
        skip_count=0,
        findings=[finding],
    )
    assert report.pass_count == 1
    assert report.findings[0].campaign_id == "CAMP-EXAMPLE-001"


@pytest.mark.hlk
def test_finding_dimension_rejects_unknown_code() -> None:
    with pytest.raises(ValidationError):
        MKTOpsFindingRow(
            campaign_id="CAMP-EXAMPLE-001",
            dimension_code="MKT-99-UNKNOWN",  # type: ignore[arg-type]
            status="PASS",
            finding_text="should not validate",
        )
