"""Initiative 45 P3 — Skill router (the missing middle of the registry-router triangle).

Closes the gap that ``akos.intent.classify_request`` consults
``config/intent-exemplars.json`` for routing but never consults
``SKILL_REGISTRY.csv`` (evidence-matrix E2). This module reads the registry
and resolves an intent route → list of candidate skills.

Used by ``akos.intent.classify_request`` (P3 enriches its response with
``candidate_skills``) and by future per-skill execution paths (P5+, I46 P3,
Initiative 34 multi-tenant).

Routing condition DSL (I45 P3 minimum, per Abstract Algorithms minimum
contract):

- empty               → always-eligible (back-compat)
- intent_in=R1;R2;R3  → eligible when classify_request returns route in {R1,R2,R3}
- intent=R            → eligible when classify_request returns route R (singular)
- agent=A             → eligible only when the calling agent is A

The DSL is intentionally minimal in P3. P7 promotion-gate enforces non-empty
``routing_condition``; richer expressions land in I47+ if needed.
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("akos.skill_router")

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "SKILL_REGISTRY.csv"
)


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def load_skills(*, csv_path: Path | None = None, active_only: bool = True) -> list[dict[str, str]]:
    """Load all skills from SKILL_REGISTRY.csv.

    Returns a list of dicts (one per row). When ``active_only`` is True (default),
    rows with ``lifecycle_status != 'active'`` are filtered out.
    """
    path = csv_path or SKILL_CSV
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if active_only:
        rows = [r for r in rows if (r.get("lifecycle_status") or "").strip() == "active"]
    return rows


def parse_routing_condition(rc: str) -> dict[str, Any]:
    """Parse the routing_condition string into a structured filter.

    Returns one of:
    - {"kind": "always"}                                  empty input
    - {"kind": "intent_in", "intents": [...]}              intent_in=R1;R2
    - {"kind": "intent",    "intent": "R"}                 intent=R
    - {"kind": "agent",     "agent": "A"}                  agent=A
    - {"kind": "invalid",   "raw": "<input>"}              unparseable
    """
    rc = (rc or "").strip()
    if not rc:
        return {"kind": "always"}
    if "=" not in rc:
        return {"kind": "invalid", "raw": rc}
    key, _, val = rc.partition("=")
    key = key.strip().lower()
    val = val.strip()
    if key == "intent_in":
        intents = [i.strip() for i in val.split(";") if i.strip()]
        if not intents:
            return {"kind": "invalid", "raw": rc}
        return {"kind": "intent_in", "intents": intents}
    if key == "intent":
        if not val:
            return {"kind": "invalid", "raw": rc}
        return {"kind": "intent", "intent": val}
    if key == "agent":
        if not val:
            return {"kind": "invalid", "raw": rc}
        return {"kind": "agent", "agent": val}
    return {"kind": "invalid", "raw": rc}


def matches(condition: dict[str, Any], *, intent_route: str | None, agent: str | None) -> bool:
    """Return True if the parsed condition matches the given context."""
    kind = condition.get("kind", "always")
    if kind == "always":
        return True
    if kind == "intent_in":
        return intent_route in (condition.get("intents") or [])
    if kind == "intent":
        return intent_route == condition.get("intent")
    if kind == "agent":
        return agent == condition.get("agent")
    return False  # invalid


def candidate_skills(
    intent_route: str,
    *,
    agent: str | None = None,
    skills: list[dict[str, str]] | None = None,
    csv_path: Path | None = None,
) -> list[dict[str, str]]:
    """Return active skills whose routing_condition matches (intent_route, agent).

    A skill matches if EITHER:
    - Its routing_condition matches via ``matches()``, OR
    - Its routing_condition is empty (always-eligible) AND the calling agent is in
      the skill's agents_supported list (or skill is ``shared``).

    When ``agent`` is None, only routing_condition-driven matches are considered
    (no agent-side constraint applied).
    """
    skills = skills if skills is not None else load_skills(csv_path=csv_path)
    out: list[dict[str, str]] = []
    for s in skills:
        rc = parse_routing_condition(s.get("routing_condition", ""))
        if matches(rc, intent_route=intent_route, agent=agent):
            if rc.get("kind") == "always" and agent is not None:
                supported = _split_semi(s.get("agents_supported", ""))
                if "shared" not in supported and agent not in supported:
                    continue
            out.append(s)
    return out


def candidate_skill_ids(
    intent_route: str,
    *,
    agent: str | None = None,
    skills: list[dict[str, str]] | None = None,
    csv_path: Path | None = None,
) -> list[str]:
    """Convenience: same as candidate_skills() but returns skill_id strings only."""
    return [s["skill_id"] for s in candidate_skills(intent_route, agent=agent, skills=skills, csv_path=csv_path)]
