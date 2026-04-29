#!/usr/bin/env python3
"""Wave-2 operator-answers scaffolder.

Reads docs/wip/planning/22a-i22-post-closure-followups/operator-answers-wave2.yaml
and emits the canonical artifacts the wave needs: PROGRAM_REGISTRY.csv rows,
brand foundation MDs, GOI/POI voice column backfill, etc.

Three modes:

    py scripts/wave2_backfill.py --check-only
        Sentinel scan; prints `pending: N items` per section. Exit 0 always
        (informational); used by the `wave2_backfill_check` verify profile.

    py scripts/wave2_backfill.py --dry-run [--section <name>]
        Prints what would be written, without touching files. Refuses if the
        target sections still carry __OPERATOR_CONFIRM__ sentinels.

    py scripts/wave2_backfill.py [--section <name>] [--allow-pending]
        Full write. Refuses by default if any sentinel remains in the sections
        being processed. --allow-pending lets you write a partial pass during
        operator review (sentinel cells are skipped, not written).

Sections: programs | brand_voice | goi_poi_voice | kirbe_duality | g_24_3_signoff

Authority: ~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md
§"Backfill discipline & operator UX".

SOC: never reads or writes real adviser emails or GOI/POI real names. The
composer (I24-P4) is responsible for SMTP-time inlining.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
ANSWERS_PATH = (
    REPO_ROOT
    / "docs"
    / "wip"
    / "planning"
    / "22a-i22-post-closure-followups"
    / "operator-answers-wave2.yaml"
)
SENTINEL = "__OPERATOR_CONFIRM__"

SECTIONS = (
    "meta",
    "programs",
    "brand_voice",
    "goi_poi_voice",
    "kirbe_duality",
    "g_24_3_signoff",
)


def _import_yaml() -> Any:
    """Import PyYAML lazily with an actionable error message."""
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        sys.stderr.write(
            "wave2_backfill: PyYAML is required.\n"
            "  Install:  py -m pip install pyyaml\n"
            "  (Often already present as a transitive dep of streamlit / pytest.)\n"
        )
        raise SystemExit(2)
    return yaml


def load_answers(path: Path = ANSWERS_PATH) -> dict[str, Any]:
    """Load and minimally validate the operator-answers YAML."""
    if not path.is_file():
        sys.stderr.write(f"wave2_backfill: not found: {path}\n")
        raise SystemExit(2)
    yaml = _import_yaml()
    with path.open(encoding="utf-8") as fh:
        try:
            data = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            sys.stderr.write(f"wave2_backfill: YAML parse error in {path}: {exc}\n")
            raise SystemExit(2) from exc
    if not isinstance(data, dict):
        sys.stderr.write("wave2_backfill: expected top-level mapping in YAML\n")
        raise SystemExit(2)
    return data


def count_sentinels(node: Any) -> int:
    """Count occurrences of the SENTINEL string anywhere in a nested structure."""
    if isinstance(node, str):
        return 1 if node == SENTINEL else 0
    if isinstance(node, dict):
        return sum(count_sentinels(v) for v in node.values())
    if isinstance(node, list):
        return sum(count_sentinels(v) for v in node)
    return 0


def section_status(data: dict[str, Any], section: str) -> tuple[int, int]:
    """Return (sentinel_count, leaf_count) for a top-level section."""
    node = data.get(section)
    if node is None:
        return 0, 0
    sentinels = count_sentinels(node)
    leaves = _leaf_count(node)
    return sentinels, leaves


def _leaf_count(node: Any) -> int:
    """Count primitive leaves (str/int/float/bool/None) in a nested structure."""
    if isinstance(node, dict):
        return sum(_leaf_count(v) for v in node.values())
    if isinstance(node, list):
        return sum(_leaf_count(v) for v in node)
    return 1


def cmd_check_only(data: dict[str, Any]) -> int:
    """Print sentinel counts per section. Always exit 0 (informational)."""
    print("wave2_backfill: sentinel scan")
    print(f"  source: {ANSWERS_PATH.relative_to(REPO_ROOT)}")
    print("  " + "-" * 56)
    total_sentinels = 0
    total_leaves = 0
    for section in SECTIONS:
        sentinels, leaves = section_status(data, section)
        total_sentinels += sentinels
        total_leaves += leaves
        if leaves == 0:
            mark = "?"
            note = "(absent)"
        elif sentinels == 0:
            mark = "OK"
            note = f"({leaves} leaves filled)"
        else:
            mark = "PEND"
            note = f"({sentinels} of {leaves} pending)"
        print(f"  [{mark:>4}]  {section:<20s} {note}")
    print("  " + "-" * 56)
    print(f"  total: {total_sentinels} pending across {total_leaves} leaves")
    if total_sentinels == 0:
        print("  status: READY — all sections complete; safe to run --dry-run then full write")
    else:
        nxt = _next_section(data)
        print(f"  status: pending — fill section '{nxt}' next, then re-run --check-only")
    return 0


_PRIORITY_ORDER: tuple[str, ...] = (
    "programs",
    "brand_voice",
    "goi_poi_voice",
    "kirbe_duality",
    "g_24_3_signoff",
)


def _next_section(data: dict[str, Any]) -> str:
    """Return the next section the operator should fill, following priority order.

    Priority follows the unblock chain from the Wave-2 plan:
    programs (I23) -> brand_voice (I24-P0a) -> goi_poi_voice (I24-P2) ->
    kirbe_duality (I23-P6) -> g_24_3_signoff (I24-P6, irreversible — LAST).
    """
    for section in _PRIORITY_ORDER:
        sentinels, _ = section_status(data, section)
        if sentinels > 0:
            return section
    return "(none)"


def cmd_dry_run(data: dict[str, Any], section_filter: str | None) -> int:
    """Print what would be written; refuses on sentinels in target sections."""
    target_sections = _resolve_target_sections(section_filter)
    blocking = []
    for s in target_sections:
        sentinels, _ = section_status(data, s)
        if sentinels > 0:
            blocking.append((s, sentinels))
    if blocking:
        print("wave2_backfill: --dry-run BLOCKED on pending sentinels")
        for s, n in blocking:
            print(f"  - section '{s}': {n} pending")
        print("  Fill the sentinels and re-run, or use --allow-pending to skip them.")
        return 1
    print("wave2_backfill: --dry-run (no writes)")
    print("  target sections: " + ", ".join(target_sections))
    print("  (write logic for each section is NOT YET implemented in this bootstrap;")
    print("   it lands as the relevant Wave-2 phases ship — see plan §Backfill discipline)")
    return 0


def cmd_write(
    data: dict[str, Any],
    section_filter: str | None,
    allow_pending: bool,
) -> int:
    """Full write. Refuses on sentinels unless --allow-pending."""
    target_sections = _resolve_target_sections(section_filter)
    if not allow_pending:
        blocking = []
        for s in target_sections:
            sentinels, _ = section_status(data, s)
            if sentinels > 0:
                blocking.append((s, sentinels))
        if blocking:
            print("wave2_backfill: REFUSED — sentinels remain in target sections")
            for s, n in blocking:
                print(f"  - section '{s}': {n} pending")
            print("  Fill all __OPERATOR_CONFIRM__ tokens, or pass --allow-pending.")
            return 1
    print("wave2_backfill: write mode")
    print("  target sections: " + ", ".join(target_sections))
    print("  (per-section writers are NOT YET implemented in this bootstrap;")
    print("   each Wave-2 phase that consumes a section adds its writer.)")
    print("  scaffolder is sentinel-safe; nothing was written.")
    return 0


def _resolve_target_sections(section_filter: str | None) -> list[str]:
    if section_filter is None:
        return [s for s in SECTIONS if s != "meta"]
    if section_filter not in SECTIONS:
        sys.stderr.write(
            f"wave2_backfill: unknown section '{section_filter}'. Valid: "
            + ", ".join(SECTIONS)
            + "\n"
        )
        raise SystemExit(2)
    return [section_filter]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Wave-2 operator-answers scaffolder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Sentinel scan; report pending per section; always exit 0",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be written without touching files",
    )
    parser.add_argument(
        "--section",
        type=str,
        default=None,
        help="Process one section only (programs|brand_voice|goi_poi_voice|kirbe_duality|g_24_3_signoff)",
    )
    parser.add_argument(
        "--allow-pending",
        action="store_true",
        help="Allow partial writes — skip sentinel cells (default: refuse)",
    )
    args = parser.parse_args(argv)

    data = load_answers()

    if args.check_only:
        return cmd_check_only(data)
    if args.dry_run:
        return cmd_dry_run(data, args.section)
    return cmd_write(data, args.section, args.allow_pending)


if __name__ == "__main__":
    raise SystemExit(main())
