"""Tests for scripts/check_external_repo_ci_posture.py.

Verifies presence checks, branch-protection / vercel / sast / sentry / slack /
secret-rotation sub-checks across PASS / FAIL / SKIPPED / WARN states. Live
calls (gh, vercel, Sentry) are mocked or auto-skip when CLIs unavailable.
"""

from __future__ import annotations

import importlib.util
import sys
import textwrap
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_external_repo_ci_posture.py"


def _load() -> object:
    spec = importlib.util.spec_from_file_location("_ci_posture_test", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def posture():
    return _load()


@pytest.fixture()
def fake_repo(tmp_path: Path) -> Path:
    root = tmp_path / "fake-repo"
    (root / ".github" / "workflows").mkdir(parents=True)
    return root


# ---------------------------------------------------------------------------
# Job-name extraction + token matching
# ---------------------------------------------------------------------------


def test_extract_ci_job_names_returns_top_level_jobs(posture):
    workflow = textwrap.dedent("""
        name: CI
        jobs:
          lint-typecheck:
            runs-on: ubuntu-latest
          unit:
            runs-on: ubuntu-latest
          build:
            runs-on: ubuntu-latest
    """).strip()
    assert posture._extract_ci_job_names(workflow) == ["lint-typecheck", "unit", "build"]


def test_required_jobs_satisfied_compound_token(posture):
    missing = posture._required_jobs_satisfied(["lint-typecheck", "audit", "build", "unit"])
    assert missing == []


def test_required_jobs_satisfied_misses_typecheck(posture):
    missing = posture._required_jobs_satisfied(["lint", "build", "audit"])
    assert "typecheck" in missing


# ---------------------------------------------------------------------------
# Presence sub-check
# ---------------------------------------------------------------------------


def _good_workflow() -> str:
    return textwrap.dedent("""
        name: CI
        jobs:
          lint:
            runs-on: ubuntu-latest
          typecheck:
            runs-on: ubuntu-latest
          audit:
            runs-on: ubuntu-latest
          build:
            runs-on: ubuntu-latest
    """).strip()


def test_presence_all_good(posture, fake_repo):
    (fake_repo / ".github" / "workflows" / "ci.yml").write_text(_good_workflow(), encoding="utf-8")
    (fake_repo / ".github" / "dependabot.yml").write_text("version: 2", encoding="utf-8")
    (fake_repo / ".github" / "CODEOWNERS").write_text("* @x", encoding="utf-8")
    results = posture.check_presence(fake_repo)
    assert all(r.level == "PASS" for r in results)


def test_presence_missing_workflow_fails(posture, fake_repo):
    results = posture.check_presence(fake_repo)
    assert any(r.level == "FAIL" and "ci_yml" in r.name for r in results)


def test_presence_missing_required_job_fails(posture, fake_repo):
    bad = textwrap.dedent("""
        name: CI
        jobs:
          unit:
            runs-on: ubuntu-latest
    """).strip()
    (fake_repo / ".github" / "workflows" / "ci.yml").write_text(bad, encoding="utf-8")
    (fake_repo / ".github" / "dependabot.yml").write_text("version: 2", encoding="utf-8")
    (fake_repo / ".github" / "CODEOWNERS").write_text("* @x", encoding="utf-8")
    results = posture.check_presence(fake_repo)
    assert any(r.level == "FAIL" and "missing required job" in r.message for r in results)


# ---------------------------------------------------------------------------
# License + secret rotation
# ---------------------------------------------------------------------------


def test_license_present_warn_when_missing(posture, fake_repo):
    r = posture.check_license_present(fake_repo)
    assert r.level == "WARN"


def test_license_present_pass_when_root_license(posture, fake_repo):
    (fake_repo / "LICENSE").write_text("All Rights Reserved", encoding="utf-8")
    r = posture.check_license_present(fake_repo)
    assert r.level == "PASS"


def test_secret_rotation_warn_when_runbook_missing(posture, fake_repo):
    r = posture.check_secret_rotation(fake_repo)
    assert r.level == "WARN"


def test_secret_rotation_pass_with_recent_rotations(posture, fake_repo):
    (fake_repo / "docs" / "runbooks").mkdir(parents=True)
    today = date.today().isoformat()
    body = textwrap.dedent(f"""
        ---
        secrets:
          - name: SUPABASE_KEY
            last_rotated: {today}
        ---
        # Secrets
    """).strip()
    (fake_repo / "docs" / "runbooks" / "secrets-rotation.md").write_text(body, encoding="utf-8")
    r = posture.check_secret_rotation(fake_repo)
    assert r.level == "PASS"


def test_secret_rotation_fail_when_overdue(posture, fake_repo):
    (fake_repo / "docs" / "runbooks").mkdir(parents=True)
    overdue = (date.today() - timedelta(days=120)).isoformat()
    body = textwrap.dedent(f"""
        ---
        secrets:
          - name: STALE_KEY
            last_rotated: {overdue}
        ---
    """).strip()
    (fake_repo / "docs" / "runbooks" / "secrets-rotation.md").write_text(body, encoding="utf-8")
    r = posture.check_secret_rotation(fake_repo)
    assert r.level == "FAIL"
    assert "STALE_KEY" in r.message


def test_secret_rotation_warn_when_approaching(posture, fake_repo):
    (fake_repo / "docs" / "runbooks").mkdir(parents=True)
    approaching = (date.today() - timedelta(days=80)).isoformat()
    body = textwrap.dedent(f"""
        ---
        secrets:
          - name: SOON_KEY
            last_rotated: {approaching}
        ---
    """).strip()
    (fake_repo / "docs" / "runbooks" / "secrets-rotation.md").write_text(body, encoding="utf-8")
    r = posture.check_secret_rotation(fake_repo)
    assert r.level == "WARN"


# ---------------------------------------------------------------------------
# Live-API checks: gracefully SKIPPED when CLIs unavailable
# ---------------------------------------------------------------------------


def test_branch_protection_skips_without_gh(posture, monkeypatch):
    monkeypatch.setattr(posture, "_gh_auth_ok", lambda: False)
    r = posture.check_branch_protection("https://github.com/example/x")
    assert r.level == "SKIPPED"


def test_vercel_skips_without_cli(posture, monkeypatch):
    monkeypatch.setattr(posture, "_vercel_available", lambda: False)
    r = posture.check_vercel_projects("hlk-erp")
    assert r.level == "SKIPPED"


def test_sentry_skips_without_token(posture, monkeypatch):
    monkeypatch.delenv("SENTRY_AUTH_TOKEN", raising=False)
    r = posture.check_sentry_liveness("hlk-erp")
    assert r.level == "SKIPPED"


def test_slack_warn_without_env(posture, monkeypatch):
    monkeypatch.delenv("SLACK_OPS_WEBHOOK", raising=False)
    r = posture.check_slack_webhook_present()
    assert r.level == "WARN"


def test_slack_pass_with_env(posture, monkeypatch):
    monkeypatch.setenv("SLACK_OPS_WEBHOOK", "https://hooks.slack.com/services/xxx")
    r = posture.check_slack_webhook_present()
    assert r.level == "PASS"


# ---------------------------------------------------------------------------
# Branch protection — mocked gh response, all good
# ---------------------------------------------------------------------------


def test_branch_protection_passes_with_well_formed_payload(posture, monkeypatch):
    monkeypatch.setattr(posture, "_gh_auth_ok", lambda: True)
    fake_resp = mock.Mock()
    fake_resp.returncode = 0
    fake_resp.stdout = (
        '{"required_pull_request_reviews": {"required_approving_review_count": 1, "dismiss_stale_reviews": true},'
        ' "required_status_checks": {"contexts": ["lint", "typecheck", "audit", "build"]}}'
    )
    fake_resp.stderr = ""
    monkeypatch.setattr(posture.subprocess, "run", lambda *a, **kw: fake_resp)
    r = posture.check_branch_protection("https://github.com/example/x")
    assert r.level == "PASS"


def test_branch_protection_fails_when_dismiss_stale_off(posture, monkeypatch):
    monkeypatch.setattr(posture, "_gh_auth_ok", lambda: True)
    fake_resp = mock.Mock()
    fake_resp.returncode = 0
    fake_resp.stdout = (
        '{"required_pull_request_reviews": {"required_approving_review_count": 1, "dismiss_stale_reviews": false},'
        ' "required_status_checks": {"contexts": ["lint", "typecheck", "audit", "build"]}}'
    )
    fake_resp.stderr = ""
    monkeypatch.setattr(posture.subprocess, "run", lambda *a, **kw: fake_resp)
    r = posture.check_branch_protection("https://github.com/example/x")
    assert r.level == "FAIL"
    assert "dismiss_stale" in r.message
