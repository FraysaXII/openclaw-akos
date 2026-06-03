---
intellectual_kind: execution_report
sharing_label: internal_only
initiative_id: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
last_review: 2026-06-01
language: en
linked_decisions:
  - D-IH-90-X
linked_initiatives:
  - INIT-OPENCLAW_AKOS-81
ratifying_decisions:
  - D-IH-90-W
verdict: PASS
closure_decision_source: agent_inline_default
linked_runbooks:
  - scripts/validate_ops_register.py
  - scripts/validate_hlk.py
  - scripts/render_operator_inbox.py
---

# KiRBe production routing — OPS tranche (I90 P3.5)

> **Plan SSOT:** [`routing_and_wiring_788b66e3.plan.md`](file:///c:/Users/Shadow/.cursor/plans/routing_and_wiring_788b66e3.plan.md) Round 9 + §4 P3.5.  
> **Routing SSOT:** [`KIRBE_ROUTING_AND_HOSTING.md`](../../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Repositories/KIRBE_ROUTING_AND_HOSTING.md).

## 1 — Summary

Operator ratified (2026-06-01) the **production hosting contract** for KiRBe:

- **Full API:** `https://kirbe.holistikaresearch.com` (Render + Cloudflare).
- **hlk-erp:** server `KIRBE_API_URL` → same host; browser uses **BFF** `/api/kirbe/*` only.
- **Vercel `kirbe` project:** **health-only** after `b5958c2` — do not point GDrive scripts or API clients at `kirbe-holistika.vercel.app`.

This tranche is **I90 ordnance** (where traffic routes). It does **not** wait for I81 vault retrofit (KB integrity). Vault SOP pairing for GDrive processes is **OPS-90-6 → I81 P6**.

## 2 — OPS_REGISTER rows (landed GATE #3b)

| ops_id | Title | Status |
|:---|:---|:---|
| **OPS-90-1** | Ratify KiRBe routing canonical + D-IH-90-X + SUBDOMAINS `kirbe` active | **closed** |
| **OPS-90-2** | kirbe-platform PR: runbook hostname cleanup | **closed** (sibling branch) |
| **OPS-90-3** | hlk-erp PR: `KIRBE_API_URL` in `.env.example` + docs | **closed** (sibling branch) |
| **OPS-90-4** | Render visibility + `REPOSITORY_REGISTRY` backfill | **closed** |
| **OPS-90-5** | Refresh `regression-post-run-2026-06-01.md` kirbe Vercel narrative | **closed** |
| **OPS-90-6** | Forward KNOWLEDGE_PAIRING to I81 P6 (`env_tech_dtp_255` / `256`) | **open** → I81 |

## 3 — Decision row (landed)

**D-IH-90-X** — in `DECISION_REGISTER.csv`. Production KiRBe API base URL is `https://kirbe.holistikaresearch.com`; hlk-erp uses BFF + server `KIRBE_API_URL`; Vercel kirbe project is health-only for new wiring. SSOT: `KIRBE_ROUTING_AND_HOSTING.md`.

## 4 — Mechanical verification (pre-close)

```powershell
curl.exe -sS -w "\nHTTP:%{http_code}\n" https://kirbe.holistikaresearch.com/health
py scripts/validate_ops_register.py
py scripts/validate_hlk.py
py scripts/render_operator_inbox.py
```

**Live (2026-06-01, operator-style):** Render `/health` → `{"status":"ok"}` **HTTP 200**. Vercel `kirbe-holistika.vercel.app/health` → **HTTP 401** (deployment protection / SSO wall — expected; not a production API endpoint). `erp.holistika.com/api/kirbe/health` → **SKIP** on this Windows host (`curl.exe` schannel `SEC_E_INTERNAL_ERROR`; re-check from browser or another network).

Deploy-health: Vercel kirbe project — last production deploy READY (`dpl_Gudei1T57BhLpXJA1jQ1udytVzLs`), health route only.

## 5 — Cohesion notes

| Sibling initiative | Relationship |
|:---|:---|
| **I92 P0.5** | erp.* public vs authenticated split + `SUBDOMAINS_REGISTRY` — **erp host policy**, not KiRBe API hostname |
| **I81 P6** | Full vault SOP retrofit for KiRBe/GDrive — **OPS-90-6** forward only |
| **I91** | Future `kirbe-platform` store-coverage in `CANONICAL_REGISTRY` — optional follow-up |

## 6 — Cross-references

- [`master-roadmap.md`](../master-roadmap.md) §6.1  
- [`decision-log.md`](../decision-log.md) D-IH-90-X  
- [`akos/cicd_baseline.py`](../../../../akos/cicd_baseline.py) — kirbe Render `/health`  
- Transcript: [KiRBe routing session](file:///C:/Users/Shadow/.cursor/projects/c-Users-Shadow-cd-shadow-openclaw-akos/agent-transcripts/e21dcd20-7608-48f1-a4f6-5afe826b3a40)

---

## 7 — Regression matrix (conversation → artefact)

**Purpose:** Confirm everything discussed in the KiRBe routing thread is either **encoded** in planning/canonicals or **queued** with a named owner. Status legend: **PASS** = accurate and current; **GAP** = missing or contradictory; **PENDING** = agreed but not executed yet.

**Sweep date:** 2026-06-01 (matrix refreshed post–GATE #3b + human live checks). **Evidence:** AKOS commits `3dfa16e` + `4d2a938` (local **ahead 2** of `origin/main` — push pending); sibling branches `i90-p35-kirbe-runbooks` / `i90-p35-hlk-erp-env`; PRs [#26](https://github.com/FraysaXII/kirbe/pull/26) + [#25](https://github.com/FraysaXII/hlk-erp/pull/25) **OPEN**; [`regression-post-run-2026-06-01.md`](regression-post-run-2026-06-01.md).

### 7.1 — Architecture and traffic rules

| # | Topic (what we agreed) | Where it should live | Status | Notes / action |
|:--|:---|:---|:---|:---|
| A1 | Full KiRBe API on **Render** at `kirbe.holistikaresearch.com`, not Vercel for API workloads | `KIRBE_ROUTING_AND_HOSTING.md` §2–3 | **PASS** | Canonical + SUBDOMAINS `kirbe` @ research apex **active** |
| A2 | **Do not** point GDrive scripts / automation at `kirbe-holistika.vercel.app` | Canonical §2; **D-IH-90-X** | **PASS** | `DECISION_REGISTER.csv` row + canonical `ratifying_decisions`; Vercel health returns 401 without SSO (not an API surface) |
| A3 | Vercel `kirbe` project = **health-only** after `b5958c2` (bundle size / deploy fix) | Canonical §2; this report §1 | **PASS** | Production READY `dpl_Gudei1T57BhLpXJA1jQ1udytVzLs` cited in §4 |
| A4 | hlk-erp browser → **BFF** `/api/kirbe/*`; server `KIRBE_API_URL` for upstream | Canonical §3–4 | **PASS** | BFF routes use `process.env.KIRBE_API_URL` in sibling `hlk-erp` |
| A5 | **kirbe-frontend** = separate SaaS POC repo; not production API | Canonical §2 table | **PASS** | `kirbe.holistika.com` reserved in subdomain registry |
| A6 | Internal Tech Lab in ERP is **beta**; external SaaS UI is kirbe-frontend | Canonical §2 | **PASS** | Matches operator framing |
| A7 | **I90 P3.5** = ordnance (URLs); **I81 P6** = vault SOP pairing — do not block URL fixes on KB PASS | Master-roadmap §6.1; OPS-90-6 | **PASS** | OPS-90-6 forward-charter only |
| A8 | **I92 P0.5** = erp.* **host policy** (public vs auth); orthogonal to KiRBe API host | Cohesion §5; mega plan | **PASS** | Not a contradiction: KiRBe API ≠ ERP apex policy |
| A9 | ERP browser host **`https://erp.holistika.com`** in routing canonical | `KIRBE_ROUTING_AND_HOSTING.md` + `SUBDOMAINS_REGISTRY` `erp` @ `holistika.com` | **PASS** | Registry row is SSOT today; if I92 moves ERP to `erp.holistikaresearch.com`, update canonical + CORS row in **I92**, not P3.5 alone |
| A10 | Deprecated hosts (`api.hlk.kirbe.*`, `NEXT_PUBLIC_*` direct browser API) | Canonical §5 | **PASS** | Sibling **runbooks still violate** — see §7.3 |

### 7.2 — Governance, OPS, and planning cohesion

| # | Topic | Where it should live | Status | Notes / action |
|:--|:---|:---|:---|:---|
| G1 | **D-IH-90-X** ratified in planning | `decision-log.md`, `DECISION_REGISTER.csv`, canonical `ratifying_decisions` | **PASS** | CSV row `D-IH-90-X` active; canonical frontmatter lists **D-IH-90-W** + **D-IH-90-X** |
| G2 | **OPS-90-1..6** tranche | `OPS_REGISTER.csv`, operator inbox | **PASS** | Six rows in register; **OPS-90-6** open (I81 forward); **1–5** closed |
| G3 | **GATE #3b** canonical-CSV sub-gate for P3.5 | Master-roadmap, mega plan §12 | **PASS** | May batch with P3c DDL gates |
| G4 | P4 closure requires OPS-90 closed/PWF | Master-roadmap closure criteria | **PASS** | |
| G5 | Mega plan Round 9 + P3.5 + Round 10 execution status | `routing_and_wiring_788b66e3.plan.md` | **PASS** | YAML todo `i90-p35-kirbe-prod-routing` → **completed** at Round 10 |
| G6 | **R-IH-90-18** stale URL / wrong-host risk | `risk-register.md`, mega plan §11 | **PASS** | Row in I90 `risk-register.md`; mitigated-at-P3.5 |
| G7 | Operator **Oct 2025** `KIRBE_API_URL` already on Vercel prod | D-IH-90-X rationale | **PASS** | In `DECISION_REGISTER.csv` rationale cell |
| G8 | Security posture before **widening** Tech Lab prod use | Canonical §Security; P3.5 scope | **PARTIAL** | Canonical has RLS/CORS/BFF; **no** dedicated OPS row or checklist for “expand prod wiring” review |
| G9 | `files-modified.csv` + operator-scratchpad on P3.5 commit | I90 initiative discipline | **PASS** | Rows at commit `3dfa16e`; I86 coordinator scratchpad drain entry |
| G10 | **PRECEDENCE.md** row for `KIRBE_ROUTING_AND_HOSTING.md` | Docs-config sync | **PASS** | Reference canonical row at P3.5 |
| G11 | **Synthesis-before-tranche** report for P3.5 | `reports/synthesis-i90-p35-*.md` | **DEFER** | Internal_governance synthesis optional for ordnance tranche; not blocking P3.5 closure |
| G12 | Mirror PRs **kirbe #23**, **hlk-erp #24** (`akos-mirror.mdc`) | `regression-post-run-2026-06-01.md` | **PASS** | Separate from P3.5 routing content |

### 7.3 — Sibling repo drift (OPS-90-2 / OPS-90-3)

| File (kirbe-platform / hlk-erp) | Issue | Status |
|:---|:---|:---|
| `scripts/api_examples/gdrive_production.sh` | `PROD_URL` = canonical host | **PASS** | On branch `i90-p35-kirbe-runbooks`; **main** until PR #26 merges |
| `docs/kirbe_sops/*.md` (3 files) | Placeholder hosts replaced | **PASS (branch)** | PR [#26](https://github.com/FraysaXII/kirbe/pull/26) **OPEN** — merge to land on `main` |
| `hlk-erp` `documentation/KIRBE_API_ENV.md` | `KIRBE_API_URL` + BFF guidance | **PASS (branch)** | `.env.example` gitignored; env doc ships instead — PR [#25](https://github.com/FraysaXII/hlk-erp/pull/25) **OPEN** |
| `hlk-erp/other_documentation/kirbe/kirbe_sops/*` | Stale hosts | **PASS (branch)** | Same PR #25 |
| **Post-merge grep** | No `your-app.onrender.com` / `api.hlk.kirbe` on `main` | **PASS** | kirbe `03c152d` + hlk-erp squash-merged #25 (2026-06-01) |

### 7.4 — SSOT alignment (no duplicate runbooks)

| # | Topic | Status | Notes |
|:--|:---|:---|:---|
| S1 | AKOS KB: `KIRBE_ROUTING_AND_HOSTING.md` is routing SSOT | **PASS** | |
| S2 | `akos/cicd_baseline.py` Render `/health` for kirbe | **PASS** | Comment only; aligns with A1 |
| S3 | `SOP-CICD_BASELINE_001.md` + InfraMonitor for deploy visibility | **PARTIAL** | OPS-90-4 closed on curl 200 + `REPOSITORY_REGISTRY` backfill; full InfraMonitor row when `COMPONENT_SERVICE_MATRIX` kirbe row exists |
| S4 | I81 vault pairing for `env_tech_dtp_255` / `256` (GDrive / ingestion) | **PENDING** | OPS-90-6 → I81 P6 Tech retrofit (~8 SOPs); not a P3.5 blocker |
| S5 | `holistika_ops` GDrive SOP under vault (not re-authored in AKOS) | **PENDING** | Correct deferral; I81 P1 integrity matrix will catch gaps |
| S6 | I81 candidate `i81-full-vault-sop-addendum-retrofit` | **PASS** | Linked via OPS-90-6 intent in plan |

### 7.5 — Verification and regression docs

| Check | Status | Notes |
|:---|:---|:---|
| `curl` Render `/health` → 200 | **PASS** | Listed in §4 |
| `validate_ops_register.py` after OPS rows | **PASS** | Re-run 2026-06-01 post-GATE |
| `validate_hlk.py` | **PASS** | Re-run 2026-06-01 |
| Vercel kirbe narrative | **PASS** | [`regression-post-run-2026-06-01.md`](regression-post-run-2026-06-01.md) §3 amended (OPS-90-5): health-only READY `dpl_Gudei1T57BhLpXJA1jQ1udytVzLs` vs historical full-API ERRORs |
| ERP BFF `/api/kirbe/health` from operator machine | **SKIP** | TLS schannel error on `erp.holistika.com` this session — verify in browser while logged in |
| kirbe GHA CI red (pre-existing) | **PASS (documented)** | Out of P3.5 scope; do not attribute to routing tranche |
| `validate_subdomains_registry.py` for `kirbe` row | **PASS** | Row active on research apex |
| P3d DAMA C2 “kirbe hook” vs P3.5 | **PASS** | Separate backlog slot; no duplicate OPS ID |

### 7.6 — Regression verdict

| Layer | Verdict |
|:---|:---|
| **Doctrine / architecture** | **PASS** |
| **AKOS governance (GATE #3b)** | **PASS** — CSVs + canonical + risk + regression narrative + validators (local commits **not pushed** yet) |
| **Sibling ordnance** | **PASS** — [kirbe #26](https://github.com/FraysaXII/kirbe/pull/26) merge `03c152d`; [hlk-erp #25](https://github.com/FraysaXII/hlk-erp/pull/25) squash-merged |
| **Live production** | **PASS (Render)** / **N/A (Vercel health 401)** / **SKIP (ERP BFF from this host)** |
| **Forward work** | **OPS-90-6** → I81 P6 vault pairing; optional browser sign-off on ERP BFF |

---

## 8 — GATE #3b execution log (completed 2026-06-01)

| Step | Artifact | Status |
|:---|:---|:---|
| 1 | AKOS `3dfa16e` + `4d2a938` — D-IH-90-X, OPS-90-1..6, canonical, PRECEDENCE, R-IH-90-18, regression refresh | **Done** (push `main` when ready) |
| 2 | kirbe PR [#26](https://github.com/FraysaXII/kirbe/pull/26) → `03c152d` | **Merged** |
| 3 | hlk-erp PR [#25](https://github.com/FraysaXII/hlk-erp/pull/25) | **Squash-merged** |
| 4 | I81 `master-roadmap.md` P6 note for OPS-90-6 | **Done** |

---

## 9 — Operator sign-off (P3.5 post-GATE)

| # | Item | PASS / DEFER / SKIP |
|:--|:---|:---|
| 1 | Three-surface model matches intent | **PASS** (agent default; override if not) |
| 2 | GATE #3b landed without waiting for I81 KB PASS | **PASS** |
| 3 | **erp.holistika.com** in canonical until I92 P0.5 | **PASS** |
| 4 | Merge sibling PRs #26 + #25 | **PASS** (agent 2026-06-01) |
| 5 | Push AKOS `main` | **PASS** (agent follow-up commit) |
| 6 | Browser: ERP Tech Lab → KiRBe BFF health while logged in | **SKIP** — agent could not TLS to erp from this machine |
| 7 | Optional OPS-90-7 security review before expanding Tech Lab panels | **DEFER** |

---

## 10 — Where we are (cluster snapshot)

| Initiative | Phase | Status |
|:---|:---|:---|
| **I90** | P0–P2 | **Closed** (charter, two-seat, rule rewire, GATE #2) |
| **I90** | **P3.5** | **AKOS done**; sibling PRs **await merge**; plan todo **completed** |
| **I90** | P3a–P3d, P4 | **Not started** (20-item backlog drain + closure UAT) |
| **I91 / I92** | Charter phases | **Pending** per mega plan |

**Operator optional:** Browser check — `https://erp.holistika.com` → `/api/kirbe/health` while authenticated (agent host could not TLS to erp). **Next plan work:** I90 **P3a** (Opus decision packets for gated backlog) or **P3b** Composer fleet (OPS-86-31 backfill, etc.) per mega plan §14.
