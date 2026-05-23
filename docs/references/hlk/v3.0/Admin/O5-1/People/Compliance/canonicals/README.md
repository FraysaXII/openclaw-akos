---
language: en
---

# HLK Compliance — directory layout and SSOT conventions

**Owner**: Compliance, Data Architecture (joint)  
**Status**: Forward layout convention (Initiative 22 P1, 2026-04-29)  
**Authority**: see [`PRECEDENCE.md`](PRECEDENCE.md) §"Layout convention (forward)" for the precedence ledger pointer.

This README documents the **forward** layout convention for canonical compliance assets so the directory does not flood as new initiatives add registers. **Existing files stay in place** for now (D-IH-1, Initiative 22) — the goal is a clean, scalable target plus a deprecation-alias map so reviewers always know *where a new register would go* even if a legacy register currently lives at the root.

> Treat this as a **convention SSOT**. The actual SSOT for individual registers is the row in `PRECEDENCE.md`. New initiatives must classify their canonical CSVs into one of the planes below and write them to the corresponding subfolder when they are introduced; legacy flat files may be migrated in their own dedicated initiative when the cost/benefit ratio flips.

## Three-axis taxonomy

Every governed compliance asset is keyed by **at most three** stable axes:

| Axis | Values (current) | Where it lives in the canonical row |
|:-----|:-----------------|:------------------------------------|
| **Plane** | `compliance` (cross-cutting), `finops`, `advops`, `techops`, `dimensions` (knowledge dimensions used across planes), `marops`, `devops` | Subfolder under `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/` (forward) |
| **Program / engagement** | `PRJ-HOL-FOUNDING-2026`, future `PRJ-HOL-*-YYYY` | `program_id` column on the canonical row (already present on Initiative-21 registers) |
| **Topic / register name** | e.g. `adviser_open_questions`, `filed_instruments`, `goipoi_register` | The CSV file basename and / or `topic_id` in the matching KM manifest |

Three axes are sufficient — deeper trees become role/topic concerns and live inside the register's own SOP, not in the directory layout.

## Forward layout (target)

```
docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/
├── README.md                                     (this file)
├── PRECEDENCE.md                                 (canonical precedence ledger)
├── SOP-META_PROCESS_MGMT_001.md                  (governing SOP for process registry)
├── HLK_KM_TOPIC_FACT_SOURCE.md                   (KM contract; cross-plane)
├── access_levels.md
├── confidence_levels.md
├── source_taxonomy.md
├── baseline_organisation.csv                     (cross-plane SSOT — stays at root)
├── process_list.csv                              (cross-plane SSOT — stays at root)
│
├── advops/                                       (External Adviser Engagement plane)
│   ├── ADVISER_ENGAGEMENT_DISCIPLINES.csv        (forward target — currently at root)
│   ├── ADVISER_OPEN_QUESTIONS.csv                (forward target — currently at root)
│   └── FILED_INSTRUMENTS.csv                     (forward rename target — currently FOUNDER_FILED_INSTRUMENTS.csv at root)
│
├── finops/                                       (Finance / counterparty plane)
│   └── FINOPS_COUNTERPARTY_REGISTER.csv          (MIGRATED 2026-05-23 per I81 P2 T1 / D-IH-81-Q under D-IH-81-G umbrella)
│
├── techops/                                      (CTO / component & service plane)
│   └── COMPONENT_SERVICE_MATRIX.csv              (relocated 2026-05-22 per D-IH-81-G-T5)
│
└── dimensions/                                   (cross-plane knowledge dimensions)
    ├── GOI_POI_REGISTER.csv                      (RELOCATED Initiative 32 P7, D-IH-32-D)
    ├── PROGRAM_REGISTRY.csv                      (Initiative 23)
    ├── TOPIC_REGISTRY.csv                        (Initiative 25)
    ├── PERSONA_REGISTRY.csv                      (Initiative 31 P2.1)
    ├── CHANNEL_TOUCHPOINT_REGISTRY.csv           (Initiative 31 P3)
    ├── SOURCING_REGISTER.csv                     (Initiative 31 P5.2)
    ├── POC_TO_COMMERCIAL_MAP.csv                 (Initiative 29 P4)
    ├── SKILL_REGISTRY.csv                        (Initiative 32 P2, D-IH-32-B)
    ├── TOUCHPOINT_KIT_CELL_REGISTRY.csv          (Initiative 32 P3, D-IH-32-C)
    └── POLICY_REGISTER.csv                       (Initiative 32 P4, D-IH-32-Q4)
```

**Why `dimensions/` exists.** A *dimension* is a register that is FK-target for two or more planes (e.g. `GOI_POI_REGISTER.csv` joins ADVOPS open questions, ADVOPS filed instruments, future MKTOPS lead routing, future FINOPS counterparty enrichment). Putting it under any single plane would imply ownership it does not have.

**Why `process_list.csv` and `baseline_organisation.csv` stay flat.** They are the cross-plane registry; every plane references them; nesting them would invert the precedence ladder. They remain at the compliance root.

## Deprecation alias map (current ↔ forward)

| Current path (do not move yet) | Forward path | Deferral rationale |
|:-------------------------------|:-------------|:-------------------|
| ~~`compliance/GOI_POI_REGISTER.csv`~~ **MOVED I32 P7** | `compliance/dimensions/GOI_POI_REGISTER.csv` | **Relocated 2026-04-30 per D-IH-32-D**. Legacy path supported via deprecation alias in `validate_goipoi_register.py` and `sync_compliance_mirrors_from_csv.py` for **one initiative cycle**; alias to be removed in I33. |
| `compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv` | `compliance/advops/ADVISER_ENGAGEMENT_DISCIPLINES.csv` | Single-plane register; physical move deferred to FINOPS / ADVOPS expansion initiative |
| `compliance/ADVISER_OPEN_QUESTIONS.csv` | `compliance/advops/ADVISER_OPEN_QUESTIONS.csv` | Same as above |
| `compliance/FOUNDER_FILED_INSTRUMENTS.csv` | `compliance/advops/FILED_INSTRUMENTS.csv` | Rename + move; file name still encodes "founder" — should be program-keyed via `program_id` column instead |
| ~~`compliance/FINOPS_COUNTERPARTY_REGISTER.csv`~~ **MIGRATED I81 P2 T1** | `compliance/finops/FINOPS_COUNTERPARTY_REGISTER.csv` | **Relocated 2026-05-23 per D-IH-81-Q under D-IH-81-G umbrella** (FINOPS synthesis gated the move; T1 advance ratified after operator inline-ratify of q1-a + q2-a + q5-a). Legacy path supported via deprecation alias in `validate_finops_counterparty_register.py`, `sync_compliance_mirrors_from_csv.py`, `validate_review_stamps.py` for **one initiative cycle**; alias to be removed at I81 P9 closure. |
| `compliance/COMPONENT_SERVICE_MATRIX.csv` | `compliance/techops/COMPONENT_SERVICE_MATRIX.csv` | **Migrated 2026-05-22 (D-IH-81-G-T5 / I81 P2 Tranche T5)**; deprecation alias supported in validators for one initiative cycle (to be removed at I81 P9 closure) |

**Aliasing during migration.** When a register is physically moved, the moving initiative must:

1. Use `git mv` (preserves history).
2. Update **every** reference in: `PRECEDENCE.md`, `akos/hlk_*_csv.py`, `scripts/validate_*.py`, `scripts/validate_hlk.py`, `scripts/sync_compliance_mirrors_from_csv.py`, `supabase/migrations/*.sql` comments, `scripts/sql/*_staging/*.sql`, the corresponding maintenance SOP, `tests/test_*`, plus any vault MD that resolves the file by relative path.
3. Re-run `py scripts/validate_hlk.py` and `py scripts/validate_hlk_vault_links.py`.
4. Document the move in the initiative's `decision-log.md` as a deprecation alias closure.

## When to add a new plane

- The new plane has **at least one** canonical CSV register **and** a corresponding maintenance SOP.
- It is reflected in `akos-holistika-operations.mdc` "Holistika operations planes" table.
- It has a cursor rule under `.cursor/rules/akos-<plane>.mdc` (or is folded into an existing one with explicit globs).
- New CSVs go directly into `compliance/<plane>/`; no flat-root variant is created.

## Cross-references

- KM directory contract: [`docs/references/hlk/v3.0/_assets/README.md`](../v3.0/_assets/README.md) (Initiative 22 P2)
- Vault role × program convention: [`docs/references/hlk/v3.0/index.md`](../v3.0/index.md) §"Program-scoped casework" (Initiative 22 P3)
- Initiative 22 master roadmap: [`docs/wip/planning/22-hlk-scalability-and-i21-closures/master-roadmap.md`](../../../wip/planning/22-hlk-scalability-and-i21-closures/master-roadmap.md)
- Operations planes cursor rule: [`.cursor/rules/akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc)
- ADVOPS plane cursor rule: [`.cursor/rules/akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc)
