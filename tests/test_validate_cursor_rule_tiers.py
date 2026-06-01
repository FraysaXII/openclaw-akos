"""Tests for cursor rule tier validator."""

from __future__ import annotations

import json
from pathlib import Path

from akos.hlk_cursor_rule_tiers import (
    CONFIG_RELATIVE,
    RuleTierRow,
    load_cursor_rule_tiers_config,
    validate_rule_tiers,
    parse_rule_frontmatter,
)
from akos.io import REPO_ROOT


def test_config_ssot_loads() -> None:
    cfg = load_cursor_rule_tiers_config()
    assert cfg.max_always_on_rules >= len(cfg.core_always_on_slugs)
    assert "akos-rule-router.mdc" in cfg.core_always_on_slugs
    path = REPO_ROOT / CONFIG_RELATIVE
    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    assert raw["ratifying_decision_id"] == "D-IH-90-R"


def test_parse_frontmatter_globs() -> None:
    text = """---
description: Example rule
globs:
  - docs/wip/**
alwaysApply: false
---
# Body
"""
    meta = parse_rule_frontmatter(text)
    assert meta["always_apply"] is False
    assert meta["globs"] == ("docs/wip/**",)


def test_validate_core_always_on_ok() -> None:
    cfg = load_cursor_rule_tiers_config()
    rows = [
        RuleTierRow(slug, True, (), "core", 10)
        for slug in sorted(cfg.core_always_on_slugs)
    ]
    rows.append(
        RuleTierRow(
            "akos-planning-traceability.mdc",
            False,
            ("docs/wip/planning/**",),
            "planning",
            200,
        )
    )
    assert not [f for f in validate_rule_tiers(rows, cfg) if f.severity == "FAIL"]


def test_validate_rejects_always_on_with_globs() -> None:
    cfg = load_cursor_rule_tiers_config()
    rows = [
        RuleTierRow(slug, True, (), "core", 10)
        for slug in sorted(cfg.core_always_on_slugs)
    ]
    rows[0] = RuleTierRow(rows[0].slug, True, ("**/*",), "bad", 10)
    findings = validate_rule_tiers(rows, cfg)
    assert any(f.code == "CRT-FM-04-ALWAYS-ON-WITH-GLOBS" for f in findings)
