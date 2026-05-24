"""Pydantic SSOT models for PASS-WITH-FOLLOWUP governance (12th Quality Fabric specialty).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md``
Paired runbook: ``scripts/validate_pwf_governance.py`` (the validator IS the runbook —
this discipline is check-class, not fix-class; rationale authoring is human/AIC work
and can't be auto-fixed).
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_PWF_GOVERNANCE_001.md``
Companion cursor rule: ``.cursor/rules/akos-pwf-governance.mdc``
Companion skill: ``.cursor/skills/pwf-governance-craft/SKILL.md``

Decision lineage:
- D-IH-86-CW (Wave R+1 Commit 1; UAT_DISCIPLINE.md charter→active promotion + the
  Wave R UAT amendment that exposed PWF-without-rationale as a recurring failure
  mode worth its own specialty mint).
- D-IH-86-CX (Wave R+1 Commit 3-a; this mint; codifies the 5-class followup
  taxonomy + structural rationale shape + INFO→FAIL ramp).

Architecture (compose_PWF rule materialisation):

``compose_PWF(uat_class, verdict, frontmatter) -> structural finding set``

  where:
    if verdict != "PASS-WITH-FOLLOWUP": no-op (this specialty governs PWF only)
    else:
      rationale = parse_followup_rationale(frontmatter.get("verdict_followup_rationale"))
      if rationale is None or rationale.followup_class is None:
        emit PWF-FM-01-CLASS-MISSING  (FAIL)
      if rationale.followup_class not in VALID_FOLLOWUP_CLASSES:
        emit PWF-FM-02-CLASS-UNKNOWN  (FAIL)
      if rationale.followup_class in REQUIRED_CLOSURE_TARGET_CLASSES and not rationale.closure_target:
        emit PWF-FM-03-CLOSURE-TARGET-MISSING  (FAIL)
      if rationale.followup_class in REQUIRED_TRACKER_PATH_CLASSES and not rationale.tracker_path:
        emit PWF-FM-04-TRACKER-PATH-MISSING  (FAIL)
      if rationale.tracker_path and not Path(rationale.tracker_path).exists():
        emit PWF-FM-04-TRACKER-PATH-INVALID  (FAIL)
      if rationale.owner is None or rationale.owner.strip() == "":
        emit PWF-FM-05-OWNER-MISSING  (WARN)

The 5 followup classes (D-IH-86-CX §3 enum):

1. ``monitoring-obligation`` — verdict carries forward an obligation to monitor
   a multi-wave field-test window or post-promotion observation cadence.
   The UAT itself is PASS in substance; the FOLLOWUP is the cadence to keep
   observing. Worked example: Wave R+1 P1 UAT promoting UAT_DISCIPLINE to
   ``active`` with a 3-wave FTW carries this class.
   Required: closure_target (e.g., "Wave U close"). Optional: tracker_path.

2. ``deferred-work-with-tracker`` — verdict carries forward concrete work that
   was scoped-out of the current wave but is named + tracked in a tracker file
   or OPS_REGISTER row. Worked example: B-2c closure UAT carrying live MCP
   spot-checks deferred to a future wave with a named tracker.
   Required: closure_target, tracker_path. Optional: closure_decision_id_target.

3. ``convention-class-followup`` — verdict carries forward a doctrinal /
   convention-class refinement that surfaced during the wave but is not
   blocking. Often shapes a successor wave's authoring; sometimes ratifies
   into a follow-up decision row. Worked example: Wave R surfacing "PWF
   discipline needs its own specialty" itself (which became this very
   canonical's birth artifact).
   Required: closure_target (the wave or decision where convention promotes).
   Optional: closure_decision_id_target.

4. ``mechanical-recovery-with-eta`` — verdict carries forward a known
   mechanical fix that the agent has identified but has not landed in the
   wave's commit window (e.g., validator threshold tweak, sync emit
   regeneration, mirror reseed). Worked example: a release-gate INFO advisory
   that should flip to FAIL after a paired commit lands.
   Required: closure_target (ISO date or wave), ETA-shaped notes.

5. ``escalation-to-blocker-tracker`` — verdict could not clear because of
   external dependency or operator judgement gap; tracker file under
   ``docs/wip/planning/_blockers/`` records the escalation per
   ``akos-conflict-surfacing-and-blocker-trackers.mdc``.
   Required: closure_target, tracker_path (under _blockers/).

Per ``akos-holistika-operations.mdc`` §"New git-canonical compliance registers"
+ ``CONTRIBUTING.md`` §"Python Code Standards": frozen BaseModel, Literal enums
for governed columns, regex patterns on slug-shaped fields, length bounds on
free-text fields.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


PWF_FOLLOWUP_RATIONALE_FIELDNAMES: tuple[str, ...] = (
    "followup_class",
    "closure_target",
    "owner",
    "tracker_path",
    "closure_decision_id_target",
    "notes",
)


PWF_GOVERNANCE_FINDING_FIELDNAMES: tuple[str, ...] = (
    "finding_code",
    "surface_path",
    "severity",
    "class_observed",
    "proposed_remediation",
    "notes",
)


PWF_GOVERNANCE_REPORT_FIELDNAMES: tuple[str, ...] = (
    "report_id",
    "swept_at",
    "swept_by",
    "scope",
    "findings",
    "clean_count",
    "warn_count",
    "fail_count",
    "total_findings",
)


VALID_FOLLOWUP_CLASSES: frozenset[str] = frozenset({
    "monitoring-obligation",
    "deferred-work-with-tracker",
    "convention-class-followup",
    "mechanical-recovery-with-eta",
    "escalation-to-blocker-tracker",
})


VALID_FINDING_CODES: frozenset[str] = frozenset({
    "PWF-FM-01-CLASS-MISSING",
    "PWF-FM-02-CLASS-UNKNOWN",
    "PWF-FM-03-CLOSURE-TARGET-MISSING",
    "PWF-FM-04-TRACKER-PATH-MISSING",
    "PWF-FM-04-TRACKER-PATH-INVALID",
    "PWF-FM-05-OWNER-MISSING",
})


VALID_SEVERITIES: frozenset[str] = frozenset({
    "info",
    "warn",
    "fail",
})


VALID_SCOPES: frozenset[str] = frozenset({
    "single-report",
    "wave-close-sweep",
    "full-sweep",
})


REQUIRED_CLOSURE_TARGET_CLASSES: frozenset[str] = frozenset({
    "deferred-work-with-tracker",
    "convention-class-followup",
    "mechanical-recovery-with-eta",
    "escalation-to-blocker-tracker",
    "monitoring-obligation",
})


REQUIRED_TRACKER_PATH_CLASSES: frozenset[str] = frozenset({
    "deferred-work-with-tracker",
    "escalation-to-blocker-tracker",
})


CLOSURE_TARGET_PATTERN: str = (
    r"^(Wave-[A-Z]+(\.\d+)?(\s+close)?"
    r"|\d{4}-\d{2}-\d{2}"
    r"|OPS-\d+-\d+(\s+closed)?"
    r"|D-IH-\d+-[A-Z0-9_]+"
    r"|I\d+\s+P\d+(\s+entry)?"
    r"|FTW-[A-Z0-9-]+\s+(closes|opens)"
    r")$"
)


class PWFFollowupRationale(BaseModel):
    """Structural shape of the ``verdict_followup_rationale:`` frontmatter field.

    Per D-IH-86-CX, when a UAT report carries ``verdict: PASS-WITH-FOLLOWUP``,
    the paired ``verdict_followup_rationale:`` field MUST conform to this
    model. The model accepts both YAML dict shape (canonical going forward)
    and YAML string shape (legacy, soft-parsed via
    ``parse_followup_rationale`` helper — string-shape carries empty class
    field and triggers PWF-FM-01 finding to nudge the author toward the dict
    shape).

    The model is intentionally permissive at field-presence level — most
    fields are optional — because the **validator** (not the model) enforces
    the conditional requirements per class. This keeps the model usable for
    partial-parse scenarios (legacy strings) without throwing at construction
    time.

    Worked examples per the 5-class enum live in the paired skill
    ``.cursor/skills/pwf-governance-craft/SKILL.md``.
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    followup_class: (
        Literal[
            "monitoring-obligation",
            "deferred-work-with-tracker",
            "convention-class-followup",
            "mechanical-recovery-with-eta",
            "escalation-to-blocker-tracker",
        ]
        | None
    ) = Field(
        default=None,
        description=(
            "One of the 5-class enum per D-IH-86-CX §3. None on the model "
            "signals a parse failure or legacy free-text rationale; the "
            "validator emits PWF-FM-01-CLASS-MISSING in that case."
        ),
    )
    closure_target: str | None = Field(
        default=None,
        max_length=128,
        description=(
            "Free-text closure target. Common shapes (validator soft-checks "
            "via CLOSURE_TARGET_PATTERN regex): 'Wave-X close' / "
            "'YYYY-MM-DD' / 'OPS-NN-N closed' / 'D-IH-NN-X' / "
            "'I-NN P-N entry' / 'FTW-CODE closes'. Required for most "
            "classes (REQUIRED_CLOSURE_TARGET_CLASSES); optional for none "
            "currently (all 5 classes require a target — but model stays "
            "permissive for partial-parse)."
        ),
    )
    owner: str | None = Field(
        default=None,
        max_length=128,
        description=(
            "Named role or AIC accountable for the followup. Role names "
            "come from baseline_organisation.csv role_name column. AIC "
            "shape is 'AIC:<role>' per the agentic-doctrine convention. "
            "Missing owner triggers PWF-FM-05-OWNER-MISSING at WARN "
            "severity (advisory, not blocking)."
        ),
    )
    tracker_path: str | None = Field(
        default=None,
        max_length=512,
        description=(
            "Repo-root-relative POSIX path to the followup tracker file. "
            "Typically under docs/wip/planning/_trackers/ for "
            "deferred-work-with-tracker class OR under "
            "docs/wip/planning/_blockers/ for escalation-to-blocker-tracker "
            "class. Required for REQUIRED_TRACKER_PATH_CLASSES. Existence "
            "checked at validator runtime; missing file triggers "
            "PWF-FM-04-TRACKER-PATH-INVALID at FAIL severity."
        ),
    )
    closure_decision_id_target: str | None = Field(
        default=None,
        pattern=r"^D-IH-\d+-[A-Z0-9_]+$",
        min_length=8,
        max_length=64,
        description=(
            "Optional DECISION_REGISTER.csv slot reserved for the closure "
            "ratification. When known at PWF authoring time, citing the "
            "slot inline makes the closure trail bidirectional. Pattern "
            "matches the standard D-IH-NN-<letter(s)> shape."
        ),
    )
    notes: str = Field(
        default="",
        max_length=2048,
        description=(
            "Free-text context. For legacy string-rationale carry-over: "
            "the original rationale prose lands here when "
            "parse_followup_rationale soft-coerces a string into a dict "
            "with class=None + this notes field carrying the prose."
        ),
    )

    @field_validator("closure_target")
    @classmethod
    def _normalise_closure_target(cls, value: str | None) -> str | None:
        """Strip whitespace but don't validate shape here — the regex check is
        a soft validator-side advisory, not a model-time error, because
        permissive parsing of legacy rationales is the explicit design goal.
        """
        if value is None:
            return None
        stripped = value.strip()
        return stripped if stripped else None


class PWFGovernanceFinding(BaseModel):
    """One PWF-governance finding emitted by ``scripts/validate_pwf_governance.py``.

    A clean validator run on a single PASS-WITH-FOLLOWUP report emits zero
    findings. A non-clean run emits one row per gap. Each finding becomes
    one option set in an inline-ratify ``AskQuestion`` at the wave-close
    disposition gate per the canonical's §6.

    Severity mapping (see canonical §4):
    - ``fail``: PWF-FM-01 / PWF-FM-02 / PWF-FM-03 / PWF-FM-04 (tracker-path
      gaps + invalid paths)
    - ``warn``: PWF-FM-05 (owner missing)
    - ``info``: reserved for future ramp (currently no info-only codes)

    Per ``CONTRIBUTING.md`` Python Code Standards: frozen BaseModel +
    ``str_strip_whitespace=True`` + Literal enums for governed columns.
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    finding_code: Literal[
        "PWF-FM-01-CLASS-MISSING",
        "PWF-FM-02-CLASS-UNKNOWN",
        "PWF-FM-03-CLOSURE-TARGET-MISSING",
        "PWF-FM-04-TRACKER-PATH-MISSING",
        "PWF-FM-04-TRACKER-PATH-INVALID",
        "PWF-FM-05-OWNER-MISSING",
    ]
    surface_path: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description=(
            "Repo-root-relative POSIX path of the UAT report (or other "
            "PWF-class artifact) this finding concerns."
        ),
    )
    severity: Literal["info", "warn", "fail"] = Field(
        ...,
        description=(
            "Severity per canonical §4. FAIL blocks closure under strict "
            "mode; WARN surfaces at INFO advisory under default mode."
        ),
    )
    class_observed: str = Field(
        default="",
        max_length=64,
        description=(
            "The followup_class value observed in the rationale (one of the "
            "5 enum values, or 'missing' / 'unknown' / 'legacy-string-"
            "rationale' for special parse cases). Empty for non-class-"
            "specific findings."
        ),
    )
    proposed_remediation: str = Field(
        default="",
        max_length=1024,
        description=(
            "One-line proposed action for the AskQuestion option set at "
            "disposition. Empty acceptable but discouraged."
        ),
    )
    notes: str = Field(
        default="",
        max_length=2048,
        description=(
            "Free-text context for the finding (parse trace, suggested "
            "rationale value, etc.)."
        ),
    )


class PWFGovernanceReport(BaseModel):
    """Aggregate report for one PWF-governance sweep run.

    The validator emits this model from three modes:
    - ``--report <path>``: single-report scope; sweeps one UAT report.
    - ``--wave-closing <wave>``: wave-close-sweep scope; sweeps every UAT
      report whose parent commit landed in the closing wave's window.
    - ``--all``: full-sweep scope; sweeps every closure UAT under
      ``docs/wip/planning/**/reports/uat-*.md`` (forward-only-by-date per
      the UAT_DISCIPLINE watershed 2026-05-19).

    Counts are eagerly computed at construction time (not lazy properties)
    so the JSON artifact carries them directly for downstream agents.

    The ``swept_by`` field records who ran the sweep: 'agent:<chat-uuid>'
    for AC-AUTOMATION path; 'operator' or 'AIC:<role>' for AC-HUMAN path.
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    report_id: str = Field(
        ...,
        pattern=r"^pwf-governance-sweep-\d{4}-\d{2}-\d{2}(-[a-z0-9-]+)?$",
        min_length=28,
        max_length=96,
        description=(
            "Stable slug matching ``pwf-governance-sweep-YYYY-MM-DD`` with "
            "optional ``-<slug>`` suffix for multiple sweeps per day."
        ),
    )
    swept_at: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="ISO date YYYY-MM-DD when the sweep ran.",
    )
    swept_by: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description=(
            "Agent or operator identifier that ran the sweep. AC-AUTOMATION "
            "path: 'agent:<chat-uuid>'; AC-HUMAN path: 'operator' or "
            "'AIC:<role>'."
        ),
    )
    scope: Literal["single-report", "wave-close-sweep", "full-sweep"] = Field(
        ...,
        description=(
            "Sweep scope per canonical §4. single-report is the most common "
            "(authoring-time check on one UAT); wave-close-sweep fires at "
            "wave-close gates; full-sweep is the cadence audit."
        ),
    )
    findings: list[PWFGovernanceFinding] = Field(
        ...,
        description=(
            "All findings emitted across all PWF reports in scope. Empty "
            "list is the PASS case."
        ),
    )
    clean_count: int = Field(
        ..., ge=0, description="Count of clean (zero-finding) reports"
    )
    warn_count: int = Field(
        ..., ge=0, description="Count of WARN-severity findings"
    )
    fail_count: int = Field(
        ..., ge=0, description="Count of FAIL-severity findings"
    )
    total_findings: int = Field(
        ...,
        ge=0,
        description=(
            "Total findings across all severities. The model does not "
            "enforce sum-equality internally; the runbook asserts it at "
            "construction."
        ),
    )


def parse_followup_rationale(
    raw_value: object,
) -> PWFFollowupRationale | None:
    """Soft-parse a frontmatter ``verdict_followup_rationale:`` raw value.

    Accepted shapes:
    - ``None`` → returns None (caller emits PWF-FM-01 when verdict is PWF).
    - ``str`` (legacy free-text rationale) → returns
      ``PWFFollowupRationale(followup_class=None, notes=raw_value)``.
      Caller emits PWF-FM-01-CLASS-MISSING to nudge author toward dict shape.
    - ``dict`` (canonical going forward) → strict-validate against the model;
      returns the constructed model. Unknown keys are silently dropped
      (Pydantic default behaviour); missing optional keys remain None.
    - any other type → returns None (caller emits PWF-FM-01).

    The function NEVER raises — parse failures return None and let the
    validator emit the appropriate finding code with context.
    """
    if raw_value is None:
        return None
    if isinstance(raw_value, str):
        stripped = raw_value.strip()
        if not stripped:
            return None
        return PWFFollowupRationale(followup_class=None, notes=stripped)
    if isinstance(raw_value, dict):
        try:
            payload = {
                key: raw_value.get(key)
                for key in PWF_FOLLOWUP_RATIONALE_FIELDNAMES
                if key in raw_value
            }
            return PWFFollowupRationale(**payload)
        except Exception:
            return None
    return None


def fixture_followup_clean() -> PWFFollowupRationale:
    """Fixture for the runbook's --self-test mode (canonical PASS shape)."""
    return PWFFollowupRationale(
        followup_class="monitoring-obligation",
        closure_target="Wave U close",
        owner="System Owner",
        tracker_path=None,
        closure_decision_id_target=None,
        notes=(
            "3-wave field-test window monitoring obligation per "
            "UAT_DISCIPLINE.md §10 promotion log; observation entries land "
            "at Wave S close, Wave T close, Wave U close."
        ),
    )


def fixture_followup_deferred_work() -> PWFFollowupRationale:
    """Fixture for the deferred-work-with-tracker class."""
    return PWFFollowupRationale(
        followup_class="deferred-work-with-tracker",
        closure_target="2026-06-15",
        owner="System Owner",
        tracker_path="docs/wip/planning/_trackers/example-tracker.md",
        closure_decision_id_target="D-IH-86-CX",
        notes=(
            "Live MCP spot-checks deferred to a follow-up wave when "
            "operator authenticates the relevant vendor MCPs."
        ),
    )


def fixture_finding_fail() -> PWFGovernanceFinding:
    """Fixture for a FAIL-severity finding (PWF-FM-01-CLASS-MISSING)."""
    return PWFGovernanceFinding(
        finding_code="PWF-FM-01-CLASS-MISSING",
        surface_path="docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/uat-wave-r-closure-2026-05-24.md",
        severity="fail",
        class_observed="missing",
        proposed_remediation=(
            "Author verdict_followup_rationale as dict with explicit "
            "followup_class field per D-IH-86-CX 5-class enum."
        ),
        notes=(
            "Detected via PWF governance sweep --report; UAT verdict was "
            "PASS-WITH-FOLLOWUP but rationale was empty/missing."
        ),
    )


def fixture_finding_warn() -> PWFGovernanceFinding:
    """Fixture for a WARN-severity finding (PWF-FM-05-OWNER-MISSING)."""
    return PWFGovernanceFinding(
        finding_code="PWF-FM-05-OWNER-MISSING",
        surface_path="docs/wip/planning/example/reports/uat-example.md",
        severity="warn",
        class_observed="monitoring-obligation",
        proposed_remediation=(
            "Add owner field naming the role or AIC accountable for "
            "monitoring (e.g., 'System Owner' or 'AIC:PMO')."
        ),
        notes="Advisory only; does not block closure under default mode.",
    )


def fixture_report_pass() -> PWFGovernanceReport:
    """Fixture for a clean sweep report (zero findings)."""
    return PWFGovernanceReport(
        report_id="pwf-governance-sweep-2026-05-24-self-test",
        swept_at="2026-05-24",
        swept_by="agent:self-test",
        scope="single-report",
        findings=[],
        clean_count=1,
        warn_count=0,
        fail_count=0,
        total_findings=0,
    )


def fixture_report_mixed() -> PWFGovernanceReport:
    """Fixture for a mixed-severity sweep report (1 fail + 1 warn)."""
    findings = [fixture_finding_fail(), fixture_finding_warn()]
    return PWFGovernanceReport(
        report_id="pwf-governance-sweep-2026-05-24-mixed",
        swept_at="2026-05-24",
        swept_by="agent:self-test",
        scope="wave-close-sweep",
        findings=findings,
        clean_count=0,
        warn_count=1,
        fail_count=1,
        total_findings=2,
    )
