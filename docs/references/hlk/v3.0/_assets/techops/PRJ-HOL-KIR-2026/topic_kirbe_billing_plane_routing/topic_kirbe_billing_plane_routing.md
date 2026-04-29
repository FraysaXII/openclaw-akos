# Topic: KiRBe billing-plane routing (`PRJ-HOL-KIR-2026`)

**source_id**: `topic_kirbe_billing_plane_routing`  
**topic_id**: `topic_kirbe_billing_plane_routing`  
**program_id**: `PRJ-HOL-KIR-2026`  
**plane**: `techops`  
**primary_owner_role**: System Owner (CTO chain)  
**access_level**: 2 (Internal Use)  
**output_type**: 2 (text — companion to `topic_kirbe_billing_plane_routing.manifest.md`)

## Scope

How Stripe webhook payloads route between the KiRBe product plane (`kirbe.*` schema) and the Holistika company plane (`holistika_ops.*` schema), and how downstream counterparty enrichment joins through `FINOPS_COUNTERPARTY_REGISTER.csv`. First non-founder Topic asset under the Initiative 22 P2 plane × program × topic layout — validates the convention at N=2.

## Facts

- **F-K-001** — Stripe webhooks carry `metadata.hlk_billing_plane` ∈ {`kirbe`, `holistika_ops`}; the `stripe-webhook-handler` Edge Function routes accordingly. Source: [`akos-holistika-operations.mdc`](../../../../../../.cursor/rules/akos-holistika-operations.mdc) §"Schema responsibilities (DAMA)".
- **F-K-002** — KiRBe subscription state lives in `kirbe.*` (product plane); ops/billing state lives in `holistika_ops.*` (company plane). The two are intentionally distinct — KiRBe is a SaaS product, not a Holistika operating account.
- **F-K-003** — Counterparty enrichment for KiRBe customers joins through `holistika_ops.stripe_customer_link.finops_counterparty_id` to `FINOPS_COUNTERPARTY_REGISTER.csv` (counterparty_id slug; no relational FK to mirror, per Initiative 18 D-FIN-2).
- **F-K-004** — Cross-program edge: `PRJ-HOL-KIR-2026 :CONSUMES PRJ-HOL-FOUNDING-2026` because KiRBe SaaS billing activation requires the founder-incorporation legal/fiscal foundation to be in place. Source: `PROGRAM_REGISTRY.csv`.
- **F-K-005** — Initiative 23 P-graph projects this CONSUMES edge into Neo4j as `(:Program {program_id: 'PRJ-HOL-KIR-2026'})-[:CONSUMES]->(:Program {program_id: 'PRJ-HOL-FOUNDING-2026'})`.

## Sources

| `source_id` | `output_type` | `location` | Notes |
|:------------|:-------------:|:-----------|:------|
| `S-RULE-OPS-2026` | 2 | `.cursor/rules/akos-holistika-operations.mdc` | Schema responsibilities + dual-plane routing rule |
| `S-CSV-PROGRAM-2026` | 3 | `docs/references/hlk/compliance/dimensions/PROGRAM_REGISTRY.csv` | Program registry; PRJ-HOL-KIR-2026 row |
| `S-CSV-FINOPS-2026` | 3 | `docs/references/hlk/compliance/FINOPS_COUNTERPARTY_REGISTER.csv` | Counterparty register joined via stripe_customer_link |
| `S-PROC-FIN-261` | 3 | `docs/references/hlk/compliance/process_list.csv` (`thi_finan_dtp_261`) | KiRBe Stripe Billing Activation process |
| `S-PROC-TECH-PRJ2` | 3 | `docs/references/hlk/compliance/process_list.csv` (`env_tech_prj_2`) | KiRBe Platform project granularity |
| `S-INI-23` | 2 | `docs/wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md` | Initiative 23 P6 onboarding scope |

## Refresh hooks

- After any change to `metadata.hlk_billing_plane` routing or KiRBe schema split, refresh the Mermaid `.mmd` source and re-render via `py scripts/render_km_diagrams.py … --update-manifest`.
- After any change to `PROGRAM_REGISTRY.csv` `consumes_program_ids` for KIR, update **F-K-004** and re-render.
- Validate via `py scripts/validate_hlk_km_manifests.py` and `py scripts/validate_program_id_consistency.py` before commit.

## Related

- Tech KiRBe folder: [`Admin/O5-1/Tech/System Owner/programs/PRJ-HOL-KIR-2026/README.md`](../../../../Admin/O5-1/Tech/System%20Owner/programs/PRJ-HOL-KIR-2026/README.md)
- Finance KiRBe folder: [`Admin/O5-1/Finance/Business Controller/programs/PRJ-HOL-KIR-2026/README.md`](../../../../Admin/O5-1/Finance/Business%20Controller/programs/PRJ-HOL-KIR-2026/README.md)
- PMO KiRBe folder: [`Admin/O5-1/Operations/PMO/programs/PRJ-HOL-KIR-2026/README.md`](../../../../Admin/O5-1/Operations/PMO/programs/PRJ-HOL-KIR-2026/README.md)
- Initiative 23 master roadmap: [`docs/wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md`](../../../../../../wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md)
- KM contract: [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md)
