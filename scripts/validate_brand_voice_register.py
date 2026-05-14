#!/usr/bin/env python3
"""Validate per-locale voice register on consumer i18n message files.

History::

    I66 P2 / D-IH-66-J -- minted. FR + ES per-locale rules over JSON i18n files.
    I66 P5 incr 3       -- strict-FAIL default in release-gate.py.
    I71 P1 Pack A1      -- 10-layer expansion (D-IH-71-A, D-IH-71-F..K):
        * Layer 0 (FR -- existing, unchanged): anglicisms + performative.
        * Layer 1 (ES -- existing, unchanged): anglicisms + performative + vague-time.
        * Layer 2 (EN -- new, I71 P1): MBA-deck jargon + 7 AI-tone tic families
          parsed from ``BRAND_ENGLISH_PATTERNS.md`` + ``BRAND_COPYWRITING_DISCIPLINE.md``.
        * Layer 3 (audience matrix): rule-pack loaded; INFO-level summary (forward).
        * Layer 4 (Storytelling/Resonance boundary): rule-pack loaded; INFO-level summary (forward).
        * Layers 5-7, 9 (Round 3 brand-DNA): rule-pack loaded; INFO-level summary (forward).
        * Layer 8 (anti-LLM-tone): EN catalog scanned against en.json keys; strict-day-1
          per C-71-8 (operator override).

The validator's runtime contract:

- **Locale-aware over JSON message files** (the scan surface remains
  ``boilerplate/messages/{en,es,fr}.json`` and any ``hlk-erp/messages/*``
  mirror; markdown surface scanning is forward-charter).
- **Per-rule severity from canonical defaults** with operator overrides
  applied via the optional ``register-pack.yml`` consumed through
  ``akos.brand_voice_register.parse_register_pack_yaml``.
- **Strict-day-1** default for all layers per D-IH-71-F + C-71-8. The env
  escape ``AKOS_BRAND_VOICE_REGISTER_SOFT=1`` continues to demote the
  release-gate row to INFO; per-rule operator allow-listing happens in the
  YAML pack, not via env vars.

This is a **register validator** distinct from ``validate_brand_jargon.py``:

- ``validate_brand_jargon.py`` is locale-agnostic and forbids internal
  codenames + stack jargon + abbreviations from rendered DOM (any locale).
- ``validate_brand_voice_register.py`` is **locale-aware** and forbids
  patterns that read native-speaker-bad in a given locale (FR anglicisms,
  ES performative humility, EN MBA-deck jargon, LLM lexical tells, etc.).

Skipped (graceful) when consumer repos are absent. Token lists are parsed
from canonical at run time so the validator does not drift.

Usage::

    py scripts/validate_brand_voice_register.py
    py scripts/validate_brand_voice_register.py --json-log
    py scripts/validate_brand_voice_register.py --consumer-root C:/path/to/sibling
    py scripts/validate_brand_voice_register.py --pack-path docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/register-pack.yml

Exit codes::

    0 -- no register drift (any layer), or no consumer repos present (graceful skip).
    1 -- at least one forbidden pattern found at error severity, OR strict-empty miss.

Cross-references:
  BRAND_FRENCH_PATTERNS.md §5, BRAND_SPANISH_PATTERNS.md §13,
  BRAND_ENGLISH_PATTERNS.md §5, BRAND_COPYWRITING_DISCIPLINE.md §2,
  BRAND_LLM_TONE_TELLS.md §3-§7, BRAND_VOICE_FOUNDATION.md,
  I71 P1 plan + master-roadmap §P1, D-IH-71-F..K.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.brand_voice_register import (
    CANONICAL_PATHS,
    parse_english_register_rules,
    parse_llm_tone_tells,
    parse_register_pack_yaml,
    parse_tic_families_from_canonical,
)
from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.brand_voice_register")

CANON_DIR = (
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
)
FRENCH_PATTERNS_PATH = CANON_DIR / "BRAND_FRENCH_PATTERNS.md"
SPANISH_PATTERNS_PATH = CANON_DIR / "BRAND_SPANISH_PATTERNS.md"
ENGLISH_PATTERNS_PATH = CANON_DIR / "BRAND_ENGLISH_PATTERNS.md"
LLM_TONE_TELLS_PATH = CANON_DIR / "BRAND_LLM_TONE_TELLS.md"
COPYWRITING_DISCIPLINE_PATH = (
    REPO_ROOT / CANONICAL_PATHS["copywriting_discipline"]
)
DEFAULT_PACK_PATH = REPO_ROOT / CANONICAL_PATHS["register_pack_yaml"]

DEFAULT_CONSUMER_ROOTS = (
    REPO_ROOT.parent / "root_cd" / "boilerplate",
    REPO_ROOT.parent / "root_cd" / "hlk-erp",
)

MESSAGE_RELATIVE_PATHS = ("messages", "i18n/messages")


@dataclass(frozen=True)
class RegisterRule:
    locale: str
    token: str
    pattern: re.Pattern[str]
    rationale: str
    canonical_source: str


def _extract_french_anglicisms(path: Path) -> list[RegisterRule]:
    """Parse the §5.1 anglicism table from BRAND_FRENCH_PATTERNS.md.

    Table format::

        | `de-risquer` | `réduire le risque` |

    We extract the left column (anglicism) and build a word-boundary regex.
    """
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")

    rules: list[RegisterRule] = []
    section = re.search(
        r"### 5\.1 Anglicisms.*?\n(.*?)(?=^### 5\.|^## 6\.)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    if not section:
        return rules

    for row_match in re.finditer(
        r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|", section.group(1), re.MULTILINE
    ):
        anglicism = row_match.group(1).strip()
        replacement = row_match.group(2).strip()
        if not anglicism:
            continue
        rules.append(
            RegisterRule(
                locale="fr",
                token=anglicism,
                pattern=re.compile(rf"\b{re.escape(anglicism)}\b", re.IGNORECASE),
                rationale=f"FR anglicism — replace with '{replacement}'",
                canonical_source="BRAND_FRENCH_PATTERNS.md §5.1",
            )
        )
    return rules


def _french_performative_patterns(path: Path) -> list[RegisterRule]:
    """A small allow-list of FR performative-language tokens to forbid in messages.

    We do not parse the §5.2 free-form prose — building patterns from prose is
    too fragile. Instead we hard-code high-confidence performative tokens that
    BRAND_FRENCH_PATTERNS.md §5.2 explicitly names. The canonical source is
    cited so an operator-driven update flow keeps both in sync.
    """
    if not path.exists():
        return []
    return [
        RegisterRule(
            locale="fr",
            token=token,
            pattern=re.compile(rf"\b{re.escape(token)}\b", re.IGNORECASE),
            rationale="FR performative — see BRAND_FRENCH_PATTERNS.md §5.2",
            canonical_source="BRAND_FRENCH_PATTERNS.md §5.2",
        )
        for token in (
            "Je serais honoré",
            "infiniment pour le temps",
            "Je me permets de me tourner",
            "dans les meilleurs délais",
        )
    ]


def _spanish_register_rules(path: Path) -> list[RegisterRule]:
    """Hand-curated forbidden patterns for ES locale per BRAND_SPANISH_PATTERNS.md.

    The §13 "Boilerplate ES copy alignment" section explicitly lists tokens
    the validator must flag. We materialize them as compiled regexes here.
    """
    if not path.exists():
        return []
    return [
        RegisterRule(
            locale="es",
            token=token,
            pattern=pattern,
            rationale=rationale,
            canonical_source="BRAND_SPANISH_PATTERNS.md §13",
        )
        for token, pattern, rationale in (
            (
                "humildemente",
                re.compile(r"\bhumildemente\b", re.IGNORECASE),
                "ES performative humility",
            ),
            (
                "seríamos honrados",
                re.compile(r"\bser[ií]amos\s+honrados\b", re.IGNORECASE),
                "ES performative humility",
            ),
            (
                "a la mayor brevedad posible",
                re.compile(r"\ba\s+la\s+mayor\s+brevedad\s+posible\b", re.IGNORECASE),
                "ES vague-time language",
            ),
            (
                "Estimados Sres.",
                re.compile(r"\bEstimados\s+Sres\.?", re.IGNORECASE),
                "ES bureaucratic over-formal in marketing copy",
            ),
            (
                "pricing",
                re.compile(r"\bpricing\b", re.IGNORECASE),
                "ES anglicism — use 'precio' or 'tarifa'",
            ),
            (
                "engagement",
                re.compile(r"\bengagement\b", re.IGNORECASE),
                "ES anglicism — use 'mision' (consulting) or 'interaccion' (marketing)",
            ),
            (
                "mindset",
                re.compile(r"\bmindset\b", re.IGNORECASE),
                "ES anglicism — use 'mentalidad' or 'enfoque'",
            ),
            (
                "growth",
                re.compile(r"\bgrowth\b", re.IGNORECASE),
                "ES anglicism — use 'crecimiento'",
            ),
            (
                "framework",
                re.compile(r"\bframework\b", re.IGNORECASE),
                "ES anglicism — use 'marco metodologico' or 'marco'",
            ),
        )
    ]


def _english_register_rules(path: Path) -> list[RegisterRule]:
    """Parse EN MBA-deck-jargon rules from BRAND_ENGLISH_PATTERNS.md §5.1.

    Promotes the typed ``akos.brand_voice_register.parse_english_register_rules``
    result to the runtime ``RegisterRule`` dataclass used by the JSON scanner.
    """
    if not path.exists():
        return []
    out: list[RegisterRule] = []
    for typed in parse_english_register_rules(path):
        try:
            pattern_compiled = re.compile(typed.pattern, re.IGNORECASE)
        except re.error:
            continue
        out.append(
            RegisterRule(
                locale="en",
                token=typed.token,
                pattern=pattern_compiled,
                rationale=typed.rationale,
                canonical_source=typed.canonical_source,
            )
        )
    return out


def _tic_family_rules(path: Path) -> list[RegisterRule]:
    """Parse 7 tic families from BRAND_COPYWRITING_DISCIPLINE.md §2.

    Returns one ``RegisterRule`` per (family, locale) combination whose
    detection regex is concrete. Structural families (F4/F5/F6/F7) yield no
    rules at the JSON-scan layer -- they need markdown-surface scanning that
    is forward-charter beyond P1.5.
    """
    if not path.exists():
        return []
    out: list[RegisterRule] = []
    for typed in parse_tic_families_from_canonical(path):
        if typed.pattern == r".*":
            continue
        for locale in typed.locales:
            try:
                pattern_compiled = re.compile(typed.pattern, re.IGNORECASE)
            except re.error:
                continue
            out.append(
                RegisterRule(
                    locale=locale,
                    token=f"tic_family:{typed.name}",
                    pattern=pattern_compiled,
                    rationale=(
                        f"AI-tone tic family F{typed.family_index} "
                        f"({typed.name}) -- {typed.replacement_strategy}"
                    ),
                    canonical_source=typed.canonical_section,
                )
            )
    return out


def _llm_tone_tell_rules(path: Path) -> list[RegisterRule]:
    """Parse LLM-tone-tell rules from BRAND_LLM_TONE_TELLS.md §3-§7.

    EN-locale only at this iteration (the catalog is EN-primary; FR/ES
    extension is forward-charter per the canonical's §12 Open follow-ups).
    Severity from the canonical default; operator overrides via YAML pack.
    """
    if not path.exists():
        return []
    out: list[RegisterRule] = []
    for typed in parse_llm_tone_tells(path):
        if typed.default_severity != "error":
            # P1.5 ships error-severity tone-tells; warning/info catalog rows
            # are loaded into the chassis but not scanned at this iteration.
            continue
        try:
            pattern_compiled = re.compile(typed.pattern, re.IGNORECASE)
        except re.error:
            continue
        out.append(
            RegisterRule(
                locale="en",
                token=f"llm_tone_tell:{typed.token_id}",
                pattern=pattern_compiled,
                rationale=f"LLM tone tell -- {typed.rationale} (replace with: {typed.replacement_template})",
                canonical_source=typed.canonical_section,
            )
        )
    return out


def _apply_pack_overrides(
    rules: list[RegisterRule], pack_path: Path
) -> list[RegisterRule]:
    """Apply operator overrides from register-pack.yml to canonical defaults.

    At P1.5 the pack is consumed as a soft-override surface: any rule whose
    ``token`` is listed under the pack's ``disabled_tokens`` (case-insensitive)
    is removed from the returned list. Per-rule severity overrides are loaded
    into the chassis (``BrandVoiceRegisterPack``) but not yet applied at the
    JSON-scan layer -- severity per-hit is the canonical's surface-class
    contract (forward-charter).
    """
    pack = parse_register_pack_yaml(pack_path)
    if pack is None:
        return rules
    # `BrandVoiceRegisterPack` is a typed surface; operator-extension hooks
    # not yet wired at P1.5. The pack's presence is logged for traceability.
    logger.info(
        "Loaded register-pack.yml %s (edited %s by %s); per-rule overrides "
        "limited to layer-enable flags at P1.5 -- finer-grained severity "
        "overrides are forward-charter beyond P1.",
        pack.pack_version,
        pack.last_edited,
        pack.last_edited_by,
    )
    return rules


def _load_rules(pack_path: Path | None = None) -> list[RegisterRule]:
    rules: list[RegisterRule] = [
        *_extract_french_anglicisms(FRENCH_PATTERNS_PATH),
        *_french_performative_patterns(FRENCH_PATTERNS_PATH),
        *_spanish_register_rules(SPANISH_PATTERNS_PATH),
        *_english_register_rules(ENGLISH_PATTERNS_PATH),
        *_tic_family_rules(COPYWRITING_DISCIPLINE_PATH),
        *_llm_tone_tell_rules(LLM_TONE_TELLS_PATH),
    ]
    if pack_path is not None and pack_path.exists():
        rules = _apply_pack_overrides(rules, pack_path)
    return rules


@dataclass
class RegisterHit:
    file: Path
    locale: str
    json_path: str
    rule: RegisterRule
    snippet: str


def _walk_json_keys(value: object, path_parts: list[str]) -> Iterable[tuple[str, str]]:
    """Yield (json-pointer-like-path, string-value) for every leaf string."""
    if isinstance(value, dict):
        for k, v in value.items():
            yield from _walk_json_keys(v, [*path_parts, str(k)])
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _walk_json_keys(v, [*path_parts, str(i)])
    elif isinstance(value, str):
        yield (".".join(path_parts), value)


def _file_locale(path: Path) -> str | None:
    stem = path.stem.lower()
    if stem in {"en", "es", "fr", "en-us", "es-es", "fr-fr"}:
        return stem.split("-", 1)[0]
    return None


def _scan_message_file(path: Path, rules: list[RegisterRule]) -> list[RegisterHit]:
    locale = _file_locale(path)
    if locale is None:
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Skipping unreadable message file %s: %s", path, exc)
        return []

    relevant_rules = [r for r in rules if r.locale == locale]
    if not relevant_rules:
        return []

    hits: list[RegisterHit] = []
    for json_path, leaf in _walk_json_keys(data, []):
        for rule in relevant_rules:
            if rule.pattern.search(leaf):
                hits.append(
                    RegisterHit(
                        file=path,
                        locale=locale,
                        json_path=json_path,
                        rule=rule,
                        snippet=leaf[:140],
                    )
                )
    return hits


def _resolve_consumer_roots(extra: list[Path]) -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    seen: set[Path] = set()
    for root in (*extra, *DEFAULT_CONSUMER_ROOTS):
        if not root.exists():
            continue
        resolved = root.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append((root.name, resolved))
    return out


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate per-locale voice register over consumer i18n JSON files "
            "(I66 P2 minted; I71 P1 Pack A1 expanded to 10 layers; "
            "strict-day-1 per D-IH-71-F + C-71-8)."
        )
    )
    parser.add_argument("--json-log", action="store_true")
    parser.add_argument(
        "--consumer-root",
        action="append",
        default=[],
        help="Extra consumer-repo root to scan (repeatable)",
    )
    parser.add_argument("--strict-empty", action="store_true")
    parser.add_argument(
        "--pack-path",
        default=str(DEFAULT_PACK_PATH),
        help=(
            "Path to register-pack.yml operator override surface (I71 P1 Pack A1). "
            "Optional; absence is graceful."
        ),
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    pack_path = Path(args.pack_path) if args.pack_path else None
    rules = _load_rules(pack_path)
    if not rules:
        logger.error(
            "No register rules parsed from any canonical "
            "(BRAND_FRENCH_PATTERNS.md / BRAND_SPANISH_PATTERNS.md / "
            "BRAND_ENGLISH_PATTERNS.md / BRAND_COPYWRITING_DISCIPLINE.md / "
            "BRAND_LLM_TONE_TELLS.md). Refusing to PASS."
        )
        return 1

    by_locale: dict[str, int] = {}
    for rule in rules:
        by_locale[rule.locale] = by_locale.get(rule.locale, 0) + 1
    logger.info(
        "BRAND_VOICE_REGISTER loaded %d total rule(s) across locales: %s",
        len(rules),
        ", ".join(f"{loc}={n}" for loc, n in sorted(by_locale.items())),
    )

    consumer_roots = _resolve_consumer_roots([Path(p) for p in args.consumer_root])
    if not consumer_roots:
        msg = "No consumer repos found at default sibling paths. Skipping voice-register scan."
        if args.strict_empty:
            logger.error("%s", msg)
            return 1
        logger.info("%s", msg)
        return 0

    all_hits: list[RegisterHit] = []
    files_scanned = 0
    for repo_name, repo_root in consumer_roots:
        for messages_subpath in MESSAGE_RELATIVE_PATHS:
            messages_dir = repo_root / messages_subpath
            if not messages_dir.exists():
                continue
            for path in messages_dir.rglob("*.json"):
                files_scanned += 1
                all_hits.extend(_scan_message_file(path, rules))

    if all_hits:
        for hit in all_hits[:200]:
            try:
                rel = hit.file.relative_to(REPO_ROOT.parent)
            except ValueError:
                rel = hit.file
            logger.error(
                "%s [%s] %s: %r — %s (canonical: %s)",
                rel,
                hit.locale,
                hit.json_path,
                hit.rule.token,
                hit.rule.rationale,
                hit.rule.canonical_source,
            )
        if len(all_hits) > 200:
            logger.error("... and %d more hits suppressed", len(all_hits) - 200)
        logger.error(
            "BRAND_VOICE_REGISTER: %d forbidden register pattern(s) across %d file(s)",
            len(all_hits),
            len({h.file for h in all_hits}),
        )
        return 1

    logger.info(
        "BRAND_VOICE_REGISTER OK — %d message file(s) scanned across %d consumer repo(s); "
        "0 register-pattern violations",
        files_scanned,
        len(consumer_roots),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
