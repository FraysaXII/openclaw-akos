"""Pydantic models for MADEIRA mode parity per I76 P1.

Mirrors `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_MODE_PARITY.md`.
Sister modules: akos.hlk_madeira_tool_csv (I76 P2 forward), akos.orthography (validator pattern reference).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


MadeiraModeId = Literal["ask", "plan", "agent", "debug", "methodology"]
"""Canonical mode identifiers per MADEIRA_MODE_PARITY.md §3.1."""

RBACPosture = Literal[
    "read",
    "read + plan-write",
    "full",
    "read + observability",
    "methodology-checkpoint",
]
"""RBAC posture per MADEIRA_MODE_PARITY.md §6 RBAC posture taxonomy."""

PersistenceDefault = Literal[
    "ephemeral",
    "plan-doc-scoped",
    "per-task",
    "session-scoped",
    "persistent-across-sessions",
]
"""Per-mode default session-state-retention discipline per MADEIRA_MODE_PARITY.md §3.2."""

ModeAddedBy = Literal["I17 P1", "I76 P1"]
"""Initiative that added the mode. Ask/Plan/Agent inherit from I17 P1; Debug/Methodology added by I76 P1."""


class MadeiraModeSpec(BaseModel):
    """Spec for one MADEIRA mode. One row per mode in the canonical."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    mode_id: MadeiraModeId = Field(..., description="Canonical mode identifier.")
    name: str = Field(..., min_length=1, description="Human-readable mode name (Title Case).")
    added_by: ModeAddedBy = Field(..., description="Initiative + phase that introduced this mode.")
    rbac_posture: RBACPosture = Field(..., description="RBAC posture (which tool category is allowed).")
    persistence_default: PersistenceDefault = Field(..., description="Default session-state-retention shape.")


class MadeiraModeRegistry(BaseModel):
    """The full set of 5 canonical MADEIRA modes. Frozen + extra-forbid for SSOT enforcement."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    modes: tuple[MadeiraModeSpec, ...] = Field(..., min_length=5, max_length=5)

    def by_id(self, mode_id: MadeiraModeId) -> MadeiraModeSpec:
        for spec in self.modes:
            if spec.mode_id == mode_id:
                return spec
        raise KeyError(f"mode_id not in registry: {mode_id!r}")


CANONICAL_MODE_SPECS: tuple[MadeiraModeSpec, ...] = (
    MadeiraModeSpec(
        mode_id="ask",
        name="Ask",
        added_by="I17 P1",
        rbac_posture="read",
        persistence_default="ephemeral",
    ),
    MadeiraModeSpec(
        mode_id="plan",
        name="Plan",
        added_by="I17 P1",
        rbac_posture="read + plan-write",
        persistence_default="plan-doc-scoped",
    ),
    MadeiraModeSpec(
        mode_id="agent",
        name="Agent",
        added_by="I17 P1",
        rbac_posture="full",
        persistence_default="per-task",
    ),
    MadeiraModeSpec(
        mode_id="debug",
        name="Debug",
        added_by="I76 P1",
        rbac_posture="read + observability",
        persistence_default="session-scoped",
    ),
    MadeiraModeSpec(
        mode_id="methodology",
        name="Methodology",
        added_by="I76 P1",
        rbac_posture="methodology-checkpoint",
        persistence_default="persistent-across-sessions",
    ),
)
"""Canonical 5-mode registry per MADEIRA_MODE_PARITY.md §3.1. Frozen tuple = SSOT."""


CANONICAL_REGISTRY = MadeiraModeRegistry(modes=CANONICAL_MODE_SPECS)
"""Singleton canonical registry. Importable for any code that needs to enumerate modes."""
