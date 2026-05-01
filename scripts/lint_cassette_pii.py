#!/usr/bin/env python3
"""Initiative 45 P5 — PII linter for cassettes (R-45-4 mitigation).

Scans every cassette JSONL under tests/evals/cassettes/ for real-looking PII
patterns (email, phone, SSN, public IPv4). Synthetic patterns
(``*@example.com``, ``555-01XX``, private IP ranges, common test IPs) are
allowed.

Exit 0 if all clean. Exit 1 if any cassette contains PII findings; prints the
findings for operator review.

Usage::

    py scripts/lint_cassette_pii.py
    py scripts/lint_cassette_pii.py --root tests/evals/cassettes/adversarial
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.eval_harness.adversarial import scan_cassettes_dir_for_pii


def main() -> int:
    parser = argparse.ArgumentParser(description="Cassette PII linter (I45 P5; R-45-4)")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent / "tests" / "evals" / "cassettes"),
        help="Cassette root directory",
    )
    args = parser.parse_args()

    root = Path(args.root)
    print(f"\n  Cassette PII linter (I45 P5)")
    print(f"  Root: {root}")
    print("  " + "=" * 60)

    if not root.is_dir():
        print(f"  SKIP: cassette root not present: {root}")
        return 0

    findings = scan_cassettes_dir_for_pii(root)
    cassette_count = len(list(root.glob("**/*.jsonl")))
    print(f"  Scanned: {cassette_count} cassettes")

    if not findings:
        print("  PASS")
        return 0

    print(f"  FAIL: {len(findings)} cassettes contain real-looking PII")
    for path, items in findings.items():
        rel = path.relative_to(root.parent.parent.parent) if root.parent.parent.parent in path.parents else path
        print(f"    - {rel}")
        for item in items[:5]:
            print(f"        {item}")
        if len(items) > 5:
            print(f"        ... and {len(items) - 5} more")
    print()
    print("  Per R-45-4: cassettes must contain SYNTHETIC data only.")
    print("  - Emails: use *@example.com / *.example.org")
    print("  - Phones: use 555-01XX (IETF reserved fictional range)")
    print("  - IPs: use 127.0.0.1, 0.0.0.0, 1.1.1.1, 8.8.8.8, or private ranges")
    return 1


if __name__ == "__main__":
    sys.exit(main())
