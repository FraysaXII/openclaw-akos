#!/usr/bin/env python3
"""Validate AKOS cursor rule tier invariants (D-IH-90-R).

Policy SSOT: ``config/cursor-rule-tiers.json``.

``--self-test`` — fixture invariants (pre_commit).
Default — scan ``.cursor/rules/akos-*.mdc`` and emit findings table.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_cursor_rule_tiers import (  # noqa: E402
    load_cursor_rule_tiers_config,
    load_rule_rows,
    validate_rule_tiers,
    fixture_rule_rows_minimal,
)


def self_test() -> int:
    cfg = load_cursor_rule_tiers_config()
    findings = validate_rule_tiers(fixture_rule_rows_minimal(), cfg)
    if findings:
        for f in findings:
            print(f"FAIL: {f.code} {f.rule_slug} {f.message}")
        return 1
    print(
        f"PASS: cursor-rule-tiers self-test "
        f"(core={len(cfg.core_always_on_slugs)} max={cfg.max_always_on_rules})"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--rules-dir",
        type=Path,
        default=None,
        help="Directory containing akos-*.mdc rules (default from config)",
    )
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()

    cfg = load_cursor_rule_tiers_config()
    rules_dir = args.rules_dir or (REPO_ROOT / cfg.rules_dir)
    rows = load_rule_rows(rules_dir, cfg)
    findings = validate_rule_tiers(rows, cfg)
    always_on = sum(1 for r in rows if r.always_apply)
    print(f"rules={len(rows)} always_on={always_on} max={cfg.max_always_on_rules}")
    if not findings:
        print("OVERALL: PASS")
        return 0
    fail = sum(1 for f in findings if f.severity == "FAIL")
    for f in findings:
        print(f"{f.severity}: {f.code} [{f.rule_slug}] {f.message}")
    print(f"OVERALL: {'FAIL' if fail else 'PASS'}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
