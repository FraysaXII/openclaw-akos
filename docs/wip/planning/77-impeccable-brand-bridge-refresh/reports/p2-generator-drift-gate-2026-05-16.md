---
phase: P2
initiative: INIT-OPENCLAW_AKOS-77
title: Strand B — Generator + drift gate (Pydantic chassis + validator + release-gate wiring)
status: shipped
ship_date: 2026-05-16
owner_role: Brand Manager (drift contract) + System Owner (chassis + validator + release-gate wiring)
linked_decisions:
  - D-IH-77-A (charter; P0)
  - D-IH-77-C (Strand B posture — soft-30d-then-strict per validate_cicd_baseline precedent)
linked_ops: OPS-77-1 (open; closes at P3 UAT)
phase_dependency_satisfied:
  - I77 P1 ship (MET — three bridges refreshed/created 2026-05-16; coverage 18/18 brand canonicals)
  - I71 P1 Pack A1 ship (MET — `akos/brand_voice_register.py` Pydantic chassis precedent followed)
language: en
---

# I77 P2 — Generator + drift gate (Strand B) phase report

> **Status: shipped 2026-05-16.** Pydantic chassis `akos/impeccable_bridge.py` (351 lines) mints three models (`CanonicalCrossReference`, `BridgeFileSpec`, `BridgeCoverageReport`) + parser helpers + coverage computation. Two scripts ship: `scripts/validate_impeccable_bridge_drift.py` (drift gate; soft-30d-then-strict per D-IH-77-C) and `scripts/generate_impeccable_bridges.py` (`--check` coverage report; `--write` mode reserved for forward-charter). 19 governance tests (`tests/test_impeccable_bridge.py`) pass; release-gate wiring complete with new `impeccable_bridge_drift_smoke` verification profile. Current coverage: **18/18 brand canonicals cited by ≥ 1 bridge (100%)** — drift gate ships green.

## Scope

Per the I77 [`master-roadmap.md`](../master-roadmap.md) §"Strand B — Generator + drift gate (P2)", deliver:

1. **Pydantic chassis** at [`akos/impeccable_bridge.py`](../../../../akos/impeccable_bridge.py) following the `akos.brand_voice_register` pattern from I71 P1.4 — models for `CanonicalCrossReference`, `BridgeFileSpec`, `BridgeCoverageReport` + parser helpers `parse_canonical_inventory`, `extract_cross_referenced_filenames`, `parse_bridge_file`, `parse_all_bridge_files` + coverage computation `compute_coverage` + markdown rendering `render_coverage_section_markdown`.
2. **Drift gate** at [`scripts/validate_impeccable_bridge_drift.py`](../../../../scripts/validate_impeccable_bridge_drift.py) that scans the canonical inventory (`CANONICAL_REGISTRY.csv` `owning_area=Marketing AND owning_role=Brand AND non-SOP`) and asserts each active row appears as a cross-reference in ≥ 1 of the 3 bridges. Strictness ladder per D-IH-77-C: **soft-30d-then-strict** default; promote via `AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT=1` or `--strict`.
3. **Generator** at [`scripts/generate_impeccable_bridges.py`](../../../../scripts/generate_impeccable_bridges.py) operating in `--check` mode today (non-mutating; prints markdown coverage report to stdout). `--write` mode is deliberately reserved — bridges remain operator-authored prose for now; mechanical regeneration deferred to a forward-charter I-NN initiative once the fenced-regenerable-section pattern is ratified.
4. **Governance tests** at [`tests/test_impeccable_bridge.py`](../../../../tests/test_impeccable_bridge.py) — 19 tests covering Pydantic model validity (4), parser robustness on missing files + malformed input (5), coverage computation happy-path + drift-detection + missing-bridges (3), markdown rendering smoke (1), drift-gate script invocation (1), generator script invocation + write-mode rejection (2), and cross-reference extraction patterns (3).
5. **Release-gate + verification-profile wiring** — new `run_impeccable_bridge_drift_validation()` function in [`scripts/release-gate.py`](../../../../scripts/release-gate.py); new `impeccable_bridge_drift_smoke` profile in [`config/verification-profiles.json`](../../../../config/verification-profiles.json); `brand` test group description in [`scripts/test.py`](../../../../scripts/test.py) extended to mention the I77 P2 additions so the when-to-run hint is current.

All deliverables follow [`CONTRIBUTING.md`](../../../../CONTRIBUTING.md) §"Python Code Standards": Pydantic v2 models with `model_config = ConfigDict(frozen=True)` + field validators (no hand-written `assert` chains); type hints on every signature + return type; structured logging via `akos.log.setup_logging` (no `print()`); `pathlib.Path` (no shell-specific constructs); tests registered under `@pytest.mark.brand` (existing registered marker covering I71 P1 chassis tests — natural fit for this sibling family) and runnable via `py scripts/test.py brand`.

## Mechanical evidence

### Files modified or created

| Path | Change kind | Lines | Description |
|:---|:---|:---:|:---|
| [`akos/impeccable_bridge.py`](../../../../akos/impeccable_bridge.py) | **created** | +351 | Pydantic chassis — 3 models + 6 parser helpers + coverage computation + markdown renderer. Excludes 2 canonicals: `impeccable_bridge_baseline_reality` (self-reference avoidance) + `brand_validators_readme` (I71 P1 Pack A1 `_validators/` folder meta-doc; not brand SSOT). |
| [`scripts/validate_impeccable_bridge_drift.py`](../../../../scripts/validate_impeccable_bridge_drift.py) | **created** | +147 | Drift gate. CLI flags: `--strict` + env var `AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT=1`. Default soft-30d-then-strict per D-IH-77-C. Exits 1 on missing bridges or in strict mode on drift; exits 0 with WARN otherwise. |
| [`scripts/generate_impeccable_bridges.py`](../../../../scripts/generate_impeccable_bridges.py) | **created** | +135 | `--check` mode (default; non-mutating; prints coverage markdown). `--write` mode explicitly reserved (exit 2 with "not yet implemented" message; forward-charter to a successor initiative once fenced-regenerable-section pattern lands per `D-IH-77-C` forward-clause). |
| [`tests/test_impeccable_bridge.py`](../../../../tests/test_impeccable_bridge.py) | modified | +428 / −81 | Mostly **created** content (file existed as P0 stub; P2 fills it out). 19 tests under `@pytest.mark.brand`. Includes Pydantic-validity, parser-robustness, coverage-computation, markdown-render smoke, and script-invocation tests. |
| [`scripts/release-gate.py`](../../../../scripts/release-gate.py) | modified | +30 | New `run_impeccable_bridge_drift_validation()` function + INFO-row registration (flips to PASS/FAIL with `AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT=1`). Inserted between BRAND vision drift and dossier-companion-drift rows. |
| [`config/verification-profiles.json`](../../../../config/verification-profiles.json) | modified | +15 | New `impeccable_bridge_drift_smoke` profile with 2 steps: `validate_impeccable_bridge_drift` + `generate_impeccable_bridges_check`. |
| [`scripts/test.py`](../../../../scripts/test.py) | modified | +7 / −1 | Extended `brand` group description + when-to-run hint to cover the I77 P2 chassis + scripts + bridges. |
| [`CHANGELOG.md`](../../../../CHANGELOG.md) | modified | +14 | New `## [Unreleased]` `### Added` entry for I77 P2. |
| [`docs/wip/planning/77-impeccable-brand-bridge-refresh/files-modified.csv`](../files-modified.csv) | modified | +15 | P1 + P2 row appends (per `akos-planning-traceability.mdc` §"Per-initiative file-changes CSV"). |
| [`docs/wip/planning/77-impeccable-brand-bridge-refresh/reports/p2-generator-drift-gate-2026-05-16.md`](./p2-generator-drift-gate-2026-05-16.md) | **created** | +this | This phase report. |

**Total P2 net delta:** +1142 lines / −82 lines across 7 modified + 4 created files (excluding this report).

### Validators run

| Validator | Verdict | Notes |
|:---|:---:|:---|
| `py scripts/validate_impeccable_bridge_drift.py` | **PASS** (soft) | Coverage 18/18 = 100% — no drift; gate ships green. |
| `py scripts/generate_impeccable_bridges.py --check` | **PASS** | Full per-canonical coverage table emitted to stdout. |
| `py scripts/generate_impeccable_bridges.py --write` | **FAIL** (intended) | Exits 2 with "not yet implemented" message — write-mode reservation verified. |
| `py -m pytest tests/test_impeccable_bridge.py -v` | **PASS** | 19/19 tests pass in 1.29s. |
| `py scripts/test.py brand` | **PASS** | 274 passed / 2121 deselected in 10.67s — full brand test group green (I71 Pack A1 + I77 P2). |
| `py scripts/release-gate.py` | **OVERALL: PASS** | New `IMPECCABLE bridge drift` INFO row registered cleanly between BRAND vision drift + dossier-companion-drift. |
| `py scripts/verify.py impeccable_bridge_drift_smoke` | **PASS** | Both profile steps complete cleanly. |

### Drift gate strictness ladder (D-IH-77-C)

The drift gate ships in **soft mode** today (warn-only; exit 0 on drift). Per `D-IH-77-C`:

- **Soft window:** 30 days from P2 ship (2026-05-16 → 2026-06-15). Operator + agents have time to adopt the bridge-citation discipline without CI fail-on-drift pressure.
- **Auto-promotion to strict:** 2026-06-15 forward, the gate promotes to strict (fail-loud on drift) — either via a single-line code change (default-flip) or via the env var `AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT=1` set in CI workflow. Operator decides at P3 UAT closure which path to take.
- **Manual override always available:** `--strict` CLI flag or env var flips strict mode in any session, regardless of date.

Coverage as of P2 ship: **100% (18/18)** — no missing canonicals; gate is already strict-ready before the soft window expires. If the operator decides to promote early, the single change is in `scripts/release-gate.py` (drop the `os.environ.get("AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT")` check and make the row PASS/FAIL unconditionally).

### Exclusion list (deliberate)

`EXCLUDED_CANONICAL_IDS` in `akos/impeccable_bridge.py` carries 2 entries:

| canonical_id | Reason | Justification |
|:---|:---|:---|
| `impeccable_bridge_baseline_reality` | Self-reference avoidance | The `BASELINE_REALITY.md` bridge is itself a registered canonical (I77 P1 row in CANONICAL_REGISTRY.csv) but does not need to cross-reference itself. |
| `brand_validators_readme` | Not brand SSOT | I71 P1 Pack A1 `_validators/` folder index (`canonicals/_validators/README.md`). Meta-documentation for operator-editable YAML rule packs — not voice/visual/audience content that Impeccable should consume. |

Both exclusions are documented inline with comments in the chassis; future additions should follow the same justification pattern (one-line code comment + entry in this report or its P-N successor).

## Documentary evidence

### Decision close-outs

- **D-IH-77-A** (charter): operationalised — drift gate exists, ships green, registered with release-gate.
- **D-IH-77-C** (Strand B posture — soft-30d-then-strict): operationalised — env-var override available, CLI `--strict` flag available, default soft mode active, 30-day window starts now.
- **D-IH-77-B** (Strand A scope): no P2 impact; already closed at P1.
- **D-IH-77-D** (I71 dependency): no P2 impact; already satisfied at P1.

No new decisions added in P2; the P0 charter fully anticipated the P2 scope.

### Cross-canonical link integrity

- Pydantic chassis follows `akos/brand_voice_register.py` precedent (I71 P1.4) — same `ConfigDict(frozen=True)` pattern, same parser-helper naming convention, same exclusion-list documentation pattern.
- Drift gate follows `scripts/validate_cicd_baseline.py` soft-30d-then-strict precedent (I68 P5 / D-IH-68-K).
- Release-gate wiring follows `run_brand_baseline_reality_validation()` pattern (I66 P2 / D-IH-66-M) — INFO-with-env-promotion-to-strict.
- Verification profile follows `brand_voice_register_smoke` shape (I71 P1 Pack A1).
- Test marker follows the registered `@pytest.mark.brand` marker (no new pytest marker registration needed; one-line addition to `pyproject.toml` would be required if a new marker were minted — not done here).

### CHANGELOG entry

Added under `## [Unreleased]` → `### Added`:

> **I77 P2 — Impeccable bridge generator + drift gate.** Pydantic chassis `akos/impeccable_bridge.py` (351 lines; `CanonicalCrossReference` / `BridgeFileSpec` / `BridgeCoverageReport` models + parsers + coverage computation). Drift gate `scripts/validate_impeccable_bridge_drift.py` (asserts each active brand canonical in CANONICAL_REGISTRY.csv is cross-referenced in ≥ 1 of PRODUCT.md / DESIGN.md / BASELINE_REALITY.md; soft-30d-then-strict per D-IH-77-C). Generator `scripts/generate_impeccable_bridges.py --check` for non-mutating coverage report (write mode reserved). 19 governance tests under `@pytest.mark.brand`. Release-gate registers IMPECCABLE bridge drift as INFO (flips to PASS/FAIL with `AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT=1`); new `impeccable_bridge_drift_smoke` verification profile.

## Pre-next-phase self-checkpoint (P3 — Operator UAT, Strand C)

### What I have read

- I77 master-roadmap §"Strand C — Operator UAT (P3)" (canonical scope at lines 59–73).
- `.cursor/skills/impeccable/SKILL.md` (full 331 lines) — understanding of `/critique` + `/polish` invocation flow, the 3-bridge consumption model (PRODUCT.md + DESIGN.md + BASELINE_REALITY.md), and IMPECCABLE_PREFLIGHT gate semantics.
- I71 P3 UAT report (for reference on prior brand-DNA UAT structure).

### What I have authored (P2 deliverables)

All files listed in §"Files modified or created" above.

### What is outstanding for P3

1. **Author P3 UAT runbook** at `docs/wip/planning/77-impeccable-brand-bridge-refresh/reports/p3-uat-impeccable-template-<date>.md` — operator-facing runbook with concrete invocation steps (which surface to invoke `/critique` on, what to expect from Impeccable now that 3 bridges cite 18 canonicals, how to verify Pack A1 voice validator runs clean on the rendered critique output).
2. **Run UAT** — operator-driven session. Suggested target surfaces: a Holistika sub-mark deck slide (Tier 1 R&S or Tier 2 HLK Tech Lab) where Impeccable can demonstrate brand-DNA awareness via the refreshed bridges. Self-test option: run `/critique` against `BASELINE_REALITY.md` itself (meta-check — does Impeccable understand its own consumption contract).
3. **Capture UAT evidence** per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT evidence contract" — dated `reports/uat-impeccable-<topic>-<YYYYMMDD>.md` with per-step PASS/SKIP/N/A results table.
4. **Close OPS-77-1** in `OPS_REGISTER.csv` once UAT lands.
5. **Decide on strict-mode auto-promotion** — at UAT closure, operator decides whether to flip the drift gate to strict-default at 2026-06-15 (no code change) or keep soft-mode default and require operator to set env var manually for strict runs.

### What I have decided NOT to do (out-of-scope deferrals)

- **`--write` mode for the generator** — DEFER to a future I-NN initiative. The chassis is ready; the only blocker is the fenced-regenerable-section pattern (need to ratify with operator which sections of the bridges are operator-authored prose vs auto-regenerable cross-link lists). Forward-charter clause in D-IH-77-C anticipates this.
- **Wider Impeccable test coverage** — DEFER. Smoke tests on script invocation are sufficient for P2; deeper integration tests (e.g., running Impeccable in a sandboxed cursor session and asserting it cites the refreshed bridges) are out-of-scope for this initiative.
- **Auto-promotion to strict at the 30-day boundary** — DEFER to P3 operator decision. Not auto-flipped to avoid surprise CI breakage when the soft window expires.
- **New brand canonicals added by future initiatives** — the drift gate already detects them. No P2 work needed; future canonical additions will land via their own initiative + this gate will WARN until they get cited in ≥ 1 bridge.

### First three concrete next actions for P3

1. Read I71 P3 UAT report shape (`docs/wip/planning/71-.../reports/p3-uat-pack-a1-*.md` if exists) to mirror the canonical UAT-runbook template.
2. Author `reports/p3-uat-impeccable-template-2026-05-16.md` with: prerequisite check (3 bridges + 19 tests + release-gate green; all done), operator invocation steps (cursor session invoking `/critique` against a chosen Holistika surface), expected outcomes (Impeccable cites refreshed bridges; rendered output passes `validate_brand_voice_register.py`), and per-step PASS/SKIP/N/A capture template.
3. Operator schedules a 30-minute UAT pocket (concurrent with I77 closure; can pair with the I77 CHANGELOG-final-entry sweep at P3-close).

## Operator approval checklist

Reviewer should validate before P3 entry:

1. **Chassis follows precedent** — `akos/impeccable_bridge.py` mirrors the `akos/brand_voice_register.py` shape (Pydantic v2 + ConfigDict(frozen=True) + field validators + parser helpers + exclusion-list comments).
2. **Drift gate ships green at 100% coverage** — 18/18 brand canonicals cited; no missing canonicals warning.
3. **Soft-30d-then-strict honored** — env var + CLI flag both work; default exits 0 on drift; strict mode exits 1 on drift.
4. **Generator write-mode reserved** — `--write` exits 2 with explicit "not yet implemented" message; no accidental file mutation possible.
5. **19 governance tests pass** — `py -m pytest tests/test_impeccable_bridge.py -v` clean in <2s.
6. **Release-gate OVERALL: PASS** — new IMPECCABLE row registered as INFO (not FAIL).
7. **New verification profile works standalone** — `py scripts/verify.py impeccable_bridge_drift_smoke` exits 0 with coverage report emitted.

## Cross-references

- [`master-roadmap.md`](../master-roadmap.md) §"Strand B — Generator + drift gate (P2)"
- [`decision-log.md`](../decision-log.md) §"D-IH-77-C — Strand B posture"
- [`p1-bridge-refresh-2026-05-16.md`](./p1-bridge-refresh-2026-05-16.md) — P1 phase report (this report's precondition)
- [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) — per-initiative file-changes CSV contract
- [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) — phase + commit discipline
- [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-HLK_TOOLING_STANDARDS_001.md) §3.7 — thin-redirect contract
- [`CONTRIBUTING.md`](../../../../CONTRIBUTING.md) §"Python Code Standards" — chassis quality bar
- Precedent: I71 P1 Pack A1 chassis ([`akos/brand_voice_register.py`](../../../../akos/brand_voice_register.py)) + I68 P5 strictness ladder ([`scripts/validate_cicd_baseline.py`](../../../../scripts/validate_cicd_baseline.py))
