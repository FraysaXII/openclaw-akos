"""Pydantic chassis for the universal MADEIRA voice/personality contract per I76 P3 Lane C.

PROSE-FIRST canonical mint per operator ratify 2026-05-19 21:00 (`D-IH-76-G`):
SOP + Pydantic chassis only at v1; **no CSV registry today**. CSV promotion
deferred to I76 P5 UAT signal when N>1 operator OR N>1 AIC OR N>3 role-classes
prove the need (operator quote: "not overengineered" — keep the v1 surface tight).

This module is the runtime SSOT for the **9-trait closed vocabulary**
(`STANDARD_TRAIT_VOCABULARY: frozenset[str]`) per `D-IH-76-H`, the **3-class
v1 audience constraint set** (`STANDARD_AUDIENCE_CONSTRAINTS`) per
`D-IH-76-I`, the **anti-sycophancy 3-consecutive-agreement default**
(`OperatorVoiceProfile.anti_sycophancy_threshold`) per `D-IH-76-J`, the
**FK-only corpus access pattern** (`OperatorVoiceProfile.corpus_paths`) per
`D-IH-76-K`, the **quarterly knowledge-test cadence default**
(`OperatorVoiceProfile.knowledge_test_cadence_days = 90`) per `D-IH-76-L`,
and the **per-AIC re-load posture** (no shared session state across AICs;
each AIC loads its profile fresh at session start) per `D-IH-76-M`.

Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-TECH_MADEIRA_PERSONALITY_001.md``.

Paired runbook: ``scripts/madeira_personality_check.py`` (load + voice-audit
subcommands; consumes ``akos.brand_baseline_reality.scan_text`` for jargon-leak
detection).

Two seed profiles ship in :data:`STANDARD_VOICE_PROFILES`:

- ``voice_akos_founder_2026`` — Founder/CEO voice: all 5 founder traits
  (methodology-checkpoint-explicit, cite-by-file-path-and-line,
  numbered-explicit-lists, multilingual-en-fr-es, lowercase-casual);
  audience_constraint = (`J-OP`, `J-AD-post-NDA`, `J-CO`).
- ``voice_akos_system_owner_2026`` — System Owner voice: all 4 system-owner
  traits (validator-first, evidence-citation-required, decision-id-explicit,
  pause-point-conscious) + cite-by-file-path-and-line shared;
  audience_constraint = (`J-OP`,) only.

Extension contract: adding a trait to ``STANDARD_TRAIT_VOCABULARY`` or an
audience to ``STANDARD_AUDIENCE_CONSTRAINTS`` is a **canonical-gate semantics**
operation per `D-IH-76-H` + `D-IH-76-I` (PR + operator ratify + test). Adding
a profile to ``STANDARD_VOICE_PROFILES`` is similarly canonical-gated. None of
these are runtime-mutable (`frozen=True, extra="forbid"`).

Cross-references:
- `BRAND_BASELINE_REALITY_MATRIX.md` §3 — dual-register vocabulary contract
  (the BBR scanner enforces external-register on outputs; this module enforces
  voice + persona + audience-routing on Madeira's emission shape).
- `akos.brand_baseline_reality` — the BBR scanner the voice-audit runbook
  consumes for jargon-leak detection (Lane A lifted at 5e90dd4).
- `akos-brand-baseline-reality.mdc` — sister cursor rule.
- `akos-people-discipline-of-disciplines.mdc` — anti-jargon discipline +
  Madeira-named-explicit pattern.
- `akos-executable-process-catalog.mdc` RULE 1 — SOP+runbook pairing.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


VoiceTrait = Literal[
    "methodology-checkpoint-explicit",
    "cite-by-file-path-and-line",
    "numbered-explicit-lists",
    "multilingual-en-fr-es",
    "lowercase-casual",
    "validator-first",
    "evidence-citation-required",
    "decision-id-explicit",
    "pause-point-conscious",
]
"""Closed 9-trait vocabulary per `D-IH-76-H`. Founder set (5) +
System Owner set (4). Additions via Pydantic edit + canonical-gate."""


STANDARD_TRAIT_VOCABULARY: frozenset[str] = frozenset(
    {
        "methodology-checkpoint-explicit",
        "cite-by-file-path-and-line",
        "numbered-explicit-lists",
        "multilingual-en-fr-es",
        "lowercase-casual",
        "validator-first",
        "evidence-citation-required",
        "decision-id-explicit",
        "pause-point-conscious",
    }
)
"""Frozen 9-trait set per `D-IH-76-H`. Pydantic enforces subset semantics on
``OperatorVoiceProfile.traits``."""


FOUNDER_TRAITS: tuple[str, ...] = (
    "methodology-checkpoint-explicit",
    "cite-by-file-path-and-line",
    "numbered-explicit-lists",
    "multilingual-en-fr-es",
    "lowercase-casual",
)
"""The 5 founder traits per `D-IH-76-H` ratify. Used by the founder seed profile."""


SYSTEM_OWNER_TRAITS: tuple[str, ...] = (
    "validator-first",
    "evidence-citation-required",
    "decision-id-explicit",
    "pause-point-conscious",
)
"""The 4 system-owner traits per `D-IH-76-H` ratify. Used by the system-owner seed
profile; `cite-by-file-path-and-line` is also inherited (shared trait)."""


AudienceConstraint = Literal["J-OP", "J-AD-post-NDA", "J-CO"]
"""v1 audience constraint set per `D-IH-76-I`. Three classes:
- ``J-OP`` (operator-internal) — chat with operator + cleared agents + AICs.
- ``J-AD-post-NDA`` (advisor post-NDA) — adviser cleared on internal vocab.
- ``J-CO`` (collaborator) — methodology peers + open-source contributors +
  academic research-collaborators per AUDIENCE_REGISTRY.csv. Operator
  framing: this is extensible via Pydantic ``Literal`` + canonical-gate."""


STANDARD_AUDIENCE_CONSTRAINTS: frozenset[str] = frozenset(
    {"J-OP", "J-AD-post-NDA", "J-CO"}
)
"""Frozen v1 audience constraint set per `D-IH-76-I`. Pydantic enforces
subset semantics on ``OperatorVoiceProfile.audience_constraint``."""


_PROFILE_ID_PATTERN = r"^voice_[a-z0-9_]+$"
_METHODOLOGY_VERSION_PATTERN = r"^v\d+\.\d+$"
_ISO_DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"

_DEFAULT_ANTI_SYCOPHANCY_THRESHOLD = 3
"""Per `D-IH-76-J`: 3 consecutive Madeira emissions agreeing without surfacing
counter-options triggers friction-injection (validator emits INFO warning)."""

_DEFAULT_KNOWLEDGE_TEST_CADENCE_DAYS = 90
"""Per `D-IH-76-L`: quarterly inline-ratify cadence (does voice profile still
match operator's lived voice?). Default 90 days."""


class OperatorVoiceProfile(BaseModel):
    """One operator-voice profile. Frozen + extra-forbid per CONTRIBUTING.md.

    Each profile binds a closed trait set (subset of
    :data:`STANDARD_TRAIT_VOCABULARY`) to a closed audience-constraint set
    (subset of :data:`STANDARD_AUDIENCE_CONSTRAINTS`) plus FK-only corpus
    paths (paths into FOUNDER_CORPUS_INVENTORY when that canonical lands;
    runbook reads paths but never inlines content per `D-IH-76-K`).

    The chassis encodes operator-ratified defaults so AICs can self-load the
    profile at session start (per `D-IH-76-M` per-AIC re-load) without
    re-deriving the voice contract from scratch every time.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    profile_id: str = Field(
        ...,
        min_length=1,
        pattern=_PROFILE_ID_PATTERN,
        description="Stable identifier; pattern ^voice_[a-z0-9_]+$ (e.g., voice_akos_founder_2026).",
    )
    profile_name: str = Field(
        ...,
        min_length=1,
        description="Human-readable name (Title Case OK; e.g., 'AKOS Founder Voice 2026').",
    )
    description: str = Field(
        ...,
        min_length=1,
        description="One-line description of which operator/role this profile captures.",
    )
    traits: tuple[VoiceTrait, ...] = Field(
        ...,
        min_length=1,
        description=(
            "Closed trait set per D-IH-76-H. Non-empty; subset of "
            "STANDARD_TRAIT_VOCABULARY; deduplicated by validator."
        ),
    )
    audience_constraint: tuple[AudienceConstraint, ...] = Field(
        ...,
        min_length=1,
        description=(
            "Closed audience-constraint set per D-IH-76-I v1 set "
            "{J-OP, J-AD-post-NDA, J-CO}. Non-empty; subset of "
            "STANDARD_AUDIENCE_CONSTRAINTS; deduplicated by validator."
        ),
    )
    corpus_paths: tuple[str, ...] = Field(
        ...,
        min_length=1,
        description=(
            "FK-only paths into FOUNDER_CORPUS_INVENTORY (forward-chartered "
            "canonical at C-76-A; runbook reads paths but never inlines "
            "content per D-IH-76-K access_level 5 confidentiality "
            "preservation)."
        ),
    )
    anti_sycophancy_threshold: int = Field(
        default=_DEFAULT_ANTI_SYCOPHANCY_THRESHOLD,
        ge=1,
        description=(
            "Consecutive Madeira-agreement emissions in J-OP/Methodology "
            "triggering friction-injection per D-IH-76-J. Default 3."
        ),
    )
    knowledge_test_cadence_days: int = Field(
        default=_DEFAULT_KNOWLEDGE_TEST_CADENCE_DAYS,
        ge=30,
        description=(
            "Days between quarterly inline-ratify 'does this profile still "
            "match your lived voice?' per D-IH-76-L. Default 90 (quarterly); "
            "minimum 30."
        ),
    )
    last_knowledge_test_at: Optional[str] = Field(
        default=None,
        pattern=_ISO_DATE_PATTERN,
        description=(
            "ISO date (YYYY-MM-DD) of the last operator-ratified knowledge "
            "test. None = never tested (initial mint state); runbook surfaces "
            "inline-ratify when (today - last_knowledge_test_at) > "
            "knowledge_test_cadence_days."
        ),
    )
    methodology_version: str = Field(
        ...,
        pattern=_METHODOLOGY_VERSION_PATTERN,
        description=(
            "HLK methodology version at profile mint (pattern ^v\\d+\\.\\d+$; "
            "e.g., v3.1). Bumped when the profile is re-ratified under a new "
            "methodology version."
        ),
    )

    @model_validator(mode="after")
    def _enforce_trait_vocabulary_subset(self) -> "OperatorVoiceProfile":
        """Every trait must be in STANDARD_TRAIT_VOCABULARY. Catches drift."""
        for trait in self.traits:
            if trait not in STANDARD_TRAIT_VOCABULARY:
                raise ValueError(
                    f"profile_id={self.profile_id}: trait {trait!r} not in "
                    f"STANDARD_TRAIT_VOCABULARY (closed 9-trait set per "
                    f"D-IH-76-H); add via canonical-gate Pydantic edit"
                )
        return self

    @model_validator(mode="after")
    def _enforce_traits_deduplicated(self) -> "OperatorVoiceProfile":
        """traits tuple must not carry duplicates."""
        if len(self.traits) != len(set(self.traits)):
            raise ValueError(
                f"profile_id={self.profile_id}: traits has duplicates: "
                f"{list(self.traits)}"
            )
        return self

    @model_validator(mode="after")
    def _enforce_audience_constraint_subset(self) -> "OperatorVoiceProfile":
        """Every audience-constraint value must be in STANDARD_AUDIENCE_CONSTRAINTS."""
        for aud in self.audience_constraint:
            if aud not in STANDARD_AUDIENCE_CONSTRAINTS:
                raise ValueError(
                    f"profile_id={self.profile_id}: audience_constraint entry "
                    f"{aud!r} not in STANDARD_AUDIENCE_CONSTRAINTS (v1 set per "
                    f"D-IH-76-I); add via canonical-gate Pydantic edit"
                )
        return self

    @model_validator(mode="after")
    def _enforce_audience_constraint_deduplicated(self) -> "OperatorVoiceProfile":
        """audience_constraint tuple must not carry duplicates."""
        if len(self.audience_constraint) != len(set(self.audience_constraint)):
            raise ValueError(
                f"profile_id={self.profile_id}: audience_constraint has "
                f"duplicates: {list(self.audience_constraint)}"
            )
        return self


STANDARD_VOICE_PROFILES: dict[str, OperatorVoiceProfile] = {
    "voice_akos_founder_2026": OperatorVoiceProfile(
        profile_id="voice_akos_founder_2026",
        profile_name="AKOS Founder Voice 2026",
        description=(
            "Founder/CEO (operator) voice as of 2026 methodology v3.1: "
            "methodology-first, cite-anchored, numbered-list-explicit, "
            "trilingual EN/FR/ES, lowercase casual register."
        ),
        traits=(
            "methodology-checkpoint-explicit",
            "cite-by-file-path-and-line",
            "numbered-explicit-lists",
            "multilingual-en-fr-es",
            "lowercase-casual",
        ),
        audience_constraint=("J-OP", "J-AD-post-NDA", "J-CO"),
        corpus_paths=(
            "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_CORPUS_INVENTORY.md",
        ),
        anti_sycophancy_threshold=_DEFAULT_ANTI_SYCOPHANCY_THRESHOLD,
        knowledge_test_cadence_days=_DEFAULT_KNOWLEDGE_TEST_CADENCE_DAYS,
        last_knowledge_test_at=None,
        methodology_version="v3.1",
    ),
    "voice_akos_system_owner_2026": OperatorVoiceProfile(
        profile_id="voice_akos_system_owner_2026",
        profile_name="AKOS System Owner Voice 2026",
        description=(
            "System Owner voice as of 2026 methodology v3.1: validator-first, "
            "evidence-citation-required, decision-id-explicit, pause-point-conscious, "
            "with cite-by-file-path-and-line shared with the founder voice."
        ),
        traits=(
            "validator-first",
            "evidence-citation-required",
            "decision-id-explicit",
            "pause-point-conscious",
            "cite-by-file-path-and-line",
        ),
        audience_constraint=("J-OP",),
        corpus_paths=(
            "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_CORPUS_INVENTORY.md",
        ),
        anti_sycophancy_threshold=_DEFAULT_ANTI_SYCOPHANCY_THRESHOLD,
        knowledge_test_cadence_days=_DEFAULT_KNOWLEDGE_TEST_CADENCE_DAYS,
        last_knowledge_test_at=None,
        methodology_version="v3.1",
    ),
}
"""Two seed profiles per `D-IH-76-G` PROSE-FIRST mint. The corpus_paths value
points at the **forward-chartered** ``FOUNDER_CORPUS_INVENTORY.md`` canonical
(slot ID ``C-76-A``); the inventory itself does not exist yet at v1 — it is
deferred to a successor commit/initiative once operator ratifies its content
shape (this profile chassis only encodes the *path FK* per the FK-only
contract in `D-IH-76-K`, not the corpus content)."""


def get_profile(profile_id: str) -> OperatorVoiceProfile:
    """Resolve a profile by ``profile_id`` from :data:`STANDARD_VOICE_PROFILES`.

    Raises ``KeyError`` when ``profile_id`` is unknown (AICs at session start
    per `D-IH-76-M` per-AIC re-load: catch the KeyError + fall back to the
    operator-default profile ``voice_akos_founder_2026`` if no AIC-specific
    profile is registered).
    """
    if profile_id not in STANDARD_VOICE_PROFILES:
        raise KeyError(
            f"profile_id={profile_id!r} not in STANDARD_VOICE_PROFILES; "
            f"known profiles: {sorted(STANDARD_VOICE_PROFILES.keys())}"
        )
    return STANDARD_VOICE_PROFILES[profile_id]


__all__ = [
    "AudienceConstraint",
    "FOUNDER_TRAITS",
    "OperatorVoiceProfile",
    "STANDARD_AUDIENCE_CONSTRAINTS",
    "STANDARD_TRAIT_VOCABULARY",
    "STANDARD_VOICE_PROFILES",
    "SYSTEM_OWNER_TRAITS",
    "VoiceTrait",
    "get_profile",
]
