#!/usr/bin/env python3
"""One-off generator for Automation OS R4 manifest (Ops + RevOps + PMO harvest)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/tranches/r4-manifest.json"
)

# Priority-ordered CORP-VAULT-OPS (+ limited FINOPS/compliance ops crossover per charter).
CORPINT_PATHS: list[tuple[str, str, str]] = [
    ("Operations area charter", "docs/references/hlk/v3.0/Admin/O5-1/Operations/OPERATIONS_AREA_CHARTER.md", "P3-OPS"),
    ("Operations delivery discipline", "docs/references/hlk/v3.0/Admin/O5-1/Operations/OPERATIONS_DELIVERY_DISCIPLINE.md", "P3-OPS"),
    ("Operations cross-area handoffs", "docs/references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_CROSS_AREA_HANDOFFS.md", "P3-OPS"),
    ("Operations process catalog", "docs/references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_PROCESS_CATALOG.yaml", "P3-OPS"),
    ("Operational cohesion doctrine", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md", "P3-OPS"),
    ("Workspace blueprint Holistika", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md", "P3-OPS"),
    ("PMO client delivery hub topic", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/TOPIC_PMO_CLIENT_DELIVERY_HUB.md", "P3-OPS"),
    ("SOP ops area completeness sweep", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-OPS_AREA_COMPLETENESS_SWEEP_001.md", "P3-OPS"),
    ("SOP PMO operational cohesion index render", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_OPERATIONAL_COHESION_INDEX_RENDER_001.md", "P3-OPS"),
    ("SOP PMO operator inbox render", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_OPERATOR_INBOX_RENDER_001.md", "P3-OPS"),
    ("SOP PMO WIP dashboard render", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_WIP_DASHBOARD_RENDER_001.md", "P3-OPS"),
    ("SOP PMO vault promotion gate", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_VAULT_PROMOTION_GATE_001.md", "P3-OPS"),
    ("SOP PMO initiative program anchors", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md", "P3-OPS"),
    ("SOP initiative governance", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_GOVERNANCE_001.md", "P3-OPS"),
    ("SOP initiative process harmonisation", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md", "P3-OPS"),
    ("SOP PMO process_list CSV maintenance", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md", "P3-OPS"),
    ("SOP external adviser engagement", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md", "P3-OPS"),
    ("External adviser router", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/EXTERNAL_ADVISER_ROUTER.md", "P3-OPS"),
    ("KB human readability charter", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md", "P3-OPS"),
    ("Research backlog Trello registry", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md", "P3-OPS"),
    ("Holistika ops discovery", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md", "P3-OPS"),
    ("RevOps area charter", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/REVOPS_AREA_CHARTER.md", "P3-OPS"),
    ("RevOps process catalog", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/REVOPS_PROCESS_CATALOG.yaml", "P3-OPS"),
    ("SOP RevOps CRM sync", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-REVOPS_CRM_SYNC_001.md", "P3-OPS"),
    ("SOP revenue rollup", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-REVENUE_ROLLUP_001.md", "P3-OPS"),
    ("SOP RevOps QBR", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-REVOPS_QBR_001.md", "P3-OPS"),
    ("SOP engagement scaffolding", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-ENGAGEMENT_SCAFFOLDING_001.md", "P3-OPS"),
    ("SOP engagement template promotion", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md", "P3-OPS"),
    ("SOP RevOps regulator checkpoint", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-REVOPS_REGULATOR_CHECKPOINT_001.md", "P3-OPS"),
    ("SOP RevOps media review", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-REVOPS_MEDIA_REVIEW_001.md", "P3-OPS"),
    ("SOP MADEIRA RevOps handoff", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-MADEIRA_REVOPS_HANDOFF_001.md", "P3-OPS"),
    ("Engagement template registry", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv", "P3-OPS"),
    ("SOP engagement discovery questionnaire", "docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/canonicals/SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md", "P3-OPS"),
    ("SOP engagement estimation discipline", "docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/canonicals/SOP-ENG_ESTIMATION_DISCIPLINE_001.md", "P3-OPS"),
    ("SOP engagement proposal", "docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_PROPOSAL_001.md", "P3-OPS"),
    ("SOP engagement design", "docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md", "P3-OPS"),
    ("SMO service management SOP", "docs/references/hlk/v3.0/Admin/O5-1/Operations/SMO/canonicals/SOP-SERVICE_MGMT_001.md", "P3-OPS"),
    ("SMO service catalog CSV", "docs/references/hlk/v3.0/Admin/O5-1/Operations/SMO/canonicals/SERVICE_CATALOG.csv", "P3-OPS"),
    ("SMO SLA matrix", "docs/references/hlk/v3.0/Admin/O5-1/Operations/SMO/canonicals/SLA_MATRIX.md", "P3-OPS"),
    ("Operations README", "docs/references/hlk/v3.0/Admin/O5-1/Operations/README.md", "P3-OPS"),
    ("Holistika mirror DML apply guide", "docs/guides/holistika-mirror-dml-apply.md", "P3-OPS"),
    ("Holistika ops governance lattice", "docs/guides/holistika-ops-governance-lattice.md", "P3-OPS"),
    ("render_pmo_hub runbook", "scripts/render_pmo_hub.py", "P3-OPS"),
    ("render_operator_inbox runbook", "scripts/render_operator_inbox.py", "P3-OPS"),
    ("render_wip_dashboard runbook", "scripts/render_wip_dashboard.py", "P3-OPS"),
    ("render_operational_cohesion_index runbook", "scripts/render_operational_cohesion_index.py", "P3-OPS"),
    ("revops_dispatch runbook", "scripts/revops_dispatch.py", "P3-OPS"),
    ("validate_area_completeness runbook", "scripts/validate_area_completeness.py", "P3-OPS"),
    ("validate_revops_spine runbook", "scripts/validate_revops_spine.py", "P3-OPS"),
    ("validate_ops_register runbook", "scripts/validate_ops_register.py", "P3-OPS"),
    ("finops_monthly_recon runbook", "scripts/finops_monthly_recon.py", "P7-FINANCE"),
    ("validate_finops_ledger runbook", "scripts/validate_finops_ledger.py", "P7-FINANCE"),
    ("FINOPS discipline", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/FINOPS_DISCIPLINE.md", "P7-FINANCE"),
]

# (title, url, topic_cluster, prong, source_level, skeptic)
OSINT_SOURCES: list[tuple[str, str, str, str, str, bool]] = [
    ("Google SRE workbook", "https://sre.google/workbook/", "OSINT-OPS-ROI", "P3-OPS", "4.1", False),
    ("Google four keys devops", "https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-devops-performance", "OSINT-OPS-ROI", "P3-OPS", "4.1", False),
    ("Accelerate book summary", "https://itrevolution.com/product/accelerate/", "OSINT-OPS-ROI", "P3-OPS", "3.1", False),
    ("Team Topologies", "https://teamtopologies.com/", "OSINT-OPS-ROI", "P3-OPS", "3.1", False),
    ("Internal developer platform guide", "https://internaldeveloperplatform.org/", "OSINT-SCRIPT-GOV", "P3-OPS", "4.1", False),
    ("Backstage docs", "https://backstage.io/docs/overview/what-is-backstage/", "OSINT-SCRIPT-GOV", "P3-OPS", "4.1", False),
    ("Crossplane control plane", "https://docs.crossplane.io/latest/", "OSINT-SCRIPT-GOV", "P3-OPS", "4.1", False),
    ("Port internal developer portal", "https://docs.getport.io/", "OSINT-SCRIPT-GOV", "P3-OPS", "4.1", False),
    ("OpsLevel catalog", "https://docs.opslevel.com/", "OSINT-SCRIPT-GOV", "P3-OPS", "4.1", False),
    ("Cortex IDP", "https://docs.cortex.io/", "OSINT-SCRIPT-GOV", "P3-OPS", "4.1", False),
    ("LaunchDarkly runbooks", "https://docs.launchdarkly.com/home/getting-started", "OSINT-OPS-ROI", "P3-OPS", "4.1", False),
    ("PagerDuty automation", "https://support.pagerduty.com/docs/automation-actions", "OSINT-OPS-ROI", "P3-OPS", "4.1", False),
    ("ServiceNow ITOM", "https://docs.servicenow.com/", "OSINT-OPS-ROI", "P3-OPS", "4.1", True),
    ("Atlassian JSM automation", "https://support.atlassian.com/jira-service-management-cloud/docs/automation-rules/", "OSINT-OPS-ROI", "P3-OPS", "4.1", False),
    ("HubSpot RevOps playbook", "https://www.hubspot.com/revops", "OSINT-OPS-ROI", "P3-OPS", "3.1", False),
    ("Salesforce RevOps guide", "https://www.salesforce.com/resources/articles/revops/", "OSINT-OPS-ROI", "P3-OPS", "3.1", False),
    ("Gartner RevOps hype", "https://www.gartner.com/en/sales/insights/revenue-operations", "OSINT-OPS-ROI", "P3-OPS", "3.1", True),
    ("Forrester RevOps ROI", "https://www.forrester.com/blogs/category/revenue-operations/", "OSINT-OPS-ROI", "P3-OPS", "3.1", True),
    ("LeanIX EA automation", "https://docs.leanix.net/", "OSINT-SCRIPT-GOV", "P3-OPS", "4.1", False),
    ("Terraform run workflow", "https://developer.hashicorp.com/terraform/cloud-docs/run/run-workflows", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
    ("Ansible playbooks best practice", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_best_practices.html", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
    ("Chef Infra runbooks", "https://docs.chef.io/", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", True),
    ("Puppet docs", "https://www.puppet.com/docs", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", True),
    ("SaltStack automation", "https://docs.saltproject.io/", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", True),
    ("GitHub Actions reusable workflows", "https://docs.github.com/en/actions/using-workflows/reusing-workflows", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
    ("GitLab CI components", "https://docs.gitlab.com/ee/ci/components/", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
    ("CircleCI orbs", "https://circleci.com/docs/orb-intro/", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
    ("Pulumi automation API", "https://www.pulumi.com/docs/iac/automation-api/", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
    ("Runbook automation skeptic", "https://www.theregister.com/2023/05/09/platform_engineering/", "OSINT-SKEP", "P3-OPS", "2.1", True),
    ("RevOps tooling sprawl post", "https://www.revenueoperationsalliance.com/", "OSINT-SKEP", "P3-OPS", "2.1", True),
    ("PMO automation limits HBR", "https://hbr.org/topic/subject/project-management", "OSINT-OPS-ROI", "P3-OPS", "2.1", True),
    ("ITIL 4 practice guides", "https://www.axelos.com/best-practice-solutions/itil", "OSINT-OPS-ROI", "P3-OPS", "4.1", False),
    ("PMI standards", "https://www.pmi.org/standards", "OSINT-OPS-ROI", "P3-OPS", "4.1", False),
    ("Scrum Guide", "https://scrumguides.org/scrum-guide.html", "OSINT-OPS-ROI", "P3-OPS", "4.1", False),
    ("Kanban guide", "https://kanbanguides.org/", "OSINT-OPS-ROI", "P3-OPS", "4.1", False),
    ("OKR framework", "https://www.whatmatters.com/faqs/okr-meaning-definition-example/", "OSINT-OPS-ROI", "P3-OPS", "3.1", False),
    ("RevOps council maturity", "https://revopscouncil.com/", "OSINT-OPS-ROI", "P3-OPS", "3.1", False),
    ("Clari RevOps platform", "https://www.clari.com/revenue-platform/", "OSINT-OPS-ROI", "P3-OPS", "3.1", True),
    ("Gong RevOps insights", "https://www.gong.io/revenue-intelligence/", "OSINT-OPS-ROI", "P3-OPS", "3.1", True),
    ("Lean portfolio management", "https://scaledagileframework.com/lean-portfolio-management/", "OSINT-OPS-ROI", "P3-OPS", "4.1", False),
    ("Value stream management", "https://www.plutora.com/blog/value-stream-management", "OSINT-OPS-ROI", "P3-OPS", "3.1", True),
    ("PMI operational excellence PMO", "https://www.pmi.org/learning/library/operational-excellence-pmo-11763", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
    ("Just command runner", "https://github.com/casey/just", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
    ("Make automation manual", "https://www.gnu.org/software/make/manual/make.html", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
    ("Invoke Python tasks", "https://www.pyinvoke.org/", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
    ("Earthly CI reproducibility", "https://docs.earthly.dev/", "OSINT-SCRIPT-GOV", "P1-TECH", "4.1", False),
]


def corp_row(seq: int, title: str, url: str, prong: str) -> dict:
    fmt = "internal_canonical"
    if url.endswith(".yaml"):
        fmt = "internal_canonical"
    elif url.endswith(".csv"):
        fmt = "internal_canonical"
    elif url.startswith("scripts/"):
        fmt = "internal_canonical"
    return {
        "source_id": f"SRC-AOS-R4I-{seq:03d}",
        "prong": prong,
        "topic_cluster": "corp_vault_ops",
        "source_title_or_owner": title,
        "url": url,
        "format": fmt,
        "source_category": "CORPINT",
        "source_level": "5.1",
        "holistika_reliability_score": "5",
        "external_perceived_credibility_score": "2",
        "control_confidence_level": "Safe",
        "decision_use": "def-vault-harvest",
        "notes": (
            f"R4 Ops/RevOps/PMO vault; impacts: TECH_AUTOMATION_REGISTRY; "
            f"ICS:High; prong={prong}"
        ),
    }


def osint_row(seq: int, title: str, url: str, cluster: str, prong: str, level: str, skeptic: bool) -> dict:
    notes = f"R4 OSINT; ICS:Load-bearing;"
    if skeptic:
        notes += " CON: vendor-hype or paywall;"
    return {
        "source_id": f"SRC-AOS-R4E-{seq:03d}",
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
        if seq > 35:
            break
        path = REPO / url.replace("/", "\\") if "\\" in str(REPO) else REPO / url
        if not path.is_file() and not url.startswith("https://"):
            raise SystemExit(f"missing corpint path: {url}")
        corp_rows.append(corp_row(seq, title, url, prong))
        seq += 1
    if len(corp_rows) != 35:
        raise SystemExit(f"expected 35 corpint rows, got {len(corp_rows)}")

    osint_rows: list[dict] = []
    for idx, (title, url, cluster, prong, level, skeptic) in enumerate(OSINT_SOURCES[:44], start=1):
        osint_rows.append(osint_row(idx, title, url, cluster, prong, level, skeptic))
    if len(osint_rows) != 44:
        raise SystemExit(f"expected 44 osint rows, got {len(osint_rows)}")

    manifest = {
        "tranche": "R4",
        "id_prefix": "AOS-R4",
        "corpint_target": 35,
        "osint_target": 44,
        "census": {"enabled": False},
        "rows": corp_rows + osint_rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(manifest['rows'])} rows)")


if __name__ == "__main__":
    main()
