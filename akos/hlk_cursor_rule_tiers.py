"""Cursor rule tier invariants — SSOT: config/cursor-rule-tiers.json."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from akos.io import REPO_ROOT

FindingSeverity = Literal["FAIL", "WARN", "INFO"]

CONFIG_RELATIVE = Path("config") / "cursor-rule-tiers.json"
RULES_DIR_REL = ".cursor/rules"


@dataclass(frozen=True)
class CursorRuleTiersConfig:
    """Machine-readable tier policy (editable without code changes)."""

    version: int
    ratifying_decision_id: str
    max_always_on_rules: int
    rules_dir: str
    agents_index_path: str
    core_always_on_slugs: frozenset[str]
    active_initiatives_pointer: str


@dataclass(frozen=True)
class RuleTierFinding:
    code: str
    severity: FindingSeverity
    message: str
    rule_slug: str


@dataclass(frozen=True)
class RuleTierRow:
    slug: str
    always_apply: bool
    globs: tuple[str, ...]
    description: str
    line_count: int


_FRONTMATTER_RE = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", re.DOTALL)


def load_cursor_rule_tiers_config(
    repo_root: Path | None = None,
    config_path: Path | None = None,
) -> CursorRuleTiersConfig:
    """Load tier policy from config/cursor-rule-tiers.json."""
    root = repo_root or REPO_ROOT
    path = config_path or (root / CONFIG_RELATIVE)
    if not path.is_file():
        raise FileNotFoundError(f"cursor rule tiers config not found: {path}")
    raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8-sig"))
    slugs = raw.get("core_always_on_slugs")
    if not isinstance(slugs, list) or not slugs:
        raise ValueError("core_always_on_slugs must be a non-empty list")
    return CursorRuleTiersConfig(
        version=int(raw.get("version", 1)),
        ratifying_decision_id=str(raw.get("ratifying_decision_id", "")),
        max_always_on_rules=int(raw.get("max_always_on_rules", 4)),
        rules_dir=str(raw.get("rules_dir", RULES_DIR_REL)),
        agents_index_path=str(raw.get("agents_index_path", "AGENTS.md")),
        core_always_on_slugs=frozenset(str(s) for s in slugs),
        active_initiatives_pointer=str(
            raw.get("active_initiatives_pointer", "docs/wip/planning/README.md")
        ),
    )


def parse_rule_frontmatter(text: str) -> dict[str, object]:
    """Parse minimal YAML frontmatter from an .mdc rule file."""
    text = text.replace("\r\n", "\n")
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    block = match.group(1)
    out: dict[str, object] = {}
    globs: list[str] = []
    in_globs = False
    for line in block.splitlines():
        if line.strip() == "globs:":
            in_globs = True
            continue
        if in_globs:
            if line.startswith("  - "):
                globs.append(line[4:].strip().strip('"').strip("'"))
                continue
            in_globs = False
        if line.startswith("alwaysApply:"):
            out["always_apply"] = line.split(":", 1)[1].strip().lower() == "true"
        elif line.startswith("description:"):
            raw = line.split(":", 1)[1].strip()
            out["description"] = raw.strip('"').strip("'")
    if globs:
        out["globs"] = tuple(globs)
    return out


def load_rule_rows(
    rules_dir: Path | None = None,
    config: CursorRuleTiersConfig | None = None,
) -> list[RuleTierRow]:
    cfg = config or load_cursor_rule_tiers_config()
    base = rules_dir or (REPO_ROOT / cfg.rules_dir)
    rows: list[RuleTierRow] = []
    for path in sorted(base.glob("akos-*.mdc")):
        text = path.read_text(encoding="utf-8-sig")
        meta = parse_rule_frontmatter(text)
        rows.append(
            RuleTierRow(
                slug=path.name,
                always_apply=bool(meta.get("always_apply")),
                globs=tuple(meta.get("globs") or ()),
                description=str(meta.get("description") or ""),
                line_count=len(text.splitlines()),
            )
        )
    return rows


def validate_rule_tiers(
    rows: list[RuleTierRow],
    config: CursorRuleTiersConfig | None = None,
) -> list[RuleTierFinding]:
    cfg = config or load_cursor_rule_tiers_config()
    findings: list[RuleTierFinding] = []
    always_on = [r for r in rows if r.always_apply]
    core = cfg.core_always_on_slugs

    if len(always_on) > cfg.max_always_on_rules:
        findings.append(
            RuleTierFinding(
                code="CRT-FM-01-ALWAYS-ON-COUNT",
                severity="FAIL",
                message=(
                    f"always-on count {len(always_on)} exceeds max "
                    f"{cfg.max_always_on_rules} (config/cursor-rule-tiers.json)"
                ),
                rule_slug="*",
            )
        )

    core_missing = core - {r.slug for r in always_on}
    for slug in sorted(core_missing):
        findings.append(
            RuleTierFinding(
                code="CRT-FM-02-CORE-MISSING",
                severity="FAIL",
                message=f"core always-on rule missing per config: {slug}",
                rule_slug=slug,
            )
        )

    for row in always_on:
        if row.slug not in core and len(always_on) <= cfg.max_always_on_rules:
            findings.append(
                RuleTierFinding(
                    code="CRT-FM-03-NON-CORE-ALWAYS-ON",
                    severity="FAIL",
                    message=(
                        "always-on rule not listed in config "
                        "core_always_on_slugs — add to config or demote"
                    ),
                    rule_slug=row.slug,
                )
            )

    for row in rows:
        if row.always_apply and row.globs:
            findings.append(
                RuleTierFinding(
                    code="CRT-FM-04-ALWAYS-ON-WITH-GLOBS",
                    severity="FAIL",
                    message="alwaysApply:true cannot also declare globs",
                    rule_slug=row.slug,
                )
            )
        if not row.always_apply and not row.globs and not row.description.strip():
            findings.append(
                RuleTierFinding(
                    code="CRT-FM-05-ORPHAN-RULE",
                    severity="WARN",
                    message="non-always-on rule has neither globs nor description (agent-requested)",
                    rule_slug=row.slug,
                )
            )

    return findings


def fixture_rule_rows_minimal() -> list[RuleTierRow]:
    """Minimal valid tier set for self-test (matches default config)."""
    cfg = load_cursor_rule_tiers_config()
    return [
        RuleTierRow(slug, True, (), "core", 40)
        for slug in sorted(cfg.core_always_on_slugs)
    ] + [
        RuleTierRow(
            "akos-uat-discipline.mdc",
            False,
            ("docs/wip/planning/**/reports/uat-*.md",),
            "uat",
            120,
        ),
    ]
