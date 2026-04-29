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


# ─── Brand voice writer (Initiative 24 P0a) ──────────────────────────────────
#
# Reads YAML Section 2 (`brand_voice`) and writes the three canonical brand
# foundation MDs under `v3.0/Admin/O5-1/Marketing/Brand/`:
#
#   BRAND_VOICE_FOUNDATION.md   - voice charter + archetype + narrative pillars
#   BRAND_REGISTER_MATRIX.md    - (relationship, channel) -> register table
#   BRAND_DO_DONT.md            - voice IS / voice IS NOT tables
#
# Each MD's frontmatter `status:` flips from `scaffold-awaiting-discovery` to
# `active` once written. Idempotent: same YAML input -> byte-identical output.
# Refuses on sentinels unless `--allow-pending`.

_BRAND_DIR = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Marketing"
    / "Brand"
)
_BRAND_VOICE_FOUNDATION_MD = _BRAND_DIR / "BRAND_VOICE_FOUNDATION.md"
_BRAND_REGISTER_MATRIX_MD = _BRAND_DIR / "BRAND_REGISTER_MATRIX.md"
_BRAND_DO_DONT_MD = _BRAND_DIR / "BRAND_DO_DONT.md"


def _md_escape_cell(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def _render_brand_voice_foundation(payload: dict[str, Any]) -> str:
    charter = str(payload.get("voice_charter") or "").strip()
    archetype = str(payload.get("archetype") or "").strip()
    pillars = [str(p).strip() for p in (payload.get("narrative_pillars") or []) if str(p).strip()]
    return (
        "---\n"
        "status: active\n"
        "role_owner: Brand Manager\n"
        "area: Marketing\n"
        "entity: Holistika\n"
        "program_id: shared\n"
        "topic_ids:\n"
        "  - topic_brand_voice\n"
        "artifact_role: canonical\n"
        "intellectual_kind: brand_asset\n"
        "authority: Operator (lived protocols)\n"
        "last_review: 2026-04-29\n"
        "ssot: true\n"
        "---\n\n"
        "# BRAND_VOICE_FOUNDATION\n\n"
        "> **Status — Active (Initiative 24 P0a; Operator-authored 2026-04-29).** Operator-lived "
        "brand voice per D-IH-17. Maintained by the Brand Manager (CMO chain); annual review trigger "
        "lives in `process_list.csv` `thi_mkt_dtp_293` (Initiative 24 P1).\n\n"
        "## Voice charter\n\n"
        f"> {charter}\n\n"
        "## Archetype\n\n"
        f"`{archetype}` — see [`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md) for archetype definitions used across the organisation.\n\n"
        "## Narrative pillars\n\n"
        + "".join(f"{i}. {pillar}\n" for i, pillar in enumerate(pillars, start=1))
        + "\nThese three pillars anchor every Holistika message. The composer "
        "(`scripts/compose_adviser_message.py`, Initiative 24 P4) validates that drafts align with at "
        "least one pillar; messages that align with none flag for operator review.\n\n"
        "## Voice IS / IS NOT\n\n"
        "See companion [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) for the per-trait do/don't pairs.\n\n"
        "## Register matrix\n\n"
        "See companion [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) for the "
        "`(relationship, channel) -> register` lookup the composer uses at Layer 4 eloquence resolution.\n\n"
        "## Language patterns\n\n"
        "Spanish-language patterns (salutations, register matching, jargon-to-refuse) are captured in "
        "[`BRAND_SPANISH_PATTERNS.md`](BRAND_SPANISH_PATTERNS.md) — hand-authored companion sourced "
        "from real Holistika ↔ external-counsel exchanges. The composer cites it at Layer 4 when "
        "`language_preference: es` resolves. English / bilingual patterns get added as separate "
        "companions (`BRAND_ENGLISH_PATTERNS.md`, etc.) when the operator surfaces enough lived "
        "examples.\n\n"
        "## How this is used\n\n"
        "The methodology SOP [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) "
        "cites this foundation as **Layer 1 (Brand foundation)**. The composer reads:\n\n"
        "- `voice_charter` and `archetype` to validate every outgoing message stays inside the brand envelope.\n"
        "- `narrative_pillars` to align the message's \"why\" with one or more pillars.\n"
        "- The companion register matrix to pick the right tonal register for `(relationship, channel)`.\n\n"
        "The **eloquence layer** (Layer 4) operates **inside** the brand voice — it adjusts register, "
        "language, and pronoun within the bounds set here. It does not override the brand voice.\n\n"
        "## Maintenance\n\n"
        "- **Source of truth**: `docs/wip/planning/22a-i22-post-closure-followups/operator-answers-wave2.yaml` "
        "Section 2. Edits to this MD by hand will be **overwritten** on next "
        "`py scripts/wave2_backfill.py --section brand_voice` — edit the YAML and re-run.\n"
        "- Annual Brand Manager review (D-IH-17 re-evaluation trigger).\n"
        "- Per-message dry-run via `py scripts/compose_adviser_message.py --recipient <ref_id> "
        "--discipline <id> --dry-run` to surface mismatches.\n"
        "- Drift detection: if the methodology SOP's brand-foundation citations stop resolving, the next "
        "composer run fails loudly.\n\n"
        "## Related\n\n"
        "- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md)\n"
        "- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md)\n"
        "- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md)\n"
        "- Cross-program glossary §\"Voice register\": "
        "[`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md)\n"
    )


def _render_brand_register_matrix(payload: dict[str, Any]) -> str:
    matrix = payload.get("register_matrix") or []
    rows: list[str] = []
    for entry in matrix:
        if not isinstance(entry, dict):
            continue
        rows.append(
            "| {rel} | {ch} | `{reg}` |".format(
                rel=_md_escape_cell(str(entry.get("relationship") or "")),
                ch=_md_escape_cell(str(entry.get("channel") or "")),
                reg=_md_escape_cell(str(entry.get("register") or "")),
            )
        )
    table = (
        "| Relationship | Channel | Register |\n"
        "|:-------------|:--------|:---------|\n"
        + "\n".join(rows)
        + "\n"
    ) if rows else "_(no rows yet — operator fills YAML Section 2 `brand_voice.register_matrix`)_\n"

    return (
        "---\n"
        "status: active\n"
        "role_owner: Brand Manager\n"
        "area: Marketing\n"
        "entity: Holistika\n"
        "program_id: shared\n"
        "topic_ids:\n"
        "  - topic_brand_voice\n"
        "artifact_role: canonical\n"
        "intellectual_kind: brand_asset\n"
        "authority: Operator (lived protocols)\n"
        "last_review: 2026-04-29\n"
        "---\n\n"
        "# BRAND_REGISTER_MATRIX\n\n"
        "> **Status — Active (Initiative 24 P0a; Operator-authored 2026-04-29).** Auto-emitted by "
        "`scripts/wave2_backfill.py --section brand_voice` from "
        "`operator-answers-wave2.yaml` Section 2 `brand_voice.register_matrix`. Edit the YAML and "
        "re-run; do **not** edit this file by hand — it will be overwritten.\n\n"
        "## How (relationship, channel) maps to a register\n\n"
        "The composer (`scripts/compose_adviser_message.py`, Initiative 24 P4) looks up the "
        "(relationship, channel) pair against this matrix to pick the right tonal register. When a "
        "pair is missing, the composer falls back to the discipline default "
        "(`ADVISER_ENGAGEMENT_DISCIPLINES.csv`), then to the brand foundation default "
        "(archetype-implied register).\n\n"
        + table
        + "\nCommon register tokens: `formal_legal`, `peer_consulting`, `casual_internal`, "
        "`regulator_neutral`, `investor_aspirational`. Add new tokens by extending YAML Section 2 + "
        "(optionally) the `voice_register` enum on `GOI_POI_REGISTER.csv` (Initiative 24 P2).\n\n"
        "## Related\n\n"
        "- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md)\n"
        "- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md)\n"
        "- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) §3 Use-case layer\n"
        "- Cross-program glossary §\"Voice register\": "
        "[`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md)\n"
    )


def _render_brand_do_dont(payload: dict[str, Any]) -> str:
    is_rows: list[str] = []
    for entry in (payload.get("voice_is") or []):
        if not isinstance(entry, dict):
            continue
        is_rows.append(
            "| {trait} | {ex} |".format(
                trait=_md_escape_cell(str(entry.get("trait") or "")),
                ex=_md_escape_cell(str(entry.get("example") or "")),
            )
        )
    is_not_rows: list[str] = []
    for entry in (payload.get("voice_is_not") or []):
        if not isinstance(entry, dict):
            continue
        is_not_rows.append(
            "| {trait} | {ex} |".format(
                trait=_md_escape_cell(str(entry.get("trait") or "")),
                ex=_md_escape_cell(str(entry.get("example") or "")),
            )
        )
    is_table = (
        "| Trait | Example phrasing |\n"
        "|:------|:-----------------|\n"
        + "\n".join(is_rows) + "\n"
    ) if is_rows else "_(no rows yet)_\n"
    is_not_table = (
        "| Trait | Example of what we'd refuse to say |\n"
        "|:------|:-----------------------------------|\n"
        + "\n".join(is_not_rows) + "\n"
    ) if is_not_rows else "_(no rows yet)_\n"

    return (
        "---\n"
        "status: active\n"
        "role_owner: Brand Manager\n"
        "area: Marketing\n"
        "entity: Holistika\n"
        "program_id: shared\n"
        "topic_ids:\n"
        "  - topic_brand_voice\n"
        "artifact_role: canonical\n"
        "intellectual_kind: brand_asset\n"
        "authority: Operator (lived protocols)\n"
        "last_review: 2026-04-29\n"
        "---\n\n"
        "# BRAND_DO_DONT\n\n"
        "> **Status — Active (Initiative 24 P0a; Operator-authored 2026-04-29).** Auto-emitted by "
        "`scripts/wave2_backfill.py --section brand_voice` from `operator-answers-wave2.yaml` "
        "Section 2 `brand_voice.voice_is` / `voice_is_not`. Edit the YAML and re-run.\n\n"
        "## Voice IS\n\n"
        + is_table
        + "\n## Voice IS NOT\n\n"
        + is_not_table
        + "\n## How the composer uses this\n\n"
        "Per-message reviewer checks (every Layer-4 eloquence pass):\n\n"
        "- The proposed phrasing matches at least one **Voice IS** trait.\n"
        "- The proposed phrasing does **not** match any **Voice IS NOT** pattern.\n\n"
        "When ambiguous, the composer flags the message for operator review rather than auto-generate.\n\n"
        "## Related\n\n"
        "- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md)\n"
        "- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md)\n"
        "- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md)\n"
    )


def _write_brand_voice(
    data: dict[str, Any], *, allow_pending: bool
) -> list[Path]:
    """Initiative 24 P0a writer: emit the three brand foundation MDs from YAML Section 2.

    Reads `brand_voice:` and writes:

    - `BRAND_VOICE_FOUNDATION.md` — charter + archetype + narrative pillars.
    - `BRAND_REGISTER_MATRIX.md`  — (relationship, channel) -> register table.
    - `BRAND_DO_DONT.md`          — voice IS / voice IS NOT tables.

    All three flip frontmatter `status:` from `scaffold-awaiting-discovery` to
    `active`. Idempotent (same YAML -> same output). Refuses on sentinels unless
    `allow_pending=True` (in which case sentinel cells are emitted as empty).
    """
    section = data.get("brand_voice")
    if not isinstance(section, dict) or not section:
        return []

    if allow_pending:
        # Replace sentinels with empty strings deeply for safe partial render.
        def _strip(node: Any) -> Any:
            if isinstance(node, str):
                return "" if node == SENTINEL else node
            if isinstance(node, dict):
                return {k: _strip(v) for k, v in node.items()}
            if isinstance(node, list):
                return [_strip(v) for v in node]
            return node

        section = _strip(section)

    _BRAND_DIR.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for path, renderer in (
        (_BRAND_VOICE_FOUNDATION_MD, _render_brand_voice_foundation),
        (_BRAND_REGISTER_MATRIX_MD, _render_brand_register_matrix),
        (_BRAND_DO_DONT_MD, _render_brand_do_dont),
    ):
        body = renderer(section)
        path.write_text(body, encoding="utf-8", newline="\n")
        written.append(path)
    return written


_SECTION_WRITERS: dict[str, Any] = {
    "programs": _write_program_registry,
    "brand_voice": _write_brand_voice,
    # goi_poi_voice: handled inline during I24-P2 (CSV ALTER + 6-row backfill via MCP).
    # kirbe_duality: confirmation block; no writer (decisions captured in I23/I24 decision logs).
    # g_24_3_signoff: I24-P6 (irreversible workflow gate; the actual SMTP send is operator-driven).
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
