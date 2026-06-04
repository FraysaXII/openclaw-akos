"""Method registry for SOP-DATA_MS_DEMO_FACTORY_001 (I93 P5c).

Mirrors method library table in the SOP body; drift-detected by tests.
"""

from __future__ import annotations

from typing import Literal, TypedDict


class MsDemoMethod(TypedDict):
    method_id: str
    label: str
    executor_class: Literal["human", "aic", "hybrid"]
    runbook_path: str
    when: str


MS_DEMO_METHODS: dict[str, MsDemoMethod] = {
    "MS-DEMO-METHOD-A": {
        "method_id": "MS-DEMO-METHOD-A",
        "label": "Azure CLI + Power Platform CLI (pac)",
        "executor_class": "hybrid",
        "runbook_path": "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/runbooks/ms-demo-cli-method-a.md",
        "when": "Deterministic export/import; CI-friendly; licensing already provisioned",
    },
    "MS-DEMO-METHOD-B": {
        "method_id": "MS-DEMO-METHOD-B",
        "label": "Power Platform portal + Composio Browser Tool",
        "executor_class": "hybrid",
        "runbook_path": "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/runbooks/ms-demo-browser-method-b.md",
        "when": "UI-only licensing; screenshot capture for customer-pack PDF",
    },
}
