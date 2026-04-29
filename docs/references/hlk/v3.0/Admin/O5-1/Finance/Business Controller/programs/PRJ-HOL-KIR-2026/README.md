# Program — `PRJ-HOL-KIR-2026` (Finance / Business Controller chain)

**Owner role**: Business Controller (CFO chain)  
**Program registry**: [`PROGRAM_REGISTRY.csv`](../../../../../../../compliance/dimensions/PROGRAM_REGISTRY.csv) → `PRJ-HOL-KIR-2026`.  
**Scope**: All Finance casework specifically scoped to KiRBe SaaS billing activation and revenue reconciliation.

This folder is the **program-scoped landing point** for Finance casework on KiRBe SaaS billing. KiRBe's product plane (`kirbe.*` Postgres schema) is routed via `metadata.hlk_billing_plane` through `stripe-webhook-handler` (per [`akos-holistika-operations.mdc`](../../../../../../../../../.cursor/rules/akos-holistika-operations.mdc) §"Schema responsibilities (DAMA)") — distinct from `holistika_ops.*` company-plane billing.

> **Process-list anchors** — `thi_finan_dtp_261 KiRBe Stripe Billing Activation and Reconciliation`. Stripe API is authoritative; vault casework here is the operational reconciliation layer per Initiative 18 D-FIN-1.

## Casework scope (incoming)

- KiRBe subscription lifecycle reconciliation against Stripe FDW reads.
- Counterparty enrichment for KiRBe customers (joins to `FINOPS_COUNTERPARTY_REGISTER.csv`).
- SaaS metric reporting (MRR / ARR / churn) for KiRBe vs Holistika company plane.

## Cross-references

- Tech KiRBe folder: [`Admin/O5-1/Tech/System Owner/programs/PRJ-HOL-KIR-2026/`](../../../../Tech/System%20Owner/programs/PRJ-HOL-KIR-2026/README.md)
- PMO KiRBe folder: [`Admin/O5-1/Operations/PMO/programs/PRJ-HOL-KIR-2026/`](../../../../Operations/PMO/programs/PRJ-HOL-KIR-2026/README.md)
- FINOPS counterparty register: [`docs/references/hlk/compliance/FINOPS_COUNTERPARTY_REGISTER.csv`](../../../../../../../compliance/FINOPS_COUNTERPARTY_REGISTER.csv)
- Initiative 23 master roadmap: [`docs/wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md`](../../../../../../../../wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md)
