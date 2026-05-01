---
language: en
status: draft
audience: ERP team lead + ERP engineering
delivery_method: GitHub PR thread + email to lead
---

**Subject:** [Holistika Ops] hlk-erp seed PR + architecture audit + handoff bundle

Hi team,

Initiative 32 in the AKOS repo includes three deliverables for the hlk-erp side:

**1. PR patch (2 files)** — see `hlk-erp.patch` in the I32 reports folder.

The patch ships a 1-page `EXTERNAL_REPO_CONTRACT.md` for your repo root and a small `akos-mirror.mdc` cursor rule for `.cursor/rules/`. Both files are derived from AKOS canonical templates; the contract is non-prescriptive on your Next.js / shadcn / Tailwind / Supabase / FastAPI stack.

**2. Architecture audit memo** — `erp-architecture-audit-2026-04-30.md`.

We read your README, your 13 cursor rules, and your `documentation/` folder. The audit notes two latent drifts:

- Your local `data-ssot.mdc` cursor rule says "Centralize in `lib/*`" but AKOS PRECEDENCE.md says canonical CSVs are in `docs/references/hlk/compliance/` (which lives in AKOS, not in your repo). Recommendation: the new `akos-mirror.mdc` takes precedence over `data-ssot.mdc` (Q10 supersession path); keep `data-ssot.mdc` for non-HLK constants/types only. Initiative 44 (deferred) will rewrite or remove `data-ssot.mdc` after a clean quarter under supersession.
- `other_documentation/kirbe/` and `other_documentation/hlk/documentation-hlk/` are stale snapshots. Recommendation: archive them and replace with pointer files linking to AKOS and KiRBe SSOT.

**3. ERP handoff bundle** — `erp-handoff-bundle-2026-04-30/` folder with 7 files.

The bundle gives the ERP team the read-side map: schema map of all 16 compliance mirrors with example queries (`01-mirror-schema-map.md`), a 5-axis integration spec for ERP screens (`02-five-axis-integration-spec.md`), pointer to the operator SQL gate runbook (`03`), pointer to the relocated localisation policy SOP (`04`), changelog snippet for the ERP team (`05`), pointer to `TEAM_SOTA_HLK_ERP.md` (`06`).

**What we need from you, in order:**

1. Review the PR patch + memo + bundle. Reply with feedback or "merge as-is".
2. Confirm the Q10 supersession recommendation (akos-mirror.mdc takes precedence) is acceptable for your team, or propose an alternative.
3. Merge the patch when comfortable.

**What we explicitly are NOT asking you to change:**

- Next.js App Router patterns and the `chart-wrapper-enforcement` rule.
- shadcn / Tailwind theme tokens and visual identity.
- Supabase Auth integration.
- Your existing `hooks/`, `components/`, `lib/` directory pattern.

ERP prod-readiness gates (auth, tenancy RLS, rollback runbook) ship as a separate Initiative 33 — out of scope here, but on the roadmap.

Best,

— Holistika AKOS governance (Founder + System Owner)

---

**Cross-references:**

- AKOS repo: https://github.com/FraysaXII/openclaw-akos
- ERP handoff bundle: `docs/wip/planning/32-holistik-ops-maturation/reports/erp-handoff-bundle-2026-04-30/`
- HLK PRECEDENCE.md: `docs/references/hlk/compliance/PRECEDENCE.md`
- Initiative 33 (deferred): ERP prod-readiness gates
