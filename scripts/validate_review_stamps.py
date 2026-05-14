#!/usr/bin/env python3
"""I71 P4 + P4 follow-up — Review-stamp freshness validator (Strand C2).

Walks every canonical CSV that carries review-stamp columns + the Artifact subject class
(``CANONICAL_REGISTRY.csv``) and emits three rule classes per the I71 P4 design + P4
follow-up design ratification docs:

P4 baseline (commit ``bb04f08``): 4 mirrored canonicals (process_list / decision_register /
initiative_registry / ops_register).

P4 follow-up (D-IH-71-R; this commit): 17 additional mirrored canonicals get the same
4-column review-stamp shape; CANONICAL_REGISTRY.csv (Artifact subject class) gets an
additional scan path that treats its existing ``last_review`` column as the stamp date.
Total surfaces validated: 21 (4 P4 mirrors + 17 follow-up mirrors) + 1 Artifact scan.

- ``stale-row`` (severity ``warning``): ``last_review_at`` populated AND days-since-review
  exceeds the freshness window (default 180 days; 6 months).
- ``missing-stamp`` (severity ``info``): ``last_review_at`` empty AND the row's authored-date
  proxy (per CSV: ``decided_at`` for decisions; ``inception_date`` for initiatives;
  ``opened_at`` for ops; no proxy for process_list — flagged unconditionally for non-empty
  rows when stamp missing) was authored more than 30 days ago.
- ``invalid-decision-ref`` (severity ``error``): ``last_review_decision_id`` set AND the ID
  does not exist in ``DECISION_REGISTER.csv`` ``decision_id`` column.

Stale + missing rows surface to the sidecar inbox at
``docs/wip/planning/REVIEW_STAMP_INBOX.md`` (NEW companion to ``OPERATOR_INBOX.md``;
auto-rendered by this script). Idempotent: each run replaces the dated section block
between ``<!-- BEGIN REVIEW-STAMP-AUTO -->`` and ``<!-- END REVIEW-STAMP-AUTO -->``.

Wired into ``scripts/release-gate.py`` as an INFO row (advisory only; never blocks).

Usage (repo root):

    py scripts/validate_review_stamps.py
    py scripts/validate_review_stamps.py --json-log
    py scripts/validate_review_stamps.py --threshold-days 90
    py scripts/validate_review_stamps.py --strict   # exit 1 on any warning OR error
                                                     # (default: exit 1 only on error)
    py scripts/validate_review_stamps.py --inbox-path /tmp/inbox.md
    py scripts/validate_review_stamps.py --no-inbox  # skip inbox surfacing

Authority:

- ``D-IH-71-E`` (P0; review-stamp dimension proposal).
- ``D-IH-71-Q`` (P4; column-extension verdict + this validator live).
- ``OPS-71-3`` closes with ``closure_decision_id: D-IH-71-Q``.

Cross-references:

- Design doc: ``docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p4-design-2026-05-14.md``.
- SQL proposal: ``docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/sql-proposal-p4-review-stamp-2026-05-14.md``.
- Migration: ``supabase/migrations/20260514193709_i71_p4_review_stamp.sql``.
- Sidecar inbox: ``docs/wip/planning/REVIEW_STAMP_INBOX.md`` (auto-rendered by this
  script; sibling to ``docs/wip/planning/OPERATOR_INBOX.md`` which is auto-rendered
  from ``OPS_REGISTER.csv`` by ``scripts/render_operator_inbox.py``).

Exit codes:

- ``0`` — no errors (warnings + info advisories may still be present; surfaced via
  the dated inbox section + console output).
- ``1`` — at least one ``invalid-decision-ref`` error AND not ``--strict``;
  OR any warning/error/info advisory AND ``--strict``.
- ``2`` — internal error (missing canonical CSV / unreadable file).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_adviser_disciplines_csv import ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES  # noqa: E402
from akos.hlk_adviser_questions_csv import ADVISER_OPEN_QUESTIONS_FIELDNAMES  # noqa: E402
from akos.hlk_baseline_org_csv import BASELINE_ORGANISATION_FIELDNAMES  # noqa: E402
from akos.hlk_channel_touchpoint_registry_csv import CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_decision_register_csv import DECISION_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_finops_counterparty_csv import FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_founder_filed_instruments_csv import FOUNDER_FILED_INSTRUMENTS_FIELDNAMES  # noqa: E402
from akos.hlk_goipoi_csv import GOIPOI_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_initiative_registry_csv import INITIATIVE_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_ops_register_csv import OPS_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_persona_registry_csv import PERSONA_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_persona_scenario_csv import PERSONA_SCENARIO_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_policy_register_csv import POLICY_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_process_csv import PROCESS_LIST_FIELDNAMES  # noqa: E402
from akos.hlk_program_registry_csv import PROGRAM_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_repo_health_csv import REPO_HEALTH_SNAPSHOT_FIELDNAMES  # noqa: E402
from akos.hlk_repository_registry_csv import REPOSITORY_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_skill_registry_csv import SKILL_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_sourcing_register_csv import SOURCING_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_topic_registry_csv import TOPIC_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_touchpoint_kit_cell_csv import TOUCHPOINT_KIT_CELL_FIELDNAMES  # noqa: E402

CANONICALS_DIR = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Compliance"
    / "canonicals"
)
DIMENSIONS_DIR = CANONICALS_DIR / "dimensions"

# P4 baseline (4 mirrors)
DECISION_REGISTER_CSV = CANONICALS_DIR / "DECISION_REGISTER.csv"
INITIATIVE_REGISTRY_CSV = CANONICALS_DIR / "INITIATIVE_REGISTRY.csv"
OPS_REGISTER_CSV = CANONICALS_DIR / "OPS_REGISTER.csv"
PROCESS_LIST_CSV = CANONICALS_DIR / "process_list.csv"

# P4 follow-up additions (17 mirrors + Artifact via CANONICAL_REGISTRY)
BASELINE_ORGANISATION_CSV = CANONICALS_DIR / "baseline_organisation.csv"
FINOPS_COUNTERPARTY_REGISTER_CSV = CANONICALS_DIR / "FINOPS_COUNTERPARTY_REGISTER.csv"
GOIPOI_REGISTER_CSV = DIMENSIONS_DIR / "GOI_POI_REGISTER.csv"
ADVISER_ENGAGEMENT_DISCIPLINES_CSV = CANONICALS_DIR / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"
ADVISER_OPEN_QUESTIONS_CSV = CANONICALS_DIR / "ADVISER_OPEN_QUESTIONS.csv"
FOUNDER_FILED_INSTRUMENTS_CSV = CANONICALS_DIR / "FOUNDER_FILED_INSTRUMENTS.csv"
PROGRAM_REGISTRY_CSV = DIMENSIONS_DIR / "PROGRAM_REGISTRY.csv"
TOPIC_REGISTRY_CSV = DIMENSIONS_DIR / "TOPIC_REGISTRY.csv"
PERSONA_REGISTRY_CSV = DIMENSIONS_DIR / "PERSONA_REGISTRY.csv"
PERSONA_SCENARIO_REGISTRY_CSV = DIMENSIONS_DIR / "PERSONA_SCENARIO_REGISTRY.csv"
CHANNEL_TOUCHPOINT_REGISTRY_CSV = DIMENSIONS_DIR / "CHANNEL_TOUCHPOINT_REGISTRY.csv"
SOURCING_REGISTER_CSV = DIMENSIONS_DIR / "SOURCING_REGISTER.csv"
SKILL_REGISTRY_CSV = DIMENSIONS_DIR / "SKILL_REGISTRY.csv"
TOUCHPOINT_KIT_CELL_REGISTRY_CSV = DIMENSIONS_DIR / "TOUCHPOINT_KIT_CELL_REGISTRY.csv"
POLICY_REGISTER_CSV = DIMENSIONS_DIR / "POLICY_REGISTER.csv"
REPO_HEALTH_SNAPSHOT_CSV = CANONICALS_DIR / "REPO_HEALTH_SNAPSHOT.csv"
REPOSITORY_REGISTRY_CSV = CANONICALS_DIR / "REPOSITORY_REGISTRY.csv"

# Artifact subject class — CANONICAL_REGISTRY.csv (unmirrored; standalone-table path)
CANONICAL_REGISTRY_CSV = CANONICALS_DIR / "CANONICAL_REGISTRY.csv"

DEFAULT_INBOX_PATH = REPO_ROOT / "docs" / "wip" / "planning" / "REVIEW_STAMP_INBOX.md"

DEFAULT_THRESHOLD_DAYS = 180   # 6-month freshness window per D-IH-71-E + D-IH-71-Q
MISSING_STAMP_GRACE_DAYS = 30  # rows authored within last 30 days don't emit missing-stamp

REVIEW_STAMP_COLUMNS: tuple[str, ...] = (
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
)


@dataclass(frozen=True)
class CanonicalSpec:
    """Per-CSV registration: path, primary key column, authored-date proxy column (if any)."""

    csv_path: Path
    fieldnames: tuple[str, ...]
    pk_column: str
    authored_date_column: str | None
    label: str


_REGISTRY: tuple[CanonicalSpec, ...] = (
    # ------------------------- P4 baseline (4 mirrors) -------------------------
    CanonicalSpec(
        csv_path=PROCESS_LIST_CSV,
        fieldnames=tuple(PROCESS_LIST_FIELDNAMES),
        pk_column="item_id",
        authored_date_column=None,  # process_list rows have no canonical authored-date column
        label="process_list",
    ),
    CanonicalSpec(
        csv_path=DECISION_REGISTER_CSV,
        fieldnames=tuple(DECISION_REGISTER_FIELDNAMES),
        pk_column="decision_id",
        authored_date_column="decided_at",
        label="decision_register",
    ),
    CanonicalSpec(
        csv_path=INITIATIVE_REGISTRY_CSV,
        fieldnames=tuple(INITIATIVE_REGISTRY_FIELDNAMES),
        pk_column="initiative_id",
        authored_date_column="inception_date",
        label="initiative_registry",
    ),
    CanonicalSpec(
        csv_path=OPS_REGISTER_CSV,
        fieldnames=tuple(OPS_REGISTER_FIELDNAMES),
        pk_column="ops_action_id",
        authored_date_column="opened_at",
        label="ops_register",
    ),
    # ------------------ P4 follow-up (D-IH-71-R; 17 mirrors) -------------------
    CanonicalSpec(
        csv_path=BASELINE_ORGANISATION_CSV,
        fieldnames=tuple(BASELINE_ORGANISATION_FIELDNAMES),
        pk_column="org_uuid",
        authored_date_column=None,
        label="baseline_organisation",
    ),
    CanonicalSpec(
        csv_path=FINOPS_COUNTERPARTY_REGISTER_CSV,
        fieldnames=tuple(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES),
        pk_column="counterparty_id",
        authored_date_column=None,
        label="finops_counterparty_register",
    ),
    CanonicalSpec(
        csv_path=GOIPOI_REGISTER_CSV,
        fieldnames=tuple(GOIPOI_REGISTER_FIELDNAMES),
        pk_column="ref_id",
        authored_date_column="distance_assessed_date",
        label="goipoi_register",
    ),
    CanonicalSpec(
        csv_path=ADVISER_ENGAGEMENT_DISCIPLINES_CSV,
        fieldnames=tuple(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES),
        pk_column="discipline_id",
        authored_date_column=None,
        label="adviser_engagement_disciplines",
    ),
    CanonicalSpec(
        csv_path=ADVISER_OPEN_QUESTIONS_CSV,
        fieldnames=tuple(ADVISER_OPEN_QUESTIONS_FIELDNAMES),
        pk_column="question_id",
        authored_date_column="target_date",
        label="adviser_open_questions",
    ),
    CanonicalSpec(
        csv_path=FOUNDER_FILED_INSTRUMENTS_CSV,
        fieldnames=tuple(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES),
        pk_column="instrument_id",
        authored_date_column="effective_or_filing_date",
        label="founder_filed_instruments",
    ),
    CanonicalSpec(
        csv_path=PROGRAM_REGISTRY_CSV,
        fieldnames=tuple(PROGRAM_REGISTRY_FIELDNAMES),
        pk_column="program_id",
        authored_date_column="start_date",
        label="program_registry",
    ),
    CanonicalSpec(
        csv_path=TOPIC_REGISTRY_CSV,
        fieldnames=tuple(TOPIC_REGISTRY_FIELDNAMES),
        pk_column="topic_id",
        authored_date_column=None,
        label="topic_registry",
    ),
    CanonicalSpec(
        csv_path=PERSONA_REGISTRY_CSV,
        fieldnames=tuple(PERSONA_REGISTRY_FIELDNAMES),
        pk_column="persona_id",
        authored_date_column=None,
        label="persona_registry",
    ),
    CanonicalSpec(
        csv_path=PERSONA_SCENARIO_REGISTRY_CSV,
        fieldnames=tuple(PERSONA_SCENARIO_REGISTRY_FIELDNAMES),
        pk_column="scenario_id",
        authored_date_column=None,
        label="persona_scenario_registry",
    ),
    CanonicalSpec(
        csv_path=CHANNEL_TOUCHPOINT_REGISTRY_CSV,
        fieldnames=tuple(CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES),
        pk_column="channel_id",
        authored_date_column=None,
        label="channel_touchpoint_registry",
    ),
    CanonicalSpec(
        csv_path=SOURCING_REGISTER_CSV,
        fieldnames=tuple(SOURCING_REGISTER_FIELDNAMES),
        pk_column="vendor_id",
        authored_date_column="last_engagement_date",
        label="sourcing_register",
    ),
    CanonicalSpec(
        csv_path=SKILL_REGISTRY_CSV,
        fieldnames=tuple(SKILL_REGISTRY_FIELDNAMES),
        pk_column="skill_id",
        authored_date_column=None,
        label="skill_registry",
    ),
    CanonicalSpec(
        csv_path=TOUCHPOINT_KIT_CELL_REGISTRY_CSV,
        fieldnames=tuple(TOUCHPOINT_KIT_CELL_FIELDNAMES),
        pk_column="cell_id",
        authored_date_column="last_review",
        label="touchpoint_kit_cell",
    ),
    CanonicalSpec(
        csv_path=POLICY_REGISTER_CSV,
        fieldnames=tuple(POLICY_REGISTER_FIELDNAMES),
        pk_column="policy_id",
        authored_date_column="last_review",
        label="policy_register",
    ),
    CanonicalSpec(
        csv_path=REPO_HEALTH_SNAPSHOT_CSV,
        fieldnames=tuple(REPO_HEALTH_SNAPSHOT_FIELDNAMES),
        pk_column="snapshot_date",
        authored_date_column="snapshot_date",
        label="repo_health_snapshot",
    ),
    CanonicalSpec(
        csv_path=REPOSITORY_REGISTRY_CSV,
        fieldnames=tuple(REPOSITORY_REGISTRY_FIELDNAMES),
        pk_column="repo_slug",
        authored_date_column=None,
        label="repository_registry",
    ),
)


# Artifact subject class — separate scan path. CANONICAL_REGISTRY.csv has a different
# column shape (no review-stamp columns; uses its existing `last_review` column as the
# stamp date). The scan emits advisories under canonical label "canonical_registry_artifact"
# and pk = canonical_id.
ARTIFACT_REGISTRY_LABEL = "canonical_registry_artifact"
ARTIFACT_REGISTRY_PK_COLUMN = "canonical_id"
ARTIFACT_REGISTRY_PATH_COLUMN = "file_path"
ARTIFACT_REGISTRY_STAMP_COLUMN = "last_review"
ARTIFACT_REGISTRY_STATUS_COLUMN = "status"


@dataclass
class Advisory:
    """One advisory hit for one row."""

    severity: str          # "info" | "warning" | "error"
    rule: str              # "stale-row" | "missing-stamp" | "invalid-decision-ref"
    canonical: str         # e.g. "decision_register"
    pk: str                # row primary key value
    detail: str            # human-readable detail
    age_days: int | None = None    # for stale-row + missing-stamp
    decision_ref: str | None = None  # for invalid-decision-ref


@dataclass
class CanonicalReport:
    label: str
    csv_path: str
    rows_total: int = 0
    rows_with_stamp: int = 0
    rows_missing_stamp: int = 0
    rows_stale: int = 0
    rows_invalid_decision_ref: int = 0
    advisories: list[Advisory] = field(default_factory=list)


def _parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _load_decision_ids() -> set[str]:
    """Read DECISION_REGISTER.csv decision_id column for invalid-decision-ref check."""
    if not DECISION_REGISTER_CSV.exists():
        return set()
    with DECISION_REGISTER_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return {(r.get("decision_id") or "").strip() for r in reader if (r.get("decision_id") or "").strip()}


def _safe_relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _check_one_csv(
    spec: CanonicalSpec,
    *,
    today: date,
    threshold_days: int,
    decision_ids: set[str],
) -> CanonicalReport:
    report = CanonicalReport(label=spec.label, csv_path=_safe_relative_path(spec.csv_path))
    if not spec.csv_path.exists():
        return report
    with spec.csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            report.rows_total += 1
            pk = (r.get(spec.pk_column) or "").strip() or "(unkeyed)"
            stamp_value = (r.get("last_review_at") or "").strip()
            stamp_date = _parse_iso_date(stamp_value) if stamp_value else None
            decision_ref = (r.get("last_review_decision_id") or "").strip()

            # Rule 3 — invalid-decision-ref (highest severity; check first)
            if decision_ref and decision_ref not in decision_ids:
                report.rows_invalid_decision_ref += 1
                report.advisories.append(
                    Advisory(
                        severity="error",
                        rule="invalid-decision-ref",
                        canonical=spec.label,
                        pk=pk,
                        detail=f"last_review_decision_id={decision_ref!r} not present in DECISION_REGISTER.csv decision_id column",
                        decision_ref=decision_ref,
                    )
                )

            # Rule 1 — stale-row (when stamp present but old)
            if stamp_date is not None:
                report.rows_with_stamp += 1
                age = (today - stamp_date).days
                if age > threshold_days:
                    report.rows_stale += 1
                    report.advisories.append(
                        Advisory(
                            severity="warning",
                            rule="stale-row",
                            canonical=spec.label,
                            pk=pk,
                            detail=f"last_review_at={stamp_value} is {age} days old (threshold={threshold_days}d)",
                            age_days=age,
                        )
                    )
                continue  # if stamped, skip missing-stamp check

            # Rule 2 — missing-stamp (only when authored date proxy is old enough)
            authored_date: date | None = None
            if spec.authored_date_column:
                authored_date = _parse_iso_date(r.get(spec.authored_date_column))
            grace_window_passed = True
            authored_age: int | None = None
            if authored_date is not None:
                authored_age = (today - authored_date).days
                grace_window_passed = authored_age > MISSING_STAMP_GRACE_DAYS
            # process_list has no authored-date proxy; we still flag (treat as authored long ago).
            if grace_window_passed:
                report.rows_missing_stamp += 1
                detail_parts = ["last_review_at empty"]
                if authored_age is not None:
                    detail_parts.append(f"authored {authored_age} days ago")
                detail_parts.append("operator backfill recommended")
                report.advisories.append(
                    Advisory(
                        severity="info",
                        rule="missing-stamp",
                        canonical=spec.label,
                        pk=pk,
                        detail="; ".join(detail_parts),
                        age_days=authored_age,
                    )
                )
    return report


def _scan_canonical_md_artifacts(
    *,
    today: date,
    threshold_days: int,
    decision_ids: set[str],
) -> CanonicalReport:
    """I71 P4 follow-up — Artifact subject class scan over CANONICAL_REGISTRY.csv.

    Walks every row in CANONICAL_REGISTRY.csv and treats its existing ``last_review``
    column as the review-stamp date. Emits the same three rule classes as the column-
    extension scan (stale-row / missing-stamp / invalid-decision-ref).

    Per the P4 follow-up design §4.2: this scan reads CSV (not Supabase) for the same
    reason the P4 validator reads CSVs — keeps the validator hot path Supabase-free
    and avoids a service_role round-trip per run. The standalone-table backfill at
    migration time is a forward-provisioning move; richer stamps via the standalone
    table land in a future commit when the operator drives them.

    Rows with empty ``file_path`` (status='proposed' future-reserved canonicals) are
    skipped — there's no stamp surface to rate.
    """
    report = CanonicalReport(
        label=ARTIFACT_REGISTRY_LABEL,
        csv_path=_safe_relative_path(CANONICAL_REGISTRY_CSV),
    )
    if not CANONICAL_REGISTRY_CSV.exists():
        return report
    with CANONICAL_REGISTRY_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            file_path = (r.get(ARTIFACT_REGISTRY_PATH_COLUMN) or "").strip()
            if not file_path:
                # status='proposed' / future-reserved row with no path — skip silently
                continue
            report.rows_total += 1
            pk = (r.get(ARTIFACT_REGISTRY_PK_COLUMN) or "").strip() or "(unkeyed)"
            stamp_value = (r.get(ARTIFACT_REGISTRY_STAMP_COLUMN) or "").strip()
            stamp_date = _parse_iso_date(stamp_value) if stamp_value else None
            # CANONICAL_REGISTRY.csv has no last_review_decision_id column today — skip
            # invalid-decision-ref rule for the Artifact scan. (When richer stamps land
            # via compliance.review_stamps_standalone, that scan path picks up the rule.)

            if stamp_date is not None:
                report.rows_with_stamp += 1
                age = (today - stamp_date).days
                if age > threshold_days:
                    report.rows_stale += 1
                    report.advisories.append(
                        Advisory(
                            severity="warning",
                            rule="stale-row",
                            canonical=ARTIFACT_REGISTRY_LABEL,
                            pk=f"{pk} ({file_path})",
                            detail=f"last_review={stamp_value} is {age} days old (threshold={threshold_days}d)",
                            age_days=age,
                        )
                    )
            else:
                # No authored-date proxy; flag every empty-stamp row as missing-stamp info.
                report.rows_missing_stamp += 1
                report.advisories.append(
                    Advisory(
                        severity="info",
                        rule="missing-stamp",
                        canonical=ARTIFACT_REGISTRY_LABEL,
                        pk=f"{pk} ({file_path})",
                        detail="last_review empty; operator backfill recommended",
                    )
                )
    return report


def _surface_to_inbox(reports: Iterable[CanonicalReport], inbox_path: Path, *, today: date) -> int:
    """Idempotent dated-section write between BEGIN/END markers."""
    advisories_by_class: dict[str, list[Advisory]] = {"stale-row": [], "missing-stamp": [], "invalid-decision-ref": []}
    for report in reports:
        for adv in report.advisories:
            advisories_by_class.setdefault(adv.rule, []).append(adv)

    today_iso = today.isoformat()
    begin_marker = "<!-- BEGIN REVIEW-STAMP-AUTO -->"
    end_marker = "<!-- END REVIEW-STAMP-AUTO -->"

    lines: list[str] = []
    lines.append("---")
    lines.append("language: en")
    lines.append("status: continuous")
    lines.append("continuous_rationale: Auto-rendered review-stamp inbox (I71 P4) — re-renders from canonical CSVs on every validate_review_stamps.py run; never hand-edit between markers.")
    lines.append("---")
    lines.append("")
    lines.append("# Review-stamp inbox (I71 P4 — sidecar to OPERATOR_INBOX.md)")
    lines.append("")
    lines.append("> **SSOT** is the four canonical CSVs that carry review-stamp columns")
    lines.append("> (`process_list.csv`, `DECISION_REGISTER.csv`, `INITIATIVE_REGISTRY.csv`, `OPS_REGISTER.csv`).")
    lines.append("> This file is auto-rendered by `scripts/validate_review_stamps.py` on every run.")
    lines.append("> The dated section between the BEGIN/END markers is replaced wholesale; never hand-edit between them.")
    lines.append("> Operator backfills review stamps in the canonical CSVs; subsequent runs drop backfilled rows from this inbox.")
    lines.append("")
    lines.append("## Cadence")
    lines.append("")
    lines.append("- **Stale window**: 180 days (6 months) per `D-IH-71-Q` default.")
    lines.append("- **Missing-stamp grace**: rows authored within 30 days don't surface (operator review can wait until the row settles).")
    lines.append("- **Invalid-decision-ref**: surfaces immediately as an `error` advisory (data integrity).")
    lines.append("")
    lines.append(begin_marker)
    lines.append("")
    lines.append(f"_Last rendered: {today_iso} UTC (validate_review_stamps.py)._ ")
    lines.append("")

    for rule_label, header in (
        ("invalid-decision-ref", "## Invalid decision references (error)"),
        ("stale-row", "## Stale rows (warning; review window exceeded)"),
        ("missing-stamp", "## Missing review stamps (info; backfill recommended)"),
    ):
        lines.append(header)
        lines.append("")
        rule_advisories = advisories_by_class.get(rule_label, [])
        if not rule_advisories:
            lines.append("_No advisories at this severity._")
        else:
            lines.append("| Canonical | Row PK | Detail |")
            lines.append("|:---|:---|:---|")
            for adv in sorted(rule_advisories, key=lambda a: (a.canonical, a.pk)):
                lines.append(f"| `{adv.canonical}` | `{adv.pk}` | {adv.detail} |")
        lines.append("")

    lines.append(end_marker)
    lines.append("")
    lines.append("## Cross-references")
    lines.append("")
    lines.append("- Design doc: [`p4-design-2026-05-14.md`](71-cicd-discipline-and-aiops-baseline-maturity/reports/p4-design-2026-05-14.md).")
    lines.append("- Phase report: [`p4-strand-c2-review-stamp-2026-05-14.md`](71-cicd-discipline-and-aiops-baseline-maturity/reports/p4-strand-c2-review-stamp-2026-05-14.md).")
    lines.append("- SQL proposal (audit trail): [`sql-proposal-p4-review-stamp-2026-05-14.md`](71-cicd-discipline-and-aiops-baseline-maturity/reports/sql-proposal-p4-review-stamp-2026-05-14.md).")
    lines.append("- Sibling inbox (OPS): [`OPERATOR_INBOX.md`](OPERATOR_INBOX.md).")
    lines.append("")

    inbox_path.parent.mkdir(parents=True, exist_ok=True)
    inbox_path.write_text("\n".join(lines), encoding="utf-8")
    total = sum(len(v) for v in advisories_by_class.values())
    return total


def _format_human(reports: list[CanonicalReport]) -> int:
    error_count = 0
    warning_count = 0
    info_count = 0
    print(f"validate_review_stamps: checked {len(reports)} canonical CSVs")
    for report in reports:
        marker = "OK"
        if report.rows_invalid_decision_ref > 0:
            marker = "ERROR"
        elif report.rows_stale > 0:
            marker = "WARN"
        elif report.rows_missing_stamp > 0:
            marker = "INFO"
        print(
            f"  [{marker}] {report.label:<22s} {report.rows_total:>5d} rows | "
            f"stamped={report.rows_with_stamp} stale={report.rows_stale} "
            f"missing={report.rows_missing_stamp} invalid_ref={report.rows_invalid_decision_ref}"
        )
        for adv in report.advisories:
            print(f"        [{adv.severity}] {adv.rule}: {adv.pk} -- {adv.detail}")
            if adv.severity == "error":
                error_count += 1
            elif adv.severity == "warning":
                warning_count += 1
            else:
                info_count += 1
    print(
        f"\nSummary: {error_count} error / {warning_count} warning / {info_count} info advisory hits across "
        f"{sum(r.rows_total for r in reports)} rows (window=180d; grace=30d)"
    )
    return error_count


def _format_json(reports: list[CanonicalReport]) -> int:
    error_count = 0
    payload = []
    for report in reports:
        payload.append(
            {
                "canonical": report.label,
                "csv_path": report.csv_path,
                "rows_total": report.rows_total,
                "rows_with_stamp": report.rows_with_stamp,
                "rows_stale": report.rows_stale,
                "rows_missing_stamp": report.rows_missing_stamp,
                "rows_invalid_decision_ref": report.rows_invalid_decision_ref,
                "advisories": [
                    {
                        "severity": a.severity,
                        "rule": a.rule,
                        "pk": a.pk,
                        "detail": a.detail,
                        "age_days": a.age_days,
                        "decision_ref": a.decision_ref,
                    }
                    for a in report.advisories
                ],
            }
        )
        for adv in report.advisories:
            if adv.severity == "error":
                error_count += 1
    print(json.dumps({"reports": payload, "error_count": error_count}))
    return error_count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--threshold-days",
        type=int,
        default=DEFAULT_THRESHOLD_DAYS,
        help=f"Stale-row threshold in days (default {DEFAULT_THRESHOLD_DAYS}).",
    )
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any warning/error/info hit (default: only error).")
    parser.add_argument("--json-log", action="store_true", help="Emit structured JSON output instead of human-readable.")
    parser.add_argument("--inbox-path", type=Path, default=DEFAULT_INBOX_PATH, help="Path for sidecar review-stamp inbox.")
    parser.add_argument("--no-inbox", action="store_true", help="Skip surfacing advisories to the sidecar inbox.")
    parser.add_argument("--today", type=str, default=None, help="Override today date for testing (YYYY-MM-DD).")
    args = parser.parse_args(argv)

    today = _parse_iso_date(args.today) if args.today else date.today()
    if today is None:
        print(f"FAIL: invalid --today value {args.today!r}; expected YYYY-MM-DD")
        return 2

    decision_ids = _load_decision_ids()
    if not decision_ids:
        print(f"WARN: DECISION_REGISTER.csv missing or empty; invalid-decision-ref check disabled")

    reports: list[CanonicalReport] = []
    for spec in _REGISTRY:
        if not spec.csv_path.exists():
            print(f"FAIL: {spec.label} CSV missing at {spec.csv_path}")
            return 2
        reports.append(
            _check_one_csv(spec, today=today, threshold_days=args.threshold_days, decision_ids=decision_ids)
        )

    # I71 P4 follow-up — Artifact subject class scan over CANONICAL_REGISTRY.csv.
    if CANONICAL_REGISTRY_CSV.exists():
        reports.append(
            _scan_canonical_md_artifacts(
                today=today, threshold_days=args.threshold_days, decision_ids=decision_ids
            )
        )

    if args.json_log:
        error_count = _format_json(reports)
    else:
        error_count = _format_human(reports)

    if not args.no_inbox:
        total_surfaced = _surface_to_inbox(reports, args.inbox_path, today=today)
        if not args.json_log:
            inbox_display = _safe_relative_path(args.inbox_path) if args.inbox_path.is_absolute() else str(args.inbox_path)
            print(f"\nInbox: {total_surfaced} advisory rows written to {inbox_display}")

    has_warning_or_info = any(
        a.severity in ("warning", "info")
        for r in reports
        for a in r.advisories
    )
    if args.strict and (error_count > 0 or has_warning_or_info):
        return 1
    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
