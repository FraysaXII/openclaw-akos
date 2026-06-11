#!/usr/bin/env python3
"""One-off generator for Automation OS R9 manifest (Marketing + CRM adapters)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/tranches/r9-manifest.json"
)
GITHUB_MAIN = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def ledger_url(path: str) -> str:
    """Repo-relative docs/ paths pass through; other paths use GitHub blob URLs."""
    if path.startswith("docs/"):
        return path
    return GITHUB_MAIN + path.replace(chr(92), "/")


# Priority-ordered CORP-VAULT-MKT + CORP-VAULT-ADAPTERS (CRM/RPA registries).
CORPINT_PATHS: list[tuple[str, str, str]] = [
    ("Marketing lifecycle taxonomy", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/canonicals/MARKETING_LIFECYCLE_TAXONOMY.md", "P9-MARKETING"),
    ("Marketing area M3 redesign", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/canonicals/MARKETING_AREA_M3_REDESIGN.md", "P9-MARKETING"),
    ("Brand architecture", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ARCHITECTURE.md", "P9-MARKETING"),
    ("Brand baseline reality matrix", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md", "P9-MARKETING"),
    ("Brand voice foundation", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_VOICE_FOUNDATION.md", "P9-MARKETING"),
    ("Brand register matrix", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_REGISTER_MATRIX.md", "P9-MARKETING"),
    ("SOP brand canon maintenance", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_CANON_MAINTENANCE_001.md", "P9-MARKETING"),
    ("SOP GTM qualification", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/SOP-GTM_QUALIFICATION_001.md", "P9-MARKETING"),
    ("SOP GTM BD handoff", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/SOP-GTM_BD_HANDOFF_001.md", "P9-MARKETING"),
    ("SOP GTM inbound SLA", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/SOP-GTM_INBOUND_SLA_001.md", "P9-MARKETING"),
    ("Web form doctrine", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/WEB_FORM_DOCTRINE.md", "P9-MARKETING"),
    ("Cal schedule doctrine", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/CAL_SCHEDULE_DOCTRINE.md", "P9-MARKETING"),
    ("Resonance area charter", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Resonance/canonicals/RESONANCE_AREA_CHARTER.md", "P9-MARKETING"),
    ("Storytelling area charter", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/STORYTELLING_AREA_CHARTER.md", "P9-MARKETING"),
    ("Service offering catalog", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/SERVICE_OFFERING_CATALOG.md", "P9-MARKETING"),
    ("CRM adapter registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/dimensions/CRM_ADAPTER_REGISTRY.csv", "P9-MARKETING"),
    ("Communication adapter registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/dimensions/COMMUNICATION_ADAPTER_REGISTRY.csv", "P12-RPA-ADAPTERS"),
    ("Attribution adapter registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Experimentation/canonicals/dimensions/ATTRIBUTION_ADAPTER_REGISTRY.csv", "P12-RPA-ADAPTERS"),
    ("RPA adapter registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/dimensions/RPA_ADAPTER_REGISTRY.csv", "P12-RPA-ADAPTERS"),
    ("Data integration plane", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_INTEGRATION_PLANE.md", "P12-RPA-ADAPTERS"),
    ("DATAOPS discipline", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md", "P12-RPA-ADAPTERS"),
    ("SOP data engagement integration scaffold", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md", "P12-RPA-ADAPTERS"),
    ("Brand baseline reality cursor rule", ".cursor/rules/akos-brand-baseline-reality.mdc", "P9-MARKETING"),
    ("External render discipline cursor rule", ".cursor/rules/akos-external-render-discipline.mdc", "P9-MARKETING"),
    ("validate_adapter_registries runbook", "scripts/validate_adapter_registries.py", "P12-RPA-ADAPTERS"),
    ("validate_brand_canon_drift runbook", "scripts/validate_brand_canon_drift.py", "P9-MARKETING"),
    ("validate_brand_baseline_reality_drift runbook", "scripts/validate_brand_baseline_reality_drift.py", "P9-MARKETING"),
    ("akos hlk adapter registry module", "akos/hlk_adapter_registry_csv.py", "P12-RPA-ADAPTERS"),
]

# OSINT-RPA + OSINT-INTEROP â€” MarTech automation + integration interop.
OSINT_SOURCES: list[tuple[str, str, str, str, str, bool]] = [
    ("HubSpot CRM API", "https://developers.hubspot.com/docs/api/overview", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Salesforce REST API", "https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Pipedrive API", "https://developers.pipedrive.com/docs/api/v1", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Zoho CRM API", "https://www.zoho.com/crm/developer/docs/api/v6/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Microsoft Dynamics 365", "https://learn.microsoft.com/en-us/dynamics365/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("n8n workflow automation", "https://docs.n8n.io/", "OSINT-RPA", "P12-RPA-ADAPTERS", "4.1", False),
    ("Make Integromat", "https://www.make.com/en/help", "OSINT-RPA", "P12-RPA-ADAPTERS", "4.1", False),
    ("Zapier platform", "https://platform.zapier.com/docs", "OSINT-RPA", "P12-RPA-ADAPTERS", "4.1", False),
    ("Power Automate docs", "https://learn.microsoft.com/en-us/power-automate/", "OSINT-RPA", "P12-RPA-ADAPTERS", "4.1", False),
    ("UiPath automation platform", "https://docs.uipath.com/", "OSINT-RPA", "P12-RPA-ADAPTERS", "3.1", True),
    ("Automation Anywhere", "https://docs.automationanywhere.com/", "OSINT-RPA", "P12-RPA-ADAPTERS", "3.1", True),
    ("RPA hype cycle Gartner", "https://www.gartner.com/en/articles/rpa-hype-cycle", "OSINT-SKEP", "P12-RPA-ADAPTERS", "2.1", True),
    ("iPaaS vendor lock-in warning", "https://www.theregister.com/2023/09/12/ipaas_vendor_lock/", "OSINT-SKEP", "P12-RPA-ADAPTERS", "2.1", True),
    ("Segment CDP docs", "https://segment.com/docs/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("RudderStack open CDP", "https://www.rudderstack.com/docs/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("mParticle CDP", "https://docs.mparticle.com/", "OSINT-INTEROP", "P9-MARKETING", "3.1", True),
    ("Calendly API", "https://developer.calendly.com/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Cal.com API", "https://cal.com/docs/developing/introduction", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Typeform API", "https://www.typeform.com/developers/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Tally forms API", "https://tally.so/help/api", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Mailchimp Marketing API", "https://mailchimp.com/developer/marketing/api/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("SendGrid API", "https://docs.sendgrid.com/api-reference", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Brevo API", "https://developers.brevo.com/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Customer.io docs", "https://docs.customer.io/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("ActiveCampaign API", "https://developers.activecampaign.com/reference/overview", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Mautic open marketing", "https://docs.mautic.org/", "OSINT-INTEROP", "P9-MARKETING", "4.1", False),
    ("Apache Camel integration", "https://camel.apache.org/manual/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("MuleSoft Anypoint", "https://docs.mulesoft.com/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "3.1", True),
    ("Boomi integration platform", "https://help.boomi.com/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "3.1", True),
    ("Workato automation", "https://docs.workato.com/", "OSINT-RPA", "P12-RPA-ADAPTERS", "3.1", True),
    ("Tray.io automation", "https://tray.io/documentation", "OSINT-RPA", "P12-RPA-ADAPTERS", "3.1", True),
    ("OpenAPI specification", "https://spec.openapis.org/oas/latest.html", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("AsyncAPI event-driven", "https://www.asyncapi.com/docs", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("GraphQL federation", "https://www.apollographql.com/docs/federation/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("MarTech stack sprawl skeptic", "https://www.chiefmartec.com/2024/01/martech-stack-complexity/", "OSINT-SKEP", "P9-MARKETING", "2.1", True),
    ("CRM customization debt", "https://www.salesforceben.com/crm-customization-debt/", "OSINT-SKEP", "P9-MARKETING", "3.1", True),
    ("Low-code integration limits", "https://www.infoq.com/articles/low-code-integration-pitfalls/", "OSINT-SKEP", "P12-RPA-ADAPTERS", "2.1", True),
    ("Attribution modeling skeptic", "https://www.nngroup.com/articles/analytics-attribution/", "OSINT-SKEP", "P9-MARKETING", "2.1", True),
    ("Marketing automation overpromise", "https://www.theguardian.com/media/2023/mar/15/marketing-automation-ai-hype", "OSINT-SKEP", "P9-MARKETING", "2.1", True),
    ("CDP category confusion", "https://www.theregister.com/2024/04/10/cdp_market_confusion/", "OSINT-SKEP", "P9-MARKETING", "3.1", True),
    ("Webhook reliability patterns", "https://webhooks.fyi/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Stripe Connect marketplace", "https://stripe.com/docs/connect", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Shopify API interop", "https://shopify.dev/docs/api", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Composio tool integration", "https://docs.composio.dev/", "OSINT-RPA", "P12-RPA-ADAPTERS", "4.1", False),
    ("Temporal workflow engine", "https://docs.temporal.io/", "OSINT-RPA", "P12-RPA-ADAPTERS", "4.1", False),
]


def corp_row(seq: int, title: str, url: str, prong: str) -> dict:
    cluster = "corp_vault_adapters" if prong == "P12-RPA-ADAPTERS" else "corp_vault_mkt"
    return {
        "source_id": f"SRC-AOS-R9I-{seq:03d}",
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
            f"R9 Marketing/CRM adapters vault; impacts: TECH_AUTOMATION_REGISTRY; "
            f"ICS:Medium; prong={prong}"
        ),
    }


def osint_row(seq: int, title: str, url: str, cluster: str, prong: str, level: str, skeptic: bool) -> dict:
    notes = "R9 OSINT; ICS:Load-bearing;"
    if skeptic:
        notes += " CON: vendor-hype or paywall;"
    return {
        "source_id": f"SRC-AOS-R9E-{seq:03d}",
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
        "tranche": "R9",
        "id_prefix": "AOS-R9",
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
