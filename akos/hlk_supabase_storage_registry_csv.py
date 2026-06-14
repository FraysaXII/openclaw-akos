"""Field contract for SUPABASE_STORAGE_REGISTRY.csv (I99 EG-5 / D-IH-99-J)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SUPABASE_STORAGE_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "storage_row_id",
    "row_kind",
    "bucket_id",
    "path_prefix",
    "visibility",
    "consumer_initiative",
    "consumer_binding",
    "posture",
    "owner_role",
    "last_review_decision_id",
    "notes",
)

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_STORAGE_REGISTRY.csv"
)


class SupabaseStorageRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    storage_row_id: str = Field(pattern=r"^SUPA-ST-\d{2}$")
    row_kind: Literal[
        "module",
        "bucket_drift",
        "ssot_active",
        "bucket",
        "path_rule",
        "rls_policy",
        "delivery_posture",
        "analytics_bucket",
        "vector_bucket",
        "migration_ddl",
        "analytics_namespace",
        "extension_link",
        "cross_tier_link",
    ]
    bucket_id: str = Field(default="", max_length=120)
    path_prefix: str = Field(default="", max_length=200)
    visibility: str = Field(default="", max_length=80)
    consumer_initiative: str = Field(default="", max_length=64)
    consumer_binding: str = Field(default="", max_length=200)
    posture: Literal[
        "active",
        "scheduled",
        "drift",
        "coordinated",
        "git_repo",
    ]
    owner_role: str = Field(min_length=1, max_length=60)
    last_review_decision_id: str = Field(default="", max_length=32)
    notes: str = Field(default="", max_length=500)
