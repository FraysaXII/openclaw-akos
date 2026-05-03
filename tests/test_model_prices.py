"""Tests for ``config/eval/model-prices.json`` (Initiative 50 P2 truth-up).

Schema, sanity, and monotonic-ordering tests so 2026-Q2-style pricing
refreshes don't silently regress (R-50-1).

Cross-references:
- Initiative 50 P2 (`docs/wip/planning/50-live-cycle-closure/master-roadmap.md`).
- Decision D-IH-50-A (formalize cost ceilings via POLICY rows).
- Consumer: ``akos.eval_harness.cost_obs.MODEL_PRICES_PATH``.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MODEL_PRICES_PATH = REPO_ROOT / "config" / "eval" / "model-prices.json"


@pytest.fixture(scope="module")
def model_prices() -> dict:
    raw = MODEL_PRICES_PATH.read_text(encoding="utf-8")
    return json.loads(raw)


def test_model_prices_file_exists():
    assert MODEL_PRICES_PATH.exists(), (
        f"Missing canonical pricing source: {MODEL_PRICES_PATH}. "
        "akos.eval_harness.cost_obs depends on this path."
    )


def test_top_level_keys_present(model_prices: dict):
    required = {"_note", "_last_reviewed", "_owner_role", "models"}
    missing = required - set(model_prices.keys())
    assert not missing, f"model-prices.json missing top-level keys: {sorted(missing)}"


def test_last_reviewed_is_iso_date(model_prices: dict):
    raw = model_prices["_last_reviewed"]
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw), (
        f"_last_reviewed must be YYYY-MM-DD; got {raw!r}"
    )
    parsed = _dt.date.fromisoformat(raw)
    assert parsed <= _dt.date.today() + _dt.timedelta(days=1), (
        f"_last_reviewed in the future: {parsed}"
    )


def test_owner_role_is_finops(model_prices: dict):
    assert model_prices["_owner_role"] == "FinOps", (
        "FinOps owns model pricing per AKOS responsibility matrix; "
        "do not reassign without operator approval."
    )


def test_models_is_non_empty_mapping(model_prices: dict):
    models = model_prices["models"]
    assert isinstance(models, dict) and models, "models must be a non-empty mapping"


@pytest.mark.parametrize("model_id", [
    "deterministic:akos.intent.classify_request",
    "ollama:nomic-embed-text",
    "anthropic:claude-3-5-sonnet-20241022",
    "openai:gpt-4o-mini",
    "openai:gpt-4o",
])
def test_canonical_models_present(model_prices: dict, model_id: str):
    assert model_id in model_prices["models"], (
        f"Canonical model entry missing: {model_id!r}. "
        "Removing entries breaks historical cassette cost reproducibility."
    )


def test_each_model_has_required_fields(model_prices: dict):
    required_fields = {"input_per_1k_usd", "output_per_1k_usd", "tier"}
    for model_id, entry in model_prices["models"].items():
        missing = required_fields - set(entry.keys())
        assert not missing, (
            f"Model {model_id!r} missing required fields: {sorted(missing)}"
        )


VALID_TIERS = frozenset({"deterministic", "cheap", "mid", "flagship"})


def test_each_model_tier_is_valid(model_prices: dict):
    for model_id, entry in model_prices["models"].items():
        tier = entry["tier"]
        assert tier in VALID_TIERS, (
            f"Model {model_id!r} tier {tier!r} not in {sorted(VALID_TIERS)}"
        )


def test_each_model_prices_are_non_negative(model_prices: dict):
    for model_id, entry in model_prices["models"].items():
        for key in ("input_per_1k_usd", "output_per_1k_usd"):
            value = entry[key]
            assert isinstance(value, (int, float)), (
                f"{model_id!r}.{key} not numeric: {value!r}"
            )
            assert value >= 0, f"{model_id!r}.{key} negative: {value}"


def test_output_price_at_least_input_price(model_prices: dict):
    """Output tokens are at least as expensive as input tokens for every commercial provider
    we currently track (Anthropic + OpenAI 2026-Q2). Local Ollama and deterministic
    entries have both at 0.0 which trivially satisfies the invariant.
    """
    for model_id, entry in model_prices["models"].items():
        in_price = entry["input_per_1k_usd"]
        out_price = entry["output_per_1k_usd"]
        assert out_price >= in_price, (
            f"{model_id!r}: output_per_1k_usd ({out_price}) < "
            f"input_per_1k_usd ({in_price}). 2026-Q2 reality check failed; "
            "either a real pricing inversion shipped (rare; needs operator review) "
            "or an entry was edited incorrectly."
        )


def test_cheap_tier_strictly_cheaper_than_flagship(model_prices: dict):
    """For input *and* output price separately, the maximum across cheap-tier
    entries must be strictly less than the minimum across flagship-tier
    entries. Catches accidental swap of cheap and flagship rows.
    """
    cheap_in: list[float] = []
    cheap_out: list[float] = []
    flagship_in: list[float] = []
    flagship_out: list[float] = []

    for entry in model_prices["models"].values():
        if entry["tier"] == "cheap":
            cheap_in.append(entry["input_per_1k_usd"])
            cheap_out.append(entry["output_per_1k_usd"])
        elif entry["tier"] == "flagship":
            flagship_in.append(entry["input_per_1k_usd"])
            flagship_out.append(entry["output_per_1k_usd"])

    if cheap_in and flagship_in:
        assert max(cheap_in) < min(flagship_in), (
            f"cheap-tier max input ({max(cheap_in)}) >= "
            f"flagship-tier min input ({min(flagship_in)}). "
            "Likely tier-label swap in model-prices.json."
        )
    if cheap_out and flagship_out:
        assert max(cheap_out) < min(flagship_out), (
            f"cheap-tier max output ({max(cheap_out)}) >= "
            f"flagship-tier min output ({min(flagship_out)})."
        )


def test_deterministic_and_local_zero_priced(model_prices: dict):
    """Deterministic + local ollama entries must remain $0/$0; non-zero values
    indicate accidental LLM substitution (POL-EVAL-COST-CEILING-SHARED-LOCALE-DETECT
    pattern from I45 P4).
    """
    zero_required = {
        "deterministic:akos.intent.classify_request",
        "ollama:nomic-embed-text",
    }
    for model_id in zero_required:
        entry = model_prices["models"][model_id]
        assert entry["input_per_1k_usd"] == 0.0, (
            f"{model_id!r} should remain $0 input — non-zero indicates "
            "accidental LLM substitution"
        )
        assert entry["output_per_1k_usd"] == 0.0, (
            f"{model_id!r} should remain $0 output"
        )


def test_2026_q2_reference_prices(model_prices: dict):
    """Hard-pin to 2026-Q2-published reference prices to lock in the I50 P2 truth-up.
    If a real price change ships, this test must be updated together with the
    model-prices.json refresh and a decision-log entry in the relevant initiative.
    """
    reference_2026_q2: dict[str, tuple[float, float]] = {
        "anthropic:claude-3-5-sonnet-20241022": (0.003, 0.015),
        "openai:gpt-4o-mini": (0.00015, 0.0006),
        "openai:gpt-4o": (0.0025, 0.01),
    }
    for model_id, (expected_in, expected_out) in reference_2026_q2.items():
        entry = model_prices["models"][model_id]
        assert entry["input_per_1k_usd"] == expected_in, (
            f"{model_id!r} input price ({entry['input_per_1k_usd']}) "
            f"!= 2026-Q2 reference ({expected_in}). Update both this test "
            "and the decision-log if a real price change occurred."
        )
        assert entry["output_per_1k_usd"] == expected_out, (
            f"{model_id!r} output price ({entry['output_per_1k_usd']}) "
            f"!= 2026-Q2 reference ({expected_out})."
        )


def test_2026_q2_review_note_present(model_prices: dict):
    """The I50 P2 truth-up records a verification note. Future quarterly truth-ups
    should overwrite this key (or add a sibling); the test only enforces that
    *some* explicit review note exists at file level."""
    review_keys = [k for k in model_prices.keys() if k.startswith("_") and "review" in k.lower()]
    assert review_keys, (
        "model-prices.json must carry at least one _*review* key documenting the "
        "most recent verification. I50 P2 added _2026_q2_review_note."
    )
