#!/usr/bin/env python3
"""Cross-platform bootstrap for OpenCLAW-AKOS.

Mirrors the phases of bootstrap.ps1 but works on Windows, macOS, and Linux
using only Python stdlib + subprocess.

Usage:
    python scripts/bootstrap.py
    python scripts/bootstrap.py --skip-ollama --skip-mcp
    python scripts/bootstrap.py --primary-model deepseek-r1:14b --embed-model nomic-embed-text

Requires: Python 3.10+, Node.js >= 22, Ollama running.
"""

import argparse
import json
import logging
import os
import platform
import re
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import (
    AGENT_WORKSPACES,
    REPO_ROOT,
    RUNTIME_ENV_PLACEHOLDERS,
    deep_merge,
    deploy_openclaw_plugins,
    deploy_scaffold_files,
    deploy_soul_prompts,
    ensure_memory_journal_files,
    get_variant_for_model,
    load_env_file,
    load_json,
    resolve_mcporter_paths,
    resolve_openclaw_home,
    save_json,
)
from akos.log import setup_logging
from akos.models import load_tiers
from akos.policy import CapabilityMatrix
from akos.runtime import resolve_openclaw_cli
from akos.tools import GATEWAY_CORE_TOOLS

logger = logging.getLogger("akos.bootstrap")

TIERS_PATH = REPO_ROOT / "config" / "model-tiers.json"
CONFIG_EXAMPLE = REPO_ROOT / "config" / "openclaw.json.example"
CAPABILITIES_PATH = REPO_ROOT / "config" / "agent-capabilities.json"
MCPORTER_EXAMPLE = REPO_ROOT / "config" / "mcporter.json.example"


def _categories_to_profile(allowed_categories: list[str]) -> str:
    """Map AKOS allowed_categories to OpenClaw profile name."""
    if "write" in allowed_categories or "shell" in allowed_categories or "shell_limited" in allowed_categories:
        return "coding"
    return "minimal"


def _resolve_runtime_profile(policy) -> str:
    """Resolve the gateway runtime profile for a role policy."""
    if getattr(policy, "runtime_profile", None):
        return str(policy.runtime_profile)
    return _categories_to_profile(policy.allowed_categories)


def _sync_tool_profiles_from_capability_matrix(merged: dict) -> None:
    """Translate agent-capabilities.json into per-agent OpenClaw tools blocks.

    Gateway runtime semantics are curated in the committed template:
      - `profile` comes from the AKOS capability matrix.
      - `alsoAllow` and `deny` come from the gateway template SSOT.

    This keeps the capability matrix as the AKOS policy/audit authority while
    preserving the gateway-compatible tool names that OpenClaw actually
    recognizes at runtime.
    """
    if not CAPABILITIES_PATH.exists():
        logger.warning("Capability matrix not found at %s; skipping tool profile sync", CAPABILITIES_PATH)
        return

    matrix = CapabilityMatrix.load(CAPABILITIES_PATH)
    agents = merged.get("agents", {}).get("list", [])

    for agent in agents:
        agent_id = agent.get("id", "")
        policy = matrix.get_policy(agent_id)
        if not policy:
            continue

        profile = _resolve_runtime_profile(policy)
        existing_tools = agent.get("tools") or {}
        tools_block: dict[str, object] = {"profile": profile}

        if existing_tools.get("alsoAllow"):
            tools_block["alsoAllow"] = list(existing_tools["alsoAllow"])
        elif existing_tools.get("allow"):
            # Migrate legacy allowlists into the gateway-supported additive field.
            legacy_allow = list(existing_tools["allow"])
            unknown_legacy = [tool for tool in legacy_allow if tool not in GATEWAY_CORE_TOOLS]
            if unknown_legacy:
                logger.warning(
                    "Agent %s legacy allowlist contains non-core IDs; moving them to alsoAllow for compatibility: %s",
                    agent_id,
                    ", ".join(sorted(unknown_legacy)),
                )
            tools_block["alsoAllow"] = legacy_allow

        if existing_tools.get("deny"):
            tools_block["deny"] = list(existing_tools["deny"])

        agent["tools"] = tools_block

    status("PASS", "Tool profiles synced from capability matrix")

PASS_COUNT = 0
FAIL_COUNT = 0
SKIP_COUNT = 0
WARN_COUNT = 0


def status(level: str, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT, SKIP_COUNT, WARN_COUNT
    log_map = {"PASS": logger.info, "FAIL": logger.error, "SKIP": logger.warning,
               "WARN": logger.warning, "INFO": logger.info}
    log_fn = log_map.get(level, logger.info)
    log_fn(msg)
    if level == "PASS": PASS_COUNT += 1
    elif level == "FAIL": FAIL_COUNT += 1
    elif level == "SKIP": SKIP_COUNT += 1
    elif level == "WARN": WARN_COUNT += 1


import akos.process as proc


def cmd_exists(name: str) -> bool:
    return shutil.which(name) is not None


def get_node_version() -> tuple[int, ...] | None:
    result = proc.run(["node", "--version"], timeout=15)
    if result.success:
        version_str = result.stdout.strip().lstrip("v")
        try:
            return tuple(int(x) for x in version_str.split("."))
        except ValueError:
            return None
    return None


def ollama_is_running() -> bool:
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5):
            return True
    except (urllib.error.URLError, OSError):
        return False


# ── Phase 0: Preflight ──────────────────────────────────────────────────

def phase_preflight(args: argparse.Namespace) -> bool:
    status("INFO", "Phase 0: Preflight checks")

    os_name = platform.system()
    status("PASS", f"OS detected: {os_name} ({platform.release()})")

    if sys.version_info < (3, 10):
        status("FAIL", f"Python >= 3.10 required, found {sys.version}")
        return False
    status("PASS", f"Python {sys.version.split()[0]}")

    node_ver = get_node_version()
    if node_ver is None:
        status("FAIL", "Node.js not found. Install Node.js >= 22.")
        return False
    if node_ver[0] < 22:
        status("FAIL", f"Node.js >= 22 required, found {'.'.join(map(str, node_ver))}")
        return False
    status("PASS", f"Node.js {'.'.join(map(str, node_ver))}")

    oc_cli = resolve_openclaw_cli()
    if not oc_cli:
        status("WARN", "OpenCLAW CLI not in PATH. Install: curl -fsSL https://molt.bot/install.sh | bash")
    else:
        status("PASS", f"OpenCLAW CLI found ({oc_cli})")

    if os_name == "Windows" and not args.skip_wsl:
        result = proc.run(["wsl", "--status"], timeout=15)
        if result.success:
            status("PASS", "WSL2 available")
        else:
            status("WARN", "WSL2 not detected. Consider: wsl --install -d Ubuntu-24.04")

    return True


# ── Phase 1: Ollama Models ──────────────────────────────────────────────

def phase_ollama(args: argparse.Namespace) -> bool:
    status("INFO", "Phase 1: Ollama model setup")

    if not ollama_is_running():
        status("FAIL", "Ollama not running at 127.0.0.1:11434. Start Ollama first.")
        return False
    status("PASS", "Ollama is running")

    for model in [args.primary_model, args.embed_model]:
        status("INFO", f"Pulling model: {model}")
        result = proc.run(["ollama", "pull", model], timeout=300, capture=False)
        if result.success:
            status("PASS", f"Model ready: {model}")
        else:
            status("WARN", f"Could not pull {model}. It may already be available locally.")

    return True


# ── Phase 2: OpenCLAW Config ────────────────────────────────────────────

def _collect_unresolved_provider_inputs(config: dict) -> list[str]:
    """Return unresolved provider env inputs without mutating provider inventory."""
    providers = config.get("models", {}).get("providers", {})
    issues: list[str] = []
    for name, block in list(providers.items()):
        base_url = block.get("baseUrl", "")
        if isinstance(base_url, str) and "${" in base_url:
            match = re.search(r"\$\{(\w+)\}", base_url)
            if match and not os.environ.get(match.group(1)):
                issues.append(f"{name}.baseUrl references unset env var {match.group(1)}")
        api_key = block.get("apiKey", {})
        if isinstance(api_key, dict) and api_key.get("source") == "env":
            env_id = api_key.get("id", "")
            if env_id and not os.environ.get(env_id):
                issues.append(f"{name}.apiKey references unset env var {env_id}")
    return issues


def _seed_env_file_if_missing(oc_home: Path) -> None:
    """Materialize ``~/.openclaw/.env`` with safe placeholder defaults.

    Runtime flows must not read ``*.env.example`` files. Bootstrap therefore
    creates a real env file from the shared placeholder contract when no live
    runtime env exists yet.
    """
    env_dest = oc_home / ".env"
    if env_dest.exists():
        return
    lines = [f"{key}={value}" for key, value in RUNTIME_ENV_PLACEHOLDERS.items()]
    env_dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    status(
        "PASS",
        f"Seeded {env_dest} with runtime placeholder defaults "
        "(run switch-model.py to select a real environment profile)",
    )


def _backfill_env_placeholders(oc_home: Path) -> None:
    """Ensure existing ``~/.openclaw/.env`` contains all required placeholders."""
    env_dest = oc_home / ".env"
    if not env_dest.exists():
        return

    current = load_env_file(env_dest)
    added = 0
    lines = env_dest.read_text(encoding="utf-8").splitlines()
    for key, value in RUNTIME_ENV_PLACEHOLDERS.items():
        if key not in current or current[key] == "":
            lines.append(f"{key}={value}")
            added += 1
    if added:
        env_dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
        status("PASS", f"Backfilled {added} missing env placeholder(s) into {env_dest}")


def _extract_akos_keys(config: dict) -> dict:
    """Remove AKOS-specific keys that OpenClaw doesn't recognize and return them
    as a separate dict for sidecar storage."""
    akos_keys = {}
    for key in ["logging", "permissions"]:
        if key in config:
            akos_keys[key] = config.pop(key)
    diagnostics = config.get("diagnostics")
    if isinstance(diagnostics, dict) and "logWatcher" in diagnostics:
        akos_keys.setdefault("diagnostics", {})["logWatcher"] = diagnostics.pop("logWatcher")
        if not diagnostics:
            config.pop("diagnostics", None)
    gw = config.get("gateway", {})
    if "host" in gw:
        akos_keys.setdefault("gateway", {})["host"] = gw.pop("host")
        if not gw:
            config.pop("gateway", None)
    return akos_keys


def phase_config(args: argparse.Namespace) -> bool:
    status("INFO", "Phase 2: OpenCLAW configuration")

    oc_home = resolve_openclaw_home()
    oc_home.mkdir(parents=True, exist_ok=True)
    status("PASS", f"OpenCLAW home: {oc_home}")

    oc_config = oc_home / "openclaw.json"
    if oc_config.exists():
        backup = oc_config.with_suffix(".json.bootstrap-bak")
        shutil.copy2(oc_config, backup)
        status("PASS", f"Backed up existing config to {backup.name}")
        existing = load_json(oc_config)
    else:
        existing = {}

    template = load_json(CONFIG_EXAMPLE)
    merged = deep_merge(existing, template)

    model_id = f"ollama/{args.primary_model}"
    merged.setdefault("agents", {}).setdefault("defaults", {})
    merged["agents"]["defaults"]["model"] = {"primary": model_id}

    registry = load_tiers(TIERS_PATH)
    tier_result = registry.lookup_tier(model_id)
    if tier_result:
        tier_name, tier_data = tier_result
        merged["agents"]["defaults"]["thinkingDefault"] = tier_data.thinkingDefault
        status("PASS", f"Model tier: {tier_name} (thinkingDefault={tier_data.thinkingDefault})")
    else:
        status("WARN", f"Model '{model_id}' not in model-tiers.json; using template defaults")

    # Fix 2: Force-sync agents.list from template to ensure all 5 agents
    if "agents" in template and "list" in template["agents"]:
        merged["agents"]["list"] = template["agents"]["list"]
        agent_names = [a.get("id", "?") for a in merged["agents"]["list"]]
        status("PASS", f"Agents synced: {', '.join(agent_names)}")

    if "models" in template and "providers" in template["models"]:
        merged.setdefault("models", {})
        merged["models"]["providers"] = json.loads(json.dumps(template["models"]["providers"]))
        status("PASS", "Providers synced to strict full inventory contract")

    unresolved_inputs = _collect_unresolved_provider_inputs(merged)
    if unresolved_inputs:
        for issue in unresolved_inputs:
            status("WARN", f"Provider input unresolved (provider retained): {issue}")
        _seed_env_file_if_missing(oc_home)
        _backfill_env_placeholders(oc_home)
    else:
        status("PASS", "All provider env-backed inputs resolved or intentionally empty")

    # Fix 2b: Sync per-agent tool profiles from capability matrix
    _sync_tool_profiles_from_capability_matrix(merged)

    # Fix 3: Extract AKOS-specific keys into sidecar file
    akos_keys = _extract_akos_keys(merged)
    if akos_keys:
        sidecar = oc_home / "akos-config.json"
        save_json(sidecar, akos_keys)
        status("PASS", f"AKOS-specific keys saved to {sidecar.name}")

    save_json(oc_config, merged)
    status("PASS", f"Config written: {oc_config}")

    # Create agent workspace directories
    for ws_name in AGENT_WORKSPACES.values():
        ws_dir = oc_home / ws_name
        ws_dir.mkdir(parents=True, exist_ok=True)
    status("PASS", f"All {len(AGENT_WORKSPACES)} agent workspace directories created")

    # Fix 4: Create session directories for all agents
    for agent_id in AGENT_WORKSPACES:
        sessions_dir = oc_home / "agents" / agent_id.lower() / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
    status("PASS", "Agent session directories created")

    scaffolded = deploy_scaffold_files(oc_home)
    if scaffolded:
        status("PASS", f"Deployed {len(scaffolded)} scaffold files to agent workspaces")
    else:
        status("SKIP", "Scaffold files already present in all workspaces")

    journaled = ensure_memory_journal_files(oc_home)
    if journaled:
        status("PASS", f"Created {len(journaled)} workspace memory continuity journals")
    else:
        status("SKIP", "Workspace memory continuity journals already present")

    deployed_plugins = deploy_openclaw_plugins(oc_home)
    if deployed_plugins:
        status("PASS", f"Synced {len(deployed_plugins)} OpenClaw plugin files")
    else:
        status("SKIP", "OpenClaw plugin files already match repo state")

    return True


# ── Phase 3: MCP Setup ─────────────────────────────────────────────────

def phase_mcp(args: argparse.Namespace) -> bool:
    status("INFO", "Phase 3: MCP server setup")

    if not cmd_exists("npx"):
        status("FAIL", "npx not found. Ensure Node.js is installed correctly.")
        return False

    mcporter_dir = Path.home() / ".mcporter"
    mcporter_config = mcporter_dir / "mcporter.json"

    if MCPORTER_EXAMPLE.exists():
        raw_text = MCPORTER_EXAMPLE.read_text(encoding="utf-8")
        resolved_text = resolve_mcporter_paths(raw_text)
        if mcporter_config.exists():
            existing = mcporter_config.read_text(encoding="utf-8")
            if existing != resolved_text:
                mcporter_dir.mkdir(parents=True, exist_ok=True)
                mcporter_config.write_text(resolved_text, encoding="utf-8")
                status("PASS", f"Refreshed mcporter.json from repo template at {mcporter_config}")
            else:
                status("SKIP", f"mcporter.json already matches resolved repo template at {mcporter_config}")
        else:
            mcporter_dir.mkdir(parents=True, exist_ok=True)
            mcporter_config.write_text(resolved_text, encoding="utf-8")
            status("PASS", f"Deployed mcporter.json (paths resolved) to {mcporter_config}")
    else:
        if mcporter_config.exists():
            raw = mcporter_config.read_text(encoding="utf-8")
            resolved = resolve_mcporter_paths(raw)
            if raw != resolved:
                mcporter_config.write_text(resolved, encoding="utf-8")
                status("PASS", f"Re-resolved mcporter.json paths at {mcporter_config}")
            else:
                status("SKIP", f"mcporter.json already resolved at {mcporter_config}")
    if not MCPORTER_EXAMPLE.exists() and not mcporter_config.exists():
        status("WARN", "mcporter.json.example not found in repo; skipping MCP config")
    return True


# ── Phase 4: Prompt Assembly ────────────────────────────────────────────

def phase_prompts(args: argparse.Namespace) -> bool:
    status("INFO", "Phase 4: Prompt assembly")

    assemble_script = REPO_ROOT / "scripts" / "assemble-prompts.py"
    if not assemble_script.exists():
        status("FAIL", f"assemble-prompts.py not found at {assemble_script}")
        return False

    result = proc.run([sys.executable, str(assemble_script)], timeout=60, capture=False)
    if result.success:
        status("PASS", "All prompt variants assembled")
    else:
        status("FAIL", "Prompt assembly failed")
        return False

    oc_home = resolve_openclaw_home()
    model_id = f"ollama/{args.primary_model}"
    registry = load_tiers(TIERS_PATH)
    variant = get_variant_for_model(registry, model_id, default="compact")

    status("PASS", f"Deploying prompt variant: {variant}")

    assembled_dir = REPO_ROOT / "prompts" / "assembled"
    try:
        deployed = deploy_soul_prompts(assembled_dir, variant, oc_home)
        for p in deployed:
            status("PASS", f"Deployed SOUL.md -> {p}")
    except FileNotFoundError as exc:
        status("FAIL", str(exc))
        return False

    return True


# ── Phase 5: Summary ───────────────────────────────────────────────────

def phase_summary() -> None:
    print()
    print("=" * 60)
    print(f"  PASS: {PASS_COUNT}  |  FAIL: {FAIL_COUNT}  |  SKIP: {SKIP_COUNT}  |  WARN: {WARN_COUNT}")
    print("=" * 60)

    if FAIL_COUNT > 0:
        print("\n  Some checks failed. Review the output above and fix issues.")
        print("  Re-run this script after fixing.")
    else:
        print("\n  Bootstrap complete! Next steps:")
        print("    1. Repair/start the gateway:    py scripts/doctor.py --repair-gateway")
        print("    2. Open the dashboard:          openclaw dashboard")
        print("    3. Switch environments:         python scripts/switch-model.py <env-name>")
        print("    4. Control plane (+ optional graph UI): py scripts/serve-api.py")
        print("       (Neo4j optional: compose or Aura + ~/.openclaw/.env; see USER_GUIDE §9.10)")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenCLAW-AKOS cross-platform bootstrap")
    parser.add_argument("--skip-wsl", action="store_true", help="Skip WSL2 checks (Windows)")
    parser.add_argument("--skip-ollama", action="store_true", help="Skip Ollama model setup")
    parser.add_argument("--skip-mcp", action="store_true", help="Skip MCP server setup")
    parser.add_argument("--primary-model", default="deepseek-r1:14b", help="Primary LLM model (default: deepseek-r1:14b)")
    parser.add_argument("--embed-model", default="nomic-embed-text", help="Embedding model (default: nomic-embed-text)")
    parser.add_argument("--json-log", action="store_true", help="Emit structured JSON logs (for CI/aggregation)")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    logger.info("OpenCLAW-AKOS Bootstrap")
    logger.info("Platform: %s %s", platform.system(), platform.release())
    logger.info("Python:   %s", sys.version.split()[0])

    if not phase_preflight(args):
        phase_summary()
        sys.exit(1)

    if not args.skip_ollama:
        if not phase_ollama(args):
            phase_summary()
            sys.exit(1)
    else:
        status("SKIP", "Phase 1: Ollama (--skip-ollama)")

    if not phase_config(args):
        phase_summary()
        sys.exit(1)

    if not args.skip_mcp:
        if not phase_mcp(args):
            phase_summary()
            sys.exit(1)
    else:
        status("SKIP", "Phase 3: MCP (--skip-mcp)")

    if not phase_prompts(args):
        phase_summary()
        sys.exit(1)

    phase_summary()
    sys.exit(1 if FAIL_COUNT > 0 else 0)


if __name__ == "__main__":
    main()
