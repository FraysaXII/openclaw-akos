"""Brand voice register Pydantic chassis for I71 P1 Pack A1.

Backs ``scripts/validate_brand_voice_register.py`` (extended at I71 P1 Pack A1)
with typed schemas for the 10 enforcement layers + parser helpers that read
the brand canonical markdown sources and the operator-editable YAML pack.

Canonical sources (read at runtime):

- `docs/.../Brand/Copywriter/canonicals/BRAND_COPYWRITING_DISCIPLINE.md` §2
  -- 7 AI-tone tic families with detection regex + replacement strategy.
- `docs/.../Brand/canonicals/BRAND_ENGLISH_PATTERNS.md` §5 -- EN MBA-deck
  jargon + performative-EN + template-vendor refuse-list.
- `docs/.../Brand/canonicals/BRAND_FRENCH_PATTERNS.md` §5 -- FR anglicism +
  performative-FR refuse-list (existing I66 P1 canonical).
- `docs/.../Brand/canonicals/BRAND_SPANISH_PATTERNS.md` §13 -- ES anglicism +
  performative-ES refuse-list (existing I66 P1 canonical).
- `docs/.../Brand/canonicals/BRAND_LLM_TONE_TELLS.md` §3-§7 -- EN-corporate
  LLM lexical signature catalog (strict-day-1 per C-71-8).
- `docs/.../Brand/canonicals/BRAND_REGISTER_MATRIX.md` -- six register tokens
  in a (relationship, channel) -> register lookup.
- `docs/.../Brand/UX Designer/canonicals/BRAND_GANTT_DISCIPLINE.md` §2 --
  Variant A/B/C/D audience-formality x data-maturity matrix.
- `docs/.../Brand/canonicals/_validators/register-pack.yml` -- operator
  override surface (consumed by ``parse_register_pack_yaml``).

Decisions: D-IH-71-F (strict-day-1 default), D-IH-71-G (Pydantic chassis
pattern), D-IH-71-H (3-axis audience matrix), D-IH-71-I (Storytelling AUTHORS
/ Resonance CONSUMES boundary), D-IH-71-J (release-gate row policy),
D-IH-71-K (Round 3 brand-DNA Layers 5-9 scope).

Forward-compatible: tolerates absence of any canonical source file (parser
returns ``[]``); strict-mode in the validator raises only when ``_load_rules``
returns empty (existing I66 P2 contract preserved).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# -----------------------------------------------------------------------------
# Type aliases (Literal-based enums per cicd_baseline.py chassis pattern)
# -----------------------------------------------------------------------------

Locale = Literal["en", "fr", "es"]
Severity = Literal["error", "warning", "info"]
GanttVariant = Literal["A", "B", "C", "D"]
SurfaceClass = Literal[
    "cover_slide",
    "customer_pack_body",
    "operator_pack_body",
    "internal_canonical",
    "investor_deck",
    "advisor_email",
    "regulator_memo",
    "boilerplate_i18n",
    "press_release",
    "founder_bio",
]
SubMarkClass = Literal["holistika_research", "holistika_tech_lab", "hlk_erp", "kirbe"]
VoicePersonaClass = Literal[
    "founder",
    "brand_manager",
    "copywriter",
    "account_manager",
    "community_manager",
    "system_owner",
]
EngagementTypeClass = Literal[
    "advisor_intro",
    "advisor_ongoing",
    "investor_outreach",
    "investor_followup",
    "regulator_filing",
    "client_prospect",
    "client_delivery",
    "partner_pitch",
    "recruiter_intake",
    "press_pitch",
    "internal_team",
]


# -----------------------------------------------------------------------------
# Canonical-source constants
# -----------------------------------------------------------------------------

STANDARD_TIC_FAMILY_NAMES: tuple[str, ...] = (
    "contrastive",
    "chained_negation_affirmation",
    "false_singularity",
    "triadic_abstract_noun_stack",
    "discipline_overuse",
    "repeated_openings",
    "operator_instruction_echo",
)

STANDARD_REGISTER_TOKEN_NAMES: frozenset[str] = frozenset(
    {
        "formal_legal",
        "peer_consulting",
        "casual_internal",
        "regulator_neutral",
        "investor_aspirational",
    }
)

CANONICAL_PATHS: dict[str, str] = {
    "copywriting_discipline": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/Copywriter/canonicals/"
        "BRAND_COPYWRITING_DISCIPLINE.md"
    ),
    "english_patterns": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/"
        "BRAND_ENGLISH_PATTERNS.md"
    ),
    "french_patterns": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/"
        "BRAND_FRENCH_PATTERNS.md"
    ),
    "spanish_patterns": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/"
        "BRAND_SPANISH_PATTERNS.md"
    ),
    "llm_tone_tells": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/"
        "BRAND_LLM_TONE_TELLS.md"
    ),
    "register_matrix": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/"
        "BRAND_REGISTER_MATRIX.md"
    ),
    "gantt_discipline": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/UX Designer/canonicals/"
        "BRAND_GANTT_DISCIPLINE.md"
    ),
    "register_pack_yaml": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/"
        "register-pack.yml"
    ),
    "gantt_pack_yaml": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/"
        "gantt-pack.yml"
    ),
    "multilingual_pack_yaml": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/"
        "multilingual-pack.yml"
    ),
    "multilingual_contract": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/"
        "BRAND_MULTILINGUAL_CONTRACT.md"
    ),
    "localised_formats": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/"
        "BRAND_LOCALISED_FORMATS.md"
    ),
    "workspace_blueprint": (
        "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/"
        "WORKSPACE_BLUEPRINT_HOLISTIKA.md"
    ),
    "render_ownership_pack_yaml": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/"
        "render-ownership-pack.yml"
    ),
}


# -----------------------------------------------------------------------------
# I71 P5 -- Pack A4 -- render-pipeline ownership coverage (WORKSPACE §16)
# Additive; no signature changes to existing models per the additive-only
# chassis contract (P1 28-case regression suite locks signatures).
# -----------------------------------------------------------------------------


DeliverableKind = Literal[
    "deck",
    "proposal",
    "tarification",
    "gantt",
    "dossier",
    "counterparty_brief",
    "objections",
    "press",
    "advisor_email",
]

STANDARD_DELIVERABLE_KINDS: tuple[str, ...] = (
    "deck",
    "proposal",
    "tarification",
    "gantt",
    "dossier",
    "counterparty_brief",
    "objections",
    "press",
    "advisor_email",
)


# -----------------------------------------------------------------------------
# Layer 2 -- 7 AI-tone tic families (BRAND_COPYWRITING_DISCIPLINE.md §2)
# -----------------------------------------------------------------------------


class TicFamily(BaseModel):
    """One of the 7 AI-tone tic families codified in §2 of the discipline canonical.

    The validator's Layer 2 scan emits one violation per match; severity is
    layer-wide ``error`` for cover slides + customer-pack body prose, ``warning``
    for operator-pack body prose, ``info`` for internal canonicals per the
    canonical's §5 contract.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(pattern=r"^[a-z][a-z0-9_]+$")
    family_index: int = Field(ge=1, le=7)
    locales: tuple[Locale, ...]
    pattern: str = Field(min_length=1, description="Detection regex (verbatim from canonical)")
    replacement_strategy: str = Field(min_length=1)
    default_severity: Severity = "error"
    canonical_section: str = "BRAND_COPYWRITING_DISCIPLINE.md §2"

    @field_validator("name")
    @classmethod
    def name_is_known(cls, v: str) -> str:
        if v not in STANDARD_TIC_FAMILY_NAMES:
            raise ValueError(
                f"tic-family name {v!r} not in STANDARD_TIC_FAMILY_NAMES "
                f"{STANDARD_TIC_FAMILY_NAMES}"
            )
        return v

    @field_validator("pattern")
    @classmethod
    def pattern_compiles(cls, v: str) -> str:
        try:
            re.compile(v)
        except re.error as exc:
            raise ValueError(f"detection regex does not compile: {exc}") from exc
        return v


# -----------------------------------------------------------------------------
# Layer 0/1 -- per-locale rules (existing I66 P2; promoted to Pydantic at I71 P1)
# -----------------------------------------------------------------------------


class RegisterRule(BaseModel):
    """A single forbidden-token rule for a given locale.

    Pydantic-backed promotion of the existing ``@dataclass(frozen=True)``
    surface in ``scripts/validate_brand_voice_register.py``. The validator
    keeps the dataclass at the call site for backward compatibility; this
    model is the typed contract for YAML-pack consumption.
    """

    model_config = ConfigDict(frozen=True)

    locale: Locale
    token: str = Field(min_length=1)
    pattern: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    canonical_source: str = Field(min_length=1)
    default_severity: Severity = "error"

    @field_validator("pattern")
    @classmethod
    def pattern_compiles(cls, v: str) -> str:
        try:
            re.compile(v)
        except re.error as exc:
            raise ValueError(f"detection regex does not compile: {exc}") from exc
        return v


# -----------------------------------------------------------------------------
# Layer 3 -- audience formality x data maturity matrix (BRAND_GANTT_DISCIPLINE.md §2)
# -----------------------------------------------------------------------------


class AudienceQuadrant(BaseModel):
    """One quadrant of the (audience-formality x data-maturity) matrix.

    Variants A/B/C/D per BRAND_GANTT_DISCIPLINE.md §2:
    - A: customer-facing + low data maturity (posture sketch).
    - B: customer-facing + high data maturity (proof of discipline).
    - C: operator-internal + low data maturity (hypothesis sketch).
    - D: operator-internal + high data maturity (execution plan).

    Pack A1 Layer 3 reuses this matrix as the 3-axis audience class primary
    key (audience x formality x data-maturity).
    """

    model_config = ConfigDict(frozen=True)

    variant: GanttVariant
    audience_facing: Literal["customer", "operator"]
    data_maturity: Literal["low", "high"]
    label: str = Field(min_length=1)
    description: str = Field(min_length=1)
    canonical_section: str = "BRAND_GANTT_DISCIPLINE.md §2"


# -----------------------------------------------------------------------------
# Layer 3 (continued) -- register tokens (BRAND_REGISTER_MATRIX.md)
# -----------------------------------------------------------------------------


class RegisterToken(BaseModel):
    """One register token from BRAND_REGISTER_MATRIX.md (6 canonical tokens).

    Loaded from the (relationship, channel) -> register lookup. The validator
    asserts each (relationship, channel) pair declared on an engagement-deck
    frontmatter resolves to a known token before render.
    """

    model_config = ConfigDict(frozen=True)

    token: str = Field(min_length=1)
    relationship: str = Field(min_length=1)
    channel: str = Field(min_length=1)
    canonical_section: str = "BRAND_REGISTER_MATRIX.md"

    @field_validator("token")
    @classmethod
    def token_is_known(cls, v: str) -> str:
        if v not in STANDARD_REGISTER_TOKEN_NAMES:
            raise ValueError(
                f"register token {v!r} not in STANDARD_REGISTER_TOKEN_NAMES "
                f"{sorted(STANDARD_REGISTER_TOKEN_NAMES)}"
            )
        return v


class AudienceClass(BaseModel):
    """3-axis audience matrix entry per D-IH-71-H.

    Synthesizes (audience x formality x data-maturity) into a single class
    that the validator uses as the primary key for register expectation
    lookup. Each declared engagement deck/document maps to exactly one class.
    """

    model_config = ConfigDict(frozen=True)

    audience: Literal["customer", "operator", "investor", "advisor", "regulator", "partner", "press"]
    formality: Literal["high", "medium", "low"]
    data_maturity: Literal["low", "high"]
    expected_register_token: str
    expected_variant: GanttVariant
    canonical_basis: str = "BRAND_GANTT_DISCIPLINE.md §2 + BRAND_REGISTER_MATRIX.md"


# -----------------------------------------------------------------------------
# Layer 4 -- Storytelling/Resonance boundary (D-IH-70-X)
# -----------------------------------------------------------------------------


class BoundaryRule(BaseModel):
    """Storytelling AUTHORS / Resonance CONSUMES boundary per D-IH-70-X.

    The validator enforces: any artifact whose frontmatter declares
    ``area: Resonance`` is read-only with respect to narrative content. On
    edit, the validator computes a narrative diff vs the upstream Storytelling
    artifact and refuses if the diff exceeds ``max_narrative_token_diff``.

    Single-ownership of brand narrative authorship is preserved by separating
    the verbs author-vs-deploy.
    """

    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(pattern=r"^B-[A-Z0-9_-]+$")
    authoring_area: Literal["Storytelling"] = "Storytelling"
    consuming_area: Literal["Resonance"] = "Resonance"
    max_narrative_token_diff: int = Field(ge=0, le=10_000, default=0)
    decision_anchor: Literal["D-IH-70-X"] = "D-IH-70-X"


# -----------------------------------------------------------------------------
# Round 3 -- Layer 5 -- sub-mark tier + archetype + Branded House
# -----------------------------------------------------------------------------


class SubMarkTier(BaseModel):
    """Sub-mark tier classification per BRAND_ARCHITECTURE.md (Branded House).

    Pack A1 Layer 5 enforces that any artifact carrying ``sub_mark:`` in its
    frontmatter resolves to a known tier; the validator refuses if an
    artifact's voice tier conflicts with its sub-mark's expected tier.
    """

    model_config = ConfigDict(frozen=True)

    sub_mark: SubMarkClass
    tier_label: str = Field(min_length=1)
    expected_voice_register: str = Field(min_length=1)
    canonical_section: str = "BRAND_ARCHITECTURE.md"


class ArchetypeViolation(BaseModel):
    """Result row for an archetype-mismatch hit (Layer 5)."""

    file: Path
    surface: str
    declared_archetype: str
    detected_archetype: str
    rule_id: str
    severity: Severity
    rationale: str


class BrandedHouseViolation(BaseModel):
    """Result row for a Branded-House structural violation (Layer 5).

    Examples: an artifact declares ``sub_mark: holistika_tech_lab`` but uses
    investor-aspirational register where peer-engineering register is expected;
    an artifact mixes two sub-marks' voice tiers within a single deliverable;
    a cobrand surface uses sub-mark precedence inconsistent with
    BRAND_COBRANDING_PATTERN.md.
    """

    file: Path
    surface: str
    sub_mark: SubMarkClass
    declared_tier: str
    detected_tier: str
    rule_id: str
    severity: Severity
    rationale: str


# -----------------------------------------------------------------------------
# Round 3 -- Layer 6 -- voice persona + engagement type
# -----------------------------------------------------------------------------


class VoicePersona(BaseModel):
    """A named voice persona per BRAND_VOICE_FOUNDATION.md (operator-authored).

    Each role in the operator's lived protocol (Founder, Brand Manager,
    Copywriter, Account Manager, Community Manager, System Owner) carries a
    voice signature. Pack A1 Layer 6 enforces that artifacts declaring
    ``voice_persona:`` in frontmatter use the corresponding signature.
    """

    model_config = ConfigDict(frozen=True)

    persona: VoicePersonaClass
    canonical_label: str = Field(min_length=1)
    expected_register_tokens: tuple[str, ...]
    canonical_section: str = "BRAND_VOICE_FOUNDATION.md"


class EngagementType(BaseModel):
    """Engagement-type classifier per `process_list.csv` engagement disciplines.

    Pack A1 Layer 6 maps every engagement-deck/document to its engagement type
    and enforces register expectations: a regulator filing must use
    ``regulator_neutral``; an investor outreach must use
    ``investor_aspirational``; etc. Mismatches fail at strict-day-1.
    """

    model_config = ConfigDict(frozen=True)

    engagement_type: EngagementTypeClass
    canonical_label: str = Field(min_length=1)
    expected_register_token: str
    expected_locales: tuple[Locale, ...]
    canonical_basis: str = "BRAND_REGISTER_MATRIX.md + process_list.csv adviser-engagement disciplines"


# -----------------------------------------------------------------------------
# Round 3 -- Layer 7 -- locale-leak + cobrand surface check
# -----------------------------------------------------------------------------


class LocaleLeakRule(BaseModel):
    """Cross-locale leak detection for parallel i18n keys (Layer 7).

    Asserts that English/French/Spanish variants of the same i18n key are
    register-consistent (per Layer 0-3) AND that none re-introduces an
    internal-register token from BRAND_BASELINE_REALITY_MATRIX.md §3.
    """

    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(pattern=r"^LL-[A-Z0-9_-]+$")
    json_key_pattern: str = Field(min_length=1)
    locales_checked: tuple[Locale, ...] = ("en", "fr", "es")
    max_register_drift_tokens: int = Field(ge=0, default=2)
    default_severity: Severity = "warning"


class CobrandRule(BaseModel):
    """Cobrand surface check per BRAND_COBRANDING_PATTERN.md (Layer 7).

    Asserts that artifacts on cobranded surfaces (e.g., joint client + Holistika
    deliverable) use the expected precedence: Holistika sub-mark vs partner
    mark; logo prominence; closing-line attribution.
    """

    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(pattern=r"^CB-[A-Z0-9_-]+$")
    surface_pattern: str = Field(min_length=1)
    expected_precedence: Literal["holistika_first", "partner_first", "equal"]
    canonical_section: str = "BRAND_COBRANDING_PATTERN.md"
    default_severity: Severity = "warning"


# -----------------------------------------------------------------------------
# Round 3 -- Layer 8 -- anti-LLM-tone catalog (BRAND_LLM_TONE_TELLS.md)
# -----------------------------------------------------------------------------


class LLMToneTell(BaseModel):
    """One LLM-default lexical pattern per BRAND_LLM_TONE_TELLS.md §3-§7.

    Per the C-71-8 operator override, default_severity for ``error`` tokens
    is enforced strict-day-1 (no 30-day soft window). The validator may
    accept per-token allowlist via ``<!-- llm-tone-allow: T-N-token-slug -->``.
    """

    model_config = ConfigDict(frozen=True)

    token_id: str = Field(pattern=r"^T-[3-7]-[a-z0-9-]+$")
    category: Literal["verb", "noun", "adjective", "hedge_phrase", "construction"]
    pattern: str = Field(min_length=1)
    replacement_template: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    default_severity: Severity = "error"
    canonical_section: str = "BRAND_LLM_TONE_TELLS.md"

    @field_validator("pattern")
    @classmethod
    def pattern_compiles(cls, v: str) -> str:
        try:
            re.compile(v)
        except re.error as exc:
            raise ValueError(f"detection regex does not compile: {exc}") from exc
        return v


# -----------------------------------------------------------------------------
# Round 3 -- Layer 9 -- anonymized track-record + brand-abbrev surface
# -----------------------------------------------------------------------------


class TrackRecordRule(BaseModel):
    """Anonymized track-record format guard (Layer 9).

    Asserts that public-facing track-record citations follow the canonical
    anonymized format (counterparty-tier + sector + outcome metric) rather
    than identifying a counterparty by name without consent. See
    BRAND_BASELINE_REALITY_MATRIX.md §"Anonymized track record".
    """

    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(pattern=r"^TR-[A-Z0-9_-]+$")
    surface_pattern: str = Field(min_length=1)
    canonical_format_regex: str = Field(min_length=1)
    default_severity: Severity = "error"
    canonical_section: str = "BRAND_BASELINE_REALITY_MATRIX.md"


class BrandAbbreviationRule(BaseModel):
    """Brand-abbreviation surface check per BRAND_ABBREVIATIONS.md (Layer 9).

    Asserts that artifacts use the canonical short form for sub-marks and
    program names (e.g., ``HLK`` for ``Holistika``; ``HRL`` for
    ``Holistika Research Lab``) rather than ad-hoc abbreviations.
    """

    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(pattern=r"^BA-[A-Z0-9_-]+$")
    canonical_short_form: str = Field(min_length=1)
    full_form: str = Field(min_length=1)
    surface_pattern: str = Field(min_length=1)
    default_severity: Severity = "warning"
    canonical_section: str = "BRAND_ABBREVIATIONS.md"


# -----------------------------------------------------------------------------
# I71 P2 -- Pack A2 -- Gantt confidence ladder + audience-quadrant rules
# (additive; no signature changes to existing models per kickoff §"DO NOT")
# -----------------------------------------------------------------------------


_CONFIDENCE_BAND_LABELS: dict[int, str] = {
    1: "Reserved",
    2: "Hypothesis",
    3: "Posture",
    4: "Probable",
    5: "Confirmed",
}


class GanttConfidenceRule(BaseModel):
    """One row of the 5-level confidence ladder per BRAND_GANTT_DISCIPLINE.md §4.

    Pack A2 emits one violation per Gantt artifact whose ``confidence_band``
    frontmatter falls outside the ladder, or whose declared ``gantt_variant``
    is not in ``allowed_variants`` for the artifact's band. Pack A2 also uses
    this rule set to detect ``confidence inflation`` (e.g., a Variant A
    posture-sketch declaring band 4 Probable when §4 reserves Probable for
    Variant B post-acceptance).
    """

    model_config = ConfigDict(frozen=True)

    band: int = Field(ge=1, le=5)
    label: Literal["Reserved", "Hypothesis", "Posture", "Probable", "Confirmed"]
    allowed_variants: tuple[GanttVariant, ...]
    display_rule: str = Field(min_length=1)
    default_severity: Severity = "error"
    canonical_section: str = "BRAND_GANTT_DISCIPLINE.md §4"

    @model_validator(mode="after")
    def _label_matches_band(self) -> "GanttConfidenceRule":
        expected = _CONFIDENCE_BAND_LABELS[self.band]
        if self.label != expected:
            raise ValueError(
                f"band {self.band} expects label {expected!r}, got {self.label!r}"
            )
        return self


class AudienceQuadrantRule(BaseModel):
    """One quadrant-assignment rule per BRAND_GANTT_DISCIPLINE.md §2.

    Codifies the discipline rule that customer-pack only ships Variant A or B
    (low or high data maturity); operator-internal only ships Variant C or D.
    Pack A2 emits a violation when a Gantt artifact's surface class (derived
    from path: ``02-customer-pack/`` vs ``01-operator-pack/``) disagrees with
    the declared ``gantt_variant`` frontmatter per the per-variant
    ``forbidden_in_customer_pack`` / ``forbidden_in_operator_pack`` flags.
    """

    model_config = ConfigDict(frozen=True)

    variant: GanttVariant
    audience_facing: Literal["customer", "operator"]
    data_maturity: Literal["low", "high"]
    forbidden_in_customer_pack: bool
    forbidden_in_operator_pack: bool
    default_severity: Severity = "error"
    canonical_section: str = "BRAND_GANTT_DISCIPLINE.md §2"


# -----------------------------------------------------------------------------
# I71 P2 -- Pack A3 -- multilingual locale suffix + README triad
# (additive; no signature changes to existing models)
# -----------------------------------------------------------------------------


class LocaleSuffixRule(BaseModel):
    """Per-locale README suffix discipline per BRAND_MULTILINGUAL_CONTRACT.md §2.

    Asserts that a per-locale README (e.g., ``README.fr.md``) declares the
    matching ``language:`` frontmatter value. Pack A3 emits a violation when
    a README's suffix says one locale and its frontmatter says another.
    """

    model_config = ConfigDict(frozen=True)

    locale: Locale
    expected_suffix: str = Field(min_length=1)
    frontmatter_language_value: str = Field(min_length=1)
    default_severity: Severity = "error"
    canonical_section: str = "BRAND_MULTILINGUAL_CONTRACT.md §2"


class ReadmeTriadRule(BaseModel):
    """3-file README triad rule per BRAND_MULTILINGUAL_CONTRACT.md §2 + D-IH-70-P.

    Asserts that an engagement folder declaring ``README.fr.md`` and / or
    ``README.en.md`` link targets in its 5-line pointer ``README.md`` also
    has those files present on disk, and that the pointer matches the 5-line
    skeleton (title + blank + intro + bullets + closing blank).

    Severity downgradable to ``warning`` via the C-71-2 inline-ratify gate
    (default at P2 = warn-until-2-bilingual; promote to ``error`` when the
    second consecutive bilingual engagement ships per master-roadmap §P2).
    """

    model_config = ConfigDict(frozen=True)

    pointer_line_count_min: int = Field(ge=2, le=12, default=3)
    pointer_line_count_max: int = Field(ge=3, le=20, default=12)
    required_pointer_keywords: tuple[str, ...] = (
        "Per-language READMEs:",
    )
    per_locale_readme_required: bool = True
    default_severity: Severity = "warning"
    canonical_section: str = (
        "BRAND_MULTILINGUAL_CONTRACT.md §2 + BRAND_COUNTERPARTY_README_CONTRACT.md + D-IH-70-P"
    )


# -----------------------------------------------------------------------------
# I71 P2 -- Addition 11 -- per-locale number / currency / date formats
# (additive; no signature changes to existing models)
# -----------------------------------------------------------------------------


class NumberFormatRule(BaseModel):
    """Per-locale number format rule per BRAND_LOCALISED_FORMATS.md §1.

    Codifies thousands-separator + decimal-separator per locale. Surfaces via
    Pack A2's validator (Gantt confidence cells frequently carry money/dates
    in their per-deliverable copy). en uses ',' + '.'; fr uses NARROW NO-BREAK
    SPACE U+202F + ','; es uses '.' + ','.
    """

    model_config = ConfigDict(frozen=True)

    locale: Locale
    thousands_separator: str
    decimal_separator: str
    canonical_section: str = "BRAND_LOCALISED_FORMATS.md §1"
    default_severity: Severity = "error"


class CurrencyFormatRule(BaseModel):
    """Per-currency × per-locale format rule per BRAND_LOCALISED_FORMATS.md §2.

    EUR symbol position varies by locale (fr suffix, en prefix, es suffix).
    USD prefix all locales. GBP prefix all locales.
    """

    model_config = ConfigDict(frozen=True)

    locale: Locale
    currency: Literal["EUR", "USD", "GBP", "CHF"]
    symbol_position: Literal["prefix", "suffix"]
    symbol_separator: str = " "
    canonical_section: str = "BRAND_LOCALISED_FORMATS.md §2"
    default_severity: Severity = "error"


class DateFormatRule(BaseModel):
    """Per-locale × per-format-class date format rule per BRAND_LOCALISED_FORMATS.md §3.

    ISO 8601 canonical / technical contexts (all locales); per-locale
    natural-language formats: en "May 14, 2026" / fr "14 mai 2026" /
    es "14 de mayo de 2026".
    """

    model_config = ConfigDict(frozen=True)

    locale: Locale
    format_class: Literal["iso", "natural_long", "natural_short"]
    pattern: str = Field(min_length=1)
    example: str = Field(min_length=1)
    canonical_section: str = "BRAND_LOCALISED_FORMATS.md §3"
    default_severity: Severity = "warning"


# -----------------------------------------------------------------------------
# I71 P2 -- Gantt operator-override pack (sibling to BrandVoiceRegisterPack)
# -----------------------------------------------------------------------------


class BrandGanttPack(BaseModel):
    """Operator-editable Gantt confidence + audience-quadrant override pack.

    Loaded from `docs/.../Brand/canonicals/_validators/gantt-pack.yml` via
    ``parse_gantt_pack_yaml``. Operator overrides apply over canonical
    defaults; the YAML pack is the final word at runtime.

    Carries the Pack A2 + Addition 11 surfaces under a single typed pack so
    the validator can resolve all Gantt-adjacent rules from one operator
    artifact. ``register-pack.yml`` (Pack A1) remains untouched.
    """

    model_config = ConfigDict(frozen=True)

    pack_version: str = Field(pattern=r"^v[0-9]+\.[0-9]+\.[0-9]+$")
    last_edited: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_edited_by: str = Field(min_length=1)
    canonical_source_refs: tuple[str, ...]
    layers_enabled: dict[str, bool] = Field(default_factory=dict)
    gantt_confidence_rules: tuple[GanttConfidenceRule, ...] = ()
    audience_quadrant_rules: tuple[AudienceQuadrantRule, ...] = ()
    number_format_rules: tuple[NumberFormatRule, ...] = ()
    currency_format_rules: tuple[CurrencyFormatRule, ...] = ()
    date_format_rules: tuple[DateFormatRule, ...] = ()


# -----------------------------------------------------------------------------
# I71 P2 -- Pack A3 multilingual operator-override pack
# -----------------------------------------------------------------------------


class BrandMultilingualPack(BaseModel):
    """Operator-editable multilingual locale-suffix + README triad pack.

    Loaded from `docs/.../Brand/canonicals/_validators/multilingual-pack.yml`
    via ``parse_multilingual_pack_yaml``. Carries the Pack A3 surfaces under
    a single typed pack so the validator can resolve locale + triad rules
    from one operator artifact.

    Severity-override knob ``default_triad_severity`` operationalises the
    C-71-2 inline-ratify gate (``warning`` = warn-until-2-bilingual default;
    ``error`` = strict-day-1 override matching Pack A1 precedent).
    """

    model_config = ConfigDict(frozen=True)

    pack_version: str = Field(pattern=r"^v[0-9]+\.[0-9]+\.[0-9]+$")
    last_edited: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_edited_by: str = Field(min_length=1)
    canonical_source_refs: tuple[str, ...]
    layers_enabled: dict[str, bool] = Field(default_factory=dict)
    default_triad_severity: Severity = "warning"
    locale_suffix_rules: tuple[LocaleSuffixRule, ...] = ()
    readme_triad_rules: tuple[ReadmeTriadRule, ...] = ()


# -----------------------------------------------------------------------------
# Composite pack -- single Pydantic model loaded from register-pack.yml
# -----------------------------------------------------------------------------


class BrandVoiceRegisterPack(BaseModel):
    """Composite pack consumed by the validator at runtime.

    Loaded from `docs/.../Brand/canonicals/_validators/register-pack.yml` via
    ``parse_register_pack_yaml``. Operator overrides applied to canonical
    defaults; the YAML pack is the final word at runtime.
    """

    model_config = ConfigDict(frozen=True)

    pack_version: str = Field(pattern=r"^v[0-9]+\.[0-9]+\.[0-9]+$")
    last_edited: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_edited_by: str = Field(min_length=1)
    canonical_source_refs: tuple[str, ...]
    layers_enabled: dict[str, bool] = Field(default_factory=dict)
    tic_families: tuple[TicFamily, ...] = ()
    register_rules: tuple[RegisterRule, ...] = ()
    audience_quadrants: tuple[AudienceQuadrant, ...] = ()
    register_tokens: tuple[RegisterToken, ...] = ()
    audience_classes: tuple[AudienceClass, ...] = ()
    boundary_rules: tuple[BoundaryRule, ...] = ()
    sub_mark_tiers: tuple[SubMarkTier, ...] = ()
    voice_personas: tuple[VoicePersona, ...] = ()
    engagement_types: tuple[EngagementType, ...] = ()
    llm_tone_tells: tuple[LLMToneTell, ...] = ()
    locale_leak_rules: tuple[LocaleLeakRule, ...] = ()
    cobrand_rules: tuple[CobrandRule, ...] = ()
    track_record_rules: tuple[TrackRecordRule, ...] = ()
    brand_abbreviation_rules: tuple[BrandAbbreviationRule, ...] = ()


# -----------------------------------------------------------------------------
# Parser helpers (read canonical markdown sources; tolerate file absence)
# -----------------------------------------------------------------------------


_TIC_SECTION_RE = re.compile(
    r"^### Family (\d) — .*?(?=^### Family \d|^## 3\.)",
    re.DOTALL | re.MULTILINE,
)
_DETECTION_REGEX_LINE_RE = re.compile(
    r"\*\*Detection regex(?:\s*\(([^)]+)\))?:?\*\*\s*`([^`]+)`",
    re.IGNORECASE,
)


def parse_tic_families_from_canonical(path: Path) -> list[TicFamily]:
    """Parse the 7 AI-tone tic families from BRAND_COPYWRITING_DISCIPLINE.md §2.

    Returns one ``TicFamily`` per family * declared-locale combination. The
    canonical declares 7 family names in a fixed order; the parser maps to
    ``STANDARD_TIC_FAMILY_NAMES`` by index. Families without a parseable
    regex (F4 -- triadic abstract-noun stack; F5 -- discipline overuse; F6 --
    repeated openings; F7 -- structural pattern) are returned with a default
    locale-agnostic pattern surface for the validator to handle via custom
    detection rather than pure regex match.
    """
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")

    out: list[TicFamily] = []
    for section_match in _TIC_SECTION_RE.finditer(text):
        family_block = section_match.group(0)
        family_index_match = re.match(r"^### Family (\d)", family_block)
        if not family_index_match:
            continue
        family_index = int(family_index_match.group(1))
        if family_index < 1 or family_index > 7:
            continue
        canonical_name = STANDARD_TIC_FAMILY_NAMES[family_index - 1]

        replacement_match = re.search(
            r"\*\*Replacement strategy\.?\*\*\s*(.+?)(?=\n\n|^### |^## )",
            family_block,
            re.DOTALL | re.MULTILINE,
        )
        replacement = (
            replacement_match.group(1).strip().splitlines()[0]
            if replacement_match
            else "See canonical for replacement strategy."
        )

        regex_hits = list(_DETECTION_REGEX_LINE_RE.finditer(family_block))
        if regex_hits:
            for hit in regex_hits:
                locale_label = (hit.group(1) or "all").strip().lower()
                pattern = hit.group(2).strip()
                locales: tuple[Locale, ...]
                if locale_label.startswith("fr"):
                    locales = ("fr",)
                elif locale_label.startswith("en"):
                    locales = ("en",)
                elif locale_label.startswith("es"):
                    locales = ("es",)
                elif "fr" in locale_label and "en" in locale_label:
                    locales = ("fr", "en")
                else:
                    locales = ("en", "fr", "es")
                try:
                    out.append(
                        TicFamily(
                            name=canonical_name,
                            family_index=family_index,
                            locales=locales,
                            pattern=pattern,
                            replacement_strategy=replacement,
                        )
                    )
                except ValueError:
                    continue
        else:
            # Structural family (F4 / F5 / F6 / F7) -- no pure regex; validator
            # handles via custom detection. Emit a sentinel placeholder pattern
            # the validator inspects (.*).
            try:
                out.append(
                    TicFamily(
                        name=canonical_name,
                        family_index=family_index,
                        locales=("en", "fr", "es"),
                        pattern=r".*",
                        replacement_strategy=replacement,
                    )
                )
            except ValueError:
                continue
    return out


_EN_JARGON_ROW_RE = re.compile(
    r"^\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
    re.MULTILINE,
)


def parse_english_register_rules(path: Path) -> list[RegisterRule]:
    """Parse EN register rules from BRAND_ENGLISH_PATTERNS.md §5.1.

    Each row in the MBA-deck-jargon table yields one ``RegisterRule`` with
    locale=en and a word-boundary regex over the avoid-token. The rationale
    captures the canonical's replacement + rationale text.
    """
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")

    section = re.search(
        r"### 5\.1 MBA-deck jargon.*?\n(.*?)(?=^### 5\.\d|^## 6\.)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    if not section:
        return []
    body = section.group(1)
    out: list[RegisterRule] = []
    for row_match in _EN_JARGON_ROW_RE.finditer(body):
        token = row_match.group(1).strip()
        replacement = row_match.group(2).strip()
        rationale_text = row_match.group(3).strip()
        if not token:
            continue
        try:
            out.append(
                RegisterRule(
                    locale="en",
                    token=token,
                    pattern=rf"\b{re.escape(token)}\b",
                    rationale=f"EN MBA-deck jargon -- replace with '{replacement}' ({rationale_text})",
                    canonical_source="BRAND_ENGLISH_PATTERNS.md §5.1",
                )
            )
        except ValueError:
            continue
    return out


_LLM_TELL_TABLE_RE = re.compile(
    r"^\|\s*`?([^`|]+?)`?\s*\|\s*(error|warning|info)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
    re.MULTILINE | re.IGNORECASE,
)


def parse_llm_tone_tells(path: Path) -> list[LLMToneTell]:
    """Parse the BRAND_LLM_TONE_TELLS.md §3-§7 tables into typed rules.

    Each section (§3 verbs / §4 nouns / §5 adjectives / §6 hedge phrases /
    §7 constructions) maps to a category. Token IDs synthesize as
    ``T-{section}-{slugified-token}``.
    """
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")

    section_categories: dict[str, str] = {
        "3": "verb",
        "4": "noun",
        "5": "adjective",
        "6": "hedge_phrase",
        "7": "construction",
    }
    out: list[LLMToneTell] = []
    for section_index, category in section_categories.items():
        section_match = re.search(
            rf"^## {section_index}\..*?\n(.*?)(?=^## \d|\Z)",
            text,
            re.DOTALL | re.MULTILINE,
        )
        if not section_match:
            continue
        body = section_match.group(1)
        for row in _LLM_TELL_TABLE_RE.finditer(body):
            token_raw = row.group(1).strip()
            severity_raw = row.group(2).strip().lower()
            replacement = row.group(3).strip()
            rationale = row.group(4).strip()
            if not token_raw or severity_raw not in ("error", "warning", "info"):
                continue
            slug = re.sub(r"[^a-z0-9]+", "-", token_raw.lower()).strip("-")
            if not slug:
                continue
            token_id = f"T-{section_index}-{slug}"[:80]
            try:
                out.append(
                    LLMToneTell(
                        token_id=token_id,
                        category=category,  # type: ignore[arg-type]
                        pattern=rf"\b{re.escape(token_raw)}\b",
                        replacement_template=replacement,
                        rationale=rationale,
                        default_severity=severity_raw,  # type: ignore[arg-type]
                    )
                )
            except ValueError:
                continue
    return out


_REGISTER_MATRIX_ROW_RE = re.compile(
    r"^\|\s*([a-z_]+)\s*\|\s*([a-z_]+)\s*\|\s*`([a-z_]+)`\s*\|",
    re.MULTILINE | re.IGNORECASE,
)


def parse_register_matrix(path: Path) -> list[RegisterToken]:
    """Parse BRAND_REGISTER_MATRIX.md (relationship, channel) -> register rows."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    out: list[RegisterToken] = []
    for row in _REGISTER_MATRIX_ROW_RE.finditer(text):
        relationship = row.group(1).strip().lower()
        channel = row.group(2).strip().lower()
        token = row.group(3).strip().lower()
        try:
            out.append(
                RegisterToken(token=token, relationship=relationship, channel=channel)
            )
        except ValueError:
            continue
    return out


def parse_audience_quadrants(path: Path) -> list[AudienceQuadrant]:
    """Parse BRAND_GANTT_DISCIPLINE.md §2 4-quadrant audience matrix.

    The canonical §2 declares four labeled variants; this parser returns one
    ``AudienceQuadrant`` per variant with the canonical label + description.
    """
    if not path.exists():
        return []
    # The canonical §2 structure is stable; emit the 4 quadrants directly with
    # the canonical labels rather than fragile markdown-table regex parsing.
    return [
        AudienceQuadrant(
            variant="A",
            audience_facing="customer",
            data_maturity="low",
            label="Posture sketch",
            description="No dates; phase ribbons; ratify-via-discovery.",
        ),
        AudienceQuadrant(
            variant="B",
            audience_facing="customer",
            data_maturity="high",
            label="Proof of discipline",
            description="Concrete dates; per-phase deliverables; per-phase ownership.",
        ),
        AudienceQuadrant(
            variant="C",
            audience_facing="operator",
            data_maturity="low",
            label="Hypothesis sketch",
            description="Cross-linked sources; assumption flags; revisit cadence.",
        ),
        AudienceQuadrant(
            variant="D",
            audience_facing="operator",
            data_maturity="high",
            label="Execution plan",
            description="Granular weekly task breakdown; dependency arrows; resource allocation.",
        ),
    ]


def parse_register_pack_yaml(path: Path) -> BrandVoiceRegisterPack | None:
    """Load `register-pack.yml` and return a typed pack, or None if absent.

    Uses ``yaml.safe_load`` for parsing; raises on schema-validation failure
    (Pydantic model is the contract). Returns ``None`` when the file is
    absent so the validator can fall back to canonical-source defaults.
    """
    if not path.exists():
        return None
    try:
        import yaml  # local import keeps yaml optional at import time
    except ImportError:
        return None
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return BrandVoiceRegisterPack.model_validate(raw)


# -----------------------------------------------------------------------------
# I71 P2 -- Pack A2 + A3 + Addition 11 parsers (additive)
# -----------------------------------------------------------------------------


def parse_gantt_confidence_rules(path: Path) -> list[GanttConfidenceRule]:
    """Return the 5-level confidence ladder per BRAND_GANTT_DISCIPLINE.md §4.

    The §4 structure is stable (5 named bands with allowed-variant assignment
    derived from the discipline's §4 "When to use" column). The parser emits
    the 5 rules directly with canonical labels rather than fragile
    markdown-table regex parsing (same approach as ``parse_audience_quadrants``
    for §2). Returns ``[]`` when the canonical is absent (graceful skip).

    Allowed-variant assignment from §4 "When to use":
        Band 5 Confirmed  -> Variant B post-contract.
        Band 4 Probable   -> Variant B mid-acceptance.
        Band 3 Posture    -> Variant A + Variant C.
        Band 2 Hypothesis -> Variant C only.
        Band 1 Reserved   -> Variant A only.
    """
    if not path.exists():
        return []
    return [
        GanttConfidenceRule(
            band=5,
            label="Confirmed",
            allowed_variants=("B",),
            display_rule="solid bar + dates in title",
        ),
        GanttConfidenceRule(
            band=4,
            label="Probable",
            allowed_variants=("B",),
            display_rule="solid bar + dates with ~ prefix",
        ),
        GanttConfidenceRule(
            band=3,
            label="Posture",
            allowed_variants=("A", "C"),
            display_rule="dotted bar + dates with ~ prefix + footnote-mark",
        ),
        GanttConfidenceRule(
            band=2,
            label="Hypothesis",
            allowed_variants=("C",),
            display_rule="dotted bar + dates with ? prefix + explicit hypothesis footnote",
        ),
        GanttConfidenceRule(
            band=1,
            label="Reserved",
            allowed_variants=("A",),
            display_rule="phase ribbon only; no bars",
        ),
    ]


def parse_audience_quadrant_rules(path: Path) -> list[AudienceQuadrantRule]:
    """Return the 4 quadrant-assignment rules per BRAND_GANTT_DISCIPLINE.md §2.

    Codifies the §2 4-quadrant matrix as enforceable variant-vs-surface rules:
    customer-pack ships Variant A or B; operator-internal ships Variant C or D.
    Returns ``[]`` when the canonical is absent.
    """
    if not path.exists():
        return []
    return [
        AudienceQuadrantRule(
            variant="A",
            audience_facing="customer",
            data_maturity="low",
            forbidden_in_customer_pack=False,
            forbidden_in_operator_pack=True,
        ),
        AudienceQuadrantRule(
            variant="B",
            audience_facing="customer",
            data_maturity="high",
            forbidden_in_customer_pack=False,
            forbidden_in_operator_pack=True,
        ),
        AudienceQuadrantRule(
            variant="C",
            audience_facing="operator",
            data_maturity="low",
            forbidden_in_customer_pack=True,
            forbidden_in_operator_pack=False,
        ),
        AudienceQuadrantRule(
            variant="D",
            audience_facing="operator",
            data_maturity="high",
            forbidden_in_customer_pack=True,
            forbidden_in_operator_pack=False,
        ),
    ]


def parse_gantt_pack_yaml(path: Path) -> BrandGanttPack | None:
    """Load `gantt-pack.yml` and return a typed pack, or None if absent.

    Same contract as ``parse_register_pack_yaml`` for the sibling Pack A1
    surface: graceful absence; yaml import-tolerant; Pydantic schema is the
    contract.
    """
    if not path.exists():
        return None
    try:
        import yaml
    except ImportError:
        return None
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return BrandGanttPack.model_validate(raw)


def parse_locale_suffix_rules(path: Path) -> list[LocaleSuffixRule]:
    """Return the 3 per-locale README suffix rules per BRAND_MULTILINGUAL_CONTRACT.md §2.

    The §2 contract enumerates 3 active audience languages: fr (Tier 0), es
    (Tier 1), en (Tier 2). Returns ``[]`` when the canonical is absent.
    """
    if not path.exists():
        return []
    return [
        LocaleSuffixRule(
            locale="en",
            expected_suffix=".en.md",
            frontmatter_language_value="en",
        ),
        LocaleSuffixRule(
            locale="fr",
            expected_suffix=".fr.md",
            frontmatter_language_value="fr",
        ),
        LocaleSuffixRule(
            locale="es",
            expected_suffix=".es.md",
            frontmatter_language_value="es",
        ),
    ]


def parse_readme_triad_rules(path: Path) -> list[ReadmeTriadRule]:
    """Return the 5-line README triad rule per BRAND_MULTILINGUAL_CONTRACT.md §2 + D-IH-70-P.

    Returns one default rule with the pointer line-count window 5-12 (5-line
    skeleton + reasonable expansion room), required pointer keyword
    ``"Per-language READMEs:"`` from the §2 canonical example, and
    severity ``warning`` (downgradable to ``error`` via the C-71-2
    inline-ratify gate operationalised as ``default_triad_severity`` on
    ``BrandMultilingualPack``).
    """
    if not path.exists():
        return []
    return [
        ReadmeTriadRule(
            pointer_line_count_min=3,
            pointer_line_count_max=12,
            required_pointer_keywords=("Per-language READMEs:",),
            per_locale_readme_required=True,
            default_severity="warning",
        ),
    ]


def parse_multilingual_pack_yaml(path: Path) -> BrandMultilingualPack | None:
    """Load `multilingual-pack.yml` and return a typed pack, or None if absent.

    Same contract as ``parse_register_pack_yaml`` for the sibling Pack A1
    surface.
    """
    if not path.exists():
        return None
    try:
        import yaml
    except ImportError:
        return None
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return BrandMultilingualPack.model_validate(raw)


def parse_localised_format_rules(
    path: Path,
) -> tuple[
    list[NumberFormatRule],
    list[CurrencyFormatRule],
    list[DateFormatRule],
]:
    """Return per-locale number / currency / date format rules per BRAND_LOCALISED_FORMATS.md.

    The canonical declares fixed per-locale rules (en / fr / es). The parser
    emits them directly rather than parsing the canonical's markdown table
    fragilely; the canonical's existence remains the authority for "is this
    layer enabled" (parser returns empty triples when canonical is absent).
    """
    if not path.exists():
        return [], [], []

    NBSP_NARROW = "\u202F"  # U+202F NARROW NO-BREAK SPACE per fr thousands
    number_rules = [
        NumberFormatRule(
            locale="en",
            thousands_separator=",",
            decimal_separator=".",
        ),
        NumberFormatRule(
            locale="fr",
            thousands_separator=NBSP_NARROW,
            decimal_separator=",",
        ),
        NumberFormatRule(
            locale="es",
            thousands_separator=".",
            decimal_separator=",",
        ),
    ]
    currency_rules = [
        CurrencyFormatRule(
            locale="en", currency="EUR", symbol_position="prefix", symbol_separator=""
        ),
        CurrencyFormatRule(
            locale="fr", currency="EUR", symbol_position="suffix", symbol_separator=" "
        ),
        CurrencyFormatRule(
            locale="es", currency="EUR", symbol_position="suffix", symbol_separator=" "
        ),
        CurrencyFormatRule(
            locale="en", currency="USD", symbol_position="prefix", symbol_separator=""
        ),
        CurrencyFormatRule(
            locale="en", currency="GBP", symbol_position="prefix", symbol_separator=""
        ),
    ]
    date_rules = [
        DateFormatRule(
            locale="en",
            format_class="iso",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            example="2026-05-14",
        ),
        DateFormatRule(
            locale="fr",
            format_class="iso",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            example="2026-05-14",
        ),
        DateFormatRule(
            locale="es",
            format_class="iso",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            example="2026-05-14",
        ),
        DateFormatRule(
            locale="en",
            format_class="natural_long",
            pattern=r"^[A-Z][a-z]+ \d{1,2}, \d{4}$",
            example="May 14, 2026",
        ),
        DateFormatRule(
            locale="fr",
            format_class="natural_long",
            pattern=r"^\d{1,2} [a-zéûôîà]+ \d{4}$",
            example="14 mai 2026",
        ),
        DateFormatRule(
            locale="es",
            format_class="natural_long",
            pattern=r"^\d{1,2} de [a-záéíóúñ]+ de \d{4}$",
            example="14 de mayo de 2026",
        ),
    ]
    return number_rules, currency_rules, date_rules


# -----------------------------------------------------------------------------
# I71 P5 -- Pack A4 -- RenderOwnershipRule + RenderOwnershipPack chassis
# -----------------------------------------------------------------------------


class RenderOwnershipRule(BaseModel):
    """One row of WORKSPACE_BLUEPRINT_HOLISTIKA.md §16 render-pipeline ownership.

    Maps a per-deliverable-kind expected `role_owner` (matches a `role_name`
    from baseline_organisation.csv) to a surface glob describing where this
    deliverable lives in engagement folders (e.g.,
    ``02-customer-pack/deck.customer.*.md``).

    Pack A4 default_severity is ``warning`` per the discipline -- render
    ownership is forward-tracked advisory (transition triggers PMO -> RevOps
    when pipeline >= 3 active engagements; PMO -> HLK Tech Lab when render
    tooling complexity exceeds operator-handled threshold); transition hints
    don't block CI. Operators can promote to ``error`` via
    ``render-ownership-pack.yml`` per-rule overrides.
    """

    model_config = ConfigDict(frozen=True)

    deliverable_kind: DeliverableKind
    expected_role_owner: str = Field(min_length=1)
    surface_pattern: str = Field(min_length=1)
    default_severity: Severity = "warning"
    canonical_section: str = "WORKSPACE_BLUEPRINT_HOLISTIKA.md §16"


class RenderOwnershipPack(BaseModel):
    """Operator-editable render-ownership override pack.

    Loaded from `docs/.../Brand/canonicals/_validators/render-ownership-pack.yml`
    via ``parse_render_ownership_pack_yaml``. Same shape as
    ``BrandGanttPack`` / ``BrandMultilingualPack`` sibling packs.

    ``transition_trigger_hints`` carries the §16.3 forward-tracked transition
    advisories (PMO -> RevOps; PMO -> HLK Tech Lab) as free-form prose that
    the validator surfaces as ``info`` advisories when pipeline cardinality
    exceeds the threshold codified at WORKSPACE §16.3.
    """

    model_config = ConfigDict(frozen=True)

    pack_version: str = Field(pattern=r"^v[0-9]+\.[0-9]+\.[0-9]+$")
    last_edited: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_edited_by: str = Field(min_length=1)
    canonical_source_refs: tuple[str, ...]
    layers_enabled: dict[str, bool] = Field(default_factory=dict)
    render_ownership_rules: tuple[RenderOwnershipRule, ...] = ()
    transition_trigger_hints: tuple[str, ...] = ()


# -----------------------------------------------------------------------------
# I71 P5 -- Pack A4 parsers
# -----------------------------------------------------------------------------


def parse_render_ownership_rules(path: Path) -> list[RenderOwnershipRule]:
    """Return the 9 canonical render-ownership rules per WORKSPACE §16.

    The §16 structure is stable (per-owner table at §16.1 + per-deliverable
    owner-coverage check at §16.2 + transition triggers at §16.3). The parser
    emits the 9 rules directly with canonical ``role_owner`` (matching
    ``baseline_organisation.csv`` ``role_name`` values) rather than fragile
    markdown-table regex parsing (same approach as ``parse_audience_quadrants``
    for §2 of BRAND_GANTT_DISCIPLINE). Returns ``[]`` when the canonical is
    absent (graceful skip).

    Deliverable -> role_owner mapping derived from WORKSPACE §16.1:

        deck                 -> Copywriter       (Brand/Copywriter authors prose)
        proposal             -> PMO              (engagement orchestration)
        tarification         -> PMO              (engagement orchestration; financial)
        gantt                -> UX Designer      (Brand/UX-Designer; gantt discipline)
        dossier              -> PMO              (per-engagement companion artifact)
        counterparty_brief   -> Copywriter       (5-line README pointer per multilingual contract)
        objections           -> Account Manager  (per-account relationship signals)
        press                -> Storytelling Manager (M3 Storytelling sub-area; PR Manager subordinate)
        advisor_email        -> PMO              (engagement orchestration; advisor track)
    """
    if not path.exists():
        return []
    return [
        RenderOwnershipRule(
            deliverable_kind="deck",
            expected_role_owner="Copywriter",
            surface_pattern="02-customer-pack/deck.customer.*.md",
        ),
        RenderOwnershipRule(
            deliverable_kind="proposal",
            expected_role_owner="PMO",
            surface_pattern="02-customer-pack/proposal.*.md",
        ),
        RenderOwnershipRule(
            deliverable_kind="tarification",
            expected_role_owner="PMO",
            surface_pattern="02-customer-pack/tarification.*.md",
        ),
        RenderOwnershipRule(
            deliverable_kind="gantt",
            expected_role_owner="UX Designer",
            surface_pattern="02-customer-pack/gantt.*.md",
        ),
        RenderOwnershipRule(
            deliverable_kind="dossier",
            expected_role_owner="PMO",
            surface_pattern="02-customer-pack/dossier.*.md",
        ),
        RenderOwnershipRule(
            deliverable_kind="counterparty_brief",
            expected_role_owner="Copywriter",
            surface_pattern="README*.md",
        ),
        RenderOwnershipRule(
            deliverable_kind="objections",
            expected_role_owner="Account Manager",
            surface_pattern="01-operator-pack/objections*.md",
        ),
        RenderOwnershipRule(
            deliverable_kind="press",
            expected_role_owner="Storytelling Manager",
            surface_pattern="02-customer-pack/press*.md",
        ),
        RenderOwnershipRule(
            deliverable_kind="advisor_email",
            expected_role_owner="PMO",
            surface_pattern="02-customer-pack/advisor-email*.md",
        ),
    ]


def parse_render_ownership_pack_yaml(path: Path) -> RenderOwnershipPack | None:
    """Load `render-ownership-pack.yml` and return a typed pack, or None if absent.

    Same contract as ``parse_register_pack_yaml`` for the sibling Pack A1/A2/A3
    surfaces: graceful absence; yaml import-tolerant; Pydantic schema is the
    contract.
    """
    if not path.exists():
        return None
    try:
        import yaml
    except ImportError:
        return None
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return RenderOwnershipPack.model_validate(raw)


__all__ = [
    "Locale",
    "Severity",
    "GanttVariant",
    "SurfaceClass",
    "SubMarkClass",
    "VoicePersonaClass",
    "EngagementTypeClass",
    "DeliverableKind",
    "STANDARD_TIC_FAMILY_NAMES",
    "STANDARD_REGISTER_TOKEN_NAMES",
    "STANDARD_DELIVERABLE_KINDS",
    "CANONICAL_PATHS",
    "TicFamily",
    "RegisterRule",
    "AudienceQuadrant",
    "RegisterToken",
    "AudienceClass",
    "BoundaryRule",
    "SubMarkTier",
    "VoicePersona",
    "EngagementType",
    "LocaleLeakRule",
    "CobrandRule",
    "LLMToneTell",
    "TrackRecordRule",
    "BrandAbbreviationRule",
    "ArchetypeViolation",
    "BrandedHouseViolation",
    "BrandVoiceRegisterPack",
    # I71 P2 -- Pack A2 + A3 + Addition 11 additive surfaces
    "GanttConfidenceRule",
    "AudienceQuadrantRule",
    "LocaleSuffixRule",
    "ReadmeTriadRule",
    "NumberFormatRule",
    "CurrencyFormatRule",
    "DateFormatRule",
    "BrandGanttPack",
    "BrandMultilingualPack",
    "parse_tic_families_from_canonical",
    "parse_english_register_rules",
    "parse_llm_tone_tells",
    "parse_register_matrix",
    "parse_audience_quadrants",
    "parse_register_pack_yaml",
    # I71 P2 -- Pack A2 + A3 + Addition 11 parsers
    "parse_gantt_confidence_rules",
    "parse_audience_quadrant_rules",
    "parse_gantt_pack_yaml",
    "parse_locale_suffix_rules",
    "parse_readme_triad_rules",
    "parse_multilingual_pack_yaml",
    "parse_localised_format_rules",
    # I71 P5 -- Pack A4 additive surfaces + parsers
    "RenderOwnershipRule",
    "RenderOwnershipPack",
    "parse_render_ownership_rules",
    "parse_render_ownership_pack_yaml",
]
