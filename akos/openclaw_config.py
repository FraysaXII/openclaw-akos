"""OpenClaw operator-local config normalization (AKOS adapter layer).

Maps AKOS SSOT semantics onto the installed OpenClaw CLI schema without
requiring operators to hand-edit ``~/.openclaw/openclaw.json`` when upstream
enum values change (e.g. ``sandbox.mode: strict`` rejected by OpenClaw 2026.4.x).
"""

from __future__ import annotations

import copy
import logging
from pathlib import Path
from typing import Any

from akos.docker_engine_probe import probe_docker_engine
from akos.io import load_json, resolve_openclaw_home, save_json

logger = logging.getLogger("akos.openclaw_config")

# OpenClaw 2026.4.x CLI allowed values (see upstream gateway config schema).
OPENCLAW_SANDBOX_MODES = frozenset({"off", "non-main", "all"})

# AKOS Path B legacy label → upstream enum (I87/I90 gateway tranche).
LEGACY_SANDBOX_MODE_MAP: dict[str, str] = {
    "strict": "all",
}

EXEC_HOSTS = frozenset({"gateway", "sandbox", "node"})


def normalize_openclaw_config_dict(config: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Return a copy of ``config`` with AKOS→OpenClaw schema alignment applied.

    Changes are recorded as human-readable strings for operator logs.
    """
    out = copy.deepcopy(config)
    notes: list[str] = []

    agents = out.setdefault("agents", {})
    defaults = agents.setdefault("defaults", {})
    sandbox = defaults.get("sandbox")
    if not isinstance(sandbox, dict):
        sandbox = {}
        defaults["sandbox"] = sandbox

    mode = sandbox.get("mode")
    if isinstance(mode, str):
        mapped = LEGACY_SANDBOX_MODE_MAP.get(mode.strip().lower())
        if mapped and mapped != mode:
            sandbox["mode"] = mapped
            notes.append(f"agents.defaults.sandbox.mode: {mode!r} → {mapped!r} (AKOS legacy→OpenClaw schema)")
        elif mode not in OPENCLAW_SANDBOX_MODES:
            sandbox["mode"] = "off"
            notes.append(
                f"agents.defaults.sandbox.mode: invalid {mode!r} → 'off' "
                f"(allowed: {', '.join(sorted(OPENCLAW_SANDBOX_MODES))})"
            )

    effective_mode = str(sandbox.get("mode") or "off").lower()
    tools = out.setdefault("tools", {})
    exec_cfg = tools.setdefault("exec", {})
    host = exec_cfg.get("host")

    if effective_mode == "off":
        if host != "gateway":
            exec_cfg["host"] = "gateway"
            notes.append(f"tools.exec.host: {host!r} → 'gateway' (sandbox.mode is off)")
    elif effective_mode in {"all", "non-main"}:
        docker_ok, _ = probe_docker_engine(timeout_sec=1.5)
        desired = "sandbox" if docker_ok else "gateway"
        if host != desired:
            exec_cfg["host"] = desired
            if docker_ok:
                notes.append(f"tools.exec.host: {host!r} → 'sandbox' (Path B; Docker engine reachable)")
            else:
                notes.append(
                    f"tools.exec.host: {host!r} → 'gateway' "
                    f"(sandbox.mode={effective_mode!r} but Docker engine unreachable on this host)"
                )

    if isinstance(host, str) and host not in EXEC_HOSTS:
        exec_cfg["host"] = "gateway"
        notes.append(f"tools.exec.host: invalid {host!r} → 'gateway'")

    return out, notes


def apply_normalize_to_user_config(
    oc_home: Path | None = None,
    *,
    dry_run: bool = False,
) -> tuple[bool, list[str]]:
    """Load ``openclaw.json`` from the operator home, normalize, and save if changed."""
    home = oc_home or resolve_openclaw_home()
    path = home / "openclaw.json"
    if not path.is_file():
        return False, [f"skip: {path} not found"]

    raw = load_json(path)
    if not isinstance(raw, dict):
        return False, [f"skip: {path} is not a JSON object"]

    normalized, notes = normalize_openclaw_config_dict(raw)
    if not notes:
        return False, ["no changes required"]

    if not dry_run:
        backup = path.with_suffix(".json.akos-normalize-bak")
        if not backup.exists():
            backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        save_json(path, normalized)
        logger.info("Normalized %s (%d change(s))", path, len(notes))

    return True, notes
