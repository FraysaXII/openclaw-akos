"""Cursor rule × skill pairing invariants (D-IH-86-CT / I90 P2f)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from akos.io import REPO_ROOT

FindingSeverity = Literal["FAIL", "WARN", "INFO"]

RULES_DIR_REL = Path(".cursor/rules")
SKILLS_DIR_REL = Path(".cursor/skills")

# Rules where a paired *-craft skill is intentionally absent (drain7 LOW + structural).
EXEMPT_NO_CRAFT_REQUIRED: frozenset[str] = frozenset(
    {
        "akos-operator-communication.mdc",
        "akos-baseline-governance.mdc",
        "akos-rule-router.mdc",
        "akos-mirror-template.mdc",
        "akos-people-discipline-of-disciplines.mdc",
        "akos-madeira-management.mdc",
        "akos-adviser-engagement.mdc",
        "akos-mktops-discipline.mdc",
        "akos-techops-discipline.mdc",
        "akos-dataops-discipline.mdc",
        "akos-holistika-operations.mdc",
        "akos-docs-config-sync.mdc",
        "akos-research-area.mdc",
    }
)

# Non-derivable rule stem → skill folder name (under `.cursor/skills/`).
CRAFT_SLUG_OVERRIDES: dict[str, str] = {
    "akos-inline-ratification.mdc": "inline-ratify-craft",
    "akos-conflict-surfacing-and-blocker-trackers.mdc": "conflict-surfacing-craft",
    "akos-frontend-design.mdc": "impeccable",
    "akos-ux-discipline.mdc": "impeccable",
}

_SKILL_PATH_RE = re.compile(
    r"\.cursor/skills/([a-z0-9-]+)/SKILL\.md",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class RuleSkillFinding:
    code: str
    severity: FindingSeverity
    message: str
    rule_slug: str


@dataclass(frozen=True)
class RuleSkillRow:
    rule_slug: str
    expected_craft_slug: str | None
    craft_exists: bool
    cited_in_rule: bool


def _craft_slug_candidates(rule_slug: str) -> list[str]:
    if rule_slug in CRAFT_SLUG_OVERRIDES:
        return [CRAFT_SLUG_OVERRIDES[rule_slug]]
    if not rule_slug.startswith("akos-") or not rule_slug.endswith(".mdc"):
        return []
    stem = rule_slug[len("akos-") : -len(".mdc")]
    out = [f"{stem}-craft"]
    if stem.endswith("-discipline"):
        out.append(f"{stem[: -len('-discipline')]}-craft")
    return out


def expected_craft_slug_for_rule(
    rule_slug: str,
    available_craft_slugs: frozenset[str] | None = None,
) -> str | None:
    if rule_slug in EXEMPT_NO_CRAFT_REQUIRED:
        return None
    candidates = _craft_slug_candidates(rule_slug)
    if not candidates:
        return None
    if available_craft_slugs is not None:
        for cand in candidates:
            if cand in available_craft_slugs:
                return cand
    return candidates[0]


def craft_skill_path(craft_slug: str, repo_root: Path | None = None) -> Path:
    root = repo_root or REPO_ROOT
    return root / SKILLS_DIR_REL / craft_slug / "SKILL.md"


def cited_craft_slugs_in_rule(text: str) -> set[str]:
    return set(_SKILL_PATH_RE.findall(text))


def list_available_craft_slugs(skills_dir: Path) -> frozenset[str]:
    return frozenset(
        p.name
        for p in skills_dir.iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    )


def load_rule_skill_rows(
    rules_dir: Path | None = None,
    skills_dir: Path | None = None,
    repo_root: Path | None = None,
) -> list[RuleSkillRow]:
    root = repo_root or REPO_ROOT
    rdir = rules_dir or (root / RULES_DIR_REL)
    sdir = skills_dir or (root / SKILLS_DIR_REL)
    available = list_available_craft_slugs(sdir)
    rows: list[RuleSkillRow] = []
    for path in sorted(rdir.glob("akos-*.mdc")):
        slug = path.name
        expected = expected_craft_slug_for_rule(slug, available)
        text = path.read_text(encoding="utf-8-sig")
        cited = cited_craft_slugs_in_rule(text)
        exists = False
        cited_ok = False
        if expected:
            exists = expected in available
            cited_ok = expected in cited
        rows.append(
            RuleSkillRow(
                rule_slug=slug,
                expected_craft_slug=expected,
                craft_exists=exists,
                cited_in_rule=cited_ok or (not expected),
            )
        )
    return rows


def validate_rule_skill_pairing(
    rows: list[RuleSkillRow],
) -> list[RuleSkillFinding]:
    findings: list[RuleSkillFinding] = []
    for row in rows:
        if row.expected_craft_slug is None:
            continue
        if not row.craft_exists:
            findings.append(
                RuleSkillFinding(
                    code="RSP-FM-01-CRAFT-MISSING",
                    severity="WARN",
                    message=(
                        f"expected paired skill "
                        f".cursor/skills/{row.expected_craft_slug}/SKILL.md missing"
                    ),
                    rule_slug=row.rule_slug,
                )
            )
        elif not row.cited_in_rule:
            findings.append(
                RuleSkillFinding(
                    code="RSP-FM-02-CRAFT-NOT-CITED",
                    severity="INFO",
                    message=(
                        f"skill exists but rule body does not cite "
                        f".cursor/skills/{row.expected_craft_slug}/SKILL.md"
                    ),
                    rule_slug=row.rule_slug,
                )
            )
    return findings


def fixture_rows_all_paired() -> list[RuleSkillRow]:
    """Synthetic row set for self-test."""
    return [
        RuleSkillRow(
            "akos-uat-discipline.mdc",
            "uat-discipline-craft",
            True,
            True,
        ),
        RuleSkillRow(
            "akos-rule-router.mdc",
            None,
            False,
            True,
        ),
    ]
