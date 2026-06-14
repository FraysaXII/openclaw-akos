"""Field contract for SUPABASE_REALTIME_REGISTRY.csv (I99 EG-5 / D-IH-99-J)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SUPABASE_REALTIME_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "realtime_row_id",
    "row_kind",
    "surface_key",
    "schema_table",
    "channel_name",
    "consumer_initiative",
    "consumer_binding",
    "posture",
    "owner_role",
    "last_review_decision_id",
    "notes",
)

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_REALTIME_REGISTRY.csv"
)


class SupabaseRealtimeRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    realtime_row_id: str = Field(pattern=r"^SUPA-RT-\d{2}$")
    row_kind: Literal[
        "publication",
        "table_subscription",
        "channel",
        "consumer_surface",
        "fallback_policy",
        "badge_binding",
        "rls_requirement",
        "migration_ddl",
        "presence_broadcast",
    ]
    surface_key: str = Field(min_length=1, max_length=80)
    schema_table: str = Field(default="", max_length=200)
    channel_name: str = Field(default="", max_length=80)
    consumer_initiative: str = Field(default="", max_length=64)
    consumer_binding: str = Field(default="", max_length=200)
    posture: Literal[
        "active",
        "scheduled",
        "drift",
        "polling_active",
        "polling_only",
        "out_of_scope",
    ]
    owner_role: str = Field(min_length=1, max_length=60)
    last_review_decision_id: str = Field(default="", max_length=32)
    notes: str = Field(default="", max_length=500)
