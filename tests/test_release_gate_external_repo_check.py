"""Tests for scripts/check_external_repo_contract.py.

Verifies the external-repo contract check (wired into release-gate.py via
``run_external_repo_contract_check()``) catches missing artifacts, stale
contract review dates, and sha256 drift between consumer mirror copies and
the AKOS template.
"""

from __future__ import annotations

import csv
import importlib.util
import sys
import textwrap
from datetime import date, timedelta
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_external_repo_contract.py"


def _load() -> object:
    spec = importlib.util.spec_from_file_location("_external_repo_contract_test", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def check():
    return _load()


def _write_registry(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    path = tmp_path / "REPOSITORY_REGISTRY.csv"
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _write_snapshot(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    path = tmp_path / "REPO_HEALTH_SNAPSHOT.csv"
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


# ---------------------------------------------------------------------------
# Real-shipped artefacts
# ---------------------------------------------------------------------------


def test_real_repos_pass_with_current_snapshot(check):
    """The shipped registry + snapshot + cached AKOS template must validate clean."""
    rc = check.main([])
    assert rc == 0


# ---------------------------------------------------------------------------
# Missing artifacts
# ---------------------------------------------------------------------------


def test_missing_contract_in_snapshot_fails(check, tmp_path, monkeypatch):
    registry = _write_registry(tmp_path, [{
        "repo_slug": "fake-platform",
        "github_url": "https://github.com/example/fake-platform",
        "class": "platform",
        "primary_owner_role": "System Owner",
        "topic_ids": "",
        "vault_doc_root": "",
        "api_spec_pointer": "",
        "api_topic_id": "",
        "lifecycle_status": "active",
        "notes": "",
    }])
    snapshot = _write_snapshot(tmp_path, [{
        "repo_slug": "fake-platform",
        "snapshot_date": "2026-05-06",
        "commit_sha_at_snapshot": "deadbeef",
        "cursor_rule_count": "1",
        "has_external_repo_contract": "false",
        "has_akos_mirror_rule": "true",
        "language_frontmatter_compliance_pct": "100.0",
        "brand_jargon_violations": "0",
        "embedded_obsidian_snapshot_present": "false",
        "notes": "test row",
    }])
    monkeypatch.setattr(check, "REGISTRY_CSV", registry)
    monkeypatch.setattr(check, "SNAPSHOT_CSV", snapshot)
    monkeypatch.setattr(check, "_resolve_repo_paths", lambda: {"fake-platform": tmp_path / "nonexistent"})

    rc = check.main([])
    assert rc == 1


def test_missing_snapshot_row_for_real_repo_fails(check, tmp_path, monkeypatch):
    registry = _write_registry(tmp_path, [{
        "repo_slug": "fake-platform",
        "github_url": "https://github.com/example/fake-platform",
        "class": "platform",
        "primary_owner_role": "System Owner",
        "topic_ids": "",
        "vault_doc_root": "",
        "api_spec_pointer": "",
        "api_topic_id": "",
        "lifecycle_status": "active",
        "notes": "",
    }])
    snapshot = tmp_path / "empty_snapshot.csv"
    snapshot.write_text(
        "repo_slug,snapshot_date,commit_sha_at_snapshot,cursor_rule_count,has_external_repo_contract,has_akos_mirror_rule,language_frontmatter_compliance_pct,brand_jargon_violations,embedded_obsidian_snapshot_present,notes\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(check, "REGISTRY_CSV", registry)
    monkeypatch.setattr(check, "SNAPSHOT_CSV", snapshot)
    # Slug *is* in the path map, so it shouldn't be skipped as a placeholder.
    monkeypatch.setattr(check, "_resolve_repo_paths", lambda: {"fake-platform": tmp_path / "nonexistent"})

    rc = check.main([])
    assert rc == 1


# ---------------------------------------------------------------------------
# Stale review
# ---------------------------------------------------------------------------


def test_stale_last_review_fails(check, tmp_path, monkeypatch):
    repo_path = tmp_path / "fake-repo"
    (repo_path / ".cursor" / "rules").mkdir(parents=True)
    contract = repo_path / "EXTERNAL_REPO_CONTRACT.md"
    stale_date = (date.today() - timedelta(days=200)).isoformat()
    contract.write_text(textwrap.dedent(f"""
        ---
        last_review: {stale_date}
        ---

        # Contract
    """).strip(), encoding="utf-8")
    mirror = repo_path / ".cursor" / "rules" / "akos-mirror.mdc"
    mirror.write_text(check.MIRROR_TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")

    registry = _write_registry(tmp_path, [{
        "repo_slug": "fake-platform",
        "github_url": "https://github.com/example/fake-platform",
        "class": "platform",
        "primary_owner_role": "System Owner",
        "topic_ids": "",
        "vault_doc_root": "",
        "api_spec_pointer": "",
        "api_topic_id": "",
        "lifecycle_status": "active",
        "notes": "",
    }])
    snapshot = _write_snapshot(tmp_path, [{
        "repo_slug": "fake-platform",
        "snapshot_date": "2026-05-06",
        "commit_sha_at_snapshot": "deadbeef",
        "cursor_rule_count": "1",
        "has_external_repo_contract": "true",
        "has_akos_mirror_rule": "true",
        "language_frontmatter_compliance_pct": "100.0",
        "brand_jargon_violations": "0",
        "embedded_obsidian_snapshot_present": "false",
        "notes": "test row",
    }])
    monkeypatch.setattr(check, "REGISTRY_CSV", registry)
    monkeypatch.setattr(check, "SNAPSHOT_CSV", snapshot)
    monkeypatch.setattr(check, "_resolve_repo_paths", lambda: {"fake-platform": repo_path})

    rc = check.main(["--freshness-days", "90"])
    assert rc == 1


def test_freshness_days_argument_extends_window(check, tmp_path, monkeypatch):
    repo_path = tmp_path / "fake-repo"
    (repo_path / ".cursor" / "rules").mkdir(parents=True)
    stale_date = (date.today() - timedelta(days=200)).isoformat()
    contract = repo_path / "EXTERNAL_REPO_CONTRACT.md"
    contract.write_text(f"---\nlast_review: {stale_date}\n---\n", encoding="utf-8")
    mirror = repo_path / ".cursor" / "rules" / "akos-mirror.mdc"
    mirror.write_text(check.MIRROR_TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")

    registry = _write_registry(tmp_path, [{
        "repo_slug": "fake-platform",
        "github_url": "https://github.com/example/fake-platform",
        "class": "platform",
        "primary_owner_role": "System Owner",
        "topic_ids": "",
        "vault_doc_root": "",
        "api_spec_pointer": "",
        "api_topic_id": "",
        "lifecycle_status": "active",
        "notes": "",
    }])
    snapshot = _write_snapshot(tmp_path, [{
        "repo_slug": "fake-platform",
        "snapshot_date": "2026-05-06",
        "commit_sha_at_snapshot": "deadbeef",
        "cursor_rule_count": "1",
        "has_external_repo_contract": "true",
        "has_akos_mirror_rule": "true",
        "language_frontmatter_compliance_pct": "100.0",
        "brand_jargon_violations": "0",
        "embedded_obsidian_snapshot_present": "false",
        "notes": "test row",
    }])
    monkeypatch.setattr(check, "REGISTRY_CSV", registry)
    monkeypatch.setattr(check, "SNAPSHOT_CSV", snapshot)
    monkeypatch.setattr(check, "_resolve_repo_paths", lambda: {"fake-platform": repo_path})

    rc = check.main(["--freshness-days", "365"])
    assert rc == 0


# ---------------------------------------------------------------------------
# sha256 drift
# ---------------------------------------------------------------------------


def test_mirror_sha256_drift_fails(check, tmp_path, monkeypatch):
    repo_path = tmp_path / "fake-repo"
    (repo_path / ".cursor" / "rules").mkdir(parents=True)
    fresh_date = date.today().isoformat()
    contract = repo_path / "EXTERNAL_REPO_CONTRACT.md"
    contract.write_text(f"---\nlast_review: {fresh_date}\n---\n", encoding="utf-8")
    mirror = repo_path / ".cursor" / "rules" / "akos-mirror.mdc"
    mirror.write_text("# DRIFTED CONTENT\n", encoding="utf-8")

    registry = _write_registry(tmp_path, [{
        "repo_slug": "fake-platform",
        "github_url": "https://github.com/example/fake-platform",
        "class": "platform",
        "primary_owner_role": "System Owner",
        "topic_ids": "",
        "vault_doc_root": "",
        "api_spec_pointer": "",
        "api_topic_id": "",
        "lifecycle_status": "active",
        "notes": "",
    }])
    snapshot = _write_snapshot(tmp_path, [{
        "repo_slug": "fake-platform",
        "snapshot_date": "2026-05-06",
        "commit_sha_at_snapshot": "deadbeef",
        "cursor_rule_count": "1",
        "has_external_repo_contract": "true",
        "has_akos_mirror_rule": "true",
        "language_frontmatter_compliance_pct": "100.0",
        "brand_jargon_violations": "0",
        "embedded_obsidian_snapshot_present": "false",
        "notes": "test row",
    }])
    monkeypatch.setattr(check, "REGISTRY_CSV", registry)
    monkeypatch.setattr(check, "SNAPSHOT_CSV", snapshot)
    monkeypatch.setattr(check, "_resolve_repo_paths", lambda: {"fake-platform": repo_path})

    rc = check.main([])
    assert rc == 1


# ---------------------------------------------------------------------------
# Skip rules
# ---------------------------------------------------------------------------


def test_reference_class_repos_are_skipped(check, tmp_path, monkeypatch):
    registry = _write_registry(tmp_path, [{
        "repo_slug": "fake-reference",
        "github_url": "https://github.com/example/fake-reference",
        "class": "reference",
        "primary_owner_role": "Brand Manager",
        "topic_ids": "",
        "vault_doc_root": "",
        "api_spec_pointer": "",
        "api_topic_id": "",
        "lifecycle_status": "reference",
        "notes": "",
    }])
    monkeypatch.setattr(check, "REGISTRY_CSV", registry)
    monkeypatch.setattr(check, "SNAPSHOT_CSV", tmp_path / "no-snapshot.csv")
    monkeypatch.setattr(check, "_resolve_repo_paths", lambda: {})

    rc = check.main([])
    assert rc == 0


def test_akos_internal_repos_are_skipped(check, tmp_path, monkeypatch):
    registry = _write_registry(tmp_path, [{
        "repo_slug": "openclaw-akos",
        "github_url": "https://github.com/FraysaXII/openclaw-akos",
        "class": "platform",
        "primary_owner_role": "AI Engineer",
        "topic_ids": "",
        "vault_doc_root": "",
        "api_spec_pointer": "",
        "api_topic_id": "",
        "lifecycle_status": "active",
        "notes": "",
    }])
    snapshot = tmp_path / "empty_snap.csv"
    snapshot.write_text(
        "repo_slug,snapshot_date,commit_sha_at_snapshot,cursor_rule_count,has_external_repo_contract,has_akos_mirror_rule,language_frontmatter_compliance_pct,brand_jargon_violations,embedded_obsidian_snapshot_present,notes\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(check, "REGISTRY_CSV", registry)
    monkeypatch.setattr(check, "SNAPSHOT_CSV", snapshot)
    monkeypatch.setattr(check, "_resolve_repo_paths", lambda: {})

    rc = check.main([])
    assert rc == 0
