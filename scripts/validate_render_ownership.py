#!/usr/bin/env python3
"""Validate render-pipeline ownership coverage (I71 P5 Pack A4).

Walks direct-child folders of ``Think Big/Clients/`` and ``Think Big/Advisers/``
(skipping ``_``-prefixed templates / placeholders); enforces per-deliverable
owner-coverage against the WORKSPACE_BLUEPRINT_HOLISTIKA.md §16 canonical 9-row
render-pipeline ownership matrix.

For each engagement folder, the validator inventories deliverables that match
the canonical 9 surface globs (deck / proposal / tarification / Gantt / dossier
/ counterparty-brief / objections / press / advisor-email), parses each
deliverable's frontmatter, and compares the declared ``role_owner`` against
the expected role per the canonical map.

Detection classes (per the §16 discipline; default severity ``warning``
because render-ownership coverage is forward-tracked advisory -- transition
hints don't block CI today; D-IH-71-S ratifies the Pack A4 thresholds):

1. **render-ownership-mismatch** -- deliverable declares ``role_owner:`` but
   the value diverges from the canonical expected role. Default ``warning``;
   per-rule severity override via ``render-ownership-pack.yml``.

2. **render-ownership-undeclared** -- deliverable has no ``role_owner:``
   frontmatter at all. Default ``info``; surfaces as an advisory pointing to
   the canonical mapping so authors can add the missing key.

3. **transition-trigger-hint** (advisory ``info``) -- emitted once per
   validator run when either (a) >= 3 active engagements ship PMO-owned
   deliverables (signals the PMO -> RevOps transition per WORKSPACE §16.3);
   or (b) render-tooling complexity exceeds operator-handled threshold (the
   pack YAML carries operator-curated complexity hints via
   ``transition_trigger_hints``). The hints surface the §16.3 forward-track;
   they never block CI.

Exit codes::

    0 -- no error-severity hits (warnings + info advisories OK); or
         ``--strict-empty`` not set and zero engagement folders found.
    1 -- at least one ``error``-severity hit (operator-promoted via
         ``render-ownership-pack.yml``); or ``--strict-empty`` and no
         engagement roots found.

Cross-references::

    WORKSPACE_BLUEPRINT_HOLISTIKA.md §16 (canonical 9-row render-pipeline
        ownership matrix; per-deliverable role_owner assignment).
    BRAND_GANTT_DISCIPLINE.md §7 (Gantt artifact forward-link to validator).
    BRAND_COUNTERPARTY_README_CONTRACT.md (counterparty-brief pointer pattern).
    akos/brand_voice_register.py (chassis; Pack A4 additive surfaces).
    I71 P5 master-roadmap + initiative-scoped plan §P5 Pack A4.
    D-IH-71-S (Pack A4 ratification; render-ownership coverage thresholds +
        transition-trigger advisory model + chassis-extension verdict).
    D-IH-71-T (Strand B observability cardinality + C-71-5 every-gate-its-own
        -row default applied).
"""

from __future__ import annotations

import argparse
import fnmatch
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.brand_voice_register import (
    DeliverableKind,
    RenderOwnershipPack,
    RenderOwnershipRule,
    Severity,
    parse_render_ownership_pack_yaml,
    parse_render_ownership_rules,
)
from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.render_ownership")

WORKSPACE_BLUEPRINT_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Operations"
    / "PMO"
    / "canonicals"
    / "WORKSPACE_BLUEPRINT_HOLISTIKA.md"
)
DEFAULT_PACK_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Marketing"
    / "Brand"
    / "canonicals"
    / "_validators"
    / "render-ownership-pack.yml"
)
DEFAULT_ENGAGEMENT_ROOTS = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Think Big"
    / "Clients",
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Think Big"
    / "Advisers",
)

# §16.3 transition-trigger threshold (PMO -> RevOps when pipeline >= N active).
PMO_TO_REVOPS_THRESHOLD = 3


# -----------------------------------------------------------------------------
# Frontmatter parsing (intentionally simple; matches Pack A3 pattern)
# -----------------------------------------------------------------------------


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_frontmatter(text: str) -> dict[str, str]:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    out: dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            out[key] = value
    return out


# -----------------------------------------------------------------------------
# Hit type
# -----------------------------------------------------------------------------


@dataclass
class RenderOwnershipHit:
    engagement: Path
    file: Path
    deliverable_kind: str
    rule_id: str
    severity: Severity
    rationale: str


# -----------------------------------------------------------------------------
# Engagement scan helpers
# -----------------------------------------------------------------------------


def _iter_engagements(roots: Iterable[Path]) -> list[Path]:
    out: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for child in sorted(root.iterdir()):
            if not child.is_dir():
                continue
            if child.name.startswith("_"):
                continue
            out.append(child)
    return out


def _find_deliverable_files(
    engagement: Path, rule: RenderOwnershipRule
) -> list[Path]:
    """Resolve the rule's surface glob inside one engagement folder."""
    pattern = rule.surface_pattern
    # Pattern may include subdirectories (e.g., "02-customer-pack/deck.*.md").
    if "/" in pattern:
        subdir, _, filename_glob = pattern.rpartition("/")
        scan_dir = engagement / subdir
    else:
        scan_dir = engagement
        filename_glob = pattern
    if not scan_dir.exists():
        return []
    return [
        p
        for p in sorted(scan_dir.iterdir())
        if p.is_file() and fnmatch.fnmatch(p.name, filename_glob)
    ]


def scan_engagement(
    engagement: Path,
    rules: list[RenderOwnershipRule],
) -> tuple[list[RenderOwnershipHit], dict[DeliverableKind, int]]:
    """Scan one engagement folder; return hits + deliverable-kind cardinalities."""
    hits: list[RenderOwnershipHit] = []
    cardinality: dict[DeliverableKind, int] = {}
    for rule in rules:
        files = _find_deliverable_files(engagement, rule)
        if not files:
            continue
        cardinality[rule.deliverable_kind] = cardinality.get(rule.deliverable_kind, 0) + len(files)
        for path in files:
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                logger.warning("Skipping unreadable deliverable %s: %s", path, exc)
                continue
            fm = _parse_frontmatter(text)
            declared = (fm.get("role_owner") or fm.get("owner") or "").strip()
            if not declared:
                hits.append(
                    RenderOwnershipHit(
                        engagement=engagement,
                        file=path,
                        deliverable_kind=rule.deliverable_kind,
                        rule_id="render-ownership-undeclared",
                        severity="info",
                        rationale=(
                            f"`{path.name}` lacks `role_owner:` frontmatter; "
                            f"WORKSPACE_BLUEPRINT §16 expects "
                            f"`role_owner: {rule.expected_role_owner}` for "
                            f"deliverable_kind={rule.deliverable_kind!r}."
                        ),
                    )
                )
                continue
            if declared.lower() != rule.expected_role_owner.lower():
                hits.append(
                    RenderOwnershipHit(
                        engagement=engagement,
                        file=path,
                        deliverable_kind=rule.deliverable_kind,
                        rule_id="render-ownership-mismatch",
                        severity=rule.default_severity,
                        rationale=(
                            f"`{path.name}` declares `role_owner: "
                            f"{declared!r}` but WORKSPACE_BLUEPRINT §16 maps "
                            f"deliverable_kind={rule.deliverable_kind!r} to "
                            f"`{rule.expected_role_owner}`."
                        ),
                    )
                )
    return hits, cardinality


# -----------------------------------------------------------------------------
# Transition-trigger hints (§16.3 advisory; never blocks)
# -----------------------------------------------------------------------------


def _aggregate_transition_hints(
    cardinality_totals: dict[DeliverableKind, int],
    n_engagements: int,
    pack_hints: tuple[str, ...],
) -> list[RenderOwnershipHit]:
    """Emit §16.3 transition advisories. Never blocks CI."""
    hints: list[RenderOwnershipHit] = []
    pmo_kinds = {"proposal", "tarification", "dossier", "advisor_email"}
    pmo_total = sum(v for k, v in cardinality_totals.items() if k in pmo_kinds)
    if n_engagements >= PMO_TO_REVOPS_THRESHOLD and pmo_total > 0:
        hints.append(
            RenderOwnershipHit(
                engagement=REPO_ROOT,
                file=WORKSPACE_BLUEPRINT_PATH,
                deliverable_kind="proposal",
                rule_id="transition-trigger-pmo-to-revops",
                severity="info",
                rationale=(
                    f"{n_engagements} active engagements detected with "
                    f"{pmo_total} PMO-owned deliverables (>= "
                    f"{PMO_TO_REVOPS_THRESHOLD} engagement threshold per "
                    f"WORKSPACE_BLUEPRINT §16.3 PMO -> RevOps transition "
                    f"drift signal). RevOps activation gated by I72 P4 "
                    f"per D-IH-72-B."
                ),
            )
        )
    for hint in pack_hints:
        hints.append(
            RenderOwnershipHit(
                engagement=REPO_ROOT,
                file=DEFAULT_PACK_PATH,
                deliverable_kind="dossier",
                rule_id="transition-trigger-operator-hint",
                severity="info",
                rationale=(
                    f"Operator-curated transition hint via "
                    f"render-ownership-pack.yml: {hint}"
                ),
            )
        )
    return hints


# -----------------------------------------------------------------------------
# Pack overrides
# -----------------------------------------------------------------------------


def _apply_pack_overrides(
    rules: list[RenderOwnershipRule],
    pack: RenderOwnershipPack | None,
) -> tuple[list[RenderOwnershipRule], tuple[str, ...]]:
    """Apply operator overrides from ``render-ownership-pack.yml``."""
    if pack is None:
        return rules, ()
    layers = pack.layers_enabled or {}
    if layers.get("render_ownership_coverage", True) is False:
        rules = []
    if pack.render_ownership_rules:
        # Operator-supplied rules replace canonical rule for the same
        # deliverable_kind; otherwise append.
        by_kind = {r.deliverable_kind: r for r in rules}
        for override in pack.render_ownership_rules:
            by_kind[override.deliverable_kind] = override
        rules = list(by_kind.values())
    logger.info(
        "Loaded render-ownership-pack.yml %s (edited %s by %s); "
        "layers_enabled=%s; transition_trigger_hints=%d",
        pack.pack_version,
        pack.last_edited,
        pack.last_edited_by,
        sorted({k for k, v in layers.items() if v}),
        len(pack.transition_trigger_hints),
    )
    return rules, pack.transition_trigger_hints


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate render-pipeline ownership coverage across "
            "Think Big engagement folders (I71 P5 Pack A4; WORKSPACE_BLUEPRINT "
            "§16; D-IH-71-S)."
        )
    )
    parser.add_argument("--json-log", action="store_true")
    parser.add_argument(
        "--engagement-root",
        action="append",
        default=[],
        help=(
            "Engagement-folder root to scan (repeatable). "
            "Defaults to Think Big/Clients/ + Think Big/Advisers/."
        ),
    )
    parser.add_argument(
        "--pack-path",
        default=str(DEFAULT_PACK_PATH),
        help=(
            "Path to render-ownership-pack.yml operator override surface. "
            "Optional; absence is graceful."
        ),
    )
    parser.add_argument(
        "--strict-empty",
        action="store_true",
        help="Exit 1 if no engagement folders found at any scanned root.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    rules = parse_render_ownership_rules(WORKSPACE_BLUEPRINT_PATH)
    if not rules:
        logger.error(
            "Pack A4 chassis loaded zero rules from WORKSPACE_BLUEPRINT_HOLISTIKA.md "
            "§16 (expected 9 canonical rules). Refusing to PASS."
        )
        return 1

    pack = parse_render_ownership_pack_yaml(Path(args.pack_path)) if args.pack_path else None
    rules, pack_hints = _apply_pack_overrides(rules, pack)

    logger.info(
        "RENDER OWNERSHIP loaded %d rule(s) across deliverable kinds %s",
        len(rules),
        sorted({r.deliverable_kind for r in rules}),
    )

    roots = [Path(p) for p in args.engagement_root] or list(DEFAULT_ENGAGEMENT_ROOTS)
    engagements = _iter_engagements(roots)

    if not engagements:
        msg = (
            "No engagement folders found at default roots "
            "(Think Big/Clients/ + Think Big/Advisers/). Skipping Pack A4 scan."
        )
        if args.strict_empty:
            logger.error("%s", msg)
            return 1
        logger.info("%s", msg)
        return 0

    all_hits: list[RenderOwnershipHit] = []
    cardinality_totals: dict[DeliverableKind, int] = {}
    for engagement in engagements:
        hits, cardinality = scan_engagement(engagement, rules)
        all_hits.extend(hits)
        for k, v in cardinality.items():
            cardinality_totals[k] = cardinality_totals.get(k, 0) + v

    all_hits.extend(
        _aggregate_transition_hints(cardinality_totals, len(engagements), pack_hints)
    )

    error_hits = [h for h in all_hits if h.severity == "error"]
    warning_hits = [h for h in all_hits if h.severity == "warning"]
    info_hits = [h for h in all_hits if h.severity == "info"]

    for hit in all_hits[:200]:
        try:
            rel = hit.file.relative_to(REPO_ROOT)
        except ValueError:
            rel = hit.file
        level = (
            logger.error
            if hit.severity == "error"
            else logger.warning
            if hit.severity == "warning"
            else logger.info
        )
        level(
            "%s %s (%s; %s): %s",
            rel,
            hit.rule_id,
            hit.deliverable_kind,
            hit.severity,
            hit.rationale,
        )
    if len(all_hits) > 200:
        logger.info("... and %d more advisories suppressed", len(all_hits) - 200)

    if error_hits:
        logger.error(
            "RENDER OWNERSHIP: %d error(s) + %d warning(s) + %d info advisor(y/ies) "
            "across %d engagement(s)",
            len(error_hits),
            len(warning_hits),
            len(info_hits),
            len(engagements),
        )
        return 1

    logger.info(
        "RENDER OWNERSHIP OK -- %d engagement(s) scanned; 0 error hits "
        "(%d warning(s), %d info advisor(y/ies))",
        len(engagements),
        len(warning_hits),
        len(info_hits),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
