"""Tests for AIC_REGISTRY + MADEIRA_AIC_PER_TASK validators (I82 P4 / Wave Q CSV 4)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from akos.hlk_aic_registry_csv import AICRegistryRow
from akos.hlk_madeira_aic_per_task_csv import MadeiraAICPerTaskRow

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_validate_aic_registry_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_aic_registry.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_madeira_aic_per_task_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_madeira_aic_per_task.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_aic_id_pattern_rejects_freeform() -> None:
    with pytest.raises(Exception):
        AICRegistryRow(
            aic_id="madeira",
            aic_name="Madeira",
            substrate_id="SUBS-ANYSPHERE-CURSOR-SDK",
            runtime_instance="cursor-desktop",
            role_owner_class="ai-o5-1",
            parent_doctrine_canonical="docs/...",
            status="active",
            notes="",
            last_review_at="2026-05-22",
            last_review_by="Founder",
            last_review_decision_id="D-IH-82-S",
            methodology_version_at_review="v3.1",
        )


def test_madeira_task_aic_id_must_be_madeira_prefixed() -> None:
    with pytest.raises(Exception):
        MadeiraAICPerTaskRow(
            task_id="MTASK-FOO",
            aic_id="AIC-KIRBE-ON-LLAMAINDEX",
            task_class="code-authoring",
            dispatcher_pattern="operator-inline",
            tool_catalog_ref="ref",
            rbac_class="read-only",
            status="active",
            notes="",
            last_audit_at="2026-05-22",
            last_audit_by="Founder",
            last_review_at="2026-05-22",
            last_review_by="Founder",
            last_review_decision_id="D-IH-82-S",
            methodology_version_at_review="v3.1",
        )
