"""CICD baseline Pydantic models for I68 P5 (D-IH-68-D, D-IH-68-J).

Models the per-class CI/CD baseline matrix codified in
``docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-CICD_BASELINE_001.md``
§3 + the per-repo opt-out matrix in §7.

Forward-compatible: tolerates absence of the new ``REPOSITORY_REGISTRY.csv``
columns (``ci_baseline_version``, ``build_time_target_seconds``,
``ci_baseline_optouts``) until I68 P5 PAUSE POINT #3 — canonical CSV gate
lands the bumps. Until then ``CICDBaselineRow.from_registry_row`` returns a
defaulted model (no opt-outs; no version pinned; no build-time target).
"""

from __future__ import annotations

import json
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# Per-class enforcement matrix per SOP-CICD_BASELINE_001 §3 (the "✓" cells).
RepoClass = Literal["platform", "reference", "internal", "client-delivery"]

# Per-check opt-out string identifiers from SOP-CICD_BASELINE_001 §3 + §7.
# Per-viewport opt-outs (``playwright-viewport-<name>``) are governed by the
# I68 P2 Playwright baseline rule and re-used here without enumeration.
KNOWN_CHECK_OPTOUTS: frozenset[str] = frozenset(
    {
        "lint",
        "typecheck",
        "unit-test",
        "playwright-smoke",
        "visual-regression",
        "lighthouse",
        "brand-jargon",
        "brand-voice-register",
        "sentry-release-format",
        "sentry-skip-on-preview",
        "build-time-target",
        # Inherited from I68 P2 Playwright baseline rule:
        "playwright-retries",
        "playwright-viewport-iphone-se",
        "playwright-viewport-iphone-11",
        "playwright-viewport-ipad",
        "playwright-viewport-desktop",
        "playwright-viewport-wide",
    }
)

# Per-class required-checks set per SOP-CICD_BASELINE_001 §3.
PER_CLASS_REQUIRED_CHECKS: dict[RepoClass, frozenset[str]] = {
    "platform": frozenset(
        {
            "lint",
            "typecheck",
            "unit-test",
            "playwright-smoke",
            "visual-regression",
            "lighthouse",
            "brand-jargon",
            "brand-voice-register",
            "sentry-release-format",
            "sentry-skip-on-preview",
            "build-time-target",
        }
    ),
    "reference": frozenset(
        {
            "lint",
            "typecheck",
            "unit-test",
            "playwright-smoke",
            "visual-regression",
            "lighthouse",
            "brand-jargon",
            "brand-voice-register",
            "sentry-release-format",
            "sentry-skip-on-preview",
            "build-time-target",
        }
    ),
    "internal": frozenset({"lint", "typecheck", "unit-test"}),
    # Defined in a successor SOP version when first such repo blesses.
    "client-delivery": frozenset({"lint", "typecheck", "unit-test"}),
}

# Per-class default `build_time_target_seconds` per D-IH-68-E.
PER_CLASS_DEFAULT_BUILD_TIME_TARGET_SECONDS: dict[RepoClass, int] = {
    "platform": 300,  # default for Render Python+Node hybrid (kirbe-platform); Vercel-only narrows to 120.
    "reference": 120,  # default for Vercel Next.js (boilerplate)
    "internal": 60,  # static-only-ish default
    "client-delivery": 300,  # conservative default until first such repo defines.
}

# Pin: the first SOP version that introduces the canonical CSV-gated baseline
# (post I68 P5 PAUSE POINT #3 + I68 P8 closure promotion). Until P8 promotion,
# consumer repos may carry ``ci_baseline_version: v0.9.0``.
KNOWN_SOP_VERSIONS: frozenset[str] = frozenset({"v0.9.0", "v1.0.0"})


class CICDBaselineRow(BaseModel):
    """A single repo's CI/CD baseline metadata extracted from REPOSITORY_REGISTRY.csv.

    Fields with default ``None`` correspond to columns that ship after I68 P5
    PAUSE POINT #3; the validator treats them as "no opt-outs" / "no target"
    until the column lands.
    """

    repo_slug: str = Field(pattern=r"^[a-z0-9][a-z0-9-]+[a-z0-9]$")
    repo_class: RepoClass
    ci_baseline_version: str | None = Field(
        default=None,
        description=(
            "SOP-CICD_BASELINE_001 version this repo's workflow mirrors. "
            "Populated by `bless_external_repo.py --with ci-baseline`."
        ),
    )
    build_time_target_seconds: int | None = Field(
        default=None,
        ge=10,
        le=3600,
        description="Per-repo preview build-time target per D-IH-68-E.",
    )
    ci_baseline_optouts: list[str] = Field(default_factory=list)

    @field_validator("ci_baseline_version")
    @classmethod
    def known_sop_version_or_none(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        if v not in KNOWN_SOP_VERSIONS:
            raise ValueError(
                f"ci_baseline_version {v!r} is not a known SOP-CICD_BASELINE_001 "
                f"version; allowed values: {sorted(KNOWN_SOP_VERSIONS)}"
            )
        return v

    @field_validator("ci_baseline_optouts")
    @classmethod
    def opt_outs_must_be_known(cls, v: list[str]) -> list[str]:
        unknown = [s for s in v if s not in KNOWN_CHECK_OPTOUTS]
        if unknown:
            raise ValueError(
                f"ci_baseline_optouts contains unknown opt-out keys {sorted(unknown)}; "
                f"allowed values are documented in SOP-CICD_BASELINE_001.md §3 + §7"
            )
        return v

    def required_checks(self) -> frozenset[str]:
        """Return the set of checks this repo MUST run (per SOP §3 minus opt-outs)."""
        baseline = PER_CLASS_REQUIRED_CHECKS[self.repo_class]
        return frozenset(c for c in baseline if c not in self.ci_baseline_optouts)

    def missing_checks(self, *, observed_checks: frozenset[str]) -> list[str]:
        """Return the names of required checks not present in ``observed_checks``."""
        return sorted(self.required_checks() - observed_checks)

    @classmethod
    def from_registry_row(cls, row: dict[str, str]) -> "CICDBaselineRow":
        """Construct a baseline row from a REPOSITORY_REGISTRY.csv DictReader row.

        Forward-compatible: tolerates missing ``ci_baseline_version``,
        ``build_time_target_seconds``, ``ci_baseline_optouts`` columns.
        """
        repo_slug = (row.get("repo_slug") or "").strip()
        repo_class_raw = (row.get("class") or "").strip().lower()
        # Pydantic Literal validation handles the class check.
        version_raw = (row.get("ci_baseline_version") or "").strip() or None
        build_time_raw = (row.get("build_time_target_seconds") or "").strip()
        build_time = int(build_time_raw) if build_time_raw.isdigit() else None
        optouts_raw = (row.get("ci_baseline_optouts") or "").strip()
        if not optouts_raw:
            optouts: list[str] = []
        elif optouts_raw.startswith("["):
            try:
                parsed = json.loads(optouts_raw)
                optouts = [str(x) for x in parsed]
            except Exception:  # noqa: BLE001 - tolerate malformed values, treat as no opt-outs
                optouts = []
        else:
            optouts = [s.strip() for s in optouts_raw.split(";") if s.strip()]
        return cls(
            repo_slug=repo_slug,
            repo_class=repo_class_raw,  # type: ignore[arg-type]
            ci_baseline_version=version_raw,
            build_time_target_seconds=build_time,
            ci_baseline_optouts=optouts,
        )
