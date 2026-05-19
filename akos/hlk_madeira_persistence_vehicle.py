"""Pydantic SSOT for MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv per I76 P3.

Mirrors `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv`.
Sister modules: akos.hlk_madeira_mode (the mode taxonomy that names methodology-mode persistence
vehicles); akos.hlk_madeira_tool_rbac (the tool catalog that authorises vehicle writes).

Operator framing per I76 P3 axis 1 ratify (2026-05-19, novel option d): persistence vehicles must
be REGISTRY-SHAPED + scalable + co-designed — not hardcoded into a prose SOP. Each row carries its
own `staleness_days` + `staleness_posture` so vehicle-specific staleness cadence is parameterized
(operator framing per I76 P3 axis 2 ratify: hardcoded N=90 days for DECISION_REGISTER doesn't
generalise; LOGIC_CHANGE_LOG, scratchpads, future-AIC-readable handoff vehicles all need their own
threshold).

Schema refined per I76 P3 strawman-research subagent findings (2026-05-19): added six columns over
the original 14-col strawman per inside-repo dimension-CSV precedent + outside-industry agent-memory
framework convergence (LangGraph long-term memory, Letta MemGPT, mem0, Anthropic Memory tool). Net
schema = 21 columns. Rejected `rotation_cadence` (redundant with read_cadence + vehicle_scope) and
`access_level` (redundant with target_audience).

Per-row primary key: `vehicle_id`. Per-row constraints:
- `staleness_days` non-empty REQUIRES `staleness_posture` in {`cite_and_flag`, `refuse_without_ratify`}
- `staleness_posture == none` REQUIRES `staleness_days` empty (no stale constraint detection)
- vehicle_id is globally unique within the registry
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


VehicleScope = Literal[
    "per_session",
    "cross_session",
    "methodology_scoped",
    "wave_bounded",
]
"""Where the vehicle's freshness boundary is. per_session = lives within one chat session;
cross_session = persistent across sessions; methodology_scoped = persistent across sessions AND
canonical-grade (the LOGIC_CHANGE_LOG / DECISION_REGISTER class); wave_bounded = persistent
within an I86-style execution wave + drained at wave boundary (the operator-scratchpad pattern)."""

TargetAudience = Literal[
    "operator_private",
    "operator_plus_aics",
    "external_handoff",
]
"""Who can READ the vehicle. operator_private = current operator only (J-OP audience);
operator_plus_aics = operator + future AICs in the same role-class (J-OP + AI O5-1 role-class);
external_handoff = also reachable by external-handoff AICs / human receivers when their engagement
exposes a quoted decision (J-AD / J-CU / J-PT post-NDA audiences). Semicolon-list when multiple."""

WriteAuthority = Literal[
    "operator_only",
    "madeira_writes_flagged",
    "agent_writes_auto",
]
"""Who can WRITE to the vehicle. operator_only = operator types the bytes (Madeira may surface
candidate text via AskQuestion but never writes); madeira_writes_flagged = Madeira may write
when operator ratifies inline + the write is committed via git (mechanical trail); agent_writes_auto
= an agent / runbook writes automatically without per-write ratification (typically per-session
ephemeral surfaces; should be rare for cross-session vehicles)."""

ReadCadence = Literal[
    "every_session",
    "on_demand",
    "methodology_checkpoint",
    "wave_boundary",
    "next_session_entry",
]
"""When Madeira reads the vehicle. every_session = at every chat session start; on_demand = only
when relevant (search-shaped, not read-shaped); methodology_checkpoint = at each LOGIC_CHANGE_LOG
candidate moment + each decision-row mint; wave_boundary = at I86-wave entry + exit;
next_session_entry = once at the start of the immediately-following session, then archived."""

StalenessPosture = Literal[
    "none",
    "cite_and_flag",
    "refuse_without_ratify",
]
"""What Madeira does when reading a row older than `staleness_days`. none = no staleness check
(treat as fresh; rely on reversibility metadata); cite_and_flag = quote + append staleness note
inline (operator decides whether to re-ratify); refuse_without_ratify = surface AskQuestion gate
before acting on the row (highest discipline; reserved for highest-blast-radius decisions)."""

VehicleProvenance = Literal[
    "canonical_csv",
    "markdown_log",
    "git_tracked_md",
    "external_system",
    "agent_private",
]
"""Where the vehicle lives. canonical_csv = a canonical-CSV per PRECEDENCE.md (DECISION_REGISTER,
INITIATIVE_REGISTRY class); markdown_log = a canonical markdown log per PRECEDENCE.md
(LOGIC_CHANGE_LOG class); git_tracked_md = a non-canonical but git-tracked markdown file
(operator-scratchpad, _trackers/, reports/ class); external_system = a system outside the repo
(Cursor memory, MCP-server state, Supabase row); agent_private = a Madeira-only file under
.cursor/madeira/ that operator can read but does not author."""

MemoryClass = Literal[
    "semantic",
    "episodic",
    "procedural",
    "working",
    "organizational",
]
"""Convergent industry taxonomy for agent memory class. semantic = facts + concepts (brand
canonicals; KM topic substrate); episodic = time-bound events + states (transcripts; scratchpads;
audit trails); procedural = rules + skills + methodology (decisions; logic-change-log; cursor-rules);
working = active task scratch (per-session; ephemeral); organizational = enterprise-scale shared
state (initiative-registry; cross-initiative coordination). Per LangGraph long-term memory taxonomy
+ mem0 entity-linked taxonomy + Letta MemGPT tier model + Zylos 2026 review."""

VehicleStatus = Literal[
    "active",
    "inactive",
    "planned",
    "deprecated",
    "experimental",
]
"""Adapter-status-style lifecycle metadata per akos-executable-process-catalog.mdc RULE 2."""

MethodologyVersion = Literal["v3.0", "v3.1"]
"""HLK methodology version at last review. Matches all 14 surveyed dimension CSVs convention."""


MADEIRA_PERSISTENCE_VEHICLE_FIELDNAMES: tuple[str, ...] = (
    "vehicle_id",
    "vehicle_name",
    "vehicle_path",
    "vehicle_scope",
    "target_audience",
    "write_authority",
    "read_cadence",
    "staleness_days",
    "staleness_posture",
    "provenance",
    "memory_class",
    "owner_role",
    "topic_ids",
    "depends_on_vehicle_ids",
    "status",
    "added_at",
    "last_review_at",
    "last_review_by",
    "methodology_version_at_review",
    "last_review_decision_id",
    "notes",
)
"""Canonical 21-column header for MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv. Validator enforces exact match."""


_VEHICLE_ID_PATTERN = r"^vehicle_[a-z0-9_]+$"
_ISO_DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"
_DECISION_ID_PATTERN = (
    r"^D-IH-(\d{1,3}-[A-Z]{1,2}(-V\d+)?|\d{1,3}-CLOSURE(-[A-Z0-9-]+)?|OPS-\d{1,3})$"
)
_TOPIC_ID_PATTERN = r"^topic_[a-z0-9_]+$"
_OWNER_ROLE_MIN_LENGTH = 2


def _validate_target_audience_list(value: str) -> str:
    """target_audience is a semicolon-list of TargetAudience values. Empty = invalid."""
    if not value.strip():
        raise ValueError("target_audience must be non-empty")
    valid = {"operator_private", "operator_plus_aics", "external_handoff"}
    items = [item.strip() for item in value.split(";") if item.strip()]
    if not items:
        raise ValueError("target_audience must contain at least one entry")
    for item in items:
        if item not in valid:
            raise ValueError(
                f"target_audience entry '{item}' not in {sorted(valid)}"
            )
    if len(items) != len(set(items)):
        raise ValueError(f"target_audience has duplicate entries: {value}")
    return value


def _validate_optional_semicolon_id_list(value: str, *, pattern: str, field_name: str) -> str:
    """Generic validator for semicolon-list of pattern-matched IDs. Empty allowed."""
    if not value.strip():
        return value
    import re

    compiled = re.compile(pattern)
    items = [item.strip() for item in value.split(";") if item.strip()]
    for item in items:
        if not compiled.match(item):
            raise ValueError(
                f"{field_name} entry '{item}' does not match pattern {pattern}"
            )
    if len(items) != len(set(items)):
        raise ValueError(f"{field_name} has duplicate entries: {value}")
    return value


class MadeiraPersistenceVehicleRow(BaseModel):
    """One row of MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv. Frozen + extra-forbid per CONTRIBUTING.md."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    vehicle_id: str = Field(..., min_length=1, pattern=_VEHICLE_ID_PATTERN, description="PK; matches ^vehicle_[a-z0-9_]+$.")
    vehicle_name: str = Field(..., min_length=1, description="Human-readable name (Title Case OK).")
    vehicle_path: str = Field(
        ...,
        min_length=1,
        description="Repo-relative file path / path-pattern / schema reference (e.g., 'docs/.../DECISION_REGISTER.csv', 'docs/wip/planning/<NN>/decision-log.md', or 'cursor:memory' for external systems).",
    )
    vehicle_scope: VehicleScope = Field(..., description="Freshness boundary of the vehicle.")
    target_audience: str = Field(
        ...,
        min_length=1,
        description="Semicolon-list of TargetAudience values; validated post-parse.",
    )
    write_authority: WriteAuthority = Field(..., description="Who can write to the vehicle.")
    read_cadence: ReadCadence = Field(..., description="When Madeira reads the vehicle.")
    staleness_days: Optional[int] = Field(
        default=None,
        ge=1,
        description="Number of days before a row is flagged stale. Empty (null) = no staleness check.",
    )
    staleness_posture: StalenessPosture = Field(
        ...,
        description="What Madeira does on stale read. Must align with staleness_days emptiness.",
    )
    provenance: VehicleProvenance = Field(..., description="Where the vehicle lives.")
    memory_class: MemoryClass = Field(
        ...,
        description="Industry-convergent memory taxonomy: semantic/episodic/procedural/working/organizational.",
    )
    owner_role: str = Field(
        ...,
        min_length=_OWNER_ROLE_MIN_LENGTH,
        description="Role accountable for the vehicle (drawn from baseline_organisation.csv role_name; e.g., 'PMO', 'System Owner', 'Madeira', 'Operator', 'Compliance Officer').",
    )
    topic_ids: str = Field(
        default="",
        description="Semicolon-list FK to TOPIC_REGISTRY.csv topic_id (pattern ^topic_[a-z0-9_]+$). Empty allowed.",
    )
    depends_on_vehicle_ids: str = Field(
        default="",
        description="Semicolon-list self-FK to other vehicle_id rows (vehicle this vehicle depends on; pattern ^vehicle_[a-z0-9_]+$). Empty allowed.",
    )
    status: VehicleStatus = Field(..., description="Lifecycle status per akos-executable-process-catalog.mdc RULE 2.")
    added_at: str = Field(..., pattern=_ISO_DATE_PATTERN, description="ISO date YYYY-MM-DD when the row was minted.")
    last_review_at: str = Field(..., pattern=_ISO_DATE_PATTERN, description="ISO date YYYY-MM-DD of last review.")
    last_review_by: str = Field(
        ...,
        min_length=_OWNER_ROLE_MIN_LENGTH,
        description="Role of last reviewer (e.g., 'PMO', 'System Owner', 'Founder').",
    )
    methodology_version_at_review: MethodologyVersion = Field(
        ...,
        description="HLK methodology version at last review. Matches all 14 surveyed dimension CSVs convention.",
    )
    last_review_decision_id: str = Field(
        ...,
        pattern=_DECISION_ID_PATTERN,
        description="FK to DECISION_REGISTER.csv. Matches validate_decision_register regex.",
    )
    notes: str = Field(default="", description="Free-text notes; can be empty.")

    @model_validator(mode="after")
    def _enforce_target_audience_semicolon_list(self) -> "MadeiraPersistenceVehicleRow":
        _validate_target_audience_list(self.target_audience)
        return self

    @model_validator(mode="after")
    def _enforce_topic_ids_format(self) -> "MadeiraPersistenceVehicleRow":
        _validate_optional_semicolon_id_list(
            self.topic_ids, pattern=_TOPIC_ID_PATTERN, field_name="topic_ids"
        )
        return self

    @model_validator(mode="after")
    def _enforce_depends_on_format(self) -> "MadeiraPersistenceVehicleRow":
        _validate_optional_semicolon_id_list(
            self.depends_on_vehicle_ids,
            pattern=_VEHICLE_ID_PATTERN,
            field_name="depends_on_vehicle_ids",
        )
        # Self-dependency check
        items = {item.strip() for item in self.depends_on_vehicle_ids.split(";") if item.strip()}
        if self.vehicle_id in items:
            raise ValueError(
                f"vehicle_id={self.vehicle_id}: self-dependency forbidden in depends_on_vehicle_ids"
            )
        return self

    @model_validator(mode="after")
    def _enforce_staleness_alignment(self) -> "MadeiraPersistenceVehicleRow":
        """staleness_days + staleness_posture must align.

        Rules:
        - posture == 'none' REQUIRES staleness_days empty (null). Otherwise stale-constraint drift.
        - posture in {'cite_and_flag', 'refuse_without_ratify'} REQUIRES staleness_days non-empty.
        """
        if self.staleness_posture == "none" and self.staleness_days is not None:
            raise ValueError(
                f"vehicle_id={self.vehicle_id}: staleness_posture='none' requires staleness_days empty "
                f"(got {self.staleness_days}); set posture to cite_and_flag/refuse_without_ratify if you "
                "want a staleness threshold"
            )
        if self.staleness_posture != "none" and self.staleness_days is None:
            raise ValueError(
                f"vehicle_id={self.vehicle_id}: staleness_posture='{self.staleness_posture}' requires "
                "staleness_days non-empty (specify the day threshold)"
            )
        return self


class MadeiraPersistenceVehicleRegistry(BaseModel):
    """Collection of MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv rows with uniqueness + FK closure enforcement."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    rows: tuple[MadeiraPersistenceVehicleRow, ...] = Field(..., min_length=1, description="At least one vehicle row.")

    @model_validator(mode="after")
    def _enforce_unique_vehicle_ids(self) -> "MadeiraPersistenceVehicleRegistry":
        seen: set[str] = set()
        for row in self.rows:
            if row.vehicle_id in seen:
                raise ValueError(f"duplicate vehicle_id={row.vehicle_id}")
            seen.add(row.vehicle_id)
        return self

    @model_validator(mode="after")
    def _enforce_depends_on_closure(self) -> "MadeiraPersistenceVehicleRegistry":
        """depends_on_vehicle_ids entries must reference vehicle_ids that exist in this registry."""
        ids = {row.vehicle_id for row in self.rows}
        for row in self.rows:
            if not row.depends_on_vehicle_ids:
                continue
            deps = {item.strip() for item in row.depends_on_vehicle_ids.split(";") if item.strip()}
            unknown = deps - ids
            if unknown:
                raise ValueError(
                    f"vehicle_id={row.vehicle_id}: depends_on_vehicle_ids references unknown vehicles: {sorted(unknown)}"
                )
        return self
