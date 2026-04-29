# Program — `PRJ-HOL-KIR-2026` (Tech / System Owner chain)

**Owner role**: System Owner (CTO chain)  
**Program registry**: [`PROGRAM_REGISTRY.csv`](../../../../../../../compliance/dimensions/PROGRAM_REGISTRY.csv) → `PRJ-HOL-KIR-2026` (program_code `KIR`, default plane `techops`).  
**Scope**: All Tech/System-Owner-chain casework specifically scoped to the KiRBe SaaS platform program.  
**Forward layout convention**: [`docs/references/hlk/compliance/README.md`](../../../../../../../compliance/README.md) (Initiative 22 P1).

This folder is the **program-scoped landing point** for Tech/System-Owner casework on Holistika's KiRBe platform program (Initiative 23 P6). KiRBe is **dual-natured** (D-IH-16): it is BOTH a SaaS product (`kirbe.*` Postgres schema, Stripe billing per `metadata.hlk_billing_plane`, telemetry `kirbe.monitoring_logs`) AND a vault KM ingestion source (`v3.0/index.md`). New KiRBe engineering casework lands here; existing KiRBe SOPs at the System Owner root remain in place and are linked from this folder.

> **Process-list anchors** — `env_tech_prj_2 KiRBe Platform`, `env_tech_ws_k1 KiRBe Security and Governance`, plus the multiple `SOP-KIRBE_*` files under [`Admin/O5-1/Tech/System Owner/`](../..). Every KiRBe casework doc cites at least one of these.

## See also (KiRBe-scoped Tech docs)

- [`SOP-KIRBE_ENVOYTECH_SHOWCASE_003.md`](../../SOP-KIRBE_ENVOYTECH_SHOWCASE_003.md) — KiRBe Envoy Tech showcase architecture.
- Other `SOP-KIRBE_*` files under the System Owner root (LLM management, node management, parser/postprocessors, traceability/observability, etc.).

## Cross-references

- KM Topic asset: [`_assets/techops/PRJ-HOL-KIR-2026/topic_kirbe_billing_plane_routing/topic_kirbe_billing_plane_routing.manifest.md`](../../../../../../../_assets/techops/PRJ-HOL-KIR-2026/topic_kirbe_billing_plane_routing/topic_kirbe_billing_plane_routing.manifest.md)
- Data governance KiRBe folder: [`Admin/O5-1/Data/Governance/programs/PRJ-HOL-KIR-2026/`](../../../../Data/Governance/programs/PRJ-HOL-KIR-2026/README.md)
- Data architecture KiRBe folder: [`Admin/O5-1/Data/Architecture/programs/PRJ-HOL-KIR-2026/`](../../../../Data/Architecture/programs/PRJ-HOL-KIR-2026/README.md)
- Finance KiRBe folder: [`Admin/O5-1/Finance/Business Controller/programs/PRJ-HOL-KIR-2026/`](../../../../Finance/Business%20Controller/programs/PRJ-HOL-KIR-2026/README.md)
- PMO KiRBe folder: [`Admin/O5-1/Operations/PMO/programs/PRJ-HOL-KIR-2026/`](../../../../Operations/PMO/programs/PRJ-HOL-KIR-2026/README.md)
- Initiative 23 master roadmap: [`docs/wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md`](../../../../../../../../wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md)
