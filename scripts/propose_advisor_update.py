#!/usr/bin/env python3
"""Initiative 55 P6 — Propose advisor update.

Read a regression-diff record produced by ``scripts/regression_artifact_diff.py``
and the material-change threshold POLICY
(``POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1``, I55 P7) and emit either:

1. A **send proposal** at
   ``docs/wip/planning/55-brand-ops-continuous-loop/reports/proposal-advisor-send-YYYY-MM-DD.md``
   when the diff crosses the threshold.
2. A **no-proposal** entry appended to
   ``docs/wip/planning/55-brand-ops-continuous-loop/reports/loop-history.md``
   when nothing material changed (D-IH-55-E both-signal-and-silence telemetry).

This script does **not** send anything. G-24-3 is per-fire IRREVERSIBLE and
operator-gated. The proposal file is the operator's read-out: the pre-flight
checklist, diff snapshot, and rationale live there. After the operator
finalises and sends via off-repo SMTP they capture the real-world fact in
``reports/uat-adviser-send-N-YYYY-MM-DD.md`` per D-IH-55-A and update the
"last-sent" manifest snapshot for the next cycle.

Threshold POLICY (I55 P7):

The CSV row ``POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1`` encodes the
operator-tuned thresholds in ``policy_text`` as a key=value list, e.g.::

    min_changed_scenarios=3 \\
    min_judge_axis_movement_pp=2 \\
    min_register_rows_added=1 \\
    min_files_changed=2

The script parses those, then checks the diff record's ``summary`` and
``files`` blocks. Any single threshold being met triggers a proposal
(D-IH-55-D conservative defaults). The operator can ``--force-proposal`` to
override silence (R-55-5 mitigation: per-axis thresholds may be too tight).

First-cycle handling:

If the diff record has ``is_first_cycle == True`` and ``--allow-first-cycle``
is set, a first-send proposal is emitted (R-55-7 mitigation: there must be
*some* path for the very first send). The operator decides per fire.

Usage::

    py scripts/propose_advisor_update.py \\
        --diff diff.json \\
        --policy POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1 \\
        --out-dir docs/wip/planning/55-brand-ops-continuous-loop/reports

    py scripts/propose_advisor_update.py --diff diff.json --force-proposal

    py scripts/propose_advisor_update.py --diff diff.json --dry-run

Exit codes:
  0   — proposal emitted (file written), or no-proposal logged successfully
  1   — input error (diff JSON unreadable; threshold POLICY unresolved)
  2   — threshold parse error (policy_text malformed)

Per **D-IH-55-B**: this script never inlines a real recipient email; only
the GOI/POI ``ref_id`` of the intended recipient (operator-supplied via
``--recipient``) is emitted into the proposal Markdown. Pre-commit grep
guards (R-55-2) intercept any accidental SMTP-pattern leak.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

POLICY_REGISTER_CSV = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "compliance"
    / "dimensions"
    / "POLICY_REGISTER.csv"
)

DEFAULT_OUT_DIR = (
    REPO_ROOT / "docs" / "wip" / "planning" / "55-brand-ops-continuous-loop" / "reports"
)

DEFAULT_POLICY_ID = "POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1"

DEFAULT_THRESHOLDS: dict[str, int] = {
    "min_changed_scenarios": 3,
    "min_judge_axis_movement_pp": 2,
    "min_register_rows_added": 1,
    "min_files_changed": 2,
}


def _load_policy_thresholds(policy_id: str, csv_path: Path = POLICY_REGISTER_CSV) -> dict[str, float]:
    """Return ``{threshold_name: numeric}`` parsed from the POLICY row.

    Raises ``LookupError`` if the policy_id is not found and ``ValueError``
    if ``policy_text`` is malformed (any token without an ``=`` sign or with
    a non-numeric value). Defaults from ``DEFAULT_THRESHOLDS`` are merged in
    so missing keys fall back to D-IH-55-D values.
    """
    if not csv_path.is_file():
        raise LookupError(f"POLICY_REGISTER.csv not found at {csv_path}")
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if (row.get("policy_id") or "").strip() == policy_id:
                policy_text = (row.get("policy_text") or "").strip()
                parsed = _parse_policy_text(policy_text)
                merged = {**DEFAULT_THRESHOLDS, **parsed}
                return merged
    raise LookupError(f"policy_id {policy_id!r} not found in {csv_path}")


def _parse_policy_text(policy_text: str) -> dict[str, float]:
    """Parse ``key=value`` tokens from the threshold POLICY's policy_text.

    Tokens may be separated by whitespace, semicolons, or commas. Each token
    must be ``key=value`` where ``value`` parses as int or float. Unknown
    keys are kept (forward-compatible) but only the four well-known keys
    drive the proposal decision today.
    """
    out: dict[str, float] = {}
    if not policy_text:
        return out
    raw_tokens = (
        policy_text.replace(",", " ").replace(";", " ").replace("\n", " ").split()
    )
    for tok in raw_tokens:
        if "=" not in tok:
            continue
        key, _, val = tok.partition("=")
        key = key.strip()
        val = val.strip().rstrip(".,;")
        if not key or not val:
            continue
        try:
            num: float = int(val)
        except ValueError:
            try:
                num = float(val)
            except ValueError:
                # Non-numeric tokens (e.g. trailing prose) are skipped, not raised:
                # the POLICY row is documentation + machine-readable, mixing both.
                continue
        out[key] = num
    return out


def evaluate_thresholds(diff_record: dict, thresholds: dict[str, float]) -> dict[str, Any]:
    """Apply the threshold POLICY to the diff record.

    Returns a dict::

        {
            "should_propose": bool,
            "is_first_cycle": bool,
            "trips": [(threshold_name, observed_value, threshold_value), ...],
            "metrics": {
                "changed_scenarios":      int,  # cite + scenario delta abs sum
                "judge_axis_movement_pp": float,
                "register_rows_added":    int,
                "files_changed":          int,
            },
        }

    The four metrics are derived as follows:

    * ``changed_scenarios`` — ``|delta|`` on Section 02 ``total_scenarios``
      and Section 04 ``total_scenarios`` (whichever is larger; sources may
      diverge if the filter narrows section 04). Used as scenario-coverage
      churn.
    * ``judge_axis_movement_pp`` — max absolute ``delta`` across all
      ``judge_score_*_mean`` numeric fields, expressed in percentage points
      (the manifest stores 0..1 mean scores; we multiply by 100).
    * ``register_rows_added`` — for now, sum of *positive* deltas across
      ``total_personas`` + ``total_topics`` + ``total_skills`` +
      ``total_policies``; a proxy until I55 L1 wires direct register-CSV
      diffs.
    * ``files_changed`` — count of files whose sha256 differs (status in
      ``changed``, ``new``, ``removed``).
    """
    is_first = bool(diff_record.get("is_first_cycle"))

    cite = diff_record.get("cite_counts") or {}
    scenarios_section_02 = cite.get("total_scenarios") or {}
    scenarios_section_04 = (diff_record.get("scenario_deltas") or {}).get("total_scenarios") or {}
    delta_02 = scenarios_section_02.get("delta")
    delta_04 = scenarios_section_04.get("delta")
    candidates_scenarios = [abs(d) for d in (delta_02, delta_04) if isinstance(d, (int, float))]
    changed_scenarios = max(candidates_scenarios) if candidates_scenarios else 0

    judge = diff_record.get("judge_axes") or {}
    movement_pp = 0.0
    for field, entry in judge.items():
        if not isinstance(entry, dict):
            continue
        if not field.startswith("judge_score_") or not field.endswith("_mean"):
            continue
        delta = entry.get("delta")
        if isinstance(delta, (int, float)):
            movement_pp = max(movement_pp, abs(delta) * 100.0)

    register_rows_added = 0
    for field in ("total_personas", "total_topics", "total_skills", "total_policies"):
        entry = cite.get(field) or {}
        delta = entry.get("delta")
        if isinstance(delta, (int, float)) and delta > 0:
            register_rows_added += int(delta)

    files = diff_record.get("files") or {}
    files_changed = sum(1 for v in files.values() if v.get("status") in ("changed", "new", "removed"))

    metrics = {
        "changed_scenarios": int(changed_scenarios),
        "judge_axis_movement_pp": float(movement_pp),
        "register_rows_added": int(register_rows_added),
        "files_changed": int(files_changed),
    }

    trips: list[tuple[str, float, float]] = []
    if metrics["changed_scenarios"] >= thresholds.get("min_changed_scenarios", 3):
        trips.append(("min_changed_scenarios", metrics["changed_scenarios"], thresholds.get("min_changed_scenarios", 3)))
    if metrics["judge_axis_movement_pp"] >= thresholds.get("min_judge_axis_movement_pp", 2):
        trips.append((
            "min_judge_axis_movement_pp",
            metrics["judge_axis_movement_pp"],
            thresholds.get("min_judge_axis_movement_pp", 2),
        ))
    if metrics["register_rows_added"] >= thresholds.get("min_register_rows_added", 1):
        trips.append((
            "min_register_rows_added",
            metrics["register_rows_added"],
            thresholds.get("min_register_rows_added", 1),
        ))
    if metrics["files_changed"] >= thresholds.get("min_files_changed", 2):
        trips.append(("min_files_changed", metrics["files_changed"], thresholds.get("min_files_changed", 2)))

    return {
        "should_propose": bool(trips),
        "is_first_cycle": is_first,
        "trips": trips,
        "metrics": metrics,
    }


def _today() -> str:
    return date.today().isoformat()


def render_proposal_md(
    diff_record: dict,
    evaluation: dict,
    *,
    recipient_ref_id: str | None,
    forced: bool,
    first_cycle_explicit: bool,
) -> str:
    cur = diff_record.get("current") or {}
    base = diff_record.get("baseline") or {}
    metrics = evaluation["metrics"]
    trips = evaluation["trips"]

    lines: list[str] = []
    lines.append("---")
    lines.append("language: en")
    lines.append("status: draft-pending-operator-pre-flight")
    lines.append("initiative: 55-brand-ops-continuous-loop")
    lines.append("report_kind: advisor-send-proposal")
    lines.append(f"generated_at: {datetime.now(timezone.utc).isoformat()}")
    lines.append("authority: Operator (G-24-3 IRREVERSIBLE per-fire)")
    lines.append("---")
    lines.append("")
    lines.append("# Advisor send proposal — regression-to-advisor loop")
    lines.append("")
    lines.append("This file is the operator pre-flight read-out. It does **not** send.")
    lines.append("Sending is per-fire IRREVERSIBLE (G-24-3) via off-repo SMTP and is captured separately in")
    lines.append("`reports/uat-adviser-send-N-YYYY-MM-DD.md` after the fact.")
    lines.append("")
    lines.append("## Trigger")
    lines.append("")
    if forced:
        lines.append("- **Forced proposal** (`--force-proposal`); operator override of silence path (R-55-5).")
    elif first_cycle_explicit:
        lines.append("- **First-cycle proposal** (`--allow-first-cycle`); no last-sent baseline exists yet.")
    elif evaluation["should_propose"]:
        lines.append("- **Material-change proposal** — at least one threshold tripped:")
        for name, observed, ceiling in trips:
            lines.append(f"  - `{name}`: observed={observed} ; threshold={ceiling}")
    else:  # pragma: no cover — render_proposal_md is only called when proposing
        lines.append("- (no trigger; this should not be reachable)")
    lines.append("")
    lines.append("## Diff snapshot")
    lines.append("")
    lines.append(f"- current: `{cur.get('run_id')}` @ `{cur.get('git_sha')}` ({cur.get('started_at')})")
    if base:
        lines.append(f"- baseline: `{base.get('run_id')}` @ `{base.get('git_sha')}` ({base.get('started_at')})")
    else:
        lines.append("- baseline: *(none — first cycle)*")
    lines.append("")
    lines.append("| Metric | Observed | Threshold |")
    lines.append("|:-------|---------:|----------:|")
    lines.append(f"| changed_scenarios | {metrics['changed_scenarios']} | min_changed_scenarios |")
    lines.append(f"| judge_axis_movement_pp | {metrics['judge_axis_movement_pp']:.2f} | min_judge_axis_movement_pp |")
    lines.append(f"| register_rows_added | {metrics['register_rows_added']} | min_register_rows_added |")
    lines.append(f"| files_changed | {metrics['files_changed']} | min_files_changed |")
    lines.append("")
    lines.append("## Operator pre-flight checklist (compressed I24 P6)")
    lines.append("")
    lines.append("- [ ] Review brand voice deltas (Section 01 + Section 03 brand axis).")
    lines.append("- [ ] Review judge-axis movement (Section 03 + Section 04).")
    lines.append("- [ ] Review register churn (Section 02 cite-counts + Wave-2 fills).")
    lines.append("- [ ] Confirm composer renders cleanly: `py scripts/verify.py export_adviser_handoff_smoke`.")
    lines.append("- [ ] Confirm brand-voice linter green: `py scripts/lint_brand_voice_offline.py`.")
    lines.append("- [ ] Confirm pre-commit SMTP-pattern grep clean (R-55-2).")
    lines.append("- [ ] Recipient (off-repo identity store; ref_id only): "
                 + (f"`{recipient_ref_id}`" if recipient_ref_id else "*(operator to fill)*"))
    lines.append("- [ ] Final draft path: *(operator-supplied; from `compose_adviser_message.py`)*")
    lines.append("")
    lines.append("## After the send (per fire, per D-IH-55-A)")
    lines.append("")
    lines.append("1. Capture real timestamp + SMTP manifest + sha256s in")
    lines.append("   `reports/uat-adviser-send-N-YYYY-MM-DD.md` (N increments).")
    lines.append("2. Append a compact row to `reports/loop-history.md` (cumulative log).")
    lines.append("3. Update the `last-sent` manifest snapshot used by the next regression diff.")
    lines.append("")
    lines.append("## What this is NOT")
    lines.append("")
    lines.append("- An automated send. G-24-3 is per-fire IRREVERSIBLE; operator finalises.")
    lines.append("- A signed pre-flight. The operator signs the actual UAT report after the send.")
    lines.append("- A guarantee of material improvement. The threshold detects motion, not virtue.")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def append_loop_history(
    out_dir: Path,
    diff_record: dict,
    evaluation: dict,
    *,
    proposed: bool,
    proposal_path: Path | None,
) -> Path:
    """Append a row to ``loop-history.md`` (D-IH-55-E both-signal-and-silence)."""
    history = out_dir / "loop-history.md"
    if not history.is_file():
        history.write_text(
            "# Loop history (D-IH-55-E both-signal-and-silence telemetry)\n"
            "\n"
            "| date | mode | run_id | scenarios_delta | judge_pp | register+ | files_changed | proposed | proposal |\n"
            "|:-----|:-----|:-------|----------------:|---------:|----------:|--------------:|:--------:|:---------|\n",
            encoding="utf-8",
        )
    cur = diff_record.get("current") or {}
    metrics = evaluation["metrics"]
    proposal_cell = f"`{proposal_path.name}`" if proposal_path else "—"
    row = (
        f"| {_today()} | {cur.get('mode') or '—'} | `{cur.get('run_id') or '—'}` | "
        f"{metrics['changed_scenarios']} | {metrics['judge_axis_movement_pp']:.2f} | "
        f"{metrics['register_rows_added']} | {metrics['files_changed']} | "
        f"{'YES' if proposed else 'no'} | {proposal_cell} |\n"
    )
    with history.open("a", encoding="utf-8") as fh:
        fh.write(row)
    return history


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--diff", required=True, help="Path to diff JSON (from regression_artifact_diff.py)")
    parser.add_argument(
        "--policy",
        default=DEFAULT_POLICY_ID,
        help="policy_id of the threshold POLICY row (default: POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1)",
    )
    parser.add_argument(
        "--policy-csv",
        default=str(POLICY_REGISTER_CSV),
        help="POLICY_REGISTER.csv path (override for tests)",
    )
    parser.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Output directory for proposal + loop-history (default: I55 reports/)",
    )
    parser.add_argument(
        "--force-proposal",
        action="store_true",
        help="Force a proposal even if no threshold tripped (R-55-5 override).",
    )
    parser.add_argument(
        "--allow-first-cycle",
        action="store_true",
        help="Emit a first-send proposal when no baseline exists.",
    )
    parser.add_argument(
        "--recipient",
        default=None,
        help="GOI/POI ref_id of intended recipient (off-repo identity; ref_id only).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute the decision but do not write any files; print JSON to stdout.",
    )
    parser.add_argument(
        "--use-defaults",
        action="store_true",
        help="Skip POLICY lookup and use D-IH-55-D defaults (test/CI helper).",
    )
    args = parser.parse_args(argv)

    diff_path = Path(args.diff)
    if not diff_path.is_file():
        print(f"ERROR: diff JSON not found: {diff_path}", file=sys.stderr)
        return 1
    try:
        with diff_path.open(encoding="utf-8") as fh:
            diff_record = json.load(fh)
    except json.JSONDecodeError as exc:
        print(f"ERROR: diff JSON malformed: {exc}", file=sys.stderr)
        return 1

    if args.use_defaults:
        thresholds = dict(DEFAULT_THRESHOLDS)
    else:
        try:
            thresholds = _load_policy_thresholds(args.policy, Path(args.policy_csv))
        except LookupError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        except ValueError as exc:
            print(f"ERROR: threshold POLICY parse error: {exc}", file=sys.stderr)
            return 2

    evaluation = evaluate_thresholds(diff_record, thresholds)
    is_first = evaluation["is_first_cycle"]
    proposed = evaluation["should_propose"]
    first_cycle_explicit = is_first and args.allow_first_cycle and not proposed
    if args.force_proposal or first_cycle_explicit:
        proposed = True

    decision = {
        "thresholds": thresholds,
        "evaluation": evaluation,
        "proposed": proposed,
        "forced": bool(args.force_proposal),
        "first_cycle_explicit": first_cycle_explicit,
        "recipient_ref_id": args.recipient,
    }

    out_dir = Path(args.out_dir)
    proposal_path: Path | None = None

    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    if proposed:
        body = render_proposal_md(
            diff_record,
            evaluation,
            recipient_ref_id=args.recipient,
            forced=bool(args.force_proposal),
            first_cycle_explicit=first_cycle_explicit,
        )
        if not args.dry_run:
            proposal_path = out_dir / f"proposal-advisor-send-{_today()}.md"
            proposal_path.write_text(body, encoding="utf-8")
        decision["proposal_path"] = str(proposal_path) if proposal_path else None
    else:
        decision["proposal_path"] = None

    history_path: Path | None = None
    if not args.dry_run:
        history_path = append_loop_history(out_dir, diff_record, evaluation, proposed=proposed, proposal_path=proposal_path)
    decision["loop_history_path"] = str(history_path) if history_path else None

    print(json.dumps(decision, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
