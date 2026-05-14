"""Field contract for DECISION_REGISTER.csv (Initiative 59 P1.5; **D-IH-59-E**).

Canonical CSV lives under ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv``.
Mirrored to ``compliance.decision_register_mirror`` on Supabase.

Folded into I59 (vs I60 deferral) so ``INITIATIVE_REGISTRY.inception_decision_id``
and ``closure_decision_id`` can be **real FKs** (not strings ALTER TABLE'd later).

Per-initiative ``decision-log.md`` files stay **canonical** for prose (full
alternatives + rationale + reversibility narrative). This CSV is **canonical**
for governed metadata (queryable index; cross-references become real FKs).

Sync between decision-log.md headers (``## D-IH-XX-Y — title``) and CSV is
checked by ``scripts/validate_decision_register_decision_log_md_sync.py``
(advisory; warns when MD has decisions not in CSV — the audit is best-effort
and idempotent).

PRIMARY KEY format: ``D-IH-{NN}-{LETTER}`` (e.g. ``D-IH-58-A``) or
``D-IH-{NN}-DECISION-P{n}-{TAG}-{YYYY-MM-DD}`` for special closure decisions
(e.g. ``D-IH-46-Decision-P3-NO-SHIP-2026-05-03``). Validator regex covers both.

FK targets:

- ``initiating_initiative_id`` → INITIATIVE_REGISTRY.initiative_id.
- ``linked_initiative_ids`` → semicolon-list FK to INITIATIVE_REGISTRY (other
  initiatives this decision references; nullable).
- ``linked_ops_action_ids`` → semicolon-list FK to OPS_REGISTER (nullable).
- ``linked_policies`` → semicolon-list FK to POLICY_REGISTER.policy_id (nullable).
- ``linked_topic_ids`` → semicolon-list FK to TOPIC_REGISTRY (nullable).
- ``decision_log_path`` → relative path to the canonical decision-log.md
  containing the full prose entry.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv header row.
DECISION_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "decision_id",                # PRIMARY KEY
    "title",                      # human-readable
    "initiating_initiative_id",   # FK to INITIATIVE_REGISTRY.initiative_id
    "linked_initiative_ids",      # semicolon-list FK to INITIATIVE_REGISTRY (nullable)
    "linked_ops_action_ids",      # semicolon-list FK to OPS_REGISTER (nullable)
    "linked_policies",            # semicolon-list FK to POLICY_REGISTER (nullable)
    "linked_topic_ids",           # semicolon-list FK to TOPIC_REGISTRY (nullable)
    "decision_class",             # architecture | governance | scope | execution | closure
    "status",                     # active | superseded | retired
    "reversibility",              # high | medium | low
    "decided_at",                 # YYYY-MM-DD
    "decision_log_path",           # relative path to source decision-log.md
    "supersedes_decision_id",     # FK to DECISION_REGISTER (nullable)
    "summary",                    # 1-2 sentence outcome (NOT the full rationale)
    "notes",
    "last_review_at",                  # I71 P4 review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)
)

VALID_DECISION_CLASSES: frozenset[str] = frozenset({
    "architecture", "governance", "scope", "execution", "closure",
})

VALID_DECISION_STATUSES: frozenset[str] = frozenset({
    "active", "superseded", "retired",
})

VALID_REVERSIBILITY: frozenset[str] = frozenset({
    "high", "medium", "low",
})
