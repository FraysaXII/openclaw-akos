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
    "ORCHESTRATOR": "workspace-orchestrator",
    "ARCHITECT": "workspace-architect",
    "EXECUTOR": "workspace-executor",
    "VERIFIER": "workspace-verifier",
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


def load_env_file(path: Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE env file into a dict, skipping comments and blanks."""
    result: dict[str, str] = {}
    if not path.exists():
        logger.warning("Env file not found: %s", path)
        return result
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            result[key] = value
    return result


def get_variant_for_model(
    registry: ModelTiersRegistry, model_id: str, default: str = "compact"
) -> str:
    """Look up the prompt variant for *model_id*, returning *default* if unknown."""
    tier_result = registry.lookup_tier(model_id)
    if tier_result:
        return tier_result[1].promptVariant
    return default


def resolve_workspace_path(subpath: str) -> str:
    """Return the OS-appropriate absolute path for a workspace sub-path.

    Resolves paths relative to the OpenCLAW home directory, ensuring
    cross-platform compatibility (Windows, macOS, Linux).
    """
    oc_home = resolve_openclaw_home()
    return str(oc_home / subpath)


def resolve_mcporter_paths(config_text: str, repo_root: Path | None = None) -> str:
    """Replace Linux placeholder paths in mcporter JSON text with OS-correct values.

    Text-based (not dict-based) to preserve ``_note`` keys, formatting, and
    key ordering.  Idempotent: returns the input unchanged when no placeholders
    remain.  Longest match is replaced first to avoid partial substitution.
    """
    import re as _re

    root = repo_root or REPO_ROOT
    oc_home = resolve_openclaw_home()
    ws = (oc_home / "workspace").as_posix()
    exports = (oc_home / "workspace" / "exports").as_posix()
    akos_script = (root / "scripts" / "mcp_akos_server.py").as_posix()

    result = config_text
    result = result.replace("/opt/openclaw/workspace/exports", exports)
    result = result.replace("/opt/openclaw/workspace", ws)
    # Only replace the relative path when it is NOT already part of an absolute path.
    # Match "scripts/mcp_akos_server.py" only when NOT preceded by / or a drive letter.
    result = _re.sub(
        r'(?<![/\\A-Za-z])scripts/mcp_akos_server\.py',
        akos_script,
        result,
    )
    return result


def deploy_scaffold_files(oc_home: Path) -> list[Path]:
    """Copy workspace scaffold files (IDENTITY.md, MEMORY.md, etc.) to
    each agent workspace directory. Only copies files that don't already exist
    to avoid overwriting user customizations.

    Returns the list of newly deployed file paths.
    """
    scaffold_dir = REPO_ROOT / "config" / "workspace-scaffold"
    deployed: list[Path] = []

    agent_scaffold_map = {
        "ORCHESTRATOR": "orchestrator",
        "ARCHITECT": "architect",
        "EXECUTOR": "executor",
        "VERIFIER": "verifier",
    }

    for agent_key, scaffold_name in agent_scaffold_map.items():
        ws_dir_name = AGENT_WORKSPACES[agent_key]
        src_dir = scaffold_dir / scaffold_name
        dest_dir = oc_home / ws_dir_name

        if not src_dir.exists():
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)
        for src_file in src_dir.iterdir():
            if src_file.is_file():
                dest_file = dest_dir / src_file.name
                if not dest_file.exists():
                    shutil.copy2(src_file, dest_file)
                    logger.info("Scaffold: %s -> %s", src_file.name, dest_file)
                    deployed.append(dest_file)

    return deployed


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
