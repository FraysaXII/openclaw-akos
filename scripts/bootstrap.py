#!/usr/bin/env python3
"""Cross-platform bootstrap for OpenCLAW-AKOS.

Mirrors the phases of bootstrap.ps1 but works on Windows, macOS, and Linux
using only Python stdlib + subprocess.

Usage:
    python scripts/bootstrap.py
    python scripts/bootstrap.py --skip-ollama --skip-mcp
    python scripts/bootstrap.py --primary-model qwen3:8b --embed-model nomic-embed-text

Requires: Python 3.10+, Node.js >= 22, Ollama running.
"""

import argparse
import logging
import platform
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import (
    AGENT_WORKSPACES,
    REPO_ROOT,
    deep_merge,
    deploy_scaffold_files,
    deploy_soul_prompts,
    get_variant_for_model,
    load_json,
    resolve_openclaw_home,
    save_json,
)
from akos.log import setup_logging
from akos.models import load_tiers

logger = logging.getLogger("akos.bootstrap")

TIERS_PATH = REPO_ROOT / "config" / "model-tiers.json"
CONFIG_EXAMPLE = REPO_ROOT / "config" / "openclaw.json.example"
MCPORTER_EXAMPLE = REPO_ROOT / "config" / "mcporter.json.example"

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

    if not cmd_exists("openclaw"):
        status("WARN", "OpenCLAW CLI not in PATH. Install: curl -fsSL https://molt.bot/install.sh | bash")
    else:
        status("PASS", "OpenCLAW CLI found")

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

    save_json(oc_config, merged)
    status("PASS", f"Config written: {oc_config}")

    for ws_name in AGENT_WORKSPACES.values():
        ws_dir = oc_home / ws_name
        ws_dir.mkdir(parents=True, exist_ok=True)
    status("PASS", f"All {len(AGENT_WORKSPACES)} agent workspace directories created")

    scaffolded = deploy_scaffold_files(oc_home)
    if scaffolded:
        status("PASS", f"Deployed {len(scaffolded)} scaffold files to agent workspaces")
    else:
        status("SKIP", "Scaffold files already present in all workspaces")

    return True


# ── Phase 3: MCP Setup ─────────────────────────────────────────────────

def phase_mcp(args: argparse.Namespace) -> bool:
    status("INFO", "Phase 3: MCP server setup")

    if not cmd_exists("npx"):
        status("FAIL", "npx not found. Ensure Node.js is installed correctly.")
        return False

    mcporter_dir = Path.home() / ".mcporter"
    mcporter_config = mcporter_dir / "mcporter.json"

    if mcporter_config.exists():
        status("SKIP", f"mcporter.json already exists at {mcporter_config}")
    elif MCPORTER_EXAMPLE.exists():
        mcporter_dir.mkdir(parents=True, exist_ok=True)
        raw_text = MCPORTER_EXAMPLE.read_text(encoding="utf-8")
        oc_home = resolve_openclaw_home()
        ws_path = str(oc_home / "workspace").replace("\\", "/")
        exports_path = str(oc_home / "workspace" / "exports").replace("\\", "/")
        resolved_text = raw_text.replace("/opt/openclaw/workspace/exports", exports_path)
        resolved_text = resolved_text.replace("/opt/openclaw/workspace", ws_path)
        mcporter_config.write_text(resolved_text, encoding="utf-8")
        status("PASS", f"Deployed mcporter.json (paths resolved) to {mcporter_config}")
    else:
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
        print("    1. Start/restart the gateway:  openclaw gateway restart")
        print("    2. Open the dashboard:          openclaw dashboard")
        print("    3. Switch environments:          python scripts/switch-model.py <env-name>")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenCLAW-AKOS cross-platform bootstrap")
    parser.add_argument("--skip-wsl", action="store_true", help="Skip WSL2 checks (Windows)")
    parser.add_argument("--skip-ollama", action="store_true", help="Skip Ollama model setup")
    parser.add_argument("--skip-mcp", action="store_true", help="Skip MCP server setup")
    parser.add_argument("--primary-model", default="qwen3:8b", help="Primary LLM model (default: qwen3:8b)")
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
