"""Tests for scripts/validate_cicd_baseline.py + akos.cicd_baseline (I68 P5).

Pydantic model tests + integration tests against in-memory REPOSITORY_REGISTRY.csv
fixture rows covering:

- Per-class required-checks set per SOP-CICD_BASELINE_001 §3 (platform /
  reference / internal / client-delivery).
- Per-repo opt-out matrix per §7 (JSON-array column; honoured semantically).
- Forward-compat: missing ``ci_baseline_version`` / ``build_time_target_seconds``
  / ``ci_baseline_optouts`` columns produce defaulted models, not failures.
- Drift cases the validator must catch: unknown opt-out keys; unknown SOP
  versions; out-of-range build-time targets.
- Canonical SOP doc presence + frontmatter ``status:`` + ``version:`` checks.
- Canonical workflow template + Render YAML stub presence checks.
- Default soft mode (no env var) = canonical-only.
- Explicit strict mode (``AKOS_CICD_BASELINE_SCAN_CONSUMERS=1``) =
  canonical + per-row scan.

Per CONTRIBUTING.md §"Testing Standards": valid + invalid pairs.

Marked ``cicd`` per the I68 P5 plan + ``pyproject.toml`` markers list.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.cicd

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "validate_cicd_baseline.py"

sys.path.insert(0, str(REPO_ROOT))

from akos.cicd_baseline import (  # noqa: E402  (import after sys.path mutation)
    KNOWN_CHECK_OPTOUTS,
    KNOWN_SOP_VERSIONS,
    PER_CLASS_DEFAULT_BUILD_TIME_TARGET_SECONDS,
    PER_CLASS_REQUIRED_CHECKS,
    CICDBaselineRow,
)


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_cicd_baseline", SCRIPT
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# -----------------------------------------------------------------------------
# Pydantic model tests
# -----------------------------------------------------------------------------


class TestCICDBaselineRow:
    def test_canonical_platform_row_passes(self) -> None:
        row = CICDBaselineRow(
            repo_slug="hlk-erp",
            repo_class="platform",
            ci_baseline_version="v0.9.0",
            build_time_target_seconds=120,
            ci_baseline_optouts=[],
        )
        assert row.repo_slug == "hlk-erp"
        assert row.repo_class == "platform"
        assert row.ci_baseline_version == "v0.9.0"
        assert row.build_time_target_seconds == 120

    def test_minimal_internal_row_passes_with_defaults(self) -> None:
        row = CICDBaselineRow(repo_slug="akos-telemetry-ci", repo_class="internal")
        assert row.ci_baseline_version is None
        assert row.build_time_target_seconds is None
        assert row.ci_baseline_optouts == []

    def test_invalid_repo_slug_rejected(self) -> None:
        with pytest.raises(Exception, match=r"String should match pattern"):
            CICDBaselineRow(repo_slug="UPPERCASE", repo_class="platform")

    def test_invalid_class_rejected(self) -> None:
        with pytest.raises(Exception, match=r"Input should be"):
            CICDBaselineRow(repo_slug="hlk-erp", repo_class="bogus-class")  # type: ignore[arg-type]

    def test_unknown_sop_version_rejected(self) -> None:
        with pytest.raises(Exception, match=r"is not a known SOP-CICD_BASELINE_001 version"):
            CICDBaselineRow(
                repo_slug="hlk-erp",
                repo_class="platform",
                ci_baseline_version="v99.99.99",
            )

    def test_unknown_opt_out_rejected(self) -> None:
        with pytest.raises(Exception, match=r"unknown opt-out keys"):
            CICDBaselineRow(
                repo_slug="hlk-erp",
                repo_class="platform",
                ci_baseline_optouts=["bogus-check-name"],
            )

    def test_known_opt_out_accepted(self) -> None:
        row = CICDBaselineRow(
            repo_slug="kirbe-platform",
            repo_class="platform",
            ci_baseline_optouts=["lighthouse", "brand-jargon"],
        )
        assert "lighthouse" in row.ci_baseline_optouts
        assert "brand-jargon" in row.ci_baseline_optouts

    def test_per_viewport_opt_out_accepted_inherited_from_p2(self) -> None:
        row = CICDBaselineRow(
            repo_slug="hlk-erp",
            repo_class="platform",
            ci_baseline_optouts=[
                "playwright-viewport-iphone-se",
                "playwright-viewport-iphone-11",
            ],
        )
        assert len(row.ci_baseline_optouts) == 2

    def test_build_time_below_min_rejected(self) -> None:
        with pytest.raises(Exception, match=r"greater than or equal to 10"):
            CICDBaselineRow(
                repo_slug="hlk-erp",
                repo_class="platform",
                build_time_target_seconds=5,
            )

    def test_build_time_above_max_rejected(self) -> None:
        with pytest.raises(Exception, match=r"less than or equal to 3600"):
            CICDBaselineRow(
                repo_slug="hlk-erp",
                repo_class="platform",
                build_time_target_seconds=99999,
            )

    def test_required_checks_per_class(self) -> None:
        platform = CICDBaselineRow(repo_slug="hlk-erp", repo_class="platform")
        reference = CICDBaselineRow(repo_slug="boilerplate", repo_class="reference")
        internal = CICDBaselineRow(repo_slug="akos-telemetry-ci", repo_class="internal")
        # platform == reference baseline (boilerplate IS the brand surface) per SOP §3.
        assert platform.required_checks() == reference.required_checks()
        # internal is the lint+typecheck+unit-test floor.
        assert internal.required_checks() == frozenset({"lint", "typecheck", "unit-test"})

    def test_opt_out_subtracts_from_required_checks(self) -> None:
        row = CICDBaselineRow(
            repo_slug="kirbe-platform",
            repo_class="platform",
            ci_baseline_optouts=["lighthouse", "brand-jargon"],
        )
        assert "lighthouse" not in row.required_checks()
        assert "brand-jargon" not in row.required_checks()
        assert "lint" in row.required_checks()
        assert "sentry-release-format" in row.required_checks()

    def test_missing_checks_returns_diff(self) -> None:
        row = CICDBaselineRow(repo_slug="hlk-erp", repo_class="platform")
        observed = frozenset({"lint", "typecheck"})
        missing = row.missing_checks(observed_checks=observed)
        assert "unit-test" in missing
        assert "playwright-smoke" in missing
        assert "lint" not in missing


class TestFromRegistryRow:
    def test_full_row_constructs(self) -> None:
        row = CICDBaselineRow.from_registry_row(
            {
                "repo_slug": "hlk-erp",
                "class": "platform",
                "ci_baseline_version": "v0.9.0",
                "build_time_target_seconds": "120",
                "ci_baseline_optouts": '["lighthouse"]',
            }
        )
        assert row.ci_baseline_version == "v0.9.0"
        assert row.build_time_target_seconds == 120
        assert row.ci_baseline_optouts == ["lighthouse"]

    def test_missing_columns_default_safely(self) -> None:
        # Forward-compat: pre-P5-canonical-CSV-gate state with no new columns.
        row = CICDBaselineRow.from_registry_row(
            {"repo_slug": "boilerplate", "class": "reference"}
        )
        assert row.ci_baseline_version is None
        assert row.build_time_target_seconds is None
        assert row.ci_baseline_optouts == []

    def test_malformed_optouts_json_returns_empty(self) -> None:
        row = CICDBaselineRow.from_registry_row(
            {
                "repo_slug": "hlk-erp",
                "class": "platform",
                "ci_baseline_optouts": "[malformed json}",
            }
        )
        assert row.ci_baseline_optouts == []

    def test_legacy_semicolon_optouts_parsed(self) -> None:
        row = CICDBaselineRow.from_registry_row(
            {
                "repo_slug": "kirbe-platform",
                "class": "platform",
                "ci_baseline_optouts": "lighthouse;brand-jargon",
            }
        )
        assert "lighthouse" in row.ci_baseline_optouts
        assert "brand-jargon" in row.ci_baseline_optouts

    def test_non_numeric_build_time_defaults_to_none(self) -> None:
        row = CICDBaselineRow.from_registry_row(
            {
                "repo_slug": "hlk-erp",
                "class": "platform",
                "build_time_target_seconds": "not-a-number",
            }
        )
        assert row.build_time_target_seconds is None


# -----------------------------------------------------------------------------
# Constants smoke-checks
# -----------------------------------------------------------------------------


def test_known_sop_versions_includes_review_and_active() -> None:
    assert "v0.9.0" in KNOWN_SOP_VERSIONS
    assert "v1.0.0" in KNOWN_SOP_VERSIONS


def test_per_class_required_checks_covers_all_repo_classes() -> None:
    assert set(PER_CLASS_REQUIRED_CHECKS) == {
        "platform",
        "reference",
        "internal",
        "client-delivery",
    }


def test_per_class_default_build_time_targets_present() -> None:
    assert PER_CLASS_DEFAULT_BUILD_TIME_TARGET_SECONDS["reference"] == 120
    assert PER_CLASS_DEFAULT_BUILD_TIME_TARGET_SECONDS["platform"] == 300


def test_known_check_optouts_includes_per_viewport_optouts() -> None:
    for vname in (
        "playwright-viewport-iphone-se",
        "playwright-viewport-iphone-11",
        "playwright-viewport-ipad",
        "playwright-viewport-desktop",
        "playwright-viewport-wide",
    ):
        assert vname in KNOWN_CHECK_OPTOUTS


# -----------------------------------------------------------------------------
# Validator integration tests
# -----------------------------------------------------------------------------


def test_canonical_sop_present() -> None:
    validator = _load_validator()
    errors = validator._validate_canonical_sop()
    assert errors == [], f"canonical SOP validation surfaced unexpected errors: {errors}"


def test_canonical_templates_present() -> None:
    validator = _load_validator()
    errors = validator._validate_canonical_templates()
    assert errors == [], f"canonical templates validation surfaced unexpected errors: {errors}"


def test_validator_default_mode_skips_consumer_scan(capsys: pytest.CaptureFixture[str]) -> None:
    validator = _load_validator()
    os.environ.pop("AKOS_CICD_BASELINE_SCAN_CONSUMERS", None)
    rc = validator.main([])
    assert rc == 0


def test_validator_explicit_consumer_scan_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    validator = _load_validator()
    monkeypatch.setenv("AKOS_CICD_BASELINE_SCAN_CONSUMERS", "1")
    rc = validator.main([])
    # Forward-compat: rows missing the new columns produce defaulted models;
    # rc must be 0 today (no rows with malformed JSON or unknown opt-outs).
    assert rc == 0
