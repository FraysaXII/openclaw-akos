#!/usr/bin/env python3
"""Sync AKOS runtime files to agent workspaces.

Assembles prompts, deploys scaffold files and SOUL.md variants to the
OpenCLAW home directory. Run this after editing prompts or scaffold
templates to push changes to the live agent workspaces.

Usage:
    py scripts/sync-runtime.py
    py scripts/sync-runtime.py --variant standard
    py scripts/sync-runtime.py --json-log
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import akos.process as proc
from akos.io import REPO_ROOT, deploy_scaffold_files, deploy_soul_prompts, resolve_openclaw_home
from akos.log import setup_logging

logger = logging.getLogger("akos.sync")

ASSEMBLE_SCRIPT = REPO_ROOT / "scripts" / "assemble-prompts.py"
ASSEMBLED_DIR = REPO_ROOT / "prompts" / "assembled"


def run_assemble() -> bool:
    """Run assemble-prompts.py to regenerate assembled prompt files."""
    logger.info("Running assemble-prompts.py ...")
    result = proc.run([sys.executable, str(ASSEMBLE_SCRIPT)], timeout=60)
    if result.success:
        logger.info("Prompt assembly succeeded")
    else:
        logger.error("Prompt assembly failed: %s", result.stderr)
    return result.success


def sync_scaffold(oc_home: Path) -> list[Path]:
    """Deploy scaffold files (IDENTITY.md, MEMORY.md, etc.) to workspaces."""
    deployed = deploy_scaffold_files(oc_home)
    if deployed:
        logger.info("Deployed %d scaffold file(s)", len(deployed))
    else:
        logger.info("Scaffold files already up to date")
    return deployed


def sync_soul_prompts(variant: str, oc_home: Path) -> list[Path]:
    """Deploy assembled SOUL.md prompts to agent workspaces."""
    from akos.madeira_interaction import apply_madeira_interaction_to_soul
    from akos.state import load_state

    deployed = deploy_soul_prompts(ASSEMBLED_DIR, variant, oc_home)
    st = load_state(oc_home)
    apply_madeira_interaction_to_soul(
        oc_home, mode=st.madeiraInteractionMode, assembled_dir=ASSEMBLED_DIR
    )
    logger.info(
        "Deployed %d SOUL.md file(s) (variant=%s, madeiraInteractionMode=%s)",
        len(deployed),
        variant,
        st.madeiraInteractionMode,
    )
    return deployed


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync AKOS runtime files to agent workspaces")
    parser.add_argument(
        "--variant", default="compact",
        help="Prompt variant to deploy (default: compact)",
    )
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    oc_home = resolve_openclaw_home()
    logger.info("OpenCLAW home: %s", oc_home)

    if not run_assemble():
        print("\n  FAIL: Prompt assembly failed. Fix errors and retry.\n")
        sys.exit(1)

    scaffold_deployed = sync_scaffold(oc_home)
    try:
        soul_deployed = sync_soul_prompts(args.variant, oc_home)
    except FileNotFoundError as exc:
        logger.error("SOUL prompt deployment failed: %s", exc)
        print(f"\n  FAIL: {exc}\n")
        sys.exit(1)

    total = len(scaffold_deployed) + len(soul_deployed)
    print()
    print("=" * 56)
    print(f"  Sync complete: {total} file(s) deployed")
    print(f"    Scaffold files:  {len(scaffold_deployed)}")
    print(f"    SOUL.md files:   {len(soul_deployed)}")
    print(f"    Variant:         {args.variant}")
    print(f"    Target:          {oc_home}")
    print("=" * 56)
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
