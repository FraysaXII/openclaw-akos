---
language: en
status: draft
initiative: 32-holistik-ops-maturation
report_kind: external-team-pointer
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-04-30
audience: ERP team engineering
---

# TEAM_SOTA_HLK_ERP — pointer

The canonical "state of the art" instructions for the ERP team live at:

`docs/wip/planning/14-holistika-internal-gtm-mops/reports/TEAM_SOTA_HLK_ERP.md`

GitHub link: `https://github.com/FraysaXII/openclaw-akos/blob/main/docs/wip/planning/14-holistika-internal-gtm-mops/reports/TEAM_SOTA_HLK_ERP.md`

## Standalone

This document is **standalone**. It is sufficient to operate the ERP repo without opening the Initiative 14 cursor plan. It covers:

1. Purpose of the ERP shell (operator UI; not a replacement for canonical CSVs)
2. Data rules (read from Supabase views projecting `compliance.*_mirror`; never hand-edit production rows as SSOT)
3. SQL and migrations (operator SQL gate workflow)
4. Schema map (compliance / holistika_ops / kirbe / public legacy)
5. Auth (OAuth/OIDC or Supabase Auth)
6. Local dev
7. Release order (CSV merge + validator → mirror ingest → ERP deploy → cutover legacy reads)
8. Security
9. Related repositories

## Initiative 32 P10 extensions (deferred to TEAM_SOTA_HLK_ERP next-rev)

The audit memo recommends three additions to TEAM_SOTA_HLK_ERP:

- **§10 EXTERNAL_REPO_CONTRACT pointer** — confirm the contract is at the repo root + cite D-IH-32-K
- **§11 data-ssot rule supersession note** — explain Q10 supersession (akos-mirror.mdc takes precedence over local data-ssot.mdc for HLK content)
- **§12 cross-Neo4j note** (parity with KiRBe TEAM_SOTA §13) — clarify ERP does NOT have its own Neo4j; AKOS Neo4j is the governance projection ERP can read

These extensions will land in TEAM_SOTA_HLK_ERP after the ERP team merges the I32 P7 PR patch. They are deferred from the bundle itself to keep the bundle pure-pointer (the bundle does not modify TEAM_SOTA_HLK_ERP; it points at it).

## Cross-references

- TEAM_SOTA_KIRBE.md: `docs/wip/planning/14-holistika-internal-gtm-mops/reports/TEAM_SOTA_KIRBE.md` (companion for the KiRBe team)
- ERP architecture audit memo (sibling): `../erp-architecture-audit-2026-04-30.md`
- Initiative 33 (deferred): ERP prod-readiness gates 1-3 (auth, tenancy RLS, rollback runbook)
