#!/usr/bin/env python3
"""Cross-surface evidence-class gate (I90 P4).

Runs initiative-closure cross-checks and self-test fixtures.
Component checks also live in validate_research_action, validate_uat_report,
validate_aic_capability_implementation_matrix (import akos.evidence_class_gate).

Usage:
    py scripts/validate_evidence_class_gate.py --self-test
    py scripts/validate_evidence_class_gate.py
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.evidence_class_gate import (  # noqa: E402
    INITIATIVE_CLOSURE_EVIDENCE_WATERSHED,
    is_on_or_after_watershed,
    load_valid_evidence_classes,
)
from akos.io import REPO_ROOT as AKOS_REPO_ROOT  # noqa: E402

INITIATIVE_CSV = (
    AKOS_REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv"
)
PLANNING_ROOT = AKOS_REPO_ROOT / "docs/wip/planning"


def _parse_uat_frontmatter_verdict_and_evidence(path: Path) -> dict[str, str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {"verdict": None, "evidence_class": None, "evidence_proof_ref": None, "last_review": None}
    end = re.search(r"^---\s*$", text[3:], re.MULTILINE)
    if not end:
        return {"verdict": None, "evidence_class": None, "evidence_proof_ref": None, "last_review": None}
    fm = text[3 : 3 + end.start()]
    out: dict[str, str | None] = {
        "verdict": None,
        "evidence_class": None,
        "evidence_proof_ref": None,
        "last_review": None,
    }
    for line in fm.splitlines():
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$", line.strip())
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip().strip('"').strip("'")
        if key in out:
            out[key] = val or None
    return out


def _find_closure_uat(folder_path: str) -> Path | None:
    rel = (folder_path or "").strip().rstrip("/")
    if not rel:
        return None
    reports = AKOS_REPO_ROOT / rel / "reports"
    if not reports.is_dir():
        return None
    candidates = sorted(reports.glob("uat-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def validate_initiative_closure_evidence() -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not INITIATIVE_CSV.is_file():
        return True, []

    with INITIATIVE_CSV.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    for row in rows:
        status = (row.get("status") or "").strip()
        if status != "closed":
            continue
        closed_at = (row.get("closed_at") or "").strip()
        if not is_on_or_after_watershed(closed_at, INITIATIVE_CLOSURE_EVIDENCE_WATERSHED):
            continue
        iid = row.get("initiative_id", "?")
        uat = _find_closure_uat(row.get("folder_path") or "")
        if uat is None:
            errors.append(f"{iid}: closed_at={closed_at} but no uat-*.md in reports/")
            continue
        meta = _parse_uat_frontmatter_verdict_and_evidence(uat)
        verdict = meta.get("verdict")
        if verdict not in {"PASS", "PASS-WITH-FOLLOWUP"}:
            errors.append(
                f"{iid}: closure UAT {uat.relative_to(AKOS_REPO_ROOT).as_posix()} "
                f"verdict={verdict!r} — cannot close initiative on FAIL/PENDING"
            )
            continue
        ec = meta.get("evidence_class")
        proof = meta.get("evidence_proof_ref")
        lr = meta.get("last_review")
        if is_on_or_after_watershed(lr) and verdict == "PASS":
            if not ec or ec not in load_valid_evidence_classes():
                errors.append(
                    f"{iid}: PASS closure UAT missing valid evidence_class "
                    f"(got {ec!r}); see I90 P4 evidence-class gate"
                )
            if not proof:
                errors.append(
                    f"{iid}: PASS closure UAT missing evidence_proof_ref "
                    f"(path to validator output, probe artifact, or browser bundle)"
                )
            elif not (AKOS_REPO_ROOT / proof).exists() and not proof.startswith("artifacts/"):
                # allow repo-relative paths; warn if missing file
                p = AKOS_REPO_ROOT / proof
                if not p.exists():
                    errors.append(
                        f"{iid}: evidence_proof_ref {proof!r} not found under repo root"
                    )

    return not errors, errors


def self_test() -> int:
    from akos.evidence_class_gate import (  # noqa: E402
        acim_has_evidence_proof,
        is_url_hash_padding,
        parse_acim_evidence_from_notes,
    )

    assert is_url_hash_padding("https://vercel.com/docs/foo#12")
    assert not is_url_hash_padding("https://vercel.com/docs/foo")
    ec, pr = parse_acim_evidence_from_notes("evidence_class=git_shape; evidence_proof_ref=scripts/x.py")
    assert ec == "git_shape" and pr == "scripts/x.py"
    assert acim_has_evidence_proof(
        notes="evidence_class=live_probe; evidence_proof_ref=artifacts/x.json",
        realisation_refs="",
        tool_catalog_ref="",
    )
    print("PASS: evidence-class gate self-test")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()

    ok, errors = validate_initiative_closure_evidence()
    if ok:
        print("PASS: evidence-class gate (initiative closure cross-check)")
        return 0
    print(f"FAIL: evidence-class gate ({len(errors)} findings)")
    for err in errors[:30]:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
