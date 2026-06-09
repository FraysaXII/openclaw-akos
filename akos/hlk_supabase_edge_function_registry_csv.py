"""Field contract for SUPABASE_EDGE_FUNCTION_REGISTRY.csv (I95 EG-3 / D-IH-95-G)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SUPABASE_EDGE_FUNCTION_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "function_id",
    "function_slug",
    "repo_path",
    "invoke_pattern",
    "verify_jwt",
    "owner_role",
    "rpa_adapter_id",
    "status",
    "last_review_decision_id",
    "notes",
)

VALID_INVOKE_PATTERNS: frozenset[str] = frozenset({
    "webhook",
    "cron",
    "manual",
    "hybrid",
})

VALID_EDGE_STATUSES: frozenset[str] = frozenset({
    "active",
    "deprecated",
    "forward",
})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_EDGE_FUNCTION_REGISTRY.csv"
)


class SupabaseEdgeFunctionRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    function_id: str = Field(pattern=r"^SUPA-EF-\d{2}$")
    function_slug: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9-]+$")
    repo_path: str = Field(min_length=1, max_length=200)
    invoke_pattern: Literal["webhook", "cron", "manual", "hybrid"]
    verify_jwt: Literal["true", "false"]
    owner_role: str = Field(min_length=1, max_length=60)
    rpa_adapter_id: str = Field(default="", max_length=64)
    status: Literal["active", "deprecated", "forward"]
    last_review_decision_id: str = Field(default="", max_length=32)
    notes: str = Field(default="", max_length=400)
