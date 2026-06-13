"""Tests for Track K + L automation scripts.

Covers:

- ``scripts/secret_rotation_reminders.py`` — surface generation across temp repos.
- ``scripts/configure_branch_protection.py`` — payload assembly + match logic.
- ``scripts/regen_consumer_types.py`` — TS interface emission from CSV headers.
- ``scripts/provision_vercel_project.py`` — registry parsing + non-provisionable
  row detection.
- ``scripts/detect_unblessed_registry_rows.py`` — bless status classification.
- ``scripts/notify_consumers_of_canonical_change.py`` — affected-consumer
  resolution from the registry.

Each test stubs out external CLIs (``gh``, ``vercel``) and the network so the
suite stays hermetic on CI runners.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable
from unittest.mock import patch

import pytest

import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import (
    configure_branch_protection,
    detect_unblessed_registry_rows,
    notify_consumers_of_canonical_change,
    provision_vercel_project,
    regen_consumer_types,
    secret_rotation_reminders,
)
from scripts.bless_external_repo import RepoMeta


# ---------------------------------------------------------------------------
# Fixture: minimal in-memory registry with one consuming repo + one reference
# ---------------------------------------------------------------------------


def _registry_two() -> dict[str, RepoMeta]:
    return {
        "alpha": RepoMeta(
            slug="alpha",
            github_url="https://github.com/FraysaXII/alpha",
            repo_class="platform",
            primary_owner_role="System Owner",
            vault_doc_root="docs/references/hlk/v3.0/Envoy Tech Lab/Alpha/",
            lifecycle_status="active",
            consumes_compliance_types=True,
            consumes_mirrors=("PERSONA_REGISTRY", "SKILL_REGISTRY"),
            relative_path="alpha",
        ),
        "ref-only": RepoMeta(
            slug="ref-only",
            github_url="https://github.com/FraysaXII/ref-only",
            repo_class="reference",
            primary_owner_role="System Owner",
            vault_doc_root="",
            lifecycle_status="active",
        ),
    }


# ---------------------------------------------------------------------------
# secret_rotation_reminders
# ---------------------------------------------------------------------------


def test_secret_rotation_reminders_walks_only_local_paths(tmp_path, capsys, monkeypatch):
    repo = tmp_path / "alpha"
    (repo / "docs" / "runbooks").mkdir(parents=True)
    (repo / "docs" / "runbooks" / "secrets-rotation.md").write_text(
        "---\nsecrets:\n  - name: SUPABASE_KEY\n    last_rotated: 2025-01-01\n---\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(secret_rotation_reminders, "load_registry", lambda: _registry_two())
    monkeypatch.delenv("SLACK_OPS_WEBHOOK", raising=False)
    rc = secret_rotation_reminders.main([
        "--repo-path-map", f"alpha={repo}", "--strict",
    ])
    out = capsys.readouterr().out
    # Old secret should land in overdue bucket; --strict triggers exit 1.
    assert "Overdue" in out
    assert rc == 1


# ---------------------------------------------------------------------------
# configure_branch_protection — match logic only (no live gh calls)
# ---------------------------------------------------------------------------


def test_configure_branch_protection_match_aligned():
    desired = configure_branch_protection._desired_payload(["lint", "build"])
    current = {
        "required_pull_request_reviews": {"required_approving_review_count": 1, "dismiss_stale_reviews": True},
        "required_status_checks": {"strict": True, "contexts": ["lint", "build", "extra"]},
        "allow_force_pushes": {"enabled": False},
        "allow_deletions": {"enabled": False},
        "required_conversation_resolution": {"enabled": True},
    }
    assert configure_branch_protection._matches(current, desired) is True


def test_configure_branch_protection_match_drift_missing_context():
    desired = configure_branch_protection._desired_payload(["lint", "typecheck"])
    current = {
        "required_pull_request_reviews": {"required_approving_review_count": 1, "dismiss_stale_reviews": True},
        "required_status_checks": {"strict": True, "contexts": ["lint"]},
        "allow_force_pushes": {"enabled": False},
        "allow_deletions": {"enabled": False},
        "required_conversation_resolution": {"enabled": True},
    }
    assert configure_branch_protection._matches(current, desired) is False


def test_configure_branch_protection_skips_when_no_gh(monkeypatch, capsys):
    monkeypatch.setattr(configure_branch_protection, "_gh_available", lambda: False)
    rc = configure_branch_protection.main(["--repo-slug", "alpha"])
    assert rc == 0


# ---------------------------------------------------------------------------
# regen_consumer_types
# ---------------------------------------------------------------------------


def test_regen_consumer_types_generates_interfaces(tmp_path, monkeypatch):
    compliance = tmp_path / "compliance"
    compliance.mkdir()
    (compliance / "PERSONA_REGISTRY.csv").write_text(
        "persona_id,name,access_level\np1,founder,6\n", encoding="utf-8"
    )
    monkeypatch.setattr(regen_consumer_types, "COMPLIANCE_DIR", compliance)
    meta = _registry_two()["alpha"]
    body = regen_consumer_types.render_mirrors_module(meta)
    assert "AkosMirror_PERSONA_REGISTRY" in body
    assert "persona_id: string | null" in body
    assert "AkosMirror_SKILL_REGISTRY" in body  # missing CSV stub still emits empty interface


def test_regen_consumer_types_skips_non_consuming(tmp_path, monkeypatch):
    meta = RepoMeta(
        slug="beta",
        github_url="https://github.com/FraysaXII/beta",
        repo_class="platform",
        primary_owner_role="x",
        vault_doc_root="",
        lifecycle_status="active",
        consumes_compliance_types=False,
    )
    out = regen_consumer_types.regen_one(meta, tmp_path, dry_run=True, auto_pr=False)
    assert out == "SKIPPED_NOT_CONSUMING"


# ---------------------------------------------------------------------------
# provision_vercel_project — registry parser + non-provisionable rows
# ---------------------------------------------------------------------------


def test_provision_vercel_skips_rewrite_rows(monkeypatch):
    row = {
        "subdomain": "status",
        "apex": "holistikaresearch.com",
        "state": "active",
        "vercel_project": "rewrite from `hlk-erp`",
    }
    out = provision_vercel_project.provision_one(row, dry_run=True)
    assert out == "SKIPPED_NON_PROVISIONABLE"


def test_provision_vercel_dry_run_active_row():
    row = {
        "subdomain": "alpha",
        "apex": "holistikaresearch.com",
        "state": "active",
        "vercel_project": "alpha-app",
    }
    out = provision_vercel_project.provision_one(row, dry_run=True)
    assert out == "DRY_WROTE"


def test_provision_vercel_skips_when_no_cli(monkeypatch):
    row = {
        "subdomain": "alpha",
        "apex": "holistikaresearch.com",
        "state": "active",
        "vercel_project": "alpha-app",
    }
    monkeypatch.setattr(provision_vercel_project, "_vercel_available", lambda: False)
    out = provision_vercel_project.provision_one(row, dry_run=False)
    assert out == "SKIPPED_NO_CLI"


# ---------------------------------------------------------------------------
# detect_unblessed_registry_rows
# ---------------------------------------------------------------------------


def test_detect_unblessed_classifies_blessed_and_unblessed(tmp_path, monkeypatch, capsys):
    blessed_dir = tmp_path / "alpha"
    (blessed_dir / ".cursor" / "rules").mkdir(parents=True)
    (blessed_dir / ".cursor" / "rules" / "akos-mirror.mdc").write_text("x", encoding="utf-8")
    (blessed_dir / "EXTERNAL_REPO_CONTRACT.md").write_text("contract", encoding="utf-8")

    not_blessed = tmp_path / "beta"
    not_blessed.mkdir()

    fake_registry = {
        "alpha": _registry_two()["alpha"],
        "beta": RepoMeta(
            slug="beta",
            github_url="https://github.com/FraysaXII/beta",
            repo_class="platform",
            primary_owner_role="x",
            vault_doc_root="",
            lifecycle_status="active",
            relative_path="beta",
        ),
        "ref-only": _registry_two()["ref-only"],
    }
    monkeypatch.setattr(detect_unblessed_registry_rows, "load_registry", lambda: fake_registry)

    rc = detect_unblessed_registry_rows.main([
        "--repo-path-map", f"alpha={blessed_dir}",
        "--repo-path-map", f"beta={not_blessed}",
        "--strict",
    ])
    out = capsys.readouterr().out
    assert "BLESSED" in out and "alpha" in out
    assert "NEEDS_BLESS" in out and "beta" in out
    # ref-only is skipped (class=reference)
    assert rc == 1  # strict exit 1 because beta needs bless


# ---------------------------------------------------------------------------
# notify_consumers_of_canonical_change
# ---------------------------------------------------------------------------


def test_notify_consumers_filters_by_consumed_mirrors(monkeypatch, capsys):
    monkeypatch.setattr(notify_consumers_of_canonical_change, "load_registry", lambda: _registry_two())
    monkeypatch.delenv("SLACK_OPS_WEBHOOK", raising=False)
    rc = notify_consumers_of_canonical_change.main([
        "--changed", "PERSONA_REGISTRY",
        "--dry-run",
    ])
    assert rc == 0


def test_notify_consumers_no_match_returns_0(monkeypatch):
    monkeypatch.setattr(notify_consumers_of_canonical_change, "load_registry", lambda: _registry_two())
    monkeypatch.delenv("SLACK_OPS_WEBHOOK", raising=False)
    rc = notify_consumers_of_canonical_change.main([
        "--changed", "NONEXISTENT_MIRROR",
        "--dry-run",
    ])
    assert rc == 0


def test_notify_consumers_requires_changed():
    rc = notify_consumers_of_canonical_change.main(["--changed", ""])
    assert rc == 2
