---
language: en
status: draft
initiative: 32-holistik-ops-maturation
report_kind: external-team-memo
program_id: PRJ-HOL-KIR-2026
plane: techops
authority: Founder + System Owner
last_review: 2026-04-30
audience: KiRBe team lead + KiRBe engineering
---

# KiRBe team — section-2-frozen-until-I32-P9 memo (D-IH-32-G)

**From:** AKOS governance (Founder + System Owner)
**To:** KiRBe team lead + KiRBe engineering
**Subject:** Heads-up — `kirbe-sync-contract.md` §2 frozen for ~2 weeks; rewrite landing in I32-P9
**Date:** 2026-04-30

## What this memo is

A short heads-up that AKOS Initiative 32 ("Holistik Ops Maturation") will rewrite `config/sync/kirbe-sync-contract.md` §2 ("Canonical-to-KiRBe Propagation Ownership") in roughly two weeks. We are freezing the file as it stands today so we can land a clean rewrite without merge conflicts. **No action required from your side this week**; we'll come back with the rewrite + a 6-section handoff memo + an architecture audit memo + bilingual cover-emails (EN + ES) at I32-P9.

## Why §2 is being rewritten

The contract enumerates 3 mirrors today (process_list, baseline_organisation, FINOPS counterparty). The actual canonical mirror set is **12 mirrors** as of I31 (added: persona, channel touchpoint, sourcing, GOI/POI w/ distance schema, adviser disciplines, adviser open questions, founder filed instruments, program registry, topic registry). After I32 it will be **16 mirrors** (added: skill registry, touchpoint-kit cell registry, policy register, repo health snapshot).

KiRBe is operating on a stale map. The rewrite makes the map current.

## What we're asking you to NOT do during the freeze window

- Do not write a parallel KiRBe-side migration that hard-codes mirror table names from the current §2.
- Do not start a new ingestion pattern this week; wait for the I32-P9 rewrite.
- Do not invent new persona / channel / sourcing / skill / topic IDs locally — request them via PR to AKOS as you would today.

## What we're asking you to do (read-only, 5 minutes)

- Confirm receipt of this memo (a thumbs-up emoji on the relevant slack thread is enough, or a one-line reply).
- Tell us your preferred consumption pattern for the new mirrors (Q6 in our decision log):
  - **(a) RLS read-only** — KiRBe consumes via Supabase RLS-scoped reads, server-side, `service_role` for sync jobs only
  - **(b) Versioned JSON snapshot** — AKOS emits dated JSON snapshots, KiRBe ingests on its own cadence
  - We recommend (a); aligns with how `compliance.process_list_mirror` and `compliance.baseline_organisation_mirror` are consumed today.

## What you'll get at I32-P9 (~2 weeks out)

- **Rewritten `config/sync/kirbe-sync-contract.md` §2** — all 16 mirrors enumerated with `sync_direction; rls_posture; consumer_role`
- **New §11** — cross-repo contract section codifying the EXTERNAL_REPO_CONTRACT.md pattern (D-IH-32-K)
- **6-section handoff memo** covering: (1) new dimensions; (2) §2 contract status; (3) `language:` frontmatter discipline; (4) billing-plane unchanged (`hlk_billing_plane` metadata, `kirbe.*` vs `holistika_ops.*`); (5) webhook idempotency fixture; (6) `service_role` quarterly rotation cadence
- **KiRBe architecture audit memo** — uses your v1.2 reality (we read your README; we know about the 7 connectors, hybrid search, audit logging, Stripe FDW + webhook, usage metering, WebSocket streams, service-first DI, LlamaIndex readers, **your local Neo4j**, Logfire) and proposes 5 concrete architecture-level deltas:
  1. KiRBe ingests `compliance.persona_registry_mirror` read-only and exposes a "persona-aware vault search"
  2. KiRBe ingests `compliance.channel_touchpoint_registry_mirror` and ties incoming web/Discord/Gmail ingestion to the matching `channel_id` for provenance
  3. KiRBe ingests `compliance.skill_registry_mirror` to expose "what AKOS skills are wired against KiRBe data" as a tenant-facing dashboard tile (the MADEIRA-SaaS bridge)
  4. KiRBe's local Neo4j stays separate from AKOS Neo4j (D-IH-32-M); cross-link only via `repo_slug`
  5. Cite `policy_id` from AKOS POLICY_REGISTER (new in I32-P4) for every RLS rule in `kirbe.*` (cross-repo policy traceability)
- **Things we are explicitly NOT changing**: billing-plane discipline; LlamaIndex pipeline; FastAPI patterns; your `60-graphdb-neo4j.mdc` cursor rule
- **PR-ready patch** for your repo: ships an `EXTERNAL_REPO_CONTRACT.md` at root + a tiny `.cursor/rules/akos-mirror.mdc` cursor rule that imports AKOS HLK doctrine without copying it. You review and merge.
- **Bilingual cover-email drafts** (EN + ES per D-IH-32-P): EN for the GitHub PR thread, ES for direct outreach to the team lead

## Timeline

- **2026-04-30 (today)** — this freeze memo
- **~2 weeks out (I32-P9)** — full rewrite + handoff bundle + architecture audit + PR patch + cover-emails
- **+1 week after that** — operator forwards bundles; you review and ack

## Questions

Reply to this memo or ping the founder directly. Open AKOS-side question for you: **Q6** (consumption pattern preference, see above).

---

**Cross-references:**
- Initiative 32 master roadmap: [`docs/wip/planning/32-holistik-ops-maturation/master-roadmap.md`](../master-roadmap.md)
- Initiative 32 decision log: [`docs/wip/planning/32-holistik-ops-maturation/decision-log.md`](../decision-log.md) (D-IH-32-G freeze decision; D-IH-32-K cross-repo contract; D-IH-32-M Neo4j separation; D-IH-32-P bilingual emails)
- Current `config/sync/kirbe-sync-contract.md`: [link](../../../../config/sync/kirbe-sync-contract.md) (will be rewritten at I32-P9)
- `TEAM_SOTA_KIRBE.md`: [link](../../../14-holistika-internal-gtm-mops/reports/TEAM_SOTA_KIRBE.md) (will gain §11 + §12 + §13)
