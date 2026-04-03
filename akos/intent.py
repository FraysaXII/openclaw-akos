"""Query intent classification helpers for AKOS flagship agent flows.

Keeps simple, deterministic routing heuristics in one place so prompts,
telemetry, and API surfaces can share the same decision model.
"""

from __future__ import annotations

import re
from typing import Literal

IntentRoute = Literal[
    "admin_escalate",
    "finance_research",
    "hlk_search",
    "hlk_lookup",
    "other",
]

_ADMIN_VERB_RE = re.compile(
    r"\b(restructure|change|update|add|remove|delete|create|merge|split|remediate|modify)\b",
    re.IGNORECASE,
)
_ADMIN_OBJECT_RE = re.compile(
    r"\b(role|process|area|baseline|vault|organisation|org chart|hierarchy|reporting line|csv|access level)\b",
    re.IGNORECASE,
)
_FINANCE_RE = re.compile(
    r"\b(stock|ticker|quote|price|market cap|earnings|shares|sentiment|company|equity|trading|valuation)\b",
    re.IGNORECASE,
)
_SEARCH_RE = re.compile(r"\b(search|find|look up|lookup)\b", re.IGNORECASE)
_HLK_RE = re.compile(
    r"\b(hlk|role|roles|process|processes|workstream|workstreams|project|projects|baseline|org|organisation|cto|cfo|cpo|coo|cmo|cdo)\b",
    re.IGNORECASE,
)


def classify_request(query: str) -> dict[str, object]:
    """Classify a user request into a deterministic flagship route."""
    text = query.strip()
    lowered = text.lower()

    if _ADMIN_VERB_RE.search(text) and _ADMIN_OBJECT_RE.search(text):
        return {
            "route": "admin_escalate",
            "must_escalate": True,
            "reason": "Mutation or organisational restructure intent detected.",
            "operator_message": (
                "This is a write/admin workflow and must be escalated to the Orchestrator "
                "for coordinated execution. If you want, I can first summarize the current canonical structure."
            ),
        }

    if _FINANCE_RE.search(text):
        return {
            "route": "finance_research",
            "must_escalate": False,
            "reason": "Finance research intent detected.",
            "operator_message": (
                "This is a finance research request. I should resolve the ticker first when needed, "
                "then surface source, freshness, and any degraded-state warnings."
            ),
        }

    if _SEARCH_RE.search(text) and _HLK_RE.search(text):
        return {
            "route": "hlk_search",
            "must_escalate": False,
            "reason": "Explicit HLK discovery/search phrasing detected.",
            "operator_message": (
                "This is an HLK search request. I should search silently and answer with the resolved canonical item."
            ),
        }

    if _HLK_RE.search(text):
        return {
            "route": "hlk_lookup",
            "must_escalate": False,
            "reason": "HLK lookup intent detected.",
            "operator_message": (
                "This is an HLK lookup request. I should use exact lookup first and fall back to ranked search only if needed."
            ),
        }

    return {
        "route": "other",
        "must_escalate": False,
        "reason": "No specific flagship route matched.",
        "operator_message": "No special route required.",
    }
