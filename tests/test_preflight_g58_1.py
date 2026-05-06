"""Regression tests for ``scripts/preflight_g58_1.py`` (Initiative 58 A.0 gate).

Locks the G-58-1 contract:

* exactly 11 checks run.
* exit 0 only when every check passes.
* ``MAX_DOSSIER_USD`` ceiling is enforced at the D-IH-57-G inheritance value.
* RunPod / Kalavai alias seam (D-IH-58-G) accepts either canonical or alias.
* Truthy parsing for AKOS_RECORD_LIVE / AKOS_GRAPHRAG_POC_LIVE rejects ``0``.
* ``AKOS_JUDGE_ROSTER`` requires both Anthropic and OpenAI providers.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "preflight_g58_1.py"


def _load_module():
    """Import the preflight script under a private module name for testing.

    The module is registered in ``sys.modules`` before ``exec_module`` so
    introspection paths (``cls.__module__`` lookups) resolve cleanly under
    Python 3.14.
    """
    spec = importlib.util.spec_from_file_location("preflight_g58_1", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["preflight_g58_1"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def preflight(monkeypatch, tmp_path):
    """Yield the preflight module with a clean env (all 11 vars unset).

    Redirects ``OPENCLAW_HOME`` to a temp directory so
    ``bootstrap_openclaw_process_env()`` (called inside ``main()``) does not
    re-populate the env from the operator's real ``~/.openclaw/.env`` —
    otherwise tests that depend on a key being *unset* would silently see
    real placeholder values flow back in.
    """
    module = _load_module()

    monkeypatch.setenv("OPENCLAW_HOME", str(tmp_path))

    for var in (
        "AKOS_RECORD_LIVE",
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE_KEY",
        "MAX_DOSSIER_USD",
        "RUNPOD_ENDPOINT_URL",
        "VLLM_RUNPOD_URL",
        "KALAVAI_ENDPOINT_URL",
        "VLLM_SHADOW_URL",
        "AKOS_JUDGE_ROSTER",
        "AKOS_GRAPHRAG_POC_LIVE",
    ):
        monkeypatch.delenv(var, raising=False)

    yield module


def _all_set(monkeypatch) -> None:
    """Populate every env var with a satisfying value (used as a baseline)."""
    monkeypatch.setenv("AKOS_RECORD_LIVE", "1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("SUPABASE_URL", "https://swrmqpelgoblaquequzb.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "eyJtest")
    monkeypatch.setenv("MAX_DOSSIER_USD", "50")
    monkeypatch.setenv("VLLM_RUNPOD_URL", "http://localhost:8000/v1")
    monkeypatch.setenv("VLLM_SHADOW_URL", "https://kalavai.test/v1")
    monkeypatch.setenv("AKOS_JUDGE_ROSTER", "anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o")
    monkeypatch.setenv("AKOS_GRAPHRAG_POC_LIVE", "1")


def test_evaluate_checks_returns_exactly_11_results(preflight):
    """The pre-flight contract is locked at 11 checks (D-IH-58 P0 spec)."""
    results = preflight.evaluate_checks()
    assert len(results) == 11


def test_clean_env_reports_all_misses(preflight):
    """With no env vars set, exactly 1 of 11 is met (the alarm script presence)."""
    results = preflight.evaluate_checks()
    met, total = preflight.summarize(results)
    assert total == 11
    assert met == 1
    alarm_check = next(r for r in results if r.name == "endpoint_envelope_alarm.py")
    assert alarm_check.available is True


def test_full_env_returns_zero(preflight, monkeypatch):
    """Operator paste-complete env passes G-58-1."""
    _all_set(monkeypatch)
    rc = preflight.main([])
    assert rc == 0


def test_main_returns_one_on_any_miss(preflight, monkeypatch):
    """Even one missing prerequisite trips G-58-1 NO-FIRE."""
    _all_set(monkeypatch)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    rc = preflight.main([])
    assert rc == 1


def test_max_dossier_usd_above_ceiling_fails(preflight, monkeypatch):
    """D-IH-57-G inheritance: anything above 50 is a hard miss, not a warn."""
    _all_set(monkeypatch)
    monkeypatch.setenv("MAX_DOSSIER_USD", "100")
    results = preflight.evaluate_checks()
    envelope = next(r for r in results if r.name == "MAX_DOSSIER_USD")
    assert envelope.available is False
    assert "ceiling" in envelope.detail


def test_max_dossier_usd_non_integer_fails(preflight, monkeypatch):
    """Garbage strings are missed, not silently coerced."""
    _all_set(monkeypatch)
    monkeypatch.setenv("MAX_DOSSIER_USD", "twenty-five")
    results = preflight.evaluate_checks()
    envelope = next(r for r in results if r.name == "MAX_DOSSIER_USD")
    assert envelope.available is False


def test_max_dossier_usd_within_ceiling_passes(preflight, monkeypatch):
    """Operator may pick a value below 50 (e.g., 25) for tighter discipline."""
    _all_set(monkeypatch)
    monkeypatch.setenv("MAX_DOSSIER_USD", "25")
    results = preflight.evaluate_checks()
    envelope = next(r for r in results if r.name == "MAX_DOSSIER_USD")
    assert envelope.available is True


def test_runpod_alias_seam_resolves_either_name(preflight, monkeypatch):
    """D-IH-58-G alias seam: VLLM_RUNPOD_URL and RUNPOD_ENDPOINT_URL are equivalent at the gate."""
    _all_set(monkeypatch)
    monkeypatch.delenv("VLLM_RUNPOD_URL", raising=False)
    monkeypatch.setenv("RUNPOD_ENDPOINT_URL", "http://runpod.test/v1")
    results = preflight.evaluate_checks()
    runpod = next(r for r in results if r.name == "VLLM_RUNPOD_URL or RUNPOD_ENDPOINT_URL")
    assert runpod.available is True
    assert "alias" in runpod.detail


def test_kalavai_alias_seam_resolves_either_name(preflight, monkeypatch):
    """D-IH-58-G alias seam: VLLM_SHADOW_URL and KALAVAI_ENDPOINT_URL are equivalent at the gate."""
    _all_set(monkeypatch)
    monkeypatch.delenv("VLLM_SHADOW_URL", raising=False)
    monkeypatch.setenv("KALAVAI_ENDPOINT_URL", "https://kalavai.alias.test/v1")
    results = preflight.evaluate_checks()
    kal = next(r for r in results if r.name == "VLLM_SHADOW_URL or KALAVAI_ENDPOINT_URL")
    assert kal.available is True
    assert "alias" in kal.detail


def test_runpod_both_unset_fails(preflight, monkeypatch):
    _all_set(monkeypatch)
    monkeypatch.delenv("VLLM_RUNPOD_URL", raising=False)
    monkeypatch.delenv("RUNPOD_ENDPOINT_URL", raising=False)
    results = preflight.evaluate_checks()
    runpod = next(r for r in results if r.name == "VLLM_RUNPOD_URL or RUNPOD_ENDPOINT_URL")
    assert runpod.available is False


def test_truthy_parsing_rejects_zero(preflight, monkeypatch):
    """``AKOS_RECORD_LIVE=0`` is a miss, not a partial credit."""
    _all_set(monkeypatch)
    monkeypatch.setenv("AKOS_RECORD_LIVE", "0")
    results = preflight.evaluate_checks()
    rec = next(r for r in results if r.name == "AKOS_RECORD_LIVE")
    assert rec.available is False


def test_judge_roster_rejects_single_member(preflight, monkeypatch):
    """Single-member rosters fail (consensus mode requires >=2 members)."""
    _all_set(monkeypatch)
    monkeypatch.setenv("AKOS_JUDGE_ROSTER", "anthropic:claude-sonnet-4-5")
    results = preflight.evaluate_checks()
    roster = next(r for r in results if r.name == "AKOS_JUDGE_ROSTER")
    assert roster.available is False
    assert "1" in roster.detail or "member" in roster.detail.lower()


def test_judge_roster_truthy_with_cross_family(preflight, monkeypatch):
    """Canonical cross-family pair (anthropic + openai) is preferred."""
    _all_set(monkeypatch)
    results = preflight.evaluate_checks()
    roster = next(r for r in results if r.name == "AKOS_JUDGE_ROSTER")
    assert roster.available is True
    assert "cross-family" in roster.detail.lower()


def test_judge_roster_accepts_in_family_fallback(preflight, monkeypatch):
    """Per D-IH-58-I: 2-member same-family roster is a valid fallback while
    OPS-58-2 (OpenAI key rotation) remains open."""
    _all_set(monkeypatch)
    monkeypatch.setenv(
        "AKOS_JUDGE_ROSTER",
        "anthropic:claude-sonnet-4-5,anthropic:claude-haiku-4-5",
    )
    results = preflight.evaluate_checks()
    roster = next(r for r in results if r.name == "AKOS_JUDGE_ROSTER")
    assert roster.available is True
    assert "in-family" in roster.detail.lower()
    assert "anthropic" in roster.detail.lower()


def test_judge_roster_rejects_unknown_provider_prefix(preflight, monkeypatch):
    """Members must start with anthropic: or openai: (the two SDKs the
    dispatcher knows how to dispatch)."""
    _all_set(monkeypatch)
    monkeypatch.setenv(
        "AKOS_JUDGE_ROSTER", "cohere:command-r,mistral:large"
    )
    results = preflight.evaluate_checks()
    roster = next(r for r in results if r.name == "AKOS_JUDGE_ROSTER")
    assert roster.available is False
    assert "provider prefix" in roster.detail.lower()


def test_render_table_lists_all_eleven(preflight):
    """The rendered table has 11 data rows + 2 header rows = 13 lines."""
    results = preflight.evaluate_checks()
    table = preflight.render_table(results)
    lines = table.splitlines()
    assert len(lines) == 13
    assert "Prerequisite" in lines[0]
