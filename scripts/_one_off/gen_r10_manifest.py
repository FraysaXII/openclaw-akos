#!/usr/bin/env python3
"""One-off generator for Automation OS R10 manifest (verify profiles + CI/CD automation OS)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/tranches/r10-manifest.json"
)
GITHUB_MAIN = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def ledger_url(path: str) -> str:
    """Repo-relative docs/ paths pass through; other paths use GitHub blob URLs."""
    if path.startswith("docs/"):
        return path
    return GITHUB_MAIN + path.replace(chr(92), "/")


# Priority-ordered CORP-RUNTIME + CORP-VAULT-TECH (verification-profiles harvest).
CORPINT_PATHS: list[tuple[str, str, str]] = [
    ("Verification profiles SSOT", "config/verification-profiles.json", "P1-TECH"),
    ("verify.py orchestrator", "scripts/verify.py", "P1-TECH"),
    ("release-gate runbook", "scripts/release-gate.py", "P1-TECH"),
    ("check-drift runbook", "scripts/check-drift.py", "P1-TECH"),
    ("test.py runner", "scripts/test.py", "P1-TECH"),
    ("browser-smoke runbook", "scripts/browser-smoke.py", "P1-TECH"),
    ("SOP CICD baseline", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-CICD_BASELINE_001.md", "P1-TECH"),
    ("TECHOPS discipline", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/TECHOPS_DISCIPLINE.md", "P1-TECH"),
    ("SOP HLK tooling standards", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-HLK_TOOLING_STANDARDS_001.md", "P1-TECH"),
    ("SOP tech system reliability", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-TECH_SYSTEM_RELIABILITY_001.md", "P1-TECH"),
    ("SOP tech dataops quality", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-TECH_DATAOPS_QUALITY_001.md", "P1-TECH"),
    ("SOP release taxonomy", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-RELEASE_TAXONOMY_001.md", "P1-TECH"),
    ("SOP MCP server definition", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-MCP_SERVER_DEFINITION.md", "P1-TECH"),
    ("Developer checklist", "docs/DEVELOPER_CHECKLIST.md", "P3-OPS"),
    ("DEV verification reference", "docs/guides/DEV_VERIFICATION_REFERENCE.md", "P3-OPS"),
    ("Understanding verification guide", "docs/guides/understanding_verification.md", "P3-OPS"),
    ("validate_cicd_baseline runbook", "scripts/validate_cicd_baseline.py", "P1-TECH"),
    ("validate_playwright_baseline runbook", "scripts/validate_playwright_baseline.py", "P1-TECH"),
    ("validate_sentry_release_format runbook", "scripts/validate_sentry_release_format.py", "P1-TECH"),
    ("akos cicd_baseline module", "akos/cicd_baseline.py", "P1-TECH"),
    ("akos playwright_baseline module", "akos/playwright_baseline.py", "P1-TECH"),
    ("CI baseline workflow template", "docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/github-workflows/ci-baseline.yml.tmpl", "P1-TECH"),
    ("Render baseline template", "docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/render/render-baseline.yaml.tmpl", "P1-TECH"),
    ("Deploy health cursor rule", ".cursor/rules/akos-deploy-health.mdc", "P3-OPS"),
    ("AGENTS.md workspace index", "AGENTS.md", "P3-OPS"),
]

# OSINT-CICD-OS â€” CI/CD automation OS depth.
OSINT_SOURCES: list[tuple[str, str, str, str, str, bool]] = [
    ("GitHub Actions docs", "https://docs.github.com/en/actions", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("GitLab CI/CD", "https://docs.gitlab.com/ee/ci/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("CircleCI docs", "https://circleci.com/docs/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Jenkins handbook", "https://www.jenkins.io/doc/book/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Azure DevOps pipelines", "https://learn.microsoft.com/en-us/azure/devops/pipelines/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Buildkite pipelines", "https://buildkite.com/docs/pipelines", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Tekton pipelines", "https://tekton.dev/docs/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Argo Workflows", "https://argo-workflows.readthedocs.io/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Dagger CI engine", "https://docs.dagger.io/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Earthly reproducible builds", "https://docs.earthly.dev/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Bazel build system", "https://bazel.build/start", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Nx monorepo CI", "https://nx.dev/concepts/ci", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Turborepo CI caching", "https://turbo.build/repo/docs/core-concepts/caching", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Vercel deployment docs", "https://vercel.com/docs/deployments/overview", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Render deploy docs", "https://render.com/docs/deploys", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Google SRE workbook", "https://sre.google/workbook/", "OSINT-CICD-OS", "P3-OPS", "4.1", False),
    ("Accelerate DORA metrics", "https://dora.dev/", "OSINT-CICD-OS", "P3-OPS", "4.1", False),
    ("Platform engineering guide", "https://internaldeveloperplatform.org/", "OSINT-CICD-OS", "P3-OPS", "4.1", False),
    ("Backstage IDP", "https://backstage.io/docs/overview/what-is-backstage/", "OSINT-CICD-OS", "P3-OPS", "4.1", False),
    ("Testcontainers CI", "https://testcontainers.com/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Playwright CI guide", "https://playwright.dev/docs/ci", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Semgrep SAST", "https://semgrep.dev/docs/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Dependabot security", "https://docs.github.com/en/code-security/dependabot", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Snyk container scanning", "https://docs.snyk.io/scan-with-snyk/snyk-container", "OSINT-CICD-OS", "P1-TECH", "3.1", True),
    ("CI/CD tool sprawl skeptic", "https://www.theregister.com/2023/05/09/platform_engineering/", "OSINT-SKEP", "P3-OPS", "2.1", True),
    ("DevOps silver bullet critique", "https://martinfowler.com/bliki/ContinuousDelivery.html", "OSINT-SKEP", "P1-TECH", "4.1", False),
    ("Pipeline complexity warning", "https://queue.acm.org/detail.cfm?id=3454122", "OSINT-SKEP", "P1-TECH", "4.1", True),
    ("Flaky test epidemic", "https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html", "OSINT-SKEP", "P1-TECH", "4.1", True),
    ("Shift-left overreach", "https://www.thoughtworks.com/insights/blog/shift-left-doesnt-mean-no-ops", "OSINT-SKEP", "P3-OPS", "2.1", True),
    ("GitHub Actions marketplace risk", "https://www.stepsecurity.io/blog/github-actions-security-best-practices", "OSINT-SKEP", "P1-TECH", "3.1", True),
    ("Codecov supply chain incident", "https://about.codecov.io/security-update/", "OSINT-SKEP", "P1-TECH", "2.1", True),
    ("SonarQube quality gates", "https://docs.sonarsource.com/sonarqube/latest/user-guide/quality-gates/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("CodeClimate maintainability", "https://docs.codeclimate.com/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Renovate dependency updates", "https://docs.renovatebot.com/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Changesets monorepo releases", "https://github.com/changesets/changesets", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Semantic release", "https://semantic-release.gitbook.io/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Conventional commits", "https://www.conventionalcommits.org/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Trunk-based development", "https://trunkbaseddevelopment.com/", "OSINT-CICD-OS", "P3-OPS", "4.1", False),
    ("Feature flags LaunchDarkly", "https://docs.launchdarkly.com/home/getting-started", "OSINT-CICD-OS", "P3-OPS", "3.1", True),
    ("Canary deployments", "https://martinfowler.com/bliki/CanaryRelease.html", "OSINT-CICD-OS", "P3-OPS", "4.1", False),
    ("Blue-green deployments", "https://martinfowler.com/bliki/BlueGreenDeployment.html", "OSINT-CICD-OS", "P3-OPS", "4.1", False),
    ("Progressive delivery", "https://www.progressivedelivery.io/", "OSINT-CICD-OS", "P3-OPS", "4.1", False),
    ("Observability-driven CI", "https://opentelemetry.io/docs/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Sentry release health", "https://docs.sentry.io/product/releases/health/", "OSINT-CICD-OS", "P1-TECH", "4.1", False),
    ("Datadog CI visibility", "https://docs.datadoghq.com/continuous_integration/", "OSINT-CICD-OS", "P1-TECH", "3.1", True),
    ("Harness CI platform", "https://developer.harness.io/docs/continuous-integration", "OSINT-CICD-OS", "P1-TECH", "3.1", True),
    ("CI vendor lock-in warning", "https://www.infoq.com/articles/ci-cd-vendor-lock-in/", "OSINT-SKEP", "P1-TECH", "2.1", True),
]


def corp_row(seq: int, title: str, url: str, prong: str) -> dict:
    cluster = "corp_runtime" if url.startswith(("scripts/", "config/", "akos/")) else "corp_vault_tech"
    if prong == "P3-OPS" and url.startswith("docs/"):
        cluster = "corp_vault_ops"
    return {
        "source_id": f"SRC-AOS-R10I-{seq:03d}",
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
            f"R10 verify/CI automation OS; impacts: TECH_AUTOMATION_REGISTRY; "
            f"ICS:Load-bearing; prong={prong}"
        ),
    }


def osint_row(seq: int, title: str, url: str, cluster: str, prong: str, level: str, skeptic: bool) -> dict:
    notes = "R10 OSINT; ICS:Load-bearing;"
    if skeptic:
        notes += " CON: vendor-hype or paywall;"
    return {
        "source_id": f"SRC-AOS-R10E-{seq:03d}",
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
    if len(corp_rows) < 25:
        raise SystemExit(f"expected >=25 corpint rows, got {len(corp_rows)}")

    osint_rows: list[dict] = []
    for idx, (title, url, cluster, prong, level, skeptic) in enumerate(OSINT_SOURCES, start=1):
        osint_rows.append(osint_row(idx, title, url, cluster, prong, level, skeptic))
    if len(osint_rows) < 46:
        raise SystemExit(f"expected >=46 osint rows, got {len(osint_rows)}")

    manifest = {
        "tranche": "R10",
        "id_prefix": "AOS-R10",
        "corpint_target": 25,
        "osint_target": 46,
        "census": {"enabled": False},
        "rows": corp_rows + osint_rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(manifest['rows'])} rows)")


if __name__ == "__main__":
    main()
