"""Validator wrapper for baseline-index freshness (Wave N P3 mint).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md``
Paired runbook: ``scripts/baseline_index_sweep.py``
Cursor rule companion: ``.cursor/rules/akos-index-integrity.mdc``

Posture per D-IH-86-CD:

- ``--self-test``  : Pydantic-fixture validation; zero CI cost; always exits 0
                     on PASS. Wired into ``release-gate.py`` +
                     ``pre_commit`` profile.
- (no args)        : run full sweep at sweep_trigger=on_demand; emit summary
                     to stdout; exit 0 (INFO posture during Wave N backfill
                     window per the canonical §5 ramp).
- ``--strict``     : run full sweep; exit non-zero if any drift/gap finding
                     surfaces. Operator-explicit; FAIL ramp lives here.

The validator is intentionally thin — almost all real work lives in
``baseline_index_sweep.py``. This wrapper exists so the release-gate +
verification-profiles surface has the conventional ``validate_*.py`` naming
that downstream tooling expects.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.baseline_index_sweep import run_sweep, self_test  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test", action="store_true",
        help="Pydantic-fixture validation only; zero CI cost; always exit 0 on PASS",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="exit non-zero on any drift/gap finding (FAIL ramp posture)",
    )
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    report = run_sweep(sweep_trigger="on_demand", swept_by="agent:validate")
    print(
        f"validate_index_freshness: total={report.total_findings} "
        f"fresh={report.fresh_count} drift={report.drift_count} "
        f"gap={report.gap_count} blocked={report.blocked_count} "
        f"skip={report.skip_count}"
    )

    if args.strict:
        if report.drift_count or report.gap_count or report.blocked_count:
            print(
                "STRICT MODE FAIL: surfaced drift/gap/blocked findings. "
                "Run `py scripts/baseline_index_sweep.py --check` for the "
                "full report; remediate or escalate per "
                "akos-index-integrity.mdc RULE 3.",
                file=sys.stderr,
            )
            return 1

    return 0  # INFO posture: always exit 0 unless --strict


if __name__ == "__main__":
    sys.exit(main())
