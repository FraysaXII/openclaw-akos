"""Initiative 47 P14 tests — Tier B 4-D matrix extension.

Coverage:
- workflow YAML structure preserved (still triggers on schedule + workflow_dispatch)
- Matrix dimensions extended with `persona` (Tier-1 + OPERATOR)
- Per-persona spend cap MAX_PERSONA_USD env var
- AKOS_JUDGE_COST_CAP env var wired
- SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY exposed (P13 item 4 dependency)
- Tier-2/3 personas excluded from default schedule (only via persona_filter input)
- --persona flag passed through to scripts/eval.py invocations
- Job summary surfaces compliance.eval_run writer stats
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "eval-tier-b.yml"


@pytest.fixture(scope="module")
def yaml_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Workflow shape preserved
# ---------------------------------------------------------------------------

def test_workflow_file_exists(yaml_text: str) -> None:
    assert WORKFLOW.is_file()
    assert "name: eval-tier-b" in yaml_text


def test_workflow_still_triggers_on_schedule(yaml_text: str) -> None:
    assert "schedule:" in yaml_text
    assert "cron: '0 6 * * 1'" in yaml_text


def test_workflow_still_triggers_on_workflow_dispatch(yaml_text: str) -> None:
    assert "workflow_dispatch:" in yaml_text
    assert "max_spend_usd:" in yaml_text


def test_workflow_gated_by_repo_var(yaml_text: str) -> None:
    """Operator opt-in via AKOS_TIER_B_ENABLED repo var preserved."""
    assert "vars.AKOS_TIER_B_ENABLED" in yaml_text


# ---------------------------------------------------------------------------
# 4-D matrix extension (D-IH-47-H)
# ---------------------------------------------------------------------------

def test_matrix_includes_model_tier_dim(yaml_text: str) -> None:
    assert "model_tier:" in yaml_text
    assert "cheap" in yaml_text and "flagship" in yaml_text


def test_matrix_includes_persona_dim(yaml_text: str) -> None:
    """I47 P14: persona is a matrix dimension."""
    assert "persona:" in yaml_text


def test_default_persona_matrix_includes_tier1_plus_operator(yaml_text: str) -> None:
    """OPERATOR + 4 Tier-1 personas in the default matrix; Tier-2/3 excluded."""
    for required in (
        "OPERATOR",
        "PERSONA-INVESTOR-COLD",
        "PERSONA-INVESTOR-WARM",
        "PERSONA-ADVISOR-REFERRAL",
        "PERSONA-CUSTOMER-KIRBE-PROSPECT",
    ):
        assert required in yaml_text, f"persona matrix missing {required}"


def test_default_persona_matrix_excludes_tier3(yaml_text: str) -> None:
    """Tier-2/3 personas are NOT in the default matrix; only via persona_filter input."""
    matrix_block_start = yaml_text.find("matrix:")
    matrix_block_end = yaml_text.find("timeout-minutes:", matrix_block_start)
    matrix_block = yaml_text[matrix_block_start:matrix_block_end]
    for excluded in (
        "PERSONA-PRESS",
        "PERSONA-IDEA-PROPOSER",
        "PERSONA-RANDOM-INBOUND",
        "PERSONA-CUSTOMER-SERVICE-PROSPECT",
        "PERSONA-VENDOR-INBOUND",
        "PERSONA-VENDOR-OUTBOUND",
        "PERSONA-EXISTING-CUSTOMER",
        "PERSONA-EXISTING-PARTNER",
        "PERSONA-PARTNER-JOINT-EQUITY",
        "PERSONA-PARTNER-SUBCONTRACT",
        "PERSONA-TALENT-INBOUND",
        "PERSONA-ADVISOR-COLD",
    ):
        assert excluded not in matrix_block, f"matrix should not include {excluded} by default"


def test_persona_filter_input_exists(yaml_text: str) -> None:
    """workflow_dispatch persona_filter input enables Tier-2/3 opt-in."""
    assert "persona_filter:" in yaml_text


# ---------------------------------------------------------------------------
# Cost discipline (R-47-3 + R-47-11)
# ---------------------------------------------------------------------------

def test_max_persona_usd_env_wired(yaml_text: str) -> None:
    """R-47-3: per-persona spend cap default $1."""
    assert "MAX_PERSONA_USD:" in yaml_text
    assert "max_persona_usd:" in yaml_text  # workflow_dispatch input
    # Default value visible in YAML
    assert "default: '1.0'" in yaml_text


def test_judge_cost_cap_env_wired(yaml_text: str) -> None:
    """R-47-11: LLM-judge cost cap per scenario default $0.01."""
    assert "AKOS_JUDGE_COST_CAP:" in yaml_text
    assert "judge_cost_cap:" in yaml_text  # workflow_dispatch input
    assert "default: '0.01'" in yaml_text


def test_eval_invocations_use_per_persona_cap(yaml_text: str) -> None:
    """Tier B invocations use --max-spend $MAX_PERSONA_USD (not $MAX_TIER_B_USD)."""
    # The replay + adversarial sweeps should use per-persona cap.
    replay_idx = yaml_text.find("--mode replay")
    adv_idx = yaml_text.find("--mode adversarial")
    for idx in (replay_idx, adv_idx):
        assert idx > 0
        block = yaml_text[idx:idx + 600]
        assert "MAX_PERSONA_USD" in block, "per-persona cap not used in eval invocation"


def test_judge_cost_cap_passed_to_eval(yaml_text: str) -> None:
    assert "--judge-cost-cap $AKOS_JUDGE_COST_CAP" in yaml_text


# ---------------------------------------------------------------------------
# --persona flag wiring (P10 + P14)
# ---------------------------------------------------------------------------

def test_persona_flag_passed_to_eval_invocations(yaml_text: str) -> None:
    """All 3 eval steps (Tier A baseline + Tier B replay + Tier B adversarial) pass --persona."""
    persona_flag_count = yaml_text.count('--persona "${{ steps.preflight.outputs.persona }}"')
    assert persona_flag_count >= 3, (
        f"expected --persona in 3 eval steps; found {persona_flag_count}"
    )


def test_preflight_resolves_persona_filter_or_matrix(yaml_text: str) -> None:
    """preflight step picks persona_filter (workflow_dispatch) over matrix.persona when set."""
    assert "github.event.inputs.persona_filter || matrix.persona" in yaml_text


# ---------------------------------------------------------------------------
# P13 item 4 dependency (compliance.eval_run live writes)
# ---------------------------------------------------------------------------

def test_supabase_secrets_exposed_for_eval_run_writer(yaml_text: str) -> None:
    """SUPABASE_URL + SERVICE_ROLE_KEY must be in env so eval_run_writer activates."""
    assert "SUPABASE_URL:" in yaml_text
    assert "SUPABASE_SERVICE_ROLE_KEY:" in yaml_text
    assert "secrets.SUPABASE_URL" in yaml_text
    assert "secrets.SUPABASE_SERVICE_ROLE_KEY" in yaml_text


def test_job_summary_surfaces_eval_run_writer_stats(yaml_text: str) -> None:
    """Job summary should report compliance.eval_run write stats per cell."""
    assert "eval_run_writer" in yaml_text


# ---------------------------------------------------------------------------
# Artifact upload uses 4-D cell name
# ---------------------------------------------------------------------------

def test_scorecard_artifact_name_includes_persona(yaml_text: str) -> None:
    """Artifact name uniquely identifies each cell (model_tier x persona)."""
    assert "eval-scorecards-${{ matrix.model_tier }}-${{ matrix.persona }}" in yaml_text


def test_scorecard_filenames_include_persona(yaml_text: str) -> None:
    assert "tier-a-${{ matrix.model_tier }}-${{ matrix.persona }}.json" in yaml_text
    assert "tier-b-${{ matrix.model_tier }}-${{ matrix.persona }}.json" in yaml_text


# ---------------------------------------------------------------------------
# Documentation / I47 P14 markers
# ---------------------------------------------------------------------------

def test_yaml_documents_4d_matrix_intent(yaml_text: str) -> None:
    """P14 header comment names the 4-D matrix decision and trade-off."""
    assert "I47 P14" in yaml_text
    assert "4-D matrix" in yaml_text
    assert "D-IH-47-H" in yaml_text
