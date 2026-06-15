#!/usr/bin/env python3
"""One-off: full CAPABILITY_REGISTRY substrate backfill (D-IH-76-R / operator full_103 ratify)."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAP_PATH = ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/CAPABILITY_REGISTRY.csv"
)
DECISION_PATH = ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv"
)

DECISION_ID = "D-IH-76-R"
REVIEW_DATE = "2026-06-16"

L1_DEFAULT: dict[str, str] = {
    "Applied AI & MADEIRA": "SUBS-HOLISTIKA-OPENCLAW",
    "Corporate Intelligence & Research": "SUBS-HOLISTIKA-OPENCLAW",
    "Data Governance & Enterprise Knowledge": "SUBS-HOLISTIKA-KIRBE",
    "People, Org Design & Quality Fabric": "SUBS-ANYSPHERE-CURSOR-SDK",
    "Product & Platform Engineering": "SUBS-HOLISTIKA-OPENCLAW",
    "Go-to-Market & Brand": "SUBS-VERCEL-VERCEL-AI-SDK",
    "Finance & Revenue Operations": "SUBS-HOLISTIKA-OPENCLAW",
    "Legal, Compliance & Privacy": "SUBS-ANYSPHERE-CURSOR-SDK",
    "Delivery & Client Engagement Operations": "SUBS-ANYSPHERE-CURSOR-SDK",
}

ID_OVERRIDES: dict[str, str] = {
    "CAP-DATA-PLATFORM-PRODUCTS": "SUBS-HOLISTIKA-KIRBE",
    "CAP-DATA-PIPELINE-QUALITY-LINEAGE": "SUBS-HOLISTIKA-LLAMAINDEX-WORKER",
    "CAP-DATA-MODELING-ENGINEERING": "SUBS-HOLISTIKA-LLAMAINDEX-WORKER",
    "CAP-DATAOPS-QUALITY-ASSURANCE": "SUBS-HOLISTIKA-LLAMAINDEX-WORKER",
    "CAP-OPS-KNOWLEDGE-MGMT-SYSTEM": "SUBS-HOLISTIKA-KIRBE",
    "CAP-KNOWLEDGE-REGISTER-STEWARDSHIP": "SUBS-HOLISTIKA-KIRBE",
    "CAP-KNOWLEDGE-VAULT-GOVERNANCE": "SUBS-HOLISTIKA-KIRBE",
    "CAP-RES-KB-PIPELINE-RADAR": "SUBS-HOLISTIKA-KIRBE",
    "CAP-RES-OSINT": "SUBS-HOLISTIKA-KIRBE",
    "CAP-RES-SECONDARY-SYNTHESIS": "SUBS-HOLISTIKA-KIRBE",
    "CAP-DATABASE-GRAPH-MGMT": "SUBS-HOLISTIKA-KIRBE",
    "CAP-CLIENT-AI-DATAOPS-DELIVERY": "SUBS-HOLISTIKA-KIRBE",
    "CAP-WEB-APP-EXPERIENCE-ENG": "SUBS-VERCEL-VERCEL-AI-SDK",
    "CAP-ECOMMERCE-PLATFORM-INTEGRATION": "SUBS-VERCEL-VERCEL-AI-SDK",
    "CAP-ENVOY-TECHLAB-SHOWCASE": "SUBS-VERCEL-VERCEL-AI-SDK",
    "CAP-OPS-ERP-DATA-PLATFORM-BUILD": "SUBS-VERCEL-VERCEL-AI-SDK",
    "CAP-MKT-CREATIVE-WEB": "SUBS-VERCEL-VERCEL-AI-SDK",
    "CAP-LAB-PLATFORM-BINDING-GOVERNANCE": "SUBS-PATTERN-MADEIRA-DIRECT-OWN-RUNTIME",
    "CAP-LAB-COMPONENT-ECOSYSTEM-GOVERNANCE": "SUBS-PATTERN-MADEIRA-DIRECT-OWN-RUNTIME",
    "CAP-MULTIPLATFORM-DEPLOYMENT": "SUBS-VERCEL-VERCEL-AI-SDK",
    "CAP-MADEIRA-RESEARCH-CENTER-SURFACE": "SUBS-HOLISTIKA-LLAMAINDEX-WORKER",
    "CAP-MADEIRA-CONTEXT-ECONOMICS": "SUBS-HOLISTIKA-OPENCLAW",
}


def resolve_substrate(row: dict) -> str:
    cid = row["capability_id"]
    if (row.get("substrate_id") or "").strip():
        return row["substrate_id"].strip()
    if cid in ID_OVERRIDES:
        return ID_OVERRIDES[cid]
    l1 = (row.get("l1_domain") or "").strip()
    return L1_DEFAULT.get(l1, "SUBS-HOLISTIKA-OPENCLAW")


def main() -> None:
    with CAP_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    filled = 0
    for row in rows:
        if (row.get("substrate_id") or "").strip():
            continue
        row["substrate_id"] = resolve_substrate(row)
        row["last_review_at"] = REVIEW_DATE
        row["last_review_by"] = "Data Governance Office"
        row["last_review_decision_id"] = DECISION_ID
        row["methodology_version_at_review"] = "v3.2"
        filled += 1

    with CAP_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    decision_row = (
        f"{DECISION_ID},MADEIRA v3.2 full capability substrate backfill (103 rows),"
        f"INIT-OPENCLAW_AKOS-76,,,,,governance,active,low,{REVIEW_DATE},"
        f"docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/"
        f"reports/capability-registry-gap-analysis-post-full-substrate-2026-06-16.md,,"
        f"Operator ratifies full 103-row substrate_id backfill + validator FAIL on any empty FK "
        f"(AskQuestion full_103 2026-06-15).,{filled} rows backfilled via L1-domain defaults + "
        f"semantic overrides.,{REVIEW_DATE},Operator,{DECISION_ID},v3.2\n"
    )
    text = DECISION_PATH.read_text(encoding="utf-8")
    if DECISION_ID not in text:
        DECISION_PATH.write_text(text.rstrip("\n") + "\n" + decision_row, encoding="utf-8")

    print(f"apply_capability_substrate_full_sweep: filled {filled} rows -> 103/103 substrate_id")


if __name__ == "__main__":
    main()
