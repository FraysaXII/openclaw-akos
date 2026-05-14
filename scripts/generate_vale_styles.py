#!/usr/bin/env python3
"""Generate Vale style files from Holistika brand canonicals (I71 P2 Tier 1 Vale sibling).

Reads brand canonicals via ``akos.brand_voice_register`` parsers + ``CANONICAL_PATHS``
and emits deterministic Vale style + per-canonical Vocab files at:

- ``.vale/styles/Holistika/LLMToneTells.yml``    -- from BRAND_LLM_TONE_TELLS.md
- ``.vale/styles/Holistika/TicFamilies.yml``     -- from BRAND_COPYWRITING_DISCIPLINE.md §2
- ``.vale/styles/Holistika/MBADeckJargon.yml``   -- from BRAND_ENGLISH_PATTERNS.md §5.1
- ``.vale/styles/Vocab/Holistika-CopywritingDiscipline.txt``           -- accept (Holistika sub-marks)
- ``.vale/styles/Vocab/Holistika-CopywritingDiscipline-rejected.txt``  -- reject (tic-family canonical absent → empty)
- ``.vale/styles/Vocab/Holistika-EnglishPatterns.txt``                 -- accept (minimal EN-specific)
- ``.vale/styles/Vocab/Holistika-EnglishPatterns-rejected.txt``        -- reject (MBA-deck jargon)
- ``.vale/styles/Vocab/Holistika-LLMToneTells.txt``                    -- accept (empty)
- ``.vale/styles/Vocab/Holistika-LLMToneTells-rejected.txt``           -- reject (LLM tone tells)
- ``.vale/styles/Vocab/Holistika-FrenchPatterns.txt``                  -- accept (FR brand surface)
- ``.vale/styles/Vocab/Holistika-FrenchPatterns-rejected.txt``         -- reject (FR anglicisms + performative)
- ``.vale/styles/Vocab/Holistika-SpanishPatterns.txt``                 -- accept (ES brand surface)
- ``.vale/styles/Vocab/Holistika-SpanishPatterns-rejected.txt``        -- reject (ES anglicisms + performative)

The per-canonical Vocab strategy was ratified at the C-71-Vale-2 inline-ratify
gate (2026-05-14): each brand canonical maintains its own accept/reject pair so
canonical edits regenerate one localised pair rather than the global Holistika
pair. The Vocab packages list lives in `.vale.ini`'s ``Vocab =`` line.

Determinism contract::

    Two invocations against the same canonical inputs produce byte-identical
    output (UTF-8, LF line endings, no BOM, sorted dict keys + list items).
    The ``--check`` mode exits 1 if any generated file would change vs the
    on-disk copy (CI-friendly drift detection).

CLI::

    py scripts/generate_vale_styles.py            # write the files
    py scripts/generate_vale_styles.py --dry-run  # print would-write paths only
    py scripts/generate_vale_styles.py --check    # exit 1 if any file would change
    py scripts/generate_vale_styles.py --clean    # rm -rf .vale/styles/Vocab before regenerating

Cross-references::

    BRAND_COPYWRITING_DISCIPLINE.md §2 -- 7 AI-tone tic families (TicFamilies.yml).
    BRAND_LLM_TONE_TELLS.md           -- LLM-default lexical patterns (LLMToneTells.yml).
    BRAND_ENGLISH_PATTERNS.md §5.1    -- MBA-deck jargon refuse-list (MBADeckJargon.yml).
    BRAND_FRENCH_PATTERNS.md §5.1+§5.2 -- FR anglicisms + performative (Vocab only).
    BRAND_SPANISH_PATTERNS.md         -- ES anglicisms + performative (Vocab only).
    akos/brand_voice_register.py      -- chassis (Pydantic models + parsers).
    .vale.ini                          -- repo-root config (StylesPath = .vale/styles).
    I71 P2 plan §P2 Step 2d           -- Tier 1 Vale sibling architecture.
    D-IH-71-O                          -- Tier 1 Vale sibling ratification.
    C-71-Vale-2                        -- per-canonical Vocab ratification 2026-05-14.
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.brand_voice_register import (  # noqa: E402
    CANONICAL_PATHS,
    LLMToneTell,
    RegisterRule,
    TicFamily,
    parse_english_register_rules,
    parse_llm_tone_tells,
    parse_tic_families_from_canonical,
)
from akos.io import REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

logger = logging.getLogger("akos.generate_vale_styles")

# ---------------------------------------------------------------------------
# Paths -- stable, repo-rooted, never absolute on the operator's host
# ---------------------------------------------------------------------------

VALE_ROOT = REPO_ROOT / ".vale"
STYLES_DIR = VALE_ROOT / "styles"
HOLISTIKA_STYLES_DIR = STYLES_DIR / "Holistika"
VOCAB_DIR = STYLES_DIR / "Vocab"

LLM_TONE_TELLS_PATH = HOLISTIKA_STYLES_DIR / "LLMToneTells.yml"
TIC_FAMILIES_PATH = HOLISTIKA_STYLES_DIR / "TicFamilies.yml"
MBA_DECK_JARGON_PATH = HOLISTIKA_STYLES_DIR / "MBADeckJargon.yml"

# Per-canonical Vocab pair paths (10 files; 5 accept + 5 reject) per C-71-Vale-2
VOCAB_COPYWRITING_ACCEPT_PATH = VOCAB_DIR / "Holistika-CopywritingDiscipline.txt"
VOCAB_COPYWRITING_REJECT_PATH = VOCAB_DIR / "Holistika-CopywritingDiscipline-rejected.txt"
VOCAB_ENGLISH_ACCEPT_PATH = VOCAB_DIR / "Holistika-EnglishPatterns.txt"
VOCAB_ENGLISH_REJECT_PATH = VOCAB_DIR / "Holistika-EnglishPatterns-rejected.txt"
VOCAB_LLM_ACCEPT_PATH = VOCAB_DIR / "Holistika-LLMToneTells.txt"
VOCAB_LLM_REJECT_PATH = VOCAB_DIR / "Holistika-LLMToneTells-rejected.txt"
VOCAB_FRENCH_ACCEPT_PATH = VOCAB_DIR / "Holistika-FrenchPatterns.txt"
VOCAB_FRENCH_REJECT_PATH = VOCAB_DIR / "Holistika-FrenchPatterns-rejected.txt"
VOCAB_SPANISH_ACCEPT_PATH = VOCAB_DIR / "Holistika-SpanishPatterns.txt"
VOCAB_SPANISH_REJECT_PATH = VOCAB_DIR / "Holistika-SpanishPatterns-rejected.txt"

# ---------------------------------------------------------------------------
# Per-canonical accept-list curation
#
# Each accept-list is the set of brand-specific terms that legitimately appear
# when this canonical applies. Per C-71-Vale-2 ratification: copywriting carries
# the Holistika sub-mark surface (the canonical names appear in any brand-voice
# example); EN/LLM-tone are intentionally minimal (LLM rejects are universal,
# not locale-specific); FR/ES carry FR/ES-specific brand surface tokens.
# ---------------------------------------------------------------------------

_HOLISTIKA_SUB_MARKS: tuple[str, ...] = (
    "AKOS",
    "FraysaXII",
    "HLK",
    "Holistika",
    "Holistika Research",
    "Holistika Tech Lab",
    "KiRBe",
    "MADEIRA",
    "Njoya",
    "OpenCLAW",
    "SUEZ",
)

ACCEPT_LIST_BY_CANONICAL: dict[str, tuple[str, ...]] = {
    # CopywritingDiscipline canonical: brand sub-mark names appear throughout
    # the prose examples; this is where the brand-name surface lives.
    "copywriting": _HOLISTIKA_SUB_MARKS,
    # EnglishPatterns canonical: minimal accepts; the canonical's job is to
    # codify EN MBA-deck jargon refuse-list, not to enumerate brand surface.
    # Keep only the umbrella + AKOS (used in operator-side technical prose).
    "english": ("AKOS", "HLK", "Holistika", "OpenCLAW"),
    # LLMToneTells canonical: empty accepts. LLM-default lexical patterns are
    # universal; no brand-specific allowlist applies at this layer.
    "llm": (),
    # FrenchPatterns canonical: brand surface that legitimately appears in FR
    # prose. "Asesoría" stays under SpanishPatterns (different accent + locale).
    "french": ("FraysaXII", "Holistika", "Holistika Research", "Njoya"),
    # SpanishPatterns canonical: ES-specific brand surface, including the
    # accented "Asesoría" sub-mark name.
    "spanish": ("Asesoría", "FraysaXII", "Holistika", "Holistika Research", "Njoya"),
}


# ---------------------------------------------------------------------------
# Vale severity mapping (chassis Severity -> Vale level)
# ---------------------------------------------------------------------------

_VALE_LEVEL_MAP: dict[str, str] = {
    "error": "error",
    "warning": "warning",
    "info": "suggestion",
}


def _vale_level(chassis_severity: str) -> str:
    """Map chassis Severity Literal to Vale level keyword.

    Vale recognises ``suggestion`` / ``warning`` / ``error``; the chassis uses
    ``info`` / ``warning`` / ``error``. Map ``info`` to ``suggestion``.
    """
    return _VALE_LEVEL_MAP.get(chassis_severity, "warning")


# ---------------------------------------------------------------------------
# Deterministic file writer (UTF-8, LF, no BOM)
# ---------------------------------------------------------------------------


def _write_deterministic(path: Path, contents: str) -> None:
    """Write ``contents`` to ``path`` with deterministic UTF-8 + LF line endings.

    Creates parent directories when needed. No BOM. Output is byte-identical
    across platforms when the contents string is identical.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = contents.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(encoded)


def _file_hash(path: Path) -> str:
    """Return sha256 hex of ``path`` contents, or empty string when absent."""
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _content_hash(contents: str) -> str:
    return hashlib.sha256(contents.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Vale-YAML synthesis helpers (no PyYAML; emit canonical text directly so the
# determinism contract is independent of the yaml library's dump preferences)
# ---------------------------------------------------------------------------


def _yaml_quote(s: str) -> str:
    """Return a YAML-safe double-quoted string literal.

    Escapes embedded backslashes + double-quotes; does not attempt to
    minimize escaping. Newlines in input are converted to ``\\n`` (rare).
    """
    escaped = (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )
    return f'"{escaped}"'


def _file_header_comment(canonical_label: str, source_paths: tuple[str, ...]) -> str:
    """Return a header comment block for a generated Vale style file."""
    lines = [
        "# Generated by scripts/generate_vale_styles.py -- DO NOT EDIT BY HAND.",
        "#",
        f"# Brand source: {canonical_label}",
        "# Regenerate via: py scripts/generate_vale_styles.py",
        "#",
        "# Canonical inputs:",
    ]
    for source in source_paths:
        lines.append(f"#   - {source}")
    lines.extend(
        [
            "#",
            "# I71 P2 Pack A2 Tier 1 Vale sibling. Plan reference:",
            "#   .cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_a71c0d6e.plan.md",
            "#   docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md",
            "",
        ]
    )
    return "\n".join(lines)


def _vocab_header_comment(label: str) -> str:
    return (
        "# Generated by scripts/generate_vale_styles.py -- DO NOT EDIT BY HAND.\n"
        f"# {label}\n"
        "# Regenerate via: py scripts/generate_vale_styles.py\n"
    )


# ---------------------------------------------------------------------------
# Style generators
# ---------------------------------------------------------------------------


def _placeholder_style(file_label: str, missing_canonical: str) -> str:
    """Return a graceful-skip placeholder style file.

    Emitted when the canonical source is absent on disk. Uses
    ``extends: existence`` with an empty token list so Vale loads the file
    without error but emits zero hits.
    """
    header = _file_header_comment(
        canonical_label=file_label,
        source_paths=(missing_canonical + " (ABSENT at generation time)",),
    )
    body = (
        "extends: existence\n"
        "message: \"placeholder -- canonical absent at generation time\"\n"
        "level: suggestion\n"
        "ignorecase: true\n"
        "tokens: []\n"
    )
    return header + body


def _llm_tone_tells_style(rules: list[LLMToneTell]) -> str:
    """Synthesize ``LLMToneTells.yml`` from the parsed ``LLMToneTell`` rule list.

    Single ``extends: substitution`` style with a sorted-key ``swap:`` dict.
    Each LLM tell maps the regex pattern to the canonical replacement
    template; severity uses the highest-severity hit across the input list
    (``error`` if any error-severity hit; else ``warning``; else
    ``suggestion``) so a single Vale rule expresses the catalog conservatively.
    """
    header = _file_header_comment(
        canonical_label="BRAND_LLM_TONE_TELLS.md (anti-LLM-tone catalog)",
        source_paths=(CANONICAL_PATHS["llm_tone_tells"],),
    )
    if not rules:
        return _placeholder_style(
            file_label="BRAND_LLM_TONE_TELLS.md (anti-LLM-tone catalog)",
            missing_canonical=CANONICAL_PATHS["llm_tone_tells"],
        )
    severities = {rule.default_severity for rule in rules}
    if "error" in severities:
        worst_severity = "error"
    elif "warning" in severities:
        worst_severity = "warning"
    else:
        worst_severity = "info"
    swap_pairs: dict[str, str] = {}
    for rule in rules:
        swap_pairs[rule.pattern] = rule.replacement_template
    body_lines = [
        "extends: substitution",
        "message: \"Holistika LLM tone tell -- '%s' reads as automated; consider '%s'.\"",
        f"level: {_vale_level(worst_severity)}",
        f"link: {CANONICAL_PATHS['llm_tone_tells']}",
        "ignorecase: true",
        "nonword: false",
        "swap:",
    ]
    for key in sorted(swap_pairs):
        body_lines.append(f"  {_yaml_quote(key)}: {_yaml_quote(swap_pairs[key])}")
    return header + "\n".join(body_lines) + "\n"


def _tic_families_style(families: list[TicFamily]) -> str:
    """Synthesize ``TicFamilies.yml`` from parsed ``TicFamily`` instances.

    Tic families with a real detection regex (F1-F3, F6, F7) become
    ``extends: existence`` tokens (regex matches a sentence shape; no plain
    substitution available); structural families (F4 / F5) are documented as
    a comment but emit no tokens (their detection requires multi-line
    inspection that Vale's regex engine cannot express).
    """
    header = _file_header_comment(
        canonical_label="BRAND_COPYWRITING_DISCIPLINE.md §2 (7 AI-tone tic families)",
        source_paths=(CANONICAL_PATHS["copywriting_discipline"],),
    )
    if not families:
        return _placeholder_style(
            file_label="BRAND_COPYWRITING_DISCIPLINE.md §2 (7 AI-tone tic families)",
            missing_canonical=CANONICAL_PATHS["copywriting_discipline"],
        )
    pattern_set: set[str] = set()
    for family in families:
        pattern = family.pattern
        if pattern == r".*":
            # Structural family (F4 / F5) -- skip; commented as note in body.
            continue
        pattern_set.add(pattern)
    body_lines = [
        "extends: existence",
        "message: \"Holistika tic-family hit -- inspect for AI-tone (see BRAND_COPYWRITING_DISCIPLINE.md §2).\"",
        "level: warning",
        f"link: {CANONICAL_PATHS['copywriting_discipline']}",
        "ignorecase: true",
        "nonword: true",
        "tokens:",
    ]
    if not pattern_set:
        body_lines.append("  []")
    else:
        for pattern in sorted(pattern_set):
            body_lines.append(f"  - {_yaml_quote(pattern)}")
    body_lines.append("")
    body_lines.append(
        "# Note: structural families F4 (triadic abstract-noun stack) and F5 (`discipline`"
    )
    body_lines.append(
        "# overuse) are not expressible as single-line Vale regex; the regex chassis at"
    )
    body_lines.append(
        "# scripts/validate_brand_voice_register.py handles them via custom detection."
    )
    return header + "\n".join(body_lines) + "\n"


def _mba_deck_jargon_style(rules: list[RegisterRule]) -> str:
    """Synthesize ``MBADeckJargon.yml`` from the EN MBA-deck-jargon table.

    ``extends: substitution`` with a sorted-key ``swap:`` dict. The chassis's
    ``parse_english_register_rules`` parses the table at
    ``BRAND_ENGLISH_PATTERNS.md §5.1``; each row yields a ``RegisterRule``
    whose rationale carries the canonical replacement (parsed via the
    surrounding text "replace with 'X'").
    """
    header = _file_header_comment(
        canonical_label="BRAND_ENGLISH_PATTERNS.md §5.1 (MBA-deck jargon refuse-list)",
        source_paths=(CANONICAL_PATHS["english_patterns"],),
    )
    if not rules:
        return _placeholder_style(
            file_label="BRAND_ENGLISH_PATTERNS.md §5.1 (MBA-deck jargon refuse-list)",
            missing_canonical=CANONICAL_PATHS["english_patterns"],
        )
    swap_pairs: dict[str, str] = {}
    for rule in rules:
        if rule.locale != "en":
            continue
        replacement = _extract_replacement_from_rationale(rule.rationale) or "use plain English"
        swap_pairs[rule.pattern] = replacement
    body_lines = [
        "extends: substitution",
        "message: \"Holistika MBA-deck jargon -- '%s' reads as template; consider '%s'.\"",
        "level: warning",
        f"link: {CANONICAL_PATHS['english_patterns']}",
        "ignorecase: true",
        "nonword: false",
        "swap:",
    ]
    if not swap_pairs:
        body_lines.append("  {}")
    else:
        for key in sorted(swap_pairs):
            body_lines.append(f"  {_yaml_quote(key)}: {_yaml_quote(swap_pairs[key])}")
    return header + "\n".join(body_lines) + "\n"


def _extract_replacement_from_rationale(rationale: str) -> str | None:
    """Return the replacement phrase from a ``RegisterRule`` rationale text.

    The chassis's parser builds rationale strings of the shape
    ``EN MBA-deck jargon -- replace with 'X' (Y)`` where X is the operator's
    suggested replacement and Y is the canonical's free-text rationale. We
    extract X conservatively; falls back to ``None`` on a parse miss so the
    caller emits a sane default.
    """
    marker = "replace with '"
    idx = rationale.find(marker)
    if idx == -1:
        return None
    rest = rationale[idx + len(marker) :]
    end = rest.find("'")
    if end == -1:
        return None
    return rest[:end].strip() or None


# ---------------------------------------------------------------------------
# FR / ES anglicism extraction
#
# The chassis exposes parse_english_register_rules + parse_llm_tone_tells but
# does NOT expose FR/ES parsers (the live FR/ES rule loaders live in
# scripts/validate_brand_voice_register.py as private helpers). To keep this
# generator independent of that script's import surface, we inline minimal
# parsers here that mirror the §5.1 anglicism-table shape used in the FR
# canonical and the equivalent §13 / patterns-to-refuse table in ES.
#
# Tokens are surface forms (operator-readable) rather than regex patterns;
# Vale's Vocab files are plain text, one token per line.
# ---------------------------------------------------------------------------

_FR_ANGLICISM_ROW_RE = re.compile(
    r"^\|\s*`([^`]+)`\s*\|",
    re.MULTILINE,
)


def _parse_french_anglicism_tokens(path: Path) -> list[str]:
    """Return the list of FR anglicism + performative-FR tokens from BRAND_FRENCH_PATTERNS.md.

    Parses the §5.1 anglicism table for the left-column tokens, then appends
    the §5.2 performative-FR + §5.3 corporate-filler patterns (literal phrases
    extracted from the canonical's bullet list). Returns ``[]`` when the
    canonical is absent (graceful skip).

    The shape mirrors the chassis's ``parse_english_register_rules`` for the
    EN equivalent (BRAND_ENGLISH_PATTERNS.md §5.1), but FR has additional
    performative + filler patterns the chassis does not codify because the
    operator-facing scripts/validate_brand_voice_register.py keeps them as
    hand-curated literal patterns.
    """
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")

    section_51 = re.search(
        r"^### 5\.1 Anglicisms.*?\n(.*?)(?=^### 5\.|^## 6\.)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    tokens: set[str] = set()
    if section_51:
        for row_match in _FR_ANGLICISM_ROW_RE.finditer(section_51.group(1)):
            token = row_match.group(1).strip()
            # Drop parenthetical context (e.g., "process (singular)" -> "process")
            token = re.sub(r"\s*\(.*?\)\s*$", "", token).strip()
            if token and not token.startswith("Anglicism"):
                tokens.add(token)

    # Performative FR patterns (§5.2 bullet list literals; canonical phrasing).
    performative_fr: tuple[str, ...] = (
        "Je serais honoré de pouvoir collaborer avec vous",
        "Je vous remercie infiniment",
        "Je me permets de me tourner vers vous",
        "dans les meilleurs délais",
    )
    tokens.update(performative_fr)

    # Empty corporate filler (§5.3 bullet list literals).
    filler_fr: tuple[str, ...] = (
        "Dans le cadre de nos échanges",
        "Étant entendu que",
        "Pour faire court",
    )
    tokens.update(filler_fr)
    return sorted(tokens, key=str.lower)


_ES_ANGLICISM_LITERALS: tuple[str, ...] = (
    # Hand-curated mirror of scripts/validate_brand_voice_register.py
    # _spanish_register_rules tokens. Operator-readable surface forms.
    "approach",
    "de-riskear",
    "engagement",
    "framework",
    "growth",
    "mindset",
    "pricing",
    # Performative ES from BRAND_SPANISH_PATTERNS.md §"Patterns to refuse".
    "Sería un honor poder colaborar con usted",
    "Le agradezco infinitamente",
    "En el contexto de nuestras conversaciones",
    "consulta el pricing",
)


def _parse_spanish_anglicism_tokens(path: Path) -> list[str]:
    """Return the list of ES anglicism + performative-ES tokens.

    Mirrors the hand-curated list in
    ``scripts/validate_brand_voice_register.py::_spanish_register_rules``
    (the canonical's §"Patterns to refuse" + the operator-curated anglicism
    list). Returns ``[]`` when the canonical is absent.
    """
    if not path.exists():
        return []
    return sorted(set(_ES_ANGLICISM_LITERALS), key=str.lower)


# ---------------------------------------------------------------------------
# Vocab synthesis (per-canonical pairs per C-71-Vale-2)
# ---------------------------------------------------------------------------


def _strip_word_boundary_regex(pattern: str) -> str:
    """Return the literal token text from a chassis-style ``\\b<re.escape token>\\b`` regex.

    Falls back to the raw pattern on any unexpected shape so the reject-list
    never silently loses a token.
    """
    if pattern.startswith(r"\b") and pattern.endswith(r"\b"):
        inner = pattern[2:-2]
        # re.escape leaves alphanumerics + underscore alone but escapes most
        # punctuation as ``\X``. Reverse the common escapes for human reading.
        unescaped: list[str] = []
        i = 0
        while i < len(inner):
            ch = inner[i]
            if ch == "\\" and i + 1 < len(inner):
                unescaped.append(inner[i + 1])
                i += 2
            else:
                unescaped.append(ch)
                i += 1
        return "".join(unescaped)
    return pattern


def _accept_vocab(canonical_key: str, label: str) -> str:
    """Return per-canonical accept-list contents (sorted; LF endings)."""
    header = _vocab_header_comment(label)
    tokens = sorted(set(ACCEPT_LIST_BY_CANONICAL.get(canonical_key, ())))
    body = "\n".join(tokens) + ("\n" if tokens else "")
    return header + body


def _reject_vocab(label: str, tokens: list[str]) -> str:
    """Return a reject-list file body (sorted case-insensitively; LF endings)."""
    header = _vocab_header_comment(label)
    sorted_tokens = sorted(set(t for t in tokens if t), key=str.lower)
    body = "\n".join(sorted_tokens) + ("\n" if sorted_tokens else "")
    return header + body


def _copywriting_reject_tokens(_families: list[TicFamily]) -> list[str]:
    """Return the BRAND_COPYWRITING_DISCIPLINE reject tokens.

    Tic families are detected via regex shapes (Vale style YAML), not surface
    tokens. This canonical's reject vocab therefore carries no tokens by
    design; the rejection surface is the TicFamilies.yml style file. Returning
    an empty list keeps the file emission deterministic + non-empty (header
    only).
    """
    return []


def _english_reject_tokens(rules: list[RegisterRule]) -> list[str]:
    return [r.token for r in rules if r.token]


def _llm_reject_tokens(rules: list[LLMToneTell]) -> list[str]:
    out: list[str] = []
    for rule in rules:
        token_text = _strip_word_boundary_regex(rule.pattern)
        if token_text:
            out.append(token_text)
    return out


# ---------------------------------------------------------------------------
# Generation orchestration
# ---------------------------------------------------------------------------


def _build_outputs() -> dict[Path, str]:
    """Return a deterministic dict of {path: contents} for every generated file."""
    llm_tells = parse_llm_tone_tells(REPO_ROOT / CANONICAL_PATHS["llm_tone_tells"])
    tic_families = parse_tic_families_from_canonical(
        REPO_ROOT / CANONICAL_PATHS["copywriting_discipline"]
    )
    en_rules = parse_english_register_rules(
        REPO_ROOT / CANONICAL_PATHS["english_patterns"]
    )
    fr_tokens = _parse_french_anglicism_tokens(
        REPO_ROOT / CANONICAL_PATHS["french_patterns"]
    )
    es_tokens = _parse_spanish_anglicism_tokens(
        REPO_ROOT / CANONICAL_PATHS["spanish_patterns"]
    )

    outputs: dict[Path, str] = {
        # Style files (3) -- unchanged from C-71-Vale-2 ratification.
        LLM_TONE_TELLS_PATH: _llm_tone_tells_style(llm_tells),
        TIC_FAMILIES_PATH: _tic_families_style(tic_families),
        MBA_DECK_JARGON_PATH: _mba_deck_jargon_style(en_rules),
        # Per-canonical Vocab pairs (10 files; 5 accept + 5 reject).
        VOCAB_COPYWRITING_ACCEPT_PATH: _accept_vocab(
            "copywriting",
            "Holistika CopywritingDiscipline accept-list "
            "(brand sub-mark surface from BRAND_COPYWRITING_DISCIPLINE.md).",
        ),
        VOCAB_COPYWRITING_REJECT_PATH: _reject_vocab(
            "Holistika CopywritingDiscipline reject-list "
            "(tic-family detection lives in TicFamilies.yml; vocab empty by design).",
            _copywriting_reject_tokens(tic_families),
        ),
        VOCAB_ENGLISH_ACCEPT_PATH: _accept_vocab(
            "english",
            "Holistika EnglishPatterns accept-list "
            "(EN-specific brand surface from BRAND_ENGLISH_PATTERNS.md).",
        ),
        VOCAB_ENGLISH_REJECT_PATH: _reject_vocab(
            "Holistika EnglishPatterns reject-list "
            "(MBA-deck jargon from BRAND_ENGLISH_PATTERNS.md §5.1).",
            _english_reject_tokens(en_rules),
        ),
        VOCAB_LLM_ACCEPT_PATH: _accept_vocab(
            "llm",
            "Holistika LLMToneTells accept-list "
            "(empty by design; LLM-default lexical patterns are universal, "
            "no brand-specific allowlist applies).",
        ),
        VOCAB_LLM_REJECT_PATH: _reject_vocab(
            "Holistika LLMToneTells reject-list "
            "(LLM-default lexical patterns from BRAND_LLM_TONE_TELLS.md §3-§7).",
            _llm_reject_tokens(llm_tells),
        ),
        VOCAB_FRENCH_ACCEPT_PATH: _accept_vocab(
            "french",
            "Holistika FrenchPatterns accept-list "
            "(FR brand surface that legitimately appears in French prose).",
        ),
        VOCAB_FRENCH_REJECT_PATH: _reject_vocab(
            "Holistika FrenchPatterns reject-list "
            "(FR anglicisms + performative-FR + corporate filler "
            "from BRAND_FRENCH_PATTERNS.md §5.1-§5.3).",
            fr_tokens,
        ),
        VOCAB_SPANISH_ACCEPT_PATH: _accept_vocab(
            "spanish",
            "Holistika SpanishPatterns accept-list "
            "(ES brand surface, including the accented Asesoría sub-mark).",
        ),
        VOCAB_SPANISH_REJECT_PATH: _reject_vocab(
            "Holistika SpanishPatterns reject-list "
            "(ES anglicisms + performative-ES from BRAND_SPANISH_PATTERNS.md "
            "§Patterns to refuse).",
            es_tokens,
        ),
    }
    return outputs


def write_styles(
    target_root: Path | None = None, clean: bool = False
) -> dict[Path, str]:
    """Write all Vale style files; return the {path: contents} map for callers.

    ``target_root`` lets tests redirect output to ``tmp_path`` without touching
    the real repo. When ``None`` (default), writes to the canonical
    ``REPO_ROOT/.vale/`` location.

    ``clean=True`` removes ``<root>/.vale/styles/Vocab/`` before regenerating
    so stale Vocab files (e.g., the pre-C-71-Vale-2 single-pair files
    ``Holistika.txt`` + ``Holistika-rejected.txt``) are not left behind.
    """
    outputs = _build_outputs()
    if target_root is not None:
        outputs = _retarget_outputs(outputs, target_root)
    if clean:
        if target_root is None:
            vocab_root = VOCAB_DIR
        else:
            vocab_root = target_root / VOCAB_DIR.relative_to(REPO_ROOT)
        if vocab_root.exists():
            shutil.rmtree(vocab_root)
    for path, contents in outputs.items():
        _write_deterministic(path, contents)
    return outputs


def _retarget_outputs(
    outputs: dict[Path, str], target_root: Path
) -> dict[Path, str]:
    """Rewrite output keys to live under ``target_root/.vale/`` for tests."""
    new_outputs: dict[Path, str] = {}
    for path, contents in outputs.items():
        relative = path.relative_to(REPO_ROOT)
        new_outputs[target_root / relative] = contents
    return new_outputs


def check_styles() -> tuple[bool, list[Path]]:
    """Return ``(in_sync, drifted_paths)`` without writing.

    ``in_sync`` is True only when every generated file matches its on-disk
    sha256. Useful as a CI drift gate so a stale ``.vale/styles/...`` blocks
    a PR until the operator regenerates.
    """
    outputs = _build_outputs()
    drifted: list[Path] = []
    for path, contents in outputs.items():
        if _file_hash(path) != _content_hash(contents):
            drifted.append(path)
    return (not drifted, drifted)


def dry_run() -> dict[Path, str]:
    """Return the {path: contents} map without writing; useful for inspection."""
    return _build_outputs()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate Vale style files from Holistika brand canonicals."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if any generated file would change vs the on-disk copy.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the would-write paths + line counts; do not write to disk.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help=(
            "Remove .vale/styles/Vocab/ before regenerating to drop stale Vocab "
            "files (e.g., pre-C-71-Vale-2 single-pair Holistika.txt / "
            "Holistika-rejected.txt). No effect with --check / --dry-run."
        ),
    )
    parser.add_argument("--json-log", action="store_true", help="JSON logging output.")
    args = parser.parse_args(argv)

    setup_logging(json_output=args.json_log)

    if args.check and args.dry_run:
        logger.error("--check and --dry-run are mutually exclusive.")
        return 2

    if args.dry_run:
        outputs = dry_run()
        for path in sorted(outputs):
            line_count = outputs[path].count("\n")
            print(f"would-write {path.relative_to(REPO_ROOT)} ({line_count} lines)")
        return 0

    if args.check:
        in_sync, drifted = check_styles()
        if in_sync:
            print("Vale styles in sync with brand canonicals.")
            return 0
        for path in drifted:
            print(f"DRIFT: {path.relative_to(REPO_ROOT)}")
        print(
            "Run `py scripts/generate_vale_styles.py` to regenerate "
            f"{len(drifted)} drifted file(s)."
        )
        return 1

    outputs = write_styles(clean=args.clean)
    for path in sorted(outputs):
        print(f"wrote {path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
