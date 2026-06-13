"""Tests for scripts/validate_subdomains_registry.py (I62 P0)."""

from __future__ import annotations

import importlib.util
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "validate_subdomains_registry.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("_validate_subdomains_registry_test", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def validator(monkeypatch):
    """Load the validator module fresh per test, with REGISTRY_PATH overridable."""
    return _load_validator()


def _write_registry(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "SUBDOMAINS_REGISTRY.md"
    path.write_text(body, encoding="utf-8")
    return path


def test_real_registry_passes(validator):
    """The shipped SUBDOMAINS_REGISTRY.md must validate clean."""
    rc = validator.main([])
    assert rc == 0


def test_missing_required_field_fails(validator, tmp_path, monkeypatch):
    body = textwrap.dedent(
        """
        ---
        language: en
        ---

        # Subdomains

        | subdomain | apex | state | data_mode | auth | brand_register | vercel_project | repo | linked_initiative | notes |
        |-----------|------|-------|-----------|------|----------------|----------------|------|-------------------|-------|
        | `erp` | `holistikaresearch.com` | active |  | required | internal | `hlk-erp` | `hlk-erp` | I62 | active row missing data_mode |
        """
    ).lstrip()
    path = _write_registry(tmp_path, body)
    monkeypatch.setattr(validator, "REGISTRY_PATH", path)

    rc = validator.main([])
    assert rc == 1


def test_duplicate_slug_rejected(validator, tmp_path, monkeypatch):
    body = textwrap.dedent(
        """
        # Subdomains

        | subdomain | apex | state | data_mode | auth | brand_register | vercel_project | repo | linked_initiative | notes |
        |-----------|------|-------|-----------|------|----------------|----------------|------|-------------------|-------|
        | `erp` | `holistikaresearch.com` | active | live | required | internal | `hlk-erp` | `hlk-erp` | I62 | row 1 |
        | `erp` | `holistikaresearch.com` | active | live | required | internal | `hlk-erp` | `hlk-erp` | I62 | row 2 dup |
        """
    ).lstrip()
    path = _write_registry(tmp_path, body)
    monkeypatch.setattr(validator, "REGISTRY_PATH", path)

    rc = validator.main([])
    assert rc == 1


def test_active_without_vercel_project_rejected(validator, tmp_path, monkeypatch):
    body = textwrap.dedent(
        """
        # Subdomains

        | subdomain | apex | state | data_mode | auth | brand_register | vercel_project | repo | linked_initiative | notes |
        |-----------|------|-------|-----------|------|----------------|----------------|------|-------------------|-------|
        | `madeira` | `holistikaresearch.com` | active | demo | none | external | _(none yet)_ | `hlk-erp` | I62 | should fail |
        """
    ).lstrip()
    path = _write_registry(tmp_path, body)
    monkeypatch.setattr(validator, "REGISTRY_PATH", path)

    rc = validator.main([])
    assert rc == 1


def test_reserved_row_minimal_passes(validator, tmp_path, monkeypatch):
    body = textwrap.dedent(
        """
        # Subdomains

        | subdomain | apex | state | data_mode | auth | brand_register | vercel_project | repo | linked_initiative | notes |
        |-----------|------|-------|-----------|------|----------------|----------------|------|-------------------|-------|
        | `api` | `holistikaresearch.com` | reserved | live | required | internal | _(none yet)_ | _(future)_ | _(future)_ | reserved |
        """
    ).lstrip()
    path = _write_registry(tmp_path, body)
    monkeypatch.setattr(validator, "REGISTRY_PATH", path)

    rc = validator.main([])
    assert rc == 0


def test_invalid_state_rejected(validator, tmp_path, monkeypatch):
    body = textwrap.dedent(
        """
        # Subdomains

        | subdomain | apex | state | data_mode | auth | brand_register | vercel_project | repo | linked_initiative | notes |
        |-----------|------|-------|-----------|------|----------------|----------------|------|-------------------|-------|
        | `foo` | `holistikaresearch.com` | live | live | required | internal | `hlk-foo` | `hlk-foo` | I62 | bad state value |
        """
    ).lstrip()
    path = _write_registry(tmp_path, body)
    monkeypatch.setattr(validator, "REGISTRY_PATH", path)

    rc = validator.main([])
    assert rc == 1


def test_missing_file_returns_1(validator, tmp_path, monkeypatch):
    monkeypatch.setattr(validator, "REGISTRY_PATH", tmp_path / "does_not_exist.md")
    rc = validator.main([])
    assert rc == 1
