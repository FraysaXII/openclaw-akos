---
intellectual_kind: internal_evidence_sweep
authored: 2026-06-15
tranche: R2
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
decision_use: D-MBH-W1-01 — answers previously asked of operator; all from v3.0 / AKOS SSOT
---

# Internal vault sweep R2 — substrate, I96, mint gates (end-to-end)

> **Purpose:** Double the internal research before mint tranche T1b. Every row below is already in `docs/references/hlk/v3.0/` or AKOS scripts — no operator questions required.

## 1. Consumer repo paths (hlk-erp)

| Question | Vault / script answer |
|:---|:---|
| Where is hlk-erp? | `REPOSITORY_REGISTRY.csv` → `local_path=root_cd/hlk-erp` → **`C:\Users\Shadow\cd_shadow\root_cd\hlk-erp`** (sibling of openclaw-akos, not under akos repo) |
| SSOT for fleet paths | `scripts/snapshot_external_repos.py`, `scripts/workspace_fleet_hygiene_sweep.py`, `scripts/bless_external_repo.py` |
| Remote | `https://github.com/FraysaXII/hlk-erp` — class `platform`, owner System Owner, D-IH-32-K |

**Prior agent error:** searched `cd_shadow/hlk-erp` — wrong. Correct prefix is **`cd_shadow/root_cd/`**.

## 2. Research Center local dev (I96 L3)

| Field | SSOT |
|:---|:---|
| Dev port | **`3010`** — experiential ladder + B1.5 workflow notes |
| Auth path (automation) | `http://localhost:3010/api/dev/sign-in?next=/research-center` |
| Auth path (operator UAT) | Magic link via `http://localhost:3010/sign-in?next=%2Fresearch-center` |
| Redirect URL registry | `SUPABASE_AUTH_REGISTRY` **SUPA-AUTH-07** → `http://localhost:3010/auth/callback` |
| Preview dev-password binding | **SUPA-AUTH-16** + `SOP-TECH_LAB_PLATFORM_BINDING_001` §4 |
| Playwright spec | `root_cd/hlk-erp/tests/e2e/research-center-v2.visual.spec.ts` |
| Evidence storage | **git-first** — `SUPABASE_STORAGE_REGISTRY` SUPA-ST-17 → `artifacts/uat-screenshots/` in AKOS repo |
| Proof adapter | `PROOF_ADAPTER_REGISTRY` **PAD-001** → `browser_experiential` |
| Visual review SOP | `SOP-PEOPLE_UAT_VISUAL_EVIDENCE_001` — parent agent must Read PNGs; no subagent-only PASS |

Production host: `https://erp.holistikaresearch.com` — separate ladder tier; localhost L3 = **dev evidence**, not production PASS.

## 3. OpenClaw gateway (adapter, not product)

| Field | SSOT |
|:---|:---|
| Repair runbook | `scripts/openclaw_gateway_repair.py` + `SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001` §4.6 |
| Process row | `process_list` → `env_tech_dtp_openclaw_runtime_health_triage_001` |
| Substrate row | `SUBSTRATE_REGISTRY` — OpenClaw as one row; `AGENTIC_FRAMEWORK_LANDSCAPE` thin adapter |
| Escalation | `scripts/openclaw_health_escalate.py` — symptom-class `gateway-cold-start` |
| Evidence class | Repair JSON ≠ MADEIRA α0; binds to CO-90-004 / PROOF_ADAPTER on mint |

## 4. Mint gate prerequisites (canonical CSV)

| Gate | Rule |
|:---|:---|
| CSV before SOP | `SOP-META_PROCESS_MGMT_001` §4.2–4.3; `akos-baseline-governance` canonical CSV gates |
| SUBSTRATE + DATA_CONTRACT | Draft in substrate audit; atomic tranche in mint-gate packet |
| PROOF_ADAPTER | `PROOF_ADAPTER_REGISTRY.csv` — pair PAD-001 pattern for gateway JSON |
| HLK validate | `py scripts/validate_hlk.py` after any CSV mint |
| Operator ratify | `OPERATOR_STEERING_AND_CARRYOVER.md` RULE 6 — AskQuestion on registry mint only |

## 5. Lab platform / Preview (when not localhost)

| Field | SSOT |
|:---|:---|
| Env contract | `DC-HOL-LAB-PLATFORM-ENV-001` + `SOP-TECH_LAB_PLATFORM_BINDING_001` |
| Investigation ladder | Platform docs → auth-probe → config kind → redeploy → credentials last |
| Failure 8 | Sensitive toggle on non-secret runtime gates — not wrong password |
| Preview host | `preview.erp.holistikaresearch.com` or PR branch Vercel URL |

## 6. Multi-method portfolio (vault-backed)

| Method | Registry / canonical |
|:---|:---|
| OpenClaw local | SUBSTRATE row + I90 routing |
| LangChain / LlamaIndex | SUBSTRATE_REGISTRY existing rows; I84 roadmap |
| LangGraph OSS | Evaluation spike — not yet in CSV |
| MCP tools | `AGENTIC_FRAMEWORK_LANDSCAPE` §3 postures |
| KiRBe BFF | `KIRBE_ROUTING_AND_HOSTING.md` — browser never calls Kirbe API direct |

## 7. Info economics link

Agent runs (5–15 min) execute tranches; human calendar dates on carryover index are for **operator review**, not agent duration. See `agent-run-timing-doctrine.md`.

## 8. Gaps this sweep closes (for AIC)

- ~~Ask operator for hlk-erp path~~ → **root_cd/hlk-erp**
- ~~Ask when to mint~~ → after R1+R2 research + mint packet ratify (T1b)
- ~~Ask auth path~~ → SUPA-AUTH-07/16 + ladder § L3

## Source IDs added to ledger

INT-046..052, EXT-034..039 (see `source-ledger.csv`). External R2 expansion adds upstream issues **41804**, **61579**, **91926** (Session 0 / schtasks races) alongside prior **63491**, **49871**, **PR 52487**.

## 9. Mint tranche T1b readiness (research complete)

| Prerequisite | Status |
|:---|:---|
| P-A..P-I prong synthesis | Done |
| R1 external OpenClaw + LangGraph sweep | Done (91 ledger rows) |
| R2 internal v3.0 vault sweep | Done |
| Post-reboot gateway PROOF evidence | Done (`artifacts/gateway-repair-post-reboot-2026-06-15.json`) |
| I96 T0 experiential manifest | Done (6 captures; CO-MBH-006 satisfied) |
| Mint gate packet draft | Ready for operator ratify |
| FOUNDER_METHODOLOGY_VERSIONING §2 v3.2 lineage row | **Scheduled** with T1b CSV commit |

**Remaining human gate:** ratify `mint-gate-packet-draft-2026-06-15.md` — not an agent-duration question.
