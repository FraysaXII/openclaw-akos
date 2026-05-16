"""Tests for ``scripts/validate_openclaw_plugin_pinning.py`` (I87 P2 / D-IH-87-B).

Mirrors the I77 P4.C ``validate_*_pinning`` precedent: schema sanity, required
AKOS plugin presence, unknown-plugin warning, orphan-entry rejection.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_openclaw_plugin_pinning as validator  # noqa: E402


@pytest.mark.openclaw_runtime
def test_canonical_example_passes() -> None:
    """The canonical config/openclaw.json.example must PASS validation."""
    assert validator.validate() == 0


@pytest.mark.openclaw_runtime
def test_required_akos_plugins_set_is_nonempty() -> None:
    """``REQUIRED_AKOS_PINNED_PLUGINS`` must include akos-runtime-tools (D-IH-87-B)."""
    assert "akos-runtime-tools" in validator.REQUIRED_AKOS_PINNED_PLUGINS


@pytest.mark.openclaw_runtime
def test_known_third_party_plugins_constant() -> None:
    """``KNOWN_THIRD_PARTY_PLUGINS`` is the curated allow-list (immutable frozenset)."""
    assert isinstance(validator.KNOWN_THIRD_PARTY_PLUGINS, frozenset)
    for plugin in ("device-pair", "memory-core", "phone-control", "talk-voice"):
        assert plugin in validator.KNOWN_THIRD_PARTY_PLUGINS


@pytest.mark.openclaw_runtime
def test_required_akos_plugins_constant() -> None:
    """``REQUIRED_AKOS_PINNED_PLUGINS`` is an immutable frozenset."""
    assert isinstance(validator.REQUIRED_AKOS_PINNED_PLUGINS, frozenset)


@pytest.mark.openclaw_runtime
def test_discovers_akos_plugins() -> None:
    """``_discover_akos_plugins`` returns at least akos-runtime-tools."""
    discovered = validator._discover_akos_plugins()
    assert "akos-runtime-tools" in discovered


@pytest.mark.openclaw_runtime
def test_canonical_allow_list_contains_required(tmp_path: Path) -> None:
    """All ``REQUIRED_AKOS_PINNED_PLUGINS`` are present in canonical example."""
    config_text = validator.OPENCLAW_EXAMPLE_PATH.read_text(encoding="utf-8")
    config = json.loads(config_text)
    allow_set = set(config["plugins"]["allow"])
    for required in validator.REQUIRED_AKOS_PINNED_PLUGINS:
        assert required in allow_set, (
            f"Canonical example missing required pinned plugin {required}"
        )


@pytest.mark.openclaw_runtime
def test_canonical_no_orphan_entries() -> None:
    """No ``plugins.entries`` entry should lack a corresponding ``plugins.allow`` row."""
    config = json.loads(
        validator.OPENCLAW_EXAMPLE_PATH.read_text(encoding="utf-8")
    )
    allow_set = set(config["plugins"]["allow"])
    for entry_id in config["plugins"].get("entries", {}):
        assert entry_id in allow_set, (
            f"orphan plugins.entries row {entry_id} (must also be in plugins.allow)"
        )
