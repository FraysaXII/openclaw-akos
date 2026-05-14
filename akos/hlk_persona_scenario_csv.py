"""Field contract for PERSONA_SCENARIO_REGISTRY.csv (Initiative 47 P1).

Canonical CSV lives under ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``.
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

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv header row.
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
    "lifecycle_status",         # active | deprecated | scaffold (+ quarantined I49 P10)
    "priority_score",           # I49 — non-negative float; empty allowed until calibrated
    "safety_lane",              # I49 — true|false|empty (pinned for backlog sort)
    "release_blocking",         # I49 — true|false|empty (active rows that gate releases)
    "target_difficulty_band",   # I51 P3 D-IH-51-A — per-persona "<t>/<m>/<h>/<i>" pp summing to 100; empty = global D-IH-47-C 40/40/10/10 fallthrough
    "notes",
    "last_review_at",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 follow-up (D-IH-71-R) review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)
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
    "active", "deprecated", "scaffold", "quarantined",
})

# 'OPERATOR' is a special pseudo-persona for the founder/system-owner
# scenarios; not a row in PERSONA_REGISTRY.csv but accepted by the validator.
OPERATOR_PSEUDO_PERSONA: str = "OPERATOR"

# I51 P3 D-IH-51-A: target_difficulty_band format helpers.
# Empty string = "fall through to global D-IH-47-C 40/40/10/10".
# Otherwise: 4 integer pp values (trivial/moderate/hard/impossible) summing to exactly 100.
TARGET_DIFFICULTY_BAND_KEYS: tuple[str, ...] = ("trivial", "moderate", "hard", "impossible")
TARGET_DIFFICULTY_BAND_TOTAL_PP: int = 100


def parse_target_difficulty_band(raw: str) -> dict[str, float] | None:
    """Parse a `target_difficulty_band` cell into a dict; empty -> None.

    Returns None for empty/blank input (caller should fall through to the
    global D-IH-47-C target). Raises ValueError on malformed input.
    """
    s = (raw or "").strip()
    if not s:
        return None
    parts = [p.strip() for p in s.split("/")]
    if len(parts) != len(TARGET_DIFFICULTY_BAND_KEYS):
        raise ValueError(
            f"target_difficulty_band {raw!r}: expected 4 slash-separated values "
            f"(trivial/moderate/hard/impossible), got {len(parts)}"
        )
    out: dict[str, float] = {}
    for k, v in zip(TARGET_DIFFICULTY_BAND_KEYS, parts):
        try:
            iv = int(v)
        except ValueError as exc:
            raise ValueError(f"target_difficulty_band {raw!r}: {k} {v!r} not an integer") from exc
        if iv < 0 or iv > 100:
            raise ValueError(f"target_difficulty_band {raw!r}: {k}={iv} outside [0, 100]")
        out[k] = float(iv)
    total = int(sum(out.values()))
    if total != TARGET_DIFFICULTY_BAND_TOTAL_PP:
        raise ValueError(
            f"target_difficulty_band {raw!r}: sum {total} != {TARGET_DIFFICULTY_BAND_TOTAL_PP}"
        )
    return out


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
