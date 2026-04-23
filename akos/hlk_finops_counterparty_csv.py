"""Field contract for FINOPS_COUNTERPARTY_REGISTER.csv (Initiative 18).

Canonical CSV lives under docs/references/hlk/compliance/.
Mirrored to compliance.finops_counterparty_register_mirror on Supabase.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/FINOPS_COUNTERPARTY_REGISTER.csv header row.
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
    "notes",
)
