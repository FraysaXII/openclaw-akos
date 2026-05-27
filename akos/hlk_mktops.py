"""Pydantic SSOT for the MKTOps discipline (7-dimension campaign quality bar).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/
MKTOPS_DISCIPLINE.md`` (7-dim quality bar; status flipped to ``active`` at
Wave R+4 C3a per ``D-IH-86-EY``).

Paired runbook: ``scripts/validate_mktops_campaign.py``.
Paired cursor rule: ``.cursor/rules/akos-mktops-discipline.mdc``.

The 7 dimensions follow ``MKTOPS_DISCIPLINE.md`` §2:

- ``MKT-01-CAMPAIGN-LIFECYCLE-QUALITY``
- ``MKT-02-FUNNEL-STAGE-UX``
- ``MKT-03-LANDING-PAGE-CONVERSION``
- ``MKT-04-ATTRIBUTION-TRAIL``
- ``MKT-05-CHANNEL-COVERAGE``
- ``MKT-06-PERSONA-FIT``
- ``MKT-07-BRAND-VOICE-INTEGRITY``

Cadence per the canonical:

- ``--self-test`` runs at every pre_commit (chassis/fixtures only; no real
  campaign artifact inspection).
- ``--check-campaign <manifest.yaml>`` runs at campaign-brief authoring time
  and at each lifecycle gate.

This module intentionally does NOT introduce a new canonical CSV: MKTOps
quality is per-campaign-manifest. Campaign manifests live alongside their
engagement folder when authored.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


VALID_MKTOPS_DIMENSIONS: frozenset[str] = frozenset({
    "MKT-01-CAMPAIGN-LIFECYCLE-QUALITY",
    "MKT-02-FUNNEL-STAGE-UX",
    "MKT-03-LANDING-PAGE-CONVERSION",
    "MKT-04-ATTRIBUTION-TRAIL",
    "MKT-05-CHANNEL-COVERAGE",
    "MKT-06-PERSONA-FIT",
    "MKT-07-BRAND-VOICE-INTEGRITY",
})

VALID_FUNNEL_STAGES: frozenset[str] = frozenset({
    "awareness",
    "consideration",
    "decision",
    "retention",
    "advocacy",
})

VALID_LIFECYCLE_STATES: frozenset[str] = frozenset({
    "brief",
    "creative",
    "review",
    "launch",
    "measure",
    "closed",
})

VALID_FINDING_STATUSES: frozenset[str] = frozenset({
    "PASS",
    "WARN",
    "FAIL",
    "INFO",
    "SKIP",
})

VALID_ADAPTER_STATUSES: frozenset[str] = frozenset({
    "active",
    "inactive",
    "planned",
    "deprecated",
    "experimental",
})

DIMENSION_DESCRIPTIONS: dict[str, str] = {
    "MKT-01-CAMPAIGN-LIFECYCLE-QUALITY": (
        "Campaign moves brief -> creative -> review -> launch -> measure "
        "with operator approval at each gate."
    ),
    "MKT-02-FUNNEL-STAGE-UX": (
        "Funnel stage UX bar derived from UX_DISCIPLINE.md per stage class."
    ),
    "MKT-03-LANDING-PAGE-CONVERSION": (
        "Landing page Core Web Vitals plus brand voice plus persona "
        "alignment plus form friction within benchmark."
    ),
    "MKT-04-ATTRIBUTION-TRAIL": (
        "Every campaign artefact tags UTM correctly and FK-resolves into "
        "ATTRIBUTION_ADAPTER_REGISTRY.csv."
    ),
    "MKT-05-CHANNEL-COVERAGE": (
        "CRM plus EMAIL plus COMMUNICATION plus SCHEDULING adapter health "
        "is active per registry for every adapter the campaign invokes."
    ),
    "MKT-06-PERSONA-FIT": (
        "Every campaign targets at least one FK-resolved persona from "
        "PERSONA_REGISTRY.csv."
    ),
    "MKT-07-BRAND-VOICE-INTEGRITY": (
        "Every external-facing artefact passes BRAND_DO_DONT scan plus "
        "brand-baseline-reality dual-register check."
    ),
}


class MKTOpsCampaignManifest(BaseModel):
    """Minimal manifest a campaign carries to satisfy the 7-dim quality bar.

    A campaign manifest is a frontmatter-shaped YAML/JSON object that lives
    next to the campaign's source artifacts (brief markdown, landing page
    source, email template). The runbook reads this manifest to validate
    the 7 MKTOps dimensions structurally.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    campaign_id: str = Field(min_length=1, max_length=120)
    campaign_name: str = Field(min_length=1, max_length=240)
    funnel_stage: Literal[
        "awareness", "consideration", "decision", "retention", "advocacy"
    ]
    lifecycle_state: Literal[
        "brief", "creative", "review", "launch", "measure", "closed"
    ]
    target_persona_ids: list[str] = Field(
        min_length=1,
        description="FK list into PERSONA_REGISTRY.persona_id (MKT-06).",
    )
    channel_ids: list[str] = Field(
        min_length=1,
        description="FK list into CHANNEL_TOUCHPOINT_REGISTRY.channel_id (MKT-05).",
    )
    adapters_invoked: list[str] = Field(
        default_factory=list,
        description=(
            "FK list into adapter registries (CRM / EMAIL / COMMUNICATION / "
            "SCHEDULING / ATTRIBUTION). MKT-04 + MKT-05."
        ),
    )
    utm_source: str = Field(default="", max_length=120)
    utm_medium: str = Field(default="", max_length=120)
    utm_campaign: str = Field(default="", max_length=240)
    landing_page_path: str = Field(default="", max_length=400)
    measurement_event: str = Field(
        default="",
        max_length=240,
        description=(
            "Named conversion event the campaign measures (MKT-03 + MKT-04)."
        ),
    )
    brand_register: Literal[
        "internal-corpint", "external-translated", "mixed", "internal-only"
    ] = "external-translated"
    ratifying_decision_ids: list[str] = Field(default_factory=list)
    notes: str = Field(default="", max_length=2000)

    @field_validator("campaign_id")
    @classmethod
    def campaign_id_shape(cls, value: str) -> str:
        if not value.startswith("CAMP-"):
            raise ValueError("campaign_id must start with CAMP-")
        return value


class MKTOpsFindingRow(BaseModel):
    """One finding emitted by ``scripts/validate_mktops_campaign.py``.

    The validator emits one row per dimension fired; campaigns that pass
    every dimension get 7 PASS rows.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    campaign_id: str = Field(min_length=1, max_length=120)
    dimension_code: Literal[
        "MKT-01-CAMPAIGN-LIFECYCLE-QUALITY",
        "MKT-02-FUNNEL-STAGE-UX",
        "MKT-03-LANDING-PAGE-CONVERSION",
        "MKT-04-ATTRIBUTION-TRAIL",
        "MKT-05-CHANNEL-COVERAGE",
        "MKT-06-PERSONA-FIT",
        "MKT-07-BRAND-VOICE-INTEGRITY",
    ]
    status: Literal["PASS", "WARN", "FAIL", "INFO", "SKIP"]
    finding_text: str = Field(min_length=1, max_length=600)
    recommended_action: str = Field(default="", max_length=600)


class MKTOpsCampaignReport(BaseModel):
    """Aggregate per-campaign report rolled up from the 7 dimensions."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str
    funnel_stage: Literal[
        "awareness", "consideration", "decision", "retention", "advocacy"
    ] = "awareness"
    dimensions_fired: list[str]
    pass_count: int = Field(ge=0)
    warn_count: int = Field(ge=0)
    fail_count: int = Field(ge=0)
    info_count: int = Field(ge=0)
    skip_count: int = Field(ge=0)
    findings: list[MKTOpsFindingRow] = Field(default_factory=list)


def fixture_campaign_manifest() -> MKTOpsCampaignManifest:
    """Return a minimal-valid manifest for self-tests and tests."""

    return MKTOpsCampaignManifest(
        campaign_id="CAMP-EXAMPLE-001",
        campaign_name="Example campaign for self-test",
        funnel_stage="consideration",
        lifecycle_state="brief",
        target_persona_ids=["PERSONA-INVESTOR-HIGH-CRAFT"],
        channel_ids=["CHAN-EMAIL-INBOUND"],
        adapters_invoked=[],
        utm_source="example",
        utm_medium="email",
        utm_campaign="self-test",
        landing_page_path="",
        measurement_event="self-test-event",
        brand_register="external-translated",
        ratifying_decision_ids=["D-IH-86-EY"],
        notes="Self-test fixture only; not a real campaign.",
    )


def fixture_finding_pass(dimension_code: str = "MKT-06-PERSONA-FIT") -> MKTOpsFindingRow:
    """Return one PASS finding row for self-tests."""

    return MKTOpsFindingRow(
        campaign_id="CAMP-EXAMPLE-001",
        dimension_code=dimension_code,  # type: ignore[arg-type]
        status="PASS",
        finding_text="Self-test fixture passes target persona FK resolution.",
        recommended_action="",
    )
