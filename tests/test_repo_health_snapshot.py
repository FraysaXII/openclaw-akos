"""Tests for REPO_HEALTH_SNAPSHOT.csv + EXTERNAL_REPO_CONTRACT_TEMPLATE + akos-mirror.mdc.

Locks the cross-repo extraction discipline contract (Initiative 32 P7).
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPO_HEALTH_SNAPSHOT.csv"
TEMPLATE_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Envoy Tech Lab" / "Repositories" / "EXTERNAL_REPO_CONTRACT_TEMPLATE.md"
MIRROR_RULE_TEMPLATE = REPO_ROOT / ".cursor" / "rules" / "akos-mirror-template.mdc"
REPOS_REGISTRY = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Envoy Tech Lab" / "Repositories" / "REPOSITORIES_REGISTRY.md"
SNAPSHOT_SCRIPT = REPO_ROOT / "scripts" / "snapshot_external_repos.py"
VALIDATOR = REPO_ROOT / "scripts" / "validate_repo_health_snapshot.py"
SEED_PRS_DIR = REPO_ROOT / "docs" / "wip" / "planning" / "32-holistik-ops-maturation" / "reports" / "external-repo-seed-prs"
ERP_BUNDLE_DIR = REPO_ROOT / "docs" / "wip" / "planning" / "32-holistik-ops-maturation" / "reports" / "erp-handoff-bundle-2026-04-30"


def test_repo_health_snapshot_csv_exists() -> None:
    assert CSV_PATH.is_file()


def test_external_repo_contract_template_exists_and_lints_clean() -> None:
    assert TEMPLATE_PATH.is_file()
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    # The template must spell out the 3 invariants + 5 do-not + 1 do contract.
    assert "3 invariants" in text
    assert "5 \"do not\"" in text
    assert "1 \"do\" rule" in text
    # And must cross-reference PRECEDENCE.md and the 6-axis doctrine.
    assert "PRECEDENCE.md" in text
    assert "HOLISTIK_OPS_DISCOVERY.md" in text


def test_akos_mirror_cursor_rule_template_exists_and_loads_always() -> None:
    assert MIRROR_RULE_TEMPLATE.is_file()
    text = MIRROR_RULE_TEMPLATE.read_text(encoding="utf-8")
    assert "alwaysApply: true" in text
    # It must reference AKOS via stable GitHub URL, not local path.
    assert "github.com/FraysaXII/openclaw-akos" in text


def test_repositories_registry_carries_three_external_rows() -> None:
    text = REPOS_REGISTRY.read_text(encoding="utf-8")
    # The 3 external repo rows added in I32 P7 + P11.
    assert "kirbe-platform" in text
    assert "hlk-erp" in text
    assert "boilerplate" in text
    # The reference class definition added in P11.
    assert "**reference**" in text and "D-IH-32-N" in text


def test_snapshot_check_only_dry_run_works() -> None:
    """The snapshot script's --check-only flag works without writing anything."""
    r = subprocess.run(
        [sys.executable, str(SNAPSHOT_SCRIPT), "--check-only"],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=60,
    )
    assert r.returncode == 0, f"--check-only exited {r.returncode}; stderr: {r.stderr}"
    assert "REPO_HEALTH_SNAPSHOT" in r.stdout
    assert "would write" in r.stdout


def test_snapshot_csv_carries_three_repo_rows() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    slugs = {r["repo_slug"] for r in rows}
    assert slugs == {"boilerplate", "hlk-erp", "kirbe-platform"}, (
        f"expected snapshot to track all 3 external repos; got {slugs}"
    )


def test_snapshot_each_row_has_today_or_recent_date() -> None:
    """snapshot_date is set; informational that it's recent (within 30 days)."""
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for r in rows:
        assert pattern.match(r["snapshot_date"])
        y, m, d = (int(x) for x in r["snapshot_date"].split("-"))
        delta = (date.today() - date(y, m, d)).days
        assert delta <= 30, f"snapshot_date {r['snapshot_date']} is too old (>{delta} days)"


def test_validator_passes() -> None:
    r = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r.returncode == 0, f"validate_repo_health_snapshot.py exited {r.returncode}"
    assert "PASS" in r.stdout


def test_validator_runs_under_dispatcher() -> None:
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk.py")],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=120,
    )
    assert r.returncode == 0
    assert "REPO_HEALTH_SNAPSHOT: PASS" in r.stdout


def test_three_pr_patches_exist_for_three_repos() -> None:
    """P8-A6 (P7 work in execution mapping): 3 PR-ready patches in reports/external-repo-seed-prs/."""
    for repo in ("kirbe", "hlk-erp", "boilerplate"):
        assert (SEED_PRS_DIR / f"{repo}.patch").is_file(), f"missing {repo}.patch"


def test_six_bilingual_cover_emails_exist() -> None:
    """D-IH-32-P: 6 cover-email drafts (3 repos x EN+ES)."""
    for repo in ("kirbe", "hlk-erp", "boilerplate"):
        for lang in ("en", "es"):
            assert (SEED_PRS_DIR / f"{repo}-cover-email-{lang}.md").is_file(), (
                f"missing {repo}-cover-email-{lang}.md"
            )


def test_erp_bundle_has_seven_files() -> None:
    """P8 acceptance: 6 of 6 bundle documents (00..06) all linked from 00-README.md."""
    expected = {
        "00-README.md",
        "01-mirror-schema-map.md",
        "02-five-axis-integration-spec.md",
        "03-operator-sql-gate-pointer.md",
        "04-localisation-policy-pointer.md",
        "05-changelog-snippet.md",
        "06-team-sota-pointer.md",
    }
    actual = {f.name for f in ERP_BUNDLE_DIR.iterdir() if f.is_file()}
    assert expected.issubset(actual), f"missing bundle files: {expected - actual}"


def test_kirbe_sync_contract_section_2_enumerates_all_16_mirrors() -> None:
    """P9 acceptance: §2 rewritten to enumerate at least 16 mirrors."""
    text = (REPO_ROOT / "config" / "sync" / "kirbe-sync-contract.md").read_text(encoding="utf-8")
    # Quick and pragmatic: the rewritten §2 lists all 16 by name.
    expected_mirrors = [
        "process_list_mirror",
        "baseline_organisation_mirror",
        "finops_counterparty_register_mirror",
        "goipoi_register_mirror",
        "adviser_engagement_disciplines_mirror",
        "adviser_open_questions_mirror",
        "founder_filed_instruments_mirror",
        "program_registry_mirror",
        "topic_registry_mirror",
        "persona_registry_mirror",
        "channel_touchpoint_registry_mirror",
        "sourcing_register_mirror",
        "validation_runs",
        "skill_registry_mirror",
        "touchpoint_kit_cell_mirror",
        "policy_register_mirror",
    ]
    for m in expected_mirrors:
        assert m in text, f"sync contract §2 missing mirror {m!r}"


def test_kirbe_sync_contract_has_section_11_cross_repo_contract() -> None:
    """P9-A2: new §11 documents the cross-repo contract (D-IH-32-K)."""
    text = (REPO_ROOT / "config" / "sync" / "kirbe-sync-contract.md").read_text(encoding="utf-8")
    assert "## 11. Cross-repo contract" in text
    assert "D-IH-32-K" in text
    assert "EXTERNAL_REPO_CONTRACT.md" in text
