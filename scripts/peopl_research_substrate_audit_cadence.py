#!/usr/bin/env python3
"""Research Substrate Audit Cadence runbook (Initiative 84 P6).

Paired runbook for ``SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`` per
[`akos-executable-process-catalog.mdc`](../.cursor/rules/akos-executable-process-catalog.mdc)
Rule 1. Operationalises the quarterly Research-area substrate-audit cadence
described in the SOP `Steps` section.

Reads SUBSTRATE_REGISTRY.csv (Pydantic SSOT via
``akos.hlk_substrate_registry_csv.SUBSTRATE_REGISTRY_FIELDNAMES``), the
SUBSTRATE_LANDSCAPE_DOCTRINE.md doctrine canonical, and the dated quarterly
audit reports under ``docs/wip/intelligence/substrate-audit-YYYY-QN/``.
Provides four CLI modes the SOP cadence references:

- ``--uat-mode <quarterly-report-path>`` — validate a freshly-committed
  quarterly report parses cleanly + cross-references resolve.
- ``--staleness-check`` — scan SUBSTRATE_REGISTRY ``last_audit_date`` column;
  warn (exit 1) if any row's last_audit_date is > 90 days old (quarterly
  cadence boundary).
- ``--emit-delta <prior-q-path> <current-q-path>`` — emit a Markdown delta
  report between two quarterly reports.
- ``--list-quarters`` — list all ``docs/wip/intelligence/substrate-audit-YYYY-QN/``
  folders discovered in the workspace.

Default (no args): print usage hint + a current registry summary (rows by
status / akos_integration_state). Exit 0.

Decision lineage:

- ``D-IH-84-A`` (mega scope; charter)
- ``D-IH-84-G`` (SUBSTRATE_LANDSCAPE_DOCTRINE.md authoring posture)
- ``D-IH-84-H`` (quarterly cadence + owner-activation interim)

Cross-references:

- ``SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`` (paired SOP).
- ``akos/hlk_substrate_registry_csv.py`` (Pydantic SSOT; fieldnames tuple +
  Literal enum frozensets used for row decoding).
- ``scripts/validate_substrate_registry.py`` (sibling validator; this runbook
  defers schema enforcement to that validator).
- ``config/verification-profiles.json`` `substrate_audit_smoke` profile
  (wires ``--staleness-check`` + the test suite).
- ``akos-executable-process-catalog.mdc`` Rule 1 (pairing rule).
- ``process_list.csv`` row ``env_tech_dtp_substrate_landscape_mtnce_001``
  (operator-pending; this is the paired runbook for that scheduled cadence
  row once minted per SOP-META ordering).

Per ``CONTRIBUTING.md`` Python Code Standards: type hints on every signature +
return; structured logging via ``akos.log.setup_logging``; ``pathlib.Path``;
stdlib-only (no subprocess; no external deps); cross-platform.

Exit codes::

    0  PASS / informational
    1  FAIL (staleness violation, --uat-mode error, --emit-delta failure)
    2  internal error (missing canonical CSV, missing report path)

Usage::

    py scripts/peopl_research_substrate_audit_cadence.py
    py scripts/peopl_research_substrate_audit_cadence.py --staleness-check
    py scripts/peopl_research_substrate_audit_cadence.py --uat-mode \
        docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md
    py scripts/peopl_research_substrate_audit_cadence.py --emit-delta \
        docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md \
        docs/wip/intelligence/substrate-audit-2026-Q3/2026-Q3-substrate-audit.md
    py scripts/peopl_research_substrate_audit_cadence.py --list-quarters
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import logging
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_substrate_registry_csv import (  # noqa: E402
    CSV_PATH_RELATIVE,
    SUBSTRATE_REGISTRY_FIELDNAMES,
)
from akos.log import setup_logging  # noqa: E402

SUBSTRATE_REGISTRY_CSV = REPO_ROOT / CSV_PATH_RELATIVE

INTELLIGENCE_ROOT = REPO_ROOT / "docs" / "wip" / "intelligence"

DOCTRINE_CANONICAL = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Research"
    / "Methodology"
    / "canonicals"
    / "SUBSTRATE_LANDSCAPE_DOCTRINE.md"
)

PAIRED_SOP = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Research"
    / "Methodology"
    / "canonicals"
    / "SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md"
)

# Quarterly cadence boundary in days. Per D-IH-84-H quarterly default; 90 days
# is the soft upper bound before staleness flag fires. Off-cycle event-trigger
# audits can keep last_audit_date current intra-quarter.
STALENESS_THRESHOLD_DAYS: int = 90

QUARTER_FOLDER_RE = re.compile(r"^substrate-audit-(\d{4})-Q([1-4])(?:-[a-z0-9-]+)?$")

logger = logging.getLogger("peopl_research_substrate_audit_cadence")


def _today() -> dt.date:
    return dt.date.today()


def _load_registry_rows() -> list[dict[str, str]]:
    """Read SUBSTRATE_REGISTRY.csv via the canonical fieldnames tuple."""
    if not SUBSTRATE_REGISTRY_CSV.is_file():
        raise FileNotFoundError(
            f"SUBSTRATE_REGISTRY.csv missing at {SUBSTRATE_REGISTRY_CSV.relative_to(REPO_ROOT)}"
        )
    with SUBSTRATE_REGISTRY_CSV.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        header = tuple(reader.fieldnames or ())
        if header != SUBSTRATE_REGISTRY_FIELDNAMES:
            raise ValueError(
                f"SUBSTRATE_REGISTRY.csv header drift: expected {list(SUBSTRATE_REGISTRY_FIELDNAMES)!r}; "
                f"got {list(header)!r}. Run scripts/validate_substrate_registry.py to diagnose."
            )
        return list(reader)


def _parse_iso_date(value: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def _format_summary(rows: list[dict[str, str]]) -> str:
    by_status: dict[str, int] = defaultdict(int)
    by_integration: dict[str, int] = defaultdict(int)
    for row in rows:
        by_status[row.get("status", "")] += 1
        by_integration[row.get("akos_integration_state", "")] += 1
    lines: list[str] = [
        f"  Total rows: {len(rows)}",
        "  By status: " + ", ".join(f"{k}={v}" for k, v in sorted(by_status.items())),
        "  By akos_integration_state: " + ", ".join(f"{k}={v}" for k, v in sorted(by_integration.items())),
    ]
    return "\n".join(lines)


def _print_usage_summary(rows: list[dict[str, str]]) -> int:
    print()
    print("  Research Substrate Audit Cadence Runbook")
    print("  " + "=" * 44)
    print(f"  Paired SOP: {PAIRED_SOP.relative_to(REPO_ROOT)}")
    print(f"  Canonical:  {SUBSTRATE_REGISTRY_CSV.relative_to(REPO_ROOT)}")
    print(f"  Doctrine:   {DOCTRINE_CANONICAL.relative_to(REPO_ROOT)}")
    print()
    print("  Current SUBSTRATE_REGISTRY summary:")
    print(_format_summary(rows))
    print()
    print("  Modes (run with -h for full help):")
    print("    --staleness-check                       check rows last_audit_date > 90 days")
    print("    --uat-mode <quarterly-report-path>      validate freshly-committed report")
    print("    --emit-delta <prior-path> <current>     emit Markdown delta report")
    print("    --list-quarters                         list discovered substrate-audit-YYYY-QN folders")
    print()
    return 0


def _staleness_check(rows: list[dict[str, str]], *, today: dt.date) -> int:
    """Scan last_audit_date column; FAIL when any row > 90 days old."""
    threshold_days = STALENESS_THRESHOLD_DAYS
    stale_rows: list[tuple[str, str, int]] = []
    parse_errors: list[tuple[str, str]] = []
    fresh_rows: list[tuple[str, str, int]] = []

    for row in rows:
        sid = row.get("substrate_id", "<missing-id>")
        raw = row.get("last_audit_date", "")
        parsed = _parse_iso_date(raw)
        if parsed is None:
            parse_errors.append((sid, raw))
            continue
        age_days = (today - parsed).days
        if age_days > threshold_days:
            stale_rows.append((sid, raw, age_days))
        else:
            fresh_rows.append((sid, raw, age_days))

    print()
    print("  Staleness check (quarterly cadence boundary)")
    print("  " + "=" * 44)
    print(f"  Threshold: {threshold_days} days; today: {today.isoformat()}")
    print(f"  Total rows scanned: {len(rows)}")
    print(f"  Fresh rows: {len(fresh_rows)}")
    print(f"  Stale rows: {len(stale_rows)}")
    print(f"  Parse-error rows: {len(parse_errors)}")
    if parse_errors:
        print()
        print("  Parse errors (last_audit_date not ISO YYYY-MM-DD):")
        for sid, raw in parse_errors:
            print(f"    - {sid}: {raw!r}")
    if stale_rows:
        print()
        print("  Stale rows (require audit refresh per SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001 step 3):")
        for sid, raw, age in sorted(stale_rows, key=lambda r: -r[2]):
            print(f"    - {sid}: last_audit_date={raw} ({age} days old)")
    if stale_rows or parse_errors:
        print()
        print("  FAIL")
        logger.error("staleness check FAIL: %s stale; %s parse-error", len(stale_rows), len(parse_errors))
        return 1
    print()
    print("  PASS")
    logger.info("staleness check PASS: %s rows fresh", len(fresh_rows))
    return 0


def _extract_substrate_ids_from_report(report_path: Path) -> set[str]:
    """Scan report body for SUBS-* substrate_id tokens (FK to canonical)."""
    if not report_path.is_file():
        raise FileNotFoundError(f"quarterly report missing at {report_path}")
    body = report_path.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(r"\bSUBS-[A-Z0-9-]+\b")
    return set(pattern.findall(body))


def _uat_mode(report_path: Path, rows: list[dict[str, str]]) -> int:
    """Validate a freshly-committed quarterly report parses + FK-resolves."""
    print()
    print("  UAT mode (quarterly report freshly-committed parse + FK resolution)")
    print("  " + "=" * 70)
    print(f"  Report path: {report_path}")

    errors: list[str] = []
    warnings: list[str] = []

    if not report_path.exists():
        errors.append(f"Report file not found: {report_path}")
    elif not report_path.is_file():
        errors.append(f"Report path is not a file: {report_path}")
    else:
        try:
            body = report_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            errors.append(f"Failed to read report: {exc}")
            body = ""

        # Cheap structural checks: frontmatter + a few load-bearing sections.
        if body.strip():
            if not body.lstrip().startswith("---"):
                warnings.append("Report does not start with YAML frontmatter")
            for section_token in ("# ", "## "):
                if section_token not in body:
                    warnings.append(f"Report appears to lack any '{section_token.strip()}' header")
                    break

            # FK resolution: every SUBS-* token cited in the report must
            # appear in SUBSTRATE_REGISTRY.csv substrate_id column.
            registered = {row.get("substrate_id", "") for row in rows}
            cited = _extract_substrate_ids_from_report(report_path)
            unresolved = sorted(token for token in cited if token not in registered)
            print(f"  Substrate IDs cited in report: {len(cited)}")
            print(f"  Substrate IDs registered:      {len(registered)}")
            print(f"  Unresolved citations:          {len(unresolved)}")
            if unresolved:
                for token in unresolved:
                    errors.append(f"Unresolved substrate_id citation: {token!r}")

    if warnings:
        print()
        print(f"  Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"    - {w}")
    if errors:
        print()
        print(f"  ERRORS ({len(errors)}):")
        for e in errors:
            print(f"    - {e}")
        print()
        print("  FAIL")
        logger.error("UAT FAIL: %s errors; %s warnings", len(errors), len(warnings))
        return 1
    print()
    print("  PASS")
    logger.info("UAT PASS: %s warnings", len(warnings))
    return 0


def _emit_delta(prior_path: Path, current_path: Path) -> int:
    """Emit Markdown delta report between two quarterly reports."""
    print()
    print("  Emit delta (Markdown) between quarterly reports")
    print("  " + "=" * 50)

    missing: list[Path] = [p for p in (prior_path, current_path) if not p.is_file()]
    if missing:
        for p in missing:
            print(f"  Missing report: {p}")
        print()
        print("  FAIL")
        logger.error("emit-delta FAIL: %s missing reports", len(missing))
        return 1

    prior_ids = _extract_substrate_ids_from_report(prior_path)
    current_ids = _extract_substrate_ids_from_report(current_path)
    added = sorted(current_ids - prior_ids)
    removed = sorted(prior_ids - current_ids)
    unchanged = sorted(prior_ids & current_ids)

    print(f"  Prior report:   {prior_path}")
    print(f"  Current report: {current_path}")
    print()
    print("---")
    print()
    print(f"# Substrate audit delta: {prior_path.stem} -> {current_path.stem}")
    print()
    print(f"Generated by `scripts/peopl_research_substrate_audit_cadence.py --emit-delta` on {_today().isoformat()}.")
    print()
    print(f"- Substrate IDs in prior:   {len(prior_ids)}")
    print(f"- Substrate IDs in current: {len(current_ids)}")
    print(f"- Net added: {len(added)}")
    print(f"- Net removed: {len(removed)}")
    print(f"- Unchanged: {len(unchanged)}")
    print()
    if added:
        print("## Added substrate citations")
        print()
        for sid in added:
            print(f"- `{sid}`")
        print()
    if removed:
        print("## Removed substrate citations")
        print()
        for sid in removed:
            print(f"- `{sid}`")
        print()
    if unchanged:
        print("## Unchanged substrate citations")
        print()
        for sid in unchanged:
            print(f"- `{sid}`")
        print()
    logger.info(
        "emit-delta PASS: added=%s removed=%s unchanged=%s",
        len(added),
        len(removed),
        len(unchanged),
    )
    return 0


def _list_quarters() -> int:
    """List discovered substrate-audit-YYYY-QN folders under docs/wip/intelligence/."""
    print()
    print("  Substrate audit quarter folders discovered")
    print("  " + "=" * 44)
    print(f"  Root: {INTELLIGENCE_ROOT.relative_to(REPO_ROOT)}")

    if not INTELLIGENCE_ROOT.is_dir():
        print(f"  Intelligence root missing: {INTELLIGENCE_ROOT}")
        print()
        print("  PASS (informational; no folders discovered)")
        return 0

    candidates: list[Path] = sorted(
        p for p in INTELLIGENCE_ROOT.iterdir() if p.is_dir() and QUARTER_FOLDER_RE.match(p.name)
    )
    print(f"  Folders found: {len(candidates)}")
    print()
    for folder in candidates:
        readme = folder / "README.md"
        report_pattern = list(folder.glob("*-substrate-audit.md"))
        report_count = len(report_pattern)
        readme_flag = "yes" if readme.is_file() else "no"
        print(f"  - {folder.name}: README={readme_flag}; cycle-report-files={report_count}")
    print()
    print("  PASS (informational)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Research Substrate Audit Cadence runbook (Initiative 84 P6)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--staleness-check",
        action="store_true",
        help="Scan SUBSTRATE_REGISTRY last_audit_date; FAIL if any row > 90 days old",
    )
    group.add_argument(
        "--uat-mode",
        type=str,
        default=None,
        metavar="QUARTERLY_REPORT_PATH",
        help="Validate a freshly-committed quarterly report parses + cross-references resolve",
    )
    group.add_argument(
        "--emit-delta",
        nargs=2,
        type=str,
        default=None,
        metavar=("PRIOR_QUARTERLY_REPORT_PATH", "CURRENT_QUARTERLY_REPORT_PATH"),
        help="Emit Markdown delta report between two quarterly reports",
    )
    group.add_argument(
        "--list-quarters",
        action="store_true",
        help="List discovered substrate-audit-YYYY-QN folders under docs/wip/intelligence/",
    )
    parser.add_argument(
        "--json-log",
        action="store_true",
        help="Emit structured JSON log lines (for CI / log aggregation)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="DEBUG-level logging",
    )
    args = parser.parse_args(argv)

    setup_logging(json_output=args.json_log, level=logging.DEBUG if args.verbose else logging.INFO)

    # --list-quarters and unset-flag paths don't need the registry; everything
    # else does. Load up-front and surface I/O failures cleanly.
    if args.list_quarters:
        return _list_quarters()

    try:
        rows = _load_registry_rows()
    except FileNotFoundError as exc:
        logger.error("registry load FAIL: %s", exc)
        return 2
    except ValueError as exc:
        logger.error("registry load FAIL: %s", exc)
        return 2

    if args.staleness_check:
        return _staleness_check(rows, today=_today())

    if args.uat_mode:
        report_path = Path(args.uat_mode)
        if not report_path.is_absolute():
            report_path = REPO_ROOT / report_path
        try:
            return _uat_mode(report_path, rows)
        except FileNotFoundError as exc:
            logger.error("uat-mode FAIL: %s", exc)
            return 2

    if args.emit_delta:
        prior_path = Path(args.emit_delta[0])
        current_path = Path(args.emit_delta[1])
        if not prior_path.is_absolute():
            prior_path = REPO_ROOT / prior_path
        if not current_path.is_absolute():
            current_path = REPO_ROOT / current_path
        try:
            return _emit_delta(prior_path, current_path)
        except FileNotFoundError as exc:
            logger.error("emit-delta FAIL: %s", exc)
            return 2

    return _print_usage_summary(rows)


if __name__ == "__main__":
    raise SystemExit(main())
