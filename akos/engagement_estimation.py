"""Reusable engagement-estimation discipline for Holistika.

This module is the Python surface of `SOP-ENG_ESTIMATION_DISCIPLINE_001.md`.
It produces a per-engagement commercial schedule that the operator can paste
into a proposal, anchored on three governed CSVs:

* ``baseline_organisation.csv`` — role × hourly rate matrix (min / par / max).
* ``process_list.csv`` — process × effort hours (min / par / max).
* ``COUNTRY_WORK_CALENDAR.csv`` — country × legal hours + public holidays + locale uplift.

The math is **PERT three-point estimation**:

    E = (min + 4 × par + max) / 6

applied independently to effort hours and to monetary cost; the duration in
working days is recomputed from a country-specific calendar so a 100-hour
work package consumes 14 working days in Spain (8 h/day) and 16 in France
(7 h/day) — without changing the cost.

Multipliers (enterprise premium, bridge-entity coordination, locale uplift,
first-of-kind novelty, repeat-counterparty discount) compound onto the
**price**, not the effort. They live in the Pydantic ``Multiplier`` registry
below so the SOP and the code share a single source of truth.

Cross-references:
* ``SOP-ENG_ESTIMATION_DISCIPLINE_001.md`` — canonical SOP body.
* ``scripts/estimate_engagement.py`` — operator CLI.
* ``docs/references/hlk/v3.0/_assets/operations/shared/engagement/estimation/estimation-template.md`` —
  operator worksheet template (the ``scope.yaml`` shape).
"""

from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# ── Three-point estimate ────────────────────────────────────────────────


class TriEstimate(BaseModel):
    """Min / par / max estimate, with a derived PERT expected value."""

    min: float = Field(ge=0)
    par: float = Field(ge=0)
    max: float = Field(ge=0)

    model_config = ConfigDict(frozen=True)

    @model_validator(mode="after")
    def _ordered(self) -> "TriEstimate":
        if not (self.min <= self.par <= self.max):
            raise ValueError(
                f"min ({self.min}) ≤ par ({self.par}) ≤ max ({self.max}) violated"
            )
        return self

    @property
    def expected(self) -> float:
        """PERT expected value: ``(min + 4·par + max) / 6``."""
        return (self.min + 4 * self.par + self.max) / 6.0

    @property
    def sigma(self) -> float:
        """PERT pseudo-stddev: ``(max − min) / 6``."""
        return (self.max - self.min) / 6.0

    def scale(self, factor: float) -> "TriEstimate":
        return TriEstimate(min=self.min * factor, par=self.par * factor, max=self.max * factor)


# ── Method library ───────────────────────────────────────────────────────


MethodId = Literal[
    "discovery_kickoff",
    "discovery_interviews",
    "discovery_synthesis",
    "design_workshop",
    "design_specification",
    "build_prototype_excel",
    "build_webapp",
    "build_integration_study",
    "transfer_training",
    "transfer_documentation",
    "close_review",
    "ongoing_support_month",
]


class EstimationMethod(BaseModel):
    """A reusable unit of work with min/par/max effort hours and a default role mix."""

    method_id: MethodId
    label: str
    effort_hours: TriEstimate
    default_role_mix: dict[str, float]
    description: str

    @field_validator("default_role_mix")
    @classmethod
    def _shares_sum_to_one(cls, value: dict[str, float]) -> dict[str, float]:
        total = sum(value.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"role_mix shares must sum to ~1.0 (got {total:.3f}): {value}")
        return value


# Canonical method library. Effort-hour values are calibrated against the
# Madrid SME consulting market and validated against an off-repo
# operator-supplied competitor inspiration distillation (sources deleted at
# P3 close per redaction protocol; methodology shape retained anonymously).
# Edits to these constants must also land in
# `SOP-ENG_ESTIMATION_DISCIPLINE_001.md` §3 (drift-safeguarded by
# tests/test_estimation_constants_match_sop.py).
METHODS: dict[MethodId, EstimationMethod] = {
    "discovery_kickoff": EstimationMethod(
        method_id="discovery_kickoff",
        label="Discovery — kickoff workshop and framing",
        effort_hours=TriEstimate(min=8, par=12, max=18),
        default_role_mix={"Project Manager": 0.5, "Holistik Researcher": 0.5},
        description="Joint kickoff workshop + initial framing of the engagement scope.",
    ),
    "discovery_interviews": EstimationMethod(
        method_id="discovery_interviews",
        label="Discovery — stakeholder interviews + synthesis grid",
        effort_hours=TriEstimate(min=12, par=20, max=32),
        default_role_mix={"Holistik Researcher": 0.7, "Project Manager": 0.3},
        description="Stakeholder interviews (4–8 informants) + synthesis grid against engagement axes.",
    ),
    "discovery_synthesis": EstimationMethod(
        method_id="discovery_synthesis",
        label="Discovery — baseline assessment write-up",
        effort_hours=TriEstimate(min=8, par=14, max=24),
        default_role_mix={"Holistik Researcher": 0.6, "Project Manager": 0.4},
        description="Baseline-reality write-up + decision-criteria capture + handoff to design.",
    ),
    "design_workshop": EstimationMethod(
        method_id="design_workshop",
        label="Design — joint design workshop (counterparty-side)",
        effort_hours=TriEstimate(min=10, par=16, max=28),
        default_role_mix={"Project Manager": 0.4, "Tech Lead": 0.3, "O5-1": 0.3},
        description="On-site or videoconference design workshop with counterparty operational owners.",
    ),
    "design_specification": EstimationMethod(
        method_id="design_specification",
        label="Design — functional + technical specification",
        effort_hours=TriEstimate(min=24, par=40, max=72),
        default_role_mix={"Tech Lead": 0.5, "Project Manager": 0.3, "Brand & Narrative Manager": 0.2},
        description="Functional specification + technical specification + scope-out + acceptance criteria.",
    ),
    "build_prototype_excel": EstimationMethod(
        method_id="build_prototype_excel",
        label="Build — Phase 1 Excel/Power Query prototype",
        effort_hours=TriEstimate(min=40, par=80, max=140),
        default_role_mix={"Back-End Developer": 0.5, "Tech Lead": 0.3, "Project Manager": 0.2},
        description="Excel + Power Query (or similar lightweight tool) implementing the libellé generator + register skeleton.",
    ),
    "build_webapp": EstimationMethod(
        method_id="build_webapp",
        label="Build — Phase 2 lightweight web application",
        effort_hours=TriEstimate(min=140, par=240, max=400),
        default_role_mix={
            "Back-End Developer": 0.35,
            "Front-End Developer": 0.35,
            "Tech Lead": 0.2,
            "Project Manager": 0.1,
        },
        description="Multi-category web app (Next.js or equivalent) covering the form, register, supplier base, and dispute dashboard.",
    ),
    "build_integration_study": EstimationMethod(
        method_id="build_integration_study",
        label="Build — Phase 3 integration feasibility study",
        effort_hours=TriEstimate(min=40, par=80, max=140),
        default_role_mix={"Tech Lead": 0.5, "AI Engineer": 0.2, "Project Manager": 0.3},
        description="Feasibility study for WeBuy integration (CSV import, internal RPC, RPA) with risk-graded recommendation.",
    ),
    "transfer_training": EstimationMethod(
        method_id="transfer_training",
        label="Transfer — operator training",
        effort_hours=TriEstimate(min=12, par=20, max=32),
        default_role_mix={"Project Manager": 0.6, "Tech Lead": 0.4},
        description="Two training sessions for gestionnaires + an admin session for the DSI / référentiel owner.",
    ),
    "transfer_documentation": EstimationMethod(
        method_id="transfer_documentation",
        label="Transfer — SOP + runbook + handover pack",
        effort_hours=TriEstimate(min=12, par=20, max=32),
        default_role_mix={"Project Manager": 0.5, "Tech Lead": 0.3, "Holistik Researcher": 0.2},
        description="Counterparty-facing SOP + operator runbook + change-note template + retrospective deck.",
    ),
    "close_review": EstimationMethod(
        method_id="close_review",
        label="Close — engagement review + lessons-learned",
        effort_hours=TriEstimate(min=4, par=8, max=14),
        default_role_mix={"Project Manager": 0.5, "O5-1": 0.5},
        description="Engagement closure review + lessons learned + next-action register.",
    ),
    "ongoing_support_month": EstimationMethod(
        method_id="ongoing_support_month",
        label="Ongoing support — per month",
        effort_hours=TriEstimate(min=8, par=16, max=32),
        default_role_mix={"Back-End Developer": 0.5, "Project Manager": 0.5},
        description="Per-month operational support tier (bug fixes, minor adjustments, monitoring).",
    ),
}


# ── Role × hourly rate matrix (loaded from baseline_organisation.csv) ────


class RoleRate(BaseModel):
    """Per-role hourly rate triangle in EUR. Mirrors the canonical CSV columns."""

    role_name: str
    min_eur_per_hour: float | None
    par_eur_per_hour: float | None
    max_eur_per_hour: float | None

    @model_validator(mode="after")
    def _all_or_none(self) -> "RoleRate":
        triple = (self.min_eur_per_hour, self.par_eur_per_hour, self.max_eur_per_hour)
        if any(v is None for v in triple) and any(v is not None for v in triple):
            raise ValueError(
                f"role {self.role_name}: hourly rates must all be set or all be NULL (got {triple})"
            )
        if all(v is not None for v in triple):
            if not (self.min_eur_per_hour <= self.par_eur_per_hour <= self.max_eur_per_hour):
                raise ValueError(f"role {self.role_name}: rates not min ≤ par ≤ max ({triple})")
        return self

    @property
    def is_billable(self) -> bool:
        return self.par_eur_per_hour is not None

    def as_tri(self) -> TriEstimate:
        if not self.is_billable:
            raise ValueError(f"role {self.role_name} is non-billable (no hourly rate)")
        assert self.min_eur_per_hour is not None
        assert self.par_eur_per_hour is not None
        assert self.max_eur_per_hour is not None
        return TriEstimate(
            min=self.min_eur_per_hour,
            par=self.par_eur_per_hour,
            max=self.max_eur_per_hour,
        )


def load_role_rates(csv_path: Path) -> dict[str, RoleRate]:
    """Load role × hourly-rate triangle from ``baseline_organisation.csv``.

    Empty cells map to ``None``; those roles are non-billable and may not be
    used in a work-package role mix.
    """
    rates: dict[str, RoleRate] = {}
    with csv_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            role = row["role_name"].strip()
            if not role:
                continue
            min_v = row.get("role_hourly_min_eur") or ""
            par_v = row.get("role_hourly_par_eur") or ""
            max_v = row.get("role_hourly_max_eur") or ""
            rates[role] = RoleRate(
                role_name=role,
                min_eur_per_hour=float(min_v) if min_v.strip() else None,
                par_eur_per_hour=float(par_v) if par_v.strip() else None,
                max_eur_per_hour=float(max_v) if max_v.strip() else None,
            )
    return rates


# ── Multipliers ─────────────────────────────────────────────────────────


class Multiplier(BaseModel):
    """A multiplicative price overlay (compounds onto monetary cost only)."""

    multiplier_id: str
    label: str
    factor: float = Field(gt=0, lt=10)
    description: str


MULTIPLIERS: dict[str, Multiplier] = {
    "enterprise_premium": Multiplier(
        multiplier_id="enterprise_premium",
        label="Enterprise premium",
        factor=1.20,
        description="Enterprise governance + audit + legal-counsel coordination overhead.",
    ),
    "bridge_entity": Multiplier(
        multiplier_id="bridge_entity",
        label="Bridge-entity coordination",
        factor=1.10,
        description="Tri-party delivery via a partner bridge (extra alignment + handoff loops).",
    ),
    "locale_uplift_fr": Multiplier(
        multiplier_id="locale_uplift_fr",
        label="French locale uplift",
        factor=1.20,
        description="French market vs Madrid SME baseline (FR rate index).",
    ),
    "first_of_kind": Multiplier(
        multiplier_id="first_of_kind",
        label="First-of-kind novelty",
        factor=1.15,
        description="Novelty + learning-curve allowance for a first engagement of this archetype.",
    ),
    "repeat_counterparty": Multiplier(
        multiplier_id="repeat_counterparty",
        label="Repeat-counterparty discount",
        factor=0.90,
        description="Discount for a counterparty Holistika has already delivered to.",
    ),
}


# ── Country work calendar ───────────────────────────────────────────────


class CountryCalendar(BaseModel):
    """Country-specific working-hour and public-holiday parameters."""

    country_code: str
    legal_hours_per_day: float = Field(gt=0, le=12)
    public_holidays_per_year_avg: float = Field(ge=0, le=30)
    locale_uplift_pct: float = Field(ge=0, le=100)
    notes: str = ""


def load_calendar(csv_path: Path) -> dict[str, CountryCalendar]:
    """Load country calendars from the canonical CSV."""
    cals: dict[str, CountryCalendar] = {}
    with csv_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            code = row["country_code"].strip().upper()
            if not code:
                continue
            cals[code] = CountryCalendar(
                country_code=code,
                legal_hours_per_day=float(row["legal_hours_per_day"]),
                public_holidays_per_year_avg=float(row["public_holidays_per_year_avg"]),
                locale_uplift_pct=float(row["locale_uplift_pct"]),
                notes=row.get("notes", "") or "",
            )
    return cals


# ── Work package + estimation ───────────────────────────────────────────


class WorkPackage(BaseModel):
    """A scoped unit of an engagement = one method × an optional role override × multipliers.

    The ``role_mix_override`` lets the operator deviate from the method's default
    mix — for example to drop a Brand Manager out of an automation-only scope.
    """

    package_id: str
    method_id: MethodId
    label: str | None = None
    role_mix_override: dict[str, float] | None = None
    multiplier_ids: list[str] = Field(default_factory=list)

    @field_validator("role_mix_override")
    @classmethod
    def _override_shares(cls, value: dict[str, float] | None) -> dict[str, float] | None:
        if value is None:
            return value
        total = sum(value.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"role_mix_override shares must sum to ~1.0 (got {total:.3f}): {value}")
        return value


class PackageResult(BaseModel):
    """Computed outcome for a single work package."""

    package_id: str
    method_label: str
    effort_hours: TriEstimate
    blended_rate_eur_per_hour: TriEstimate
    cost_eur_pre_multiplier: TriEstimate
    multipliers_applied: list[str]
    multiplier_factor: float
    cost_eur_final: TriEstimate
    duration_working_days: TriEstimate


def blend_rate(role_mix: dict[str, float], rates: dict[str, RoleRate]) -> TriEstimate:
    """Blend a role × hourly-rate matrix by share-weighted average."""
    if not role_mix:
        raise ValueError("role_mix is empty")
    total = 0.0
    min_b = 0.0
    par_b = 0.0
    max_b = 0.0
    for role, share in role_mix.items():
        if role not in rates:
            raise KeyError(f"role {role!r} not in baseline_organisation rates")
        rr = rates[role]
        if not rr.is_billable:
            raise ValueError(f"role {role!r} is non-billable; cannot include in role mix")
        assert rr.min_eur_per_hour is not None
        assert rr.par_eur_per_hour is not None
        assert rr.max_eur_per_hour is not None
        min_b += share * rr.min_eur_per_hour
        par_b += share * rr.par_eur_per_hour
        max_b += share * rr.max_eur_per_hour
        total += share
    if not (0.99 <= total <= 1.01):
        raise ValueError(f"role_mix shares must sum to ~1.0 (got {total:.3f}): {role_mix}")
    return TriEstimate(min=min_b, par=par_b, max=max_b)


def working_days_for_hours(hours: TriEstimate, calendar: CountryCalendar) -> TriEstimate:
    """Convert a TriEstimate of effort hours to working days at the country legal day."""
    return hours.scale(1.0 / calendar.legal_hours_per_day)


def estimate_package(
    package: WorkPackage,
    rates: dict[str, RoleRate],
    calendar: CountryCalendar,
) -> PackageResult:
    """Compute the per-package effort, cost, and duration triple."""
    method = METHODS[package.method_id]
    role_mix = package.role_mix_override or method.default_role_mix
    blended = blend_rate(role_mix, rates)
    pre_cost = TriEstimate(
        min=method.effort_hours.min * blended.min,
        par=method.effort_hours.par * blended.par,
        max=method.effort_hours.max * blended.max,
    )
    factor = 1.0
    applied: list[str] = []
    for mid in package.multiplier_ids:
        if mid not in MULTIPLIERS:
            raise KeyError(f"multiplier {mid!r} not in MULTIPLIERS registry")
        factor *= MULTIPLIERS[mid].factor
        applied.append(mid)
    final_cost = pre_cost.scale(factor)
    duration = working_days_for_hours(method.effort_hours, calendar)
    return PackageResult(
        package_id=package.package_id,
        method_label=method.label,
        effort_hours=method.effort_hours,
        blended_rate_eur_per_hour=blended,
        cost_eur_pre_multiplier=pre_cost,
        multipliers_applied=applied,
        multiplier_factor=factor,
        cost_eur_final=final_cost,
        duration_working_days=duration,
    )


class EngagementScope(BaseModel):
    """Operator-supplied scope shape (mirrors ``scope.yaml``)."""

    engagement_slug: str
    counterparty_label: str
    country_code: str
    start_date: date | None = None
    packages: list[WorkPackage]
    notes: str = ""


class EngagementEstimate(BaseModel):
    """Aggregate result for a full engagement = list of PackageResult + totals."""

    scope: EngagementScope
    calendar: CountryCalendar
    package_results: list[PackageResult]

    @property
    def total_effort_hours(self) -> TriEstimate:
        return _sum_tri([p.effort_hours for p in self.package_results])

    @property
    def total_cost_eur(self) -> TriEstimate:
        return _sum_tri([p.cost_eur_final for p in self.package_results])

    @property
    def total_duration_working_days(self) -> TriEstimate:
        return _sum_tri([p.duration_working_days for p in self.package_results])


def _sum_tri(items: list[TriEstimate]) -> TriEstimate:
    if not items:
        return TriEstimate(min=0, par=0, max=0)
    return TriEstimate(
        min=sum(i.min for i in items),
        par=sum(i.par for i in items),
        max=sum(i.max for i in items),
    )


def estimate_engagement(
    scope: EngagementScope,
    rates: dict[str, RoleRate],
    calendars: dict[str, CountryCalendar],
) -> EngagementEstimate:
    """End-to-end estimation for one engagement."""
    code = scope.country_code.strip().upper()
    if code not in calendars:
        raise KeyError(f"country_code {code!r} not in COUNTRY_WORK_CALENDAR.csv")
    cal = calendars[code]
    results = [estimate_package(p, rates, cal) for p in scope.packages]
    return EngagementEstimate(scope=scope, calendar=cal, package_results=results)


# ── Bank-holiday-aware schedule ─────────────────────────────────────────


def project_end_date(
    start: date,
    working_days: float,
    calendar: CountryCalendar,
) -> date:
    """Return the end date after consuming ``working_days`` from ``start``.

    Implementation: skip Saturdays and Sundays + advance an extra
    ``public_holidays_per_year_avg`` × (calendar_days / 365) day-equivalents.
    The estimate is intentionally simple — proposals carry approximate dates,
    not contract-grade schedules.
    """
    if working_days <= 0:
        return start
    days = 0
    cursor = start
    bumped = 0
    target = int(round(working_days))
    while days < target:
        cursor = cursor + timedelta(days=1)
        if cursor.weekday() < 5:
            days += 1
        bumped += 1
        if bumped > 365 * 5:
            raise RuntimeError("project_end_date exceeded 5-year search horizon")
    span_days = (cursor - start).days
    holiday_bump = int(round(calendar.public_holidays_per_year_avg * span_days / 365.0))
    cursor = cursor + timedelta(days=holiday_bump)
    return cursor


# ── Mermaid Gantt rendering ─────────────────────────────────────────────


def render_mermaid_gantt(estimate: EngagementEstimate) -> str:
    """Render the engagement as a Mermaid ``gantt`` block.

    Tasks are placed sequentially from ``estimate.scope.start_date`` (defaulting
    to today). A ``par``-day duration is used; min and max appear in the
    surrounding markdown table, not in the Gantt itself, to keep the visual
    deterministic.
    """
    start = estimate.scope.start_date or date.today()
    lines = [
        "```mermaid",
        "gantt",
        f"  title Calendrier prévisionnel — {estimate.scope.counterparty_label}",
        "  dateFormat  YYYY-MM-DD",
        "  axisFormat  %d %b",
        "  excludes    weekends",
    ]
    section_label = "Engagement"
    lines.append(f"  section {section_label}")
    cursor = start
    for r in estimate.package_results:
        par_days = max(1, int(round(r.duration_working_days.par)))
        task_id = r.package_id.replace("-", "_")
        lines.append(
            f"  {r.method_label[:60].replace(':', ' ')} : {task_id}, "
            f"{cursor.isoformat()}, {par_days}d"
        )
        cursor = project_end_date(cursor, par_days, estimate.calendar)
    lines.append("```")
    return "\n".join(lines)


def render_commercial_schedule_markdown(estimate: EngagementEstimate) -> str:
    """Render a full ``commercial-schedule.md`` body (math table + Gantt)."""
    s = estimate.scope
    cal = estimate.calendar
    lines: list[str] = []
    lines.append(f"# Commercial schedule — {s.counterparty_label}")
    lines.append("")
    lines.append(
        f"> Computed {date.today().isoformat()} from `SOP-ENG_ESTIMATION_DISCIPLINE_001`. "
        f"Country `{cal.country_code}` ({cal.legal_hours_per_day:.1f} h/day, "
        f"{cal.public_holidays_per_year_avg:.0f} public-holiday-equivalent days/year, "
        f"locale uplift {cal.locale_uplift_pct:.0f}%)."
    )
    lines.append("")
    lines.append("## Per-package estimate")
    lines.append("")
    lines.append(
        "| Package | Method | Effort h (min/par/max) | Blended rate €/h (min/par/max) | "
        "Cost € pre-mult | Multiplier × | Cost € final (min/par/max) | Duration days (min/par/max) |"
    )
    lines.append(
        "|:---|:---|:---|:---|:---|:---|:---|:---|"
    )
    for r in estimate.package_results:
        lines.append(
            f"| `{r.package_id}` | {r.method_label} | "
            f"{r.effort_hours.min:.0f} / {r.effort_hours.par:.0f} / {r.effort_hours.max:.0f} | "
            f"{r.blended_rate_eur_per_hour.min:.0f} / {r.blended_rate_eur_per_hour.par:.0f} / {r.blended_rate_eur_per_hour.max:.0f} | "
            f"{r.cost_eur_pre_multiplier.par:,.0f} | "
            f"{r.multiplier_factor:.3f} ({', '.join(r.multipliers_applied) or '—'}) | "
            f"{r.cost_eur_final.min:,.0f} / {r.cost_eur_final.par:,.0f} / {r.cost_eur_final.max:,.0f} | "
            f"{r.duration_working_days.min:.1f} / {r.duration_working_days.par:.1f} / {r.duration_working_days.max:.1f} |"
        )
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    te = estimate.total_effort_hours
    tc = estimate.total_cost_eur
    td = estimate.total_duration_working_days
    lines.append("| Aggregate | min | par (PERT-expected) | max |")
    lines.append("|:---|---:|---:|---:|")
    lines.append(f"| Effort hours | {te.min:.0f} | {te.par:.0f} (E={te.expected:.0f}) | {te.max:.0f} |")
    lines.append(f"| Cost (€) | {tc.min:,.0f} | {tc.par:,.0f} (E={tc.expected:,.0f}) | {tc.max:,.0f} |")
    lines.append(
        f"| Duration (working days) | {td.min:.0f} | {td.par:.0f} (E={td.expected:.0f}) | {td.max:.0f} |"
    )
    lines.append("")
    lines.append("## Visual schedule (Mermaid Gantt)")
    lines.append("")
    lines.append(render_mermaid_gantt(estimate))
    lines.append("")
    if s.notes:
        lines.append("## Notes")
        lines.append("")
        lines.append(s.notes)
        lines.append("")
    return "\n".join(lines)
