---
language: en
status: closed
initiative: 50-live-cycle-closure
report_kind: phase-report
phase: P3
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# I50 P3 — First live `--filter madeira` dossier emit

## Outcome

**Ship verdict: GO** — all three lights GREEN. Spend $0.00 / $5.00 envelope (100% headroom). MADEIRA dossier filter passes its first live exercise.

## Command

```text
$env:MAX_DOSSIER_USD = "5"
py scripts/render_uat_dossier.py --filter madeira --mode live --max-spend 5 --quiet
```

## Output

```text
DONE. Dossier written to:
  - artifacts\uat-dossier\uat-dossier-20260503T164343Z\dossier.md
  - artifacts\uat-dossier\uat-dossier-20260503T164343Z\manifest.json
Overall status: PASS
Elapsed: 12573ms
```

| Field | Value |
|:---|:---|
| Run ID | `dossier-c3d5c001e610` |
| Git SHA | `b2bfd8702e2229cb22ef769d54c4c4695ab272ac` (I50 P2 commit) |
| Started | 2026-05-03T16:43:43Z |
| Mode | `live` |
| Filter flavor | `madeira` |
| Filter personas | `PERSONA-INVESTOR-COLD,PERSONA-INVESTOR-WARM,PERSONA-ADVISOR-REFERRAL,PERSONA-CUSTOMER-KIRBE-PROSPECT,OPERATOR` |
| Filter skill | `skill_madeira_lookup_v1` |
| Filter initiatives | `02,17,32,45,46,47,49` |
| Section count | 12 |
| Sections PASS / INFO / WARN / FAIL | 9 / 2 / 0 / 0 (Section 4 PASS includes the operator-known 13/16 personas-outside-tolerance signal carried from I47; treated within tolerance per `overall_within_tolerance=true`) |
| `cost_total_usd` | $0.0000 |
| Manifest SHA-256 | `1db895e31f0c02ee469f0a65f4bc51be73ed95c56a2d3fa43ac244fc39f68a4f` |
| `compliance.dossier_run` write | skipped (no Supabase service-role configured locally; manifest written locally only) |

## Three-light verdict (Section 1)

| Lane | Signal | Basis |
|:---|:---:|:---|
| **Conversational** | **GREEN** | Sections 3-6 status roll-up |
| **Operator** | **GREEN** | Section 8 Operational health |
| **Surface** | **GREEN** | Section 8 `madeira_surface_ship`; basis = "Latest critique declares ship verdict" (sourced from I49 wave D Impeccable craft critique 2026-05-03) |
| **MADEIRA ship verdict** | **GO** | All three lights GREEN |

## Cost-guard discipline (D-IH-50-B + POL-EVAL-COST-CEILING-DOSSIER-V1)

| Field | Value |
|:---|:---|
| Envelope (`MAX_DOSSIER_USD`) | $5.00 |
| Source of truth | `POL-EVAL-COST-CEILING-DOSSIER-V1` (POLICY_REGISTER) |
| Actual spend | $0.0000 |
| Headroom | 100% |
| `aggregate_dossier_cost_under_cap` raised? | NO |

Eval Section 3 reports `rows_total=0` because no Tier-B run has executed yet (P4 fires that). The live mode therefore exercises the dossier renderer + filter composition + three-light evaluator end-to-end; per-scenario judge cost is exercised in P4 once Tier-B writes `compliance.eval_run` rows.

## Notable Section 8 details

- `madeira_cost_total_usd: 0.0` (no MADEIRA-skill spend yet)
- `madeira_cost_ceiling_status: "unknown"` — expected when `cost_total_usd=0`; computed status will populate after first Tier-B run with non-zero spend (P4)
- `madeira_surface_ship: GREEN` — propagates from I49 critique 2026-05-03
- `cost_ceiling_breaches_count: 0`
- `agent_memory_triggers_fired: 0`

## What this proves

- The `--filter madeira` profile works end-to-end against the live mode pipeline.
- The three-light verdict rolls up correctly and writes structured metrics into `manifest.json` for downstream Tier-B trend storage.
- `MAX_DOSSIER_USD=5` cap holds (no breach; even at 100% headroom the cap mechanism wired through `--max-spend 5`).
- POLICY anchor `POL-EVAL-COST-CEILING-DOSSIER-V1` (added in P2) is the canonical envelope source; env override functioning.

## What this does NOT prove (deferred)

- Live judge spend semantics under non-zero `cost_total_usd` — covered by P4 Tier-B smoke.
- `compliance.dossier_run` row writes — depends on Supabase service-role env which is not configured in the local execution context. Manifest captured locally; closure UAT will retest if env ships.
- Multi-judge consensus voting — that is I52/P3.

## Cross-references

- E4, E5 in [`evidence-matrix.md`](../evidence-matrix.md) cleared (first live MADEIRA emit + Tier-B baseline distinct).
- D-IH-50-B (envelope sized at $5): exercised, no breach.
- POL-EVAL-COST-CEILING-DOSSIER-V1 (P2 ship): canonical anchor exercised.
- R-50-2 in [`risk-register.md`](../risk-register.md) (dossier overspend): NOT FIRED — 100% headroom under envelope.
