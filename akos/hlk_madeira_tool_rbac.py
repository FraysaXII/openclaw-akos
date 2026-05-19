"""Pydantic SSOT for MADEIRA_TOOL_RBAC.csv per I76 P2.

Mirrors `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/MADEIRA_TOOL_RBAC.csv`.
Sister modules: akos.hlk_madeira_mode (the mode taxonomy this RBAC matrix indexes against).

Per-row primary key: `tool_id`. Per-mode permission cells use a 3-value enum (yes/no/conditional)
matching the akos-executable-process-catalog.mdc adapter-status enum pattern but specialised for
mode-vs-tool RBAC. The `conditional` value requires `conditional_constraint` to be non-empty.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


ToolPermission = Literal["yes", "no", "conditional"]
"""Per-mode permission cell value. 'conditional' MUST be paired with conditional_constraint text."""

ToolStatus = Literal["active", "experimental", "deprecated", "planned"]
"""Adapter-status-style lifecycle metadata per akos-executable-process-catalog.mdc RULE 2."""

ToolProvenance = Literal[
    "cursor-native",
    "shell",
    "mcp-server",
    "agent-skill",
    "scripts-runbook",
]
"""Where the tool surface comes from. cursor-native = built into Cursor IDE; shell = OS shell
exec; mcp-server = MCP protocol server (cursor-ide-browser / supabase / cloudflare / etc.);
agent-skill = .cursor/skills/<name>/SKILL.md invocation; scripts-runbook = scripts/<name>.py
invocation per akos-executable-process-catalog.mdc RULE 1."""


MADEIRA_TOOL_RBAC_FIELDNAMES: tuple[str, ...] = (
    "tool_id",
    "tool_category_name",
    "description",
    "allowed_in_ask",
    "allowed_in_plan",
    "allowed_in_agent",
    "allowed_in_debug",
    "allowed_in_methodology",
    "conditional_constraint",
    "representative_tools",
    "provenance",
    "status",
    "last_review",
    "last_review_decision_id",
    "notes",
)
"""Canonical 15-column header for MADEIRA_TOOL_RBAC.csv. Validator enforces exact match."""


class MadeiraToolRbacRow(BaseModel):
    """One row of MADEIRA_TOOL_RBAC.csv. Frozen + extra-forbid per CONTRIBUTING.md."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    tool_id: str = Field(..., min_length=1, pattern=r"^tool_[a-z0-9_]+$", description="PK; matches ^tool_[a-z0-9_]+$.")
    tool_category_name: str = Field(..., min_length=1, description="Human-readable category name (Title Case OK).")
    description: str = Field(..., min_length=1, description="One-line description of the tool category.")
    allowed_in_ask: ToolPermission = Field(..., description="Permission cell for Ask mode (read posture).")
    allowed_in_plan: ToolPermission = Field(..., description="Permission cell for Plan mode (read+plan-write posture).")
    allowed_in_agent: ToolPermission = Field(..., description="Permission cell for Agent mode (full posture).")
    allowed_in_debug: ToolPermission = Field(..., description="Permission cell for Debug mode (read+observability posture).")
    allowed_in_methodology: ToolPermission = Field(..., description="Permission cell for Methodology mode (methodology-checkpoint posture).")
    conditional_constraint: str = Field(
        default="",
        description="Free-text constraint that applies when any allowed_in_* cell == 'conditional'. Empty when no cell is conditional.",
    )
    representative_tools: str = Field(
        ...,
        min_length=1,
        description="Semicolon-list of specific tool names that fall into this category (e.g., 'Read;Glob;Grep;SemanticSearch').",
    )
    provenance: ToolProvenance = Field(..., description="Where the tool surface comes from.")
    status: ToolStatus = Field(..., description="Lifecycle status per akos-executable-process-catalog.mdc RULE 2.")
    last_review: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="ISO date YYYY-MM-DD.")
    last_review_decision_id: str = Field(
        ...,
        pattern=r"^D-IH-(\d{1,3}-[A-Z]{1,2}(-V\d+)?|\d{1,3}-CLOSURE(-[A-Z0-9-]+)?|OPS-\d{1,3})$",
        description="FK to DECISION_REGISTER.csv. Matches the validate_decision_register regex (standard | closure | OPS).",
    )
    notes: str = Field(default="", description="Free-text notes; can be empty.")

    @model_validator(mode="after")
    def _enforce_conditional_constraint(self) -> "MadeiraToolRbacRow":
        """If any allowed_in_* cell is 'conditional', conditional_constraint MUST be non-empty.

        Inversely, if no cell is 'conditional', conditional_constraint MUST be empty (avoids
        stale constraints lingering when permissions tighten).
        """
        has_conditional = any(
            cell == "conditional"
            for cell in (
                self.allowed_in_ask,
                self.allowed_in_plan,
                self.allowed_in_agent,
                self.allowed_in_debug,
                self.allowed_in_methodology,
            )
        )
        if has_conditional and not self.conditional_constraint.strip():
            raise ValueError(
                f"tool_id={self.tool_id}: conditional_constraint must be non-empty when any "
                "allowed_in_* cell is 'conditional'"
            )
        if not has_conditional and self.conditional_constraint.strip():
            raise ValueError(
                f"tool_id={self.tool_id}: conditional_constraint must be empty when no "
                "allowed_in_* cell is 'conditional' (stale constraint detected)"
            )
        return self


class MadeiraToolRbacRegistry(BaseModel):
    """Collection of MADEIRA_TOOL_RBAC.csv rows with uniqueness enforcement."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    rows: tuple[MadeiraToolRbacRow, ...] = Field(..., min_length=1, description="At least one tool category row.")

    @model_validator(mode="after")
    def _enforce_unique_tool_ids(self) -> "MadeiraToolRbacRegistry":
        seen: set[str] = set()
        for row in self.rows:
            if row.tool_id in seen:
                raise ValueError(f"duplicate tool_id={row.tool_id}")
            seen.add(row.tool_id)
        return self
