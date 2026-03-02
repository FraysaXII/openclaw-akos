#!/usr/bin/env python3
"""Switch the active model/environment for the AKOS OpenCLAW deployment.

Activates an environment profile by:
  1. Copying the .env file to ~/.openclaw/.env
  2. Deep-merging the JSON overlay into ~/.openclaw/openclaw.json
  3. Looking up the model tier from config/model-tiers.json
  4. Deploying the correct assembled SOUL.md variant to agent workspaces
  5. Restarting the OpenCLAW gateway

Supports --rollback to restore the previous state from backup.

Usage:
    python scripts/switch-model.py dev-local
    python scripts/switch-model.py gpu-runpod
    python scripts/switch-model.py prod-cloud --dry-run
    python scripts/switch-model.py --rollback

Requires: Python 3.10+ (stdlib + pydantic).
"""

import argparse
import logging
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import akos.process as proc
from akos.io import REPO_ROOT, deep_merge, load_json, resolve_openclaw_home, save_json
from akos.log import setup_logging
from akos.models import load_tiers
from akos.state import load_state, record_switch

logger = logging.getLogger("akos.switch-model")

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


def do_rollback(oc_home: Path) -> None:
    """Restore openclaw.json from backup and report previous state."""
    backup = oc_home / "openclaw.json.bak"
    config = oc_home / "openclaw.json"
    if not backup.exists():
        logger.error("No backup found at %s -- cannot rollback", backup)
        sys.exit(1)

    shutil.copy2(backup, config)
    logger.info("Restored %s from backup", config)

    prev = load_state(oc_home)
    if prev.activeEnvironment:
        logger.info("Previous state: %s / %s (%s)", prev.activeEnvironment, prev.activeModel, prev.activeTier)
    logger.info("Rollback complete. Restart the gateway manually if needed.")


def main():
    parser = argparse.ArgumentParser(description="Switch AKOS model/environment")
    parser.add_argument("environment", nargs="?", help="Environment name (e.g., dev-local, gpu-runpod, prod-cloud)")
    parser.add_argument("--rollback", action="store_true", help="Restore config from backup")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--no-restart", action="store_true", help="Skip gateway restart")
    parser.add_argument("--json-log", action="store_true", help="Emit structured JSON logs")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    oc_home = resolve_openclaw_home()

    if args.rollback:
        do_rollback(oc_home)
        return

    if not args.environment:
        parser.error("environment is required (or use --rollback)")

    env_name = args.environment

    overlay_path = ENVS_DIR / f"{env_name}.json"
    if not overlay_path.exists():
        logger.error("Environment overlay not found: %s", overlay_path)
        logger.info("Available: %s", ", ".join(p.stem for p in ENVS_DIR.glob("*.json")))
        sys.exit(1)

    env_file = find_env_file(env_name)
    overlay = load_json(overlay_path)
    registry = load_tiers(TIERS_PATH)

    model_id = overlay.get("agents", {}).get("defaults", {}).get("model", {}).get("primary")
    if not model_id:
        logger.error("Overlay does not specify agents.defaults.model.primary")
        sys.exit(1)

    tier_result = registry.lookup_tier(model_id)
    if tier_result:
        tier_name, tier_data = tier_result
        variant = tier_data.promptVariant
    else:
        logger.warning("Model '%s' not in model-tiers.json, defaulting to 'full'", model_id)
        tier_name = "unknown"
        variant = "full"

    logger.info("Environment: %s | Model: %s | Tier: %s | Variant: %s", env_name, model_id, tier_name, variant)

    # Step 1: Copy .env (safe -- not part of critical section)
    if env_file:
        dest_env = oc_home / ".env"
        if args.dry_run:
            logger.info("[DRY-RUN] Would copy %s -> %s", env_file.name, dest_env)
        else:
            oc_home.mkdir(parents=True, exist_ok=True)
            shutil.copy2(env_file, dest_env)
            logger.info("Copied %s -> %s", env_file.name, dest_env)
    else:
        logger.info("No .env file for '%s'; skipping", env_name)

    if args.dry_run:
        _dry_run_preview(oc_home, overlay_path, overlay, variant)
        return

    # Critical section: steps 2-4 with rollback on failure
    oc_config_path = oc_home / "openclaw.json"
    backup = oc_config_path.with_suffix(".json.bak")
    made_backup = False

    try:
        # Step 2: Deep-merge JSON overlay
        if oc_config_path.exists():
            existing = load_json(oc_config_path)
            merged = deep_merge(existing, overlay)
            shutil.copy2(oc_config_path, backup)
            made_backup = True
            save_json(oc_config_path, merged)
            logger.info("Merged %s into %s (backup: %s)", overlay_path.name, oc_config_path, backup.name)
        else:
            logger.warning("%s does not exist; run bootstrap first", oc_config_path)

        # Step 3: Deploy assembled SOUL.md variants
        workspaces = {
            "ARCHITECT": oc_home / "workspace-architect" / "SOUL.md",
            "EXECUTOR": oc_home / "workspace-executor" / "SOUL.md",
        }
        for agent, soul_dest in workspaces.items():
            assembled_name = f"{agent}_PROMPT.{variant}.md"
            assembled_path = ASSEMBLED_DIR / assembled_name
            if not assembled_path.exists():
                raise FileNotFoundError(f"Assembled prompt not found: {assembled_path}. Run: python scripts/assemble-prompts.py")
            soul_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(assembled_path, soul_dest)
            logger.info("Deployed %s -> %s", assembled_name, soul_dest)

        # Step 4: Restart gateway
        if not args.no_restart:
            logger.info("Restarting OpenCLAW gateway...")
            result = proc.run(["openclaw", "gateway", "restart"], timeout=60, capture=False)
            if result.success:
                logger.info("Gateway restarted.")
            elif result.returncode == -1 and "not found" in result.stderr:
                logger.warning("'openclaw' not in PATH; restart manually.")
            else:
                logger.warning("Gateway restart exit code %d", result.returncode)

    except Exception:
        logger.error("Switch failed mid-operation -- rolling back config")
        if made_backup and backup.exists():
            shutil.copy2(backup, oc_config_path)
            logger.info("Restored %s from backup", oc_config_path)
        record_switch(oc_home, environment=env_name, model=model_id, tier=tier_name, variant=variant, success=False)
        raise

    record_switch(oc_home, environment=env_name, model=model_id, tier=tier_name, variant=variant, success=True)
    logger.info("Switched to %s (%s) in %s environment.", model_id, tier_name, env_name)


def _dry_run_preview(oc_home: Path, overlay_path: Path, overlay: dict, variant: str) -> None:
    oc_config_path = oc_home / "openclaw.json"
    if oc_config_path.exists():
        logger.info("[DRY-RUN] Would merge %s into %s (keys: %s)", overlay_path.name, oc_config_path, list(overlay.keys()))
    for agent in ["ARCHITECT", "EXECUTOR"]:
        name = f"{agent}_PROMPT.{variant}.md"
        dest = oc_home / f"workspace-{agent.lower()}" / "SOUL.md"
        logger.info("[DRY-RUN] Would copy %s -> %s", name, dest)
    logger.info("[DRY-RUN] Preview complete.")


if __name__ == "__main__":
    main()
