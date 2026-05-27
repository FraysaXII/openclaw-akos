from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from akos.hlk_mktops import (
    VALID_MKTOPS_DIMENSIONS,
    fixture_campaign_manifest,
)
from scripts.validate_mktops_campaign import (
    run_campaign_check,
    self_test,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR_SCRIPT = REPO_ROOT / "scripts" / "validate_mktops_campaign.py"


@pytest.mark.hlk
def test_validator_self_test_returns_zero() -> None:
    assert self_test() == 0


@pytest.mark.hlk
def test_validator_script_self_test_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_SCRIPT), "--self-test"],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "PASS" in result.stdout


@pytest.mark.hlk
def test_run_campaign_check_emits_seven_findings() -> None:
    manifest = fixture_campaign_manifest()
    report = run_campaign_check(manifest)
    assert len(report.findings) == 7
    assert set(report.dimensions_fired) == VALID_MKTOPS_DIMENSIONS
    assert report.fail_count == 0


@pytest.mark.hlk
def test_run_campaign_check_resolves_persona_and_channel() -> None:
    manifest = fixture_campaign_manifest()
    report = run_campaign_check(manifest)
    persona_finding = next(
        f for f in report.findings if f.dimension_code == "MKT-06-PERSONA-FIT"
    )
    channel_finding = next(
        f for f in report.findings if f.dimension_code == "MKT-05-CHANNEL-COVERAGE"
    )
    assert persona_finding.status == "PASS"
    assert channel_finding.status == "PASS"


@pytest.mark.hlk
def test_validator_script_check_campaign_runs(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(fixture_campaign_manifest().model_dump()),
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_SCRIPT), "--check-campaign", str(manifest_path)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "PASS=" in result.stdout
    assert "MKT-06-PERSONA-FIT" in result.stdout
