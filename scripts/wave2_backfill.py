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
# Make `akos.*` importable when this script is invoked directly (e.g.
# `py scripts/wave2_backfill.py`); tests already prepend via conftest.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

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
    written: list[Path] = []
    skipped: list[str] = []
    for section in target_sections:
        writer = _SECTION_WRITERS.get(section)
        if writer is None:
            skipped.append(section)
            continue
        result = writer(data, allow_pending=allow_pending)
        if result is not None:
            written.extend(result)
    if written:
        for path in written:
            try:
                rel = path.relative_to(REPO_ROOT)
            except ValueError:
                rel = path
            print(f"  wrote: {rel}")
    if skipped:
        print(f"  scaffolder writer not yet implemented for: {', '.join(skipped)}")
        print("  (each Wave-2 phase that consumes a section adds its writer.)")
    return 0


# ─── Section writers ─────────────────────────────────────────────────────────
#
# Each writer takes (data, allow_pending) and returns a list of Paths it wrote
# (or [] / None when nothing changed). Writers are idempotent: same YAML input
# produces byte-identical output. Cells carrying SENTINEL are skipped only
# when allow_pending=True.

_PROGRAM_REGISTRY_CSV = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "compliance"
    / "dimensions"
    / "PROGRAM_REGISTRY.csv"
)


def _csv_escape(value: str) -> str:
    """Escape a single CSV cell using csv.writer-style quoting when needed."""
    if value is None:
        return ""
    s = str(value)
    if any(ch in s for ch in (",", '"', "\n", "\r")):
        return '"' + s.replace('"', '""') + '"'
    return s


def _write_program_registry(
    data: dict[str, Any], *, allow_pending: bool
) -> list[Path]:
    """Initiative 23 P1 writer: emit PROGRAM_REGISTRY.csv from YAML `programs` section.

    Reads the YAML's `programs:` mapping (one mapping per row, keyed by either
    `program_id` (PRJ-HOL-...) or `process_item_id` (e.g. env_tech_prj_2)) and
    writes `docs/references/hlk/compliance/dimensions/PROGRAM_REGISTRY.csv` with
    column order matching `akos.hlk_program_registry_csv.PROGRAM_REGISTRY_FIELDNAMES`.

    The YAML key is treated as the **canonical program_id** when it matches
    PRJ-HOL-style; otherwise the row's `program_id:` field is used (or, when
    absent, the agent constructs `PRJ-HOL-<CODE>-<YEAR>` from `program_code`
    and the year inferred from `start_date` / current year).

    Idempotent: rows are sorted by `program_id` for deterministic output.
    """
    from akos.hlk_program_registry_csv import PROGRAM_REGISTRY_FIELDNAMES

    section = data.get("programs")
    if not isinstance(section, dict) or not section:
        return []

    rows: list[dict[str, str]] = []
    for key, payload in section.items():
        if not isinstance(payload, dict):
            continue
        # Key resolution: prefer the YAML key as program_id when PRJ-HOL-style;
        # otherwise build one from program_code + year.
        program_id = str(key).strip()
        if not program_id.startswith("PRJ-HOL-"):
            # Use process_item_id-style key as a hint; build PRJ-HOL-<CODE>-<YYYY>.
            code = str(payload.get("program_code") or "").strip().upper()
            start = str(payload.get("start_date") or "").strip()
            year = ""
            if start and "-" in start and start[:4].isdigit():
                year = start[:4]
            else:
                year = "2026"
            if code and len(code) == 3:
                # Map process_item_id slug like "thi_legal_prj_1" to PRJ-HOL-LEG-2026.
                program_id = f"PRJ-HOL-{code}-{year}"

        process_item_id = str(payload.get("process_item_id") or "").strip()
        # When the YAML key was already a process_item_id, it's the FK back.
        if not process_item_id and not str(key).startswith("PRJ-HOL-"):
            process_item_id = str(key).strip()

        row = {field: "" for field in PROGRAM_REGISTRY_FIELDNAMES}
        row["program_id"] = program_id
        row["process_item_id"] = process_item_id
        row["program_name"] = str(payload.get("program_name") or "").strip()
        row["program_code"] = str(payload.get("program_code") or "").strip().upper()
        row["lifecycle_status"] = str(payload.get("lifecycle_status") or "").strip()
        row["parent_program_id"] = str(payload.get("parent_program_id") or "").strip()
        row["consumes_program_ids"] = _normalize_program_ids(
            str(payload.get("consumes_program_ids") or "").strip(), section
        )
        row["produces_for_program_ids"] = _normalize_program_ids(
            str(payload.get("produces_for_program_ids") or "").strip(), section
        )
        row["subsumes_program_ids"] = _normalize_program_ids(
            str(payload.get("subsumes_program_ids") or "").strip(), section
        )
        row["primary_owner_role"] = str(payload.get("primary_owner_role") or "").strip()
        row["default_plane"] = str(payload.get("default_plane") or "").strip()
        row["start_date"] = str(payload.get("start_date") or "").strip()
        row["target_close_date"] = str(payload.get("target_close_date") or "").strip()
        row["risk_class"] = str(payload.get("risk_class") or "").strip()
        row["notes"] = str(payload.get("notes") or "").strip()

        # Sentinel handling: if --allow-pending, skip cells carrying SENTINEL
        # (they emit empty); else this branch is unreachable (cmd_write blocks
        # on sentinels by default).
        if allow_pending:
            for field, value in row.items():
                if value == SENTINEL:
                    row[field] = ""

        rows.append(row)

    rows.sort(key=lambda r: r["program_id"])

    _PROGRAM_REGISTRY_CSV.parent.mkdir(parents=True, exist_ok=True)
    with _PROGRAM_REGISTRY_CSV.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(",".join(PROGRAM_REGISTRY_FIELDNAMES) + "\n")
        for row in rows:
            fh.write(",".join(_csv_escape(row[field]) for field in PROGRAM_REGISTRY_FIELDNAMES) + "\n")
    return [_PROGRAM_REGISTRY_CSV]


def _normalize_program_ids(raw: str, section: dict[str, Any]) -> str:
    """Resolve YAML-key references (e.g. `hol_resea_prj_1`) to canonical
    `program_id` values (e.g. `PRJ-HOL-RES-2026`) using the same key-resolution
    rule as the writer. Semicolon-separated list preserved.

    Items already in PRJ-HOL- form pass through unchanged.
    Unknown items pass through (validator catches forward references).
    """
    if not raw:
        return ""
    parts = [p.strip() for p in raw.split(";") if p.strip()]
    resolved: list[str] = []
    for part in parts:
        if part.startswith("PRJ-HOL-"):
            resolved.append(part)
            continue
        # Look up YAML key payload
        payload = section.get(part) if isinstance(section, dict) else None
        if isinstance(payload, dict):
            code = str(payload.get("program_code") or "").strip().upper()
            start = str(payload.get("start_date") or "").strip()
            year = start[:4] if (start and start[:4].isdigit()) else "2026"
            if code and len(code) == 3:
                resolved.append(f"PRJ-HOL-{code}-{year}")
                continue
        resolved.append(part)  # leave as-is; validator will surface
    return ";".join(resolved)


_SECTION_WRITERS: dict[str, Any] = {
    "programs": _write_program_registry,
    # brand_voice: I24-P0a (lands in i24-brand-foundation-alignment todo)
    # goi_poi_voice: I24-P2 (lands in i24-goipoi-mirror-ddl-alter)
    # kirbe_duality: I23-P6 confirmation block (lands in i23-onboard-program-2)
    # g_24_3_signoff: I24-P6 (irreversible; lands in i24-send-real-email)
}


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
