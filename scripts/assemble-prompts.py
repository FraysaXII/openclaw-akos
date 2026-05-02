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
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging
from akos.models import load_tiers

logger = logging.getLogger("akos.assemble-prompts")

TIERS_PATH = REPO_ROOT / "config" / "model-tiers.json"
BASE_DIR = REPO_ROOT / "prompts" / "base"
OVERLAY_DIR = REPO_ROOT / "prompts" / "overlays"
PERSONAS_DIR = REPO_ROOT / "prompts" / "personas"
OUTPUT_DIR = REPO_ROOT / "prompts" / "assembled"

AGENTS = {
    "ORCHESTRATOR": "ORCHESTRATOR_BASE.md",
    "ARCHITECT": "ARCHITECT_BASE.md",
    "EXECUTOR": "EXECUTOR_BASE.md",
    "VERIFIER": "VERIFIER_BASE.md",
    "MADEIRA": "MADEIRA_BASE.md",
}

BOOTSTRAP_MAX_CHARS = 20_000

# I47 P11 (R-47-9): persona overlay budget is BOOTSTRAP_MAX_CHARS (20000) shared
# with all standard overlays. Today's MADEIRA standard is 19731 chars at baseline,
# so the persona overlay budget is ~270 chars at most. Operator-authored hint
# fragments are capped at PERSONA_HINT_MAX_CHARS to keep within budget; any
# headroom expansion requires shrinking other MADEIRA overlays first.
PERSONA_OVERLAY_FILENAME = "PERSONA_OVERLAY.md"
PERSONA_HINTS_FILENAME = "MADEIRA_HINTS.md"
PERSONA_HINT_MAX_CHARS = 500  # operator-authored fragment cap per D-IH-47-I


def _persona_overlay_paths(persona_id: str) -> list[Path]:
    """Resolve persona overlay + per-persona hints file paths.

    Returns paths in the order they must be appended to the assembled prompt.
    Soft-fails (returns only existing paths) when files are missing.
    """
    out: list[Path] = []
    framework = OVERLAY_DIR / PERSONA_OVERLAY_FILENAME
    if framework.exists():
        out.append(framework)
    hints = PERSONAS_DIR / persona_id / PERSONA_HINTS_FILENAME
    if hints.exists():
        out.append(hints)
    return out


# I47 P11 (D-IH-47-I + R-47-9): when MADEIRA is assembled with a persona overlay,
# OVERLAY_HLK_GRAPH is swapped out (persona-aware MADEIRA delegates graph
# traversal awareness to the persona context). This keeps total chars under
# bootstrapMaxChars without shrinking other overlays.
PERSONA_SWAPPED_OUT_OVERLAYS = frozenset({"OVERLAY_HLK_GRAPH.md"})


def assemble_one(
    agent_name: str,
    base_file: str,
    overlays: list[str],
    *,
    persona_id: str | None = None,
) -> str:
    base_path = BASE_DIR / base_file
    if not base_path.exists():
        print(f"  ERROR: base file not found: {base_path}", file=sys.stderr)
        sys.exit(1)

    parts = [base_path.read_text(encoding="utf-8").rstrip()]

    persona_active = bool(persona_id) and agent_name == "MADEIRA"

    for overlay_name in overlays:
        if persona_active and overlay_name in PERSONA_SWAPPED_OUT_OVERLAYS:
            # Persona context replaces this overlay; skip silently (logged once below).
            continue
        overlay_path = OVERLAY_DIR / overlay_name
        if not overlay_path.exists():
            print(f"  WARNING: overlay not found, skipping: {overlay_path}", file=sys.stderr)
            continue
        parts.append(overlay_path.read_text(encoding="utf-8").rstrip())

    # I47 P11 (D-IH-47-I): persona overlay only applies to MADEIRA agent.
    if persona_active:
        for p in _persona_overlay_paths(persona_id or ""):
            parts.append(p.read_text(encoding="utf-8").rstrip())

    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble tiered SOUL.md prompts")
    parser.add_argument("--variant", choices=["compact", "standard", "full"],
                        help="Build only this variant (default: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview output without writing files")
    parser.add_argument("--json-log", action="store_true",
                        help="Emit structured JSON logs")
    parser.add_argument(
        "--persona", default="",
        help=("I47 P11 (D-IH-47-I): assemble MADEIRA prompt with persona overlay. "
              "Lazy-loads prompts/overlays/PERSONA_OVERLAY.md + "
              "prompts/personas/<id>/MADEIRA_HINTS.md. Soft-fails if missing."),
    )
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    registry = load_tiers(TIERS_PATH)

    variants_to_build = (
        [args.variant] if args.variant else list(registry.variantOverlays.keys())
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    built = 0
    warnings = 0

    for variant in variants_to_build:
        for agent_name, base_file in AGENTS.items():
            overlays = registry.overlays_for(variant, agent_name)
            content = assemble_one(
                agent_name, base_file, overlays, persona_id=(args.persona or None)
            )
            persona_suffix = f".{args.persona}" if (args.persona and agent_name == "MADEIRA") else ""
            out_name = f"{agent_name}_PROMPT.{variant}{persona_suffix}.md"
            out_path = OUTPUT_DIR / out_name
            char_count = len(content)

            # I47 P11 (R-47-9): MADEIRA + persona overlay must stay <= bootstrapMaxChars (20000).
            # Today's MADEIRA standard baseline is 19731 chars, so persona overlay budget is ~270.
            persona_active = bool(args.persona) and agent_name == "MADEIRA"
            applicable_limit = BOOTSTRAP_MAX_CHARS

            status = "OK"
            if char_count > applicable_limit:
                status = f"WARNING: {char_count} chars exceeds bootstrapMaxChars ({applicable_limit})"
                warnings += 1
            # Additional warning when persona-conditioned variant has < 100 chars headroom.
            if persona_active and char_count > applicable_limit - 100 and char_count <= applicable_limit:
                status = f"OK (low headroom: {applicable_limit - char_count} chars)"

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
