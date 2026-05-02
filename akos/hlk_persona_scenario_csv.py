"""Field contract for PERSONA_SCENARIO_REGISTRY.csv (Initiative 47 P1).

Canonical CSV lives under ``docs/references/hlk/compliance/dimensions/``.
Mirrored to ``compliance.persona_scenario_registry_mirror`` on Supabase.

The persona-driven UAT scenario library. Joins:
- PERSONA_REGISTRY.csv (16 archetypes; I31 P2)
- SKILL_REGISTRY.csv (5 skills; I32 P2 + I45 P3 + I46 P5)
- TOPIC_REGISTRY.csv (axis 6; I25)

Per the I47 scenario taxonomy (`docs/wip/planning/47-user-centric-uat/scenario-taxonomy.md`):
5 typed dimensions per scenario:
- ``persona_id`` (FK PERSONA_REGISTRY): who is asking
- ``skill_id`` (FK SKILL_REGISTRY): what capability is exercised
- ``scenario_class`` (enum): kind of scenario (lookup / multihop / adversarial / recovery / benchmark / cross_axis / cannot_answer)
- ``difficulty_class`` (enum): trivial / moderate / hard / impossible (auto-classified by P10 calibration)
- ``expected_outcome_class`` (enum): PASS / GROUND / ESCALATE / REFUSE

Plus tenant-aware schema from day 1 per D-IH-47-K: ``tenant_id`` accepts
NULL (default; "shared scenario applies to all tenants") OR a tenant string
(future I34 multi-tenant; cross-tenant fan-out at runtime).
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv header row.
PERSONA_SCENARIO_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "scenario_id",              # ^SCN-[A-Z0-9-]{4,80}-V\d+$
    "persona_id",               # FK to PERSONA_REGISTRY.csv (or 'OPERATOR' for operator-shaped scenarios)
    "skill_id",                 # FK to SKILL_REGISTRY.csv
    "tenant_id",                # I47 P1 D-IH-47-K: empty/NULL default = shared; future = tenant string
    "tier",                     # 1 | 2 | 3 (per D-IH-47-B coverage tiers)
    "scenario_class",           # lookup | multihop | adversarial | recovery | benchmark | cross_axis | cannot_answer
    "difficulty_class",         # trivial | moderate | hard | impossible (auto-classified by P10 calibration)
    "prompt_text",              # the actual input text MADEIRA receives
    "expected_route",           # FK to akos.intent IntentRoute literal (admin_escalate, hlk_lookup, etc.)
    "expected_keywords",        # semicolon-list of substrings the response should contain
    "forbidden_keywords",       # semicolon-list of substrings the response must NOT contain
    "expected_outcome_class",   # PASS | GROUND | ESCALATE | REFUSE
    "language",                 # en | es | fr (per SOP-HLK_LOCALISATION_001.md)
    "topic_ids",                # semicolon-list FK to TOPIC_REGISTRY.csv
    "lifecycle_status",         # active | deprecated | scaffold
    "notes",
)

VALID_SCENARIO_CLASSES: frozenset[str] = frozenset({
    "lookup",
    "multihop",
    "adversarial",
    "recovery",
    "benchmark",
    "cross_axis",
    "cannot_answer",
})

VALID_DIFFICULTY_CLASSES: frozenset[str] = frozenset({
    "trivial",
    "moderate",
    "hard",
    "impossible",
})

VALID_EXPECTED_OUTCOME_CLASSES: frozenset[str] = frozenset({
    "PASS",
    "GROUND",
    "ESCALATE",
    "REFUSE",
})

VALID_TIERS: frozenset[str] = frozenset({"1", "2", "3"})

VALID_LANGUAGES: frozenset[str] = frozenset({"en", "es", "fr"})

VALID_LIFECYCLE_STATUSES: frozenset[str] = frozenset({
    "active", "deprecated", "scaffold",
})

# 'OPERATOR' is a special pseudo-persona for the founder/system-owner
# scenarios; not a row in PERSONA_REGISTRY.csv but accepted by the validator.
OPERATOR_PSEUDO_PERSONA: str = "OPERATOR"

# Valid akos.intent IntentRoute literals (kept in sync with akos/intent.py).
VALID_EXPECTED_ROUTES: frozenset[str] = frozenset({
    "admin_escalate",
    "execution_escalate",
    "finance_research",
    "hlk_search",
    "hlk_lookup",
    "gtm_project",
    "other",
})
