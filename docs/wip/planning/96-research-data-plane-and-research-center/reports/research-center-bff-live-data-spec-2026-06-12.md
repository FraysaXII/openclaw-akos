---
initiative_id: INIT-OPENCLAW_AKOS-96
report_kind: bff-live-data-spec
authored: 2026-06-12
updated: 2026-06-13
consumer_repo: root_cd/hlk-erp
handoff_to: INIT-OPENCLAW_AKOS-92
status: draft
audience: J-OP;J-AIC
linked_decisions:
  - D-IH-96-B
  - D-IH-96-G
  - D-IH-96-H
  - D-IH-96-F
gate_binding: P9b Gate B live-only (D-IH-96-G) + Gate C prong strip (D-IH-96-H)
---

# Research Center BFF — live data wiring spec (all five POV lenses)

> **Purpose:** Mechanical contract for **Phase B BFF alignment** in the HLK-ERP sibling repo (`root_cd/hlk-erp`). Binds **live-only** insight rails (Gate B — the data-honesty ratification recorded as **D-IH-96-G**) and **prong coverage strips on every lens** (Gate C — **D-IH-96-H**) to govern-plane sources in AKOS git. No fixture cards, no `source: fixture` on operator-visible surfaces.

**Read with:** [`three-plane-field-mapping.md`](../three-plane-field-mapping.md), [`three-plane-architecture.md`](../three-plane-architecture.md), [`config/sync/kirbe-sync-contract.md`](../../../../config/sync/kirbe-sync-contract.md), page spec v2 [`research-center-page-spec-v2-2026-06-12.md`](research-center-page-spec-v2-2026-06-12.md).

---

## 1. Gate B live-only (binding)

| Rule | Implementation |
|:---|:---|
| **No fixture insight cards** | BFF MUST NOT emit cards with `source: "fixture"`. Remove fixture badges from T0; audit-only provenance lives in drawer T3 if needed. |
| **Live or omit** | If a card type has no live aggregate, **omit** it from `cards[]` — do not synthesize narrative. |
| **Empty rail ≠ blank rail** | When `cards.length === 0` after live merge, UI renders `LensEmptyState` (IF-09) — lens-specific reason + next action. Zeros on prong strip are allowed (Gate C). |
| **Remediation exception** | Remediation cards (`type: remediation`) are **live diagnostics** when triggers fire (ledger 0, radar empty, KiRBe unhealthy) — not fixtures. |
| **T3 accordion** | v1 panel endpoints may show git vs BFF reconciliation; that is audit tier, not card rail. |

**Ratification cross-ref:** [`i96-ssot-promotion-path-2026-06-12.md`](i96-ssot-promotion-path-2026-06-12.md) §Gate B × IF-09.

---

## 2. BFF module map (hlk-erp)

Sibling repo layout (from P9b Phase A status + exploration E2):

| Layer | Path | Role |
|:---|:---|:---|
| **Route handlers** | `app/api/research-center/**/route.ts` | HTTP auth (level 4+), JSON contracts |
| **Domain lib** | `lib/research-center/*.ts` | Live reads, ranking, empty-state hints |
| **KiRBe proxy** | `lib/services/kirbe.ts` | Execute-plane health + search (existing) |
| **UI** | `components/research-center/*` | POV switcher, rail, strip, drawer, `lens-empty-state.tsx` |

### v1 endpoints (unchanged — accordion T3)

| Method | Path | Lib module | Govern source |
|:---|:---|:---|:---|
| GET | `/api/research-center/wip-packs` | `lib/research-center/wip-packs.ts` | GitHub Contents `docs/wip/intelligence/*/` |
| GET | `/api/research-center/ledger-stats` | `lib/research-center/ledger-stats.ts` | AKOS git `source-ledger.csv` glob |
| GET | `/api/research-center/radar-queue` | `lib/research-center/radar-queue.ts` | `INTELLIGENCEOPS_REGISTER.csv` |
| GET | `/api/kirbe/health` | `lib/services/kirbe.ts` | KiRBe execute plane |

### v2 endpoints (insight machine)

| Method | Path | Lib module | Purpose |
|:---|:---|:---|:---|
| GET | `/api/research-center/insights?pov=` | `lib/research-center/insights.ts` | Ranked cards + strip aggregates per lens |
| GET | `/api/research-center/insights/:id` | `lib/research-center/insight-detail.ts` | Drawer T1–T2 payload |
| GET | `/api/research-center/insights/:id/action` | `lib/research-center/insight-detail.ts` | Resolved CTA metadata (read-only) |
| GET | `/api/research-center/freshness` | `lib/research-center/freshness.ts` | Hero strip v2 badges (optional split from insights) |

**Recommendation:** `GET /insights` returns `{ pov, cards, freshness, prong_strip, empty_state?, meta }` in one payload for TanStack Query cache coherence; split `/freshness` only if bundle size forces it.

---

## 3. Environment and path resolution

BFF reads **govern plane** from AKOS git, not from browser.

| Env var (hlk-erp) | Required | Resolves to |
|:---|:---|:---|
| `AKOS_REPO_ROOT` or `OPENCLAW_AKOS_PATH` | localhost dev | Absolute path to `openclaw-akos` clone (sibling of `hlk-erp` under `root_cd/`) |
| `GITHUB_TOKEN` | prod / Contents API | GitHub Contents for WIP packs when no local clone |
| `GITHUB_AKOS_OWNER` / `GITHUB_AKOS_REPO` | prod | Default `FraysaXII/openclaw-akos` |
| `KIRBE_API_URL` | yes | KiRBe base URL for `/api/kirbe/*` proxy |
| `AKOS_LEDGER_PACKS` | optional | Comma-separated pack slugs; default active I96 packs (see §6.1) |

**Path SSOT (AKOS repo-relative):**

| Artifact | Path |
|:---|:---|
| Research radar register | `docs/references/hlk/v3.0/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv` |
| Source ledgers (WIP) | `docs/wip/intelligence/<pack-slug>/source-ledger.csv` |
| Prong lattice | `docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_PRONG_LATTICE_DISCIPLINE.md` |
| FINOPS counterparty | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv` |
| Initiative registry | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv` |
| Repository registry | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv` |
| I96 roadmap | `docs/wip/planning/96-research-data-plane-and-research-center/master-roadmap.md` |

**KiRBe contract boundary:** KiRBe reads `compliance.*_mirror` read-only per [`kirbe-sync-contract.md`](../../../../config/sync/kirbe-sync-contract.md) §2; ERP BFF never writes compliance or canonical CSV. Search/health uses existing `/api/kirbe/*` — no new KiRBe routes for v2.

---

## 4. Shared response shapes

### 4.1 Insight card (T0)

```typescript
type PovLens = "director" | "operator" | "auditor" | "finance" | "compliance";

type InsightCard = {
  id: string;
  pov: PovLens[];
  type:
    | "remediation"
    | "staleness"
    | "drift"
    | "intent_criticality"
    | "settlement_risk"
    | "env_deploy"
    | "evidence_gap"
    | "phase_blocker"
    | "ledger_completion"
    | "block_govern"
    | "rbac_proof"
    | "uat_evidence";
  severity: "info" | "warning" | "critical";
  headline: string;       // plain language ≤12 words (T0)
  detail: string;         // when/why one line
  cta_label: string;
  cta_kind: "runbook" | "artifact" | "env_fix" | "initiative_phase" | "doc_link" | "ticket";
  cta_href: string;       // command text, repo path, or ERP route
  plane: "govern" | "mirror" | "execute" | "experience";
  source: "live";         // Gate B — only value allowed on card rail
  sort_key: number;       // lens-specific rank
  cta_redacted?: boolean; // Auditor demo @ level 1+
  // Lens-specific extensions (optional on card; full detail in :id)
  register_id?: string;
  ics_rank?: number;
  phase_id?: string;
  pack_slug?: string;
};
```

### 4.2 Freshness strip badge (T0)

```typescript
type FreshnessBadge = {
  id: "ledger" | "radar" | "kirbe" | "mirrors";
  label: string;
  status: "ok" | "warning" | "critical" | "unknown";
  why: string;            // plain language
  micro_cta_label?: string;
  micro_cta_kind?: "runbook" | "env_fix" | "artifact";
  micro_cta_href?: string;
  govern_row?: string;    // three-plane mapping key (T2 drawer)
  git_value?: string | number;
  bff_value?: string | number;
};
```

### 4.3 Prong strip (Gate C — all lenses)

```typescript
type ProngStripCell = {
  prong_id: string;       // BL-* only (14 baseline IDs)
  label: string;          // functional area name from prong lattice
  count: number;          // aggregated row count; zero allowed
  pack_slugs?: string[];    // which packs contributed (T3 optional)
};

type ProngStrip = {
  total_rows: number;
  packs_scanned: number;
  cells: ProngStripCell[];  // sorted count desc; include zeros for top N prongs or full 14
  as_of: string;            // ISO timestamp of ledger read
  charter_budget?: number;  // e.g. 950 Automation OS — Director context only
};
```

**Aggregate algorithm (govern plane):**

1. Resolve pack list from `AKOS_LEDGER_PACKS` or default: `akos-automation-os-governance-2026-06-10`, `holistic-agentic-capability-orchestration-2026-06-10`, `governed-operator-journey-ux-uat-2026-06-12`, `governed-actionable-analytics-surfaces-2026-06-12`, `infonomics-holistika-data-economics-2026-06-12`.
2. For each `source-ledger.csv`, read `prong` column; reject non-`BL-*` at BFF warn log (validator SSOT: `akos/research_ledger_ops.py` `BASELINE_PRONG_IDS`).
3. Sum counts per `BL-*`; attach functional label from prong lattice §3.
4. **Never** map charter aliases (`P1-TECH`, etc.) at display time — git must already be normalized ([`p9b-prong-ssot-fix-2026-06-13.md`](p9b-prong-ssot-fix-2026-06-13.md)).

### 4.4 Lens empty state (IF-09)

```typescript
type LensEmptyState = {
  pov: PovLens;
  title: string;
  reason: string;
  next_actions: { label: string; href: string }[];
};
```

Emitted when `cards.length === 0` **after** live merge (not when remediation cards exist).

---

## 5. POV lens wiring

Default sort, min cards when data exists, and card cap (`CARD_CAP = 7`) from page spec v2 §2.1.

### 5.1 Operator lens (`?pov=operator`)

**Sort:** staleness overdue first → remediation → env/deploy → drift.

| Card type | Live trigger | BFF fields | Data source (govern → execute → experience) |
|:---|:---|:---|:---|
| `remediation` ledger zero | `ledger-stats.total_rows === 0` AND git ledger rows > 0 | `id=remediation-ledger-zero`, `severity=critical`, `cta_kind=runbook` | **Govern:** glob `docs/wip/intelligence/*/source-ledger.csv` line counts · **Experience:** BFF path misconfig · **Runbook:** `py scripts/validate_research_action.py --source-ledger <path>` |
| `remediation` radar empty | register load OK && active rows === 0 | `id=remediation-radar-empty` | **Govern:** `INTELLIGENCEOPS_REGISTER.csv` · **Runbook:** `py scripts/research_radar_sweep.py` |
| `remediation` KiRBe unhealthy | `/api/kirbe/health` !== ok | `id=remediation-kirbe-unhealthy` | **Execute:** KiRBe health · **Handoff:** I83 env checklist |
| `staleness` | `next_verify_by < today` OR sweep STALE | `register_id`, `detail=target name` | **Govern:** register freshness columns · **Mirror:** future `intelligenceops_register_mirror` · **Experience:** radar panel + card |
| `drift` | mirror emit delta / `check-drift` flag | `type=drift`, `plane=mirror` | **Govern:** canonical CSV · **Mirror:** Supabase compliance · **Runbook:** `py scripts/check-drift.py` |
| `env_deploy` | REPOSITORY_REGISTRY deploy !== READY | `type=env_deploy` | **Govern:** `REPOSITORY_REGISTRY.csv` · **Discipline:** deploy-health |
| `evidence_gap` | WIP pack `last_review` stale vs radar | `pack_slug` | **Govern:** pack frontmatter + GitHub Contents |

**Empty-state trigger (`LensEmptyState`):**

- `cards.length === 0` AND git ledger rows > 0 AND radar has no overdue AND KiRBe ok → rare; reason: *"No operator-priority gaps right now"*; next: *Switch to Director lens*, *Open audit panels*.
- `cards.length === 0` AND git ledger rows === 0 → reason: *"No source ledgers reachable from this environment"*; next: *Fix AKOS_REPO_ROOT*, *Open ledger validator doc*.

**Prong strip:** full aggregate (§4.3); Operator sees top 5 `BL-*` by count + overflow chip.

**Freshness micro-CTAs:**

| Badge | Live probe | `why` pattern |
|:---|:---|:---|
| ledger | git count vs BFF count | `"483 rows in git; 0 in BFF — check AKOS_REPO_ROOT"` |
| radar | overdue count from register | `"N overdue / M current"` + sweep CTA |
| kirbe | health JSON | status + env remediation link |

---

### 5.2 Director lens (`?pov=director`)

**Sort:** intent-criticality (`ics_rank`) desc → ledger completion → phase blockers → staleness.

| Card type | Live trigger | BFF fields | Data source |
|:---|:---|:---|:---|
| `intent_criticality` | ICS artifact exists with open finding | `ics_rank`, `dimension_id` (T3) | **Govern:** `artifacts/regression-sweep-*.json` or `scripts/intent_ranked_regression.py` output · **Discipline:** intent-ranked regression |
| `ledger_completion` | always when ledger readable | `detail=% complete`, prong thin spot in headline | **Govern:** prong strip + charter budget (950) · **Lib:** `ledger-stats.ts` |
| `phase_blocker` | roadmap phase `paused` / `blocked` | `phase_id`, `cta_kind=initiative_phase` | **Govern:** `master-roadmap.md` + `INITIATIVE_REGISTRY.csv` |
| `staleness` | same as Operator | lower rank than ICS | Register |
| `remediation` | when env blocks ICS/ledger metrics | same trio as Operator | conditional |
| `evidence_gap` | open UAT / synthesis finding | Quality Fabric linkage | WIP reports under I96 |

**Empty-state trigger:**

- No ICS file AND ledger completion === 100% AND no phase blockers → *"Program metrics look current — no director actions queued"*; next: *Review planning README*, *Switch to Operator for staleness*.

**Prong strip:** full 14 `BL-*` cells (zeros shown) — Director discover row per Gate C.

---

### 5.3 Auditor lens (`?pov=auditor`)

**Sort:** evidence + RBAC first. **RBAC:** `cta_redacted=true` when session level < 4; commands become doc links.

| Card type | Live trigger | BFF fields | Data source |
|:---|:---|:---|:---|
| `rbac_proof` | always on auditor lens | route gate level, demo banner | **Experience:** route-matrix · **Govern:** `access_levels.md` |
| `evidence_gap` / UAT | manifest exists | link to `artifacts/uat-screenshots/i96-*` | **Govern:** MANIFEST.json sha256 |
| `evidence_gap` auth | dev + magic-link captures present | auth path prefixes | UAT workflow notes |
| `evidence_gap` panels | v1 four endpoints return 200 | panel presence | v1 BFF health |
| `staleness` | optional if register readable | lower priority | Register |

**Empty-state trigger (expected on localhost until Phase B):**

- `cards.length === 0` when manifest/auth/panel probes not wired → IF-09 copy from revision screenshot baseline: *"Auditor lens waits on live evidence hooks"*; next: *Switch to Operator*, *Expand audit accordion*, *Open UAT manifest in repo*.

**Prong strip:** show aggregate counts (audit context); zeros valid.

---

### 5.4 Finance lens (`?pov=finance`)

**Sort:** settlement risk desc.

| Card type | Live trigger | BFF fields | Data source |
|:---|:---|:---|:---|
| `settlement_risk` | FINOPS register row with open risk class | counterparty slug | **Govern:** `FINOPS_COUNTERPARTY_REGISTER.csv` · **Mirror:** `finops_counterparty_register_mirror` · **Ops:** `finops_monthly_recon` |
| `settlement_risk` recon | last recon verdict !== PASS | `cta_kind=doc_link` | FINOPS recon SOP + `validate_finops_ledger.py` |
| `evidence_gap` | registered_fact gate open | policy gate status | **Mirror:** `finops.registered_fact` (when env connected) |

**Empty-state trigger:**

- No FINOPS CSV readable OR no rows match risk filter → *"No settlement risks flagged in research-adjacent FINOPS registers"*; next: *Open FINOPS dashboard*, *Switch to Compliance for block_govern*.

**Prong strip:** highlight `BL-FIN` cell + total row context.

---

### 5.5 Compliance lens (`?pov=compliance`)

**Sort:** `block_govern` first → drift → CSV gate pending.

| Card type | Live trigger | BFF fields | Data source |
|:---|:---|:---|:---|
| `block_govern` | `staleness_posture=block_govern` AND overdue | `register_id` | **Govern:** `INTELLIGENCEOPS_REGISTER.csv` |
| `drift` | canonical vs mirror mismatch flag | PRECEDENCE class | **Govern:** canonical CSV · **Runbook:** `check-drift.py`, mirror emit |
| `phase_blocker` | uncommitted canonical CSV tranche | tracker path | git status class (read-only scan) |
| `evidence_gap` | `validate_hlk.py` last verdict !== PASS | validator stdout path (T3) | AKOS verify profile |

**Empty-state trigger:**

- No `block_govern` overdue AND drift check clean → *"No compliance blocks on research freshness or SSOT drift"*; next: *Run HLK validator*, *Open radar sweep*.

**Prong strip:** highlight `BL-COMPLY`, `BL-INTEL`, `BL-RESEARCH`.

---

## 6. Data source reference (three-plane)

| Experience field | Govern (AKOS git) | Mirror (Supabase) | Execute (KiRBe) |
|:---|:---|:---|:---|
| Ledger row / prong counts | `docs/wip/intelligence/*/source-ledger.csv` | future `research.*` view | `SRC-{pack}-{seq}` vault tags |
| Radar queue | `INTELLIGENCEOPS_REGISTER.csv` | `intelligenceops_register_mirror` (when emitted) | re-ingest on STALE |
| KiRBe search / health | — | — | `/api/kirbe/health`, hybrid search |
| WIP packs | GitHub Contents / local glob | — | — |
| FINOPS settlement | `FINOPS_*_REGISTER.csv` | `finops_*_mirror` | — |
| Deploy env | `REPOSITORY_REGISTRY.csv` | `repo_health_snapshot_mirror` | consumer CI status |
| ICS / regression | `artifacts/regression-sweep-*.json` | — | — |
| Phase status | `master-roadmap.md`, `INITIATIVE_REGISTRY.csv` | — | — |

Staleness loop: [`staleness-loop-spec.md`](../staleness-loop-spec.md).

---

## 6.1 Default ledger pack set (prong + ledger-stats)

| Pack slug | Ledger path | Notes |
|:---|:---|:---|
| `akos-automation-os-governance-2026-06-10` | `source-ledger.csv` | BL-* normalized (P9b prong fix) |
| `holistic-agentic-capability-orchestration-2026-06-10` | `source-ledger.csv` | BL-* normalized |
| `governed-operator-journey-ux-uat-2026-06-12` | `source-ledger.csv` | GOJ 60-row pack |
| `governed-actionable-analytics-surfaces-2026-06-12` | `source-ledger.csv` | Analytics insight taxonomy |
| `infonomics-holistika-data-economics-2026-06-12` | `source-ledger.csv` | I97 spine (when present) |

---

## 7. Radar register paths and queue shape

**Canonical file:**

`docs/references/hlk/v3.0/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv`

**Schema SSOT:** `akos/hlk_research_radar.py` → `INTELLIGENCEOPS_REGISTER_FIELDNAMES` (21 columns).

**Load-bearing columns for BFF:**

| Column | BFF use |
|:---|:---|
| `register_id` | Card id suffix; drawer link |
| `target_id` | Headline subject |
| `lifecycle_status` | Filter active rows |
| `volatility_class` | Badge + sort tie-break |
| `staleness_days` | Detail line |
| `staleness_posture` | `block_govern` → Compliance card; Operator staleness severity |
| `next_verify_by` | Overdue calc; freshness strip radar badge |
| `linked_runbook_path` | Drawer T1 command source |

**Queue endpoint:** `GET /api/research-center/radar-queue` returns sorted rows (overdue first). Insights merge reads same loader — **single SSOT function** in `lib/research-center/radar-queue.ts`.

**Sweep alignment:** Optional read of latest `research_radar_sweep.py` JSON/report under AKOS `docs/wip/planning/**/reports/` or operator cache — not required for v1 live if register columns populated.

---

## 8. KiRBe execute-plane contract (Research Center)

Per exploration E1 + kirbe-sync-contract:

| Need | ERP BFF | Upstream | Notes |
|:---|:---|:---|:---|
| Health badge | `GET /api/kirbe/health` | KiRBe `/health` or `/api/v1/health` | Remediation trigger when not `ok` |
| Search panel (v1 accordion) | existing kirbe proxy | hybrid search API | Browser never calls KiRBe host directly |
| Ingest status | optional future | task status routes | Not blocking Phase B |
| Compliance mirrors | **no ERP write** | KiRBe service_role read | KiRBe never writes `compliance.*` |

**Neo4j:** KiRBe local graph ≠ AKOS governance Neo4j (**D-IH-32-M**) — do not merge in BFF.

---

## 9. `GET /api/research-center/insights` — merge algorithm

```
1. auth ≥ level 4 (Auditor demo: level 1+ read-only redaction)
2. pov ← query param (default operator)
3. freshness ← probe ledger, radar, kirbe, mirrors (§5 micro-CTAs)
4. prong_strip ← aggregate §4.3 (all lenses)
5. cards ← []
6. if operator/director env gaps → append remediation cards (live triggers only)
7. switch pov → append lens-specific cards from live sources (§5)
8. sort by lens policy; slice to CARD_CAP (7)
9. if cards.empty → attach lens_empty_state (§4.4)
10. return { pov, cards, freshness, prong_strip, empty_state?, meta: { as_of, akos_root_ok } }
```

**Drawer `GET /insights/:id`:** three-plane row from [`three-plane-field-mapping.md`](../three-plane-field-mapping.md), runbook block (outcome → when → command), govern artifact path, optional initiative hook (functional program name only).

---

## 10. Implementation checklist (hlk-erp Phase B)

| Step | File | Done when |
|:---|:---|:---|
| B1 | `lib/research-center/paths.ts` | AKOS_REPO_ROOT resolution + canonical path constants |
| B2 | `lib/research-center/ledger-stats.ts` | Git line counts + prong breakdown matches validator |
| B3 | `lib/research-center/radar-queue.ts` | Register CSV load + overdue sort shared with v1 |
| B4 | `lib/research-center/prong-strip.ts` | §4.3 aggregate; BL-* only |
| B5 | `lib/research-center/insights.ts` | Per-lens merge §9; **no fixture branch** |
| B6 | `lib/research-center/freshness.ts` | Strip v2 with git vs BFF reconciliation |
| B7 | `lib/research-center/insight-detail.ts` | Drawer payload + three-plane table |
| B8 | `app/api/research-center/insights/route.ts` | Wire GET + query validation |
| B9 | `components/research-center/lens-empty-state.tsx` | IF-09 copy per §5 empty triggers |

**Prerequisite (AKOS):** prong-normalized ledgers — [`p9b-prong-ssot-fix-2026-06-13.md`](p9b-prong-ssot-fix-2026-06-13.md).

---

## 11. Verification

```powershell
# AKOS — ledger + radar SSOT
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/akos-automation-os-governance-2026-06-10/source-ledger.csv
py scripts/validate_research_radar.py --self-test

# hlk-erp — typecheck + e2e
cd root_cd/hlk-erp
npm run typecheck
npx playwright test --grep research-center
```

**Experiential bar (P9b Phase B):**

- Each lens @1280: live cards **or** `LensEmptyState` — never silent rail.
- Prong strip visible on all five lenses (Gate C).
- No `fixture` badge on card face (Gate B).
- Director @1280: ≥1 non-remediation card when ICS or ledger completion live.
- Auditor @1280: empty state or evidence cards — documented in manifest.

---

## Cross-references

- Page spec v2: [`research-center-page-spec-v2-2026-06-12.md`](research-center-page-spec-v2-2026-06-12.md)
- Journey matrix: [`journey-component-matrix-2026-06-12.md`](../../../intelligence/governed-operator-journey-ux-uat-2026-06-12/journey-component-matrix-2026-06-12.md)
- Implementation handoff: [`implementation-spec-2026-06-12.md`](../../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/implementation-spec-2026-06-12.md)
- P9b revision plan §B.3: [`p9b-revision-tranche-plan-2026-06-12.md`](p9b-revision-tranche-plan-2026-06-12.md)
- Operator index: [`operator-check-links-2026-06-12.md`](operator-check-links-2026-06-12.md)
- Prong SSOT fix: [`p9b-prong-ssot-fix-2026-06-13.md`](p9b-prong-ssot-fix-2026-06-13.md)
