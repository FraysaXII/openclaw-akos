---
intellectual_kind: research_action_pack
authored: 2026-06-14
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
linked_discipline: RESEARCH_ACTION_DISCIPLINE.md
---

# Research action pack — next governed tranches

## Refresh tranche R1+R2 (2026-06-15 — ~one agent run block)

**Charter:** [`week-1-substrate-reliability-refresh-charter.md`](week-1-substrate-reliability-refresh-charter.md) (legacy filename)  
**Internal sweep R2:** [`internal-vault-sweep-substrate-mint-R2-2026-06-15.md`](internal-vault-sweep-substrate-mint-R2-2026-06-15.md)  
**Synthesis:** [`prong-synthesis-P-I-substrate-reliability.md`](prong-synthesis-P-I-substrate-reliability.md)  
**Mint tranche T1b gate:** [`mint-gate-packet-draft-2026-06-15.md`](mint-gate-packet-draft-2026-06-15.md)

| Step | Owner | Status |
|:---|:---|:---|
| External sweep (OpenClaw Windows issues + LangGraph OSS posture) | AIC | **Done** (SRC-MBH-EXT-027..036) |
| Internal evidence (vault SSOT + post-reboot repair) | AIC | **Done** (SRC-MBH-INT-041..052) |
| P-I synthesis + mint gate packet | AIC | **Done** |
| I96 T0 browser manifest (6 captures) | AIC | **Done** 2026-06-15 |
| Operator ratify mint packet | Operator | **Done** 2026-06-15 (`D-IH-76-MINT`) |
| CSV tranche commit | AIC after ratify | **Done** T1b |

## Govern (operator decisions required)

| Decision | Options | Evidence |
|:---|:---|:---|
| D-MBH-01 Charter home | A) I76 annex only B) New forward initiative C) I49 rollup extension | Master synthesis § operating model |
| D-MBH-02 v3.2 logic row timing | A) At α0 open B) At α1 partner open C) After three-lights | SOP-RELEASE_TAXONOMY_001 |
| D-MBH-03 First alpha scenario order | A) A→B→C B) A+B parallel C) B-first (Research Center) | Prong H; CO-90-004 blocker for A |
| D-MBH-04 Context economics tranche | A) I76 P* B) I84 substrate C) I90 routing | GAP-MBH-01/02 Keter |
| D-MBH-05 CAPABILITY_REGISTRY CSV mint | A) 30-row seed from matrix B) Full 100+ sweep C) Defer | akos-baseline-governance CSV gate |

## Implement (AIC executes after ratify)

### Tranche T1 — Capability harmonization (I76; ~1 week)

- Import `capability-functionality-inventory-matrix.md` rows into WIP CSV
- Cross-link `files-modified.csv` on I76, I96, I90, I84
- Add INTELLIGENCEOPS_REGISTER row: `madeira-brand-capability-harmonization-v32-alpha`
- Update carryover index for GAP-MBH-01..08 as **scheduled**

### Tranche T2 — Context economics spec (I76/I84; ~1–2 weeks)

- Draft `PROMPT_CACHE_AND_COMPACTION_POLICY.md` (WIP; Envoy Tech Lab)
- Extend MADEIRA_AIC_PER_TASK_REGISTRY proposal columns: `cache_policy`, `compaction_policy`, `model_policy`, `budget_class`
- Wire Langfuse export fields for cached tokens
- Postprocessing: extend `lint_brand_voice_offline.py` hook or new `akos/postprocess.py` minimal pipeline

### Tranche T3 — α0 internal closed alpha (I49 + I76; ~2 weeks)

**Prerequisites:** CO-90-004 PASS; T2 spec ratified; dossier conversational light green

- Mint `reports/alpha-v32-exit-criteria-2026-06-*.md`
- Run MADEIRA dossier `--filter madeira` baseline
- Internal cohort: operator + AIC substitution scenarios only
- Closure UAT: PASS or PASS-WITH-FOLLOWUP with PWF rationale

### Tranche T4 — Scenario B experiential (I96; parallel if operator prioritizes UI)

- Complete Research Center browser manifest (375/768/1280)
- Flip Track D from FAIL-until-evidence when manifest complete
- Update operator check-links index

## Test (verification matrix per tranche)

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/source-ledger.csv
py scripts/verify.py pre_commit_fast
py scripts/openclaw_gateway_repair.py   # CO-90-004
py scripts/render_uat_dossier.py --filter madeira
py scripts/browser-smoke.py --playwright
```

## Iterate

- Quarterly research radar sweep on substrate + cache literature
- After each alpha phase: wave-close research enrichment per applied-research discipline
- Promote stable WIP to vault only via ssot-canonical-touch AskQuestion

## Files touched by this research pass

| File | Action |
|:---|:---|
| `docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/*` | Created (this pack) |
| Canonical CSVs | **Not modified** — await D-MBH-05 |
| Carryover index | Update on T1 closure |
