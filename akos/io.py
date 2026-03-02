"""Shared I/O utilities for AKOS scripts.

Single source of truth for JSON handling, config merging, path resolution,
and prompt deployment.  All scripts import from here -- never duplicate these
helpers.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from akos.models import ModelTiersRegistry

REPO_ROOT = Path(__file__).resolve().parent.parent

logger = logging.getLogger("akos.io")

AGENT_WORKSPACES: dict[str, str] = {
    "ARCHITECT": "workspace-architect",
    "EXECUTOR": "workspace-executor",
}


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


def get_variant_for_model(
    registry: ModelTiersRegistry, model_id: str, default: str = "compact"
) -> str:
    """Look up the prompt variant for *model_id*, returning *default* if unknown."""
    tier_result = registry.lookup_tier(model_id)
    if tier_result:
        return tier_result[1].promptVariant
    return default


def deploy_soul_prompts(
    assembled_dir: Path, variant: str, oc_home: Path
) -> list[Path]:
    """Copy assembled SOUL.md prompt variants to their agent workspaces.

    Returns the list of destination paths that were written.
    Raises ``FileNotFoundError`` if an expected assembled file is missing.
    """
    deployed: list[Path] = []
    for agent, ws_dir_name in AGENT_WORKSPACES.items():
        src = assembled_dir / f"{agent}_PROMPT.{variant}.md"
        if not src.exists():
            raise FileNotFoundError(
                f"Assembled prompt not found: {src}. "
                "Run: python scripts/assemble-prompts.py"
            )
        dest = oc_home / ws_dir_name / "SOUL.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        logger.info("Deployed %s -> %s", src.name, dest)
        deployed.append(dest)
    return deployed
