---
language: en
status: active
initiative: 54-surface-test-hardening
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 54 — Risk register

## R-54-1 — Playwright + axe not available on operator's machine; CI false-flagging

**Severity:** Medium.

**Mitigation:** Warn-only at pre_commit when not installed; install runbook in `USER_GUIDE`. CI gates only when the dependency is actually present. Status semantics: `SKIP` with a clear "Playwright + axe-core not installed" detail message (mirrors the existing `--playwright not installed` SKIP path in `browser-smoke.py`).

**Status:** Active.

---

## R-54-2 — A11y fix breaks existing operator workflow

**Severity:** Medium-Low (the redesign baseline is already clean per I49 P15 + impeccable critique).

**Mitigation:** G-54-1 gate (any breaking HTML structural change requires explicit operator approval); impeccable critique re-run after each Critical fix. Today's expected zero-Critical baseline means G-54-1 is unlikely to fire.

**Status:** Active.

---

## R-54-3 — Dossier HTML template auto-renders new violations as KM data lands

**Severity:** Low.

**Mitigation:** Dossier HTML template is canonical (small surface; the Jinja-style template lives in `akos/dossier/`); the test asserts at template-time, not at render-time, so accumulated KM data cannot introduce a regression.

**Status:** Active.

---

## R-54-4 — `axe-playwright-python` not installable in this cursor session

**Severity:** Low (anticipated; stub-mode is the documented response).

**Mitigation:** P3 ships in **stub mode** (zero-finding dispatcher-validation report) mirroring I52 P3 / P5 / I53 P3 pattern; **OPS-54-1 forwarded** to next operator-side install + run cycle.

**Status:** Active; will be realized at P3.

---

## Deferred backlog (D-IH-54-D defer-policy)

The defer-policy table receives Moderate / Minor findings as P3 audits surface them. Empty today.

| Finding | WCAG ID | Severity | Surface | Remediation hint | Status |
|:--------|:--------|:---------|:--------|:-----------------|:-------|
| (none yet) | | | | | |
