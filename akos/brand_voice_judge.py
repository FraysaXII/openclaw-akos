"""Pydantic chassis for the brand-voice LLM-as-judge advisory layer (I78 P1).

Sister module to ``akos/brand_voice_register.py`` (I71 P1 Pack A1 — the deterministic
regex floor). The judge runs **one layer above** the register: catches paraphrased
violations the regex chassis can't see, returns structured verdicts (PASS / FAIL /
INFO + severity + rationale + suggested rewrite), and runs in **soft mode by default**
while the bias-audit cadence (Strand C — forward-chartered to a strict-mode-promotion
follow-up initiative per I78 cluster-burndown axis-2 pragmatic-closure) establishes
false-positive / false-negative thresholds.

Architecture per I78 candidate Strand B:

- ``JudgeRequest`` — prose under audit + which canonicals to use as system prompt
  + which provider + which prompt version.
- ``JudgeVerdict`` — structured response from the LLM judge (verdict + severity +
  rationale + suggested rewrite + position-bias trace).
- ``JudgePromptVersion`` — versioned judge prompt registry; cache-busts when bumped.
- ``JudgeBiasMitigation`` — bias-test result row (position / verbosity /
  self-preference / authority) per Strand C.
- ``BrandVoiceJudgeConfig`` — operator-tunable knobs (provider, cost ceiling,
  caching mode, run-after-pack-a1 flag) loaded from ``judge-pack.yml``.

**Operator self-discipline pre-call (per akos-brand-baseline-reality.mdc):**
The judge consumes brand canonicals as system prompt. The dual-register contract
applies: when the prose under audit is external-tagged (J-IN / J-CU / J-ENISA /
etc. per ``akos-external-render-discipline.mdc``), the judge prompt MUST be the
external-register canonicals (BRAND_VISION.md public-vision region, public BRAND
files). When the prose is internal-tagged (J-OP), internal-register canonicals
(BRAND_BASELINE_REALITY_MATRIX.md full body, CORPINT vocabulary) are admissible.
Mixing registers in the judge system prompt produces incoherent verdicts; the
``JudgeRequest`` validator enforces the audience-tag → canonical-set mapping.

**Provider abstraction**: ``JudgeProvider`` is a Literal of supported LLM
providers per ``config/openclaw.json.example`` multi-provider SSOT. P1 ships
``mock`` (deterministic in-process stub for tests + offline use) + ``anthropic``
+ ``openai`` + ``deepseek-r1-local``; concrete API wiring lives in
``scripts/judge_brand_voice.py`` runtime layer to keep this chassis framework-pure.

**Closure shape (per I78 cluster-burndown executive call)**: P1 (this module) +
P2 (release-gate INFO advisory wiring) close in Wave H of the I86 cluster
burndown. P3 (30-day bias audit launch) + P4 (promotion-to-strict ratification)
+ P5 (closure UAT) forward-charter to a successor strict-mode-promotion
follow-up initiative; the candidate Strand D bias-audit gates remain the gate
for the strict-mode promotion (no calendar promotion). ``D-IH-78-CLOSURE``
ratifies this closure shape with reversibility = single-diff (a successor
``D-IH-78-PROMOTE`` can flip back to active when bias-audit signals fire).
"""

from __future__ import annotations

import hashlib
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# -----------------------------------------------------------------------------
# Type aliases (Literal-based enums per akos.brand_voice_register chassis pattern)
# -----------------------------------------------------------------------------

JudgeProvider = Literal[
    "mock",
    "anthropic",
    "openai",
    "deepseek-r1-local",
    "ollama",
]
"""Supported judge providers per ``config/openclaw.json.example`` multi-provider SSOT.

``mock`` is the deterministic in-process stub used by tests + offline operation;
returns canned verdicts based on prose-hash modulo for reproducibility.
"""

JudgeMode = Literal["soft", "strict", "advisory"]
"""Judge mode per I78 candidate §3 Strand B.

- ``soft`` (default): emit verdict + suggested rewrite; never block (treated as INFO).
- ``strict``: emit verdict; FAIL on severity error; mutable per-bias-category opt-out
  via ``judge-pack.yml`` overrides.
- ``advisory``: alias for ``soft`` retained for I71 Pack A1 parity (``AKOS_BRAND_VOICE_REGISTER_SOFT=1``).

Promotion from ``soft`` to ``strict`` is gated on Strand C bias-audit completion
+ explicit operator ratify at ``D-IH-78-PROMOTE`` (forward-chartered; not in P2).
"""

JudgeSeverity = Literal["error", "warning", "info", "pass"]
"""Per-verdict severity. ``pass`` = no violation detected; the rest map to one
of the standard severities for downstream sink-handling parity with
``akos.brand_voice_register.Severity``.
"""

JudgeBiasCategory = Literal[
    "position",
    "verbosity",
    "self_preference",
    "authority",
]
"""4 canonical bias categories per Strand C (LMSYS chatbot arena + LLM-as-a-Judge
survey). Each carries a separate measurement that promotion-to-strict reads
(quantitative thresholds per C-78-4).
"""

JudgeAudienceClass = Literal[
    "internal_register",
    "external_register",
]
"""Audience-class binary that selects the judge's canonical system-prompt
corpus. ``internal_register`` reads BRAND_BASELINE_REALITY_MATRIX.md +
internal CORPINT vocabulary; ``external_register`` reads the public BRAND
files + BRAND_VISION.md public-vision region only. Mixed-register prose under
audit must be split into segments and judged twice (one per register), then
the verdicts merged at the consumer layer.

Per ``akos-brand-baseline-reality.mdc`` §"When generating prose, ask one
question" — the audience-class question maps 1:1 onto this enum.
"""

JudgePromptCategory = Literal[
    "register_compliance",
    "voice_consistency",
    "audience_appropriateness",
    "rewrite_suggestion",
]
"""4 canonical judge-prompt categories. The judge prompt is composed at
runtime by concatenating the active category-templates; this enum keeps the
composition typed.
"""


# -----------------------------------------------------------------------------
# Canonical constants
# -----------------------------------------------------------------------------

DEFAULT_JUDGE_PROVIDER: JudgeProvider = "mock"
"""Default provider for offline / test runs. Operator overrides via
``judge-pack.yml`` or ``AKOS_BRAND_VOICE_JUDGE_PROVIDER`` env var."""

DEFAULT_JUDGE_MODE: JudgeMode = "soft"
"""Default mode per I78 candidate Strand B + axis-2 cluster-burndown
executive call. ``strict`` requires Strand C bias-audit completion."""

DEFAULT_COST_CEILING_EUR_MONTH: int = 50
"""Hard ceiling per C-78-2 default; circuit-breaker fires when exceeded."""

DEFAULT_CACHE_DIR_NAME: str = ".akos-cache/judge"
"""Cache directory relative to repo root. Cache key = SHA256(prose +
prompt_version + canonical_set_sha256) per C-78-3 default."""

DEFAULT_PROMPT_VERSION: str = "v1.0.0"
"""Initial judge-prompt version. Bumping invalidates all cached verdicts per
C-78-6 default (full invalidation; aggressive caching absorbs re-run cost)."""


# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------


class JudgePromptVersion(BaseModel):
    """Versioned judge-prompt registry entry.

    Bumping ``version`` invalidates all cached verdicts that reference the
    previous version (per C-78-6 default). The ``canonical_basis`` field
    captures which brand canonicals were folded into the prompt at this
    version; downstream consumers can FK-resolve against
    ``akos.brand_voice_register.CANONICAL_PATHS`` to verify the basis.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    version: str = Field(..., pattern=r"^v[0-9]+\.[0-9]+\.[0-9]+$")
    audience_class: JudgeAudienceClass
    category: JudgePromptCategory
    canonical_basis: tuple[str, ...] = Field(..., min_length=1)
    template_sha256: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    minted_at: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")


class JudgeRequest(BaseModel):
    """One judge invocation. The CLI consumes this to issue a provider call."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    prose: str = Field(..., min_length=1, description="The prose under audit (verbatim).")
    audience_class: JudgeAudienceClass = Field(
        ...,
        description="Determines which canonicals are folded into the system prompt; "
        "enforced by ``akos-brand-baseline-reality.mdc`` dual-register contract.",
    )
    provider: JudgeProvider = DEFAULT_JUDGE_PROVIDER
    prompt_version: str = Field(default=DEFAULT_PROMPT_VERSION, pattern=r"^v[0-9]+\.[0-9]+\.[0-9]+$")
    locale: Literal["en", "fr", "es"] = "en"
    mode: JudgeMode = DEFAULT_JUDGE_MODE
    surface_path: str | None = Field(
        default=None,
        description="Optional path to the source artifact (for cache key + verdict provenance).",
    )
    canonical_paths: tuple[str, ...] = Field(
        default=(),
        description="Optional override of which canonicals to fold into the system prompt; "
        "empty = default per audience_class. Each entry must FK-resolve to "
        "``akos.brand_voice_register.CANONICAL_PATHS`` values.",
    )

    def cache_key(self) -> str:
        """Deterministic cache key per C-78-3 aggressive-caching default.

        Hashes: prose + audience_class + provider + prompt_version + locale +
        sorted canonical_paths. Surface path is intentionally excluded so that
        identical prose at different surfaces hits the same cache entry.
        """
        h = hashlib.sha256()
        h.update(self.prose.encode("utf-8"))
        h.update(self.audience_class.encode("utf-8"))
        h.update(self.provider.encode("utf-8"))
        h.update(self.prompt_version.encode("utf-8"))
        h.update(self.locale.encode("utf-8"))
        for p in sorted(self.canonical_paths):
            h.update(p.encode("utf-8"))
        return h.hexdigest()


class JudgeVerdict(BaseModel):
    """Structured response from the judge."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    request_cache_key: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    verdict: Literal["pass", "fail", "info"]
    severity: JudgeSeverity
    rationale: str = Field(..., min_length=1, description="Operator-readable reasoning.")
    suggested_rewrite: str | None = Field(
        default=None,
        description="Concrete rewrite suggestion when verdict is fail/info; "
        "None when verdict is pass.",
    )
    canonicals_cited: tuple[str, ...] = Field(
        default=(),
        description="Which canonical files the rationale references.",
    )
    provider_used: JudgeProvider
    prompt_version: str = Field(..., pattern=r"^v[0-9]+\.[0-9]+\.[0-9]+$")
    cost_eur: float = Field(default=0.0, ge=0.0, description="Estimated cost for this call.")
    latency_ms: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def _pass_has_no_rewrite(self) -> JudgeVerdict:
        if self.verdict == "pass" and self.suggested_rewrite is not None:
            raise ValueError(
                "verdict=pass cannot carry suggested_rewrite; rewrites are emitted only "
                "for fail/info verdicts."
            )
        if self.verdict == "fail" and self.severity == "pass":
            raise ValueError("verdict=fail cannot carry severity=pass.")
        return self


class JudgeBiasMitigation(BaseModel):
    """One bias-test result row per Strand C audit cadence.

    Forward-chartered to the strict-mode-promotion follow-up initiative; this
    model is shipped in P1 to lock the schema so the bias-audit log file
    (``BRAND_VOICE_JUDGE_BIAS_LOG.md``) doesn't drift when audit cadence
    actually launches.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    bias_category: JudgeBiasCategory
    test_name: str = Field(..., min_length=1)
    sample_size: int = Field(..., ge=1)
    false_positive_rate: float = Field(..., ge=0.0, le=1.0)
    false_negative_rate: float = Field(..., ge=0.0, le=1.0)
    measured_at: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    measured_by: str = Field(..., min_length=1)
    notes: str | None = None


class BrandVoiceJudgeConfig(BaseModel):
    """Operator-tunable knobs loaded from ``judge-pack.yml``.

    Mirrors ``BrandVoiceRegisterPack`` shape per I71 P1 Pack A1 sibling
    pattern. Operator overrides apply over chassis defaults; the YAML pack is
    the final word at runtime.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    pack_version: str = Field(..., pattern=r"^v[0-9]+\.[0-9]+\.[0-9]+$")
    last_edited: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_edited_by: str = Field(..., min_length=1)
    enabled: bool = Field(default=True)
    default_provider: JudgeProvider = DEFAULT_JUDGE_PROVIDER
    default_mode: JudgeMode = DEFAULT_JUDGE_MODE
    cost_ceiling_eur_month: int = Field(default=DEFAULT_COST_CEILING_EUR_MONTH, ge=1)
    cache_dir: str = Field(default=DEFAULT_CACHE_DIR_NAME, min_length=1)
    prompt_versions: tuple[JudgePromptVersion, ...] = Field(default=())
    run_after_pack_a1_only: bool = Field(
        default=True,
        description="C-78-7 default: judge only fires on prose Pack A1 passed; "
        "exposed for spot-audit override via ``--judge-all-surfaces``.",
    )
    per_bias_category_strict_optout: tuple[JudgeBiasCategory, ...] = Field(
        default=(),
        description="Per-Strand-D operator override surface — bias categories "
        "still being audited stay opt-out from strict mode until ratify.",
    )
    notes: str | None = None

    @field_validator("prompt_versions")
    @classmethod
    def _unique_version_audience_category_keys(
        cls, v: tuple[JudgePromptVersion, ...]
    ) -> tuple[JudgePromptVersion, ...]:
        seen: set[tuple[str, str, str]] = set()
        for pv in v:
            key = (pv.version, pv.audience_class, pv.category)
            if key in seen:
                raise ValueError(
                    f"duplicate prompt-version composite key {key!r} in pack; each "
                    "(version, audience_class, category) triple must be unique."
                )
            seen.add(key)
        return v


__all__ = [
    "DEFAULT_CACHE_DIR_NAME",
    "DEFAULT_COST_CEILING_EUR_MONTH",
    "DEFAULT_JUDGE_MODE",
    "DEFAULT_JUDGE_PROVIDER",
    "DEFAULT_PROMPT_VERSION",
    "BrandVoiceJudgeConfig",
    "JudgeAudienceClass",
    "JudgeBiasCategory",
    "JudgeBiasMitigation",
    "JudgeMode",
    "JudgePromptCategory",
    "JudgePromptVersion",
    "JudgeProvider",
    "JudgeRequest",
    "JudgeSeverity",
    "JudgeVerdict",
]
