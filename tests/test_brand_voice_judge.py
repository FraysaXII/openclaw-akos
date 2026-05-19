"""Tests for akos/brand_voice_judge.py + scripts/judge_brand_voice.py per I78 P1+P2."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from akos.brand_voice_judge import (
    DEFAULT_CACHE_DIR_NAME,
    DEFAULT_COST_CEILING_EUR_MONTH,
    DEFAULT_JUDGE_MODE,
    DEFAULT_JUDGE_PROVIDER,
    DEFAULT_PROMPT_VERSION,
    BrandVoiceJudgeConfig,
    JudgeBiasMitigation,
    JudgePromptVersion,
    JudgeRequest,
    JudgeVerdict,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
CLI_PATH = REPO_ROOT / "scripts" / "judge_brand_voice.py"


def _load_cli_module():
    spec = importlib.util.spec_from_file_location("judge_brand_voice", CLI_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("judge_brand_voice", module)
    spec.loader.exec_module(module)
    return module


# -----------------------------------------------------------------------------
# Pydantic chassis tests (akos/brand_voice_judge.py)
# -----------------------------------------------------------------------------


@pytest.mark.brand
class TestJudgeChassisDefaults:
    def test_default_provider_is_mock(self):
        assert DEFAULT_JUDGE_PROVIDER == "mock"

    def test_default_mode_is_soft(self):
        assert DEFAULT_JUDGE_MODE == "soft"

    def test_default_prompt_version_pattern(self):
        assert DEFAULT_PROMPT_VERSION.startswith("v")
        assert DEFAULT_PROMPT_VERSION.count(".") == 2

    def test_default_cost_ceiling_is_positive(self):
        assert DEFAULT_COST_CEILING_EUR_MONTH >= 1

    def test_default_cache_dir_is_subpath(self):
        assert "/judge" in DEFAULT_CACHE_DIR_NAME


@pytest.mark.brand
class TestJudgeRequest:
    def test_minimal_request_validates(self):
        req = JudgeRequest(prose="hello", audience_class="external_register")
        assert req.provider == "mock"
        assert req.mode == "soft"
        assert req.locale == "en"
        assert req.prompt_version == DEFAULT_PROMPT_VERSION

    def test_empty_prose_rejected(self):
        with pytest.raises(ValidationError):
            JudgeRequest(prose="", audience_class="external_register")

    def test_unknown_audience_rejected(self):
        with pytest.raises(ValidationError):
            JudgeRequest(prose="x", audience_class="rude_register")  # type: ignore[arg-type]

    def test_invalid_prompt_version_rejected(self):
        with pytest.raises(ValidationError):
            JudgeRequest(
                prose="x",
                audience_class="external_register",
                prompt_version="not-semver",
            )

    def test_unknown_provider_rejected(self):
        with pytest.raises(ValidationError):
            JudgeRequest(
                prose="x",
                audience_class="external_register",
                provider="bedrock",  # type: ignore[arg-type]
            )

    def test_unknown_locale_rejected(self):
        with pytest.raises(ValidationError):
            JudgeRequest(
                prose="x",
                audience_class="external_register",
                locale="de",  # type: ignore[arg-type]
            )

    def test_extra_field_rejected(self):
        with pytest.raises(ValidationError):
            JudgeRequest(
                prose="x",
                audience_class="external_register",
                surprise=True,  # type: ignore[call-arg]
            )

    def test_cache_key_is_deterministic(self):
        a = JudgeRequest(prose="hello", audience_class="external_register")
        b = JudgeRequest(prose="hello", audience_class="external_register")
        assert a.cache_key() == b.cache_key()

    def test_cache_key_differs_on_prose(self):
        a = JudgeRequest(prose="hello world", audience_class="external_register")
        b = JudgeRequest(prose="hello there", audience_class="external_register")
        assert a.cache_key() != b.cache_key()

    def test_cache_key_differs_on_audience(self):
        a = JudgeRequest(prose="hello", audience_class="external_register")
        b = JudgeRequest(prose="hello", audience_class="internal_register")
        assert a.cache_key() != b.cache_key()

    def test_cache_key_ignores_surface_path(self):
        a = JudgeRequest(prose="hello", audience_class="external_register", surface_path="/x.md")
        b = JudgeRequest(prose="hello", audience_class="external_register", surface_path="/y.md")
        assert a.cache_key() == b.cache_key()


@pytest.mark.brand
class TestJudgeVerdict:
    def test_pass_verdict_validates(self):
        v = JudgeVerdict(
            request_cache_key="a" * 64,
            verdict="pass",
            severity="pass",
            rationale="no violation",
            suggested_rewrite=None,
            provider_used="mock",
            prompt_version="v1.0.0",
        )
        assert v.verdict == "pass"

    def test_pass_with_rewrite_rejected(self):
        with pytest.raises(ValidationError):
            JudgeVerdict(
                request_cache_key="a" * 64,
                verdict="pass",
                severity="pass",
                rationale="no violation",
                suggested_rewrite="rewrite here",
                provider_used="mock",
                prompt_version="v1.0.0",
            )

    def test_fail_with_severity_pass_rejected(self):
        with pytest.raises(ValidationError):
            JudgeVerdict(
                request_cache_key="a" * 64,
                verdict="fail",
                severity="pass",
                rationale="violation",
                suggested_rewrite="fix",
                provider_used="mock",
                prompt_version="v1.0.0",
            )

    def test_invalid_cache_key_rejected(self):
        with pytest.raises(ValidationError):
            JudgeVerdict(
                request_cache_key="not-a-sha",
                verdict="pass",
                severity="pass",
                rationale="x",
                provider_used="mock",
                prompt_version="v1.0.0",
            )

    def test_negative_cost_rejected(self):
        with pytest.raises(ValidationError):
            JudgeVerdict(
                request_cache_key="a" * 64,
                verdict="pass",
                severity="pass",
                rationale="x",
                provider_used="mock",
                prompt_version="v1.0.0",
                cost_eur=-1.0,
            )


@pytest.mark.brand
class TestJudgePromptVersion:
    def test_valid_prompt_version(self):
        pv = JudgePromptVersion(
            version="v1.0.0",
            audience_class="external_register",
            category="register_compliance",
            canonical_basis=("docs/foo/BRAND_FOO.md",),
            template_sha256="0" * 64,
            minted_at="2026-05-19",
        )
        assert pv.version == "v1.0.0"

    def test_empty_canonical_basis_rejected(self):
        with pytest.raises(ValidationError):
            JudgePromptVersion(
                version="v1.0.0",
                audience_class="external_register",
                category="register_compliance",
                canonical_basis=(),
                template_sha256="0" * 64,
                minted_at="2026-05-19",
            )

    def test_invalid_sha256_rejected(self):
        with pytest.raises(ValidationError):
            JudgePromptVersion(
                version="v1.0.0",
                audience_class="external_register",
                category="register_compliance",
                canonical_basis=("x",),
                template_sha256="not-hex",
                minted_at="2026-05-19",
            )

    def test_invalid_date_rejected(self):
        with pytest.raises(ValidationError):
            JudgePromptVersion(
                version="v1.0.0",
                audience_class="external_register",
                category="register_compliance",
                canonical_basis=("x",),
                template_sha256="0" * 64,
                minted_at="not-iso",
            )


@pytest.mark.brand
class TestBiasMitigation:
    def test_valid_row(self):
        b = JudgeBiasMitigation(
            bias_category="position",
            test_name="position-swap-en",
            sample_size=42,
            false_positive_rate=0.03,
            false_negative_rate=0.07,
            measured_at="2026-05-19",
            measured_by="Brand & Narrative Manager",
        )
        assert b.bias_category == "position"

    def test_out_of_range_rate_rejected(self):
        with pytest.raises(ValidationError):
            JudgeBiasMitigation(
                bias_category="position",
                test_name="x",
                sample_size=1,
                false_positive_rate=1.5,
                false_negative_rate=0.0,
                measured_at="2026-05-19",
                measured_by="x",
            )

    def test_zero_sample_size_rejected(self):
        with pytest.raises(ValidationError):
            JudgeBiasMitigation(
                bias_category="position",
                test_name="x",
                sample_size=0,
                false_positive_rate=0.0,
                false_negative_rate=0.0,
                measured_at="2026-05-19",
                measured_by="x",
            )


@pytest.mark.brand
class TestBrandVoiceJudgeConfig:
    def test_minimal_config_validates(self):
        cfg = BrandVoiceJudgeConfig(
            pack_version="v1.0.0",
            last_edited="2026-05-19",
            last_edited_by="Brand & Narrative Manager",
        )
        assert cfg.enabled
        assert cfg.default_provider == "mock"

    def test_duplicate_prompt_version_key_rejected(self):
        pv = JudgePromptVersion(
            version="v1.0.0",
            audience_class="external_register",
            category="register_compliance",
            canonical_basis=("x",),
            template_sha256="0" * 64,
            minted_at="2026-05-19",
        )
        with pytest.raises(ValidationError):
            BrandVoiceJudgeConfig(
                pack_version="v1.0.0",
                last_edited="2026-05-19",
                last_edited_by="x",
                prompt_versions=(pv, pv),
            )


# -----------------------------------------------------------------------------
# CLI tests (scripts/judge_brand_voice.py)
# -----------------------------------------------------------------------------


@pytest.mark.brand
class TestCLI:
    def test_self_test_returns_zero(self):
        cli = _load_cli_module()
        rc = cli._self_test()
        assert rc == 0

    def test_mock_pass_path(self):
        cli = _load_cli_module()
        req = JudgeRequest(prose="The project ships next week.", audience_class="external_register")
        v = cli.judge(req)
        assert v.verdict == "pass"
        assert v.suggested_rewrite is None
        assert v.provider_used == "mock"
        assert v.cost_eur == 0.0

    def test_mock_fail_delve_paraphrase(self):
        cli = _load_cli_module()
        req = JudgeRequest(
            prose="We delve into the customer pain to unlock value.",
            audience_class="external_register",
        )
        v = cli.judge(req)
        assert v.verdict == "fail"
        assert v.suggested_rewrite is not None
        assert "delve" in v.rationale or "delve" in (v.suggested_rewrite or "")

    def test_mock_fail_drill_paraphrase(self):
        cli = _load_cli_module()
        req = JudgeRequest(
            prose="Drill down into the data to find insights.",
            audience_class="external_register",
        )
        v = cli.judge(req)
        assert v.verdict == "fail"

    def test_live_provider_raises_not_implemented(self):
        cli = _load_cli_module()
        req = JudgeRequest(prose="x", audience_class="external_register", provider="anthropic")
        with pytest.raises(NotImplementedError):
            cli.judge(req)

    def test_canonical_set_external_register(self):
        cli = _load_cli_module()
        canonicals = cli._canonical_set_for("external_register", ())
        assert any("BRAND_VISION.md" in c for c in canonicals)
        assert any("BRAND_REGISTER_MATRIX.md" in c for c in canonicals)
        assert not any("BRAND_BASELINE_REALITY_MATRIX.md" in c for c in canonicals)

    def test_canonical_set_internal_register(self):
        cli = _load_cli_module()
        canonicals = cli._canonical_set_for("internal_register", ())
        assert any("BRAND_BASELINE_REALITY_MATRIX.md" in c for c in canonicals)

    def test_canonical_set_override_takes_precedence(self):
        cli = _load_cli_module()
        custom = ("docs/foo/CUSTOM.md",)
        canonicals = cli._canonical_set_for("external_register", custom)
        assert canonicals == custom

    def test_bias_audit_summary_returns_zero(self, capsys):
        cli = _load_cli_module()
        rc = cli._bias_audit_summary()
        assert rc == 0
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["status"] == "deferred"
        assert "JudgeBiasMitigation" in payload["schema_locked"]
