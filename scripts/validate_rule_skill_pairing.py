#!/usr/bin/env python3
"""Validate AKOS cursor rule × skill pairing (D-IH-86-CT / I90 P2f).

``--self-test`` — fixture invariants (pre_commit, INFO ramp).
Default — scan ``.cursor/rules/akos-*.mdc`` vs ``.cursor/skills/*/SKILL.md``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_rule_skill_pairing import (  # noqa: E402
    EXEMPT_NO_CRAFT_REQUIRED,
    load_rule_skill_rows,
    validate_rule_skill_pairing,
    fixture_rows_all_paired,
)


def self_test() -> int:
    findings = validate_rule_skill_pairing(fixture_rows_all_paired())
    if any(f.severity == "FAIL" for f in findings):
        for f in findings:
            print(f"FAIL: {f.code} {f.rule_slug} {f.message}")
        return 1
    print("PASS: rule-skill-pairing self-test")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Treat WARN as exit 1")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()

    rows = load_rule_skill_rows()
    findings = validate_rule_skill_pairing(rows)
    require_craft = [r for r in rows if r.expected_craft_slug]
    paired = sum(1 for r in require_craft if r.craft_exists)
    exempt = len(EXEMPT_NO_CRAFT_REQUIRED)
    print(
        f"rules={len(rows)} require_craft={len(require_craft)} "
        f"paired={paired} exempt={exempt}"
    )
    if not findings:
        print("OVERALL: PASS")
        return 0
    fail = sum(1 for f in findings if f.severity == "FAIL")
    warn = sum(1 for f in findings if f.severity == "WARN")
    for f in findings:
        print(f"{f.severity}: {f.code} [{f.rule_slug}] {f.message}")
    if fail or (args.strict and warn):
        print("OVERALL: FAIL")
        return 1
    print("OVERALL: PASS (INFO/WARN only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
