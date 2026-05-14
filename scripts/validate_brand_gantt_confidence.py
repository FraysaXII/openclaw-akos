#!/usr/bin/env python3
"""Validate Brand Gantt confidence ladder + audience-quadrant discipline (I71 P2 Pack A2).

Walks `gantt.*.md` artifacts under engagement folders (defaults to
``docs/references/hlk/v3.0/Think Big/Clients/`` and ``Advisers/``); parses
YAML frontmatter; derives a surface class from the parent folder name
(``02-customer-pack/`` -> customer; ``01-operator-pack/`` or ``00-internal/``
-> operator; else unknown); applies three rule families from the chassis at
``akos.brand_voice_register``:

1. **Confidence-band ladder** (per BRAND_GANTT_DISCIPLINE.md §4).
   - ``confidence_band`` must be present + integer 1..5.
   - Band label (derived) must match band number.
2. **Variant-quadrant consistency** (per BRAND_GANTT_DISCIPLINE.md §2).
   - Customer-pack artifacts only ship Variant A or B.
   - Operator-internal artifacts only ship Variant C or D.
3. **Confidence inflation** (per §4 "When to use" allowed-variants column).
   - Variant A: bands 1-3 allowed; bands 4-5 forbidden (inflation).
   - Variant B: bands 4-5 allowed; bands 1-2 forbidden (customer-pack should
     not ship low-confidence per §4 footer rule).
   - Variant C: bands 2-3 allowed; bands 4-5 forbidden (inflation); band 1
     allowed at most as warning (Variant C is operator hypothesis surface).
   - Variant D: bands 4-5 expected; bands 1-2 forbidden (Variant D is
     execution plan with concrete cadence).

Pack overrides are loaded from
``docs/.../Brand/canonicals/_validators/gantt-pack.yml`` via
``akos.brand_voice_register.parse_gantt_pack_yaml``; absent file = canonical
defaults only.

Exit codes::

    0 -- no Gantt violations (any severity ``error``); informational hits OK.
    1 -- at least one ``error``-severity violation; or ``--strict-empty``
         and no Gantt artifacts found.

Cross-references::

    BRAND_GANTT_DISCIPLINE.md §2 (4-quadrant audience matrix)
    BRAND_GANTT_DISCIPLINE.md §4 (5-level confidence ladder)
    BRAND_GANTT_DISCIPLINE.md §7 (validator forward-link to I71)
    akos/brand_voice_register.py (chassis; Pack A2 additive surfaces)
    I71 P2 master-roadmap + initiative-scoped plan §P2 Step 2a
    D-IH-71-L (Pack A2 ratification).
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.brand_voice_register import (
    AudienceQuadrantRule,
    BrandGanttPack,
    GanttConfidenceRule,
    GanttVariant,
    Severity,
    parse_audience_quadrant_rules,
    parse_gantt_confidence_rules,
    parse_gantt_pack_yaml,
)
from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.brand_gantt_confidence")

GANTT_DISCIPLINE_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Marketing"
    / "Brand"
    / "UX Designer"
    / "canonicals"
    / "BRAND_GANTT_DISCIPLINE.md"
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
    / "gantt-pack.yml"
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

# Variant -> allowed confidence bands per §4 "When to use" column.
ALLOWED_BANDS_PER_VARIANT: dict[GanttVariant, set[int]] = {
    "A": {1, 3},  # Reserved or Posture only.
    "B": {4, 5},  # Probable or Confirmed; customer-pack high-confidence.
    "C": {2, 3},  # Hypothesis or Posture; operator-internal low-maturity.
    "D": {3, 4, 5},  # Posture, Probable, or Confirmed; execution plan.
}


# -----------------------------------------------------------------------------
# Frontmatter parsing
# -----------------------------------------------------------------------------


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Parse a minimal YAML frontmatter block. Returns ``{}`` if none.

    Intentionally simple (key: value) extraction; no nested mappings. The
    Gantt frontmatter contract per BRAND_GANTT_DISCIPLINE.md §3 is flat.
    """
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
# Surface class detection
# -----------------------------------------------------------------------------


def _surface_class(path: Path) -> str:
    """Derive surface class from path components.

    Returns one of ``"customer"`` / ``"operator"`` / ``"unknown"``.
    """
    parts = {p.lower() for p in path.parts}
    if any("customer-pack" in p for p in parts) or "02-customer-pack" in parts:
        return "customer"
    if any("operator-pack" in p for p in parts) or "01-operator-pack" in parts:
        return "operator"
    if any("internal" in p for p in parts) or "00-internal" in parts:
        return "operator"
    return "unknown"


# -----------------------------------------------------------------------------
# Hit type
# -----------------------------------------------------------------------------


@dataclass
class GanttHit:
    file: Path
    surface_class: str
    rule_id: str
    severity: Severity
    rationale: str


# -----------------------------------------------------------------------------
# Detection
# -----------------------------------------------------------------------------


def _check_band(
    path: Path,
    frontmatter: dict[str, str],
    confidence_rules: list[GanttConfidenceRule],
    surface_class: str,
) -> list[GanttHit]:
    hits: list[GanttHit] = []
    band_raw = frontmatter.get("confidence_band")
    if band_raw is None:
        hits.append(
            GanttHit(
                file=path,
                surface_class=surface_class,
                rule_id="confidence-band-missing",
                severity="error",
                rationale=(
                    "Gantt frontmatter missing `confidence_band:` per BRAND_GANTT_DISCIPLINE.md §3."
                ),
            )
        )
        return hits
    try:
        band = int(band_raw)
    except ValueError:
        hits.append(
            GanttHit(
                file=path,
                surface_class=surface_class,
                rule_id="confidence-band-non-integer",
                severity="error",
                rationale=(
                    f"`confidence_band: {band_raw!r}` not parseable as integer 1-5 "
                    f"per BRAND_GANTT_DISCIPLINE.md §4."
                ),
            )
        )
        return hits

    valid_bands = {r.band for r in confidence_rules}
    if band not in valid_bands:
        hits.append(
            GanttHit(
                file=path,
                surface_class=surface_class,
                rule_id="confidence-band-out-of-ladder",
                severity="error",
                rationale=(
                    f"`confidence_band: {band}` outside the 5-level ladder "
                    f"(1=Reserved..5=Confirmed) per BRAND_GANTT_DISCIPLINE.md §4."
                ),
            )
        )
    return hits


def _check_variant_quadrant(
    path: Path,
    frontmatter: dict[str, str],
    quadrant_rules: list[AudienceQuadrantRule],
    surface_class: str,
) -> list[GanttHit]:
    hits: list[GanttHit] = []
    variant_raw = frontmatter.get("gantt_variant")
    if variant_raw is None:
        hits.append(
            GanttHit(
                file=path,
                surface_class=surface_class,
                rule_id="variant-missing",
                severity="error",
                rationale=(
                    "Gantt frontmatter missing `gantt_variant:` per BRAND_GANTT_DISCIPLINE.md §3."
                ),
            )
        )
        return hits
    variant = variant_raw.strip().upper()
    if variant not in ("A", "B", "C", "D"):
        hits.append(
            GanttHit(
                file=path,
                surface_class=surface_class,
                rule_id="variant-invalid",
                severity="error",
                rationale=(
                    f"`gantt_variant: {variant_raw!r}` not in A | B | C | D per "
                    f"BRAND_GANTT_DISCIPLINE.md §2."
                ),
            )
        )
        return hits

    if surface_class == "unknown":
        # Cannot enforce variant/surface consistency without a known surface.
        return hits

    for rule in quadrant_rules:
        if rule.variant != variant:
            continue
        if surface_class == "customer" and rule.forbidden_in_customer_pack:
            hits.append(
                GanttHit(
                    file=path,
                    surface_class=surface_class,
                    rule_id="variant-quadrant-mismatch",
                    severity=rule.default_severity,
                    rationale=(
                        f"Variant {variant} is operator-internal "
                        f"({rule.audience_facing}/{rule.data_maturity}) but artifact lives "
                        f"in a customer-pack surface; customer-pack only ships Variant A or B "
                        f"per BRAND_GANTT_DISCIPLINE.md §2."
                    ),
                )
            )
        if surface_class == "operator" and rule.forbidden_in_operator_pack:
            hits.append(
                GanttHit(
                    file=path,
                    surface_class=surface_class,
                    rule_id="variant-quadrant-mismatch",
                    severity=rule.default_severity,
                    rationale=(
                        f"Variant {variant} is customer-facing "
                        f"({rule.audience_facing}/{rule.data_maturity}) but artifact lives "
                        f"in an operator-internal surface; operator-internal only ships "
                        f"Variant C or D per BRAND_GANTT_DISCIPLINE.md §2."
                    ),
                )
            )
        break
    return hits


def _check_confidence_inflation(
    path: Path,
    frontmatter: dict[str, str],
    surface_class: str,
) -> list[GanttHit]:
    hits: list[GanttHit] = []
    variant_raw = frontmatter.get("gantt_variant")
    band_raw = frontmatter.get("confidence_band")
    if variant_raw is None or band_raw is None:
        return hits
    variant = variant_raw.strip().upper()
    try:
        band = int(band_raw)
    except ValueError:
        return hits
    if variant not in ALLOWED_BANDS_PER_VARIANT:
        return hits
    allowed = ALLOWED_BANDS_PER_VARIANT[variant]  # type: ignore[index]
    if band in allowed:
        return hits
    hits.append(
        GanttHit(
            file=path,
            surface_class=surface_class,
            rule_id="confidence-inflation",
            severity="error",
            rationale=(
                f"Variant {variant} with band {band} violates "
                f"BRAND_GANTT_DISCIPLINE.md §4 allowed-variants column "
                f"(Variant {variant} allows bands {sorted(allowed)})."
            ),
        )
    )
    return hits


def scan_gantt_file(
    path: Path,
    confidence_rules: list[GanttConfidenceRule],
    quadrant_rules: list[AudienceQuadrantRule],
) -> list[GanttHit]:
    """Scan one ``gantt.*.md`` artifact; return all hits."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        logger.warning("Skipping unreadable Gantt artifact %s: %s", path, exc)
        return []
    frontmatter = _parse_frontmatter(text)
    if not frontmatter:
        return [
            GanttHit(
                file=path,
                surface_class=_surface_class(path),
                rule_id="frontmatter-missing",
                severity="error",
                rationale=(
                    "Gantt artifact has no YAML frontmatter; "
                    "BRAND_GANTT_DISCIPLINE.md §3 requires `gantt_variant:` + "
                    "`confidence_band:` + `ratify_cadence:`."
                ),
            )
        ]
    surface_class = _surface_class(path)
    hits = []
    hits.extend(_check_band(path, frontmatter, confidence_rules, surface_class))
    hits.extend(_check_variant_quadrant(path, frontmatter, quadrant_rules, surface_class))
    hits.extend(_check_confidence_inflation(path, frontmatter, surface_class))
    return hits


# -----------------------------------------------------------------------------
# Pack overrides
# -----------------------------------------------------------------------------


def _apply_pack_overrides(
    confidence_rules: list[GanttConfidenceRule],
    quadrant_rules: list[AudienceQuadrantRule],
    pack: BrandGanttPack | None,
) -> tuple[list[GanttConfidenceRule], list[AudienceQuadrantRule]]:
    """Apply operator overrides from ``gantt-pack.yml`` to canonical defaults.

    At P2 the pack consumes ``layers_enabled`` flags (a layer flag = False
    drops the corresponding rule family) + operator-extended rule rows
    (additional confidence / quadrant rules appended to canonical defaults).
    Per-rule severity overrides are forward-charter.
    """
    if pack is None:
        return confidence_rules, quadrant_rules
    layers = pack.layers_enabled or {}
    if layers.get("confidence_band_validity", True) is False:
        confidence_rules = []
    if layers.get("variant_quadrant_consistency", True) is False:
        quadrant_rules = []
    if pack.gantt_confidence_rules:
        confidence_rules = list(confidence_rules) + list(pack.gantt_confidence_rules)
    if pack.audience_quadrant_rules:
        quadrant_rules = list(quadrant_rules) + list(pack.audience_quadrant_rules)
    logger.info(
        "Loaded gantt-pack.yml %s (edited %s by %s); layers_enabled=%s",
        pack.pack_version,
        pack.last_edited,
        pack.last_edited_by,
        sorted({k for k, v in layers.items() if v}),
    )
    return confidence_rules, quadrant_rules


# -----------------------------------------------------------------------------
# Engagement walk
# -----------------------------------------------------------------------------


def _iter_gantt_files(roots: Iterable[Path]) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("gantt*.md"):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            out.append(path)
    return sorted(out)


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate Brand Gantt confidence ladder + audience-quadrant "
            "discipline (I71 P2 Pack A2; BRAND_GANTT_DISCIPLINE.md §§2,4,7; "
            "D-IH-71-L)."
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
            "Path to gantt-pack.yml operator override surface. "
            "Optional; absence is graceful."
        ),
    )
    parser.add_argument(
        "--strict-empty",
        action="store_true",
        help="Exit 1 if no Gantt artifacts found at any scanned root.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    confidence_rules = parse_gantt_confidence_rules(GANTT_DISCIPLINE_PATH)
    quadrant_rules = parse_audience_quadrant_rules(GANTT_DISCIPLINE_PATH)
    if not confidence_rules or not quadrant_rules:
        logger.error(
            "Pack A2 chassis loaded zero rules from BRAND_GANTT_DISCIPLINE.md "
            "(expected 5 confidence + 4 quadrant). Refusing to PASS."
        )
        return 1

    pack = parse_gantt_pack_yaml(Path(args.pack_path)) if args.pack_path else None
    confidence_rules, quadrant_rules = _apply_pack_overrides(
        confidence_rules, quadrant_rules, pack
    )

    logger.info(
        "BRAND_GANTT_CONFIDENCE loaded %d confidence rule(s) + %d quadrant rule(s)",
        len(confidence_rules),
        len(quadrant_rules),
    )

    roots = [Path(p) for p in args.engagement_root] or list(DEFAULT_ENGAGEMENT_ROOTS)
    gantt_files = _iter_gantt_files(roots)

    if not gantt_files:
        msg = (
            "No Gantt artifacts (`gantt*.md`) found at default engagement roots "
            "(Think Big/Clients/ + Think Big/Advisers/). Skipping Pack A2 scan."
        )
        if args.strict_empty:
            logger.error("%s", msg)
            return 1
        logger.info("%s", msg)
        return 0

    all_hits: list[GanttHit] = []
    for path in gantt_files:
        all_hits.extend(scan_gantt_file(path, confidence_rules, quadrant_rules))

    error_hits = [h for h in all_hits if h.severity == "error"]
    warning_hits = [h for h in all_hits if h.severity == "warning"]

    for hit in all_hits[:200]:
        try:
            rel = hit.file.relative_to(REPO_ROOT)
        except ValueError:
            rel = hit.file
        level = logger.error if hit.severity == "error" else logger.warning
        level(
            "%s [%s] %s (%s): %s",
            rel,
            hit.surface_class,
            hit.rule_id,
            hit.severity,
            hit.rationale,
        )
    if len(all_hits) > 200:
        logger.error("... and %d more hits suppressed", len(all_hits) - 200)

    if error_hits:
        logger.error(
            "BRAND_GANTT_CONFIDENCE: %d error(s) + %d warning(s) across %d Gantt file(s) (%d scanned)",
            len(error_hits),
            len(warning_hits),
            len({h.file for h in all_hits}),
            len(gantt_files),
        )
        return 1

    logger.info(
        "BRAND_GANTT_CONFIDENCE OK — %d Gantt artifact(s) scanned; "
        "0 error hits (%d warning(s))",
        len(gantt_files),
        len(warning_hits),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
