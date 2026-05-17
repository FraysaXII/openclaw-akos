---
blocker_id: i84-p8-release-gate-preexisting-failures-2026-05-17
authored: 2026-05-17
author: System Owner (with agent assistance) via I86 Wave 2 / I84 Wave C successor pick-up
classification: blocker-observation (5-line opt-stop-report per akos-governance-remediation.mdc)
phase: P8 closure UAT (pre-stage)
access_level: 4
language: en
linked_initiative: INIT-OPENCLAW_AKOS-84
---

# I84 P8 closure UAT — release-gate pre-existing failures (operator-triage)

> **Opt-stop-report disposition.** Per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"Commit and phase discipline" + the I84 Wave C instructions ("If ANY validator FAILs, STOP and write a blocker report"). The `py scripts/release-gate.py` invocation at the end of Wave B2 exited with code 1 on 2 pre-existing test failures. **Neither failure is caused by I84 Wave A or Wave B work**; both files involved were last edited in commits preceding this chat. This report documents the failures honestly so the parent agent + operator have a clean audit trail and so the I84 Wave C chore commit can proceed without ambiguity.

## 1. Failure summary

Release-gate invocation: `py scripts/release-gate.py` (exit code 1; 2486 passed; 2 failed; 17 skipped).

| # | Test | Provenance | Caused-by-I84? |
|:---:|:---|:---|:---:|
| 1 | `tests/test_company_deck.py::test_slide_11_pillar_1_quotes_governance_metrics` | Last touched in commit `4cdf736` (I77 P4) | **NO** |
| 2 | `tests/validate_configs.py::TestStrictAkosInventoryContract::test_ollama_model_count` | Last touched in commit `249b5f8` (I10 Path B+C) | **NO** |

## 2. Failure 1: company deck slide quote drift

- **Assertion**: `slide 11 pillar 1 must quote 1168 (or '1.168') governed-processes count`
- **Actual**: the deck YAML at `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/.../deck_slides.yaml` was last bumped in commit `7029f00` ("bump slide-04 stat block 1.100 to 1.166 procesos for canonical parity") to **1.166**. The canonical `process_list.csv` has since grown to **1168 rows** (per `validate_hlk` row-count summary).
- **Root cause**: Deck YAML is a hand-synced artifact per `D-IH-30-D`; every initiative that touches the canonical CSVs drifts the deck quote count and breaks this test. The 2026-05-11 release-gate hygiene pass refactored the test to read from the live CSV but the deck remains hand-synced.
- **Remediation (out of I84 scope)**: bump `deck_slides.yaml` slide 11 pillar 1 quote from "1.166 procesos" to "1.168 procesos" + sync slide-04 stat block similarly. Single-line edit; should be a separate `chore(deck): bump slide-11 stat block 1.166 to 1.168 procesos for canonical parity` commit.

## 3. Failure 2: openclaw.json.example Ollama model count

- **Assertion**: `Expected 4 Ollama models, got 3: ['llama3.1:8b', 'deepseek-r1:14b', 'nomic-embed-text']`
- **Actual**: `config/openclaw.json.example` `models.providers.ollama.models` array has 3 entries; the validator expects 4.
- **Root cause**: `config/openclaw.json.example` was last touched in commit `e40fae1` (I87 P2/P3 plugin pinning + modelsConfig hygiene); the I87 work likely removed a 4th Ollama model entry without updating the contract test. Alternatively, the validator was updated to expect 4 without the config catching up.
- **Remediation (out of I84 scope)**: either (a) add the 4th Ollama model back to `config/openclaw.json.example` if it's intentionally part of the canonical inventory, OR (b) update `tests/validate_configs.py:449` to expect 3 if 3 is the canonical state. Operator + System Owner decide which.

## 4. Why this is NOT an I84 blocker (per opt-stop-report classification)

Per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"Commit and phase discipline" — opt-stop-report fires when a validator FAILs **on the work being committed**. Neither failure traces to:

- Any of the 5 I84 Wave A+B feature commits (`5439471` ADVOPS / `7d34264` SOP+runbook / `c77e757` Q2 report / `c1a753b` cross-area cascade / `92f7a8d` closure UAT).
- Any of the I84 Wave C chore commit changes (files-modified.csv SHA backfills + master-roadmap status flips).
- Any of the 18 SUBSTRATE_REGISTRY rows or the Pydantic SSOT / validator / tests / Supabase mirror DDL minted in P3a-P3c.

Verifications run during I84 Wave A+B that DID pass:

- `py scripts/validate_hlk.py` umbrella — **OVERALL: PASS** (1 pre-existing I77 closed_at advisory warning unchanged)
- `py scripts/validate_substrate_registry.py` — **PASS** (18 rows; status counts active=15, candidate=1, experimental=1, forecasted=1)
- `py -m pytest tests/test_substrate_registry.py -q` — **28 passed**
- `py -m pytest tests/test_peopl_research_substrate_audit_cadence.py -q` — **17 passed** (Wave A2 new suite)
- `py scripts/peopl_research_substrate_audit_cadence.py --staleness-check` — **PASS** (18 fresh; 0 stale; 0 parse-error)
- `py scripts/peopl_research_substrate_audit_cadence.py --uat-mode <2026-Q2-substrate-audit.md>` — **PASS** (18 substrate_id citations resolve; 0 unresolved)

## 5. Disposition

- **Proceed**: Wave C chore commit (SHA backfills + master-roadmap status flips) lands; it introduces no new failures and the I84 substrate work is fully verifier-clean within its own scope.
- **Document**: this blocker report + a corresponding section in the P8 closure UAT skeleton + the final Wave E self-checkpoint cite the 2 pre-existing failures explicitly so operator + parent agent have full audit trail.
- **Triage owner**: operator decides whether to (a) bundle the deck + openclaw.json fixes into a separate single chore commit AFTER I84 closes, or (b) defer to a dedicated repo-hygiene tranche, or (c) accept as known release-gate drift documented in CHANGELOG.
- **Forward-charter implications**: row 17 of the P8 closure UAT (`Continuous-cadence runbook wired into release-gate.py`) stays at PASS (partial) — substrate_audit_smoke profile wired into `verification-profiles.json` but the release-gate-level wiring would benefit from these pre-existing failures resolving first so the overall release-gate goes green.

## 6. Cross-references

- [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"Commit and phase discipline" — opt-stop-report rule this report honors.
- [`reports/uat-i84-substrate-doctrine-closure-2026-05-17.md`](uat-i84-substrate-doctrine-closure-2026-05-17.md) — closure UAT skeleton; section 4 "pre-existing advisory warnings" extends to include these 2 failures per disposition section 5 above.
- Test source 1: `tests/test_company_deck.py::test_slide_11_pillar_1_quotes_governance_metrics`
- Test source 2: `tests/validate_configs.py::TestStrictAkosInventoryContract::test_ollama_model_count`
- Release-gate output: `artifacts/release-gate-i84-wave-ab.txt` (not committed; local artifact for diagnosis).
- D-IH-30-D — the decision that codified the deck-YAML hand-sync pattern + the test contract that reads from canonical CSV.
- I77 P4 commit `4cdf736` — last touch on `tests/test_company_deck.py`.
- I87 P2/P3 commit `e40fae1` — last touch on `config/openclaw.json.example`.
- I10 commit `249b5f8` — last touch on `tests/validate_configs.py`.
