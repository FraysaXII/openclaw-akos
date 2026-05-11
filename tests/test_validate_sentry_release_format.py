"""Tests for scripts/validate_sentry_release_format.py + akos.sentry_release (I68 P4).

Pydantic model tests + integration tests against in-memory Sentry config
fixtures covering:

- Canonical ``<repo>@<sha>`` shape (boilerplate@74f9a95d, hlk-erp@a3b1c92e,
  kirbe-platform@5fe2d18b).
- Drift cases the validator must catch: vendor-default ``release: undefined``,
  semver-only ``release: "1.0.0"``, sha-only ``release: "<sha>"`` (no repo
  prefix), wrong-separator ``release: "<repo>-<sha>"``, wrong-repo prefix
  ``release: "wrong-repo@<sha>"``.
- Templating placeholders the validator must accept (Vercel
  ``${process.env.VERCEL_GIT_COMMIT_SHA}``, Render
  ``f"...@{os.environ['RENDER_GIT_COMMIT'][:8]}"``, generic ``${...}`` and
  ``{{...}}`` interpolation forms).
- Canonical doc presence + the canonical example block.
- Default soft mode (no env var) = canonical-doc-only.
- Explicit strict mode (``AKOS_SENTRY_RELEASE_SCAN_CONSUMERS=1``) =
  canonical-doc + per-consumer-repo scan.

Per CONTRIBUTING.md §"Testing Standards": valid + invalid pairs.

Marked ``cicd`` per the I68 P4 plan + ``pyproject.toml`` markers list.
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
SCRIPT = REPO_ROOT / "scripts" / "validate_sentry_release_format.py"

sys.path.insert(0, str(REPO_ROOT))

from akos.sentry_release import (  # noqa: E402  (import after sys.path mutation)
    RELEASE_TEMPLATE_CANONICAL,
    SentryReleaseFormatRule,
    SentryReleaseValue,
    parse_release_value,
)


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_sentry_release_format", SCRIPT
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# -----------------------------------------------------------------------------
# Pydantic model tests
# -----------------------------------------------------------------------------


class TestSentryReleaseFormatRule:
    def test_canonical_template_passes(self) -> None:
        rule = SentryReleaseFormatRule(release_template=RELEASE_TEMPLATE_CANONICAL)
        assert rule.release_template == RELEASE_TEMPLATE_CANONICAL

    def test_semver_only_template_rejected(self) -> None:
        with pytest.raises(Exception, match=r"release_template must be"):
            SentryReleaseFormatRule(release_template="{version}")

    def test_dash_separator_rejected(self) -> None:
        with pytest.raises(Exception, match=r"release_template must be"):
            SentryReleaseFormatRule(release_template="{repo_slug}-{sha_short}")

    def test_sha_only_rejected(self) -> None:
        with pytest.raises(Exception, match=r"release_template must be"):
            SentryReleaseFormatRule(release_template="{sha_short}")


class TestSentryReleaseValue:
    @pytest.mark.parametrize(
        "raw,expected_slug,expected_sha",
        [
            ("boilerplate@74f9a95d", "boilerplate", "74f9a95d"),
            ("hlk-erp@a3b1c92e", "hlk-erp", "a3b1c92e"),
            ("kirbe-platform@5fe2d18b", "kirbe-platform", "5fe2d18b"),
            ("openclaw-akos@1234567", "openclaw-akos", "1234567"),
            ("openclaw-akos@123456789012", "openclaw-akos", "123456789012"),
        ],
    )
    def test_canonical_values_parse(
        self, raw: str, expected_slug: str, expected_sha: str
    ) -> None:
        parsed = parse_release_value(raw)
        assert parsed is not None
        assert parsed.repo_slug == expected_slug
        assert parsed.sha_short == expected_sha

    @pytest.mark.parametrize(
        "raw",
        [
            "undefined",
            "1.0.0",
            "74f9a95d",  # SHA only, no repo prefix
            "boilerplate-74f9a95d",  # wrong separator
            "BOILERPLATE@74f9a95d",  # uppercase repo (canonical is kebab-case lowercase)
            "boilerplate@FFFFFFF",  # uppercase SHA
            "boilerplate@123",  # SHA too short (<7 chars)
            "boilerplate@1234567890123",  # SHA too long (>12 chars)
        ],
    )
    def test_drift_values_dont_parse(self, raw: str) -> None:
        assert parse_release_value(raw) is None

    def test_invalid_repo_slug_constructed_directly_rejected(self) -> None:
        with pytest.raises(Exception, match=r"repo_slug.*does not match"):
            SentryReleaseValue(raw="X@1234567", repo_slug="X", sha_short="1234567")

    def test_invalid_sha_short_constructed_directly_rejected(self) -> None:
        with pytest.raises(Exception, match=r"sha_short.*does not match"):
            SentryReleaseValue(raw="boilerplate@bogus!", repo_slug="boilerplate", sha_short="bogus!")


# -----------------------------------------------------------------------------
# Validator integration tests
# -----------------------------------------------------------------------------


def test_canonical_doc_present_and_carries_canonical_example() -> None:
    validator = _load_validator()
    errors = validator._validate_canonical_doc()
    assert errors == [], f"canonical doc validation surfaced unexpected errors: {errors}"


def test_validator_default_mode_skips_consumer_scan(capsys: pytest.CaptureFixture[str]) -> None:
    validator = _load_validator()
    os.environ.pop("AKOS_SENTRY_RELEASE_SCAN_CONSUMERS", None)
    rc = validator.main([])
    assert rc == 0
    # Validator logs to a logger (handler may be stderr); be lenient.
    out = capsys.readouterr()
    combined = (out.out + out.err).lower()
    assert "skipped (default soft mode)" in combined or "consumer-repo scan SKIPPED".lower() in combined


def test_validator_explicit_consumer_scan_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    validator = _load_validator()
    monkeypatch.setenv("AKOS_SENTRY_RELEASE_SCAN_CONSUMERS", "1")
    # Default sibling-repo state today is "no resolvable local_path" or "no
    # release: field yet" — both produce 0 errors. The test verifies the
    # scan runs without crashing under strict mode.
    rc = validator.main([])
    assert rc == 0


# -----------------------------------------------------------------------------
# Release-string regex parsing tests
# -----------------------------------------------------------------------------


@pytest.fixture()
def make_nextjs_sentry_config(tmp_path: Path):
    """Factory that writes a fake Next.js Sentry client config and returns its path."""
    def _make(release_value: str) -> Path:
        path = tmp_path / "sentry.client.config.ts"
        path.write_text(
            textwrap.dedent(
                f"""
                import * as Sentry from '@sentry/nextjs';
                Sentry.init({{
                  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
                  release: '{release_value}',
                  environment: process.env.VERCEL_ENV ?? 'development',
                }});
                """
            ),
            encoding="utf-8",
        )
        return path
    return _make


@pytest.fixture()
def make_python_sentry_init(tmp_path: Path):
    """Factory that writes a fake FastAPI Sentry init file and returns its path."""
    def _make(release_expr: str) -> Path:
        path = tmp_path / "main.py"
        path.write_text(
            textwrap.dedent(
                f"""
                import os
                import sentry_sdk

                sentry_sdk.init(
                    dsn=os.environ.get("SENTRY_DSN"),
                    release={release_expr},
                    environment=os.environ.get("RENDER_SERVICE_TYPE", "development"),
                )
                """
            ),
            encoding="utf-8",
        )
        return path
    return _make


def test_scan_for_release_strings_finds_nextjs_release(
    make_nextjs_sentry_config, tmp_path: Path
) -> None:
    validator = _load_validator()
    make_nextjs_sentry_config("boilerplate@74f9a95d")
    hits = validator._scan_for_release_strings(tmp_path, repo_slug="boilerplate")
    assert len(hits) == 1
    _, raw = hits[0]
    assert raw == "boilerplate@74f9a95d"


def test_scan_for_release_strings_finds_python_release(
    make_python_sentry_init, tmp_path: Path
) -> None:
    validator = _load_validator()
    make_python_sentry_init('"kirbe-platform@5fe2d18b"')
    hits = validator._scan_for_release_strings(tmp_path, repo_slug="kirbe-platform")
    assert len(hits) == 1
    _, raw = hits[0]
    assert raw == "kirbe-platform@5fe2d18b"


def test_validate_release_value_canonical_passes() -> None:
    validator = _load_validator()
    errors = validator._validate_release_value(
        "boilerplate@74f9a95d",
        expected_repo_slug="boilerplate",
        source_path=Path("/tmp/sentry.client.config.ts"),
    )
    assert errors == []


def test_validate_release_value_missing_at_separator_flagged() -> None:
    validator = _load_validator()
    errors = validator._validate_release_value(
        "1.0.0",
        expected_repo_slug="boilerplate",
        source_path=Path("/tmp/sentry.client.config.ts"),
    )
    assert len(errors) == 1
    assert "missing '@<sha>' suffix" in errors[0]


def test_validate_release_value_wrong_repo_prefix_flagged() -> None:
    validator = _load_validator()
    errors = validator._validate_release_value(
        "wrong-repo@74f9a95d",
        expected_repo_slug="boilerplate",
        source_path=Path("/tmp/sentry.client.config.ts"),
    )
    assert len(errors) == 1
    assert "does not match REPOSITORY_REGISTRY repo_slug 'boilerplate'" in errors[0]


def test_validate_release_value_dash_separator_flagged() -> None:
    validator = _load_validator()
    # The regex split-on-@ produces bare="boilerplate-74f9a95d" which differs
    # from the expected_repo_slug "boilerplate"; that surfaces as a prefix
    # mismatch rather than a missing-@ error.
    errors = validator._validate_release_value(
        "boilerplate-74f9a95d",
        expected_repo_slug="boilerplate",
        source_path=Path("/tmp/sentry.client.config.ts"),
    )
    assert len(errors) == 1
    assert "missing '@<sha>' suffix" in errors[0]


def test_validate_release_value_vercel_template_placeholder_accepted() -> None:
    validator = _load_validator()
    errors = validator._validate_release_value(
        "boilerplate@${process.env.VERCEL_GIT_COMMIT_SHA}",
        expected_repo_slug="boilerplate",
        source_path=Path("/tmp/sentry.client.config.ts"),
    )
    assert errors == [], f"unexpected errors: {errors}"


def test_validate_release_value_render_template_placeholder_accepted() -> None:
    validator = _load_validator()
    errors = validator._validate_release_value(
        "kirbe-platform@${RENDER_GIT_COMMIT}",
        expected_repo_slug="kirbe-platform",
        source_path=Path("/tmp/sentry.client.config.ts"),
    )
    assert errors == [], f"unexpected errors: {errors}"


def test_validate_release_value_garbage_sha_portion_flagged() -> None:
    validator = _load_validator()
    errors = validator._validate_release_value(
        "boilerplate@!!notasha!!",
        expected_repo_slug="boilerplate",
        source_path=Path("/tmp/sentry.client.config.ts"),
    )
    assert len(errors) == 1
    assert "neither a 7-12 char hex short-SHA nor a recognised templating placeholder" in errors[0]


# -----------------------------------------------------------------------------
# Constants smoke-checks
# -----------------------------------------------------------------------------


def test_release_template_canonical_constant() -> None:
    assert RELEASE_TEMPLATE_CANONICAL == "{repo_slug}@{sha_short}"


def test_repo_slug_pattern_kebab_case_lowercase() -> None:
    from akos.sentry_release import REPO_SLUG_RE
    assert REPO_SLUG_RE.match("boilerplate") is not None
    assert REPO_SLUG_RE.match("hlk-erp") is not None
    assert REPO_SLUG_RE.match("kirbe-platform") is not None
    assert REPO_SLUG_RE.match("openclaw-akos") is not None
    # Reject uppercase and edge-leading hyphen.
    assert REPO_SLUG_RE.match("Boilerplate") is None
    assert REPO_SLUG_RE.match("-boilerplate") is None
    assert REPO_SLUG_RE.match("boilerplate-") is None


def test_sha_short_pattern_7_to_12_chars_lowercase_hex() -> None:
    from akos.sentry_release import SHA_SHORT_RE
    assert SHA_SHORT_RE.match("1234567") is not None
    assert SHA_SHORT_RE.match("abcdef0") is not None
    assert SHA_SHORT_RE.match("123456789012") is not None
    # Too short / too long / wrong charset.
    assert SHA_SHORT_RE.match("123456") is None
    assert SHA_SHORT_RE.match("1234567890123") is None
    assert SHA_SHORT_RE.match("ABCDEFG") is None
    assert SHA_SHORT_RE.match("xyz1234") is None
