---
status: complete
classification: working
access_level: 5
language: en
register: internal
phase: P3c
phase_name: SUEZ application — scope.yaml + commercial-schedule.md (variants A/B/C + Mermaid Gantt)
recorded_at: 2026-05-10
---

# P3c — SUEZ application self-checkpoint

## Files authored

| File | Purpose |
|:---|:---|
| `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/scope-a.yaml` | Variant A scope (CDC + faisabilité only). 8 packages. |
| `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/scope-b.yaml` | Variant B scope (recommended; + Phase 1 POC + design workshop + training). 11 packages. |
| `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/scope-c.yaml` | Variant C scope (full operationalisation; + webapp + 2nd training wave + extended docs). 14 packages. |
| `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/scope.yaml` | Canonical = Variant B (recommended) with WP-NN package ids. |
| `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/commercial-schedule-a.md` | CLI-rendered Variant A schedule (math table + Gantt). |
| `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/commercial-schedule-b.md` | CLI-rendered Variant B schedule. |
| `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/commercial-schedule-c.md` | CLI-rendered Variant C schedule. |
| `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/commercial-schedule.md` | Hand-authored consolidated dossier — variant comparison + Variant B detail + multipliers + margin posture + sanity-check appendix + operator review checklist + cross-references. |

## Outputs (all variants priced in EUR; FR locale uplift active in COUNTRY_WORK_CALENDAR)

| Variant | Effort h (par) | Cost € (par) | Cost € (PERT-expected) | Duration days (par) |
|:---|---:|---:|---:|---:|
| A — CDC + faisabilité | 274 | 38,652 | 42,504 | 39 |
| B — recommended | 390 | **53,611** | **58,934** | 56 |
| C — full operationalisation | 670 | 87,059 | 95,333 | 96 |

The progression A → B → C is strictly monotonic; the multiplier stack is identical across variants (× 1.822 for discovery/design/build, × 1.584 for transfer/close), so the comparison reflects effort delta only — clean methodology.

## Multipliers stacked

* `enterprise_premium` × 1.20 — counterparty enterprise procurement chain.
* `bridge_entity` × 1.10 — collaboration partner bridge.
* `locale_uplift_fr` × 1.20 — FR market vs Madrid SME baseline.
* `first_of_kind` × 1.15 — first engagement of this archetype (discovery + design + build only).

Stack on discovery/design/build packages: 1.822 ×.
Stack on transfer + close packages: 1.584 × (no `first_of_kind` once novelty leaves).

## Verification

```
py -m pytest tests/test_engagement_estimation.py tests/test_estimation_constants_match_sop.py -v
==> 39 passed
   - 35 test_engagement_estimation cases (was 33 passed + 2 skipped at end of P3a; SUEZ smoke + canonical CSV smoke now pass).
   - 4 test_estimation_constants_match_sop cases (SOP §3 / §5 ↔ Python registries drift safeguard).

py scripts/estimate_engagement.py --scope <scope-a.yaml>  --out <commercial-schedule-a.md>  ==> ok
py scripts/estimate_engagement.py --scope <scope-b.yaml>  --out <commercial-schedule-b.md>  ==> ok
py scripts/estimate_engagement.py --scope <scope-c.yaml>  --out <commercial-schedule-c.md>  ==> ok
py scripts/estimate_engagement.py --scope <scope.yaml>    --out <commercial-schedule-canonical-cli.md>  ==> ok
```

The CLI is deterministic — re-running on any scope file regenerates the per-variant schedule byte-identical to the committed copy. The hand-authored `commercial-schedule.md` is the dossier-grade roll-up; the CLI-rendered `commercial-schedule-b.md` mirrors §3 of the consolidated document and is preserved as the auto-generated reference.

## Design notes

* **Brand Manager exclusion held** — none of the 11 (Variant B) / 8 (A) / 14 (C) packages assigns a Brand Manager. Brand-voice work distributes to Holistik Researcher (FR translation, register), Project Manager (operational manual structure), founder + bridge (strategy). The SOP body (`SOP-ENG_ESTIMATION_DISCIPLINE_001` §4) keeps Brand Manager as a Senior Operational tier role with a populated rate (60 / 80 / 100 EUR/h) — the role is canon, this engagement just doesn't activate it.
* **All client-identifiable strings absent** — `rg` for the bridge-collaborator real name + GDF / SUEZ / ENGIE + competitor organisation + competitor internal cost-model identifier returns 0 hits across the four scope files and the four commercial-schedule files (counterparty referenced as "Counterparty enterprise (FR)" + "the bridge" + "the collaboration partner").
* **Mermaid Gantt** — every variant emits a deterministic Mermaid block. The consolidated `commercial-schedule.md` carries a section-grouped Gantt (Discovery / Design / Build / Transfer + close) for proposal-facing visual rhythm; the CLI-rendered siblings carry a flat one-section Gantt for byte-identical reproducibility.
* **Margin posture** — captured at three tiers in the consolidated doc: cost-of-effort floor, target (35 % gross), cap (50 % gross internal-only). The proposal exposes a tightened fork; the cap never leaves the engagement folder.
* **Sanity-check anecdotes appendix** — lawyers/RCD parallel and the off-repo competitive distillation logged as cross-checks; neither pulls the math.

## Next

P4 — CDC feasibility shape (FR, centerpiece). 6–12 pages of point-by-point fonctionnalités sourced from the mode opératoire extract, structured per Faycal's guidance ("L'utilisateur clique sur X, le formulaire Y se déclenche, ces données sont envoyées à l'application Z, qui doit retourner W"); each functionality flagged actionnable / nécessite accès application X / manuel uniquement (opérationnel).
