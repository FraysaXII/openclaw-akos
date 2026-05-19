"""Validate locale orthography per BRAND_<LANG>_PATTERNS.md anti-pattern catalogues.

Per Wave F Strand 3a (I86; ratified at second axis-2 ratify gate 2026-05-19 option
B1 "Orthography validator covers ES+FR+EN with strict modes per locale").

Sister validator to ``validate_external_render_trail.py``. Where that validator
gates the *existence* of an external-render trail, this validator gates the
*orthographic quality* of the source markdown the trail renders from. Diacritic
errors, missing cedillas, and ASCII smart-quote leaks in body prose reach the
external recipient regardless of which surface they render to (PDF / Web / Mail
all carry the source typography).

Scope contract (intentionally narrow to keep false-positive risk near zero):

- Scans the same SCAN_GLOBS as ``validate_external_render_trail.py``
  (`docs/references/hlk/v3.0/_assets/advops/**`, `Think Big/Advisers/**`, etc.).
- Only acts on surfaces that declare ``language:`` in frontmatter (es / fr / en
  or locale variants like es-ES, fr-FR, en-US).
- Strips frontmatter + code blocks + URLs + markdown link targets before scan.
- Anti-pattern catalogue lives in ``akos/orthography.py`` (Pydantic-modelled;
  SSOT for word-list rules per locale).
- ES + FR rules: word-list-based diacritic / cedilla / tilde anti-patterns.
- EN rules: smart-quote threshold scan (straight-double-quote count >= 4
  triggers; lower thresholds produce too many false positives on legitimate
  inline code that escaped the strip pipeline).

Exit code: 0 PASS or INFO advisory; 1 FAIL when ``--strict`` or
``AKOS_LOCALE_ORTHOGRAPHY_STRICT=1`` set.

Per-locale override: ``--strict-es`` / ``--strict-fr`` / ``--strict-en`` enable
FAIL only for the named locale (so e.g. you can promote ES to FAIL while FR + EN
remain advisory during backfill).

CLI:
    py scripts/validate_locale_orthography.py                  # advisory all
    py scripts/validate_locale_orthography.py --strict         # FAIL all locales
    py scripts/validate_locale_orthography.py --strict-es      # FAIL ES only
"""
from __future__ import annotations

import logging
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos import log  # noqa: E402
from akos.orthography import (  # noqa: E402
    ANTI_PATTERNS_BY_LOCALE,
    FRONTMATTER_PATTERN,
    OrthographyAntiPattern,
    VALID_LOCALES,
    extract_language,
    strip_non_prose,
)

log.setup_logging()
logger = logging.getLogger(__name__)

SCAN_GLOBS: tuple[str, ...] = (
    "docs/references/hlk/v3.0/_assets/advops/**/*.md",
    "docs/references/hlk/v3.0/_assets/touchpoint-kit/**/*.md",
    "docs/references/hlk/v3.0/_assets/touchpoint_kits/**/*.md",
    "docs/references/hlk/v3.0/Think Big/Advisers/**/*.md",
)

SKIP_PATTERNS: tuple[re.Pattern, ...] = (
    re.compile(r"\.objections\.md$"),
    re.compile(r"\.counterparty-brief\.md$"),
    re.compile(r"\.manifest\.md$"),
    re.compile(r"/_template"),
    re.compile(r"/templates?/"),
    re.compile(r"/_engagement-template/"),
    re.compile(r"/_candidates/"),
    re.compile(r"/topic_[^/]*\.md$"),
    re.compile(r"/README\.md$", re.IGNORECASE),
)

EN_STRAIGHT_QUOTE_THRESHOLD: int = 4


def _should_skip(path: Path) -> bool:
    rel = path.as_posix()
    return any(pattern.search(rel) for pattern in SKIP_PATTERNS)


def _extract_frontmatter(text: str) -> str | None:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return None
    return match.group(1)


def _scan_word_list(body: str, patterns: tuple[OrthographyAntiPattern, ...]) -> list[tuple[OrthographyAntiPattern, int]]:
    """Return list of (pattern, count) tuples for word-list rules that fired."""
    hits: list[tuple[OrthographyAntiPattern, int]] = []
    for pattern in patterns:
        regex = re.compile(rf"(?<![A-Za-zÀ-ÿ]){re.escape(pattern.ascii_form)}(?![A-Za-zÀ-ÿ])")
        matches = regex.findall(body)
        if matches:
            hits.append((pattern, len(matches)))
    return hits


def _scan_en_smart_quotes(body: str) -> int:
    """Count straight double-quote characters in body prose (heuristic).

    Returns the count; the validator flags when count >= EN_STRAIGHT_QUOTE_THRESHOLD.
    Single-quote scanning is deliberately omitted (apostrophe / contraction
    ambiguity produces too many false positives).
    """
    return body.count('"')


def _iter_target_files() -> list[Path]:
    files: list[Path] = []
    for glob_pattern in SCAN_GLOBS:
        for path in REPO_ROOT.glob(glob_pattern):
            if path.is_file() and path.suffix == ".md" and not _should_skip(path):
                files.append(path)
    seen: set[Path] = set()
    deduped: list[Path] = []
    for path in files:
        if path not in seen:
            deduped.append(path)
            seen.add(path)
    return deduped


def validate(
    strict: bool = False,
    strict_es: bool = False,
    strict_fr: bool = False,
    strict_en: bool = False,
) -> int:
    files_scanned = 0
    files_with_language = 0
    files_with_hits = 0
    total_hits = 0
    per_locale_counts: dict[str, int] = {"es": 0, "fr": 0, "en": 0}
    findings: list[tuple[str, str, list[tuple[OrthographyAntiPattern, int]], int]] = []

    for path in _iter_target_files():
        files_scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        frontmatter = _extract_frontmatter(text)
        if frontmatter is None:
            continue
        locale = extract_language(frontmatter)
        if locale is None or locale not in VALID_LOCALES:
            continue
        files_with_language += 1

        body = strip_non_prose(text)
        rel_path = path.relative_to(REPO_ROOT).as_posix()

        word_hits = _scan_word_list(body, ANTI_PATTERNS_BY_LOCALE[locale])
        en_quote_count = _scan_en_smart_quotes(body) if locale == "en" else 0
        en_flagged = locale == "en" and en_quote_count >= EN_STRAIGHT_QUOTE_THRESHOLD

        if word_hits or en_flagged:
            files_with_hits += 1
            local_total = sum(count for _, count in word_hits)
            if en_flagged:
                local_total += en_quote_count
            total_hits += local_total
            per_locale_counts[locale] += local_total
            findings.append((rel_path, locale, word_hits, en_quote_count if en_flagged else 0))

    is_global_strict = strict or os.environ.get("AKOS_LOCALE_ORTHOGRAPHY_STRICT") == "1"
    strict_by_locale: dict[str, bool] = {
        "es": is_global_strict or strict_es,
        "fr": is_global_strict or strict_fr,
        "en": is_global_strict or strict_en,
    }

    has_fail = False
    for rel_path, locale, word_hits, en_quote_count in findings:
        is_locale_strict = strict_by_locale[locale]
        level = logger.error if is_locale_strict else logger.info
        if word_hits:
            for pattern, count in word_hits:
                level(
                    "orthography %s: %s — '%s' x%d (suggest '%s') [%s; %s]",
                    locale,
                    rel_path,
                    pattern.ascii_form,
                    count,
                    pattern.canonical_form,
                    pattern.category,
                    pattern.rationale,
                )
        if en_quote_count:
            level(
                "orthography en: %s — %d straight-double-quote characters in body prose (threshold %d); consider curly quotes per BRAND_ENGLISH_PATTERNS §10 LLM-tone-tells",
                rel_path,
                en_quote_count,
                EN_STRAIGHT_QUOTE_THRESHOLD,
            )
        if is_locale_strict:
            has_fail = True

    summary_level = logger.error if has_fail else logger.info
    summary_level(
        "%s: validate_locale_orthography — scanned %d ; language-tagged %d ; with hits %d ; total hits %d (es=%d fr=%d en=%d ; strict_es=%s strict_fr=%s strict_en=%s)",
        "FAIL" if has_fail else "PASS",
        files_scanned,
        files_with_language,
        files_with_hits,
        total_hits,
        per_locale_counts["es"],
        per_locale_counts["fr"],
        per_locale_counts["en"],
        strict_by_locale["es"],
        strict_by_locale["fr"],
        strict_by_locale["en"],
    )
    return 1 if has_fail else 0


def main() -> int:
    strict = "--strict" in sys.argv or "-S" in sys.argv
    strict_es = "--strict-es" in sys.argv
    strict_fr = "--strict-fr" in sys.argv
    strict_en = "--strict-en" in sys.argv
    return validate(
        strict=strict,
        strict_es=strict_es,
        strict_fr=strict_fr,
        strict_en=strict_en,
    )


if __name__ == "__main__":
    sys.exit(main())
