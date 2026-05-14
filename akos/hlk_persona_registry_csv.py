"""Field contract for PERSONA_REGISTRY.csv (Initiative 31 P2.1).

Canonical CSV lives under ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``.
Mirrored to ``compliance.persona_registry_mirror`` on Supabase.

Persona = archetype (the **shape** of who's interacting) — distinct from
GOI/POI which tracks named individuals (the **identity**). The persona
registry is operations-side: routing rules, qualifying gates, intro
artifacts. The GOI/POI register is identity-side: actual people, current
distance, voice profile.

Operating rule: every inbound human gets bucketed into exactly one persona
at first-touch; the persona then drives template selection in the
touchpoint kit (per :doc:`HOLISTIK_OPS_DISCOVERY.md` 5-axis system).
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_REGISTRY.csv header row.
PERSONA_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "persona_id",
    "name",
    "direction",
    "intent_summary",
    "value_band",
    "typical_languages",
    "typical_channels",
    "typical_distance_band",
    "qualification_gate",
    "intro_artifact_path",
    "handoff_role",
    "linked_topic_ids",
    "notes",    "last_review_at",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 follow-up (D-IH-71-R) review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)

)
