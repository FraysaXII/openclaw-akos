"""Field contract for CHANNEL_TOUCHPOINT_REGISTRY.csv (Initiative 31 P3).

Canonical CSV lives under ``docs/references/hlk/compliance/dimensions/``.
Mirrored to ``compliance.channel_touchpoint_registry_mirror`` on Supabase.

A channel touchpoint is **where humans physically reach Holistika** (LinkedIn
DM, email, web form, Cal scheduling, paid ad, partner referral, event). This
is operationally distinct from ``CHANNEL_STRATEGY.md`` in
``business-strategy/`` — that file lists *acquisition channel hypotheses*
(founder-led outbound, partner B2B Websitz pattern, etc.). Touchpoint
registry is what shows up at our front door; CHANNEL_STRATEGY is where we
choose to walk to find customers. They cross-reference: each acquisition
channel maps to one or more touchpoint channels.

Operating rule: every inbound human gets bucketed into exactly one
touchpoint at first-contact; the touchpoint then drives the persona match
and the SLA per :doc:`HOLISTIK_OPS_DISCOVERY.md` 5-axis system.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv header row.
CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "channel_id",
    "name",
    "direction",
    "supported_languages",
    "typical_personas",
    "typical_distance_band_inbound",
    "triage_rule",
    "response_sla_band",
    "response_owner_role",
    "linked_topic_ids",
    "notes",
)
