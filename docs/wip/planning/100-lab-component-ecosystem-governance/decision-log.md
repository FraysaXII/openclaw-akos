---
language: en
status: active
intellectual_kind: decision_log
initiative: INIT-OPENCLAW_AKOS-100
authored: 2026-06-14
last_review: 2026-06-14
role_owner: System Owner
---

# I100 — Decision Log

## P0 inception (2026-06-14)

### D-IH-100-A — Adopt Supabase EG pattern as lab-wide component doctrine

**Decision.** Mint **Lab Component Ecosystem Governance** under Tech/System Owner — umbrella doctrine + `COMPONENT_MODULE_REGISTRY.csv` classifying all 110 matrix rows. Do **not** mint one SOP per matrix row or standalone per-vendor SOPs that duplicate `SOP-CICD_BASELINE_001` / `SOP-TECH_LAB_PLATFORM_BINDING_001`.

**Parent:** I95 HCAM L2 (`D-IH-95-G` Supabase EG is the worked template).

**Evidence:** Internal sweep — matrix 110 rows, I99 folder, BT-10 lab binding tranche, Vercel dashboard audit (2026-06-13/14).

---

### D-IH-100-B — Wave-1 vendors = Vercel + Cloudflare + GitHub

**Decision.** Wave-1 dimension registries cover the lab critical path hosting stack before Wave-2 observability/RPA vendors.

**Registry gate (PAUSE POINT #2):** Canonical CSV mint in P2 — operator approval recorded at implementation per full-plan ratify.

---

### D-IH-100-C — Governance depth D0–D3 taxonomy

**Decision.** Every matrix row maps to exactly one depth: D0 inventory, D1 doc trace, D2 dimension registry, D3 full ecosystem. Aliases (`alias_of=` in notes) remain D0 inventory FKs pointing at canonical row.

**Baseline at P1 close:** 110 module rows — 6 D3 · 7 D2 · 15 D1 · 82 D0 (includes 10 alias rows).

---

### D-IH-100-D — Matrix FK via notes-first (no new column at P2)

**Decision.** Prefer `alias_of=` and `ecosystem_module_id` references in matrix **notes** until a dedicated column passes canonical CSV gate. Full dedupe scheduled P4.

---

### D-IH-100-E — Unified lab platform registry validator

**Decision.** Single `validate_lab_platform_registries.py` for Wave-1 + Wave-2 dimension CSVs (row count < 80 combined); per-vendor split deferred unless row count exceeds maintainability threshold.

---

### D-IH-100-F — I100 parallel to I96 (not spine replacement)

**Decision.** I100 runs **parallel** to I96 Preview UAT completion. P5 wires probes to I96 evidence; I100 closure does not require I96 PASS (I96 may remain PASS-WITH-FOLLOWUP).

---

### D-IH-100-G — Supabase family owned by I99; indexed by I100 module registry only

**Decision.** `module_family=supabase` rows link to `SUPABASE_MODULE_REGISTRY.csv` and `SUPABASE_ECOSYSTEM_GOVERNANCE.md` — no duplicate Supabase umbrella under I100.

---

### D-IH-100-H — Component Doc Trace + Research Radar field reuse

**Decision.** §4 of umbrella doctrine mints Component Documentation Trace; reuse `volatility_class` + `next_verify_by` from Research Radar discipline on module registry rows.

**Evidence:** [`../../intelligence/lab-component-ecosystem-governance-2026-06-14/research-synthesis-wave1-2026-06-14.md`](../../intelligence/lab-component-ecosystem-governance-2026-06-14/research-synthesis-wave1-2026-06-14.md)

**External citations:** Vercel [Shared Responsibility Model](https://vercel.com/docs/security/shared-responsibility); Cloudflare [DNS records](https://developers.cloudflare.com/dns/manage-dns-records/); GitHub [deployment protection](https://docs.github.com/en/actions/deployment/about-deployments/deploying-with-github-actions).

---

### D-IH-100-CLOSURE — I100 closure ratification (P8)

**Decision.** Accept I100 P0–P8 deliverables: umbrella + 110-row module registry, Wave-1/2 dimension registries, HCAM triples, maintenance SOP draft, I96 probe pointers, carryover propagation for Wave-3 long tail and Pro-trial features.

**Verdict target:** PASS-WITH-FOLLOWUP if live alias re-point or Supabase credential tier still open in I96 — registry SSOT is complete regardless.

**Evidence:** [`reports/uat-i100-lab-component-ecosystem-governance-2026-06-14.md`](reports/uat-i100-lab-component-ecosystem-governance-2026-06-14.md)

---

### D-IH-100-REOPEN — Premature closure; harmonization tranche required (2026-06-14)

**Trigger.** Operator review: minted vault reads unharmonized vs `DATA_GOVERNANCE_POLICY.md`, OPS_REGISTER cross-initiative demand, and research-action bar (ledger was 7 rows; validators do not prove live intent).

**Decision (pending ratification).** Reopen I100 for harmonization tranche **P9** — not a full P0 rewind. Mechanical P0–P8 artifacts remain; closure verdict superseded until `D-IH-100-I` + harmonization UAT.

**Evidence pack:** [`../../intelligence/lab-component-ecosystem-governance-2026-06-14/harmonization-proposal-2026-06-14.md`](../../intelligence/lab-component-ecosystem-governance-2026-06-14/harmonization-proposal-2026-06-14.md)

**Research ledger:** 780 rows PASS (`source-ledger.csv`, 2026-06-14 regenerate).

---

### D-IH-100-I — Lab platform dimension lexicon + registry consolidation (PENDING)

**Proposal.** Data Governance Office owns `dimension_kind` lexicon; consolidate Wave-1/2 CSVs into `LAB_PLATFORM_DIMENSION_REGISTRY.csv`. See harmonization proposal §1–2.

**Gate:** Operator AskQuestion ratification before canonical CSV mint.
