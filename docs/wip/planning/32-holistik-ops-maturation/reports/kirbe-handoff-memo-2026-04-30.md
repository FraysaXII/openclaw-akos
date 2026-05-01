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

# KiRBe handoff memo — 6-section (Initiative 32 P7)

**From:** AKOS governance (Founder + System Owner)
**To:** KiRBe team lead + KiRBe engineering
**Subject:** I32 P7 deliverables — sync contract §2 rewritten + cross-repo contract + 5 architecture-level deltas
**Date:** 2026-04-30

This memo follows the 2026-04-30 freeze memo (`reports/kirbe-freeze-memo-2026-04-30.md` in AKOS). The freeze is now lifted — `config/sync/kirbe-sync-contract.md` §2 has been rewritten and §11 is new.

## Section 1 — New canonical dimensions live since I31 + I32

KiRBe now has access to 16 governed compliance mirrors (was 3 in the legacy §2). Net-new since the legacy contract:

- **I21**: `goipoi_register_mirror`, `adviser_engagement_disciplines_mirror`, `adviser_open_questions_mirror`, `founder_filed_instruments_mirror` (all under PRJ-HOL-FOUNDING-2026)
- **I23**: `program_registry_mirror`
- **I25**: `topic_registry_mirror`
- **I31**: `persona_registry_mirror`, `channel_touchpoint_registry_mirror`, `sourcing_register_mirror` + GOI/POI distance schema bump
- **I32**: `validation_runs` (operational), `skill_registry_mirror`, `touchpoint_kit_cell_mirror`, `policy_register_mirror`, `repo_health_snapshot_mirror` (operational; AKOS-cron-only)

Read-only via Supabase RLS; service_role-scoped sync job on the KiRBe side.

## Section 2 — Sync contract status

`kirbe-sync-contract.md` §2 enumerates all 16 mirrors with `sync_direction; rls_posture; consumer_role`. New §11 codifies the cross-repo contract (D-IH-32-K) and confirms the 4 things NOT being changed: billing-plane discipline; LlamaIndex pipeline; KiRBe local Neo4j; existing 36 cursor rules.

## Section 3 — Language frontmatter discipline

Per `SOP-HLK_LOCALISATION_001.md` (relocated to `Marketing/Brand/` in I32 P7), every canonical MD declares `language: en|es|fr` in frontmatter. Today KiRBe MD compliance is 0% (REPO_HEALTH_SNAPSHOT 2026-04-30). Adopt on new MD files; existing files migrate on a non-blocking timeline. The audience-canonical exception (D-IH-31-A) applies to ES strategy artifacts.

## Section 4 — Billing-plane unchanged

`hlk_billing_plane` metadata key on Stripe webhook routing stays. `kirbe.*` schema (KiRBe SaaS product subscriptions) and `holistika_ops.*` schema (Holistika company billing) stay separated. Per existing `TEAM_SOTA_KIRBE.md` §3 ("Billing — two planes (mandatory)"). Initiative 32 does not touch this.

## Section 5 — Webhook idempotency fixture (cite policy_id from POLICY_REGISTER)

POL-RLS-FINOPS-DENY-ANON and POL-RLS-FINOPS-DENY-AUTH (new in I32 P4) are the FINOPS-side RLS policies. Recommend the KiRBe webhook handler cite `POL-RLS-FINOPS-DENY-ANON` in its docstring and add an idempotency-key fixture test that asserts duplicate webhook payloads do not double-write `kirbe.subscriptions`. Cross-repo policy traceability: future audits can answer "which RLS rule governs this webhook?" with one CSV lookup.

## Section 6 — service_role quarterly rotation cadence

POL-SERVICE-ROLE-ROTATION-QUARTERLY (new in I32 P4) codifies the cadence from I26 P2 SOP-HLK_GOIPOI §6.1: all service_role keys rotate quarterly (last business day of each quarter; old keys revoked within 24h). The KiRBe sync job's service_role consumer must respect this cadence. Next rotation: 2026-06-30. Dashboard query: `SELECT * FROM compliance.policy_register_mirror WHERE policy_class='service_role_rotation' ORDER BY next_review`.

## Operator open question for KiRBe team

**Q6 (D-IH-32-Q6):** consumption pattern for the new mirrors — RLS read-only via Supabase (recommended; aligns with how `process_list_mirror` is consumed today) or versioned JSON snapshot? Reply on the GitHub PR thread to lock in.

## Cross-references

- Initiative 32 master roadmap: `docs/wip/planning/32-holistik-ops-maturation/master-roadmap.md`
- Updated `kirbe-sync-contract.md`: `config/sync/kirbe-sync-contract.md` (§2 rewritten + §11 new)
- KiRBe architecture audit (separate memo): `kirbe-architecture-audit-2026-04-30.md`
- 3-PR seed: `reports/external-repo-seed-prs/kirbe.patch` + bilingual cover-emails (D-IH-32-P)
- POLICY_REGISTER.csv: `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv`
- 6-axis Holistik Ops doctrine (v2): `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md`
