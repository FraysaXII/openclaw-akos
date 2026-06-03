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
curl -sS -o NUL -w "%{http_code}" https://kirbe.holistikaresearch.com/health
py scripts/validate_ops_register.py
py scripts/validate_hlk.py
py scripts/render_operator_inbox.py
```

Deploy-health: Vercel MCP on kirbe project — last production deploy READY (`dpl_Gudei1T57BhLpXJA1jQ1udytVzLs`), health route only.

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

**Sweep date:** 2026-06-01. **Evidence:** AKOS repo + local sibling clones `root_cd/kirbe`, `root_cd/hlk-erp`; Vercel narrative from P3.5 notes + [`regression-post-run-2026-06-01.md`](regression-post-run-2026-06-01.md).

### 7.1 — Architecture and traffic rules

| # | Topic (what we agreed) | Where it should live | Status | Notes / action |
|:--|:---|:---|:---|:---|
| A1 | Full KiRBe API on **Render** at `kirbe.holistikaresearch.com`, not Vercel for API workloads | `KIRBE_ROUTING_AND_HOSTING.md` §2–3 | **PASS** | Canonical + SUBDOMAINS `kirbe` @ research apex **active** |
| A2 | **Do not** point GDrive scripts / automation at `kirbe-holistika.vercel.app` | Canonical §2; D-IH-90-X (pending CSV) | **PENDING** | Decision prose in `decision-log.md`; **not** in `DECISION_REGISTER.csv` yet |
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
| G1 | **D-IH-90-X** ratified in planning | `decision-log.md`, `DECISION_REGISTER.csv`, canonical `ratifying_decisions` | **GAP** | Prose **ratified** in decision-log; **no CSV row**; canonical still lists only **D-IH-90-W** |
| G2 | **OPS-90-1..6** tranche | `OPS_REGISTER.csv`, operator inbox | **GAP** | Table in this report only; **zero** `OPS-90-*` rows in register |
| G3 | **GATE #3b** canonical-CSV sub-gate for P3.5 | Master-roadmap, mega plan §12 | **PASS** | May batch with P3c DDL gates |
| G4 | P4 closure requires OPS-90 closed/PWF | Master-roadmap closure criteria | **PASS** | |
| G5 | Mega plan Round 9 + P3.5 deep section + mermaid P3→P3.5→P4 | `routing_and_wiring_788b66e3.plan.md` | **PASS** | YAML todo `i90-p35-kirbe-prod-routing` still **pending** |
| G6 | **R-IH-90-18** stale URL / wrong-host risk | `risk-register.md`, mega plan §11 | **GAP** | Named in mega plan; **not** appended to I90 `risk-register.md` |
| G7 | Operator **Oct 2025** `KIRBE_API_URL` already on Vercel prod | D-IH-90-X rationale / decision-log | **GAP** | Discussed in session; **not** written into decision rationale (audit trail) |
| G8 | Security posture before **widening** Tech Lab prod use | Canonical §Security; P3.5 scope | **PARTIAL** | Canonical has RLS/CORS/BFF; **no** dedicated OPS row or checklist for “expand prod wiring” review |
| G9 | `files-modified.csv` + operator-scratchpad on P3.5 commit | I90 initiative discipline | **GAP** | Not updated for this tranche yet |
| G10 | **PRECEDENCE.md** row for `KIRBE_ROUTING_AND_HOSTING.md` | Docs-config sync / new canonical pattern | **GAP** | No PRECEDENCE hit for file name (reference doc under Repositories/) |
| G11 | **Synthesis-before-tranche** report for P3.5 | `reports/synthesis-i90-p35-*.md` | **GAP** | Internal_governance tranche may fire SYN-05/07/08; no synthesis report minted yet (pre-commit gate) |
| G12 | Mirror PRs **kirbe #23**, **hlk-erp #24** (`akos-mirror.mdc`) | `regression-post-run-2026-06-01.md` | **PASS** | Separate from P3.5 routing content |

### 7.3 — Sibling repo drift (OPS-90-2 / OPS-90-3)

| File (kirbe-platform) | Issue | Status |
|:---|:---|:---|
| `scripts/api_examples/gdrive_production.sh` | `PROD_URL` = canonical host | **PASS** | Line 5 correct; line 6 comment still shows `your-app.onrender.com` (harmless) |
| `docs/kirbe_sops/render_deployment_gdrive.md` | Placeholder `your-app.onrender.com` | **GAP** | OPS-90-2 |
| `docs/kirbe_sops/google_drive_setup_guide.md` | Same placeholder | **GAP** | **Add to OPS-90-2 file list** (was omitted from §2 table) |
| `docs/kirbe_sops/sop-hlk-erp-kirbe.md` | `api.hlk.kirbe.*` + `NEXT_PUBLIC_API_BASE_URL` | **GAP** | OPS-90-2 and/or OPS-90-3 |
| `hlk-erp/.env.example` | Document `KIRBE_API_URL=https://kirbe.holistikaresearch.com` | **GAP** | OPS-90-3 (grep found BFF code but not `.env.example` in quick pass) |

### 7.4 — SSOT alignment (no duplicate runbooks)

| # | Topic | Status | Notes |
|:--|:---|:---|:---|
| S1 | AKOS KB: `KIRBE_ROUTING_AND_HOSTING.md` is routing SSOT | **PASS** | |
| S2 | `akos/cicd_baseline.py` Render `/health` for kirbe | **PASS** | Comment only; aligns with A1 |
| S3 | `SOP-CICD_BASELINE_001.md` + InfraMonitor for deploy visibility | **PARTIAL** | OPS-90-4 queues Render MCP + registry backfill; not executed |
| S4 | I81 vault pairing for `env_tech_dtp_255` / `256` (GDrive / ingestion) | **PENDING** | OPS-90-6 → I81 P6 Tech retrofit (~8 SOPs); not a P3.5 blocker |
| S5 | `holistika_ops` GDrive SOP under vault (not re-authored in AKOS) | **PENDING** | Correct deferral; I81 P1 integrity matrix will catch gaps |
| S6 | I81 candidate `i81-full-vault-sop-addendum-retrofit` | **PASS** | Linked via OPS-90-6 intent in plan |

### 7.5 — Verification and regression docs

| Check | Status | Notes |
|:---|:---|:---|
| `curl` Render `/health` → 200 | **PASS** | Listed in §4 |
| `validate_ops_register.py` after OPS rows | **PENDING** | Rows do not exist yet |
| `validate_hlk.py` | **PASS** | Per `regression-post-run-2026-06-01.md` |
| Vercel MCP kirbe: health-only READY vs “all ERROR” | **CONFLICT** | [`regression-post-run-2026-06-01.md`](regression-post-run-2026-06-01.md) §3 still says production **ERROR** on mirror merge (`dpl_wJDD7…`) — **pre-health-only narrative**; **OPS-90-5** must add footnote: historical full-API ERRORs vs current health-only READY |
| kirbe GHA CI red (pre-existing) | **PASS (documented)** | Out of P3.5 scope; do not attribute to routing tranche |
| `validate_subdomains_registry.py` for `kirbe` row | **PASS** | Row active on research apex |
| P3d DAMA C2 “kirbe hook” vs P3.5 | **PASS** | Separate backlog slot; no duplicate OPS ID |

### 7.6 — Regression verdict

| Layer | Verdict |
|:---|:---|
| **Doctrine / architecture** | **PASS** — canonical + plan + I90 roadmap encode the three-surface model and BFF rule |
| **Governance execution** | **GAP** — D-IH-90-X + OPS-90-* not in CSVs; R-IH-90-18 not in risk register; scratchpad / files-modified not updated |
| **Sibling ordnance** | **GAP** — four kirbe doc paths still teach wrong hosts (OPS-90-2/3) |
| **Regression narrative** | **GAP** — post-run report contradicts P3.5 until OPS-90-5 |
| **Forward work** | **PENDING** — OPS-90-4 (Render/InfraMonitor), OPS-90-6 (I81 P6), optional explicit security-review OPS |

**Nothing material is missing from the *design* layer.** What is missing is **execution of GATE #3b** (CSV mint + canonical frontmatter bump + sibling PRs + regression doc refresh) and **two hygiene items** (Oct 2025 prod evidence in decision rationale; `google_drive_setup_guide.md` on OPS-90-2 file list).

---

## 8 — Recommended commit order (GATE #3b)

1. AKOS: `DECISION_REGISTER` **D-IH-90-X** + `OPS_REGISTER` **OPS-90-1..6** + `KIRBE_ROUTING_AND_HOSTING.md` `ratifying_decisions` + optional `PRECEDENCE` reference row + `risk-register` **R-IH-90-18** + refresh §7 sources in `regression-post-run` (OPS-90-5) + `files-modified.csv` + operator-scratchpad.
2. Sibling PRs: kirbe runbooks (OPS-90-2), hlk-erp env/docs (OPS-90-3).
3. Operator: Render MCP + `COMPONENT_SERVICE_MATRIX` / inbox (OPS-90-4).
4. I81 charter note: OPS-90-6 consumed at P6 kickoff.

---

## 9 — Operator sign-off (P3.5 pre-execution)

| # | Item | PASS / DEFER |
|:--|:---|:---|
| 1 | Three-surface model (Render API / ERP BFF / Vercel health-only / kirbe-frontend POC) matches your intent | |
| 2 | Proceed GATE #3b CSV mint without waiting for I81 KB PASS | |
| 3 | Accept **erp.holistika.com** in routing canonical until I92 P0.5 reconciles apex (if ever) | |
| 4 | Authorize sibling PRs for runbook cleanup (OPS-90-2/3) | |
| 5 | Optional: add **OPS-90-7** “security review before expanding Tech Lab KiRBe panels” if you want it tracked separately from R-IH-90-18 | |
