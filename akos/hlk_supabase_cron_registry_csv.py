"""Field contract for SUPABASE_CRON_REGISTRY.csv (I95 EG-3 / D-IH-95-G)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SUPABASE_CRON_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "job_id",
    "job_name",
    "schedule_cron",
    "target_function_slug",
    "migration_ref",
    "auth_pattern",
    "owner_role",
    "status",
    "last_review_decision_id",
    "gap",
    "notes",
)

VALID_AUTH_PATTERNS: frozenset[str] = frozenset({
    "anon_jwt_embedded",
    "service_role_vault",
    "none",
})

VALID_CRON_STATUSES: frozenset[str] = frozenset({
    "active",
    "paused",
    "deprecated",
})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_CRON_REGISTRY.csv"
)


class SupabaseCronRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    job_id: str = Field(pattern=r"^SUPA-CR-\d{2}$")
    job_name: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9_]+$")
    schedule_cron: str = Field(min_length=1, max_length=40)
    target_function_slug: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9-]+$")
    migration_ref: str = Field(min_length=1, max_length=200)
    auth_pattern: Literal["anon_jwt_embedded", "service_role_vault", "none"]
    owner_role: str = Field(min_length=1, max_length=60)
    status: Literal["active", "paused", "deprecated"]
    last_review_decision_id: str = Field(default="", max_length=32)
    gap: str = Field(default="", max_length=300)
    notes: str = Field(default="", max_length=400)
