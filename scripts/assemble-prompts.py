#!/usr/bin/env python3
"""Assemble tiered SOUL.md prompts from base + overlay files.

Reads config/model-tiers.json to determine which overlays apply to each
prompt variant (compact, standard, full), then concatenates base + overlays
and writes the result to prompts/assembled/.

Usage:
    python scripts/assemble-prompts.py                  # build all variants
    python scripts/assemble-prompts.py --variant compact # build one variant
    python scripts/assemble-prompts.py --dry-run         # preview without writing

Requires: Python 3.10+ (stdlib + pydantic).
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.models import load_tiers

TIERS_PATH = REPO_ROOT / "config" / "model-tiers.json"
BASE_DIR = REPO_ROOT / "prompts" / "base"
OVERLAY_DIR = REPO_ROOT / "prompts" / "overlays"
OUTPUT_DIR = REPO_ROOT / "prompts" / "assembled"

AGENTS = {
    "ARCHITECT": "ARCHITECT_BASE.md",
    "EXECUTOR": "EXECUTOR_BASE.md",
}

BOOTSTRAP_MAX_CHARS = 20_000


def assemble_one(agent_name: str, base_file: str, overlays: list[str]) -> str:
    base_path = BASE_DIR / base_file
    if not base_path.exists():
        print(f"  ERROR: base file not found: {base_path}", file=sys.stderr)
        sys.exit(1)

    parts = [base_path.read_text(encoding="utf-8").rstrip()]

    for overlay_name in overlays:
        overlay_path = OVERLAY_DIR / overlay_name
        if not overlay_path.exists():
            print(f"  WARNING: overlay not found, skipping: {overlay_path}", file=sys.stderr)
            continue
        parts.append(overlay_path.read_text(encoding="utf-8").rstrip())

    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Assemble tiered SOUL.md prompts")
    parser.add_argument("--variant", choices=["compact", "standard", "full"],
                        help="Build only this variant (default: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview output without writing files")
    args = parser.parse_args()

    registry = load_tiers(TIERS_PATH)
    variant_overlays = registry.variantOverlays

    variants_to_build = [args.variant] if args.variant else list(variant_overlays.keys())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    built = 0
    warnings = 0

    for variant in variants_to_build:
        overlays = variant_overlays[variant]
        for agent_name, base_file in AGENTS.items():
            content = assemble_one(agent_name, base_file, overlays)
            out_name = f"{agent_name}_PROMPT.{variant}.md"
            out_path = OUTPUT_DIR / out_name
            char_count = len(content)

            status = "OK"
            if char_count > BOOTSTRAP_MAX_CHARS:
                status = f"WARNING: {char_count} chars exceeds bootstrapMaxChars ({BOOTSTRAP_MAX_CHARS})"
                warnings += 1

            if args.dry_run:
                print(f"  [DRY-RUN] {out_name}: {char_count} chars, {len(overlays)} overlays -- {status}")
            else:
                out_path.write_text(content, encoding="utf-8")
                print(f"  [BUILT] {out_name}: {char_count} chars, {len(overlays)} overlays -- {status}")
            built += 1

    print(f"\n  {built} prompts {'previewed' if args.dry_run else 'assembled'}, {warnings} warnings.")

    if warnings > 0:
        print("  Some prompts exceed the bootstrapMaxChars limit. Consider shortening overlays.")
        sys.exit(1)


if __name__ == "__main__":
    main()
