"""Pydantic SSOT models for UAT (User Acceptance Testing) closure reports.

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md``
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_UAT_GOVERNANCE_001.md``
Paired runbook: ``scripts/validate_uat_report.py``
Companion cursor rule: ``.cursor/rules/akos-uat-discipline.mdc``

I86 Wave R+1 decision lineage (2026-05-24):
- D-IH-86-AV (UAT_DISCIPLINE canonical mint, 2026-05-20).
- D-IH-86-AS (UAT quality bar canonization in akos-planning-traceability.mdc, 2026-05-20).
- D-IH-86-CW (charter→active promotion via this Pydantic + SOP + runbook + skill + rule
  + process_list row + pattern_uat_class_taxonomy registry row + 3-wave field-test window
  monitoring obligation; operator-ratified at META-RATIFY batch meta4-b).

Frozen models:

- ``UATReportFrontmatter`` — frozen BaseModel; mandatory + optional UAT-report frontmatter
  shape per UAT_DISCIPLINE.md §8.5 §"Mandatory frontmatter fields".
- ``UATReportFinding`` — one row per validator finding (typically 1-10 per report).
- ``UATReportValidation`` — wrapper aggregating findings + counts + metadata for one
  UAT-report validation pass.
- ``CanonicalFieldTestWindow`` — the ``field_test_window:`` frontmatter block on a Quality
  Fabric specialty canonical (first instantiation: UAT_DISCIPLINE.md per
  D-IH-86-CW META4-b operator ratification; future specialty promotions inherit the same
  schema). Carries open/close metadata, conjunctive promotion criteria, disjunctive
  revocation triggers, and a 4-state lifecycle (open / closing / closed / revoked).
- ``CanonicalFieldTestWindowPromotionCriterion`` — one conjunctive PASS clause; FTW-XXX-NN
  coded for traceability across observation waves.
- ``CanonicalFieldTestWindowRevocationTrigger`` — one disjunctive demotion trigger; coded
  symmetrically for traceability when fired.

All models follow ``akos-holistika-operations.mdc`` §"New git-canonical compliance
registers" + ``CONTRIBUTING.md`` §"Python Code Standards": frozen BaseModel, Literal
enums for governed columns, regex patterns on slug-shaped fields, length bounds on
free-text fields.

The runbook ``scripts/validate_uat_report.py`` constructs these models from the parsed
markdown frontmatter + section structure and emits findings via the 5-option enum per
UAT_DISCIPLINE.md §6 + akos-uat-discipline.mdc RULE 2 (rework-now / amend-followup-
rationale / defer-OPS / accept-as-canon / escalate-to-blocker-tracker). The release-gate
``run_uat_report_validation()`` exercises self-test mode (fixture-based) at every
pre_commit; the full sweep is on_demand cadence per the canonical §4.
"""

from __future__ import annotations

import datetime as _dt
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

UAT_REPORT_FRONTMATTER_FIELDNAMES: tuple[str, ...] = (
    "title",
    "verdict",
    "closure_decision_source",
    "ratifying_decisions",
    "linked_runbooks",
    "verdict_history",
    "verdict_followup_rationale",
    "last_review",
    "audience",
    "channel",
    "scenario",
    "register",
    "status",
)


UAT_REPORT_FINDING_FIELDNAMES: tuple[str, ...] = (
    "finding_code",
    "section",
    "severity",
    "verdict",
    "proposed_action",
    "notes",
)


UAT_REPORT_VALIDATION_FIELDNAMES: tuple[str, ...] = (
    "report_id",
    "report_path",
    "validated_at",
    "validated_by",
    "is_forward_only",
    "findings",
    "pass_count",
    "fail_count",
    "warn_count",
    "info_count",
    "skip_count",
    "total_findings",
)


CANONICAL_FIELD_TEST_WINDOW_FIELDNAMES: tuple[str, ...] = (
    "open_date",
    "open_decision_id",
    "open_wave",
    "close_target_wave",
    "close_target_date_estimate",
    "revocation_decision_id_template",
    "monitoring_obligation_owner",
    "monitoring_obligation_co_owner",
    "promotion_criteria",
    "revocation_triggers",
    "status",
    "last_observation_wave",
    "last_observation_date",
    "last_observation_summary",
)


VALID_FIELD_TEST_WINDOW_STATUSES: frozenset[str] = frozenset({
    "open",      # currently monitoring; promotion is provisional + revocable
    "closing",   # final monitoring wave reached; verdict pending operator review
    "closed",    # window closed; promotion is durable (window archived)
    "revoked",   # window forced demotion back to charter (successor decision minted)
})


# FTW code shapes (both promotion criteria + revocation triggers):
#   Promotion:  FTW-<discipline>-<NN>-<short-slug>      e.g. FTW-UAT-01-THREE-CLOSURE-UATS
#   Revocation: FTW-<discipline>-RT-<NN>-<short-slug>   e.g. FTW-UAT-RT-01-VALIDATOR-MISFIRE
FIELD_TEST_WINDOW_CODE_PATTERN: str = r"^FTW-[A-Z]+(?:-RT)?-\d{2}-[A-Z0-9\-]+$"


VALID_VERDICTS: frozenset[str] = frozenset({
    "PASS",
    "PASS-WITH-FOLLOWUP",
    "FAIL",
    "PENDING-OPERATOR-WALK",
})


VALID_CLOSURE_DECISION_SOURCES: frozenset[str] = frozenset({
    "agent_inline_default",
    "operator_explicit",
    "n/a",
})


VALID_FINDING_CODES: frozenset[str] = frozenset({
    "UAT-FM-01-VERDICT-MISSING",
    "UAT-FM-02-VERDICT-INVALID",
    "UAT-FM-03-CLOSURE-DECISION-SOURCE-MISSING",
    "UAT-FM-04-CLOSURE-DECISION-SOURCE-INVALID",
    "UAT-FM-05-RATIFYING-DECISIONS-MISSING",
    "UAT-FM-06-RATIFYING-DECISIONS-FK-UNRESOLVED",
    "UAT-FM-07-LINKED-RUNBOOKS-MISSING",
    "UAT-FM-08-LINKED-RUNBOOKS-FK-UNRESOLVED",
    "UAT-FM-09-VERDICT-HISTORY-MISSING-ON-AMENDMENT",
    "UAT-FM-10-LAST-REVIEW-MISSING-OR-MALFORMED",
    "UAT-FM-11-PWF-WITHOUT-RATIONALE",
    "UAT-SEC-01-CLOSURE-SUMMARY-MISSING",
    "UAT-SEC-02-CLOSURE-CRITERIA-VERIFICATION-MISSING",
    "UAT-SEC-03-MECHANICAL-EVIDENCE-MISSING",
    "UAT-SEC-04-PER-DIMENSION-FINDINGS-MISSING",
    "UAT-SEC-05-D-IH-86-D-CROSS-CHECK-MISSING",
    "UAT-SEC-06-SOP-RUNBOOK-PAIR-MISSING",
    "UAT-SEC-07-RISK-REGISTER-CLOSURE-MISSING",
    "UAT-SEC-08-DECISION-CLOSE-OUTS-MISSING",
    "UAT-SEC-09-CLOSURE-REGISTRY-EDITS-MISSING",
    "UAT-SEC-10-VERDICT-SIGNOFF-CHECKLIST-MISSING",
    "UAT-SEC-11-CROSS-REFERENCES-MISSING",
    "UAT-RB-01-HISTORICAL-EXEMPT",
})


VALID_FINDING_SEVERITIES: frozenset[str] = frozenset({
    "FAIL",
    "WARN",
    "INFO",
    "N/A",
})


VALID_FINDING_VERDICTS: frozenset[str] = frozenset({
    "clean",
    "drift",
    "gap",
    "exempt",
    "skip",
})


# Section regex patterns. Each pattern matches the section header line.
# Accepts BOTH compact form (`## 1 — Closure summary`) and verbose form
# (`## Section 1 — Closure summary`) per the I86 cluster-coordinator Wave R closure
# precedent (the worked example minted simultaneously with this bar). Dashes accepted:
# em-dash (U+2014), en-dash (U+2013), hyphen, or omitted entirely.
_SEC_PREFIX = r"^##\s+(?:Section\s+)?"
_SEC_DASH = r"\s*[\u2014\u2013\-:]?\s*"
MANDATORY_SECTION_PATTERNS: tuple[tuple[str, str], ...] = (
    ("UAT-SEC-01", _SEC_PREFIX + r"1[.\)]?" + _SEC_DASH + r"Closure\s+summary"),
    ("UAT-SEC-02", _SEC_PREFIX + r"2[.\)]?" + _SEC_DASH + r"Closure[\-\s]criteria\s+verification"),
    ("UAT-SEC-03", _SEC_PREFIX + r"3[.\)]?" + _SEC_DASH + r"Mechanical\s+evidence"),
    ("UAT-SEC-04", _SEC_PREFIX + r"4[.\)]?" + _SEC_DASH + r"Per[\-\s]dimension\s+findings"),
    ("UAT-SEC-05", _SEC_PREFIX + r"5[.\)]?" + _SEC_DASH + r"D[\-\s]?IH[\-\s]?86[\-\s]?D"),
    ("UAT-SEC-06", _SEC_PREFIX + r"6[.\)]?" + _SEC_DASH + r"SOP\s*[\+\&\s]+runbook\s+pair"),
    ("UAT-SEC-07", _SEC_PREFIX + r"7[.\)]?" + _SEC_DASH + r"Risk[\-\s]register\s+closure"),
    ("UAT-SEC-08", _SEC_PREFIX + r"8[.\)]?" + _SEC_DASH + r"Decision\s+close[\-\s]outs?"),
    ("UAT-SEC-09", _SEC_PREFIX + r"9[.\)]?" + _SEC_DASH + r"Closure\s+registry\s+edits"),
    ("UAT-SEC-10", _SEC_PREFIX + r"10[.\)]?" + _SEC_DASH + r"Verdict"),
    ("UAT-SEC-11", _SEC_PREFIX + r"11[.\)]?" + _SEC_DASH + r"Cross[\-\s]references"),
)


# 2026-05-19 is the watershed date per UAT_DISCIPLINE.md §"Migration posture for
# pre-2026-05-19 initiatives" (D-IH-86-AS canonization).
FORWARD_ONLY_WATERSHED_ISO_DATE: str = "2026-05-19"


DECISION_ID_PATTERN: str = r"^D-IH-\d+-[A-Z]{1,2}(?:-[a-z][a-z0-9\-]*)?$"


class UATReportFrontmatter(BaseModel):
    """Frozen Pydantic model for closure-UAT report frontmatter shape.

    Mirrors UAT_DISCIPLINE.md §8.5 §"Mandatory frontmatter fields" + the SOP-PEOPLE_
    UAT_GOVERNANCE_001 contract. Optional fields use defaults; required fields raise
    on construction.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="allow",
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    title: str = Field(..., min_length=1, max_length=500)
    verdict: Literal[
        "PASS",
        "PASS-WITH-FOLLOWUP",
        "FAIL",
        "PENDING-OPERATOR-WALK",
    ]
    closure_decision_source: Literal[
        "agent_inline_default",
        "operator_explicit",
        "n/a",
    ]
    ratifying_decisions: list[str] = Field(..., min_length=1)
    linked_runbooks: list[str] = Field(default_factory=list)
    verdict_history: list[str] = Field(default_factory=list)
    verdict_followup_rationale: str | None = Field(default=None, max_length=2000)
    last_review: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    audience: str | None = Field(default=None, max_length=200)
    channel: str | None = Field(default=None, max_length=200)
    scenario: str | None = Field(default=None, max_length=500)
    report_register: Literal["internal", "external", "mixed"] | None = Field(
        default=None, alias="register"
    )
    status: str | None = Field(default=None, max_length=200)


class UATReportFinding(BaseModel):
    """Frozen Pydantic model for one validator finding row."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    finding_code: str = Field(..., min_length=1, max_length=80)
    section: str = Field(..., min_length=1, max_length=160)
    severity: Literal["FAIL", "WARN", "INFO", "N/A"]
    verdict: Literal["clean", "drift", "gap", "exempt", "skip"]
    proposed_action: str = Field(..., min_length=1, max_length=600)
    notes: str = Field(default="", max_length=1000)


class UATReportValidation(BaseModel):
    """Frozen Pydantic model wrapping one UAT-report validation run."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    report_id: str = Field(..., min_length=1, max_length=200)
    report_path: str = Field(..., min_length=1, max_length=400)
    validated_at: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?$")
    validated_by: str = Field(..., min_length=1, max_length=80)
    is_forward_only: bool
    findings: list[UATReportFinding] = Field(default_factory=list)
    pass_count: int = Field(..., ge=0)
    fail_count: int = Field(..., ge=0)
    warn_count: int = Field(..., ge=0)
    info_count: int = Field(..., ge=0)
    skip_count: int = Field(..., ge=0)
    total_findings: int = Field(..., ge=0)


class CanonicalFieldTestWindowPromotionCriterion(BaseModel):
    """One conjunctive PASS clause inside a CanonicalFieldTestWindow.

    Promotion criteria are CONJUNCTIVE: ALL criteria must observe PASS at the
    close_target_wave for the window to land at ``status: closed`` (durable
    promotion). Any criterion observing FAIL surfaces an inline-ratify gate;
    if not recoverable, the operator (or AIC role_owner) flips the window to
    ``status: revoked`` + mints the revocation decision per the parent
    canonical's ``revocation_decision_id_template``.

    Code shape ``FTW-<discipline>-<NN>-<short-slug>`` enables traceability
    across observation waves (the same criterion is referenced by code from
    each wave-close UAT report; observation cumulates without ambiguity).
    """

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    code: str = Field(
        ...,
        min_length=1,
        max_length=80,
        pattern=FIELD_TEST_WINDOW_CODE_PATTERN,
    )
    statement: str = Field(..., min_length=1, max_length=600)


class CanonicalFieldTestWindowRevocationTrigger(BaseModel):
    """One disjunctive demotion trigger inside a CanonicalFieldTestWindow.

    Revocation triggers are DISJUNCTIVE: ANY observed trigger fires the
    window's revocation path (status flips to ``revoked``; successor decision
    minted per ``revocation_decision_id_template``). Triggers are evaluated
    at every observation wave; the first-fired trigger wins.

    Code shape symmetric to promotion criteria (``FTW-<discipline>-RT-NN-...``)
    for cross-wave traceability when fired.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    code: str = Field(
        ...,
        min_length=1,
        max_length=80,
        pattern=FIELD_TEST_WINDOW_CODE_PATTERN,
    )
    statement: str = Field(..., min_length=1, max_length=600)


class CanonicalFieldTestWindow(BaseModel):
    """Frozen Pydantic model for the ``field_test_window:`` frontmatter block.

    First instantiation: ``UAT_DISCIPLINE.md`` @ I86 Wave R+1 (D-IH-86-CW; META4-b
    operator ratification: 'PASS now + explicit field-test window'). Future
    Quality Fabric specialty promotions (D-IH-86-CX PWF discipline; future
    SYNTHESIS_BEFORE_TRANCHE; etc.) inherit this schema verbatim.

    Lifecycle (status enum semantics):

    - ``open`` — window is monitoring; promotion is provisional + revocable.
      Each observation wave updates ``last_observation_wave`` /
      ``last_observation_date`` / ``last_observation_summary`` in-place.
    - ``closing`` — final monitoring wave reached; verdict pending operator
      review at the next wave-close ratify gate.
    - ``closed`` — promotion is durable (window archived; canonical's
      ``status: active`` is no longer provisional).
    - ``revoked`` — promotion demoted (revocation decision minted; canonical's
      ``status:`` reverts to charter or earlier-stage; sibling pattern-registry
      + process_list rows flip to ``status: inactive`` until re-promoted).

    Rationale for surfacing this as machine-readable frontmatter (vs body
    prose) per operator's Q3-b ratification at I86 Wave R+1: the field-test
    window is governance metadata, not narrative. Burying it in §10.4 prose
    would erode visibility across waves + make programmatic monitoring
    (future ``validate_field_test_windows.py`` runbook forward-charter)
    impossible.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    open_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    open_decision_id: str = Field(..., pattern=DECISION_ID_PATTERN)
    open_wave: str = Field(..., min_length=1, max_length=20)
    close_target_wave: str = Field(..., min_length=1, max_length=20)
    close_target_date_estimate: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    revocation_decision_id_template: str = Field(
        ..., min_length=1, max_length=80
    )
    monitoring_obligation_owner: str = Field(..., min_length=1, max_length=80)
    monitoring_obligation_co_owner: str | None = Field(default=None, max_length=80)
    promotion_criteria: list[CanonicalFieldTestWindowPromotionCriterion] = Field(
        ..., min_length=1
    )
    revocation_triggers: list[CanonicalFieldTestWindowRevocationTrigger] = Field(
        ..., min_length=1
    )
    status: Literal["open", "closing", "closed", "revoked"]
    last_observation_wave: str | None = Field(default=None, max_length=20)
    last_observation_date: str | None = Field(
        default=None, pattern=r"^\d{4}-\d{2}-\d{2}$"
    )
    last_observation_summary: str | None = Field(default=None, max_length=600)

    @field_validator(
        "open_date",
        "close_target_date_estimate",
        "last_observation_date",
        mode="before",
    )
    @classmethod
    def _coerce_date_to_iso(cls, v: Any) -> Any:
        """Coerce PyYAML-parsed ``datetime.date`` to ISO string.

        PyYAML auto-parses unquoted ``YYYY-MM-DD`` tokens into ``datetime.date``
        objects. We accept either shape and normalise to the canonical ISO
        string so the regex ``pattern=`` constraint sees the string form.
        Quoting dates in YAML is also fine — this validator no-ops on strings.
        """
        if isinstance(v, _dt.date) and not isinstance(v, _dt.datetime):
            return v.isoformat()
        if isinstance(v, _dt.datetime):
            return v.date().isoformat()
        return v


def fixture_frontmatter_pass() -> UATReportFrontmatter:
    """Self-test fixture: clean PASS frontmatter (no PWF; no amendment)."""
    return UATReportFrontmatter(
        title="Closure UAT — Wave Z (fixture)",
        verdict="PASS",
        closure_decision_source="operator_explicit",
        ratifying_decisions=["D-IH-86-CW"],
        linked_runbooks=["scripts/validate_uat_report.py"],
        verdict_history=[],
        verdict_followup_rationale=None,
        last_review="2026-05-24",
        audience="J-OP;J-AIC",
        channel="CHAN-EMAIL-OUTBOUND",
        scenario="fixture_self_test",
        report_register="internal",
        status="active",
    )


def fixture_frontmatter_pwf_clean() -> UATReportFrontmatter:
    """Self-test fixture: clean PASS-WITH-FOLLOWUP with mandatory rationale."""
    return UATReportFrontmatter(
        title="Closure UAT — Wave Z PWF (fixture)",
        verdict="PASS-WITH-FOLLOWUP",
        closure_decision_source="operator_explicit",
        ratifying_decisions=["D-IH-86-CW", "D-IH-86-CX"],
        linked_runbooks=["scripts/validate_uat_report.py"],
        verdict_history=[],
        verdict_followup_rationale=(
            "Field-test window per D-IH-86-CW promotion-with-revocability framing; "
            "demote to charter via D-IH-86-CW-revoke if Waves S+T+U misfire."
        ),
        last_review="2026-05-24",
        audience="J-OP;J-AIC",
        channel=None,
        scenario="fixture_self_test_pwf",
        report_register="internal",
        status="active",
    )


def fixture_finding_fail() -> UATReportFinding:
    """Self-test fixture: a representative FAIL finding."""
    return UATReportFinding(
        finding_code="UAT-FM-11-PWF-WITHOUT-RATIONALE",
        section="frontmatter:verdict_followup_rationale",
        severity="FAIL",
        verdict="gap",
        proposed_action=(
            "Append verdict_followup_rationale: <text> field OR change verdict from "
            "PASS-WITH-FOLLOWUP to PASS / FAIL per PWF discipline."
        ),
        notes="Closes the PWF abuse pattern surfaced by operator at I86 Wave R+1 ex5.",
    )


def fixture_validation_pass() -> UATReportValidation:
    """Self-test fixture: clean PASS validation (no findings)."""
    return UATReportValidation(
        report_id="fixture-uat-validation-pass",
        report_path="reports/uat-fixture.md",
        validated_at="2026-05-24T00:00:00Z",
        validated_by="self_test",
        is_forward_only=True,
        findings=[],
        pass_count=15,
        fail_count=0,
        warn_count=0,
        info_count=0,
        skip_count=0,
        total_findings=0,
    )


def fixture_canonical_field_test_window_open() -> CanonicalFieldTestWindow:
    """Self-test fixture: open field-test window per UAT_DISCIPLINE.md @ Wave R+1.

    This fixture mirrors the EXACT frontmatter block landed at
    UAT_DISCIPLINE.md per D-IH-86-CW. Any deviation between this fixture and
    the canonical's frontmatter block is a structural drift that the validator
    surfaces at self-test time.
    """
    return CanonicalFieldTestWindow(
        open_date="2026-05-24",
        open_decision_id="D-IH-86-CW",
        open_wave="R+1",
        close_target_wave="U",
        close_target_date_estimate="2026-06-14",
        revocation_decision_id_template="D-IH-86-CW-revoke",
        monitoring_obligation_owner="PMO",
        monitoring_obligation_co_owner="AIC role_owner",
        promotion_criteria=[
            CanonicalFieldTestWindowPromotionCriterion(
                code="FTW-UAT-01-THREE-CLOSURE-UATS",
                statement=(
                    ">= 3 closure-UAT reports authored under the new bar across "
                    "Waves S, T, U with verdict in PASS / PASS-WITH-FOLLOWUP "
                    "and all 11 sections + mandatory frontmatter fields present."
                ),
            ),
            CanonicalFieldTestWindowPromotionCriterion(
                code="FTW-UAT-02-FAIL-CEILING",
                statement=(
                    "<= 2 cumulative validator FAIL findings across the 3 reports "
                    "(after disposition + amendment commits land)."
                ),
            ),
            CanonicalFieldTestWindowPromotionCriterion(
                code="FTW-UAT-03-NO-VALIDATOR-MISFIRES",
                statement=(
                    "0 false-positive findings requiring accept-as-canon disposition "
                    "for structural validator regex misfire (RULE 5 option 4 used "
                    "exclusively for genuine validator/canonical schema drift, never "
                    "to paper over a draft that forgot a section)."
                ),
            ),
            CanonicalFieldTestWindowPromotionCriterion(
                code="FTW-UAT-04-PWF-RATIONALE-COMPLIANCE",
                statement=(
                    "0 RULE-3 PWF-without-rationale findings on Waves S/T/U reports "
                    "(the bar self-proves via the Wave R UAT amendment landing first, "
                    "in the same commit-window as this promotion, as the canonical "
                    "worked-example for the 12th/13th specialty enforcement)."
                ),
            ),
        ],
        revocation_triggers=[
            CanonicalFieldTestWindowRevocationTrigger(
                code="FTW-UAT-RT-01-VALIDATOR-MISFIRE",
                statement=(
                    ">= 1 validator false-positive requiring structural regex amendment "
                    "in < 3 waves (signal that the regex set is too strict / brittle; "
                    "specialty needs re-grounding against more real-report variance)."
                ),
            ),
            CanonicalFieldTestWindowRevocationTrigger(
                code="FTW-UAT-RT-02-PWF-DISCIPLINE-NOT-SINKING",
                statement=(
                    ">= 2 RULE-3 PWF-without-rationale findings on Waves S/T/U reports "
                    "(signal that PWF discipline is not sinking in across agent + "
                    "operator authoring practice; 12th specialty needs revision or "
                    "the 13th sibling specialty D-IH-86-CX needs sharpening)."
                ),
            ),
            CanonicalFieldTestWindowRevocationTrigger(
                code="FTW-UAT-RT-03-OPERATOR-EXPLICIT",
                statement=(
                    "Operator-explicit revocation (any wave, any reason; honored "
                    "verbatim per operator-explicit override per "
                    "akos-inline-ratification.mdc §Time-box recovery escape)."
                ),
            ),
        ],
        status="open",
        last_observation_wave=None,
        last_observation_date=None,
        last_observation_summary=None,
    )
