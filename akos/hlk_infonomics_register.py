"""Shared Infonomics register economic-hook enums (Initiative 97 P6b-CSV).

Pairs with ``INFONOMICS_DISCIPLINE.md`` §4 register amend targets.
"""

from __future__ import annotations

import re

VALID_ECONOMIC_VALUE_CLASSES: frozenset[str] = frozenset({
    "rework_avoided",
    "revenue_enabled",
    "risk_reduced",
    "opex_only",
    "unclassified",
})

VALID_CARRYING_COST_BANDS: frozenset[str] = frozenset({
    "negligible",
    "low",
    "medium",
    "high",
})

VALID_HANDOFF_COST_BANDS: frozenset[str] = frozenset(VALID_CARRYING_COST_BANDS)

VALID_MONETIZATION_STATUSES: frozenset[str] = frozenset({
    "not_applicable",
    "indirect",
    "direct",
    "deferred",
})

VALID_REVOPS_VALUE_STREAM_IDS: frozenset[str] = frozenset({
    "vs_engagement_to_finops",
    "vs_engagement_to_people",
    "vs_engagement_to_legal",
    "vs_engagement_to_madeira",
})

INFORMATION_ASSET_REF_RE = re.compile(
    r"^(DC-HOL-[A-Z0-9-]+|[a-z][a-z0-9_]{2,79})$"
)
