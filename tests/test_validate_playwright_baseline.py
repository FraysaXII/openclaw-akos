"""Tests for scripts/validate_playwright_baseline.py + akos.playwright_baseline (I68 P2).

Pydantic model tests + integration tests against a fixture directory of
sample playwright.config.ts inputs covering:

- 5-viewport canonical pass (mirrors the AKOS template).
- Browser-named projects (the pre-carry-over state of `hlk-erp` /
  `boilerplate` today; reports all 5 viewports as missing).
- Per-viewport opt-out via ``ci_baseline_optouts`` JSON list.
- Explicit-size drift (e.g. ``viewport: { width: 1366, height: 768 }`` for
  ``desktop`` instead of canonical 1280x800).
- Retries-on-CI drift without opt-out.

Per CONTRIBUTING.md §"Testing Standards": valid + invalid pairs.

Marked ``cicd`` per the I68 P2 plan + ``pyproject.toml`` markers list, so
operators can run only the I68 CICD-baseline / observability suite via
``py -m pytest -m cicd``.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import textwrap
from pathlib import Path

import pytest

pytestmark = pytest.mark.cicd

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "validate_playwright_baseline.py"

sys.path.insert(0, str(REPO_ROOT))

from akos.playwright_baseline import (  # noqa: E402  (import after sys.path mutation)
    STANDARD_VIEWPORT_NAMES,
    STANDARD_VIEWPORT_SIZES,
    PlaywrightBaselineConfig,
    PlaywrightProject,
)


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "_validate_playwright_baseline_test", SCRIPT
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def validator():
    return _load_validator()


# ---------------------------------------------------------------------------
# Pydantic model tests (valid + invalid pairs per CONTRIBUTING.md)
# ---------------------------------------------------------------------------


class TestPlaywrightProjectModel:
    """Tests for the PlaywrightProject Pydantic model."""

    def test_valid_iphone_se_with_devices_key_passes(self):
        project = PlaywrightProject(name="iphone-se", devices_key="iPhone SE")
        assert project.name == "iphone-se"
        assert project.devices_key == "iPhone SE"
        assert project.viewport_width is None

    def test_valid_desktop_with_explicit_size_passes(self):
        project = PlaywrightProject(name="desktop", viewport_width=1280, viewport_height=800)
        assert project.viewport_width == 1280
        assert project.viewport_height == 800

    def test_invalid_viewport_name_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            PlaywrightProject(name="chromium")  # type: ignore[arg-type]

    def test_invalid_viewport_width_below_bound_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            PlaywrightProject(name="desktop", viewport_width=100, viewport_height=800)

    def test_invalid_viewport_height_above_bound_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            PlaywrightProject(name="wide", viewport_width=1920, viewport_height=5000)


class TestPlaywrightBaselineConfigModel:
    """Tests for the PlaywrightBaselineConfig Pydantic model."""

    def _canonical_5_projects(self) -> list[PlaywrightProject]:
        return [
            PlaywrightProject(name="iphone-se", devices_key="iPhone SE"),
            PlaywrightProject(name="iphone-11", devices_key="iPhone 11"),
            PlaywrightProject(name="ipad", viewport_width=768, viewport_height=1024),
            PlaywrightProject(name="desktop", viewport_width=1280, viewport_height=800),
            PlaywrightProject(name="wide", viewport_width=1920, viewport_height=1080),
        ]

    def test_canonical_5_passes(self):
        config = PlaywrightBaselineConfig(
            repo_slug="boilerplate",
            projects=self._canonical_5_projects(),
        )
        assert config.missing_viewports() == []
        assert config.has_explicit_size_drift() == []
        assert config.retries_on_ci == 2

    def test_missing_one_viewport_flagged(self):
        projects = self._canonical_5_projects()[:-1]  # drop 'wide'
        config = PlaywrightBaselineConfig(repo_slug="hlk-erp", projects=projects)
        assert config.missing_viewports() == ["wide"]

    def test_per_viewport_opt_out_honoured(self):
        projects = self._canonical_5_projects()[:-1]  # drop 'wide'
        config = PlaywrightBaselineConfig(
            repo_slug="hlk-erp",
            projects=projects,
            ci_baseline_optouts=["playwright-viewport-wide"],
        )
        assert config.missing_viewports() == []

    def test_invalid_repo_slug_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            PlaywrightBaselineConfig(repo_slug="UPPER_BAD", projects=[])

    def test_explicit_size_drift_detected(self):
        projects = [
            PlaywrightProject(name="desktop", viewport_width=1366, viewport_height=768),
        ]
        config = PlaywrightBaselineConfig(repo_slug="boilerplate", projects=projects)
        drift = config.has_explicit_size_drift()
        assert len(drift) == 1
        assert "1366x768" in drift[0]
        assert "1280x800" in drift[0]

    def test_devices_key_exempt_from_size_drift(self):
        # When viewport sizes are not explicit (devices['<key>'] only), the
        # validator does not surface size drift — the device preset is
        # Playwright's source of truth for that viewport.
        projects = [
            PlaywrightProject(name="desktop", devices_key="Desktop Chrome"),
        ]
        config = PlaywrightBaselineConfig(repo_slug="boilerplate", projects=projects)
        assert config.has_explicit_size_drift() == []

    def test_retries_default_is_2(self):
        config = PlaywrightBaselineConfig(repo_slug="boilerplate", projects=self._canonical_5_projects())
        assert config.retries_on_ci == 2


# ---------------------------------------------------------------------------
# Standard viewport name + size constants (locked source of truth)
# ---------------------------------------------------------------------------


def test_standard_viewport_names_exact():
    assert STANDARD_VIEWPORT_NAMES == (
        "iphone-se",
        "iphone-11",
        "ipad",
        "desktop",
        "wide",
    )


def test_standard_viewport_sizes_exact():
    assert STANDARD_VIEWPORT_SIZES == {
        "iphone-se": (375, 667),
        "iphone-11": (414, 896),
        "ipad": (768, 1024),
        "desktop": (1280, 800),
        "wide": (1920, 1080),
    }


# ---------------------------------------------------------------------------
# Validator integration tests
# ---------------------------------------------------------------------------


def test_real_canonical_template_passes(validator):
    """The shipped AKOS canonical template must validate clean."""
    template_errors = validator._validate_canonical_template()
    assert template_errors == [], template_errors


def test_validator_default_mode_skips_consumer_scan(validator, monkeypatch, capsys):
    """Default validator run only checks the canonical template."""
    monkeypatch.delenv("AKOS_PLAYWRIGHT_BASELINE_SCAN_CONSUMERS", raising=False)
    rc = validator.main([])
    assert rc == 0


def test_validator_explicit_consumer_scan_strict(validator, monkeypatch, tmp_path):
    """With AKOS_PLAYWRIGHT_BASELINE_SCAN_CONSUMERS=1 the validator scans local consumer repos."""
    monkeypatch.setenv("AKOS_PLAYWRIGHT_BASELINE_SCAN_CONSUMERS", "1")
    # Run is non-deterministic (depends on whether the operator's local
    # ../boilerplate / ../hlk-erp checkouts exist). We assert exit code is
    # either 0 (no consumer drift today, e.g. on a CI runner without sibling
    # checkouts) or 1 (drift surfaced because sibling repos pre-date P2
    # carry-over). Either is correct behavior.
    rc = validator.main([])
    assert rc in {0, 1}


def _write_ts_config(tmp_path: Path, body: str) -> Path:
    target = tmp_path / "playwright.config.ts"
    target.write_text(body, encoding="utf-8")
    return target


def test_parse_canonical_5_viewports_passes(validator, tmp_path):
    body = textwrap.dedent(
        """
        import { defineConfig, devices } from '@playwright/test';
        export default defineConfig({
          retries: process.env.CI ? 2 : 0,
          projects: [
            { name: 'iphone-se', use: { ...devices['iPhone SE'] } },
            { name: 'iphone-11', use: { ...devices['iPhone 11'] } },
            { name: 'ipad',      use: { viewport: { width: 768,  height: 1024 } } },
            { name: 'desktop',   use: { viewport: { width: 1280, height: 800  } } },
            { name: 'wide',      use: { viewport: { width: 1920, height: 1080 } } },
          ],
        });
        """
    ).lstrip()
    path = _write_ts_config(tmp_path, body)
    config = validator._parse_config_file(path, repo_slug="fixture-canonical", opt_outs=[])
    assert config.missing_viewports() == []
    assert config.retries_on_ci == 2
    errors = validator._validate_config(config, source_path=path)
    assert errors == [], errors


def test_parse_browser_named_projects_reports_all_5_missing(validator, tmp_path):
    """Pre-carry-over `boilerplate` / `hlk-erp` shape — chromium/firefox/webkit."""
    body = textwrap.dedent(
        """
        import { defineConfig, devices } from '@playwright/test';
        export default defineConfig({
          retries: process.env.CI ? 2 : 0,
          projects: [
            { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
            { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
            { name: 'webkit',   use: { ...devices['Desktop Safari'] } },
          ],
        });
        """
    ).lstrip()
    path = _write_ts_config(tmp_path, body)
    config = validator._parse_config_file(path, repo_slug="fixture-browser", opt_outs=[])
    assert sorted(config.missing_viewports()) == sorted(STANDARD_VIEWPORT_NAMES)
    errors = validator._validate_config(config, source_path=path)
    assert len(errors) == 1
    assert "missing required viewports" in errors[0]


def test_parse_explicit_size_drift_for_desktop_flagged(validator, tmp_path):
    body = textwrap.dedent(
        """
        import { defineConfig, devices } from '@playwright/test';
        export default defineConfig({
          retries: process.env.CI ? 2 : 0,
          projects: [
            { name: 'iphone-se', use: { ...devices['iPhone SE'] } },
            { name: 'iphone-11', use: { ...devices['iPhone 11'] } },
            { name: 'ipad',      use: { viewport: { width: 768,  height: 1024 } } },
            { name: 'desktop',   use: { viewport: { width: 1366, height: 768  } } },
            { name: 'wide',      use: { viewport: { width: 1920, height: 1080 } } },
          ],
        });
        """
    ).lstrip()
    path = _write_ts_config(tmp_path, body)
    config = validator._parse_config_file(path, repo_slug="fixture-drift", opt_outs=[])
    assert config.missing_viewports() == []
    errors = validator._validate_config(config, source_path=path)
    drift_errors = [e for e in errors if "1366x768" in e]
    assert len(drift_errors) == 1


def test_parse_per_viewport_optout_honoured(validator, tmp_path):
    """A repo opting out of `wide` via JSON-array opt-out passes with 4 viewports."""
    body = textwrap.dedent(
        """
        import { defineConfig, devices } from '@playwright/test';
        export default defineConfig({
          retries: process.env.CI ? 2 : 0,
          projects: [
            { name: 'iphone-se', use: { ...devices['iPhone SE'] } },
            { name: 'iphone-11', use: { ...devices['iPhone 11'] } },
            { name: 'ipad',      use: { viewport: { width: 768,  height: 1024 } } },
            { name: 'desktop',   use: { viewport: { width: 1280, height: 800  } } },
          ],
        });
        """
    ).lstrip()
    path = _write_ts_config(tmp_path, body)
    config = validator._parse_config_file(
        path,
        repo_slug="fixture-optout",
        opt_outs=["playwright-viewport-wide"],
    )
    assert config.missing_viewports() == []
    errors = validator._validate_config(config, source_path=path)
    assert errors == [], errors


def test_parse_retries_drift_without_optout_flagged(validator, tmp_path):
    body = textwrap.dedent(
        """
        import { defineConfig } from '@playwright/test';
        export default defineConfig({
          retries: process.env.CI ? 5 : 0,
          projects: [
            { name: 'iphone-se', use: { ...devices['iPhone SE'] } },
            { name: 'iphone-11', use: { ...devices['iPhone 11'] } },
            { name: 'ipad',      use: { viewport: { width: 768,  height: 1024 } } },
            { name: 'desktop',   use: { viewport: { width: 1280, height: 800  } } },
            { name: 'wide',      use: { viewport: { width: 1920, height: 1080 } } },
          ],
        });
        """
    ).lstrip()
    path = _write_ts_config(tmp_path, body)
    config = validator._parse_config_file(path, repo_slug="fixture-retries", opt_outs=[])
    errors = validator._validate_config(config, source_path=path)
    retries_errors = [e for e in errors if "retries on CI is 5" in e]
    assert len(retries_errors) == 1


def test_optouts_for_supports_json_array(validator):
    row = {"ci_baseline_optouts": '["playwright-viewport-wide", "lighthouse"]'}
    assert validator._opt_outs_for(row) == ["playwright-viewport-wide", "lighthouse"]


def test_optouts_for_supports_semicolon_list_legacy(validator):
    row = {"ci_baseline_optouts": "playwright-viewport-wide;lighthouse"}
    assert validator._opt_outs_for(row) == ["playwright-viewport-wide", "lighthouse"]


def test_optouts_for_handles_empty_or_missing_column(validator):
    assert validator._opt_outs_for({}) == []
    assert validator._opt_outs_for({"ci_baseline_optouts": ""}) == []


def test_optouts_for_handles_malformed_json(validator):
    row = {"ci_baseline_optouts": "[malformed json}"}
    # Tolerates malformed JSON-like strings by returning empty list (treats
    # as no opt-outs); the underlying CSV validator should already have
    # caught a malformed value.
    assert validator._opt_outs_for(row) == []


def test_resolve_consumer_config_returns_none_for_missing_local_path(validator):
    row = {"local_path": ""}
    assert validator._resolve_consumer_config(row) is None
