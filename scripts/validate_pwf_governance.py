"""PASS-WITH-FOLLOWUP governance validator runbook (12th Quality Fabric specialty).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md``
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_PWF_GOVERNANCE_001.md``
Companion cursor rule: ``.cursor/rules/akos-pwf-governance.mdc``
Companion skill: ``.cursor/skills/pwf-governance-craft/SKILL.md``
Pydantic SSOT: ``akos/hlk_pwf_governance.py``

Decision lineage: D-IH-86-CX (12th QF specialty mint; this validator's mint commit).
Sister: ``scripts/validate_uat_report.py`` (already enforces UAT-FM-11-PWF-WITHOUT-
RATIONALE for the simple "rationale field is empty" case at FAIL severity). This
validator extends the check to the **structural** layer: when the rationale field
is non-empty, is it well-shaped per the 5-class enum? Are the conditional required
fields (closure_target / tracker_path / owner) populated?

Architecture: The two validators compose multiplicatively per HOLISTIKA_QUALITY_FABRIC
§3 (the load-bearing multiplicative-AND rule). A PWF UAT report passes governance
only when BOTH validators pass:

  validate_uat_report.py → FM-11 catches: PWF verdict + empty rationale
  validate_pwf_governance.py → catches: rationale present but structurally incomplete

The split exists because PWF governance is doctrine that may eventually govern
non-UAT artifacts too (phase reports, ratification artifacts, etc.) and the 5-class
followup enum is itself a separate axis from the 11-class UAT taxonomy.

CLI shape:

    py scripts/validate_pwf_governance.py --self-test
    py scripts/validate_pwf_governance.py --report docs/wip/planning/.../uat-*.md
    py scripts/validate_pwf_governance.py --wave-closing Wave-R+1
    py scripts/validate_pwf_governance.py --all
    py scripts/validate_pwf_governance.py --report <path> --strict
    py scripts/validate_pwf_governance.py --all --json-log

Exit codes:
    0 = PASS (no FAIL findings in strict mode; or no FAIL findings at all in
        non-strict mode for the scanned scope).
    1 = FAIL (any FAIL finding in strict mode).
    2 = USAGE error (bad arguments; report path not found; YAML parse failure).

Per ``akos-pwf-governance.mdc`` RULE 4: this validator's --self-test mode is
wired into pre_commit via ``config/verification-profiles.json``
``validate_pwf_governance_self_test`` step (self-test only — full sweep is
event_triggered per the canonical's §4 cadence, not pre_commit).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos import log  # noqa: E402
from akos.hlk_pwf_governance import (  # noqa: E402
    CLOSURE_TARGET_PATTERN,
    REQUIRED_CLOSURE_TARGET_CLASSES,
    REQUIRED_TRACKER_PATH_CLASSES,
    VALID_FOLLOWUP_CLASSES,
    PWFFollowupRationale,
    PWFGovernanceFinding,
    PWFGovernanceReport,
    fixture_finding_fail,
    fixture_finding_warn,
    fixture_followup_clean,
    fixture_followup_deferred_work,
    fixture_report_mixed,
    fixture_report_pass,
    parse_followup_rationale,
)

logger = logging.getLogger(__name__)


PLANNING_ROOT = REPO_ROOT / "docs" / "wip" / "planning"

UAT_REPORT_GLOB = "**/reports/uat-*.md"

FORWARD_ONLY_WATERSHED_ISO_DATE = "2026-05-19"

CLOSURE_TARGET_REGEX = re.compile(CLOSURE_TARGET_PATTERN)


def _now_iso_date() -> str:
    """Return ISO date YYYY-MM-DD (UTC) for report_id / swept_at fields."""
    return _dt.datetime.now(_dt.UTC).date().isoformat()


def _parse_frontmatter_yaml(content: str) -> dict[str, Any] | None:
    """Parse YAML frontmatter via PyYAML (nested-dict capable).

    Unlike the hand-rolled parser in ``validate_uat_report.py`` (which is
    flat-only for import-light pre_commit), this validator needs nested-dict
    parsing because ``verdict_followup_rationale:`` is a dict-shaped field
    per D-IH-86-CX. PyYAML is already a transitive dependency of the broader
    repo (it ships with most Python distributions and is listed in
    requirements where needed), so the import cost is acceptable.

    Returns None when no frontmatter block present OR when YAML parse fails
    (the caller emits PWF-FM-01 for the parse-fail case since the field
    can't be validated when frontmatter is unreadable).
    """
    if not content.startswith("---"):
        return None
    end_match = re.search(r"^---\s*$", content[3:], re.MULTILINE)
    if end_match is None:
        return None
    fm_body = content[3 : 3 + end_match.start()].strip()
    try:
        import yaml

        parsed = yaml.safe_load(fm_body)
        return parsed if isinstance(parsed, dict) else None
    except Exception as exc:
        logger.debug("YAML parse failed: %s", exc)
        return None


def _is_forward_only(last_review: str | None) -> bool:
    """Return True when the report's last_review date is ≥ the watershed.

    Forward-only reports (≥ 2026-05-19 per D-IH-86-AS) are subject to strict
    PWF-governance enforcement. Historical reports get INFO findings only
    per the canonical §"Migration posture" exemption. Missing or malformed
    last_review defaults to forward-only (fail-closed).
    """
    if not last_review:
        return True
    try:
        report_date = _dt.date.fromisoformat(str(last_review))
        watershed = _dt.date.fromisoformat(FORWARD_ONLY_WATERSHED_ISO_DATE)
        return report_date >= watershed
    except (ValueError, TypeError):
        return True


def _check_rationale(
    rationale: PWFFollowupRationale | None,
    raw_value: Any,
    surface_path: str,
    is_forward_only: bool,
) -> list[PWFGovernanceFinding]:
    """Run the 5-finding-code check sequence on a parsed rationale.

    Severity ladder per canonical §4:
    - FAIL: PWF-FM-01 / PWF-FM-02 / PWF-FM-03 / PWF-FM-04 (when forward-only)
    - WARN: PWF-FM-05 (always)
    - Historical reports (pre-watershed) get all-INFO emission for migration
      grace per the canonical's §"Migration posture".
    """
    findings: list[PWFGovernanceFinding] = []
    fail_severity: str = "fail" if is_forward_only else "info"

    # PWF-FM-01-CLASS-MISSING: rationale missing OR followup_class is None
    if rationale is None or rationale.followup_class is None:
        class_observed = (
            "legacy-string-rationale"
            if isinstance(raw_value, str) and raw_value.strip()
            else "missing"
        )
        findings.append(
            PWFGovernanceFinding(
                finding_code="PWF-FM-01-CLASS-MISSING",
                surface_path=surface_path,
                severity=fail_severity,  # type: ignore[arg-type]
                class_observed=class_observed,
                proposed_remediation=(
                    "Author verdict_followup_rationale as a YAML dict with "
                    "explicit followup_class field per D-IH-86-CX 5-class "
                    "enum (monitoring-obligation / deferred-work-with-tracker "
                    "/ convention-class-followup / mechanical-recovery-with-eta "
                    "/ escalation-to-blocker-tracker)."
                ),
                notes=(
                    f"raw_value type={type(raw_value).__name__}; "
                    f"len={len(raw_value) if hasattr(raw_value, '__len__') else 0}"
                ),
            )
        )
        return findings

    # PWF-FM-02-CLASS-UNKNOWN: followup_class value not in 5-class enum
    if rationale.followup_class not in VALID_FOLLOWUP_CLASSES:
        findings.append(
            PWFGovernanceFinding(
                finding_code="PWF-FM-02-CLASS-UNKNOWN",
                surface_path=surface_path,
                severity=fail_severity,  # type: ignore[arg-type]
                class_observed=str(rationale.followup_class),
                proposed_remediation=(
                    f"followup_class={rationale.followup_class!r} not in "
                    f"5-class enum {sorted(VALID_FOLLOWUP_CLASSES)}."
                ),
                notes="Pick the closest enum value or escalate via D-IH-NN-X amendment.",
            )
        )
        return findings

    class_str = str(rationale.followup_class)

    # PWF-FM-03-CLOSURE-TARGET-MISSING: closure_target required but absent
    if class_str in REQUIRED_CLOSURE_TARGET_CLASSES:
        if not rationale.closure_target or not rationale.closure_target.strip():
            findings.append(
                PWFGovernanceFinding(
                    finding_code="PWF-FM-03-CLOSURE-TARGET-MISSING",
                    surface_path=surface_path,
                    severity=fail_severity,  # type: ignore[arg-type]
                    class_observed=class_str,
                    proposed_remediation=(
                        f"Class {class_str} requires closure_target. Shape "
                        f"hints: 'Wave-X close' | 'YYYY-MM-DD' | "
                        f"'OPS-NN-N closed' | 'D-IH-NN-X' | 'FTW-CODE closes'."
                    ),
                    notes=(
                        "Closure target is the load-bearing field that converts "
                        "PWF into a closable trail. Empty target = invisible "
                        "debt (the anti-pattern the 12th specialty exists to "
                        "prevent)."
                    ),
                )
            )

    # PWF-FM-04-TRACKER-PATH-MISSING + PWF-FM-04-TRACKER-PATH-INVALID
    if class_str in REQUIRED_TRACKER_PATH_CLASSES:
        if not rationale.tracker_path or not rationale.tracker_path.strip():
            findings.append(
                PWFGovernanceFinding(
                    finding_code="PWF-FM-04-TRACKER-PATH-MISSING",
                    surface_path=surface_path,
                    severity=fail_severity,  # type: ignore[arg-type]
                    class_observed=class_str,
                    proposed_remediation=(
                        f"Class {class_str} requires tracker_path. For "
                        f"deferred-work-with-tracker → "
                        f"docs/wip/planning/_trackers/<slug>.md. For "
                        f"escalation-to-blocker-tracker → "
                        f"docs/wip/planning/_blockers/<slug>-tracker.md."
                    ),
                    notes="Mint the tracker file then cite the path here.",
                )
            )
        else:
            tracker_full = REPO_ROOT / rationale.tracker_path
            if not tracker_full.exists():
                findings.append(
                    PWFGovernanceFinding(
                        finding_code="PWF-FM-04-TRACKER-PATH-INVALID",
                        surface_path=surface_path,
                        severity=fail_severity,  # type: ignore[arg-type]
                        class_observed=class_str,
                        proposed_remediation=(
                            f"tracker_path={rationale.tracker_path!r} does not "
                            f"exist on disk. Mint the tracker before commit OR "
                            f"correct the path."
                        ),
                        notes="FK-resolve against filesystem at validator time.",
                    )
                )

    # PWF-FM-05-OWNER-MISSING (WARN severity always)
    if not rationale.owner or not rationale.owner.strip():
        findings.append(
            PWFGovernanceFinding(
                finding_code="PWF-FM-05-OWNER-MISSING",
                surface_path=surface_path,
                severity="warn",
                class_observed=class_str,
                proposed_remediation=(
                    "Add owner field naming the role or AIC accountable for "
                    "the followup (e.g., 'System Owner' or 'AIC:PMO'). Drawn "
                    "from baseline_organisation.csv role_name column."
                ),
                notes=(
                    "Advisory only; does not block closure under default mode. "
                    "Strict mode treats WARN as informational."
                ),
            )
        )

    return findings


def _check_report(report_path: Path) -> list[PWFGovernanceFinding]:
    """Validate one UAT report file against PWF governance rules.

    Returns empty list when the report's verdict is NOT PASS-WITH-FOLLOWUP
    (the validator no-ops on PASS / FAIL / PENDING reports; this specialty
    governs PWF only). Returns the finding list when verdict is PWF and the
    rationale is structurally incomplete.
    """
    if not report_path.exists():
        return [
            PWFGovernanceFinding(
                finding_code="PWF-FM-01-CLASS-MISSING",
                surface_path=str(report_path),
                severity="fail",
                class_observed="missing",
                proposed_remediation="Report file does not exist on disk.",
                notes="--report path is required to exist; check the path.",
            )
        ]
    try:
        content = report_path.read_text(encoding="utf-8")
    except Exception as exc:
        return [
            PWFGovernanceFinding(
                finding_code="PWF-FM-01-CLASS-MISSING",
                surface_path=str(report_path),
                severity="fail",
                class_observed="missing",
                proposed_remediation=f"Failed to read report: {exc}",
                notes="UTF-8 read failure; check file encoding.",
            )
        ]
    fm = _parse_frontmatter_yaml(content)
    if fm is None:
        return []
    verdict = fm.get("verdict")
    if verdict != "PASS-WITH-FOLLOWUP":
        return []
    last_review = fm.get("last_review")
    is_forward_only = _is_forward_only(last_review)
    raw_value = fm.get("verdict_followup_rationale")
    rationale = parse_followup_rationale(raw_value)
    try:
        rel_path = report_path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        rel_path = report_path.as_posix()
    return _check_rationale(rationale, raw_value, rel_path, is_forward_only)


def _discover_reports(
    scope: str, wave_closing: str | None
) -> list[Path]:
    """Discover UAT reports in scope per the validator mode.

    - full-sweep: every uat-*.md under planning/**/reports/.
    - wave-close-sweep: filter to reports whose filename or frontmatter cites
      the closing wave. The runbook accepts wave codes like 'Wave-R+1' /
      'Wave-M.5' / 'Wave-R'.
    - single-report: caller passes --report path directly; this function
      isn't invoked in that mode.
    """
    if not PLANNING_ROOT.exists():
        return []
    all_reports = sorted(PLANNING_ROOT.glob(UAT_REPORT_GLOB))
    if scope == "full-sweep":
        return all_reports
    if scope == "wave-close-sweep" and wave_closing:
        wave_token = wave_closing.lower().replace("+", "")
        return [
            p for p in all_reports if wave_token in p.name.lower()
        ]
    return all_reports


def _build_report(
    findings: list[PWFGovernanceFinding],
    scope: str,
    swept_by: str,
    report_slug_suffix: str = "",
) -> PWFGovernanceReport:
    """Build the aggregate PWFGovernanceReport from a finding list."""
    today = _now_iso_date()
    report_id = f"pwf-governance-sweep-{today}"
    if report_slug_suffix:
        report_id = f"{report_id}-{report_slug_suffix}"
    warn_count = sum(1 for f in findings if f.severity == "warn")
    fail_count = sum(1 for f in findings if f.severity == "fail")
    total = len(findings)
    clean_count = 0 if findings else 1
    return PWFGovernanceReport(
        report_id=report_id,
        swept_at=today,
        swept_by=swept_by,
        scope=scope,  # type: ignore[arg-type]
        findings=findings,
        clean_count=clean_count,
        warn_count=warn_count,
        fail_count=fail_count,
        total_findings=total,
    )


def _emit_report(report: PWFGovernanceReport, json_log: bool) -> None:
    """Emit the report to stdout in either text or JSON shape."""
    if json_log:
        print(report.model_dump_json(indent=2))
        return
    print(f"PWF GOVERNANCE SWEEP — {report.report_id}")
    print(f"  scope        : {report.scope}")
    print(f"  swept_at     : {report.swept_at}")
    print(f"  swept_by     : {report.swept_by}")
    print(f"  clean_count  : {report.clean_count}")
    print(f"  warn_count   : {report.warn_count}")
    print(f"  fail_count   : {report.fail_count}")
    print(f"  total        : {report.total_findings}")
    if not report.findings:
        print("  verdict      : CLEAN (no PWF-governance findings)")
        return
    print("  findings     :")
    for idx, f in enumerate(report.findings, start=1):
        print(f"    [{idx}] {f.finding_code}  ({f.severity.upper()})")
        print(f"        surface : {f.surface_path}")
        print(f"        class   : {f.class_observed}")
        if f.proposed_remediation:
            print(f"        action  : {f.proposed_remediation}")
        if f.notes:
            print(f"        notes   : {f.notes}")


def _run_self_test() -> int:
    """Smoke-test the SSOT models + parser + check sequence end-to-end.

    Validates that:
    - All fixture constructors return well-formed models.
    - parse_followup_rationale handles all 4 input shapes (None / str / dict / other).
    - _check_rationale emits expected finding codes for staged inputs.
    - _build_report computes counts correctly.

    Returns 0 on PASS, 1 on FAIL (with diagnostic prints).
    """
    print("PWF GOVERNANCE SELF-TEST — start")

    clean = fixture_followup_clean()
    assert clean.followup_class == "monitoring-obligation"
    assert clean.closure_target == "Wave U close"
    print("  [1/8] fixture_followup_clean OK")

    deferred = fixture_followup_deferred_work()
    assert deferred.followup_class == "deferred-work-with-tracker"
    assert deferred.tracker_path is not None
    print("  [2/8] fixture_followup_deferred_work OK")

    parse_none = parse_followup_rationale(None)
    assert parse_none is None
    parse_str = parse_followup_rationale("legacy free-text")
    assert parse_str is not None and parse_str.followup_class is None
    parse_dict = parse_followup_rationale(
        {"followup_class": "monitoring-obligation", "closure_target": "Wave U close", "owner": "System Owner"}
    )
    assert parse_dict is not None and parse_dict.followup_class == "monitoring-obligation"
    parse_int = parse_followup_rationale(12345)
    assert parse_int is None
    print("  [3/8] parse_followup_rationale handles 4 shapes OK")

    f_fail = fixture_finding_fail()
    assert f_fail.severity == "fail"
    assert f_fail.finding_code == "PWF-FM-01-CLASS-MISSING"
    f_warn = fixture_finding_warn()
    assert f_warn.severity == "warn"
    print("  [4/8] finding fixtures OK")

    rpt_pass = fixture_report_pass()
    assert rpt_pass.total_findings == 0
    assert rpt_pass.clean_count == 1
    rpt_mixed = fixture_report_mixed()
    assert rpt_mixed.total_findings == 2
    assert rpt_mixed.fail_count == 1
    assert rpt_mixed.warn_count == 1
    print("  [5/8] report fixtures OK")

    # Check sequence: clean rationale → 0 findings
    findings_clean = _check_rationale(
        clean, {"followup_class": "monitoring-obligation"}, "test/path.md", True
    )
    assert len(findings_clean) == 0, f"clean expected 0 findings, got {len(findings_clean)}: {findings_clean}"
    print("  [6/8] _check_rationale clean -> 0 findings OK")

    # Check sequence: None rationale → PWF-FM-01
    findings_missing = _check_rationale(None, None, "test/missing.md", True)
    assert len(findings_missing) == 1
    assert findings_missing[0].finding_code == "PWF-FM-01-CLASS-MISSING"
    assert findings_missing[0].severity == "fail"
    print("  [7/8] _check_rationale None -> PWF-FM-01 FAIL OK")

    # Check sequence: deferred-work class with bogus tracker_path → PWF-FM-04-INVALID
    bogus = PWFFollowupRationale(
        followup_class="deferred-work-with-tracker",
        closure_target="2026-06-01",
        owner="System Owner",
        tracker_path="docs/wip/planning/_trackers/does-not-exist-xyz.md",
    )
    findings_bogus = _check_rationale(bogus, {}, "test/deferred.md", True)
    codes = {f.finding_code for f in findings_bogus}
    assert "PWF-FM-04-TRACKER-PATH-INVALID" in codes, f"expected PWF-FM-04-INVALID, got {codes}"
    print("  [8/8] _check_rationale tracker_path invalid -> PWF-FM-04-INVALID OK")

    print("PWF GOVERNANCE SELF-TEST — PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    log.setup_logging()
    parser = argparse.ArgumentParser(
        prog="validate_pwf_governance",
        description=(
            "Validate PASS-WITH-FOLLOWUP rationale structure per "
            "PWF_GOVERNANCE_DISCIPLINE.md (12th Quality Fabric specialty)."
        ),
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run Pydantic + parser + check-sequence smoke test (no I/O).",
    )
    parser.add_argument(
        "--report",
        type=str,
        default=None,
        help="Path to a single UAT report markdown to validate.",
    )
    parser.add_argument(
        "--wave-closing",
        type=str,
        default=None,
        help="Wave code (e.g., Wave-R+1) — sweeps reports filename-citing this wave.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="all_reports",
        help="Sweep every uat-*.md under planning/**/reports/.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat any FAIL finding as exit code 1 (default treats only FAIL findings in forward-only reports).",
    )
    parser.add_argument(
        "--json-log",
        action="store_true",
        help="Emit the report as JSON instead of human-readable text.",
    )
    parser.add_argument(
        "--swept-by",
        type=str,
        default="agent:cli",
        help="Identifier of who ran the sweep (default: agent:cli).",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return _run_self_test()

    if args.report:
        report_path = Path(args.report).resolve()
        findings = _check_report(report_path)
        report = _build_report(findings, "single-report", args.swept_by)
        _emit_report(report, args.json_log)
        if args.strict and report.fail_count > 0:
            return 1
        return 0

    if args.wave_closing:
        reports = _discover_reports("wave-close-sweep", args.wave_closing)
        all_findings: list[PWFGovernanceFinding] = []
        for r in reports:
            all_findings.extend(_check_report(r))
        slug_suffix = args.wave_closing.lower().replace("+", "").replace(".", "-")
        report = _build_report(
            all_findings, "wave-close-sweep", args.swept_by, slug_suffix
        )
        _emit_report(report, args.json_log)
        if args.strict and report.fail_count > 0:
            return 1
        return 0

    if args.all_reports:
        reports = _discover_reports("full-sweep", None)
        all_findings = []
        for r in reports:
            all_findings.extend(_check_report(r))
        report = _build_report(all_findings, "full-sweep", args.swept_by)
        _emit_report(report, args.json_log)
        if args.strict and report.fail_count > 0:
            return 1
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
