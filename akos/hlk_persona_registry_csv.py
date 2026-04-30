"""Field contract for PERSONA_REGISTRY.csv (Initiative 31 P2.1).

Canonical CSV lives under ``docs/references/hlk/compliance/dimensions/``.
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

# Keep in sync with docs/references/hlk/compliance/dimensions/PERSONA_REGISTRY.csv header row.
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
    "notes",
)
