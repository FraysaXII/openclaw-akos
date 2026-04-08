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
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from akos.models import ModelTiersRegistry

REPO_ROOT = Path(__file__).resolve().parent.parent

logger = logging.getLogger("akos.io")

OPENCLAW_PLUGIN_SOURCE_ROOT = REPO_ROOT / "openclaw-plugins"
MANAGED_OPENCLAW_PLUGIN_IDS = ("akos-runtime-tools",)
AKOS_SIDECAR_PATH = "akos-config.json"

AGENT_WORKSPACES: dict[str, str] = {
    "ORCHESTRATOR": "workspace-orchestrator",
    "ARCHITECT": "workspace-architect",
    "EXECUTOR": "workspace-executor",
    "VERIFIER": "workspace-verifier",
    "MADEIRA": "workspace-madeira",
}

RUNTIME_ENV_PLACEHOLDERS: dict[str, str] = {
    "OLLAMA_API_KEY": "ollama-local",
    "OLLAMA_GPU_URL": "http://127.0.0.1:11434",
    "OPENAI_API_KEY": "not-configured",
    "ANTHROPIC_API_KEY": "not-configured",
    "VLLM_RUNPOD_URL": "http://localhost:8000/v1",
    "RUNPOD_API_KEY": "not-configured",
    "VLLM_SHADOW_URL": "http://localhost:8080/v1",
    "LANGFUSE_PUBLIC_KEY": "your-public-key-here",
    "LANGFUSE_SECRET_KEY": "your-secret-key-here",
    "LANGFUSE_HOST": "https://cloud.langfuse.com",
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
    """Parse a simple KEY=VALUE env file into a dict, skipping comments and blanks.

    Raises ``ValueError`` when a non-comment, non-empty line is malformed so
    secret/config loading failures do not silently degrade.
    """
    result: dict[str, str] = {}
    if not path.exists():
        logger.warning("Env file not found: %s", path)
        return result
    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Malformed env line {lineno} in {path}: missing '='")
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            result[key] = value
    return result


def load_runtime_env(oc_home: Path | None = None) -> dict[str, str]:
    """Load the canonical runtime env from ``~/.openclaw/.env``."""
    home = oc_home or resolve_openclaw_home()
    return load_env_file(home / ".env")


def set_process_env_defaults(values: dict[str, str]) -> None:
    """Populate unset process env vars from *values*, skipping empty entries."""
    for key, value in values.items():
        if value and key not in os.environ:
            os.environ[key] = value


def load_akos_sidecar_config(oc_home: Path | None = None) -> dict:
    """Load the AKOS sidecar config from ``~/.openclaw/akos-config.json``."""
    home = oc_home or resolve_openclaw_home()
    sidecar = home / AKOS_SIDECAR_PATH
    if not sidecar.exists():
        return {}
    return load_json(sidecar)


def get_log_watcher_settings(oc_home: Path | None = None) -> dict:
    """Return the operator-facing log watcher settings from AKOS sidecar config."""
    config = load_akos_sidecar_config(oc_home)
    diagnostics = config.get("diagnostics", {})
    if not isinstance(diagnostics, dict):
        return {}
    watcher = diagnostics.get("logWatcher", {})
    return watcher if isinstance(watcher, dict) else {}


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

    Any repo-local ``scripts/<name>.py`` reference is resolved to an absolute
    path under *repo_root* so that bootstrap works for all custom MCP servers.
    """
    import re as _re

    root = repo_root or REPO_ROOT
    oc_home = resolve_openclaw_home()
    ws = (oc_home / "workspace").as_posix()
    exports = (oc_home / "workspace" / "exports").as_posix()
    python_executable = Path(sys.executable).as_posix()

    result = config_text
    result = result.replace("/opt/openclaw/workspace/exports", exports)
    result = result.replace("/opt/openclaw/workspace", ws)
    result = _re.sub(
        r'("command"\s*:\s*)"python"',
        rf'\1"{python_executable}"',
        result,
    )

    def _resolve_script(match: _re.Match[str]) -> str:
        script_name = match.group(1)
        return (root / "scripts" / script_name).as_posix()

    result = _re.sub(
        r'(?<![/\\A-Za-z])scripts/(\w+\.py)',
        _resolve_script,
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
        "MADEIRA": "madeira",
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


def ensure_memory_journal_files(oc_home: Path, *, days: int = 2) -> list[Path]:
    """Ensure each workspace with a MEMORY.md has dated continuity notes.

    OpenClaw's post-compaction audit may ask agents to re-read recent memory
    journal files under ``memory/YYYY-MM-DD.md`` after a context reset.  AKOS
    creates those deterministic files from the workspace ``MEMORY.md`` so the
    runtime contract is procedural instead of relying on ad-hoc model behavior.
    """

    deployed: list[Path] = []
    today = date.today()

    for ws_dir_name in AGENT_WORKSPACES.values():
        ws_dir = oc_home / ws_dir_name
        memory_src = ws_dir / "MEMORY.md"
        if not memory_src.is_file():
            continue

        memory_dir = ws_dir / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)
        base_text = memory_src.read_text(encoding="utf-8").rstrip()

        for offset in range(days):
            journal_date = today - timedelta(days=offset)
            journal_path = memory_dir / f"{journal_date.isoformat()}.md"
            if journal_path.exists():
                continue

            header = (
                f"# Memory Continuity Note - {journal_date.isoformat()}\n\n"
                "Bootstrap-generated continuity mirror for post-compaction startup recovery.\n"
                "Use as supporting session context only. The canonical business truth remains\n"
                "the HLK vault and other governed assets.\n\n"
            )
            journal_path.write_text(header + base_text + "\n", encoding="utf-8")
            logger.info("Memory journal: %s", journal_path)
            deployed.append(journal_path)

    return deployed


def deploy_openclaw_plugins(
    oc_home: Path, plugin_source_root: Path | None = None
) -> list[Path]:
    """Sync repo-managed OpenClaw plugins into the live OpenClaw extensions dir.

    These plugins are part of the AKOS runtime contract, so bootstrap keeps the
    deployed copy in sync with the repo version instead of treating them as
    user-customized workspace files.
    """

    source_root = plugin_source_root or OPENCLAW_PLUGIN_SOURCE_ROOT
    if not source_root.exists():
        return []

    dest_root = oc_home / "extensions"
    deployed: list[Path] = []

    for plugin_dir in sorted(p for p in source_root.iterdir() if p.is_dir()):
        target_dir = dest_root / plugin_dir.name
        target_dir.mkdir(parents=True, exist_ok=True)

        for src_path in sorted(plugin_dir.rglob("*")):
            rel_path = src_path.relative_to(plugin_dir)
            dest_path = target_dir / rel_path

            if src_path.is_dir():
                dest_path.mkdir(parents=True, exist_ok=True)
                continue

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            src_bytes = src_path.read_bytes()
            if dest_path.exists() and dest_path.read_bytes() == src_bytes:
                continue

            dest_path.write_bytes(src_bytes)
            logger.info("Plugin: %s -> %s", src_path.name, dest_path)
            deployed.append(dest_path)

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
