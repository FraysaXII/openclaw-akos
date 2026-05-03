---
language: en
status: active
initiative: 54-surface-test-hardening
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 54 — Decision log

Four decisions seeded; operator-ratified at I50-I56 master roadmap greenlight 2026-05-03.

## D-IH-54-A — axe-core severity bar for CI fail: Critical only

**Decision:** **Critical only** (default); Serious is warn-only at first run, escalates after one cycle of clean operation.

**Rationale:** axe-core's "Critical" tier maps to the WCAG-2.1 Level-A barriers that consistently break assistive-tech users (e.g., missing form labels, contrast <3:1 on text, kb-trap). "Serious" tier maps to issues that are problematic but not always blocking (e.g., contrast 3:1 ≤ ratio < 4.5:1). A two-step ramp (Serious warn-only → Serious-fail after one clean cycle) avoids the adoption tax of importing a fully strict bar on day one while still putting Serious findings on a planned escalation track.

**Reversibility:** Medium — one POLICY row + decision-log update.

---

## D-IH-54-B — Test runner location: pre_commit (warn) + release_gate (Critical-only gate)

**Decision:** `playwright_a11y_smoke` step lives in **pre_commit** (warn-only when not installed; warn on any Critical when installed) AND in **release_gate** (Critical-only gate; release blocks if any Critical found).

**Rationale:** Pre-commit is the dev-time signal; release-gate is the ship-time gate. Splitting the two avoids both the "everyone has to install Playwright + axe to commit" tax and the "ship with known Critical violations" risk. Mirrors the existing pattern in [`config/verification-profiles.json`](../../../config/verification-profiles.json) where `pre_commit` is fast/permissive and `release_gate` is comprehensive/strict.

**Reversibility:** Medium — single profile JSON edit.

---

## D-IH-54-C — HTML surfaces in scope: madeira_control + dossier HTML; NOT deck assets

**Decision:** In-scope surfaces are **`static/madeira_control.html`** + **dossier HTML output** (rendered by `scripts/render_uat_dossier.py --format html`). **Out of scope:** deck assets and any non-operator-facing static HTML.

**Rationale:** The deck assets have their own [brand-jargon-audit lint at I49 P12](../49-madeira-management-rollup/reports/p12-brand-jargon-audit-2026-05-03.md) and are not assistive-tech-consumed (they're presentation slides; a11y is a different quality gate from WCAG operator-surface compliance). The two surfaces in scope are the surfaces operators interact with daily.

**Reversibility:** High — scope is a list, can be extended.

---

## D-IH-54-D — Defer-policy for Moderate/Minor findings

**Decision:** Moderate and Minor findings get a **backlog row in `risk-register.md`** with WCAG ID + brief remediation hint; revisit at the next WCAG 2.2 industry adoption signal (e.g., when WCAG 2.2 becomes the de facto standard in EU enterprise procurement contracts).

**Rationale:** Moderate and Minor findings are by definition not blocking. Recording them in `risk-register.md` (not in CHANGELOG, not in deck) keeps them visible for a future cycle without expanding the ship gate. Tying revisit to an industry adoption signal (rather than an arbitrary calendar date) avoids "the deferred-fix list grows because nothing has changed externally."

**Reversibility:** High — defer→fix is a per-finding promotion.

---

## Decisions made during execution

(Will be appended as P0-P6 phases execute.)
