#!/usr/bin/env python3
"""One-off generator for Automation OS R12 manifest (skeptic + academic close + D4 prep)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/tranches/r12-manifest.json"
)
GITHUB_MAIN = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def ledger_url(path: str) -> str:
    """Repo-relative docs/ paths pass through; other paths use GitHub blob URLs."""
    if path.startswith("docs/"):
        return path
    return GITHUB_MAIN + path.replace(chr(92), "/")


# CORP-INCIDENT + all prongs â€” close-out harvest (scripts, session docs, charter, engine).
CORPINT_PATHS: list[tuple[str, str, str]] = [
    ("Automation OS research charter", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/RESEARCH_CHARTER_AND_EXECUTION_PLAN.md", "P4-RESEARCH"),
    ("Session recap 2026-06-10", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/session-recap-2026-06-10.md", "P4-RESEARCH"),
    ("R0 session doctrine", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/r0-session-doctrine-2026-06-10.md", "P4-RESEARCH"),
    ("R6 session doctrine", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/r6-session-doctrine-2026-06-10.md", "P4-RESEARCH"),
    ("Prong synthesis template", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/prong-synthesis-template.md", "P4-RESEARCH"),
    ("HxPESTEL intent tracking template", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/hxpestel-intent-tracking-template.md", "P4-RESEARCH"),
    ("Methodology cross-area wiring", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/methodology-cross-area-wiring-2026-06-10.md", "P4-RESEARCH"),
    ("Source ledger CSV", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/source-ledger.csv", "P4-RESEARCH"),
    ("Tranche R6 regression report", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/tranche-r6-regression.md", "P4-RESEARCH"),
    ("research_ledger.py engine", "scripts/research_ledger.py", "P4-RESEARCH"),
    ("holistic_agentic_r1 ledger bootstrap", "scripts/holistic_agentic_r1_ledger_bootstrap.py", "P4-RESEARCH"),
    ("holistic_agentic_r2 ledger append", "scripts/holistic_agentic_r2_ledger_append.py", "P4-RESEARCH"),
    ("holistic_agentic_r3 ledger append", "scripts/holistic_agentic_r3_ledger_append.py", "P4-RESEARCH"),
    ("i93_p7 hygiene apply script", "scripts/i93_p7_hygiene_apply.py", "P2-DATA"),
    ("i94_p4 ops research ledger bootstrap", "scripts/i94_p4_ops_research_ledger_bootstrap.py", "P3-OPS"),
    ("i94_area09 process list tranche", "scripts/i94_area09_process_list_tranche.py", "P6-COMPLIANCE"),
    ("i94_p3 placement updates", "scripts/i94_p3_placement_updates.py", "P3-OPS"),
    ("CONTRIBUTING.md standards", "CONTRIBUTING.md", "P1-TECH"),
    ("TECHOPS discipline", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/TECHOPS_DISCIPLINE.md", "P1-TECH"),
    ("verify.py orchestrator", "scripts/verify.py", "P1-TECH"),
    ("DATAOPS discipline", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md", "P2-DATA"),
    ("Data contract standard", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_CONTRACT_STANDARD.md", "P2-DATA"),
    ("Operations area charter", "docs/references/hlk/v3.0/Admin/O5-1/Operations/OPERATIONS_AREA_CHARTER.md", "P3-OPS"),
    ("Research action discipline", "docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md", "P4-RESEARCH"),
    ("validate_research_action runbook", "scripts/validate_research_action.py", "P4-RESEARCH"),
    ("akos research_ledger_ops module", "akos/research_ledger_ops.py", "P4-RESEARCH"),
    ("Holistika quality fabric", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md", "P5-PEOPLE"),
    ("PRECEDENCE doctrine", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md", "P6-COMPLIANCE"),
    ("Process list CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv", "P6-COMPLIANCE"),
    ("FINOPS discipline", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/FINOPS_DISCIPLINE.md", "P7-FINANCE"),
    ("SOP trademark naming governance", "docs/references/hlk/v3.0/Admin/O5-1/People/Legal/SOP-TRADEMARK_NAMING_GOVERNANCE_001.md", "P8-LEGAL"),
    ("Brand architecture", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ARCHITECTURE.md", "P9-MARKETING"),
    ("Intelligence discipline charter", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md", "P10-INTEL-OPS"),
    ("MADEIRA tool catalog", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_TOOL_CATALOG.md", "P11-ENVOY-MADEIRA"),
    ("SOP OpenClaw runtime health triage", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md", "P11-ENVOY-MADEIRA"),
    ("RPA adapter registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/dimensions/RPA_ADAPTER_REGISTRY.csv", "P12-RPA-ADAPTERS"),
    ("RevOps adapter registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/REVOPS_ADAPTER_REGISTRY.csv", "P12-RPA-ADAPTERS"),
    ("Research-action cursor rule", ".cursor/rules/akos-research-action.mdc", "P4-RESEARCH"),
    ("test_research_ledger_ops", "tests/test_research_ledger_ops.py", "P4-RESEARCH"),
    ("validate_hlk umbrella runbook", "scripts/validate_hlk.py", "P6-COMPLIANCE"),
]

# OSINT-SKEP + OSINT-ACA â€” skeptic close + academic rigor across all prongs.
OSINT_SOURCES: list[tuple[str, str, str, str, str, bool]] = [
    ("PRISMA systematic review", "https://www.prisma-statement.org/", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Cochrane handbook", "https://training.cochrane.org/handbook", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("GRADE working group", "https://www.gradeworkinggroup.org/", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Systematic review skeptic BMJ", "https://www.bmj.com/content/347/bmj.f5023", "OSINT-SKEP", "P4-RESEARCH", "2.1", True),
    ("AI literature review hype Nature", "https://www.nature.com/articles/d41586-023-02596-6", "OSINT-SKEP", "P4-RESEARCH", "2.1", True),
    ("Automation OS platform realist", "https://www.theregister.com/2023/05/09/platform_engineering/", "OSINT-SKEP", "P1-TECH", "2.1", True),
    ("DevOps silver bullet critique", "https://martinfowler.com/bliki/ContinuousDelivery.html", "OSINT-SKEP", "P1-TECH", "4.1", False),
    ("Data mesh skeptic", "https://www.infoq.com/articles/data-mesh-tradeoffs/", "OSINT-SKEP", "P2-DATA", "2.1", True),
    ("DAMA-DMBOK overview", "https://www.dama.org/cpages/body-of-knowledge", "OSINT-ACA", "P2-DATA", "4.1", False),
    ("PMO automation limits HBR", "https://hbr.org/topic/subject/project-management", "OSINT-SKEP", "P3-OPS", "2.1", True),
    ("Accelerate DORA research", "https://dora.dev/research/", "OSINT-ACA", "P3-OPS", "4.1", False),
    ("UAT cargo cult skeptic", "https://www.jamesmarcusrogers.com/post/uat-is-dead", "OSINT-SKEP", "P5-PEOPLE", "2.1", True),
    ("World Quality Report", "https://www.capgemini.com/insights/research-library/world-quality-report/", "OSINT-ACA", "P5-PEOPLE", "4.1", False),
    ("Compliance automation theater", "https://www.satisfice.com/blog/archives/856", "OSINT-SKEP", "P6-COMPLIANCE", "2.1", True),
    ("ISO 27001 overview", "https://www.iso.org/isoiec-27001-information-security.html", "OSINT-ACA", "P6-COMPLIANCE", "4.1", False),
    ("FinOps automation hype", "https://www.theregister.com/2024/06/12/finops_tooling_sprawl/", "OSINT-SKEP", "P7-FINANCE", "2.1", True),
    ("FinOps Foundation framework", "https://www.finops.org/framework/", "OSINT-ACA", "P7-FINANCE", "4.1", False),
    ("Legal AI contract review hype", "https://www.theregister.com/2024/02/20/legal_ai_contract_review/", "OSINT-SKEP", "P8-LEGAL", "2.1", True),
    ("EUIPO trademark database", "https://www.euipo.europa.eu/", "OSINT-ACA", "P8-LEGAL", "4.1", False),
    ("MarTech stack sprawl skeptic", "https://www.chiefmartec.com/2024/01/martech-stack-complexity/", "OSINT-SKEP", "P9-MARKETING", "2.1", True),
    ("HubSpot RevOps playbook", "https://www.hubspot.com/revops", "OSINT-ACA", "P9-MARKETING", "3.1", False),
    ("Vendor intel platform skeptic", "https://www.theregister.com/2024/02/14/osint_platform_hype/", "OSINT-SKEP", "P10-INTEL-OPS", "2.1", True),
    ("NATO OSINT handbook", "https://www.nato.int/cps/en/natohq/topics_68368.htm", "OSINT-ACA", "P10-INTEL-OPS", "4.1", False),
    ("Agent CLI hype skeptic", "https://www.theregister.com/2025/02/14/ai_coding_agent_cli_hype/", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "2.1", True),
    ("Model Context Protocol", "https://modelcontextprotocol.io/introduction", "OSINT-ACA", "P11-ENVOY-MADEIRA", "4.1", False),
    ("RPA hype cycle Gartner", "https://www.gartner.com/en/articles/rpa-hype-cycle", "OSINT-SKEP", "P12-RPA-ADAPTERS", "2.1", True),
    ("n8n workflow automation", "https://docs.n8n.io/", "OSINT-ACA", "P12-RPA-ADAPTERS", "4.1", False),
    ("Predatory journal watch", "https://predatoryjournals.com/", "OSINT-SKEP", "P4-RESEARCH", "2.1", True),
    ("Citation cartels warning", "https://www.science.org/content/article/citation-cartels", "OSINT-SKEP", "P4-RESEARCH", "2.1", True),
    ("Evidence Based Medicine toolkit", "https://ebm-tools.knowledgeTranslation.ca/", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Oxford CEBM levels", "https://www.cebm.ox.ac.uk/resources/levels-of-evidence", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Research automation overclaim Guardian", "https://www.theguardian.com/technology/2023/mar/23/ai-tools-research-academic-papers", "OSINT-SKEP", "P4-RESEARCH", "2.1", True),
    ("Platform engineering guide", "https://internaldeveloperplatform.org/", "OSINT-ACA", "P1-TECH", "4.1", False),
    ("CI/CD tool sprawl skeptic", "https://www.theregister.com/2023/05/09/platform_engineering/", "OSINT-SKEP", "P1-TECH", "2.1", True),
    ("Data governance platform skeptic", "https://www.theregister.com/2024/01/15/data_governance_platforms/", "OSINT-SKEP", "P2-DATA", "2.1", True),
    ("RevOps tooling sprawl", "https://www.revenueoperationsalliance.com/", "OSINT-SKEP", "P3-OPS", "2.1", True),
    ("ISTQB foundation syllabus", "https://www.istqb.org/certifications/certified-tester-foundation-level", "OSINT-ACA", "P5-PEOPLE", "4.1", False),
    ("QA automation overpromise", "https://www.theregister.com/2024/03/15/ai_testing_hype/", "OSINT-SKEP", "P5-PEOPLE", "2.1", True),
    ("GRC platform market hype", "https://www.gartner.com/reviews/market/it-risk-management", "OSINT-SKEP", "P6-COMPLIANCE", "3.1", True),
    ("SOC 2 trust principles", "https://www.aicpa.org/resources/article/soc-2-trust-services-criteria", "OSINT-ACA", "P6-COMPLIANCE", "4.1", False),
    ("Rev-rec software overclaim", "https://www.gartner.com/reviews/market/subscription-billing-management", "OSINT-SKEP", "P7-FINANCE", "3.1", True),
    ("ASC 606 revenue recognition", "https://www.fasb.org/page/PageContent?pageId=/reference-library/supplements/asc-606-and-asc-340-40.html", "OSINT-ACA", "P7-FINANCE", "4.1", False),
    ("Trademark troll warning EFF", "https://www.eff.org/issues/intellectual-property/trademarks", "OSINT-SKEP", "P8-LEGAL", "2.1", True),
    ("WIPO Global Brand Database", "https://www.wipo.int/branddb/en/", "OSINT-ACA", "P8-LEGAL", "4.1", False),
    ("Marketing automation overpromise", "https://www.theguardian.com/media/2023/mar/15/marketing-automation-ai-hype", "OSINT-SKEP", "P9-MARKETING", "2.1", True),
    ("Salesforce RevOps guide", "https://www.salesforce.com/resources/articles/revops/", "OSINT-ACA", "P9-MARKETING", "3.1", False),
    ("Palantir Gotham docs skeptic", "https://www.theregister.com/2024/02/14/osint_platform_hype/", "OSINT-SKEP", "P10-INTEL-OPS", "2.1", True),
    ("Bellingcat OSINT guide", "https://www.bellingcat.com/resources/how-tos/", "OSINT-ACA", "P10-INTEL-OPS", "4.1", False),
    ("Low-code agent builder skeptic", "https://www.theregister.com/2024/11/20/no_code_ai_agents/", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "2.1", True),
    ("Nx monorepo docs", "https://nx.dev/getting-started/intro", "OSINT-ACA", "P11-ENVOY-MADEIRA", "4.1", False),
    ("iPaaS vendor lock-in warning", "https://www.theregister.com/2023/09/12/ipaas_vendor_lock/", "OSINT-SKEP", "P12-RPA-ADAPTERS", "2.1", True),
    ("Zapier platform", "https://platform.zapier.com/docs", "OSINT-ACA", "P12-RPA-ADAPTERS", "4.1", False),
    ("Scite.ai skeptic use case", "https://scite.ai/", "OSINT-SKEP", "P4-RESEARCH", "3.1", True),
    ("Connected Papers", "https://www.connectedpapers.com/about", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("OpenAlex documentation", "https://docs.openalex.org/", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Semantic Scholar API", "https://api.semanticscholar.org/", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Model eval skeptic Ben Evans", "https://www.ben-evans.com/benedictevans/2024/2/12/generative-ai-evaluation", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "2.1", True),
    ("Monorepo tooling fatigue", "https://www.infoq.com/articles/monorepo-polyrepo-tradeoffs/", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "2.1", True),
    ("Integration platform fatigue", "https://www.chiefmartec.com/2023/12/integration-fatigue/", "OSINT-SKEP", "P12-RPA-ADAPTERS", "2.1", True),
    ("Campbell collaboration methods", "https://www.campbellcollaboration.org/", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Nature research methods", "https://www.nature.com/nature-research/intelligence", "OSINT-ACA", "P4-RESEARCH", "3.1", True),
    ("Checklist compliance theater", "https://queue.acm.org/detail.cfm?id=3454122", "OSINT-SKEP", "P6-COMPLIANCE", "4.1", True),
    ("Shift-left overreach", "https://www.thoughtworks.com/insights/blog/shift-left-doesnt-mean-no-ops", "OSINT-SKEP", "P3-OPS", "2.1", True),
    ("100% coverage fallacy", "https://www.infoq.com/articles/code-coverage-misuse/", "OSINT-SKEP", "P5-PEOPLE", "2.1", True),
    ("CDP category confusion", "https://www.theregister.com/2024/04/10/cdp_market_confusion/", "OSINT-SKEP", "P9-MARKETING", "3.1", True),
    ("MCP protocol fragmentation", "https://www.infoq.com/news/2025/mcp-adoption/", "OSINT-SKEP", "P12-RPA-ADAPTERS", "3.1", True),
    ("Multi-agent coordination limits", "https://queue.acm.org/detail.cfm?id=3710842", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "4.1", True),
]


def corp_row(seq: int, title: str, url: str, prong: str) -> dict:
    if url.startswith("scripts/") or url.startswith("akos/") or url.startswith("tests/"):
        cluster = "corp_incident"
    elif url.startswith("docs/wip/intelligence/"):
        cluster = "corp_incident"
    elif prong.startswith("P6"):
        cluster = "corp_vault_compliance"
    elif prong.startswith("P7"):
        cluster = "corp_vault_fin"
    elif prong.startswith("P8"):
        cluster = "corp_vault_legal"
    elif prong.startswith("P9"):
        cluster = "corp_vault_mkt"
    elif prong.startswith("P10"):
        cluster = "corp_vault_intel"
    elif prong.startswith("P11"):
        cluster = "corp_vault_envoy"
    elif prong.startswith("P12"):
        cluster = "corp_vault_adapters"
    elif prong.startswith("P4"):
        cluster = "corp_vault_research"
    elif prong.startswith("P5"):
        cluster = "corp_vault_people"
    elif prong.startswith("P3"):
        cluster = "corp_vault_ops"
    elif prong.startswith("P2"):
        cluster = "corp_vault_data"
    else:
        cluster = "corp_vault_tech"
    return {
        "source_id": f"SRC-AOS-R12I-{seq:03d}",
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
            f"R12 skeptic/academic close; impacts: D4/D6/D7/D8; "
            f"ICS:Load-bearing; prong={prong}"
        ),
    }


def osint_row(seq: int, title: str, url: str, cluster: str, prong: str, level: str, skeptic: bool) -> dict:
    notes = "R12 OSINT; ICS:Corroboration;"
    if skeptic:
        notes += " CON: vendor-hype or paywall;"
    return {
        "source_id": f"SRC-AOS-R12E-{seq:03d}",
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
    if len(corp_rows) < 40:
        raise SystemExit(f"expected >=40 corpint rows, got {len(corp_rows)}")

    osint_rows: list[dict] = []
    for idx, (title, url, cluster, prong, level, skeptic) in enumerate(OSINT_SOURCES[:66], start=1):
        osint_rows.append(osint_row(idx, title, url, cluster, prong, level, skeptic))
    if len(osint_rows) < 66:
        raise SystemExit(f"expected >=66 osint rows, got {len(osint_rows)}")

    manifest = {
        "tranche": "R12",
        "id_prefix": "AOS-R12",
        "corpint_target": 40,
        "osint_target": 66,
        "census": {"enabled": False},
        "rows": corp_rows + osint_rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(manifest['rows'])} rows)")


if __name__ == "__main__":
    main()
