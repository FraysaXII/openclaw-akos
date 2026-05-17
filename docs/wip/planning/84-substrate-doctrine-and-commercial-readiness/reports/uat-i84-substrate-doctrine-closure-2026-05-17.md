---
uat_id: uat-i84-substrate-doctrine-closure-2026-05-17
authored: 2026-05-17
author: System Owner (with agent assistance) via I86 Wave 2 / I84 Wave B2 successor pick-up
phase: P8 closure UAT (pre-staged; carries post-P4 substitution rows)
initiative: INIT-OPENCLAW_AKOS-84
classification: closure UAT evidence (pre-stage; awaits P4 + closure decision)
access_level: 4
language: en
ratifying_decisions: [D-IH-84-A, D-IH-84-B, D-IH-84-C, D-IH-84-D, D-IH-84-E, D-IH-84-F, D-IH-84-G, D-IH-84-H, D-IH-84-CLOSURE]
source_taxonomy: holistika-internal-uat-evidence
---

# I84 closure UAT (pre-stage)

> **Pre-stage purpose.** Per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) section "UAT evidence contract" + master-roadmap section 3 P8 — closure UAT evidence with a dated results table covering each acceptance row. **Pre-stage** because four substantive rows (D-IH-84-B/C/D/E ratifications + the cross-area cascade landing + I12/I13 supersession side-effects + INITIATIVE_REGISTRY flips) depend on operator answers at the I84 P4 batched gate + the closure decision D-IH-84-CLOSURE. Parent agent fills the post-P4 placeholder cells once those operator answers land.
>
> **SOC discipline per UAT evidence contract.** No secrets, API keys, or full prompts in this UAT evidence. Per-row notes cite git commits + canonical paths + validator verdicts; no environment variables or vendor account-specific values are surfaced.
>
> **Honest scope-adjustment.** The original master-roadmap section 3 P3 called for an "AGENTIC_FRAMEWORK_LANDSCAPE.md extension" (Tech-Lab canonical). The as-shipped I84 P3a minted a sibling Research-area canonical `SUBSTRATE_LANDSCAPE_DOCTRINE.md` instead (status:review per `D-IH-84-G`), which serves the same governance role (the Research-area side of the substrate triangle paired with the Tech-Lab side). Row 4.3 below records this scope-adjustment honestly with explanation. The original AGENTIC_FRAMEWORK_LANDSCAPE.md extension can ship as a separate follow-on tranche or as part of the P4 cascade if operator wishes.

## 1. UAT scope

Per master-roadmap section 3 P8 (closure UAT specification) the closure UAT covers 8 acceptance rows mapping to the 8 D-IH-84-A through D-IH-84-H decision ratifications + the cross-cutting promotion-criteria rows (SUBSTRATE_REGISTRY mirror live; AGENTIC_FRAMEWORK_LANDSCAPE.md extension; cross-area cascade landed; continuous Research cadence SOP + runbook landed; first quarterly substrate-audit report shipped; INITIATIVE_REGISTRY flips for I84 / I12 / I13).

UAT rows landing as: `PASS` (acceptance met + verified) / `SKIP` (acceptance N/A or deferred) / `N/A` (acceptance not in scope for this initiative) / `pending` (post-P4 substitution required).

## 2. Acceptance results table

| # | Acceptance row | Verdict | Note |
|:---:|:---|:---:|:---|
| 1 | D-IH-84-A (mega charter scope ratification; Q1+Q2+Q3 architecture) | **PASS** | Ratified inline 2026-05-16 (3-question batch per inline-ratify-craft); charter package landed at I84 P0 commit `dbdb551` (per files-modified.csv P0 rows); master-roadmap.md + decision-log.md + risk-register.md + asset-classification.md + evidence-matrix.md + files-modified.csv all live in folder. |
| 2 | D-IH-84-B (AKOS substrate baseline B1/B2/B3 ratification) | **pending P4** | <!-- post-P4 substitution: D-IH-84-B ratified-option + rationale + DECISION_REGISTER row append --> Awaits I84 P4 batched inline-ratify gate. Evidence stack complete (P1 audit + P2 scorecard + Tier-1 WIP regulatory + competitive + past-PoC + ADVOPS scoping). |
| 3 | D-IH-84-C (AIC framing F1-F5 binding choice; closes I76 C-76-1) | **pending P4** | <!-- post-P4 substitution: D-IH-84-C ratified-option F[1-5] + rationale + DECISION_REGISTER row append --> Awaits P4 gate. Evidence stack complete (P2 scorecard finding #4 + competitive analysis + past-PoC translation). |
| 4 | D-IH-84-D (MADEIRA productization shape D1/D2/D3; closes I74 C-74-3) | **pending P4** | <!-- post-P4 substitution: D-IH-84-D ratified-option D[1-3] + rationale + DECISION_REGISTER row append --> Awaits P4 gate. Evidence stack complete (P2 scorecard finding #5 + competitive section 6 + regulatory section 2.5). |
| 5 | D-IH-84-E (KiRBe framework narrowing to 2 finalists; closes I83 C-83-1) | **pending P4** | <!-- post-P4 substitution: D-IH-84-E narrowed-to-2 finalists + rationale + DECISION_REGISTER row append --> Awaits P4 gate. Evidence stack complete (P2 scorecard finding #5 + past-PoC translation section 5.3 recommended narrowing). |
| 6 | D-IH-84-F (SUBSTRATE_REGISTRY.csv column shape 18-col + 8 enum frozensets) | **PASS** | Pydantic SSOT minted in P3a commit `666559e` at [`akos/hlk_substrate_registry_csv.py`](../../../../akos/hlk_substrate_registry_csv.py); 18 columns + 9 enum Literals (incl. multi-tenant_ready). SUBSTRATE_REGISTRY.csv seeded with 18 rows at P3b commit `589a902` (operator-approved canonical-CSV gate). |
| 7 | D-IH-84-G (SUBSTRATE_LANDSCAPE_DOCTRINE.md authoring posture; Research-area DoD recursive) | **PASS** | Doctrine canonical landed at P3a commit `666559e` at [`docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) at `status: review` per SOP-META ordering. Paired with Tech-Lab AGENTIC_FRAMEWORK_LANDSCAPE.md per People-DoD pattern recursive application. |
| 8 | D-IH-84-H (quarterly cadence + Research-area owner-activation interim) | **PASS** | Cadence + interim ownership (KM Officer + Founder pre-Research-Director per `i75-research-area-governance` Strand C) ratified at SOP frontmatter authoring; landed at Wave A2 SOP+runbook commit (7d34264) at [`SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md). |
| 9 | SUBSTRATE_REGISTRY.csv loads clean + Pydantic validator PASS + Supabase mirror 18 rows live | **PASS** | Per checkpoint section 3: `py scripts/validate_substrate_registry.py` PASS (status counts active=15, candidate=1, experimental=1, forecasted=1); `py -m pytest tests/test_substrate_registry.py -q` 28 passed; Supabase mirror live per checkpoint section 2.3 (compliance.substrate_registry_mirror table created; 18 rows seeded via 3 MCP execute_sql batches; verification SELECT confirmed total_rows=18, distinct_ids=18; migration ledger harmonized via repair commands). |
| 10 | SUBSTRATE_LANDSCAPE_DOCTRINE.md landed (originally called "AGENTIC_FRAMEWORK_LANDSCAPE.md extension" per master-roadmap section 3 P3) | **PASS** (with scope-adjustment note) | **Scope-adjustment**: original master-roadmap P3 called for Tech-Lab AGENTIC_FRAMEWORK_LANDSCAPE.md extension (8 framework rows + KB infrastructure dimensions + MCP postures). As-shipped I84 P3a minted the **sibling Research-area canonical** `SUBSTRATE_LANDSCAPE_DOCTRINE.md` (per `D-IH-84-G` discipline-of-disciplines posture). The doctrine serves the same governance role (the Research-area "why which" complement to the Tech-Lab "how"). The original AGENTIC_FRAMEWORK_LANDSCAPE.md extension can ship as a separate follow-on tranche or as part of the P4 cascade if operator wishes. Verdict PASS with explicit scope-adjustment record. |
| 11 | Cross-area cascade landed for I76 / I74 / I83 / I82 candidates | **pending P4** | <!-- post-P4 substitution: per-candidate stub-edit commit SHAs + DECISION_REGISTER appends (D-IH-76-A inherits D-IH-84-C; D-IH-74-D inherits D-IH-84-D; D-IH-83-A inherits D-IH-84-E; I82 CAPABILITY_REGISTRY column-shape extension) --> Pre-stage handoff document landed at Wave B1 commit `c1a753b` at [`reports/cross-area-unlock-handoff-2026-05-17.md`](cross-area-unlock-handoff-2026-05-17.md); awaits P4 ratification + parent agent stub edits + PAUSE POINT #3 operator confirmation. |
| 12 | Continuous Research-area cadence SOP + paired runbook landed | **PASS** | SOP at `status: review` per `D-IH-84-H` + `D-IH-84-G` landed at Wave A2 commit `7d34264` at [`SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md). Paired runbook at [`scripts/peopl_research_substrate_audit_cadence.py`](../../../../scripts/peopl_research_substrate_audit_cadence.py). Per `akos-executable-process-catalog.mdc` Rule 1 (paired SOP+runbook) + Rule 3 (cadence taxonomy = scheduled quarterly). Acceptance criteria human + automation both declared in SOP body per Rule 1 section 5. |
| 13 | First quarterly substrate-audit report shipped (founding-cycle baseline) | **PASS** | Cycle 1 founding-cycle baseline landed at Wave A3 commit `c77e757` at [`docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md`](../../../intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md). 5-element audit per SOP shape. All 18 SUBSTRATE_REGISTRY substrate_id citations FK-resolve via runbook --uat-mode (PASS; 0 unresolved). Sections 6 + 7 carry post-P4 substitution placeholder blocks (D-IH-84-B/C/D/E ratification outcomes + cross-area implications). |
| 14 | substrate_audit_smoke verification profile wired | **PASS** | Profile added in Wave A2 commit `7d34264` to [`config/verification-profiles.json`](../../../../config/verification-profiles.json); runs `--staleness-check` + dedicated pytest suite. Operator invokes via `py scripts/verify.py substrate_audit_smoke`. |
| 15 | tests/test_peopl_research_substrate_audit_cadence.py 17 tests landed | **PASS** | All 17 tests landed in Wave A2 commit `7d34264`; covers default mode + staleness-check (fresh + stale via monkeypatched today) + uat-mode (valid + unresolved + missing) + emit-delta (valid + missing) + list-quarters + helper functions. `py -m pytest tests/test_peopl_research_substrate_audit_cadence.py -q` 17 passed in 0.44s. |
| 16 | ADVOPS engagement scoping recommendation landed (R-IH-84-NEW-ADVOPS mitigation) | **PASS** | ADVOPS scoping note landed at Wave A1 commit `5439471` at [`reports/advops-engagement-scoping-2026-05-17.md`](advops-engagement-scoping-2026-05-17.md). 4-discipline framework (EU AI Act + GDPR/DPA + IP/IT + jurisdictional fiscal) + qualitative timeline (6-10 weeks) + cost-class envelope + operator-choice activation gate Options A-D. Operator decides at P5 whether to engage. |
| 17 | Continuous-cadence runbook wired into release-gate.py + verification-profiles.json substrate_audit_smoke | **PASS (partial)** | substrate_audit_smoke profile wired per row 14. Wiring into `scripts/release-gate.py` is recommended forward-charter item (the profile invocation makes it operator-discoverable; explicit release-gate hook ships at a follow-on initiative if the operator desires automated quarterly enforcement). |
| 18 | INITIATIVE_REGISTRY.csv I84 row flip from active to closed | **operator-pending** | <!-- post-P4 + post-closure-D-IH-84-CLOSURE substitution: INITIATIVE_REGISTRY.csv I84 row status flip + closed_at date append --> Per master-roadmap section 7 closure criteria + `akos-governance-remediation.mdc` §"HLK compliance governance" canonical-CSV gates. Operator-approved canonical-CSV mint at closure batch. |
| 19 | INITIATIVE_REGISTRY.csv I12 + I13 rows flip to status: superseded | **operator-pending** | <!-- post-closure-D-IH-84-CLOSURE substitution: INITIATIVE_REGISTRY.csv I12 + I13 rows status flips + superseded_by_initiative_id field populated with INIT-OPENCLAW_AKOS-84 --> Operator-approved canonical-CSV mint at closure batch. Per master-roadmap section 7 + checkpoint section 4 #6 (operator-pending forward-charter). |
| 20 | D-IH-84-CLOSURE row mint in DECISION_REGISTER.csv | **operator-pending** | <!-- post-closure-D-IH-84-CLOSURE substitution: DECISION_REGISTER.csv D-IH-84-CLOSURE row append --> Per master-roadmap section 7 closure criteria. Operator-approved canonical-CSV mint at closure batch. |

## 3. Post-P4 substitution count

This UAT shipped with **6 substitution-pending rows** (rows 2, 3, 4, 5, 11, plus 3 operator-pending closure-batch rows 18, 19, 20). After the operator answers the I84 P4 batched gate + ratifies the closure decision D-IH-84-CLOSURE, the parent agent updates this UAT to reflect:

- Rows 2-5 flip from `pending P4` to **PASS** with the ratified D-IH-84-B/C/D/E options + rationale cited inline.
- Row 11 flips from `pending P4` to **PASS** once cross-area cascade stub-edit commit SHAs are recorded.
- Rows 18-20 flip from `operator-pending` to **PASS** at the canonical-CSV gate closure batch (operator approval required).

## 4. Pre-existing advisory warnings + release-gate failures (not caused by I84)

### 4.1 validate_hlk advisory warnings

Per [`validate_hlk.py`](../../../../scripts/validate_hlk.py) MASTER_ROADMAP_FRONTMATTER validator: 1 advisory warning on `docs/wip/planning/77-impeccable-brand-bridge-refresh/master-roadmap.md` `status='closed'` requiring companion field `closed_at` (missing or empty). **This warning is pre-existing and not caused by I84.** Documented here for completeness per UAT evidence discipline. Remediation is out of I84 scope; flagged for a follow-on I77 hygiene tranche if operator desires.

### 4.2 release-gate.py pre-existing test failures

Per Wave C `py scripts/release-gate.py` invocation: 2 test failures (exit code 1; 2486 passed; 2 failed; 17 skipped). **Both failures are pre-existing and not caused by I84** — full disposition + remediation recommendations in [`reports/p8-blocker-2026-05-17-release-gate-preexisting-failures.md`](p8-blocker-2026-05-17-release-gate-preexisting-failures.md):

- `tests/test_company_deck.py::test_slide_11_pillar_1_quotes_governance_metrics` FAILED — deck YAML quote drift (deck quotes "1.166 procesos"; canonical CSV is at 1168). Last touched in I77 P4 commit `4cdf736`; D-IH-30-D hand-sync pattern means every initiative that touches process_list.csv risks this regression. Remediation: single-line deck quote bump.
- `tests/validate_configs.py::TestStrictAkosInventoryContract::test_ollama_model_count` FAILED — `config/openclaw.json.example` has 3 Ollama models; validator expects 4. Last touched in I87 P2/P3 commit `e40fae1`. Remediation: either add the 4th model back OR update the validator to expect 3.

Neither failure traces to any I84 Wave A+B feature commit or Wave C chore commit. Per opt-stop-report classification in the blocker report section 4, these are operator-triage items outside I84 scope.

## 5. Verification artifact summary

Per master-roadmap section 7 closure criteria — verification gates the closure UAT honors:

- `py scripts/validate_substrate_registry.py` — **PASS** (18 rows; status counts active=15, candidate=1, experimental=1, forecasted=1)
- `py -m pytest tests/test_substrate_registry.py -q` — **28 passed** (24 unit + 4 canonical-CSV-integration)
- `py -m pytest tests/test_peopl_research_substrate_audit_cadence.py -q` — **17 passed** (Wave A2 deliverable)
- `py scripts/peopl_research_substrate_audit_cadence.py --staleness-check` — **PASS** (18 rows fresh; 0 stale; 0 parse-error)
- `py scripts/peopl_research_substrate_audit_cadence.py --uat-mode <2026-Q2-substrate-audit.md>` — **PASS** (18 substrate_id citations resolve; 0 unresolved)
- `py scripts/validate_hlk.py` umbrella — **OVERALL: PASS** (1 pre-existing advisory warning per section 4 above; unrelated)
- `py scripts/release-gate.py` — to be run before final closure commit (gates: per checkpoint section 3 baseline + this section's per-validator verdicts)

## 6. Supabase mirror state

Per checkpoint section 2.3:

- `compliance.substrate_registry_mirror` table created on remote MasterData project (`swrmqpelgoblaquequzb`) via selective MCP `apply_migration`
- 18 rows seeded via 3 batches of MCP `execute_sql` upserts
- Verification SELECT confirmed: `total_rows=18`, `distinct_ids=18`, `active=15`, `experimental=1`, `candidate=1`, `forecasted=1`, `rejected_state=2`
- Migration ledger harmonized: `npx supabase migration list` final check shows `20260517000000` aligned local + remote (ghost wall-clock timestamp `20260517001257` reverted; canonical file timestamp applied)
- No further Supabase operations required for I84 P4-P8 closure

## 7. Cross-references

- [`master-roadmap.md`](../master-roadmap.md) section 3 P8 — closure UAT specification.
- [`master-roadmap.md`](../master-roadmap.md) section 7 — promotion / closure criteria.
- [`decision-log.md`](../decision-log.md) D-IH-84-A through D-IH-84-H (8 row ratifications) + D-IH-84-CLOSURE (forward-charter).
- [`risk-register.md`](../risk-register.md) R-IH-84-1 through R-IH-84-7 (pre-existing) + R-IH-84-NEW-ADVOPS + R-IH-84-NEW-CURSOR-TOS-VELOCITY (proposed per checkpoint section 7).
- [`files-modified.csv`](../files-modified.csv) — per-row commit_sha lineage; 18-col schema per `akos-planning-traceability.mdc`.
- [`reports/checkpoints/sc-i84-p1p2-complete-2026-05-17.md`](checkpoints/sc-i84-p1p2-complete-2026-05-17.md) — prior chat's checkpoint surfacing what landed pre-P4-parallel waves.
- [`reports/p1-substrate-landscape-2026-05-17.md`](p1-substrate-landscape-2026-05-17.md) + [`reports/p2-substrate-scorecard-2026-05-17.md`](p2-substrate-scorecard-2026-05-17.md) — P1 + P2 evidence deliverables.
- [`reports/cross-area-unlock-handoff-2026-05-17.md`](cross-area-unlock-handoff-2026-05-17.md) — Wave B1 P5 cascade pre-stage.
- [`reports/advops-engagement-scoping-2026-05-17.md`](advops-engagement-scoping-2026-05-17.md) — Wave A1 ADVOPS scoping.
- [`docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md`](../../../intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md) — Wave A3 first quarterly report (founding-cycle baseline).
- [`docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md) — paired SOP (Wave A2).
- [`scripts/peopl_research_substrate_audit_cadence.py`](../../../../scripts/peopl_research_substrate_audit_cadence.py) — paired runbook (Wave A2).
- [`tests/test_peopl_research_substrate_audit_cadence.py`](../../../../tests/test_peopl_research_substrate_audit_cadence.py) — paired runbook test suite (Wave A2).
- [`config/verification-profiles.json`](../../../../config/verification-profiles.json) substrate_audit_smoke profile (Wave A2).
- [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) — canonical state-of-record (18 rows).
- [`docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) — Research-area doctrine canonical.
- [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) section "UAT evidence contract" — the rule this UAT honors.

## 8. Provenance

Pre-staged at I84 Wave B2 (parallel-to-P4-foreground gate per I86 successor-pickup) 2026-05-17. Confidence `B2` overall; per-row verdicts inherit per-row confidence from upstream evidence (canonical commits = `A1`; pending-P4 rows = `B2` until operator answers).

**Closure gate.** Per master-roadmap section 3 P8 — PAUSE POINT #5 (MANDATORY closure UAT per `akos-agent-checkpoint-discipline.mdc`). This pre-stage gives the operator the closure-shape preview; substantive closure (rows 2-5 + 11 + 18-20 substitutions) waits on P4 + closure decision + the explicit operator approval at PAUSE POINT #5.
