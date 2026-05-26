#!/usr/bin/env python3
"""Per-engagement collaborator-share calculation runbook (Wave R+2 Commit 3).

Canonical doctrine:
  ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md``
Pydantic SSOT:
  ``akos/hlk_collaborator_share.py``
Paired validator:
  ``scripts/validate_collaborator_share.py``
Cursor rule:
  ``.cursor/rules/akos-collaborator-share.mdc``
Skill:
  ``.cursor/skills/collaborator-share-craft/SKILL.md``
SOP:
  ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_COLLABORATOR_SHARE_001.md``
Decision lineage (Wave R+2 rewrite):
  D-IH-86-DA (formula-c-hybrid TRUE-MARGIN benefits formula),
  D-IH-86-EJ (4-base + 1-overlay enum rewrite — supersedes 3-shape enum),
  D-IH-86-EK (parallel_invoice_stream_indicator flag),
  D-IH-86-EL (overlay arithmetic stacking semantics),
  D-IH-86-EM (per-row split application on TRUE-MARGIN benefits),
  D-IH-86-EN (methodology_readiness axis as share_pattern eligibility gate).

The runbook computes — for one engagement_id — the doctrine §2.1 TRUE-MARGIN
formula and applies a per-row split on benefits per the 4 base + 1 overlay
shapes codified at Wave R+2:

UNIFIED FORMULA (all 4 base patterns):

    revenue
  - project_costs (transparent; cash-bearing items only)
  = benefits
  -> per-row split applied per SHARE_REGISTRY row's holistika_share_pct
     + collaborator_share_pct (per-pattern default anchors below).

Per-pattern default anchors (per doctrine §2.3 + §3 worked examples):

(A) deep_partner_65_35 (default; backward-compatible):
        65/35 per-row split on benefits.
        Default-anchor mismatch -> CS-04 WARN; requires OVERRIDE row.
        Example: Websitz / Rushly lived precedent.

(B) bd_intro_only:
        85/15 per-row split on benefits (default `bd_commission_pct` = 15%).
        Single SHARE_REGISTRY row per engagement.
        Collaborator did intro only; performs NO operational work.

(C) joint_venture_aventure:
        50/50 per-row split on benefits (symmetric framing).
        Both parties contribute methodology + execution stack.

(D) consulting_direct (no overlay; solo):
        100/0 per-row split on benefits (Holistika retains 100%).
        Founder + execution team bill against engagement transparently.

(E) consulting_direct + bd_commission_overlay (TWO rows):
        Holistika base row: 85% of benefits.
        Overlay row (sibling, same engagement_id, share_overlay =
        bd_commission_overlay): 15% of benefits.
        CS-09 verifies the overlay-base pairing; CS-03 verifies across-rows
        sum = 100.
        Canonical instantiation: Aïsha on SUEZ POC (D-IH-86-EG).

(F) deep_partner_65_35 + bd_commission_overlay (rare; THREE parties):
        Holistika base row: 65% - overlay_pct = 50% of benefits.
        Deep-partner row: 35% of benefits.
        Overlay row: overlay_pct (default 15%) of benefits.
        Validator + runbook handle multi-row case generically.

The runbook is now unified — there is no per-pattern arithmetic branching.
All patterns compute benefits = revenue - costs and apply each row's
holistika_share_pct / collaborator_share_pct on benefits. Per-pattern
behaviour surfaces in (a) default-anchor advisory notes; (b)
methodology_readiness eligibility checks; (c) overlay-base pairing validation;
(d) parallel_invoice_stream_indicator settlement reminders.

Project costs aggregate (TRUE-MARGIN inputs, all patterns):

  (a) Collaborator billed time     = sum(SHARE_REGISTRY rows whose
                                          engagement_id matches) of
                                          collaborator_billed_rate * billed_hours
                                          (when billed_hours provided via
                                          --collaborator-hours arg).
  (b) Vendor billed services       = sum(HOLISTIKA_VENDOR_SERVICES_BILLED
                                          rows whose engagement_id matches AND
                                          bill_mode='billed') of
                                          billed_hours * billed_rate
                                          (in_kind rows contribute 0).
  (c) Direct project pass-throughs = sum of --direct-cost <amount> args (CLI
                                      pass-through for external invoices that
                                      the engagement absorbs).
  (d) Founder billed time          = --founder-hours * --founder-rate when
                                      both flags present (per doctrine §2.2
                                      founder-bill-mode policy).

CLI shape::

    py scripts/collaborator_share_calculate.py \\
        --engagement-id ENG-SUEZ-POC-2026 \\
        --revenue 38000 \\
        --collaborator-id POI-AISHA-2026 \\
        --founder-hours 80 \\
        --founder-rate 250 \\
        --direct-cost 1500 \\
        --currency EUR \\
        --emit-report

    py scripts/collaborator_share_calculate.py --self-test

The default mode prints a settlement table to stdout. --emit-report also
writes a markdown report under
``docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/
collaborator-share-<engagement_id>-<YYYY-MM-DD>.md``.

Per ``akos-executable-process-catalog.mdc`` Rule 1: this runbook is the
AC-AUTOMATION half of the SOP+runbook pair. The SOP carries the AC-HUMAN
narrative + operator walkthrough.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import logging
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_collaborator_share import (  # noqa: E402
    CSV_PATH_RELATIVE_SHARE_REGISTRY,
    CSV_PATH_RELATIVE_VENDOR_BILLED,
    DEFAULT_BD_COMMISSION_OVERLAY_PCT,
    DEFAULT_BD_INTRO_COLLABORATOR_PCT,
    DEFAULT_BD_INTRO_HOLISTIKA_PCT,
    DEFAULT_COLLABORATOR_SHARE_PCT,
    DEFAULT_CONSULTING_DIRECT_COLLABORATOR_PCT_SOLO,
    DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_SOLO,
    DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_WITH_OVERLAY,
    DEFAULT_HOLISTIKA_SHARE_PCT,
    DEFAULT_JOINT_VENTURE_COLLABORATOR_PCT,
    DEFAULT_JOINT_VENTURE_HOLISTIKA_PCT,
    DEFAULT_SHARE_PATTERN,
    VALID_OVERLAY_BASE_PAIRINGS,
    VALID_SHARE_OVERLAYS,
    VALID_SHARE_PATTERNS,
    methodology_permits_share_pattern,
    methodology_readiness_is_valid,
    overlay_base_pairing_is_valid,
    share_overlay_is_valid,
    share_pattern_is_valid,
)

logger = logging.getLogger(__name__)

SHARE_REGISTRY_CSV = REPO_ROOT / CSV_PATH_RELATIVE_SHARE_REGISTRY
VENDOR_BILLED_CSV = REPO_ROOT / CSV_PATH_RELATIVE_VENDOR_BILLED

# Per-pattern default anchor lookup. CS-04 advisory fires when a row's
# (h_pct, c_pct) deviates from its pattern's anchor without a matching
# OVERRIDE row. For consulting_direct the runbook detects overlay presence
# at the engagement scope to decide between SOLO (100/0) and WITH_OVERLAY
# (85/15) anchors.
_PER_PATTERN_DEFAULT_ANCHORS: dict[str, tuple[int, int]] = {
    "deep_partner_65_35": (
        DEFAULT_HOLISTIKA_SHARE_PCT,
        DEFAULT_COLLABORATOR_SHARE_PCT,
    ),
    "bd_intro_only": (
        DEFAULT_BD_INTRO_HOLISTIKA_PCT,
        DEFAULT_BD_INTRO_COLLABORATOR_PCT,
    ),
    "joint_venture_aventure": (
        DEFAULT_JOINT_VENTURE_HOLISTIKA_PCT,
        DEFAULT_JOINT_VENTURE_COLLABORATOR_PCT,
    ),
    # consulting_direct anchor resolved dynamically per engagement scope
    # (overlay-presence detection in _default_anchor_for_row).
}


def _today() -> str:
    return _dt.date.today().isoformat()


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return [
            {k: (v or "") for k, v in row.items() if k}
            for row in csv.DictReader(fh)
        ]


def _share_priority(status: str) -> int:
    return {
        "active": 0,
        "signed": 1,
        "settled": 2,
        "proposed": 3,
        "draft": 4,
        "archived": 5,
    }.get(status, 99)


def _read_all_engagement_share_rows(engagement_id: str) -> list[dict[str, str]]:
    """Return every active-status SHARE_REGISTRY row for an engagement.

    Multi-row engagements (overlay-bearing or multi-party JV) require the
    runbook to consider ALL rows when computing the settlement breakdown,
    not just the row matching a single collaborator_id (that pattern was a
    pre-rewrite single-shape assumption).
    """
    rows = [
        r for r in _read_rows(SHARE_REGISTRY_CSV)
        if r.get("engagement_id") == engagement_id
    ]
    rows.sort(key=lambda r: _share_priority(r.get("status", "draft")))
    return rows


def _read_share_row(
    engagement_id: str, collaborator_id: str | None
) -> dict[str, str] | None:
    """Return the active SHARE_REGISTRY row for (engagement, collaborator), if any.

    Preserved for the single-collaborator-focused settlement output path
    (when --collaborator-id is supplied). Multi-row settlement work uses
    ``_read_all_engagement_share_rows`` instead.
    """
    candidates = _read_all_engagement_share_rows(engagement_id)
    if collaborator_id:
        candidates = [
            r for r in candidates if r.get("collaborator_id") == collaborator_id
        ]
    return candidates[0] if candidates else None


def _share_pattern_for_row(share_row: dict[str, str] | None) -> str:
    """Resolve the share_pattern for a SHARE_REGISTRY row; fall back to the
    doctrine default when missing or invalid (caller renders an advisory
    note in the settlement output so the operator can fix the CSV).
    """
    if not share_row:
        return DEFAULT_SHARE_PATTERN
    raw = (share_row.get("share_pattern") or "").strip()
    if share_pattern_is_valid(raw):
        return raw
    return DEFAULT_SHARE_PATTERN


def _share_overlay_for_row(share_row: dict[str, str] | None) -> str:
    """Resolve the share_overlay for a SHARE_REGISTRY row (empty string when
    no overlay declared, which is the doctrine default).
    """
    if not share_row:
        return ""
    raw = (share_row.get("share_overlay") or "").strip()
    return raw


def _methodology_readiness_for_row(share_row: dict[str, str] | None) -> str:
    if not share_row:
        return ""
    return (share_row.get("methodology_readiness") or "").strip()


def _parallel_invoice_stream_indicator_for_row(
    share_row: dict[str, str] | None,
) -> bool:
    if not share_row:
        return False
    raw = (share_row.get("parallel_invoice_stream_indicator") or "").strip().lower()
    return raw in {"true", "1", "yes", "y"}


def _engagement_has_overlay(engagement_id: str) -> bool:
    """Return True iff any SHARE_REGISTRY row for the engagement carries a
    non-empty share_overlay value. Used by the consulting_direct anchor
    resolver: solo (100/0) when no overlay sibling row exists; with-overlay
    (85/15 + 15-overlay) when a sibling overlay row exists.
    """
    for r in _read_all_engagement_share_rows(engagement_id):
        if (r.get("share_overlay") or "").strip():
            return True
    return False


def _default_anchor_for_row(
    pattern: str, engagement_id: str
) -> tuple[int, int]:
    """Return the (holistika_pct, collaborator_pct) default anchor for a
    row given its share_pattern and the engagement scope (overlay presence
    detection for consulting_direct).
    """
    if pattern in _PER_PATTERN_DEFAULT_ANCHORS:
        return _PER_PATTERN_DEFAULT_ANCHORS[pattern]
    if pattern == "consulting_direct":
        if _engagement_has_overlay(engagement_id):
            return (
                DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_WITH_OVERLAY,
                DEFAULT_BD_COMMISSION_OVERLAY_PCT,
            )
        return (
            DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_SOLO,
            DEFAULT_CONSULTING_DIRECT_COLLABORATOR_PCT_SOLO,
        )
    return (DEFAULT_HOLISTIKA_SHARE_PCT, DEFAULT_COLLABORATOR_SHARE_PCT)


def _collect_cost_lines(
    engagement_id: str,
    collaborator_id: str | None,
    collaborator_hours: float | None,
    collaborator_billed_rate: float,
    founder_hours: float | None,
    founder_rate: float | None,
    direct_costs: list[float],
) -> list[dict[str, Any]]:
    """Compose the transparent project-cost lines for the TRUE-MARGIN formula.

    All 4 base patterns subtract the same cost roster from revenue to derive
    benefits. The per-pattern split is then applied on benefits — there is
    no per-pattern cost-collection branching at Wave R+2 (the pre-rewrite
    orchestration_broker pattern that skipped costs was removed under
    D-IH-86-EJ).
    """
    cost_lines: list[dict[str, Any]] = []
    if collaborator_hours and collaborator_billed_rate > 0:
        amt = collaborator_hours * collaborator_billed_rate
        cost_lines.append({
            "label": f"Collaborator billed time ({collaborator_id or '?'})",
            "hours": collaborator_hours,
            "rate": collaborator_billed_rate,
            "amount": round(amt, 2),
            "kind": "collaborator_billed_time",
        })
    if founder_hours and founder_rate and founder_rate > 0:
        amt = founder_hours * founder_rate
        cost_lines.append({
            "label": "Founder billed time",
            "hours": founder_hours,
            "rate": founder_rate,
            "amount": round(amt, 2),
            "kind": "founder_billed_time",
        })
    for vrow in _read_rows(VENDOR_BILLED_CSV):
        if vrow.get("engagement_id") != engagement_id:
            continue
        if vrow.get("bill_mode") != "billed":
            continue
        try:
            hrs = float(vrow.get("billed_hours") or "0")
            rate = float(vrow.get("billed_rate") or "0")
        except ValueError:
            continue
        if hrs <= 0 or rate <= 0:
            continue
        cost_lines.append({
            "label": f"Vendor billed service ({vrow.get('holistika_service_class', '?')})",
            "hours": hrs,
            "rate": rate,
            "amount": round(hrs * rate, 2),
            "kind": "vendor_billed_service",
        })
    for amt in direct_costs:
        if amt <= 0:
            continue
        cost_lines.append({
            "label": "Direct project pass-through",
            "hours": None,
            "rate": None,
            "amount": round(amt, 2),
            "kind": "direct_pass_through",
        })
    return cost_lines


def _compute_row_breakdown(
    share_row: dict[str, str],
    benefits: float,
    engagement_id: str,
) -> dict[str, Any]:
    """Compute one SHARE_REGISTRY row's split application on benefits + the
    per-row advisory notes (default-anchor / methodology / overlay-pairing /
    parallel-invoice-stream).
    """
    try:
        h_pct = int(share_row.get("holistika_share_pct") or DEFAULT_HOLISTIKA_SHARE_PCT)
        c_pct = int(share_row.get("collaborator_share_pct") or DEFAULT_COLLABORATOR_SHARE_PCT)
    except ValueError:
        h_pct = DEFAULT_HOLISTIKA_SHARE_PCT
        c_pct = DEFAULT_COLLABORATOR_SHARE_PCT

    pattern = _share_pattern_for_row(share_row)
    overlay = _share_overlay_for_row(share_row)
    methodology = _methodology_readiness_for_row(share_row)
    parallel_invoice = _parallel_invoice_stream_indicator_for_row(share_row)

    holistika_amount = round(benefits * (h_pct / 100.0), 2)
    collaborator_amount = round(benefits * (c_pct / 100.0), 2)

    advisory_notes: list[str] = []

    anchor_h, anchor_c = _default_anchor_for_row(pattern, engagement_id)
    if (h_pct, c_pct) != (anchor_h, anchor_c):
        override_id = (share_row.get("share_override_decision_id") or "").strip()
        if not override_id:
            advisory_notes.append(
                f"split ({h_pct}/{c_pct}) deviates from pattern "
                f"'{pattern}' default anchor ({anchor_h}/{anchor_c}) "
                "without a matching share_override_decision_id "
                "(CS-04 WARN at validator)"
            )
        else:
            advisory_notes.append(
                f"split ({h_pct}/{c_pct}) is operator-ratified deviation "
                f"from pattern '{pattern}' anchor ({anchor_h}/{anchor_c}) "
                f"via {override_id}"
            )

    if methodology:
        if not methodology_readiness_is_valid(methodology):
            advisory_notes.append(
                f"methodology_readiness '{methodology}' is unknown "
                "(CS-08 FAIL at validator)"
            )
        elif not methodology_permits_share_pattern(methodology, pattern):
            advisory_notes.append(
                f"methodology_readiness '{methodology}' does NOT permit "
                f"share_pattern '{pattern}' per the doctrine §2.4 "
                "permissibility matrix (CS-09 FAIL at validator); "
                "reclassify the pattern or upgrade the collaborator's "
                "methodology state"
            )

    if overlay:
        if not share_overlay_is_valid(overlay):
            advisory_notes.append(
                f"share_overlay '{overlay}' is unknown "
                "(CS-08 FAIL at validator)"
            )
        elif not overlay_base_pairing_is_valid(overlay, pattern):
            permitted = sorted(VALID_OVERLAY_BASE_PAIRINGS.get(overlay, frozenset()))
            advisory_notes.append(
                f"share_overlay '{overlay}' is NOT permitted on base "
                f"pattern '{pattern}'; permitted bases: "
                f"{', '.join(permitted) or '(none)'} "
                "(CS-09 FAIL at validator)"
            )

    if parallel_invoice:
        advisory_notes.append(
            "parallel_invoice_stream_indicator=True: collaborator "
            "carries an independent B2B invoice stream with the "
            "customer that Holistika is NOT party to. Settlement "
            "below covers ONLY the Holistika-orchestrated revenue; "
            "operator must reconcile the parallel stream separately "
            "(D-IH-86-EK)"
        )

    return {
        "share_id": share_row.get("share_id", ""),
        "collaborator_id": share_row.get("collaborator_id", ""),
        "share_pattern": pattern,
        "share_overlay": overlay,
        "methodology_readiness": methodology,
        "parallel_invoice_stream_indicator": parallel_invoice,
        "holistika_share_pct": h_pct,
        "collaborator_share_pct": c_pct,
        "anchor_holistika_pct": anchor_h,
        "anchor_collaborator_pct": anchor_c,
        "split_matches_anchor": (h_pct, c_pct) == (anchor_h, anchor_c),
        "holistika_share_amount": holistika_amount,
        "collaborator_share_amount": collaborator_amount,
        "share_override_decision_id": (share_row.get("share_override_decision_id") or "").strip(),
        "advisory_notes": advisory_notes,
    }


def _empty_row_breakdown_from_overrides(
    engagement_id: str,
    collaborator_id: str | None,
    h_pct: int,
    c_pct: int,
    pattern: str,
    overlay: str,
    benefits: float,
) -> dict[str, Any]:
    """Build a row breakdown for what-if scenarios where no CSV row exists
    yet (--share-pattern + --share-overlay CLI overrides supplied).
    """
    holistika_amount = round(benefits * (h_pct / 100.0), 2)
    collaborator_amount = round(benefits * (c_pct / 100.0), 2)
    anchor_h, anchor_c = _default_anchor_for_row(pattern, engagement_id)
    return {
        "share_id": "",
        "collaborator_id": collaborator_id or "",
        "share_pattern": pattern,
        "share_overlay": overlay,
        "methodology_readiness": "",
        "parallel_invoice_stream_indicator": False,
        "holistika_share_pct": h_pct,
        "collaborator_share_pct": c_pct,
        "anchor_holistika_pct": anchor_h,
        "anchor_collaborator_pct": anchor_c,
        "split_matches_anchor": (h_pct, c_pct) == (anchor_h, anchor_c),
        "holistika_share_amount": holistika_amount,
        "collaborator_share_amount": collaborator_amount,
        "share_override_decision_id": "",
        "advisory_notes": [
            "what-if scenario: no SHARE_REGISTRY row exists for this "
            "engagement; values driven by CLI overrides only"
        ],
    }


def calculate_settlement(
    engagement_id: str,
    revenue: float,
    collaborator_id: str | None,
    collaborator_hours: float | None,
    founder_hours: float | None,
    founder_rate: float | None,
    direct_costs: list[float],
    currency: str,
    share_pattern_override: str | None = None,
    share_overlay_override: str | None = None,
) -> dict[str, Any]:
    """Compute the settlement dict for a given engagement.

    Wave R+2 unified TRUE-MARGIN architecture: all 4 base patterns
    (deep_partner_65_35 / bd_intro_only / joint_venture_aventure /
    consulting_direct) compute benefits = revenue - costs and apply each
    SHARE_REGISTRY row's split on benefits. Per-pattern behaviour surfaces
    as advisory notes only (default-anchor mismatch, methodology eligibility,
    overlay-base pairing, parallel-invoice-stream indicator).

    Pure function — no I/O beyond reading the canonical CSVs through
    ``_read_share_row`` / ``_read_rows``. Suitable for unit tests.

    Returns a dict with:
        engagement_id, currency, revenue, cost_lines, total_costs, benefits,
        primary_row_share_pattern (the row matched by collaborator_id or the
        first engagement row when no collaborator filter), per_row_breakdowns
        (list[dict] — one per active SHARE_REGISTRY row for the engagement),
        across_rows_total_holistika_pct, across_rows_total_collaborator_pct,
        across_rows_split_sums_to_100 (bool; CS-03 mirror),
        across_rows_holistika_amount, across_rows_collaborator_amount,
        advisory_notes, computed_at.

    Args:
        share_pattern_override: optional CLI-supplied override; used for
            what-if scenarios when no SHARE_REGISTRY row exists yet (uses
            the override to synthesize a one-row breakdown).
        share_overlay_override: optional CLI-supplied overlay value paired
            with share_pattern_override.
    """
    advisory_notes: list[str] = []

    # Resolve the focal row (for cost-collection collaborator_billed_rate +
    # primary settlement view). Multi-row engagements still surface every
    # row in per_row_breakdowns.
    focal_row = _read_share_row(engagement_id, collaborator_id)
    collaborator_billed_rate = 0.0
    if focal_row:
        try:
            collaborator_billed_rate = float(
                focal_row.get("collaborator_billed_rate") or "0"
            )
        except ValueError:
            collaborator_billed_rate = 0.0

    cost_lines = _collect_cost_lines(
        engagement_id=engagement_id,
        collaborator_id=collaborator_id,
        collaborator_hours=collaborator_hours,
        collaborator_billed_rate=collaborator_billed_rate,
        founder_hours=founder_hours,
        founder_rate=founder_rate,
        direct_costs=direct_costs,
    )
    total_costs = round(sum(line["amount"] for line in cost_lines), 2)
    benefits = round(revenue - total_costs, 2)

    all_rows = _read_all_engagement_share_rows(engagement_id)
    per_row_breakdowns: list[dict[str, Any]] = []

    if all_rows:
        for row in all_rows:
            per_row_breakdowns.append(_compute_row_breakdown(row, benefits, engagement_id))
    elif share_pattern_override and share_pattern_is_valid(share_pattern_override):
        # No CSV rows yet — synthesize a one-row what-if breakdown from CLI.
        synth_pattern = share_pattern_override
        synth_overlay = ""
        if share_overlay_override and share_overlay_is_valid(share_overlay_override):
            synth_overlay = share_overlay_override
        anchor_h, anchor_c = _default_anchor_for_row(synth_pattern, engagement_id)
        per_row_breakdowns.append(
            _empty_row_breakdown_from_overrides(
                engagement_id=engagement_id,
                collaborator_id=collaborator_id,
                h_pct=anchor_h,
                c_pct=anchor_c,
                pattern=synth_pattern,
                overlay=synth_overlay,
                benefits=benefits,
            )
        )

    # Across-rows aggregate (CS-03 mirror; advisory only — validator owns FAIL).
    total_h_pct = sum(b["holistika_share_pct"] for b in per_row_breakdowns)
    total_c_pct = sum(b["collaborator_share_pct"] for b in per_row_breakdowns)
    sum_to_100 = (total_h_pct + total_c_pct) == 100
    across_rows_h_amount = round(
        sum(b["holistika_share_amount"] for b in per_row_breakdowns), 2
    )
    across_rows_c_amount = round(
        sum(b["collaborator_share_amount"] for b in per_row_breakdowns), 2
    )

    if per_row_breakdowns and not sum_to_100:
        advisory_notes.append(
            f"engagement {engagement_id!r} across-rows split sum "
            f"{total_h_pct + total_c_pct}% != 100% "
            f"(CS-03 FAIL at validator); ensure overlay + base rows are "
            "correctly paired"
        )

    primary_pattern = (
        per_row_breakdowns[0]["share_pattern"]
        if per_row_breakdowns
        else DEFAULT_SHARE_PATTERN
    )

    return {
        "engagement_id": engagement_id,
        "collaborator_id": collaborator_id,
        "currency": currency,
        "revenue": round(revenue, 2),
        "cost_lines": cost_lines,
        "total_costs": total_costs,
        "benefits": benefits,
        "primary_row_share_pattern": primary_pattern,
        "per_row_breakdowns": per_row_breakdowns,
        "across_rows_total_holistika_pct": total_h_pct,
        "across_rows_total_collaborator_pct": total_c_pct,
        "across_rows_split_sums_to_100": sum_to_100,
        "across_rows_holistika_amount": across_rows_h_amount,
        "across_rows_collaborator_amount": across_rows_c_amount,
        "share_row_present": focal_row is not None,
        "share_row_id": (focal_row or {}).get("share_id", ""),
        "advisory_notes": advisory_notes,
        "computed_at": _today(),
    }


def _fmt_amount(value: Any, currency: str) -> str:
    """Format an optional numeric amount; return MANUAL placeholder when None."""
    if value is None:
        return "MANUAL"
    return f"{value:.2f} {currency}"


def render_settlement_markdown(settlement: dict[str, Any]) -> str:
    """Operator-readable markdown table for one engagement settlement.

    Unified Wave R+2 layout: TRUE-MARGIN cost-line + benefits header
    table (same for all 4 base patterns) + per-row split breakdown table
    (one block per SHARE_REGISTRY row for the engagement, supporting
    multi-row overlay + JV multi-party cases) + advisory notes.
    """
    cur = settlement["currency"]
    primary = settlement.get("primary_row_share_pattern", DEFAULT_SHARE_PATTERN)
    per_row = settlement.get("per_row_breakdowns") or []

    lines = [
        f"# Collaborator Share Settlement — {settlement['engagement_id']}",
        "",
        f"- **Computed at**: {settlement['computed_at']}",
        f"- **Currency**: {cur}",
        f"- **Primary share_pattern**: `{primary}`",
        f"- **SHARE_REGISTRY rows**: {len(per_row)}",
    ]
    if settlement.get("share_row_id"):
        lines.append(
            f"- **Focal row**: `{settlement['share_row_id']}` "
            f"(collaborator `{settlement.get('collaborator_id') or '-'}`)"
        )

    lines.extend([
        "",
        "## TRUE-MARGIN (revenue minus transparent costs)",
        "",
        "| Line | Hours | Rate | Amount |",
        "|:---|---:|---:|---:|",
        f"| **Revenue** | --- | --- | **{settlement['revenue']:.2f} {cur}** |",
    ])
    for line in settlement["cost_lines"]:
        hours = f"{line['hours']:.2f}" if line["hours"] is not None else "---"
        rate = f"{line['rate']:.2f} {cur}" if line["rate"] is not None else "---"
        lines.append(
            f"| {line['label']} | {hours} | {rate} | "
            f"-{line['amount']:.2f} {cur} |"
        )
    lines.append(
        f"| **Total project costs** | --- | --- | "
        f"**-{settlement['total_costs']:.2f} {cur}** |"
    )
    lines.append(
        f"| **Benefits (= revenue - costs)** | --- | --- | "
        f"**{settlement['benefits']:.2f} {cur}** |"
    )

    lines.extend([
        "",
        "## Per-row split application on benefits",
        "",
        "| share_id | collaborator_id | pattern | overlay | H% | C% | Anchor | H amount | C amount |",
        "|:---|:---|:---|:---|---:|---:|:---|---:|---:|",
    ])
    if per_row:
        for b in per_row:
            anchor = f"{b['anchor_holistika_pct']}/{b['anchor_collaborator_pct']}"
            if b["split_matches_anchor"]:
                anchor_cell = f"{anchor} (default)"
            else:
                deviation_note = (
                    f"{anchor} - deviation"
                    + (f" via {b['share_override_decision_id']}" if b["share_override_decision_id"] else "")
                )
                anchor_cell = deviation_note
            lines.append(
                f"| `{b['share_id'] or '(synthesized)'}` "
                f"| `{b['collaborator_id'] or '-'}` "
                f"| `{b['share_pattern']}` "
                f"| `{b['share_overlay'] or '-'}` "
                f"| {b['holistika_share_pct']} "
                f"| {b['collaborator_share_pct']} "
                f"| {anchor_cell} "
                f"| {_fmt_amount(b['holistika_share_amount'], cur)} "
                f"| {_fmt_amount(b['collaborator_share_amount'], cur)} |"
            )
        lines.append(
            f"| **TOTAL** | --- | --- | --- "
            f"| **{settlement['across_rows_total_holistika_pct']}** "
            f"| **{settlement['across_rows_total_collaborator_pct']}** "
            f"| --- "
            f"| **{_fmt_amount(settlement['across_rows_holistika_amount'], cur)}** "
            f"| **{_fmt_amount(settlement['across_rows_collaborator_amount'], cur)}** |"
        )
        lines.append("")
        if settlement["across_rows_split_sums_to_100"]:
            lines.append(
                "> Across-rows split sums to 100% (CS-03 invariant holds)."
            )
        else:
            lines.append(
                "> **WARNING**: Across-rows split does NOT sum to 100% "
                "(CS-03 FAIL at validator)."
            )
    else:
        lines.append(
            "| _no SHARE_REGISTRY rows for engagement; supply --share-pattern "
            "for what-if_ | --- | --- | --- | --- | --- | --- | --- | --- |"
        )

    # Per-row advisory notes (collated).
    per_row_advisories: list[tuple[str, str]] = []
    for b in per_row:
        for note in b.get("advisory_notes") or []:
            per_row_advisories.append(
                (b["share_id"] or b["collaborator_id"] or "(synth)", note)
            )

    advisory = settlement.get("advisory_notes") or []
    if advisory or per_row_advisories:
        lines.extend(["", "## Advisory notes", ""])
        for note in advisory:
            lines.append(f"- (engagement) {note}")
        for row_label, note in per_row_advisories:
            lines.append(f"- (row `{row_label}`) {note}")

    lines.append("")
    lines.append(
        "> Generated by `scripts/collaborator_share_calculate.py` per "
        "`COLLABORATOR_SHARE_DOCTRINE.md` §2 + §3 (Wave R+2 4-base + "
        "1-overlay enum)."
    )
    return "\n".join(lines) + "\n"


def self_test() -> int:
    """Worked-example fixture validation; zero-cost; wired into release-gate.

    Five in-memory fixtures (no CSV reads) verify the calculator's
    unified TRUE-MARGIN formula + per-pattern split application:

      (A) deep_partner_65_35 (no CSV row; CLI what-if):
            EUR 100k revenue; EUR 20k direct cost; benefits EUR 80k;
            65/35 split => Holistika EUR 52k + Collaborator EUR 28k.

      (B) bd_intro_only (no CSV row; CLI what-if):
            EUR 100k revenue; EUR 20k direct cost; benefits EUR 80k;
            85/15 split => Holistika EUR 68k + Collaborator EUR 12k.

      (C) joint_venture_aventure (no CSV row; CLI what-if):
            EUR 100k revenue; EUR 20k direct cost; benefits EUR 80k;
            50/50 split => Holistika EUR 40k + Collaborator EUR 40k.

      (D) consulting_direct SOLO (no overlay; no CSV row; CLI what-if):
            EUR 100k revenue; EUR 20k direct cost; benefits EUR 80k;
            100/0 split => Holistika EUR 80k + Collaborator EUR 0.

      (E) Unified-formula benefits arithmetic:
            EUR 38k revenue; EUR 8k direct cost (SUEZ-shape proxy);
            benefits EUR 30k. (Verifies the formula independent of
            pattern selection.)
    """
    # (A) deep_partner_65_35
    s_a = calculate_settlement(
        engagement_id="ENG-SELFTEST-DP-2026",
        revenue=100_000.0,
        collaborator_id=None,
        collaborator_hours=None,
        founder_hours=None,
        founder_rate=None,
        direct_costs=[20_000.0],
        currency="EUR",
        share_pattern_override="deep_partner_65_35",
    )
    if s_a["primary_row_share_pattern"] != "deep_partner_65_35":
        return 1
    if s_a["revenue"] != 100_000.0:
        return 2
    if s_a["total_costs"] != 20_000.0:
        return 3
    if s_a["benefits"] != 80_000.0:
        return 4
    if len(s_a["per_row_breakdowns"]) != 1:
        return 5
    if s_a["per_row_breakdowns"][0]["holistika_share_amount"] != 52_000.0:
        return 6
    if s_a["per_row_breakdowns"][0]["collaborator_share_amount"] != 28_000.0:
        return 7
    if s_a["per_row_breakdowns"][0]["holistika_share_pct"] != 65:
        return 8
    if s_a["per_row_breakdowns"][0]["collaborator_share_pct"] != 35:
        return 9

    # (B) bd_intro_only (85/15)
    s_b = calculate_settlement(
        engagement_id="ENG-SELFTEST-BD-2026",
        revenue=100_000.0,
        collaborator_id=None,
        collaborator_hours=None,
        founder_hours=None,
        founder_rate=None,
        direct_costs=[20_000.0],
        currency="EUR",
        share_pattern_override="bd_intro_only",
    )
    if s_b["primary_row_share_pattern"] != "bd_intro_only":
        return 10
    if s_b["benefits"] != 80_000.0:
        return 11
    if s_b["per_row_breakdowns"][0]["holistika_share_amount"] != 68_000.0:
        return 12
    if s_b["per_row_breakdowns"][0]["collaborator_share_amount"] != 12_000.0:
        return 13
    if s_b["per_row_breakdowns"][0]["holistika_share_pct"] != 85:
        return 14
    if s_b["per_row_breakdowns"][0]["collaborator_share_pct"] != 15:
        return 15

    # (C) joint_venture_aventure (50/50)
    s_c = calculate_settlement(
        engagement_id="ENG-SELFTEST-JV-2026",
        revenue=100_000.0,
        collaborator_id=None,
        collaborator_hours=None,
        founder_hours=None,
        founder_rate=None,
        direct_costs=[20_000.0],
        currency="EUR",
        share_pattern_override="joint_venture_aventure",
    )
    if s_c["primary_row_share_pattern"] != "joint_venture_aventure":
        return 16
    if s_c["benefits"] != 80_000.0:
        return 17
    if s_c["per_row_breakdowns"][0]["holistika_share_amount"] != 40_000.0:
        return 18
    if s_c["per_row_breakdowns"][0]["collaborator_share_amount"] != 40_000.0:
        return 19

    # (D) consulting_direct SOLO (100/0)
    s_d = calculate_settlement(
        engagement_id="ENG-SELFTEST-CD-2026",
        revenue=100_000.0,
        collaborator_id=None,
        collaborator_hours=None,
        founder_hours=None,
        founder_rate=None,
        direct_costs=[20_000.0],
        currency="EUR",
        share_pattern_override="consulting_direct",
    )
    if s_d["primary_row_share_pattern"] != "consulting_direct":
        return 20
    if s_d["benefits"] != 80_000.0:
        return 21
    if s_d["per_row_breakdowns"][0]["holistika_share_amount"] != 80_000.0:
        return 22
    if s_d["per_row_breakdowns"][0]["collaborator_share_amount"] != 0.0:
        return 23
    if s_d["per_row_breakdowns"][0]["holistika_share_pct"] != 100:
        return 24
    if s_d["per_row_breakdowns"][0]["collaborator_share_pct"] != 0:
        return 25

    # (E) Unified-formula benefits arithmetic (SUEZ-shape proxy)
    s_e = calculate_settlement(
        engagement_id="ENG-SELFTEST-SUEZ-2026",
        revenue=38_000.0,
        collaborator_id=None,
        collaborator_hours=None,
        founder_hours=None,
        founder_rate=None,
        direct_costs=[8_000.0],
        currency="EUR",
        share_pattern_override="consulting_direct",
    )
    if s_e["benefits"] != 30_000.0:
        return 26
    if s_e["total_costs"] != 8_000.0:
        return 27

    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engagement-id", default=None)
    parser.add_argument("--revenue", type=float, default=None)
    parser.add_argument("--collaborator-id", default=None)
    parser.add_argument("--collaborator-hours", type=float, default=None)
    parser.add_argument("--founder-hours", type=float, default=None)
    parser.add_argument("--founder-rate", type=float, default=None)
    parser.add_argument(
        "--direct-cost", type=float, action="append", default=None,
        help="add a direct pass-through cost (currency amount); may be repeated",
    )
    parser.add_argument("--currency", default="EUR")
    parser.add_argument(
        "--share-pattern",
        choices=sorted(VALID_SHARE_PATTERNS),
        default=None,
        help=(
            "what-if override for the share_pattern (used when no "
            "SHARE_REGISTRY row exists for the engagement yet; ignored "
            "when CSV rows are present — they always take precedence)"
        ),
    )
    parser.add_argument(
        "--share-overlay",
        choices=sorted(VALID_SHARE_OVERLAYS),
        default=None,
        help=(
            "what-if overlay value paired with --share-pattern; ignored "
            "when CSV rows are present"
        ),
    )
    parser.add_argument("--emit-report", action="store_true")
    parser.add_argument("--report-path", type=Path, default=None)
    parser.add_argument("--emit-json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    if not args.engagement_id or args.revenue is None:
        parser.error("--engagement-id and --revenue are required (unless --self-test)")

    settlement = calculate_settlement(
        engagement_id=args.engagement_id,
        revenue=args.revenue,
        collaborator_id=args.collaborator_id,
        collaborator_hours=args.collaborator_hours,
        founder_hours=args.founder_hours,
        founder_rate=args.founder_rate,
        direct_costs=list(args.direct_cost or []),
        currency=args.currency,
        share_pattern_override=args.share_pattern,
        share_overlay_override=args.share_overlay,
    )

    if args.emit_json:
        json.dump(settlement, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(render_settlement_markdown(settlement))

    if args.emit_report:
        report_path = args.report_path or (
            REPO_ROOT
            / "docs/wip/planning/86-initiative-cluster-execution-coordinator/reports"
            / f"collaborator-share-{args.engagement_id}-{_today()}.md"
        )
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_settlement_markdown(settlement), encoding="utf-8")
        try:
            shown_path = report_path.relative_to(REPO_ROOT)
        except ValueError:
            shown_path = report_path
        print(
            f"  wrote {shown_path}",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
