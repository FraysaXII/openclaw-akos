"""Field contract for SUPABASE_AUTH_REGISTRY.csv (I99 EG-5 / D-IH-99-J)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SUPABASE_AUTH_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "auth_row_id",
    "row_kind",
    "surface_key",
    "config_surface",
    "consumer_initiative",
    "consumer_binding",
    "posture",
    "owner_role",
    "last_review_decision_id",
    "notes",
)

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_AUTH_REGISTRY.csv"
)


class SupabaseAuthRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    auth_row_id: str = Field(pattern=r"^SUPA-AUTH-\d{2}$")
    row_kind: Literal[
        "provider",
        "redirect_url",
        "smtp",
        "email_template",
        "hook",
        "session_policy",
        "rbac_post_auth",
        "consumer_route",
        "env_var",
    ]
    surface_key: str = Field(min_length=1, max_length=80)
    config_surface: str = Field(default="", max_length=200)
    consumer_initiative: str = Field(default="", max_length=64)
    consumer_binding: str = Field(default="", max_length=200)
    posture: Literal["active", "scheduled", "parked", "drift"]
    owner_role: str = Field(min_length=1, max_length=60)
    last_review_decision_id: str = Field(default="", max_length=32)
    notes: str = Field(default="", max_length=500)
