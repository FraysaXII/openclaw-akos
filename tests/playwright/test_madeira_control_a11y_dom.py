"""Initiative 54 P2 — DOM-level a11y scenarios for `static/madeira_control.html`.

These tests do **not** require Playwright or axe-playwright-python to be
installed on the operator's machine; they exercise the **wiring** of the
new `--axe` flag in `scripts/browser-smoke.py` (Initiative 54 P1) and lock
in the DOM-level scenarios that the live Playwright run will assert
against (three-light status surfacing, language switcher, aria-pressed
toggles, focus-visible outlines, role=status announcements).

When Playwright + axe are installed, the live audit runs via
`py scripts/browser-smoke.py --playwright --axe`. The full live-audit
contract is tested separately at I54 P3 (operator-driven).

Test categories:
  1. Wiring tests — `_summarise_axe_violations`, `_check_axe_for_url`
     severity logic, `run_axe_audits` SKIP semantics.
  2. DOM-source contract tests — assert that `static/madeira_control.html`
     contains the **DOM-targetable** structure that the live Playwright
     run will assert against (locator selectors that the live tests need
     to be able to resolve).

These DOM-source contract tests overlap intentionally with the existing
HTML-source tests in `tests/test_madeira_control_a11y.py` (12 tests; I49
P15 baseline). The HTML-source tests stay unchanged; these tests target
DOM-locator stability for the live axe run.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

CONTROL_HTML_PATH = REPO_ROOT / "static" / "madeira_control.html"
BROWSER_SMOKE_PATH = REPO_ROOT / "scripts" / "browser-smoke.py"


@pytest.fixture(scope="module")
def html_text() -> str:
    return CONTROL_HTML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def browser_smoke_module():
    """Load `scripts/browser-smoke.py` as a module so we can exercise its
    helpers without invoking the CLI."""
    spec = importlib.util.spec_from_file_location("scripts.browser_smoke_axe", BROWSER_SMOKE_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["scripts.browser_smoke_axe"] = mod
    spec.loader.exec_module(mod)
    return mod


# ---- 1. Wiring tests for the I54 P1 helpers ------------------------------


def test_summarise_axe_violations_counts_by_impact(browser_smoke_module):
    fn = browser_smoke_module._summarise_axe_violations
    violations = [
        {"impact": "critical", "id": "color-contrast"},
        {"impact": "critical", "id": "label"},
        {"impact": "serious", "id": "aria-roles"},
        {"impact": "moderate", "id": "region"},
        {"impact": "minor", "id": "valid-lang"},
        {"impact": None, "id": "experimental-rule"},
    ]
    counts = fn(violations)
    assert counts["critical"] == 2
    assert counts["serious"] == 1
    assert counts["moderate"] == 1
    assert counts["minor"] == 1
    assert counts["unknown"] == 1


def test_summarise_axe_violations_handles_empty(browser_smoke_module):
    fn = browser_smoke_module._summarise_axe_violations
    assert fn([]) == {"critical": 0, "serious": 0, "moderate": 0, "minor": 0, "unknown": 0}
    assert fn(None) == {"critical": 0, "serious": 0, "moderate": 0, "minor": 0, "unknown": 0}  # type: ignore[arg-type]


def test_summarise_axe_violations_unknown_impact_routes_to_unknown_bucket(browser_smoke_module):
    fn = browser_smoke_module._summarise_axe_violations
    counts = fn([{"impact": "trivial-not-real", "id": "x"}])
    assert counts["unknown"] == 1
    assert sum(counts.values()) == 1


def test_axe_in_scope_surfaces_includes_madeira_control(browser_smoke_module):
    surfaces = browser_smoke_module.AXE_IN_SCOPE_SURFACES
    scenario_ids = [s for s, _ in surfaces]
    url_paths = [u for _, u in surfaces]
    assert "axe_madeira_control" in scenario_ids
    assert "/madeira/control" in url_paths


def test_run_axe_audits_skips_when_playwright_unavailable(browser_smoke_module, monkeypatch):
    monkeypatch.setattr(browser_smoke_module, "PLAYWRIGHT_AVAILABLE", False)
    results = browser_smoke_module.run_axe_audits(headed=False, engine=None)
    assert all(r["status"] == "SKIP" for r in results)
    assert any("Playwright not installed" in r["detail"] for r in results)


def test_run_axe_audits_skips_when_axe_unavailable(browser_smoke_module, monkeypatch):
    monkeypatch.setattr(browser_smoke_module, "PLAYWRIGHT_AVAILABLE", True)
    monkeypatch.setattr(browser_smoke_module, "AXE_AVAILABLE", False)
    results = browser_smoke_module.run_axe_audits(headed=False, engine=None)
    assert all(r["status"] == "SKIP" for r in results)
    assert any("axe-playwright-python not installed" in r["detail"] for r in results)
    assert any("Initiative 54 P1" in r["detail"] for r in results)


def test_run_axe_audits_returns_one_result_per_in_scope_surface(browser_smoke_module, monkeypatch):
    monkeypatch.setattr(browser_smoke_module, "PLAYWRIGHT_AVAILABLE", False)
    results = browser_smoke_module.run_axe_audits(headed=False, engine=None)
    expected = len(browser_smoke_module.AXE_IN_SCOPE_SURFACES)
    assert len(results) == expected


def test_axe_flag_argparse_present(browser_smoke_module):
    """The CLI must accept --axe (regression test for the I54 P1 flag)."""
    src = BROWSER_SMOKE_PATH.read_text(encoding="utf-8")
    assert '"--axe"' in src
    assert "Initiative 54 P1" in src


# ---- 2. DOM-source contract tests ----------------------------------------


def test_madeira_control_has_dom_locator_for_three_light_status(html_text: str) -> None:
    """The live Playwright run will resolve a `role=status` element. Lock
    the locator stability at the source so a future redesign cannot move
    the live target without an explicit decision."""
    assert 'role="status"' in html_text
    assert 'aria-live="polite"' in html_text


def test_madeira_control_has_dom_locator_for_locale_buttons(html_text: str) -> None:
    """Live Playwright run must be able to click each locale button by a
    stable selector."""
    assert 'data-locale-set="en"' in html_text
    assert 'data-locale-set="es"' in html_text
    assert 'data-locale-set="fr"' in html_text


def test_madeira_control_has_dom_locator_for_mode_buttons(html_text: str) -> None:
    """`btn-ask` carries the aria-pressed toggle that the live Playwright
    run will assert flips on click."""
    assert 'id="btn-ask"' in html_text
    assert 'aria-pressed=' in html_text


def test_madeira_control_has_focus_visible_rule(html_text: str) -> None:
    """Live Playwright tab-traversal test will require focus-visible to be
    visually distinguishable; lock the rule at the source."""
    assert "button:focus-visible" in html_text


def test_madeira_control_has_main_landmark_for_axe_landmark_rule(html_text: str) -> None:
    """axe-core's `landmark-one-main` rule requires exactly one <main>;
    failing this is Critical."""
    assert "<main>" in html_text and "</main>" in html_text


def test_madeira_control_no_external_resources_for_offline_audit(html_text: str) -> None:
    """The live axe run must work fully offline; any `<script src=` or
    `<link>` makes that brittle and risks Critical findings if the remote
    asset goes down or pins drift."""
    assert "<script src=" not in html_text
    assert "<link " not in html_text


def test_madeira_control_no_blocking_alert_for_axe_keyboard_trap(html_text: str) -> None:
    """`alert()` is a screen-reader keyboard trap; the I49 P15 redesign
    explicitly removed it. Lock that removal at the source."""
    assert "alert(" not in html_text


# ---- 3. I57 P1 — OPS-54-1.a + OPS-54-1.b regression locks --------------------


def test_i57_locale_buttons_have_explicit_high_contrast_styling(html_text: str) -> None:
    """OPS-54-1.a (closes I54 audit F-1) — inactive locale buttons must carry
    explicit ``color: var(--ink)`` + ``border-color: var(--ink-2)`` styling so
    axe-core's color-contrast (WCAG 1.4.3) Serious finding does not regress.

    The fix is a single CSS rule ``.locale button { ... }`` at static/madeira_control.html.
    """
    assert ".locale button { color: var(--ink); border-color: var(--ink-2); }" in html_text, (
        "OPS-54-1.a regression: the explicit `.locale button` color + border rule is missing; "
        "axe-core color-contrast (WCAG 1.4.3) Serious finding will return"
    )


def test_i57_handoff_example_is_keyboard_focusable(html_text: str) -> None:
    """OPS-54-1.b (closes I54 audit F-2) — ``#handoff-example`` is a scrollable
    ``<pre>`` region and must be reachable by keyboard (axe rule
    ``scrollable-region-focusable``, WCAG 2.1.1 + 2.1.3).

    The fix is ``tabindex="0"`` on the ``<pre id="handoff-example">`` element
    plus an ``aria-label`` describing the region.
    """
    assert 'id="handoff-example" tabindex="0"' in html_text, (
        "OPS-54-1.b regression: scrollable region #handoff-example must carry tabindex=0 "
        "or axe scrollable-region-focusable (WCAG 2.1.1 + 2.1.3) Serious finding will return"
    )
    assert 'aria-label="Madeira plan handoff schema example (scrollable)"' in html_text, (
        "OPS-54-1.b regression: keyboard-focusable scrollable region should expose an "
        "aria-label so screen readers announce its purpose"
    )


def test_i57_p6_followup_light_mode_accent_is_deepened_for_wcag_contrast(html_text: str) -> None:
    """OPS-54-1.c — the light-mode ``--accent`` must be deepened to oklch(48%)
    so the active ``aria-pressed="true"`` state on locale buttons clears the
    WCAG 1.4.3 4.5:1 contrast boundary against ``--accent-ink`` (oklch 99%).

    The previous ``oklch(56%)`` value sat at the boundary and produced a
    residual axe-core color-contrast Serious finding even after OPS-54-1.a
    hardened the inactive state. This regression lock asserts the deepened
    value is present in the light-mode ``:root`` block.
    """
    assert "--accent: oklch(48% 0.16 var(--brand-h));" in html_text, (
        "OPS-54-1.c regression: light-mode --accent must be oklch(48%) (deepened from "
        "oklch(56%)) or the active locale button color-contrast Serious finding will return"
    )
    # Dark-mode --accent at oklch(70%) was already passing and stays untouched;
    # this test does NOT lock the dark-mode value (out of scope for OPS-54-1.c).
