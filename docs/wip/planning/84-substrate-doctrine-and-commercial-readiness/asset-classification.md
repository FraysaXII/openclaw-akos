# I84 — Asset classification

> Per [`PRECEDENCE.md`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) classes. Each row classifies one asset I84 mints / modifies / references.

## Canonical (edit here first)

| Asset | Path | Class rationale | Mint phase |
|:---|:---|:---|:---:|
| `SUBSTRATE_REGISTRY.csv` | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv` | New dimensional canonical sibling to SKILL_REGISTRY / PEOPLE_DESIGN_PATTERN_REGISTRY / etc. Pydantic SSOT + validator + mirror per [`akos-holistika-operations.mdc`](../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers". | **P2** |
| `SUBSTRATE_LANDSCAPE_DOCTRINE.md` | `docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md` | New Research-area doctrine; pairs with AGENTIC_FRAMEWORK_LANDSCAPE.md (Tech-Lab) the way HOLISTIKA_AGENTIC_DOCTRINE (People) pairs with AGENTIC_FRAMEWORK_LANDSCAPE (Tech-Lab). Applies discipline-of-disciplines pattern recursively to Research-area. | **P6** |
| `SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md` | `docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md` | New SOP at `status: review` per SOP-META order (process_list row mint deferred to I60). Paired runbook per [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1. | **P6** |
| `AGENTIC_FRAMEWORK_LANDSCAPE.md` | `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md` | Existing canonical; **modified** at P3 — §1 extended (5 new framework rows + OpenClaw retrospective); §2 extended (4 → 5 KB infrastructure dimensions); §3 extended (MCP postures matrix); new §7 OpenClaw / LlamaIndex / Cursor SDK retrospective. | **P3** |
| `HOLISTIKA_AGENTIC_DOCTRINE.md` | `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md` | Existing People canonical; **modified** at P3 — adds cross-reference hyperlinks to Substrate Doctrine + extended Tech-Lab landscape. **NO jargon leakage** per Rule 4 anti-jargon mandate. | **P3** |
| `PRECEDENCE.md` | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md` | Existing canonical; **modified** at P2 to register SUBSTRATE_REGISTRY.csv + its mirror. | **P2** |

## Mirrored / derived (resync from canonical)

| Asset | Path | Class rationale | Mint phase |
|:---|:---|:---|:---:|
| `compliance.substrate_registry_mirror` | `supabase/migrations/<YYYYMMDDHHMMSS>_i84_substrate_registry_mirror.sql` (DDL) + `scripts/sync_compliance_mirrors_from_csv.py` emit function | Postgres mirror of SUBSTRATE_REGISTRY.csv via standard sync chain. RLS deny anon / authenticated; service_role for sync jobs per [`akos-holistika-operations.mdc`](../../../.cursor/rules/akos-holistika-operations.mdc) §"Schema responsibilities". | **P2** |
| `akos/hlk_substrate_registry_csv.py` | `akos/hlk_substrate_registry_csv.py` | Pydantic SSOT — derived from CSV column shape via fieldnames tuple. Single-source for column structure consumed by validator + sync + tests. | **P2** |
| Future KiRBe / Neo4j projections of substrate landscape | (not in I84 scope) | If cross-program-substrate-graph proves useful, project into Neo4j per [`i07-hlk-neo4j-graph-projection`](../07-hlk-neo4j-graph-projection/master-roadmap.md) pattern. Out-of-scope for I84; potential I85 follow-on. | (deferred) |

## Reference-only (not canonical; not edited as current truth)

| Asset | Path | Class rationale | Mint phase |
|:---|:---|:---|:---:|
| P1 substrate-audit dossier (4 threads + synthesis) | `docs/wip/intelligence/substrate-audit-2026-Q2/` | Tier-1 WIP per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §17 (Research owns Tier-1). Not canonical until WIP-to-canonical promotion via [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md). | **P1** |
| P3 §7 OpenClaw / LlamaIndex / Cursor SDK retrospective | embedded in `AGENTIC_FRAMEWORK_LANDSCAPE.md` §7 | Historical narrative; cited via `LOGIC_CHANGE_LOG.md` rows to anchor in minted decisions (not free agent narrative). The §7 itself becomes canonical at P3.5 ratification. | **P3** |
| P1.5 + P3.5 + P4 + P6 inline-ratify records | embedded in agent transcript + reports under `docs/wip/planning/84-.../reports/` | Inline-ratify records are not canonical CSV mutations; they live as evidence under the planning folder + cascade into DECISION_REGISTER.csv rows at gate close. | **P1.5 / P3.5 / P4 / P6** |
| Initiative-meta plan artefacts | `docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/{master-roadmap,decision-log,risk-register,asset-classification,evidence-matrix,files-modified}.md/.csv` | Planning-meta per [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc); planning artefacts not canonical SSOT for HLK operations. | **P0** |

## Cross-area artefact-classification implications

- **Tech-Lab side** carries the framework jargon (AGENTIC_FRAMEWORK_LANDSCAPE row additions; SUBSTRATE_REGISTRY column shape with framework-name vendors).
- **People-side** stays jargon-free (HOLISTIKA_AGENTIC_DOCTRINE cross-references via hyperlink only; no inline framework names).
- **Research-area** sits between the two — SUBSTRATE_LANDSCAPE_DOCTRINE.md uses substrate-vocabulary (the meta-discipline that names which substrates earn canonical-status) but does NOT use Tech-Lab implementation jargon (e.g. names "Cursor SDK" but not "the Composer 2 model built on Moonshot Kimi 2.5").
- **Marketing-area** consumes the doctrine via brand-baseline-reality dual-register translation per [`akos-brand-baseline-reality.mdc`](../../../.cursor/rules/akos-brand-baseline-reality.mdc) when substrate-evidence flows into customer-facing positioning prose.
