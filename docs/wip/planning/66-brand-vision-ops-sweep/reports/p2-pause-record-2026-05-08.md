---
phase: P2
phase_name: Drift gates and rules
initiative: I66
date: 2026-05-08
status: complete
operator_pause: pre-P3
---

# I66 P2 — Drift gates and rules — pause record (2026-05-08)

## Summary

P2 ships **four mechanical drift gates** + **two new cursor rules** + **two updated cursor rules** that codify the canon harderning shipped in P1 (Branded House architecture, dual-register communication, internal/external register separation). All four gates are wired into `release-gate.py` with deterministic exit semantics; three of them (jargon, voice register, baseline reality) start in **soft-INFO** mode and flip to FAIL via opt-in environment flags or at I66 P5/P6 closure; the fourth (canon drift) is **strict-FAIL** from day one because it guards canon self-consistency that has no pre-P5 dependency.

The shipped artefacts are the operational face of P1's canon: where P1 declared what the brand is, P2 ensures the brand cannot drift. Subsequent phases (P3–P7) accrete on this base — every new SOP, every public surface rewrite, every deck or dossier built in P3-P6 will be governed by these gates.

## Phase 2 deliverables

### 1. Four drift gates (`scripts/validate_brand_*.py`)

| Validator | Strictness | Lines | What it asserts |
|:---|:---|:---:|:---|
| [`scripts/validate_brand_canon_drift.py`](../../../../../scripts/validate_brand_canon_drift.py) | **strict-FAIL** | ~270 | All 13 P0+P1 canonicals exist with `status: active`; BRAND_VISION.md carries ≥ 1 well-ordered `<!-- public-vision:start/end -->` marker pair; BRAND_BASELINE_REALITY_MATRIX.md §3 "External" column never contains internal-register tokens; BRAND_LOGO_SYSTEM.md cites BRAND_ARCHITECTURE.md + BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md; BRAND_HIERARCHY's frontmatter declares `supersedes:`. Soft upstream check (boilerplate brand-namespaced CSS variable) emits INFO-level findings only. |
| [`scripts/validate_brand_jargon.py`](../../../../../scripts/validate_brand_jargon.py) | **soft-INFO** until P5 (then strict via `AKOS_BRAND_JARGON_STRICT=1`) | ~290 | Forbidden tokens parsed at run time from BRAND_JARGON_AUDIT.md §4.1 (only first-of-bullet backticked tokens, with `CANONICAL_ALLOWLIST` so legitimate brand entities like "Holistika" / "HLK Tech Lab" are never flagged) + §4.2 (stack jargon); plus per-locale abbreviation-namespaced short-forms (MA/KB/EV/TB/TL/HRS — only fire in `messages/*.json`). Skips TS/JS import + comment lines (libraries-as-imports != prose). Skips `app/dashboard/**` + `app/(authapp)/**` legacy out-of-scope per D-IH-66-H. Graceful-skip when consumer repos absent. **Current real signal: 13 hits in 6 boilerplate files**, all legitimate pre-P5 signal (`OPS`, `plane`/`Control Plane`, `RBAC`/`RRF` in MADEIRA/Envoy/KiRBe manifesto pages + leaked OAuth credentials JSON). |
| [`scripts/validate_brand_voice_register.py`](../../../../../scripts/validate_brand_voice_register.py) | **soft-INFO** until P5 (then strict via `AKOS_BRAND_VOICE_REGISTER_STRICT=1`) | ~270 | Per-locale forbidden patterns parsed from BRAND_FRENCH_PATTERNS.md §5.1 (anglicism table, dynamic) + §5.2 (curated performative set) + BRAND_SPANISH_PATTERNS.md §13 (curated ES register rules: `humildemente`, `seríamos honrados`, `pricing`, `engagement`, `mindset`, etc.). Scans `messages/{en,es,fr}.json`; locale-aware (FR rules don't fire on ES files). |
| [`scripts/validate_brand_baseline_reality_drift.py`](../../../../../scripts/validate_brand_baseline_reality_drift.py) | **soft-INFO** until P6 (then strict via `AKOS_BRAND_BASELINE_REALITY_STRICT=1`) | ~250 | Internal-register tokens parsed from BRAND_BASELINE_REALITY_MATRIX.md §3 (with `DEFAULT_INTERNAL_TOKENS` fallback so the validator never silently weakens). Scans `_assets/advops/**/deck/*.yaml`, `dossier_*.md`, `deck_slides.yaml` + sibling `boilerplate/{app,components,messages}/`. **Exempts** `*.objections.md` and `*.counterparty-brief.md` companions — these are the explicit homes of internal vocabulary. |

**Common contract** across all four:

- Token lists are **parsed from canon at run time** — no hard-coded duplicates that drift from canon.
- All four return exit `0` on PASS, `1` on FAIL.
- All consumer-repo scans use `--strict-empty` toggle (default = graceful skip).
- All four are wired into `release-gate.py` with explicit strictness annotation in the verdict line.

### 2. Tests (`tests/test_validate_brand_drift_gates.py`)

27 tests covering all four validators:

- **Canon drift** (6 tests): required-canonicals presence + active-status, vision-marker order, dual-register external-column cleanliness, logo-system cross-refs, hierarchy-supersedes, full main() pass.
- **Brand jargon** (8 tests): canonical token extraction, HLK-paired-form negative-lookahead behaviour, abbreviation locale-only firing, import-line skip, dashboard-legacy-path exclusion, prose tokens still caught, strict-empty failure semantics, graceful-skip semantics.
- **Voice register** (7 tests): FR anglicism extraction, ES register rule presence, FR message file with anglicism flagged, FR clean message file no hits, ES performative humility flagged, EN locale no rules, main graceful-skip on empty.
- **Baseline reality** (6 tests): internal-token extraction (with fallback), companion-file exemption, counterparty-brief exemption, dossier file flags internal tokens, skip-consumer mode passes, default run passes against clean repo.

All 27 PASS. Combined with re-run of `validate_subdomains_registry` (7 tests), full drift-gate test suite is 34 PASS / 0 FAIL.

### 3. Two new cursor rules (`.cursor/rules/`)

- **[`akos-agent-checkpoint-discipline.mdc`](../../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc)** (D-IH-66-Q): Codifies the operator-pause-point + agent-self-checkpoint discipline that enables I66 (and any future ≥ 5-week initiative) to operate auditably across many phases. Defines pause-record schema, self-checkpoint schema, depth heuristics (1 pause per phase for ≥ 5-week work, mandatory pauses at canonical-CSV gates / trademark filings / public-prose publish), and pause-fatigue mitigations (front-loaded review at P0+P1, skimmable record format, batched approvals, soft auto-clear after 24h silence + clean validators).
- **[`akos-brand-baseline-reality.mdc`](../../../../../.cursor/rules/akos-brand-baseline-reality.mdc)** (D-IH-66-M): Codifies the dual-register contract. Specifies allowed-context table (8 surfaces where internal register OK) vs forbidden-context table (10 surfaces where external register only). Embeds the §3 translation table (counterparty → client / advisor / regulator; elicitation → structured discovery; intelligence collection → research; etc.). Documents the drift gate's behaviour and self-discipline rules for agents authoring prose.

### 4. Two updated cursor rules (`.cursor/rules/`)

- **[`akos-docs-config-sync.mdc`](../../../../../.cursor/rules/akos-docs-config-sync.mdc)**: Added 9 new rows in §"HLK compliance changes" mapping every new I66 P0+P1 brand canonical to its downstream sync surfaces (BRAND_ARCHITECTURE.md → boilerplate entities-section, USER_GUIDE, ARCHITECTURE; BRAND_VISION.md → P5 rewrite of `/manifiesto/holistika`; BRAND_BASELINE_REALITY_MATRIX.md → cursor rule + drift gate + per-repo BASELINE_REALITY.md bridges; BRAND_LOGO_SYSTEM.md → `boilerplate/public/holistika-*.svg`; BRAND_ABBREVIATIONS.md → jargon validator + JARGON_AUDIT cross-refs; BRAND_FRENCH_PATTERNS.md, BRAND_SPANISH_PATTERNS.md → voice-register validator + per-locale messages files; BRAND_HIERARCHY → operator-facing legal-posture surfaces). Added 2 new rows in §"Cursor rules" for the two new I66 rules.
- **[`akos-planning-traceability.mdc`](../../../../../.cursor/rules/akos-planning-traceability.mdc)**: Added new §"Long-running initiatives: pause-point + self-checkpoint discipline" cross-referencing the new `akos-agent-checkpoint-discipline.mdc` for ≥ 5-phase / ≥ 1-week / ≥ 5-week initiatives. Self-sufficient summary for shorter initiatives (no cross-rule jump required when the initiative is small).

## Mechanical evidence (P2)

### Files created (10)

| Path | Lines | Purpose |
|:---|---:|:---|
| `scripts/validate_brand_canon_drift.py` | ~270 | Drift gate #1 — canon self-consistency |
| `scripts/validate_brand_jargon.py` | ~290 | Drift gate #2 — public-DOM forbidden tokens |
| `scripts/validate_brand_voice_register.py` | ~270 | Drift gate #3 — per-locale voice register |
| `scripts/validate_brand_baseline_reality_drift.py` | ~250 | Drift gate #4 — dual-register contract |
| `tests/test_validate_brand_drift_gates.py` | ~250 | 27 tests across all 4 gates |
| `.cursor/rules/akos-agent-checkpoint-discipline.mdc` | ~110 | Pause-point + self-checkpoint discipline (D-IH-66-Q) |
| `.cursor/rules/akos-brand-baseline-reality.mdc` | ~95 | Dual-register contract (D-IH-66-M) |
| `docs/wip/planning/66-brand-vision-ops-sweep/reports/p2-pause-record-2026-05-08.md` | this file | P2 pause record |

### Files modified (3)

| Path | Changes |
|:---|:---|
| `scripts/release-gate.py` | +4 runner functions; +4 result-table entries with strict-via-env opt-in; ~80 LOC added |
| `.cursor/rules/akos-docs-config-sync.mdc` | +9 rows (new I66 brand canonicals → downstream sync); +2 rows (new I66 cursor rules) |
| `.cursor/rules/akos-planning-traceability.mdc` | +1 new section "Long-running initiatives: pause-point + self-checkpoint discipline"; ~14 LOC added |

### Validators (P2 self-verification)

| Command | Verdict | Notes |
|:---|:---|:---|
| `py scripts/validate_brand_canon_drift.py` | **PASS** | 13 canonicals present + dual-register contract clean; boilerplate brand-namespaced CSS variable present in `globals.css`, `tailwind.config.ts` |
| `py scripts/validate_brand_jargon.py` | **FAIL** (13 hits, soft-INFO) | All 13 are legitimate P5-cleanup signal: `OPS` lowercase parenthetical (1), `Control Plane` × 5 in MADEIRA/Envoy manifestos, `RBAC`/`RRF` × 4 in KiRBe + manifiesto data, `OAuth2` × 3 in leaked Google service-account credentials JSON (separately concerning). |
| `py scripts/validate_brand_voice_register.py` | **PASS** | 0 message file hits across 2 consumer repos. |
| `py scripts/validate_brand_baseline_reality_drift.py` | **PASS** | Dual-register contract holds; 7 internal tokens checked. |
| `py -m pytest tests/test_validate_brand_drift_gates.py -v` | **PASS** (27/27) | All four gates exercised by tmpdir fixtures + real-canon checks. |
| `py scripts/validate_hlk.py` | **PASS** | Pre-existing canon validators unaffected. |
| `py scripts/validate_initiative_registry.py` | **PASS** | Pre-existing initiative validator unaffected. |
| `ReadLints` on all 6 modified Python files | **PASS** | 0 linter errors. |

### Git status (pre-commit)

10 new files + 3 modified files = ~1700 LOC of governed Python + Markdown. No incidental changes.

## Documentary evidence (P2)

### Decisions encoded in P2

| Decision ID | Encoded in | Status |
|:---|:---|:---|
| **D-IH-66-J** (drift gates wired into release-gate as INFO until P5/P6, opt-in strict via env flags) | `scripts/release-gate.py` lines 297-318 | **encoded** |
| **D-IH-66-K** (token lists parsed from canon at run time; no hard-coded duplicates) | All 4 validator parsers | **encoded** |
| **D-IH-66-L** (validators graceful-skip when consumer repos absent; `--strict-empty` opt-in) | `validate_brand_jargon.py`, `validate_brand_voice_register.py` | **encoded** |
| **D-IH-66-M** (dual-register contract; internal vs external register asymmetric) | `BRAND_BASELINE_REALITY_MATRIX.md` (P1) + `validate_brand_baseline_reality_drift.py` (P2) + `akos-brand-baseline-reality.mdc` (P2) | **encoded across all 3 surfaces** |
| **D-IH-66-N** (companion-file exemption for `.objections.md` + `.counterparty-brief.md`) | `validate_brand_baseline_reality_drift.py` `EXEMPT_FILE_SUFFIXES` | **encoded** |
| **D-IH-66-Q** (operator pause-point + agent self-checkpoint discipline as cursor rule) | `akos-agent-checkpoint-discipline.mdc` | **encoded** |

Other I66 decisions (D-IH-66-A through D-IH-66-Z) are tracked in the I66 `decision-log.md` (deferred to P0 / P1 records). P3 will close the remaining ones.

### Cross-references

The P2 deliverables form a tight closure with P0+P1:

- **P0** (Impeccable v3.1, BASELINE_REALITY.md gate) → **P1** (BRAND_BASELINE_REALITY_MATRIX.md as canon SSOT) → **P2** (drift gate `validate_brand_baseline_reality_drift.py` + cursor rule `akos-brand-baseline-reality.mdc`).
- **P1** (BRAND_JARGON_AUDIT.md §4 expanded with HUMINT register tokens, BRAND_ABBREVIATIONS.md created) → **P2** (drift gate `validate_brand_jargon.py` parses §4 + abbreviations registry at run time).
- **P1** (BRAND_FRENCH_PATTERNS.md promoted to active, BRAND_SPANISH_PATTERNS.md expanded with §13 boilerplate-ES alignment) → **P2** (drift gate `validate_brand_voice_register.py` parses both at run time).
- **P1** (13 brand canonicals + status frontmatter) → **P2** (drift gate `validate_brand_canon_drift.py` asserts presence + status + cross-refs).

## Pre-P3 self-checkpoint

### What I have read

- All 6 P1 canonicals (BRAND_ARCHITECTURE.md, BRAND_VISION.md, BRAND_BASELINE_REALITY_MATRIX.md, BRAND_LOGO_SYSTEM.md, BRAND_ABBREVIATIONS.md, BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) and verified parser outputs against them.
- `scripts/validate_subdomains_registry.py` (pattern reference for new validators).
- `scripts/release-gate.py` full file (wiring pattern).
- `scripts/validate_hlk.py` first 80 lines (dispatcher graph awareness for future P3 validator additions).
- All 7 existing `.cursor/rules/akos-*.mdc` files (rule format + scope conventions).

### What I have authored (P0 + P1 + P2 cumulative)

- **P0**: 8 governance files in I66 planning folder + Impeccable v3.1 upgrade + INITIATIVE_REGISTRY row + planning README row + 5 carry-over commits in `hlk-erp/` and `boilerplate/` for the Impeccable bridge files.
- **P1**: 5 new + 2 rewritten + 4 cross-referenced BRAND canonicals + `docs/_assets/transcripts/` working space.
- **P2**: 4 drift validators + 27 tests + 2 new cursor rules + 2 updated cursor rules + release-gate wiring.

### What is outstanding for P3

P3 (5-6d) — Ops, process, organization, catalog, SOPs:

1. **16 process_list.csv rows** — operator-approved canonical-CSV gate. Tranche structure to draft.
2. **3 sub-mark Lead rows** in `baseline_organisation.csv` — same operator gate, same tranche.
3. **`SERVICE_OFFERING_CATALOG.md` canonical** under `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/` — the 6×3 service matrix referenced by P5's `/services` rewrite.
4. **11 new SOPs**, including the 4 HUMINT-derived ones (counterparty baseline assessment, elicitation discipline, reliability grading, intelligence report) — under a new `docs/references/hlk/v3.0/Admin/O5-1/Operations/IntelligenceOps/` folder structure.
5. **`docs/wip/intelligence/`** working space scaffold (already cited by `akos-brand-baseline-reality.mdc` allowed-contexts table).
6. **SOP-META cross-refs** — every new SOP must register against `process_list.csv` rows per `SOP-META_PROCESS_MGMT_001.md` §4.2-4.3 ordering (CSV before SOP).

### What I have decided not to do (out-of-scope for P2)

- **OPS / plane / Control Plane prose-token cleanup in boilerplate** — DEFERRED to P5 (boilerplate rewrite). The validator surfacing them in soft-INFO mode is the correct P2 deliverable.
- **Leaked Google service-account credentials JSON** (`hlk-gtm-0001-365101c1624d.json`) — flagged for operator awareness but **not in I66 scope**. Should be revoked + scrubbed via separate security action; the validator caught it as a side-effect of OAuth2 token matching, but the security concern is a separate issue.
- **`validate_pause_records.py`** (mechanical pause-record schema validation) — explicitly out of scope per `akos-agent-checkpoint-discipline.mdc` §"Drift gate / enforcement". Future I-NN may codify.

### First three concrete next actions for P3

1. **Read** `docs/references/hlk/compliance/process_list.csv` header + a representative ~10-row sample to understand the schema before drafting 16 new rows.
2. **Read** `docs/references/hlk/compliance/baseline_organisation.csv` for the 3 sub-mark Lead row format.
3. **Draft** the SOP-META-compliant **CSV tranche** for the 16 new process_list rows + 3 baseline rows + present to operator as the **canonical-CSV gate** (mandatory pause point per `akos-agent-checkpoint-discipline.mdc` and `akos-governance-remediation.mdc`).

## Operator approval checklist (pre-P3 entry)

Operator must validate before P3 begins:

1. ☐ All four drift gates run cleanly in their declared modes (canon strict-PASS; jargon/voice/baseline soft-INFO with documented signal).
2. ☐ The 13-hit jargon signal in boilerplate is acknowledged as expected pre-P5 cleanup; operator is aware the leaked Google credentials JSON warrants a separate security action.
3. ☐ The two new cursor rules (`akos-agent-checkpoint-discipline.mdc`, `akos-brand-baseline-reality.mdc`) read correctly and the operator is comfortable with their scope.
4. ☐ The two updated cursor rules (`akos-docs-config-sync.mdc`, `akos-planning-traceability.mdc`) preserve existing semantics + only additively reference new I66 surfaces.
5. ☐ Release-gate's strict-via-env flag pattern (`AKOS_BRAND_*_STRICT=1`) is the right escape hatch for the operator to flip gates to FAIL when P5/P6 close.
6. ☐ The P3 entry is approved (16 new `process_list.csv` rows + 3 new `baseline_organisation.csv` rows + 11 new SOPs is a substantial canonical-CSV gate; explicit go-ahead acknowledged).
7. ☐ The IntelligenceOps SOP folder location (`docs/references/hlk/v3.0/Admin/O5-1/Operations/IntelligenceOps/`) is acceptable as the new canonical home for HUMINT-derived SOPs.

## Cross-references

- I66 master-roadmap: `docs/wip/planning/66-brand-vision-ops-sweep/master-roadmap.md` §"P2 — Drift gates and rules"
- P0 pause record: [`p0-pause-record-2026-05-08.md`](p0-pause-record-2026-05-08.md)
- P1 pause record: [`p1-pause-record-2026-05-08.md`](p1-pause-record-2026-05-08.md)
- Pre-P1 self-checkpoint: [`checkpoints/sc-pre-p1-2026-05-08.md`](checkpoints/sc-pre-p1-2026-05-08.md)
- Decision log: `docs/wip/planning/66-brand-vision-ops-sweep/decision-log.md` (D-IH-66-J through D-IH-66-Q encoded across P0+P1+P2 surfaces)
