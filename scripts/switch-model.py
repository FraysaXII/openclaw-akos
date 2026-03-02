#!/usr/bin/env python3
"""Switch the active model/environment for the AKOS OpenCLAW deployment.

Activates an environment profile by:
  1. Copying the .env file to ~/.openclaw/.env
  2. Deep-merging the JSON overlay into ~/.openclaw/openclaw.json
  3. Looking up the model tier from config/model-tiers.json
  4. Deploying the correct assembled SOUL.md variant to agent workspaces
  5. Restarting the OpenCLAW gateway

Usage:
    python scripts/switch-model.py dev-local
    python scripts/switch-model.py gpu-runpod
    python scripts/switch-model.py prod-cloud --dry-run

Requires: Python 3.10+ (stdlib + pydantic).
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT, deep_merge, load_json, resolve_openclaw_home, save_json
from akos.models import load_tiers

TIERS_PATH = REPO_ROOT / "config" / "model-tiers.json"
ENVS_DIR = REPO_ROOT / "config" / "environments"
ASSEMBLED_DIR = REPO_ROOT / "prompts" / "assembled"


def find_env_file(env_name: str) -> Path | None:
    real_env = ENVS_DIR / f"{env_name}.env"
    if real_env.exists():
        return real_env
    example_env = ENVS_DIR / f"{env_name}.env.example"
    if example_env.exists():
        return example_env
    return None


def main():
    parser = argparse.ArgumentParser(description="Switch AKOS model/environment")
    parser.add_argument("environment", help="Environment name (e.g., dev-local, gpu-runpod, prod-cloud)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--no-restart", action="store_true", help="Skip gateway restart")
    args = parser.parse_args()

    env_name = args.environment
    oc_home = resolve_openclaw_home()

    overlay_path = ENVS_DIR / f"{env_name}.json"
    if not overlay_path.exists():
        print(f"ERROR: environment overlay not found: {overlay_path}", file=sys.stderr)
        print(f"Available environments: {', '.join(p.stem for p in ENVS_DIR.glob('*.json'))}")
        sys.exit(1)

    env_file = find_env_file(env_name)
    overlay = load_json(overlay_path)
    registry = load_tiers(TIERS_PATH)

    model_id = overlay.get("agents", {}).get("defaults", {}).get("model", {}).get("primary")
    if not model_id:
        print("ERROR: overlay does not specify agents.defaults.model.primary", file=sys.stderr)
        sys.exit(1)

    tier_result = registry.lookup_tier(model_id)
    if tier_result:
        tier_name, tier_data = tier_result
        variant = tier_data.promptVariant
    else:
        print(f"WARNING: model '{model_id}' not found in model-tiers.json, defaulting to 'full' variant")
        tier_name = "unknown"
        variant = "full"

    print(f"Environment:  {env_name}")
    print(f"Model:        {model_id}")
    print(f"Tier:         {tier_name}")
    print(f"Variant:      {variant}")
    print(f"OpenCLAW Home: {oc_home}")
    print()

    # Step 1: Copy .env
    if env_file:
        dest_env = oc_home / ".env"
        if args.dry_run:
            print(f"[DRY-RUN] Would copy {env_file.name} -> {dest_env}")
        else:
            oc_home.mkdir(parents=True, exist_ok=True)
            shutil.copy2(env_file, dest_env)
            print(f"[OK] Copied {env_file.name} -> {dest_env}")
    else:
        print(f"[SKIP] No .env file for '{env_name}' (neither .env nor .env.example found)")

    # Step 2: Deep-merge JSON overlay into openclaw.json
    oc_config_path = oc_home / "openclaw.json"
    if oc_config_path.exists():
        existing = load_json(oc_config_path)
        merged = deep_merge(existing, overlay)
        if args.dry_run:
            print(f"[DRY-RUN] Would merge {overlay_path.name} into {oc_config_path}")
            diff_keys = list(overlay.keys())
            print(f"          Overlay top-level keys: {diff_keys}")
        else:
            backup = oc_config_path.with_suffix(".json.bak")
            shutil.copy2(oc_config_path, backup)
            save_json(oc_config_path, merged)
            print(f"[OK] Merged {overlay_path.name} into {oc_config_path} (backup: {backup.name})")
    else:
        print(f"[SKIP] {oc_config_path} does not exist; run bootstrap first")

    # Step 3: Deploy assembled SOUL.md variants
    workspaces = {
        "ARCHITECT": oc_home / "workspace-architect" / "SOUL.md",
        "EXECUTOR": oc_home / "workspace-executor" / "SOUL.md",
    }
    for agent, soul_dest in workspaces.items():
        assembled_name = f"{agent}_PROMPT.{variant}.md"
        assembled_path = ASSEMBLED_DIR / assembled_name
        if not assembled_path.exists():
            print(f"[ERROR] Assembled prompt not found: {assembled_path}")
            print(f"        Run: python scripts/assemble-prompts.py")
            sys.exit(1)

        if args.dry_run:
            print(f"[DRY-RUN] Would copy {assembled_name} -> {soul_dest}")
        else:
            soul_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(assembled_path, soul_dest)
            print(f"[OK] Deployed {assembled_name} -> {soul_dest}")

    # Step 4: Restart gateway
    if not args.no_restart and not args.dry_run:
        print()
        print("Restarting OpenCLAW gateway...")
        try:
            subprocess.run(["openclaw", "gateway", "restart"], check=True)
            print("[OK] Gateway restarted.")
        except FileNotFoundError:
            print("[SKIP] 'openclaw' command not found in PATH; restart manually.")
        except subprocess.CalledProcessError as e:
            print(f"[WARNING] Gateway restart returned exit code {e.returncode}")

    print()
    tag = "[DRY-RUN] " if args.dry_run else ""
    print(f"{tag}Switched to {model_id} ({tier_name}) in {env_name} environment.")


if __name__ == "__main__":
    main()
