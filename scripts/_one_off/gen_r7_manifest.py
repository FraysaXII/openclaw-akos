#!/usr/bin/env python3
"""One-off generator for Automation OS R7 manifest (Compliance + PRECEDENCE + process_list)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/tranches/r7-manifest.json"
)
GITHUB_MAIN = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def ledger_url(path: str) -> str:
    """Repo-relative docs/ paths pass through; other paths use GitHub blob URLs."""
    if path.startswith("docs/"):
        return path
    return GITHUB_MAIN + path.replace(chr(92), "/")


# Priority-ordered CORP-VAULT-COMPLIANCE (PRECEDENCE + canonical gates + process_list).
CORPINT_PATHS: list[tuple[str, str, str]] = [
    ("PRECEDENCE canonical/mirror doctrine", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md", "P6-COMPLIANCE"),
    ("Process list CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv", "P6-COMPLIANCE"),
    ("Baseline organisation CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv", "P6-COMPLIANCE"),
    ("Access levels", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/access_levels.md", "P6-COMPLIANCE"),
    ("Confidence levels", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md", "P6-COMPLIANCE"),
    ("Source taxonomy", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md", "P6-COMPLIANCE"),
    ("Canonical registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv", "P6-COMPLIANCE"),
    ("Initiative registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv", "P6-COMPLIANCE"),
    ("Decision register CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv", "P6-COMPLIANCE"),
    ("SOP meta process management", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md", "P6-COMPLIANCE"),
    ("HLK KM topic-fact-source", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md", "P6-COMPLIANCE"),
    ("Initiative dependencies", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_DEPENDENCIES.md", "P6-COMPLIANCE"),
    ("Compliance canonicals README", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/README.md", "P6-COMPLIANCE"),
    ("People compliance vs ethics boundary", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PEOPLE_COMPLIANCE_VS_ETHICS_BOUNDARY.md", "P6-COMPLIANCE"),
    ("Canonical governance registry", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CANONICAL_GOVERNANCE_REGISTRY.csv", "P6-COMPLIANCE"),
    ("Policy register CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/POLICY_REGISTER.csv", "P6-COMPLIANCE"),
    ("Capability registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv", "P6-COMPLIANCE"),
    ("Classification lattice", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CLASSIFICATION_LATTICE.md", "P6-COMPLIANCE"),
    ("OPS register CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv", "P6-COMPLIANCE"),
    ("Cycle register CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CYCLE_REGISTER.csv", "P6-COMPLIANCE"),
    ("Repo health snapshot CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPO_HEALTH_SNAPSHOT.csv", "P6-COMPLIANCE"),
    ("Component service matrix CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv", "P6-COMPLIANCE"),
    ("SOP ENISA readiness", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-ENISA_READINESS_001.md", "P6-COMPLIANCE"),
    ("Founder governance document lifecycle", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md", "P6-COMPLIANCE"),
    ("SOP transcript redaction", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-HLK_TRANSCRIPT_REDACTION_001.md", "P6-COMPLIANCE"),
    ("validate_hlk runbook", "scripts/validate_hlk.py", "P6-COMPLIANCE"),
    ("validate_compliance_schema_drift runbook", "scripts/validate_compliance_schema_drift.py", "P6-COMPLIANCE"),
    ("validate_canonical_registry runbook", "scripts/validate_canonical_registry.py", "P6-COMPLIANCE"),
    ("validate_decision_register runbook", "scripts/validate_decision_register.py", "P6-COMPLIANCE"),
    ("validate_process_list_pairing runbook", "scripts/validate_process_list_pairing.py", "P6-COMPLIANCE"),
    ("Repository registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv", "P6-COMPLIANCE"),
]

# OSINT-REG-AUDIT â€” compliance audit bar + regulatory voices (charter R7 pairing).
OSINT_SOURCES: list[tuple[str, str, str, str, str, bool]] = [
    ("ISO 27001 overview", "https://www.iso.org/isoiec-27001-information-security.html", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("SOC 2 trust principles", "https://www.aicpa.org/resources/article/soc-2-trust-services-criteria", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("NIST CSF 2.0", "https://www.nist.gov/cyberframework", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("GDPR official text portal", "https://gdpr-info.eu/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("CNIL GDPR guidance", "https://www.cnil.fr/en/gdpr", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("ENISA cloud security", "https://www.enisa.europa.eu/topics/cloud-and-big-data/cloud-security", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("EU AI Act summary", "https://artificialintelligenceact.eu/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("DAMA-DMBOK overview", "https://www.dama.org/cpages/body-of-knowledge", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("COBIT 2019 framework", "https://www.isaca.org/resources/cobit", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("ITIL 4 governance practices", "https://www.axelos.com/best-practice-solutions/itil", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("Open Compliance and Ethics Group", "https://www.oceg.org/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "3.1", False),
    ("GRC platform market hype", "https://www.gartner.com/reviews/market/it-risk-management", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "3.1", True),
    ("Compliance automation overclaim", "https://www.theregister.com/2023/11/02/compliance_automation_hype/", "OSINT-SKEP", "P6-COMPLIANCE", "2.1", True),
    ("Checkbox compliance theater", "https://www.satisfice.com/blog/archives/856", "OSINT-SKEP", "P6-COMPLIANCE", "2.1", True),
    ("Audit fatigue HBR", "https://hbr.org/2016/03/audit-committees-need-to-look-beyond-the-numbers", "OSINT-SKEP", "P6-COMPLIANCE", "2.1", True),
    ("ISO certification skeptic", "https://www.ncsc.gov.uk/collection/board-toolkit/supply-chain-security", "OSINT-SKEP", "P6-COMPLIANCE", "2.1", True),
    ("SOC 2 scope creep warning", "https://www.vanta.com/resources/soc-2-scope", "OSINT-SKEP", "P6-COMPLIANCE", "3.1", True),
    ("OpenSSF best practices", "https://openssf.org/projects/best-practices-badge/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("SLSA supply chain levels", "https://slsa.dev/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("CIS Controls v8", "https://www.cisecurity.org/controls", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("PCI DSS overview", "https://www.pcisecuritystandards.org/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("HIPAA security rule summary", "https://www.hhs.gov/hipaa/for-professionals/security/index.html", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("FedRAMP marketplace", "https://www.fedramp.gov/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("CSA STAR registry", "https://cloudsecurityalliance.org/star", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("Vanta compliance automation", "https://www.vanta.com/products/automated-compliance", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "3.1", True),
    ("Drata GRC platform", "https://drata.com/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "3.1", True),
    ("OneTrust privacy management", "https://www.onetrust.com/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "3.1", True),
    ("ServiceNow GRC", "https://www.servicenow.com/products/grc.html", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "3.1", True),
    ("Process mining for compliance", "https://www.celonis.com/process-mining/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "3.1", False),
    ("ArchiMate governance viewpoint", "https://pubs.opengroup.org/architecture/archimate3-doc/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("Open Group IT4IT reference", "https://www.opengroup.org/it4it", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("CMMI governance practices", "https://cmmiinstitute.com/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("Regulatory sandboxes EU", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-sandbox", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("Basel operational risk", "https://www.bis.org/basel_framework/chapter/opr/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("COSO internal control framework", "https://www.coso.org/guidance-on-ic", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("Three lines of defense model", "https://www.iia.org.uk/resources/three-lines-model/", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("Audit trail best practices NIST", "https://csrc.nist.gov/publications/detail/sp/800-92/final", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("Records management ISO 15489", "https://www.iso.org/standard/62542.html", "OSINT-REG-AUDIT", "P6-COMPLIANCE", "4.1", False),
    ("Data governance skeptic", "https://www.theregister.com/2024/01/15/data_governance_platforms/", "OSINT-SKEP", "P6-COMPLIANCE", "2.1", True),
    ("GRC tool sprawl post", "https://www.gartner.com/en/articles/grc-technology", "OSINT-SKEP", "P6-COMPLIANCE", "3.1", True),
    ("Compliance debt accumulation", "https://queue.acm.org/detail.cfm?id=3454122", "OSINT-SKEP", "P6-COMPLIANCE", "4.1", True),
    ("Regulatory capture warning", "https://www.brookings.edu/articles/regulatory-capture/", "OSINT-SKEP", "P6-COMPLIANCE", "2.1", True),
    ("Privacy theater critique", "https://www.eff.org/deeplinks/2020/01/gdpr-after-first-year", "OSINT-SKEP", "P6-COMPLIANCE", "2.1", True),
    ("Audit automation limits", "https://www.journalofaccountancy.com/issues/2021/mar/audit-automation-risks.html", "OSINT-SKEP", "P6-COMPLIANCE", "3.1", True),
]


def corp_row(seq: int, title: str, url: str, prong: str) -> dict:
    return {
        "source_id": f"SRC-AOS-R7I-{seq:03d}",
        "prong": prong,
        "topic_cluster": "corp_vault_compliance",
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
            f"R7 Compliance/PRECEDENCE/process_list vault; impacts: TECH_AUTOMATION_REGISTRY; "
            f"ICS:Load-bearing; prong={prong}"
        ),
    }


def osint_row(seq: int, title: str, url: str, cluster: str, prong: str, level: str, skeptic: bool) -> dict:
    notes = "R7 OSINT; ICS:Load-bearing;"
    if skeptic:
        notes += " CON: vendor-hype or paywall;"
    return {
        "source_id": f"SRC-AOS-R7E-{seq:03d}",
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
    for title, url, prong in CORPINT_PATHS[:30]:
        path = REPO / url.replace("/", "\\") if "\\" in str(REPO) else REPO / url
        if not path.is_file():
            raise SystemExit(f"missing corpint path: {url}")
        corp_rows.append(corp_row(seq, title, url, prong))
        seq += 1
    if len(corp_rows) < 30:
        raise SystemExit(f"expected >=30 corpint rows, got {len(corp_rows)}")

    osint_rows: list[dict] = []
    for idx, (title, url, cluster, prong, level, skeptic) in enumerate(OSINT_SOURCES[:44], start=1):
        osint_rows.append(osint_row(idx, title, url, cluster, prong, level, skeptic))
    if len(osint_rows) != 44:
        raise SystemExit(f"expected 44 osint rows, got {len(osint_rows)}")

    manifest = {
        "tranche": "R7",
        "id_prefix": "AOS-R7",
        "corpint_target": 30,
        "osint_target": 44,
        "census": {"enabled": False},
        "rows": corp_rows + osint_rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(manifest['rows'])} rows)")


if __name__ == "__main__":
    main()
