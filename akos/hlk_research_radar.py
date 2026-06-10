"""Pydantic SSOT for Research Radar freshness sweeps (I75 / Wave R+5 C1).

Canonical doctrine:
``docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_RADAR_DISCIPLINE.md``

Paired runbook: ``scripts/research_radar_sweep.py``
Paired validator: ``scripts/validate_research_radar.py``

Decision lineage: D-IH-86-FG (16th Quality Fabric specialty mint),
D-IH-86-FH (INTELLIGENCEOPS_REGISTER freshness columns),
D-IH-86-FI (substrate process row + radar subsume).

Cadence is **per-target data** on ``INTELLIGENCEOPS_REGISTER`` rows and
``SUBSTRATE_VOLATILITY_PROFILES`` — never a global schedule constant.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from akos.io import REPO_ROOT

SUBSTRATE_REGISTRY_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions"
    / "SUBSTRATE_REGISTRY.csv"
)
INTELLIGENCEOPS_REGISTER_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Research/Intelligence/canonicals/dimensions"
    / "INTELLIGENCEOPS_REGISTER.csv"
)

INTELLIGENCEOPS_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "register_id",
    "target_id",
    "target_class",
    "cadence",
    "source_type",
    "reliability",
    "output_artifact",
    "responsible_role",
    "lifecycle_status",
    "intro_decision_id",
    "linked_sop_path",
    "linked_runbook_path",
    "notes",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "volatility_class",
    "staleness_days",
    "staleness_posture",
    "next_verify_by",
)

VALID_VOLATILITY_CLASSES: frozenset[str] = frozenset({
    "fast",
    "medium",
    "slow",
    "static",
})

VALID_STALENESS_POSTURES: frozenset[str] = frozenset({
    "cite_and_flag",
    "block_govern",
    "none",
})

# Register-level default decay hints (overridable per row via staleness_days).
VOLATILITY_DEFAULT_STALENESS_DAYS: dict[str, int | None] = {
    "fast": 30,
    "medium": 90,
    "slow": 365,
    "static": None,
}

RADAR_FINDING_FIELDNAMES: tuple[str, ...] = (
    "target_key",
    "source_register",
    "verdict",
    "staleness_posture",
    "last_verified_at",
    "next_verify_by",
    "staleness_days",
    "volatility_class",
    "notes",
)


class IntelligenceOpsRadarRow(BaseModel):
    """One INTELLIGENCEOPS_REGISTER row with radar freshness columns."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    register_id: str = Field(min_length=1, max_length=80)
    target_id: str = Field(min_length=1, max_length=120)
    target_class: str
    cadence: str
    source_type: str
    reliability: str
    output_artifact: str = ""
    responsible_role: str
    lifecycle_status: Literal["active", "scaffold", "deprecated"]
    intro_decision_id: str = ""
    linked_sop_path: str = ""
    linked_runbook_path: str = ""
    notes: str = ""
    last_review_at: str = ""
    last_review_by: str = ""
    last_review_decision_id: str = ""
    methodology_version_at_review: str = ""
    volatility_class: Literal["fast", "medium", "slow", "static"]
    staleness_days: str = ""
    staleness_posture: Literal["cite_and_flag", "block_govern", "none"]
    next_verify_by: str = ""

    @model_validator(mode="after")
    def _staleness_alignment(self) -> IntelligenceOpsRadarRow:
        if self.staleness_posture == "none" and self.staleness_days.strip():
            raise ValueError(
                f"register_id={self.register_id}: staleness_posture=none requires empty staleness_days"
            )
        if self.staleness_posture != "none" and not self.staleness_days.strip():
            raise ValueError(
                f"register_id={self.register_id}: staleness_posture={self.staleness_posture} "
                "requires non-empty staleness_days"
            )
        if self.staleness_days.strip():
            days = int(self.staleness_days)
            if days < 1:
                raise ValueError(f"register_id={self.register_id}: staleness_days must be >= 1")
        return self

    def resolved_staleness_days(self) -> int | None:
        if self.staleness_posture == "none":
            return None
        if self.staleness_days.strip():
            return int(self.staleness_days)
        return VOLATILITY_DEFAULT_STALENESS_DAYS[self.volatility_class]


class SubstrateFreshnessProfile(BaseModel):
    """Per-substrate radar profile (subsume substrate freshness without a global cadence)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    substrate_id: str
    volatility_class: Literal["fast", "medium", "slow", "static"]
    staleness_days: int | None = None
    staleness_posture: Literal["cite_and_flag", "block_govern", "none"] = "cite_and_flag"

    @model_validator(mode="before")
    @classmethod
    def _default_days(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if data.get("staleness_posture") == "none":
            return data
        if data.get("staleness_days") is not None:
            return data
        vc = data.get("volatility_class")
        if vc is None:
            return data
        default = VOLATILITY_DEFAULT_STALENESS_DAYS.get(vc)
        if default is None:
            sid = data.get("substrate_id", "?")
            raise ValueError(
                f"substrate_id={sid}: static volatility requires explicit staleness_days or posture none"
            )
        return {**data, "staleness_days": default}


# Per-substrate overrides (not a single global threshold).
SUBSTRATE_VOLATILITY_PROFILES: dict[str, SubstrateFreshnessProfile] = {
    "SUBS-HOLISTIKA-OPENCLAW": SubstrateFreshnessProfile(
        substrate_id="SUBS-HOLISTIKA-OPENCLAW",
        volatility_class="fast",
        staleness_days=45,
        staleness_posture="block_govern",
    ),
    "SUBS-LANGCHAIN-AI-LANGGRAPH": SubstrateFreshnessProfile(
        substrate_id="SUBS-LANGCHAIN-AI-LANGGRAPH",
        volatility_class="fast",
        staleness_days=60,
        staleness_posture="cite_and_flag",
    ),
    "SUBS-LANGCHAIN-AI-LANGCHAIN": SubstrateFreshnessProfile(
        substrate_id="SUBS-LANGCHAIN-AI-LANGCHAIN",
        volatility_class="medium",
        staleness_days=90,
        staleness_posture="cite_and_flag",
    ),
    "SUBS-RUN-LLAMA-LLAMAINDEX": SubstrateFreshnessProfile(
        substrate_id="SUBS-RUN-LLAMA-LLAMAINDEX",
        volatility_class="medium",
        staleness_days=120,
        staleness_posture="cite_and_flag",
    ),
    "SUBS-ANYSPHERE-CURSOR-SDK": SubstrateFreshnessProfile(
        substrate_id="SUBS-ANYSPHERE-CURSOR-SDK",
        volatility_class="fast",
        staleness_days=30,
        staleness_posture="block_govern",
    ),
    "SUBS-ANTHROPIC-CLAUDE-CODE-SDK": SubstrateFreshnessProfile(
        substrate_id="SUBS-ANTHROPIC-CLAUDE-CODE-SDK",
        volatility_class="fast",
        staleness_days=30,
        staleness_posture="block_govern",
    ),
    "SUBS-OPENAI-AGENTS-SDK": SubstrateFreshnessProfile(
        substrate_id="SUBS-OPENAI-AGENTS-SDK",
        volatility_class="fast",
        staleness_days=45,
        staleness_posture="cite_and_flag",
    ),
    "SUBS-VERCEL-VERCEL-AI-SDK": SubstrateFreshnessProfile(
        substrate_id="SUBS-VERCEL-VERCEL-AI-SDK",
        volatility_class="medium",
        staleness_days=75,
        staleness_posture="cite_and_flag",
    ),
    "SUBS-OLLAMA-OLLAMA": SubstrateFreshnessProfile(
        substrate_id="SUBS-OLLAMA-OLLAMA",
        volatility_class="medium",
        staleness_days=90,
        staleness_posture="cite_and_flag",
    ),
    "SUBS-HOLISTIKA-KIRBE": SubstrateFreshnessProfile(
        substrate_id="SUBS-HOLISTIKA-KIRBE",
        volatility_class="medium",
        staleness_days=120,
        staleness_posture="cite_and_flag",
    ),
    "SUBS-DEEPSEEK-DEEPSEEK-V4": SubstrateFreshnessProfile(
        substrate_id="SUBS-DEEPSEEK-DEEPSEEK-V4",
        volatility_class="fast",
        staleness_days=45,
        staleness_posture="block_govern",
    ),
    "SUBS-MOONSHOT-KIMI-K26": SubstrateFreshnessProfile(
        substrate_id="SUBS-MOONSHOT-KIMI-K26",
        volatility_class="fast",
        staleness_days=45,
        staleness_posture="block_govern",
    ),
}


class RadarFreshnessFinding(BaseModel):
    """One stale-or-due target surfaced by the sweep."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    target_key: str
    source_register: Literal["INTELLIGENCEOPS_REGISTER", "SUBSTRATE_REGISTRY"]
    verdict: Literal["FRESH", "DUE", "STALE", "NO_THRESHOLD", "SKIPPED"]
    staleness_posture: str = ""
    last_verified_at: str = ""
    next_verify_by: str = ""
    staleness_days: int | None = None
    volatility_class: str = ""
    notes: str = ""


class RadarFreshnessReport(BaseModel):
    """Aggregate sweep output."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    report_id: str
    swept_at: str
    swept_by: str
    findings: tuple[RadarFreshnessFinding, ...]
    fresh_count: int
    due_count: int
    stale_count: int
    no_threshold_count: int
    skipped_count: int
    total_findings: int


def fixture_intelligenceops_radar_row() -> IntelligenceOpsRadarRow:
    return IntelligenceOpsRadarRow(
        register_id="IO-FIXTURE-RADAR-001",
        target_id="GOI-FIXTURE-001",
        target_class="regulator",
        cadence="scheduled",
        source_type="OSINT",
        reliability="B",
        output_artifact="docs/wip/intelligence/fixture-radar-brief.md",
        responsible_role="Lead Researcher",
        lifecycle_status="active",
        intro_decision_id="D-IH-86-FG",
        linked_sop_path="docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md",
        linked_runbook_path="scripts/research_radar_sweep.py",
        notes="Self-test fixture row.",
        last_review_at="2026-05-01",
        last_review_by="Lead Researcher",
        last_review_decision_id="D-IH-86-FG",
        methodology_version_at_review="v3.2",
        volatility_class="medium",
        staleness_days="90",
        staleness_posture="cite_and_flag",
        next_verify_by="2026-08-01",
    )


def parse_iso_date(value: str) -> date | None:
    value = (value or "").strip()
    if not value:
        return None
    return date.fromisoformat(value)
