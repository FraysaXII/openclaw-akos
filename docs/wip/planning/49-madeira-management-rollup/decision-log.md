---
language: en
status: active
initiative: 49-madeira-management-rollup
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 49 — Decision log

## Pre-seeded decisions (plan baseline)

| ID | Question | Decision |
|:---|:---|:---|
| D-IH-49-A | UC-rank as canonical CSV fields on `PERSONA_SCENARIO_REGISTRY`? | YES — operator approval gated before CSV merge |
| D-IH-49-B | `process_list` workstream parent? | `env_tech_ws_madeira_quality` under MADEIRA Platform `env_tech_prj_3` |
| D-IH-49-C | Extend `lifecycle_status` with `quarantined`? | YES |
| D-IH-49-D | Surface UX scope in I49? | Critique + redesign (Impeccable shape and craft); a11y + i18n |
| D-IH-49-E | Dossier filter implementation? | CLI `--filter madeira`; Section 1 and Section 8 specialize for MADEIRA flavor; preserves 12-section order |
| D-IH-49-F | Telemetry promotion auto-merge to CSV? | NO — emits JSON proposals only; operator reviews |
| D-IH-49-G | New process `item_id` pattern? | `env_tech_dtp_madeira_<verb>` |
| D-IH-49-H | 18 commits vs wave PR split? | **Single implementation branch** commits batched per phase where practical; reviewer may squash by wave |

---

## Execution updates

_Use this subsection for phased ratifications logged during Implementation._

- **2026-05-03 (D-IH-49-B)** — Operator-approved `process_list.csv` tranche: workstream **`env_tech_ws_madeira_quality`** plus six **`env_tech_dtp_madeira_*`** processes anchored to MADEIRA Platform (`env_tech_prj_3`), aligned vault SOPs land in Initiative 49 P6.
- **2026-05-03 (D-IH-49-C)** — `lifecycle_status` enum extended to **`{active, deprecated, scaffold, quarantined}`** in `akos/hlk_persona_scenario_csv.py` and validator. `scripts/quarantine_scenario.py` emitted as the deterministic operator path (atomic CSV rewrite, dated note prefix `I49-QUARANTINE`). Dossier Section 4 surfaces quarantine count + sample ids; metrics row includes `quarantined_scenarios_count` for trend continuity. SOP-MADEIRA_SCENARIO_LIFECYCLE_001 §5.2 anchors the operator policy.
- **2026-05-03 (D-IH-49-E execution)** — `--filter madeira` saved profile shipped on `scripts/render_uat_dossier.py`; `DossierFilter` extended with `flavor` + `skill_id`; `Section01ExecutiveSummaryMadeira` swaps in for the three-light verdict while preserving the legacy 12-section table (D-IH-48-D order intact). Persona/initiative roster + replay skill carried via `akos/dossier/madeira_preset.py`. CLI helper `single_persona_for_cli` ensures a CSV roster does not break `eval.py --persona` exact-match matching.
