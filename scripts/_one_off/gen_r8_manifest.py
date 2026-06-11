#!/usr/bin/env python3
"""One-off generator for Automation OS R8 manifest (Finance + Legal audit bar)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/tranches/r8-manifest.json"
)
GITHUB_MAIN = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def ledger_url(path: str) -> str:
    """Repo-relative docs/ paths pass through; other paths use GitHub blob URLs."""
    if path.startswith("docs/"):
        return path
    return GITHUB_MAIN + path.replace(chr(92), "/")


# Priority-ordered CORP-VAULT-FIN + CORP-VAULT-LEGAL.
CORPINT_PATHS: list[tuple[str, str, str]] = [
    ("Finance area README", "docs/references/hlk/v3.0/Admin/O5-1/Finance/README.md", "P7-FINANCE"),
    ("Finance area charter", "docs/references/hlk/v3.0/Admin/O5-1/Finance/canonicals/FINANCE_AREA_CHARTER.md", "P7-FINANCE"),
    ("FINOPS discipline", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/FINOPS_DISCIPLINE.md", "P7-FINANCE"),
    ("FINOPS revenue recognition policy", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/FINOPS_REVENUE_RECOGNITION_POLICY.md", "P7-FINANCE"),
    ("SOP FINOPS counterparty register maintenance", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md", "P7-FINANCE"),
    ("SOP FINOPS vendor register maintenance", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/SOP-HLK_FINOPS_VENDOR_REGISTER_MAINTENANCE_001.md", "P7-FINANCE"),
    ("SOP founder company funding", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/SOP-FOUNDER_COMPANY_FUNDING_001.md", "P7-FINANCE"),
    ("Founder capitalization decision note", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md", "P7-FINANCE"),
    ("Pricing tier registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/dimensions/PRICING_TIER_REGISTRY.csv", "P7-FINANCE"),
    ("FINOPS tax calendar CSV", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/dimensions/FINOPS_TAX_CALENDAR.csv", "P7-FINANCE"),
    ("FINOPS performance obligation registry", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/dimensions/FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv", "P7-FINANCE"),
    ("FINOPS counterparty register CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv", "P7-FINANCE"),
    ("SOP trademark naming governance", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/SOP-TRADEMARK_NAMING_GOVERNANCE_001.md", "P8-LEGAL"),
    ("Brand hierarchy and trademark scope", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md", "P8-LEGAL"),
    ("SOP legal IP register maintenance", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/SOP-LEGAL_IP_REGISTER_MAINTENANCE_001.md", "P8-LEGAL"),
    ("SOP legal trademark monitoring", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/SOP-LEGAL_TRADEMARK_MONITORING_001.md", "P8-LEGAL"),
    ("Founder filed instrument register", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/FOUNDER_FILED_INSTRUMENT_REGISTER.md", "P8-LEGAL"),
    ("Trademark filing strategy", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/TRADEMARK_FILING_STRATEGY_2026-05.md", "P8-LEGAL"),
    ("External counsel handoff package", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md", "P8-LEGAL"),
    ("Filed instruments CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/advops/FILED_INSTRUMENTS.csv", "P8-LEGAL"),
    ("SOP founder entity formation", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/SOP-FOUNDER_ENTITY_FORMATION_001.md", "P8-LEGAL"),
    ("Founder entity formation decision memo", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md", "P8-LEGAL"),
    ("Founder incorporation knowledge index", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md", "P8-LEGAL"),
    ("validate_finops_ledger runbook", "scripts/validate_finops_ledger.py", "P7-FINANCE"),
    ("finops_monthly_recon runbook", "scripts/finops_monthly_recon.py", "P7-FINANCE"),
    ("validate_filed_instruments runbook", "scripts/validate_filed_instruments.py", "P8-LEGAL"),
    ("Finance ops cursor rule", ".cursor/rules/akos-finance-ops.mdc", "P7-FINANCE"),
    ("akos finance module", "akos/finance.py", "P7-FINANCE"),
]

# OSINT-FINOPS-AUTO + OSINT-REG-AUDIT â€” FinOps automation + legal audit bar.
OSINT_SOURCES: list[tuple[str, str, str, str, str, bool]] = [
    ("Stripe billing docs", "https://docs.stripe.com/billing", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Chargebee subscription billing", "https://www.chargebee.com/docs/2.0/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Recurly billing platform", "https://docs.recurly.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Zuora revenue automation", "https://knowledgecenter.zuora.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "3.1", True),
    ("NetSuite ERP finance", "https://docs.oracle.com/en/cloud/saas/netsuite/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "3.1", True),
    ("QuickBooks API", "https://developer.intuit.com/app/developer/qbo/docs/get-started", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Xero developer docs", "https://developer.xero.com/documentation/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Paddle billing", "https://developer.paddle.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("ASC 606 revenue recognition", "https://www.fasb.org/page/PageContent?pageId=/reference-library/supplements/asc-606-and-asc-340-40.html", "OSINT-REG-AUDIT", "P7-FINANCE", "4.1", False),
    ("IFRS 15 revenue standard", "https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/", "OSINT-REG-AUDIT", "P7-FINANCE", "4.1", False),
    ("FinOps Foundation framework", "https://www.finops.org/framework/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Cloudability FinOps", "https://docs.apptio.com/bundle/cloudability/page/cloudability-overview.html", "OSINT-FINOPS-AUTO", "P7-FINANCE", "3.1", True),
    ("FinOps automation hype", "https://www.theregister.com/2024/06/12/finops_tooling_sprawl/", "OSINT-SKEP", "P7-FINANCE", "2.1", True),
    ("Rev-rec software overclaim", "https://www.gartner.com/reviews/market/subscription-billing-management", "OSINT-SKEP", "P7-FINANCE", "3.1", True),
    ("EUIPO trademark database", "https://www.euipo.europa.eu/", "OSINT-REG-AUDIT", "P8-LEGAL", "4.1", False),
    ("WIPO Global Brand Database", "https://www.wipo.int/branddb/en/", "OSINT-REG-AUDIT", "P8-LEGAL", "4.1", False),
    ("USPTO trademark search", "https://www.uspto.gov/trademarks/search", "OSINT-REG-AUDIT", "P8-LEGAL", "4.1", False),
    ("INPI France trademarks", "https://www.inpi.fr/", "OSINT-REG-AUDIT", "P8-LEGAL", "4.1", False),
    ("Nice Classification WIPO", "https://www.wipo.int/classifications/nice/en/", "OSINT-REG-AUDIT", "P8-LEGAL", "4.1", False),
    ("Legal tech automation skeptic", "https://www.law.com/legaltechnews/2024/03/15/legal-tech-hype-cycle/", "OSINT-SKEP", "P8-LEGAL", "2.1", True),
    ("Trademark clearance limits", "https://www.inta.org/perspectives/trademark-clearinghouse/", "OSINT-SKEP", "P8-LEGAL", "3.1", True),
    ("Ramp spend management", "https://ramp.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "3.1", True),
    ("Brex corporate cards API", "https://developer.brex.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "3.1", True),
    ("Airbase spend automation", "https://www.airbase.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "3.1", True),
    ("Coupa spend management", "https://www.coupa.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "3.1", True),
    ("Tipalti AP automation", "https://tipalti.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "3.1", True),
    ("Bill.com AP platform", "https://developer.bill.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Avalara tax compliance", "https://developer.avalara.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("TaxJar sales tax API", "https://developers.taxjar.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("SOX compliance overview", "https://www.sec.gov/about/laws/sox2002.pdf", "OSINT-REG-AUDIT", "P8-LEGAL", "4.1", False),
    ("GDPR legal basis guide ICO", "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/", "OSINT-REG-AUDIT", "P8-LEGAL", "4.1", False),
    ("Contract lifecycle CLM Gartner", "https://www.gartner.com/reviews/market/contract-life-cycle-management", "OSINT-REG-AUDIT", "P8-LEGAL", "3.1", True),
    ("Ironclad CLM platform", "https://ironcladapp.com/", "OSINT-REG-AUDIT", "P8-LEGAL", "3.1", True),
    ("DocuSign CLM", "https://www.docusign.com/products/clm", "OSINT-REG-AUDIT", "P8-LEGAL", "3.1", True),
    ("Legal ops technology survey", "https://www.acc.com/resource-library/legal-operations-technology", "OSINT-REG-AUDIT", "P8-LEGAL", "4.1", False),
    ("FinOps maturity model", "https://www.finops.org/framework/maturity-model/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("AWS Cost Explorer", "https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Azure Cost Management", "https://learn.microsoft.com/en-us/azure/cost-management-billing/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("GCP billing export", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Kubecost Kubernetes FinOps", "https://docs.kubecost.com/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Infracost IaC cost estimation", "https://www.infracost.io/docs/", "OSINT-FINOPS-AUTO", "P7-FINANCE", "4.1", False),
    ("Vendor payment fraud skeptic", "https://www.ft.com/content/business-payment-fraud", "OSINT-SKEP", "P7-FINANCE", "2.1", True),
    ("Automated recon false confidence", "https://www.journalofaccountancy.com/issues/2022/jan/automation-risks-in-accounting.html", "OSINT-SKEP", "P7-FINANCE", "3.1", True),
    ("Legal AI contract review hype", "https://www.theregister.com/2024/02/20/legal_ai_contract_review/", "OSINT-SKEP", "P8-LEGAL", "2.1", True),
    ("Trademark troll warning EFF", "https://www.eff.org/issues/intellectual-property/trademarks", "OSINT-SKEP", "P8-LEGAL", "2.1", True),
]


def corp_row(seq: int, title: str, url: str, prong: str) -> dict:
    cluster = "corp_vault_legal" if prong == "P8-LEGAL" else "corp_vault_fin"
    return {
        "source_id": f"SRC-AOS-R8I-{seq:03d}",
        "prong": prong,
        "topic_cluster": cluster,
        "source_title_or_owner": title,
        "url": ledger_url(url),
        "format": "internal_canonical",
        "source_category": "CORPINT",
        "source_level": "5.1",
        "holistika_reliability_score": "5",
        "external_perceived_credibility_score": "2",
        "control_confidence_level": "Safe",
        "decision_use": "def-vault-harvest",
        "notes": (
            f"R8 Finance/Legal vault; impacts: TECH_AUTOMATION_REGISTRY; "
            f"ICS:High; prong={prong}"
        ),
    }


def osint_row(seq: int, title: str, url: str, cluster: str, prong: str, level: str, skeptic: bool) -> dict:
    notes = "R8 OSINT; ICS:Load-bearing;"
    if skeptic:
        notes += " CON: vendor-hype or paywall;"
    return {
        "source_id": f"SRC-AOS-R8E-{seq:03d}",
        "prong": prong,
        "topic_cluster": cluster,
        "source_title_or_owner": title,
        "url": url,
        "format": "webpage",
        "source_category": "OSINT",
        "source_level": level,
        "holistika_reliability_score": "4",
        "external_perceived_credibility_score": "4",
        "control_confidence_level": "Euclid",
        "decision_use": "def-automation-os",
        "notes": notes,
    }


def main() -> None:
    corp_rows: list[dict] = []
    seq = 1
    for title, url, prong in CORPINT_PATHS:
        path = REPO / url.replace("/", "\\") if "\\" in str(REPO) else REPO / url
        if not path.is_file():
            raise SystemExit(f"missing corpint path: {url}")
        corp_rows.append(corp_row(seq, title, url, prong))
        seq += 1
    if len(corp_rows) < 28:
        raise SystemExit(f"expected >=28 corpint rows, got {len(corp_rows)}")

    osint_rows: list[dict] = []
    for idx, (title, url, cluster, prong, level, skeptic) in enumerate(OSINT_SOURCES, start=1):
        osint_rows.append(osint_row(idx, title, url, cluster, prong, level, skeptic))
    if len(osint_rows) < 44:
        raise SystemExit(f"expected >=44 osint rows, got {len(osint_rows)}")

    manifest = {
        "tranche": "R8",
        "id_prefix": "AOS-R8",
        "corpint_target": 28,
        "osint_target": 44,
        "census": {"enabled": False},
        "rows": corp_rows + osint_rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(manifest['rows'])} rows)")


if __name__ == "__main__":
    main()
