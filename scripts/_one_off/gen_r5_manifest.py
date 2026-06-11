#!/usr/bin/env python3
"""One-off generator for Automation OS R5 manifest (People + Quality Fabric + regression)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/tranches/r5-manifest.json"
)
GITHUB_MAIN = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def ledger_url(path: str) -> str:
    """Repo-relative docs/ paths pass through; other paths use GitHub blob URLs."""
    if path.startswith("docs/"):
        return path
    return GITHUB_MAIN + path.replace("\\", "/")

# Priority-ordered CORP-VAULT-PEOPLE (+ QF specialty runbooks/rules).
CORPINT_PATHS: list[tuple[str, str, str]] = [
    ("Holistika Quality Fabric", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md", "P5-PEOPLE"),
    ("Holistika organising doctrine", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md", "P5-PEOPLE"),
    ("Holistika agentic doctrine", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md", "P5-PEOPLE"),
    ("Holistika stakeholder lenses", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_STAKEHOLDER_LENSES.md", "P5-PEOPLE"),
    ("UAT discipline", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md", "P5-PEOPLE"),
    ("Synthesis before tranche discipline", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md", "P5-PEOPLE"),
    ("Intent-ranked regression discipline", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTENT_RANKED_REGRESSION_DISCIPLINE.md", "P5-PEOPLE"),
    ("Index integrity discipline", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md", "P5-PEOPLE"),
    ("PASS-WITH-FOLLOWUP governance", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md", "P5-PEOPLE"),
    ("Collaborator share doctrine", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md", "P5-PEOPLE"),
    ("Area governance discipline", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md", "P5-PEOPLE"),
    ("Research head discipline", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md", "P5-PEOPLE"),
    ("People design pattern library", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md", "P5-PEOPLE"),
    ("UX discipline (QF specialty)", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/UX Designer/canonicals/UX_DISCIPLINE.md", "P5-PEOPLE"),
    ("SOP People area governance", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AREA_GOVERNANCE_001.md", "P5-PEOPLE"),
    ("SOP People index integrity", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_INDEX_INTEGRITY_001.md", "P5-PEOPLE"),
    ("SOP People PWF governance", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_PWF_GOVERNANCE_001.md", "P5-PEOPLE"),
    ("SOP People collaborator share", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_COLLABORATOR_SHARE_001.md", "P5-PEOPLE"),
    ("SOP People UAT governance", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_UAT_GOVERNANCE_001.md", "P5-PEOPLE"),
    ("SOP People inter-wave regression", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md", "P5-PEOPLE"),
    ("SOP People synthesis before tranche", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001.md", "P5-PEOPLE"),
    ("SOP People intent-ranked regression", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_INTENT_RANKED_REGRESSION_001.md", "P5-PEOPLE"),
    ("SOP meta process management", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md", "P6-COMPLIANCE"),
    ("Audience registry", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv", "P5-PEOPLE"),
    ("People design pattern registry", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv", "P5-PEOPLE"),
    ("UAT closure template", "docs/wip/planning/_templates/uat-closure-template.md", "P5-PEOPLE"),
    ("Quality Fabric cursor rule", ".cursor/rules/akos-quality-fabric.mdc", "P5-PEOPLE"),
    ("Inter-wave regression cursor rule", ".cursor/rules/akos-inter-wave-regression.mdc", "P5-PEOPLE"),
    ("Index integrity cursor rule", ".cursor/rules/akos-index-integrity.mdc", "P5-PEOPLE"),
    ("validate_uat_report runbook", "scripts/validate_uat_report.py", "P5-PEOPLE"),
    ("validate_synthesis_before_tranche runbook", "scripts/validate_synthesis_before_tranche.py", "P5-PEOPLE"),
    ("intent_ranked_regression runbook", "scripts/intent_ranked_regression.py", "P5-PEOPLE"),
    ("validate_index_freshness runbook", "scripts/validate_index_freshness.py", "P5-PEOPLE"),
    ("inter_wave_regression_sweep runbook", "scripts/inter_wave_regression_sweep.py", "P5-PEOPLE"),
    # Overflow vault (beyond manifest cap; available for dedup backfill if needed)
    ("Baseline organisation CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv", "P6-COMPLIANCE"),
    ("Access levels", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/access_levels.md", "P6-COMPLIANCE"),
    ("Confidence levels", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md", "P6-COMPLIANCE"),
    ("Source taxonomy", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md", "P6-COMPLIANCE"),
    ("Ethical agentic boundaries", "docs/references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md", "P5-PEOPLE"),
    ("SOP People cross-area breakthrough", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md", "P5-PEOPLE"),
    ("Channel touchpoint registry", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv", "P5-PEOPLE"),
    ("Component primitive library", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COMPONENT_PRIMITIVE_LIBRARY.md", "P5-PEOPLE"),
    ("Output type library", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/OUTPUT_TYPE_LIBRARY.md", "P5-PEOPLE"),
    ("Holistika capability doctrine", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_CAPABILITY_DOCTRINE.md", "P5-PEOPLE"),
    ("UAT discipline cursor rule", ".cursor/rules/akos-uat-discipline.mdc", "P5-PEOPLE"),
    ("Synthesis-before-tranche cursor rule", ".cursor/rules/akos-synthesis-before-tranche.mdc", "P5-PEOPLE"),
    ("Intent-ranked regression cursor rule", ".cursor/rules/akos-intent-ranked-regression.mdc", "P5-PEOPLE"),
    ("Inline ratification cursor rule", ".cursor/rules/akos-inline-ratification.mdc", "P5-PEOPLE"),
    ("Collaborator share cursor rule", ".cursor/rules/akos-collaborator-share.mdc", "P5-PEOPLE"),
    ("PWF governance cursor rule", ".cursor/rules/akos-pwf-governance.mdc", "P5-PEOPLE"),
    ("Deploy health cursor rule", ".cursor/rules/akos-deploy-health.mdc", "P5-PEOPLE"),
    ("validate_collaborator_share runbook", "scripts/validate_collaborator_share.py", "P5-PEOPLE"),
    ("validate_pwf_governance runbook", "scripts/validate_pwf_governance.py", "P5-PEOPLE"),
    ("quality-fabric-craft skill", ".cursor/skills/quality-fabric-craft/SKILL.md", "P5-PEOPLE"),
    ("uat-discipline-craft skill", ".cursor/skills/uat-discipline-craft/SKILL.md", "P5-PEOPLE"),
    ("inter-wave-regression-craft skill", ".cursor/skills/inter-wave-regression-craft/SKILL.md", "P5-PEOPLE"),
    ("index-integrity-craft skill", ".cursor/skills/index-integrity-craft/SKILL.md", "P5-PEOPLE"),
    ("SSOT canonical-touch rule", ".cursor/rules/akos-ssot-canonical-touch.mdc", "P5-PEOPLE"),
]

# OSINT-EVAL + OSINT-SKEP — QA/UAT/evaluation + skeptic voices (charter R5 pairing).
OSINT_SOURCES: list[tuple[str, str, str, str, str, bool]] = [
    ("World Quality Report 2024", "https://www.capgemini.com/insights/research-library/world-quality-report/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Standish CHAOS Report", "https://www.standishgroup.com/sample_research_files/CHAOSReport2020.pdf", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("ISTQB foundation syllabus", "https://www.istqb.org/certifications/certified-tester-foundation-level", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("ISO/IEC 25010 quality model", "https://iso25000.com/index.php/en/iso-25000-standards/iso-25010", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Google testing blog", "https://testing.googleblog.com/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Playwright docs", "https://playwright.dev/docs/intro", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Cypress best practices", "https://docs.cypress.io/guides/references/best-practices", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Selenium documentation", "https://www.selenium.dev/documentation/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("WCAG 2.2 guidelines", "https://www.w3.org/WAI/WCAG22/quickref/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("axe accessibility engine", "https://www.deque.com/axe/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Google Lighthouse", "https://developer.chrome.com/docs/lighthouse/overview/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Nielsen usability heuristics", "https://www.nngroup.com/articles/ten-usability-heuristics/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Microsoft testing guidance", "https://learn.microsoft.com/en-us/dotnet/core/testing/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("AWS testing best practices", "https://docs.aws.amazon.com/wellarchitected/latest/framework/testing.html", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("SonarQube quality gates", "https://docs.sonarsource.com/sonarqube/latest/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Mutation testing Stryker", "https://stryker-mutator.io/docs/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Property-based Hypothesis", "https://hypothesis.readthedocs.io/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Gremlin chaos engineering", "https://www.gremlin.com/community/tutorials/what-is-chaos-engineering/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("OpenTelemetry testing", "https://opentelemetry.io/docs/concepts/signals/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("GitHub required status checks", "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Codecov coverage gates", "https://docs.codecov.com/docs/codecov-yaml", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Shift-left testing", "https://www.atlassian.com/continuous-delivery/software-testing/shift-left-testing", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Test pyramid Cohn", "https://martinfowler.com/bliki/TestPyramid.html", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Continuous testing DevOps", "https://www.guru99.com/continuous-testing.html", "OSINT-EVAL", "P5-PEOPLE", "3.1", True),
    ("CMMI appraisal", "https://cmmiinstitute.com/learning/appraisals", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("ISO 9001 quality management", "https://www.iso.org/iso-9001-quality-management.html", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Gartner MQ testing tools", "https://www.gartner.com/reviews/market/software-test-automation", "OSINT-EVAL", "P5-PEOPLE", "3.1", True),
    ("Forrester QA automation wave", "https://www.forrester.com/blogs/category/quality-assurance/", "OSINT-EVAL", "P5-PEOPLE", "3.1", True),
    ("Appium mobile testing", "https://appium.io/docs/en/latest/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("BrowserStack visual testing", "https://www.browserstack.com/docs/percy/overview/what-is-percy", "OSINT-EVAL", "P5-PEOPLE", "4.1", True),
    ("Percy visual regression", "https://docs.percy.io/docs/visual-regression-testing", "OSINT-EVAL", "P5-PEOPLE", "4.1", True),
    ("TestRail UAT management", "https://www.testrail.com/user-acceptance-testing/", "OSINT-EVAL", "P5-PEOPLE", "3.1", True),
    ("UAT documentation guide", "https://www.softwaretestinghelp.com/user-acceptance-testing-uat/", "OSINT-EVAL", "P5-PEOPLE", "3.1", True),
    ("UAT cargo cult skeptic", "https://www.jamesmarcusrogers.com/post/uat-is-dead", "OSINT-SKEP", "P5-PEOPLE", "2.1", True),
    ("QA automation overpromise", "https://www.theregister.com/2024/03/15/ai_testing_hype/", "OSINT-SKEP", "P5-PEOPLE", "2.1", True),
    ("100% coverage fallacy", "https://www.infoq.com/articles/code-coverage-misuse/", "OSINT-SKEP", "P5-PEOPLE", "2.1", True),
    ("Checklist compliance theater", "https://www.satisfice.com/blog/archives/856", "OSINT-SKEP", "P5-PEOPLE", "2.1", True),
    ("Agile testing without UAT", "https://www.agilealliance.org/glossary/user-acceptance-testing/", "OSINT-SKEP", "P5-PEOPLE", "3.1", True),
    ("Gartner AI testing hype", "https://www.gartner.com/en/articles/ai-augmented-software-testing", "OSINT-SKEP", "P5-PEOPLE", "3.1", True),
    ("Visual regression false positives", "https://www.chromatic.com/docs/visual-regression-testing/", "OSINT-SKEP", "P5-PEOPLE", "3.1", True),
    ("Accessibility audit limits", "https://www.w3.org/WAI/test-evaluate/preliminary/", "OSINT-SKEP", "P5-PEOPLE", "4.1", False),
    ("Shift-left skeptic", "https://www.thoughtworks.com/insights/blog/shift-left-doesnt-mean-no-ops", "OSINT-SKEP", "P5-PEOPLE", "2.1", True),
    ("Quality gate bureaucracy", "https://queue.acm.org/detail.cfm?id=3454122", "OSINT-SKEP", "P5-PEOPLE", "4.1", True),
    ("Regression suite decay", "https://www.testingexcellence.com/regression-test-suite-maintenance/", "OSINT-SKEP", "P5-PEOPLE", "3.1", True),
    ("Evals for LLM apps", "https://docs.smith.langchain.com/evaluation", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Langfuse evaluations", "https://langfuse.com/docs/scores/model-based-evals", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("Ragas LLM evaluation", "https://docs.ragas.io/en/stable/", "OSINT-EVAL", "P5-PEOPLE", "4.1", False),
    ("DeepEval framework", "https://docs.confident-ai.com/", "OSINT-EVAL", "P5-PEOPLE", "4.1", True),
    ("Human-in-the-loop eval", "https://humanloop.com/docs/evaluation", "OSINT-EVAL", "P5-PEOPLE", "3.1", True),
    ("Model eval skeptic", "https://www.ben-evans.com/benedictevans/2024/2/12/generative-ai-evaluation", "OSINT-SKEP", "P5-PEOPLE", "2.1", True),
]


def corp_row(seq: int, title: str, url: str, prong: str) -> dict:
    return {
        "source_id": f"SRC-AOS-R5I-{seq:03d}",
        "prong": prong,
        "topic_cluster": "corp_vault_people",
        "source_title_or_owner": title,
        "url": url,
        "format": "internal_canonical",
        "source_category": "CORPINT",
        "source_level": "5.1",
        "holistika_reliability_score": "5",
        "external_perceived_credibility_score": "2",
        "control_confidence_level": "Safe",
        "decision_use": "def-vault-harvest",
        "notes": (
            f"R5 People/QF/regression vault; impacts: TECH_AUTOMATION_REGISTRY; "
            f"ICS:High; prong={prong}"
        ),
    }


def osint_row(seq: int, title: str, url: str, cluster: str, prong: str, level: str, skeptic: bool) -> dict:
    notes = "R5 OSINT; ICS:Load-bearing;"
    if skeptic:
        notes += " CON: vendor-hype or paywall;"
    return {
        "source_id": f"SRC-AOS-R5E-{seq:03d}",
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
        "tranche": "R5",
        "id_prefix": "AOS-R5",
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
