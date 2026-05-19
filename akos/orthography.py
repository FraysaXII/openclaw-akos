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

Consumed by ``scripts/validate_locale_orthography.py``.

Decision lineage:
- D-IH-86-P (external-render discipline canonization; parent doctrine)
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
