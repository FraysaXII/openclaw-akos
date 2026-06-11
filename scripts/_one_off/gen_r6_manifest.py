#!/usr/bin/env python3
"""One-off generator for Automation OS R6 manifest (Research + IntelOps + radar)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/tranches/r6-manifest.json"
)
GITHUB_MAIN = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def ledger_url(path: str) -> str:
    """Repo-relative docs/ paths pass through; other paths use GitHub blob URLs."""
    if path.startswith("docs/") or path.startswith(".cursor/"):
        return path
    return GITHUB_MAIN + path.replace("\\", "/")


# Priority-ordered CORP-VAULT-RESEARCH + CORP-VAULT-INTEL (+ radar runbooks).
CORPINT_PATHS: list[tuple[str, str, str]] = [
    ("Research area README", "docs/references/hlk/v3.0/Research/README.md", "P4-RESEARCH"),
    ("Research area charter", "docs/references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md", "P4-RESEARCH"),
    ("Research lifecycle doctrine", "docs/references/hlk/v3.0/Research/canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md", "P4-RESEARCH"),
    ("Research vs Tech Lab rationale", "docs/references/hlk/v3.0/Research/canonicals/RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md", "P4-RESEARCH"),
    ("Methodology README", "docs/references/hlk/v3.0/Research/Methodology/README.md", "P4-RESEARCH"),
    ("Methodology discipline charter", "docs/references/hlk/v3.0/Research/Methodology/canonicals/METHODOLOGY_DISCIPLINE_CHARTER.md", "P4-RESEARCH"),
    ("Research prong lattice discipline", "docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_PRONG_LATTICE_DISCIPLINE.md", "P4-RESEARCH"),
    ("HxPESTAL intent tracking discipline", "docs/references/hlk/v3.0/Research/Methodology/canonicals/HXPESTAL_INTENT_TRACKING_DISCIPLINE.md", "P4-RESEARCH"),
    ("Research radar discipline", "docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_RADAR_DISCIPLINE.md", "P4-RESEARCH"),
    ("SOP research radar", "docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md", "P4-RESEARCH"),
    ("SOP research action", "docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_ACTION_001.md", "P4-RESEARCH"),
    ("SOP prong synthesis", "docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_PRONG_SYNTHESIS_001.md", "P4-RESEARCH"),
    ("SOP research outake handoff", "docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_OUTAKE_HANDOFF_001.md", "P4-RESEARCH"),
    ("SOP substrate audit cadence", "docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md", "P4-RESEARCH"),
    ("Substrate landscape doctrine", "docs/references/hlk/v3.0/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md", "P4-RESEARCH"),
    ("Derived recall discipline", "docs/references/hlk/v3.0/Research/Methodology/canonicals/DERIVED_RECALL_DISCIPLINE.md", "P4-RESEARCH"),
    ("HxPESTAL analysis pillar", "docs/references/hlk/v3.0/Research/Methodology/Pillars/HXPESTAL_ANALYSIS.md", "P4-RESEARCH"),
    ("PESTEL analysis pillar", "docs/references/hlk/v3.0/Research/Methodology/Pillars/PESTEL_ANALYSIS.md", "P4-RESEARCH"),
    ("Porter competitive analysis pillar", "docs/references/hlk/v3.0/Research/Methodology/Pillars/PORTER_COMPETITIVE_ANALYSIS.md", "P4-RESEARCH"),
    ("Methodology pillars README", "docs/references/hlk/v3.0/Research/Methodology/Pillars/README.md", "P4-RESEARCH"),
    ("Intelligence README", "docs/references/hlk/v3.0/Research/Intelligence/README.md", "P10-INTEL-OPS"),
    ("Intelligence discipline charter", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md", "P10-INTEL-OPS"),
    ("Counter-intelligence discipline", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/COUNTER_INTELLIGENCE_DISCIPLINE.md", "P10-INTEL-OPS"),
    ("GOI/POI stance doctrine", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/GOI_POI_STANCE_DOCTRINE.md", "P10-INTEL-OPS"),
    ("SOP IO elicitation discipline", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/SOP-IO_ELICITATION_DISCIPLINE_001.md", "P10-INTEL-OPS"),
    ("SOP counterparty baseline assessment", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md", "P10-INTEL-OPS"),
    ("SOP IO reliability grading", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/SOP-IO_RELIABILITY_GRADING_001.md", "P10-INTEL-OPS"),
    ("SOP IO intelligence report", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/SOP-IO_INTELLIGENCE_REPORT_001.md", "P10-INTEL-OPS"),
    ("SOP research engagement trigger", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/SOP-RESEARCH_ENGAGEMENT_TRIGGER_001.md", "P10-INTEL-OPS"),
    ("SOP regulator relationship", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/SOP-REGULATOR_RELATIONSHIP_001.md", "P10-INTEL-OPS"),
    ("GOI/POI register CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv", "P10-INTEL-OPS"),
    ("SOP GOI/POI register maintenance", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md", "P10-INTEL-OPS"),
    ("Research radar Pydantic SSOT", "akos/hlk_research_radar.py", "P4-RESEARCH"),
    ("Research ledger ops module", "akos/research_ledger_ops.py", "P4-RESEARCH"),
    ("validate_goipoi_register runbook", "scripts/validate_goipoi_register.py", "P10-INTEL-OPS"),
    ("Research-action cursor rule", ".cursor/rules/akos-research-action.mdc", "P4-RESEARCH"),
    ("Research-radar cursor rule", ".cursor/rules/akos-research-radar.mdc", "P4-RESEARCH"),
    ("Research-area cursor rule", ".cursor/rules/akos-research-area.mdc", "P4-RESEARCH"),
    ("Applied-research cursor rule", ".cursor/rules/akos-applied-research-discipline.mdc", "P4-RESEARCH"),
    ("research-action-craft skill", ".cursor/skills/research-action-craft/SKILL.md", "P4-RESEARCH"),
    ("research-radar-craft skill", ".cursor/skills/research-radar-craft/SKILL.md", "P4-RESEARCH"),
    ("applied-research-craft skill", ".cursor/skills/applied-research-craft/SKILL.md", "P4-RESEARCH"),
    ("HxPESTAL intent tracking template", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/hxpestel-intent-tracking-template.md", "P4-RESEARCH"),
    ("Prong synthesis template", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/prong-synthesis-template.md", "P4-RESEARCH"),
    ("Methodology cross-area wiring", "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/methodology-cross-area-wiring-2026-06-10.md", "P4-RESEARCH"),
    ("Research radar Stage B charter", "docs/wip/intelligence/research-radar-2026-05-29/charter-2026-05-29.md", "P4-RESEARCH"),
    ("Diagnosis discipline charter", "docs/references/hlk/v3.0/Research/Diagnosis/canonicals/DIAGNOSIS_DISCIPLINE_CHARTER.md", "P4-RESEARCH"),
    ("Validation discipline charter", "docs/references/hlk/v3.0/Research/Validation/canonicals/VALIDATION_DISCIPLINE_CHARTER.md", "P4-RESEARCH"),
    ("test_hlk_research_radar", "tests/test_hlk_research_radar.py", "P4-RESEARCH"),
    ("test_research_ledger_ops", "tests/test_research_ledger_ops.py", "P4-RESEARCH"),
    ("test_validate_research_radar", "tests/test_validate_research_radar.py", "P4-RESEARCH"),
    ("Source taxonomy", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md", "P4-RESEARCH"),
    ("Confidence levels", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md", "P4-RESEARCH"),
]

# OSINT-DX + OSINT-ACA — research pipeline DX + academic method bar.
OSINT_SOURCES: list[tuple[str, str, str, str, str, bool]] = [
    ("Jupyter documentation", "https://jupyter.org/documentation", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Observable notebooks", "https://observablehq.com/docs/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Deepnote docs", "https://deepnote.com/docs", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Hex notebooks", "https://learn.hex.tech/docs", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Zotero documentation", "https://www.zotero.org/support/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Semantic Scholar API", "https://api.semanticscholar.org/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("OpenAlex documentation", "https://docs.openalex.org/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Crossref REST API", "https://www.crossref.org/documentation/retrieve-metadata/rest-api/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Connected Papers", "https://www.connectedpapers.com/about", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Research Rabbit", "https://www.researchrabbit.ai/", "OSINT-DX", "P4-RESEARCH", "3.1", True),
    ("Litmaps", "https://www.litmaps.com/", "OSINT-DX", "P4-RESEARCH", "3.1", True),
    ("Scite.ai", "https://scite.ai/", "OSINT-DX", "P4-RESEARCH", "3.1", True),
    ("Elicit AI research assistant", "https://elicit.com/", "OSINT-DX", "P4-RESEARCH", "3.1", True),
    ("Consensus research app", "https://consensus.app/", "OSINT-DX", "P4-RESEARCH", "3.1", True),
    ("Hypothesis web annotation", "https://web.hypothes.is/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Readwise Reader", "https://readwise.io/read", "OSINT-DX", "P4-RESEARCH", "3.1", True),
    ("Obsidian knowledge base", "https://help.obsidian.md/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Logseq docs", "https://docs.logseq.com/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Open Knowledge Maps", "https://openknowledgemaps.org/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("CORE open access", "https://core.ac.uk/documentation/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("DOAJ directory", "https://doaj.org/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("arXiv API", "https://info.arxiv.org/help/api/index.html", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("Dimensions.ai research", "https://www.dimensions.ai/", "OSINT-DX", "P4-RESEARCH", "3.1", True),
    ("Lens.org scholarly search", "https://about.lens.org/", "OSINT-DX", "P4-RESEARCH", "4.1", False),
    ("PRISMA systematic review", "https://www.prisma-statement.org/", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Cochrane handbook", "https://training.cochrane.org/handbook", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Campbell collaboration methods", "https://www.campbellcollaboration.org/", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("GRADE working group", "https://www.gradeworkinggroup.org/", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Oxford CEBM levels", "https://www.cebm.ox.ac.uk/resources/levels-of-evidence", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("NIH research methods", "https://www.nih.gov/health-information/nih-clinical-research-trials-you", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Nature research methods", "https://www.nature.com/nature-research/intelligence", "OSINT-ACA", "P4-RESEARCH", "3.1", True),
    ("ACM research methods guide", "https://www.acm.org/publications/authors/research", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Evidence Based Medicine toolkit", "https://ebm-tools.knowledge Translation.ca/", "OSINT-ACA", "P4-RESEARCH", "4.1", False),
    ("Systematic review skeptic", "https://www.bmj.com/content/347/bmj.f5023", "OSINT-SKEP", "P4-RESEARCH", "2.1", True),
    ("AI literature review hype", "https://www.nature.com/articles/d41586-023-02596-6", "OSINT-SKEP", "P4-RESEARCH", "2.1", True),
    ("Predatory journal watch", "https://predatoryjournals.com/", "OSINT-SKEP", "P4-RESEARCH", "2.1", True),
    ("Citation cartels warning", "https://www.science.org/content/article/citation-cartels", "OSINT-SKEP", "P4-RESEARCH", "2.1", True),
    ("Research automation overclaim", "https://www.theguardian.com/technology/2023/mar/23/ai-tools-research-academic-papers", "OSINT-SKEP", "P4-RESEARCH", "2.1", True),
    ("OSINT framework", "https://osintframework.com/", "OSINT-DX", "P10-INTEL-OPS", "4.1", False),
    ("Bellingcat OSINT guide", "https://www.bellingcat.com/resources/how-tos/", "OSINT-DX", "P10-INTEL-OPS", "4.1", False),
    ("First Draft verification", "https://firstdraftnews.org/latest/", "OSINT-DX", "P10-INTEL-OPS", "4.1", False),
    ("Google Fact Check Tools", "https://toolbox.google.com/factcheck/explorer", "OSINT-DX", "P10-INTEL-OPS", "4.1", False),
    ("MISP threat intel", "https://www.misp-project.org/documentation/", "OSINT-DX", "P10-INTEL-OPS", "4.1", False),
    ("OpenCTI documentation", "https://docs.opencti.io/latest/", "OSINT-DX", "P10-INTEL-OPS", "4.1", False),
    ("Maltego OSINT", "https://docs.maltego.com/", "OSINT-DX", "P10-INTEL-OPS", "3.1", True),
    ("Recorded Future intel", "https://www.recordedfuture.com/", "OSINT-DX", "P10-INTEL-OPS", "3.1", True),
    ("Palantir Gotham docs", "https://www.palantir.com/platforms/gotham/", "OSINT-SKEP", "P10-INTEL-OPS", "2.1", True),
    ("Vendor intel platform skeptic", "https://www.theregister.com/2024/02/14/osint_platform_hype/", "OSINT-SKEP", "P10-INTEL-OPS", "2.1", True),
    ("FM 2-22.3 HUMINT reference", "https://irp.fas.org/doddir/army/fm2-22-3.pdf", "OSINT-ACA", "P10-INTEL-OPS", "4.1", False),
    ("NATO OSINT handbook", "https://www.nato.int/cps/en/natohq/topics_68368.htm", "OSINT-ACA", "P10-INTEL-OPS", "4.1", False),
]


def corp_row(seq: int, title: str, url: str, prong: str) -> dict:
    cluster = "corp_vault_intel" if prong == "P10-INTEL-OPS" else "corp_vault_research"
    return {
        "source_id": f"SRC-AOS-R6I-{seq:03d}",
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
            f"R6 Research/IntelOps/radar vault; impacts: TECH_AUTOMATION_REGISTRY; "
            f"ICS:High; prong={prong}"
        ),
    }


def osint_row(seq: int, title: str, url: str, cluster: str, prong: str, level: str, skeptic: bool) -> dict:
    notes = "R6 OSINT; ICS:Load-bearing;"
    if skeptic:
        notes += " CON: vendor-hype or paywall;"
    return {
        "source_id": f"SRC-AOS-R6E-{seq:03d}",
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
        corp_rows.append(corp_row(seq, title, ledger_url(url), prong))
        seq += 1
    if len(corp_rows) < 32:
        raise SystemExit(f"expected >=32 corpint candidates, got {len(corp_rows)}")

    osint_rows: list[dict] = []
    for idx, (title, url, cluster, prong, level, skeptic) in enumerate(OSINT_SOURCES[:44], start=1):
        osint_rows.append(osint_row(idx, title, url, cluster, prong, level, skeptic))
    if len(osint_rows) != 44:
        raise SystemExit(f"expected 44 osint rows, got {len(osint_rows)}")

    manifest = {
        "tranche": "R6",
        "id_prefix": "AOS-R6",
        "corpint_target": 32,
        "osint_target": 44,
        "census": {"enabled": False},
        "rows": corp_rows + osint_rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(manifest['rows'])} rows)")


if __name__ == "__main__":
    main()
