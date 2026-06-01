"""Tests for rule × skill pairing validator."""

from __future__ import annotations

from akos.hlk_rule_skill_pairing import (
    expected_craft_slug_for_rule,
    validate_rule_skill_pairing,
    RuleSkillRow,
    fixture_rows_all_paired,
)


def test_exempt_rules_have_no_expected_craft() -> None:
    assert expected_craft_slug_for_rule("akos-rule-router.mdc") is None
    assert expected_craft_slug_for_rule("akos-baseline-governance.mdc") is None


def test_standard_naming_convention() -> None:
    available = frozenset({"uat-discipline-craft", "impeccable", "inline-ratify-craft"})
    assert (
        expected_craft_slug_for_rule("akos-uat-discipline.mdc", available)
        == "uat-discipline-craft"
    )
    assert expected_craft_slug_for_rule("akos-frontend-design.mdc", available) == "impeccable"
    assert (
        expected_craft_slug_for_rule("akos-inline-ratification.mdc", available)
        == "inline-ratify-craft"
    )


def test_self_test_fixture_passes() -> None:
    assert not [
        f
        for f in validate_rule_skill_pairing(fixture_rows_all_paired())
        if f.severity == "FAIL"
    ]


def test_missing_craft_warns() -> None:
    rows = [
        RuleSkillRow("akos-uat-discipline.mdc", "uat-discipline-craft", False, False),
    ]
    findings = validate_rule_skill_pairing(rows)
    assert any(f.code == "RSP-FM-01-CRAFT-MISSING" for f in findings)
