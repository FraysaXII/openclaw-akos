---
language: en
status: draft
initiative: 32-holistik-ops-maturation
report_kind: external-team-architecture-audit
program_id: shared
plane: ops
authority: Founder + System Owner + AI Engineer
last_review: 2026-04-30
audience: ERP team lead + ERP engineering
---

# ERP architecture audit (Initiative 32 P8)

**Date:** 2026-04-30
**Scope:** Audit of `hlk-erp` against the AKOS HLK doctrine + the new I31 / I32 governance substrate.
**Source materials read:** `c:\Users\Shadow\cd_shadow\root_cd\hlk-erp\README.md`, `hlk-erp/.cursor/rules/index.mdc`, `architecture.mdc`, `data-ssot.mdc`, `documentation/README.md`, plus REPO_HEALTH_SNAPSHOT for `hlk-erp` (2026-04-30; 13 cursor rules, 0% language-frontmatter, 23 brand-jargon violations, no contract yet).

## Executive summary

ERP is a Next.js 14 + React + shadcn/ui + Tailwind + Supabase + FastAPI shell. Smaller and earlier-stage than KiRBe but architecturally clean. Two latent drifts threaten the cross-repo discipline: a local `data-ssot.mdc` cursor rule that contradicts AKOS PRECEDENCE.md (E13), and stale snapshots of KiRBe + AKOS HLK content under `other_documentation/` (E14). Both are addressable without disrupting your stack.

## 6 architecture-level deltas (recommendations on a non-blocking timeline)

### Delta 1 — Adopt language frontmatter (Brand-owned policy)

**What:** every new canonical MD in `hlk-erp` declares `language: en|es|fr` per AKOS `SOP-HLK_LOCALISATION_001.md` (relocated to Marketing/Brand in I32 P7). Existing files migrate on a non-blocking timeline.

**Why:** REPO_HEALTH_SNAPSHOT 2026-04-30 reports 0% compliance. The audience-canonical exception (D-IH-31-A) applies to ES-targeted ERP screens.

**Cost:** trivial. One frontmatter block per new file.

### Delta 2 — Adopt the akos-mirror cursor rule (Q10 supersession path)

**What:** land `.cursor/rules/akos-mirror.mdc` from the I32 P7 PR patch. This rule is `alwaysApply: true` and reminds every cursor session that AKOS is SSOT for HLK doctrine. It **takes precedence** over the local `data-ssot.mdc` for HLK content (Q10 supersession) without rewriting `data-ssot.mdc`.

**Why:** today `data-ssot.mdc` says "Centralize in `lib/*`" — directly contradicting AKOS PRECEDENCE.md which says canonical CSVs are in `docs/references/hlk/compliance/` (in AKOS). New ERP contributors writing HLK-related features against `lib/` SSOT is a real risk; the cursor rule supersession closes it without a `data-ssot.mdc` rewrite.

**Cost:** zero (the file ships in the I32 P7 PR patch). Future `data-ssot.mdc` rewrite or removal is Initiative 44 (deferred).

### Delta 3 — Replace `other_documentation/kirbe/` with a pointer file

**What:** archive the 50+ files under `other_documentation/kirbe/supabase_queries/` and `other_documentation/kirbe/kirbe_sops/` (stale snapshots of KiRBe content). Replace with a 1-page pointer file linking to the live KiRBe repo at `https://github.com/FraysaXII/kirbe`.

**Why:** stale snapshots create 3-way drift risk. KiRBe ships features daily; the snapshots in this folder are weeks behind. Pointer is always current.

**Cost:** ~½ day to archive + write the pointer.

### Delta 4 — Replace `other_documentation/hlk/documentation-hlk/` with a pointer file

**What:** same pattern. Archive the AKOS HLK content snapshot. Replace with a 1-page pointer linking to AKOS `docs/references/hlk/v3.0/`.

**Why:** AKOS HLK doctrine is SSOT in AKOS, not in your repo. Snapshot here is by definition stale.

**Cost:** ~½ day.

### Delta 5 — ERP screens read mirrors via Supabase views, not from `lib/types.ts`

**What:** every ERP screen that displays org / process / role / dimension data reads from a Supabase view projecting the appropriate `compliance.*_mirror`, not from `lib/types.ts` as SSOT.

**Why:** `lib/types.ts` and `lib/supabase-types.ts` are valuable as TypeScript snapshots (auto-regenerated; treat as snapshot per AKOS PRECEDENCE.md "Mirrored / derived assets" §`supabase.ts` typings). They are NOT SSOT for organisational truth. Reading from views ensures the ERP screen reflects the latest canonical CSV without redeploy.

**Cost:** as encountered. New screens written this way; existing screens migrated when touched.

### Delta 6 — Adopt the 5-axis integration spec

**What:** every "humans list" screen gains a persona filter, a distance-band column, and an optional channel-tag join. Per `02-five-axis-integration-spec.md` in the I32 P8 handoff bundle.

**Why:** integrates ERP with the new I31 governance substrate without inventing local conventions.

**Cost:** ~1 day per screen modernised. Apply opportunistically.

## 5 things to NOT change

1. **Next.js App Router patterns** — preserved per `architecture.mdc`.
2. **shadcn/ui + Tailwind theme tokens** — visual identity is OK as-is; AKOS does not override.
3. **The chart-wrapper-enforcement rule** (`use ChartContainer/Tooltip/Legend from components/ui/chart.tsx`) — preserved.
4. **Supabase Auth integration** — out of scope for I32; ERP team's domain.
5. **The `hooks/`, `components/`, `lib/` directory pattern** — preserved.

ERP prod-readiness gates 1-3 (auth, tenancy RLS, rollback runbook) ship as a separate **Initiative 33** — out of scope for I32.

## Operator action

ERP team lead: review this audit + the 7-file handoff bundle + the 3-PR seed (`hlk-erp.patch`). Reply with feedback on the 6 deltas + Q10 supersession recommendation, or "schedule against your roadmap".

## Cross-references

- ERP repo README: `https://github.com/FraysaXII/hlk-erp/blob/main/README.md`
- ERP handoff bundle (sibling folder): `erp-handoff-bundle-2026-04-30/`
- 3-PR seed: `external-repo-seed-prs/hlk-erp.patch` + bilingual cover-emails
- Q10 (data-ssot supersession), D-IH-32-K (cross-repo contract), D-IH-32-E (localisation SOP relocation)
- Initiative 33 (deferred): ERP prod-readiness gates 1-3
- Initiative 44 (deferred): `data-ssot.mdc` rewrite after a clean quarter under supersession
