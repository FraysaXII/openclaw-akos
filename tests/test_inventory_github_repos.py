"""Tests for scripts/inventory_github_repos.py + akos.hlk_repository_registry_csv
(I86 Wave H; D-IH-86-AF runbook + D-IH-86-AD schema extension).

Covers:
- JSON parsing of `gh repo list … --json …` output (positive + edge cases).
- Diff computation against a fixture REPOSITORY_REGISTRY.csv.
- Pydantic round-trip of the 29-column schema (existing rows + new rows).
- Drift report rendering shape (sections + counts).
- Subcommand routing (sweep / classify / audit).
- --dry-run flag prevents writes.
- classify subcommand validates app_class via Pydantic before write.

All tests grouped under @pytest.mark.unit (the default lane in scripts/test.py).
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_repository_registry_csv import (  # noqa: E402
    REPOSITORY_REGISTRY_FIELDNAMES,
    VALID_APP_CLASS,
    VALID_GITHUB_VISIBILITY,
    VALID_GOVERNANCE_STATUS,
    RepositoryRegistryRow,
)
from akos.process import CommandResult  # noqa: E402

# Importing the runbook module pulls in its CLI argparse + subcommand registry.
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import inventory_github_repos as ig  # noqa: E402


pytestmark = pytest.mark.unit


# ---------- fixtures ----------

SAMPLE_GH_JSON = json.dumps(
    [
        {
            "name": "openclaw-akos",
            "url": "https://github.com/FraysaXII/openclaw-akos",
            "visibility": "PUBLIC",
            "isArchived": False,
            "isFork": False,
            "primaryLanguage": {"name": "Python"},
            "createdAt": "2024-01-01T00:00:00Z",
            "pushedAt": "2026-05-19T15:00:00Z",
            "repositoryTopics": [{"name": "hlk"}, {"name": "akos"}],
        },
        {
            "name": "visiongen",
            "url": "https://github.com/FraysaXII/visiongen",
            "visibility": "PUBLIC",
            "isArchived": False,
            "isFork": False,
            "primaryLanguage": {"name": "Python"},
            "createdAt": "2025-06-01T00:00:00Z",
            "pushedAt": "2025-06-30T12:00:00Z",
            "repositoryTopics": [],
        },
        {
            "name": "supabase",
            "url": "https://github.com/FraysaXII/supabase",
            "visibility": "PUBLIC",
            "isArchived": False,
            "isFork": True,
            "primaryLanguage": {"name": "TypeScript"},
            "createdAt": "2023-01-01T00:00:00Z",
            "pushedAt": "2024-05-08T08:00:00Z",
            "repositoryTopics": [],
        },
    ]
)


SAMPLE_REGISTRY_ROW = {
    "repo_slug": "openclaw-akos",
    "github_url": "https://github.com/FraysaXII/openclaw-akos",
    "class": "platform",
    "primary_owner_role": "AI Engineer",
    "topic_ids": "",
    "vault_doc_root": "",
    "api_spec_pointer": "—",
    "api_topic_id": "—",
    "lifecycle_status": "active",
    "notes": "",
    "consumes_compliance_types": "no",
    "consumes_mirrors": "",
    "local_path": "",
    "last_review_at": "",
    "last_review_by": "",
    "last_review_decision_id": "",
    "methodology_version_at_review": "",
    "app_class": "",
    "metadata_tags": "",
    "github_topics": "",
    "github_visibility": "",
    "primary_language": "",
    "created_at": "",
    "pushed_at": "",
    "last_inventory_at": "",
    "governance_status": "",
    "related_initiative_ids": "",
    "codeowners_present": "",
    "branch_protection_enabled": "",
}


# ---------- parse_gh_repo_list ----------

def test_parse_gh_repo_list_happy_path():
    snapshots = ig.parse_gh_repo_list(SAMPLE_GH_JSON)
    assert len(snapshots) == 3
    assert snapshots[0].name == "openclaw-akos"
    assert snapshots[0].visibility == "PUBLIC"
    assert snapshots[0].primary_language == "Python"
    assert snapshots[0].created_at == "2024-01-01"
    assert snapshots[0].pushed_at == "2026-05-19"
    assert snapshots[0].topics == ("hlk", "akos")
    assert snapshots[2].is_fork is True


def test_parse_gh_repo_list_empty():
    assert ig.parse_gh_repo_list("[]") == []
    assert ig.parse_gh_repo_list("") == []
    assert ig.parse_gh_repo_list("   ") == []


def test_parse_gh_repo_list_missing_fields_tolerated():
    raw = json.dumps([{"name": "spike", "url": "https://github.com/x/spike"}])
    snapshots = ig.parse_gh_repo_list(raw)
    assert len(snapshots) == 1
    assert snapshots[0].name == "spike"
    assert snapshots[0].primary_language is None
    assert snapshots[0].is_archived is False
    assert snapshots[0].topics == ()


def test_parse_gh_repo_list_rejects_non_array():
    with pytest.raises(ValueError, match="JSON array"):
        ig.parse_gh_repo_list(json.dumps({"name": "single"}))


def test_parse_gh_repo_list_rejects_invalid_json():
    with pytest.raises(ValueError, match="not valid JSON"):
        ig.parse_gh_repo_list("not-json")


def test_parse_gh_repo_list_skips_nameless_items():
    raw = json.dumps([{"url": "https://x"}, {"name": "valid", "url": "https://y"}])
    snapshots = ig.parse_gh_repo_list(raw)
    assert len(snapshots) == 1
    assert snapshots[0].name == "valid"


# ---------- diff_against_registry ----------

def test_diff_detects_new_repos():
    snaps = ig.parse_gh_repo_list(SAMPLE_GH_JSON)
    diff = ig.diff_against_registry(snaps, [SAMPLE_REGISTRY_ROW])
    new_names = {s.name for s in diff.new_repos}
    assert "visiongen" in new_names
    assert "supabase" in new_names
    assert "openclaw-akos" not in new_names


def test_diff_detects_ghost_slugs():
    ghost_row = dict(SAMPLE_REGISTRY_ROW)
    ghost_row["repo_slug"] = "ghost-row"
    ghost_row["github_url"] = "https://github.com/FraysaXII/does-not-exist"
    diff = ig.diff_against_registry(ig.parse_gh_repo_list(SAMPLE_GH_JSON), [ghost_row])
    assert "ghost-row" in diff.ghost_slugs


def test_diff_detects_changed_metadata():
    snaps = ig.parse_gh_repo_list(SAMPLE_GH_JSON)
    # Existing row claims github_visibility=PRIVATE; GH says PUBLIC → drift signal.
    row = dict(SAMPLE_REGISTRY_ROW)
    row["github_visibility"] = "PRIVATE"
    row["pushed_at"] = "2024-01-01"
    diff = ig.diff_against_registry(snaps, [row])
    matched = [c for c in diff.changed if c[0] == "openclaw-akos"]
    assert len(matched) == 1
    deltas = matched[0][1]
    assert deltas.get("github_visibility") == "PUBLIC"
    assert deltas.get("pushed_at") == "2026-05-19"


def test_diff_empty_inputs():
    diff = ig.diff_against_registry([], [])
    assert diff.new_repos == []
    assert diff.ghost_slugs == []
    assert diff.changed == []


# ---------- classify_default heuristic ----------

def test_classify_default_archive_takes_precedence():
    snap = ig.GhRepoSnapshot(
        name="dead", url="x", visibility="PRIVATE", is_archived=True,
        is_fork=False, primary_language=None, created_at="2020-01-01",
        pushed_at="2020-01-01", topics=(),
    )
    assert ig.classify_default(snap) == "archive"


def test_classify_default_fork_before_template():
    snap = ig.GhRepoSnapshot(
        name="nextjs-starter", url="x", visibility="PUBLIC", is_archived=False,
        is_fork=True, primary_language=None, created_at="2024-01-01",
        pushed_at="2024-01-01", topics=(),
    )
    assert ig.classify_default(snap) == "fork"


def test_classify_default_template_pattern():
    for name in ("nextjs-supabase-kit", "platforms-starter-kit", "boilerplate-2"):
        snap = ig.GhRepoSnapshot(
            name=name, url="x", visibility="PRIVATE", is_archived=False,
            is_fork=False, primary_language=None, created_at="2024-01-01",
            pushed_at="2024-01-01", topics=(),
        )
        assert ig.classify_default(snap) == "template", f"{name} should classify as template"


def test_classify_default_fallback_experiment():
    snap = ig.GhRepoSnapshot(
        name="my-spike", url="x", visibility="PRIVATE", is_archived=False,
        is_fork=False, primary_language=None, created_at="2024-01-01",
        pushed_at="2024-01-01", topics=(),
    )
    assert ig.classify_default(snap) == "experiment"


# ---------- Pydantic round-trip ----------

def test_pydantic_row_round_trip_minimal():
    """Existing-row shape (all new I86 fields empty) must Pydantic-validate."""
    row = RepositoryRegistryRow.model_validate(
        {**SAMPLE_REGISTRY_ROW, "app_class": None, "github_visibility": None,
         "primary_language": None, "created_at": None, "pushed_at": None,
         "last_inventory_at": None, "governance_status": None,
         "codeowners_present": None, "branch_protection_enabled": None}
    )
    assert row.repo_slug == "openclaw-akos"
    assert row.app_class is None
    assert row.governance_status is None


def test_pydantic_row_round_trip_full():
    """Backfilled row shape must Pydantic-validate."""
    full = {
        **SAMPLE_REGISTRY_ROW,
        "app_class": "production",
        "metadata_tags": "platform;ssot",
        "github_topics": "hlk;akos",
        "github_visibility": "PUBLIC",
        "primary_language": "Python",
        "created_at": "2024-01-01",
        "pushed_at": "2026-05-19",
        "last_inventory_at": "2026-05-19",
        "governance_status": "governed",
        "related_initiative_ids": "I86",
        "codeowners_present": True,
        "branch_protection_enabled": True,
    }
    row = RepositoryRegistryRow.model_validate(full)
    assert row.app_class == "production"
    assert row.governance_status == "governed"


def test_pydantic_row_rejects_invalid_app_class():
    bad = {**SAMPLE_REGISTRY_ROW, "app_class": "not-a-class"}
    with pytest.raises(ValidationError):
        RepositoryRegistryRow.model_validate(bad)


def test_pydantic_row_rejects_invalid_governance_status():
    bad = {**SAMPLE_REGISTRY_ROW, "governance_status": "wrong"}
    with pytest.raises(ValidationError):
        RepositoryRegistryRow.model_validate(bad)


def test_pydantic_row_rejects_invalid_date():
    bad = {**SAMPLE_REGISTRY_ROW, "pushed_at": "yesterday"}
    with pytest.raises(ValidationError):
        RepositoryRegistryRow.model_validate(bad)


def test_pydantic_row_rejects_invalid_slug():
    bad = {**SAMPLE_REGISTRY_ROW, "repo_slug": "UPPER-CASE-BAD"}
    with pytest.raises(ValidationError):
        RepositoryRegistryRow.model_validate(bad)


def test_fieldnames_count_is_29():
    assert len(REPOSITORY_REGISTRY_FIELDNAMES) == 29, (
        f"I86 Wave H schema extension expects 29 columns; got "
        f"{len(REPOSITORY_REGISTRY_FIELDNAMES)}"
    )


def test_new_enum_frozensets_have_expected_values():
    assert "production" in VALID_APP_CLASS
    assert "uncategorized" in VALID_APP_CLASS
    assert len(VALID_APP_CLASS) == 7
    assert "governed" in VALID_GOVERNANCE_STATUS
    assert len(VALID_GOVERNANCE_STATUS) == 4
    assert VALID_GITHUB_VISIBILITY == frozenset({"PUBLIC", "PRIVATE", "INTERNAL"})


# ---------- drift report rendering ----------

def test_render_drift_report_has_required_sections():
    snaps = ig.parse_gh_repo_list(SAMPLE_GH_JSON)
    diff = ig.diff_against_registry(snaps, [SAMPLE_REGISTRY_ROW])
    report = ig.render_drift_report(diff)
    assert "# GitHub repo inventory" in report
    assert "## Summary" in report
    assert "## New repos" in report
    assert "## Ghost slugs" in report
    assert "## Changed metadata" in report
    assert "D-IH-86-AF" in report


def test_render_drift_report_includes_suggested_app_class():
    snaps = ig.parse_gh_repo_list(SAMPLE_GH_JSON)
    diff = ig.diff_against_registry(snaps, [SAMPLE_REGISTRY_ROW])
    report = ig.render_drift_report(diff)
    # visiongen → experiment, supabase (fork) → fork
    assert "`experiment`" in report
    assert "`fork`" in report


# ---------- fetch_github_inventory (mocked) ----------

def test_fetch_github_inventory_soft_fails_when_gh_missing():
    def fake_runner(args, *, timeout=120, capture=True, check=False):
        return CommandResult(success=False, stdout="", stderr="gh not found", returncode=-1)

    snapshots = ig.fetch_github_inventory(runner=fake_runner)
    assert snapshots == []


def test_fetch_github_inventory_parses_runner_output():
    def fake_runner(args, *, timeout=120, capture=True, check=False):
        return CommandResult(success=True, stdout=SAMPLE_GH_JSON, stderr="", returncode=0)

    snapshots = ig.fetch_github_inventory(runner=fake_runner)
    assert len(snapshots) == 3
    assert snapshots[0].name == "openclaw-akos"


# ---------- write_drift_report --dry-run ----------

def test_write_drift_report_dry_run_does_not_write(tmp_path, monkeypatch):
    monkeypatch.setattr(ig, "INVENTORY_DIR", tmp_path / "artifacts" / "inventory")
    from datetime import date
    out = ig.write_drift_report("hello", at=date(2026, 5, 19), dry_run=True)
    assert not out.exists()


def test_write_drift_report_writes_to_disk(tmp_path, monkeypatch):
    monkeypatch.setattr(ig, "INVENTORY_DIR", tmp_path / "artifacts" / "inventory")
    from datetime import date
    out = ig.write_drift_report("hello world", at=date(2026, 5, 19), dry_run=False)
    assert out.exists()
    assert out.read_text(encoding="utf-8") == "hello world"


# ---------- update_app_class ----------

def _write_fixture_csv(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    csv_path = tmp_path / "REPOSITORY_REGISTRY.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REPOSITORY_REGISTRY_FIELDNAMES)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return csv_path


def test_update_app_class_dry_run_does_not_write(tmp_path):
    csv_path = _write_fixture_csv(tmp_path, [SAMPLE_REGISTRY_ROW])
    before = csv_path.read_text(encoding="utf-8")
    ok = ig.update_app_class(csv_path, "openclaw-akos", "production", dry_run=True)
    assert ok is True
    assert csv_path.read_text(encoding="utf-8") == before


def test_update_app_class_writes_when_not_dry_run(tmp_path):
    csv_path = _write_fixture_csv(tmp_path, [SAMPLE_REGISTRY_ROW])
    ok = ig.update_app_class(csv_path, "openclaw-akos", "production", dry_run=False)
    assert ok is True
    with csv_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert rows[0]["app_class"] == "production"
    assert rows[0]["last_inventory_at"]  # populated


def test_update_app_class_rejects_invalid_value(tmp_path):
    csv_path = _write_fixture_csv(tmp_path, [SAMPLE_REGISTRY_ROW])
    ok = ig.update_app_class(csv_path, "openclaw-akos", "not-real", dry_run=False)
    assert ok is False


def test_update_app_class_returns_false_for_missing_slug(tmp_path):
    csv_path = _write_fixture_csv(tmp_path, [SAMPLE_REGISTRY_ROW])
    ok = ig.update_app_class(csv_path, "does-not-exist", "experiment", dry_run=False)
    assert ok is False


# ---------- CLI argparse routing ----------

def test_argparse_sweep_subcommand():
    parser = ig.build_parser()
    args = parser.parse_args(["sweep", "--org", "FraysaXII", "--limit", "50"])
    assert args.cmd == "sweep"
    assert args.org == "FraysaXII"
    assert args.limit == 50
    assert args.func is ig.cmd_sweep


def test_argparse_classify_subcommand():
    parser = ig.build_parser()
    args = parser.parse_args(["classify", "--repo", "x", "--app-class", "research"])
    assert args.cmd == "classify"
    assert args.repo == "x"
    assert args.app_class == "research"
    assert args.func is ig.cmd_classify


def test_argparse_audit_subcommand():
    parser = ig.build_parser()
    args = parser.parse_args(["--dry-run", "audit"])
    assert args.cmd == "audit"
    assert args.dry_run is True
    assert args.func is ig.cmd_audit


def test_argparse_classify_rejects_invalid_app_class():
    parser = ig.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["classify", "--repo", "x", "--app-class", "bogus"])
