"""Playwright baseline configuration contract for Holistika consumer repos.

Initiative 68 P2 (D-IH-68-B). The canonical Playwright config template lives
at:

    docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/playwright.config.ts.tmpl

Every ``class=platform`` or ``class=reference`` consumer repo (per
``REPOSITORY_REGISTRY.csv``) mirrors that template into its own
``playwright.config.ts`` so multi-viewport visual regression coverage is
uniform across the fleet.

This module defines the **shape contract** as Pydantic models per
``CONTRIBUTING.md`` §"Python Code Standards":

- :class:`PlaywrightProject` — one entry of the ``projects[]`` array.
- :class:`PlaywrightBaselineConfig` — the canonical 5-viewport baseline
  every consumer-repo config must satisfy unless explicitly opted-out via
  ``REPOSITORY_REGISTRY.csv ci_baseline_optouts`` (column added in I68 P5).

The 5 standard viewport names + sizes are codified here so the validator,
the template, the Cursor rule (``akos-deploy-health.mdc``), and the
``REPOSITORY_REGISTRY.csv ci_baseline_optouts`` column all share a single
source of truth.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

# Five standard viewport names per akos-deploy-health.mdc §"Step 3 - Multi-viewport visual smoke".
# Keep in sync with the template at:
#   docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/playwright.config.ts.tmpl
ViewportName = Literal["iphone-se", "iphone-11", "ipad", "desktop", "wide"]

STANDARD_VIEWPORT_NAMES: tuple[ViewportName, ...] = (
    "iphone-se",
    "iphone-11",
    "ipad",
    "desktop",
    "wide",
)

# Canonical viewport sizes, used both for the template and for the validator
# when the consumer-repo config uses explicit ``viewport: { width, height }``
# rather than the Playwright ``devices['<name>']`` shorthand.
STANDARD_VIEWPORT_SIZES: dict[ViewportName, tuple[int, int]] = {
    "iphone-se": (375, 667),
    "iphone-11": (414, 896),
    "ipad": (768, 1024),
    "desktop": (1280, 800),
    "wide": (1920, 1080),
}


class PlaywrightProject(BaseModel):
    """One entry of a Playwright config ``projects[]`` array.

    The ``name`` must be one of the 5 :data:`STANDARD_VIEWPORT_NAMES`; an
    explicit width+height pair is required when the project does not use
    Playwright's ``devices['<name>']`` shorthand. When ``devices_key`` is
    set (e.g. ``'iPhone SE'``), ``viewport_width`` + ``viewport_height``
    may be ``None`` because Playwright's device preset supplies them.
    """

    name: ViewportName
    devices_key: str | None = Field(
        default=None,
        description=(
            "Optional Playwright device preset key (e.g. 'iPhone SE', 'iPhone 11')."
            " When set, viewport_width and viewport_height may be omitted because"
            " the device preset supplies them."
        ),
    )
    viewport_width: int | None = Field(default=None, ge=320, le=3840)
    viewport_height: int | None = Field(default=None, ge=480, le=2160)

    @field_validator("viewport_width", "viewport_height")
    @classmethod
    def _viewport_must_be_set_when_no_devices_key(
        cls, v: int | None, info
    ) -> int | None:
        # Pydantic v2 cross-field validation runs in model_validator; here we
        # only do single-field bounds checking. Cross-field validation lives
        # in PlaywrightBaselineConfig._validate_each_project_has_size.
        return v


class PlaywrightBaselineConfig(BaseModel):
    """A consumer repo's Playwright config baseline.

    The validator (``scripts/validate_playwright_baseline.py``) parses the
    consumer-repo ``playwright.config.ts`` into this model and asserts that
    every viewport in :data:`STANDARD_VIEWPORT_NAMES` is present unless the
    repo declares an opt-out in ``REPOSITORY_REGISTRY.csv ci_baseline_optouts``.

    ``retries_on_ci`` enforces the canonical 2-retries-on-CI policy from the
    template; deviations require an explicit ``ci_baseline_optouts``
    inclusion of ``"playwright-retries"``.
    """

    repo_slug: str = Field(
        pattern=r"^[a-z0-9][a-z0-9-]{1,80}$",
        description="REPOSITORY_REGISTRY.csv repo_slug primary key.",
    )
    # ``projects`` may be empty when the consumer repo's playwright.config.ts
    # uses a non-AKOS-canonical project naming convention (e.g. browser-named
    # 'chromium' / 'firefox' / 'webkit' instead of viewport-named 'iphone-se'
    # / 'desktop' / 'wide'); in that case ``missing_viewports()`` reports all
    # 5 standard viewports as missing — which is the actionable signal for
    # the I68 P2 sibling-repo carry-over PR.
    projects: list[PlaywrightProject] = Field(default_factory=list)
    retries_on_ci: int = Field(default=2, ge=0, le=5)
    ci_baseline_optouts: list[str] = Field(default_factory=list)

    def missing_viewports(self) -> list[ViewportName]:
        """Return the standard viewport names absent from this config.

        Opt-outs are honoured: a viewport listed in ``ci_baseline_optouts``
        as ``"playwright-viewport-<name>"`` is treated as intentionally
        absent and not reported as missing.
        """
        present_names = {p.name for p in self.projects}
        missing: list[ViewportName] = []
        for std in STANDARD_VIEWPORT_NAMES:
            opt_out_key = f"playwright-viewport-{std}"
            if std in present_names:
                continue
            if opt_out_key in self.ci_baseline_optouts:
                continue
            missing.append(std)
        return missing

    def has_explicit_size_drift(self) -> list[str]:
        """Return human-readable strings for projects whose explicit size
        deviates from :data:`STANDARD_VIEWPORT_SIZES`.

        Projects using the Playwright device preset shorthand
        (``devices_key`` set + ``viewport_width=None``) are exempt because
        Playwright's preset is the source of truth for that viewport.
        """
        drift: list[str] = []
        for project in self.projects:
            if project.viewport_width is None or project.viewport_height is None:
                continue
            if project.name not in STANDARD_VIEWPORT_SIZES:
                continue
            expected = STANDARD_VIEWPORT_SIZES[project.name]
            actual = (project.viewport_width, project.viewport_height)
            if actual != expected:
                drift.append(
                    f"project '{project.name}' uses viewport {actual[0]}x{actual[1]}"
                    f" but the AKOS canonical is {expected[0]}x{expected[1]}"
                )
        return drift
