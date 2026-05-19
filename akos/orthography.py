"""Locale orthography rules — Pydantic chassis for ES / FR / EN diacritic + typography gates.

Per Wave F Strand 3a (I86; ratified at second axis-2 ratify gate 2026-05-19 option B1
"strict per locale"). Codifies high-confidence orthography anti-patterns derived from
the BRAND_<LANG>_PATTERNS.md canonicals:

- ES rules SSOT: ``docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_SPANISH_PATTERNS.md``
- FR rules SSOT: ``docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_FRENCH_PATTERNS.md``
- EN rules SSOT: ``docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ENGLISH_PATTERNS.md``

Scope contract: this module catalogues **high-confidence anti-patterns only** —
unambiguous diacritic omissions in common words that are misspellings when they
appear without their canonical diacritic in body prose. Low-confidence rules
(e.g., `tres` → `très` which is also a valid Spanish word for "three") are
**deliberately excluded** to keep false-positive risk near zero at strict-mode
default.

Wave G Bundle B-G1 extension (2026-05-19, D-IH-86-R): adds
``apply_smart_quotes(text, language)`` — the render-step auto-curl helper. The
function transforms straight ASCII quotes into locale-correct curly quotes
(EN: U+201C/U+201D + U+2018/U+2019; ES/FR: U+00AB/U+00BB + U+2018/U+2019) while
protecting code blocks, URLs, and HTML attribute values. Hooked into
``render_pdf_branded`` so rendered PDFs carry curly typography regardless of
source-markdown keystroke convenience. The locale-orthography validator's EN
smart-quote scan also calls this helper before counting straight quotes — the
gate semantics shift from "source must be curly" to "delivery surface (after
auto-curl) must be curly". Per operator stance: *auto-curl is for rendered
outputs, not for hand-authored markdown source-of-truth.*

Consumed by ``scripts/validate_locale_orthography.py`` and
``akos/hlk_pdf_render.py``.

Decision lineage:
- D-IH-86-P (external-render discipline canonization; parent doctrine)
- D-IH-86-Q (Wave F INFO->FAIL gate promotion; parent strand)
- D-IH-86-R (Wave G B-G1 auto-curl + strict-EN promotion; this strand)
- Operator B1 ratify (2026-05-19 axis-2 second gate; strict per locale)
"""
from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


VALID_LOCALES: frozenset[str] = frozenset({"es", "fr", "en"})


class OrthographyAntiPattern(BaseModel):
    """A single misspelled token + its canonical correction.

    The validator flags occurrences of ``ascii_form`` in body prose (with word
    boundaries) when the surface's declared language matches ``locale``. The
    suggested correction is ``canonical_form``.
    """

    model_config = ConfigDict(frozen=True)

    locale: Literal["es", "fr", "en"]
    ascii_form: str = Field(min_length=2)
    canonical_form: str = Field(min_length=2)
    category: Literal["diacritic", "cedilla", "tilde", "guillemet", "smart_quote"] = Field(
        description="What category of typographic discipline the rule enforces"
    )
    rationale: str = Field(
        description="One-line reason this rule fires (cites BRAND_<LANG>_PATTERNS.md section)"
    )


# ---- Spanish anti-patterns (D-IH-86-P + operator-named 'ñ' as explicit concern) ----
# Word list derived from BRAND_SPANISH_PATTERNS.md §10 + §12 (real founder/advisor
# correspondence) + dossier vocabulary. Every entry is a word that almost always
# carries its diacritic in Holistika prose (legal / fiscal / consulting / regulator
# contexts). When operator's complaint was missing `ñ`, these are the words most
# likely to leak ASCII forms in dossier / cover_email / deck drafts.

ES_ANTI_PATTERNS: tuple[OrthographyAntiPattern, ...] = (
    OrthographyAntiPattern(
        locale="es", ascii_form="ano", canonical_form="año",
        category="tilde",
        rationale="High-consequence: 'ano' = anatomical, 'año' = year. BRAND_SPANISH_PATTERNS §10.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="anos", canonical_form="años",
        category="tilde",
        rationale="Plural of 'año'; same high-consequence ambiguity.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="manana", canonical_form="mañana",
        category="tilde",
        rationale="BRAND_SPANISH_PATTERNS §1 reference exchange ('mañana a las 12:00').",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="pequeno", canonical_form="pequeño",
        category="tilde",
        rationale="Common SME-context adjective; BRAND_SPANISH_PATTERNS §10.1.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="nino", canonical_form="niño",
        category="tilde",
        rationale="Generic vocabulary; appears in advisor / founder contexts.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="senor", canonical_form="señor",
        category="tilde",
        rationale="Address form; BRAND_SPANISH_PATTERNS §3 'Estimado/a [Sr./Sra.]'.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="senora", canonical_form="señora",
        category="tilde",
        rationale="Address form (feminine); same as 'senor'.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="companeros", canonical_form="compañeros",
        category="tilde",
        rationale="Team / colleagues vocabulary; common in onboarding prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="Espana", canonical_form="España",
        category="tilde",
        rationale="Country name; BRAND_SPANISH_PATTERNS §12.5 (Spain vs LATAM).",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="espanol", canonical_form="español",
        category="tilde",
        rationale="Locale name itself; high-consequence in multilingual prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="ensenanza", canonical_form="enseñanza",
        category="tilde",
        rationale="Teaching / training vocabulary; appears in onboarding prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="diseno", canonical_form="diseño",
        category="tilde",
        rationale="Design vocabulary; common in product / consulting prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="dueno", canonical_form="dueño",
        category="tilde",
        rationale="Ownership vocabulary; common in SME / founder prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="acompanar", canonical_form="acompañar",
        category="tilde",
        rationale="Holistika's verb of choice for engagement-framing prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="ensena", canonical_form="enseña",
        category="tilde",
        rationale="Teaches / shows; common in pedagogical prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="manana,", canonical_form="mañana,",
        category="tilde",
        rationale="Specific contextual form (with comma); catches leak when 'ñ' is dropped.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="informacion", canonical_form="información",
        category="diacritic",
        rationale="High-frequency abstract noun; BRAND_SPANISH_PATTERNS §3 ('substantiation-density').",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="decision", canonical_form="decisión",
        category="diacritic",
        rationale="Core Holistika vocabulary ('cómo decidimos'); BRAND_SPANISH_PATTERNS §10.3.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="gestion", canonical_form="gestión",
        category="diacritic",
        rationale="Management vocabulary; BRAND_SPANISH_PATTERNS §1 ('Muchas gracias por la gestión').",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="relacion", canonical_form="relación",
        category="diacritic",
        rationale="High-frequency abstract noun; common in advisor / customer prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="constitucion", canonical_form="constitución",
        category="diacritic",
        rationale="Specific incorporation / founding vocabulary; BRAND_SPANISH_PATTERNS §10.2.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="certificacion", canonical_form="certificación",
        category="diacritic",
        rationale="ENISA / regulator vocabulary; high-frequency in PRJ-HOL-FOUNDING-2026 surfaces.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="version", canonical_form="versión",
        category="diacritic",
        rationale="Document-versioning vocabulary; BRAND_SPANISH_PATTERNS §10.2 ('versión 0.3').",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="atencion", canonical_form="atención",
        category="diacritic",
        rationale="Customer-care vocabulary; common in advisor / customer prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="opcion", canonical_form="opción",
        category="diacritic",
        rationale="Decision-framing vocabulary; common in consulting prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="situacion", canonical_form="situación",
        category="diacritic",
        rationale="Context-framing vocabulary.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="organizacion", canonical_form="organización",
        category="diacritic",
        rationale="Org-context vocabulary; common in baseline_organisation discussions.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="tambien", canonical_form="también",
        category="diacritic",
        rationale="High-frequency adverb; BRAND_SPANISH_PATTERNS §10 patterns.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="despues", canonical_form="después",
        category="diacritic",
        rationale="Temporal adverb; common in scheduling prose.",
    ),
    OrthographyAntiPattern(
        locale="es", ascii_form="segun", canonical_form="según",
        category="diacritic",
        rationale="Preposition; common in attribution prose.",
    ),
)


# ---- French anti-patterns (D-IH-86-P + operator scope-expansion) ----
# Derived from BRAND_FRENCH_PATTERNS.md §3 (reference exchange) + §4 (patterns
# to follow). Every entry is a word that almost always carries its diacritic
# in B2B French (legal / fiscal / consulting / regulator contexts).

FR_ANTI_PATTERNS: tuple[OrthographyAntiPattern, ...] = (
    OrthographyAntiPattern(
        locale="fr", ascii_form="francais", canonical_form="français",
        category="cedilla",
        rationale="Locale name itself; BRAND_FRENCH_PATTERNS §1 ('multicultural identity').",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="Francais", canonical_form="Français",
        category="cedilla",
        rationale="Capitalised form; same provenance.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="apres", canonical_form="après",
        category="diacritic",
        rationale="High-frequency preposition; BRAND_FRENCH_PATTERNS §4 patterns.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="deja", canonical_form="déjà",
        category="diacritic",
        rationale="High-frequency adverb; reads as drift when ASCII.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="metier", canonical_form="métier",
        category="diacritic",
        rationale="BRAND_FRENCH_PATTERNS §5.1 ('cœur de métier' anglicism-replacement).",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="methode", canonical_form="méthode",
        category="diacritic",
        rationale="Core Holistika vocabulary; appears in methodology prose.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="ecouter", canonical_form="écouter",
        category="diacritic",
        rationale="Common verb in advisor / customer prose.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="interessant", canonical_form="intéressant",
        category="diacritic",
        rationale="Common adjective.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="equipe", canonical_form="équipe",
        category="diacritic",
        rationale="Team vocabulary; BRAND_FRENCH_PATTERNS §4 ('animation d'équipe').",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="ecole", canonical_form="école",
        category="diacritic",
        rationale="Common in talent / advisor prose.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="etape", canonical_form="étape",
        category="diacritic",
        rationale="Process-step vocabulary; common in consulting prose.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="reunion", canonical_form="réunion",
        category="diacritic",
        rationale="Meeting vocabulary; BRAND_FRENCH_PATTERNS §5.1 ('meeting' anglicism-replacement).",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="cle", canonical_form="clé",
        category="diacritic",
        rationale="Key (literal/figurative); common in deck headlines.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="strategie", canonical_form="stratégie",
        category="diacritic",
        rationale="Strategy vocabulary; common in deck / dossier prose.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="presentation", canonical_form="présentation",
        category="diacritic",
        rationale="Deck / dossier vocabulary.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="evidence", canonical_form="évidence",
        category="diacritic",
        rationale="Methodology vocabulary; common in research prose.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="numerique", canonical_form="numérique",
        category="diacritic",
        rationale="Digital vocabulary; common in tech / regulator prose.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="resultat", canonical_form="résultat",
        category="diacritic",
        rationale="Outcomes vocabulary; common in pitch prose.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="reduire", canonical_form="réduire",
        category="diacritic",
        rationale="BRAND_FRENCH_PATTERNS §5.1 ('réduire le risque' anglicism-replacement).",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="developpement", canonical_form="développement",
        category="diacritic",
        rationale="Development vocabulary; high-frequency.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="experience", canonical_form="expérience",
        category="diacritic",
        rationale="Experience vocabulary; common in customer / advisor prose.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="reglementation", canonical_form="réglementation",
        category="diacritic",
        rationale="Regulatory vocabulary; common in ENISA / EU-procedural prose.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="financiere", canonical_form="financière",
        category="diacritic",
        rationale="Financial vocabulary (adjective form).",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="cybersecurite", canonical_form="cybersécurité",
        category="diacritic",
        rationale="ENISA core vocabulary; high-consequence for Holistika.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="securite", canonical_form="sécurité",
        category="diacritic",
        rationale="Security vocabulary; ENISA-adjacent.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="garcon", canonical_form="garçon",
        category="cedilla",
        rationale="Common cedilla word; example of c-cedilla discipline.",
    ),
    OrthographyAntiPattern(
        locale="fr", ascii_form="ca", canonical_form="ça",
        category="cedilla",
        rationale="High-frequency demonstrative; needs c-cedilla — BUT only flag at start of sentence or after period (high false-positive risk for English 'ca.' abbreviation; handled by regex word-boundary).",
    ),
)


# ---- English anti-patterns (smart-quote / em-dash typography discipline) ----
# Lower-density rules; EN doesn't need diacritic-gating. Focus is on
# straight-vs-curly quotes in body prose (smart-quote discipline per
# BRAND_ENGLISH_PATTERNS §10 LLM-tone-tells where ASCII quotes leak from
# auto-generated copy). The validator counts straight-quote occurrences in
# body prose and flags above a per-surface threshold (avoids false-positives
# on legitimate code snippets / file paths).

EN_ANTI_PATTERNS: tuple[OrthographyAntiPattern, ...] = (
    # EN anti-patterns are detected via threshold-based body-prose scan in the
    # validator, not via word-list. See _scan_en_smart_quotes() in
    # scripts/validate_locale_orthography.py for the heuristic.
)


# ---- Lookup helpers ----

ANTI_PATTERNS_BY_LOCALE: dict[str, tuple[OrthographyAntiPattern, ...]] = {
    "es": ES_ANTI_PATTERNS,
    "fr": FR_ANTI_PATTERNS,
    "en": EN_ANTI_PATTERNS,
}


def all_anti_patterns() -> tuple[OrthographyAntiPattern, ...]:
    """Flatten all locale anti-patterns to a single tuple for iteration."""
    return ES_ANTI_PATTERNS + FR_ANTI_PATTERNS + EN_ANTI_PATTERNS


# ---- Body-prose preparation regex ----
# Strip fenced code blocks, inline code, URLs, and frontmatter before scanning.
# Conservative: matches the validator's text-cleaning pipeline.

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FENCED_CODE_PATTERN = re.compile(r"```[\s\S]*?```")
INLINE_CODE_PATTERN = re.compile(r"`[^`\n]+`")
URL_PATTERN = re.compile(r"https?://[^\s<>\"'`]+", re.IGNORECASE)
LINK_TARGET_PATTERN = re.compile(r"\[[^\]]*\]\([^)]+\)")  # markdown link target
HTML_COMMENT_PATTERN = re.compile(r"<!--[\s\S]*?-->")


def strip_non_prose(text: str) -> str:
    """Remove frontmatter, code blocks, URLs, markdown links, HTML comments.

    Returns body prose suitable for orthography scanning. Preserves anchor
    text of markdown links (we want to scan visible text, just not URLs).
    """
    text = FRONTMATTER_PATTERN.sub("", text, count=1)
    text = HTML_COMMENT_PATTERN.sub("", text)
    text = FENCED_CODE_PATTERN.sub("", text)
    text = INLINE_CODE_PATTERN.sub("", text)
    text = LINK_TARGET_PATTERN.sub(lambda m: m.group(0).split("](")[0][1:], text)  # keep anchor text only
    text = URL_PATTERN.sub("", text)
    return text


def extract_language(frontmatter_text: str) -> str | None:
    """Extract the `language:` field from a frontmatter blob.

    Returns the locale code (lowercased; first 2 chars) or None if missing.
    """
    match = re.search(r"^language\s*:\s*(.+?)$", frontmatter_text, re.MULTILINE)
    if not match:
        return None
    raw = match.group(1).strip().strip('"').strip("'").lower()
    if raw in VALID_LOCALES:
        return raw
    # Tolerate "es-ES", "fr-FR", "en-US" forms
    if len(raw) >= 2 and raw[:2] in VALID_LOCALES:
        return raw[:2]
    return None


# ============================================================================
# Render-step auto-curl (Wave G Bundle B-G1; D-IH-86-R; 2026-05-19)
# ============================================================================
#
# ``apply_smart_quotes`` transforms straight ASCII quotes into locale-correct
# curly typography while preserving code blocks, URLs, and HTML attribute
# values. Hooked into ``render_pdf_branded`` so the rendered HTML body carries
# curly quotes regardless of how the source markdown was authored.
#
# Algorithm (executive design call, documented for operator review):
#
# 1. Multi-pass placeholder protection of regions where straight quotes are
#    semantically meaningful and must NOT be curled:
#      - ``<pre>...</pre>`` fenced blocks (and markdown ``` ... ``` if any
#        survived the markdown->HTML transform);
#      - ``<code>...</code>`` inline code;
#      - HTML attribute values inside any tag (matched by the generic
#        ``<tag ...>`` pattern; the quotes inside the tag-string are
#        consequently protected);
#      - URLs of the form ``https://...`` (defence-in-depth for bare URLs
#        that escaped link-target wrapping; tag-attr capture handles
#        ``<a href="...">`` cases);
#      - HTML comments;
#      - Markdown fenced code blocks (defence-in-depth if helper is called on
#        pre-markdown text).
# 2. Apply state-machine smart-quote conversion on the remaining "plain
#    text" segments. The state machine uses simple regex with look-behind
#    semantics (opening quote after whitespace/sentence-start vs. closing
#    quote elsewhere).
# 3. Restore placeholders.
#
# Apostrophe disambiguation in EN: ``'`` always becomes U+2019 (right single
# quote) regardless of position. This is the smartypants convention — U+2019
# doubles as apostrophe and closing single-quote (the visual glyph is the
# same in practice). Opening single quotes (e.g., ``'twas``) become U+2018
# only when preceded by whitespace/sentence-start. The disambiguation falls
# out of the regex order: opening pattern fires first; remaining ``'``
# become closing/apostrophe.
#
# ES + FR convention: outer quotes become French/Spanish guillemets ``« »``
# (U+00AB / U+00BB). Inner single quotes use U+2018 / U+2019 for nested
# quotation (matches BRAND_SPANISH_PATTERNS / BRAND_FRENCH_PATTERNS reference
# exchange). Non-breaking spaces inside guillemets (the strictest French
# typography convention) are NOT inserted here to keep the helper string-safe
# for renderers that don't honor NBSP; downstream CSS can add letter-spacing
# polish if desired.

# Protected-region regexes. Order matters: pre/code blocks before generic
# tag-attribute capture because pre/code can contain tags inside that must
# stay literal.
_AUTOCURL_PROTECT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"<pre\b[^>]*>.*?</pre>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<code\b[^>]*>.*?</code>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<!--.*?-->", re.DOTALL),
    re.compile(r"```[\s\S]*?```"),
    re.compile(r"`[^`\n]+`"),
    # Any HTML opening tag (captures attribute values via greedy [^>]* match).
    re.compile(r"<[a-zA-Z][^>]*>"),
    # Any HTML closing tag (no attributes; protected for symmetry).
    re.compile(r"</[a-zA-Z][^>]*>"),
    # Plain URLs (defence-in-depth for bare URLs in text).
    re.compile(r"https?://[^\s<>\"'`]+", re.IGNORECASE),
)

# Placeholder sentinel uses ASCII NUL bytes so it cannot collide with any
# legitimate HTML or text content.
_AUTOCURL_PLACEHOLDER_RE = re.compile(r"\x00APROT_(\d+)\x00")


def _stash_protected_regions(text: str) -> tuple[str, list[str]]:
    """Replace protected regions with sentinel placeholders.

    Returns (text_with_placeholders, stash). The stash is a list whose index
    matches the digit in each sentinel; ``_unstash_protected_regions`` reverses.
    """
    stash: list[str] = []

    def _replace(match: "re.Match[str]") -> str:
        idx = len(stash)
        stash.append(match.group(0))
        return f"\x00APROT_{idx}\x00"

    for pattern in _AUTOCURL_PROTECT_PATTERNS:
        text = pattern.sub(_replace, text)
    return text, stash


def _unstash_protected_regions(text: str, stash: list[str]) -> str:
    """Restore protected regions from sentinel placeholders.

    Robust to multiple-pass placeholder restoration (in case a restored
    region itself contains a placeholder pattern, though that shouldn't
    happen given the NUL byte sentinel).
    """

    def _replace(match: "re.Match[str]") -> str:
        idx = int(match.group(1))
        return stash[idx] if 0 <= idx < len(stash) else match.group(0)

    return _AUTOCURL_PLACEHOLDER_RE.sub(_replace, text)


# Characters that mark "the start of a new quotation" — preceding char
# context that signals an opening quote (rather than a closing quote /
# apostrophe). Sentence start, whitespace, opening brackets/parens, em-dash,
# colon, and a few HTML-friendly markers.
_AUTOCURL_OPEN_PREFIX_CLASS = r"(?:^|[\s\(\[\{>—\-:;,])"


def _apply_quotes_en(text: str) -> str:
    """Curl EN straight quotes in already-protected text.

    - Double quote after open-prefix → U+201C (left double); other ``"`` → U+201D.
    - Single quote after open-prefix → U+2018 (left single); other ``'`` → U+2019.
    """
    text = re.sub(_AUTOCURL_OPEN_PREFIX_CLASS + r'"', lambda m: m.group(0)[:-1] + "\u201c", text)
    text = text.replace('"', "\u201d")
    text = re.sub(_AUTOCURL_OPEN_PREFIX_CLASS + r"'", lambda m: m.group(0)[:-1] + "\u2018", text)
    text = text.replace("'", "\u2019")
    return text


def _apply_quotes_guillemet(text: str) -> str:
    """Curl ES / FR straight double quotes to guillemets and single quotes to U+2018/U+2019.

    Used for both ``es`` and ``fr`` per the simple convention (no NBSP inside
    guillemets here; downstream CSS can polish spacing).
    """
    text = re.sub(_AUTOCURL_OPEN_PREFIX_CLASS + r'"', lambda m: m.group(0)[:-1] + "\u00ab", text)
    text = text.replace('"', "\u00bb")
    text = re.sub(_AUTOCURL_OPEN_PREFIX_CLASS + r"'", lambda m: m.group(0)[:-1] + "\u2018", text)
    text = text.replace("'", "\u2019")
    return text


_AUTOCURL_DISPATCH: dict[str, "callable[[str], str]"] = {
    "en": _apply_quotes_en,
    "es": _apply_quotes_guillemet,
    "fr": _apply_quotes_guillemet,
}


def apply_smart_quotes(text: str, language: str) -> str:
    """Convert ASCII straight quotes to locale-correct curly quotes.

    Args:
        text: Source text. Can be raw markdown, HTML, or plain text — the
            helper preserves code blocks, HTML tags (and their attribute
            values), URLs, HTML comments, and markdown inline/fenced code.
        language: Locale code. ``"en"`` produces U+201C/U+201D + U+2018/U+2019.
            ``"es"`` and ``"fr"`` produce U+00AB/U+00BB + U+2018/U+2019. Any
            other value is treated as a no-op (returns input unchanged).

    Returns:
        Text with straight quotes curled outside protected regions. Idempotent
        for already-curly text (no double-conversion).

    Used by ``akos.hlk_pdf_render.render_pdf_branded`` (auto-curl on body_html
    before WeasyPrint render) and ``scripts/validate_locale_orthography.py``
    (post-curl simulation for the EN delivery-gate scan).
    """
    if not text:
        return text
    if language not in _AUTOCURL_DISPATCH:
        return text
    protected, stash = _stash_protected_regions(text)
    curled = _AUTOCURL_DISPATCH[language](protected)
    return _unstash_protected_regions(curled, stash)
