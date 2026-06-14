---
language: en
status: active
intellectual_kind: decision_log
initiative: INIT-OPENCLAW_AKOS-99
authored: 2026-06-13
last_review: 2026-06-13
role_owner: System Owner
---

# I99 — Decision Log

## P0 inception (2026-06-13)

### D-IH-99-A — Mint Initiative 99 + EG-5 tranche spine

**Decision.** Promote Supabase platform EG-5 work from intelligence sub-track to **I99** execution spine. Rename ad-hoc folder `99-proposals/` → `00-ad-hoc-proposals/` so initiative **99** is unambiguous.

**Ratified options (inline-ratify 2026-06-13):**

- **Option B** — Full EG-5 tranche (Auth + Storage + Realtime registries + `process_list` rows after CSV gate)
- **Advisor** — Enable MCP `get_advisors` (read-only post-DDL lint)
- **First consumer** — I96 Research Center

**Parent:** I95 L1 Supabase ecosystem governance (`D-IH-95-G`).

**Evidence:** [`../../intelligence/supabase-platform-features-holistika-impact-2026-06-13/research-synthesis-2026-06-13.md`](../../intelligence/supabase-platform-features-holistika-impact-2026-06-13/research-synthesis-2026-06-13.md)

---

### D-SUP-MCP-01 — Enable Advisor in Supabase MCP

**Decision.** Enable Advisor (`get_advisors`) in Cursor Supabase MCP as **read-only** security lint aligned with holistika-ops post-DDL expectation.

**Posture:** Active at P0; reconcile evidence in P1 MCP inventory report.

---

### D-SUP-EG5 — Auth / Storage / Realtime adoption matrix

**Decision.** Govern ungoverned modules **SUPA-MOD-22** (Auth), **SUPA-MOD-23** (Storage), **SUPA-MOD-21** (Realtime) via registry rows + processes — not dashboard-only toggles.

**CSV gate:** P5 requires explicit operator approval before `process_list` / module registry mint.

**First consumer wiring:** I96 auth redirect + Realtime freshness strip (P2–P3).

---

### D-IH-99-B — P1 inventory reconcile complete (CLI-linked)

**Decision.** Accept P1 evidence from Supabase CLI linked probes (MCP unavailable in agent session; CLI is equivalent read-only inventory per holistika-ops).

**Findings:**

- Migration parity: 95 matched; **2 local-only** (`20260612093000` I96 RPC, `20260613120000` I97 cols); **1 remote-only** (`20260611230847` no git file).
- Extensions: manifest extensions (`pgmq`, `pg_cron`, `pg_net`, `wrappers`, `vector`) all enabled on hosted.
- Advisor: 237 security lints; 39 `rls_enabled_no_policy` → EG-4; Auth password-protection lint → EG-5.

### D-IH-99-C — P1 ledger repair complete (operator 2026-06-13)

**Decision.** Accept operator-led migration repair per D-IH-OPS-2 discipline:

1. `migration repair --status reverted 20260611230847` — dashboard-applied duplicate of I96 RPC (same name `i96_current_user_role_mapping_rpc`, wrong timestamp).
2. `migration repair --status applied 20260612093000` — git SSOT version marked applied (DDL already live).
3. `db push --linked` — applied `20260613120000_i97_p6b_infonomics_register_columns.sql` only.
4. **`migration list --linked` CLEAN** — 97/97 matched; no local-only or remote-only rows.

**Evidence:** operator terminal 2026-06-13; updates [`mcp-inventory-reconcile-2026-06-13.md`](reports/mcp-inventory-reconcile-2026-06-13.md) §1 disposition.

---

### D-IH-99-D — P5 expanded to all eight ungoverned modules (operator 2026-06-13)

**Decision.** Expand I99 **P5 canonical CSV tranche** beyond Auth/Storage/Realtime only: flip **all eight** `ungoverned` rows in `SUPABASE_MODULE_REGISTRY.csv` in one governed commit (with inline-ratify before mint).

**Cross-thread:** Coordinate with I96 domain/CICD SSOT ([`research-center-domain-and-cicd-ssot-2026-06-13.md`](../96-research-data-plane-and-research-center/reports/research-center-domain-and-cicd-ssot-2026-06-13.md)) — I96 owns redirect URLs + Vercel env; I99 owns Auth registry + module governance rows.

---

### D-IH-99-E — Preview auth posture (operator 2026-06-13)

**Decision.** Accept operator Preview walk evidence on PR #36 branch host:

| Path | Verdict | Posture |
|:---|:---|:---|
| **Magic link** (Supabase OTP) | **PASS** — operator reached Research Center v2 on Preview | **Active** consumer path for I96 UAT |
| **Dev-password** (`/api/dev/sign-in`) | **PARKED** — reported invalid credentials; not investigated further this session | **Scheduled** — OPS-96-8; may be env mismatch or auth trigger side-effect (see live DB discovery) |
| **Google Workspace SSO** | Not enabled | **Scheduled** — I99 P2/P5 Auth provider registry row; not Preview blocker |
| **Custom Auth email templates** | Default Supabase mail | **Scheduled** — I99 P2 Resend SMTP + template HTML after operator ratifies sender domain |

**Product UX debt** (journey steps, GitHub CTAs, missing mirror BI) is **I96 Phase B+C / B2** in `hlk-erp` — not I99 scope. I99 enables governed Auth + mirror modules; I96 ships operator-facing insight machine.

**Evidence:** operator session 2026-06-13; cross-thread KB in [`research-center-domain-and-cicd-ssot-2026-06-13.md`](../96-research-data-plane-and-research-center/reports/research-center-domain-and-cicd-ssot-2026-06-13.md) § Preview auth outcomes.

---

### D-IH-99-F — P2 Auth registry draft complete (AIC 2026-06-13)

**Decision.** Accept I99 P2 planning deliverables without canonical CSV mint (P5 gate):

- **Spec:** [`reports/auth-registry-and-i96-consumer-spec-2026-06-13.md`](reports/auth-registry-and-i96-consumer-spec-2026-06-13.md)
- **Draft CSV:** [`drafts/SUPABASE_AUTH_REGISTRY.draft.csv`](drafts/SUPABASE_AUTH_REGISTRY.draft.csv) — 16 rows (providers, redirects, hooks, SMTP, templates, RBAC, consumer routes)
- **Data plane default:** mirror-first, GitHub fallback for I96 BFF (documented in spec §6; execution remains I96 B2)

**Next:** P3 Realtime publication contract **or** operator opens P5 early for Auth canonical mint.

---

### D-IH-99-G — P3 Realtime registry draft complete (AIC 2026-06-13)

**Decision.** Accept I99 P3 planning deliverables without canonical CSV mint or publication DDL apply (P5 gate):

- **Spec:** [`reports/realtime-publication-and-i96-freshness-spec-2026-06-13.md`](reports/realtime-publication-and-i96-freshness-spec-2026-06-13.md)
- **Draft CSV:** [`drafts/SUPABASE_REALTIME_REGISTRY.draft.csv`](drafts/SUPABASE_REALTIME_REGISTRY.draft.csv) — 18 rows (publications, channels, badge bindings, fallback policies)
- **Freshness strip today:** **polling-only** on all badges; **radar** badge first Realtime candidate when mirror emit + publication DDL land
- **Execution split:** I99 P5 = publication migration + registry mint; **I96 B2.4** = hlk-erp subscription wiring

**Next:** P4 Storage bucket/path registry draft.

---

### D-IH-99-H — P4 Storage registry draft complete (AIC 2026-06-13)

**Decision.** Accept I99 P4 planning deliverables without canonical CSV mint or bucket DDL apply (P5 gate):

- **Spec:** [`reports/storage-bucket-and-gtm-asset-spec-2026-06-13.md`](reports/storage-bucket-and-gtm-asset-spec-2026-06-13.md)
- **Draft CSV:** [`drafts/SUPABASE_STORAGE_REGISTRY.draft.csv`](drafts/SUPABASE_STORAGE_REGISTRY.draft.csv) — 25 rows (buckets, Analytics Iceberg, Vector, Neo4j cross-tier link)
- **Git-first UAT:** `artifacts/uat-screenshots/` remains active SSOT — Supabase buckets **optional mirror**, not Preview UAT blocker
- **GTM separation:** `hol.gtm.showcase-assets` (public) vs `hol.compliance.evidence-packs` (signed URL, never public)
- **I96 binding:** ERP drawer artifacts target `hol.internal.erp-attachments` + mirror tables — not GitHub blobs (execution I96 B2)

**Next:** P5 canonical CSV tranche — **AskQuestion** gate for Auth + Realtime + Storage registries + remaining ungoverned modules.

---

### D-IH-99-I — Multi-store absorption (operator 2026-06-13)

**Decision.** Absorb **Analytics/Iceberg** (`BI-HOL-ANALYTICS-BUCKETS`) and **Storage Vector / pg_vector** (`SUPA-MOD-17`) into I99 P5 scope — remove `out_of_scope` posture from Storage draft rows. **Neo4j (T3)** remains I91/I93-owned; I99 coordinates via cross-tier link row SUPA-ST-27 + alignment report.

**Drift note (scheduled vault touch):** `DATA_ARCHITECTURE.md` §9 still says Analytics Buckets "non-goal until GA" while BI consumer is **active** — reconcile at P5 gate with `D-IH-93-J`, not dropped.

**Evidence:** [`reports/multi-store-data-plane-alignment-2026-06-13.md`](reports/multi-store-data-plane-alignment-2026-06-13.md); Storage draft rows ST-20, ST-21, ST-25, ST-26, ST-27.

---

### D-IH-99-J — P5 canonical CSV tranche (operator 2026-06-13)

**Decision.** Ratify **Option A** — full EG-5 mint: three vault registries (59 rows), eight module flips, validators, governance registry rows, `DATA_ARCHITECTURE.md` §9 reconcile, process_list + umbrella SOP. Hosted publication/bucket DDL remains **scheduled** separate operator SQL gate.

**Evidence:** [`reports/p5-canonical-tranche-evidence-packet-2026-06-13.md`](reports/p5-canonical-tranche-evidence-packet-2026-06-13.md)

**Executed:** Canonical paths under `dimensions/SUPABASE_{AUTH,REALTIME,STORAGE}_REGISTRY.csv`; module scorecard 18 governed · 8 partial · 0 ungoverned.

---

### D-IH-99-K — Realtime publication SQL gate (AIC 2026-06-13)

**Decision.** Apply migration `20260613150000_i99_realtime_publication_i96_i62.sql` to hosted **MasterData** via `supabase db push` (operator SQL gate Method A). No break-glass MCP apply.

**Verify:** `pg_publication_tables` lists `compliance.intelligenceops_register_mirror` + `holistika_ops.notifications`; both `REPLICA IDENTITY FULL`. Registry rows SUPA-RT-01/02/03/17 → `active`.

**Carryover (scheduled, not dropped):** hlk-erp client subscribe (I96 B2.4 freshness strip + I62 notifications drawer); mirror heartbeat view (SUPA-RT-04).
