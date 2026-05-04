#!/usr/bin/env python3
"""Initiative 55 P6 — Regression artifact diff.

Compare a *current* dossier manifest against the *last-sent* dossier manifest
and emit a structured material-change report. This is the diff side of the
regression-to-advisor loop:

    L3   regression run produces artifact + manifest.json
    --> regression_artifact_diff.py compares vs last-sent baseline
    L4   propose_advisor_update.py reads the diff + threshold POLICY
         --> emit ``proposal-advisor-send-YYYY-MM-DD.md`` (material change)
         --> or append a "no-proposal" row to ``loop-history.md`` (silence)

The diff script does **not** decide whether to propose a send; that lives in
``propose_advisor_update.py``. This script is purely descriptive.

Per **D-IH-55-E** the loop is a both-signal-and-silence telemetry surface:
every regression cycle either produces a proposal or logs a no-proposal row,
so the operator sees both motion and stillness across the loop's lifetime.

Manifest contract (read-only):

The dossier manifest at ``artifacts/uat-dossier/<run-id>/manifest.json`` (or
any operator-curated copy under ``artifacts/dossier-iNN-closure/``) carries:

* ``files``           — per-file ``sha256`` + ``char_count`` / ``byte_count``
* ``section_metrics`` — per-section ``status`` + ``metrics`` dict (judge axes,
                        cost, ship verdict, drift, recovery, …)
* ``filter``          — initiative / persona / skill scope
* ``git_sha``         — repo HEAD at render time
* ``mode`` + ``started_at`` + ``run_id``

The diff script extracts five families of signal:

1. **Cite-counts** — Section 02 ``total_scenarios`` + ``total_personas`` +
   ``total_topics`` + ``total_skills``: registry coverage drift.
2. **Scenario deltas** — Section 04 ``total_scenarios`` +
   ``personas_outside_tolerance_count`` + ``quarantined_scenarios_count``:
   library churn since last send.
3. **Judge-axis movement** — Section 03 + Section 04 ``judge_score_*`` and
   ``judge_axis_fail_*``: did per-axis scores move (pp = percentage points)?
4. **Brand-voice diff** — Section 01 ``light_*`` + Section 03 brand axis +
   ``BRAND_VOICE_FOUNDATION.md`` sha256 if present in manifest extras.
5. **Cost / endpoint posture** — Section 08 endpoint counts + ceiling status,
   from the I52 P5 endpoint-cost surface; useful when a vendor switch
   changes the operator's cost story to the advisor.

Outputs:

* ``--out`` (json, default stdout) — machine-readable diff record.
* ``--md`` (markdown, optional) — human-readable summary; the same payload
  ``propose_advisor_update.py`` ingests via stdin/path.

Usage::

    py scripts/regression_artifact_diff.py \\
        --current artifacts/uat-dossier/dossier-<RUN>/manifest.json \\
        --last-sent artifacts/uat-dossier/last-sent/manifest.json \\
        --out diff.json

    py scripts/regression_artifact_diff.py --current X --last-sent Y --md diff.md

When ``--last-sent`` is missing OR the file does not exist, the diff is
"first-cycle": every metric is reported as ``new``, no baseline numbers, and
``material_change.is_first_cycle = True``. Downstream
``propose_advisor_update.py`` treats first-cycle as a candidate for an
initial advisor send (operator decides per fire).

Exit codes:
  0 — diff written successfully (regardless of whether material change was
      detected; that decision belongs to ``propose_advisor_update.py``)
  1 — usage error (manifest unreadable / malformed)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

SECTION_KEYS = (
    "section_01",
    "section_02",
    "section_03",
    "section_04",
    "section_05",
    "section_06",
    "section_07",
    "section_08",
    "section_09",
    "section_10",
    "section_11",
    "section_12",
)

CITE_COUNT_FIELDS = (
    "total_scenarios",
    "total_personas",
    "total_topics",
    "total_skills",
    "total_policies",
)

SCENARIO_DELTA_FIELDS = (
    "total_scenarios",
    "personas_outside_tolerance_count",
    "quarantined_scenarios_count",
)

JUDGE_AXIS_FIELDS = (
    "judge_score_brand_voice_mean",
    "judge_score_citation_mean",
    "judge_score_persona_fit_mean",
    "judge_axis_fail_brand_voice",
    "judge_axis_fail_citation",
    "judge_axis_fail_persona_fit",
    "judge_worst_axis_fail_count",
)

ENDPOINT_COST_FIELDS = (
    "madeira_endpoint_count",
    "madeira_endpoint_worst_status",
    "madeira_cost_ceiling_status",
    "madeira_cost_total_usd",
    "cost_ceiling_breaches_count",
)

BRAND_VOICE_FIELDS = (
    "light_conversational",
    "light_operator",
    "light_surface",
    "madeira_ship_go",
)


def _load_manifest(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"manifest not found: {path}")
    with path.open(encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except json.JSONDecodeError as exc:
            raise ValueError(f"manifest at {path} is not valid JSON: {exc}") from exc


def _section_metrics(manifest: dict, section_key: str) -> dict:
    sections = manifest.get("section_metrics") or {}
    section = sections.get(section_key) or {}
    metrics = section.get("metrics") or {}
    return metrics if isinstance(metrics, dict) else {}


def _diff_numeric(current: Any, baseline: Any) -> dict:
    """Return a small dict describing the movement.

    ``status`` is one of:
      - "unchanged" — equal (or both None)
      - "new"       — baseline is None / missing, current is not
      - "removed"   — current is None / missing, baseline is not
      - "changed"   — both present, but differ
    """
    if current is None and baseline is None:
        return {"status": "unchanged", "current": None, "baseline": None, "delta": None}
    if baseline is None or baseline == "":
        return {"status": "new", "current": current, "baseline": None, "delta": None}
    if current is None or current == "":
        return {"status": "removed", "current": None, "baseline": baseline, "delta": None}
    if current == baseline:
        return {"status": "unchanged", "current": current, "baseline": baseline, "delta": 0}

    delta: Any = None
    if isinstance(current, (int, float)) and isinstance(baseline, (int, float)):
        delta = current - baseline
    return {"status": "changed", "current": current, "baseline": baseline, "delta": delta}


def _build_field_diff(current_metrics: dict, baseline_metrics: dict, fields: tuple[str, ...]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for field in fields:
        cur = current_metrics.get(field)
        base = baseline_metrics.get(field)
        out[field] = _diff_numeric(cur, base)
    return out


def _summarise_changed_fields(field_diffs: dict[str, dict]) -> dict:
    changed = [k for k, v in field_diffs.items() if v["status"] in ("changed", "new", "removed")]
    return {
        "fields_compared": len(field_diffs),
        "fields_changed": len(changed),
        "changed_field_names": sorted(changed),
    }


def _file_diff(current_files: dict, baseline_files: dict) -> dict:
    """Return changed/added/removed file sets keyed by relative path.

    Each value is a small dict with current sha256, baseline sha256, and a
    ``status`` token from the same vocabulary as ``_diff_numeric``.
    """
    out: dict[str, dict] = {}
    all_paths = set(current_files.keys()) | set(baseline_files.keys())
    for path in sorted(all_paths):
        cur_sha = (current_files.get(path) or {}).get("sha256")
        base_sha = (baseline_files.get(path) or {}).get("sha256")
        if cur_sha is None and base_sha is None:
            continue
        if base_sha is None:
            status = "new"
        elif cur_sha is None:
            status = "removed"
        elif cur_sha == base_sha:
            status = "unchanged"
        else:
            status = "changed"
        out[path] = {
            "status": status,
            "current_sha256": cur_sha,
            "baseline_sha256": base_sha,
        }
    return out


def build_diff_record(
    current_manifest: dict,
    baseline_manifest: dict | None,
    current_path: Path,
    baseline_path: Path | None,
) -> dict:
    """Build the canonical diff record consumed by ``propose_advisor_update.py``.

    Shape (top-level keys):
      - schema_version: int
      - generated_at:   UTC ISO8601
      - is_first_cycle: bool (True when no baseline)
      - current:        {path, run_id, git_sha, mode, started_at}
      - baseline:       same keys (or null when first cycle)
      - cite_counts:    field diffs derived from section 02
      - scenario_deltas:field diffs from section 04
      - judge_axes:     field diffs from sections 03 + 04 (merged; 04 wins)
      - endpoint_cost:  field diffs from section 08
      - brand_voice:    field diffs from section 01
      - files:          per-file sha256 status (new / changed / removed / unchanged)
      - summary:        per-family changed-field counts (operator-readable)

    The "fields_changed" counters in ``summary`` are the canonical input for
    ``POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1`` (I55 P7).
    """

    is_first = baseline_manifest is None
    cur_section_01 = _section_metrics(current_manifest, "section_01")
    cur_section_02 = _section_metrics(current_manifest, "section_02")
    cur_section_03 = _section_metrics(current_manifest, "section_03")
    cur_section_04 = _section_metrics(current_manifest, "section_04")
    cur_section_08 = _section_metrics(current_manifest, "section_08")

    base_section_01 = _section_metrics(baseline_manifest or {}, "section_01")
    base_section_02 = _section_metrics(baseline_manifest or {}, "section_02")
    base_section_03 = _section_metrics(baseline_manifest or {}, "section_03")
    base_section_04 = _section_metrics(baseline_manifest or {}, "section_04")
    base_section_08 = _section_metrics(baseline_manifest or {}, "section_08")

    cite_counts = _build_field_diff(cur_section_02, base_section_02, CITE_COUNT_FIELDS)
    scenario_deltas = _build_field_diff(cur_section_04, base_section_04, SCENARIO_DELTA_FIELDS)
    merged_03_04_current = {**cur_section_03, **cur_section_04}
    merged_03_04_baseline = {**base_section_03, **base_section_04}
    judge_axes = _build_field_diff(merged_03_04_current, merged_03_04_baseline, JUDGE_AXIS_FIELDS)
    endpoint_cost = _build_field_diff(cur_section_08, base_section_08, ENDPOINT_COST_FIELDS)
    brand_voice = _build_field_diff(cur_section_01, base_section_01, BRAND_VOICE_FIELDS)

    files_diff = _file_diff(
        current_manifest.get("files") or {},
        (baseline_manifest or {}).get("files") or {},
    )

    record = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "is_first_cycle": is_first,
        "current": {
            "path": str(current_path),
            "run_id": current_manifest.get("run_id"),
            "git_sha": current_manifest.get("git_sha"),
            "mode": current_manifest.get("mode"),
            "started_at": current_manifest.get("started_at"),
            "filter": current_manifest.get("filter"),
        },
        "baseline": (
            {
                "path": str(baseline_path) if baseline_path else None,
                "run_id": (baseline_manifest or {}).get("run_id"),
                "git_sha": (baseline_manifest or {}).get("git_sha"),
                "mode": (baseline_manifest or {}).get("mode"),
                "started_at": (baseline_manifest or {}).get("started_at"),
                "filter": (baseline_manifest or {}).get("filter"),
            }
            if baseline_manifest is not None
            else None
        ),
        "cite_counts": cite_counts,
        "scenario_deltas": scenario_deltas,
        "judge_axes": judge_axes,
        "endpoint_cost": endpoint_cost,
        "brand_voice": brand_voice,
        "files": files_diff,
    }

    record["summary"] = {
        "cite_counts": _summarise_changed_fields(cite_counts),
        "scenario_deltas": _summarise_changed_fields(scenario_deltas),
        "judge_axes": _summarise_changed_fields(judge_axes),
        "endpoint_cost": _summarise_changed_fields(endpoint_cost),
        "brand_voice": _summarise_changed_fields(brand_voice),
        "files": {
            "files_compared": len(files_diff),
            "files_changed": sum(
                1 for v in files_diff.values() if v["status"] in ("changed", "new", "removed")
            ),
        },
    }
    return record


def render_markdown(record: dict) -> str:
    """Operator-readable summary of the diff record (one screen)."""
    lines: list[str] = []
    lines.append("# Regression artifact diff")
    lines.append("")
    lines.append(f"- generated_at: `{record['generated_at']}`")
    lines.append(f"- first_cycle: `{record['is_first_cycle']}`")
    cur = record["current"]
    lines.append(f"- current: `{cur.get('run_id')}` @ `{cur.get('git_sha')}` ({cur.get('started_at')})")
    base = record.get("baseline")
    if base is not None:
        lines.append(f"- baseline: `{base.get('run_id')}` @ `{base.get('git_sha')}` ({base.get('started_at')})")
    else:
        lines.append("- baseline: *(none — first cycle)*")
    lines.append("")
    lines.append("## Summary (changed-field counts)")
    lines.append("")
    lines.append("| Family | fields_compared | fields_changed |")
    lines.append("|:-------|----------------:|---------------:|")
    for family in ("cite_counts", "scenario_deltas", "judge_axes", "endpoint_cost", "brand_voice"):
        s = record["summary"][family]
        lines.append(f"| {family} | {s['fields_compared']} | {s['fields_changed']} |")
    files_summary = record["summary"]["files"]
    lines.append(f"| files | {files_summary['files_compared']} | {files_summary['files_changed']} |")
    lines.append("")
    lines.append("## Changed fields by family")
    lines.append("")
    for family in ("cite_counts", "scenario_deltas", "judge_axes", "endpoint_cost", "brand_voice"):
        s = record["summary"][family]
        if not s["changed_field_names"]:
            lines.append(f"- **{family}**: *(no change)*")
            continue
        lines.append(f"- **{family}**:")
        for name in s["changed_field_names"]:
            entry = record[family][name]
            status = entry["status"]
            cur_v = entry["current"]
            base_v = entry["baseline"]
            delta = entry.get("delta")
            if status == "changed" and isinstance(delta, (int, float)):
                lines.append(f"  - `{name}`: {base_v} -> {cur_v} (delta = {delta})")
            else:
                lines.append(f"  - `{name}`: {status} — current=`{cur_v}` baseline=`{base_v}`")
    lines.append("")
    files_changed = [p for p, v in record["files"].items() if v["status"] != "unchanged"]
    if files_changed:
        lines.append("## File-level diff (sha256)")
        lines.append("")
        for path in files_changed:
            v = record["files"][path]
            lines.append(f"- `{path}` — {v['status']} (current=`{v['current_sha256']}` baseline=`{v['baseline_sha256']}`)")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--current", required=True, help="Path to current dossier manifest.json")
    parser.add_argument(
        "--last-sent",
        default=None,
        help="Path to last-sent dossier manifest.json. If omitted/missing, diff is first-cycle.",
    )
    parser.add_argument("--out", default=None, help="Output JSON path (default: stdout)")
    parser.add_argument("--md", default=None, help="Optional markdown path (operator-readable summary)")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress stdout JSON when --out is set (avoids duplicate output in pipelines)",
    )
    args = parser.parse_args(argv)

    current_path = Path(args.current)
    try:
        current_manifest = _load_manifest(current_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    baseline_manifest: dict | None
    baseline_path: Path | None
    if args.last_sent:
        baseline_path = Path(args.last_sent)
        if not baseline_path.is_file():
            baseline_manifest = None
            baseline_path = None
        else:
            try:
                baseline_manifest = _load_manifest(baseline_path)
            except ValueError as exc:
                print(f"ERROR: {exc}", file=sys.stderr)
                return 1
    else:
        baseline_manifest = None
        baseline_path = None

    record = build_diff_record(current_manifest, baseline_manifest, current_path, baseline_path)
    payload = json.dumps(record, indent=2, sort_keys=True)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload + "\n", encoding="utf-8")
    if args.md:
        md_path = Path(args.md)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_markdown(record), encoding="utf-8")
    if not (args.out and args.quiet):
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
