"""Method registry for SOP-DATA_PRODUCTION_READINESS_001 (I93 P5c).

Mirrors method library table in the SOP body; drift-detected by tests.
"""

from __future__ import annotations

from typing import Literal, TypedDict


class ProductionReadinessMethod(TypedDict):
    method_id: str
    label: str
    executor_class: Literal["human", "aic", "hybrid"]
    when: str
    paired_upstream_sop: str


PRODUCTION_READINESS_METHODS: dict[str, ProductionReadinessMethod] = {
    "PROD-METHOD-INTERNAL": {
        "method_id": "PROD-METHOD-INTERNAL",
        "label": "Holistika-owned stack hardening",
        "executor_class": "human",
        "when": "Analytics Buckets, Metabase, ERP panels, Langfuse production promotion",
        "paired_upstream_sop": "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_BI_GOVERNANCE.md",
    },
    "PROD-METHOD-CLIENT-MS": {
        "method_id": "PROD-METHOD-CLIENT-MS",
        "label": "Microsoft stack production path",
        "executor_class": "hybrid",
        "when": "Power Platform + Power BI after demo factory Phase 1 evidence exists",
        "paired_upstream_sop": "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/SOP-DATA_MS_DEMO_FACTORY_001.md",
    },
    "PROD-METHOD-HYBRID": {
        "method_id": "PROD-METHOD-HYBRID",
        "label": "Stream C bridge hardening",
        "executor_class": "human",
        "when": "FDW finops, export views, Make/n8n bridges to client BI",
        "paired_upstream_sop": "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md",
    },
}
