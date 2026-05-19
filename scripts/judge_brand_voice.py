"""Brand-voice LLM-as-judge advisory CLI per I78 P1 + P2.

Paired runbook for ``akos/brand_voice_judge.py`` per
``akos-executable-process-catalog.mdc`` RULE 1. Sister CLI to
``scripts/validate_brand_voice_register.py`` (I71 P1 Pack A1 — deterministic
regex floor); this runbook lives one layer above as advisory semantics.

Usage::

    py scripts/judge_brand_voice.py --prose "Delve into the key takeaways" --audience external_register
    py scripts/judge_brand_voice.py --file path/to/draft.md --audience external_register --provider mock
    py scripts/judge_brand_voice.py --self-test           # mock-provider round-trip smoke
    py scripts/judge_brand_voice.py --print-config        # show defaults + loaded pack
    py scripts/judge_brand_voice.py --bias-audit-summary  # Strand C summary (P3 forward-chartered; stub today)

Exit codes:
    0 — verdict is pass OR mode is soft/advisory (advisory-only).
    1 — verdict is fail AND mode is strict (gate fires).
    2 — invalid input / file missing / provider misconfigured.

**Operator self-discipline pre-call** (per ``akos-brand-baseline-reality.mdc``):
the CLI enforces the audience-class → canonical-set mapping by refusing to fold
internal-register canonicals into external-register prompts and vice versa.

**Provider status**:
- ``mock``: deterministic in-process stub (default; offline-safe; used by tests).
- ``anthropic`` / ``openai`` / ``deepseek-r1-local`` / ``ollama``: framework
  scaffolds. The runtime call sites raise ``NotImplementedError`` with a
  pointer to ``config/openclaw.json.example`` provider wiring; concrete API
  integration is part of the strict-mode-promotion follow-up (forward-chartered
  from I78 P2 per ``D-IH-78-CLOSURE`` axis-2 pragmatic-closure executive call).

**P2 release-gate integration** (this commit): the gate runs this script in
``--self-test`` mode as an ``INFO`` advisory step — verifying the chassis loads
+ mock provider round-trips. Production prose-scanning rollout is deferred
until Strand C bias-audit cadence launches.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
from pathlib import Path

from akos.brand_voice_judge import (
    DEFAULT_CACHE_DIR_NAME,
    DEFAULT_JUDGE_MODE,
    DEFAULT_JUDGE_PROVIDER,
    DEFAULT_PROMPT_VERSION,
    BrandVoiceJudgeConfig,
    JudgeAudienceClass,
    JudgeMode,
    JudgeProvider,
    JudgeRequest,
    JudgeVerdict,
)
from akos.log import setup_logging

LOG = logging.getLogger("judge_brand_voice")


REPO_ROOT = Path(__file__).resolve().parent.parent
PACK_PATH_DEFAULT = (
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
    / "judge-pack.yml"
)

# Audience-class -> default canonical set (per akos-brand-baseline-reality.mdc).
# Folded into the system prompt when caller does not override via --canonical.
DEFAULT_CANONICALS_BY_AUDIENCE: dict[JudgeAudienceClass, tuple[str, ...]] = {
    "external_register": (
        # Public-vision region (operator-marked bracketed block); public BRAND files only.
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISION.md",
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ENGLISH_PATTERNS.md",
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_FRENCH_PATTERNS.md",
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_SPANISH_PATTERNS.md",
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_REGISTER_MATRIX.md",
    ),
    "internal_register": (
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md",
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ENGLISH_PATTERNS.md",
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_REGISTER_MATRIX.md",
    ),
}

# Mock-provider triggers — deterministic phrases that always FAIL in mock mode
# so the CLI is testable without live LLM calls. These mirror the I71 P1 register-
# rule "delve into" / "navigate the landscape" exemplars that the regex chassis
# already catches; the judge here demonstrates the *paraphrase* shape: same
# semantic violation, different lexical surface.
_MOCK_FAIL_PARAPHRASES: tuple[tuple[str, str, str], ...] = (
    (
        "delve into",
        "Delete the LLM filler 'delve into'; replace with a direct verb like 'review' or 'examine'.",
        "Paraphrase pattern of the canonical 'delve' tic family (BRAND_COPYWRITING_DISCIPLINE.md §2 Family 5).",
    ),
    (
        "drill down into",
        "Replace 'drill down into' with 'examine' or 'analyse'.",
        "Same brand violation as 'delve into' but with a different lexical surface; "
        "the deterministic regex chassis won't catch this — the judge does.",
    ),
    (
        "navigate the landscape",
        "Rewrite without 'landscape' metaphor; name what is actually being navigated.",
        "Performative-EN noun (BRAND_LLM_TONE_TELLS.md §4 noun-category).",
    ),
    (
        "unlock value",
        "Rewrite without 'unlock'; name the concrete change the work produced.",
        "BRAND_LLM_TONE_TELLS.md §3 verb-category — 'unlock' is a discipline-overuse hit.",
    ),
)


def _load_pack(pack_path: Path) -> BrandVoiceJudgeConfig | None:
    """Load ``judge-pack.yml`` if present; return None otherwise (chassis defaults apply).

    Mirrors the graceful-absence contract of
    ``akos.brand_voice_register.parse_register_pack_yaml``.
    """
    if not pack_path.is_file():
        return None
    try:
        import yaml  # local import; yaml is optional at module-load time
    except ImportError:
        LOG.warning("PyYAML not installed; chassis defaults apply (pack at %s ignored).", pack_path)
        return None
    raw = yaml.safe_load(pack_path.read_text(encoding="utf-8")) or {}
    return BrandVoiceJudgeConfig.model_validate(raw)


def _canonical_set_for(audience: JudgeAudienceClass, override: tuple[str, ...]) -> tuple[str, ...]:
    return override if override else DEFAULT_CANONICALS_BY_AUDIENCE[audience]


def _mock_verdict(req: JudgeRequest) -> JudgeVerdict:
    """Deterministic in-process verdict for offline / test runs.

    The mock provider scans the prose for the canonical paraphrase exemplars
    in ``_MOCK_FAIL_PARAPHRASES``; if hit, emits a ``fail`` verdict with the
    matching rewrite suggestion. Otherwise emits ``pass``. Cost = 0; latency =
    deterministic small integer derived from the prose hash so the verdict
    is fully reproducible from inputs.
    """
    prose_lower = req.prose.lower()
    canonicals = _canonical_set_for(req.audience_class, req.canonical_paths)
    for needle, suggestion, rationale in _MOCK_FAIL_PARAPHRASES:
        if needle in prose_lower:
            return JudgeVerdict(
                request_cache_key=req.cache_key(),
                verdict="fail",
                severity="warning",  # mock default; real provider can escalate to 'error'
                rationale=f"[mock] {rationale}",
                suggested_rewrite=suggestion,
                canonicals_cited=canonicals,
                provider_used=req.provider,
                prompt_version=req.prompt_version,
                cost_eur=0.0,
                latency_ms=int(hashlib.sha256(req.prose.encode("utf-8")).hexdigest()[:4], 16) % 100,
            )
    return JudgeVerdict(
        request_cache_key=req.cache_key(),
        verdict="pass",
        severity="pass",
        rationale="[mock] No canonical paraphrase patterns detected in prose under audit.",
        suggested_rewrite=None,
        canonicals_cited=canonicals,
        provider_used=req.provider,
        prompt_version=req.prompt_version,
        cost_eur=0.0,
        latency_ms=int(hashlib.sha256(req.prose.encode("utf-8")).hexdigest()[:4], 16) % 100,
    )


def _live_provider_call(req: JudgeRequest) -> JudgeVerdict:
    """Stub for live provider calls; raises NotImplementedError today.

    Concrete Anthropic/OpenAI/DeepSeek-R1/Ollama wiring is part of the
    strict-mode-promotion follow-up initiative (forward-chartered from I78
    P2 closure per axis-2 pragmatic-closure executive call). When the
    follow-up activates, this function dispatches per ``req.provider``.
    """
    raise NotImplementedError(
        f"Live provider {req.provider!r} not wired in P1+P2 — forward-chartered to the "
        "strict-mode-promotion follow-up initiative (D-IH-78-PROMOTE gate). "
        "Use --provider mock for chassis exercise + tests today."
    )


def judge(req: JudgeRequest) -> JudgeVerdict:
    """Single judge invocation. Dispatches by provider; mock is the only live path today."""
    if req.provider == "mock":
        return _mock_verdict(req)
    return _live_provider_call(req)


def _emit_json(verdict: JudgeVerdict) -> None:
    print(json.dumps(verdict.model_dump(mode="json"), indent=2, sort_keys=True))


def _self_test() -> int:
    """Mock-provider round-trip smoke (called from release-gate INFO advisory).

    Verifies: chassis loads; default audience -> canonical-set mapping
    resolves; mock provider returns deterministic verdict; cache-key is
    stable across identical inputs.
    """
    req_pass = JudgeRequest(prose="The project ships next week.", audience_class="external_register")
    req_fail = JudgeRequest(prose="We delve into the customer pain.", audience_class="external_register")
    v_pass = judge(req_pass)
    v_fail = judge(req_fail)
    assert v_pass.verdict == "pass", f"self-test PASS leg failed: {v_pass!r}"
    assert v_fail.verdict == "fail", f"self-test FAIL leg failed: {v_fail!r}"
    assert v_pass.request_cache_key != v_fail.request_cache_key, "cache keys must differ across inputs"
    req_dup = JudgeRequest(prose=req_pass.prose, audience_class=req_pass.audience_class)
    assert req_pass.cache_key() == req_dup.cache_key(), "cache key must be deterministic for identical inputs"
    LOG.info("self-test PASS — mock provider round-trips clean (2/2 verdicts; cache keys stable).")
    return 0


def _bias_audit_summary() -> int:
    """Strand C summary stub (P3 forward-chartered).

    Returns a structured placeholder indicating Strand C bias-audit cadence
    has not yet launched per the I78 cluster-burndown axis-2 pragmatic-closure
    executive call. Operators querying this flag get a clear pointer to the
    successor strict-mode-promotion initiative when it activates.
    """
    payload = {
        "status": "deferred",
        "reason": (
            "I78 P3 (30-day bias audit launch) forward-chartered to a strict-mode-promotion "
            "follow-up initiative per D-IH-78-CLOSURE axis-2 pragmatic-closure. The bias-audit "
            "log file BRAND_VOICE_JUDGE_BIAS_LOG.md is the durable evidence shape; this CLI "
            "summary surfaces actual rates only when the follow-up initiative has minted bias rows."
        ),
        "next_review_trigger": (
            "Operator decision to mint INIT-OPENCLAW_AKOS-78-PROMOTE (or equivalent) and "
            "configure a live judge provider in config/openclaw.json."
        ),
        "schema_locked": "akos/brand_voice_judge.py::JudgeBiasMitigation",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--prose", type=str, default=None, help="Prose under audit (verbatim).")
    parser.add_argument("--file", type=Path, default=None, help="Read prose from a file.")
    parser.add_argument(
        "--audience",
        type=str,
        choices=("internal_register", "external_register"),
        default="external_register",
        help="Audience class per akos-brand-baseline-reality.mdc dual-register contract.",
    )
    parser.add_argument(
        "--provider",
        type=str,
        choices=("mock", "anthropic", "openai", "deepseek-r1-local", "ollama"),
        default=DEFAULT_JUDGE_PROVIDER,
        help="Judge provider; only 'mock' is wired in P1+P2.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=("soft", "strict", "advisory"),
        default=DEFAULT_JUDGE_MODE,
        help="soft/advisory = INFO-only; strict = exit 1 on fail.",
    )
    parser.add_argument("--locale", type=str, choices=("en", "fr", "es"), default="en")
    parser.add_argument(
        "--prompt-version",
        type=str,
        default=DEFAULT_PROMPT_VERSION,
        help="Judge-prompt registry version per akos.brand_voice_judge.JudgePromptVersion.",
    )
    parser.add_argument("--surface-path", type=str, default=None)
    parser.add_argument(
        "--pack-path",
        type=Path,
        default=PACK_PATH_DEFAULT,
        help="Path to operator-editable judge-pack.yml (chassis defaults apply when absent).",
    )
    parser.add_argument("--json-log", action="store_true")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Mock-provider round-trip smoke; used by release-gate INFO advisory.",
    )
    parser.add_argument(
        "--bias-audit-summary",
        action="store_true",
        help="Print Strand C bias-audit summary (P3 forward-chartered today).",
    )
    parser.add_argument(
        "--print-config",
        action="store_true",
        help="Print chassis defaults + loaded pack as JSON.",
    )
    args = parser.parse_args()
    setup_logging(json_output=args.json_log)

    if args.self_test:
        return _self_test()

    if args.bias_audit_summary:
        return _bias_audit_summary()

    if args.print_config:
        pack = _load_pack(args.pack_path)
        payload = {
            "chassis_defaults": {
                "provider": DEFAULT_JUDGE_PROVIDER,
                "mode": DEFAULT_JUDGE_MODE,
                "prompt_version": DEFAULT_PROMPT_VERSION,
                "cache_dir": DEFAULT_CACHE_DIR_NAME,
            },
            "pack_loaded": pack.model_dump(mode="json") if pack else None,
            "pack_path": str(args.pack_path),
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if args.prose is None and args.file is None:
        LOG.error("Provide --prose, --file, --self-test, --bias-audit-summary, or --print-config.")
        return 2
    if args.prose is not None and args.file is not None:
        LOG.error("--prose and --file are mutually exclusive.")
        return 2

    if args.file is not None:
        if not args.file.is_file():
            LOG.error("--file %s does not exist.", args.file)
            return 2
        prose = args.file.read_text(encoding="utf-8")
    else:
        prose = args.prose or ""

    if not prose.strip():
        LOG.error("Prose under audit is empty.")
        return 2

    req = JudgeRequest(
        prose=prose,
        audience_class=args.audience,  # type: ignore[arg-type]
        provider=args.provider,  # type: ignore[arg-type]
        prompt_version=args.prompt_version,
        locale=args.locale,
        mode=args.mode,  # type: ignore[arg-type]
        surface_path=args.surface_path,
    )

    try:
        verdict = judge(req)
    except NotImplementedError as exc:
        LOG.error(str(exc))
        return 2

    _emit_json(verdict)

    if verdict.verdict == "fail" and args.mode == "strict":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
