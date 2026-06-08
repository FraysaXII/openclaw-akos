"""Field contract for BUILDOUT_BACKLOG.csv (D-IH-95-I).

The build-out backlog registry: the home for the 578 task-grain Trello/mind-map micro-step rows
DEMOTED out of the canonical process_list during the D-IH-95-I radical cleanup. They are NOT
deleted — they survive here as capability *realizations* (the de-densified capabilities'
`originating_process_ids` may reference these item_ids), so the canonical process catalog stays
strategy-legible (~501 stable processes) while the build-out detail remains governed + referenceable.

Lean schema (subset of process_list essentials + demotion provenance). item_id is the key and must
stay globally unique vs process_list (no id collision across the two catalogs).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

BUILDOUT_BACKLOG_FIELDNAMES: tuple[str, ...] = (
    "item_id",
    "item_name",
    "area",
    "role_owner",
    "item_granularity",
    "item_parent_id",
    "description",
    "backlog_class",
    "demoted_at",
    "demoted_decision_id",
    "notes",
)

VALID_BACKLOG_CLASSES: frozenset[str] = frozenset({
    "trello-task-grain", "madeira-product-backlog", "brand-todo", "team-todo", "research-task",
})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/BUILDOUT_BACKLOG.csv"
)


class BuildoutBacklogRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    item_id: str = Field(min_length=2, max_length=80)
    item_name: str = Field(min_length=1, max_length=400)
    area: str = Field(min_length=1, max_length=32)
    role_owner: str = Field(default="", max_length=120)
    item_granularity: Literal["", "project", "workstream", "process", "activity", "task"] = ""
    item_parent_id: str = Field(default="", max_length=80)
    description: str = Field(default="", max_length=2000)
    backlog_class: str = ""
    demoted_at: str = Field(default="", max_length=10)
    demoted_decision_id: str = Field(default="", max_length=32)
    notes: str = Field(default="", max_length=600)
