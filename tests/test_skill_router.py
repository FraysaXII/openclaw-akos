"""Initiative 45 P3 — Tests for the skill router (registry-router gap closer).

Asserts:
- Routing condition DSL parser handles all 4 forms (always / intent_in / intent / agent)
- candidate_skills() respects routing_condition + agents_supported
- intent.classify_request emits candidate_skills field (closes evidence-matrix E2)
- Invalid routing_condition is parsed defensively (returns kind='invalid')
- Soft-fail: classify_request continues to work if SKILL_REGISTRY is unavailable
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from akos.skill_router import (
    candidate_skill_ids,
    candidate_skills,
    load_skills,
    matches,
    parse_routing_condition,
)


# ── DSL parser ────────────────────────────────────────────────────────────────


def test_parse_empty_returns_always() -> None:
    assert parse_routing_condition("")["kind"] == "always"
    assert parse_routing_condition("   ")["kind"] == "always"


def test_parse_intent_in_with_csv_routes() -> None:
    c = parse_routing_condition("intent_in=hlk_lookup;hlk_search")
    assert c["kind"] == "intent_in"
    assert c["intents"] == ["hlk_lookup", "hlk_search"]


def test_parse_intent_singular() -> None:
    c = parse_routing_condition("intent=hlk_lookup")
    assert c["kind"] == "intent"
    assert c["intent"] == "hlk_lookup"


def test_parse_agent() -> None:
    c = parse_routing_condition("agent=architect")
    assert c["kind"] == "agent"
    assert c["agent"] == "architect"


def test_parse_invalid_unknown_key() -> None:
    c = parse_routing_condition("foo=bar")
    assert c["kind"] == "invalid"


def test_parse_invalid_empty_value() -> None:
    c = parse_routing_condition("intent=")
    assert c["kind"] == "invalid"


def test_parse_invalid_no_eq() -> None:
    c = parse_routing_condition("hlk_lookup")
    assert c["kind"] == "invalid"


# ── matches() ─────────────────────────────────────────────────────────────────


def test_matches_always_is_unconditional() -> None:
    cond = {"kind": "always"}
    assert matches(cond, intent_route=None, agent=None)
    assert matches(cond, intent_route="hlk_lookup", agent="madeira")


def test_matches_intent_in_hits_and_misses() -> None:
    cond = parse_routing_condition("intent_in=hlk_lookup;hlk_search")
    assert matches(cond, intent_route="hlk_lookup", agent=None)
    assert matches(cond, intent_route="hlk_search", agent=None)
    assert not matches(cond, intent_route="finance_research", agent=None)


def test_matches_agent_hits_and_misses() -> None:
    cond = parse_routing_condition("agent=architect")
    assert matches(cond, intent_route="anything", agent="architect")
    assert not matches(cond, intent_route="anything", agent="madeira")


def test_matches_invalid_returns_false() -> None:
    cond = {"kind": "invalid"}
    assert not matches(cond, intent_route="hlk_lookup", agent="madeira")


# ── candidate_skills against the live registry ────────────────────────────────


def test_load_skills_returns_5_active_skills() -> None:
    skills = load_skills()
    assert len(skills) == 5
    assert all(s.get("lifecycle_status") == "active" for s in skills)


def test_load_skills_excludes_inactive_when_filter_on(tmp_path: Path) -> None:
    csv_path = tmp_path / "skills.csv"
    csv_path.write_text(
        "skill_id,name,lifecycle_status,agents_supported,routing_condition\n"
        "SKILL-X-V1,X,active,madeira,\n"
        "SKILL-Y-V1,Y,deprecated,madeira,\n",
        encoding="utf-8",
    )
    active = load_skills(csv_path=csv_path, active_only=True)
    all_rows = load_skills(csv_path=csv_path, active_only=False)
    assert len(active) == 1
    assert len(all_rows) == 2


def test_candidate_skills_for_hlk_lookup_returns_madeira() -> None:
    sids = candidate_skill_ids("hlk_lookup", agent="madeira")
    assert "SKILL-MADEIRA-LOOKUP-V1" in sids


def test_candidate_skills_for_admin_escalate_excludes_lookup() -> None:
    sids = candidate_skill_ids("admin_escalate", agent="architect")
    assert "SKILL-MADEIRA-LOOKUP-V1" not in sids
    # Architect skill is agent-conditioned, so always-eligible filter doesn't apply.
    assert "SKILL-ARCHITECT-PLAN-V1" in sids


def test_candidate_skills_shared_locale_is_always_returned_when_agent_none() -> None:
    """SHARED-LOCALE-DETECT has empty routing_condition AND agents_supported='shared',
    so when agent is None it should be returned (always-eligible, no agent gate)."""
    sids = candidate_skill_ids("any_route", agent=None)
    assert "SKILL-SHARED-LOCALE-DETECT-V1" in sids


def test_candidate_skills_shared_locale_is_returned_for_known_agent() -> None:
    """Same skill should also surface for a known agent because 'shared' is a
    pseudo-agent that satisfies the agents_supported gate."""
    sids = candidate_skill_ids("hlk_lookup", agent="madeira")
    assert "SKILL-SHARED-LOCALE-DETECT-V1" in sids


def test_candidate_skills_madeira_routing_condition_filters_other_routes() -> None:
    """MADEIRA-LOOKUP has routing_condition=intent_in=hlk_lookup;hlk_search.
    Should NOT appear for finance_research."""
    sids = candidate_skill_ids("finance_research", agent="madeira")
    assert "SKILL-MADEIRA-LOOKUP-V1" not in sids


# ── intent.classify_request integration ───────────────────────────────────────


def test_intent_classify_request_emits_candidate_skills_field() -> None:
    from akos.intent import classify_request

    r = classify_request("Find the System Owner role", agent="madeira")
    assert "candidate_skills" in r
    assert isinstance(r["candidate_skills"], list)
    assert "SKILL-MADEIRA-LOOKUP-V1" in r["candidate_skills"]


def test_intent_classify_request_candidate_skills_is_empty_list_for_unknown_route() -> None:
    """Even for off-axis routes, candidate_skills is a list (never None)."""
    from akos.intent import classify_request

    r = classify_request("hello world", agent=None)
    assert isinstance(r["candidate_skills"], list)


def test_intent_classify_request_works_without_agent() -> None:
    from akos.intent import classify_request

    r = classify_request("Find the System Owner role")
    assert "route" in r
    assert "candidate_skills" in r


def test_intent_classify_request_back_compat_no_candidate_skills_breakage(monkeypatch) -> None:
    """If skill_router fails to import for any reason, classify_request still
    returns a valid response (route + escalation info), with candidate_skills=[]."""
    import sys
    from akos import intent as intent_mod

    real_import = __builtins__["__import__"] if isinstance(__builtins__, dict) else __builtins__.__import__

    def boom_import(name, *args, **kwargs):
        if name == "akos.skill_router":
            raise ImportError("simulated missing dependency")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", boom_import)

    r = intent_mod.classify_request("Find the System Owner role")
    assert "route" in r
    assert r["candidate_skills"] == []


# ── Drift detector (catches if someone reverts the column) ────────────────────


def test_skill_registry_csv_has_routing_condition_column() -> None:
    csv_path = (
        Path(__file__).resolve().parent.parent
        / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SKILL_REGISTRY.csv"
    )
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert "routing_condition" in (reader.fieldnames or [])
        assert "tools_required_waived" in (reader.fieldnames or [])


def test_madeira_lookup_has_intent_in_routing_condition() -> None:
    """The cursor plan default for MADEIRA: intent_in=hlk_lookup;hlk_search.
    If someone empties this, P5 promotion gate (P7) would un-anchor the routing demo."""
    skills = load_skills()
    madeira = next(s for s in skills if s["skill_id"] == "SKILL-MADEIRA-LOOKUP-V1")
    rc = madeira.get("routing_condition", "")
    assert rc == "intent_in=hlk_lookup;hlk_search", f"unexpected MADEIRA routing_condition: {rc!r}"
