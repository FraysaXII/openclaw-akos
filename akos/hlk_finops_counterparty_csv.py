"""Field contract for FINOPS_COUNTERPARTY_REGISTER.csv (Initiative 18).

Canonical CSV lives under docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops/
(moved from compliance/canonicals/ to compliance/canonicals/finops/ per I81 P2 T1 / D-IH-81-Q
under D-IH-81-G umbrella, 2026-05-23, per Initiative 22 forward layout convention).
Mirrored to compliance.finops_counterparty_register_mirror on Supabase.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv header row.
FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "counterparty_id",
    "counterparty_type",
    "display_name",
    "service_category",
    "billing_model",
    "commercial_segment",
    "revenue_model",
    "role_owner",
    "process_item_id",
    "repo_slug",
    "component_id",
    "contract_doc_pointer",
    "renewal_review_due",
    "status",
    "pci_phi_pii_scope",
    "confidence_level",
    "notes",    "last_review_at",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 follow-up (D-IH-71-R) review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)

)
