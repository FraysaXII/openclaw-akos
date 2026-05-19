"""Vault integrity audit per I81 P1.

Paired runbook for the KB integrity baseline matrix per
[`akos-executable-process-catalog.mdc`](.cursor/rules/akos-executable-process-catalog.mdc) RULE 1.
Companion chassis: [`akos/hlk_kb_integrity.py`](akos/hlk_kb_integrity.py).
Sister validator pattern: [`scripts/validate_madeira_mode_parity.py`](scripts/validate_madeira_mode_parity.py).

Walks [`process_list.csv`](docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv)
executable rows (item_granularity in {task, process}) + joins against
[`KNOWLEDGE_PAIRING_REGISTRY.csv`](docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) +
the v3.0 SOP corpus + cadence column. Emits two artifacts:

1. ``reports/i81/kb-integrity-matrix-<YYYY-MM-DD>.csv`` — one row per
   executable item_id with 5 coverage signals + verdict + gap summary.
2. ``reports/i81/kb-integrity-audit-<YYYY-MM-DD>.md`` — narrative + summary
   table + top-gap analysis + next-action routing.

Usage::

    py scripts/audit_kb_integrity.py                       # emit both artifacts under reports/i81/
    py scripts/audit_kb_integrity.py --out-dir <path>      # custom output dir
    py scripts/audit_kb_integrity.py --date 2026-05-19     # override audit date
    py scripts/audit_kb_integrity.py --strict              # exit 1 if pass_rate < threshold (default 95%)
    py scripts/audit_kb_integrity.py --print-summary       # print KbIntegrityAuditSummary as JSON to stdout

Exit codes:
    0 — emit succeeded; pass-rate threshold not enforced unless ``--strict``.
    1 — ``--strict`` and pass_rate < threshold; OR a canonical CSV is missing.
    2 — schema/structure error (e.g. process_list header changed).
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from collections import Counter
from datetime import date as date_cls
from pathlib import Path

from akos.hlk_kb_integrity import (
    ITEM_ID_RE,
    KNOWLEDGE_PAIRING_REL,
    KbIntegrityAuditSummary,
    KbIntegrityMatrixRow,
    PROCESS_LIST_REL,
    SOP_SCAN_ROOT_REL,
    repo_root,
)
from akos.log import setup_logging

LOG = logging.getLogger("audit_kb_integrity")


# Canonical cadence-type vocabulary per akos-executable-process-catalog.mdc RULE 3
# (D-IH-72-Q) — anything outside this set is treated as ``undeclared`` even if non-empty.
CANONICAL_CADENCE_TYPES: frozenset[str] = frozenset(
    {"on_demand", "scheduled", "event_triggered", "gated_operator"}
)


MATRIX_CSV_HEADER: tuple[str, ...] = (
    "item_id",
    "area",
    "role_owner",
    "item_granularity",
    "item_name",
    "knowledge_pairing_status",
    "paired_sop_status",
    "mirror_coverage_status",
    "audience_tags_status",
    "cadence_status",
    "verdict",
    "gap_summary",
)


def _load_process_list(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"process_list.csv missing at {path}")
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    if not rows:
        raise ValueError("process_list.csv is empty")
    required_cols = {"item_id", "item_granularity", "area", "role_owner", "item_name", "cadence_type"}
    missing_cols = required_cols - set(reader.fieldnames or ())
    if missing_cols:
        raise ValueError(f"process_list.csv header missing required columns: {sorted(missing_cols)}")
    return rows


def _load_pairing_item_ids(path: Path) -> set[str]:
    """Return the set of item_ids that appear in KNOWLEDGE_PAIRING_REGISTRY pairings.

    Heuristic per master-roadmap §3 P1 deliverable: an item is considered
    'matched' if its item_id appears as a substring of any pairing_id OR
    parent_doc_path OR companion_doc_paths cell. The registry is small
    (~5-10 rows) so the substring scan is cheap.
    """
    matched: set[str] = set()
    if not path.is_file():
        LOG.warning("KNOWLEDGE_PAIRING_REGISTRY.csv missing at %s; treating all rows as unmatched.", path)
        return matched
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        kp_rows = list(reader)
    return _resolve_item_ids_in_pairing_rows(kp_rows)


def _resolve_item_ids_in_pairing_rows(
    kp_rows: list[dict[str, str]], item_ids: set[str] | None = None
) -> set[str]:
    """Substring-scan helper; testable in isolation.

    When ``item_ids`` is None, the function operates against a fresh scan of
    process_list later. When tests pass a constrained item_id set, the
    function returns the subset that the KP rows reference.
    """
    matched: set[str] = set()
    haystack = " | ".join(
        f"{r.get('pairing_id', '')} | {r.get('parent_doc_path', '')} | {r.get('companion_doc_paths', '')}"
        for r in kp_rows
    )
    if item_ids is None:
        return matched  # caller will re-invoke with item_ids populated
    for iid in item_ids:
        if iid in haystack:
            matched.add(iid)
    return matched


def _scan_v3_sop_corpus_for_item_ids(sop_root: Path, item_ids: set[str]) -> set[str]:
    """Best-effort scan of v3.0 SOP markdown for item_id references.

    Walks every ``SOP-*.md`` file under ``docs/references/hlk/v3.0/**`` and
    records which item_ids appear as substrings in the body. Per master-
    roadmap §6 asset classification: SOPs are canonical surfaces and we
    expect ~50 SOPs total v3.0 (per I80 + I81 P4-P8 retrofit scope), so the
    walk is bounded and cheap. Returns the set of matched item_ids.

    Heuristic note: substring match is intentionally permissive at P1
    baseline. A future commit can promote to FK-style exact match (e.g.,
    SOP frontmatter ``process_item_ids:`` list) when the SOP shape stabilizes.
    """
    matched: set[str] = set()
    if not sop_root.is_dir():
        LOG.warning("v3.0 SOP scan root missing at %s; treating all rows as unmatched.", sop_root)
        return matched
    sop_paths = list(sop_root.rglob("SOP-*.md"))
    for sop_path in sop_paths:
        try:
            text = sop_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            LOG.warning("Skipping unreadable SOP %s: %s", sop_path, exc)
            continue
        for iid in item_ids:
            if iid in matched:
                continue
            if iid in text:
                matched.add(iid)
    LOG.info("v3.0 SOP scan: %d files scanned; %d item_ids matched.", len(sop_paths), len(matched))
    return matched


def build_matrix_rows(
    pl_rows: list[dict[str, str]],
    pairing_matched: set[str],
    sop_matched: set[str],
) -> list[KbIntegrityMatrixRow]:
    """Build matrix rows from process_list + KP + SOP scan signal sets.

    Executable predicate per D-IH-81-F: item_granularity in {task, process}.
    """
    out: list[KbIntegrityMatrixRow] = []
    for r in pl_rows:
        gran = r.get("item_granularity", "").strip()
        if gran not in ("task", "process"):
            continue
        iid = (r.get("item_id") or "").strip()
        if not iid or not ITEM_ID_RE.match(iid):
            LOG.warning("Skipping row with invalid item_id: %r", r.get("item_id"))
            continue
        cadence_raw = (r.get("cadence_type") or "").strip()
        cadence_status = "declared" if cadence_raw in CANONICAL_CADENCE_TYPES else "undeclared"
        kp_status = "matched" if iid in pairing_matched else "unmatched"
        sop_status = "matched" if iid in sop_matched else "unmatched"
        verdict, gap_summary = KbIntegrityMatrixRow.compute_verdict(
            knowledge_pairing_status=kp_status,
            paired_sop_status=sop_status,
            mirror_coverage_status="covered_by_emit",
            audience_tags_status="deferred",
            cadence_status=cadence_status,
        )
        out.append(
            KbIntegrityMatrixRow(
                item_id=iid,
                area=(r.get("area") or "").strip() or "UNKNOWN",
                role_owner=(r.get("role_owner") or "").strip() or "UNKNOWN",
                item_granularity=gran,  # type: ignore[arg-type]
                item_name=(r.get("item_name") or "").strip() or "UNKNOWN",
                knowledge_pairing_status=kp_status,  # type: ignore[arg-type]
                paired_sop_status=sop_status,  # type: ignore[arg-type]
                mirror_coverage_status="covered_by_emit",
                audience_tags_status="deferred",
                cadence_status=cadence_status,  # type: ignore[arg-type]
                verdict=verdict,
                gap_summary=gap_summary,
            )
        )
    return out


def build_summary(
    matrix_rows: list[KbIntegrityMatrixRow],
    matrix_csv_path: str,
    audit_date: str,
    pass_threshold: float = 0.95,
) -> KbIntegrityAuditSummary:
    """Aggregate matrix rows into the audit-level summary."""
    total = len(matrix_rows)
    pass_count = sum(1 for r in matrix_rows if r.verdict == "pass")
    partial_count = sum(1 for r in matrix_rows if r.verdict == "partial")
    fail_count = sum(1 for r in matrix_rows if r.verdict == "fail")
    pass_rate = (pass_count / total) if total else 0.0
    kp_matched = sum(1 for r in matrix_rows if r.knowledge_pairing_status == "matched")
    sop_matched = sum(1 for r in matrix_rows if r.paired_sop_status == "matched")
    audience_deferred = sum(1 for r in matrix_rows if r.audience_tags_status == "deferred")
    cadence_undeclared = sum(1 for r in matrix_rows if r.cadence_status == "undeclared")

    gap_counter: Counter[str] = Counter()
    for r in matrix_rows:
        if r.gap_summary:
            for gap in r.gap_summary.split(";"):
                gap_counter[gap.strip()] += 1

    top_gaps = tuple(f"{gap}({count})" for gap, count in gap_counter.most_common(5))

    return KbIntegrityAuditSummary(
        matrix_csv_path=matrix_csv_path,
        audit_date=audit_date,
        executable_row_count=total,
        pass_count=pass_count,
        partial_count=partial_count,
        fail_count=fail_count,
        pass_rate=pass_rate,
        pass_threshold=pass_threshold,
        meets_threshold=pass_rate >= pass_threshold,
        knowledge_pairing_matched_count=kp_matched,
        paired_sop_matched_count=sop_matched,
        audience_tags_deferred_count=audience_deferred,
        cadence_undeclared_count=cadence_undeclared,
        top_gap_signals=top_gaps,
        notes=(
            "P1 baseline snapshot per D-IH-81-F. audience_tags_status is deferred for every row "
            "pending I85 P1 wire (audience_tags_coverage column join). pass_rate at baseline is "
            "expected to be near-zero because of the audience_tags_deferred floor; the metric "
            "becomes meaningful once that wire lands."
        ),
    )


def write_matrix_csv(matrix_rows: list[KbIntegrityMatrixRow], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(MATRIX_CSV_HEADER)
        for r in matrix_rows:
            writer.writerow(
                [
                    r.item_id,
                    r.area,
                    r.role_owner,
                    r.item_granularity,
                    r.item_name,
                    r.knowledge_pairing_status,
                    r.paired_sop_status,
                    r.mirror_coverage_status,
                    r.audience_tags_status,
                    r.cadence_status,
                    r.verdict,
                    r.gap_summary,
                ]
            )
    LOG.info("Wrote matrix CSV with %d rows to %s", len(matrix_rows), out_path)


def write_audit_narrative(
    summary: KbIntegrityAuditSummary,
    matrix_rows: list[KbIntegrityMatrixRow],
    out_path: Path,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Per-area pass/partial/fail breakdown for the narrative.
    by_area: dict[str, dict[str, int]] = {}
    for r in matrix_rows:
        bucket = by_area.setdefault(r.area, {"pass": 0, "partial": 0, "fail": 0})
        bucket[r.verdict] += 1

    area_rows: list[str] = []
    for area in sorted(by_area):
        counts = by_area[area]
        total = sum(counts.values())
        area_rows.append(
            f"| {area} | {total} | {counts['pass']} | {counts['partial']} | {counts['fail']} |"
        )

    body = f"""---
intellectual_kind: kb_integrity_audit
parent_initiative: INIT-OPENCLAW_AKOS-81
parent_phase: P1
sharing_label: internal_only
authored: {summary.audit_date}
last_review: {summary.audit_date}
linked_decisions:
  - D-IH-81-F  # integrity matrix methodology + PASS threshold (ratified at this phase close)
  - D-IH-81-K  # I81 P1 phase ratification (this commit)
  - D-IH-86-T  # I86 cluster burndown plan (parent context)
status: active
role_owner: PMO
co_owner_role: System Owner
language: en
---

# I81 P1 — KB integrity baseline audit ({summary.audit_date})

> Wave H lane-2 (subagent stream) of the [I86 cluster burndown plan](../../86-initiative-cluster-execution-coordinator/cluster-burndown-plan.md). Authored 2026-05-19 in parallel with parent agent's foreground I76 P2 work. Paired with [`kb-integrity-matrix-{summary.audit_date}.csv`]({Path(summary.matrix_csv_path).name}); see `akos/hlk_kb_integrity.py` for the row + summary schemas.

## §1 Baseline snapshot

| Metric | Value |
|:---|---:|
| Executable rows scanned | **{summary.executable_row_count}** |
| PASS verdict | **{summary.pass_count}** ({summary.pass_count / summary.executable_row_count * 100:.1f}%) |
| PARTIAL verdict | {summary.partial_count} ({summary.partial_count / summary.executable_row_count * 100:.1f}%) |
| FAIL verdict | {summary.fail_count} |
| Pass rate | **{summary.pass_rate * 100:.2f}%** |
| Pass threshold (D-IH-81-F) | {summary.pass_threshold * 100:.0f}% |
| Meets threshold? | {'YES' if summary.meets_threshold else 'NO'} |

## §2 Per-signal coverage

| Signal | Matched / Declared | Total | Coverage |
|:---|---:|---:|---:|
| `knowledge_pairing_status` | {summary.knowledge_pairing_matched_count} | {summary.executable_row_count} | {summary.knowledge_pairing_matched_count / summary.executable_row_count * 100:.2f}% |
| `paired_sop_status` | {summary.paired_sop_matched_count} | {summary.executable_row_count} | {summary.paired_sop_matched_count / summary.executable_row_count * 100:.2f}% |
| `mirror_coverage_status` | {summary.executable_row_count - summary.fail_count} | {summary.executable_row_count} | {(summary.executable_row_count - summary.fail_count) / summary.executable_row_count * 100:.2f}% |
| `audience_tags_status` | {summary.executable_row_count - summary.audience_tags_deferred_count} | {summary.executable_row_count} | {(summary.executable_row_count - summary.audience_tags_deferred_count) / summary.executable_row_count * 100:.2f}% (P1 baseline: deferred for all) |
| `cadence_status` | {summary.executable_row_count - summary.cadence_undeclared_count} | {summary.executable_row_count} | {(summary.executable_row_count - summary.cadence_undeclared_count) / summary.executable_row_count * 100:.2f}% |

## §3 Per-area distribution

| Area | Total | PASS | PARTIAL | FAIL |
|:---|---:|---:|---:|---:|
{chr(10).join(area_rows)}

## §4 Top 5 gap signals (most-frequent shortfalls)

{chr(10).join(f'- `{gap}`' for gap in summary.top_gap_signals) if summary.top_gap_signals else '(no gaps recorded)'}

## §5 Reading guide + caveats (P1 baseline)

The P1 baseline pass-rate is **{summary.pass_rate * 100:.2f}%** — well below the {summary.pass_threshold * 100:.0f}% threshold. This is **expected** and not a regression: the `audience_tags_status` signal is `deferred` for every row at P1, pulling 100% of rows below `pass` on that signal alone. The metric becomes meaningful once two follow-ups land:

1. **I85 audience-tag wire** (I81 P1 follow-up commit): join `audience_tags_status` from `AUDIENCE_REGISTRY.csv` via role_owner → audience tag mapping. When this lands, audience_tags_deferred → audience_tags_matched for every row whose role_owner has a registered audience tag.
2. **I81 P4-P8 SOP body/addendum retrofit waves**: lift `paired_sop_status` from baseline (currently `{summary.paired_sop_matched_count / summary.executable_row_count * 100:.2f}%` matched) toward 70-90% as each area's SOPs land per `pattern_sop_addendum_split`.

The P1 baseline records the **starting point**; P4-P8 record progress against it. P9 closure UAT re-runs this audit and verifies pass_rate ≥ {summary.pass_threshold * 100:.0f}%.

## §6 Next actions (routing)

- **KNOWLEDGE_PAIRING gaps**: {summary.executable_row_count - summary.knowledge_pairing_matched_count} executable rows have no pairing registry entry. Top per-area gaps shipped in the matrix CSV; PMO + per-area role_owner can mint missing pairs as the SOP retrofits land in P4-P8.
- **Paired-SOP gaps**: {summary.executable_row_count - summary.paired_sop_matched_count} executable rows have no detectable v3.0 SOP reference. Per-area retrofit waves (P4 RevOps, P5 Marketing, P6 Tech, P7 Research/Compliance/Ethics, P8 Operations remainder) close these in scoped tranches.
- **Cadence gaps**: {summary.cadence_undeclared_count} executable rows have no `cadence_type` declared per `akos-executable-process-catalog.mdc` RULE 3. The cadence taxonomy is fully expressible; missing rows are operator-side backfill.
- **Audience-tag deferred**: ALL rows. Forward-charter to I81 P1 follow-up wire commit.

## §7 Cross-references

- [I81 master-roadmap](../master-roadmap.md) — P1 phase shape per §3.
- [`kb-integrity-matrix-{summary.audit_date}.csv`]({Path(summary.matrix_csv_path).name}) — row-level data.
- [`akos/hlk_kb_integrity.py`](../../../../akos/hlk_kb_integrity.py) — Pydantic chassis (row + summary models).
- [`scripts/audit_kb_integrity.py`](../../../../scripts/audit_kb_integrity.py) — paired runbook per `akos-executable-process-catalog.mdc` RULE 1.
- [I86 cluster burndown plan §6 Wave H](../../86-initiative-cluster-execution-coordinator/cluster-burndown-plan.md) — parent wave context.
- [`process_list.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv) — executable-row source-of-truth.
- [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) — pairing source-of-truth.
- D-IH-81-F (ratified at this phase close per the methodology + threshold values used above).
- D-IH-81-K (I81 P1 phase ratification — this commit).

## §8 Notes

{summary.notes}
"""
    out_path.write_text(body, encoding="utf-8")
    LOG.info("Wrote audit narrative to %s", out_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/i81/).",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=date_cls.today().isoformat(),
        help="Override audit date (YYYY-MM-DD); default = today.",
    )
    parser.add_argument(
        "--pass-threshold",
        type=float,
        default=0.95,
        help="Pass-rate threshold per D-IH-81-F (default: 0.95).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if pass_rate < threshold (default: emit only).",
    )
    parser.add_argument(
        "--print-summary",
        action="store_true",
        help="Print KbIntegrityAuditSummary as JSON to stdout (does not write files).",
    )
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args()
    setup_logging(json_output=args.json_log)

    root = repo_root()
    pl_path = root / PROCESS_LIST_REL
    kp_path = root / KNOWLEDGE_PAIRING_REL
    sop_root = root / SOP_SCAN_ROOT_REL

    try:
        pl_rows = _load_process_list(pl_path)
    except FileNotFoundError as exc:
        LOG.error(str(exc))
        return 1
    except ValueError as exc:
        LOG.error(str(exc))
        return 2

    # Stage 1: load KP rows then resolve which item_ids they reference.
    kp_rows: list[dict[str, str]] = []
    if kp_path.is_file():
        with kp_path.open(encoding="utf-8", newline="") as fh:
            kp_rows = list(csv.DictReader(fh))
    else:
        LOG.warning("KNOWLEDGE_PAIRING_REGISTRY.csv missing at %s; treating all rows as unmatched.", kp_path)

    executable_iids: set[str] = {
        (r.get("item_id") or "").strip()
        for r in pl_rows
        if r.get("item_granularity", "").strip() in ("task", "process")
        and (r.get("item_id") or "").strip()
    }
    pairing_matched = _resolve_item_ids_in_pairing_rows(kp_rows, executable_iids)

    # Stage 2: scan v3.0 SOPs for item_id references.
    sop_matched = _scan_v3_sop_corpus_for_item_ids(sop_root, executable_iids)

    # Stage 3: build matrix rows + summary.
    matrix_rows = build_matrix_rows(pl_rows, pairing_matched, sop_matched)

    if args.out_dir is None:
        out_dir = (
            root
            / "docs"
            / "wip"
            / "planning"
            / "81-vault-integrity-layout-milestones-retrofit"
            / "reports"
            / "i81"
        )
    else:
        out_dir = args.out_dir

    matrix_csv = out_dir / f"kb-integrity-matrix-{args.date}.csv"
    audit_md = out_dir / f"kb-integrity-audit-{args.date}.md"
    # Use repo-relative path when possible (so the narrative carries portable
    # links); fall back to absolute string when out_dir is outside the repo
    # (e.g. pytest tmp_path).
    try:
        matrix_csv_rel = str(matrix_csv.resolve().relative_to(root.resolve())).replace("\\", "/")
    except ValueError:
        matrix_csv_rel = str(matrix_csv).replace("\\", "/")
    summary = build_summary(matrix_rows, matrix_csv_rel, args.date, args.pass_threshold)

    if args.print_summary:
        print(json.dumps(summary.model_dump(mode="json"), indent=2, sort_keys=True))
        return 0

    write_matrix_csv(matrix_rows, matrix_csv)
    write_audit_narrative(summary, matrix_rows, audit_md)

    LOG.info(
        "KB integrity audit %s — %d rows; pass_rate=%.2f%% (threshold %.0f%%); meets=%s",
        args.date,
        summary.executable_row_count,
        summary.pass_rate * 100,
        summary.pass_threshold * 100,
        summary.meets_threshold,
    )

    if args.strict and not summary.meets_threshold:
        LOG.error("Pass-rate %.2f%% < threshold %.0f%% — strict-mode FAIL.", summary.pass_rate * 100, summary.pass_threshold * 100)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
