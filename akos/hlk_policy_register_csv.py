"""Field contract for POLICY_REGISTER.csv (Initiative 32 P4).

Canonical CSV lives under ``docs/references/hlk/compliance/dimensions/``.
Mirrored to ``compliance.policy_register_mirror`` on Supabase.

Promotes RLS rules, ``service_role`` rotation cadences, redaction policies, and
PII-scope policies from SOP prose to a queryable CSV. Closes the audit gap
that today these rules live as paragraphs in 5+ different SOPs (GOI/POI
maintenance, BRAND_JARGON_AUDIT, KiRBe sync contract, KM Topic-Fact-Source,
adviser engagement) and cannot be queried as a coherent set.

After P4 ships, every RLS rule in ``supabase/migrations/`` resolves to one
``policy_register`` row, and every SOP that names an RLS rule cites the row's
``policy_id`` (linkage test in P14 governance moat metrics).
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv header row.
POLICY_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "policy_id",            # ^POL-[A-Z0-9-]{4,80}$
    "policy_class",         # rls | service_role_rotation | redaction | pii_scope
    "applies_to_schema",    # e.g., 'compliance', 'finops', 'holistika_ops', '*' for cross-schema
    "applies_to_table",     # e.g., 'goipoi_register_mirror', '*' for whole schema
    "policy_text",          # the actual rule (1-3 sentences; cite SOP if longer)
    "cadence",              # quarterly | annual | on_change | never | continuous
    "owner_role",           # FK to baseline_organisation.csv role_name
    "last_review",          # YYYY-MM-DD
    "next_review",          # YYYY-MM-DD
    "topic_ids",            # semicolon-list FK to TOPIC_REGISTRY.csv
    "notes",
)

VALID_POLICY_CLASSES: frozenset[str] = frozenset({
    "rls", "service_role_rotation", "redaction", "pii_scope",
    # I45 P4: per-skill cost ceiling. policy_text encodes the threshold
    # (e.g., "max_usd_per_run=0.005"); enforced by scripts/eval.py --enforce.
    "cost_ceiling",
    # I45 P5: brand jargon / PII / prompt injection canary floors.
    "adversarial_floor",
    # I45 P7: skill graduation gate.
    "promotion_gate",
    # I46 P5 (conditional ship): which skills/topic_classes are eligible
    # for GraphRAG-hybrid retrieval.
    "graph_rag_eligibility",
    # I47 P12 (D-IH-47-J): LLM-as-judge per-axis pass threshold.
    # policy_text encodes the threshold (e.g., "min_pass_score=4");
    # enforced by akos.eval_harness.judge.load_judge_thresholds().
    "judge_threshold",
})

VALID_CADENCES: frozenset[str] = frozenset({
    "quarterly", "annual", "on_change", "never", "continuous",
})
