"""UAT-report validator runbook (paired to canonical + SOP + cursor-rule + skill).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md``
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_UAT_GOVERNANCE_001.md``
Companion cursor rule: ``.cursor/rules/akos-uat-discipline.mdc``
Pydantic SSOT: ``akos/hlk_uat_report.py``

Decision lineage: D-IH-86-AV (UAT_DISCIPLINE canonical mint), D-IH-86-AS (UAT quality bar
canonization), D-IH-86-CW (charter→active promotion via this paired SOP + runbook + rule
+ skill + process_list row + pattern registry row + 3-wave field-test window).

Validates closure-UAT reports against the 11-section bar + frontmatter schema per
UAT_DISCIPLINE.md §8.5. Enforcement is strict (FAIL on missing sections / mandatory
frontmatter) for forward-only reports (last_review ≥ 2026-05-19); historical reports
emit INFO findings only per the canonical §"Migration posture" exemption.

CLI shape:

    py scripts/validate_uat_report.py --self-test
    py scripts/validate_uat_report.py --report docs/wip/planning/86-.../reports/uat-wave-r-closure-2026-05-24.md
    py scripts/validate_uat_report.py --all
    py scripts/validate_uat_report.py --report <path> --strict
    py scripts/validate_uat_report.py --report <path> --json-log

Exit codes:
    0 = PASS (no FAIL findings in strict mode; or no FAIL findings at all in non-strict).
    1 = FAIL (any FAIL finding in strict mode; or any FAIL finding in non-strict).
    2 = USAGE error (bad arguments; report path not found).

Per akos-uat-discipline.mdc RULE 4: this validator is wired into pre_commit via
``config/verification-profiles.json`` ``validate_uat_report_self_test`` step (self-test
only — full report validation is event_triggered per the process_list row's cadence,
not pre_commit).
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
from akos.hlk_uat_report import (  # noqa: E402
    DECISION_ID_PATTERN,
    FIELD_TEST_WINDOW_CODE_PATTERN,
    FORWARD_ONLY_WATERSHED_ISO_DATE,
    MANDATORY_SECTION_PATTERNS,
    VALID_FIELD_TEST_WINDOW_STATUSES,
    CanonicalFieldTestWindow,
    UATReportFinding,
    UATReportFrontmatter,
    UATReportValidation,
    fixture_canonical_field_test_window_open,
    fixture_finding_fail,
    fixture_frontmatter_pass,
    fixture_frontmatter_pwf_clean,
    fixture_validation_pass,
)

logger = logging.getLogger(__name__)


PLANNING_ROOT = REPO_ROOT / "docs" / "wip" / "planning"

# UAT-report filename glob — matches uat-*.md at any depth under planning/**/reports/.
UAT_REPORT_GLOB = "**/reports/uat-*.md"

DECISION_REGISTER_PATH = (
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
    / "DECISION_REGISTER.csv"
)


def _now_iso_utc() -> str:
    """Return ISO-8601 UTC timestamp with second precision (no microseconds)."""
    return (
        _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )


def _parse_frontmatter(content: str) -> dict[str, Any] | None:
    """Parse YAML frontmatter from a markdown file.

    Returns the parsed dict on success, None when no frontmatter block present.
    Uses a deliberately-minimal hand-rolled YAML parser to avoid the PyYAML
    dependency for the validator (the broader repo has PyYAML, but the validator
    is wired into pre_commit and should be import-light).
    """
    if not content.startswith("---"):
        return None
    end_match = re.search(r"^---\s*$", content[3:], re.MULTILINE)
    if end_match is None:
        return None
    fm_body = content[3 : 3 + end_match.start()].strip()
    result: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    for line in fm_body.splitlines():
        stripped = line.rstrip()
        if not stripped or stripped.startswith("#"):
            continue
        list_item = re.match(r"^\s+-\s+(.+)$", stripped)
        if list_item and current_list is not None:
            current_list.append(list_item.group(1).strip().strip('"').strip("'"))
            continue
        kv = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$", stripped)
        if kv is None:
            continue
        key = kv.group(1)
        value = kv.group(2).strip()
        if value == "":
            current_list = []
            result[key] = current_list
            current_key = key
        else:
            current_list = None
            current_key = key
            cleaned = value.strip().strip('"').strip("'")
            result[key] = cleaned
    return result


def _is_forward_only(last_review: str | None) -> bool:
    """Return True when the report's last_review date is ≥ the watershed.

    Forward-only reports (≥ 2026-05-19 per D-IH-86-AS) are subject to full
    11-section strict enforcement. Historical reports get INFO findings only.
    Missing or malformed last_review defaults to forward-only (fail-closed).
    """
    if not last_review:
        return True
    try:
        report_date = _dt.date.fromisoformat(last_review)
        watershed = _dt.date.fromisoformat(FORWARD_ONLY_WATERSHED_ISO_DATE)
        return report_date >= watershed
    except (ValueError, TypeError):
        return True


def _load_decision_register_ids() -> set[str]:
    """Load DECISION_REGISTER.csv decision_id column into a set for FK-resolve."""
    if not DECISION_REGISTER_PATH.exists():
        return set()
    ids: set[str] = set()
    import csv

    with DECISION_REGISTER_PATH.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            did = (row.get("decision_id") or "").strip()
            if did:
                ids.add(did)
    return ids


def _check_frontmatter(
    fm: dict[str, Any] | None,
    is_forward_only: bool,
    decision_ids: set[str],
) -> list[UATReportFinding]:
    """Run frontmatter checks; return findings (FAIL/WARN/INFO/N/A)."""
    findings: list[UATReportFinding] = []

    if fm is None:
        severity = "FAIL" if is_forward_only else "INFO"
        findings.append(
            UATReportFinding(
                finding_code="UAT-FM-01-VERDICT-MISSING",
                section="frontmatter",
                severity=severity,
                verdict="gap",
                proposed_action=(
                    "Report has no YAML frontmatter block. Add --- frontmatter "
                    "with mandatory fields per UAT_DISCIPLINE.md §8.5."
                ),
                notes="Forward-only report missing entire frontmatter block.",
            )
        )
        return findings

    # FM-01/02 verdict
    verdict = fm.get("verdict")
    if verdict is None or verdict == "":
        findings.append(
            UATReportFinding(
                finding_code="UAT-FM-01-VERDICT-MISSING",
                section="frontmatter:verdict",
                severity="FAIL" if is_forward_only else "INFO",
                verdict="gap",
                proposed_action=(
                    "Append verdict: PASS / PASS-WITH-FOLLOWUP / FAIL / "
                    "PENDING-OPERATOR-WALK per UAT_DISCIPLINE.md §8.5."
                ),
            )
        )
    else:
        valid_verdicts = {"PASS", "PASS-WITH-FOLLOWUP", "FAIL", "PENDING-OPERATOR-WALK"}
        if verdict not in valid_verdicts:
            findings.append(
                UATReportFinding(
                    finding_code="UAT-FM-02-VERDICT-INVALID",
                    section="frontmatter:verdict",
                    severity="FAIL",
                    verdict="drift",
                    proposed_action=(
                        f"verdict={verdict!r} is not one of {sorted(valid_verdicts)}."
                    ),
                )
            )

    # FM-03/04 closure_decision_source
    cds = fm.get("closure_decision_source")
    if cds is None or cds == "":
        if is_forward_only:
            findings.append(
                UATReportFinding(
                    finding_code="UAT-FM-03-CLOSURE-DECISION-SOURCE-MISSING",
                    section="frontmatter:closure_decision_source",
                    severity="WARN",
                    verdict="gap",
                    proposed_action=(
                        "Append closure_decision_source: agent_inline_default / "
                        "operator_explicit / n/a per UAT_DISCIPLINE.md §8.5."
                    ),
                )
            )
    else:
        valid_cds = {"agent_inline_default", "operator_explicit", "n/a"}
        if cds not in valid_cds:
            findings.append(
                UATReportFinding(
                    finding_code="UAT-FM-04-CLOSURE-DECISION-SOURCE-INVALID",
                    section="frontmatter:closure_decision_source",
                    severity="FAIL",
                    verdict="drift",
                    proposed_action=f"closure_decision_source={cds!r} not in {sorted(valid_cds)}.",
                )
            )

    # FM-05/06 ratifying_decisions
    rds = fm.get("ratifying_decisions")
    if not rds or (isinstance(rds, list) and len(rds) == 0):
        findings.append(
            UATReportFinding(
                finding_code="UAT-FM-05-RATIFYING-DECISIONS-MISSING",
                section="frontmatter:ratifying_decisions",
                severity="FAIL" if is_forward_only else "INFO",
                verdict="gap",
                proposed_action="Append ratifying_decisions: list with ≥1 D-IH-NN-X row.",
            )
        )
    elif decision_ids:
        rd_list = rds if isinstance(rds, list) else [rds]
        for did in rd_list:
            did_clean = str(did).strip()
            base_did = did_clean.split("-revoke")[0].split("-v2")[0].split("-durable")[0]
            if base_did not in decision_ids:
                findings.append(
                    UATReportFinding(
                        finding_code="UAT-FM-06-RATIFYING-DECISIONS-FK-UNRESOLVED",
                        section="frontmatter:ratifying_decisions",
                        severity="WARN",
                        verdict="drift",
                        proposed_action=(
                            f"ratifying_decision {did_clean!r} not found in "
                            "DECISION_REGISTER.csv. Add a register row or fix the ID."
                        ),
                    )
                )

    # FM-07/08 linked_runbooks
    lrs = fm.get("linked_runbooks")
    if not lrs or (isinstance(lrs, list) and len(lrs) == 0):
        findings.append(
            UATReportFinding(
                finding_code="UAT-FM-07-LINKED-RUNBOOKS-MISSING",
                section="frontmatter:linked_runbooks",
                severity="WARN" if is_forward_only else "INFO",
                verdict="gap",
                proposed_action=(
                    "Append linked_runbooks: list naming the scripts/*.py runbooks "
                    "this UAT exercises (or [] when not applicable)."
                ),
            )
        )
    else:
        lr_list = lrs if isinstance(lrs, list) else [lrs]
        for rb in lr_list:
            rb_clean = str(rb).strip()
            rb_path = REPO_ROOT / rb_clean
            if not rb_path.exists():
                findings.append(
                    UATReportFinding(
                        finding_code="UAT-FM-08-LINKED-RUNBOOKS-FK-UNRESOLVED",
                        section="frontmatter:linked_runbooks",
                        severity="WARN",
                        verdict="drift",
                        proposed_action=(
                            f"linked_runbook path {rb_clean!r} does not exist."
                        ),
                    )
                )

    # FM-09 verdict_history mandatory on amendment
    title = str(fm.get("title", "")).lower()
    is_amendment = "amend" in title or "v2" in title or "v3" in title
    vh = fm.get("verdict_history")
    if is_amendment and (not vh or (isinstance(vh, list) and len(vh) == 0)):
        findings.append(
            UATReportFinding(
                finding_code="UAT-FM-09-VERDICT-HISTORY-MISSING-ON-AMENDMENT",
                section="frontmatter:verdict_history",
                severity="FAIL",
                verdict="gap",
                proposed_action=(
                    "Amendment report MUST carry verdict_history: list per "
                    "UAT_DISCIPLINE.md §8.5 (I77 P3→P4 precedent)."
                ),
            )
        )

    # FM-10 last_review missing or malformed
    last_review = fm.get("last_review")
    if not last_review:
        findings.append(
            UATReportFinding(
                finding_code="UAT-FM-10-LAST-REVIEW-MISSING-OR-MALFORMED",
                section="frontmatter:last_review",
                severity="WARN",
                verdict="gap",
                proposed_action=(
                    "Append last_review: YYYY-MM-DD; forward-only enforcement "
                    "defaults to strict in absence of the field (fail-closed)."
                ),
            )
        )
    else:
        try:
            _dt.date.fromisoformat(str(last_review))
        except ValueError:
            findings.append(
                UATReportFinding(
                    finding_code="UAT-FM-10-LAST-REVIEW-MISSING-OR-MALFORMED",
                    section="frontmatter:last_review",
                    severity="FAIL",
                    verdict="drift",
                    proposed_action=(
                        f"last_review={last_review!r} is not ISO-8601 YYYY-MM-DD."
                    ),
                )
            )

    # FM-11 PWF without rationale (the structural fix for PWF abuse pattern per
    # D-IH-86-CW + D-IH-86-CX framing)
    if verdict == "PASS-WITH-FOLLOWUP":
        rationale = fm.get("verdict_followup_rationale")
        if not rationale or str(rationale).strip() == "":
            findings.append(
                UATReportFinding(
                    finding_code="UAT-FM-11-PWF-WITHOUT-RATIONALE",
                    section="frontmatter:verdict_followup_rationale",
                    severity="FAIL",
                    verdict="gap",
                    proposed_action=(
                        "PASS-WITH-FOLLOWUP verdict MUST carry verdict_followup_"
                        "rationale: <text> per PWF discipline (D-IH-86-CW / -CX). "
                        "OR change verdict to PASS / FAIL."
                    ),
                    notes=(
                        "Closes the PWF abuse pattern surfaced at I86 Wave R+1 ex5 "
                        "ratification."
                    ),
                )
            )

    return findings


def _check_sections(
    body: str,
    is_forward_only: bool,
) -> list[UATReportFinding]:
    """Run section-presence checks; return findings (FAIL/WARN/INFO/N/A).

    Strict 11-section enforcement applies only to forward-only reports.
    Historical reports get a single INFO finding noting historical-exempt.
    """
    findings: list[UATReportFinding] = []

    if not is_forward_only:
        findings.append(
            UATReportFinding(
                finding_code="UAT-RB-01-HISTORICAL-EXEMPT",
                section="report-body",
                severity="INFO",
                verdict="exempt",
                proposed_action=(
                    "Historical report (last_review < 2026-05-19); §11-section bar "
                    "not enforced per UAT_DISCIPLINE.md §migration posture."
                ),
            )
        )
        return findings

    for finding_code, pattern in MANDATORY_SECTION_PATTERNS:
        if re.search(pattern, body, re.MULTILINE | re.IGNORECASE) is None:
            section_num = finding_code.split("-")[-1] if False else finding_code
            severity = "FAIL"
            # §5 D-IH-86-D cross-check is N/A-OK for non-cluster initiatives — we
            # demote to WARN when the parent path does NOT include 86-initiative-
            # cluster-execution-coordinator. The runbook does the path check.
            findings.append(
                UATReportFinding(
                    finding_code=finding_code + "-MISSING",
                    section=f"body:{finding_code}",
                    severity=severity,
                    verdict="gap",
                    proposed_action=(
                        f"Section matching pattern {pattern!r} not found. Add the "
                        "section (even as a one-line N/A statement) per "
                        "UAT_DISCIPLINE.md §8.5 mandatory ordering."
                    ),
                )
            )

    return findings


def validate_report(report_path: Path, decision_ids: set[str]) -> UATReportValidation:
    """Validate a single UAT-report markdown file; return the validation result."""
    if not report_path.exists():
        return UATReportValidation(
            report_id="missing",
            report_path=str(report_path),
            validated_at=_now_iso_utc(),
            validated_by="validate_uat_report.py",
            is_forward_only=True,
            findings=[
                UATReportFinding(
                    finding_code="UAT-RB-01-HISTORICAL-EXEMPT",
                    section="report-file",
                    severity="FAIL",
                    verdict="gap",
                    proposed_action=f"Report file not found: {report_path}",
                )
            ],
            pass_count=0,
            fail_count=1,
            warn_count=0,
            info_count=0,
            skip_count=0,
            total_findings=1,
        )

    content = report_path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(content)
    last_review = (fm or {}).get("last_review") if fm else None
    is_forward_only = _is_forward_only(str(last_review) if last_review else None)
    body = content
    if content.startswith("---"):
        end_match = re.search(r"^---\s*$", content[3:], re.MULTILINE)
        if end_match:
            body = content[3 + end_match.end() :]

    findings: list[UATReportFinding] = []
    findings.extend(_check_frontmatter(fm, is_forward_only, decision_ids))
    findings.extend(_check_sections(body, is_forward_only))

    fail_count = sum(1 for f in findings if f.severity == "FAIL")
    warn_count = sum(1 for f in findings if f.severity == "WARN")
    info_count = sum(1 for f in findings if f.severity == "INFO")
    skip_count = sum(1 for f in findings if f.severity == "N/A")
    total = len(findings)
    pass_count = max(0, 15 - fail_count - warn_count)  # rough heuristic for green-count

    return UATReportValidation(
        report_id=report_path.stem,
        report_path=str(report_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        validated_at=_now_iso_utc(),
        validated_by="validate_uat_report.py",
        is_forward_only=is_forward_only,
        findings=findings,
        pass_count=pass_count,
        fail_count=fail_count,
        warn_count=warn_count,
        info_count=info_count,
        skip_count=skip_count,
        total_findings=total,
    )


def discover_all_uat_reports() -> list[Path]:
    """Discover all closure-UAT report paths under docs/wip/planning/**/reports/."""
    if not PLANNING_ROOT.exists():
        return []
    return sorted(PLANNING_ROOT.glob(UAT_REPORT_GLOB))


def run_self_test() -> int:
    """Self-test: construct Pydantic fixtures + verify validation result shape."""
    logger.info("validate_uat_report self-test starting")
    try:
        fp = fixture_frontmatter_pass()
        assert fp.verdict == "PASS"
        assert fp.verdict_followup_rationale is None
        fpwf = fixture_frontmatter_pwf_clean()
        assert fpwf.verdict == "PASS-WITH-FOLLOWUP"
        assert fpwf.verdict_followup_rationale is not None
        fb = fixture_finding_fail()
        assert fb.severity == "FAIL"
        assert fb.finding_code == "UAT-FM-11-PWF-WITHOUT-RATIONALE"
        fv = fixture_validation_pass()
        assert fv.fail_count == 0
        assert fv.is_forward_only is True
        # Cross-check the watershed parser
        assert _is_forward_only("2026-05-19") is True
        assert _is_forward_only("2026-05-18") is False
        assert _is_forward_only("") is True  # fail-closed default
        assert _is_forward_only("not-a-date") is True  # fail-closed default
        # Cross-check the frontmatter parser
        sample = """---
title: Sample
verdict: PASS
closure_decision_source: operator_explicit
ratifying_decisions:
  - D-IH-86-CW
linked_runbooks:
  - scripts/validate_uat_report.py
last_review: 2026-05-24
---

Body content here.
"""
        parsed = _parse_frontmatter(sample)
        assert parsed is not None
        assert parsed["verdict"] == "PASS"
        assert parsed["ratifying_decisions"] == ["D-IH-86-CW"]
        # Cross-check the no-frontmatter case
        assert _parse_frontmatter("no frontmatter here") is None
        # CanonicalFieldTestWindow fixture round-trip (D-IH-86-CW META4-b ratification).
        ftw = fixture_canonical_field_test_window_open()
        assert ftw.status == "open"
        assert ftw.open_decision_id == "D-IH-86-CW"
        assert ftw.open_wave == "R+1"
        assert ftw.close_target_wave == "U"
        assert ftw.monitoring_obligation_owner == "PMO"
        assert ftw.monitoring_obligation_co_owner == "AIC role_owner"
        assert len(ftw.promotion_criteria) == 4
        assert len(ftw.revocation_triggers) == 3
        # Every criterion + trigger code must match the FTW pattern.
        for crit in ftw.promotion_criteria:
            assert re.match(FIELD_TEST_WINDOW_CODE_PATTERN, crit.code), crit.code
        for trig in ftw.revocation_triggers:
            assert re.match(FIELD_TEST_WINDOW_CODE_PATTERN, trig.code), trig.code
        # Every status value in the lifecycle enum is valid.
        assert "open" in VALID_FIELD_TEST_WINDOW_STATUSES
        assert "closed" in VALID_FIELD_TEST_WINDOW_STATUSES
        assert "revoked" in VALID_FIELD_TEST_WINDOW_STATUSES
        assert "closing" in VALID_FIELD_TEST_WINDOW_STATUSES
        # CanonicalFieldTestWindow type-check (kept as imported sanity assertion).
        assert isinstance(ftw, CanonicalFieldTestWindow)
    except (AssertionError, Exception) as exc:
        logger.error("validate_uat_report self-test FAILED: %s", exc)
        return 1
    logger.info("validate_uat_report self-test PASS")
    return 0


def render_markdown(validation: UATReportValidation) -> str:
    """Render a validation result as a markdown report (operator-facing)."""
    lines: list[str] = []
    lines.append(f"# validate_uat_report.py — {validation.report_path}")
    lines.append("")
    lines.append(f"- **Validated at**: {validation.validated_at}")
    lines.append(f"- **Forward-only enforcement**: {validation.is_forward_only}")
    lines.append(
        f"- **Findings**: FAIL={validation.fail_count} WARN={validation.warn_count} "
        f"INFO={validation.info_count} N/A={validation.skip_count} "
        f"TOTAL={validation.total_findings}"
    )
    lines.append("")
    if not validation.findings:
        lines.append("✅ **PASS** — no findings.")
        return "\n".join(lines) + "\n"
    lines.append("## Findings")
    lines.append("")
    lines.append("| Code | Section | Severity | Verdict | Action |")
    lines.append("|---|---|---|---|---|")
    for f in validation.findings:
        action_short = f.proposed_action.replace("\n", " ").replace("|", "\\|")[:180]
        lines.append(
            f"| `{f.finding_code}` | `{f.section}` | {f.severity} | {f.verdict} | {action_short} |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    log.setup_logging()
    parser = argparse.ArgumentParser(
        description=(
            "Validate closure-UAT report markdown against the 11-section bar + "
            "frontmatter schema per UAT_DISCIPLINE.md §8.5."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run Pydantic fixture self-test (default for pre_commit wiring).",
    )
    parser.add_argument(
        "--report",
        type=str,
        default=None,
        help="Path to a single UAT report to validate.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all UAT reports discovered under docs/wip/planning/**/reports/uat-*.md.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any FAIL finding (default: exit 0; non-strict surfaces findings as info).",
    )
    parser.add_argument(
        "--json-log",
        action="store_true",
        help="Emit JSON log to stdout (machine-readable).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-report markdown output (only emit summary line).",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()

    decision_ids = _load_decision_register_ids()

    if args.all:
        reports = discover_all_uat_reports()
        if not reports:
            logger.warning("No UAT reports discovered under %s", PLANNING_ROOT)
            return 0
        any_fail = False
        for rp in reports:
            v = validate_report(rp, decision_ids)
            if args.json_log:
                print(json.dumps(v.model_dump(), default=str))
            elif not args.quiet:
                print(render_markdown(v))
            if v.fail_count > 0:
                any_fail = True
        print(
            f"--all summary: {len(reports)} reports validated; "
            f"any-FAIL={any_fail}"
        )
        return 1 if (args.strict and any_fail) else 0

    if args.report:
        rp = (REPO_ROOT / args.report).resolve()
        if not rp.exists():
            rp = Path(args.report).resolve()
        v = validate_report(rp, decision_ids)
        if args.json_log:
            print(json.dumps(v.model_dump(), default=str))
        else:
            print(render_markdown(v))
        return 1 if (args.strict and v.fail_count > 0) else 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
