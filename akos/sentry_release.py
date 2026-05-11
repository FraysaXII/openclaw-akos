"""Sentry release-format Pydantic models for I68 P4 (D-IH-68-I).

Defines the canonical cross-repo Sentry release version string contract:

    <repo_slug>@<sha_short>

where ``repo_slug`` matches ``REPOSITORY_REGISTRY.csv repo_slug`` (lowercase
kebab-case ``[a-z0-9][a-z0-9-]+[a-z0-9]``) and ``sha_short`` is a 7-12
character lowercase hex git short-SHA. Examples:

    boilerplate@74f9a95d
    hlk-erp@a3b1c92e
    kirbe-platform@5fe2d18b

Why this format:

- **Cross-repo Sentry queries unambiguous.** Filtering by release prefix
  (``release:boilerplate@*``) returns events for that repo only.
- **No vendor lock-in to semver.** The Sentry vendor-default
  ``<package@version>`` works for npm packages but not for app deploys; the
  short-SHA is the deploy artifact identifier we actually need.
- **Consistent with akos-deploy-health.mdc release-tagging language.**

The validator at ``scripts/validate_sentry_release_format.py`` scans each
consumer-repo's Sentry init code for the ``release:`` field and asserts the
extracted template matches this rule. Drift modes the validator catches:

- ``release: undefined`` (Sentry vendor default; no cross-repo discrimination).
- ``release: "1.0.0"`` (semver-only; no commit traceability).
- ``release: "<sha>"`` (no repo prefix; ambiguous across repos).
- ``release: "<repo>-<sha>"`` (wrong separator; uses ``-`` instead of ``@``).
- ``release: "<wrong-repo>@<sha>"`` (repo_slug mismatch with REPOSITORY_REGISTRY).

The Pydantic model below is the source of truth for the regex used by both
the validator and any future consumer-side code that wants to construct the
release string programmatically.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator

REPO_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]+[a-z0-9]$")
SHA_SHORT_RE = re.compile(r"^[0-9a-f]{7,12}$")
RELEASE_TEMPLATE_CANONICAL = "{repo_slug}@{sha_short}"
RELEASE_VALUE_RE = re.compile(r"^(?P<repo_slug>[a-z0-9][a-z0-9-]+[a-z0-9])@(?P<sha_short>[0-9a-f]{7,12})$")


class SentryReleaseFormatRule(BaseModel):
    """The canonical Sentry release-format rule.

    A repo's Sentry config carries a ``release_template`` string that, after
    runtime interpolation of the literal ``{repo_slug}`` and ``{sha_short}``
    placeholders, must match :data:`RELEASE_TEMPLATE_CANONICAL`.
    """

    release_template: str = Field(
        description=(
            "Sentry release format string. Must equal "
            f"'{RELEASE_TEMPLATE_CANONICAL}' verbatim per D-IH-68-I."
        )
    )

    @field_validator("release_template")
    @classmethod
    def must_use_repo_at_sha_template(cls, v: str) -> str:
        if v != RELEASE_TEMPLATE_CANONICAL:
            raise ValueError(
                f"release_template must be {RELEASE_TEMPLATE_CANONICAL!r}, got {v!r}"
            )
        return v


class SentryReleaseValue(BaseModel):
    """A concrete Sentry release value extracted from a consumer-repo config.

    Used by the validator to assert that the release-string actually emitted
    at runtime decomposes into a known ``repo_slug`` + a short-SHA.
    """

    raw: str = Field(description="The literal release string as found in the config.")
    repo_slug: str
    sha_short: str

    @field_validator("repo_slug")
    @classmethod
    def repo_slug_must_match_pattern(cls, v: str) -> str:
        if not REPO_SLUG_RE.match(v):
            raise ValueError(
                f"repo_slug {v!r} does not match canonical pattern {REPO_SLUG_RE.pattern}"
            )
        return v

    @field_validator("sha_short")
    @classmethod
    def sha_short_must_match_pattern(cls, v: str) -> str:
        if not SHA_SHORT_RE.match(v):
            raise ValueError(
                f"sha_short {v!r} does not match canonical pattern {SHA_SHORT_RE.pattern}"
            )
        return v


def parse_release_value(raw: str) -> SentryReleaseValue | None:
    """Parse a raw Sentry release string into a :class:`SentryReleaseValue`.

    Returns ``None`` when the string does not match the ``<repo>@<sha>``
    canonical shape; the validator surfaces this as drift.
    """
    match = RELEASE_VALUE_RE.match(raw.strip())
    if not match:
        return None
    return SentryReleaseValue(
        raw=raw.strip(),
        repo_slug=match.group("repo_slug"),
        sha_short=match.group("sha_short"),
    )
