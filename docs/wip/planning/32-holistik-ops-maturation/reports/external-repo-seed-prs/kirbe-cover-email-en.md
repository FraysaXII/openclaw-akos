---
language: en
status: draft
audience: KiRBe team lead + KiRBe engineering thread
delivery_method: GitHub PR thread (engineering audience prefers EN)
---

**Subject:** [Holistika Ops] KiRBe seed PR — EXTERNAL_REPO_CONTRACT.md + akos-mirror.mdc + sync contract §2 rewrite

Hi team,

Two weeks ago we sent a freeze memo letting you know `config/sync/kirbe-sync-contract.md` §2 would be rewritten. The rewrite landed today as part of Initiative 32 P7 in the AKOS repo, alongside three deliverables for your side:

**1. PR patch (2 files)** — see `kirbe.patch` in `docs/wip/planning/32-holistik-ops-maturation/reports/external-repo-seed-prs/` of the AKOS repo.

The patch ships a 1-page `EXTERNAL_REPO_CONTRACT.md` for your repo root and a small `akos-mirror.mdc` cursor rule for `.cursor/rules/`. The contract is non-prescriptive on your stack (FastAPI, LlamaIndex, Pydantic, Logfire, Stripe FDW, your local Neo4j) — those stay yours. It pins the HLK doctrine surface only.

**2. Architecture audit memo** — `kirbe-architecture-audit-2026-04-30.md`.

We read your README and your 36 cursor rules. KiRBe is at v1.2 production with hybrid search (BM25 + vector + RRF), audit logging (SOC2/GDPR-ready), Stripe billing FDW + webhook, per-tenant usage metering, WebSocket streams, service-first DI, your local Neo4j vault graph. The audit recommends 5 architecture-level deltas focused on consuming the new I31/I32 mirrors read-only — none of them touch your billing-plane discipline (`hlk_billing_plane` metadata, `kirbe.*` vs `holistika_ops.*` separation), your local Neo4j (stays separate from AKOS Neo4j per D-IH-32-M), or your LlamaIndex pipeline.

**3. Updated `kirbe-sync-contract.md`** §2 + new §11.

§2 now enumerates all 16 mirrors (was 3) with `sync_direction; rls_posture; consumer_role`. §11 is new and codifies the cross-repo contract you're acknowledging via the PR patch.

**What we need from you, in order:**

1. Review the PR patch + memo + audit. Reply on this thread with feedback or "merge as-is".
2. Pick a consumption pattern for the new mirrors (open question Q6): RLS read-only via Supabase (recommended; aligns with how you consume `process_list_mirror` today) or versioned JSON snapshots.
3. Merge the patch when comfortable. Next AKOS weekly REPO_HEALTH_SNAPSHOT will pick up the change automatically.

**What we explicitly are NOT asking you to change:**

- Billing-plane discipline (`hlk_billing_plane`, `kirbe.*` vs `holistika_ops.*`).
- LlamaIndex pipeline and your reader composition.
- Your local Neo4j (stays separate from AKOS Neo4j; D-IH-32-M).
- Your existing 36 cursor rules.

The architecture audit's 5 deltas are recommendations on a non-blocking timeline. Initiative 33 (deferred) will pick up KiRBe-specific work on a future cycle.

Best,

— Holistika AKOS governance (Founder + System Owner)

---

**Cross-references:**

- AKOS repo: https://github.com/FraysaXII/openclaw-akos
- Initiative 32 master roadmap: `docs/wip/planning/32-holistik-ops-maturation/master-roadmap.md`
- HLK PRECEDENCE.md: `docs/references/hlk/compliance/PRECEDENCE.md`
- 6-axis Holistik Ops doctrine: `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md`
