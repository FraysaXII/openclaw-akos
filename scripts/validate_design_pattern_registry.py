#!/usr/bin/env python3
"""Validate PEOPLE_DESIGN_PATTERN_REGISTRY.csv (Initiative 79 P2).

This validator carries TWO scan modes (one script; one set of imports; one set of
tests) per `D-IH-79-N` (anti-jargon drift gate via shared validator):

1. **Default mode** — registry validation: header drift gate + per-row Pydantic
   instantiation + slug uniqueness + FK resolution to DECISION_REGISTER.csv +
   FK resolution to INITIATIVE_REGISTRY.csv + consumer_areas semicolon-token
   validation against ``VALID_CONSUMER_AREAS``. Mirrors the established
   ``validate_engagement_model_registry.py`` shape.

2. **--jargon-scan mode** — anti-jargon drift gate: scans People-area canonicals
   for forbidden technical jargon (per ``akos-people-discipline-of-disciplines.mdc``
   §4 + D-IH-79-N). Mirrors the ``validate_brand_baseline_reality_drift.py`` shape
   (scan + token-list + INFO-then-FAIL graduation). Per **D-IH-80-F** (I80 P1):
   ``*.addendum.md`` files are excluded at file-selection time — addenda may
   legitimately carry cross-area jargon since the executor reads only the body;
   auditors / system-owners read addenda. The exclusion is suffix-based (cleaner
   than parsing markdown section structure) and aligns the validator with the
   data integration boundary every other consumer adopts (Supabase mirror /
   Neo4j projection / Obsidian / RAG pipelines / ERP panel filters operate at
   file-level, not section-level).

The split mirrors I66's brand-baseline-reality drift gate logic for the
brand-DNA dual-register: same shape, different vocabulary, different audience.

Wired into ``scripts/validate_hlk.py`` dispatcher (registry mode) and
``config/verification-profiles.json`` profile ``pre_commit`` (both modes).

Usage::

    py scripts/validate_design_pattern_registry.py
    py scripts/validate_design_pattern_registry.py --jargon-scan
    py scripts/validate_design_pattern_registry.py --jargon-scan --json-log

Exit codes::

    0 — PASS (registry valid; or no jargon leakage).
    1 — FAIL (registry invalid; or forbidden tokens found in People canonicals).

Cross-references: ``akos-people-discipline-of-disciplines.mdc`` §4,
``akos-brand-baseline-reality.mdc`` (sibling drift-gate discipline),
``akos-executable-process-catalog.mdc`` (paired SOP+runbook rule the registry tracks).
"""

from __future__ import annotations

import argparse
import csv
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_design_pattern_csv import (  # noqa: E402
    DESIGN_PATTERN_FIELDNAMES,
    DesignPatternRow,
    VALID_CONSUMER_AREAS,
)
from akos.io import REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

logger = logging.getLogger("akos.design_pattern_registry")

CSV_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance"
    / "canonicals" / "dimensions" / "PEOPLE_DESIGN_PATTERN_REGISTRY.csv"
)
DECISION_CSV = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance"
    / "canonicals" / "DECISION_REGISTER.csv"
)
INITIATIVE_CSV = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance"
    / "canonicals" / "INITIATIVE_REGISTRY.csv"
)


# Forbidden tokens in People canonicals (per akos-people-discipline-of-disciplines.mdc §4 + D-IH-79-N).
# Case-sensitive; matched on word boundaries to avoid false positives (e.g. "akos-people-..."
# in lowercase file paths is allowed; "AKOS" uppercase in body prose is forbidden).
FORBIDDEN_TOKENS: tuple[str, ...] = (
    "LangChain",
    "LangGraph",
    "Ollama",
    "LlamaIndex",
    "OpenClaw",
    "CrewAI",
    "VercelAI",
    "Groq",
    "MCP",
    "embedder",
    "transformer",
    "FDW",
    "RLS",
    "pgvector",
    "AKOS",
)

# People canonicals scanned for jargon leakage.
# Tech Lab canonicals are EXEMPT — they legitimately carry framework names.
# *.addendum.md files are EXEMPT per D-IH-80-F (SOP body/addendum pattern;
# addenda may legitimately carry cross-area jargon since the executor reads only
# the body; auditors / system-owners read addenda).
PEOPLE_CANONICALS_RELATIVE: tuple[str, ...] = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md",
    "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md",
    "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md",
    "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md",
    "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md",
    "docs/references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md",
)

# Addendum exclusion glob suffix per D-IH-80-F (I80 P1 SOP body/addendum pattern mint).
# Files whose name ends with this suffix are excluded from jargon-scan even if listed
# above. The exclusion runs at file-selection time (cleaner than parsing markdown
# section structure) and aligns the validator with the data integration boundary
# every other consumer adopts (Supabase mirror / Neo4j projection / Obsidian /
# RAG pipelines / ERP panel filters operate at file-level, not section-level).
ADDENDUM_SUFFIX: str = ".addendum.md"

# Skip-line discipline: lines that mention the token inside a markdown code fence,
# inline code span, or a markdown link target are skipped to reduce false positives.
# Body prose is what we guard.
_CODE_FENCE_RE = re.compile(r"^\s*```")
_LINK_OR_CODE_RE = re.compile(r"`[^`]*`|\]\([^)]*\)|\[[^\]]*\]\([^)]*\)")


@dataclass(frozen=True)
class JargonHit:
    path: Path
    line_number: int
    line_text: str
    token: str


def _load_decision_ids() -> set[str]:
    if not DECISION_CSV.is_file():
        return set()
    with DECISION_CSV.open(encoding="utf-8", newline="") as fh:
        return {
            (row.get("decision_id") or "").strip()
            for row in csv.DictReader(fh)
            if row.get("decision_id")
        }


def _load_initiative_ids() -> set[str]:
    if not INITIATIVE_CSV.is_file():
        return set()
    with INITIATIVE_CSV.open(encoding="utf-8", newline="") as fh:
        return {
            (row.get("initiative_id") or "").strip()
            for row in csv.DictReader(fh)
            if row.get("initiative_id")
        }


def run_registry_mode() -> int:
    """Validate PEOPLE_DESIGN_PATTERN_REGISTRY.csv structure + FKs."""
    print("\n  PEOPLE_DESIGN_PATTERN_REGISTRY Validator")
    print("  " + "=" * 50)
    if not CSV_PATH.is_file():
        print(f"  FAIL: PEOPLE_DESIGN_PATTERN_REGISTRY.csv not found at {CSV_PATH}")
        return 1

    decision_ids = _load_decision_ids()
    initiative_ids = _load_initiative_ids()

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(DESIGN_PATTERN_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(DESIGN_PATTERN_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen_ids: set[str] = set()
    seen_anchors: set[str] = set()
    for i, row in enumerate(rows, start=2):
        try:
            DesignPatternRow.model_validate({k: (v or "") for k, v in row.items() if k})
        except Exception as exc:
            row_id = (row.get("pattern_id") or f"row_{i}").strip()
            errors.append(f"row {i} ({row_id}): Pydantic validation failed: {exc}")
            continue

        pid = (row.get("pattern_id") or "").strip()
        if pid in seen_ids:
            errors.append(f"row {i}: duplicate pattern_id {pid!r}")
        seen_ids.add(pid)

        anchor = (row.get("pattern_md_anchor") or "").strip()
        if anchor in seen_anchors:
            errors.append(f"row {i} ({pid}): duplicate pattern_md_anchor {anchor!r}")
        seen_anchors.add(anchor)

        # consumer_areas: semicolon-token list; each token must be in VALID_CONSUMER_AREAS.
        ca_raw = (row.get("consumer_areas") or "").strip()
        ca_tokens = [t.strip() for t in ca_raw.split(";") if t.strip()]
        for tok in ca_tokens:
            if tok not in VALID_CONSUMER_AREAS:
                errors.append(
                    f"row {i} ({pid}): consumer_areas token {tok!r} not in VALID_CONSUMER_AREAS "
                    f"(allowed: {sorted(VALID_CONSUMER_AREAS)})"
                )

        # FK to DECISION_REGISTER.csv (skip if registers absent — soft FK).
        rdid = (row.get("ratifying_decision_id") or "").strip()
        if decision_ids and rdid and rdid not in decision_ids:
            errors.append(
                f"row {i} ({pid}): ratifying_decision_id {rdid!r} not in DECISION_REGISTER.csv"
            )

        # FK to INITIATIVE_REGISTRY.csv.
        oid = (row.get("originating_initiative_id") or "").strip()
        if initiative_ids and oid and oid not in initiative_ids:
            errors.append(
                f"row {i} ({pid}): originating_initiative_id {oid!r} not in INITIATIVE_REGISTRY.csv"
            )

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for err in errors[:25]:
            print(f"    - {err}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Rows validated: {len(rows)}")
    print(f"  Pattern classes:    {sorted({(row.get('pattern_class') or '').strip() for row in rows})}")
    print(f"  Discipline origins: {sorted({(row.get('discipline_origin') or '').strip() for row in rows})}")
    print("  PASS")
    return 0


def _scan_file_for_jargon(path: Path) -> list[JargonHit]:
    """Scan a single People canonical for forbidden tokens.

    Strategy: walk lines top-to-bottom; track code-fence open/close state; on
    every body line, strip inline-code spans and markdown link targets, then
    search for word-boundary matches against FORBIDDEN_TOKENS (case-sensitive).
    """
    if not path.is_file():
        return []

    hits: list[JargonHit] = []
    inside_fence = False
    text = path.read_text(encoding="utf-8")
    for i, raw_line in enumerate(text.splitlines(), start=1):
        if _CODE_FENCE_RE.match(raw_line):
            inside_fence = not inside_fence
            continue
        if inside_fence:
            continue
        cleaned = _LINK_OR_CODE_RE.sub("", raw_line)
        for token in FORBIDDEN_TOKENS:
            pattern = re.compile(rf"\b{re.escape(token)}\b")
            if pattern.search(cleaned):
                hits.append(JargonHit(path=path, line_number=i, line_text=raw_line, token=token))
    return hits


def _discover_sibling_addenda(body_paths: list[Path]) -> list[Path]:
    """Return any sibling ``*.addendum.md`` files alongside the listed body files.

    Per D-IH-80-F (I80 P1): addenda are auto-discovered for visibility (count
    surfaced in the scan footer) but never scanned. The addendum exemption is
    file-level — a file whose name ends with ``.addendum.md`` is exempt from
    jargon-scan even if explicitly listed in ``PEOPLE_CANONICALS_RELATIVE``.
    """
    addenda: list[Path] = []
    for body in body_paths:
        # Sibling discovery: same parent folder, body filename swapped to addendum suffix.
        # E.g. ``SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`` ->
        #      ``SOP-PEOPLE_AGENTIC_OPERATIONS_001.addendum.md``.
        stem = body.name.removesuffix(".md")
        candidate = body.with_name(f"{stem}{ADDENDUM_SUFFIX}")
        if candidate.is_file():
            addenda.append(candidate)
    return addenda


def run_jargon_scan_mode() -> int:
    """Scan People canonicals for forbidden technical jargon (D-IH-79-N).

    Per D-IH-80-F (I80 P1): excludes any ``*.addendum.md`` file at file-selection
    time. Addenda may legitimately carry cross-area jargon since the executor
    reads only the body; auditors / system-owners read addenda.
    """
    print("\n  PEOPLE_DESIGN_PATTERN_REGISTRY anti-jargon drift gate")
    print("  " + "=" * 50)

    all_hits: list[JargonHit] = []
    files_scanned = 0
    files_missing: list[Path] = []
    files_excluded_addendum: list[Path] = []
    body_paths: list[Path] = []
    for rel in PEOPLE_CANONICALS_RELATIVE:
        path = REPO_ROOT / rel
        # D-IH-80-F: exclude *.addendum.md at file-selection time even if explicitly listed.
        if path.name.endswith(ADDENDUM_SUFFIX):
            files_excluded_addendum.append(path)
            continue
        if not path.is_file():
            files_missing.append(path)
            continue
        files_scanned += 1
        body_paths.append(path)
        all_hits.extend(_scan_file_for_jargon(path))

    # Auto-discover sibling addenda for visibility (informational; not scanned).
    discovered_addenda = _discover_sibling_addenda(body_paths)

    print(f"  Files scanned (body):       {files_scanned}")
    print(f"  Files not yet authored:     {len(files_missing)} (informational; phases ship them)")
    print(f"  Sibling addenda discovered: {len(discovered_addenda)} (exempt per D-IH-80-F SOP body/addendum pattern)")
    if files_excluded_addendum:
        print(f"  Listed addenda excluded:    {len(files_excluded_addendum)} (defense-in-depth; suffix-based reject at scan time)")
    print(f"  Forbidden tokens:           {len(FORBIDDEN_TOKENS)}")

    if all_hits:
        print(f"  FAIL: {len(all_hits)} forbidden-token leak(s) in People canonicals (body)")
        for hit in all_hits[:30]:
            rel = hit.path.relative_to(REPO_ROOT).as_posix()
            print(f"    - {rel}:{hit.line_number} -> {hit.token!r}")
        if len(all_hits) > 30:
            print(f"    ... and {len(all_hits) - 30} more")
        print("  See .cursor/rules/akos-people-discipline-of-disciplines.mdc §4 for the allowed-token list.")
        print("  Tech Lab canonicals (AGENTIC_FRAMEWORK_LANDSCAPE.md, SOP-TECH_AGENTIC_INFRA_001.md)")
        print("  are EXEMPT — they legitimately carry the framework names.")
        print("  *.addendum.md siblings are EXEMPT per D-IH-80-F — extra context lives there;")
        print("  body must read plain. Move cross-area jargon out of the body into the addendum.")
        return 1

    print("  PASS — no forbidden tokens in People canonicals body")
    return 0


def main(argv: list[str] | None = None) -> int:
    setup_logging()
    parser = argparse.ArgumentParser(description="Validate PEOPLE_DESIGN_PATTERN_REGISTRY.csv (or run anti-jargon drift gate)")
    parser.add_argument(
        "--jargon-scan",
        action="store_true",
        help="Run the anti-jargon drift gate over People canonicals (D-IH-79-N)",
    )
    args = parser.parse_args(argv)

    if args.jargon_scan:
        return run_jargon_scan_mode()
    return run_registry_mode()


if __name__ == "__main__":
    raise SystemExit(main())
