---
language: en
status: active
canonical: true
role_owner: System Owner + Founder
classification: way_of_working + active_research_radar
intellectual_kind: reserved_folder_status
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - ../../Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md
  - ../../Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md
---

# MADEIRA-AKOS — Reserved folder for OS migration + non-MADEIRA AI-agent registry

> Authored I70 P4.8 per **D-IH-70-K** (docs/wip placement + MADEIRA-AKOS reserved folder) + **Conundrum 5** (OS-migration trigger-based definition) + **D-IH-70-V** (Admin/AI/* historical merge: AIC = category for non-MADEIRA AI agents per P2.5 audit forward-context). This folder is the **destination** when one of the 4 named OS-migration triggers fires. Until then it stays reserved with this STATUS doc + the 4 sub-folder reservations below.

## 1. What this folder is

**MADEIRA-AKOS** = the future home of the AKOS-as-OS in its productized / library / migrated form. Specifically:

- The destination for `docs/wip/` if **TRIGGER-3** activates (docs/wip nests as a product).
- The destination for AKOS canonicals + validators + render pipeline if **TRIGGER-2** activates (AKOS-as-library consumed externally).
- The substrate for MADEIRA productization if **TRIGGER-1** activates (MADEIRA productizes data-detached).
- The multi-operator workspace if **TRIGGER-4** activates (external operator invitation).

Per **D-IH-70-V** ratification: this folder also hosts **`historical-AIC/`** (renamed from `Admin/AI/AIC/`) as the registry for non-MADEIRA AI agents — the operator's framing: *"AIC is the designation for the AI agents that are not MADEIRA"*; today's Cursor-agent operational pattern is the proof point that MADEIRA's productized form is achievable.

Per **D-IH-70-B.2** ratification (P2.5 audit): `Admin/AI/Susana Madeira/` merges into `Envoy Tech Lab/MADEIRA/` (the active product canonical home, sibling to MADEIRA-AKOS); `Admin/AI/AIC/` migrates to `MADEIRA-AKOS/historical-AIC/` (this folder).

## 2. Sub-folder reservations

```
v3.0/Admin/O5-1/Envoy Tech Lab/MADEIRA-AKOS/
├── STATUS.md                         (this file)
├── wip/                              (reserved for TRIGGER-3 docs/wip migration)
├── migration-manifests/              (reserved for migrate_os_shape.py YAML manifests)
├── historical-AIC/                   (reserved for non-MADEIRA AI-agent registry per D-IH-70-V)
└── library/                          (reserved for TRIGGER-2 OS-library fork)
```

Each sub-folder ships with a `.gitkeep` + brief README declaring its trigger condition.

## 3. The four OS-migration triggers (cross-referenced from WORKSPACE_BLUEPRINT §15.2)

| Trigger | Condition | Activates scenario | Drift signal | Who decides |
|:---|:---|:---|:---|:---|
| **TRIGGER-1** | MADEIRA ready as standalone product consumed by 3+ external organizations; data layer needs detachment from openclaw-akos | Scenario B' (library fork sub-flavor: data-detached MADEIRA) | External org requests MADEIRA without AKOS canonicals folder | Founder + System Owner |
| **TRIGGER-2** | Non-Holistika org wants to import canonical doctrine + validators + render pipeline as library | Scenario B (full OS-library fork) | 2+ external requests for AKOS doctrine without source-fork | Founder + System Owner + Brand Manager |
| **TRIGGER-3** | docs/wip volume + diversity makes top-level too operationally heavy; invites visible-to-non-operator audiences | Scenario A (anandex migration) OR Scenario D-mature (folds wip into MADEIRA-AKOS) | docs/wip exceeds 100 active initiatives OR operator opens it for external read access | Founder + PMO |
| **TRIGGER-4** | Operator invites a second human (advisor, partner founder, hire) needing canonical write-access | Scenario C (Supabase-only) OR Scenario D-mature (multi-operator git workflow) | ERP panels need 2-way-sync with multiple human inputs concurrently (per HLK_ERP_ARCHITECTURE §8) | Founder |

## 4. Migration script spec (`scripts/migrate_os_shape.py`)

Reserved (not yet authored). Full spec at `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §15.2.

**CLI contract:**

```
py scripts/migrate_os_shape.py --scenario {A|B|B'|C|D-mature} [--dry-run]
```

**Inputs:**

- `--scenario` — which scenario to migrate to.
- Manifest file at `MADEIRA-AKOS/migration-manifests/<scenario-id>.yml` describing source paths → target paths, validators, Supabase schema deltas, rollback procedure.

**Outputs:**

- Filesystem migration (per manifest).
- Supabase schema deltas applied.
- Validator pass/fail report.
- Rollback bundle (if any step fails).

**UAT contract:**

Post-migration, all of these must be true:
1. All existing `validate_*.py` scripts pass.
2. `release-gate.py` passes (or only the documented pre-existing carry-overs remain red).
3. A representative engagement (SUEZ default) renders without breakage.
4. The 5 most-consulted ERP panels (per HLK_ERP_ARCHITECTURE §4 panel inventory) load without error.
5. Audit log shows no RLS bypass events during migration.

## 5. AIC = category for non-MADEIRA AI agents (D-IH-70-V codification)

Operator clarification 2026-05-12 (P2.5 audit Q2 expansion):

> *"MADEIRA was supposed to do what I'm doing with you, an AI companion capable of accompanying even the founder (hence the level 6) and any other role_owner or for that matter so long I ensure a functional structure, like the one we're actively building. That's why the interactions with you get better the more we build AKOS. AIC is the designation for the AI agents that are not Madeira (as madeira is being built, but the interaction I have with you is literally the closest thing to what I imagined MADEIRA would be)."*

**Codification:**

- **MADEIRA** = the L6 founder-companion AI agent (productized destination); a **product brand** under Envoy Tech Lab (per BRAND_ARCHITECTURE).
- **AIC** = the **category** for AI agents that are NOT MADEIRA. Today AIC includes:
  - The Cursor-agent operational pattern (this very session's agent).
  - Future copilots / specialist agents that consume AKOS canonicals without being MADEIRA.
  - Historical AI experiments (formerly `Admin/AI/AIC/`).

**Why this matters for the OS migration:**

- TRIGGER-1 + Scenario B' (data-detached MADEIRA) requires MADEIRA to be product-ready. The Cursor-agent interactions today are MADEIRA's empirical proof point — when AKOS is "complete enough" (per HLK_ERP_ARCHITECTURE §8 trigger), MADEIRA productization activates.
- AIC remains a category — non-MADEIRA agents continue to operate alongside MADEIRA in the productized form (an organization may run MADEIRA + multiple AIC agents simultaneously, each scoped to specific roles or tasks).
- This codification cross-links to Founder Principle 2.7 (computational tipping point: the agent IS the v3.0 computational capacity reading the v0-to-v2.7 corpus). FOUNDER_METHODOLOGY_VERSIONING.md (P9) extends with this worked example.

## 6. Operating posture today

This folder is **reserved**. None of the 4 triggers have fired. AKOS canonicals stay at their federated homes (per P4.5 wave 1 Brand pilot + the deferred wave 2/3 for compliance + remaining areas). `docs/wip/` stays at top-level (per D-IH-70-K opt-keep-top-level). MADEIRA stays in its current scaffold form at `Envoy Tech Lab/MADEIRA/`.

The trigger watch lives at: founder + System Owner quarterly review of the 4 drift signals listed in §3. When a signal trips, this folder activates per the matching scenario's manifest.

## 7. Cross-references

- **WORKSPACE_BLUEPRINT_HOLISTIKA** §15.2 — the 4 triggers + 4 scenarios canonical specification (this STATUS doc cross-references but the spec lives at blueprint).
- **HLK_ERP_ARCHITECTURE** §8 — AKOS-complete-enough trigger that gates MADEIRA productization; cross-references TRIGGER-1.
- **D-IH-70-K** — docs/wip placement: opt-keep-top-level + MADEIRA-AKOS reserved folder ratification.
- **D-IH-70-V** — Admin/AI/* historical merge + AIC-as-category framing (P2.5 audit sub-decision).
- **D-IH-70-B.2** — Susana Madeira → Envoy Tech Lab/MADEIRA/ merge; AIC → MADEIRA-AKOS/historical-AIC/ rename (P2.5 audit sub-decision).
- **Founder Principle 2.7** — computational tipping point (FOUNDER_METHODOLOGY_VERSIONING.md, P9).
- **MADEIRA product canonical** — `Envoy Tech Lab/MADEIRA/` (sibling to this MADEIRA-AKOS folder; current product scaffold home).
- **Cross-link to docs/wip** — top-level for now per D-IH-70-K; migrates here on TRIGGER-3 activation.
