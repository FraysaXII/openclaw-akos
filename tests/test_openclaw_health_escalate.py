"""Tests for ``scripts/openclaw_health_escalate.py`` (I87 P1 / D-IH-87-A).

Mirrors the I59 P4 OPS_REGISTER-write discipline: schema sanity, idempotency
within-a-day, RICE-score computation, FK targeting of INIT-OPENCLAW_AKOS-87,
input validation.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import openclaw_health_escalate as escalator  # noqa: E402


@pytest.mark.openclaw_runtime
def test_symptom_class_regex_accepts_valid_slugs() -> None:
    """Valid symptom-class slugs pass the regex gate (parametrized inline)."""
    valid = [
        "ws-token-expiration",
        "docker-sandbox-churn",
        "low-context-warning",
        "bonjour-self-heal",
        "plugins-allow-trust",
        "abc",
    ]
    for slug in valid:
        assert escalator.SYMPTOM_CLASS_RE.match(slug) is not None, slug


@pytest.mark.openclaw_runtime
def test_symptom_class_regex_rejects_invalid_slugs() -> None:
    """Invalid symptom-class slugs (uppercase, leading digit, special chars) are rejected."""
    invalid = [
        "Ws-Token-Expiration",
        "1-leading-digit",
        "underscores_not_allowed",
        "with space",
        "ab",  # too short
        "a" * 50,  # too long
        "",
    ]
    for slug in invalid:
        assert escalator.SYMPTOM_CLASS_RE.match(slug) is None, slug


@pytest.mark.openclaw_runtime
def test_emit_dry_run_does_not_modify_csv() -> None:
    """``dry_run=True`` returns a row dict but does not append to the CSV."""
    before = escalator.OPS_REGISTER_CSV.read_text(encoding="utf-8")
    row = escalator.emit_escalation_row(
        symptom_class="ws-token-expiration",
        consecutive_failures=3,
        evidence_path="docs/wip/intelligence/substrate-audit-2026-Q2/openclaw-observed-symptoms-2026-05-16.md",
        dry_run=True,
        today="2099-01-01",
    )
    after = escalator.OPS_REGISTER_CSV.read_text(encoding="utf-8")
    assert before == after, "dry_run must not modify OPS_REGISTER.csv"
    assert row is not None
    assert row["ops_action_id"].startswith("OPS-87-")
    assert row["originating_initiative_id"] == "INIT-OPENCLAW_AKOS-87"
    assert row["owner_class"] == "operator"
    assert row["status"] == "open"
    assert row["linked_decision_ids"] == "D-IH-87-A"


@pytest.mark.openclaw_runtime
def test_emit_rejects_invalid_symptom_class() -> None:
    """Bad symptom-class slugs raise ValueError before any CSV I/O."""
    with pytest.raises(ValueError, match="symptom_class"):
        escalator.emit_escalation_row(
            symptom_class="BAD SLUG",
            consecutive_failures=3,
            evidence_path="docs/foo.md",
            dry_run=True,
        )


@pytest.mark.openclaw_runtime
def test_emit_rejects_zero_consecutive_failures() -> None:
    """consecutive_failures must be >= 1."""
    with pytest.raises(ValueError, match="consecutive_failures"):
        escalator.emit_escalation_row(
            symptom_class="ws-token-expiration",
            consecutive_failures=0,
            evidence_path="docs/foo.md",
            dry_run=True,
        )


@pytest.mark.openclaw_runtime
def test_emit_rejects_invalid_rice_impact() -> None:
    """rice_impact must be in the allowed enum."""
    with pytest.raises(ValueError, match="rice_impact"):
        escalator.emit_escalation_row(
            symptom_class="ws-token-expiration",
            consecutive_failures=3,
            evidence_path="docs/foo.md",
            rice_impact="999",
            dry_run=True,
        )


@pytest.mark.openclaw_runtime
def test_emit_rice_score_computed_correctly() -> None:
    """RICE score formula: reach * impact * (confidence/100) / effort, rounded to 2dp."""
    row = escalator.emit_escalation_row(
        symptom_class="ws-token-expiration",
        consecutive_failures=3,
        evidence_path="docs/foo.md",
        rice_impact="2",
        dry_run=True,
    )
    assert row is not None
    # reach=10, impact=2, conf=0.80, effort=0.5 -> 10 * 2 * 0.8 / 0.5 = 32.0
    assert row["rice_score"] == "32.00"


@pytest.mark.openclaw_runtime
def test_next_sequence_starts_at_one_when_no_prior_rows() -> None:
    """The next-sequence helper starts at 1 for an empty-of-I87 ops list."""
    rows: list[dict[str, str]] = [
        {"ops_action_id": "OPS-14-1", "originating_initiative_id": "INIT-OPENCLAW_AKOS-14"},
    ]
    assert escalator._next_ops_sequence(rows) == 1


@pytest.mark.openclaw_runtime
def test_next_sequence_increments_max_seq_within_initiative() -> None:
    """The next-sequence helper increments by 1 over the max OPS-87-N seen."""
    rows: list[dict[str, str]] = [
        {"ops_action_id": "OPS-87-1", "originating_initiative_id": "INIT-OPENCLAW_AKOS-87"},
        {"ops_action_id": "OPS-87-5", "originating_initiative_id": "INIT-OPENCLAW_AKOS-87"},
        {"ops_action_id": "OPS-87-3", "originating_initiative_id": "INIT-OPENCLAW_AKOS-87"},
    ]
    assert escalator._next_ops_sequence(rows) == 6


@pytest.mark.openclaw_runtime
def test_idempotency_guard_blocks_duplicate_open_row_same_day() -> None:
    """An open row for the same symptom_class on the same day blocks re-emit."""
    rows = [
        {
            "ops_action_id": "OPS-87-1",
            "originating_initiative_id": "INIT-OPENCLAW_AKOS-87",
            "title": "OpenClaw health-monitor escalation: ws-token-expiration",
            "status": "open",
            "opened_at": "2026-05-16",
        }
    ]
    assert escalator._has_open_row_for_today(rows, "ws-token-expiration", "2026-05-16")
    assert not escalator._has_open_row_for_today(rows, "docker-sandbox-churn", "2026-05-16")
    assert not escalator._has_open_row_for_today(rows, "ws-token-expiration", "2026-05-17")


@pytest.mark.openclaw_runtime
def test_idempotency_guard_ignores_closed_rows() -> None:
    """A closed row for the same symptom_class does NOT block re-emit."""
    rows = [
        {
            "ops_action_id": "OPS-87-1",
            "originating_initiative_id": "INIT-OPENCLAW_AKOS-87",
            "title": "OpenClaw health-monitor escalation: ws-token-expiration",
            "status": "closed",
            "opened_at": "2026-05-16",
        }
    ]
    assert not escalator._has_open_row_for_today(rows, "ws-token-expiration", "2026-05-16")


@pytest.mark.openclaw_runtime
def test_ops_register_csv_path_resolves_to_canonical_location() -> None:
    """The CSV target must be the canonical compliance/canonicals/OPS_REGISTER.csv."""
    expected = (
        REPO_ROOT
        / "docs"
        / "references"
        / "hlk"
        / "v3.0"
        / "Admin"
        / "O5-1"
        / "People"
        / "Compliance"
        / "canonicals"
        / "OPS_REGISTER.csv"
    )
    assert escalator.OPS_REGISTER_CSV.resolve() == expected.resolve()
    assert escalator.OPS_REGISTER_CSV.exists()


@pytest.mark.openclaw_runtime
def test_emitted_row_carries_runbook_self_reference() -> None:
    """The emitted row's operator_runbook_path points to this script (pairing contract)."""
    row = escalator.emit_escalation_row(
        symptom_class="ws-token-expiration",
        consecutive_failures=3,
        evidence_path="docs/foo.md",
        dry_run=True,
    )
    assert row is not None
    assert row["operator_runbook_path"] == "scripts/openclaw_health_escalate.py"
