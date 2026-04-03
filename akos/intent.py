"""Query intent classification for AKOS flagship agent flows.

Uses a semantic embedding classifier (via Ollama ``nomic-embed-text``) as the
primary routing method and falls back to deterministic regex patterns when
Ollama is unreachable.  Adding a new domain means adding exemplars to
``config/intent-exemplars.json``, not writing new regex patterns.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Literal

logger = logging.getLogger("akos.intent")

IntentRoute = Literal[
    "admin_escalate",
    "finance_research",
    "hlk_search",
    "hlk_lookup",
    "gtm_project",
    "other",
]

EXEMPLARS_PATH = Path(__file__).resolve().parent.parent / "config" / "intent-exemplars.json"

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
_GTM_RE = re.compile(
    r"\b(gtm|go.to.market|launch plan|product timeline|sales tool|proof of concept|alpha release|beta release|competitive positioning|ux capability|product release)\b",
    re.IGNORECASE,
)

_ROUTE_MESSAGES: dict[str, dict[str, Any]] = {
    "admin_escalate": {
        "must_escalate": True,
        "reason": "Mutation or organisational restructure intent detected.",
        "operator_message": (
            "This is a write/admin workflow and must be escalated to the Orchestrator "
            "for coordinated execution. If you want, I can first summarize the current canonical structure."
        ),
    },
    "finance_research": {
        "must_escalate": False,
        "reason": "Finance research intent detected.",
        "operator_message": (
            "This is a finance research request. I should resolve the ticker first when needed, "
            "then surface source, freshness, and any degraded-state warnings."
        ),
    },
    "hlk_search": {
        "must_escalate": False,
        "reason": "Explicit HLK discovery/search phrasing detected.",
        "operator_message": (
            "This is an HLK search request. I should search silently and answer with the resolved canonical item."
        ),
    },
    "hlk_lookup": {
        "must_escalate": False,
        "reason": "HLK lookup intent detected.",
        "operator_message": (
            "This is an HLK lookup request. I should use exact lookup first and fall back to ranked search only if needed."
        ),
    },
    "gtm_project": {
        "must_escalate": False,
        "reason": "GTM/product/launch scope detected.",
        "operator_message": (
            "This is a GTM project query. I should look up the relevant project/workstream in the process tree."
        ),
    },
    "other": {
        "must_escalate": False,
        "reason": "No specific flagship route matched.",
        "operator_message": "No special route required.",
    },
}

_classifier_instance = None
_classifier_loaded = False


def _get_classifier():
    """Lazy-load the embedding classifier singleton."""
    global _classifier_instance, _classifier_loaded
    if _classifier_loaded:
        return _classifier_instance

    _classifier_loaded = True
    try:
        from akos.embeddings import EmbeddingClassifier
        if EXEMPLARS_PATH.exists():
            raw = json.loads(EXEMPLARS_PATH.read_text(encoding="utf-8"))
            exemplars = {k: v for k, v in raw.items() if not k.startswith("_") and isinstance(v, list)}
            _classifier_instance = EmbeddingClassifier(exemplars)
            if _classifier_instance.available:
                logger.info("Semantic intent classifier loaded (%d routes, %d exemplars)",
                            len(exemplars), sum(len(v) for v in exemplars.values()))
            else:
                _classifier_instance = None
        else:
            logger.warning("Exemplar bank not found at %s; using regex fallback only", EXEMPLARS_PATH)
    except Exception as exc:
        logger.debug("Embedding classifier init failed: %s", exc)
        _classifier_instance = None
    return _classifier_instance


def _classify_regex(query: str) -> str:
    """Deterministic regex fallback when embeddings are unavailable."""
    text = query.strip()
    if _ADMIN_VERB_RE.search(text) and _ADMIN_OBJECT_RE.search(text):
        return "admin_escalate"
    if _FINANCE_RE.search(text):
        return "finance_research"
    if _GTM_RE.search(text):
        return "gtm_project"
    if _SEARCH_RE.search(text) and _HLK_RE.search(text):
        return "hlk_search"
    if _HLK_RE.search(text):
        return "hlk_lookup"
    return "other"


def classify_request(query: str) -> dict[str, object]:
    """Classify a user request into a flagship route.

    Tries the semantic embedding classifier first, falls back to regex when
    Ollama is unreachable.  Returns ``route``, ``confidence``, ``method``,
    ``must_escalate``, ``reason``, and ``operator_message``.
    """
    text = query.strip()
    classifier = _get_classifier()

    if classifier is not None:
        result = classifier.classify(text)
        route = str(result.get("route", "other"))
        confidence = float(result.get("confidence", 0.0))
        method = result.get("method", "embedding")
    else:
        route = _classify_regex(text)
        confidence = 1.0
        method = "regex"

    route_info = _ROUTE_MESSAGES.get(route, _ROUTE_MESSAGES["other"])
    return {
        "route": route,
        "confidence": confidence,
        "method": method,
        **route_info,
    }
