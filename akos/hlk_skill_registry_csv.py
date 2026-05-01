"""Field contract for SKILL_REGISTRY.csv (Initiative 32 P2; extended I45 P3).

Canonical CSV lives under ``docs/references/hlk/compliance/dimensions/``.
Mirrored to ``compliance.skill_registry_mirror`` on Supabase.

Skill = a versioned bundle of (intent, axes_to_resolve, tools_called,
output_contract) that one or more agents can invoke. Closes the gap that today
"skill-shaped artifacts" live in 4 unaligned places (``prompts/base/``,
``.cursor/skills/``, ``config/workspace-scaffold/<agent>/IDENTITY.md``,
``config/agent-capabilities.json``) with no SSOT for multiagentic decomposition.

Tenant-aware schema from day 1 per D-IH-32-J: ``tenant_scope`` accepts only
``shared`` until a future MADEIRA-SaaS initiative opens tenant scopes via
Initiative 34. Validator enforces the regex ``^shared$``.

Lazy-load pattern per D-IH-32-I: each agent prompt carries 1-2 line skill
descriptions; the full skill body loads only when the skill is invoked. The
``description`` field on this CSV is the cheap-load summary; the canonical
skill body lives in the ``intro_artifact_path``-equivalent surface (each agent's
``IDENTITY.md`` + a future ``SKILL_<id>.md`` body file).

I45 P3 additions:
- ``routing_condition`` — kv-style filter expression evaluated by ``akos.skill_router``
  to constrain candidate skills per intent. Empty = always-eligible (back-compat).
  Supported keys: ``intent_in=<route1;route2>``, ``intent=<route>``, ``agent=<id>``.
- ``tools_required_waived`` — boolean (``true``/``false``/empty=false). When true,
  the validator does NOT warn about tools_required entries missing from
  agent-capabilities.json. Used during the I45 P3 reconciliation period (R-45-6).
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/dimensions/SKILL_REGISTRY.csv header row.
SKILL_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "skill_id",                # ^SKILL-[A-Z0-9-]{4,80}-V\d+$
    "name",                    # human-readable name
    "agents_supported",        # semicolon-list FK to agent ids in config/workspace-scaffold/
    "axes_consumed",           # semicolon-list of {persona; channel; distance; language; artifact_class; topic}
    "tools_required",          # semicolon-list FK to config/agent-capabilities.json tool ids
    "version",                 # semver-like, e.g., 1.0.0
    "owner_role",              # FK to baseline_organisation.csv role_name
    "eval_baseline_pct",       # float in [0.0, 100.0]; baseline accuracy on the eval harness
    "langfuse_trace_pattern",  # string pattern for Langfuse trace filtering
    "tenant_scope",            # ^shared$ (D-IH-32-J: only 'shared' until Initiative 34)
    "lifecycle_status",        # active | deprecated | scaffold
    "topic_ids",               # semicolon-list FK to TOPIC_REGISTRY.csv (axis 6, populated in P5)
    "routing_condition",       # I45 P3: empty | intent_in=<r1;r2> | intent=<r> | agent=<id>
    "tools_required_waived",   # I45 P3: empty/false | true (waives tools_required FK warning)
    "description",             # short cheap-load summary (1-2 sentences; lazy-load contract)
    "notes",
)

VALID_AXES: frozenset[str] = frozenset({
    "persona", "channel", "distance", "language", "artifact_class", "topic",
})

VALID_LIFECYCLE_STATUSES: frozenset[str] = frozenset({
    "active", "deprecated", "scaffold",
})

# Known agent ids — derived from config/workspace-scaffold/<agent>/IDENTITY.md.
# Updated when a new agent ships.
KNOWN_AGENT_IDS: frozenset[str] = frozenset({
    "madeira", "orchestrator", "architect", "executor", "verifier",
})

# `shared` is a special pseudo-agent denoting cross-agent utility skills.
SHARED_AGENT_ID: str = "shared"
