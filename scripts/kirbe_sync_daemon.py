#!/usr/bin/env python3
"""KiRBe sync boundary helper — canonical fingerprint + drift evidence (dry-run).

Implements the **dry-run** surface described in
``docs/wip/planning/02-hlk-on-akos-madeira/phase-kirbe-sync-daemons-plan.md``:
fingerprints ``baseline_organisation.csv`` and ``process_list.csv`` under
``docs/references/hlk/compliance/`` without writing to canonical assets.

Authority: canonical HLK CSVs win on conflict (NBT.2 / D-KSD-1).

Usage::

    py scripts/kirbe_sync_daemon.py
    py scripts/kirbe_sync_daemon.py --output path/to/drift.json

Optional apply gate (no mirror writes implemented in-repo)::

    py scripts/kirbe_sync_daemon.py --apply --i-approve-canonical-writes

``--apply`` exits non-zero unless ``KIRBE_SYNC_APPLY=1`` is set in the
environment (explicit operator intent). Automatic canonical or KiRBe
writes remain out of scope here; use approval-gated procedures instead.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.process import run

HLK_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
ORG_CSV = HLK_DIR / "baseline_organisation.csv"
PROC_CSV = HLK_DIR / "process_list.csv"


def _fingerprint(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {"path": str(path), "error": "missing"}
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "sha256": digest,
        "bytes": len(raw),
        "line_count": len(lines),
    }


def build_drift_report(*, run_validate_hlk: bool) -> dict[str, object]:
    """Return a JSON-serializable drift evidence object."""
    report: dict[str, object] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "authority": "canonical_csv_first",
        "fingerprints": {
            "baseline_organisation": _fingerprint(ORG_CSV),
            "process_list": _fingerprint(PROC_CSV),
        },
        "validate_hlk": None,
    }
    if run_validate_hlk:
        r = run([sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk.py")], timeout=300)
        report["validate_hlk"] = {
            "success": r.success,
            "returncode": r.returncode,
            "stderr_tail": (r.stderr or "")[-4000:],
        }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="KiRBe sync drift fingerprint (dry-run)")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Write JSON report to this path (default: stdout)",
    )
    parser.add_argument(
        "--skip-validate-hlk",
        action="store_true",
        help="Do not run scripts/validate_hlk.py as part of the report",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Reserved; requires KIRBE_SYNC_APPLY=1 (no in-repo writes performed)",
    )
    parser.add_argument(
        "--i-approve-canonical-writes",
        action="store_true",
        help="Acknowledge intent to use apply mode (paired with --apply)",
    )
    args = parser.parse_args()

    if args.apply:
        if not args.i_approve_canonical_writes:
            print("Refusing --apply without --i-approve-canonical-writes", file=sys.stderr)
            return 2
        if os.environ.get("KIRBE_SYNC_APPLY") != "1":
            print(
                "Apply mode is not enabled: set KIRBE_SYNC_APPLY=1 after operator approval. "
                "This repository build does not perform KiRBe or canonical CSV writes from this script.",
                file=sys.stderr,
            )
            return 3
        print(
            "KIRBE_SYNC_APPLY=1 acknowledged; no automated mirror or canonical write path is wired here. "
            "Use KiRBe operator workflows and approval-gated CSV tranches.",
            file=sys.stderr,
        )
        return 0

    report = build_drift_report(run_validate_hlk=not args.skip_validate_hlk)
    text = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote drift report to {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
