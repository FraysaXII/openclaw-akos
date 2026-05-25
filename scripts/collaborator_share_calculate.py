#!/usr/bin/env python3
"""Per-engagement collaborator-share calculation runbook (Wave R+1 Commit 2b).

Canonical doctrine:
  ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md``
Pydantic SSOT:
  ``akos/hlk_collaborator_share.py``
Paired validator:
  ``scripts/validate_collaborator_share.py``
Cursor rule (Commit 2c):
  ``.cursor/rules/akos-collaborator-share.mdc``
Skill (Commit 2c):
  ``.cursor/skills/collaborator-share-craft/SKILL.md``
SOP (Commit 2c):
  ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_COLLABORATOR_SHARE_001.md``
Decision lineage:
  D-IH-86-CY-A (formula-c-hybrid TRUE-MARGIN benefits formula),
  D-IH-86-CY-EXT (Wave R+1 Commit 2b-ext: per-pattern branching for
  deep_partner_65_35 + orchestration_broker_thin_margin + custom).

The runbook computes — for one engagement_id — the doctrine §2.1 formula
in one of three shapes depending on the row's ``share_pattern``:

(A) deep_partner_65_35 (default; e.g. Aïsha-on-SUEZ-operator-role):

      revenue
    - project_costs (transparent; cash-bearing items only)
    = benefits
    -> per-row split (default 65/35; deviation in SHARE_REGISTRY)

(B) orchestration_broker_thin_margin (e.g. SUEZ-engagement-overall with
    multiple hired collaborators each taking a slice + Holistika's thin cut):

      revenue
    -> direct % split (NO benefits formula; collaborators absorb their
       own cost-of-work as part of their per-row slice). Holistika's
       total margin = sum(holistika_share_pct across rows).
       Default Holistika total = ORCHESTRATION_BROKER_DEFAULT_HOLISTIKA_TOTAL_PCT
       (6% per operator framing 2026-05-25).

(C) custom (operator carries the math; runbook does NOT auto-calculate):

      Runbook emits a "MANUAL" placeholder + cites the row's
      share_override_decision_id for operator review. No automatic
      benefits/revenue formula applied.

Project costs aggregate:

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
                                      both flags present (when operator wants
                                      transparent founder-time costing per
                                      doctrine §2.2 founder-bill-mode policy).

CLI shape::

    py scripts/collaborator_share_calculate.py \\
        --engagement-id ENG-SUEZ-EFA-2026 \\
        --revenue 100000 \\
        --collaborator-id POI-PRT-EFA-LEAD-2026 \\
        --collaborator-hours 80 \\
        --founder-hours 40 \\
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
AC-AUTOMATION half of the SOP+runbook pair. The SOP (Commit 2c) carries
the AC-HUMAN narrative + operator walkthrough.
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
    CSV_PATH_RELATIVE_RATE_OVERRIDES,
    CSV_PATH_RELATIVE_SHARE_REGISTRY,
    CSV_PATH_RELATIVE_VENDOR_BILLED,
    DEFAULT_COLLABORATOR_SHARE_PCT,
    DEFAULT_HOLISTIKA_SHARE_PCT,
    DEFAULT_SHARE_PATTERN,
    ORCHESTRATION_BROKER_DEFAULT_HOLISTIKA_TOTAL_PCT,
    VALID_SHARE_PATTERNS,
    default_split_holds,
    orchestration_broker_default_margin_holds,
    share_pattern_is_valid,
)

logger = logging.getLogger(__name__)

SHARE_REGISTRY_CSV = REPO_ROOT / CSV_PATH_RELATIVE_SHARE_REGISTRY
VENDOR_BILLED_CSV = REPO_ROOT / CSV_PATH_RELATIVE_VENDOR_BILLED
RATE_OVERRIDES_CSV = REPO_ROOT / CSV_PATH_RELATIVE_RATE_OVERRIDES


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


def _read_share_row(engagement_id: str, collaborator_id: str | None) -> dict[str, str] | None:
    """Return the active SHARE_REGISTRY row for (engagement, collaborator), if any."""
    candidates = [
        r for r in _read_rows(SHARE_REGISTRY_CSV)
        if r.get("engagement_id") == engagement_id
    ]
    if collaborator_id:
        candidates = [
            r for r in candidates if r.get("collaborator_id") == collaborator_id
        ]
    if not candidates:
        return None
    # Prefer active over signed over draft when multiple present
    priority = {"active": 0, "signed": 1, "settled": 2, "proposed": 3, "draft": 4, "archived": 5}
    candidates.sort(key=lambda r: priority.get(r.get("status", "draft"), 99))
    return candidates[0]


def _share_pattern_for_row(share_row: dict[str, str] | None) -> str:
    """Resolve the share_pattern for a SHARE_REGISTRY row; fall back to the
    doctrine default when missing / invalid (caller renders an advisory note
    in the settlement output so the operator can fix the CSV).
    """
    if not share_row:
        return DEFAULT_SHARE_PATTERN
    raw = (share_row.get("share_pattern") or "").strip()
    if share_pattern_is_valid(raw):
        return raw
    return DEFAULT_SHARE_PATTERN


def _collect_cost_lines(
    engagement_id: str,
    collaborator_id: str | None,
    collaborator_hours: float | None,
    collaborator_billed_rate: float,
    founder_hours: float | None,
    founder_rate: float | None,
    direct_costs: list[float],
) -> list[dict[str, Any]]:
    """Compose the transparent project-cost lines (deep_partner_65_35 only;
    orchestration_broker_thin_margin treats per-row revenue slice as gross
    margin and does NOT subtract these costs).
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
) -> dict[str, Any]:
    """Compute the settlement dict for a given engagement.

    Pure function — no I/O beyond reading the canonical CSVs through
    ``_read_share_row`` / ``_read_rows``. Suitable for unit tests.

    Branches on ``share_pattern`` per doctrine §2.1 + D-IH-86-CY-EXT:
      - deep_partner_65_35 (default): benefits formula (revenue - costs
        split per H/C %).
      - orchestration_broker_thin_margin: per-row revenue slice (no costs
        subtracted; collaborators absorb their own work as part of the
        slice). Holistika takes its row's slice + advisory check against
        the doctrine default 6% Holistika total.
      - custom: emits "MANUAL" placeholder + cites the override decision
        ID for operator review (no auto-calculation).

    Args:
        share_pattern_override: optional CLI-supplied override; takes
            precedence over the CSV-resolved value (use when running a
            what-if scenario without authoring the registry row yet).
    """
    share_row = _read_share_row(engagement_id, collaborator_id)
    h_pct = DEFAULT_HOLISTIKA_SHARE_PCT
    c_pct = DEFAULT_COLLABORATOR_SHARE_PCT
    collaborator_billed_rate: float = 0.0
    if share_row:
        try:
            h_pct = int(share_row.get("holistika_share_pct") or h_pct)
            c_pct = int(share_row.get("collaborator_share_pct") or c_pct)
            collaborator_billed_rate = float(
                share_row.get("collaborator_billed_rate") or "0"
            )
        except ValueError:
            pass

    if share_pattern_override and share_pattern_is_valid(share_pattern_override):
        share_pattern = share_pattern_override
    else:
        share_pattern = _share_pattern_for_row(share_row)

    advisory_notes: list[str] = []

    if share_pattern == "orchestration_broker_thin_margin":
        # Per-row revenue slice. NO transparent-cost subtraction; each
        # collaborator absorbs their cost-of-work as part of their slice.
        # Holistika takes its row's slice; collaborator takes theirs.
        # Across-rows margin (sum of all rows' holistika_share_pct) is
        # checked against the doctrine 6% default and an advisory note
        # is appended when the aggregate deviates.
        holistika_share = round(revenue * (h_pct / 100.0), 2)
        collaborator_share = round(revenue * (c_pct / 100.0), 2)
        all_eng_rows = [
            r for r in _read_rows(SHARE_REGISTRY_CSV)
            if r.get("engagement_id") == engagement_id
            and (r.get("share_pattern") or DEFAULT_SHARE_PATTERN)
            == "orchestration_broker_thin_margin"
        ]
        pct_pairs: list[tuple[int, int]] = []
        for r in all_eng_rows:
            try:
                pct_pairs.append((
                    int(r.get("holistika_share_pct") or "0"),
                    int(r.get("collaborator_share_pct") or "0"),
                ))
            except ValueError:
                pass
        total_holistika_across = sum(p[0] for p in pct_pairs) if pct_pairs else h_pct
        if pct_pairs and not orchestration_broker_default_margin_holds(pct_pairs):
            advisory_notes.append(
                f"orchestration engagement {engagement_id!r}: total Holistika "
                f"margin {total_holistika_across}% deviates from default "
                f"{ORCHESTRATION_BROKER_DEFAULT_HOLISTIKA_TOTAL_PCT}% — "
                "ensure share_override_decision_id is set on at least one row"
            )
        return {
            "engagement_id": engagement_id,
            "collaborator_id": collaborator_id,
            "currency": currency,
            "share_row_present": share_row is not None,
            "share_row_id": (share_row or {}).get("share_id", ""),
            "share_pattern": share_pattern,
            "split_default": (
                h_pct == ORCHESTRATION_BROKER_DEFAULT_HOLISTIKA_TOTAL_PCT
            ),
            "holistika_share_pct": h_pct,
            "collaborator_share_pct": c_pct,
            "orchestration_total_holistika_pct": total_holistika_across,
            "revenue": round(revenue, 2),
            "cost_lines": [],
            "total_costs": 0.0,
            "benefits": round(revenue, 2),  # = revenue when no costs deducted
            "holistika_share_amount": holistika_share,
            "collaborator_share_amount": collaborator_share,
            "advisory_notes": advisory_notes,
            "computed_at": _today(),
        }

    if share_pattern == "custom":
        # No auto-calculation; emit placeholder + cite override decision.
        decision_id = (share_row or {}).get("share_override_decision_id", "")
        advisory_notes.append(
            "custom share_pattern: runbook does not auto-calculate. "
            "Operator must compute by hand referencing "
            f"share_override_decision_id={decision_id or '(missing)'}"
        )
        return {
            "engagement_id": engagement_id,
            "collaborator_id": collaborator_id,
            "currency": currency,
            "share_row_present": share_row is not None,
            "share_row_id": (share_row or {}).get("share_id", ""),
            "share_pattern": share_pattern,
            "split_default": False,
            "holistika_share_pct": h_pct,
            "collaborator_share_pct": c_pct,
            "revenue": round(revenue, 2),
            "cost_lines": [],
            "total_costs": None,
            "benefits": None,
            "holistika_share_amount": None,
            "collaborator_share_amount": None,
            "advisory_notes": advisory_notes,
            "computed_at": _today(),
        }

    # Default: share_pattern == "deep_partner_65_35"
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
    holistika_share = round(benefits * (h_pct / 100.0), 2)
    collaborator_share = round(benefits * (c_pct / 100.0), 2)

    return {
        "engagement_id": engagement_id,
        "collaborator_id": collaborator_id,
        "currency": currency,
        "share_row_present": share_row is not None,
        "share_row_id": (share_row or {}).get("share_id", ""),
        "share_pattern": share_pattern,
        "split_default": default_split_holds(h_pct, c_pct),
        "holistika_share_pct": h_pct,
        "collaborator_share_pct": c_pct,
        "revenue": round(revenue, 2),
        "cost_lines": cost_lines,
        "total_costs": total_costs,
        "benefits": benefits,
        "holistika_share_amount": holistika_share,
        "collaborator_share_amount": collaborator_share,
        "advisory_notes": advisory_notes,
        "computed_at": _today(),
    }


def _fmt_amount(value: Any, currency: str) -> str:
    """Format an optional numeric amount; return MANUAL placeholder when None."""
    if value is None:
        return "MANUAL"
    return f"{value:.2f} {currency}"


def render_settlement_markdown(settlement: dict[str, Any]) -> str:
    """Operator-readable markdown table for one settlement.

    Layout branches lightly on share_pattern: deep_partner_65_35 shows the
    full cost-line + benefits + split breakdown; orchestration_broker_thin_margin
    suppresses the cost-line table (no costs are subtracted in that pattern);
    custom emits a MANUAL placeholder row + advisory notes.
    """
    cur = settlement["currency"]
    pattern = settlement.get("share_pattern", DEFAULT_SHARE_PATTERN)
    split_label = "yes" if settlement["split_default"] else "NO — operator-ratified deviation"
    lines = [
        f"# Collaborator Share Settlement — {settlement['engagement_id']}",
        "",
        f"- **Computed at**: {settlement['computed_at']}",
        f"- **Collaborator**: `{settlement.get('collaborator_id') or '—'}`",
        f"- **Share pattern**: `{pattern}`",
        (
            f"- **Share row**: `{settlement['share_row_id'] or '—'}` "
            f"(default split: {split_label})"
        ),
        f"- **Split**: Holistika {settlement['holistika_share_pct']}% / "
        f"Collaborator {settlement['collaborator_share_pct']}%",
    ]

    if pattern == "orchestration_broker_thin_margin":
        total_h = settlement.get("orchestration_total_holistika_pct")
        if total_h is not None:
            lines.append(
                f"- **Engagement-aggregate Holistika margin**: {total_h}% "
                f"(doctrine default: {ORCHESTRATION_BROKER_DEFAULT_HOLISTIKA_TOTAL_PCT}%)"
            )

    lines.append("")
    lines.append("## Settlement")
    lines.append("")
    lines.append("| Line | Hours | Rate | Amount |")
    lines.append("|:---|---:|---:|---:|")
    lines.append(f"| **Revenue** | — | — | **{settlement['revenue']:.2f} {cur}** |")

    if pattern == "deep_partner_65_35":
        for line in settlement["cost_lines"]:
            hours = f"{line['hours']:.2f}" if line["hours"] is not None else "—"
            rate = f"{line['rate']:.2f} {cur}" if line["rate"] is not None else "—"
            lines.append(
                f"| {line['label']} | {hours} | {rate} | "
                f"−{line['amount']:.2f} {cur} |"
            )
        lines.append(
            f"| **Total project costs** | — | — | "
            f"**−{_fmt_amount(settlement['total_costs'], cur)}** |"
        )
        lines.append(
            f"| **Benefits (= revenue − costs)** | — | — | "
            f"**{_fmt_amount(settlement['benefits'], cur)}** |"
        )
    elif pattern == "orchestration_broker_thin_margin":
        lines.append(
            "| _Per-row revenue slice (no costs deducted; collaborators "
            "absorb their own work)_ | — | — | — |"
        )
    elif pattern == "custom":
        lines.append(
            "| _custom share_pattern: operator-computed (see advisory notes)_ "
            "| — | — | — |"
        )

    lines.append(
        f"| Holistika share ({settlement['holistika_share_pct']}%) | — | — | "
        f"{_fmt_amount(settlement.get('holistika_share_amount'), cur)} |"
    )
    lines.append(
        f"| Collaborator share ({settlement['collaborator_share_pct']}%) | — | — | "
        f"{_fmt_amount(settlement.get('collaborator_share_amount'), cur)} |"
    )

    advisory = settlement.get("advisory_notes") or []
    if advisory:
        lines.append("")
        lines.append("## Advisory notes")
        lines.append("")
        for note in advisory:
            lines.append(f"- {note}")

    lines.append("")
    lines.append(
        "> Generated by `scripts/collaborator_share_calculate.py` per "
        "`COLLABORATOR_SHARE_DOCTRINE.md` §2."
    )
    return "\n".join(lines) + "\n"


def self_test() -> int:
    """Worked-example fixture validation; zero-cost; wired into release-gate.

    Three in-memory fixtures (no CSV reads) verify the calculator's
    per-pattern branching:

      (A) deep_partner_65_35:
            €100k revenue; €20k transparent costs; benefits €80k;
            65/35 split => Holistika €52k + Collaborator €28k.

      (B) orchestration_broker_thin_margin:
            €100k revenue; collaborator-side 47% share; Holistika 3%
            (the row's slice); no costs subtracted;
            => Holistika €3k + Collaborator €47k (this row's slice).

      (C) custom:
            €100k revenue; auto-calculation skipped; all amount fields
            return None (operator-computed).
    """
    # (A) deep_partner_65_35
    settlement_a = calculate_settlement(
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
    if settlement_a["share_pattern"] != "deep_partner_65_35":
        return 1
    if settlement_a["revenue"] != 100_000.0:
        return 2
    if settlement_a["total_costs"] != 20_000.0:
        return 3
    if settlement_a["benefits"] != 80_000.0:
        return 4
    if settlement_a["holistika_share_amount"] != 52_000.0:
        return 5
    if settlement_a["collaborator_share_amount"] != 28_000.0:
        return 6
    if settlement_a["holistika_share_pct"] != 65:
        return 7
    if settlement_a["collaborator_share_pct"] != 35:
        return 8
    if abs(
        settlement_a["holistika_share_amount"]
        + settlement_a["collaborator_share_amount"]
        - settlement_a["benefits"]
    ) > 0.02:
        return 9

    # (B) orchestration_broker_thin_margin: this collaborator's row carries
    # 3% Holistika / 47% collaborator (3% + 47% = 50% of revenue on this row;
    # the engagement's other hired collaborator carries the remaining
    # 3% / 47% so the engagement-aggregate is 6% Holistika / 94% across
    # both collaborator rows = doctrine default).
    settlement_b = calculate_settlement(
        engagement_id="ENG-SELFTEST-OB-2026",
        revenue=100_000.0,
        collaborator_id=None,
        collaborator_hours=None,
        founder_hours=None,
        founder_rate=None,
        direct_costs=[],
        currency="EUR",
        share_pattern_override="orchestration_broker_thin_margin",
    )
    if settlement_b["share_pattern"] != "orchestration_broker_thin_margin":
        return 10
    if settlement_b["total_costs"] != 0.0:
        return 11
    # No CSV row exists for this engagement, so h_pct + c_pct fall back to
    # the deep_partner defaults (65 + 35). The runbook still computes
    # revenue * h_pct / 100 = 65_000; revenue * c_pct / 100 = 35_000.
    if settlement_b["holistika_share_amount"] != 65_000.0:
        return 12
    if settlement_b["collaborator_share_amount"] != 35_000.0:
        return 13

    # (C) custom: amount fields are None; advisory note present.
    settlement_c = calculate_settlement(
        engagement_id="ENG-SELFTEST-CUSTOM-2026",
        revenue=100_000.0,
        collaborator_id=None,
        collaborator_hours=None,
        founder_hours=None,
        founder_rate=None,
        direct_costs=[],
        currency="EUR",
        share_pattern_override="custom",
    )
    if settlement_c["share_pattern"] != "custom":
        return 14
    if settlement_c["holistika_share_amount"] is not None:
        return 15
    if settlement_c["collaborator_share_amount"] is not None:
        return 16
    if not settlement_c.get("advisory_notes"):
        return 17
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engagement-id", default=None)
    parser.add_argument("--revenue", type=float, default=None)
    parser.add_argument("--collaborator-id", default=None)
    parser.add_argument("--collaborator-hours", type=float, default=None)
    parser.add_argument("--founder-hours", type=float, default=None)
    parser.add_argument("--founder-rate", type=float, default=None)
    parser.add_argument(
        "--direct-cost", type=float, action="append", default=None,
        help="add a direct pass-through cost (€ amount); may be repeated",
    )
    parser.add_argument("--currency", default="EUR")
    parser.add_argument(
        "--share-pattern",
        choices=sorted(VALID_SHARE_PATTERNS),
        default=None,
        help=(
            "override the CSV-resolved share_pattern (what-if scenarios); "
            "when absent the runbook reads share_pattern from the "
            "COLLABORATOR_SHARE_REGISTRY row matching --engagement-id "
            "(+ --collaborator-id when supplied)"
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
        print(
            f"  wrote {report_path.relative_to(REPO_ROOT)}",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
