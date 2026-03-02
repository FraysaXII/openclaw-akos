"""Shared I/O utilities for AKOS scripts.

Single source of truth for JSON handling, config merging, and path resolution.
All scripts import from here -- never duplicate these helpers.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path) -> dict | list:
    """Load and parse a JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict | list) -> None:
    """Write data to a JSON file with consistent formatting."""
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def deep_merge(base: dict, overlay: dict) -> dict:
    """Recursively merge *overlay* into *base*. Overlay values win."""
    result = base.copy()
    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def resolve_openclaw_home() -> Path:
    """Return the OpenCLAW home directory, respecting OPENCLAW_HOME env var."""
    env_home = os.environ.get("OPENCLAW_HOME")
    if env_home:
        return Path(env_home)
    return Path.home() / ".openclaw"
