"""Field contract for GOI_POI_REGISTER.csv (Initiative 21; relocated I32 P7).

Canonical CSV lives under ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/`` (per
D-IH-32-D, relocated from ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`` in Initiative 32
P7 to align with the I22 forward-layout convention; all other dimension CSVs
already live in ``dimensions/``).

Mirrored to ``compliance.goipoi_register_mirror`` on Supabase.

GOI = Group of Interest (organisation / entity).
POI = Person of Interest (role-as-position; a real human reference).

Operating rule: documents reference ``ref_id`` only. Real human and private
organisation names are kept off-repo. Public entities (``is_public_entity = true``)
may use a real name as ``display_name``; private entities must use an obfuscated
display label safe for public repository visibility.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv header row.
#
# Initiative 24 P2 (D-IH-11) added three optional voice-profile columns at the
# end (`voice_register`, `language_preference`, `pronoun_register`) so the
# composer (`scripts/compose_adviser_message.py`) can read recipient eloquence
# defaults directly from the GOI/POI dimension. Columns are nullable; default
# falls back through discipline default → brand foundation default → global
# default per `SOP-HLK_COMMUNICATION_METHODOLOGY_001.md` Layer 4 precedence.
GOIPOI_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "ref_id",
    "entity_kind",
    "class",
    "is_public_entity",
    "display_name",
    "lens",
    "sensitivity",
    "program_id",
    "role_owner",
    "process_item_id",
    "primary_link",
    "notes",
    "voice_register",
    "language_preference",
    "pronoun_register",
    # Initiative 31 P2.2 (D-IH-31-G) — distance dimension on the social graph.
    # `distance_band`: ordinal N1|N2|N3|N4 (terminal at N4; N5+ collapses to N4).
    # `bridge_via`: FK to another POI/GOI ref_id (the immediate intermediary on the path).
    #   Null only when distance_band == "N1"; required for N2-N4.
    # `distance_assessed_date`: ISO date when the distance was last validated.
    #   Drives the quarterly re-assessment cadence per SOP-HLK_GOIPOI §4.X.
    "distance_band",
    "bridge_via",
    "distance_assessed_date",
    # P13.4 (D-W13-D) — related-party disclosure for engagements with family
    # members, board members, advisors-with-equity, or other rows where SOC
    # disclosure norms require an explicit flag. Enum: "true" | "false" | "".
    # Empty default is backwards-compatible for every Initiative 21 row.
    "related_party",
    # I70 P8.5 (D-IH-70-AD) — stance dimension on the social graph encoding the
    # operator's v2.7 ally/neutral/enemy intelligence-ops doctrine
    # (canonical: docs/references/hlk/v3.0/Research/Intelligence/canonicals/
    # GOI_POI_STANCE_DOCTRINE.md). Independent of distance_band; powers
    # engagement-posture rules (free for allies, market for neutrals, never-
    # accept-payment for enemies). Enum: "ally" | "neutral" | "enemy" |
    # "unknown" | "". Empty default is backwards-compatible for every
    # Initiative 21 / 22 / 24 / 31 / P13.4 row.
    "stance",
)
