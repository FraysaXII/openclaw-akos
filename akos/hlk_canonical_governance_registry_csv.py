"""Field contract for CANONICAL_GOVERNANCE_REGISTRY.csv (I95 P95-GOV-1; D-IH-95-B).

Universal vault CSV governance inventory: Plane-1 validator wiring + Plane-2 mirror posture
for every canonical CSV under ``docs/references/hlk/v3.0/**/canonicals/**/*.csv``.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

CANONICAL_GOVERNANCE_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "governance_id",
    "csv_path",
    "owning_area",
    "owning_role",
    "asset_class",
    "plane1_validator",
    "plane1_in_validate_hlk",
    "plane2_mirror_table",
    "plane2_sync_policy",
    "plane2_emit_profile",
    "plane2_workflow_paths",
    "precedence_registered",
    "canonical_registry_id",
    "mirror_ddl_migration",
    "enum_parity_required",
    "delete_reconcile_pk",
    "last_review",
    "last_review_decision_id",
    "status",
    "notes",
)

VALID_ASSET_CLASSES: frozenset[str] = frozenset({
    "compliance_mirror",
    "finops_mirror",
    "data_contract_mirror",
    "git_only",
    "graph_projection",
    "forward_charter",
})

VALID_PLANE2_SYNC_POLICIES: frozenset[str] = frozenset({
    "active",
    "forward_charter",
    "git_only",
    "graph_projection",
    "disabled",
})

VALID_PLANE2_EMIT_PROFILES: frozenset[str] = frozenset({
    "main",
    "gap_splice",
    "scoped_flag",
    "none",
})

VALID_STATUSES: frozenset[str] = frozenset({"active", "planned", "deprecated"})

# Charter §2 summary cites 74; filesystem inventory at P95-GOV-1 mint is 73 (41 Compliance + 32 sibling).
EXPECTED_VAULT_CSV_COUNT: int = 73

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/"
    "CANONICAL_GOVERNANCE_REGISTRY.csv"
)


class CanonicalGovernanceRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    governance_id: str = Field(min_length=4, max_length=80, pattern=r"^gov_[a-z0-9_]+$")
    csv_path: str = Field(min_length=10, max_length=400)
    owning_area: str = Field(min_length=2, max_length=64)
    owning_role: str = Field(min_length=1, max_length=120)
    asset_class: str
    plane1_validator: str = Field(min_length=1, max_length=120)
    plane1_in_validate_hlk: Literal["true", "false"]
    plane2_mirror_table: str = Field(default="", max_length=120)
    plane2_sync_policy: str
    plane2_emit_profile: str = Field(default="", max_length=32)
    plane2_workflow_paths: str = Field(default="", max_length=400)
    precedence_registered: Literal["true", "false"]
    canonical_registry_id: str = Field(default="", max_length=80)
    mirror_ddl_migration: str = Field(default="", max_length=120)
    enum_parity_required: Literal["true", "false"]
    delete_reconcile_pk: str = Field(default="", max_length=64)
    last_review: str = Field(default="", max_length=10)
    last_review_decision_id: str = Field(default="", max_length=32)
    status: Literal["active", "planned", "deprecated"] = "active"
    notes: str = Field(default="", max_length=600)

    @field_validator("asset_class")
    @classmethod
    def _asset_class(cls, v: str) -> str:
        if v not in VALID_ASSET_CLASSES:
            raise ValueError(f"asset_class must be one of {sorted(VALID_ASSET_CLASSES)}")
        return v

    @field_validator("plane2_sync_policy")
    @classmethod
    def _plane2_sync(cls, v: str) -> str:
        if v not in VALID_PLANE2_SYNC_POLICIES:
            raise ValueError(f"plane2_sync_policy must be one of {sorted(VALID_PLANE2_SYNC_POLICIES)}")
        return v

    @field_validator("plane2_emit_profile")
    @classmethod
    def _emit_profile(cls, v: str) -> str:
        if v and v not in VALID_PLANE2_EMIT_PROFILES:
            raise ValueError(f"plane2_emit_profile must be one of {sorted(VALID_PLANE2_EMIT_PROFILES)}")
        return v

    @field_validator("last_review")
    @classmethod
    def _last_review(cls, v: str) -> str:
        if v and (len(v) != 10 or v[4] != "-" or v[7] != "-"):
            raise ValueError("last_review must be YYYY-MM-DD or empty")
        return v
