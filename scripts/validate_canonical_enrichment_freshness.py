"""Validate canonical enrichment freshness across v3.0 area canonicals.

Pairs with ``akos/canonical_freshness.py`` (Pydantic chassis) + cursor rule
``akos-planning-traceability.mdc`` §Cross-area enrichment cadence. Operator-
ratified 2026-05-19 (D-IH-86-AB proposed; canonical row appended by the
cluster-burndown parent after Lane A + Lane C land).

Operator quote (verbatim, 2026-05-19): "Option D but make it 3 days, because
we're real fast today. It'll be medium term 30 days then 90 days long term."

The runbook:

1. Globs ``docs/references/hlk/v3.0/Admin/O5-1/**/canonicals/**/*.md``.
2. Parses each file's frontmatter for ``last_review_at:`` (preferred) or the
   legacy ``last_review:`` key.
3. Categorises every row into one of four tiers: fresh / medium / long_term /
   stale per the 3-tier thresholds (defaults 3 / 30 / 90 days).
4. Emits a per-area summary table on stdout plus per-stale-file lines for
   the operator to action.

Exit semantics (per ``--exit-code-mode``):

* ``info``  (default) — always exit 0; output is advisory.
* ``warn``  — exit 0 on no-stale; exit 0 with WARN line otherwise.
* ``fail``  — exit 0 on no-stale; exit 1 on any stale row.

``--strict`` is a convenience alias for ``--exit-code-mode fail``.

Honouring ``akos-executable-process-catalog.mdc`` RULE 1: this is the
executable runbook side of the paired SOP / runbook pair; the paired SOP is
``SOP-TECH_CANONICAL_FRESHNESS_AUDIT_001.md`` (mint pending; planned path
``docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-TECH_CANONICAL_FRESHNESS_AUDIT_001.md``).
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos import log  # noqa: E402
from akos.canonical_freshness import (  # noqa: E402
    CANONICAL_GLOB,
    CanonicalFreshnessRow,
    FreshnessAreaSummary,
    FreshnessThresholds,
    scan_canonical,
    summarize_by_area,
)

log.setup_logging()
logger = logging.getLogger("akos.canonical_freshness")

# Skip patterns mirror validate_external_render_trail.py conventions: any
# README, any _template / _engagement-template skeleton, and any path that
# carries an explicit `_candidates/` marker.
_SKIP_SUBSTRINGS: tuple[str, ...] = (
    "/_template",
    "/_engagement-template/",
    "/_candidates/",
    "/templates/",
)


def _should_skip(path: Path) -> bool:
    rel = path.as_posix()
    if rel.lower().endswith("/readme.md"):
        return True
    return any(token in rel for token in _SKIP_SUBSTRINGS)


def _collect_rows(
    repo_root: Path,
    today: date,
    thresholds: FreshnessThresholds,
    area_filter: str | None,
) -> list[CanonicalFreshnessRow]:
    rows: list[CanonicalFreshnessRow] = []
    for path in sorted(repo_root.glob(CANONICAL_GLOB)):
        if not path.is_file():
            continue
        if _should_skip(path):
            continue
        try:
            row = scan_canonical(path, repo_root, today, thresholds)
        except Exception as exc:  # noqa: BLE001
            logger.warning("scan failed: path=%s err=%s", path, exc)
            continue
        if area_filter and row.area.lower() != area_filter.lower():
            continue
        rows.append(row)
    return rows


def _format_table(summaries: list[FreshnessAreaSummary], thresholds: FreshnessThresholds) -> str:
    if not summaries:
        return "  (no canonical surfaces matched glob)\n"
    header_lines = [
        f"CANONICAL FRESHNESS AUDIT ({thresholds.fresh_days}d / {thresholds.medium_days}d / {thresholds.long_term_days}d tiers)",
        "",
    ]
    area_width = max(len("Area"), max(len(s.area) for s in summaries))
    col_widths = {
        "area": max(area_width, 18),
        "fresh": 6,
        "medium": 7,
        "long_term": 10,
        "stale": 6,
        "total": 6,
    }
    header_row = (
        f"{'Area':<{col_widths['area']}}  "
        f"{'Fresh':>{col_widths['fresh']}}  "
        f"{'Medium':>{col_widths['medium']}}  "
        f"{'Long-term':>{col_widths['long_term']}}  "
        f"{'Stale':>{col_widths['stale']}}  "
        f"{'Total':>{col_widths['total']}}"
    )
    sep = "-" * len(header_row)
    body_rows: list[str] = []
    totals = {"fresh": 0, "medium": 0, "long_term": 0, "stale": 0}
    for s in summaries:
        totals["fresh"] += s.fresh
        totals["medium"] += s.medium
        totals["long_term"] += s.long_term
        totals["stale"] += s.stale
        body_rows.append(
            f"{s.area:<{col_widths['area']}}  "
            f"{s.fresh:>{col_widths['fresh']}}  "
            f"{s.medium:>{col_widths['medium']}}  "
            f"{s.long_term:>{col_widths['long_term']}}  "
            f"{s.stale:>{col_widths['stale']}}  "
            f"{s.total:>{col_widths['total']}}"
        )
    grand_total = sum(totals.values())
    total_row = (
        f"{'Total':<{col_widths['area']}}  "
        f"{totals['fresh']:>{col_widths['fresh']}}  "
        f"{totals['medium']:>{col_widths['medium']}}  "
        f"{totals['long_term']:>{col_widths['long_term']}}  "
        f"{totals['stale']:>{col_widths['stale']}}  "
        f"{grand_total:>{col_widths['total']}}"
    )
    return "\n".join(header_lines + [header_row, sep] + body_rows + [sep, total_row, ""]) + "\n"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit canonical enrichment freshness across v3.0 area canonicals. "
            "Operator-ratified 2026-05-19 (D-IH-86-AB proposed): 3-tier "
            "staleness — 3 days short / 30 days medium / 90 days long-term."
        ),
    )
    parser.add_argument(
        "--area",
        type=str,
        default=None,
        help="Filter to a single area (People / Marketing / Tech / Operations / Envoy Tech Lab / Research / Finance). Default: all areas.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Alias for --exit-code-mode fail; FAIL the gate on any stale canonical.",
    )
    parser.add_argument(
        "--tier-threshold-fresh",
        type=int,
        default=3,
        help="Short-term threshold in days (default 3 per operator ratify 2026-05-19).",
    )
    parser.add_argument(
        "--tier-threshold-medium",
        type=int,
        default=30,
        help="Medium-term threshold in days (default 30).",
    )
    parser.add_argument(
        "--tier-threshold-long",
        type=int,
        default=90,
        help="Long-term threshold in days (default 90); beyond is 'stale'.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Override repo root (defaults to validator's parent-parent).",
    )
    parser.add_argument(
        "--exit-code-mode",
        choices=("info", "warn", "fail"),
        default="info",
        help="Exit-code posture: info=always 0; warn=0 + WARN line; fail=1 on any stale.",
    )
    parser.add_argument(
        "--max-stale-lines",
        type=int,
        default=50,
        help="Cap per-stale-file lines emitted to stdout (avoids spamming CI logs).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    thresholds = FreshnessThresholds(
        fresh_days=args.tier_threshold_fresh,
        medium_days=args.tier_threshold_medium,
        long_term_days=args.tier_threshold_long,
    )
    today = date.today()
    repo_root: Path = args.repo_root

    rows = _collect_rows(repo_root, today, thresholds, args.area)
    summaries = summarize_by_area(rows)
    sys.stdout.write(_format_table(summaries, thresholds))

    stale_rows = [r for r in rows if r.tier == "stale"]
    long_term_rows = [r for r in rows if r.tier == "long_term"]
    medium_rows = [r for r in rows if r.tier == "medium"]

    logger.info(
        "tier counts: fresh=%d medium=%d long_term=%d stale=%d total=%d",
        sum(s.fresh for s in summaries),
        sum(s.medium for s in summaries),
        sum(s.long_term for s in summaries),
        sum(s.stale for s in summaries),
        len(rows),
    )
    if medium_rows:
        logger.info("medium-tier rows: %d (review within %d days)", len(medium_rows), thresholds.medium_days)
    if long_term_rows:
        logger.info("long-term-tier rows: %d (review within %d days)", len(long_term_rows), thresholds.long_term_days)

    if stale_rows:
        logger.info("STALE rows (last_review > %d days OR missing):", thresholds.long_term_days)
        for row in stale_rows[: args.max_stale_lines]:
            days_repr = "missing" if row.days_since_review is None else f"{row.days_since_review}d"
            logger.info("  STALE %-9s %s", days_repr, row.path)
        if len(stale_rows) > args.max_stale_lines:
            logger.info("  ... %d more stale rows truncated (raise --max-stale-lines to see all)", len(stale_rows) - args.max_stale_lines)

    mode = "fail" if args.strict else args.exit_code_mode
    if mode == "fail" and stale_rows:
        logger.error("FAIL: %d stale canonical surface(s) found (--strict / --exit-code-mode fail).", len(stale_rows))
        return 1
    if mode == "warn" and stale_rows:
        logger.warning("WARN: %d stale canonical surface(s) found (--exit-code-mode warn).", len(stale_rows))
        return 0
    logger.info("INFO: canonical-freshness scan complete (advisory; --exit-code-mode info).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
