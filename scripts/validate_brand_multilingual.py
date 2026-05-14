#!/usr/bin/env python3
"""Validate Brand multilingual locale-suffix + README triad discipline (I71 P2 Pack A3).

Walks direct-child folders of ``Think Big/Clients/`` and ``Think Big/Advisers/``
(skipping ``_``-prefixed templates / placeholders); detects three classes of
engagement-folder violation per BRAND_MULTILINGUAL_CONTRACT.md §2 + D-IH-70-P:

1. **Per-locale frontmatter cohesion (Detection C).** ``README.<locale>.md``
   must declare matching ``language: <locale>`` frontmatter. ``README.fr.md``
   declaring ``language: en`` is an ``error`` at any strictness.

2. **README triad pointer skeleton (Detection A).** When at least one
   ``README.<locale>.md`` sibling exists, the canonical ``README.md`` must be
   the **5-line pointer** (title + blank + intro sentence containing the
   required keyword ``Per-language READMEs:`` + per-locale bullet links +
   closing blank). A full-prose ``README.md`` alongside per-locale siblings
   is a triad violation (default severity ``warning``; downgradable to
   ``error`` via the C-71-2 inline-ratify gate).

3. **Pointer link-target completeness (Detection B).** When ``README.md``
   declares itself a pointer (contains ``Per-language READMEs:``), every
   declared per-locale link target must resolve to an existing file. A
   pointer linking to ``README.es.md`` while the file is absent is a triad
   violation.

Detection severity for Detection A + B follows the pack-level
``default_triad_severity`` (default ``warning`` per C-71-2 default
warn-until-2-bilingual; flip to ``error`` via inline-ratify when the second
consecutive bilingual engagement ships per master-roadmap §P2). Detection C
is always ``error`` (frontmatter/suffix cohesion is unambiguous).

Pack overrides are loaded from
``docs/.../Brand/canonicals/_validators/multilingual-pack.yml`` via
``akos.brand_voice_register.parse_multilingual_pack_yaml``.

Exit codes::

    0 -- no triad violations at ``error`` severity; informational + warning
         hits OK.
    1 -- at least one ``error``-severity violation; or ``--strict-empty``
         and no engagement folders found.

Cross-references::

    BRAND_MULTILINGUAL_CONTRACT.md §2 (per-engagement language declaration; 3-file pattern)
    BRAND_COUNTERPARTY_README_CONTRACT.md (5-line pointer skeleton + non-technical register)
    D-IH-70-P (I70 P3 bilingual README pattern ratification)
    akos/brand_voice_register.py (chassis; Pack A3 additive surfaces)
    I71 P2 master-roadmap + initiative-scoped plan §P2 Step 2b
    D-IH-71-M (Pack A3 ratification).
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
    BrandMultilingualPack,
    LocaleSuffixRule,
    Locale,
    ReadmeTriadRule,
    Severity,
    parse_locale_suffix_rules,
    parse_multilingual_pack_yaml,
    parse_readme_triad_rules,
)
from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.brand_multilingual")

MULTILINGUAL_CONTRACT_PATH = (
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
    / "BRAND_MULTILINGUAL_CONTRACT.md"
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
    / "multilingual-pack.yml"
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

# Regex to detect locale-suffixed README filename (e.g., README.fr.md).
_LOCALE_README_RE = re.compile(r"^README\.([a-z]{2})\.md$")
# Regex to harvest pointer link targets from the pointer body.
_POINTER_LINK_RE = re.compile(r"\[(README\.[a-z]{2}\.md)\]\((README\.[a-z]{2}\.md)\)")

POINTER_REQUIRED_KEYWORD = "Per-language READMEs:"


# -----------------------------------------------------------------------------
# Frontmatter parsing (reuses Pack A2's pattern; intentionally simple)
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
class MultilingualHit:
    engagement: Path
    file: Path
    rule_id: str
    severity: Severity
    rationale: str


# -----------------------------------------------------------------------------
# Engagement scan helpers
# -----------------------------------------------------------------------------


def _is_pointer_readme(text: str) -> bool:
    """Detect if a README.md is a multilingual pointer (contains required keyword)."""
    return POINTER_REQUIRED_KEYWORD in text


def _count_body_lines(text: str) -> int:
    """Count non-blank body lines (excluding frontmatter)."""
    # Strip frontmatter if present.
    fm_match = _FRONTMATTER_RE.match(text)
    body = text[fm_match.end():] if fm_match else text
    return sum(1 for line in body.splitlines() if line.strip())


def _extract_pointer_link_targets(text: str) -> list[str]:
    """Harvest per-locale link targets declared by a pointer README."""
    return [m.group(2) for m in _POINTER_LINK_RE.finditer(text)]


def scan_engagement(
    engagement_dir: Path,
    locale_rules: list[LocaleSuffixRule],
    triad_rules: list[ReadmeTriadRule],
    triad_severity: Severity,
) -> list[MultilingualHit]:
    """Scan one engagement folder; return all hits."""
    hits: list[MultilingualHit] = []
    readme = engagement_dir / "README.md"
    locale_to_path: dict[Locale, Path] = {}
    for child in engagement_dir.iterdir():
        if not child.is_file():
            continue
        m = _LOCALE_README_RE.match(child.name)
        if not m:
            continue
        locale_str = m.group(1)
        if locale_str in ("en", "fr", "es"):
            locale_to_path[locale_str] = child  # type: ignore[index]

    # Detection (c) — per-locale frontmatter cohesion.
    for rule in locale_rules:
        path = locale_to_path.get(rule.locale)
        if path is None:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            logger.warning("Skipping unreadable per-locale README %s: %s", path, exc)
            continue
        fm = _parse_frontmatter(text)
        declared = fm.get("language", "").strip().lower()
        if declared and declared != rule.frontmatter_language_value:
            hits.append(
                MultilingualHit(
                    engagement=engagement_dir,
                    file=path,
                    rule_id="locale-frontmatter-mismatch",
                    severity=rule.default_severity,
                    rationale=(
                        f"`{path.name}` declares `language: {declared!r}` but suffix "
                        f"`{rule.expected_suffix}` requires `language: "
                        f"{rule.frontmatter_language_value!r}` per "
                        f"BRAND_MULTILINGUAL_CONTRACT.md §2."
                    ),
                )
            )
        if not declared and locale_to_path:
            hits.append(
                MultilingualHit(
                    engagement=engagement_dir,
                    file=path,
                    rule_id="locale-frontmatter-missing-language",
                    severity=rule.default_severity,
                    rationale=(
                        f"`{path.name}` lacks `language:` frontmatter; "
                        f"BRAND_MULTILINGUAL_CONTRACT.md §2 requires per-locale "
                        f"frontmatter declaration."
                    ),
                )
            )

    # If no per-locale siblings exist, treat the engagement as monolingual and
    # skip Detection A + B. This is the deliberate behavior to avoid false
    # positives on engagements that have not adopted the 3-file pattern.
    if not locale_to_path:
        return hits

    if not readme.exists():
        hits.append(
            MultilingualHit(
                engagement=engagement_dir,
                file=engagement_dir / "README.md",
                rule_id="readme-missing-with-per-locale-siblings",
                severity=triad_severity,
                rationale=(
                    f"Engagement has per-locale READMEs ({sorted(locale_to_path.keys())}) "
                    f"but no `README.md` pointer; BRAND_MULTILINGUAL_CONTRACT.md §2 "
                    f"3-file pattern requires the pointer."
                ),
            )
        )
        return hits

    try:
        readme_text = readme.read_text(encoding="utf-8")
    except OSError as exc:
        logger.warning("Skipping unreadable README %s: %s", readme, exc)
        return hits

    # Detection (a) — pointer skeleton when per-locale siblings exist.
    if not _is_pointer_readme(readme_text):
        hits.append(
            MultilingualHit(
                engagement=engagement_dir,
                file=readme,
                rule_id="readme-not-a-pointer-with-per-locale-siblings",
                severity=triad_severity,
                rationale=(
                    f"`README.md` does not contain pointer keyword "
                    f"{POINTER_REQUIRED_KEYWORD!r}, but per-locale siblings "
                    f"exist ({sorted(locale_to_path.keys())}); the 3-file pattern "
                    f"requires `README.md` to be a pointer skeleton per "
                    f"BRAND_MULTILINGUAL_CONTRACT.md §2 + D-IH-70-P."
                ),
            )
        )
    else:
        # Detection (a) line-count window.
        for triad_rule in triad_rules:
            body_lines = _count_body_lines(readme_text)
            if not (triad_rule.pointer_line_count_min <= body_lines <= triad_rule.pointer_line_count_max):
                hits.append(
                    MultilingualHit(
                        engagement=engagement_dir,
                        file=readme,
                        rule_id="pointer-line-count-out-of-window",
                        severity=triad_severity,
                        rationale=(
                            f"Pointer body has {body_lines} non-blank lines; expected "
                            f"window {triad_rule.pointer_line_count_min}..{triad_rule.pointer_line_count_max} "
                            f"per BRAND_MULTILINGUAL_CONTRACT.md §2."
                        ),
                    )
                )

        # Detection (b) — declared link targets must resolve.
        declared_targets = _extract_pointer_link_targets(readme_text)
        for target in declared_targets:
            target_path = engagement_dir / target
            if not target_path.exists():
                hits.append(
                    MultilingualHit(
                        engagement=engagement_dir,
                        file=readme,
                        rule_id="pointer-target-missing",
                        severity=triad_severity,
                        rationale=(
                            f"Pointer declares link to `{target}` but the file does not "
                            f"exist on disk; the 3-file pattern requires every declared "
                            f"target to resolve per BRAND_MULTILINGUAL_CONTRACT.md §2."
                        ),
                    )
                )

    return hits


# -----------------------------------------------------------------------------
# Pack overrides
# -----------------------------------------------------------------------------


def _apply_pack_overrides(
    locale_rules: list[LocaleSuffixRule],
    triad_rules: list[ReadmeTriadRule],
    pack: BrandMultilingualPack | None,
) -> tuple[list[LocaleSuffixRule], list[ReadmeTriadRule], Severity]:
    """Apply operator overrides from ``multilingual-pack.yml``."""
    triad_severity: Severity = "warning"
    if pack is None:
        return locale_rules, triad_rules, triad_severity
    layers = pack.layers_enabled or {}
    if layers.get("locale_suffix_cohesion", True) is False:
        locale_rules = []
    if layers.get("readme_triad_pointer", True) is False:
        triad_rules = []
    if pack.locale_suffix_rules:
        locale_rules = list(locale_rules) + list(pack.locale_suffix_rules)
    if pack.readme_triad_rules:
        triad_rules = list(triad_rules) + list(pack.readme_triad_rules)
    triad_severity = pack.default_triad_severity or "warning"
    logger.info(
        "Loaded multilingual-pack.yml %s (edited %s by %s); "
        "layers_enabled=%s; default_triad_severity=%s",
        pack.pack_version,
        pack.last_edited,
        pack.last_edited_by,
        sorted({k for k, v in layers.items() if v}),
        triad_severity,
    )
    return locale_rules, triad_rules, triad_severity


# -----------------------------------------------------------------------------
# Engagement walk
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
                continue  # skip _engagement-template, _archive, etc.
            out.append(child)
    return out


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate Brand multilingual locale-suffix + README triad discipline "
            "(I71 P2 Pack A3; BRAND_MULTILINGUAL_CONTRACT.md §2 + D-IH-70-P; "
            "D-IH-71-M)."
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
            "Path to multilingual-pack.yml operator override surface. "
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

    locale_rules = parse_locale_suffix_rules(MULTILINGUAL_CONTRACT_PATH)
    triad_rules = parse_readme_triad_rules(MULTILINGUAL_CONTRACT_PATH)
    if not locale_rules or not triad_rules:
        logger.error(
            "Pack A3 chassis loaded zero rules from BRAND_MULTILINGUAL_CONTRACT.md "
            "(expected 3 locale + 1 triad). Refusing to PASS."
        )
        return 1

    pack = parse_multilingual_pack_yaml(Path(args.pack_path)) if args.pack_path else None
    locale_rules, triad_rules, triad_severity = _apply_pack_overrides(
        locale_rules, triad_rules, pack
    )

    logger.info(
        "BRAND_MULTILINGUAL loaded %d locale rule(s) + %d triad rule(s); "
        "default_triad_severity=%s",
        len(locale_rules),
        len(triad_rules),
        triad_severity,
    )

    roots = [Path(p) for p in args.engagement_root] or list(DEFAULT_ENGAGEMENT_ROOTS)
    engagements = _iter_engagements(roots)

    if not engagements:
        msg = (
            "No engagement folders found at default roots "
            "(Think Big/Clients/ + Think Big/Advisers/). Skipping Pack A3 scan."
        )
        if args.strict_empty:
            logger.error("%s", msg)
            return 1
        logger.info("%s", msg)
        return 0

    all_hits: list[MultilingualHit] = []
    for engagement in engagements:
        all_hits.extend(
            scan_engagement(engagement, locale_rules, triad_rules, triad_severity)
        )

    error_hits = [h for h in all_hits if h.severity == "error"]
    warning_hits = [h for h in all_hits if h.severity == "warning"]

    for hit in all_hits[:200]:
        try:
            rel = hit.file.relative_to(REPO_ROOT)
        except ValueError:
            rel = hit.file
        level = logger.error if hit.severity == "error" else logger.warning
        level(
            "%s %s (%s): %s",
            rel,
            hit.rule_id,
            hit.severity,
            hit.rationale,
        )
    if len(all_hits) > 200:
        logger.error("... and %d more hits suppressed", len(all_hits) - 200)

    if error_hits:
        logger.error(
            "BRAND_MULTILINGUAL: %d error(s) + %d warning(s) across %d engagement(s) (%d scanned)",
            len(error_hits),
            len(warning_hits),
            len({h.engagement for h in all_hits}),
            len(engagements),
        )
        return 1

    logger.info(
        "BRAND_MULTILINGUAL OK — %d engagement(s) scanned; 0 error hits (%d warning(s))",
        len(engagements),
        len(warning_hits),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
