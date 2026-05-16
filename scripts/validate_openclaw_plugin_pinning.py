"""Validator for OpenClaw plugin pinning in config/openclaw.json.example.

Per **D-IH-87-B** (I87 P2 — OpenClaw operator-runtime hardening):

> "Ship miniature ``scripts/validate_openclaw_plugin_pinning.py`` in P2
> mirroring I77 P4.C wiring pattern; one allow-list per environment; wired
> into ``release-gate.py`` as INFO."

Enforces that the canonical config/openclaw.json.example carries a sane
``plugins.allow`` list:

1. The AKOS-authored ``akos-runtime-tools`` plugin MUST be present and pinned
   (existence is the "pinning" surface — its absence at this layer means the
   downstream operator config drifts away from the canonical baseline).
2. Every entry in ``plugins.allow`` MUST be either:
   - a known AKOS-authored plugin (under ``openclaw-plugins/<id>/openclaw.plugin.json``), or
   - in the curated third-party allow-list constant ``KNOWN_THIRD_PARTY_PLUGINS``.
   Anything else is flagged so a rogue addition cannot silently land.
3. Any plugin in ``plugins.entries`` MUST also appear in ``plugins.allow``
   (no orphan configuration).

Exit code: 0 PASS, 1 FAIL.

Wired into ``scripts/release-gate.py`` as INFO row per D-IH-87-B (the
allow-list policy is operator-tunable; per-operator config divergence is
expected — the canonical example is the SSOT for what AKOS recommends).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import logging  # noqa: E402

from akos import log  # noqa: E402

log.setup_logging()
logger = logging.getLogger(__name__)

OPENCLAW_EXAMPLE_PATH = REPO_ROOT / "config" / "openclaw.json.example"
PLUGINS_DIR = REPO_ROOT / "openclaw-plugins"

REQUIRED_AKOS_PINNED_PLUGINS: frozenset[str] = frozenset({
    "akos-runtime-tools",
})

KNOWN_THIRD_PARTY_PLUGINS: frozenset[str] = frozenset({
    "device-pair",
    "memory-core",
    "phone-control",
    "talk-voice",
})


def _discover_akos_plugins() -> set[str]:
    """Return plugin ids discovered in ``openclaw-plugins/``."""
    if not PLUGINS_DIR.exists():
        return set()
    discovered: set[str] = set()
    for plugin_manifest in PLUGINS_DIR.glob("*/openclaw.plugin.json"):
        try:
            data = json.loads(plugin_manifest.read_text(encoding="utf-8"))
            plugin_id = data.get("id", "")
            if plugin_id:
                discovered.add(plugin_id)
        except (OSError, json.JSONDecodeError):
            continue
    return discovered


def validate() -> int:
    """Run validation and return exit code (0 PASS, 1 FAIL)."""
    if not OPENCLAW_EXAMPLE_PATH.exists():
        logger.error("config/openclaw.json.example not found at %s", OPENCLAW_EXAMPLE_PATH)
        return 1

    try:
        config = json.loads(OPENCLAW_EXAMPLE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        logger.error("config/openclaw.json.example is not valid JSON: %s", exc)
        return 1

    plugins_block = config.get("plugins", {})
    if not isinstance(plugins_block, dict):
        logger.error("`plugins` block in config is not an object")
        return 1

    allow_list = plugins_block.get("allow", [])
    if not isinstance(allow_list, list):
        logger.error("`plugins.allow` is not a list")
        return 1
    allow_set = set(allow_list)

    entries = plugins_block.get("entries", {})
    if not isinstance(entries, dict):
        logger.error("`plugins.entries` is not an object")
        return 1

    akos_plugins = _discover_akos_plugins()
    errors: list[str] = []
    warnings: list[str] = []

    for required in sorted(REQUIRED_AKOS_PINNED_PLUGINS):
        if required not in allow_set:
            errors.append(
                f"Required AKOS-pinned plugin '{required}' missing from plugins.allow "
                f"(D-IH-87-B)"
            )

    for entry in allow_list:
        if entry in akos_plugins:
            continue
        if entry in KNOWN_THIRD_PARTY_PLUGINS:
            continue
        warnings.append(
            f"Unknown plugin '{entry}' in plugins.allow — not in openclaw-plugins/ "
            f"or KNOWN_THIRD_PARTY_PLUGINS allow-list constant"
        )

    for entry_id in entries:
        if entry_id not in allow_set:
            errors.append(
                f"Plugin '{entry_id}' has plugins.entries config but is not in plugins.allow "
                f"(orphan configuration)"
            )

    for warning in warnings:
        logger.warning("%s", warning)

    if errors:
        for error in errors:
            logger.error("%s", error)
        logger.error(
            "FAIL: validate_openclaw_plugin_pinning — %d error(s), %d warning(s)",
            len(errors),
            len(warnings),
        )
        return 1

    logger.info(
        "PASS: validate_openclaw_plugin_pinning — %d plugin(s) in allow-list "
        "(%d AKOS-pinned, %d third-party, %d unknown advisory)",
        len(allow_list),
        len([p for p in allow_list if p in akos_plugins]),
        len([p for p in allow_list if p in KNOWN_THIRD_PARTY_PLUGINS]),
        len(warnings),
    )
    return 0


def main() -> int:
    return validate()


if __name__ == "__main__":
    sys.exit(main())
